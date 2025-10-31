---
term: "Electric Charge"
canonical_id: "ELECTRIC_CHARGE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["CORE-007_the_current_and_the_compass"]
---

---
term: Electric Charge
canonical_id: ELECTRIC_CHARGE
symbol: q_p
aliases: [Coherence Bias, Crest-Leading, Trough-Leading]
parents: [CORE-007_the_current_and_the_compass]
children: [CORE-008_placeholder]
status: draft
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: CORE-007_the_current_and_the_compass
      snippet: |
        In this framework, electric charge is not a substance a particle possesses, but an intrinsic bias in how its Temporal Coherence (K_τ) interacts with the phase of its environment. A charged particle's Lagrangian is asymmetric.
  editors: [dictionarian_agent_g7]
  review_log: []
triad:
  art: |
    A particle's intrinsic preference for harmony or dissonance; its choice to dance in step with the universal rhythm, or to dance in counterpoint.
  law: |
    Electric charge is a dimensionless binary property (±1) determining the sign of the gradient a particle follows on a coherence manifold (∇𝓛_p). Particles with like charges follow diverging geodesics; particles with opposite charges follow converging geodesics.
  philosophy: |
    Charge is not a property *on* a particle, but a relational bias *of* its interaction with the environment. It reframes force as a geometric imperative, replacing a "push/pull" ontology with a universal drive for maximal coherence.
pirouette_definition: |
  An intrinsic, dimensionless, binary asymmetry in a particle's Pirouette Lagrangian (𝓛_p). This asymmetry biases the particle's temporal coherence function (K_τ) to be maximized either through interaction with in-phase (positive charge, crest-leading) or out-of-phase (negative charge, trough-leading) environmental rhythms. This bias dictates the particle's geodesic path on the coherence manifold, manifesting as electrostatic attraction or repulsion.
