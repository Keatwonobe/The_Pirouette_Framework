#!/usr/bin/env python3
"""
ratify_biz.py

The Portfolio Manager for the Busiod Engine.
Scans generated Business Triad modules, extracts "Money Column" scores,
and compiles a Strategic Manifest (CSV) for analysis.
"""

import os
import re
import csv
import argparse
from pathlib import Path
from typing import List, Dict, Any

# Regex patterns for the "Money Columns"
PATTERNS = {
    "id": re.compile(r"^id:\s*(.+)$", re.MULTILINE | re.IGNORECASE),
    "title": re.compile(r"^title:\s*(.+)$", re.MULTILINE | re.IGNORECASE),
    "type": re.compile(r"^type:\s*(.+)$", re.MULTILINE | re.IGNORECASE),
    "passive": re.compile(r"^passive_score:\s*(\d+)", re.MULTILINE | re.IGNORECASE),
    "complexity": re.compile(r"^complexity_score:\s*(\d+)", re.MULTILINE | re.IGNORECASE),
    "scalability": re.compile(r"^scalability_score:\s*(\d+)", re.MULTILINE | re.IGNORECASE),
    "sector": re.compile(r"^sector:\s*(.+)$", re.MULTILINE | re.IGNORECASE),
    "probe_cost": re.compile(r"^probe_cost_est:\s*(.+)$", re.MULTILINE | re.IGNORECASE),
    "probe_time": re.compile(r"^probe_time_est:\s*(.+)$", re.MULTILINE | re.IGNORECASE),
}

def extract_metadata(text: str) -> Dict[str, Any]:
    data = {}
    for key, pattern in PATTERNS.items():
        m = pattern.search(text)
        if m:
            val = m.group(1).strip().strip('"').strip("'")
            # Convert numbers to ints for sorting
            if key in ["passive", "complexity", "scalability"]:
                try:
                    data[key] = int(val)
                except ValueError:
                    data[key] = 0
            else:
                data[key] = val
        else:
            # Defaults
            if key in ["passive", "complexity", "scalability"]:
                data[key] = 0
            else:
                data[key] = "UNKNOWN"
    return data

def calculate_grade(data: Dict[str, Any]) -> str:
    """Assigns a strategic grade to the proposal."""
    p = data["passive"]
    c = data["complexity"]
    
    # The "Golden Goose": High Passive, Low Complexity
    if p >= 8 and c <= 4:
        return "A+ (Cash Cow)"
    # The "Engine": High Passive, High Complexity
    elif p >= 8 and c >= 7:
        return "A (Moonshot)"
    # The "Quick Win": Mid Passive, Low Complexity
    elif p >= 6 and c <= 3:
        return "B+ (Quick Win)"
    # The "Trap": Low Passive, High Complexity
    elif p <= 4 and c >= 7:
        return "F (Trap)"
    else:
        return "C (Standard)"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--proposals", default="ideas", help="Folder containing _BIZ.md files")
    ap.add_argument("--out", default="busiod_manifest.csv", help="Output CSV file")
    args = ap.parse_args()

    proposals_dir = Path(args.proposals)
    if not proposals_dir.exists():
        print(f"Error: Directory {proposals_dir} not found.")
        return

    records = []
    print(f"[ratify] scanning {proposals_dir}...")

    for f in proposals_dir.glob("*.md"):
        try:
            text = f.read_text(encoding="utf-8")
            meta = extract_metadata(text)
            meta["filename"] = f.name
            meta["grade"] = calculate_grade(meta)
            
            # Only add if it looks like a valid BIZ file
            if meta["id"] != "UNKNOWN":
                records.append(meta)
        except Exception as e:
            print(f"Skipping {f.name}: {e}")

    # Sort by Grade (A+ first), then Passive Score
    records.sort(key=lambda x: (x["grade"], x["passive"]), reverse=False) 
    # Note: String sort on Grade works loosely, but let's do explicit sort for clarity:
    # Custom sort order: A+, A, B+, C, F
    grade_order = {"A+ (Cash Cow)": 0, "A (Moonshot)": 1, "B+ (Quick Win)": 2, "C (Standard)": 3, "F (Trap)": 4}
    records.sort(key=lambda x: (grade_order.get(x["grade"], 5), -x["passive"]))

    # Write to CSV
    keys = ["id", "grade", "passive", "complexity", "scalability", "sector", "probe_cost", "probe_time", "title", "filename"]
    
    with open(args.out, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        for r in records:
            # Filter record to only keys we want
            row = {k: r.get(k, "") for k in keys}
            writer.writerow(row)

    print(f"[ratify] success. {len(records)} proposals indexed.")
    print(f"[ratify] manifest written to {args.out}")
    
    # Print a "Top 10" preview to console
    print("\n--- TOP 10 GOLDEN GEESE ---")
    print(f"{'ID':<25} | {'GRADE':<15} | {'P':<3} | {'C':<3} | {'SECTOR'}")
    print("-" * 70)
    for r in records[:15]:
        print(f"{r['id'][:25]:<25} | {r['grade']:<15} | {r['passive']:<3} | {r['complexity']:<3} | {r['sector']}")

if __name__ == "__main__":
    main()