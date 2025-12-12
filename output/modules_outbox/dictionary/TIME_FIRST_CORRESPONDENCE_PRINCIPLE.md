---
term: "Time-First Correspondence Principle"
canonical_id: "TIME_FIRST_CORRESPONDENCE_PRINCIPLE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["CORE-016_the_time_first_correspondence_principle"]
---

---
term: Time-First Correspondence Principle
canonical_id: TIME_FIRST_CORRESPONDENCE_PRINCIPLE
symbol: N/A (Defines the mapping Σ)
aliases: ["SM-CG", "Standard Model Correspondence Gauge"]
parents: ["CORE-001", "CORE-006"]
children: ["DYNA-004", "DOMA-101"]
status: candidate
version: 1.0
last_updated: 2025-10-17
provenance:
  sources:
    - module: CORE-016_the_time_first_correspondence_principle
      lines: "§2"
      snippet: |
        Choose a spatialization map Σ that assigns local charts [x,y,z] to the time substrate so that, in the high-coherence, high-event-density limit, the effective action reduces to the Standard Model Lagrangian on a Lorentzian manifold.
  editors: ["system"]
  review_log: []
triad:
  art: |
    Space is but a shadow cast by the dance of Time. We live within that shadow, charting its familiar laws, while the true music plays in a dimension we can only infer.
  law: |
    There must exist a spatialization map Σ that translates the dynamics of the time-first substrate (Ki, Γ) into the Standard Model Lagrangian. This mapping must be consistent across all observable energy scales and produce no predictions that contradict established SM/GR results within their domains of validity.
  philosophy: |
    This principle reconciles Pirouette's time-only ontology with the overwhelming success of spacetime-based physics (QFT/GR). It frames spacetime not as a fundamental reality, but as a highly effective, emergent coordinate system, preserving the utility of established physics while re-grounding its ontological basis.
pirouette_definition: |
  The principle that physical reality is a time-only substrate, and that the four-dimensional spacetime and field content of the Standard Model (SM) and General Relativity (GR) are an effective description that emerges in the high-density, high-coherence limit. It posits the existence of a spatialization map, Σ, which acts as a correspondence gauge (SM-CG) to translate the substrate's dynamics into the familiar Lagrangian of the SM, treating space [x,y,z] as a derived chart, not a fundamental entity.
operational_definition:
  units: N/A (Principle/Gauge)
  symbol_table:
    - name: Σ
      meaning: The spatialization map, a gauge choice that assigns local spatial charts [x,y,z] to the time-first substrate.
      dimensions: Mapping (Functional)
      default_range: N/A
  measurement:
    procedures:
      - name: SM-CG Consistency Check
        outline: |
          1. Derive a prediction from a Pirouette core module (e.g., interaction cross-section from CORE-007).
          2. Apply the Standard Model Correspondence Gauge (SM-CG) via the spatialization map Σ to translate the result into the language of QFT (fields, momenta, spacetime coordinates).
          3. Compare the translated prediction with experimental results from particle accelerators (e.g., LHC) or precision measurements (e.g., g-2).
          4. Verify that the result matches the SM prediction within measurement uncertainty.
        expected_signals: ["Recovery of SM scattering amplitudes", "Correct prediction of particle masses and coupling constants after calibration"]
        pitfalls: ["Incorrect choice of Σ leading to gauge artifacts", "Circular reasoning if SM-derived data is used to calibrate the core substrate model before validation (see §4 of CORE-016)"]
context_windows:
  - module: CORE-016
    excerpt: |
      All that is, is Time. Physical “space” is a derived chart on a time-first substrate; coordinates [x,y,z] are a modeling gauge, not ontology... Choose a spatialization map Σ that assigns local charts [x,y,z] to the time substrate so that, in the high-coherence, high-event-density limit, the effective action reduces to the Standard Model Lagrangian...
  - module: CORE-016
    excerpt: |
      Do not feed back results derived in SM-CG to calibrate CORE primitives before an independent anchor... Standard Model/QFT successes in Pirouette are not coincidental: they are the Σ-shadow of a time-first substrate.
poetic_connections:
  motifs: ["shadow", "emergence", "gauge", "translation", "dictionary"]
  evocative_lines:
    - "space is a derived chart on a time-first substrate"
    - "the Σ-shadow of a time-first substrate"
  association_matrix:
    - [ "SPACETIME_AS_EMERGENT_PROPERTY", 1.0 ]
    - [ "TEMPORAL_PRESSURE", 0.7 ]
    - [ "KINETIC_INDUCTANCE", 0.7 ]
