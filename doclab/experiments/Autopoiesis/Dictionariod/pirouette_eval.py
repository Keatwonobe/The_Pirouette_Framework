"""
pirouette_eval.py
End-to-end evaluator for the generated pirouette_lib.

What it does:
  - Discovers all terms via pirouette_lib.registry
  - For each term:
      * instantiate class
      * run measure() -> execute each Measurement.compute(ctx) with timeout
      * run mappings()  (collect confidences)
      * run constraints() -> execute each check(ctx) with timeout
      * optionally doctest the example() snippet
  - Optionally run chain presets from spines.json via experiment.run_chain
  - Emits:
      * pir_eval_report.json   (full machine-readable results)
      * pir_eval_terms.csv     (per-term status table)
      * pir_eval_summary.md    (rollup & quick failures list)

Usage:
  python pirouette_eval.py --ctx ctx.json --spines spines.json --timeout 2.5

Notes:
  - ctx file is optional; default ctx = {"data": None, "params": {}}.
  - Timeouts use ThreadPoolExecutor (portable across OSes).
  - Doctest is best-effort; failures are recorded but not fatal.
"""

from __future__ import annotations
import argparse, json, time, traceback, doctest, csv
from pathlib import Path
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from typing import Any, Dict, List, Optional, Tuple

# --- import your generated lib
from pirouette_lib import registry, experiment

# ---------- helpers ----------
def now_iso():
    import datetime as _dt
    return _dt.datetime.now().isoformat() + "Z"

def load_json(p: Optional[str]) -> Any:
    if not p: return None
    path = Path(p)
    if not path.exists(): raise FileNotFoundError(f"Missing file: {p}")
    return json.loads(path.read_text(encoding="utf-8"))

@dataclass
class CallResult:
    name: str
    ok: bool
    duration_s: float
    error: Optional[str] = None

@dataclass
class TermEval:
    cid: str
    term_name: str
    measurements: List[CallResult]
    constraints: List[CallResult]
    mappings_count: int
    mapping_confidences: List[float]
    doctest_ok: Optional[bool] = None
    doctest_failures: Optional[int] = None
    doctest_error: Optional[str] = None

# ---------- sandboxed execution with timeout ----------
def run_with_timeout(func, timeout_s: float, ctx) -> Tuple[bool, float, Optional[str]]:
    t0 = time.perf_counter()
    with ThreadPoolExecutor(max_workers=1) as ex:
        fut = ex.submit(lambda: func(ctx))
        try:
            _ = fut.result(timeout=timeout_s)
            return True, time.perf_counter() - t0, None
        except TimeoutError:
            return False, time.perf_counter() - t0, f"Timeout after {timeout_s:.2f}s"
        except Exception as e:
            tb = "".join(traceback.format_exception(type(e), e, e.__traceback__))
            return False, time.perf_counter() - t0, tb

def doctest_snippet(snippet: str) -> Tuple[bool, int, Optional[str]]:
    try:
        # Provide pirouette_lib in doctest globals so imports work
        globs = {"pirouette_lib": __import__("pirouette_lib")}
        runner = doctest.DocTestRunner()
        parser = doctest.DocTestParser()
        test = parser.get_doctest(snippet, globs, name="example", filename="<example>", lineno=0)
        result = runner.run(test, clear_globs=False)
        return (result.failed == 0), int(result.failed), None
    except Exception as e:
        tb = "".join(traceback.format_exception(type(e), e, e.__traceback__))
        return False, 0, tb

