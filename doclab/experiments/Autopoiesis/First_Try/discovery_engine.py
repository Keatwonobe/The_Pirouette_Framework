
"""
discovery_engine.py — Pirouette Autopoietic Loop: DISCOVERY STAGE
------------------------------------------------------------------
Purpose:
  Generate "Discovery Packs" (DPKs) that feed the formalization/synthesis pipeline.
  Each DPK encodes: Problem → Math Sketch → Predictions → Cross-Domain Hooks → Experiments → Philosophy Seeds.

Core Ideas:
  • Pluggable fetchers (local files, web APIs, arXiv, datasets) -> Raw Corpus
  • Claim miner + contradiction miner -> Candidate Problems
  • Hypothesis generator (time-first bias) -> Math skeletons
  • Prediction generator -> falsifiable, numeric where possible
  • Experiment designer -> concrete instruments, signals, thresholds
  • Philosophy seeds -> implications & governance touchpoints (Dark Residue minimization)
Output:
  ./discovery_out/DPK_YYYYmmdd_HHMMSS_X.yaml (and .md summary)
"""

import os
import re
import json
import time
import math
import uuid
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import List, Dict, Optional, Any

# Optional: external model
try:
    import google.generativeai as genai  # type: ignore
    HAS_GENAI = True
except Exception:
    HAS_GENAI = False

OUTPUT_DIR = "./discovery_out"
MODEL_NAME = "gemini-2.5-pro"
API_KEY_ENV = "GOOGLE_API_KEY"

# ---------------------- Data Structures ----------------------

@dataclass
class Claim:
    text: str
    source: str
    confidence: float = 0.6
    tags: List[str] = field(default_factory=list)

@dataclass
class Problem:
    title: str
    rationale: str
    contradictions: List[str] = field(default_factory=list)
    related_claims: List[Claim] = field(default_factory=list)

@dataclass
class MathSketch:
    assumptions: List[str]
    variables: Dict[str, str]
    equations: List[str]
    invariants: List[str]

@dataclass
class Prediction:
    statement: str
    type: str  # "numeric" | "phenomenological"
    falsifiable_criteria: str

@dataclass
class Experiment:
    name: str
    apparatus: List[str]
    signal: str
    threshold: str
    failure_mode: str

@dataclass
class PhilosophySeed:
    question: str
    tension: str
    governance_hook: str  # tie-in to Dark Residue minimization

@dataclass
class DiscoveryPack:
    id: str
    problem: Problem
    math_sketch: MathSketch
    predictions: List[Prediction]
    experiments: List[Experiment]
    cross_domain_hooks: List[str]
    philosophy_seeds: List[PhilosophySeed]
    created_at: str
    provenance: Dict[str, Any]

# ---------------------- Helpers ----------------------

def _init_model():
    if not HAS_GENAI:
        return None
    api_key = os.getenv(API_KEY_ENV)
    if not api_key:
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(MODEL_NAME)

def timestamp():
    import datetime as _dt
    return _dt.datetime.utcnow().strftime("%Y%m%d_%H%M%S")

