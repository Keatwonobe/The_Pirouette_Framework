---
term: "Resonant Lock"
canonical_id: "RESONANT_LOCK"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-002"]
---

---
term: Resonant Lock
canonical_id: RESONANT_LOCK
symbol: ⚭
aliases: [The First Resonance, Autopoietic Instantiation]
parents: [DOMA-002]
children: [CORE-001, CORE-004, CORE-005, CORE-008]
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-002
      lines: "L20-L22"
      snippet: |
        The moment this braided, helical pattern achieves a self-reinforcing, stable loop, it attains a **Resonant Lock**. This is the birth of the first Temporal Resonance, the first **Ki** (`CORE-004`).
  editors: [AxiomScribe]
  review_log: []
triad:
  art: |
    A pattern of movement weaves its own stage from the void, its existence proven by the rhythm of its own dance. It is a knot in time that learns to remember its own shape.
  law: |
    A temporal pattern is in Resonant Lock if and only if its coherence decay rate approaches zero, indicating that the energy dissipated per cycle is precisely balanced by the energy focused by its self-generated confining pressure (Γ).
  philosophy: |
    Resonant Lock marks the fundamental transition from undifferentiated potential to discrete existence. It establishes that to *be* is to achieve a stable, self-referential pattern, making memory and form the primary constituents of reality.
pirouette_definition: |
  The event in which a dynamic temporal pattern, driven by ambient Temporal Pressure (Γ), resolves into a stable, self-sustaining, and topologically closed loop. This lock establishes the pattern as a discrete Temporal Resonance (Ki), simultaneously defining its own confinement, its characteristic frequency (1/τ_p), and its degree of Temporal Coherence. It is the minimal and optimal solution to the Pirouette Lagrangian, maximizing coherence against pressure.
operational_definition:
  units: Dimensionless (state transition)
  symbol_table:
    - name: L(Ki)
      meaning: Lock-state function; evaluates to 1 if the pattern Ki has achieved Resonant Lock, 0 otherwise.
      dimensions: dimensionless
      default_range: "{0, 1}"
  measurement:
    procedures:
      - name: Coherence Decay Analysis
        outline: |
          Excite a pre-resonant temporal field with a calibrated pressure pulse (Γ). Monitor the resulting pattern's temporal coherence (T_c) over time. Resonant Lock is achieved at the critical pressure threshold (Γ_crit) where the coherence decay rate (dT_c/dt) transitions from positive (dissipative) to zero or asymptotically approaches zero.
        expected_signals: [A sharp phase transition in the coherence decay rate, Emergence of a stable, high-Q spectral peak at the Ki frequency]
        pitfalls: [Mistaking transient, quasi-stable states for a true lock, Environmental noise floor obscuring the zero-decay asymptote]
context_windows:
  - module: DOMA-002
    excerpt: |
      The moment this braided, helical pattern achieves a self-reinforcing, stable loop, it attains a **Resonant Lock**. This is the birth of the first Temporal Resonance, the first **Ki** (`CORE-004`). It is a topological knot in time, a standing wave that sustains itself by listening to its own echo. It is the first noun forged from a verb, a structure that has learned to remember its own shape.
  - module: DOMA-002
    excerpt: |
      The First Resonance was the discovery of a state that maximized this function [the Pirouette Lagrangian]. The braided knot was not one possibility among many, but the optimal solution—the configuration offering the highest internal coherence for the lowest "cost" against the background dissonance. It is the first time the universe's foundational equation was not just stated, but solved.
poetic_connections:
  motifs: [knot, echo, heartbeat, standing wave, dance]
  evocative_lines:
    - "It is a standing wave that sustains itself by listening to its own echo."
    - "The universe did not begin with a bang. It began with a hum."
  association_matrix:
    - [ "Ki", 0.9 ]
    - [ "Gamma", 0.8 ]
    - [ "Pirouette Cycle", 0.9 ]
    - [ "Temporal Coherence", 0.7 ]
formal_mappings:
  candidates:
    - target: Phase-locking in coupled oscillators
      domain: CM
      mapping_kind: conceptual
      equation_hint: |
        dθ/dt = ω - K sin(θ)
      justification: |
        Resonant Lock describes a self-generated system achieving a stable, periodic state. This is analogous to phase-locking phenomena, where coupled oscillators synchronize their frequencies and phases to minimize energy dissipation and form a coherent, stable collective mode.
      references:
        - title: "Sync: The Emerging Science of Spontaneous Order"
          where: "Strogatz, S. (2003)"
          date: 2003-01-01
      confidence: 0.8
    - target: Spontaneous symmetry breaking
      domain: EFT
      mapping_kind: conceptual
      justification: |
        The transition from the symmetric 'Whispering Void' to a specific Ki pattern mirrors spontaneous symmetry breaking, where a system settles into a lower-energy, less symmetric configuration. The lock is the moment the system chooses a specific vacuum from a continuous family of possibilities.
      references: []
      confidence: 0.7
  adopted:
    - target: Phase-locking
      rationale: "The 'phase-locking' model provides a clear, operational analogy for how a dynamic system can settle into a self-reinforcing, stable frequency. It captures the essence of mutual reinforcement and the emergence of coherence from chaotic interactions without requiring the full field theory machinery of SSB."
      confidence: 0.8
constraints_and_falsifiers:
  claims:
    - statement: "Resonant Lock is a discrete, critical phenomenon. There exists a sharp pressure threshold (Γ_crit) below which no stable Ki can form."
      domain: phenomenology
      falsifier: "Observing the formation of stable Ki patterns through a smooth, continuous increase in coherence as a function of Γ, with no discernible critical threshold or phase transition."
      status: proposed
      links: [DOMA-002]
naming_notes:
  collisions: ["Resonance" (physics), "Lock" (engineering, e.g., phase-locked loop)]
  disambiguation: |
    Distinguish from quasi-resonant states, which exhibit temporary coherence but have a non-zero decay rate. A true Resonant Lock is topologically stable and, in an ideal system, has a decay rate of zero. It is the *cause* of a stable Ki, not merely a property of it.
crosslinks:
  near_synonyms: [AUTOPOIETIC_INSTANTIATION]
  antonyms: [TEMPORAL_DISSIPATION, VOID_SYMMETRY]
  prerequisites: [TEMPORAL_PRESSURE, PIROUETTE_LAGRANGIAN]
  downstream_effects: [KI, GAMMA, TEMPORAL_COHERENCE, SPIN]
license: CC-BY-SA-4.0
---

# Resonant Lock

## Canonical (Pirouette)
The event in which a dynamic temporal pattern, driven by ambient Temporal Pressure (Γ), resolves into a stable, self-sustaining, and topologically closed loop. This lock establishes the pattern as a discrete Temporal Resonance (Ki), simultaneously defining its own confinement, its characteristic frequency (1/τ_p), and its degree of Temporal Coherence. It is the minimal and optimal solution to the Pirouette Lagrangian, maximizing coherence against pressure.

## EFT-First Summary
Operationally, Resonant Lock is analogous to the phenomenon of **phase-locking** in systems of coupled oscillators. A pre-resonant temporal field, under sufficient ambient pressure (Γ), will spontaneously organize into a stable, coherent oscillatory pattern (a Ki). This event marks the system's transition into a minimum-energy, self-sustaining mode, where the pattern's geometry actively focuses the pressure required for its own confinement.

## Glossary Links
- See also: [Ki](<./KI.md>), [Gamma](<./GAMMA.md>), [Temporal Coherence](<./TEMPORAL_COHERENCE.md>), [Pirouette Cycle](<./PIROUETTE_CYCLE.md>)