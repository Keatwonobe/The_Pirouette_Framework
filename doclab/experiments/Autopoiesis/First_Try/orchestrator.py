
"""
orchestrator.py — Pirouette Autopoietic Orchestrator (patched)
Fixes:
- Use Path(<dir>).glob(<pattern>) for absolute directories (Windows-safe)
- More robust latest_file() with graceful None handling
"""

import os
import json
import subprocess
from pathlib import Path
from typing import List, Optional

# Paths (adjust as needed)
ROOT = Path(".").resolve()
MODULES_MD = str(ROOT / "pirouette_version_6.md")  # uploaded
PAPERS_DIR = str(ROOT / "generated_papers")
MANIFESTOS_DIR = str(ROOT / "generated_manifestos")
GRAND_OUT_DIR = str(ROOT / "grand_manifesto_out")
DISCOVERY_OUT = str(ROOT / "discovery_out")
DEBATE_OUT = str(ROOT / "debate_out")

# Script entry points
DISCOVERY = str(ROOT / "discovery_engine.py")
DEBATE = str(ROOT / "debate_orchestrator.py")
PAPER_SYNTH = str(ROOT / "paper_synthesizer.py")
MANIFESTO = str(ROOT / "manifesto_constructor.py")
GRAND = str(ROOT / "grand_manifesto.py")
RATIFY = str(ROOT / "ratify.py")  # your uploaded script

def run(cmd: List[str]):
    print("▶", " ".join(cmd))
    subprocess.run(cmd, check=True)

def latest_file(dir_path: str, pattern: str) -> Optional[Path]:
    """
    Windows-safe "latest file" that accepts a directory and a pattern.
    """
    d = Path(dir_path)
    if not d.exists():
        return None
    files = sorted(d.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
    return files[0] if files else None

def discovery_stage() -> Optional[Path]:
    run(["python", DISCOVERY])
    return latest_file(DISCOVERY_OUT, "DPK_*.md")

def formalization_debate(dossier_path: str):
    run(["python", DEBATE, dossier_path, "--stage", "Formalization Debate"])
    if Path(RATIFY).exists():
        print("ⓘ Ratify step available; you can call it here if desired.")

def philosophy_debate(dossier_path: str):
    run(["python", DEBATE, dossier_path, "--stage", "Philosophy Debate"])

def papers_stage(n_papers: int = 5):
    Path(PAPERS_DIR).mkdir(parents=True, exist_ok=True)
    for i in range(n_papers):
        run(["python", PAPER_SYNTH, MODULES_MD, "--out", PAPERS_DIR, "--theme", f"Resonant Unification {i+1}", "--index", str(i)])

def manifestos_stage(n_manifestos: int = 2):
    Path(MANIFESTOS_DIR).mkdir(parents=True, exist_ok=True)
    for i in range(n_manifestos):
        run(["python", MANIFESTO, PAPERS_DIR, "--out", MANIFESTOS_DIR, "--title", f"Manifesto {i+1}: Resonant Unification", "--index", str(i)])

def grand_manifesto_stage(title="A Time-First Unification") -> Path:
    run(["python", GRAND, MANIFESTOS_DIR, "--title", title])
    return Path(GRAND_OUT_DIR) / "grand_manifesto.md"

def governance_stage(artifact_path: str):
    run(["python", DEBATE, artifact_path, "--stage", "Governance Debate", "--governance"])

def main():
    import argparse
    p = argparse.ArgumentParser(description="Run the full Pirouette autopoietic loop.")
    p.add_argument("--skip_discovery", action="store_true")
    p.add_argument("--skip_debates", action="store_true")
    p.add_argument("--papers", type=int, default=5)
    p.add_argument("--manifestos", type=int, default=2)
    p.add_argument("--title", default="A Time-First Unification")
    args = p.parse_args()


    # 1) Discovery
    if not args.skip_discovery:
        dpk_path = discovery_stage()
        if dpk_path:
            print(f"✓ Latest Discovery Pack: {dpk_path}")
            if not args.skip_debates:
                formalization_debate(str(dpk_path))
        else:
            print("⚠ No Discovery Pack found; continuing.")

    # 2) Philosophy Debate (optional; on latest DPK if present)
    if not args.skip_debates:
        dpk_latest = latest_file(DISCOVERY_OUT, "DPK_*.md")
        if dpk_latest:
            philosophy_debate(str(dpk_latest))

    # 3) Papers -> Manifestos -> Grand
    papers_stage(n_papers=args.papers)
    manifestos_stage(n_manifestos=args.manifestos)
    grand = grand_manifesto_stage(title=args.title)

    # 4) Governance Debate on Grand Manifesto
    if not args.skip_debates and grand.exists():
        governance_stage(str(grand))

    print("\n✅ Orchestration complete.")
    print(f"Artifacts:\n- Papers: {PAPERS_DIR}\n- Manifestos: {MANIFESTOS_DIR}\n- Grand: {grand}")

if __name__ == "__main__":
    main()
