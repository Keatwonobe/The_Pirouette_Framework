---
term: "Weaver's Compass"
canonical_id: "WEAVER_S_COMPASS"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-018"]
---

---
term: Weaver's Compass
canonical_id: WEAVERS_COMPASS
symbol: 
aliases: []
parents: [DOMA-018]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-018
      lines: "§5"
      snippet: |
        This model provides a compass for the act of observation itself. We can never perceive a system's total presence at once. The nature of a Weaver's observation—their tools, their questions, their intent—preferentially engages one of the three coherence axes.
  editors: [system]
  review_log: []
triad:
  art: |
    To know a thing is to choose how you listen. The compass orients your ear to hear the notes of past, present, or future, but never the entire chord at once.
  law: |
    Any act of observation is a projection operator that preferentially couples to and excites one of the three coherence axes (K_p, K_i, K_r), making the resultant measurement a product of both the system's state and the observer's chosen angle of inquiry.
  philosophy: |
    There is no neutral, total observation of a system's coherence. The act of knowing is participatory and directional, shaping the phenomenon by the nature of the question asked. This principle grounds the framework's epistemology in an observer effect that is fundamental, not incidental.
pirouette_definition: |
  The Weaver's Compass is the principle that any act of observation, measurement, or interaction with a system is not a neutral act but a directed inquiry. This inquiry preferentially aligns with and excites one of the three orthogonal coherence axes—Prospective (K_p), Immediate (K_i), or Retrospective (K_r)—thereby shaping the measurement outcome. The observed state is a projection of the system's full coherence vector (**K**_τ) onto the observer's chosen axis of engagement.
operational_definition:
  units: Dimensionless (selection operator)
  symbol_table:
    - name: K_p
      meaning: Prospective Coherence
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: K_i
      meaning: Immediate Coherence
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: K_r
      meaning: Retrospective Coherence
      dimensions: dimensionless
      default_range: "[0, 1]"
  measurement:
    procedures:
      - name: Coherence Axis Probing
        outline: |
          Design an interaction or measurement that specifically targets one temporal modality. To probe K_r, perform historical analysis or trace a system's Wound Channel. To probe K_i, use real-time network interaction analysis or direct dialogue. To probe K_p, use predictive modeling, scenario planning, or quantum-state superposition tests. The experimental design itself sets the orientation of the compass.
        expected_signals: [High signal-to-noise ratio along the probed axis, Attenuated signals from orthogonal axes]
        pitfalls: [Observer Blindness (mistaking the measurement along one axis for the system's total state), Tool Bias (the measurement device being incapable of detecting signals from other axes)]
context_windows:
  - module: DOMA-018
    excerpt: |
      This model provides a compass for the act of observation itself. We can never perceive a system's total presence at once. The nature of a Weaver's observation—their tools, their questions, their intent—preferentially engages one of the three coherence axes. A quantum measurement or strategic forecast probes Prospective Coherence. A social network analysis or real-time dialogue probes Immediate Coherence. An archaeological dig or a study of memory probes Retrospective Coherence. Any act of knowing is an act of choosing an angle, of illuminating one facet of a being's temporal chord.
  - module: DOMA-018
    excerpt: |
      The coherence vector **K**_τ spans a space defined by a system's relationship to the past, present, and future. These three components are orthogonal because they represent fundamentally distinct modes of temporal engagement. An action purely in the present (K_i) does not, by definition, rewrite the past (K_r) or determine a single future (K_p) without a coupling mechanism. The Lagrangian provides that coupling.
poetic_connections:
  motifs: [angle of inquiry, listening to a chord, illuminating a facet, participatory observation]
  evocative_lines:
    - "Any act of knowing is an act of choosing an angle..."
    - "We sought to define a being and found instead a chord..."
  association_matrix:
    - [ "OBSERVERS_SHADOW", 0.8 ]
    - [ "TEMPORAL_COHERENCE_VECTOR", 0.7 ]
    - [ "WOUND_CHANNEL", 0.5 ]
formal_mappings:
  candidates:
    - target: Measurement operator / Projector (P̂)
      domain: Math
      mapping_kind: conceptual
      equation_hint: |
        ⟨ψ|P̂|ψ⟩
      justification: |
        The Weaver's Compass acts like a measurement operator in quantum mechanics, which projects a quantum state (analogous to the full coherence vector **K**_τ) onto a specific eigenstate (the measured value along one axis). The choice of measurement basis (e.g., position vs. momentum) is analogous to choosing which coherence axis to probe.
      references:
        - title: Quantum Computation and Quantum Information
          where: Nielsen & Chuang, Sec 2.2.3
          date: 2010-12-01
      confidence: 0.7
  adopted:
    - target: 
      rationale: 
      confidence: 0.0
constraints_and_falsifiers:
  claims:
    - statement: "It is impossible to simultaneously perform high-precision measurements of all three coherence components (K_p, K_i, K_r) for a complex system."
      domain: phenomenology
      falsifier: "Demonstration of a protocol or instrument that can measure the full **K**_τ vector at a single instant without mutual interference between the component measurements, akin to violating a temporal uncertainty principle."
      status: proposed
      links: [DOMA-018]
naming_notes:
  collisions: [Magnetic compass, Geometric compass]
  disambiguation: |
    This is not a physical device, but a principle of observational orientation in the abstract space of temporal coherence. It dictates *how* one measures, not *where* in physical space.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [TEMPORAL_COHERENCE_VECTOR, OBSERVERS_SHADOW]
  downstream_effects: []
license: CC-BY-SA-4.0
---

# Weaver's Compass

## Canonical (Pirouette)
The Weaver's Compass is the principle that any act of observation, measurement, or interaction with a system is not a neutral act but a directed inquiry. This inquiry preferentially aligns with and excites one of the three orthogonal coherence axes—Prospective (K_p), Immediate (K_i), or Retrospective (K_r)—thereby shaping the measurement outcome. The observed state is a projection of the system's full coherence vector (**K**_τ) onto the observer's chosen axis of engagement.

## EFT-First Summary
No direct mapping has been adopted. The Weaver's Compass serves a conceptual role analogous to a measurement operator or projector (e.g., `P̂`) in quantum mechanics, which selects a specific basis for measurement (e.g., position or momentum) and projects the system's state onto it. The act of choosing a temporal axis (*K*<sub>p</sub>, *K*<sub>i</sub>, or *K*<sub>r</sub>) is equivalent to choosing a measurement basis, collapsing the system's full temporal "wavefunction" into a specific, observable aspect.

## Glossary Links
- See also: Temporal Coherence Vector, Observer's Shadow