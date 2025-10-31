import argparse, json, os, re, sys, math
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.signal import iirnotch, filtfilt
import mne
from scipy.signal import butter, sosfiltfilt, hilbert

# -------------------------- Config -------------------------- #
CONFIG = {
    # Bands: name -> (low, high, center_Hz)
    "bands": {
        "theta": (4, 7, 5.5),
        "alpha": (8, 12, 10.0),
        "beta":  (13, 30, 21.5),
        "gamma": (31, 45, 38.0),
    },
    "epoch_tmin": -0.5,   # seconds
    "epoch_tmax":  1.0,
    "baseline":    (-0.4, -0.05),   # for ΔP (% change vs baseline)
    "hp_cut": 1.0,        # additional high-pass (Hz), matches sidecar's ~1 Hz
    "notch": 50.0,        # Hz (per sidecar)
    "q_notch": 30.0,      # notch Q factor
    "downsample": None,   # e.g., 128 if you want speed; None keeps native
    # Archetype thresholds (tune!)
    "kappa_lo": 0.15,
    "kappa_hi": 0.40,
    "deltaP_lo": 0.05,    # 5% up from baseline is "gain"
    # ROI (optional): list of regexes; if empty, median over all channels
    "roi_patterns": [],   # e.g., ["^Fz$", "^F[3-7]$"]
}

# --------------------- Utility / IO ------------------------- #
def natural_sort_key(s):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', str(s))]

def list_subjects(root: Path, subjects_arg):
    # supports "1..24" or explicit list
    if subjects_arg and len(subjects_arg)==1 and ".." in subjects_arg[0]:
        a,b = subjects_arg[0].split("..")
        return [f"sub-{i}" for i in range(int(a), int(b)+1)]
    if subjects_arg:
        return [f"sub-{int(s)}" if s.isdigit() else s for s in subjects_arg]
    # fallback: scan
    return sorted([p.name for p in root.glob("sub-*") if p.is_dir()], key=natural_sort_key)

def ensure_dirs(out_root: Path):
    (out_root / "checkpoints").mkdir(parents=True, exist_ok=True)
    (out_root / "results").mkdir(parents=True, exist_ok=True)

def load_sidecar_json(json_path: Path):
    if json_path.exists():
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def notch_filter(data, sfreq, freq=50.0, q=30.0):
    # data: (n_channels, n_times)
    b, a = iirnotch(w0=freq/(sfreq/2), Q=q)
    return filtfilt(b, a, data, axis=-1)

