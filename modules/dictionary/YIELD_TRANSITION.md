---
term: "Yield Transition"
canonical_id: "YIELD_TRANSITION"
symbol: ""
aliases: [Yielding, Plastic Deformation]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-047"]
---

---
term: Yield Transition
canonical_id: YIELD_TRANSITION
symbol: 
aliases: [Yielding, Plastic Deformation]
parents: [DOMA-047]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-047
      lines: "§3"
      snippet: |
        This is plastic deformation: the system finds a new, stable Ki pattern and permanently re-carves its own Wound Channel. The scar from this experience becomes part of its identity. This is the mechanism of learning, adaptation, and trauma.
  editors: [Weaver-Prime]
  review_log: []
triad:
  art: |
    A system under duress is forced to compose a new verse in its song to survive. The Yield Transition is this irreversible act of creation, where the scar becomes the memory of the note that was added. It is the alchemical union of a system with its own damage.
  law: |
    When Coherence Stress on a system exceeds a critical, material-dependent threshold, the system undergoes an irreversible phase transition to a new stable state. This transition permanently alters the system's Wound Channel, resulting in a non-recoverable deformation that persists after the stress is removed.
  philosophy: |
    The Yield Transition is the core mechanism of costly survival, reframing adaptation, learning, and trauma as a single geometric process. It asserts that meaningful change is inseparable from scarring; resilience is not the absence of damage, but the integration of damage into a new, more durable identity.
pirouette_definition: |
  A phase transition in the Pirouette Lagrangian where Coherence Stress forces a system to abandon its original stable state and find a new one by permanently re-carving its Wound Channel. This transition is irreversible, manifesting as a lasting change in the system's geometric and resonant identity, thereby absorbing stress at the cost of its initial form. It is the fundamental process by which a system learns from, and is marked by, its experience.
operational_definition:
  units: The transition is a dimensionless event. The resultant deformation possesses units of the system's primary state variables (e.g., meters, radians, bits). The threshold is measured in units of Coherence Stress.
  symbol_table:
    - name: σ_Y
      meaning: Yield Stress Threshold
      dimensions: "contextual (gradient of Lagrangian)"
      default_range: "system-dependent"
    - name: ε_p
      meaning: Plastic Strain (Permanent Deformation)
      dimensions: "dimensionless or system-dependent"
      default_range: "> 0 post-transition"
  measurement:
    procedures:
      - name: Cyclical Stress-Strain Analysis
        outline: |
          1. Apply a controlled, increasing Coherence Stress (input) to a system while monitoring its geometric response (strain/output).
          2. Periodically reduce the applied stress to zero and measure the residual strain.
          3. The Yield Transition is identified as the lowest stress level at which the residual strain becomes permanently non-zero.
        expected_signals: [Onset of hysteresis in the stress-strain curve, non-zero intercept on the strain axis after a stress cycle.]
        pitfalls: [Strain rate dependency (viscoelastic effects), thermal drift, misidentifying the proportional limit for the true yield point.]
context_windows:
  - module: DOMA-047
    excerpt: |
      The Yield Transition (The Permanent Scar): As stress surpasses a critical threshold, the system reaches the point of no return. Its original state is no longer a viable solution to the Lagrangian. To survive, it is forced into an alchemical union with its own damage. This is plastic deformation: the system finds a new, stable Ki pattern and permanently re-carves its own Wound Channel.
  - module: DOMA-047
    excerpt: |
      Ductility characterizes systems with adaptable, flexible coherence. They can endure significant plastic deformation, absorbing immense stress by scarring their Wound Channel and reconfiguring their internal geometry. They bend, stretch, and change shape, buying survival at the cost of their original form. They fail slowly, gracefully, and with ample warning.
poetic_connections:
  motifs: [scarring, adaptation, bending-not-breaking, forging, memory-of-damage, resilience]
  evocative_lines:
    - "The scar is the memory of the verse that was added to survive."
    - "...an alchemical union with its own damage."
    - "...composing a song so beautiful it can learn to harmonize with its own pain."
  association_matrix:
    - [ "WOUND_CHANNEL", 0.9 ]
    - [ "COHERENCE_STRESS", 0.8 ]
    - [ "FRACTURE", 0.7 ]
    - [ "ELASTIC_DEFORMATION", 0.6 ]
formal_mappings:
  candidates:
    - target: Plastic Deformation / Yield Strength (σ_y)
      domain: CM
      mapping_kind: operational
      equation_hint: |
        For stress σ > σ_y, total strain ε = ε_elastic + ε_plastic, where d(ε_plastic)/dt > 0.
      justification: |
        The Yield Transition is the direct operational and conceptual analogue of plastic deformation in continuum mechanics and materials science. It describes the onset of permanent, non-recoverable deformation in a body subjected to stress beyond its elastic limit. The Pirouette model provides a new causal explanation (re-carving the Wound Channel) for this well-established phenomenon.
      references:
        - title: Mechanical Behavior of Materials
          where: Meyers and Chawla, Chapter 6: Plastic Deformation
          date: 2008-12-21
      confidence: 0.95
  adopted:
    - target: Plastic Deformation
      rationale: The term is a direct re-conceptualization of the established physical phenomenon, providing a deeper, time-first causal model for an identical set of observables.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "All systems capable of learning or adaptation (e.g., neural networks, immune systems) must exhibit a Yield Transition, where a permanent change in structure (e.g., synaptic weights, antibody population) occurs in response to stress exceeding a threshold."
      domain: phenomenology
      falsifier: "The discovery of a system that adapts to high stress without any measurable, permanent structural change. Such a system would need to return perfectly to its pre-stress baseline state after adaptation, implying a purely elastic, non-scarring learning mechanism."
      status: proposed
      links: [DOMA-047]
naming_notes:
  collisions: [Yield (finance), yield (programming generators)]
  disambiguation: |
    In the Pirouette Framework, 'Yield' exclusively refers to the permanent geometric deformation of a system under Coherence Stress, analogous to plastic deformation in materials. It is unrelated to financial returns or programming control flow constructs.
crosslinks:
  near_synonyms: [PLASTIC_DEFORMATION]
  antonyms: [ELASTIC_DEFORMATION, FRACTURE]
  prerequisites: [COHERENCE_STRESS, WOUND_CHANNEL]
  downstream_effects: [BRITTLENESS_DUCTILITY, WORK_HARDENING]
license: CC-BY-SA-4.0
---

# Yield Transition

## Canonical (Pirouette)
A phase transition in the Pirouette Lagrangian where Coherence Stress forces a system to abandon its original stable state and find a new one by permanently re-carving its Wound Channel. This transition is irreversible, manifesting as a lasting change in the system's geometric and resonant identity, thereby absorbing stress at the cost of its initial form. It is the fundamental process by which a system learns from, and is marked by, its experience.

## EFT-First Summary
The Yield Transition is the Pirouette Framework's re-conceptualization of **Plastic Deformation** from classical materials science. It models the onset of permanent, non-recoverable change in a system's state when subjected to stress beyond a critical threshold (the yield strength, σ_y). While classical mechanics describes this as a failure of material bonds, the Pirouette model frames it as a dynamic, adaptive process where the system permanently re-carves its internal geometry (its Wound Channel) to find a new stable configuration, thus surviving the stress.

## Glossary Links
- See also: Wound Channel, Coherence Stress, Elastic Deformation, Fracture