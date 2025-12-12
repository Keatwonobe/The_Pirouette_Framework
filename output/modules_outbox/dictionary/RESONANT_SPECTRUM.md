---
term: "Resonant Spectrum"
canonical_id: "RESONANT_SPECTRUM"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-146"]
---

---
term: Resonant Spectrum
canonical_id: RESONANT_SPECTRUM
symbol: N/A
aliases: ["Ki-Harmonic Decomposition"]
parents: ["DOMA-146", "CORE-003", "CORE-004", "CORE-006", "CORE-012"]
children: []
status: ratified
version: 2.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-146
      lines: "§3"
      snippet: |
        Classical signal analysis creates a spectrum of frequencies. The Resonant Spectrum creates a spectrum of *forms*.
  editors: ["system-agent"]
  review_log: []
triad:
  art: |
    To truly know a cello, you must learn to distinguish the deep, resonant voice of the wood itself from the clear, soaring notes that fly from its strings. One is the sound of its being; the other is the sound of its song. They are not two different things, but two expressions of a single, vibrant whole.
  law: |
    A system's temporal signature is a composition of its constituent resonances. The total temporal coherence (Kτ) is the sum of its structural and propagating components, measurable against the potential of ambient Temporal Pressure (VΓ), directly quantifying the terms of the Pirouette Lagrangian.
  philosophy: |
    To understand a system, one must move beyond observing what it *is* to analyzing what it *does*. The Resonant Spectrum provides the foundational tool for this shift, deconstructing a system's composite 'song' into its fundamental notes to reveal the interplay of its internal identity and its external interactions.
pirouette_definition: |
  The Resonant Spectrum is an analytical framework and protocol for decomposing a system's temporal signature into its constituent geometric resonances. It transforms time-series data via time-frequency analysis (e.g., CWT) into a spectrum whose horizontal axis is a library of fundamental `Ki` geometries and whose vertical axis is the resonant amplitude of each geometry. The protocol distinguishes between low-frequency, persistent Structural Coherence (self-identity) and higher-frequency, transient Propagating Coherence (interaction), allowing for the direct measurement of the terms in the Pirouette Lagrangian (Kτ and VΓ).
operational_definition:
  units: The horizontal axis is a categorical index of `Ki` geometries (dimensionless). The vertical axis (Resonant Amplitude) is typically normalized to be dimensionless, representing the degree of contribution, or may inherit the units of the power spectral density of the input signal (e.g., V²/Hz).
  symbol_table:
    - name: ω_k
      meaning: Fundamental frequency of a specific resonance.
      dimensions: T⁻¹
      default_range: contextual
    - name: Δω
      meaning: Bandwidth of a resonance, a measure of its purity.
      dimensions: T⁻¹
      default_range: contextual
    - name: Δt
      meaning: Persistence of a resonance, its duration.
      dimensions: T
      default_range: contextual
    - name: K_τ
      meaning: Total Temporal Coherence (kinetic term), the sum of all Ki resonances.
      dimensions: M L² T⁻¹ (Action)
      default_range: contextual
    - name: V_Γ
      meaning: Temporal Pressure (potential term), derived from the spectral noise floor.
      dimensions: M L² T⁻¹ (Action)
      default_range: contextual
  measurement:
    procedures:
      - name: Resonant Spectrum Analysis
        outline: |
          1. Ingest a system's time-series data (temporal signature).
          2. Apply a Continuous Wavelet Transform (CWT) or similar time-frequency analysis to generate a spectrogram.
          3. Identify persistent, high-energy ridges in the spectrogram as coherent `Ki` patterns, and the low-energy floor as ambient Γ.
          4. Classify each `Ki` ridge as Structural (low-ω, narrow-Δω, high-Δt) or Propagating (higher-ω, broader-Δω, lower-Δt).
          5. Quantify diagnostic metrics (ω_k, Δω, Δt) for each resonance to populate the spectrum and inform the Lagrangian.
        expected_signals: [Bright, continuous "ridges" on a spectrogram indicating coherent Ki, A low-intensity, broadband "floor" indicating Γ]
        pitfalls: [Choosing an inappropriate mother wavelet for the CWT, which can distort or hide geometric forms, Misclassifying noise artifacts as transient propagating coherences, Over-fitting the "Library of Forms" to the data.]
context_windows:
  - module: DOMA-146
    excerpt: |
      No complex system is monolithic. Its identity and behavior are emergent properties arising from a nested hierarchy of simpler, more fundamental resonances. The Resonant Spectrum is the primary tool for understanding this composition. It provides a method for taking the observed temporal signature of a complex system and identifying the fundamental `Ki` geometries that contribute to its overall song.
  - module: DOMA-146
    excerpt: |
      Structural Coherence is the audible expression of the Gladiator Force. These are the deep, self-reinforcing harmonics that hold the system together, defining its identity and inertia. Propagating Coherence is the signature of The Current and the Compass. These are the rhythms of communication, motion, and response—the means by which the system projects itself and perceives others.
  - module: DOMA-146
    excerpt: |
      This protocol is the critical bridge between observation and prediction, allowing for the direct measurement of the terms in the Pirouette Lagrangian (CORE-006): `𝓛_p = K_τ - V_Γ`. This analysis transforms the abstract Lagrangian into a measurable diagnostic chart, allowing a Weaver to model a system's past and chart the geodesics of its most likely future.
