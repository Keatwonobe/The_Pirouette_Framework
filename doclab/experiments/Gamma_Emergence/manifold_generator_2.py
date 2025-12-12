# File: manifold_generator_v2.py
#
# This is a new "Resonant Manifold" Agent (The "EEG X-ray").
#
# This version is optimized for LOW MEMORY usage.
# Instead of building one giant Phase Bank, it iterates
# one triad at a time, calculates its time-series, and
# discards the phase data before moving to the next.
#
# This is SLOWER, but will not crash from "lack of resources."

import os, re, json, pathlib, warnings, argparse
import numpy as np
import itertools
import multiprocessing
from functools import partial
import time # To time the process

# --- Helper Functions (Re-used from previous scripts) ---
# (Imports are kept inside functions)

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
    # Add other task logic if needed
    stim = ~val.str.contains("response") & ~val.str.contains("ignore")
    return stim

def bandpass_phase(ep, fs, f_lo, f_hi):
    from scipy.signal import butter, filtfilt, hilbert
    b, a = butter(4, [f_lo/(fs/2), f_hi/(fs/2)], btype='band')
    z = filtfilt(b, a, ep, axis=-1)
    return np.angle(hilbert(z, axis=-1))

def tpci_slice(phi1_slice, phi2_slice, phi3_slice):
    # (n_epochs, n_chans, n_window_samps)
    z = np.exp(1j*(phi3_slice - phi1_slice - phi2_slice))
    # average over time, then over channels, then over epochs
    return np.abs(np.mean(np.mean(np.mean(z, axis=-1), axis=1)))

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

# --- NEW: Time-Series Worker ---
# This worker calculates the *full time series* for *one triad*
def calculate_timeseries_for_triad(triad_indices, ep_low_data, ep_high_data, sf, band, window_size_samp, step_size_samp, total_samples, tmin):
    
    f1, f2, f3 = triad_indices
    triad_label = f"{f1:.1f}-{f2:.1f}-{f3:.1f}"
    
    # 1. Calculate phase *only* for these 3 frequencies
    phi1_low = bandpass_phase(ep_low_data, sf, f1 - band, f1 + band)
    phi2_low = bandpass_phase(ep_low_data, sf, f2 - band, f2 + band)
    phi3_low = bandpass_phase(ep_low_data, sf, f3 - band, f3 + band)
    
    phi1_high = bandpass_phase(ep_high_data, sf, f1 - band, f1 + band)
    phi2_high = bandpass_phase(ep_high_data, sf, f2 - band, f2 + band)
    phi3_high = bandpass_phase(ep_high_data, sf, f3 - band, f3 + band)

    # 2. Slide the window and calculate the time-series
    tpci_low_series = []
    tpci_high_series = []
    
    for t_start_samp in range(0, total_samples - window_size_samp, step_size_samp):
        t_end_samp = t_start_samp + window_size_samp
        
        # --- Low Load ---
        phi1_low_w = phi1_low[:, :, t_start_samp:t_end_samp]
        phi2_low_w = phi2_low[:, :, t_start_samp:t_end_samp]
        phi3_low_w = phi3_low[:, :, t_start_samp:t_end_samp]
        tpci_low_series.append(tpci_slice(phi1_low_w, phi2_low_w, phi3_low_w))
        
        # --- High Load ---
        phi1_high_w = phi1_high[:, :, t_start_samp:t_end_samp]
        phi2_high_w = phi2_high[:, :, t_start_samp:t_end_samp]
        phi3_high_w = phi3_high[:, :, t_start_samp:t_end_samp]
        tpci_high_series.append(tpci_slice(phi1_high_w, phi2_high_w, phi3_high_w))

    return triad_label, tpci_low_series, tpci_high_series


# --- Main Controller ---

