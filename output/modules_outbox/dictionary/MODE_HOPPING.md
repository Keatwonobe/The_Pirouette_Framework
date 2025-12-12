---
term: "Mode Hopping"
canonical_id: "MODE_HOPPING"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-193"]
---

---
term: Mode Hopping
canonical_id: MODE_HOPPING
symbol:
aliases: []
parents: [DOMA-193]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-193
      lines: "§4"
      snippet: |
        -   **Mode Hopping:** A sudden shift where one set of harmonic peaks fades and another emerges is the definitive sign of a **phase transition**. The system has been forced to find a new, more stable `Ki` to better survive its environment.
  editors: [auto-compiler]
  review_log: []
triad:
  art: |
    A system, under duress, changes its song. The old melody dies, and in the silence, a new one is born, tuned to a harsher reality.
  law: |
    On a Coherence Spectrum, the integral of coherence (`Kτ`) over a frequency band (`Δω₁`) associated with an initial resonant mode (`Ki₁`) must decrease below a noise threshold while the integral of `Kτ` over a new band (`Δω₂`) for a final mode (`Ki₂`) must rise above it within a defined transition time (`Δt`).
  philosophy: |
    Mode Hopping reveals that stability is not static but adaptive. It is the visible evidence of a system's search for a new resonant state—a new identity—in response to overwhelming environmental pressure, demonstrating that survival is an act of creative re-tuning.
pirouette_definition: |
  A diagnostic pattern observed in a Coherence Spectrum, characterized by the rapid decay of a system's dominant set of harmonic peaks (its `Ki` pattern) and the concurrent emergence of a new, distinct set of peaks at different frequencies. This event is the canonical signature of a phase transition, indicating the system has abandoned one resonant state for another in order to maximize its Lagrangian (`𝓛_p`) under changed environmental conditions or internal stress.
operational_definition:
  units: dimensionless
  symbol_table:
    - name: Ki₁
      meaning: Initial Resonant Mode (a set of harmonic frequencies)
      dimensions: dimensionless
      default_range: contextual
    - name: Ki₂
      meaning: Final Resonant Mode (a new set of harmonic frequencies)
      dimensions: dimensionless
      default_range: contextual
    - name: Δt_transition
      meaning: Time duration of the mode hop event
      dimensions: T
      default_range: contextual
  measurement:
    procedures:
      - name: Spectrogrammatic Transition Analysis
        outline: |
          1. Generate a continuous Coherence Spectrum (`Kτ(ω, t)`) for the system under observation using the Harmonic Lens protocol.
          2. Identify the initial dominant harmonic peaks corresponding to mode `Ki₁`.
          3. Track the peak amplitudes over time.
          4. Detect a point where the amplitude of `Ki₁` peaks falls below a signal-to-noise threshold.
          5. Simultaneously, scan for the rise of a new, stable set of harmonic peaks (`Ki₂`) above the threshold.
          6. The interval between the decay of `Ki₁` and the stabilization of `Ki₂` defines the mode hop.
        expected_signals: [Coherence Spectrum showing decaying and rising frequency bands, Time-series data exhibiting a behavioral state change]
        pitfalls: [Misinterpreting harmonic flickering (Coherence Erosion) as a full mode hop, Insufficient temporal resolution blurring the transition]
context_windows:
  - module: DOMA-193
    excerpt: |
      **Mode Hopping:** A sudden shift where one set of harmonic peaks fades and another emerges is the definitive sign of a **phase transition**. The system has been forced to find a new, more stable `Ki` to better survive its environment.
  - module: DOMA-193
    excerpt: |
      The Coherence Spectrum is a rich diagnostic document that maps directly to a system's health... **Flickering or Fading Bands:** A primary `Ki` pattern that wavers in intensity or fades over time is a visual marker of **Coherence Erosion**, indicating the system is struggling to maintain its form against entropic pressure. **Mode Hopping:** A sudden shift where one set of harmonic peaks fades and another emerges is the definitive sign of a **phase transition**.
poetic_connections:
  motifs: [metamorphosis, regime shift, breaking point, re-tuning, catastrophic change]
  evocative_lines:
    - "The system has been forced to find a new, more stable Ki to better survive its environment."
    - "To become its healer, you must be able to read its music."
  association_matrix:
    - [ "PHASE_TRANSITION", 0.9 ]
    - [ "TEMPORAL_PRESSURE", 0.7 ]
    - [ "COHERENCE_EROSION", 0.6 ]
    - [ "LAMINAR_FLOW", -0.8 ]
formal_mappings:
  candidates:
    - target: Laser mode hopping
      domain: AMO
      mapping_kind: conceptual
      equation_hint:
      justification: |
        In laser physics, mode hopping is a discrete jump in the laser's output frequency to a different resonant mode of its optical cavity, often due to thermal drift. The Pirouette term generalizes this concept from an optical to any complex system, treating the jump as a diagnostic signal of a state change driven by pressure.
      references:
        - title: 'Lasers'
          where: 'A. E. Siegman, University Science Books, Chapter 30'
          date: 1986-01-01
      confidence: 0.7
  adopted:
    - target: Tipping Point / Regime Shift
      domain: Complex Systems|Ecology
      mapping_kind: conceptual|operational
      rationale: |
        This is the most direct and broadly applicable mapping. In complex systems theory, a tipping point or regime shift is a critical threshold where a system rapidly shifts from one stable state to another. Mode Hopping is the direct, observable signature of this event on a Coherence Spectrum, making the abstract concept of a tipping point a measurable phenomenon.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "Every true phase transition or regime shift within a system is accompanied by a measurable Mode Hopping event in its Coherence Spectrum."
      domain: phenomenology
      falsifier: "Observing a system undergo a well-established phase transition (e.g., a superconducting transition, a market crash) without a corresponding decay of old harmonic peaks and emergence of new ones in its temporal signature. This would imply the Coherence Spectrum is an incomplete diagnostic tool for fundamental state changes."
      status: proposed
      links: [DOMA-193]
naming_notes:
  collisions: [Laser mode hopping]
  disambiguation: |
    In Pirouette, Mode Hopping is a generalized diagnostic pattern observable in any system's Coherence Spectrum, signifying a fundamental state change. This is distinct from the more specific term in laser physics, which refers to the physical event of a laser jumping between resonant optical modes. The Pirouette term emphasizes the universal *informational signature* of the change.
crosslinks:
  near_synonyms: [PHASE_TRANSITION]
  antonyms: [HARMONIC_STABILITY, LAMINAR_FLOW]
  prerequisites: [COHERENCE_SPECTRUM, TEMPORAL_RESONANCE_KI, COHERENCE_EROSION]
  downstream_effects: []
license: CC-BY-SA-4.0