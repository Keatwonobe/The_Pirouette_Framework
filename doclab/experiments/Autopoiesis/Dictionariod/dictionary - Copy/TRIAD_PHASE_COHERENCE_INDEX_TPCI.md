---
term: "Triad Phase Coherence Index (TPCI)"
canonical_id: "TRIAD_PHASE_COHERENCE_INDEX_TPCI"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["COG-RES-002"]
---

---
term: Triad Phase Coherence Index
canonical_id: TRIAD_PHASE_COHERENCE_INDEX
symbol: TPCI, C₃(t)
aliases: [Triadic Resonance Lock Integrity]
parents: [COG-RES-001]
children: [COG-RES-002, COG-RES-003, DOMA-096]
status: draft
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: COG-RES-002
      lines: "L49-L50"
      snippet: |
        Observe triad decoherence event where TPCI → 0.
  editors: [Pirouette-Agent]
  review_log: []
triad:
  art: |
    The listening ear turned inward, discerning the fragile three-part harmony of mind. It measures not the notes, but the silence between them where resonance lives or dies, a single number attesting to the chord's integrity.
  law: |
    The Triad Phase Coherence Index quantifies the degree of phase-locking between three resonant neural frequencies. A value approaching 1 indicates a stable conscious state, while a collapse towards 0 signals imminent decoherence and loss of access under cognitive load.
  philosophy: |
    To render the ephemeral lock of conscious access into a tangible, time-varying signal. TPCI transforms the state of being 'aware' from a binary predicate into a continuous, measurable dynamic variable, exposing its fragility and resilience near critical thresholds.
pirouette_definition: |
  A real-time, normalized metric valued in [0, 1] that quantifies the statistical integrity of a phase-locked neural frequency triad (f₁, f₂, f₃). It serves as the primary order parameter for the Triad-Locked Conscious Access Protocol, where TPCI ≈ 1 signifies a stable resonance lock (conscious access) and TPCI ≈ 0 indicates decoherence (collapse of access). Its dynamics, particularly its relaxation time, are used to measure critical slowing.
operational_definition:
  units: Dimensionless
  symbol_table:
    - name: C₃(t), TPCI
      meaning: Triad Phase Coherence Index as a function of time.
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: φᵢ(t)
      meaning: Instantaneous phase of the i-th frequency component.
      dimensions: dimensionless
      default_range: "[0, 2π)"
    - name: Ψ(t)
      meaning: Composite phase variable, e.g., φ₁(t) + φ₂(t) - φ₃(t).
      dimensions: dimensionless
      default_range: contextual
  measurement:
    procedures:
      - name: Tri-phasic Coherence Calculation
        outline: |
          1. Isolate three frequency bands (f₁, f₂, f₃) from broadband neural data (e.g., EEG/MEG) using narrow band-pass filters.
          2. Compute the instantaneous phase φ₁(t), φ₂(t), φ₃(t) for each signal using a Hilbert or Morlet wavelet transform.
          3. Define a composite phase variable representing the triadic interaction, typically Ψ(t) = φ₁(t) + φ₂(t) - φ₃(t).
          4. Calculate TPCI as the magnitude of the mean resultant vector over a short, sliding time window W: C₃(t) = |⟨exp(iΨ(t))⟩_W|.
        expected_signals: [High-density EEG, MEG, LFP recordings]
        pitfalls: [Spectral leakage between frequency bands, non-stationarity of signals, incorrect choice of triad frequencies, insufficient signal-to-noise ratio]
context_windows:
  - module: COG-RES-002
    excerpt: |
      **Collapse Trigger:** Observe triad decoherence event where TPCI → 0.
      **Recovery Phase:** Maintain stimulation but reduce Γ to observe triad reformation.
  - module: COG-RES-002
    excerpt: |
      **Relaxation Time (τ_P):** Defined as time between TPCI minimum and 90% recovery. Measure across multiple Γ-load ramps.
