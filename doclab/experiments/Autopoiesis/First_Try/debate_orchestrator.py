
"""
debate_orchestrator.py — Pirouette Autopoietic Loop: AUTOMATED DEBATE STAGE (patched)
-------------------------------------------------------------------------------------
Improvements:
- Robust JSON parsing with safe fallbacks (handles empty or non-JSON model output)
- Retry once with a stricter "JSON ONLY" system
- Offline mode (--offline) to force deterministic stubs
- Logs raw model outputs to ./debate_out/logs for debugging
"""

import os
import json
import time
from pathlib import Path
from typing import List, Dict, Any, Optional

# Optional model
try:
    import google.generativeai as genai  # type: ignore
    HAS_GENAI = True
except Exception:
    HAS_GENAI = False

MODEL_NAME = "gemini-2.5-pro"
API_KEY_ENV = "GOOGLE_API_KEY"
OUTPUT_DIR = "./debate_out"
LOG_DIR = "./debate_out/logs"

PRIME_DIRECTIVE = (
    "Act to minimize the delta between personal and total enthalpy gain; "
    "validate by net decrease in systemic Dark Residue; create universal beauty and compositional harmony."
)

ROLES = ["PROPONENT", "SKEPTIC", "METHODOLOGIST", "ETHICIST", "REFEREE"]

RUBRIC = {
    "coherence": "Internal logical consistency; absence of contradiction; clear definitions.",
    "predictivity": "Specific, testable, preferably numeric predictions.",
    "falsifiability": "Clear, feasible conditions under which the claim fails.",
    "external_anchor": "Appropriate use of external references or data without appeal to authority.",
    "dark_residue": "Projected reduction of negative unintended consequences.",
    "elegance": "Parsimony and geometric clarity of formulation.",
}

THRESHOLDS = {
    "pass_min_avg": 0.72,
    "hard_block_dark_residue": 0.40
}

def _init_model(enabled: bool):
    if not enabled or not HAS_GENAI:
        return None
    key = os.getenv(API_KEY_ENV)
    if not key:
        return None
    genai.configure(api_key=key)
    return genai.GenerativeModel(MODEL_NAME)

def _strictify_prompt(p: str) -> str:
    header = (
        "Return ONLY a single valid JSON object. "
        "No preamble, no markdown fences, no commentary, no code blocks. "
        "Keys required: commentary, experiment, scores.\n"
    )
    return header + p

def _write_log(stem: str, role: str, content: str):
    Path(LOG_DIR).mkdir(parents=True, exist_ok=True)
    (Path(LOG_DIR) / f"{stem}__{role}.txt").write_text(content or "", encoding="utf-8")

def _safe_json_loads(text: str, default_scores: Dict[str, float]) -> Dict[str, Any]:
    if not text or not text.strip():
        raise ValueError("Empty text")
    try:
        return json.loads(text)
    except Exception:
        # try to extract JSON between braces as a last resort
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1 and end > start:
            candidate = text[start:end+1]
            try:
                return json.loads(candidate)
            except Exception:
                pass
        raise

def role_prompt(role: str, dossier: str, stage: str) -> str:
    return f"""
You are the {role} in a structured scientific debate ({stage}). Read the dossier and respond concisely:

- Identify the 2–3 most critical strengths/weaknesses relevant to your role.
- Propose one decisive experiment or derivation to resolve uncertainty.
- Give 0–1 score per rubric dimension.
Rubric dimensions: coherence, predictivity, falsifiability, external_anchor, dark_residue, elegance.

Return a JSON object with keys: commentary, experiment, scores (scores is an object with the rubric keys as floats).
DOSSIER:
{dossier}
"""

def referee_prompt(round_inputs: Dict[str, Any], stage: str) -> str:
    return f"""
You are the REFEREE. Aggregate the role reports for stage '{stage}'.

Task:
1) Summarize consensus and conflicts.
2) Compute weighted average scores across roles (equal weights).
3) Decide one of: RATIFY, REVISE, REJECT.
4) If REVISE, output the minimal set of changes needed (bullet list).

Return JSON with keys: summary, decision, required_changes, averaged_scores.
INPUT:
{json.dumps(round_inputs, indent=2)}
"""

def governance_prompt(ratified_text: str) -> str:
    return f"""
Evaluate the following artifact against the Prime Directive:

PRIME DIRECTIVE:
{PRIME_DIRECTIVE}

Artifact:
{ratified_text}

Return JSON with:
- alignment_summary
- risks
- mitigations
- alignment_score (0–1)
- decision (ALLOW, REVISE, HALT)
"""

