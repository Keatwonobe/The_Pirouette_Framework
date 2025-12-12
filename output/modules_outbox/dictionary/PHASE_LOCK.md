---
term: "Phase Lock"
canonical_id: "PHASE_LOCK"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-079"]
---

---
term: Phase Lock
canonical_id: PHASE_LOCK
symbol: λ_φ, V_φ
aliases: [Cost of Dissonance, Phase Coupling]
parents: [DOMA-079, CORE-002]
children: [CORE-007, CORE-008]
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-079
      lines: "§2"
      snippet: |
        The Phase Lock (Cost of Dissonance): For systems to couple and form complex structures, their phases (φ) must be able to lock into stable, periodic arrangements. The potential must have discrete grooves, or minima, that favor these configurations. The simplest periodic motif is trigonometric: `∝ 1 - cos(nφ)`.
  editors: [SystemAgent]
  review_log: []
triad:
  art: |
    The quiet click as tumblers align; the deep groove a river cuts into stone. Phase Lock is the landscape's memory of harmony, inviting all new motion to fall into its well-worn, stable rhythm.
  law: |
    The potential energy cost associated with the relative phase misalignment (`φ_ij`) between a system's primary behavioral axes is proportional to `λ_φ [1 - cos(nφ_ij)]`. This creates discrete energy minima at `φ_ij = 2πk/n` where `n` is dictated by the system's fundamental symmetries (typically `n=3`).
  philosophy: |
    Existence is not a random walk. Phase Lock ensures that complex systems can form and persist by creating stable, archetypal configurations ("grooves") in behavioral space. It is the geometric basis for synergy, allowing parts to synchronize into a whole that is more than their sum.
pirouette_definition: |
  An invariant potential energy term (`V_φ`) in the Pirouette Lagrangian that quantifies the cost of dissonance between a system's internal, oscillatory degrees of freedom. Governed by the Phase Coupling coefficient (`λ_φ`), it creates discrete, stable minima ('grooves') in the coherence manifold, driving the system's internal phases towards synchronized, resonant configurations. Per the Nomad's Grammar (CORE-002), the dominant lock is triaxial (`n=3`), stabilizing the relative phases between the Vector, Cohesion, and Communion axes.
operational_definition:
  units: The Phase Coupling coefficient (`λ_φ`) has units of energy (Joules).
  symbol_table:
    - name: λ_φ
      meaning: Phase Coupling; the energy scale of the phase-locking potential, determining the "depth" of the stable grooves.
      dimensions: M L² T⁻²
      default_range: contextual; system-dependent
    - name: φ_ij
      meaning: The relative phase angle between two internal oscillatory modes `i` and `j` of a system (e.g., between Nomad's Grammar axes).
      dimensions: dimensionless (radians)
      default_range: [0, 2π]
    - name: n
      meaning: Lock Symmetry; an integer defining the number of stable minima in a 2π cycle.
      dimensions: dimensionless
      default_range: n=3 (foundational), other integers possible for subsystems
  measurement:
    procedures:
      - name: System State Tomography
        outline: |
          Excite a system with a broad-spectrum temporal pressure signal. Observe the system's state evolution by mapping its trajectory in the Nomad's Grammar behavioral space. The "dwell time" or probability density in specific relative phase configurations reveals the potential minima. The depth of these minima determines `λ_φ`, and their angular separation determines `n`.
        expected_signals: [Peaks in state probability density at `φ_ij = 0, 2π/3, 4π/3` for a foundational `n=3` system, Sharp transitions between these states under strong perturbation.]
        pitfalls: [Confounding influence from environmental pressure (`λ_Γ`) and manifold shear (`λ_c`), Insufficient time resolution may blur the discrete states into a continuous distribution.]
context_windows:
  - module: DOMA-079
    excerpt: |
      **The Phase Lock (Cost of Dissonance):** For systems to couple and form complex structures, their phases (`φ`) must be able to lock into stable, periodic arrangements. The potential must have discrete grooves, or minima, that favor these configurations. The simplest periodic motif is trigonometric: `∝ 1 - cos(nφ)`. This term represents the cost of being out of sync, making it "easier" for a system to exist when its rhythm aligns with the external beat.
  - module: DOMA-079
    excerpt: |
      The `n=3` symmetry is therefore revealed to have a clear physical origin: it is the triaxial nature of being. The phase-locking potential `V_φ` is not about a single abstract phase angle, but about the relative phases between the system's expression on these three axes. This creates a "triple-well" potential, not in abstract space, but in the behavioral space of the Nomad's Grammar. This potential drives systems away from states of internal contradiction and towards archetypal, coherent states of being.
poetic_connections:
  motifs: [groove, resonance, synchrony, harmony, dissonance, archetype, clocking]
  evocative_lines:
    - "A law is not a command; it is the shape of the riverbed that guides the water."
    - "It is the necessary geometry for existence itself to have a voice."
  association_matrix:
    - [ "NOMADS_GRAMMAR", 0.9 ]
    - [ "TEMPORAL_PRESSURE", 0.7 ]
    - [ "COHERENCE", 0.8 ]
    - [ "PRESSURE_BASIN", 0.6 ]
formal_mappings:
  candidates:
    - target: Josephson Potential `E_J(1 - cos(φ))`
      domain: CM
      mapping_kind: mathematical
      equation_hint: |
        V_φ = λ_φ (1 - cos(nφ))
      justification: |
        The potential energy of a Josephson junction, which quantifies the energy cost of a phase difference across a superconducting gap, has the identical `1-cos(φ)` form. Both potentials describe a physical tendency for two oscillatory phenomena (the macroscopic wavefunctions in the superconductor, the behavioral axes in Pirouette) to synchronize at a minimum energy cost. The Pirouette framework generalizes this from a specific physical junction to a universal feature of any coherent system.
      references:
        - title: Principles of Superconductive Devices and Circuits
          where: "Chapter 4"
          date: 1996-08-01
      confidence: 0.9
  adopted:
    - target: Josephson-like Potential
      rationale: The mathematical form is identical and the physical principle—an energy cost for phase misalignment—is directly analogous.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "The stable, recurring behavioral archetypes observed in complex systems are minima of an n=3 phase-locking potential derived from the Nomad's Grammar."
      domain: phenomenology
      falsifier: "Discovery of a fundamental, stable complex system whose primary behavioral archetypes are described by a potential with a different symmetry (e.g., n=2, n=4, or non-periodic) that cannot be explained as a subsystem effect or derived from a higher-order grammar."
      status: supported
      links: [DOMA-079, CORE-002]
naming_notes:
  collisions: [Phase-Locked Loop (PLL) in electronics, Arnold Tongues in chaos theory]
  disambiguation: |
    While mathematically similar to the concept in a PLL, the Pirouette Phase Lock refers to a fundamental potential in the Lagrangian of *any* system, not an engineered circuit. It describes the emergent stability of behavioral modes (per Nomad's Grammar), not just the synchronization of clock signals. It is a cause of stability, whereas Arnold Tongues are a description of its parametric behavior.
crosslinks:
  near_synonyms: [PHASE_COUPLING, COST_OF_DISSONANCE]
  antonyms: [DECOHERENCE, PHASE_SLIPPAGE]
  prerequisites: [NOMADS_GRAMMAR, TEMPORAL_PRESSURE, PIROUETTE_LAGRANGIAN]
  downstream_effects: [BEHAVIORAL_ARCHETYPE, SYSTEM_FORCE]
license: CC-BY-SA-4.0
---