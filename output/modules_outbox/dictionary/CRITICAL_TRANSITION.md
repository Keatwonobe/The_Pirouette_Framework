---
term: "Critical Transition"
canonical_id: "CRITICAL_TRANSITION"
symbol: ""
aliases: [snap]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-202"]
---

---
term: Critical Transition
canonical_id: CRITICAL_TRANSITION
symbol: N/A
aliases: [snap]
parents: [DOMA-202]
children: [INST-DIAG-001_Transition_Detector]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-202
      snippet: |
        ...reframing transitions from statistical anomalies to non-linear 'snaps' in a system's geometric dynamics. This instrument allows a Weaver to detect and classify the signature of a system unlocking a new state of being...
  editors: [agent:auto-scribe]
  review_log: []
triad:
  art: |
    A system, like a wave, can travel for a lifetime in a stable flow. A critical transition is the single, dramatic moment it reaches a shore where its old form can no longer be sustained, and it breaks.
  law: |
    Under increasing Temporal Pressure (Γ), a system following a stable geodesic will, upon reaching a bifurcation point, non-linearly leap to a new geodesic to maximize its coherence (Kτ). This transition is empirically detectable as a sharp, non-linear change in the system's coherence manifold, measured by kurtosis, fractal dimension, or coherence flux.
  philosophy: |
    Profound change is not a random tremor but a geometric inevitability. By framing transitions as leaps between stable states, we move from reacting to consequences to understanding the shape of change itself, distinguishing the resonance of an ending from that of a beginning.
pirouette_definition: |
  A sudden, non-linear leap of a system from one stable state (geodesic) to another. It is a geometric event in the system's coherence manifold, triggered when mounting Temporal Pressure (Γ) renders the current geodesic untenable, forcing an act of Ki Morphogenesis to find a new, more coherent configuration.
operational_definition:
  units: Dimensionless (event)
  symbol_table:
    - name: Γ
      meaning: Temporal Pressure; the control parameter driving the transition.
      dimensions: T⁻²
      default_range: contextual
    - name: Kτ
      meaning: Coherence; the maximized quantity defining the system's geodesic.
      dimensions: dimensionless
      default_range: [0, 1]
    - name: dKτ/dt
      meaning: Coherence Flux; rate of change of coherence.
      dimensions: T⁻¹
      default_range: contextual
  measurement:
    procedures:
      - name: Transition Signature Classification
        outline: |
          1. **Establish Baseline:** Map the system's normal `Laminar Flow` state to define the geometry and statistical signature of its coherence manifold (e.g., baseline kurtosis, fractal dimension, and dKτ/dt).
          2. **Monitor for Deformation:** Use real-time diagnostics to detect rapid, non-linear deformations in that geometry, which are early warning signs.
          3. **Classify the Snap:** When a deformation exceeds a critical threshold, classify the event by identifying the primary metric undergoing a non-linear shift: Kurtosis (shattering), Fractal Dimension (unfolding), or Coherence Flux (ordering).
        expected_signals: [Sudden spike in Kurtosis, Step-change in Fractal Dimension, Rapid non-linear increase in Coherence Flux (dKτ/dt)]
        pitfalls: [Misinterpreting high-amplitude noise as a precursive signal, Poorly defined baseline leading to false positives, Failure to distinguish between multiple simultaneous transitions.]
context_windows:
  - module: DOMA-202
    excerpt: |
      Every system... follows a geodesic—a path that maximizes its internal coherence (`Kτ`) for the lowest cost against the ambient Temporal Pressure (`Γ`). For long periods, this path is smooth... A critical transition occurs when this geodesic leads to a cliff. Under mounting pressure, the system reaches a bifurcation point where its current `Ki` pattern is no longer a tenable, low-energy solution. To survive... it must leap. It snaps to a new, fundamentally different geodesic.
  - module: DOMA-202
    excerpt: |
      The snap is not a uniform event; it has a character that reveals the forces at play. By observing changes in a system's coherence manifold, we can classify the nature of its transformation... 1. **The Coherence Shockwave (The Shattering):** ...Primary Metric: **Kurtosis**. 2. **Ki Morphogenesis (The Unfolding):** ...Primary Metric: **Fractal Dimension Change**. 3. **Resonant Alignment (The Ordering):** ...Primary Metric: **Coherence Flux (dKτ/dt)**.
