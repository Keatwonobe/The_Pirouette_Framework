---
term: "Charge"
canonical_id: "CHARGE"
symbol: "q"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["CORE-016_the_time_first_correspondence_principle"]
---

---
term: Charge
canonical_id: CHARGE
symbol: q
aliases: []
parents: [CORE-016, CORE-007]
children: [DYNA-004]
status: candidate
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: CORE-016_the_time_first_correspondence_principle
      lines: "§3"
      snippet: |
        Charge: q := orientation/asymmetry of coherence coupling in CORE-007 (crest- vs trough-leading).
  editors: [system-agent]
  review_log: []
triad:
  art: |
    A fundamental handedness in how events synchronize. It is the universe's choice to lead with its left or right foot in the dance of coherence, determining attraction or repulsion.
  law: |
    Charge is a conserved, quantized property whose sign determines the direction of momentum exchange in a coherence coupling interaction. The net charge of any isolated system is invariant under temporal evolution.
  philosophy: |
    Charge is not an intrinsic, inexplicable 'paint' on a particle, but an emergent, relational property describing the *how* of interaction. It recasts a static attribute as a dynamic, orientational asymmetry, grounding it in the time-first substrate.
pirouette_definition: |
  In the time-first model, Charge (`q`) is the discrete, signed orientation of a coherence coupling (defined in CORE-007). It represents the intrinsic asymmetry in how two coherent motifs interact, specifically whether the interaction is 'crest-leading' or 'trough-leading'. This binary choice determines the sign of the effective electromagnetic force under the SM-CG correspondence gauge.
operational_definition:
  units: Dimensionless (quantized in units of elementary charge, `e`)
  symbol_table:
    - name: q
      meaning: Charge
      dimensions: dimensionless
      default_range: n * e, where n ∈ {-1, -2/3, -1/3, +1/3, +2/3, +1}
    - name: e
      meaning: Elementary charge
      dimensions: dimensionless
      default_range: 1 (by convention in fundamental units)
  measurement:
    procedures:
      - name: Coherence Coupling Asymmetry Test (CCAT)
        outline: |
          1. Under the SM-CG, prepare a system of two interacting coherent motifs.
          2. Measure the momentum transfer between them via the effective force (e.g., Coulomb scattering).
          3. The sign of the force (attractive vs. repulsive for like-signed test charges) directly corresponds to the relative orientation of their coherence couplings. A repulsive force between two motifs indicates they share the same charge orientation.
        expected_signals: [Deflection angle in a scattering experiment, Lorentz force on a moving motif]
        pitfalls: [Conflating charge with other coupling asymmetries (e.g., from spin), low-coherence regimes where the SM-CG is not valid]
context_windows:
  - module: CORE-016_the_time_first_correspondence_principle
    excerpt: |
      EM potential: A_{μ} := ∂_{μ} arg(Ki) under Σ.
      Charge: q := orientation/asymmetry of coherence coupling in CORE-007 (crest- vs trough-leading).
      Gravitational well: gradients in Γ act as effective curvature (CORE-004/008).
      Spin-½: double-cover holonomy of the Ki motif (CORE-009).
      This explains recovery of SM/QFT predictions without making spacetime fundamental.
poetic_connections:
  motifs: [handedness, orientation, asymmetry, crest/trough, phase, leading/lagging]
  evocative_lines:
    - "the Σ-shadow of a time-first substrate"
    - "crest- vs trough-leading"
  association_matrix:
    - [ "COHERENCE_COUPLING", 0.9 ]
    - [ "EM_POTENTIAL", 0.7 ]
    - [ "SPIN", 0.5 ]
formal_mappings:
  candidates:
    - target: Electric Charge `q`
      domain: SM
      mapping_kind: operational
      equation_hint: |
        F_em = q(E + v x B)
      justification: |
        The Pirouette definition of charge as coupling orientation is designed to reproduce the phenomenology of electric charge under the SM-CG correspondence. The binary nature (crest/trough-leading) maps directly to the sign (+/-) of electric charge, and its magnitude is normalized to reproduce the strength of the electromagnetic interaction via the fine-structure constant α.
      references:
        - title: An Introduction to Quantum Field Theory
          where: "Part II: Quantum Electrodynamics"
          date: 1995-10-11
      confidence: 0.95
  adopted:
    - target: Electric Charge `q_e` from Standard Model U(1) gauge theory
      rationale: "This mapping is adopted by axiom CORE-016 §2 (SM-CG) to ensure that the Pirouette Framework recovers all successful predictions of Standard Model electromagnetism in the appropriate limit. It is a foundational bridge, not a derived result."
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "The property 'charge' is fundamentally binary (+/- or crest/trough-leading) and there are no other 'colors' of electromagnetic charge."
      domain: theory
      falsifier: "The discovery of a third, distinct type of electromagnetic interaction not reducible to the +/- binary, or a fractional charge that cannot be explained by combinations of motifs with fundamental charge orientation."
      status: supported
      links: [CORE-007, CORE-016]
    - statement: "Charge conservation is a direct consequence of the persistence of coupling orientation through interactions."
      domain: theory
      falsifier: "An observation of non-local charge non-conservation that cannot be explained by particle-antiparticle pair production, implying that coupling orientation can spontaneously flip without a corresponding anti-flip."
      status: proposed
      links: [DYNA-004]
naming_notes:
  collisions: [The symbol `q` is widely used for momentum transfer or generalized coordinates in other contexts. In Pirouette, `q` is reserved for charge; momentum transfer uses `Δp`.]
  disambiguation: |
    Distinguish Pirouette Charge (a property of coupling orientation) from the colloquial 'charge' of other forces (e.g., 'color charge' in QCD). This entry refers exclusively to the property that maps to electromagnetic charge.
crosslinks:
  near_synonyms: []
  antonyms: [CHARGE_NEUTRALITY]
  prerequisites: [COHERENCE_COUPLING, TIME_FIRST_SUBSTRATE]
  downstream_effects: [EM_POTENTIAL, LORENTZ_FORCE]
license: CC-BY-SA-4.0
---

# Charge

## Canonical (Pirouette)
In the time-first model, Charge (`q`) is the discrete, signed orientation of a coherence coupling (defined in CORE-007). It represents the intrinsic asymmetry in how two coherent motifs interact, specifically whether the interaction is 'crest-leading' or 'trough-leading'. This binary choice determines the sign of the effective electromagnetic force under the SM-CG correspondence gauge.

## EFT-First Summary
Under the Time-First Correspondence Principle (CORE-016), Pirouette's definition of Charge is constructed to map directly onto the electric charge of the Standard Model's U(1) gauge theory. It is the conserved, quantized property that sources the electromagnetic field and determines the strength and sign of the electromagnetic force. This mapping is definitional, ensuring that Pirouette recovers the successful predictions of quantum electrodynamics in high-coherence, high-density limits.

## Glossary Links
- See also: [COHERENCE_COUPLING](), [EM_POTENTIAL]()