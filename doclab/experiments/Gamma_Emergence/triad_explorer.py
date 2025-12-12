# File: triad_explorer.py
#
# This script implements the 3-Pass "RPA-Triage" Agent.
# It's an exploratory tool to discover task-modulated triadic coupling
# by first finding the most relevant *time window* (Pass 1),
# then finding the most active *frequency triads* (Pass 2),
# then running a final, focused permutation test (Pass 3).

import os, re, json, pathlib, warnings, argparse
import numpy as np
import multiprocessing
from functools import partial
from collections import defaultdict
import time

# --- Helper Functions (Re-used from triad_tpci_detuning_9.py) ---
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

def gauss(x, A, mu, sig, B):
    return A * np.exp(-(x-mu)**2/(2*sig**2)) + B

def halfwidth_gauss(x, y):
    from scipy.optimize import curve_fit
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

def phase_shuffle(phi, rng):
    ep, ch, T = phi.shape
    out = np.empty_like(phi)
    for i in range(ep):
        shift = rng.integers(0, T)
        out[i] = np.roll(phi[i], shift, axis=-1)
    return out

# --- Pass 1: RPA Temporal Triage Agent (INST-NALY-001) ---

def run_pass1_temporal_triage(epochs_low, epochs_high, sf, args):
    """
    Finds the "vital few" time window using RPA.
    Uses "cheap math" (Time-Frequency Power) to find the time
    window with the maximum power *modulation* (Load High vs. Low).
    """
    import mne
    print("  -> [PASS 1] Running RPA Temporal Triage (INST-NALY-001)...")
    
    # 1. Use Morlet Wavelets to get Time-Frequency Power
    # We'll use a broad frequency range (e.g., 4-45 Hz)
    freqs = np.arange(4., 45., 2.)
    n_cycles = freqs / 2.
    
    print(f"     ...calculating TFR for Low Load (n={len(epochs_low)})...")
    tfr_low = mne.time_frequency.tfr_morlet(epochs_low, freqs, n_cycles=n_cycles,
                                            use_fft=True, return_itc=False,
                                            average=True, verbose=False)
    
    print(f"     ...calculating TFR for High Load (n={len(epochs_high)})...")
    tfr_high = mne.time_frequency.tfr_morlet(epochs_high, freqs, n_cycles=n_cycles,
                                             use_fft=True, return_itc=False,
                                             average=True, verbose=False)

    # 2. Create the "Power Modulation Map" (Load High - Load Low)
    # We use (High - Low) / Low to get relative change
    power_mod_map = (tfr_high.data - tfr_low.data) / (tfr_low.data + 1e-9)
    
    # 3. Apply RPA: Find the time point with the most change
    # Sum the absolute change across all frequencies
    total_mod_vs_time = np.sum(np.abs(power_mod_map), axis=(0, 1))
    
    # Find the time index (peak) of this modulation
    peak_time_idx = np.argmax(total_mod_vs_time)
    peak_time = tfr_low.times[peak_time_idx]
    
    # 4. Define the new rationalized time window
    t_min_new = peak_time - (args.rpa_window_hz / 2.0)
    t_max_new = peak_time + (args.rpa_window_hz / 2.0)
    
    # Clamp to original boundaries
    t_min_new = max(args.tmin, t_min_new)
    t_max_new = min(args.tmax, t_max_new)
    
    print(f"     ...RPA complete. Peak modulation at {peak_time:.3f}s.")
    print(f"     ...New rationalized window: [{t_min_new:.3f}s, {t_max_new:.3f}s]")
    
    return t_min_new, t_max_new

# --- Pass 2: Frequency Triage Agent (DOMA-075) ---

# --- Worker functions for Pass 2 (parallel processing) ---
def init_worker_pass2(phi_bank_init, f_list_init):
    """Initializes the worker for Pass 2's bicoherence map."""
    global worker_phi_bank, worker_f_list
    worker_phi_bank = phi_bank_init
    worker_f_list = f_list_init

