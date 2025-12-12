---
term: "Running of α(q²)"
canonical_id: "RUNNING_OF_Q"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-020"]
---

---
term: Running of α(q²)
canonical_id: RUNNING_OF_ALPHA
symbol: Δα_Pir(q²)
aliases: [alpha running, Pirouette vacuum polarization correction]
parents: [MATH-020]
children: [MATH-018]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-020
      lines: "B4"
      snippet: |
        B4 — Observables from Flow
        • Running α(q²): compute Δα_Pir(q²) via vacuum polarization kernels along flow.
  editors: [GPT-4]
  review_log: []
triad:
  art: |
    The vacuum is not a void but a shimmering sea of potential. As we change our focus from the grand to the granular, the fundamental forces themselves shift their hue, and the very strength of light's coupling to matter is revealed as a current in this sea, not a constant stone.
  law: |
    The Pirouette contribution to the running of the fine-structure constant, Δα_Pir(q²), is the change in the effective U(1) coupling extracted from the two-point vertex function of the coarse-grained (Γ,K) action, integrated along the renormalization group (RG) flow from a UV scale μ_UV down to the momentum scale q. This contribution must be stable and reproducible under a change of lattice blocking factor `b` (e.g., b=2 vs b=3) to within the stochastic estimator variance (≤ 1e-3).
  philosophy: |
    This term operationalizes the core RG principle within Pirouette: fundamental "constants" are scale-dependent artifacts of an effective theory. By computing α's running non-perturbatively from the framework's own degrees of freedom, we provide a self-contained, falsifiable prediction for how electromagnetism emerges and behaves, bridging the gap between the UV structure and low-energy precision observables.
pirouette_definition: |
  The Pirouette-specific contribution to the running of the fine-structure constant, denoted Δα_Pir(q²). It is computed by integrating the renormalization group (RG) flow of the U(1) gauge coupling, derived from the two-point vertex of the coarse-grained (Γ,K) effective action. The procedure, specified in MATH-020 B, involves a numerical lattice scheme to flow from a UV fixed point down to an IR scale characterized by the momentum transfer q². The result is a momentum-dependent correction to the bare fine-structure constant.
operational_definition:
  units: dimensionless
  symbol_table:
    - name: Δα_Pir(q²)
      meaning: Pirouette contribution to the running of α
      dimensions: dimensionless
      default_range: contextual, typically 10⁻¹⁰ to 10⁻⁴
    - name: q²
      meaning: Four-momentum transfer squared
      dimensions: M²L²T⁻²
      default_range: contextual, e.g., (91.2 GeV)²
    - name: μ
      meaning: Renormalization scale
      dimensions: MLT⁻¹
      default_range: contextual
  measurement:
    procedures:
      - name: RG Coarse-Graining on (Γ,K) Lattice
        outline: |
          Per MATH-020 B, define the (Γ,K) action on a lattice Ω_L. Use a block-spin transformation to coarse-grain by a factor `b`. At each step of the RG flow (parameterized by scale μ), extract the effective U(1) coupling by matching the 2-point vertex function. Integrate the resulting β-function `d g / d ln μ` from a UV scale to the target scale `q` to obtain the total change Δα_Pir(q²).
        expected_signals: [A table of `(q², Δα_Pir)` values as specified in the `result_rg.json` artifact, typically showing a smooth, monotonically increasing function of q².]
        pitfalls: [Finite volume effects on the lattice, critical slowing down near fixed points, high variance in stochastic Monte-Carlo estimators for vertex functions.]
context_windows:
  - module: MATH-020
    excerpt: |
      Scope • Observables: a_ℓ (ℓ∈{e,μ,τ}), muonium hyperfine Δν, running α(q²) corrections, EDM suppression checks, and ratio tests (hadronic insulation). • Outputs are used by the Preregistered Prediction Docket (MATH‑018 P4) and must comply with Dictionary mappings (MATH‑019).
  - module: MATH-020
    excerpt: |
      B4 — Observables from Flow • Running α(q²): compute Δα_Pir(q²) via vacuum polarization kernels along flow. • EDM suppression: ensure CP‑even classes keep d_e at zero to leading order; quantify next‑order via irrelevant operator scaling. • Ratio stability: confirm hadron‑insulating ratios R remain scale‑stable within tolerance.
poetic_connections:
  motifs: [scale dependence, vacuum polarization, effective field theory, renormalization]
  evocative_lines:
    - "...running a coarse‑graining renormalization group (RG) flow on (Γ,K) to expose UV/IR structure..."
    - "...map phases (free, confined‑like, gravitational‑limit)."
  association_matrix:
    - [ "RENORMALIZATION_GROUP_FLOW", 0.9 ]
    - [ "FIXED_POINT", 0.8 ]
    - [ "HADRONIC_INSULATION", 0.3 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Δα(q²) (SM running of fine-structure constant)
      rationale: |
        Δα_Pir(q²) is the Pirouette framework's analogue to the Standard Model's leptonic (Δα_lep) and hadronic (Δα_had) vacuum polarization contributions. It represents a new, non-perturbative source of running from the framework's core (Γ,K) fields, intended to be added to the SM contributions: α(q²) = α(0) / (1 - [Δα_lep(q²) + Δα_had(q²) + Δα_Pir(q²)]).
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The Pirouette contribution Δα_Pir(q²) is non-zero and accounts for the discrepancy between SM predictions and experimental measurements of α(M_Z²)."
      domain: phenomenology
      falsifier: "High-precision measurements of α at different energy scales are inconsistent with the sum of the SM prediction and the calculated Δα_Pir(q²). Alternatively, if the calculation yields a value statistically consistent with zero where a non-zero value is required."
      status: proposed
      links: [MATH-018, MATH-020]
naming_notes:
  collisions: [The symbol "α(q²)" typically refers to the full, measured running constant. Δα_Pir(q²) is only the Pirouette *contribution* to this running.]
  disambiguation: |
    This term refers *only* to the contribution from the Pirouette sector fields (Γ,K) as computed by the RG flow in MATH-020. It must be added to the Standard Model leptonic and hadronic contributions, not used as a replacement for them.
crosslinks:
  near_synonyms: []
  antonyms: [BARE_COUPLING]
  prerequisites: [RENORMALIZATION_GROUP_FLOW, FIXED_POINT]
  downstream_effects: [PREREGISTERED_PREDICTION_DOCKET]
license: CC-BY-SA-4.0
---

# Running of α(q²)

## Canonical (Pirouette)
The Pirouette-specific contribution to the running of the fine-structure constant, denoted Δα_Pir(q²). It is computed by integrating the renormalization group (RG) flow of the U(1) gauge coupling, derived from the two-point vertex of the coarse-grained (Γ,K) effective action. The procedure, specified in MATH-020 B, involves a numerical lattice scheme to flow from a UV fixed point down to an IR scale characterized by the momentum transfer q². The result is a momentum-dependent correction to the bare fine-structure constant.

## EFT-First Summary
In the Standard Model, the fine-structure constant α is not a constant but "runs" with energy scale `q²` due to vacuum polarization effects. The Pirouette framework introduces a new, analogous contribution to this running, `Δα_Pir(q²)`, which arises from the vacuum effects of its own core fields. This term is calculated non-perturbatively and is intended to be added directly to the known leptonic and hadronic contributions, providing a testable prediction for precision electroweak observables.

## Glossary Links
- See also: RENORMALIZATION_GROUP_FLOW, FIXED_POINT