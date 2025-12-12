---
term: "Phase-locking value"
canonical_id: "PHASE_LOCKING_VALUE"
symbol: "PLV"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-154"]
---

---
term: Phase-locking value
canonical_id: PHASE_LOCKING_VALUE
symbol: PLV
aliases: []
parents: [DOMA-154]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-154
      snippet: |
        It then measures the phase-locking value (PLV) at this frequency to quantify the synchronization. A high PLV is the definitive signature of a Macro-Ki.
  editors: [weavers.ai/synthesis-agent]
  review_log: []
triad:
  art: |
    The measure of how closely different instruments in the cosmic orchestra play the same note at the same time. It is the audible signature of a shared song, turning the cacophony of isolated events into a unified chord.
  law: |
    A phase-locking value approaching 1 between two or more normalized domain variables indicates that they are entrained by a common, powerful Temporal Pressure (Macro-Γ), revealing a shared macro-geodesic.
  philosophy: |
    PLV is the empirical tool that substantiates the Principle of Correspondence. It provides the quantitative evidence that disparate domains are not merely correlated but are participating in a single, coherent, emergent dynamic, making the invisible architecture of systemic causality visible.
pirouette_definition: |
  A dimensionless metric, ranging from 0 to 1, that quantifies the degree of phase synchronization between two or more time-series signals at a specific resonant frequency (`ωk`). A PLV of 0 indicates random, independent phase relationships, while a PLV of 1 indicates perfect, constant phase-locking. Within the Concordance Protocol, a sustained high PLV is the definitive signature of a shared resonance (Macro-Ki) linking multiple domains.
operational_definition:
  units: dimensionless
  symbol_table:
    - name: PLV
      meaning: Phase-locking value; degree of phase synchronization.
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: φ_i(t)
      meaning: Instantaneous phase of signal i at time t.
      dimensions: dimensionless (radians)
      default_range: contextual
    - name: N
      meaning: Number of signals or domains being compared.
      dimensions: dimensionless
      default_range: "≥ 2"
  measurement:
    procedures:
      - name: Resonance Detection (via Concordance Protocol)
        outline: |
          1. Select time-series data from N normalized domains per `DYNA-001`.
          2. Apply a time-frequency decomposition (e.g., Hilbert or wavelet transform) to each signal to extract its instantaneous phase `φ_i(t)`.
          3. At each time point t, compute the phase difference between all pairs of signals.
          4. Calculate the PLV as the magnitude of the mean resultant vector of these phase differences over a given time window. A value near 1 signifies strong, consistent phase-locking.
        expected_signals: [Sustained PLV > 0.7 at a common resonant frequency `ωk` across conceptually distant domains.]
        pitfalls: [Mistaking spurious correlations for true phase-locking (insufficient time window), failure to properly normalize domain variables, ignoring significant phase leads/lags.]
context_windows:
  - module: DOMA-154
    excerpt: |
      The engine searches not for amplitude correlation, but for a shared "resonant peak"—a persistent, common frequency and phase (`ωk`, `φk`) at which the systems begin to move in concert. It then measures the phase-locking value (PLV) at this frequency to quantify the synchronization. A high PLV is the definitive signature of a Macro-Ki.
  - module: DOMA-154
    excerpt: |
      When this instrument detects a shared resonance, it has found empirical evidence that these disparate systems are navigating the *same **macro-geodesic***. Subjected to a sufficiently powerful shared pressure, they have abandoned their individual paths for a new, collective path of least resistance. The threads are not just coincidentally similar; they are all flowing downhill along the same cosmic contour.
poetic_connections:
  motifs: [synchronization, resonance, harmony, entrainment, symphony, coherence]
  evocative_lines:
    - "Hearing the Symphony in the Noise."
    - "This protocol is a tuning fork for reality itself."
  association_matrix:
    - [ "MACRO_KI", 0.9 ]
    - [ "RESONANT_CONCORDANCE", 0.9 ]
    - [ "COHERENCE_Kτ", 0.7 ]
    - [ "TEMPORAL_PRESSURE_Γ", 0.6 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Phase-locking value (PLV)
      domain: Signal Processing | Neuroscience
      mapping_kind: mathematical
      equation_hint: |
        PLV = | E[exp(i * (φ_1(t) - φ_2(t)))] |
      justification: |
        The Pirouette Framework's PLV is mathematically identical to the metric used to measure phase synchrony between brain regions from EEG/MEG signals. It measures the consistency of the phase difference between two signals over time. The framework's innovation is its cross-domain application via the Concordance Protocol.
      references:
        - title: Measuring phase synchrony in brain signals
          where: Human Brain Mapping 8(4), 194-208 (Lachaux et al.)
          date: 1999-01-01
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "A sustained, high PLV (>0.7) between conceptually distant domains (e.g., market volatility and public health metrics) is sufficient evidence of a shared, non-local driver (a Macro-Γ)."
      domain: phenomenology
      falsifier: "Discovering a pair of high-PLV domains whose synchronization can be fully explained by a direct, local causal link or a third, confounding local variable, without invoking a higher-order systemic pressure."
      status: proposed
      links: [DOMA-154]
naming_notes:
  collisions: []
  disambiguation: |
    PLV is distinct from amplitude correlation (e.g., Pearson correlation). Two signals can have a high PLV while having zero amplitude correlation if their phase difference is constant but not zero (e.g., one consistently leads the other by 90 degrees). The Concordance Protocol prioritizes PLV as it reveals a shared *rhythm* over a shared *magnitude*.
crosslinks:
  near_synonyms: [COHERENCE_Kτ]
  antonyms: [DECOUPLING, DESYNCHRONIZATION]
  prerequisites: [TEMPORAL_PRESSURE_Γ, DYNA-001]
  downstream_effects: [RESONANT_CONCORDANCE, MACRO_KI]
license: CC-BY-SA-4.0
---