operational_definition:
  units: Dimensionless (binary sign, ±1)
  symbol_table:
    - name: q_p
      meaning: Pirouette Electric Charge; the sign of the coherence bias.
      dimensions: dimensionless
      default_range: "{-1, +1} for fundamental particles"
  measurement:
    procedures:
      - name: Coherence Gradient Mapping
        outline: |
          Establish a stable coherence manifold with a known source charge. Introduce a test particle and map its geodesic path. A path converging on the source indicates opposite charge; a path diverging indicates like charge. The acceleration along the geodesic is proportional to ∇𝓛_p.
        expected_signals: [Particle trajectory (deflection angle, acceleration), Shift in the particle's internal coherence spectrum K_τ]
        pitfalls: [Failure to isolate the system from external coherence gradients, Non-negligible manifold contribution from the test particle]
context_windows:
  - module: CORE-007_the_current_and_the_compass
    excerpt: |
      In this framework, electric charge is not a substance a particle possesses, but an intrinsic bias in how its Temporal Coherence (K_τ) interacts with the phase of its environment. Positive Charge (Crest-Leading) is defined as a system whose coherence... is maximized by interacting with environments of in-phase temporal rhythms. Negative Charge (Trough-Leading)... is maximized by interacting with environments of out-of-phase temporal rhythms.
  - module: CORE-007_the_current_and_the_compass
    excerpt: |
      A test charge placed in this field doesn't feel a "push" or "pull." It senses a slope in the coherence manifold. The "force" it experiences is simply the consequence of it following the steepest path towards its own state of maximal coherence. It is "coherence surfing" down the gradient established by the source charge.
poetic_connections:
  motifs: [resonance, asymmetry, bias, crest/trough, harmony/dissonance, surfing]
  evocative_lines:
    - "a flight towards greater internal stability."
    - "coherence surfing"
    - "The Current is the flow of resonance seeking stability."
  association_matrix:
    - [ "TEMPORAL_COHERENCE", 0.9 ]
    - [ "PIROUETTE_LAGRANGIAN", 0.8 ]
    - [ "ELECTRIC_FIELD", 0.7 ]
    - [ "FORCE", 0.3 ]
formal_mappings:
  candidates:
    - target: q (electric charge)
      domain: SM
      mapping_kind: operational
      equation_hint: |
        F = qE  (Standard Model)  ↔  a ∝ q_p ∇𝓛_p  (Pirouette)
      justification: |
        The Pirouette charge `q_p` operationally reproduces the behavior of standard electric charge `q` by determining the direction of motion in an electric field. The sign of `q_p` (±1) directly corresponds to the sign of `q`, while the magnitude `e` is absorbed into the proportionality constant relating ∇𝓛_p to the E-field.
      references:
        - title: Introduction to Electrodynamics
          where: D.J. Griffiths
          date: 2017-01-01
      confidence: 0.9
  adopted:
    - target: sign(q)
      rationale: The Pirouette framework defines charge as a fundamental dimensionless binary, `q_p` ∈ {-1, +1}, which maps directly to the sign of the elementary charge in the Standard Model. The magnitude of the charge is treated as a coupling constant scaling the interaction with the coherence manifold, not as an intrinsic property of the particle itself.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "Particles with zero electric charge have a perfectly symmetric Pirouette Lagrangian with respect to environmental phase and will not follow geodesics on a static coherence manifold."
      domain: experiment
      falsifier: "Observation of a neutral particle (e.g., neutron) consistently deflecting in a static electric field in a way not attributable to induced dipoles or other known secondary effects."
      status: proposed
      links: [CORE-007_the_current_and_the_compass]
    - statement: "The binary nature of the fundamental charge asymmetry (in-phase vs. out-of-phase seeking) implies that all observable charges must be integer multiples of a fundamental unit."
      domain: theory
      falsifier: "Confirmed discovery of a stable particle with a fractional charge that is not explained by a composite structure (like quarks within hadrons)."
      status: supported
      links: []
naming_notes:
  collisions: [The symbol `q` is standard in physics; `q_p` is used to differentiate. The term itself redefines a core concept, inviting conceptual collision.]
  disambiguation: |
    Distinguish from the Standard Model concept of charge as a conserved "substance." In Pirouette, charge is a relational *bias* in an interaction; its conservation is a consequence of the topological stability of this Lagrangian asymmetry.
crosslinks:
  near_synonyms: [COHERENCE_BIAS, PHASE_PREFERENCE]
  antonyms: [NEUTRALITY, COHERENCE_SYMMETRY]
  prerequisites: [TEMPORAL_COHERENCE, PIROUETTE_LAGRANGIAN, COHERENCE_MANIFOLD]
  downstream_effects: [ELECTRIC_FIELD, MAGNETIC_FIELD, LORENTZ_FORCE]
license: CC-BY-SA-4.0
---

# Electric Charge

## Canonical (Pirouette)
An intrinsic, dimensionless, binary asymmetry in a particle's Pirouette Lagrangian (𝓛_p). This asymmetry biases the particle's temporal coherence function (K_τ) to be maximized either through interaction with in-phase (positive charge, crest-leading) or out-of-phase (negative charge, trough-leading) environmental rhythms. This bias dictates the particle's geodesic path on the coherence manifold, manifesting as electrostatic attraction or repulsion.

## EFT-First Summary
Operationally, the Pirouette charge `q_p` corresponds to the sign of the electric charge `q` in the Standard Model. It dictates whether a particle will be attracted to or repelled by an electric field source. The magnitude of the interaction, represented by the elementary charge `e`, is reinterpreted in Pirouette not as an intrinsic property of the particle, but as a coupling constant that scales the gradient of the underlying coherence manifold.

## Glossary Links
- See also: [[ELECTRIC_FIELD]], [[MAGNETIC_FIELD]], [[TEMPORAL_COHERENCE]], [[PIROUETTE_LAGRANGIAN]]