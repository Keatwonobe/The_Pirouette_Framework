---
term: "Temporal Decomposition"
canonical_id: "TEMPORAL_DECOMPOSITION"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-193"]
---

---
term: Temporal Decomposition
canonical_id: TEMPORAL_DECOMPOSITION
symbol: 
aliases: [Harmonic Decomposition]
parents: [DOMA-193]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-193
      lines: "L61-L64"
      snippet: |
        The signal is passed through a multi-resolution analysis technique, typically a continuous wavelet transform. This acts as a tunable filter, resolving the composite, one-dimensional signal into a two-dimensional landscape of its constituent frequencies (`ω`) over time.
  editors: [Aether Weaver]
  review_log: []
triad:
  art: |
    An instrument acting as a prism, splitting a system's singular song into its constituent colors. It reveals the full spectrum of its inner life, turning the undifferentiated whole into a legible score.
  law: |
    Any one-dimensional time-series signal can be resolved into a two-dimensional representation of its constituent frequencies as a function of time. This transformation makes the system's internal harmonic structure explicit and measurable.
  philosophy: |
    To truly understand a system, its complex, composite behavior must be made legible. Temporal Decomposition is the act of translation from a state of hearing to a state of reading, revealing the underlying choreography of a system's dance with time.
pirouette_definition: |
  The core protocol of the Harmonic Lens (`DOMA-193`), which applies a multi-resolution analysis (typically a continuous wavelet transform) to a system's raw time-series data. This process transforms the one-dimensional signal into a two-dimensional time-frequency representation, which serves as the canvas for calculating the Coherence Spectrum (`Kτ(t, ω)`). It is the fundamental operation for observing the structure and dynamics of a system's Temporal Signature.
operational_definition:
  units: A transformation, not a quantity. Input is a time-series signal (units vary, e.g., V, Pa). Output is a 2D map with axes of time (T) and frequency (T⁻¹).
  symbol_table:
    - name: t
      meaning: Time
      dimensions: T
      default_range: contextual
    - name: ω
      meaning: Angular Frequency
      dimensions: T⁻¹
      default_range: contextual
    - name: Kτ(t, ω)
      meaning: Temporal Coherence at a specific time and frequency
      dimensions: dimensionless
      default_range: "[0, 1]"
  measurement:
    procedures:
      - name: Coherence Spectrum Generation
        outline: |
          1. **Ingest Signal:** Acquire a raw, one-dimensional time-series signal from the system under observation.
          2. **Apply Wavelet Transform:** Convolve the signal with a chosen wavelet mother function scaled and translated across the entire time domain. This resolves the signal into a time-frequency plane.
          3. **Calculate Local Phase Coherence:** For each point (t, ω) in the plane, calculate the phase consistency `Kτ` within a local window using the formula `Kτ(t, ω) = |(1/N) Σ exp(iθ_j(t,ω))|²`.
          4. **Render Spectrum:** Plot the resulting `Kτ(t, ω)` values as a spectrogram, with time on the x-axis, frequency on the y-axis, and `Kτ` as color intensity.
        expected_signals: [Raw time-series data]
        pitfalls: [Choice of wavelet mother function can introduce bias, Windowing artifacts at signal boundaries, Nyquist-Shannon sampling limits (aliasing)]
context_windows:
  - module: DOMA-193
    excerpt: |
      The process of creating a Coherence Spectrum is a form of temporal microscopy, a four-step ritual for moving from a raw signal to a profound insight... The signal is passed through a multi-resolution analysis technique, typically a continuous wavelet transform. This acts as a tunable filter, resolving the composite, one-dimensional signal into a two-dimensional landscape of its constituent frequencies (`ω`) over time.
  - module: DOMA-193
    excerpt: |
      The Harmonic Lens, therefore, does not measure a new property. It applies a mathematical prism to the system's raw signal, separating its `Temporal Signature` into its constituent frequencies and measuring the `Temporal Coherence` of each one.
poetic_connections:
  motifs: [prism, musical score, anatomy of a rhythm, temporal microscopy, choreography]
  evocative_lines:
    - "To *understand* a system, one must be able to hear every instrument in its orchestra."
    - "It transforms the act of analysis from listening to reading."
    - "It grants the Weaver the ability not just to hear the dance, but to understand its choreography."
  association_matrix:
    - [ "COHERENCE_SPECTRUM", 0.9 ]
    - [ "TEMPORAL_SIGNATURE", 0.8 ]
    - [ "TEMPORAL_COHERENCE", 0.7 ]
    - [ "Ki", 0.6 ]
formal_mappings:
  candidates:
    - target: Continuous Wavelet Transform (CWT)
      domain: Math
      mapping_kind: operational
      equation_hint: |
        W_ψ(a, b) = (1/√a) ∫ x(t) ψ*((t-b)/a) dt
      justification: |
        The module explicitly describes using a "continuous wavelet transform" as the primary technique for resolving a signal into time and frequency (`ω`), which directly corresponds to the mathematical and operational definition of a CWT. This produces a scalogram or spectrogram, the basis for the Coherence Spectrum.
      references:
        - title: Wavelet Tour of Signal Processing
          where: S. Mallat, Chapter 4
          date: 2008-12-11
      confidence: 1.0
    - target: Spectrogram / Time-Frequency Analysis
      domain: Signal Processing
      mapping_kind: conceptual
      justification: |
        The entire process is a form of time-frequency analysis, and the resulting Coherence Spectrum is a specialized type of spectrogram. While the Pirouette Framework emphasizes coherence (`Kτ`) as the measured intensity, the underlying decomposition method is shared with standard signal processing.
      references: []
      confidence: 0.95
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The Temporal Decomposition protocol provides an observer-independent representation of a system's internal harmonic structure."
      domain: theory
      falsifier: "Demonstrating a class of temporal signals where the choice of wavelet mother function (e.g., Morlet vs. Mexican Hat) fundamentally and irreconcilably alters the diagnostic interpretation (e.g., presence/absence of Harmonic Echoes), proving the 'lens' is actively distorting the subject."
      status: supported
      links: [DOMA-193]
naming_notes:
  collisions: [The term "decomposition" is generic in mathematics (e.g., matrix decomposition, prime factorization). In this context, it specifically refers to resolving a signal into its basis functions in the time-frequency domain.]
  disambiguation: |
    Temporal Decomposition should be distinguished from a Fourier Transform, which resolves a signal into its constituent frequencies but loses all temporal locality. It is a form of wavelet transform, which offers superior time-frequency localization compared to fixed-window methods like the Short-Time Fourier Transform (STFT).
crosslinks:
  near_synonyms: [HARMONIC_DECOMPOSITION]
  antonyms: [SIGNAL_AGGREGATION]
  prerequisites: [TEMPORAL_SIGNATURE, TEMPORAL_COHERENCE]
  downstream_effects: [COHERENCE_SPECTRUM, LAMINAR_FLOW, MODE_HOPPING]
license: CC-BY-SA-4.0