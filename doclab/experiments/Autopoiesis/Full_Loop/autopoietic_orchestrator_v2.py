#!/usr/bin/env python3
"""
autopoietic_orchestrator_v2.py

v2: shepherd-aware, loneliness-aware orchestration for Pirouette v7.

Flow:
1. pick emitter:
   - if next_seeds.json or lonely_rank.json exists -> emit_from_lonely_v7.py
   - else -> emit_high_residue_stubs_3.py (atlas-based)
2. for each stub:
   - build_context.py
   - weaver_5.py (openai/gemini)
   - ratify.py
3. end-of-cycle:
   - merge_and_rank_loneliness.py
   - rank_vocab_loneliness.py
   - score_shepherd_alignment.py
   - select_next_shepherd_terms.py

This lets the system BOTH:
- maintain the framework (loneliness)
- steer toward a goal (shepherd)
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
    ap.add_argument("--top", type=int, default=10, help="how many stubs to emit this run")
    ap.add_argument("--cycles", type=int, default=1)
    ap.add_argument("--shepherd", default="altruism", help="steering phrase, e.g. 'altruism', 'QED-SPINE'")
    ap.add_argument("--do-rank", action="store_true", help="re-run lonelies and shepherd scores at the end")
    # for selecting next seeds
    ap.add_argument("--w-lonely", type=float, default=0.6)
    ap.add_argument("--w-shepherd", type=float, default=0.4)
    args = ap.parse_args()

    stubs_dir = Path(args.stubs_dir)
    contexts_dir = Path(args.contexts_dir)
    authored_dir = Path(args.authored_dir)
    for d in (stubs_dir, contexts_dir, authored_dir):
        d.mkdir(parents=True, exist_ok=True)

    # 1) decide which emitter to use
    next_seeds = Path("next_seeds.json")
    lonely_list = Path("lonely_rank.json")
    if next_seeds.exists():
        # we have preselected seeds: emit exactly those
        run([
            sys.executable, "emit_from_lonely_v7.py",
            "--lonely", str(next_seeds),
            "--outdir", str(stubs_dir),
            "--shepherd", args.shepherd,
            "--authored", str(authored_dir),
            "--top", str(args.top),
        ])
    elif lonely_list.exists():
        # emit from current loneliness list
        run([
            sys.executable, "emit_from_lonely_v7.py",
            "--lonely", str(lonely_list),
            "--outdir", str(stubs_dir),
            "--shepherd", args.shepherd,
            "--authored", str(authored_dir),
            "--top", str(args.top),
        ])
    else:
        # fallback: atlas-based
        run([
            sys.executable, "emit_high_residue_stubs_3.py",
            "--atlas", args.atlas,
            "--outdir", str(stubs_dir),
            "--shepherd", args.shepherd,
            "--top", str(args.top),
            "--cycles", str(args.cycles),
        ])

    # 2) per-stub processing
    for stub_path in sorted(stubs_dir.glob("*.md")):
        stub_name = stub_path.stem
        ctx_path = contexts_dir / f"{stub_name}_context.txt"

        # you asked to name things with shepherd in mind; keep authored name simple but distinct
        out_module_path = authored_dir / f"{args.shepherd.upper()}_{stub_name}_v7.md"

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

    # 5) end-of-cycle re-rank + shepherd steering
    if args.do_rank:
        # module side: refresh loneliness
        if Path("lonely_rank.json").exists():
            Path("lonely_rank.prev.json").write_text(
                Path("lonely_rank.json").read_text(encoding="utf-8"),
                encoding="utf-8"
            )

        run([
            sys.executable, "merge_and_rank_loneliness.py",
            "--old", "canon",
            "--new", str(authored_dir),
            "--atlas", args.atlas,
            "--out", "lonely_rank.json",
        ])

        # vocab side:
        if Path(args.dictpack).is_dir():
            run([
                sys.executable, "rank_vocab_loneliness.py",
                "--vocab-dir", args.dictpack,
                "--out", "vocab_lonely.json",
            ])

        # shepherd alignment (how on-topic were we?)
        run([
            sys.executable, "score_shepherd_alignment.py",
            "--shepherd", args.shepherd,
            "--modules", str(authored_dir),
            "--canon", "canon",
            "--out", "shepherd_alignment.json",
        ])

        # choose next seeds using BOTH loneliness + shepherd
        run([
            sys.executable, "select_next_shepherd_terms.py",
            "--lonely", "lonely_rank.json",
            "--shepherd-align", "shepherd_alignment.json",
            "--out", "next_seeds.json",
            "--top", str(args.top),
            "--w-lonely", str(args.w_lonely),
            "--w-shepherd", str(args.w_shepherd),
        ])

    print("[orchestrator] done, v2 loop complete.")


if __name__ == "__main__":
    main()
