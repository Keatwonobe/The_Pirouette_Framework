
import os, json
from pathlib import Path

try:
    import google.generativeai as genai  # type: ignore
    HAS_GENAI = True
except Exception:
    HAS_GENAI = False

MODEL = "gemini-2.5-pro"
API_KEY_ENV = "GOOGLE_API_KEY"

OUT_DIR = "./sections_curated"

ROLES = ["PROPONENT","SKEPTIC","METHODOLOGIST","ETHICIST"]
RUBRIC = ["coherence","predictivity","falsifiability","external_anchor","dark_residue","elegance"]

def _init_model():
    if not HAS_GENAI: return None
    key = os.getenv(API_KEY_ENV)
    if not key: return None
    genai.configure(api_key=key)
    return genai.GenerativeModel(MODEL)

def _prompt_role(role: str, text: str) -> str:
    return f"""You are the {role}. Evaluate the draft section below.
List the 2–3 most critical strengths/weaknesses for your role.
Propose one decisive change (add/remove/tighten).
Score each rubric key in [0,1]: {', '.join(RUBRIC)}.
Return JSON with keys: commentary, change, scores.
DRAFT:
{text}
"""

def _prompt_fuse(reports_json: str, text: str) -> str:
    return f"""Fuse the following role reports into a single edited section.
Apply only changes that increase clarity, formal specificity, falsifiability, and ethical alignment.
Return Markdown only.

ROLE REPORTS (JSON):
{reports_json}

DRAFT TO EDIT:
{text}
"""

def curate_section(section_path: str, min_avg: float = 0.7, min_dark: float = 0.45) -> str:
    model = _init_model()
    raw = Path(section_path).read_text(encoding="utf-8")
    reports = {}
    if model:
        for r in ROLES:
            resp = model.generate_content(_prompt_role(r, raw))
            try:
                rep = json.loads(getattr(resp,"text","") or "{}")
            except Exception:
                rep = {"commentary": f"[fallback {r}]","change":"[none]","scores":{k:0.7 for k in RUBRIC}}
            # ensure keys
            rep.setdefault("scores", {k:0.7 for k in RUBRIC})
            for k in RUBRIC: rep["scores"].setdefault(k,0.7)
            reports[r]=rep
    else:
        reports={r:{"commentary":f"[offline {r}]","change":"[none]","scores":{k:0.7 for k in RUBRIC}} for r in ROLES}

    avg = sum(sum(v["scores"][k] for k in RUBRIC)/len(RUBRIC) for v in reports.values())/len(ROLES)
    dark = sum(v["scores"]["dark_residue"] for v in reports.values())/len(ROLES)

    decision = "PASS" if (avg>=min_avg and dark>=min_dark) else "REVISE"

    if decision=="PASS" and model:
        fused = model.generate_content(_prompt_fuse(json.dumps(reports,indent=2), raw)).text or raw
    elif decision=="PASS":
        fused = raw
    else:
        clar = "\n\n---\n**Clarifications Requested**\n" + "\n".join(f"- {r}: {reports[r]['change']}" for r in ROLES)
        fused = raw + clar

    Path(OUT_DIR).mkdir(parents=True, exist_ok=True)
    out = Path(OUT_DIR)/ (Path(section_path).stem + f"__{decision}.md")
    out.write_text(fused, encoding="utf-8")
    return f"{decision}:{out}"

def main():
    import argparse
    p = argparse.ArgumentParser(description="Debate-integrated curation for a section. Returns PASS/REVISE.")
    p.add_argument("section_path")
    p.add_argument("--min_avg", type=float, default=0.7)
    p.add_argument("--min_dark", type=float, default=0.45)
    args = p.parse_args()
    res = curate_section(args.section_path, args.min_avg, args.min_dark)
    print(f"✅ {res}")

if __name__=="__main__":
    main()
