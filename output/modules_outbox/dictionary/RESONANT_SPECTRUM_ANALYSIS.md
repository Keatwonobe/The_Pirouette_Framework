---
term: "Resonant Spectrum Analysis"
canonical_id: "RESONANT_SPECTRUM_ANALYSIS"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-146"]
---

---
term: Resonant Spectrum Analysis
canonical_id: RESONANT_SPECTRUM_ANALYSIS
symbol: 
aliases: [Ki-Harmonic Decomposition]
parents: [CORE-003, CORE-004, CORE-006, CORE-012]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-146
      snippet: |
        This protocol allows a Weaver to listen to this song and deconstruct it into its fundamental components. It is the art of distinguishing the clear, coherent melodies of a system's being (its Ki) from the ambient, chaotic harmony of its environment (its Γ).
  editors: [chain-of-thought-agent]
  review_log: []
triad:
  art: |
    To listen to a system's song and deconstruct it into its fundamental notes, distinguishing the clear melodies of its being from the ambient harmony of its environment.
  law: |
    A temporal signature, when subjected to time-frequency analysis, decomposes into a spectrum of constituent `Ki` geometries. These components are separable into Structural and Propagating coherences, distinct from a measurable noise floor corresponding to ambient Temporal Pressure (Γ).
  philosophy: |
    A complex system is never monolithic; its identity is an emergent composition of a nested hierarchy of simpler resonances. This analysis provides the tool to understand this compositionality directly, moving from what a system *is* to what it *does*.
pirouette_definition: |
  The protocol for transforming a system's one-dimensional temporal signature into a multi-dimensional resonant spectrum. This spectrum decomposes the system's total coherence (`K_τ`) into its constituent `Ki` geometries, classifying each as either Structural (self-maintaining) or Propagating (interactive), and quantifies the ambient Temporal Pressure (Γ) from the incoherent noise floor.
operational_definition:
  units: The spectrum's vertical axis is dimensionless amplitude or relative power; the horizontal axis is a qualitative library of geometric forms.
  symbol_table:
    - name: ω_k
      meaning: The fundamental frequency (rhythm) of a constituent resonance.
      dimensions: T⁻¹
      default_range: contextual
    - name: Δω
      meaning: The frequency bandwidth of a resonance, indicating its purity.
      dimensions: T⁻¹
      default_range: contextual
    - name: Δt
      meaning: The temporal persistence of a resonance, measuring its Time Adherence (T_a).
      dimensions: T
      default_range: contextual
  measurement:
    procedures:
      - name: Resonant Spectrum Analysis Protocol
        outline: |
          1. **Ingest:** Acquire a time-series signature from the target system.
          2. **Transform:** Apply a time-frequency analysis, such as a Continuous Wavelet Transform (CWT), using a basis library of `Ki` geometries to produce a spectrogram.
          3. **Decompose:** Identify persistent, high-energy "ridges" in the spectrogram as coherent `Ki` resonances and the low-energy, broadband "floor" as Temporal Pressure (Γ).
          4. **Classify:** Separate identified `Ki` resonances into Structural (low-frequency, narrow-band, high-persistence) and Propagating (higher-frequency, broader-band, transient) modes.
          5. **Quantify:** Measure the diagnostic metrics (ω_k, Δω, Δt) for each resonance.
        expected_signals: [Bright, persistent spectrogram ridges (Ki), Low-energy broadband noise floor (Γ)]
        pitfalls: [Misinterpreting transform artifacts (e.g., edge effects) as physical resonances, Selecting an inappropriate basis library ("mother wavelets") for the target system]
context_windows:
  - module: DOMA-146
    excerpt: |
      No complex system is monolithic. Its identity and behavior are emergent properties arising from a nested hierarchy of simpler, more fundamental resonances. The Resonant Spectrum is the primary tool for understanding this composition. It provides a method for taking the observed temporal signature of a complex system and identifying the fundamental `Ki` geometries that contribute to its overall song.
  - module: DOMA-146
    excerpt: |
      Classical signal analysis creates a spectrum of frequencies. The Resonant Spectrum creates a spectrum of *forms*. A peak in the spectrum indicates that the system's complex dance contains, as a primary component, the specific geometric motion of that fundamental `Ki`.
