---
term: "Sensing Layer"
canonical_id: "SENSING_LAYER"
symbol: ""
aliases: [The Probe]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-128"]
---

---
term: Sensing Layer
canonical_id: SENSING_LAYER
symbol: 
aliases: ["The Probe"]
parents: [DOMA-128]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-128
      snippet: |
        Sensing Layer | *The Probe* | Measures the primary resonant pattern of the system—its "heartbeat." Examples include a Coherence Probe analyzing a Ki pattern's phase noise, a network tap measuring packet jitter, or a linguistic model parsing conversational coherence.
  editors: [GPT-4 (Pirouette Dictionary Agent)]
  review_log: []
triad:
  art: |
    The ear pressed against the machine, listening for the quiet hum of health or the stutter of friction. It is the stethoscope that translates a system's silent, internal state into a discernible rhythm.
  law: |
    The Sensing Layer must capture the primary resonant pattern of a system with sufficient fidelity to calculate its Temporal Adherence (Tₐ) and Temporal Friction ((Δωₖ)²). Its signal-to-noise ratio must exceed the baseline entropic signature of the system itself.
  philosophy: |
    The Sensing Layer is the point of empirical grounding for the Coherence Ledger. Without a faithful probe into a system's actual behavior, all subsequent calculations are fiction; it enforces honesty by demanding direct, falsifiable observation.
pirouette_definition: |
  The first of the three functional layers in the Coherence Ledger architecture. The Sensing Layer is the instrumentation component responsible for direct measurement of a system's primary resonant pattern (its "heartbeat" or Ki pattern). It acts as a transducer, converting the system's dynamic state into a raw, time-series signal for analysis by the Computation Layer.
operational_definition:
  units: Context-dependent (e.g., V, packets/s, bits/s, token/s, phase angle).
  symbol_table:
    - name: Ψ(t)
      meaning: Raw time-series signal from the Sensing Layer representing the system's resonant pattern.
      dimensions: Contextual
      default_range: Contextual
  measurement:
    procedures:
      - name: Ki Pattern Phase Noise Analysis
        outline: |
          A Coherence Probe is coupled to the system to detect its Ki pattern. The probe measures the phase and frequency deviations of this signal over time to produce the raw data stream Ψ(t).
        expected_signals: [A periodic or quasi-periodic signal with measurable phase/frequency jitter.]
        pitfalls: [Misidentifying the primary Ki pattern, aliasing, probe-induced system interference.]
      - name: Network Packet Jitter Analysis
        outline: |
          A network tap monitors a critical data stream. The inter-arrival time of packets is measured, and the variance (jitter) constitutes the raw signal Ψ(t).
        expected_signals: [A stream of timestamps representing packet arrivals.]
        pitfalls: [Network congestion unrelated to system coherence, clock synchronization errors.]
context_windows:
  - module: DOMA-128
    excerpt: |
      **Sensing Layer** | *The Probe* | Measures the primary resonant pattern of the system—its "heartbeat." Examples include a Coherence Probe analyzing a Ki pattern's phase noise, a network tap measuring packet jitter, or a linguistic model parsing conversational coherence.
  - module: DOMA-128
    excerpt: |
      A system's health is written in the silence of its operation. The Flow Dynamics modules (`DYNA-001`, `DYNA-003`) provide the qualitative language to diagnose this health—the art of the physician. This module provides the physician's instrument—the means to move from artful diagnosis to rigorous measurement.
poetic_connections:
  motifs: [listening, heartbeat, resonance, probe, stethoscope, signal, noise, ground-truth]
  evocative_lines:
    - "A system's health is written in the silence of its operation."
    - "It hears the sound of a system arguing with itself..."
  association_matrix:
    - [ "ENTROPIC_FLUX", 0.8 ]
    - [ "KI_PATTERN", 0.7 ]
    - [ "COMPUTATION_LAYER", 0.9 ]
formal_mappings:
  candidates:
    - target: Time-series data acquisition system / Transducer
      domain: Signal Processing|Control Theory
      mapping_kind: operational
      equation_hint: |
        Ψ(t) = f(system_state) + noise
      justification: |
        The Sensing Layer functions as a transducer, converting a system's physical or informational dynamic state into a processable time-series signal, Ψ(t). This aligns with the role of sensors in control theory and data acquisition systems in signal processing, which provide the raw observational data for analysis.
      references:
        - title: Feedback Control of Dynamic Systems
          where: Chapter 2: Modeling in the Frequency Domain
          date: 2010-01-01
      confidence: 0.9
  adopted:
    - target:
      rationale:
      confidence: 0.0
constraints_and_falsifiers:
  claims:
    - statement: "Any system governed by the Pirouette Lagrangian possesses a primary resonant pattern that is detectable by a sufficiently sensitive Sensing Layer."
      domain: phenomenology
      falsifier: "Discovering a system that demonstrably exhibits coherence loss (e.g., generates waste heat, errors) but which possesses no primary, coherent, and measurable degree of freedom to serve as its resonant pattern."
      status: proposed
      links: [DOMA-128]
naming_notes:
  collisions: ["Sensor" and "Probe" are generic terms in engineering and physics.]
  disambiguation: |
    In the Pirouette Framework, the "Sensing Layer" is not just any sensor, but specifically the architectural component of the Coherence Ledger (`DOMA-128`) whose function is to capture the signal used to calculate Entropic Flux. It is defined by its role preceding the Computation Layer.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [COHERENCE_LEDGER, KI_PATTERN]
  downstream_effects: [COMPUTATION_LAYER, ENTROPIC_FLUX]
license: CC-BY-SA-4.0
---

# Sensing Layer

## Canonical (Pirouette)
The first of the three functional layers in the Coherence Ledger architecture. The Sensing Layer is the instrumentation component responsible for direct measurement of a system's primary resonant pattern (its "heartbeat" or Ki pattern). It acts as a transducer, converting the system's dynamic state into a raw, time-series signal for analysis by the Computation Layer.

## EFT-First Summary
Operationally, the Sensing Layer is analogous to a transducer or data acquisition system in signal processing and control theory. It is the physical or logical instrument that captures a time-series signal Ψ(t) which is a function of the system's core dynamic state. This raw signal serves as the empirical input for all subsequent analysis of system coherence and efficiency.

## Glossary Links
- See also: [Coherence Ledger](link), [Computation Layer](link), [Ki Pattern](link)