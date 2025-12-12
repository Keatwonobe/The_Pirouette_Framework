# File: manifold_generator.py
#
# This is the "Resonant Manifold" Agent (The "EEG X-ray").
#
# It combines the logic of all previous scripts to generate a complete
# TPCI Manifold for a single subject, mapping TPCI(triad, time).
#
# It does this by creating a one-time "Phase Bank" for all frequencies
# and then sliding a window over this bank for all triad combinations.
#
# This is computationally intensive.

import os, re, json, pathlib, warnings, argparse
import numpy as np
import itertools
import multiprocessing
from functools import partial

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
    # Add other task logic if needed
    stim = ~val.str.contains("response") & ~val.str.contains("ignore")
    return stim

def bandpass_phase(ep, fs, f_lo, f_hi):
    from scipy.signal import butter, filtfilt, hilbert
    b, a = butter(4, [f_lo/(fs/2), f_hi/(fs/2)], btype='band')
    z = filtfilt(b, a, ep, axis=-1)
    return np.angle(hilbert(z, axis=-1))

def tpci_slice(phi1_slice, phi2_slice, phi3_slice):
    # This version calculates TPCI for a *single window*
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

# --- Phase Bank Worker ---
# This function is called by the parallel pool to create the Phase Bank
def calculate_phase_for_freq(f, ep_data, sf, band):
    return f, bandpass_phase(ep_data, sf, f - band, f + band)

