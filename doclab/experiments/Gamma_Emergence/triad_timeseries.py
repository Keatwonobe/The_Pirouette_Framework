# File: triad_timeseries.py
#
# This is the "Triangulator" Agent. It is not an explorer.
# It takes a *specific triad* (f1, f2, f3) that we discovered
# with the 3-Pass Agent and generates a full time-series of its
# coupling strength across the entire trial.
#
# This allows us to "data-map the transient signal expression" and
# see the "moving shape" of the resonance.

import os, re, json, pathlib, warnings, argparse
import numpy as np

# --- Helper Functions (Re-used from previous scripts) ---
# We are moving all heavy imports inside functions to prevent
# multiprocessing errors on Windows.

def read_raw_any(eeg_path):
    import mne
    p = str(eeg_path)
    if p.lower().endswith(".bdf"):
        return mne.io.read_raw_bdf(p, preload=True, verbose=False)
    if p.lower().endswith(".set"):
        return mne.io.read_raw_eeglab(p, preload=True, verbose=False)
    if p.lower().endswith(".edf"):
        return mne.io.read_raw_edf(p, preload=True, verbose=False)
    raise RuntimeError(f"Unsupported EEG format: {p}")

def read_events_tsv(ev_path):
    import pandas as pd
    df = pd.read_csv(ev_path, sep="\t")
    df.columns = [c.strip() for c in df.columns]
    for req in ["onset", "value"]:
        if req not in df.columns:
            raise RuntimeError(f"events.tsv missing required column '{req}': {ev_path}")
    return df

def select_stim_rows(df, task):
    import pandas as pd
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
    from scipy.signal import butter, filtfilt, hilbert
    b, a = butter(4, [f_lo/(fs/2), f_hi/(fs/2)], btype='band')
    z = filtfilt(b, a, ep, axis=-1)
    return np.angle(hilbert(z, axis=-1))

def tpci(phi1, phi2, phi3):
    # (n_epochs, n_chans, n_times)
    z = np.exp(1j*(phi3 - phi1 - phi2))
    # average over time, then over channels
    return np.abs(np.mean(np.mean(z, axis=-1), axis=1))

def band_power(ep, fs, f_lo, f_hi):
    from scipy.signal import welch
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


# --- Main Controller ---

def process_file(eeg_path, ev_path, out_dir, args):
    import mne
    import pandas as pd
    
    # --- 1. Setup: Load Data (same as before) ---
    print(f"▶ Loading & Preprocessing: {eeg_path.name}...")
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
    
    epochs_full = mne.Epochs(raw, events, event_id=dict(stim=1),
                             tmin=args.tmin, tmax=args.tmax,
                             baseline=None, preload=True, verbose=False) # Preload!
    
    if len(events) < args.min_epochs: 
        warnings.warn(f"Too few events ({len(events)}) to create epochs: {eeg_path}")
        return False

    # --- 2. Setup: Get Load Bins (same as before) ---
    print("  -> Calculating load bins...")
    bp = []
    for ep_data in epochs_full.get_data(verbose=False):
        ep_data_batch = ep_data[np.newaxis, :, :] 
        power_val = band_power(ep_data_batch, sf, 15.0, 30.0) 
        bp.append(power_val[0])
    
    bp = np.array(bp)
    q = pd.qcut(pd.Series(bp).rank(method="first"), args.quantiles, labels=False, duplicates="drop")
    loads = (q + 1).to_numpy()
    
    idx_low = np.where(loads == np.min(loads))[0]
    idx_high = np.where(loads == np.max(loads))[0]
    
    if len(idx_low) < args.min_epochs or len(idx_high) < args.min_epochs:
        print(f"  ! Not enough epochs in low/high load bins to proceed.")
        return False
        
    epochs_low = epochs_full[idx_low]
    epochs_high = epochs_full[idx_high]

    # --- 3. The "Flow" Calculation (Sliding Window TPCI) ---
    
    # Get the single triad we are hunting for
    f1, f2 = map(float, args.triad.split(","))
    f3 = f1 + f2
    triad = (f1, f2, f3)
    triad_str = f"{f1:.1f}-{f2:.1f}-{f3:.1f}".replace('.', 'p')
    print(f"  -> [FLOW] Starting Time-Resolved TPCI for Triad ({f1:.1f}, {f2:.1f}, {f3:.1f})...")

    out_path_combo = out_dir / f"timeseries_triad-{triad_str}.json"
    if out_path_combo.exists() and not args.overwrite:
        print(f"     ...skipping, result file exists.")
        return True

    # Get all epoch data
    ep_low_data = epochs_low.get_data(verbose=False)
    ep_high_data = epochs_high.get_data(verbose=False)
    
    # Pre-calculate the phase for the *entire* trial, for all epochs
    # This is the optimization: filter *once*, then slice *many times*
    print("     ...pre-calculating full-trial phase data...")
    phi1_low = bandpass_phase(ep_low_data, sf, f1 - args.band, f1 + args.band)
    phi2_low = bandpass_phase(ep_low_data, sf, f2 - args.band, f2 + args.band)
    phi3_low = bandpass_phase(ep_low_data, sf, f3 - args.band, f3 + args.band)
    
    phi1_high = bandpass_phase(ep_high_data, sf, f1 - args.band, f1 + args.band)
    phi2_high = bandpass_phase(ep_high_data, sf, f2 - args.band, f2 + args.band)
    phi3_high = bandpass_phase(ep_high_data, sf, f3 - args.band, f3 + args.band)

    # --- 4. Define Sliding Window Parameters ---
    total_samples = ep_low_data.shape[2]
    window_size_samp = int(sf * args.window_sec)
    step_size_samp = int(sf * args.step_sec)
    
    if window_size_samp > total_samples:
        print(f"  ! Error: Window size ({args.window_sec}s) is larger than epoch ({total_samples/sf:.2f}s).")
        return False

    t_centers_sec = []
    tpci_low_series = []
    tpci_high_series = []

    print(f"     ...sliding {args.window_sec*1000:.0f}ms window every {args.step_sec*1000:.0f}ms...")
    
    # The sliding window loop
    for t_start_samp in range(0, total_samples - window_size_samp, step_size_samp):
        t_end_samp = t_start_samp + window_size_samp
        
        # Calculate the center time of this window
        t_center_sec = (t_start_samp + window_size_samp / 2) / sf + args.tmin
        
        # --- Slice the pre-calculated phase arrays ---
        phi1_low_w = phi1_low[:, :, t_start_samp:t_end_samp]
        phi2_low_w = phi2_low[:, :, t_start_samp:t_end_samp]
        phi3_low_w = phi3_low[:, :, t_start_samp:t_end_samp]
        
        phi1_high_w = phi1_high[:, :, t_start_samp:t_end_samp]
        phi2_high_w = phi2_high[:, :, t_start_samp:t_end_samp]
        phi3_high_w = phi3_high[:, :, t_start_samp:t_end_samp]
        
        # --- Calculate TPCI for this slice ---
        # tpci() returns (n_epochs,), so we take the mean
        tpci_low = np.mean(tpci(phi1_low_w, phi2_low_w, phi3_low_w))
        tpci_high = np.mean(tpci(phi1_high_w, phi2_high_w, phi3_high_w))
        
        # --- Store the result ---
        t_centers_sec.append(t_center_sec)
        tpci_low_series.append(tpci_low)
        tpci_high_series.append(tpci_high)

    print(f"     ...calculation complete. {len(t_centers_sec)} time points calculated.")

    # --- 5. Save the Time-Series Data ---
    result_dict = dict(
        file=str(eeg_path.name),
        subject="sub",
        session="ses",
        task=task,
        triad=list(triad),
        window_sec=args.window_sec,
        step_sec=args.step_sec,
        n_epochs_low=len(idx_low),
        n_epochs_high=len(idx_high),
        time_points_sec=t_centers_sec,
        tpci_low_load_series=[float(v) for v in tpci_low_series],
        tpci_high_load_series=[float(v) for v in tpci_high_series]
    )

    with open(out_path_combo, "w") as f:
        json.dump(result_dict, f, indent=2)

    print(f"  ✓ Time-series saved to {out_path_combo.name}")
    return True


