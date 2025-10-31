import json, re, pathlib, warnings
import numpy as np
import pandas as pd
from bids import BIDSLayout

import mne
from scipy.signal import butter, filtfilt, hilbert

# ---------- CONFIG ----------
bids_root = r"C:/Users/keatw/OneDrive/Documents/Doclab/Big_Datasets/target/paper/Pirouette_Volume_6/doclab/experiments/Gamma_Emergence/Executive_Functioning_Data"     # <-- update
task      = "NB"                    # <-- update to match dataset
subjects  = '23'                        # None = all subjects; or like ['01','02']
sessions  = 1                        # None or ['01']
runs      = 2                        # None or ['01']

out_dir   = pathlib.Path(bids_root, "derivatives", "pirouette_gamma")
out_dir.mkdir(parents=True, exist_ok=True)

# Triads and detuning
triads = [(8.0, 12.0), (10.0, 20.0)]    # (f1,f2) => target f3≈f1+f2
detune = np.linspace(-2.0, 2.0, 41)     # sweep around f3 (Hz)
band_bw = 1.0                           # ±1 Hz band for each component
epoch_tmin, epoch_tmax = 0.0, 4.0       # seconds
reject_eeg = None

# Which column(s) encode load?
LOAD_COLUMNS = ["ImgType", "Block Type", "Load", "Difficulty"]
TRIALTYPE_COLUMNS = ["pressedtask", "PressedTask", "condition", "Condition"]

# --------------------------------

def read_raw_auto(eeg_path):
    eeg_path = str(eeg_path)
    if eeg_path.endswith(".edf"):
        return mne.io.read_raw_edf(eeg_path, preload=True, verbose=False)
    if eeg_path.endswith(".vhdr"):
        return mne.io.read_raw_brainvision(eeg_path, preload=True, verbose=False)
    if eeg_path.endswith(".set"):
        return mne.io.read_raw_eeglab(eeg_path, preload=True, verbose=False)
    if eeg_path.endswith(".fif"):
        return mne.io.read_raw_fif(eeg_path, preload=True, verbose=False)
    if eeg_path.endswith(".fdt"):
        return mne.io.read_raw_eeglab(eeg_path.replace('.fdt', '.set'), preload=True, verbose=False)    
    raise RuntimeError(f"Unsupported EEG format: {eeg_path}")

def infer_loads_from_events(events_df):
    # Try explicit numeric load-like columns
    for col in LOAD_COLUMNS:
        if col in events_df.columns:
            vals = events_df[col]
            # coerce to int if possible
            try:
                return vals.astype(int).to_numpy()
            except Exception:
                pass
    # Try parsing digits from trial_type-like columns
    for col in TRIALTYPE_COLUMNS:
        if col in events_df.columns:
            def parse_load(x):
                if pd.isna(x):
                    return None
                m = re.search(r"(\d+)", str(x))
                return int(m.group(1)) if m else None
            loads = events_df[col].apply(parse_load)
            if loads.notna().any():
                return loads.fillna(0).astype(int).to_numpy()
    # Fallback: all ones (single condition)
    warnings.warn("Could not infer 'load'; defaulting to 1 for all events.")
    return np.ones(len(events_df), dtype=int)

def band_phase(x, fs, f_lo, f_hi):
    b, a = butter(4, [f_lo/(fs/2), f_hi/(fs/2)], btype='band')
    z = filtfilt(b, a, x, axis=-1)
    return np.angle(hilbert(z, axis=-1))

def tpci(phi1, phi2, phi3):  # (n_epochs, n_channels, n_times)
    z = np.exp(1j*(phi3 - phi1 - phi2))
    return np.abs(np.mean(np.mean(z, axis=-1), axis=1))  # per-epoch magnitude

def halfwidth(x, y):
    y = np.asarray(y)
    y = y - y.min()
    ymax = y.max()
    if ymax <= 0: return np.nan
    y = y / ymax
    ipk = np.argmax(y)
    left = np.where(y[:ipk] <= 1/np.sqrt(2))[0]
    right = np.where(y[ipk:] <= 1/np.sqrt(2))[0]
    if len(left)==0 or len(right)==0:
        return np.nan
    # linear interp around threshold
    xL = np.interp(1/np.sqrt(2), y[left[-1]:ipk+1], x[left[-1]:ipk+1])
    xR = np.interp(1/np.sqrt(2), y[ipk:ipk+right[0]+1], x[ipk:ipk+right[0]+1])
    return (xR - xL)/2.0

