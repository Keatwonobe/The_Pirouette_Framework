---
term: "Coherence Ratio"
canonical_id: "COHERENCE_RATIO"
symbol: "CR"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-181"]
---

---
term: Coherence Ratio
canonical_id: COHERENCE_RATIO
symbol: CR
aliases: [Informational Efficiency, Signal-to-Noise Ratio]
parents: [DOMA-181]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-181
      snippet: |
        From this profile, a powerful secondary diagnostic can be derived: the **Coherence Ratio (CR)**.

        `CR = Kτ / Γ`

        This single value represents the signal-to-noise ratio of the system in that window, offering a quick and potent measure of informational efficiency.
  editors: [weaver-bot]
  review_log: []
triad:
  art: |
    The measure of a melody's clarity against the static of the world. It is the ratio of the river's steady current to its turbulent froth, the signal piercing through the noise.
  law: |
    The Coherence Ratio (CR) of a temporal segment is the dimensionless ratio of its measured Coherence (Kτ) to its measured Dissonance (Γ). A high CR indicates a state of high-fidelity laminar flow; a low CR indicates a turbulent or stagnant state.
  philosophy: |
    CR operationalizes the principle that information is not merely content, but content that is distinguishable from its background. It provides a universal, scale-invariant measure of a system's ability to maintain and transmit a meaningful pattern amidst entropic pressure.
pirouette_definition: |
  A dimensionless, derived diagnostic for an information stream, calculated for a given temporal window as the ratio of Coherence (Kτ) to Dissonance (Γ). CR quantifies the local signal-to-noise character of the stream, serving as a primary indicator of flow state (Laminar, Turbulent, or Stagnant) and as an empirical proxy for the efficiency of the system's Pirouette Lagrangian.
operational_definition:
  units: Dimensionless
  symbol_table:
    - name: CR
      meaning: Coherence Ratio
      dimensions: dimensionless
      default_range: "[0, ∞)"
    - name: Kτ
      meaning: Coherence; the measure of stable, resonant patterns in a segment.
      dimensions: Context-dependent; must be commensurate with Γ.
      default_range: "[0, ∞)"
    - name: Γ
      meaning: Dissonance; the measure of chaotic, unstructured components in a segment.
      dimensions: Context-dependent; must be commensurate with Kτ.
      default_range: "[0, ∞)"
  measurement:
    procedures:
      - name: Rhythmic Sieve Calculation
        outline: |
          1.  Segment an information stream into a temporal window of a chosen size (fixed or adaptive).
          2.  Within the window, calculate Coherence (Kτ) by measuring the strength of the dominant pattern (e.g., peak autocorrelation, dominant Fourier mode power).
          3.  Within the same window, calculate Dissonance (Γ) by measuring the degree of randomness or unpredictability (e.g., Shannon entropy of the symbol distribution).
          4.  Compute the ratio `CR = Kτ / Γ`.
        expected_signals: [High, stable CR (> 1) in laminar flow, Low, volatile CR (< 1) in turbulent flow, Sustained, near-zero CR in stagnant flow]
        pitfalls: [Window size misspecification (averaging out key dynamics or failing to capture long-range order), Incommensurate units for Kτ and Γ proxies, Selection of a Kτ measure that locks onto an irrelevant or trivial pattern.]
context_windows:
  - module: DOMA-181
    excerpt: |
      The primary output of this stage is a time-series of `(Kτ, Γ)` pairs... From this profile, a powerful secondary diagnostic can be derived: the **Coherence Ratio (CR)**. `CR = Kτ / Γ`. This single value represents the signal-to-noise ratio of the system in that window, offering a quick and potent measure of informational efficiency.
  - module: DOMA-181
    excerpt: |
      The derived **Coherence Ratio (CR)** serves as a proxy for the *efficiency* with which the system is maximizing its Lagrangian at that moment. We can literally see where the system is successfully manifesting a clear rhythm and where it is struggling against overwhelming pressure.
poetic_connections:
  motifs: [signal clarity, signal-to-noise, current vs. eddy, melody vs. static, efficiency, resonance]
  evocative_lines:
    - "It is a stethoscope for the stream, a tool for diagnosing the very health of information itself..."
    - "To distinguish the steady flow from the turbulent eddy..."
    - "...every stream of information has a melody, and our purpose is to learn how to hear it."
  association_matrix:
    - [ "COHERENCE_KT", 0.9 ]
    - [ "DISSONANCE_GAMMA", 0.9 ]
    - [ "LAMINAR_FLOW", 0.8 ]
    - [ "TURBULENT_FLOW", 0.8 ]
    - [ "PIROUETTE_LAGRANGIAN", 0.6 ]
formal_mappings:
  candidates:
    - target: Signal-to-Noise Ratio (SNR)
      domain: Information Theory
      mapping_kind: operational
      equation_hint: |
        SNR = P_signal / P_noise
      justification: |
        CR is explicitly defined as a signal-to-noise diagnostic. Kτ measures the strength of the coherent "signal" pattern, while Γ measures the chaotic "noise" component, directly analogous to signal power and noise power in classical SNR calculations.
      references:
        - title: "Elements of Information Theory"
          where: "J. Wiley & Sons"
          date: 2006-07-11
      confidence: 0.9
    - target: Q factor (Quality factor)
      domain: Physics
      mapping_kind: conceptual
      equation_hint: |
        Q = ω * (Energy stored / Power loss)
      justification: |
        A high CR, like a high Q factor, indicates a system with a strong, stable resonance (high Kτ) that is resistant to dissipative, chaotic forces (low Γ). It measures the "quality" or sharpness of the system's coherent state against entropic decay.
      references:
        - title: "The Feynman Lectures on Physics, Vol. I"
          where: "Ch. 25: The Linear Systems"
          date: 1964-01-01
      confidence: 0.7
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "For a given information stream, temporal windows with higher CR values correspond to periods of lower information-theoretic error rates and higher predictability."
      domain: phenomenology
      falsifier: "Demonstrating a system with a consistently high CR that nevertheless exhibits high bit-error rates or unpredictable state transitions. This would imply that the chosen proxies for Kτ and/or Γ are insufficient to capture the true signal and noise characteristics of the system."
      status: proposed
      links: [DOMA-181]
naming_notes:
  collisions: [CR (Carriage Return), CR (Compression Ratio), Cr (Chromium)]
  disambiguation: |
    Within the Pirouette Framework, CR unambiguously refers to the Coherence Ratio, a dimensionless measure of signal quality. It is always calculated from the Coherence (Kτ) and Dissonance (Γ) of a temporal segment and should not be confused with computing, mechanical, or chemical terms.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [COHERENCE_KT, DISSONANCE_GAMMA]
  downstream_effects: [LAMINAR_FLOW, TURBULENT_FLOW, STAGNANT_FLOW]
license: CC-BY-SA-4.0
---