formal_mappings:
  candidates:
    - target: A_μ (Electromagnetic four-potential)
      domain: SM
      mapping_kind: mathematical
      equation_hint: |
        A_{μ} := ∂_{μ} arg(Ki)
      justification: |
        The principle maps the spacetime gradient of the phase of Kinetic Inductance (Ki), under the spatialization Σ, to the electromagnetic four-potential. This recovers the U(1) gauge symmetry of electromagnetism from the phase freedom of the underlying Ki field.
      references:
        - title: The Time-First Correspondence Principle
          where: CORE-016, §3
          date: 2025-10-17
      confidence: 0.9
    - target: R_μν - ½ g_μν R (Einstein tensor component)
      domain: GR
      mapping_kind: conceptual
      equation_hint: |
        ∇Γ ↔ Curvature
      justification: |
        Gradients in the Temporal Pressure (Γ) of the substrate are proposed to manifest as effective spacetime curvature under the Σ map. This aligns with the principle of equivalence, where gravitational effects are indistinguishable from acceleration within the substrate.
      references:
        - title: The Time-First Correspondence Principle
          where: CORE-016, §3
          date: 2025-10-17
      confidence: 0.8
  adopted:
    - target: Standard Model Lagrangian (S_SM)
      rationale: This principle is definitional: it *is* the gauge choice that recovers the Standard Model as a low-energy, high-density effective theory. Its purpose is to bridge Pirouette's ontology to established physics, not to propose an alternative model in the SM's domain.
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "The correspondence gauge Σ must be able to reproduce all Standard Model predictions without requiring fine-tuning for each energy scale."
      domain: theory
      falsifier: "Discovery of a fundamental physical phenomenon that cannot be described as an emergent property of a time-only substrate under any plausible spatialization map Σ. For example, a violation of Lorentz invariance that is not attributable to substrate effects."
      status: proposed
      links: ["CORE-016", "DYNA-004"]
    - statement: "All parameters of the Standard Model (masses, couplings) must be derivable from a smaller set of parameters governing the time-first substrate (e.g., coherence parameters from CORE-007)."
      domain: phenomenology
      falsifier: "If, after exhaustive analysis, the number of required free parameters in the Pirouette core model is greater than or equal to the number of free parameters in the Standard Model, the principle offers no increase in parsimony."
      status: proposed
      links: ["DOMA-101"]
naming_notes:
  collisions: ["SM-CG could be confused with 'Standard Model - Conjugate Gradient' in optimization contexts."]
  disambiguation: |
    `Time-First` refers to the ontological priority of time over space. `Correspondence Principle` is used in the spirit of Bohr's principle, ensuring that a new theory (Pirouette) reproduces the results of the old, successful theory (SM/GR) in the appropriate limit.
crosslinks:
  near_synonyms: ["STANDARD_MODEL_CORRESPONDENCE_GAUGE"]
  antonyms: ["SPACETIME_FUNDAMENTALISM"]
  prerequisites: ["TEMPORAL_SUBSTRATE", "KINETIC_INDUCTANCE"]
  downstream_effects: ["STANDARD_MODEL_AS_LIMIT_THEOREM", "ELECTROMAGNETIC_POTENTIAL"]
license: CC-BY-SA-4.0
---

# Time-First Correspondence Principle

## Canonical (Pirouette)
The principle that physical reality is a time-only substrate, and that the four-dimensional spacetime and field content of the Standard Model (SM) and General Relativity (GR) are an effective description that emerges in the high-density, high-coherence limit. It posits the existence of a spatialization map, Σ, which acts as a correspondence gauge (SM-CG) to translate the substrate's dynamics into the familiar Lagrangian of the SM, treating space [x,y,z] as a derived chart, not a fundamental entity.

## EFT-First Summary
The Time-First Correspondence Principle provides a dictionary to translate Pirouette's time-only substrate into the language of effective field theory. Under this gauge, the gradient of the Kinetic Inductance phase becomes the EM four-potential (A_μ), gradients in Temporal Pressure produce gravity, and the double-cover topology of the Ki motif generates spin-½ statistics. This allows all Standard Model and GR phenomena to be recovered as an effective, spatialized description of the underlying temporal dynamics.

## Glossary Links
- See also: [[STANDARD_MODEL_AS_LIMIT_THEOREM]], [[SPACETIME_AS_EMERGENT_PROPERTY]]