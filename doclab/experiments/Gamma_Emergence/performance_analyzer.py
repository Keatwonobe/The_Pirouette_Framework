# File: performance_crawler.py
#
# This "Master Script" crawls a BIDS directory, uses your 'triad_explorer'
# to score performance, and then uses your 'manifold_generator_2'
# to generate "Hit" vs. "Loser" manifolds for comparison.

import os
import json
import re
import warnings
import pathlib
import numpy as np
import pandas as pd
import mne
import logging
from multiprocessing import Pool, cpu_count
from functools import partial
import time

# --- Import key functions from your existing scripts ---
# We assume triad_explorer.py and manifold_generator_2.py
# are in the same directory or on the PYTHONPATH.

# From triad_explorer.py (for scoring)
try:
    from triad_explorer import select_stim_rows
except ImportError:
    print("WARNING: Could not import 'select_stim_rows' from triad_explorer.py")
    print("Please ensure the file is in the same directory.")
    # Define a placeholder if import fails, to allow script to be written
    def select_stim_rows(df, n=2): 
        print("Using placeholder select_stim_rows")
        return {'hit_events': [], 'miss_events': [], 'fa_events': [], 'n_hits': 0, 'n_misses': 0, 'n_fas': 0}

# From manifold_generator_2.py (for analysis)
try:
    from manifold_generator_2 import (
        read_raw_any, 
        read_events_tsv, 
        _get_phase_at_freq, 
        _calculate_bicoherence_for_triad_timeseries,
        _process_triad_chunk
    )
except ImportError:
    print("WARNING: Could not import from manifold_generator_2.py")
    # Define placeholders
    def read_raw_any(p): print("Placeholder read_raw_any"); return None
    def read_events_tsv(p): print("Placeholder read_events_tsv"); return pd.DataFrame()
    def _process_triad_chunk(chunk, all_phase_data, fs, bicoherence_threshold):
        print("Placeholder _process_triad_chunk"); return []

# --- Configuration ---
BIDS_ROOT = "data"  # Set this to your 'Executive_Functioning_Data' directory
OUTPUT_FILE = "comparative_results.json"
TASK_TO_ANALYZE = "NB"  # We're focusing on the N-Back task
N_BACK_LEVEL = 2      # You confirmed it's 2-Back
EPOCH_TMIN = 0.0      # Start epoch at the event
EPOCH_TMAX = 1.0      # Take 1 second of data
RESPONSE_WINDOW_MS = 1600 # From triad_explorer, time to link response

# --- New Wrapper for Manifold Generation ---

def compute_manifold_from_epochs(epochs_data, sfreq, f_min=4, f_max=20, f_step=1.0, bicoherence_threshold=0.5):
    """
    Runs the core logic from manifold_generator_2.py on epoched data.
    
    Args:
        epochs_data (np.ndarray): Data of shape (n_epochs, n_channels, n_times)
        sfreq (int): Sampling frequency
        f_min (int): Min f1/f2
        f_max (int): Max f1/f2
        f_step (float): Frequency step
        bicoherence_threshold (float): Bicoherence threshold
        
    Returns:
        np.ndarray: A 2D manifold (f1, f2) of coupling strength
    """
    
    # We are analyzing the 'evoked' response, so we average epochs
    # to get (n_channels, n_times). This is *one* way to do it.
    # Another way is to run on all trials and average the *manifolds*,
    # but averaging data first is "cheaper".
    if epochs_data.ndim == 3 and epochs_data.shape[0] > 1:
        print(f"Averaging {epochs_data.shape[0]} epochs...")
        data = np.mean(epochs_data, axis=0)
    elif epochs_data.ndim == 3 and epochs_data.shape[0] == 1:
        data = epochs_data[0] # Only one epoch
    else:
        data = epochs_data # Assume already (n_channels, n_times)
        
    if data.shape[0] > 100: # Heuristic: channels > times?
        data = data.T # Transpose if data is (n_times, n_channels)

    n_channels, n_samples = data.shape
    print(f"Analyzing data chunk: {n_channels} channels, {n_samples} samples")

    # 1. Get Phase for all frequencies
    freqs = np.arange(f_min, f_max + f_step, f_step)
    all_phase_data = {}
    
    # This is slow, but matches your v2 generator's method
    for f in freqs:
        all_phase_data[f] = _get_phase_at_freq(data, sfreq, f)

    # 2. Define all triad chunks
    f1_list = freqs
    f2_list = freqs
    all_triads = [(f1, f2) for f1 in f1_list for f2 in f2_list if f1 <= f2]
    
    # 3. Process triads in parallel
    n_procs = max(1, cpu_count() - 2)
    chunk_size = int(np.ceil(len(all_triads) / n_procs))
    triad_chunks = [
        all_triads[i : i + chunk_size]
        for i in range(0, len(all_triads), chunk_size)
    ]
    
    print(f"Processing {len(all_triads)} triads on {n_procs} cores...")
    
    # Create a partial function with the fixed arguments
    process_func = partial(
        _process_triad_chunk,
        all_phase_data=all_phase_data,
        fs=sfreq,
        bicoherence_threshold=bicoherence_threshold
    )

    with Pool(processes=n_procs) as pool:
        results_list_of_lists = pool.map(process_func, triad_chunks)
        
    # Flatten results
    all_results = [item for sublist in results_list_of_lists for item in sublist]
    
    # 4. Build the Manifold
    manifold = np.zeros((len(freqs), len(freqs)))
    f_to_idx = {f: i for i, f in enumerate(freqs)}
    
    for f1, f2, f_res, bicoh_val, _ in all_results:
        if f1 in f_to_idx and f2 in f_to_idx:
            i, j = f_to_idx[f1], f_to_idx[f2]
            manifold[i, j] = bicoh_val
            if i != j: # Manifold is symmetric
                manifold[j, i] = bicoh_val
                
    return manifold.tolist() # Convert to list for JSON serialization

