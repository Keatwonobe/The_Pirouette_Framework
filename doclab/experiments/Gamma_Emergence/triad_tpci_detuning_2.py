import os, re, json, pathlib, warnings, argparse
import numpy as np
import pandas as pd

import mne
from scipy.signal import butter, filtfilt, hilbert, welch
from scipy.optimize import curve_fit

# --------------------------
# Helpers
# --------------------------

def read_raw_any(eeg_path):
    p = str(eeg_path)
    if p.lower().endswith(".bdf"):
        return mne.io.read_raw_bdf(p, preload=True, verbose=False)
    if p.lower().endswith(".set"):
        return mne.io.read_raw_eeglab(p, preload=True, verbose=False)
    if p.lower().endswith(".edf"):
        return mne.io.read_raw_edf(p, preload=True, verbose=False)
    raise RuntimeError(f"Unsupported EEG format: {p}")

def find_eeg_and_events(task_dir, subj, ses, task):
    # Prefer EEG in task folder; fallback to session folder
    d = pathlib.Path(task_dir)
    eeg_files = []
    for ext in (".bdf", ".set", ".edf"):
        eeg_files += list(d.glob(f"sub-{subj}_ses-{ses}_task-{task}*{ext}"))
    if not eeg_files:
        # Broad fallback
        for ext in (".bdf", ".set", ".edf"):
            eeg_files += list(d.glob(f"*task-{task}*{ext}"))
    ev_files = list(d.glob(f"sub-{subj}_ses-{ses}_task-{task}_events.tsv"))
    if not ev_files:
        ev_files = list(d.glob(f"*task-{task}*_events.tsv"))
    return (eeg_files[0] if eeg_files else None), (ev_files[0] if ev_files else None)

def read_events_tsv(ev_path):
    df = pd.read_csv(ev_path, sep="\t")
    # normalize column names
    df.columns = [c.strip() for c in df.columns]
    # ensure required cols
    for req in ["onset", "value"]:
        if req not in df.columns:
            raise RuntimeError(f"events.tsv missing required column '{req}': {ev_path}")
    return df

def select_stim_rows(df, task):
    """Return boolean mask for rows to treat as stimuli (exclude responses)."""
    val = df["value"].astype(str).str.lower()
    if task.lower() == "nb":
        # take letters as stimuli; drop explicit 'response'
        stim = val.str.startswith("letter_")
        stim &= ~val.str.contains("response")
        return stim
    if task.lower() == "sart":
        # target / non_target are stimuli; exclude 'response'
        stim = val.isin(["target", "non_target"])
        return stim
    if task.lower() == "lg":
        # large_*_small_* are stimuli; exclude 'response' and 'ignore'
        stim = val.str.contains(r"(?:large|small)_", regex=True)
        stim &= ~val.str.contains("response")
        stim &= ~val.str.contains("ignore")
        return stim
    # default: anything that is not response/ignore
    stim = ~val.str.contains("response") & ~val.str.contains("ignore")
    return stim

def bandpass_phase(ep, fs, f_lo, f_hi):
    b, a = butter(4, [f_lo/(fs/2), f_hi/(fs/2)], btype='band')
    z = filtfilt(b, a, ep, axis=-1)
    return np.angle(hilbert(z, axis=-1))

def tpci(phi1, phi2, phi3):
    z = np.exp(1j*(phi3 - phi1 - phi2))
    # return per-epoch scalar: mean over chans & time
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
        # HW = sqrt(2 ln 2) * sigma
        return float(np.sqrt(2*np.log(2))*abs(sig)), dict(A=A, mu=mu, sig=sig, B=B)
    except Exception:
        return np.nan, None

def band_power(ep, fs, f_lo, f_hi):
    # Welch per epoch, average across channels
    n_ep, n_ch, n_t = ep.shape
    pw = []
    for i in range(n_ep):
        # stack channels -> mean
        p_list = []
        for c in range(n_ch):
            f, Pxx = welch(ep[i, c], fs=fs, nperseg=min(1024, n_t))
            m = (f >= f_lo) & (f <= f_hi)
            p_list.append(np.trapezoid(Pxx[m], f[m]))
        pw.append(np.mean(p_list))
    return np.array(pw)

