---
id: INST-DEB-001 
title: Operational Spec for the Autopoietic Unifier (Pirouette Debate Instrument)

Status: draft → ratify after first 5 dockets
Owner: Keaton (PDM-000 custodian)
Lineage: EXPAND from DYNA-002 “Geometry of Debate”
Intent: Provide an operational, testable instrument to unify (not expand) Pirouette via structured, API-driven debates that yield safe, atomic repo changes.

---

## 0) Purpose & Scope

**Purpose.** Convert debate into *governed* change: each run must yield exactly one of {EXPAND, MERGE, REVISION}, with provenance, tests, and clean diffs.
**Scope.** Applies to all modules (CORE/DOMA/DYNA/MATH/INST/XXP/TLE/PDM). This document defines schemas, prompts, scoring, CI gates, and CLI for fully automated operation with human veto points.

---

## 1) Key Definitions

* **Docket:** A machine-readable request to run a debate over one or more modules.
* **Persona:** A role with a short constitution (charter) and deliverables.
* **Scorecard:** Persona- and panel-level rubric values plus accept/veto recommendation.
* **Change Type:** EXPAND (new module), MERGE (replace ≥2 with one), REVISION (redline of one).
* **Ratified Change Set:** Materialized repo artifacts + debate dossier + commit tag.

---

## 2) Data Schemas (canonical, versioned)

### 2.1 Module header (YAML front‑matter)

```
id: MATH-022
title: Origin of P(X): Symmetry, Scale, and the Fractal of Time
version: 1.1
status: draft|stable|deprecated
parents: [MATH-018, CORE-006]
replaces: []            # for MERGE/REVISION outcomes
replaced_by: []         # auto-filled if deprecated
summary: "…"
module_type: core|doma|dyna|math|inst|xcm|xxp|tle|pdm
scale: universal|quantum|cosmic|social|clinical
engrams: [ ... ]
keywords: [ ... ]
uncertainty_tag: Foundational|Medium|Low
proof_state: heuristic|sketch|formal
tests: [XXP-012, XXP-015]      # binds to protocols
calibration_refs: [constants, datasets, priors]
```

### 2.2 Docket (JSON)

```
{
  "inst_id": "INST-DEB-001",
  "intent": "MERGE",               
  "inputs": ["CORE-003", "CORE-004"],
  "thesis": "Collapse duplicate Γ-derivations; adopt single T(x) formalism.",
  "constraints": {"no-new-symbols": true, "pin-ids": ["MATH-018"]},
  "personas": ["Formalist","Phenomenologist","Skeptic","Engineer","Archivist"],
  "rubric_weights": {"coherence":0.30,"parsimony":0.25,"predictivity":0.20,"refutability":0.15,"continuity":0.10},
  "budget": {"max_tokens": 80000, "max_cost_usd": 6.00},
  "ci": {"require_tests": true, "min_score": 0.70, "min_dimension": 0.60},
  "metadata": {"requester": "Keaton", "ts": "2025-10-11T00:00:00Z"}
}
```

### 2.3 Persona brief (JSON)

```
{
  "persona": "Formalist",
  "outline": ["Compare symbol tables", "Derive EL from L_p", "Keep minimal set"],
  "redlines": {"keep": ["Eq.(Γ=T_x)","Def.T(x)"], "drop": ["duplicate Γ-law"], "rename": []},
  "tests": ["XXP-012 recovers a_e within δ", "XXP-015 preserves COSMO-Γ HALO fits"],
  "scores": {"coherence":0.86,"parsimony":0.78,"predictivity":0.73,"refutability":0.69,"continuity":0.82},
  "verdict": "accept",
  "notes": "EL form provided; no new symbols introduced"
}
```

### 2.4 Synthesis scorecard (panel)

```
{
  "modules_out": ["CORE-004'"],
  "deprecate": ["CORE-003"],
  "decision": "accept|veto|human_review",
  "scores_mean": 0.78,
  "scores_dim": {"coherence":0.84,"parsimony":0.76,"predictivity":0.72,"refutability":0.70,"continuity":0.86},
  "evidence": ["a_e via XXP-012","Boltzmann hook retained"],
  "diffstat": {"insertions": 312, "deletions": 911},
  "provenance": {"run_id":"debate/merge/core-003_004/2025-10-11","commit":"<git-hash>"}
}
```

