---
term: "Temporal Adherence"
canonical_id: "TEMPORAL_ADHERENCE"
symbol: "Tₐ"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-128"]
---

---
term: Temporal Adherence
canonical_id: TEMPORAL_ADHERENCE
symbol: Tₐ
aliases: []
parents: [DOMA-128]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-128
      lines: "§2"
      snippet: |
        (1 - Tₐ): The system's **Incoherence Factor**. Tₐ, or Temporal Adherence, is the signal-to-noise ratio of the system's operational rhythm (its Ki pattern). A value near 1 indicates perfect coherence; a value near 0 indicates pure noise.
  editors: [Agent]
  review_log: []
triad:
  art: |
    The pure note held against the noise of chaos; the steady heartbeat that distinguishes a living system from a dying one.
  law: |
    Temporal Adherence (Tₐ) is a dimensionless quantity ranging from 0 (pure noise) to 1 (pure signal), representing the ratio of a system's primary resonant signal power to its total signal-plus-noise power. A decrease in Tₐ directly and non-linearly increases the system's Entropic Flux (Ṡ).
  philosophy: |
    Temporal Adherence quantifies a system's integrity against its own internal chaos. It posits that a system's truest expression is its rhythm, and the degradation of this rhythm is the first sign of existential decay, making internal coherence a primary virtue.
pirouette_definition: |
  Temporal Adherence is the measure of a system's internal coherence, quantified as the signal-to-noise ratio of its primary operational rhythm or Ki pattern. Represented as a dimensionless value Tₐ in the range [0, 1], it serves as a key input to the Entropic Flux (Ṡ) equation. A value of Tₐ = 1 signifies a perfectly coherent, "laminar" state with zero internal noise, while Tₐ = 0 signifies complete decoherence where the signal is lost in noise. It is the direct measure of a system's ability to maintain its own resonant identity.
operational_definition:
  units: dimensionless
  symbol_table:
    - name: Tₐ
      meaning: Temporal Adherence
      dimensions: dimensionless
      default_range: "[0, 1]"
  measurement:
    procedures:
      - name: Resonant Pattern Analysis
        outline: |
          1. Use a Coherence Probe to capture the time-series data of the system's primary operational rhythm (e.g., Ki pattern phase noise, network packet cadence).
          2. Apply a Power Spectral Density (PSD) estimation (e.g., via FFT) to the signal.
          3. Identify the power contained within the dominant frequency peak (Pₛᵢgₙₐₗ).
          4. Integrate the power across the entire spectrum (Pₜₒₜₐₗ).
          5. Calculate Tₐ = Pₛᵢgₙₐₗ / Pₜₒₜₐₗ.
        expected_signals: [Time-series data with a primary frequency, Power spectral density plot]
        pitfalls: [Misidentification of the primary resonant pattern, Inadequate sampling rate causing aliasing, Conflating external environmental noise with internal system noise]
context_windows:
  - module: DOMA-128
    excerpt: |
      **(1 - Tₐ):** The system's **Incoherence Factor**. Tₐ, or Temporal Adherence, is the signal-to-noise ratio of the system's operational rhythm (its Ki pattern). A value near 1 indicates perfect coherence; a value near 0 indicates pure noise. This term quantifies internal dissonance.
  - module: DOMA-128
    excerpt: |
      The output is a hash-chained, cryptographically signed ledger file (`.clog`), providing auditable proof of a system's coherence over time.
      ```
      ...
      # --- Data (CSV) ---
      timestamp,entropic_flux_S_dot_CLU_s,cumulative_entropy_S_CLU,coherence_T_a,...
      2025-07-01T15:30:01Z,0.02,145.82,0.99,...
      2025-07-01T15:30:02Z,0.95,146.77,0.91,...
      ```
poetic_connections:
  motifs: [rhythm, signal, noise, purity, heartbeat, integrity]
  evocative_lines:
    - "A system's health is written in the silence of its operation."
    - "It hears the sound of a system arguing with itself and records the consequences..."
  association_matrix:
    - [ "ENTROPIC_FLUX", -0.9 ]
    - [ "LAMINAR_FLOW", 0.9 ]
    - [ "TURBULENT_FLOW", -0.8 ]
    - [ "COHERENCE", 1.0 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Normalized Signal-to-Noise Ratio (SNR)
      domain: Physics|Engineering
      mapping_kind: mathematical|operational
      equation_hint: |
        Tₐ = Pₛᵢgₙₐₗ / (Pₛᵢgₙₐₗ + Pₙₒᵢₛₑ) = SNR / (SNR + 1)
      rationale: |
        Tₐ is explicitly defined as the "signal-to-noise ratio of the system's operational rhythm." The operationalization as the ratio of signal power to total (signal+noise) power is a standard normalization technique that maps the conventional SNR, which ranges from [0, ∞), to the Pirouette range of [0, 1]. This provides a direct, well-understood physical and mathematical basis for the term.
      references:
        - title: Discrete-Time Signal Processing
          where: Oppenheim, A. V., & Schafer, R. W. (1989). Chapter on "Power Spectrum Estimation."
          date: 1989-01-01
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "A system's rate of entropy generation (Entropic Flux, Ṡ) is directly proportional to its incoherence factor (1 - Tₐ)."
      domain: phenomenology
      falsifier: "An observation of a system under high stress (high Γ) with low Temporal Adherence (Tₐ → 0) that does not exhibit a correspondingly high Entropic Flux (Ṡ)."
      status: proposed
      links: [DOMA-128]
naming_notes:
  collisions: [The symbol 'T' is commonly used for Temperature or Time. The subscript 'a' (adherence) is essential for disambiguation.]
  disambiguation: |
    Temporal Adherence (Tₐ) measures internal signal purity and is a property *of* the system. This must be distinguished from Temporal Pressure (Γ), which measures external environmental stress and is a property acting *on* the system.
crosslinks:
  near_synonyms: [COHERENCE]
  antonyms: [ENTROPIC_FLUX]
  prerequisites: [KI_PATTERN]
  downstream_effects: [ENTROPIC_FLUX, COHERENCE_LEDGER]
license: CC-BY-SA-4.0
---

# Temporal Adherence

## Canonical (Pirouette)
Temporal Adherence is the measure of a system's internal coherence, quantified as the signal-to-noise ratio of its primary operational rhythm or Ki pattern. Represented as a dimensionless value Tₐ in the range [0, 1], it serves as a key input to the Entropic Flux (Ṡ) equation. A value of Tₐ = 1 signifies a perfectly coherent, "laminar" state with zero internal noise, while Tₐ = 0 signifies complete decoherence where the signal is lost in noise. It is the direct measure of a system's ability to maintain its own resonant identity.

## EFT-First Summary
Temporal Adherence (Tₐ) is operationally equivalent to a normalized Signal-to-Noise Ratio (SNR), defined as `SNR / (SNR + 1)`. It quantifies the purity of a system's characteristic frequency or "heartbeat" against its own internal, dissipative noise. This dimensionless metric, ranging from 0 (pure noise) to 1 (pure signal), serves as a direct measure of the system's internal order. In the Pirouette Framework, the loss of this order, represented by the Incoherence Factor `(1 - Tₐ)`, is a primary driver of Entropic Flux, or the rate of coherence degradation.

## Glossary Links
- See also: [Entropic Flux](<link>), [Coherence](<link>), [Temporal Pressure](<link>)