def run_one_triad_tpci(f1_idx):
    """Calculates TPCI for all f2s for a given f1."""
    global worker_phi_bank, worker_f_list
    
    f1 = worker_f_list[f1_idx]
    tpci_row = np.zeros(len(worker_f_list))
    
    for f2_idx in range(f1_idx, len(worker_f_list)):
        f2 = worker_f_list[f2_idx]
        f3 = f1 + f2
        
        # Check if f3 is in our pre-calculated bank
        if f3 in worker_phi_bank:
            phi1 = worker_phi_bank[f1]
            phi2 = worker_phi_bank[f2]
            phi3 = worker_phi_bank[f3]
            
            # Calculate TPCI
            # We take the mean, as tpci() returns a value per epoch
            val = np.mean(tpci(phi1, phi2, phi3))
            tpci_row[f2_idx] = val
    
    # We return the index and the row to re-assemble the map
    return (f1_idx, tpci_row)

def run_pass2_frequency_triage(epochs_all_windowed, sf, args):
    """
    Finds the "vital few" frequency triads using a global bicoherence map.
    This is the "Frequency Triage" step (DOMA-075).
    """
    print("  -> [PASS 2] Running Frequency Triage (DOMA-075)...")
    
    # 1. Define the frequency space to search
    f_list = np.arange(args.f_min, args.f_max + args.f_step, args.f_step)
    print(f"     ...searching {len(f_list)} frequencies from {args.f_min} to {args.f_max} Hz.")
    
    # 2. Pre-calculate all phase angles (the "Phase Bank")
    # This is the most expensive single-threaded step.
    # It creates a dictionary: {frequency -> (n_epochs, n_chans, n_times)}
    print("     ...pre-calculating phase bank (this may take a moment)...")
    phi_bank = {}
    ep_data = epochs_all_windowed.get_data(verbose=False)
    
    for f in f_list:
        # We need to check for f+f_max for the f3 component
        if f <= (args.f_max * 2): # Only calculate if it can be f1, f2, or f3
            phi_bank[f] = bandpass_phase(ep_data, sf, f - args.band, f + args.band)
    
    # Add f_max*2 just in case
    f_end = args.f_max * 2
    if f_end not in phi_bank:
         phi_bank[f_end] = bandpass_phase(ep_data, sf, f_end - args.band, f_end + args.band)

    print(f"     ...phase bank complete. {len(phi_bank)} frequencies calculated.")
    
    # 3. Calculate the Global Bicoherence (TPCI) Map in parallel
    print("     ...starting parallel bicoherence map calculation...")
    n_cpus = max(1, multiprocessing.cpu_count() - 2)
    bicoherence_map = np.zeros((len(f_list), len(f_list)))
    
    # We pass the (large) phi_bank to the workers *once*
    init_args = (phi_bank, f_list)
    
    with multiprocessing.Pool(processes=n_cpus, initializer=init_worker_pass2, initargs=init_args) as pool:
        
        f1_indices = range(len(f_list))
        
        # imap_unordered is good for load balancing
        for i, (f1_idx, tpci_row) in enumerate(pool.imap_unordered(run_one_triad_tpci, f1_indices)):
            bicoherence_map[f1_idx, :] = tpci_row
            # Make map symmetric
            bicoherence_map[:, f1_idx] = tpci_row 
            
            if (i+1) % 10 == 0 or (i+1) == len(f_list):
                print(f"     ...map calculation {int(100*(i+1)/len(f_list))}% complete...")

    print("     ...bicoherence map complete.")
    
    # 4. Apply RPA: Find the "hotspot" triads
    # We flatten the upper triangle of the map to find peaks
    flat_map = bicoherence_map[np.triu_indices(len(f_list), k=1)]
    
    # Get indices of the top N hotspots
    # We use argsort to get indices, then [-N:] to get the top N
    n_hotspots = int(args.n_hotspots)
    hotspot_indices_flat = np.argsort(flat_map)[-n_hotspots:]
    
    # Convert flat indices back to 2D (f1, f2) indices
    f1_indices_flat, f2_indices_flat = np.triu_indices(len(f_list), k=1)
    
    hotspots = []
    for idx in hotspot_indices_flat:
        f1 = f_list[f1_indices_flat[idx]]
        f2 = f_list[f2_indices_flat[idx]]
        f3 = f1 + f2
        val = flat_map[idx]
        hotspots.append(((f1, f2, f3), val))

    print(f"     ...RPA complete. Identified {len(hotspots)} hotspots.")
    for (f1,f2,f3), val in reversed(hotspots): # Print highest first
        print(f"       - Hotspot: ({f1:.1f}, {f2:.1f}, {f3:.1f}) | Global TPCI = {val:.4f}")
        
    return [h[0] for h in hotspots] # Return list of (f1,f2,f3) tuples

