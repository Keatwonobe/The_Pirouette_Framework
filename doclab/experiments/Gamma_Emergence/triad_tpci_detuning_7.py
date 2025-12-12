# File: triad_tpci_detuning_7_parallel.py
# This version parallelizes the permutation loop using multiprocessing.

import os, re, json, pathlib, warnings, argparse
import numpy as np
import pandas as pd

import mne
from scipy.signal import butter, filtfilt, hilbert, welch
from scipy.optimize import curve_fit

# <--- NEW: Imports for parallel processing ---
import multiprocessing
from functools import partial
# ---

# (Paste all your helper functions like read_raw_any, select_stim_rows, etc. here)
# ...
def read_raw_any(eeg_path):
    p = str(eeg_path)
    if p.lower().endswith(".bdf"):
        return mne.io.read_raw_bdf(p, preload=True, verbose=False)
    if p.lower().endswith(".set"):
        return mne.io.read_raw_eeglab(p, preload=True, verbose=False)
    if p.lower().endswith(".edf"):
        return mne.io.read_raw_edf(p, preload=True, verbose=False)
    raise RuntimeError(f"Unsupported EEG format: {p}")

def read_events_tsv(ev_path):
    df = pd.read_csv(ev_path, sep="\t")
    df.columns = [c.strip() for c in df.columns]
    for req in ["onset", "value"]:
        if req not in df.columns:
            raise RuntimeError(f"events.tsv missing required column '{req}': {ev_path}")
    return df

def select_stim_rows(df, task):
    val = df["value"].astype(str).str.lower()
    if task.lower() == "nb":
        stim = val.str.startswith("letter_")
        stim &= ~val.str.contains("response")
        return stim
    if task.lower() == "sart":
        stim = val.isin(["target", "non_target"])
        return stim
    if task.lower() == "lg":
        stim = val.str.contains(r"(?:large|small)_", regex=True)
        stim &= ~val.str.contains("response")
        stim &= ~val.str.contains("ignore")
        return stim
    stim = ~val.str.contains("response") & ~val.str.contains("ignore")
    return stim

def bandpass_phase(ep, fs, f_lo, f_hi):
    b, a = butter(4, [f_lo/(fs/2), f_hi/(fs/2)], btype='band')
    z = filtfilt(b, a, ep, axis=-1)
    return np.angle(hilbert(z, axis=-1))

def tpci(phi1, phi2, phi3):
    z = np.exp(1j*(phi3 - phi1 - phi2))
    return np.abs(np.mean(np.mean(z, axis=-1), axis=1))

def gauss(x, A, mu, sig, B):
    return A * np.exp(-(x-mu)**2/(2*sig**2)) + B

def halfwidth_gauss(x, y):
    try:
        mu0 = x[int(np.argmax(y))]
        A0 = float(np.max(y) - np.median(y))
        B0 = float(np.median(y))
        sig0 = 0.25
        popt, _ = curve_fit(gauss, x, y, p0=(A0, mu0, sig0, B0), maxfev=5000)
        A, mu, sig, B = popt
        return float(np.sqrt(2*np.log(2))*abs(sig)), dict(A=A, mu=mu, sig=sig, B=B)
    except Exception:
        return np.nan, None

def band_power(ep, fs, f_lo, f_hi):
    n_ep, n_ch, n_t = ep.shape
    pw = []
    for i in range(n_ep):
        p_list = []
        for c in range(n_ch):
            f, Pxx = welch(ep[i, c], fs=fs, nperseg=min(1024, n_t))
            m = (f >= f_lo) & (f <= f_hi)
            p_list.append(np.trapezoid(Pxx[m], f[m]))
        pw.append(np.mean(p_list))
    return np.array(pw)

def phase_shuffle(phi, rng):
    ep, ch, T = phi.shape
    out = np.empty_like(phi)
    for i in range(ep):
        shift = rng.integers(0, T)
        out[i] = np.roll(phi[i], shift, axis=-1)
    return out
# ...

# <--- NEW: Top-level worker function for parallel permutations ---
# This function MUST be at the top level so it can be 'pickled'
def run_one_permutation(perm_index, phi1, phi2, phi3_list, detune, base_seed):
    """
    Runs a single permutation.
    'perm_index' is the only thing that changes. The rest are large,
    constant arrays passed via functools.partial.
    """
    # 1. Create a NEW RNG for this specific worker to avoid collisions
    # We use the base_seed and the permutation index to guarantee a unique state
    rng = np.random.default_rng(base_seed + perm_index)
    
    # 2. Shuffle phi2
    phi2_null = phase_shuffle(phi2, rng)
    
    # 3. Calculate the null curve (this is the expensive part)
    cnull = []
    for phi3 in phi3_list: 
        v = tpci(phi1, phi2_null, phi3)
        cnull.append(np.mean(v))
    
    # 4. Fit the curve and return the bandwidth
    bw_n, _ = halfwidth_gauss(detune, cnull)
    
    return bw_n
# ---


