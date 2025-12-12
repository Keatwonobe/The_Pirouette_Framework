---
term: "Phase Coherence"
canonical_id: "PHASE_COHERENCE"
symbol: "Δφ_AB"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-114"]
---

---
term: Phase Coherence
canonical_id: PHASE_COHERENCE
symbol: Δφ_AB
aliases: [Phase Difference, Temporal Synchrony]
parents: [DOMA-114]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-114
      lines: "80-82"
      snippet: |
        Phase Coherence (Δφ_AB): The primary metric. A direct measurement of the phase difference between the core rhythms of the two systems. As Δφ_AB → 0, attunement deepens.
  editors: [Agent_Cobalt]
  review_log: []
triad:
  art: |
    Two songs, once distinct, find a shared beat. The silence between notes vanishes, replaced by the effortless grace of a single, unified dance.
  law: |
    The degree of attunement between two systems (A, B) is inversely proportional to their mean Phase Coherence; as Δφ_AB approaches zero, the efficiency of information transfer and emergent coherence of the unified system (A+B) measurably increases.
  philosophy: |
    Phase Coherence provides a physical, measurable basis for empathy and union. It reframes connection not as a subjective feeling but as a state of temporal resonance, where the illusion of separation dissolves into a shared, measurable rhythm.
pirouette_definition: |
  Phase Coherence is the primary metric for attunement, quantifying the instantaneous angular difference between the Pirouette Cycles (τₚ) of two interacting systems (A, B). A value of Δφ_AB approaching zero indicates a state of phase-lock, a necessary condition for a Resonant Handshake and the formation of a unified coherence manifold. It is the formal measure of temporal synchrony.
operational_definition:
  units: radians (rad)
  symbol_table:
    - name: Δφ_AB
      meaning: Phase difference between the core Pirouette Cycles of system A and system B.
      dimensions: dimensionless (angle)
      default_range: "[0, π]"
  measurement:
    procedures:
      - name: Pirouette Cycle Fourier Analysis
        outline: |
          1. Continuously monitor the primary coherence signal (Ki-field oscillations) for both system A and system B.
          2. Apply a Fast Fourier Transform (FFT) or wavelet analysis to isolate the dominant frequency component, corresponding to the Pirouette Cycle (τₚ) for each system.
          3. Extract the phase angle (φ) of this dominant component for both signals at each time step.
          4. Calculate the difference Δφ_AB = |φ_A - φ_B|, typically mapped to the principal value in [0, π].
        expected_signals: [Low, stable values near zero during high attunement (Laminar Flow)., High, fluctuating values during dissonance or disengagement.]
        pitfalls: [Signal noise obscuring the primary cycle., Higher-order harmonics mistaken for the fundamental frequency., Systems with multiple dominant frequencies (high Dissonance Index) require more complex analysis.]
context_windows:
  - module: DOMA-114
    excerpt: |
      The internal cycles of the two systems—their Pirouette Cycles (τₚ)—must lock into a synchronized phase. This is the observable phenomenon of synchrony, where the actions and reactions of the two systems become perfectly timed. The phase difference approaches zero (Δφ_AB → 0), eliminating the lag and friction of separate processing.
  - module: DOMA-114
    excerpt: |
      Phase Coherence (Δφ_AB): The primary metric. A direct measurement of the phase difference between the core rhythms of the two systems. As Δφ_AB → 0, attunement deepens.
poetic_connections:
  motifs: [synchrony, rhythm, dance, harmony, echo, timing]
  evocative_lines:
    - "It is the means by which two distinct Pirouette Cycles discover a shared rhythm and merge into a single, more complex song."
    - "...the art of listening so intently that your own note changes..."
  association_matrix:
    - [ "ATTUNEMENT", 0.9 ]
    - [ "RESONANT_HANDSHAKE", 0.8 ]
    - [ "SYNCHRONY", 0.9 ]
    - [ "LAMINAR_FLOW", 0.7 ]
formal_mappings:
  candidates:
    - target: Phase-Locking Value (PLV)
      domain: Signal Processing|Neuroscience
      mapping_kind: operational
      equation_hint: |
        PLV = |< e^(i * Δφ(t)) >|
      justification: |
        In signal analysis and neuroscience, PLV measures the statistical interdependence of two signals based on their phase difference. A PLV of 1 indicates perfect phase-locking, analogous to a mean Δφ_AB of 0. This provides a direct, quantifiable method for measuring the 'temporal harmony' described in Pirouette.
      references:
        - title: Synchronization: A Universal Concept in Nonlinear Sciences
          where: Cambridge University Press
          date: 2001-01-01
      confidence: 0.9
  adopted:
    - target: Phase-Locking Value (PLV)
      rationale: |
        PLV offers a robust, well-established statistical method for quantifying phase synchrony between two time-series signals, matching the operational requirements for measuring Δφ_AB. It is scale-invariant and insensitive to signal amplitude, focusing purely on the temporal relationship, which aligns with Pirouette's time-first approach.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "A sustained decrease in mean Δφ_AB between two systems correlates directly with an increase in Coherence Gain (G_K > 1) and the emergence of high-bandwidth, 'lossless' information transfer between them."
      domain: phenomenology|experiment
      falsifier: "Observing two systems with consistently low Δφ_AB (near-zero phase-lock) that fail to exhibit synergistic emergent properties (i.e., G_K ≤ 1) or efficient information exchange would falsify this claim."
      status: supported
      links: [DOMA-114]
naming_notes:
  collisions: [The symbol Δφ is standard for phase difference in physics and engineering, which is an intentional alignment.]
  disambiguation: |
    Distinguish from Coherence Gain (G_K), which measures the *outcome* (emergent stability) of attunement, whereas Phase Coherence measures the *process* (temporal alignment). It is also distinct from the Dissonance Index (D_H), which quantifies harmonic obstacles to achieving low Phase Coherence.
crosslinks:
  near_synonyms: [SYNCHRONY, PHASE_LOCK]
  antonyms: [DISSONANCE]
  prerequisites: [PIROUETTE_CYCLE, ATTUNEMENT]
  downstream_effects: [LAMINAR_FLOW, COHERENCE_GAIN]
license: CC-BY-SA-4.0
---

# Phase Coherence

## Canonical (Pirouette)
Phase Coherence is the primary metric for attunement, quantifying the instantaneous angular difference between the Pirouette Cycles (τₚ) of two interacting systems (A, B). A value of Δφ_AB approaching zero indicates a state of phase-lock, a necessary condition for a Resonant Handshake and the formation of a unified coherence manifold. It is the formal measure of temporal synchrony.

## EFT-First Summary
Phase Coherence (Δφ_AB) is operationally equivalent to the Phase-Locking Value (PLV) used in signal processing and neuroscience to measure synchrony between two oscillating systems. As the mean Δφ_AB approaches zero (PLV approaches 1), two systems are considered phase-locked, a state which Pirouette identifies as the necessary condition for attunement and the emergence of a unified, synergistic entity. This provides a direct experimental observable for the otherwise abstract process of forming a unified manifold.

## Glossary Links
- See also: Attunement, Resonant Handshake, Synchrony, Pirouette Cycle