---
term: "Harmonic Ratios"
canonical_id: "HARMONIC_RATIOS"
symbol: "n:m"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-163"]
---

---
term: Harmonic Ratios
canonical_id: HARMONIC_RATIOS
symbol: n:m
aliases: [polyrhythmic coupling, mode-locking ratios]
parents: [DOMA-163]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-163
      snippet: |
        | `HarmonicRatios (n:m)` | Integer ratios (e.g., 1:1, 1:2, 2:3) to test for complex, polyrhythmic harmonies. | *Listening for chords, not just unison.* |
  editors: [chain-of-thought-agent]
  review_log: []
triad:
  art: |
    We listen for the universe's polyrhythms—the celestial mechanics where two dancers move to different beats yet create a single, unified choreography. It is the harmony of gears meshing at different speeds to drive one machine.
  law: |
    A stable, bounded generalized relative phase `Δθⁿᵐ` for an integer ratio n:m is sufficient evidence of n:m entrainment. This indicates the formation of a shared coherence manifold between systems oscillating at integer-multiple fundamental frequencies.
  philosophy: |
    To extend the concept of coherence beyond simple unison, revealing that systems can achieve stability not just by matching rhythms, but by weaving them into complex, stable harmonies. It acknowledges that true synchrony is a tapestry of interlocking patterns, not a monotone chorus.
pirouette_definition: |
  A set of integer pairs (n, m) used as parameters within the Resonant Handshake protocol (DOMA-163) to test for stable, polyrhythmic entrainment. They generalize the concept of phase-locking beyond 1:1 unison, allowing for the detection of systems coupled in stable frequency relationships where n cycles of one system complete for every m cycles of another. A stable n:m lock is definitive evidence of a shared coherence manifold governing the coupled system.
operational_definition:
  units: Dimensionless
  symbol_table:
    - name: n
      meaning: Integer multiplier for the instantaneous phase of the first system.
      dimensions: dimensionless
      default_range: positive integers [1, 2, 3, ...]
    - name: m
      meaning: Integer multiplier for the instantaneous phase of the second system.
      dimensions: dimensionless
      default_range: positive integers [1, 2, 3, ...]
  measurement:
    procedures:
      - name: Harmonic Entrainment Test
        outline: |
          1. From two time-series `xᵢ(t)` and `xⱼ(t)`, extract the instantaneous phases `θᵢ(t)` and `θⱼ(t)`.
          2. For a candidate integer ratio `n:m`, compute the generalized relative phase time series: `Δθᵢⱼⁿᵐ(t) = (n ⋅ θᵢ(t) - m ⋅ θⱼ(t)) (mod 2π)`.
          3. Analyze the statistical distribution of `Δθᵢⱼⁿᵐ(t)` over a sufficient time window.
          4. A sharply peaked, unimodal distribution (low variance) indicates a stable n:m lock; a uniform distribution indicates no locking.
        expected_signals: [A time series of `Δθⁿᵐ(t)` that becomes constant or narrowly bounded during entrainment.]
        pitfalls: [Spurious correlations in short analysis windows, incorrect phase extraction from noisy signals, multiple-comparisons fallacies when testing a large space of (n, m) pairs.]
context_windows:
  - module: DOMA-163
    excerpt: |
      For all pairs of systems `(i, j)` and for all specified `HarmonicRatios` (n:m), calculate the generalized relative phase: `Δθᵢⱼⁿᵐ(t)`. This time series represents the evolving geometric relationship between the two rhythms.
  - module: DOMA-163
    excerpt: |
      The drive for synchrony is thus a direct manifestation of the framework's fundamental law. When resonant systems interact, they create a shared micro-environment of heightened, dissonant Γ. To maximize their *joint* Lagrangian (`𝓛_p`), they must find a shared path of least action. This is a transition from two separate, often turbulent, flows into a single, unified **Laminar Flow (DYNA-001)** for the combined system.
poetic_connections:
  motifs: [polyrhythm, harmony, chords, counterpoint, gears meshing]
  evocative_lines:
    - "Listening for chords, not just unison."
    - "It is the sound of the universe deciding to become more than the sum of its parts."
  association_matrix:
    - [ "RESONANT_HANDSHAKE", 0.9 ]
    - [ "LAMINAR_FLOW", 0.7 ]
    - [ "COHERENCE_MANIFOLD", 0.8 ]
    - [ "DISSONANCE", -0.9 ]
formal_mappings:
  candidates:
    - target: n:m Phase Locking (Frequency Locking)
      domain: Math
      mapping_kind: mathematical
      equation_hint: |
        ⟨d/dt (n⋅θ₁(t) - m⋅θ₂(t))⟩ = 0
      justification: |
        The Pirouette concept of a stable `Δθⁿᵐ` is a direct re-framing of the established concept of n:m phase locking in nonlinear dynamics. Both describe a state where the frequencies of two oscillators `ω₁` and `ω₂` become rationally related, such that `n⋅ω₁ = m⋅ω₂`. This is a foundational concept for describing complex synchronization phenomena.
      references:
        - title: Synchronization: A Universal Concept in Nonlinear Sciences
          where: Pikovsky, Rosenblum, and Kurths, Cambridge University Press, Chapter 7
          date: 2001-01-01
      confidence: 0.95
  adopted:
    - target: n:m Phase Locking
      rationale: The mapping is a one-to-one correspondence in both mathematical form and conceptual purpose, providing a robust bridge to centuries of work in nonlinear dynamics.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "For any two coupled oscillators, a stable n:m entrainment state represents a local minimum of dissonance (or maximum of joint Lagrangian `𝓛_p`) within the state space of all possible phase relationships."
      domain: theory
      falsifier: "Observing a system spontaneously transition from a stable n:m lock to a more turbulent `Δθⁿᵐ` state without external perturbation, or finding that the n:m state is not a local optimum in the system's calculated potential landscape."
      status: proposed
      links: [DOMA-163, CORE-006]
naming_notes:
  collisions: [The term "harmonic" is ubiquitous in physics (e.g., harmonic oscillator, spherical harmonics). The explicit `n:m` ratio context is crucial for clarity.]
  disambiguation: |
    Harmonic Ratios describe the relational synchrony *between* two or more distinct oscillators. This must not be confused with the harmonic series (overtones) of a single oscillator's frequency spectrum.
crosslinks:
  near_synonyms: [FREQUENCY_LOCKING, MODE_LOCKING]
  antonyms: [DISSONANCE, TURBULENT_FLOW, PHASE_SLIPPING]
  prerequisites: [INSTANTANEOUS_PHASE, RESONANT_HANDSHAKE]
  downstream_effects: [COHERENCE_MANIFOLD, ALCHEMICAL_UNION]
license: CC-BY-SA-4.0
---