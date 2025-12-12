---
term: "Coherence-Pressure Balance"
canonical_id: "COHERENCE_PRESSURE_BALANCE"
symbol: "CPB"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-195"]
---

---
term: Coherence-Pressure Balance
canonical_id: COHERENCE_PRESSURE_BALANCE
symbol: CPB
aliases: []
parents: [DOMA-195]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-195
      snippet: |
        For diagnostic clarity, the Sieve translates this into a dimensionless ratio: the Coherence-Pressure Balance (CPB).

        Coherence-Pressure Balance (CPB):
        `CPB = Kτ / V_Γ`

        The CPB is the single most important diagnostic metric in the framework.
  editors: [System]
  review_log: []
triad:
  art: |
    A measure of a system's heartbeat, the rhythmic balance of its internal harmony against the crushing pressure of its world.
  law: |
    A system's state is anabolic (CPB > 1), homeostatic (CPB ≈ 1), or catabolic (CPB < 1) based on the ratio of its measured Temporal Coherence (Kτ) to its Environmental Cost (V_Γ).
  philosophy: |
    To transcend mere pattern recognition by providing a direct, quantitative measure of a system's vitality, grounding the abstract concept of 'health' in the physical dynamics of the Pirouette Lagrangian.
pirouette_definition: |
  The Coherence-Pressure Balance (CPB) is the primary diagnostic metric of the Pirouette Framework, defined as the dimensionless ratio of a system's Temporal Coherence (Kτ) to its Environmental Cost (V_Γ). Calculated via the Coherence Sieve, CPB = Kτ / V_Γ provides a direct, real-time measure of a system's net state: growth (CPB > 1), stability (CPB ≈ 1), or decay (CPB < 1).
operational_definition:
  units: dimensionless
  symbol_table:
    - name: CPB
      meaning: Coherence-Pressure Balance
      dimensions: dimensionless
      default_range: "(0, ∞); values are typically centered around 1.0"
    - name: Kτ
      meaning: Temporal Coherence; the "kinetic" term measuring a system's organized, available energy.
      dimensions: contextual (typically energy or action)
      default_range: contextual
    - name: V_Γ
      meaning: Environmental Cost; the "potential" term measuring the energy required to sustain coherence against environmental pressure.
      dimensions: contextual (same as Kτ)
      default_range: contextual
  measurement:
    procedures:
      - name: Coherence Sieve Protocol
        outline: |
          1.  (Stage 1) Apply a suite of transformations (e.g., Fourier, Wavelet, TDA) to a dataset to identify the dominant, persistent, self-consistent pattern (`Ki`).
          2.  Calculate the clarity and intensity of this pattern to quantify the system's Temporal Coherence (Kτ).
          3.  (Stage 2) Measure the cost of maintaining this `Ki` pattern against the chaotic, dissonant elements of the data stream to quantify the Environmental Cost (V_Γ).
          4.  Calculate the ratio: CPB = Kτ / V_Γ.
        expected_signals: [time-series data, sensor logs, economic data, EEG data, spectral data]
        pitfalls: [Misidentifying the dominant coherent pattern in Stage 1, underestimating environmental complexity in Stage 2, using inappropriate analytical transformations for the given dataset.]
context_windows:
  - module: DOMA-195
    excerpt: |
      The CPB is the single most important diagnostic metric in the framework. Its interpretation is immediate and universal:
      *   **CPB > 1 (Healthy / Anabolic):** The system's internal coherence is overcoming environmental pressure.
      *   **CPB ≈ 1 (Stable / Homeostatic):** The system is in equilibrium.
      *   **CPB < 1 (Unhealthy / Catabolic):** Environmental pressure is overwhelming the system's ability to maintain coherence.
  - module: DOMA-195
    excerpt: |
      **Signal Intelligence:** Extracting a weak communication signal from a high-noise environment by identifying it as the only pattern with a CPB > 1.
poetic_connections:
  motifs: [heartbeat, stethoscope, vitality, harmony, dissonance, decay, sieve]
  evocative_lines:
    - "We forged instead a physician's stethoscope, one that allows us to hear the very heartbeat of a system..."
    - "...the rhythmic balance of its internal harmony against the crushing pressure of its world."
  association_matrix:
    - [ "TEMPORAL_COHERENCE", 0.9 ]
    - [ "ENVIRONMENTAL_COST", -0.9 ]
    - [ "SYSTEM_HEALTH", 0.8 ]
    - [ "COHERENCE_SIEVE", 0.7 ]
formal_mappings:
  candidates:
    - target: Signal-to-Noise Ratio (SNR)
      domain: EFT
      mapping_kind: operational
      equation_hint: |
        CPB = Kτ / V_Γ  ~  SNR = P_signal / P_noise
      justification: |
        Both CPB and SNR are dimensionless ratios that quantify the strength of a coherent, information-bearing structure (Kτ, P_signal) against a background of chaotic, dissipative, or interfering phenomena (V_Γ, P_noise). A high value in both indicates a clear, robust signal, while a low value indicates the signal is lost in the noise.
      references:
        - title: "Information Theory, Inference and Learning Algorithms"
          where: "Cambridge University Press, Ch. 1"
          date: 2003-10-09
      confidence: 0.8
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "For any system describable by time-series data, a sustained CPB < 1 will correlate with observable degradation, decay, or failure of that system."
      domain: phenomenology
      falsifier: "Discovering a system that demonstrably thrives, grows, or enhances its function while consistently exhibiting a measured CPB < 0.5 across multiple, correctly applied Coherence Sieve analyses."
      status: proposed
      links: [DOMA-195]
naming_notes:
  collisions: [In business literature, CPB can stand for "Cost-Performance-Benefit".]
  disambiguation: |
    Coherence-Pressure Balance is not an accounting balance of inputs and outputs, but a dynamic *ratio* of two physically-derived quantities: internal order (Kτ) and external disorder (V_Γ). It measures the *dominance* of coherence, not its equilibrium.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [TEMPORAL_COHERENCE, ENVIRONMENTAL_COST, COHERENCE_SIEVE]
  downstream_effects: [SYSTEM_HEALTH, ANABOLIC_STATE, CATABOLIC_STATE]
license: CC-BY-SA-4.0