poetic_connections:
  motifs: [resonance, fragility, coherence, harmony, collapse, signal-from-noise]
  evocative_lines:
    - "Observe triad decoherence event where TPCI → 0."
    - "Sharp collapse + slow recovery"
  association_matrix:
    - [ "CRITICAL_SLOWING", 0.9 ]
    - [ "COGNITIVE_LOAD", 0.8 ]
    - [ "CONSCIOUS_ACCESS", 0.9 ]
    - [ "PHASE_TRANSITION", 0.7 ]
formal_mappings:
  candidates:
    - target: Order parameter ψ
      domain: SM
      mapping_kind: mathematical
      equation_hint: |
        TPCI ↔ |ψ|
      justification: |
        TPCI behaves as the macroscopic order parameter for the conscious access phase transition. It is non-zero (≈1) in the ordered phase (access) and vanishes (→0) in the disordered phase (collapse). Its fluctuations and relaxation dynamics near the critical point (Γ_c) are predicted to exhibit universal scaling laws, characteristic of order parameters in Ginzburg-Landau theory.
      references:
        - title: "Statistical Physics of Fields"
          where: "Chapter 1"
          date: 2002-01-01
      confidence: 0.9
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The recovery time (τ_P) of the TPCI after a forced collapse diverges as a power-law as the system approaches a critical cognitive load (Γ_c)."
      domain: experiment
      falsifier: "Recovery time measured via TPCI dynamics does not diverge near Γ_c, or shows a stochastic/linear relationship with load rather than the predicted power-law scaling."
      status: proposed
      links: [COG-RES-002, MATH-026]
    - statement: "A stable TPCI ≈ 1 is a necessary condition for conscious access as defined by the Triad-Locked Protocol."
      domain: phenomenology
      falsifier: "A subject reports conscious access to a stimulus while concurrent measurement shows TPCI ≈ 0 for the relevant neural triad."
      status: proposed
      links: [COG-RES-001]
naming_notes:
  collisions: [The term "Coherence Index" is generic in signal processing.]
  disambiguation: |
    TPCI specifically refers to the *three-way* phase-locking characteristic of the Triad-Locked Conscious Access model, not generic two-signal phase coherence or spectral power. It is an order parameter whose dynamics reveal critical phenomena, not just a static signal feature.
crosslinks:
  near_synonyms: [ORDER_PARAMETER]
  antonyms: [SPECTRAL_ENTROPY]
  prerequisites: [TRIAD_LOCKED_CONSCIOUS_ACCESS]
  downstream_effects: [CRITICAL_SLOWING, AWARENESS_RECOVERY_KINETICS]
license: CC-BY-SA-4.0
---

# Triad Phase Coherence Index

## Canonical (Pirouette)
A real-time, normalized metric valued in [0, 1] that quantifies the statistical integrity of a phase-locked neural frequency triad (f₁, f₂, f₃). It serves as the primary order parameter for the Triad-Locked Conscious Access Protocol, where TPCI ≈ 1 signifies a stable resonance lock (conscious access) and TPCI ≈ 0 indicates decoherence (collapse of access). Its dynamics, particularly its relaxation time, are used to measure critical slowing.

## EFT-First Summary
In the language of statistical field theory, the Triad Phase Coherence Index (TPCI) serves as the macroscopic order parameter for the phase transition governing conscious access. Its dynamics near the critical point of cognitive load (Γ_c) are described by a Ginzburg-Landau effective theory, where critical slowing and universal scaling exponents are predicted and measured. The collapse of TPCI from 1 to 0 represents the system transitioning from an ordered (coherent, access) phase to a disordered (decoherent, non-access) phase.

## Glossary Links
- See also: [CRITICAL_SLOWING](critical-slowing), [TRIAD_LOCKED_CONSCIOUS_ACCESS](triad-locked-conscious-access), [ORDER_PARAMETER](order-parameter)