def process_file(eeg_path, ev_path, out_file, args):
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
    onsets = ev_stim["onset"].to_numpy(float)
    events = np.c_[(onsets*sf).astype(int), np.zeros_like(onsets, int), np.ones_like(onsets, int)]
    
    epochs_full = mne.Epochs(raw, events, event_id=dict(stim=1),
                             tmin=args.tmin, tmax=args.tmax,
                             baseline=None, preload=True, verbose=False) 
    
    if len(events) < args.min_epochs: 
        warnings.warn(f"Too few events ({len(events)})")
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
        
    ep_low_data = epochs_full[idx_low].get_data(verbose=False)
    ep_high_data = epochs_full[idx_high].get_data(verbose=False)

    # --- 3. Define Sliding Window & Triad Combinations ---
    total_samples = ep_low_data.shape[2]
    window_size_samp = int(sf * args.window_sec)
    step_size_samp = int(sf * args.step_sec)
    
    t_centers_sec = []
    for t_start_samp in range(0, total_samples - window_size_samp, step_size_samp):
        t_center_sec = (t_start_samp + window_size_samp / 2) / sf + args.tmin
        t_centers_sec.append(t_center_sec)

    # Generate all valid f1, f2 combinations
    f_step_hz = args.f_step
    f_all = np.arange(args.f_min, args.f_max + f_step_hz, f_step_hz)
    
    triad_indices_list = [] # List of (f1, f2, f3) tuples
    f1_range = np.arange(args.f1_min, args.f1_max + f_step_hz, f_step_hz)
    f2_range = np.arange(args.f2_min, args.f2_max + f_step_hz, f_step_hz)

    for f1 in f1_range:
        for f2 in f2_range:
            f3 = f1 + f2
            # Check if all 3 frequencies are in our bank
            if f3 <= args.f_max:
                triad_indices_list.append((f1, f2, f3))

    if not triad_indices_list:
        print("  ! No valid triads found in the specified frequency ranges. Check --f-max.")
        return False
        
    print(f"  -> [PASS 2] Generating Manifold: {len(triad_indices_list)} triads x {len(t_centers_sec)} time points...")
    
    # Initialize the "rug" data
    manifold_low_list = []
    manifold_high_list = []
    triad_labels_list = []

    # --- 4. The "Manifold" Calculation (Parallelized) ---
    n_cpus = max(1, multiprocessing.cpu_count() - 2)
    
    # Use 'partial' to "freeze" the arguments that are the same for all workers
    worker_func = partial(calculate_timeseries_for_triad, 
                          ep_low_data=ep_low_data, 
                          ep_high_data=ep_high_data, 
                          sf=sf, 
                          band=args.band, 
                          window_size_samp=window_size_samp, 
                          step_size_samp=step_size_samp,
                          total_samples=total_samples,
                          tmin=args.tmin)
    
    start_time = time.time()
    with multiprocessing.Pool(n_cpus) as pool:
        
        for i, (triad_label, low_series, high_series) in enumerate(pool.imap(worker_func, triad_indices_list)):
            
            triad_labels_list.append(triad_label)
            manifold_low_list.append(low_series)
            manifold_high_list.append(high_series)
            
            if (i+1) % 10 == 0 or (i+1) == len(triad_indices_list):
                elapsed = time.time() - start_time
                est_total = (elapsed / (i+1)) * len(triad_indices_list)
                print(f"     ...Manifold progress: {i+1}/{len(triad_indices_list)} triads complete. (Est. total time: {est_total:.0f}s)")

    print(f"  ✓ Manifold generation complete in {time.time() - start_time:.0f}s.")

    # --- 5. Save the Manifold Data ---
    result_dict = dict(
        file=str(eeg_path.name),
        subject="sub",
        session="ses",
        task=task,
        n_epochs_low=len(idx_low),
        n_epochs_high=len(idx_high),
        triad_labels=triad_labels_list, # The Y-axis
        time_points_sec=t_centers_sec, # The X-axis
        manifold_low_load=manifold_low_list, # The "rug" data
        manifold_high_load=manifold_high_list # The "rug" data
    )

    with open(out_file, "w") as f:
        json.dump(result_dict, f) # No indent, file is huge

    print(f"  ✓ Manifold data saved to {out_file.name}")
    return True