def phase_shuffle(phi, rng):
    """Circularly shift phase array along time for each epoch/channel."""
    ep, ch, T = phi.shape
    out = np.empty_like(phi)
    for i in range(ep):
        shift = rng.integers(0, T)
        out[i] = np.roll(phi[i], shift, axis=-1)
    return out

# --------------------------
# Main TPCI computation per file
# --------------------------

def process_file(eeg_path, ev_path, args):
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
    task = re.search(r"task-([A-Za-z0-9]+)", str(eeg_path))
    task = task.group(1) if task else "UNK"

    stim_mask = select_stim_rows(ev, task)
    ev_stim = ev.loc[stim_mask].copy()
    if ev_stim.empty:
        warnings.warn(f"No stimuli selected for {eeg_path}")
        return []

    # epochs from onsets
    onsets = ev_stim["onset"].to_numpy(float)
    events = np.c_[(onsets*sf).astype(int), np.zeros_like(onsets, int), np.ones_like(onsets, int)]
    event_id = dict(stim=1)
    epochs = mne.Epochs(raw, events, event_id=event_id,
                        tmin=args.tmin, tmax=args.tmax,
                        baseline=None, preload=True, verbose=False)
    ep = epochs.get_data()  # (n_ep, n_ch, n_t)
    if ep.shape[0] < 8:
        warnings.warn(f"Too few epochs: {eeg_path}")
        return []

    # --------------------------
    # Load labeling
    # --------------------------
    # If explicit column requested and present, use it; else proxy via beta power quartiles
    loads = None
    how = None
    if args.load_col and args.load_col in ev.columns:
        # Align by nearest onset index (events file has more rows than stim)
        # build a series at stim rows
        loads_all = pd.to_numeric(ev[args.load_col], errors="coerce")
        loads = loads_all.loc[stim_mask].ffill().bfill().to_numpy()
        uniq = pd.unique(loads[~pd.isna(loads)])
        if len(uniq) >= 2:
            loads = loads.astype(int)
            how = f"explicit:{args.load_col}"
        else:
            loads = None

    if loads is None:
        # Proxy: beta power 15-30 Hz quantiles => 1..4
        bp = band_power(ep, sf, 15.0, 30.0)
        q = pd.qcut(pd.Series(bp).rank(method="first"), args.quantiles, labels=False, duplicates="drop")
        loads = (q + 1).to_numpy()
        how = f"proxy:beta_q{args.quantiles}"

    # --------------------------
    # TPCI detuning per load
    # --------------------------
    triads = []
    # Subject-specific IAF optional: here we keep fixed bands unless requested
    triads_in = []
    for tri in args.triad:
        f1, f2 = map(float, tri.split(","))
        triads_in.append((f1, f2, f1+f2))
    detune = np.linspace(-args.detune, args.detune, 2*int(args.detune*args.pph)+1)  # pph=points per Hz

    out_rows = []
    for (f1, f2, f3_nom) in triads_in:
        for L in sorted(np.unique(loads)):
            idx = np.where(loads == L)[0]
            if len(idx) < 5:
                continue
            epL = ep[idx]
            # Pre-compute phases for f1,f2 once
            phi1 = bandpass_phase(epL, sf, f1-args.band, f1+args.band)
            phi2 = bandpass_phase(epL, sf, f2-args.band, f2+args.band)

            curve = []
            for df in detune:
                f3 = f3_nom + df
                phi3 = bandpass_phase(epL, sf, f3-args.band, f3+args.band)
                vals = tpci(phi1, phi2, phi3)
                curve.append(np.mean(vals))
            curve = np.array(curve)
            bw_half, fitpars = halfwidth_gauss(detune, curve)

            # Phase-shuffle null (p-value)
            rng = np.random.default_rng(args.seed)
            null_bw = []
            Nperm = args.perm
            for _ in range(Nperm):
                phi2_null = phase_shuffle(phi2, rng)
                cnull = []
                for df in detune:
                    f3 = f3_nom + df
                    phi3 = bandpass_phase(epL, sf, f3-args.band, f3+args.band)
                    v = tpci(phi1, phi2_null, phi3)
                    cnull.append(np.mean(v))
                cnull = np.array(cnull)
                bw_n, _ = halfwidth_gauss(detune, cnull)
                if np.isfinite(bw_n):
                    null_bw.append(bw_n)
            null_bw = np.array(null_bw)
            pval = float(np.mean(null_bw >= bw_half)) if (np.isfinite(bw_half) and len(null_bw)>9) else None

            out_rows.append(dict(
                file=str(eeg_path),
                events=str(ev_path),
                subject=re.search(r"sub-([0-9A-Za-z]+)", str(eeg_path)).group(1) if re.search(r"sub-([0-9A-Za-z]+)", str(eeg_path)) else "NA",
                session=re.search(r"ses-([0-9A-Za-z]+)", str(eeg_path)).group(1) if re.search(r"ses-([0-9A-Za-z]+)", str(eeg_path)) else "NA",
                task=task,
                triad=(f1, f2, f3_nom),
                detune=detune.tolist(),
                tpci_curve=curve.tolist(),
                bandwidth_half=None if not np.isfinite(bw_half) else float(bw_half),
                gauss_fit=fitpars,
                load=int(L),
                load_method=how,
                p_bw_ge_null=pval
            ))
    return out_rows

