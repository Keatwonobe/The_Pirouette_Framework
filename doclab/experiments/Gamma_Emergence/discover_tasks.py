# File: 1_discover_tasks.py
import re, pathlib, argparse
import pandas as pd

def find_eeg_and_events(task_dir, subj, ses, task):
    """Finds matching EEG and events files for a given task."""
    d = pathlib.Path(task_dir)
    eeg_files = []
    for ext in (".bdf", ".set", ".edf"):
        eeg_files += list(d.glob(f"sub-{subj}_ses-{ses}_task-{task}*{ext}"))
    if not eeg_files:
        for ext in (".bdf", ".set", ".edf"):
            eeg_files += list(d.glob(f"*task-{task}*{ext}"))
    ev_files = list(d.glob(f"sub-{subj}_ses-{ses}_task-{task}_events.tsv"))
    if not ev_files:
        ev_files = list(d.glob(f"*task-{task}*_events.tsv"))
    return (eeg_files[0] if eeg_files else None), (ev_files[0] if ev_files else None)

def main():
    """
    Scans a BIDS-like root directory to find all (EEG, events.tsv) pairs
    and saves them to a CSV file for later processing.
    """
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="Root of the BIDS dataset (e.g., Executive_Functioning_Data)")
    ap.add_argument("--out-csv", default="tasks_to_process.csv", help="Output CSV file listing tasks to run.")
    args = ap.parse_args()

    rootp = pathlib.Path(args.root)
    entries = []
    print(f"🔍 Scanning for tasks in: {rootp}")

    for subdir in rootp.glob("sub-*"):
        subj = subdir.name.split("-")[-1]
        for sesdir in subdir.glob("ses-*"):
            ses = sesdir.name.split("-")[-1]
            eegdir = sesdir / "eeg"
            if not eegdir.exists():
                continue
            
            # Find all unique tasks from event files
            tasks = set()
            for ev in eegdir.glob("*_events.tsv"):
                m = re.search(r"task-([A-Za-z0-9]+)", ev.name)
                if m:
                    tasks.add(m.group(1))
            
            for task in sorted(tasks):
                eeg_path, ev_path = find_eeg_and_events(eegdir, subj, ses, task)
                if ev_path and eeg_path:
                    entries.append({
                        "eeg_path": str(eeg_path.resolve()),
                        "events_path": str(ev_path.resolve())
                    })

    if not entries:
        print("❌ No valid (EEG, events.tsv) pairs found.")
        return

    df = pd.DataFrame(entries)
    df.to_csv(args.out_csv, index=False)
    print(f"✅ Found {len(df)} tasks. Saved list to '{args.out_csv}'.")

if __name__ == "__main__":
    main()