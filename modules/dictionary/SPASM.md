---
term: "Spasm"
canonical_id: "SPASM"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-061"]
---

---
term: Spasm
canonical_id: SPASM
symbol: ↯
aliases: [Coherence Collapse, Pressure Break, Γ-Break]
parents: [DOMA-061, CORE-005]
children: [CORE-011]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-061
      lines: "§2"
      snippet: |
        A Quiescent Forge: The external Temporal Pressure (Γ) is low and stable. This is not a crisis moment forcing a chaotic Spasm...
  editors: [anthropic-claude-v3]
  review_log: []
triad:
  art: |
    The string snaps under tension; the dam breaks under flood. A Spasm is not a choice, but the violent shattering of the vessel that could no longer contain its own crisis.
  law: |
    When the rate of increase of Temporal Pressure (dΓ/dt) exceeds a system's maximum rate of coherent adaptation (∂K/∂t), the system undergoes an uncontrolled phase transition into a lower-coherence, higher-entropy state.
  philosophy: |
    A Spasm reveals the absolute limit of resilience. It is a reminder that choice requires poise and time; without them, there is only fracture. It demonstrates that not all change is evolution—some is simply collapse.
pirouette_definition: |
  A Spasm is an uncontrolled, chaotic phase transition of a system into a state of lower coherence and higher entropy. It occurs when a sudden, high-magnitude increase in external Temporal Pressure (Γ) overwhelms the system's internal resonant integrity (Ki), precluding the possibility of an orderly Resonant Inquiry and Fork. Unlike a Fork, which is a poised selection between viable futures, a Spasm is a forced breakdown into a less structured, often fragmented state.
operational_definition:
  units: Dimensionless event count. Trigger condition is measured in units of Temporal Pressure rate (Γ/T).
  symbol_table:
    - name: ↯
      meaning: A Spasm event.
      dimensions: dimensionless
      default_range: N/A (event)
    - name: Γ
      meaning: Temporal Pressure.
      dimensions: Coherence / Time
      default_range: contextual
    - name: K_crit
      meaning: The system's coherence threshold below which integrity is lost.
      dimensions: Coherence
      default_range: contextual
  measurement:
    procedures:
      - name: Spasm Detection via Coherence Flux Monitoring
        outline: |
          Continuously monitor a system's internal coherence (Ki) and the local Temporal Pressure (Γ) using flow diagnostics. A Spasm is inferred when a rapid increase in Γ (dΓ/dt ≫ 0) is immediately followed by a sharp, non-geodesic drop in Ki and a significant, broadband increase in the system's entropic noise floor.
        expected_signals: [Precursor: sharp positive spike in Γ, Event: sharp negative derivative of Ki, Post-event: elevated, disordered power spectrum]
        pitfalls: [Distinguishing from the controlled 'Resonant Loosening' of a Fork. The key differentiator is the high-Γ trigger and the absence of subsequent coherent path selection.]
context_windows:
  - module: DOMA-061
    excerpt: |
      A system does not Fork from a state of chaos, but from a state of poised stability... The external Temporal Pressure (Γ) is low and stable. This is not a crisis moment forcing a chaotic Spasm, but a calm environment that provides the quiet space necessary for the system to hear the subtle echoes of its potential futures.
poetic_connections:
  motifs: [fracture, collapse, breakdown, shattering, overload, crisis]
  evocative_lines:
    - "a crisis moment forcing a chaotic Spasm"
    - "the string snaps under tension"
  association_matrix:
    - [ "Temporal Pressure", 0.9 ]
    - [ "Fork", -0.8 ]
    - [ "Wound Channel", 0.7 ]
    - [ "Coherence", -0.9 ]
formal_mappings:
  candidates:
    - target: Cascading Failure
      domain: Systems Theory
      mapping_kind: operational
      equation_hint: N/A
      justification: |
        In engineering, a cascading failure occurs when a system under stress experiences a component failure that triggers a chain reaction of subsequent failures. A Spasm is the Pirouette equivalent, where overwhelming Temporal Pressure causes an initial coherence break that propagates through the system, leading to a total collapse rather than a controlled adaptation.
      references: []
      confidence: 0.8
    - target: Hagedorn Transition
      domain: SM
      mapping_kind: conceptual
      justification: |
        The Hagedorn temperature represents a point where a hadronic system's partition function diverges, as energy input creates new particles instead of increasing kinetic energy. This mirrors a Spasm, where extreme pressure (energy) causes a system to break down into a 'gas' of lower-coherence components rather than following an ordered path.
      references: []
      confidence: 0.4
  adopted:
    - target: Cascading Failure
      rationale: The mapping is direct and operational, linking Spasm to well-understood phenomena in complex systems analysis and engineering, emphasizing the role of stress thresholds and runaway positive feedback loops.
      confidence: 0.8
constraints_and_falsifiers:
  claims:
    - statement: "A Spasm event always results in a net decrease in the system's integrated future coherence potential (S_p = ∫ 𝓛_p dt) compared to its pre-event state."
      domain: theory
      falsifier: "Observing a system undergoing a Γ-induced chaotic transition that consistently results in a new state with a higher projected coherence integral than a controlled Fork would have achieved from the same initial conditions."
      status: proposed
      links: [DOMA-061, CORE-006]
naming_notes:
  collisions: [The term "spasm" in biology refers to an involuntary muscle contraction. This is a useful, if imprecise, analogy for the uncontrolled nature of the event.]
  disambiguation: |
    A Spasm must be distinguished from the 'Resonant Loosening' stage of a Fork. A Spasm is *forced* by external Γ and is a total breakdown; Resonant Loosening is an *internal, controlled* process in a low-Γ environment that enables a poised choice.
crosslinks:
  near_synonyms: [COHERENCE_COLLAPSE]
  antonyms: [FORK]
  prerequisites: [TEMPORAL_PRESSURE, COHERENCE]
  downstream_effects: [WOUND_CHANNEL, INFORMATION_DESTRUCTION]
license: CC-BY-SA-4.0
---

# Spasm

## Canonical (Pirouette)
A Spasm is an uncontrolled, chaotic phase transition of a system into a state of lower coherence and higher entropy. It occurs when a sudden, high-magnitude increase in external Temporal Pressure (Γ) overwhelms the system's internal resonant integrity (Ki), precluding the possibility of an orderly Resonant Inquiry and Fork. Unlike a Fork, which is a poised selection between viable futures, a Spasm is a forced breakdown into a less structured, often fragmented state.

## EFT-First Summary
Operationally, a Spasm is analogous to a cascading failure in complex systems. When external stress (Temporal Pressure, Γ) exceeds a critical threshold, the system does not adapt but instead undergoes a rapid, uncontrolled phase transition. This results in a fragmented, higher-entropy state, corresponding to a catastrophic loss of system integrity and information.

## Glossary Links
- See also: [[Fork]], [[Temporal Pressure]], [[Coherence]]