---

## 3) Personas & Constitutions

| Persona         | Constitution (one-liner)                                        | Obligations                                                              |
| --------------- | --------------------------------------------------------------- | ------------------------------------------------------------------------ |
| Formalist       | Minimize symbols; all claims derivable from explicit 𝓛 and EL. | Produce symbol map, minimal set, EL derivations, boxed definitions.      |
| Phenomenologist | Tie every claim to XXP/INST tests and falsifiers.               | Emit test list, calibration hooks, falsifiable predictions.              |
| Skeptic         | Expose hidden assumptions; provide counterexample or veto.      | Red-team assumptions, propose minimal rival; justify refutability score. |
| Engineer        | Ensure implementability and config interfaces.                  | Provide config schema, solver path, complexity notes.                    |
| Archivist       | Preserve lineage and repo hygiene.                              | Parents/children updates, deprecation stubs, ToC diffs, changelog.       |

**Deliverable format**: each persona returns machine JSON (2.3). All natural language content must be mirrored in structured fields.

---

## 4) Prompt Templates (deterministic skeletons)

**Global preamble (all personas):**

```
You are the {Persona}. Charter: {constitution}.
Docket: {intent, inputs, thesis, constraints}.
Tasks:
1) Summarize overlaps/divergences (bullets).
2) Propose synthesis outline (sections + equations to keep/remove) with reasons.
3) Emit acceptance tests (XXP/INST hooks) and explicit falsifiers.
4) Score rubric [0..1] with rationale. Propose accept/veto.
Return strictly as JSON: {outline, redlines:{keep,drop,rename}, tests, scores, verdict, notes}.
```

**Skeptic addendum:**

```
Add a minimal rival hypothesis using only symbols already present. Identify a decisive observation that would prefer the rival.
```

**Engineer addendum:**

```
Emit a concrete config snippet for CLASS/CAMB-like pipeline, listing required priors and bounds. Describe O(T) complexity per run.
```

---

## 5) Orchestration & State Machine

```
[NEW_DOCKET] → [BRIEFS_PARALLEL] → [CROSS_EXAM] → [SYNTHESIS_DRAFT]
→ [SCORING_GATE] → {ACCEPT → MATERIALIZE → CI_TESTS → PR}
                   {VETO → ARCHIVE}
                   {HUMAN_REVIEW → QUEUE}
```

**Panel vote weights (sum=1.0):** Skeptic 0.30, Formalist 0.25, Phenomenologist 0.20, Engineer 0.15, Archivist 0.10.
**Thresholds:** mean ≥ 0.70, no dimension < 0.60; otherwise `human_review`.

---

## 6) Materialization Rules (the three moves)

### 6.1 EXPAND

* Create new module `NEW-<series>-<id>` with `status: draft` and required `tests` section.
* Add to `/new/` staging; CI prevents `stable` until tests bound and passing.

### 6.2 MERGE

* Produce successor module with `replaces: [A,B,…]`.
* Write deprecation stubs into A,B with `replaced_by: [SuccessorID]` and short rationale.
* One PR contains successor + stubs + ToC update.

### 6.3 REVISION

* Keep same id, bump `version`.
* Attach semantic redline (machine diff + human-readable summary).
* Re-run bound tests; failure forces `draft` status.

---

## 7) Repository Layout & Hygiene

```
/modules/
  /core /doma /dyna /math /inst /xxp /tle /pdm
/staging/
  /new /merge /rev  # WIP artifacts per docket
/docs/debates/<intent>/<ids>/<date>/  # dossiers & logs
/tools/inst-deb-001/  # CLI + schemas + prompts
```

**Branch naming:** `debate/<intent>/<ids>/<YYYYMMDD>`
**Tags:** `debate-run-<epoch>`

---

## 8) CI/CD Gates

* **Schema check:** YAML front-matter required keys; no orphan `replaces`.
* **Linker:** parents/children exist; ToC updated.
* **Tests:** all referenced `XXP-*` reachable; failing tests block `stable`.
* **Glossary:** updates to MATH-019 if new terms introduced (else block).
* **Provenance:** `debate.json` and `scorecard.json` included in PR.