def process_file(eeg_file, events_file):
    raw = read_raw_auto(eeg_file)
    raw.filter(0.5, 80., fir_design='firwin', verbose=False)
    sfreq = raw.info['sfreq']

    # load events.tsv
    ev = pd.read_csv(events_file, sep='\t')
    if 'Onset' not in ev.columns:
        raise RuntimeError(f"No 'Onset' column in {events_file}")
    onsets = ev['Onset'].to_numpy()
    loads = infer_loads_from_events(ev)
    # Build MNE events array
    samp = (onsets * sfreq).astype(int)
    events = np.c_[samp, np.zeros_like(samp), loads]
    event_id = {f"load_{L}": L for L in np.unique(loads)}

    # Epochs (all channels)
    if reject_eeg is not None:
        reject = {'eeg': reject_eeg}
    else:
        reject = None # This will disable rejection

# The Epochs call now correctly receives either the dict or None
    epochs = mne.Epochs(raw, events, event_id=event_id,
                    tmin=epoch_tmin, tmax=epoch_tmax,
                    preload=True, reject=reject, baseline=None, # Use the new reject variable
                    event_repeated='drop', verbose=False)
    data = {evk.comment: evk.get_data() for evk in epochs.iter_evoked()}  # careful: iter_evoked averages
    # We want raw epochs per condition; use this instead:
    cond_epochs = {cond: epochs[cond].get_data() for cond in epochs.event_id.keys()}

    results = []
    for (f1, f2) in triads:
        f3_nom = f1 + f2
        for L, ep in cond_epochs.items():
            if ep.shape[0] == 0:
                continue
            tpci_curve = []
            for df in detune:
                f3 = f3_nom + df
                phi1 = band_phase(ep, sfreq, f1 - band_bw, f1 + band_bw)
                phi2 = band_phase(ep, sfreq, f2 - band_bw, f2 + band_bw)
                phi3 = band_phase(ep, sfreq, f3 - band_bw, f3 + band_bw)
                vals = tpci(phi1, phi2, phi3)
                tpci_curve.append(np.mean(vals))
            bw_half = halfwidth(detune, tpci_curve)
            results.append(dict(
                file=str(eeg_file),
                events=str(events_file),
                triad=(f1, f2, f3_nom),
                load=int(L.split('_')[-1]),
                detune_grid=detune.tolist(),
                tpci_curve=tpci_curve,
                bandwidth_half=None if np.isnan(bw_half) else float(bw_half),
            ))
    return results

def main():
    layout = BIDSLayout(bids_root, validate=False, derivatives=False)
    # Collect EEG files for task
    eeg_files = layout.get(suffix='eeg', task=task, return_type='filename')
    # If dataset uses edf/vhdr/set without suffix, broaden:
    if not eeg_files:
        eeg_files = layout.get(suffix=None, task=task, extension=['edf','vhdr','set','fif'],
                               return_type='filename')

    # Filter by subject/session/run if specified
    def keep(fp):
        ent = layout.parse_file_entities(fp)
        if subjects and ent.get('subject') not in subjects: return False
        if sessions and ent.get('session') not in sessions: return False
        if runs and ent.get('run') not in runs: return False
        return True
    eeg_files = [f for f in eeg_files if keep(f)]
    if not eeg_files:
        raise RuntimeError("No EEG files found for the requested filters.")

    all_results = []
    for eeg_path in eeg_files:
        ent = layout.parse_file_entities(eeg_path)
        evs = layout.get(subject=ent.get('subject'), session=ent.get('session'),
                         task=ent.get('task'), run=ent.get('run'),
                         suffix='beh', extension='tsv',
                         return_type='filename')
        if not evs:
            warnings.warn(f"No events.tsv for {eeg_path}; skipping.")
            continue
        res = process_file(eeg_path, evs[0])
        all_results.extend(res)

    # Save per subject and summary
    # group by subject
    by_sub = {}
    for r in all_results:
        sub = layout.parse_file_entities(r['file']).get('subject','NA')
        by_sub.setdefault(sub, []).append(r)

    for sub, rows in by_sub.items():
        out_json = out_dir / f"tpci_detuning_sub-{sub}.json"
        with open(out_json, "w") as f:
            json.dump(rows, f, indent=2)
        print(f"Wrote {out_json}")

    # Quick law fit per triad (Δf vs. load) across whole set
    from collections import defaultdict
    agg = defaultdict(list)
    for r in all_results:
        bw = r['bandwidth_half']
        if bw is not None:
            agg[tuple(r['triad'])].append((r['load'], bw))
    for triad, pairs in agg.items():
        arr = np.array(pairs, float)
        Ls = arr[:,0]; BWs = arr[:,1]
        x = Ls**(-0.5)
        A = np.dot(x, BWs)/np.dot(x, x)
        yhat = A*x
        SS_res = np.sum((BWs - yhat)**2)
        SS_tot = np.sum((BWs - BWs.mean())**2)
        R2 = 1 - SS_res/SS_tot if SS_tot>0 else np.nan
        print(f"Triad {triad}: A={A:.4f}, R²={R2:.3f}, n={len(BWs)}")

if __name__ == "__main__":
    main()
