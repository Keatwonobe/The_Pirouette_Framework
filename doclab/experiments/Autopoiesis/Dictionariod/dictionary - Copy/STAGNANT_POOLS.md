---
term: "Stagnant Pools"
canonical_id: "STAGNANT_POOLS"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-181"]
---

---
term: Stagnant Pools
canonical_id: STAGNANT_POOLS
symbol: S₀
aliases: [Information Desert, Blocked Flow, Null Current]
parents: [DOMA-181, DYNA-001]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-181
      lines: "§3, Stage III"
      snippet: |
        -   **Stagnant Pools:** Regions where both `Kτ` and `Γ` are persistently low, indicating a lack of new information or a blocked flow. These regions will exhibit a **sustained, near-zero CR**.
  editors: [System Agent]
  review_log: []
triad:
  art: |
    A quiet surface concealing no depth; the silence not of peace, but of cessation. It is the riverbed run dry, where the current of information has ceased to flow.
  law: |
    A system is in a Stagnant Pool state if, over a sustained observation window, both its Coherence (`Kτ`) and Dissonance (`Γ`) remain below a context-dependent noise floor, resulting in a Coherence Ratio (CR) that is statistically indistinguishable from zero.
  philosophy: |
    Stagnant Pools reveal that the absence of chaos is not always desirable. They distinguish the disciplined silence of a clear signal from the empty silence of a dead channel, providing a crucial diagnostic for system health, decay, or informational starvation.
pirouette_definition: |
  A Stagnant Pool is a diagnosed state of an information stream, identified by the Rhythmic Sieve protocol, characterized by persistently low values for both Coherence (`Kτ`) and Dissonance (`Γ`). This dual-low condition indicates a lack of both structured signal and chaotic noise, signifying a state of informational inactivity, blockage, or system death. It is operationally confirmed by a Coherence Ratio (`CR`) that remains near-zero over a significant temporal window.
operational_definition:
  units: Dimensionless (state classification)
  symbol_table:
    - name: Kτ
      meaning: Coherence; measure of internal order and stable patterns in a window.
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: Γ
      meaning: Dissonance; measure of internal chaos and noise in a window.
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: CR
      meaning: Coherence Ratio (Kτ / Γ); measure of signal-to-noise.
      dimensions: dimensionless
      default_range: "≈ 0 for this state"
  measurement:
    procedures:
      - name: Rhythmic Sieve Flow Diagnosis
        outline: |
          1. Apply Rhythmic Segmentation to the information stream to create temporal windows.
          2. For each window, compute Coherence (`Kτ`) and Dissonance (`Γ`) to generate a Coherence Profile.
          3. Identify consecutive windows where both `Kτ < ε` and `Γ < ε`, where `ε` is the empirically determined noise floor for the system.
          4. Confirm that the Coherence Ratio `CR` for this region is sustained near zero.
        expected_signals: [A time-series plot of `Kτ` and `Γ` both showing a flatline near zero.]
        pitfalls: [Mistaking a low-amplitude Laminar Channel for a Stagnant Pool (remedy: check `CR`, which is high for Laminar). Setting the noise floor `ε` too high, leading to false positives.]
context_windows:
  - module: DOMA-181
    excerpt: |
      **Stagnant Pools:** Regions where both `Kτ` and `Γ` are persistently low, indicating a lack of new information or a blocked flow. These regions will exhibit a **sustained, near-zero CR**.
  - module: DOMA-181
    excerpt: |
      By profiling a stream in terms of the interplay between Coherence and Dissonance, we can diagnose its state of flow (`Laminar`, `Turbulent`, or `Stagnant`) with far greater precision...
poetic_connections:
  motifs: [stillness, silence, blockage, desert, calm, decay, zero-point]
  evocative_lines:
    - "...the deep, silent channels hidden beneath the surface noise."
    - "...a lack of new information or a blocked flow."
  association_matrix:
    - [ "COHERENCE", 0.9 ]
    - [ "DISSONANCE", 0.9 ]
    - [ "LAMINAR_CHANNELS", 0.7 ]
    - [ "TURBULENT_EDDIES", 0.7 ]
    - [ "COHERENCE_RATIO", 0.8 ]
formal_mappings:
  candidates: []
  adopted:
    - target: System ground state / Quiescent state
      domain: CM|Signal Processing
      mapping_kind: conceptual
      equation_hint: |
        ⟨E⟩ → 0
      justification: |
        A Stagnant Pool represents an information-theoretic ground state. Like a physical system at its lowest energy level (e.g., 0 K) or a circuit in a quiescent state, it exhibits minimal internal dynamics (low `Kτ`) and minimal random fluctuations (low `Γ`). It is the state of "nothing happening" informationally.
      references: []
      confidence: 0.6
constraints_and_falsifiers:
  claims:
    - statement: "A complex system cannot transition from a Turbulent Eddy directly to a Laminar Channel without passing through a transient or stable Stagnant Pool state."
      domain: phenomenology
      falsifier: "Observing a statistically significant number of direct `Turbulent -> Laminar` transitions where `Kτ` rises as `Γ` falls, without an intermediary period where both are below the system's noise floor."
      status: proposed
      links: [DOMA-181, DYNA-001]
naming_notes:
  collisions: [The `S₀` symbol is commonly used for entropy or ground state energy in other domains; context is critical.]
  disambiguation: |
    Stagnant Pools must be distinguished from low-amplitude Laminar Channels. A Laminar Channel, however quiet, has high internal Coherence (`Kτ`) relative to its Dissonance (`Γ`), yielding a high Coherence Ratio (`CR`). A Stagnant Pool is defined by the near-zero value of *both* `Kτ` and `Γ`, resulting in a `CR` near zero.
crosslinks:
  near_synonyms: [INFORMATION_DESERT]
  antonyms: [LAMINAR_CHANNELS, TURBULENT_EDDIES]
  prerequisites: [COHERENCE, DISSONANCE, COHERENCE_RATIO]
  downstream_effects: []
license: CC-BY-SA-4.0
---