def compute_analytic_band(epoch_data, sfreq, f_lo, f_hi):
    """
    IIR (Butterworth) band-pass + Hilbert to get complex analytic signal.
    epoch_data: (n_channels, n_times) float
    returns: complex analytic array, shape (n_channels, n_times)
    """
    nyq = 0.5 * sfreq
    wp = [f_lo / nyq, f_hi / nyq]

    # Order heuristics: shorter windows → lower order
    n_times = epoch_data.shape[-1]
    # For ~1–2 s windows at 128–256 Hz, order 4–6 is a good sweet spot
    order = 4 if n_times < 1.5 * sfreq else 6

    sos = butter(order, wp, btype='bandpass', output='sos')
    # Pad to reduce edge transients
    padlen = min(3 * int(sfreq // 2), max(0, n_times // 2))

    # Filter channel-wise
    bp = sosfiltfilt(sos, epoch_data, axis=-1, padlen=padlen)
    # Analytic signal per channel
    z = hilbert(bp, axis=-1)
    return z

def inner_prod(a, b):
    # L2 inner product over time axis (-1)
    return np.sum(np.conj(a) * b, axis=-1)

def kappa_estimator(z, sfreq, band_center_hz):
    """
    z: complex analytic, shape (n_channels, n_times)
    derivative via centered finite difference
    """
    dt = 1.0 / sfreq
    # time derivative z'
    zp = np.gradient(z, dt, axis=-1)
    omega = 2.0 * np.pi * band_center_hz  # rad/s
    num = np.imag(inner_prod(zp, z))      # Im <z', z>
    den = omega * np.real(inner_prod(z, z)) + 1e-12
    kappa = - num / den
    return kappa   # per-channel

def robust_aggregate(values, ch_names, roi_patterns):
    vals = np.asarray(values)
    if not roi_patterns:
        return np.nanmedian(vals)
    # ROI: union of channels matching any pattern
    import re as _re
    sel = np.zeros(len(ch_names), dtype=bool)
    for pat in roi_patterns:
        r = _re.compile(pat)
        sel |= np.array([bool(r.search(c)) for c in ch_names])
    if not sel.any():
        return np.nanmedian(vals)
    return np.nanmedian(vals[sel])

def classify_archetype(kappa_abs, deltaP, cfg):
    if kappa_abs <= cfg["kappa_lo"] and deltaP >= cfg["deltaP_lo"]:
        return "Weaver"
    if kappa_abs >  cfg["kappa_hi"] and deltaP >= cfg["deltaP_lo"]:
        return "Gladiator"
    if kappa_abs <= cfg["kappa_lo"] and deltaP <  cfg["deltaP_lo"]:
        return "Drifter"
    if kappa_abs >  cfg["kappa_hi"] and deltaP <  cfg["deltaP_lo"]:
        return "Vortex"
    # gray zone
    return "Borderline"

def pct_change(new, base):
    return (new - base) / (base + 1e-12)

# ---------------------- Main pipeline ----------------------- #
def process_task(root, out_root, subject, ses, task, resume, cfg):
    ses_dir = root / subject / f"ses-{ses}" / "eeg"
    if not ses_dir.exists():
        return []
    # Filenames (BIDS-ish)
    stem = f"{subject}_ses-{ses}_task-{task}"
    set_path = ses_dir / f"{stem}_eeg.set"
    evt_tsv  = ses_dir / f"{stem}_events.tsv"
    ch_tsv   = ses_dir / f"{stem}_channels.tsv"
    json_path= ses_dir / f"{stem}_eeg.json"

    if not set_path.exists():
        return []

    # Checkpoint state
    ckpt_path = out_root / "checkpoints" / f"{stem}_progress.json"
    if resume and ckpt_path.exists():
        with open(ckpt_path, "r", encoding="utf-8") as f:
            state = json.load(f)
    else:
        state = {"last_event_index": -1}

    results_path = out_root / "results" / "helical_epochs.csv"
    summary_path = out_root / "results" / "helical_summary.csv"
    # load metadata
    sidecar = load_sidecar_json(json_path)
    # Respect sampling; fall back to raw info if missing
    # (Your sample shows SamplingFrequency=256, notch=50)  # sidecar-cited

    # Read raw EEGLAB
    raw = mne.io.read_raw_eeglab(set_path, preload=True, verbose=False)
    raw.pick('eeg', exclude='bads')
    # Optional resample to speed
    sfreq = float(raw.info["sfreq"])
    if CONFIG["downsample"] and CONFIG["downsample"] < sfreq:
        raw.resample(CONFIG["downsample"])
        sfreq = CONFIG["downsample"]

    # Notch + HP (if present in sidecar / config)
    if CONFIG["notch"]:
        data = raw.get_data()
        data = notch_filter(data, sfreq, freq=CONFIG["notch"], q=CONFIG["q_notch"])
        raw._data = data
    if CONFIG["hp_cut"] and CONFIG["hp_cut"] > 0:
        raw.filter(CONFIG["hp_cut"], None, method="fir", phase="zero", verbose=False)

    # Events: prefer TSV if present to preserve codes/onsets
    if evt_tsv.exists():
        events_df = pd.read_csv(evt_tsv, sep="\t")
        # Expect 'onset' (seconds) and 'value' (str/int)
        if "onset" not in events_df.columns:
            raise RuntimeError(f"events.tsv missing 'onset': {evt_tsv}")
        # Build MNE events array: onset_samples, 0, code
        onsets_samp = (events_df["onset"].values * sfreq).astype(int)
        # Create stable numeric codes
        codes, uniques = pd.factorize(events_df.get("value", pd.Series(np.arange(len(events_df)))), sort=True)
        mne_events = np.c_[onsets_samp, np.zeros_like(onsets_samp), codes + 1]
        event_id = {str(u): i+1 for i, u in enumerate(uniques)}
    else:
        mne_events, event_id = mne.events_from_annotations(raw, verbose=False)

    # Channels (optional; for ROI)
    ch_names = raw.info["ch_names"]

    # Epoching
    epochs = mne.Epochs(raw, mne_events, event_id=event_id,
                        tmin=CONFIG["epoch_tmin"], tmax=CONFIG["epoch_tmax"],
                        baseline=None, preload=True, detrend=1, verbose=False)

    # Baseline mask
    times = epochs.times
    b0, b1 = CONFIG["baseline"]
    bmask = (times >= b0) & (times <= b1)

    # Iterate events with resume
    start_idx = state.get("last_event_index", -1) + 1
    n_events = len(epochs)

    rows = []
    srows = []

    for ei in range(start_idx, n_events):
        ep = epochs.get_data()[ei]  # shape (n_channels, n_times)
        # Optionally reject bad epochs here

        # For each band: analytic, kappa, power, ΔP, classify
        for bname, (f_lo, f_hi, f_c) in CONFIG["bands"].items():
            z = compute_analytic_band(ep, sfreq, f_lo, f_hi)  # complex (ch, t)
            kap = kappa_estimator(z, sfreq, f_c)              # per channel
            # power over full post-event window vs baseline
            P_full = np.mean(np.abs(z)**2, axis=-1)           # per channel
            P_base = np.mean(np.abs(z[:, bmask])**2, axis=-1)

            # aggregate (median or ROI)
            kap_med  = robust_aggregate(kap, ch_names, CONFIG["roi_patterns"])
            P_med    = robust_aggregate(P_full, ch_names, CONFIG["roi_patterns"])
            Pb_med   = robust_aggregate(P_base, ch_names, CONFIG["roi_patterns"])
            dP       = pct_change(P_med, Pb_med)

            arche = classify_archetype(abs(kap_med), dP, CONFIG)

            # record detailed row
            rows.append({
                "subject": subject, "session": f"ses-{ses}", "task": task,
                "event_index": ei, "event_label": epochs.events[ei, 2],
                "band": bname, "sfreq": sfreq,
                "kappa": kap_med, "kappa_abs": abs(kap_med),
                "power": P_med, "power_baseline": Pb_med, "delta_power": dP,
                "archetype": arche,
            })

        # summary (majority vote across bands by archetype; tie -> Borderline)
        df_e = pd.DataFrame([r for r in rows if r["event_index"]==ei and r["subject"]==subject and r["task"]==task])
        top = df_e["archetype"].value_counts()
        arch_summary = top.index[0] if len(top)>0 else "Borderline"
        srows.append({
            "subject": subject, "session": f"ses-{ses}", "task": task,
            "event_index": ei, "event_label": epochs.events[ei, 2],
            "archetype": arch_summary,
            "kappa_abs_med": df_e["kappa_abs"].median(),
            "delta_power_med": df_e["delta_power"].median(),
        })

        # append to disk every N events for safety
        if (ei % 10 == 0) or (ei == n_events - 1):
            if rows:
                pd.DataFrame(rows).to_csv(results_path, mode="a", index=False,
                                          header=not results_path.exists())
                rows.clear()
            if srows:
                pd.DataFrame(srows).to_csv(summary_path, mode="a", index=False,
                                           header=not summary_path.exists())
                srows.clear()
            # update checkpoint
            state["last_event_index"] = ei
            with open(ckpt_path, "w", encoding="utf-8") as f:
                json.dump(state, f)

    return []

# ---------------------- New Debugging Function ----------------------- #
def log_events_for_task(root, out_root, subject, ses, task, cfg):
    """
    A debugging function that only loads data, finds events, and logs them to a CSV.
    This helps verify that events are being detected correctly in each file.
    """
    ses_dir = root / subject / f"ses-{ses}" / "eeg"
    stem = f"{subject}_ses-{ses}_task-{task}"
    set_path = ses_dir / f"{stem}_eeg.set"
    evt_tsv  = ses_dir / f"{stem}_events.tsv"

    if not set_path.exists():
        print(f"SKIPPING: EEG file not found for {stem}")
        return

    # Prepare log file
    log_path = out_root / "results" / "event_log.csv"
    
    try:
        raw = mne.io.read_raw_eeglab(set_path, preload=False, verbose=False) # No need to preload data
        sfreq = float(raw.info["sfreq"])

        # Events: prefer TSV if present
        if evt_tsv.exists():
            events_df = pd.read_csv(evt_tsv, sep="\t")
            onsets_samp = (events_df["onset"].values * sfreq).astype(int)
            codes, uniques = pd.factorize(events_df.get("value", pd.Series(np.arange(len(events_df)))), sort=True)
            mne_events = np.c_[onsets_samp, np.zeros_like(onsets_samp), codes + 1]
            event_id = {str(u): i+1 for i, u in enumerate(uniques)}
        else:
            mne_events, event_id = mne.events_from_annotations(raw, verbose=False)

        if len(mne_events) == 0:
            print(f"WARNING: No events found for {stem}")
            return

        # Create a reverse mapping from ID to human-readable label
        id_to_label = {v: k for k, v in event_id.items()}

        rows = []
        for i, event in enumerate(mne_events):
            event_sample, _, event_code = event
            rows.append({
                "subject": subject,
                "session": f"ses-{ses}",
                "task": task,
                "event_index": i,
                "onset_sample": event_sample,
                "onset_sec": event_sample / sfreq,
                "event_code": event_code,
                "event_label": id_to_label.get(event_code, "N/A")
            })
        
        # Save results for this file
        pd.DataFrame(rows).to_csv(log_path, mode="a", index=False, header=not log_path.exists())
        print(f"SUCCESS: Logged {len(rows)} events for {stem}")

    except Exception as e:
        # Log any other errors during file loading
        errlog = out_root / "results" / "errors.log"
        with open(errlog, "a", encoding="utf-8") as f:
            f.write(f"EVENT_LOGGING - {subject},{ses},{task}: {repr(e)}\n")
        print(f"ERROR: Failed to process {stem}. See errors.log.")

def main():
    ap = argparse.ArgumentParser(description="Helical κ EEG event-wise pipeline with resume.")
    ap.add_argument("--root", required=True, help="BIDS-like root folder")
    ap.add_argument("--out", default=None, help="Output folder (defaults to <root>/helical_out)")
    ap.add_argument("--tasks", nargs="+", default=["LG","NB","SART"])
    ap.add_argument("--subjects", nargs="*", default=None, help="List like 1 2 3 or range '1..24'")
    ap.add_argument("--sessions", nargs="*", default=None, help="e.g., 1 or 1 2; defaults to all ses-* present")
    ap.add_argument("--resume", action="store_true")
    args = ap.parse_args()

    root = Path(args.root)
    out_root = Path(args.out) if args.out else (root / "helical_out")
    ensure_dirs(out_root)

    subjects = list_subjects(root, args.subjects)

    for subj in subjects:
        subj_dir = root / subj
        ses_dirs = sorted([p for p in subj_dir.glob("ses-*") if p.is_dir()], key=natural_sort_key)
        if args.sessions:
            ses_dirs = [subj_dir / f"ses-{s}" for s in args.sessions]
        for ses_dir in ses_dirs:
            m = re.match(r"ses-(\w+)", ses_dir.name)
            ses = m.group(1) if m else "1"
            for task in args.tasks:
                try:
                    process_task(root, out_root, subj, ses, task, args.resume, CONFIG)
                    log_events_for_task(root, out_root, subj, ses, task, CONFIG)
                except Exception as e:
                    # log and continue to next file
                    errlog = out_root / "results" / "errors.log"
                    with open(errlog, "a", encoding="utf-8") as f:
                        f.write(f"{subj},{ses},{task}: {repr(e)}\n")
                    continue

if __name__ == "__main__":
    main()
