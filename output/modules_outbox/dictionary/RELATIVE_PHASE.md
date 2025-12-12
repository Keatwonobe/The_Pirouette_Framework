---
term: "Relative Phase"
canonical_id: "RELATIVE_PHASE"
symbol: "Δθ"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-163"]
---

---
term: Relative Phase
canonical_id: RELATIVE_PHASE
symbol: Δθ
aliases: []
parents: [DOMA-163, CORE-006, DYNA-001, CORE-012]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-163
      snippet: |
        **Relative Phase (Δθ):** This is no longer just a timing difference. It is the fundamental *geometric coordinate* describing the shape of the new, unified coherence manifold. A constant Δθ indicates a stable, low-energy configuration—a healthy, coherent union.
  editors: [autonom-pl-a7, system-dict-gen]
  review_log: []
triad:
  art: |
    The geometric angle of a shared dance. It is the shape of the silence between two notes that makes them a chord, the shape of the space between two dancers that makes them a pair.
  law: |
    A time-invariant relative phase (d(Δθ)/dt ≈ 0) between two or more coupled oscillators is the necessary and sufficient condition for a stable, coherent Resonant Handshake, representing a state of maximal joint Lagrangian.
  philosophy: |
    Relative Phase refutes the illusion of separation. It is the primary observable that proves two systems have dissolved their boundaries to form a single, higher-order entity. Its stability is the measure of their success in finding a shared path of least action.
pirouette_definition: |
  The fundamental geometric coordinate describing the shape and stability of the unified coherence manifold formed when two or more oscillating systems achieve entrainment. As a generalization of classical phase difference, it accounts for n:m harmonic locking and serves as the primary diagnostic for the flow state (laminar, turbulent, or stagnant) of the coupled system. Its value represents the specific, stable configuration that maximizes the joint Lagrangian of the system in accordance with the Principle of Maximal Coherence.
operational_definition:
  units: radians (rad), or dimensionless
  symbol_table:
    - name: Δθᵢⱼⁿᵐ
      meaning: Generalized relative phase between system `i` and `j` at harmonic ratio `n:m`.
      dimensions: dimensionless (angle)
      default_range: "[0, 2π)"
    - name: θᵢ(t)
      meaning: Instantaneous phase of system `i` at time `t`.
      dimensions: dimensionless (angle)
      default_range: "[0, 2π)"
    - name: n, m
      meaning: Harmonic ratio integers for polyrhythmic coupling.
      dimensions: dimensionless (count)
      default_range: "Positive integers (e.g., 1, 2, 3...)"
  measurement:
    procedures:
      - name: Generalized Relative Phase Estimation
        outline: |
          1. From two or more simultaneous time-series `xᵢ(t)`, extract the instantaneous phase `θᵢ(t)` for each signal using an appropriate method (e.g., Hilbert transform for analytic signal, or wavelet transform).
          2. For a specified harmonic ratio `n:m`, compute the time-series of the generalized relative phase: `Δθᵢⱼⁿᵐ(t) = (n ⋅ θᵢ(t) - m ⋅ θⱼ(t)) mod 2π`.
          3. Analyze the stability of the resulting `Δθ(t)` time-series within a sliding analysis window. A low variance indicates a stable, laminar (entrained) state.
        expected_signals: ["Laminar (stable Δθ)", "Turbulent (chaotic Δθ)", "Stagnant (drifting Δθ)"]
        pitfalls: ["Poor signal-to-noise ratio in source data.", "Inappropriate phase extraction method for the signal type.", "Analysis window is too short to capture the dynamics or too long to detect transient changes."]
context_windows:
  - module: DOMA-163
    excerpt: |
      **Relative Phase (Δθ):** This is no longer just a timing difference. It is the fundamental *geometric coordinate* describing the shape of the new, unified coherence manifold. A constant Δθ indicates a stable, low-energy configuration—a healthy, coherent union.
  - module: DOMA-163
    excerpt: |
      Diagnose the Flow State: Within each `AnalysisWindow`, analyze the stability of `Δθᵢⱼⁿᵐ(t)`. The character of this time series is a direct diagnosis of the health of the connection: Laminar (Entrained), Turbulent (Dissonant), or Stagnant (Drifting).
