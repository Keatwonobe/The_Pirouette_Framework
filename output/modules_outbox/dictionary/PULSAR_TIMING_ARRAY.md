---
term: "Pulsar Timing Array"
canonical_id: "PULSAR_TIMING_ARRAY"
symbol: "PTA"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-073"]
---

---
term: Pulsar Timing Array
canonical_id: PULSAR_TIMING_ARRAY
symbol: PTA
aliases: []
parents: [DOMA-073]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-073
      lines: "L101-L104"
      snippet: |
        1.  **The Instrument**: Combine the long-term timing data from the world's leading Pulsar Timing Arrays (NANOGrav, EPTA, PPTA) into a single dataset of the highest possible sensitivity and sky coverage.
  editors: [auto-scribe-v2]
  review_log: []
triad:
  art: |
    A vast, galactic stethoscope built from the cosmos's most stable clocks, used to listen for the faint, resonant heartbeat of spacetime itself.
  law: |
    An array of millisecond pulsars, when their timing residuals are cross-correlated, acts as a long-baseline detector for periodic, nanohertz-frequency variations in background Temporal Pressure (Γ).
  philosophy: |
    The PTA elevates the framework's principles from a local theory to a universal law, testing its scale-invariance by using the entire galaxy as a laboratory to measure the universe's primordial memory.
pirouette_definition: |
  A galactic-scale instrument composed of a distributed set of highly stable millisecond pulsars. Within the Pirouette Framework, a PTA serves as a direct probe of cosmological-scale, time-dependent variations in background Temporal Pressure (Γ). By analyzing the cross-correlated timing residuals of its constituent pulsars, a PTA can isolate a common-mode signal, such as the primordial Γ oscillation (the 'cosmic heartbeat'), and verify its origin via the Ki-Lock Test.
operational_definition:
  units: seconds (s)
  symbol_table:
    - name: δt
      meaning: Pulsar timing residual; deviation from the expected time-of-arrival.
      dimensions: T
      default_range: 10⁻⁹ to 10⁻⁶ s
  measurement:
    procedures:
      - name: Cosmic Heartbeat Detection
        outline: |
          1.  Combine multi-decade timing data from multiple PTAs (e.g., NANOGrav, EPTA, PPTA).
          2.  Pre-whiten the timing residuals for each pulsar to remove known noise sources (e.g., interstellar medium, clock errors, stochastic GW background).
          3.  Perform a matched-filter search for a coherent, common-mode periodic signal across the array.
          4.  Validate any candidate signal using the Ki-Lock Test to confirm its harmonic content aligns with the framework's fundamental constants.
        expected_signals: [A common, narrow-band, periodic signal in timing residuals, Ki-locked harmonic content]
        pitfalls: [Misidentification of the stochastic gravitational-wave background, Insufficient sensitivity to distinguish the signal from instrumental or ephemeris noise]
context_windows:
  - module: DOMA-073
    excerpt: |
      A pulsar's signal is more than a beacon; it is a measuring line laid across the cosmos. The light from these celestial clocks is a coherent pattern propagating through the dynamic medium of the coherence manifold. As the pulsar's signal traverses the oscillating Γ(t) of the cosmic heartbeat, its travel time will be periodically stretched and compressed to maintain maximal coherence along its geodesic path. This will imprint a predictable, periodic "wobble" onto the time-of-arrival data recorded by Pulsar Timing Arrays (PTAs).
  - module: DOMA-073
    excerpt: |
      Employ a matched-filter search across the cleaned residual data, specifically looking for a faint, narrow-band, periodic signal that is **common across a significant number of pulsars**. This shared nature is the key indicator of a global, cosmological effect. The definitive confirmation is not just finding a signal, but verifying its identity. A true detection of the cosmic heartbeat must exhibit amplitude ratios and harmonic content that are geometrically locked to the framework's fundamental Ki constants.
poetic_connections:
  motifs: [cosmic stethoscope, galactic metronome, celestial clockwork]
  evocative_lines:
    - "We sought to test our laws against the heavens and found ourselves taking the pulse of the universe."
    - "A theory proven only in the laboratory is a song sung in a quiet room."
  association_matrix:
    - [ "TEMPORAL_PRESSURE", 0.9 ]
    - [ "WOUND_CHANNEL", 0.7 ]
    - [ "SCALE_INVARIANCE", 0.8 ]
formal_mappings:
  candidates:
    - target: Nanohertz Gravitational-Wave Detector
      domain: GR
      mapping_kind: operational
      equation_hint: |
        Signal ∝ h(t) [GR] vs. Signal ∝ ∫ δΓ(t) dt [Pirouette]
      justification: |
        In General Relativity, a PTA is an instrument designed to detect nanohertz-frequency gravitational waves, particularly the stochastic background from supermassive black hole binary mergers. Both the Pirouette and GR models use the cross-correlation of timing residuals from multiple pulsars to detect a common, spatially correlated signal. The experimental apparatus and data analysis techniques are identical.
      references:
        - title: The NANOGrav 15-year Data Set - Evidence for a Nanohertz Gravitational-Wave Background
          where: The Astrophysical Journal Letters, 951(1), L8
          date: 2023-06-28
      confidence: 0.95
  adopted:
    - target: Nanohertz Gravitational-Wave Detector
      rationale: The mapping is adopted because the physical instrument and measurement procedure are identical. The Pirouette Framework reinterprets the detected signal not as a metric perturbation (a GW) but as an integrated oscillation in Temporal Pressure (Γ), which it posits as the more fundamental quantity.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "A PTA can distinguish the primordial Γ oscillation (Cosmic Heartbeat) from the stochastic gravitational-wave background (SGWB)."
      domain: phenomenology
      falsifier: "The signal detected by PTAs is shown to have properties (e.g., Hellings-Downs correlation) that are uniquely consistent with a tensorial metric perturbation from GR and inconsistent with the scalar-like perturbation predicted for Γ oscillations. Furthermore, no Ki-locked harmonic content is ever detected despite sufficient signal-to-noise."
      status: proposed
      links: [DOMA-073]
naming_notes:
  collisions: []
  disambiguation: |
    While operationally identical to the instrument used in standard cosmology to search for gravitational waves, in the Pirouette context, 'PTA' specifically refers to its function as a detector of Temporal Pressure (Γ) variations. The interpretation of the signal, not the hardware or initial data processing, is what differs.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [CORE-006, CORE-008, CORE-011]
  downstream_effects: []
license: CC-BY-SA-4.0