def create_phase_bank(ep_data, sf, freqs, band):
    """
    Calculates phase for all frequencies in parallel.
    Returns a dictionary: { freq: phase_data }
    """
    phase_bank = {}
    n_cpus = max(1, multiprocessing.cpu_count() - 2)
    
    # Use 'partial' to "freeze" the arguments that are the same for all workers
    worker_func = partial(calculate_phase_for_freq, 
                          ep_data=ep_data, sf=sf, band=band)

    with multiprocessing.Pool(n_cpus) as pool:
        # pool.imap_unordered is faster as it doesn't wait
        for i, (f, phase_data) in enumerate(pool.imap_unordered(worker_func, freqs)):
            phase_bank[f] = phase_data
            if (i+1) % 10 == 0 or (i+1) == len(freqs):
                print(f"     ...Phase bank progress: {i+1}/{len(freqs)} frequencies calculated.")
    
    return phase_bank

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

    # --- 3. The "Phase Bank" Calculation ---
    print(f"  -> [PASS 1] Creating Phase Bank for Low Load (n={len(idx_low)})...")
    freqs = np.arange(args.f_min, args.f_max + 1, args.f_step)
    phase_bank_low = create_phase_bank(ep_low_data, sf, freqs, args.band)
    
    print(f"  -> [PASS 1] Creating Phase Bank for High Load (n={len(idx_high)})...")
    phase_bank_high = create_phase_bank(ep_high_data, sf, freqs, args.band)
    print("  ✓ Phase Banks complete.")

    # --- 4. Define Sliding Window & Triad Combinations ---
    total_samples = ep_low_data.shape[2]
    window_size_samp = int(sf * args.window_sec)
    step_size_samp = int(sf * args.step_sec)
    
    t_centers_sec = []
    for t_start_samp in range(0, total_samples - window_size_samp, step_size_samp):
        t_center_sec = (t_start_samp + window_size_samp / 2) / sf + args.tmin
        t_centers_sec.append(t_center_sec)

    # Generate all valid f1, f2 combinations
    triads_list = []
    triad_indices = [] # (f1, f2, f3)
    f1_range = np.arange(args.f1_min, args.f1_max + 1, args.f_step)
    f2_range = np.arange(args.f2_min, args.f2_max + 1, args.f_step)

    for f1 in f1_range:
        for f2 in f2_range:
            f3 = f1 + f2
            # Check if all 3 frequencies are in our bank
            if f1 in phase_bank_low and f2 in phase_bank_low and f3 in phase_bank_low:
                triads_list.append(f"{f1:.1f}-{f2:.1f}-{f3:.1f}")
                triad_indices.append((f1, f2, f3))

    if not triads_list:
        print("  ! No valid triads found in the specified frequency ranges. Check --f-max.")
        return False
        
    print(f"  -> [PASS 2] Generating Manifold: {len(triads_list)} triads x {len(t_centers_sec)} time points...")
    
    # Initialize the "rugs"
    manifold_low = np.zeros((len(triads_list), len(t_centers_sec)))
    manifold_high = np.zeros((len(triads_list), len(t_centers_sec)))

    # --- 5. The "Manifold" Calculation (The "X-ray") ---
    for t_idx, t_start_samp in enumerate(range(0, total_samples - window_size_samp, step_size_samp)):
        t_end_samp = t_start_samp + window_size_samp
        
        for f_idx, (f1, f2, f3) in enumerate(triad_indices):
            
            # Slice the bank for LOW load
            phi1_low_w = phase_bank_low[f1][:, :, t_start_samp:t_end_samp]
            phi2_low_w = phase_bank_low[f2][:, :, t_start_samp:t_end_samp]
            phi3_low_w = phase_bank_low[f3][:, :, t_start_samp:t_end_samp]
            
            # Slice the bank for HIGH load
            phi1_high_w = phase_bank_high[f1][:, :, t_start_samp:t_end_samp]
            phi2_high_w = phase_bank_high[f2][:, :, t_start_samp:t_end_samp]
            phi3_high_w = phase_bank_high[f3][:, :, t_start_samp:t_end_samp]
            
            # Calculate TPCI for this (triad, time) pixel
            manifold_low[f_idx, t_idx] = tpci_slice(phi1_low_w, phi2_low_w, phi3_low_w)
            manifold_high[f_idx, t_idx] = tpci_slice(phi1_high_w, phi2_high_w, phi3_high_w)
            
        if (t_idx+1) % 10 == 0 or (t_idx+1) == len(t_centers_sec):
            print(f"     ...Manifold progress: {t_idx+1}/{len(t_centers_sec)} time points calculated.")

    print("  ✓ Manifold generation complete.")

    # --- 6. Save the Manifold Data ---
    result_dict = dict(
        file=str(eeg_path.name),
        subject="sub",
        session="ses",
        task=task,
        n_epochs_low=len(idx_low),
        n_epochs_high=len(idx_high),
        triad_labels=triads_list, # The Y-axis
        time_points_sec=t_centers_sec, # The X-axis
        manifold_low_load=manifold_low.tolist(), # The "rug" data
        manifold_high_load=manifold_high.tolist() # The "rug" data
    )

    with open(out_file, "w") as f:
        json.dump(result_dict, f) # No indent, file is huge

    print(f"  ✓ Manifold data saved to {out_file.name}")
    return True


def main():
    ap = argparse.ArgumentParser(description="Resonant Manifold 'X-ray' Generator")
    
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
    
    out_dir_for_file = outdir_base / f"sub-{sub}_ses-{ses}_task-{task}_manifold_results"
    out_dir_for_file.mkdir(parents=True, exist_ok=True)
    
    out_file_path = out_dir_for_file / "manifold_data.json"
    
    if out_file_path.exists() and not args.overwrite:
        print(f"  ! Manifold file {out_file_path.name} already exists. Use --overwrite to re-run.")
        return

    print(f"▶ Starting Manifold 'X-ray' Agent for: {eeg_path.name}...")
    print(f"  Manifold data will be saved in: {out_file_path.name}")
    try:
        # We need to wrap the main function in this if __name__ == "__main__"
        # block to make multiprocessing happy on Windows
        process_file(eeg_path, ev_path, out_file_path, args)

    except Exception as e:
        print(f"  ✗ FAILED {eeg_path.name} -> {e}")
        raise e 

if __name__ == "__main__":
    # This is CRITICAL for multiprocessing on Windows
    # It prevents the script from re-running when workers are spawned
    main()