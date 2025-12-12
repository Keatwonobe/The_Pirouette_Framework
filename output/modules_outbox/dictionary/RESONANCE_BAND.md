---
term: "Resonance Band"
canonical_id: "RESONANCE_BAND"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-129"]
---

---
term: Resonance Band
canonical_id: RESONANCE_BAND
symbol: "[Γ_low, Γ_high]"
aliases: []
parents: [DOMA-129]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-129
      lines: "§3"
      snippet: |
        Resonance Band | Transitional | **Isolate a Specific Rhythm.** Retain segments within a specific coherence range. Used to focus on systems of a particular complexity.
  editors: [GPT-4]
  review_log: []
triad:
  art: |
    Like tuning a radio past the static and the silent gaps to find a specific station's broadcast. It is an act of listening for a particular melody, neither perfectly simple nor completely chaotic.
  law: |
    A Resonance Band filter, when applied to a data stream segmented and quantified by a Temporal Pressure proxy (Γ), retains only those segments `s_i` where the measured value `Γ(s_i)` falls within a defined range `[Γ_low, Γ_high]`. All other segments are discarded.
  philosophy: |
    This principle asserts that the most interesting and complex systems often exist not at the extremes of order or chaos, but in a transitional "edge of chaos" state. A Resonance Band is a tool for focusing analysis on this creative, adaptive zone of intermediate complexity.
pirouette_definition: |
  A filtering principle of the Coherence Sieve that isolates signal segments whose local Temporal Pressure (Γ) falls within a specified range, `[Γ_low, Γ_high]`. This method targets systems of a specific complexity or rhythm, distinct from the extremes of pure laminar (low-Γ) or turbulent (high-Γ) flow.
operational_definition:
  units: bits or nats (when using Shannon Entropy as the proxy for Γ)
  symbol_table:
    - name: Γ_low
      meaning: The lower bound of the targeted Temporal Pressure band.
      dimensions: dimensionless (information)
      default_range: contextual
    - name: Γ_high
      meaning: The upper bound of the targeted Temporal Pressure band.
      dimensions: dimensionless (information)
      default_range: contextual
  measurement:
    procedures:
      - name: Resonance Band Sieving
        outline: |
          1. **Segmentation:** Divide the input data stream into discrete, uniform temporal segments.
          2. **Quantification:** Calculate the local Temporal Pressure (Γ) for each segment using a chosen proxy method (e.g., Shannon Entropy).
          3. **Sieving:** Apply the Resonance Band logic: retain a segment if its calculated Γ satisfies `Γ_low ≤ Γ ≤ Γ_high`.
          4. **Output:** Construct a new data stream from the retained segments.
        expected_signals: [A filtered data stream exhibiting a consistent, intermediate level of complexity or "liveliness."]
        pitfalls: [Poor calibration of Γ_low and Γ_high can exclude the target phenomena or include excessive noise. The choice of `GammaProxyMethod` heavily influences the measured Γ values.]
context_windows:
  - module: DOMA-129
    excerpt: |
      **Resonance Band** | Transitional | **Isolate a Specific Rhythm.** Retain segments within a specific coherence range. Used to focus on systems of a particular complexity.
  - module: DOMA-129
    excerpt: |
      **Financial Market Analysis:** A *Resonance Band* filter can be used to study the behavior of assets within a specific volatility (coherence) class, while a *Turbulent Pass* identifies moments of market panic or chaotic trading.
poetic_connections:
  motifs: [tuning, rhythm, complexity, specific frequency, edge of chaos, bandpass]
  evocative_lines:
    - "Isolate a Specific Rhythm."
    - "...build a net that catches only the bells."
  association_matrix:
    - [ "COHERENCE_SIEVE", 0.9 ]
    - [ "TEMPORAL_PRESSURE", 0.8 ]
    - [ "LAMINAR_FLOW", 0.5 ]
    - [ "TURBULENT_FLOW", 0.5 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Band-pass filter
      domain: Signal Processing
      mapping_kind: operational
      equation_hint: |
        Output(s) = Input(s) if F(s) ∈ [f_low, f_high]
      rationale: |
        Operationally, the Resonance Band is identical to a band-pass filter. However, instead of filtering based on frequency (f), it filters based on local Temporal Pressure (Γ), a proxy for complexity or information density. It passes a "band" of coherence.
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "A system's organizational complexity class corresponds to a stable and identifiable band of Temporal Pressure (Γ)."
      domain: phenomenology
      falsifier: "If systems of demonstrably different complexity (e.g., a crystal vs. a bacterium vs. a star) are found to consistently occupy the same Γ-band, or a system's complexity changes without a corresponding shift in its Γ-band, the claim is falsified."
      status: proposed
      links: [DOMA-129]
naming_notes:
  collisions: []
  disambiguation: |
    Must be distinguished from a conventional *frequency-based* band-pass filter. Resonance Band operates on the *coherence* or *complexity* of a signal segment, not its oscillation frequency. It is also the inverse of a Dissonance Notch filter, which *removes* a specific band of dissonance.
crosslinks:
  near_synonyms: []
  antonyms: [LAMINAR_PASS, TURBULENT_PASS, DISSONANCE_NOTCH]
  prerequisites: [COHERENCE_SIEVE, TEMPORAL_PRESSURE]
  downstream_effects: []
license: CC-BY-SA-4.0
---

# Resonance Band

## Canonical (Pirouette)
A filtering principle of the Coherence Sieve that isolates signal segments whose local Temporal Pressure (Γ) falls within a specified range, `[Γ_low, Γ_high]`. This method targets systems of a specific complexity or rhythm, distinct from the extremes of pure laminar (low-Γ) or turbulent (high-Γ) flow.

## EFT-First Summary
Operationally, the Resonance Band is a direct analog to a **band-pass filter** from classical signal processing. It selects for a specific "band" of activity, but instead of filtering on frequency, it filters on a measure of local complexity or information density (Temporal Pressure, Γ). This allows for the isolation of phenomena existing in a state of intermediate complexity, often associated with the "edge of chaos."

## Glossary Links
- See also: Coherence Sieve, Temporal Pressure, Laminar Pass, Turbulent Pass