# --- Pass 3: Focused Permutation Test ---

# --- Worker functions for Pass 3 (parallel processing) ---
def init_worker_pass3(phi1_init, phi2_init, phi3_init):
    """Initializes the worker for the final permutation test."""
    global worker_phi1, worker_phi2, worker_phi3
    worker_phi1 = phi1_init
    worker_phi2 = phi2_init
    worker_phi3 = phi3_init

def run_one_permutation_pass3(perm_index, base_seed):
    """Runs a single permutation shuffle and calculates null TPCI."""
    global worker_phi1, worker_phi2, worker_phi3
    
    rng = np.random.default_rng(base_seed + perm_index)
    
    # Shuffle phi2
    phi2_null = phase_shuffle(worker_phi2, rng)
    
    # Calculate null TPCI (mean over epochs)
    v_null = np.mean(tpci(worker_phi1, phi2_null, worker_phi3))
    return v_null

def run_pass3_focused_test(hotspot_triad, epochs_low_w, epochs_high_w, sf, args, out_dir):
    """
    Runs the final, focused permutation test on a single hotspot.
    This is the "Execution" step.
    """
    import pandas as pd
    
    f1, f2, f3 = hotspot_triad
    triad_str = f"{f1:.1f}-{f2:.1f}-{f3:.1f}".replace('.', 'p')
    print(f"  -> [PASS 3] Running Focused Test for Triad ({f1:.1f}, {f2:.1f}, {f3:.1f})...")

    out_path_combo = out_dir / f"explorer_triad-{triad_str}.json"
    if out_path_combo.exists() and not args.overwrite:
        print(f"     ...skipping, result file exists.")
        return

    # 1. Get phase data for this specific triad for LOW and HIGH loads
    ep_low = epochs_low_w.get_data(verbose=False)
    ep_high = epochs_high_w.get_data(verbose=False)

    phi1_low = bandpass_phase(ep_low, sf, f1 - args.band, f1 + args.band)
    phi2_low = bandpass_phase(ep_low, sf, f2 - args.band, f2 + args.band)
    phi3_low = bandpass_phase(ep_low, sf, f3 - args.band, f3 + args.band)
    
    phi1_high = bandpass_phase(ep_high, sf, f1 - args.band, f1 + args.band)
    phi2_high = bandpass_phase(ep_high, sf, f2 - args.band, f2 + args.band)
    phi3_high = bandpass_phase(ep_high, sf, f3 - args.band, f3 + args.band)

    # 2. Calculate the "real" TPCI values
    # tpci() returns (n_epochs,), so we take the mean
    tpci_low_real = np.mean(tpci(phi1_low, phi2_low, phi3_low))
    tpci_high_real = np.mean(tpci(phi1_high, phi2_high, phi3_high))
    tpci_diff_real = tpci_high_real - tpci_low_real
    
    print(f"     ...Real TPCI: Low={tpci_low_real:.4f}, High={tpci_high_real:.4f}, Diff={tpci_diff_real:.4f}")

    # 3. Run permutation test on the *difference*
    # We combine all phi1, phi2, phi3. We will shuffle the (High/Low) labels.
    
    # Concatenate Low and High epochs for shuffling
    # (n_epochs_total, n_chans, n_times)
    phi1_all = np.concatenate([phi1_low, phi1_high], axis=0)
    phi2_all = np.concatenate([phi2_low, phi2_high], axis=0)
    phi3_all = np.concatenate([phi3_low, phi3_high], axis=0)
    
    n_low = len(phi1_low)
    n_total = len(phi1_all)
    
    print(f"     ...starting {args.perm} permutations on the difference...")
    
    # We don't need the Pool for this, we can do it differently.
    # We'll calculate all TPCI values first, then shuffle labels.
    
    all_tpci_vals = tpci(phi1_all, phi2_all, phi3_all)
    
    null_diffs = []
    rng = np.random.default_rng(args.seed)
    
    for i in range(args.perm):
        # Shuffle the TPCI values
        shuffled_indices = rng.permutation(n_total)
        
        # Re-assign to "null" Low and "null" High groups
        null_low_vals = all_tpci_vals[shuffled_indices[:n_low]]
        null_high_vals = all_tpci_vals[shuffled_indices[n_low:]]
        
        # Calculate the null difference
        null_diff = np.mean(null_high_vals) - np.mean(null_low_vals)
        null_diffs.append(null_diff)

    null_diffs = np.array(null_diffs)

    # 4. Calculate p-value
    # How many null diffs were *more extreme* (larger absolute value) than our real diff?
    pval = (np.abs(null_diffs) >= np.abs(tpci_diff_real)).mean()
    
    print(f"     ...Permutation test complete. p-value = {pval:.4f}")
    
    # 5. Save results
    result_dict = dict(
        triad=list(hotspot_triad),
        status="computed",
        t_min_window=epochs_low_w.tmin,
        t_max_window=epochs_low_w.tmax,
        tpci_low_load=float(tpci_low_real),
        tpci_high_load=float(tpci_high_real),
        tpci_diff_high_minus_low=float(tpci_diff_real),
        perm_p_value=float(pval),
        n_epochs_low=n_low,
        n_epochs_high=len(phi1_high),
        n_permutations=args.perm
    )
    
    with open(out_path_combo, "w") as f:
        json.dump(result_dict, f, indent=2)