def main():
    ap = argparse.ArgumentParser(description="Resonant Manifold 'X-ray' Generator (v2, Memory-Safe)")
    
    # --- Main Args ---
    ap.add_argument("--eeg-path", required=True, help="Path to the EEG file (.bdf, .set, .edf)")
    ap.add_argument("--events-path", required=True, help="Path to the corresponding events.tsv file")
    ap.add_argument("--outdir", required=True, help="Base output directory for results")
    
    ap.add_argument("--min-epochs", type=int, default=8, help="Minimum epochs per load bin (default 8)")
    ap.add_argument("--roi", nargs="*", default=None, help="ROI channels (e.g., O1 O2 Oz POz)")
    ap.add_argument("--quantiles", type=int, default=4, help="Quantiles for proxy load (default 4)")
    ap.add_argument("--tmin", type=float, default=0.0, help="Full epoch tmin")
    ap.add_argument("--tmax", type=float, default=1.0, help="Full epoch tmax") 
    ap.add_argument("--highpass", type=float, default=0.5)
    ap.add_argument("--lowpass", type=float, default=45.0) 
    ap.add_argument("--band", type=float, default=1.0, help="+/- Hz for bandpass around f1,f2,f3")
    ap.add_argument("--overwrite", action="store_true", help="Overwrite existing output files.")

    # --- Sliding Window Args (for Time axis) ---
    ap.add_argument("--window-sec", type=float, default=0.200, help="Width of the sliding window in seconds (default 0.200s)")
    ap.add_argument("--step-sec", type=float, default=0.020, help="Step size of the sliding window in seconds (default 0.020s)")

    # --- Manifold Args (for Frequency axis) ---
    ap.add_argument("--f-step", type=int, default=1, help="Frequency step in Hz for phase bank (default 1Hz)")
    ap.add_argument("--f-min", type=int, default=4, help="Min freq to calculate for phase bank (default 4Hz)")
    ap.add_argument("--f-max", type=int, default=40, help="Max freq to calculate for phase bank (default 40Hz)")
    
    ap.add_argument("--f1-min", type=int, default=4, help="Min f1 to include in manifold (default 4Hz)")
    ap.add_argument("--f1-max", type=int, default=12, help="Max f1 to include in manifold (default 12Hz)")
    ap.add_argument("--f2-min", type=int, default=4, help="Min f2 to include in manifold (default 4Hz)")
    ap.add_argument("--f2-max", type=int, default=20, help="Max f2 to include in manifold (default 20Hz)")

    args = ap.parse_args()

    # --- Setup Output File ---
    eeg_path = pathlib.Path(args.eeg_path)
    ev_path = pathlib.Path(args.events_path)
    outdir_base = pathlib.Path(args.outdir)
    
    sub_match = re.search(r"sub-([0-9A-Za-z]+)", str(eeg_path.name))
    ses_match = re.search(r"ses-([0-9A-Za-z]+)", str(eeg_path.name))
    task_match = re.search(r"task-([A-Za-z0-9]+)", str(eeg_path.name))
    sub = sub_match.group(1) if sub_match else "NA"
    ses = ses_match.group(1) if ses_match else "NA"
    task = task_match.group(1) if task_match else "UNK"
    
    out_dir_for_file = outdir_base / f"sub-{sub}_ses-{ses}_task-{task}_manifold_results_v2"
    out_dir_for_file.mkdir(parents=True, exist_ok=True)
    
    out_file_path = out_dir_for_file / "manifold_data_v2.json"
    
    if out_file_path.exists() and not args.overwrite:
        print(f"  ! Manifold file {out_file_path.name} already exists. Use --overwrite to re-run.")
        return

    print(f"▶ Starting Manifold 'X-ray' Agent (v2) for: {eeg_path.name}...")
    print(f"  Manifold data will be saved in: {out_file_path.name}")
    try:
        process_file(eeg_path, ev_path, out_file_path, args)
    except Exception as e:
        print(f"  ✗ FAILED {eeg_path.name} -> {e}")
        raise e 

if __name__ == "__main__":
    main()