#!/usr/bin/env python
"""
Summarize triad_explorer results across subjects.

By default, prints all triads. Use --triad 5 7 12 to focus on that one.
"""

import json
import re
from pathlib import Path
import argparse


def parse_subject_task_from_dir(dir_name: str):
    """
    dir_name looks like: sub-1_ses-1_task-NB_explorer_results
    """
    m_sub = re.search(r"(sub-[^_]+)", dir_name)
    m_ses = re.search(r"(ses-[^_]+)", dir_name)
    m_task = re.search(r"(task-[^_]+)", dir_name)
    sub = m_sub.group(1) if m_sub else "sub-UNK"
    ses = m_ses.group(1) if m_ses else "ses-UNK"
    task = m_task.group(1) if m_task else "task-UNK"
    return sub, ses, task


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--base",
        required=True,
        help="Base derivatives dir (e.g. ...\\Executive_Functioning_Data\\derivatives\\pirouette_gamma)",
    )
    ap.add_argument(
        "--triad",
        nargs=3,
        type=float,
        help="Optional triad to filter on, e.g. --triad 5 7 12",
    )
    args = ap.parse_args()

    base = Path(args.base)

    rows = []
    for json_path in base.rglob("explorer_triad-*.json"):
        try:
            data = json.loads(json_path.read_text())
        except Exception as e:
            print(f"! Failed to read {json_path}: {e}")
            continue

        triad = data.get("triad")
        if triad is None or len(triad) != 3:
            continue

        if args.triad:
            # compare as floats with small tolerance
            target = args.triad
            if any(abs(t - triad[i]) > 1e-3 for i, t in enumerate(target)):
                continue

        dir_name = json_path.parent.name
        sub, ses, task = parse_subject_task_from_dir(dir_name)

        rows.append(
            dict(
                subject=sub,
                session=ses,
                task=task,
                triad=triad,
                tmin=data.get("t_min_window"),
                tmax=data.get("t_max_window"),
                tpci_low=data.get("tpci_low_load"),
                tpci_high=data.get("tpci_high_load"),
                diff=data.get("tpci_diff_high_minus_low"),
                p=data.get("perm_p_value"),
                n_low=data.get("n_epochs_low"),
                n_high=data.get("n_epochs_high"),
            )
        )

    if not rows:
        print("No matching triad_explorer results found.")
        return

    # Sort: triad, then subject, then p-value
    rows.sort(key=lambda r: (tuple(r["triad"]), r["subject"], r["p"]))

    # Print header
    print(
        "subject  session  task     triad        twin(s)      low     high    diff     p       n_low n_high"
    )
    print("-" * 100)
    for r in rows:
        tri = r["triad"]
        twin = f"{r['tmin']:.3f}-{r['tmax']:.3f}" if r["tmin"] is not None else "NA"
        print(
            f"{r['subject']:7s} {r['session']:7s} {r['task']:7s} "
            f"{tri[0]:4.1f}-{tri[1]:4.1f}-{tri[2]:4.1f}  "
            f"{twin:11s}  "
            f"{r['tpci_low']:.3f}  {r['tpci_high']:.3f}  {r['diff']:+.3f}  "
            f"{r['p']:.4f}  "
            f"{int(r['n_low']):5d} {int(r['n_high']):6d}"
        )


if __name__ == "__main__":
    main()