# --- Main Crawler Function ---

def main():
    print(f"Starting BIDS crawl of '{BIDS_ROOT}' for task '{TASK_TO_ANALYZE}'")
    
    # Use rglob to recursively find all matching events.tsv files
    bids_path = pathlib.Path(BIDS_ROOT)
    event_files = list(bids_path.rglob(f'*_task-{TASK_TO_ANALYZE}_*_events.tsv'))
    
    print(f"Found {len(event_files)} matching event files.")
    
    master_results = {}

    for events_file in event_files:
        try:
            print(f"\n--- Processing: {events_file.name} ---")
            
            # Find matching EEG file (assuming .set format from your dirlist)
            eeg_filename = events_file.name.replace("_events.tsv", "_eeg.set")
            eeg_file = events_file.parent / eeg_filename
            
            if not eeg_file.exists():
                # Try .vhdr as well
                eeg_filename = events_file.name.replace("_events.tsv", "_eeg.vhdr")
                eeg_file = events_file.parent / eeg_filename
            
            if not eeg_file.exists():
                logging.warning(f"No matching EEG file found for {events_file.name}. Skipping.")
                continue

            # Extract subject ID
            sub_match = re.search(r'sub-([a-zA-Z0-9]+)', events_file.name)
            sub_id = sub_match.group(1) if sub_match else "unknown"
            
            # 1. Score Performance
            events_df = read_events_tsv(events_file)
            # You may need to pass sfreq here if select_stim_rows needs it
            performance = select_stim_rows(events_df, n=N_BACK_LEVEL)
            
            perf_summary = {
                "hits": performance['n_hits'],
                "misses": performance['n_misses'],
                "false_alarms": performance['n_fas']
            }
            print(f"Performance: {perf_summary}")
            
            # 2. Load Raw EEG Data
            raw = read_raw_any(eeg_file)
            raw.load_data()
            raw.set_eeg_reference('average') # Re-reference
            raw.filter(l_freq=1.0, h_freq=45.0) # Basic filtering
            sfreq = int(raw.info['sfreq'])
            
            # 3. Create Biased Epochs
            
            # --- "WINNER" / FLOW-STATE EPOCHS (Hits) ---
            manifold_hits = []
            if performance['hit_events']:
                hit_events_mne = np.array(
                    [[s, 0, 1] for s in performance['hit_events']], dtype=int
                )
                epochs_hits = mne.Epochs(raw, hit_events_mne, event_id={'hit': 1},
                                         tmin=EPOCH_TMIN, tmax=EPOCH_TMAX,
                                         baseline=None, preload=True,
                                         picks='eeg', on_missing='warning')
                if len(epochs_hits) > 0:
                    manifold_hits = compute_manifold_from_epochs(
                        epochs_hits.get_data(copy=False), sfreq
                    )
                
            # --- "LOSER" / FAILED-STATE EPOCHS (Misses + FAs) ---
            manifold_losers = []
            loser_events = performance['miss_events'] + performance['fa_events']
            if loser_events:
                loser_events_mne = np.array(
                    [[s, 0, 2] for s in loser_events], dtype=int
                )
                epochs_losers = mne.Epochs(raw, loser_events_mne, event_id={'loser': 2},
                                           tmin=EPOCH_TMIN, tmax=EPOCH_TMAX,
                                           baseline=None, preload=True,
                                           picks='eeg', on_missing='warning')
                if len(epochs_losers) > 0:
                    manifold_losers = compute_manifold_from_epochs(
                        epochs_losers.get_data(copy=False), sfreq
                    )
            
            # 4. Store Results
            if sub_id not in master_results:
                master_results[sub_id] = []
                
            master_results[sub_id].append({
                "source_file": str(events_file.name),
                "performance": perf_summary,
                "manifold_hits": manifold_hits,
                "manifold_losers": manifold_losers
            })
            
        except Exception as e:
            logging.error(f"Failed to process {events_file.name}: {e}")
            logging.exception("Exception details:") # Pring stack trace
            
    # 5. Write single JSON output
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(master_results, f, indent=2)
        
    print(f"\n--- CRAWL COMPLETE ---")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    warnings.simplefilter('ignore', RuntimeWarning)
    # This is to fix multiprocessing issues on Windows/macOS
    # Your scripts already do this, which is great.
    mne.utils.set_config('MNE_NJOBS', '1')
    
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Total processing time: {(end_time - start_time) / 60:.2f} minutes")