---

## 9) Budget & Safety Controls

* **Per-run caps:** `max_tokens`, `max_cost_usd`; stop if Skeptic refutability < 0.5 while others > 0.8 (re-run with counter-prompts).
* **Auto-stop day cap:** configurable daily USD limit; hard-stop on exceed.
* **Determinism:** use fixed templates; keep temperature low for synthesis rounds.

---

## 10) Minimal CLI (spec)

```
inst-deb run --docket dockets/core_003_004.merge.json \
             --out docs/debates/merge/core_003_004/20251011 \
             --budget 6.00 --strict

inst-deb triage --modules modules/core/*.md --top 20 --intent MERGE

inst-deb materialize --scorecard docs/debates/.../scorecard.json --repo .
```

**Return codes:** 0 success; 2 schema fail; 3 CI fail; 5 budget exceeded.

---

## 11) Config & Secrets

```
[api]
provider = openai|anthropic|...
model_brief = gpt-4.1
model_synth = gpt-4.1
max_cost_usd = 300.00

[ci]
min_score = 0.70
min_dimension = 0.60
require_tests = true

[repo]
root = .
branch_prefix = debate
```

---

## 12) Acceptance Tests (for this instrument)

1. **Schema Roundtrip:** Docket → Briefs → Scorecard → Materialize → Valid PR (no manual edits).
2. **Merge Hygiene:** After MERGE, `replaces/replaced_by` chains consistent; search finds no dangling pointers.
3. **Veto Logic:** Force low refutability; engine returns `human_review` not `accept`.
4. **Budget Guard:** Artificially high token estimate → engine halts pre-synthesis.
5. **Test Binding:** Introduce failing XXP; CI blocks `stable` status.

---

## 13) Example Docket Pack (Day‑1)

* MERGE: CORE-003 ↔ CORE-004 (Γ unify).
* REVISION: MATH-011 with MATH-018 guardrails (quantization roadmap).
* MERGE: DOMA-051/034/032 → canonical “Fractal Bridge”.
* REVISION: COSMO‑Γ‑CMB & APP configs unified; emit config schema.
* EXPAND: This very instrument as INST-DEB-001 (this doc) → ratify after the four above.

---

## 14) Human Oversight & Ratification

* **Veto right:** PDM-000 custodian (Keaton) can veto any `accept`.
* **Cooling-off:** 24h delay for deprecations unless blocking bugfix.
* **Errata:** Post‑ratification errata appended as `version.patch` with explicit scope.

---

## 15) Roadmap (v1 → v1.2)

* v1.0: Templates, schemas, CLI skeleton, CI gates, 5 inaugural dockets.
* v1.1: Add dataset adapters (constants & Boltzmann priors), richer rival‑hypothesis library.
* v1.2: Telemetry dashboard (run rates, acceptance %, median diffs), cost optimizer.

---

## 16) Appendix A — Code Skeletons

**A.1 Persona contract (Python-like pseudocode)**

```
class Persona:
    name: str
    charter: str
    def brief(self, docket) -> dict: ...   # returns JSON schema 2.3
```

**A.2 Orchestrator outline**

```
run_docket(d):
  briefs = parallel([p.brief(d) for p in d.personas])
  xexam  = cross_examine(briefs)
  synth  = synthesize(briefs, xexam)
  scores = score_panel(synth, d.rubric_weights)
  decision = decide(scores, d)
  artifacts = materialize(decision, synth, d)
  pr = open_pr(artifacts)
  return pr
```

**A.3 CI checks (pseudo)**

```
assert schema_ok(module_yaml)
assert links_ok(parents, children, replaces)
assert tests_bind_ok(tests)
assert glossary_ok()
```

---

## 17) Appendix B — Config Snippets

**B.1 CLASS/CAMB‑like hook (Engineer deliverable)**

```
[cmb]
Gamma0 = 1.2e-5
PX_beta = 1/3
k_min = 1e-5
k_max = 0.5
priors = {Omega_b: [0.04,0.06], H0: [60,75]}
```

---

**Signature for ratification:**

* [ ] Keaton (PDM-000)
* [ ] Archivist persona (automated)
* [ ] Skeptic counter‑sign (automated)
