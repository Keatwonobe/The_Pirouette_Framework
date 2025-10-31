---
term: "Lorentz Invariance"
canonical_id: "LORENTZ_INVARIANCE"
symbol: ""
aliases: [Covariance]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-025"]
---

---
term: Lorentz Invariance
canonical_id: LORENTZ_INVARIANCE
symbol: N/A
aliases: [Covariance, Relativity]
parents: [DOMA-025]
children: [CORE-007]
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-025
      lines: "L1-L2"
      snippet: |
        A physical law that changes depending on who is watching is not a law, but an opinion. A song whose melody bends when you run is not a melody of truth.
  editors: [system]
  review_log: []
triad:
  art: |
    The universe's song must have the same melody for all dancers, whether they stand still or race alongside a beam of light. Its harmony cannot be a matter of perspective, but an absolute constant of spacetime.
  law: |
    The mathematical form of physical laws, specifically the Pirouette Action `S = ∫ d⁴x √-g 𝓛`, must be identical in all inertial reference frames. This is enforced by ensuring the Lagrangian Density `𝓛` is constructed as a Lorentz scalar.
  philosophy: |
    Lorentz Invariance guarantees that the Principle of Maximal Coherence is a universal, observer-independent truth, not a parochial feature of a single reference frame. It elevates the framework from a conceptual model to a candidate fundamental theory by grounding it in the rigorous, established language of covariant field theory.
pirouette_definition: |
  The principle that the laws of physics, derived from the invariant Pirouette Action, are the same for all observers in uniform relative motion. This is achieved by constructing the Lagrangian Density from Lorentz scalars and tensors, such as `g^μν (∂_μ C)^* (∂_ν C)`, ensuring that the fundamental drive for Maximal Coherence is a universal, not a perspectival, law. This covariance is considered an innate property of a time-first framework, not an external constraint.
operational_definition:
  units: Dimensionless principle
  symbol_table:
    - name: N/A
      meaning: This is a foundational principle, not a measurable quantity with its own symbol.
      dimensions: Dimensionless
      default_range: N/A
  measurement:
    procedures:
      - name: Test of Relativistic Kinematics
        outline: |
          Measure the lifetime of unstable particles accelerated to relativistic speeds in a particle accelerator. Compare the measured lifetime in the lab frame to the particle's known proper lifetime (lifetime in its rest frame). The discrepancy must match the time dilation prediction `γ = (1 - v²/c²)^(-1/2)`.
        expected_signals: [Particle decay rates consistent with Special Relativity's time dilation formula.]
        pitfalls: [Imprecise velocity measurements, uncertainty in the particle's proper lifetime.]
      - name: Test for Anisotropy of Spacetime
        outline: |
          Perform a modern Michelson-Morley experiment using resonant optical cavities. Search for tiny changes in the resonant frequency of the cavities as they are rotated relative to the Earth's motion through the cosmos.
        expected_signals: [A null result; no frequency shift correlated with orientation.]
        pitfalls: [Thermal and mechanical instabilities mimicking a signal, unaccounted for gravitational effects.]
context_windows:
  - module: DOMA-025
    excerpt: |
      The dancer’s pirouette must appear just as graceful, the laws governing its stability just as true, whether viewed from the stage or from a passing starship. This is the mandate of Lorentz Invariance. In the time-first paradigm, this covariance is not an external constraint to be engineered; it is an innate consequence.
  - module: DOMA-025
    excerpt: |
      The Action for the entire universe of interacting fields is given by the integral of a Lagrangian Density (`𝓛`) over all of spacetime: `S = ∫ d⁴x √-g 𝓛`. By ensuring that `𝓛` is a Lorentz scalar—a quantity that has the same value in all reference frames—we guarantee that the Action, and the physics derived from it, are universal.
poetic_connections:
  motifs: [universal song, invariant dance, observer-independence, absolute harmony]
  evocative_lines:
    - "A melody that bends when you run is no melody of truth."
    - "The dance shapes the stage."
    - "...the universe's song... is not a local tune, but the anthem of spacetime itself."
  association_matrix:
    - [ "ACTION_PRINCIPLE", 0.9 ]
    - [ "LAGRANGIAN_DENSITY", 0.9 ]
    - [ "MAXIMAL_COHERENCE", 0.7 ]
    - [ "COHERENCE_FIELD", 0.5 ]
formal_mappings:
  candidates:
    - target: Lorentz Invariance / Principle of Covariance
      domain: GR|SM|QFT
      mapping_kind: mathematical
      equation_hint: |
        x' = Λx  →  𝓛'(x') = 𝓛(x)
      justification: |
        The Pirouette Framework explicitly adopts the core principle of modern physics that the Action must be a Lorentz scalar. The construction of the Lagrangian Density `𝓛` from scalar products of four-vectors and tensors is the standard, direct method for enforcing this invariance, making this a one-to-one mapping.
      references:
        - title: A. Zee, "Quantum Field Theory in a Nutshell"
          where: Part I.3
          date: 2010-03-22
      confidence: 1.0
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The Pirouette Lagrangian Density `𝓛 = [ g^μν (∂_μ C)^* (∂_ν C) + ... ] - V(|C|^2, Γ)` is a Lorentz scalar."
      domain: theory
      falsifier: "A mathematical proof showing that any term in the full Lagrangian, including the potential `V`, does not transform as a scalar under a Lorentz transformation, thereby breaking the invariance of the Action."
      status: proposed
      links: [DOMA-025]
    - statement: "No physical process governed by the Pirouette Framework will exhibit a violation of Lorentz Invariance."
      domain: experiment
      falsifier: "A confirmed experimental result, such as a direction-dependent speed of light or particle decay rates that contradict Special Relativity, which would falsify the foundational premise of the framework."
      status: supported
      links: []
naming_notes:
  collisions: []
  disambiguation: |
    While often used interchangeably in physics discourse, "invariance" technically refers to a quantity that does not change under a transformation (e.g., the value of `c`), while "covariance" refers to the form of an equation retaining its structure under transformation. The Pirouette Framework, like much of physics, uses "Lorentz Invariance" as the umbrella term for the principle that the laws of physics are covariant.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [ACTION_PRINCIPLE, LAGRANGIAN_DENSITY]
  downstream_effects: [STRESS_ENERGY_TENSOR, EQUATIONS_OF_MOTION]
license: CC-BY-SA-4.0
---

# Lorentz Invariance

## Canonical (Pirouette)
The principle that the laws of physics, derived from the invariant Pirouette Action, are the same for all observers in uniform relative motion. This is achieved by constructing the Lagrangian Density from Lorentz scalars and tensors, such as `g^μν (∂_μ C)^* (∂_ν C)`, ensuring that the fundamental drive for Maximal Coherence is a universal, not a perspectival, law. This covariance is considered an innate property of a time-first framework, not an external constraint.

## EFT-First Summary
Lorentz Invariance in the Pirouette Framework is a direct adoption of the Principle of Covariance from standard General Relativity and Quantum Field Theory. The framework enforces this principle by defining dynamics via an Action `S` whose Lagrangian Density `𝓛` is constructed as a Lorentz scalar. This ensures all derived physics are observer-independent, directly mapping Pirouette dynamics onto the established mathematical structure of modern physics. (Ref: A. Zee, "QFT in a Nutshell", Part I.3)

## Glossary Links
- See also: ACTION_PRINCIPLE, LAGRANGIAN_DENSITY, MAXIMAL_COHERENCE