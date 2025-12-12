---
term: "SM Limit"
canonical_id: "SM_LIMIT"
symbol: ""
aliases: [High-coherence, high-event-density limit]
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["CORE-016_the_time_first_correspondence_principle"]
---

---
term: SM Limit
canonical_id: SM_LIMIT
symbol: —
aliases: [high-coherence, high-event-density limit, SM-CG]
parents: [CORE-016]
children: [DYNA-004, DOMA-101]
status: candidate
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: CORE-016
      lines: "L10-L16"
      snippet: |
        Choose a spatialization map Σ that assigns local charts [x,y,z] to the time substrate so that, in the high-coherence, high-event-density limit, the effective action reduces to the Standard Model Lagrangian on a Lorentzian manifold.
  editors: [GPT-4 (Pirouette Dictionary Agent)]
  review_log: []
triad:
  art: |
    From the granular flux of pure Time, a placid surface crystallizes—the familiar world of fields and forces, a stable reflection in the deep.
  law: |
    In any region where event density is sufficiently high and coherence fluctuations are sufficiently small, the time-first action `S_time` is empirically indistinguishable from the Standard Model action `S_SM` under the spatialization gauge Σ.
  philosophy: |
    The SM Limit establishes the Standard Model not as fundamental ontology, but as a powerfully effective description for a specific, stable regime of the time-first substrate. It grounds the successes of 20th-century physics within Pirouette without reifying its foundational assumptions, like a fundamental spacetime.
pirouette_definition: |
  The SM Limit is the physical regime, characterized by asymptotically high event density and low coherence fluctuations, where the time-first action (`S_time`) can be mapped by a spatialization gauge (Σ) to an effective action that is mathematically equivalent to the Standard Model Lagrangian (`S_SM`) on a derived Lorentzian manifold. Operations within this limit are said to be in the Standard Model Correspondence Gauge (SM-CG).
operational_definition:
  units: Dimensionless regime
  symbol_table:
    - name: ρ_event
      meaning: Event density in the effective spatial chart
      dimensions: T⁻¹ L⁻³
      default_range: "→ ∞"
    - name: δ_Ki
      meaning: Magnitude of coherence fluctuations
      dimensions: dimensionless
      default_range: "→ 0"
  measurement:
    procedures:
      - name: Correspondence Test
        outline: |
          1. Conduct a physical experiment (e.g., particle scattering, spectroscopy).
          2. Model the experiment using standard QFT/SM on a spacetime background, using CODATA-benchmarked constants.
          3. Compare the predictions to the measured outcomes.
          4. If the deviation between the SM prediction and the experimental result is below the instrumental noise floor, the system is operating within the SM Limit.
        expected_signals: [Agreement with SM predictions for cross-sections, particle masses, coupling constants (e.g., α)]
        pitfalls: [Mistaking new BSM physics for a deviation from the SM Limit itself, instrumental error masking subtle deviations expected outside the limit.]
context_windows:
  - module: CORE-016
    excerpt: |
      Choose a spatialization map Σ that assigns local charts [x,y,z] to the time substrate so that, in the high-coherence, high-event-density limit, the effective action reduces to the Standard Model Lagrangian... Any module that presumes fields on spacetime is canon in SM-CG, and a limit theorem of CORE-020, not ontology.
  - module: CORE-016
    excerpt: |
      Fix scales using external metrology (CODATA α, c, ħ) when operating in SM-CG. Do not feed back results derived in SM-CG to calibrate CORE primitives before an independent anchor... This preserves a clean, acyclic DAG.
poetic_connections:
  motifs: [emergence, correspondence, shadow-play, coarse-graining, stability]
  evocative_lines:
    - "...the Σ-shadow of a time-first substrate."
    - "Physical 'space' is a derived chart on a time-first substrate; coordinates [x,y,z] are a modeling gauge, not ontology."
  association_matrix:
    - [ "CORRESPONDENCE_PRINCIPLE", 0.9 ]
    - [ "SPATIALIZATION_GAUGE", 0.8 ]
    - [ "TIME_SUBSTRATE", 0.7 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Standard Model Effective Field Theory (SMEFT)
      domain: QFT/SM
      mapping_kind: mathematical
      equation_hint: |
        S_time[Ki, Γ, T_a]  →  S_SM[fields | g_{μν}]  as ρ_event → ∞, δ_Ki → 0
      rationale: "The mapping to the SM Lagrangian is adopted as the canonical correspondence. It frames all QFT calculations as operations within a specific, stable limit of the Pirouette framework, rather than as a description of fundamental reality."
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "Deviations from Standard Model predictions will appear in regimes of low event density or high coherence fluctuation, and these deviations will be systematically described by the `S_time` action."
      domain: phenomenology
      falsifier: "The discovery of new physics (e.g., at high energies or in cosmological voids) that is perfectly described by a simple extension to the SM Lagrangian (e.g., a new field) without any correlation to event density or coherence metrics. This would suggest the SM is closer to the true ontology, and the Pirouette correspondence is coincidental."
      status: proposed
      links: [CORE-016, CORE-020]
naming_notes:
  collisions: [The term 'SM Limit' is common in particle physics, often referring to the SM as a low-energy limit of a BSM theory (e.g., string theory).]
  disambiguation: |
    In Pirouette, the 'SM Limit' is not an energy limit, but a coherence/density limit of the underlying time-first substrate. The SM is the effective theory for the 'placid' regime, not necessarily the 'low-energy' one, though these may coincide in many scenarios.
crosslinks:
  near_synonyms: [SM_CORRESPONDENCE_GAUGE]
  antonyms: [SUBSTRATE_NATIVE_REGIME]
  prerequisites: [TIME_SUBSTRATE, EVENT_DENSITY, COHERENCE]
  downstream_effects: [ALL_SM_PHENOMENOLOGY]
license: CC-BY-SA-4.0
---

# SM Limit

## Canonical (Pirouette)
The SM Limit is the physical regime, characterized by asymptotically high event density and low coherence fluctuations, where the time-first action (`S_time`) can be mapped by a spatialization gauge (Σ) to an effective action that is mathematically equivalent to the Standard Model Lagrangian (`S_SM`) on a derived Lorentzian manifold. Operations within this limit are said to be in the Standard Model Correspondence Gauge (SM-CG).

## EFT-First Summary
The SM Limit posits that the Standard Model of particle physics is not a fundamental theory but an effective field theory that accurately describes the physical world in regions of high event-density and high coherence. In this regime, the underlying time-first dynamics of the Pirouette framework become mathematically indistinguishable from the familiar Lagrangian of the Standard Model operating on a derived spacetime manifold. All standard QFT predictions are recovered as a direct consequence of this correspondence.

## Glossary Links
- See also: CORRESPONDENCE_PRINCIPLE, SPATIALIZATION_GAUGE, TIME_SUBSTRATE