# --------------------------
# Directory walker
# --------------------------

def walk_dataset(root):
    rootp = pathlib.Path(root)
    # expect sub-*/ses-*/eeg dir
    entries = []
    for subdir in rootp.glob("sub-*"):
        subj = subdir.name.split("-")[-1]
        for sesdir in subdir.glob("ses-*"):
            ses = sesdir.name.split("-")[-1]
            eegdir = sesdir / "eeg"
            if not eegdir.exists():
                continue
            # tasks present (parse from events filenames)
            tasks = set()
            for ev in eegdir.glob("*_events.tsv"):
                m = re.search(r"task-([A-Za-z0-9]+)", ev.name)
                if m:
                    tasks.add(m.group(1))
            for task in sorted(tasks):
                eeg_path, ev_path = find_eeg_and_events(eegdir, subj, ses, task)
                if ev_path and eeg_path:
                    entries.append((eeg_path, ev_path))
    return entries

# --------------------------
# CLI
# --------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="Root of Executive_Functioning_Data")
    ap.add_argument("--outdir", default=None, help="Output directory for JSON")
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
    args = ap.parse_args()

    entries = walk_dataset(args.root)
    if not entries:
        raise RuntimeError("No (EEG, events.tsv) pairs found.")

    all_rows = []
    for eeg_path, ev_path in entries:
        try:
            rows = process_file(eeg_path, ev_path, args)
            all_rows.extend(rows)
            print(f"✓ {eeg_path.name}: {len(rows)} triad×load results")
        except Exception as e:
            warnings.warn(f"Failed {eeg_path} -> {e}")

    if not all_rows:
        print("No results produced.")
        return

    outdir = pathlib.Path(args.outdir or (pathlib.Path(args.root)/"derivatives"/"pirouette_gamma"))
    outdir.mkdir(parents=True, exist_ok=True)
    # Save per-subject and summary
    by_sub = {}
    for r in all_rows:
        by_sub.setdefault(r["subject"], []).append(r)
    for sub, rows in by_sub.items():
        with open(outdir/f"tpci_detuning_sub-{sub}.json","w") as f:
            json.dump(rows, f, indent=2)
    with open(outdir/"tpci_detuning_all.json","w") as f:
        json.dump(all_rows, f, indent=2)
    print(f"Wrote {len(by_sub)} subject JSONs + summary to {outdir}")

    # Quick Δf vs load law check per triad across the whole dataset
    from collections import defaultdict
    agg = defaultdict(list)
    for r in all_rows:
        bw = r["bandwidth_half"]
        if bw is not None:
            agg[tuple(r["triad"])].append((r["load"], bw))
    for triad, pairs in agg.items():
        arr = np.array(pairs, float)
        Ls = arr[:,0]; BWs = arr[:,1]
        # only meaningful if there is load variance
        if len(np.unique(Ls)) < 2:
            print(f"Triad {triad}: insufficient load variance (unique loads={np.unique(Ls)})")
            continue
        x = Ls**(-0.5)
        A = np.dot(x, BWs)/np.dot(x, x)
        yhat = A*x
        SS_res = np.sum((BWs - yhat)**2)
        SS_tot = np.sum((BWs - BWs.mean())**2)
        R2 = 1 - SS_res/SS_tot if SS_tot>0 else np.nan
        print(f"Triad {triad}: A={A:.4f}, R²={R2:.3f}, n={len(BWs)}")

if __name__ == "__main__":
    main()