# ---------- main evaluation ----------
def evaluate_all(ctx: Dict[str, Any], timeout_s: float, doctest_examples: bool) -> Dict[str, Any]:
    results: List[TermEval] = []
    failures = {"measure": [], "constraint": [], "doctest": []}

    term_map = registry.known_terms()  # {CID: "module:Class"}
    cids = sorted(term_map.keys())

    for cid in cids:
        TermClass = registry.get(cid)
        term_obj = TermClass()
        term_name = getattr(term_obj, "canonical_id", cid)

        # collect definitions
        ms = []
        mapping_conf = []
        cs = []

        # Measurements
        try:
            measures = term_obj.measure(ctx) or []
        except Exception as e:
            tb = "".join(traceback.format_exception(type(e), e, e.__traceback__))
            ms.append(CallResult(name=f"{cid}:measure::<ctor>", ok=False, duration_s=0.0, error=tb))
            failures["measure"].append(cid)
            measures = []

        for m in measures:
            ok, dt, err = run_with_timeout(m.compute, timeout_s, ctx)
            ms.append(CallResult(name=m.name, ok=ok, duration_s=dt, error=err))
            if not ok: failures["measure"].append(cid)

        # Mappings (no execution, just collect confidences)
        try:
            maps = term_obj.mappings() or []
            mapping_conf = [float(getattr(m, "confidence", 0.0)) for m in maps if hasattr(m, "confidence")]
        except Exception as e:
            tb = "".join(traceback.format_exception(type(e), e, e.__traceback__))
            mapping_conf = []
            # continue; not a fatal path

        # Constraints
        try:
            cons = term_obj.constraints() or []
        except Exception as e:
            tb = "".join(traceback.format_exception(type(e), e, e.__traceback__))
            cs.append(CallResult(name=f"{cid}:constraints::<ctor>", ok=False, duration_s=0.0, error=tb))
            failures["constraint"].append(cid)
            cons = []

        for c in cons:
            ok, dt, err = run_with_timeout(c.check, timeout_s, ctx)
            cs.append(CallResult(name=c.name, ok=ok, duration_s=dt, error=err))
            if not ok: failures["constraint"].append(cid)

        # Doctest example() (optional best-effort)
        dt_ok = dt_fail = None
        dt_err = None
        if doctest_examples:
            try:
                snippet = term_obj.example() or ""
                if snippet.strip():
                    dt_ok, dt_fail, dt_err = doctest_snippet(snippet)
                    if not dt_ok:
                        failures["doctest"].append(cid)
            except Exception as e:
                dt_ok, dt_fail = False, 0
                dt_err = "".join(traceback.format_exception(type(e), e, e.__traceback__))
                failures["doctest"].append(cid)

        results.append(
            TermEval(
                cid=cid,
                term_name=term_name,
                measurements=ms,
                constraints=cs,
                mappings_count=len(mapping_conf),
                mapping_confidences=mapping_conf,
                doctest_ok=dt_ok,
                doctest_failures=dt_fail,
                doctest_error=dt_err,
            )
        )

    # Roll up summary stats
    total = len(results)
    meas_calls = sum(len(t.measurements) for t in results)
    meas_pass = sum(1 for t in results for r in t.measurements if r.ok)
    cons_calls = sum(len(t.constraints) for t in results)
    cons_pass = sum(1 for t in results for r in t.constraints if r.ok)
    conf_all = [c for t in results for c in t.mapping_confidences]
    conf_avg = (sum(conf_all) / len(conf_all)) if conf_all else None

    summary = {
        "generated_at": now_iso(),
        "terms": total,
        "measurement_calls": meas_calls,
        "measurement_pass": meas_pass,
        "constraint_calls": cons_calls,
        "constraint_pass": cons_pass,
        "mapping_conf_avg": conf_avg,
        "failures": {k: sorted(set(v)) for k, v in failures.items()},
    }

    return {"summary": summary, "results": [asdict(r) for r in results]}

