---
term: "Harmonic Lens"
canonical_id: "HARMONIC_LENS"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-193"]
---

---
term: Harmonic Lens
canonical_id: HARMONIC_LENS
symbol: (instrument)
aliases: [Coherence Spectrum, temporal spectrogram]
parents: [CORE-003, CORE-005, CORE-006]
children: []
status: ratified
version: 2.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-193
      lines: "L15-L21"
      snippet: |
        The Harmonic Lens is the primary instrument for analyzing the fine structure of a system's Temporal Resonance (`Ki`). It is a formal protocol that takes the singular, undifferentiated signal of a system's behavior and decomposes it into a visual score. This **Coherence Spectrum** (also called a temporal spectrogram) maps the system's health, stability, and complexity...
  editors: [weaver-scribe-alpha]
  review_log: []
triad:
  art: |
    A system's life is a single, composite song. The Harmonic Lens is a prism that splits this song into its constituent colors, revealing the full spectrum of its inner harmonies and dissonances. It transforms the act of listening into the art of reading a musical score.
  law: |
    Any one-dimensional time-series signal representing a system's behavior can be decomposed into a two-dimensional spectrum of Temporal Coherence (`Kτ`) as a function of time (`t`) and frequency (`ω`). The structure of this spectrum—its peaks, echoes, and noise floor—maps directly to the system's stability, complexity, and flow state.
  philosophy: |
    To understand a system is to understand the interplay of its many internal rhythms. The Harmonic Lens provides the necessary microscopy to move beyond a single, aggregate measure of health and instead diagnose the precise sources of coherence and decoherence, enabling targeted intervention and predicting state transitions.
pirouette_definition: |
  An instrument and formal protocol for analyzing a system's Temporal Signature. The Harmonic Lens applies a multi-resolution decomposition, typically a continuous wavelet transform, to a time-series signal. It produces a Coherence Spectrum: a two-dimensional visualization of Temporal Coherence (`Kτ`) as a function of time and frequency, revealing the system's resonant patterns (`Ki`), stability against Temporal Pressure (`Γ`), and transitions between flow states.
operational_definition:
  units: The primary output, Temporal Coherence (`Kτ`), is dimensionless, ranging from 0 (incoherent) to 1 (perfectly coherent).
  symbol_table:
    - name: Kτ(t, ω)
      meaning: Temporal Coherence at a specific time `t` and frequency `ω`.
      dimensions: dimensionless
      default_range: "[0, 1]"
  measurement:
    procedures:
      - name: Harmonic Decomposition
        outline: |
          1.  **Ingest Signal:** Acquire a time-series signal representing a system's dynamic behavior.
          2.  **Decompose:** Apply a continuous wavelet transform to resolve the signal into its constituent frequencies over time.
          3.  **Calculate Coherence:** For each time-frequency point, calculate the local phase consistency using the formula:  `Kτ(t, ω) = |(1/N) * Σ e^(iθ_j(t,ω))|^2`.
          4.  **Construct Spectrum:** Render the resulting `Kτ(t, ω)` values as a 2D plot with time on the x-axis, frequency on the y-axis, and `Kτ` as color intensity.
        expected_signals: [Stable harmonic bands (Laminar Flow), broadband noise floor (Turbulent Flow), mode hopping (Phase Transition), harmonic echoes (high stability)]
        pitfalls: [Choice of wavelet basis can affect resolution, windowing artifacts can create spurious signals, low signal-to-noise ratio can obscure coherent patterns]
context_windows:
  - module: DOMA-193
    excerpt: |
      The Harmonic Lens, therefore, does not measure a new property. It applies a mathematical prism to the system's raw signal, separating its `Temporal Signature` into its constituent frequencies and measuring the `Temporal Coherence` of each one.
  - module: DOMA-193
    excerpt: |
      The Coherence Spectrum is a rich diagnostic document that maps directly to a system's health and its flow state (`DYNA-001`). A trained Weaver can read its patterns to assess and predict a system's evolution. A sudden shift where one set of harmonic peaks fades and another emerges is the definitive sign of a phase transition.
poetic_connections:
  motifs: [prism, score, orchestra, choreography, anatomy, listening]
  evocative_lines:
    - "To know a system's health, you must listen to its song."
    - "To become its healer, you must be able to read its music."
  association_matrix:
    - [ "TEMPORAL_COHERENCE", 0.9 ]
    - [ "TEMPORAL_SIGNATURE", 0.8 ]
    - [ "RESONANCE_KI", 0.8 ]
    - [ "PHASE_TRANSITION", 0.7 ]
    - [ "TEMPORAL_PRESSURE", 0.5 ]
formal_mappings:
  candidates:
    - target: Time-Frequency Analysis via Continuous Wavelet Transform (CWT)
      domain: Math
      mapping_kind: operational
      equation_hint: |
        W_x(a, b) = (1/√a) ∫ x(t) ψ*((t-b)/a) dt
        K_τ(t, ω) = | ⟨e^(iφ(t,ω))⟩ |^2
      justification: |
        The protocol described is a direct implementation of time-frequency analysis. The decomposition step maps to a CWT (or similar method like Short-Time Fourier Transform), and the calculation of `Kτ` is a standard measure of phase coherence or phase-locking value used to quantify signal synchrony. The output is a spectrogram (or more specifically, a scalogram).
      references:
        - title: Wavelet Tour of Signal Processing, A
          where: S. Mallat, Academic Press, Chapter 4
          date: 2008-12-29
      confidence: 0.95
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The Coherence Spectrum's structure, specifically 'mode hopping' (the cessation of one set of harmonic bands and emergence of another), is a necessary and sufficient indicator of a system phase transition."
      domain: phenomenology
      falsifier: "Observation of a well-documented phase transition in a system that produces no corresponding mode hopping in its Coherence Spectrum. Alternatively, observation of mode hopping in a system confirmed to be in a stable phase."
      status: supported
      links: [DOMA-193]
naming_notes:
  collisions: []
  disambiguation: |
    The "Harmonic Lens" is the name of the instrument and the protocol. Its output is the "Coherence Spectrum" or "temporal spectrogram." It is distinct from a simple Fourier Transform, which provides frequency information but discards temporal localization. The Lens provides both.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [TEMPORAL_SIGNATURE, TEMPORAL_COHERENCE]
  downstream_effects: [PHASE_TRANSITION, RESONANT_HANDSHAKE, LAMINAR_FLOW]
license: CC-BY-SA-4.0
---

# Harmonic Lens

## Canonical (Pirouette)
An instrument and formal protocol for analyzing a system's Temporal Signature. The Harmonic Lens applies a multi-resolution decomposition, typically a continuous wavelet transform, to a time-series signal. It produces a Coherence Spectrum: a two-dimensional visualization of Temporal Coherence (`Kτ`) as a function of time and frequency, revealing the system's resonant patterns (`Ki`), stability against Temporal Pressure (`Γ`), and transitions between flow states.

## EFT-First Summary
The Harmonic Lens is an operational protocol directly analogous to time-frequency analysis in signal processing, most commonly implemented via a Continuous Wavelet Transform (CWT). It decomposes a time-series signal `x(t)` into a time-frequency representation, then calculates the local phase coherence `Kτ(t, ω)` at each point. This process generates a spectrogram that visualizes the signal's spectral power and phase stability over time, a standard technique for analyzing non-stationary signals in fields from neuroscience to astrophysics.

## Glossary Links
- See also: TEMPORAL_SIGNATURE, TEMPORAL_COHERENCE, RESONANCE_KI