def main():
    ap = argparse.ArgumentParser(description="Triadic Time-Series 'Triangulator' Agent")
    
    # --- Main Args ---
    ap.add_argument("--eeg-path", required=True, help="Path to the EEG file (.bdf, .set, .edf)")
    ap.add_argument("--events-path", required=True, help="Path to the corresponding events.tsv file")
    ap.add_argument("--outdir", required=True, help="Base output directory for results")
    ap.add_argument("--triad", required=True, help="The *specific* 'f1,f2' triad to analyze (e.g., '5.0,7.0')")
    
    ap.add_argument("--min-epochs", type=int, default=8, help="Minimum epochs per load bin (default 8)")
    ap.add_argument("--roi", nargs="*", default=None, help="ROI channels (e.g., O1 O2 Oz POz)")
    ap.add_argument("--quantiles", type=int, default=4, help="Quantiles for proxy load (default 4)")
    ap.add_argument("--tmin", type=float, default=0.0, help="Full epoch tmin")
    ap.add_argument("--tmax", type=float, default=1.0, help="Full epoch tmax") # Shorter default
    ap.add_argument("--highpass", type=float, default=0.5)
    ap.add_argument("--lowpass", type=float, default=45.0) # Lower lowpass
    ap.add_argument("--band", type=float, default=1.0, help="+/- Hz for bandpass around f1,f2,f3")
    ap.add_argument("--overwrite", action="store_true", help="Overwrite existing output files.")

    # --- Sliding Window Args ---
    ap.add_argument("--window-sec", type=float, default=0.200, help="Width of the sliding window in seconds (default 0.200s)")
    ap.add_argument("--step-sec", type=float, default=0.020, help="Step size of the sliding window in seconds (default 0.020s)")

    args = ap.parse_args()

    # --- Setup Output Directory ---
    eeg_path = pathlib.Path(args.eeg_path)
    ev_path = pathlib.Path(args.events_path)
    outdir_base = pathlib.Path(args.outdir)
    
    sub_match = re.search(r"sub-([0-9A-Za-z]+)", str(eeg_path.name))
    ses_match = re.search(r"ses-([0-9A-Za-z]+)", str(eeg_path.name))
    task_match = re.search(r"task-([A-Za-z0-9]+)", str(eeg_path.name))
    sub = sub_match.group(1) if sub_match else "NA"
    ses = ses_match.group(1) if ses_match else "NA"
    task = task_match.group(1) if task_match else "UNK"
    
    # We create a new subdirectory for these time-series results
    out_dir_for_file = outdir_base / f"sub-{sub}_ses-{ses}_task-{task}_timeseries_results"
    out_dir_for_file.mkdir(parents=True, exist_ok=True)
    
    print(f"▶ Starting Time-Series 'Triangulator' Agent for: {eeg_path.name}...")
    print(f"  Results will be saved in: {out_dir_for_file.name}")
    try:
        process_file(eeg_path, ev_path, out_dir_for_file, args)

    except Exception as e:
        print(f"  ✗ FAILED {eeg_path.name} -> {e}")
        raise e 

if __name__ == "__main__":
    main()