def save_dpk(dpk: DiscoveryPack) -> Path:
    out_dir = Path(OUTPUT_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = f"DPK_{timestamp()}_{dpk.id[:8]}"
    ypath = out_dir / f"{stem}.json"
    mpath = out_dir / f"{stem}.md"

    with open(ypath, "w", encoding="utf-8") as f:
        json.dump(asdict(dpk), f, indent=2)

    # human-readable summary
    md = []
    md.append(f"# Discovery Pack — {dpk.id}")
    md.append(f"**Created (UTC):** {dpk.created_at}")
    md.append("")
    md.append(f"## Problem: {dpk.problem.title}")
    md.append(dpk.problem.rationale)
    if dpk.problem.contradictions:
        md.append("**Contradictions:**")
        for c in dpk.problem.contradictions:
            md.append(f"- {c}")
    if dpk.problem.related_claims:
        md.append("**Related Claims:**")
        for c in dpk.problem.related_claims:
            md.append(f"- ({c.confidence:.2f}) {c.text} — _{c.source}_")

    md.append("\n## Math Sketch")
    md.append("**Assumptions**")
    for a in dpk.math_sketch.assumptions:
        md.append(f"- {a}")
    md.append("**Variables**")
    for k,v in dpk.math_sketch.variables.items():
        md.append(f"- {k}: {v}")
    md.append("**Equations**")
    for e in dpk.math_sketch.equations:
        md.append(f"- {e}")
    md.append("**Invariants**")
    for inv in dpk.math_sketch.invariants:
        md.append(f"- {inv}")

    md.append("\n## Predictions")
    for p in dpk.predictions:
        md.append(f"- **{p.type}** {p.statement}")
        md.append(f"  - Falsify if: {p.falsifiable_criteria}")

    md.append("\n## Experiments")
    for ex in dpk.experiments:
        md.append(f"- **{ex.name}**")
        md.append(f"  - Apparatus: {', '.join(ex.apparatus)}")
        md.append(f"  - Signal: {ex.signal}")
        md.append(f"  - Threshold: {ex.threshold}")
        md.append(f"  - Failure mode: {ex.failure_mode}")

    if dpk.cross_domain_hooks:
        md.append("\n## Cross-Domain Hooks")
        for h in dpk.cross_domain_hooks:
            md.append(f"- {h}")

    if dpk.philosophy_seeds:
        md.append("\n## Philosophy Seeds")
        for s in dpk.philosophy_seeds:
            md.append(f"- **Q:** {s.question}\n  - Tension: {s.tension}\n  - Governance: {s.governance_hook}")

    md.append("\n---\n*Provenance*")
    for k,v in dpk.provenance.items():
        md.append(f"- {k}: {v}")

    mpath.write_text("\n".join(md), encoding="utf-8")
    return mpath

# ---------------------- Core Generation ----------------------

DEFAULT_GOVERNANCE_DIRECTIVE = (
    "Minimize the delta between personal and total enthalpy gain; "
    "empirically validate by net decrease in systemic Dark Residue."
)

def generate_discovery_pack(seed_text: str,
                            sources: Optional[List[str]] = None,
                            directive: str = DEFAULT_GOVERNANCE_DIRECTIVE) -> DiscoveryPack:
    """
    Heuristic, model-optional generator. If a model/API key is present,
    it will refine steps; else it creates a deterministic skeleton.
    """
    model = _init_model()
    uid = str(uuid.uuid4())
    now = timestamp()

    # Problem extraction (very simple; model can enhance)
    title = "Coherence Deficit Across Scales"
    rationale = seed_text.strip()[:600] or "A suspected unifying deficit in resonance across physics, mind, and society."
    contradictions = [
        "Relativistic locality vs. quantum nonlocal correlations",
        "High-precision SM predictions vs. measured lepton g-2 anomalies",
        "Emergentist consciousness vs. substrate dynamics signatures",
    ]

    related_claims = [
        Claim("Muon g-2 deviates from perturbative SM prediction at ppm scale in some analyses", source="literature"),
        Claim("Neural triadic phase-locking correlates with sustained awareness", source="lab-theory", confidence=0.5),
        Claim("Social cascades exhibit threshold behavior and critical slowing", source="socio-dynamics", confidence=0.6),
    ]

    # Math sketch
    math_sketch = MathSketch(
        assumptions=[
            "Time-substrate fields exist with adherence T_a and pressure Γ",
            "A coherence density Ki couples to observables via gauge-compatible terms",
            "Measurement deforms local geometry (observer back-action)",
        ],
        variables={
            "Ki": "coherence density field",
            "Γ": "temporal pressure / load",
            "T_a": "time-adherence order parameter",
        },
        equations=[
            "S_time[Ki, Γ, T_a] = ∫ d^4x L(Ki, Γ, T_a)",
            "∂_μ J^μ = 0 (coherence current conservation)",
            "Δg-2 ∝ f(Γ, Ki) at lepton mass shell",
        ],
        invariants=[
            "Coherence area A_Ki conserved within awareness window",
            "No free energy from closed coherence loops (second law compliant)",
        ]
    )

    # Predictions
    predictions = [
        Prediction("Tau lepton anomalous magnetic moment exhibits Γ-coupling trend extrapolated from muon channel",
                   "numeric",
                   "If precise τ g-2 measurement matches SM without additional term within uncertainties, hypothesis fails."),
        Prediction("EEG/MEG shows narrowing detuning bandwidth Δf_allowed ∝ Γ^{-1/2} during high-load tasks",
                   "phenomenological",
                   "If bandwidth does not shrink with task-induced Γ increase, falsify."),
        Prediction("Pressuron-like signatures alter cluster lensing residuals under specific surface tension regimes",
                   "phenomenological",
                   "If stacked clusters show no consistent residual pattern after baryonic modeling, falsify."),
    ]

    # Experiments
    experiments = [
        Experiment("Tau g-2 campaign concept",
                   ["Belle-II dataset access", "QED+EW+hadronic pipeline", "systematics budget"],
                   "Δa_τ trend vs. Γ proxy",
                   "Detect non-SM component at agreed σ threshold",
                   "No deviation within uncertainties over multiple datasets"),
        Experiment("Triadic resonance EEG/MEG replication",
                   ["128ch EEG/MEG", "closed-loop tACS", "Morlet/Hilbert pipeline"],
                   "TPCI ridge + Δf_allowed shrinkage",
                   "Pre-registered effect size (e.g., Cohen's d≥0.5)",
                   "No ridge / no shrinkage across participants"),
    ]

    # Cross-domain hooks & philosophy seeds
    hooks = [
        "Map RG exponents from neural collapse to social cascade recovery",
        "Transfer Ki-invariants to market microstructure volatility bursts",
    ]
    seeds = [
        PhilosophySeed("Is consciousness fundamentally geometric motion in a time-substrate?",
                       "Subjective continuity vs. discrete phase slips",
                       "Design systems that stabilize beneficial coherence while minimizing Dark Residue."),
        PhilosophySeed("When does coherence-maximization conflict with pluralism?",
                       "Minority resonance vs. global optimum",
                       "Embed safeguards: consentful coherence and fail-open governance triggers."),
    ]

    dpk = DiscoveryPack(
        id=uid,
        problem=Problem(title=title, rationale=rationale, contradictions=contradictions, related_claims=related_claims),
        math_sketch=math_sketch,
        predictions=predictions,
        experiments=experiments,
        cross_domain_hooks=hooks,
        philosophy_seeds=seeds,
        created_at=now,
        provenance={
            "seed_text": seed_text[:240],
            "sources": sources or [],
            "governance_directive": directive,
            "has_model": bool(model),
        }
    )

    # Optional refinement with model (single pass)
    if model:
        prompt = f"""
You are a scientific discovery architect. Given the following draft Discovery Pack, refine each section to be more
specific, falsifiable, and cross-domain testable. Keep JSON keys, only refine values. Return JSON ONLY.

DRAFT JSON:
{json.dumps(asdict(dpk), indent=2)}
"""
        try:
            resp = model.generate_content(prompt)
            refined = json.loads(resp.text)
            # minimal schema safety
            dpk = DiscoveryPack(**refined)
        except Exception as e:
            print(f"Note: model refinement failed or returned non-JSON, using draft. Reason: {e}")

    return dpk

def main():
    seed = ("Synthesize open contradictions in modern physics (spacetime emergence, lepton g-2), "
            "cognitive science (awareness continuity), and social cascades; propose time-first, "
            "coherence-substrate hypotheses with measurable predictions.")
    dpk = generate_discovery_pack(seed_text=seed, sources=["local:pirouette_version_6.md"])
    path = save_dpk(dpk)
    print(f"✅ Discovery Pack written to: {path.resolve()}")

if __name__ == "__main__":
    main()