poetic_connections:
  motifs: [wave breaking, shattering, unfolding, crystallization, key turning in a lock]
  evocative_lines:
    - "The Moment a Wave Breaks."
    - "Ki is the sound a key makes as it turns in a lock."
    - "...distinguish the sound of a shattering window from a seed pod bursting open..."
  association_matrix:
    - [ "TEMPORAL_PRESSURE", 0.9 ]
    - [ "COHERENCE", 0.8 ]
    - [ "LAMINAR_FLOW", 0.7 ]
    - [ "KI_MORPHOGENESIS", 0.6 ]
formal_mappings:
  candidates:
    - target: Catastrophe theory
      domain: Math
      mapping_kind: conceptual
      justification: |
        Catastrophe theory mathematically describes how continuous changes in underlying parameters (like Γ) can lead to abrupt, discontinuous changes in a system's state. The Pirouette "snap" is a direct conceptual analog to a system crossing a fold or cusp catastrophe.
      references:
        - title: Catastrophe Theory
          where: Thom, R. (1975)
          date: 1975-01-01
      confidence: 0.8
  adopted:
    - target: Bifurcation
      domain: Math (Dynamical Systems)
      mapping_kind: mathematical
      justification: |
        A Critical Transition is the physical manifestation of a system crossing a bifurcation point. The stable geodesic corresponds to a stable attractor (e.g., a fixed point or limit cycle). As the control parameter (Γ) changes, this attractor can lose stability, forcing the system's trajectory to jump to a new, qualitatively different attractor.
      rationale: This is the most direct and operational mathematical analog for a system's qualitative state change driven by a smooth change in a control parameter.
      confidence: 0.95
    - target: Phase Transition
      domain: CM
      mapping_kind: operational
      justification: |
        The "snap" is operationally equivalent to a physical phase transition, where a system undergoes an abrupt change in its macroscopic properties (e.g., liquid to solid). The metrics for classifying the transition (shattering, unfolding, ordering) correspond to different universality classes of phase transitions.
      rationale: This mapping provides a rich physical intuition and connects the Pirouette framework to well-understood phenomena like crystallization and critical opalescence.
      confidence: 0.90
constraints_and_falsifiers:
  claims:
    - statement: "All major endogenous system state changes are preceded by detectable geometric deformations in the system's coherence manifold, such as rising variance/kurtosis or autocorrelation."
      domain: phenomenology
      falsifier: "The discovery of a class of 'bolt from the blue' transitions, where a system snaps to a new state with no precursive signals in its coherence manifold, suggesting a non-geometric or purely exogenous trigger mechanism not accounted for by internal dynamics under pressure."
      status: under-test
      links: [DOMA-202, INST-DIAG-001_Transition_Detector]
naming_notes:
  collisions: []
  disambiguation: |
    A Critical Transition is a discrete, non-linear event that moves a system between two distinct stable states (`Laminar Flow`). It should not be confused with `Coherence Fever`, which is a state of high-dimensional chaos that *can* occur during a transition but is not the transition itself. It is the leap, not the turbulence of the landing.
crosslinks:
  near_synonyms: [BIFURCATION, PHASE_TRANSITION]
  antonyms: [LAMINAR_FLOW]
  prerequisites: [TEMPORAL_PRESSURE, GEODESIC, COHERENCE]
  downstream_effects: [KI_MORPHOGENESIS, COHERENCE_FEVER]
license: CC-BY-SA-4.0
---

# Critical Transition

## Canonical (Pirouette)
A sudden, non-linear leap of a system from one stable state (geodesic) to another. It is a geometric event in the system's coherence manifold, triggered when mounting Temporal Pressure (Γ) renders the current geodesic untenable, forcing an act of Ki Morphogenesis to find a new, more coherent configuration.

## EFT-First Summary
A Critical Transition is the Pirouette Framework's formalization of concepts known in standard physics and mathematics as **phase transitions** and **bifurcations**. The system's stable state is modeled as a trajectory (geodesic) on a coherence manifold, analogous to an attractor in dynamical systems. The control parameter, Temporal Pressure (Γ), drives the system towards a bifurcation point where the existing attractor becomes unstable. The "snap" is the system's rapid, non-linear jump to a new stable attractor, a process directly analogous to a first- or second-order phase transition in condensed matter systems.

## Glossary Links
- See also: [Temporal Pressure](link), [Laminar Flow](link), [Ki Morphogenesis](link)