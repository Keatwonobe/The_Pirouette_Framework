---
term: "Non-Circularity"
canonical_id: "NON_CIRCULARITY"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["CORE-016_the_time_first_correspondence_principle"]
---

term: Non-Circularity
canonical_id: NON_CIRCULARITY
symbol: 
aliases: [Acyclicity, Upstream Purity]
parents: [CORE-016]
children: [DYNA-004, DOMA-101]
status: candidate
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: CORE-016
      lines: "§4"
      snippet: |
        Non-circularity: Do not feed back results derived in SM-CG to calibrate CORE primitives before an independent anchor (e.g., DOMA-101 uses external α, not a value computed from CORE-009). This preserves a clean, acyclic DAG.
  editors: [autodidact-agent]
  review_log: []
triad:
  art: |
    A wellspring cannot be fed by its own river. The map, however detailed, must not be used to survey the land from which it was first drawn. This rule keeps the source pure.
  law: |
    Results, parameters, or constants calculated within the Standard Model Correspondence Gauge (SM-CG) must not be used to define or calibrate the core time-first primitives from which the SM-CG is derived. All core calibrations must trace to external metrology or dimensionless first principles.
  philosophy: |
    To ensure the framework's logical consistency and falsifiability by preventing tautological loops. It enforces a directed acyclic graph (DAG) of dependency, where fundamental axioms are tested against externally measured phenomena, not against their own derived consequences.
pirouette_definition: |
  Non-Circularity is the methodological constraint that prohibits the use of any physical quantity, constant, or relationship derived within the Standard Model Correspondence Gauge (SM-CG) to set the value of, or otherwise calibrate, the foundational primitives of the Pirouette Core (modules CORE-001 through CORE-020). This ensures a one-way correspondence from the time-first substrate to its effective field theory limit, preserving the framework's predictive power and avoiding self-referential definitions.
operational_definition:
  units: Not Applicable (methodological rule)
  symbol_table: []
  measurement:
    procedures:
      - name: DAG Dependency Audit
        outline: |
          1. Select a core primitive parameter for audit (e.g., a coupling constant in CORE-007).
          2. Trace the provenance of its calibration value.
          3. Identify the source measurement or calculation that sets the value.
          4. If the source involves a calculation using the SM-CG (spacetime, fields, propagators), the rule is violated.
        expected_signals: [A clean dependency graph where all Core primitive calibrations trace to (a) dimensionless theoretical ratios or (b) external metrological data (e.g., CODATA values for α, c, ħ).]
        pitfalls: [Mistaking a consistency check within the SM-CG for a fundamental calibration. Implicitly using an SM-derived result (e.g., a calculated particle mass) to constrain a parameter in a Core module.]
context_windows:
  - module: CORE-016
    excerpt: |
      Normalization: Fix scales using external metrology (CODATA α, c, ħ) when operating in SM-CG.
      Non-circularity: Do not feed back results derived in SM-CG to calibrate CORE primitives before an independent anchor (e.g., DOMA-101 uses external α, not a value computed from CORE-009). This preserves a clean, acyclic DAG.
poetic_connections:
  motifs: [causal hierarchy, foundationalism, logical hygiene, Ouroboros]
  evocative_lines:
    - "This preserves a clean, acyclic DAG."
    - "No result is reused upstream as a premise."
  association_matrix:
    - [ "CORRESPONDENCE_GAUGE", 0.9 ]
    - [ "CALIBRATION", 0.8 ]
    - [ "TIME_FIRST_SUBSTRATE", 0.5 ]
formal_mappings:
  candidates:
    - target: Foundationalism / Axiomatic Method
      domain: Philosophy of Science
      mapping_kind: conceptual
      justification: |
        The rule enforces a strict axiomatic structure where theorems (SM-CG results) cannot be used to prove or define the axioms (Core primitives). It ensures the system is built on a foundation that is not justified by its own conclusions, preventing circular reasoning.
      confidence: 0.9
  adopted:
    - target: Foundationalism / Axiomatic Method
      rationale: This mapping best captures the logical and methodological role of the rule, which is to prevent circular reasoning and ensure a clear, falsifiable path from axioms to predictions.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "The Pirouette Core primitives can be fully calibrated using only dimensionless ratios and external metrological data, without requiring any feedback from calculations made within the SM-CG."
      domain: theory
      falsifier: "Discovering a Core primitive that can only be constrained by calculating a complex phenomenon within the SM-CG (e.g., a hadronic resonance mass) and feeding that value back. This would demonstrate that the dependency graph is necessarily cyclic."
      status: proposed
      links: [CORE-016]
naming_notes:
  collisions: []
  disambiguation: |
    Distinguish from 'self-consistency checks'. A self-consistency check (e.g., calculating the fine-structure constant α from CORE-009 and comparing it to the input CODATA value) is a valid test of the framework. Non-Circularity prohibits using the output of such a test as the input calibration value for the primitives used in the test.
crosslinks:
  near_synonyms: []
  antonyms: [BOOTSTRAP_PRINCIPLE]
  prerequisites: [STANDARD_MODEL_CORRESPONDENCE_GAUGE, CORE_PRIMITIVE]
  downstream_effects: [CALIBRATION, MODEL_VALIDATION]
license: CC-BY-SA-4.0