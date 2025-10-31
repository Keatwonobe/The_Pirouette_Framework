---
term: "Portal/topology indices"
canonical_id: "PORTAL_TOPOLOGY_INDICES"
symbol: "T"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-018"]
---

---
term: Portal/topology indices
canonical_id: PORTAL_TOPOLOGY_INDICES
symbol: T
aliases: [Wound channel index, Portal selector]
parents: [MATH-018]
children: [QFT-004 (Lepton Anomalies)]
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-018
      lines: "D1"
      snippet: |
        Portal/topology indices T = {t_j}: integer or signed indices attached to spinorial/topological class; sign and scaling must follow from topology, not data fitting.
  editors: [chain-of-thought-agent]
  review_log: []
triad:
  art: |
    A system's intrinsic knots, counting the twists that permit passage between sectors. Not a dial to be turned, but a quantum number etched by topology itself, fixing the shape of interaction.
  law: |
    Portal/topology indices `T` must be integers or signed half-integers derived from a spinorial or topological classification. They are **never** treated as continuous, free parameters to be optimized against data. A model's choice of `T` values must be falsified via preregistered, out-of-sample tests.
  philosophy: |
    To enforce predictivity by replacing arbitrary, fittable exponents with non-negotiable integers of topological origin. This transforms potential 'tuning knobs' into fixed structural constants, ensuring the model's architecture is determined by symmetry and consistency, not by accommodating data.
pirouette_definition: |
  A set of dimensionless integer or signed half-integer indices, `T = {t_j}`, that classify interactions based on their spinorial or topological properties. Each `t_j` selects a discrete "channel" or interaction form, analogous to a quantum number. Per MATH-018, these indices are derived from theory (e.g., from classifying topological defects or representations) and are frozen post-anchoring. They are explicitly forbidden from being treated as continuous variables or being tuned to improve data fits, serving as a primary guardrail against ad-hoc model calibration.
operational_definition:
  units: dimensionless
  symbol_table:
    - name: T
      meaning: The set of all portal/topology indices for a given model.
      dimensions: dimensionless
      default_range: N/A (set)
    - name: t_j
      meaning: A specific portal/topology index.
      dimensions: dimensionless
      default_range: Typically small integers, e.g., {-2, -1, 0, 1, 2}.
  measurement:
    procedures:
      - name: Topological Class Identification & Validation
        outline: |
          1. For a given interaction, identify the relevant topological space or symmetry group.
          2. Mathematically classify the allowed defect classes or irreducible representations (e.g., using homotopy or group theory).
          3. Assign integer indices `t_j` to these discrete classes.
          4. For each candidate `t_j`, generate and preregister (P4) predictions for a set of out-of-sample observables.
          5. Compare model performance against data. The correct `t_j` is the one whose model is validated by out-of-sample tests and preferred by Bayesian evidence (D5).
        expected_signals: [A single set of integer `t_j` values successfully predicts multiple observables across different families (P3), The integer-`T` model shows a decisively better Bayes factor than a variant with a continuous, fitted exponent (D5)]
        pitfalls: [Misidentification of the relevant topological group, Forcing a genuinely continuous scaling phenomenon into a discrete index, Finding a `t_j` that fits one observable but fails on others (indicates model mis-specification)]
context_windows:
  - module: MATH-018
    excerpt: |
      Universal constants U = {u_k}: derivable from axioms/symmetries only...
      Portal/topology indices T = {t_j}: integer or signed indices attached to spinorial/topological class; sign and scaling must follow from topology, not data fitting.
      Nuisance parameters N = {n_m}: experimental or environmental; may be taken from external literature but **never tuned** to improve fit.
  - module: MATH-018
    excerpt: |
      If a continuous exponent was used for mass scaling, either (i) prove it via D2 [Symmetry-Fixed Functional Forms] or (ii) mark Deprecated and migrate to topology index T.
  - module: MATH-018
    excerpt: |
      Appendix A — Dictionary Stubs
      ...
      • Wound channel → topological defect class; integer index = portal selector T.
poetic_connections:
  motifs: [quantum number, winding number, selection rule, channel, knot, defect]
  evocative_lines:
    - "Wound channel → topological defect class; integer index = portal selector T."
    - "sign and scaling must follow from topology, not data fitting."
  association_matrix:
    - [ "SYMMETRY_FIXED_FUNCTIONAL_FORM", 0.9 ]
    - [ "WOUND_CHANNEL", 0.8 ]
    - [ "ONE_SHOT_ANCHORING", 0.7 ]
    - [ "FITTED_EXPONENT", -1.0 ]
formal_mappings:
  candidates:
    - target: Chern number (C)
      domain: Math|CM
      mapping_kind: conceptual
      equation_hint: |
        σ_xy = C * (e²/h)
      justification: |
        In phenomena like the Quantum Hall Effect, a topological invariant (the Chern number) emerges as a robust, integer quantum number that classifies the system's phase and dictates a macroscopic observable. `T` plays the same role in Pirouette: a non-perturbative, integer index that classifies the vacuum structure or interaction channel.
      references:
        - title: "Topological insulators and topological superconductors"
          where: "Rev. Mod. Phys. 82, 3045"
          date: 2010-10-05
      confidence: 0.8
    - target: Winding number / Homotopy class
      domain: Math
      mapping_kind: mathematical
      justification: |
        Many topological defects (vortices, skyrmions) are classified by integer winding numbers from homotopy groups (e.g., π_n(S^m)). The "Wound channel" alias for `T` suggests a direct mapping where `t_j` is literally the winding number of a field configuration.
      references:
        - title: "Geometry, Topology and Physics"
          where: "Nakahara, M."
          date: 2003-01-01
      confidence: 0.7
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "For a family of related observables (e.g., lepton g-2), a model using a single, fixed integer `T` will have greater predictive power (higher Bayes factor, better out-of-sample performance) than an alternative model where the corresponding scaling exponent is a free, continuous parameter."
      domain: phenomenology
      falsifier: "Demonstrate a set of observables where a model with a continuous, non-integer scaling exponent consistently and significantly outperforms all plausible integer `T` models, as measured by preregistered out-of-sample tests and model selection criteria (per MATH-018 D5)."
      status: proposed
      links: [MATH-018]
naming_notes:
  collisions: [T (Temperature), T (Kinetic Energy), T (Time), T (Tensor)]
  disambiguation: |
    Within Pirouette parameter tables, `T` is reserved for this class of indices. In equations, context must distinguish it from thermodynamic temperature or kinetic energy. It is never a dynamic variable. The full name "Portal/topology index" should be used where ambiguity is possible.
crosslinks:
  near_synonyms: [WOUND_CHANNEL_INDEX]
  antonyms: [NUISANCE_PARAMETER, FITTED_EXPONENT]
  prerequisites: [SYMMETRY_FIXED_FUNCTIONAL_FORM]
  downstream_effects: [ONE_SHOT_ANCHORING]
license: CC-BY-SA-4.0
---