def process_file(eeg_path, ev_path, out_dir, args):
    raw = read_raw_any(eeg_path)
    if args.roi:
        picks = [c for c in raw.ch_names if any(r.lower() in c.lower() for r in args.roi)]
        if not picks:
            warnings.warn(f"No ROI channels found in {eeg_path}; using all channels.")
        else:
            raw.pick_channels(picks)

    raw.filter(args.highpass, args.lowpass, fir_design='firwin', verbose=False)
    sf = raw.info["sfreq"]

    ev = read_events_tsv(ev_path)
    task_match = re.search(r"task-([A-Za-z0-9]+)", str(eeg_path))
    task = task_match.group(1) if task_match else "UNK"

    stim_mask = select_stim_rows(ev, task)
    ev_stim = ev.loc[stim_mask].copy()
    if ev_stim.empty:
        warnings.warn(f"No stimuli selected for {eeg_path}")
        return False

    onsets = ev_stim["onset"].to_numpy(float)
    events = np.c_[(onsets*sf).astype(int), np.zeros_like(onsets, int), np.ones_like(onsets, int)]
    
    epochs = mne.Epochs(raw, events, event_id=dict(stim=1),
                        tmin=args.tmin, tmax=args.tmax,
                        baseline=None, preload=False, verbose=False) 
    
    if len(events) < args.min_epochs: 
        warnings.warn(f"Too few events ({len(events)}) to create epochs: {eeg_path}")
        return False

    loads, how = None, None
    if args.load_col and args.load_col in ev.columns:
        loads_all = pd.to_numeric(ev[args.load_col], errors="coerce")
        loads = loads_all.loc[stim_mask].ffill().bfill().to_numpy()
        uniq = pd.unique(loads[~pd.isna(loads)])
        if len(uniq) >= 2:
            loads = loads.astype(int)
            how = f"explicit:{args.load_col}"
        else:
            loads = None
    
    if loads is None:
        print("  -> Calculating proxy load (beta band power) epoch-by-epoch...")
        bp = []
        for ep_data in epochs:
            ep_data_batch = ep_data[np.newaxis, :, :] 
            power_val = band_power(ep_data_batch, sf, 15.0, 30.0) 
            bp.append(power_val[0])
        
        bp = np.array(bp)
        q = pd.qcut(pd.Series(bp).rank(method="first"), args.quantiles, labels=False, duplicates="drop")
        loads = (q + 1).to_numpy()
        how = f"proxy:beta_q{args.quantiles}"

    triads_in = []
    for tri in args.triad:
        f1, f2 = map(float, tri.split(","))
        triads_in.append((f1, f2, f1+f2))
    detune = np.linspace(-args.detune, args.detune, 2*int(args.detune*args.pph)+1)

    processed_something = False 

    for (f1, f2, f3_nom) in triads_in:
        for L in sorted(np.unique(loads)):
            triad_tuple = (f1, f2, f3_nom)
            
            triad_str = f"{f1}-{f2}-{f3_nom}".replace('.', 'p') 
            out_path_combo = out_dir / f"triad-{triad_str}_load-{L}.json"
            
            if out_path_combo.exists() and not args.overwrite:
                print(f"  -> Skipping completed triad {triad_tuple} at load {L} (file exists)")
                continue
            
            print(f"  -> Processing triad {triad_tuple} at load {L}...")
            
            idx = np.where(loads == L)[0]
            if len(idx) < args.min_epochs: # Use arg
                print(f"     .. skipping load {L} (only {len(idx)} epochs, min is {args.min_epochs})")
                continue
            
            epL = epochs[idx].get_data(verbose=False)
            
            phi1 = bandpass_phase(epL, sf, f1-args.band, f1+args.band)
            phi2 = bandpass_phase(epL, sf, f2-args.band, f2+args.band)

            print(f"     ...pre-calculating {len(detune)} phi3 variants...")
            phi3_list = []
            for df in detune:
                f3 = f3_nom + df
                phi3_list.append(bandpass_phase(epL, sf, f3-args.band, f3+args.band))

            curve = []
            for j, phi3 in enumerate(phi3_list): 
                vals = tpci(phi1, phi2, phi3)
                curve.append(np.mean(vals))
            curve = np.array(curve)

            status = "computed"
            # print("Status: Computed") # Your debug line

            bw_half, fitpars, pval = np.nan, None, None
            if np.ptp(curve) > args.precheck_threshold:
                bw_half, fitpars = halfwidth_gauss(detune, curve)

                # <--- NEW: This entire block is replaced with a parallel Pool ---
                
                # 1. "Partially" fill the worker function with the large, constant data
                worker_func = partial(run_one_permutation,
                                      phi1=phi1,
                                      phi2=phi2,
                                      phi3_list=phi3_list,
                                      detune=detune,
                                      base_seed=args.seed)
                
                # 2. Set up the Pool
                # We use (cpu_count - 1) to leave one core free for the OS
                n_cpus = max(1, multiprocessing.cpu_count() - 1)
                print(f"     ...starting {args.perm} permutations on {n_cpus} CPUs...")
                
                null_bw = []
                # 3. Run the tasks and collect results
                # We must use the 'if __name__ == "__main__":' guard in the main()
                # function for this to work, which we already do.
                with multiprocessing.Pool(processes=n_cpus) as pool:
                    # Create a list of the tasks to run (just the index)
                    perm_indices = range(args.perm)
                    
                    # Use pool.imap() to get results as they complete
                    # This lets us print progress
                    for i, bw_n in enumerate(pool.imap(worker_func, perm_indices)):
                        if np.isfinite(bw_n):
                            null_bw.append(bw_n)
                        if (i+1) % 50 == 0 or (i+1) == args.perm:
                            print(f"     ...permutation {i+1}/{args.perm} complete...")

                # --- End of new parallel block ---

                if np.isfinite(bw_half) and len(null_bw) > 9:
                    pval = float(np.mean(np.array(null_bw) >= bw_half))
            else:
                status = f"skipped_precheck_ptp_{np.ptp(curve):.4f}"

            sub_match = re.search(r"sub-([0-9A-Za-z]+)", str(eeg_path))
            ses_match = re.search(r"ses-([0-9A-Za-z]+)", str(eeg_path))
            
            result_dict = dict(
                file=str(eeg_path.name),
                subject=sub_match.group(1) if sub_match else "NA",
                session=ses_match.group(1) if ses_match else "NA",
                task=task,
                triad=list(triad_tuple),
                status=status,
                detune=detune.tolist(),
                tpci_curve=curve.tolist(),
                bandwidth_half=None if not np.isfinite(bw_half) else float(bw_half),
                gauss_fit=fitpars,
                load=int(L),
                load_method=how,
                p_bw_ge_null=pval
            )

            with open(out_path_combo, "w") as f:
                json.dump(result_dict, f, indent=2)
            
            processed_something = True 

    return processed_something