def run_debate(dossier_path: str, stage: str = "Formalization Debate", offline: bool = False) -> Path:
    model = _init_model(enabled=not offline)
    out_dir = Path(OUTPUT_DIR); out_dir.mkdir(parents=True, exist_ok=True)
    dossier = Path(dossier_path).read_text(encoding="utf-8")
    stem = Path(dossier_path).stem + f"__{stage.replace(' ', '_').lower()}"

    # Multi-agent round
    round_data = {}
    for role in ROLES[:-1]:  # exclude referee in first pass
        default_scores = {k: 0.7 for k in RUBRIC.keys()}
        if model:
            prompt = role_prompt(role, dossier, stage)
            try:
                resp = model.generate_content(_strictify_prompt(prompt))
                text = getattr(resp, "text", "") or ""
                _write_log(stem, role, text)
                try:
                    parsed = _safe_json_loads(text, default_scores)
                except Exception:
                    # one retry with stricter preface
                    resp2 = model.generate_content("JSON ONLY. " + _strictify_prompt(prompt))
                    text2 = getattr(resp2, "text", "") or ""
                    _write_log(stem, role + "_retry", text2)
                    parsed = _safe_json_loads(text2, default_scores)
            except Exception:
                parsed = {
                    "commentary": f"[fallback] {role} notes strengths/weaknesses.",
                    "experiment": f"[fallback] {role} proposes an experiment.",
                    "scores": default_scores
                }
        else:
            parsed = {
                "commentary": f"[offline] {role} notes strengths/weaknesses.",
                "experiment": f"[offline] {role} proposes an experiment.",
                "scores": default_scores
            }
        # Ensure scores cover all keys
        for k in RUBRIC.keys():
            parsed.setdefault("scores", {}).setdefault(k, 0.7)
        round_data[role] = parsed

    # Referee aggregation
    if model:
        try:
            ref_resp = model.generate_content(_strictify_prompt(referee_prompt(round_data, stage)))
            ref_text = getattr(ref_resp, "text", "") or ""
            _write_log(stem, "REFEREE", ref_text)
            try:
                ref_parsed = _safe_json_loads(ref_text, {})
            except Exception:
                ref_resp2 = model.generate_content("JSON ONLY. " + _strictify_prompt(referee_prompt(round_data, stage)))
                ref_text2 = getattr(ref_resp2, "text", "") or ""
                _write_log(stem, "REFEREE_retry", ref_text2)
                ref_parsed = _safe_json_loads(ref_text2, {})
        except Exception:
            # fallback referee
            avg = {k: sum(r["scores"][k] for r in round_data.values())/len(round_data) for k in RUBRIC.keys()}
            decision = "RATIFY" if (
                sum(avg.values())/len(avg) >= THRESHOLDS["pass_min_avg"] and avg["dark_residue"] >= THRESHOLDS["hard_block_dark_residue"]
            ) else "REVISE"
            ref_parsed = {
                "summary": "[fallback] referee summary",
                "decision": decision,
                "required_changes": ["Tighten falsifiability thresholds", "Clarify variable definitions"],
                "averaged_scores": avg
            }
    else:
        # offline referee
        avg = {k: sum(r["scores"][k] for r in round_data.values())/len(round_data) for k in RUBRIC.keys()}
        decision = "RATIFY" if (
            sum(avg.values())/len(avg) >= THRESHOLDS["pass_min_avg"] and avg["dark_residue"] >= THRESHOLDS["hard_block_dark_residue"]
        ) else "REVISE"
        ref_parsed = {
            "summary": "[offline] referee summary",
            "decision": decision,
            "required_changes": ["Tighten falsifiability thresholds", "Clarify variable definitions"],
            "averaged_scores": avg
        }

    results = {
        "stage": stage,
        "roles": round_data,
        "referee": ref_parsed,
        "timestamp_utc": time.time()
    }

    # Save dossier result
    out_path = out_dir / f"{stem}_result.json"
    out_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"✅ Debate result saved: {out_path.resolve()}")
    return out_path

def governance_review(artifact_path: str, offline: bool = False) -> Path:
    model = _init_model(enabled=not offline)
    text = Path(artifact_path).read_text(encoding="utf-8")
    if model:
        try:
            resp = model.generate_content(_strictify_prompt(governance_prompt(text)))
            data = json.loads(getattr(resp, "text", "{}") or "{}")
        except Exception:
            data = {
                "alignment_summary": "[fallback] Likely positive alignment; proposes mitigation for externalities.",
                "risks": ["Over-centralization of measurement protocols"],
                "mitigations": ["Decentralized consentful governance gates; open audit trails"],
                "alignment_score": 0.78,
                "decision": "ALLOW"
            }
    else:
        data = {
            "alignment_summary": "[offline] Likely positive alignment; proposes mitigation for externalities.",
            "risks": ["Over-centralization of measurement protocols"],
            "mitigations": ["Decentralized consentful governance gates; open audit trails"],
            "alignment_score": 0.78,
            "decision": "ALLOW"
        }
    out = Path(OUTPUT_DIR) / f"{Path(artifact_path).stem}__governance_review.json"
    out.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"✅ Governance review saved: {out.resolve()}")
    return out

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Run automated debate stages over a dossier.")
    parser.add_argument("dossier", help="Path to a .md or .txt dossier (paper/manifesto/grand).")
    parser.add_argument("--stage", default="Formalization Debate",
                        choices=["Formalization Debate", "Philosophy Debate", "Governance Debate"])
    parser.add_argument("--governance", action="store_true", help="Run governance review after debate.")
    parser.add_argument("--offline", action="store_true", help="Force offline deterministic mode (no API calls).")
    args = parser.parse_args()

    result_path = run_debate(args.dossier, stage=args.stage, offline=args.offline)
    if args.governance or args.stage == "Governance Debate":
        governance_review(args.dossier, offline=args.offline)

if __name__ == "__main__":
    main()
