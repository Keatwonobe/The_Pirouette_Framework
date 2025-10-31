---
term: "Temporal Phase"
canonical_id: "TEMPORAL_PHASE"
symbol: "φ"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-158"]
---

---
term: Temporal Phase
canonical_id: TEMPORAL_PHASE
symbol: φ
aliases: [Phase Angle, Rhythmic Timing]
parents: [DOMA-158]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-158
      snippet: |
        *   **Temporal Phase (φ):** This remains a critical variable, describing the *timing* of a node's rhythm relative to a shared clock or its neighbors.
            *   **Inference:** Look for cyclical behavior. In a social network, this is the peak time of a user's posting cycle. In an economy, it is the phase of a business cycle. In a power grid, it is the literal phase angle of the AC signal.
            *   **Scaling:** Mapped to the circle `[0, 2π)`.
  editors: [system-generator]
  review_log: []
triad:
  art: |
    The silent count that turns a crowd into a chorus, or a set of gears into a grinding halt. It is the *when* that determines the *what* of any interaction. It is the beat of the system's shared pulse.
  law: |
    The difference in Temporal Phase (Δφ) between two nodes determines the resonance of their interaction, modulating Coherence Flow (J) via a factor of `cos(Δφ)`. Maximal flow requires phase alignment (Δφ ≈ 0), while anti-phase (Δφ ≈ π) creates destructive interference or flow reversal.
  philosophy: |
    Beyond static connection, phase introduces the dimension of *when*. It asserts that systemic health is not merely about who is connected, but whether they are acting in concert. It is the principle that coordinated action is the basis of all emergent coherence.
pirouette_definition: |
  The timing of a node's characteristic cyclical pattern, expressed as an angle on the unit circle `[0, 2π)`. It serves as a relational coordinate, defining a node's temporal position relative to its neighbors or a global reference clock. It is a primary determinant of constructive or destructive interference in Coherence Flow.
operational_definition:
  units: Radians, mapped to `[0, 2π)`. Dimensionless angle.
  symbol_table:
    - name: φ
      meaning: Temporal phase of a single node's oscillation.
      dimensions: dimensionless
      default_range: "[0, 2π)"
    - name: Δφ
      meaning: Phase difference between two nodes, `φ_i - φ_j`.
      dimensions: dimensionless
      default_range: "[-π, π]"
  measurement:
    procedures:
      - name: Phase Extraction via Spectral Analysis
        outline: |
          1. Acquire a time-series of a node's primary activity metric.
          2. Apply a Fast Fourier Transform (FFT) or Wavelet Transform to the time-series to obtain a frequency spectrum.
          3. Identify the dominant, characteristic frequency (ω) of the node's rhythm.
          4. Extract the phase angle of the complex value of the FFT at frequency ω. This is the node's Temporal Phase (φ) relative to the start of the time-series.
        expected_signals: [Time-series data with a discernible periodic component.]
        pitfalls: [Aperiodic signals (low Node Coherence, Kτ), signals with multiple strong frequency components requiring mode decomposition, insufficient time-series length to resolve the dominant frequency.]
context_windows:
  - module: DOMA-158
    excerpt: |
      **Temporal Phase (φ):** This remains a critical variable, describing the *timing* of a node's rhythm relative to a shared clock or its neighbors.
      *   **Inference:** Look for cyclical behavior. In a social network, this is the peak time of a user's posting cycle. In an economy, it is the phase of a business cycle. In a power grid, it is the literal phase angle of the AC signal.
  - module: DOMA-158
    excerpt: |
      The flow from node `i` to node `j` is given by: `J_ij = Kτ_i * cos(φ_i - φ_j) * (1 - Γ_ij)`. This formula elegantly captures the core dynamics: ... **Resonance Factor (`cos(φ_i - φ_j)`):** This is the term for temporal synchrony (`Δφ`). When nodes are in phase (`Δφ ≈ 0`), their interaction is constructive (`cos ≈ 1`) and flow is maximized. When they are out of phase (`Δφ ≈ π`), their interaction is destructive (`cos ≈ -1`) and flow reverses or ceases.
poetic_connections:
  motifs: [rhythm, synchrony, resonance, timing, cycle, concert, harmony, pulse, beat]
  evocative_lines:
    - "The low notes sing of its unity. The high, sharp notes cry out from its points of pain."
    - "To bring a dissonant chord back into harmony."
    - "To hear its song in its entirety."
  association_matrix:
    - [ "COHERENCE_FLOW", 0.9 ]
    - [ "NODE_COHERENCE", 0.7 ]
    - [ "RESONANCE", 0.9 ]
    - [ "TURBULENCE", 0.6 ]
formal_mappings:
  candidates:
    - target: Phase of a quantum wavefunction, ψ = |ψ|e^(iφ)
      domain: AMO
      mapping_kind: mathematical
      equation_hint: |
        Interference term ∝ |ψ₁ + ψ₂|² = ... + 2|ψ₁||ψ₂|cos(φ₁ - φ₂)
      justification: |
        The Coherence Flow equation's `cos(φ_i - φ_j)` term is a direct analogue to the interference term between two wavefunctions. This maps constructive/destructive interference in quantum systems to the enhancement/suppression of flow between coherent nodes in a network.
      references:
        - title: Quantum Mechanics
          where: Introductory texts on interference and the path integral formulation.
          date: 1965-01-01
      confidence: 0.8
    - target: Phase of a simple harmonic oscillator, x(t) = A cos(ωt + φ)
      domain: CM
      mapping_kind: conceptual
      justification: |
        This provides the most direct classical analogy. Each node is treated as an oscillator with a characteristic rhythm, and φ represents its timing offset. The interaction between two oscillators (e.g., driving forces, coupling) is critically dependent on their relative phase.
      references: []
      confidence: 0.7
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "A network's total Coherence Flow is maximized only when the phase differences (Δφ) across its high-conductance channels approach zero."
      domain: phenomenology
      falsifier: "Demonstrating a stable, high-efficiency network where maximal throughput is empirically achieved with significant, non-zero phase lags (e.g., Δφ ≈ π/2) across its primary channels, implying a different interaction kernel than `cos(Δφ)`, such as a sine or complex exponential dependence."
      status: supported
      links: [DOMA-158]
naming_notes:
  collisions: [φ is commonly used for the golden ratio, a scalar field in QFT, or electric potential in electromagnetism.]
  disambiguation: |
    Within the Pirouette Framework, φ *always* refers to a temporal phase angle within the `[0, 2π)` interval, related to the rhythm of a system component. It should not be confused with a spatial angle, a scalar field potential, or a mathematical constant. Its role is always relational and dynamic, defining "when" an entity acts relative to others.
crosslinks:
  near_synonyms: []
  antonyms: [PHASE_NOISE, ASYNCHRONY]
  prerequisites: [NODE_COHERENCE]
  downstream_effects: [COHERENCE_FLOW, TURBULENCE, RESONANCE]
license: CC-BY-SA-4.0