poetic_connections:
  motifs: [geometry of union, handshake, shared rhythm, harmony, dance]
  evocative_lines:
    - "It is the dissolution of 'between' itself."
    - "...the instant of connection, where two rhythms agree to dance together."
  association_matrix:
    - [ "RESONANT_HANDSHAKE", 0.9 ]
    - [ "LAMINAR_FLOW", 0.8 ]
    - [ "PRINCIPLE_OF_MAXIMAL_COHERENCE", 0.7 ]
    - [ "ENSEMBLE_COHERENCE", 0.6 ]
formal_mappings:
  candidates:
    - target: Phase difference (θ₁ - θ₂)
      domain: CM|Math
      mapping_kind: mathematical|operational
      equation_hint: |
        Δθᵢⱼⁿᵐ(t) = (n⋅θᵢ(t) - m⋅θⱼ(t)) mod 2π
      justification: |
        Mathematically, this is a generalization of the standard phase difference used to quantify synchronization (phase-locking) in coupled oscillator models like the Kuramoto model. The Pirouette framework extends this to include n:m harmonic relationships and, most importantly, re-interprets its physical meaning from a signal property to a geometric coordinate of a unified system.
      references:
        - title: "Sync: The Emerging Science of Spontaneous Order"
          where: "Steven Strogatz, 2003"
          date: 2003-01-01
        - title: "Synchronization: A Universal Concept in Nonlinear Sciences"
          where: "Pikovsky, Rosenblum, Kurths, 2001"
          date: 2001-01-01
      confidence: 0.95
  adopted:
    - target: Phase difference (in coupled oscillator theory)
      rationale: The mathematical form and operational measurement are identical to established concepts, providing a robust bridge to existing science in physics, engineering, and neuroscience. Pirouette's primary contribution is the re-interpretation of its significance under the Principle of Maximal Coherence.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "For any interacting resonant systems, the configuration that maximizes stability and minimizes energy dissipation corresponds to a state where their generalized relative phase is constant in time (d(Δθ)/dt ≈ 0)."
      domain: phenomenology
      falsifier: "Demonstration of a stable, maximally coherent, low-energy coupled system where the relative phase continuously and systematically drifts or remains chaotic, and this is not a transient state."
      status: supported
      links: [DOMA-163, CORE-006]
naming_notes:
  collisions: [The symbol Δθ is standard for phase difference in classical physics. This is an intentional alignment.]
  disambiguation: |
    Do not confuse Relative Phase with a simple timing delay or a property *between* two separate systems. In Pirouette, it is the primary coordinate describing the internal geometric shape *of* the single, unified manifold that the two systems have become. It describes the form of the union, not the distance separating its former components.
crosslinks:
  near_synonyms: []
  antonyms: [DISSONANCE, PHASE_DIVERGENCE]
  prerequisites: [INSTANTANEOUS_PHASE, TEMPORAL_PRESSURE]
  downstream_effects: [RESONANT_HANDSHAKE, ENSEMBLE_COHERENCE, LAMINAR_FLOW, ALCHEMICAL_UNION]
license: CC-BY-SA-4.0
---

# Relative Phase

## Canonical (Pirouette)
The fundamental geometric coordinate describing the shape and stability of the unified coherence manifold formed when two or more oscillating systems achieve entrainment. As a generalization of classical phase difference, it accounts for n:m harmonic locking and serves as the primary diagnostic for the flow state (laminar, turbulent, or stagnant) of the coupled system. Its value represents the specific, stable configuration that maximizes the joint Lagrangian of the system in accordance with the Principle of Maximal Coherence.

## EFT-First Summary
Relative Phase (Δθ) is operationally and mathematically equivalent to the generalized phase difference between coupled oscillators, a core concept in the study of synchronization across physics and engineering. It is the observable order parameter for phase-locking phenomena. The Pirouette Framework re-contextualizes it not as a simple signal property, but as the geometric coordinate describing the stable, low-energy configuration of the unified manifold that emerges when systems couple to maximize their joint coherence.

## Glossary Links
- See also: [Resonant Handshake](...), [Laminar Flow](...), [Ensemble Coherence](...)