#!/usr/bin/env python3
"""
autopoietic_orchestrator.py

Runs the full v7 Pirouette loop:

1. emit stubs from atlas
2. build context for each stub
3. author modules (OpenAI or Gemini)
4. ratify/sort
5. (optional) re-rank

Assumes you already have these scripts in the same folder:
- emit_high_residue_stubs_v7.py
- build_context.py
- weaver_5.py
- ratify.py
- (optional) merge_and_rank_loneliness.py / rank_vocab_loneliness.py
"""

import subprocess
from pathlib import Path
import argparse
import sys
import json

def run(cmd: list[str]):
    print(f"[orchestrator] $ {' '.join(cmd)}")
    r = subprocess.run(cmd, text=True)
    if r.returncode != 0:
        print(f"[orchestrator] step failed: {' '.join(cmd)}")
        sys.exit(r.returncode)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--atlas", required=True, help="dde_glob_manifest_modules_outbox.json")
    ap.add_argument("--stubs-dir", default="autopoiesis_runs/stubs")
    ap.add_argument("--contexts-dir", default="autopoiesis_runs/contexts")
    ap.add_argument("--authored-dir", default="autopoiesis_runs/authored")
    ap.add_argument("--dictpack", default="vocab_terms", help="folder of term .md files OR dictpack file")
    ap.add_argument("--essentialized", default="essentialized_modules", help="folder of essentialized .md files OR single file")
    ap.add_argument("--provider", choices=["openai", "gemini"], default="openai")
    ap.add_argument("--openai-model", default="gpt-5")
    ap.add_argument("--gemini-model", default="gemini-2.5-pro")
    ap.add_argument("--top", type=int, default=25, help="how many stubs to emit this run")
    ap.add_argument("--cycles", type=int, default=1)
    ap.add_argument("--shepherd", default="altruism")
    ap.add_argument("--do-rank", action="store_true", help="re-run lonelies at the end")
    args = ap.parse_args()

    stubs_dir = Path(args.stubs_dir)
    contexts_dir = Path(args.contexts_dir)
    authored_dir = Path(args.authored_dir)
    for d in (stubs_dir, contexts_dir, authored_dir):
        d.mkdir(parents=True, exist_ok=True)

    # 1) emit stubs
    run([
        sys.executable, "emit_high_residue_stubs_3.py",
        "--atlas", args.atlas,
        "--outdir", str(stubs_dir),
        "--shepherd", args.shepherd,
        "--top", str(args.top),
        "--cycles", str(args.cycles),
    ])

    # 2) for each stub, build context + author + ratify
    for stub_path in sorted(stubs_dir.glob("*.md")):
        stub_name = stub_path.stem
        ctx_path = contexts_dir / f"{stub_name}_context.txt"
        out_module_path = authored_dir / f"{stub_name}_3.md"

        # 2a) build context
        run([
            sys.executable, "build_context.py",
            "--stub", str(stub_path),
            "--dictpack", args.dictpack,
            "--essentialized", args.essentialized,
            "--out", str(ctx_path),
        ])

        # 3) author
        author_cmd = [
            sys.executable, "weaver_5.py",
            "--stub", str(stub_path),
            "--context", str(ctx_path),
            "--out", str(out_module_path),
            "--provider", args.provider,
        ]
        if args.provider == "openai":
            author_cmd.extend(["--openai-model", args.openai_model])
        else:
            author_cmd.extend(["--gemini-model", args.gemini_model])
        run(author_cmd)

        # 4) ratify/sort
        run([
            sys.executable, "ratify.py",
            "--module", str(out_module_path),
            "--atlas", args.atlas,
        ])

    # 5) (optional) re-rank at the end
    if args.do_rank:
        # module side
        if Path("lonely_rank.json").exists():
            Path("lonely_rank.prev.json").write_text(Path("lonely_rank.json").read_text(encoding="utf-8"), encoding="utf-8")
        run([
            sys.executable, "merge_and_rank_loneliness.py",
            "--old", "canon",            # you may need to adjust to your canon folder
            "--new", str(authored_dir),  # freshly authored
            "--atlas", args.atlas,
            "--out", "lonely_rank.json",
        ])
        # vocab side
        if Path(args.dictpack).is_dir():
            run([
                sys.executable, "rank_vocab_loneliness.py",
                "--vocab-dir", args.dictpack,
                "--out", "vocab_lonely.json",
            ])

    print("[orchestrator] done.")

if __name__ == "__main__":
    main()