# --- Main Controller ---

def process_file(eeg_path, ev_path, out_dir, args):
    import mne
    import pandas as pd
    
    # --- Setup: Load Data (same as before) ---
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
    task_match = re.search(r"task-([A-Za-z00-9]+)", str(eeg_path))
    task = task_match.group(1) if task_match else "UNK"

    stim_mask = select_stim_rows(ev, task)
    ev_stim = ev.loc[stim_mask].copy()
    if ev_stim.empty:
        warnings.warn(f"No stimuli selected for {eeg_path}")
        return False

    onsets = ev_stim["onset"].to_numpy(float)
    events = np.c_[(onsets*sf).astype(int), np.zeros_like(onsets, int), np.ones_like(onsets, int)]
    
    # We create the epochs with the *full* time window first
    epochs_full = mne.Epochs(raw, events, event_id=dict(stim=1),
                             tmin=args.tmin, tmax=args.tmax,
                             baseline=None, preload=True, verbose=False) # Preload!
    
    if len(events) < args.min_epochs: 
        warnings.warn(f"Too few events ({len(events)}) to create epochs: {eeg_path}")
        return False

    # --- Setup: Get Load Bins (same as before) ---
    print("  -> Calculating load bins...")
    bp = []
    # We must iterate over preloaded data
    for ep_data in epochs_full.get_data(verbose=False):
        ep_data_batch = ep_data[np.newaxis, :, :] 
        power_val = band_power(ep_data_batch, sf, 15.0, 30.0) 
        bp.append(power_val[0])
    
    bp = np.array(bp)
    q = pd.qcut(pd.Series(bp).rank(method="first"), args.quantiles, labels=False, duplicates="drop")
    loads = (q + 1).to_numpy()
    
    # Get epochs for lowest and highest load
    # --- FIX: We were looking for load 2 and load 5 by mistake ---
    idx_low = np.where(loads == np.min(loads))[0]
    idx_high = np.where(loads == np.max(loads))[0]
    
    if len(idx_low) < args.min_epochs or len(idx_high) < args.min_epochs:
        print(f"  ! Not enough epochs in low/high load bins to proceed.")
        return False
        
    epochs_low_full = epochs_full[idx_low]
    epochs_high_full = epochs_full[idx_high]
    
    # --- [PASS 1] ---
    t_min_w, t_max_w = run_pass1_temporal_triage(epochs_low_full, epochs_high_full, sf, args)
    
    # --- Create new, windowed Epochs objects for Pass 2 & 3 ---
    # We use .crop() which is fast on preloaded data
    epochs_all_windowed = epochs_full.copy().crop(tmin=t_min_w, tmax=t_max_w, verbose=False)
    epochs_low_windowed = epochs_low_full.copy().crop(tmin=t_min_w, tmax=t_max_w, verbose=False)
    epochs_high_windowed = epochs_high_full.copy().crop(tmin=t_min_w, tmax=t_max_w, verbose=False)
    
    # --- [PASS 2] ---
    # Find hotspots using *all* windowed epochs
    hotspot_triads = run_pass2_frequency_triage(epochs_all_windowed, sf, args)
    
    if not hotspot_triads:
        print("  ! [PASS 2] Found no hotspots to analyze. Exiting.")
        return False
        
    # --- [PASS 3] ---
    print(f"  -> [PASS 3] Starting focused tests on {len(hotspot_triads)} hotspots...")
    for triad in hotspot_triads:
        run_pass3_focused_test(triad, epochs_low_windowed, epochs_high_windowed, sf, args, out_dir)
    
    print(f"  ✓ Explorer run complete for {eeg_path.name}")
    return True