def run_spines(spines_path: Optional[str], ctx: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    if not spines_path: return None
    sp = load_json(spines_path)
    out = {"spines_file": spines_path, "runs": [], "generated_at": now_iso()}
    for entry in sp.get("spines", []):
        nodes = entry.get("nodes") or entry.get("cids") or []
        if not nodes: continue
        try:
            rep = experiment.run_chain(nodes, ctx)
            out["runs"].append({"rank": entry.get("rank"), "nodes": nodes, "report": rep})
        except Exception as e:
            out["runs"].append({"rank": entry.get("rank"), "nodes": nodes,
                                "error": "".join(traceback.format_exception(type(e), e, e.__traceback__))})
    return out

# ---------- writers ----------
def write_json(p: Path, obj: Any):
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")

def write_csv_terms(p: Path, results: List[Dict[str, Any]]):
    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["cid","meas_total","meas_pass","cons_total","cons_pass","maps","maps_conf_avg","doctest_ok"])
        for r in results:
            meas_total = len(r["measurements"])
            meas_pass  = sum(1 for x in r["measurements"] if x["ok"])
            cons_total = len(r["constraints"])
            cons_pass  = sum(1 for x in r["constraints"] if x["ok"])
            confs = r["mapping_confidences"] or []
            avg = (sum(confs)/len(confs)) if confs else ""
            w.writerow([r["cid"], meas_total, meas_pass, cons_total, cons_pass, r["mappings_count"], avg, r.get("doctest_ok")])

def write_summary_md(p: Path, suite: Dict[str, Any], spine_runs: Optional[Dict[str, Any]]):
    s = suite["summary"]
    lines = []
    lines.append("# Pirouette Evaluation Summary\n")
    lines.append(f"- Generated: {s['generated_at']}")
    lines.append(f"- Terms: **{s['terms']}**")
    lines.append(f"- Measurements: {s['measurement_pass']} / {s['measurement_calls']} passed")
    lines.append(f"- Constraints: {s['constraint_pass']} / {s['constraint_calls']} passed")
    if s["mapping_conf_avg"] is not None:
        lines.append(f"- Avg mapping confidence: {s['mapping_conf_avg']:.3f}")
    lines.append("")
    # Failures
    for k, lst in s["failures"].items():
        if lst:
            lines.append(f"## {k.title()} failures ({len(lst)})")
            lines.append(", ".join(lst))
            lines.append("")
    # Spines
    if spine_runs and spine_runs.get("runs"):
        lines.append("## Spine runs")
        for run in spine_runs["runs"]:
            rank = run.get("rank")
            nodes = run.get("nodes")
            if "error" in run:
                lines.append(f"- Spine {rank}: ERROR → {run['error'][:160]}…")
            else:
                checks = []
                for step in run["report"].get("steps", []):
                    ok = all(step.get("checks", {}).values()) if step.get("checks") else True
                    checks.append("✔" if ok else "✖")
                lines.append(f"- Spine {rank}: {' '.join(checks)}  ({' -> '.join(nodes[:8])}{' …' if len(nodes)>8 else ''})")
        lines.append("")
    p.write_text("\n".join(lines), encoding="utf-8")

# ---------- CLI ----------
def main():
    ap = argparse.ArgumentParser(description="Evaluate all generated Pirouette term modules.")
    ap.add_argument("--ctx", help="Path to JSON context file (default: {'data':None,'params':{}})")
    ap.add_argument("--spines", help="Optional spines.json to run chain checks")
    ap.add_argument("--timeout", type=float, default=2.5, help="Seconds per compute/check call")
    ap.add_argument("--outdir", default="./pir_eval", help="Where to write reports")
    ap.add_argument("--no_doctest", action="store_true", help="Skip doctesting example()")
    args = ap.parse_args()

    ctx = load_json(args.ctx) or {"data": None, "params": {}}
    outdir = Path(args.outdir); outdir.mkdir(parents=True, exist_ok=True)

    suite = evaluate_all(ctx=ctx, timeout_s=args.timeout, doctest_examples=(not args.no_doctest))
    sp_runs = run_spines(args.spines, ctx)

    write_json(outdir / "pir_eval_report.json", suite)
    write_csv_terms(outdir / "pir_eval_terms.csv", suite["results"])
    write_summary_md(outdir / "pir_eval_summary.md", suite, sp_runs)

    print(f"Wrote {outdir/'pir_eval_report.json'}")
    print(f"Wrote {outdir/'pir_eval_terms.csv'}")
    print(f"Wrote {outdir/'pir_eval_summary.md'}")

if __name__ == "__main__":
    main()