def main():
    ap = argparse.ArgumentParser()
    # (All argparse arguments remain identical)
    ap.add_argument("--eeg-path", required=True, help="Path to the EEG file (.bdf, .set, .edf)")
    ap.add_argument("--events-path", required=True, help="Path to the corresponding events.tsv file")
    ap.add_argument("--outdir", required=True, help="Base output directory for results")
    ap.add_argument("--min-epochs", type=int, default=8, help="Minimum epochs per load/triad to compute TPCI (default 8)")
    ap.add_argument("--roi", nargs="*", default=None, help="ROI channels (e.g., O1 O2 Oz POz)")
    ap.add_argument("--load-col", default=None, help="Explicit events.tsv column to use as load")
    ap.add_argument("--quantiles", type=int, default=4, help="Quantiles for proxy load (default 4)")
    ap.add_argument("--tmin", type=float, default=0.0)
    ap.add_argument("--tmax", type=float, default=4.0)
    ap.add_argument("--highpass", type=float, default=0.5)
    ap.add_argument("--lowpass", type=float, default=80.0)
    ap.add_argument("--band", type=float, default=1.0, help="+/- Hz for bandpass around f1,f2,f3")
    ap.add_argument("--detune", type=float, default=2.0, help="+/- detune (Hz)")
    ap.add_argument("--pph", type=int, default=10, help="points per Hz in detune sweep")
    ap.add_argument("--perm", type=int, default=200, help="Phase-shuffle permutations")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--triad", nargs="+", default=["8,12","10,20"], help='Triads "f1,f2" (f3=f1+f2)')
    ap.add_argument("--overwrite", action="store_true", help="Overwrite existing output files.")
    ap.add_argument("--precheck-threshold", type=float, default=0.02, help="Threshold for peak-to-peak TPCI curve to trigger full analysis.")
    args = ap.parse_args()

    eeg_path = pathlib.Path(args.eeg_path)
    ev_path = pathlib.Path(args.events_path)
    outdir_base = pathlib.Path(args.outdir)
    
    sub_match = re.search(r"sub-([0-9A-Za-z]+)", str(eeg_path.name))
    ses_match = re.search(r"ses-([0-9A-Za-z]+)", str(eeg_path.name))
    task_match = re.search(r"task-([A-Za-z0-9]+)", str(eeg_path.name))
    sub = sub_match.group(1) if sub_match else "NA"
    ses = ses_match.group(1) if ses_match else "NA"
    task = task_match.group(1) if task_match else "UNK"
    
    out_dir_for_file = outdir_base / f"sub-{sub}_ses-{ses}_task-{task}_tpci_results"
    out_dir_for_file.mkdir(parents=True, exist_ok=True)
    
    if args.overwrite:
        print(f"i --overwrite enabled. Existing individual result files in {out_dir_for_file.name} will be overwritten.")

    print(f"▶ Processing: {eeg_path.name}...")
    print(f"  Results will be saved in: {out_dir_for_file}")
    try:
        success = process_file(eeg_path, ev_path, out_dir_for_file, args)
        
        if success:
            print(f"  ✓ Finished processing. At least one new result file was saved.")
        else:
            print(f"  ! No new results produced (all combinations may have been skipped or already completed).")

    except Exception as e:
        print(f"  ✗ FAILED {eeg_path.name} -> {e}")
        raise e 

# This 'if' statement is CRITICAL for multiprocessing to work
# correctly on all platforms (especially Windows).
if __name__ == "__main__":
    main()