def main():
    ap = argparse.ArgumentParser(description="3-Pass RPA-Triage Agent for Triadic Coupling Exploration")
    
    # --- Main Args ---
    ap.add_argument("--eeg-path", required=True, help="Path to the EEG file (.bdf, .set, .edf)")
    ap.add_argument("--events-path", required=True, help="Path to the corresponding events.tsv file")
    ap.add_argument("--outdir", required=True, help="Base output directory for results")
    ap.add_argument("--min-epochs", type=int, default=8, help="Minimum epochs per load bin (default 8)")
    ap.add_argument("--roi", nargs="*", default=None, help="ROI channels (e.g., O1 O2 Oz POz)")
    ap.add_argument("--quantiles", type=int, default=4, help="Quantiles for proxy load (default 4)")
    ap.add_argument("--tmin", type=float, default=0.0, help="Full epoch tmin")
    ap.add_argument("--tmax", type=float, default=2.0, help="Full epoch tmax")
    ap.add_argument("--highpass", type=float, default=0.5)
    ap.add_argument("--lowpass", type=float, default=80.0) # Higher lowpass for explorer
    ap.add_argument("--band", type=float, default=1.0, help="+/- Hz for bandpass around f1,f2,f3")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--overwrite", action="store_true", help="Overwrite existing output files.")

    # --- Pass 1 (RPA) Args ---
    ap.add_argument("--rpa-window-hz", type=float, default=0.3, help="Width (in seconds) of the RPA time window (default 0.3s)")

    # --- Pass 2 (Explorer) Args ---
    ap.add_argument("--f-min", type=float, default=4.0, help="Min f1/f2 to scan (default 4.0 Hz)")
    ap.add_argument("--f-max", type=float, default=40.0, help="Max f1/f2 to scan (default 40.0 Hz)")
    ap.add_argument("--f-step", type=float, default=1.0, help="Step size for frequency scan (default 1.0 Hz)")
    ap.add_argument("--n-hotspots", type=int, default=5, help="Number of hotspots to promote to Pass 3 (default 5)")

    # --- Pass 3 (Permutation) Args ---
    ap.add_argument("--perm", type=int, default=1000, help="Phase-shuffle permutations (default 1000)")

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
    
    out_dir_for_file = outdir_base / f"sub-{sub}_ses-{ses}_task-{task}_explorer_results"
    out_dir_for_file.mkdir(parents=True, exist_ok=True)
    
    print(f"▶ Starting 3-Pass Explorer Agent for: {eeg_path.name}...")
    print(f"  Results will be saved in: {out_dir_for_file.name}")
    try:
        process_file(eeg_path, ev_path, out_dir_for_file, args)

    except Exception as e:
        print(f"  ✗ FAILED {eeg_path.name} -> {e}")
        raise e 

if __name__ == "__main__":
    # This is critical for Windows multiprocessing
    multiprocessing.freeze_support()
    main()