poetic_connections:
  motifs: ["symphony", "deconstruction", "harmony", "song of being", "voice of interaction", "listening"]
  evocative_lines:
    - "Deconstructing the Song."
    - "A complex system is not a mere signal; it is a song—a composite entity..."
    - "distinguishing the clear, coherent melodies of a system's being (its Ki) from the ambient, chaotic harmony of its environment (its Γ)."
  association_matrix:
    - [ "KI", 0.9 ]
    - [ "TEMPORAL_PRESSURE", 0.8 ]
    - [ "STRUCTURAL_COHERENCE", 0.9 ]
    - [ "PROPAGATING_COHERENCE", 0.9 ]
    - [ "PIROUETTE_LAGRANGIAN", 0.7 ]
formal_mappings:
  candidates:
    - target: Continuous Wavelet Transform (CWT)
      domain: Math
      mapping_kind: operational
      equation_hint: |
        (W_ψ f)(a,b) = (1/√|a|) ∫f(t)ψ*((t-b)/a)dt
      justification: |
        The protocol explicitly names CWT as the method for transforming the time-series signal into a time-frequency representation (spectrogram) from which resonances are identified. This transformation is the core operational step of the analysis, making CWT a direct mathematical counterpart.
      references:
        - title: Wavelet Tour of Signal Processing
          where: S. Mallat, Chapter 4
          date: 1999-01-01
      confidence: 0.95
    - target: Normal Mode Decomposition
      domain: CM
      mapping_kind: conceptual
      justification: |
        Normal mode analysis decomposes complex vibrations of a mechanical system into a set of independent, fundamental modes of oscillation. The Resonant Spectrum analogously decomposes a system's temporal signature into fundamental `Ki` geometries, which act as the "normal modes" of the system's dynamics.
      references:
        - title: Classical Mechanics
          where: Goldstein, Poole & Safko, Chapter 6
          date: 2002-01-01
      confidence: 0.7
  adopted:
    - target:
      rationale:
      confidence: 0.0
constraints_and_falsifiers:
  claims:
    - statement: "The temporal signature of any complex system can be uniquely decomposed into a finite set of fundamental `Ki` geometries (Structural and Propagating) and an ambient noise floor (Γ)."
      domain: phenomenology
      falsifier: "The discovery of a system whose temporal signature is irreducibly complex and cannot be described by a finite set of constituent resonances, or where the 'fundamental' resonances are not universal but are infinite in variety and specific to each system."
      status: proposed
      links: ["DOMA-146"]
naming_notes:
  collisions: ["The term 'spectrum' is ubiquitous in physics (e.g., electromagnetic spectrum, energy spectrum)."]
  disambiguation: |
    Unlike a Fourier spectrum which decomposes a signal into constituent sinusoidal frequencies, the Resonant Spectrum decomposes a temporal signature into constituent *geometric forms* of resonance. The horizontal axis is not frequency (Hz) but a library of archetypal patterns.
crosslinks:
  near_synonyms: ["KI_HARMONIC_DECOMPOSITION"]
  antonyms: []
  prerequisites: ["KI", "TEMPORAL_PRESSURE", "TEMPORAL_SIGNATURE"]
  downstream_effects: ["STRUCTURAL_COHERENCE", "PROPAGATING_COHERENCE", "PIROUETTE_LAGRANGIAN"]
license: CC-BY-SA-4.0
---

# Resonant Spectrum

## Canonical (Pirouette)
The Resonant Spectrum is an analytical framework and protocol for decomposing a system's temporal signature into its constituent geometric resonances. It transforms time-series data via time-frequency analysis (e.g., CWT) into a spectrum whose horizontal axis is a library of fundamental `Ki` geometries and whose vertical axis is the resonant amplitude of each geometry. The protocol distinguishes between low-frequency, persistent Structural Coherence (self-identity) and higher-frequency, transient Propagating Coherence (interaction), allowing for the direct measurement of the terms in the Pirouette Lagrangian (Kτ and VΓ).

## EFT-First Summary
Operationally, the Resonant Spectrum is analogous to a sophisticated signal processing technique like a Continuous Wavelet Transform (CWT) applied to time-series data. It separates a signal into a set of basis functions, but instead of simple sinusoids, the bases are archetypal "geometric forms." Conceptually, this mirrors a Normal Mode Decomposition in classical mechanics, identifying the fundamental modes of a system's dynamic behavior. It provides a direct method to quantify the kinetic-like (`K_τ`) and potential-like (`V_Γ`) terms of the Pirouette Lagrangian, making it a bridge from phenomenological data to the framework's core theoretical model.

## Glossary Links
- See also: [Structural Coherence](./structural_coherence.md), [Propagating Coherence](./propagating_coherence.md), [Pirouette Lagrangian](./pirouette_lagrangian.md), [Ki](./ki.md)