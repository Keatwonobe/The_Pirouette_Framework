#!/usr/bin/env python
"""
Batch wrapper for triad_explorer.py

- Loops over all subjects / sessions in the Executive_Functioning_Data tree
- Runs the 3-pass explorer on every NB run it finds.
- Uses a per-run sentinel file so already-finished runs are skipped.
"""

import subprocess
from pathlib import Path

# Path to your Executive Functioning dataset root
EXEC_ROOT = Path(
    r"C:\Users\keatw\OneDrive\Documents\Doclab\Big_Datasets\target\paper\Executive_Functioning_Data"
)

# Base outdir (same one you've been using)
OUT_BASE = EXEC_ROOT / "derivatives" / "pirouette_gamma"

# Name of the explorer script (assumed to be in the same folder as this batch file)
TRIAD_EXPLORER = Path(__file__).with_name("triad_explorer.py")


def find_nb_runs():
    """
    Yield (eeg_path, events_path) for every NB run in the dataset.
    Looks for files like sub-*/ses-*/eeg/*task-NB*eeg.set
    """
    for sub_dir in EXEC_ROOT.glob("sub-*"):
        for ses_dir in sub_dir.glob("ses-*"):
            eeg_dir = ses_dir / "eeg"
            if not eeg_dir.exists():
                continue

            for eeg_path in eeg_dir.glob("*task-NB*eeg.set"):
                ev_path = eeg_path.with_name(
                    eeg_path.name.replace("_eeg.set", "_events.tsv")
                )
                if not ev_path.exists():
                    print(f"! Missing events for {eeg_path}")
                    continue
                yield eeg_path, ev_path


def get_output_dir_for_run(eeg_path: Path) -> Path:
    """
    Mirror triad_explorer's convention for the per-subject/task output dir.

    triad_explorer does:
      sub-<sub>_ses-<ses>_task-<task>_explorer_results

    It *doesn't* include the run ID, so multiple NB runs for the same sub/task
    share the same directory. That's fine: our sentinels will still be
    per-run files inside that folder.
    """
    name = eeg_path.name
    # crude parsing consistent with triad_explorer.py
    import re

    sub_match = re.search(r"sub-([0-9A-Za-z]+)", name)
    ses_match = re.search(r"ses-([0-9A-Za-z]+)", name)
    task_match = re.search(r"task-([A-Za-z0-9]+)", name)
    sub = sub_match.group(1) if sub_match else "NA"
    ses = ses_match.group(1) if ses_match else "NA"
    task = task_match.group(1) if task_match else "UNK"

    out_dir_for_file = OUT_BASE / f"sub-{sub}_ses-{ses}_task-{task}_explorer_results"
    return out_dir_for_file


def get_sentinel_path(eeg_path: Path) -> Path:
    """
    Per-run sentinel: lives inside that subject+task explorer dir and
    is named with the run's EEG stem.

    Example:
      eeg_path.stem = 'sub-1_ses-1_task-NB_run-2_eeg'
      sentinel name = 'done_sub-1_ses-1_task-NB_run-2_eeg.txt'
    """
    out_dir = get_output_dir_for_run(eeg_path)
    sentinel_name = f"done_{eeg_path.stem}.txt"
    return out_dir / sentinel_name


def run_one(eeg_path: Path, ev_path: Path):
    out_dir_for_file = get_output_dir_for_run(eeg_path)
    sentinel_path = get_sentinel_path(eeg_path)

    # If sentinel exists, this run was already successfully completed earlier.
    if sentinel_path.exists():
        print(f"=== Skipping (already done): {eeg_path.name} ===")
        return

    # Make sure the directory exists (triad_explorer will also do this, but it's cheap)
    out_dir_for_file.mkdir(parents=True, exist_ok=True)

    print(f"=== Running explorer on: {eeg_path.name} ===")

    cmd = [
        "python",
        str(TRIAD_EXPLORER),
        "--eeg-path",
        str(eeg_path),
        "--events-path",
        str(ev_path),
        "--outdir",
        str(OUT_BASE),
        "--tmin",
        "0.0",
        "--tmax",
        "1.0",
        "--highpass",
        "0.5",
        "--lowpass",
        "45.0",
        "--perm",
        "200",
        "--min-epochs",
        "2",
        # If you want ROI, uncomment and adjust:
        # "--roi", "Fz", "Cz", "Pz", "P3", "P4",
    ]

    try:
        # If triad_explorer crashes, we do NOT create the sentinel
        # so this run will be retried on the next batch invocation.
        subprocess.run(cmd, check=True)

    except subprocess.CalledProcessError as e:
        print(f"! Explorer FAILED on {eeg_path.name} with return code {e.returncode}")
        # Don't raise; just log and move on to the next run
        return

    # If we got here, the explorer finished without raising
    # Mark this run as done
    try:
        sentinel_path.write_text(
            f"Completed triad_explorer for {eeg_path.name}\n"
            f"EEG: {eeg_path}\n"
            f"Events: {ev_path}\n"
        )
    except Exception as e:
        print(f"! Warning: could not write sentinel for {eeg_path.name}: {e}")


def main():
    OUT_BASE.mkdir(parents=True, exist_ok=True)
    any_found = False

    for eeg_path, ev_path in find_nb_runs():
        any_found = True
        run_one(eeg_path, ev_path)

    if not any_found:
        print("No NB runs found under", EXEC_ROOT)


if __name__ == "__main__":
    main()