poetic_connections:
  motifs: [symphony, deconstruction, listening, harmony, song, voice]
  evocative_lines:
    - "To truly know a cello, you must listen."
    - "One is the sound of its being; the other is the sound of its song."
  association_matrix:
    - [ "KI", 0.9 ]
    - [ "TEMPORAL_PRESSURE", 0.8 ]
    - [ "STRUCTURAL_COHERENCE", 0.7 ]
    - [ "PROPAGATING_COHERENCE", 0.7 ]
    - [ "PIROUETTE_LAGRANGIAN", 0.6 ]
formal_mappings:
  candidates:
    - target: Wavelet Transform / Time-Frequency Analysis
      domain: Math|Signal Processing
      mapping_kind: operational
      equation_hint: |
        (W_ψf)(a,b) = ∫ f(t) * (1/√a)ψ((t-b)/a) dt
      justification: |
        The module explicitly states the protocol uses a Continuous Wavelet Transform (CWT) to process the input signal into a spectrogram. This reveals the intensity of different rhythms over time, which is a direct operational mapping to time-frequency analysis methods. The "library of forms" corresponds to the set of mother wavelets (ψ).
      references:
        - title: Wavelet Tour of Signal Processing
          where: S. Mallat
          date: 1998-01-01
      confidence: 0.95
    - target: Normal Mode Analysis
      domain: CM
      mapping_kind: conceptual
      justification: |
        The analysis identifies fundamental, independent "harmonics" (Structural/Propagating Ki) that compose the system's complex motion. This is analogous to how normal modes are the independent patterns of oscillation that constitute a coupled oscillator system's general motion. Both methods decompose complex dynamics into a basis set of simpler, fundamental behaviors.
      references:
        - title: Classical Mechanics
          where: Goldstein, Poole & Safko, Ch. 6
          date: 2002-01-01
      confidence: 0.6
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "Any complex system's temporal signature can be decomposed into a finite set of discrete, coherent `Ki` resonances and an incoherent noise floor (Γ)."
      domain: phenomenology
      falsifier: "The discovery of a system whose temporal signature is irreducibly complex, showing no separable coherent structures or a clear noise floor regardless of the basis library used. Such a signal would be 'all Γ' or 'all `Ki`' in a way that defies separation."
      status: proposed
      links: [DOMA-146]
naming_notes:
  collisions: []
  disambiguation: |
    Unlike classical Fourier Analysis, which assumes stationary signals and uses a fixed sinusoidal basis, Resonant Spectrum Analysis is designed for non-stationary, transient phenomena. Its use of a "Library of Forms" (wavelets) allows it to match the analyzing function to the specific geometric character of the signal, providing localization in both time and form, not just frequency.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [KI, TEMPORAL_PRESSURE, STRUCTURAL_COHERENCE, PROPAGATING_COHERENCE, PIROUETTE_LAGRANGIAN]
  downstream_effects: []
license: CC-BY-SA-4.0
---

# Resonant Spectrum Analysis

## Canonical (Pirouette)
The protocol for transforming a system's one-dimensional temporal signature into a multi-dimensional resonant spectrum. This spectrum decomposes the system's total coherence (`K_τ`) into its constituent `Ki` geometries, classifying each as either Structural (self-maintaining) or Propagating (interactive), and quantifies the ambient Temporal Pressure (Γ) from the incoherent noise floor.

## EFT-First Summary
Operationally, Resonant Spectrum Analysis is a specialized form of Time-Frequency Analysis, typically implemented via a Continuous Wavelet Transform (CWT). It projects a time-series signal onto a basis of archetypal resonant forms ("wavelets") to produce a spectrogram. From this time-form landscape, coherent signal components ("ridges") are separated from the incoherent noise floor, allowing for the classification and quantification of the system's underlying dynamic modes.

## Glossary Links
- See also: [Temporal Pressure](link), [Ki](link), [Structural Coherence](link), [Propagating Coherence](link)