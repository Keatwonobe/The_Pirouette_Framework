---
term: "Turbulence Index"
canonical_id: "TURBULENCE_INDEX"
symbol: "T_idx"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-068"]
---

---
term: Turbulence Index
canonical_id: TURBULENCE_INDEX
symbol: T_idx
aliases: []
parents: [DOMA-068, DYNA-001]
children: [INST-DIAG-001]
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-068
      lines: "L48-L50"
      snippet: |
        **`T_idx`** is the **Turbulence Index**, a dimensionless measure (0 to 1) of the system's internal dissonance. It quantifies how much a system's Ki pattern is deviating from a pure, laminar state. `T_idx = 0` for perfect Laminar Flow; `T_idx = 1` for pure chaos.
  editors: [dictionary-generator]
  review_log: []
triad:
  art: |
    The static on a perfect signal; the grit in a flawless gear. It is the measure of a system's internal argument, the sound of its own parts working at cross-purposes.
  law: |
    The Turbulence Index is a normalized, dimensionless scalar (0 ≤ T_idx ≤ 1) quantifying the degree to which a system's measured Ki pattern deviates from an idealized laminar flow profile, where T_idx = 0 represents perfect coherence and T_idx = 1 represents maximal decoherence.
  philosophy: |
    This index reframes systemic failure not as a binary event, but as a continuous spectrum of self-sabotage. It asserts that inefficiency is a choice, encoded in the geometry of a system's flow. Measuring `T_idx` is therefore not just a diagnosis of state but an audit of a system's commitment to its own purpose.
pirouette_definition: |
  A dimensionless scalar, ranging from 0 to 1, that quantifies a system's internal friction and deviation from its geodesic of maximal coherence. It is calculated by the Coherence Engine from the system's resonant Ki pattern. A value of 0 indicates perfect Laminar Flow, where all energy is channeled into coherent work, while a value of 1 indicates total Turbulent Flow, where coherence is actively degraded into systemic noise.
operational_definition:
  units: dimensionless
  symbol_table:
    - name: T_idx
      meaning: Turbulence Index
      dimensions: dimensionless
      default_range: "[0, 1]"
  measurement:
    procedures:
      - name: Ki Pattern Spectral Analysis
        outline: |
          1. Use a Temporal Signature Array to capture the system's full-spectrum Ki pattern over a representative time interval.
          2. Establish the system's ideal laminar signature, either from a theoretical model or a baseline measurement in a known healthy state. This serves as the 'fundamental frequency'.
          3. Perform a spectral decomposition (e.g., Fourier transform) on the captured signal.
          4. The Turbulence Index is calculated as the ratio of power in the non-fundamental (turbulent) frequency bands to the total signal power.
        expected_signals: [Ki pattern spectral data, Temporal Signature Array output]
        pitfalls: [Signal aliasing from insufficient sample rate, Contamination from ambient Temporal Pressure (Γ), Misidentification of the fundamental laminar frequency]
context_windows:
  - module: DOMA-068
    excerpt: |
      The rate of local entropy production (`Ṡ_local`) is directly proportional to the ambient Temporal Pressure and the degree of the system's own internal turbulence.
      `Ṡ_local ∝ Γ ⋅ T_idx`
      Where:
      *   **`Γ`** is the local **Temporal Pressure**...
      *   **`T_idx`** is the **Turbulence Index**, a dimensionless measure (0 to 1) of the system's internal dissonance. It quantifies how much a system's Ki pattern is deviating from a pure, laminar state.
  - module: DOMA-068
    excerpt: |
      The **Coherence Auditor Kit (CAK)**... modernizes the old DRIK into a streamlined instrumentation stack for measuring and logging the Coherence Cost. The **Coherence Engine** processor, in real-time, calculates the Turbulence Index (`T_idx`) from the Ki signal and computes the local entropy rate (`Ṡ_local`) using Γ.
poetic_connections:
  motifs: [friction, dissonance, static, waste, self-sabotage]
  evocative_lines:
    - "It is the quantifiable 'heat' of a system failing to be elegant."
    - "The universe does not suffer inefficiency gladly."
  association_matrix:
    - [ "COHERENCE_COST", 0.9 ]
    - [ "TEMPORAL_PRESSURE", 0.5 ]
    - [ "LAMINAR_FLOW_STATE", 0.8 ]
formal_mappings:
  candidates:
    - target: Total Harmonic Distortion (THD)
      domain: Signal Processing
      mapping_kind: operational
      equation_hint: |
        THD = (√(P₂ + P₃ + P₄ + ...)) / P_total
      justification: |
        `T_idx` functionally measures the 'impurity' of a system's Ki signal, analogous to how THD measures the distortion of an electrical signal. A pure, laminar Ki pattern is equivalent to a pure sine wave (the fundamental), while turbulence introduces higher-order harmonics and noise. `T_idx` can be operationally defined as a normalized measure of the power contained in these non-fundamental components relative to the total signal power.
      references:
        - title: IEEE Standard 519-2014, "Recommended Practice and Requirements for Harmonic Control in Electric Power Systems"
          where: Section 10.2
          date: 2014-06-13
      confidence: 0.8
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "`T_idx` is a necessary and sufficient condition for predicting the rate of Coherence Cost production, given a stable Temporal Pressure Γ."
      domain: phenomenology
      falsifier: "Observing a system with a high `T_idx` (>0.8) producing a low Coherence Cost, or a system with a low `T_idx` (<0.1) producing a high Coherence Cost, while the ambient Temporal Pressure (Γ) is held constant."
      status: supported
      links: [DOMA-068]
naming_notes:
  collisions: [T is often Temperature or Time; "Turbulence" is a broad concept in fluid dynamics.]
  disambiguation: |
    Distinct from the Reynolds number (`Re`) in classical fluid dynamics, which predicts the *onset* of turbulence based on fluid properties and flow conditions. `T_idx` does not predict onset; it directly quantifies the *degree* of existing turbulence within a system's information-energetic flow, regardless of the underlying medium.
crosslinks:
  near_synonyms: [DISSONANCE]
  antonyms: [LAMINAR_FLOW_STATE, COHERENCE]
  prerequisites: [KI_PATTERN, TEMPORAL_SIGNATURE_ARRAY]
  downstream_effects: [COHERENCE_COST, ENTROPY_LEDGER]
license: CC-BY-SA-4.0
---

# Turbulence Index

## Canonical (Pirouette)
A dimensionless scalar, ranging from 0 to 1, that quantifies a system's internal friction and deviation from its geodesic of maximal coherence. It is calculated by the Coherence Engine from the system's resonant Ki pattern. A value of 0 indicates perfect Laminar Flow, where all energy is channeled into coherent work, while a value of 1 indicates total Turbulent Flow, where coherence is actively degraded into systemic noise.

## EFT-First Summary
The Turbulence Index is operationally analogous to Total Harmonic Distortion (THD) in signal processing. It measures the ratio of power in the dissonant, non-fundamental components of a system's Ki signal to the total signal power, providing a dimensionless measure of the system's deviation from a pure, coherent state. A high `T_idx` corresponds to a signal with significant noise and harmonic distortion, indicating inefficient and turbulent internal dynamics.

## Glossary Links
- See also: [Coherence Cost](<link>), [Laminar Flow](<link>), [Temporal Pressure](<link>)