---
term: "Phase difference"
canonical_id: "PHASE_DIFFERENCE"
symbol: "Δφ"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-074"]
---

---
term: Phase difference
canonical_id: PHASE_DIFFERENCE
symbol: Δφ
aliases: [Interference phase, Action phase]
parents: [DOMA-074]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-074
      lines: "L102-L107"
      snippet: |
        The resulting phase difference, *Δφ*, is the core observable. This phase difference is directly proportional to the difference between the Lagrangian action integrals calculated along the two chiral paths: *Δφ ∝ (S<sub>p, left</sub> - S<sub>p, right</sub>)*
  editors: [AI-Drafter]
  review_log: []
triad:
  art: |
    The faint echo of a choice made in silence, carried in the interference of what is and what could have been. It is the whisper of a particle's journey through two different labyrinths, made visible.
  law: |
    The measured phase difference Δφ between two recombined quantum paths is directly proportional to the difference in the Pirouette Action integrals (S_p) calculated along those paths. A time-varying modulation of the path geometry at frequency ω_n will induce a beat frequency in Δφ.
  philosophy: |
    Phase difference transforms the abstract Principle of Maximal Coherence into a concrete, measurable number. It is the experimental bridge between the foundational Lagrangian and a laboratory observable, proving that a particle's dynamics are governed by a global optimization of its path through a structured temporal landscape.
pirouette_definition: |
  The primary experimental observable in interferometric tests of the Pirouette Framework. Phase difference is the relative shift in the quantum phase of a particle's wavefunction after its components have traversed two or more distinct coherence manifolds and been recombined. It directly quantifies the difference in the Pirouette Action integral, *S<sub>p</sub>*, accumulated along the separate paths, thereby serving as a direct measurement of the Lagrangian's influence.
operational_definition:
  units: Radians (dimensionless)
  symbol_table:
    - name: Δφ
      meaning: Phase difference
      dimensions: dimensionless
      default_range: [0, 2π]
    - name: S_p
      meaning: Pirouette Action integral
      dimensions: M L² T⁻¹
      default_range: contextual
    - name: ω_n
      meaning: Angular frequency of manifold modulation
      dimensions: T⁻¹
      default_range: 1-100 Hz
  measurement:
    procedures:
      - name: Neutron Interferometry with Chiral Manifolds
        outline: |
          A coherent cold-neutron beam is split in a Mach-Zehnder interferometer. Each path passes through a micro-fabricated helical silicon grating (a Γ-sculptor) of opposite chirality. The beams are recombined, and the interference pattern is measured by a detector. The shift in the interference fringes relative to a baseline gives Δφ.
        expected_signals: [A static phase shift, A beat frequency in the interference pattern's intensity when the gratings are rotated]
        pitfalls: [Vibrational or thermal decoherence, Imperfect grating fabrication leading to unintended coherence costs, Instability in the incident neutron beam's temporal coherence]
context_windows:
  # Short, trimmed context quotes harvested from modules (3–6 sentences each).
  - module: DOMA-074
    excerpt: |
      This experiment provides a direct, physical measurement of the Pirouette Lagrangian's action integral, *S<sub>p</sub>*. When the two paths of the neutron's wavefunction are recombined, they interfere. The resulting phase difference, *Δφ*, is the core observable. This phase difference is directly proportional to the difference between the Lagrangian action integrals calculated along the two chiral paths: *Δφ ∝ (S<sub>p, left</sub> - S<sub>p, right</sub>)*.
  - module: DOMA-074
    excerpt: |
      The helical gratings are mechanically rotated at a known frequency (ω_n). This action creates a rhythmic, oscillating pulse in the structure of the local Temporal Pressure. This dynamic re-optimization will manifest as a measurable **beat frequency** in the interference pattern at the detector. It is a direct observation of a particle's resonance being driven by a modulated temporal environment.
poetic_connections:
  # Lightweight "word-association graph" and sticky lines.
  motifs: [echo of choice, whisper, labyrinth, silent answer, dance]
  evocative_lines:
    - "A visible graph of an abstract physical law."
    - "The faint echo of its choice, carried in a subtle shift of phase."
  association_matrix:
    # symmetric or directed; weights in [0,1]
    - [ "PIRROUETTE_LAGRANGIAN", 0.9 ]
    - [ "COHERENCE_MANIFOLD", 0.8 ]
    - [ "GLADIATOR_CONFINEMENT", 0.6 ]
    - [ "TEMPORAL_COHERENCE", 0.5 ]
formal_mappings:
  # Candidate alignments to EFT/SM/CM/GR terms, each with justification and refs.
  candidates:
    - target: Aharonov-Bohm phase shift
      domain: AMO
      mapping_kind: conceptual
      equation_hint: |
        Δφ ∝ (S_left - S_right) vs. Δφ = (q/ħ) ∮ A⋅dl
      justification: |
        Both phenomena describe a quantum mechanical phase shift acquired by a particle due to the properties of the paths taken, even if no classical force is exerted on the particle along those paths. The Aharonov-Bohm phase arises from the magnetic vector potential; the Pirouette phase difference arises from the geometry of the coherence manifold. Both are manifestations of action differences in a path-integral formalism.
      references:
        - title: Quantum effects of electromagnetic potentials
          where: Phys. Rev. 115, 485
          date: 1959-08-15
      confidence: 0.8
  adopted:
    - target: Aharonov-Bohm phase shift
      rationale: Provides the strongest conceptual and operational parallel in established physics for a non-local, path-dependent phase acquisition.
      confidence: 0.8
constraints_and_falsifiers:
  claims:
    - statement: "In a DOMA-074-type experiment, the measured static phase shift Δφ is non-zero and quantitatively matches the value predicted by the difference in the Pirouette Action integrals for the two chiral manifolds."
      domain: experiment
      falsifier: "The measured phase shift is zero, or its value is inconsistent with the prediction from the Pirouette Lagrangian (CORE-006)."
      status: proposed
      links: [DOMA-074]
    - statement: "Mechanical rotation of the chiral manifolds at frequency ω_n induces a detectable beat frequency in the interference signal equal to a theoretically-derived function of ω_n."
      domain: experiment
      falsifier: "No beat frequency is detected by a lock-in amplifier, or the detected frequency is uncorrelated with ω_n."
      status: proposed
      links: [DOMA-074, CORE-008]
naming_notes:
  collisions: [The symbol φ is widely used for electric potential, angles, and scalar fields. Δφ is standard for phase difference in wave mechanics and optics.]
  disambiguation: |
    This refers to the phase of a quantum wavefunction, a complex number determining interference, not a phase of matter (e.g., solid, liquid). It is a relative phase between two paths, not an absolute phase.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [PIRROUETTE_LAGRANGIAN, COHERENCE_MANIFOLD, TEMPORAL_COHERENCE]
  downstream_effects: [GLADIATOR_CONFINEMENT]
license: CC-BY-SA-4.0
---