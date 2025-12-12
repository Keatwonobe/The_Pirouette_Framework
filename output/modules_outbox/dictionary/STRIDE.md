---
term: "Stride"
canonical_id: "STRIDE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-184"]
---

---
term: Stride
canonical_id: STRIDE
symbol: 
aliases: []
parents: [DOMA-184]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-184
      snippet: |
        A single stride consists of two synchronized phases:
        1.  **The Grip (Anchoring the Past):** The skater momentarily and intensely increases its internal coherence (`K_τ`), "sharpening the blade" of its being.
        2.  **The Glide (Opening the Future):** Simultaneously, the skater projects a resonant field to shape the ambient Temporal Pressure (`V_Γ`).
  editors: [autodidact-scribe]
  review_log: []
triad:
  art: |
    The Stride is the heartbeat of motion, a rhythmic pulse of sharpening and softening the self. It is the skater's two-step dance with spacetime, gripping the past to leap into an invited future.
  law: |
    A Stride is a complete, asymmetric cycle of internal coherence modulation (`K_τ`) and external field shaping (`V_Γ`) that generates a net displacement along a self-induced gradient in the local Lagrangian. The displacement per Stride is zero if the cycle is symmetric or fails to overcome local temporal pressure.
  philosophy: |
    Motion is not a brute-force act but a conversation. The Stride embodies this, demonstrating that progress arises from a rhythmic, intelligent modulation of self in relation to the world, creating the conditions for graceful "falling" rather than effortful pushing.
pirouette_definition: |
  The fundamental, rhythmic cycle of action that enables Geodesic Skating. A Stride is composed of two coordinated, asymmetric phases: the **Grip**, a momentary increase in internal coherence (`K_τ`) to establish a high-inertia pivot point, and the **Glide**, a simultaneous shaping of the external temporal pressure field (`V_Γ`) to create a low-pressure trough in the direction of motion, into which the entity 'falls'.
operational_definition:
  units: process cycle
  symbol_table:
    - name: K_τ
      meaning: Internal Coherence
      dimensions: Action⁻¹
      default_range: contextual
    - name: V_Γ
      meaning: Temporal Pressure Potential
      dimensions: M L² T⁻³
      default_range: contextual
    - name: Δt_Grip
      meaning: Duration of the Grip phase
      dimensions: T
      default_range: contextual
    - name: Δt_Glide
      meaning: Duration of the Glide phase
      dimensions: T
      default_range: contextual
  measurement:
    procedures:
      - name: Stride Phase Analysis
        outline: |
          Monitor an entity's Wound Channel (`CORE-011`) and its internal coherence field simultaneously. A Stride is identified as a periodic, correlated oscillation in both signals. The Grip phase corresponds to a sharp, localized spike in internal coherence and a deepening of the Wound Channel's anchor point. The Glide phase is marked by a forward-propagating wave of low temporal pressure and a corresponding relaxation of internal coherence as the entity moves.
        expected_signals: [Periodic spike train in `K_τ`, Propagating dipole in `V_Γ`, Sawtooth pattern in displacement]
        pitfalls: [Distinguishing a true Stride from ambient fluctuations (Stagnant Skate), Misinterpreting inefficient, high-frequency oscillations of a Turbulent Skate as multiple distinct Strides.]
context_windows:
  - module: DOMA-184
    excerpt: |
      A skater is any entity capable of asymmetrically modulating its own internal state. This act of modulation is a stride, a rhythmic cycle that creates a propulsive gradient on the coherence manifold. A single stride consists of two synchronized phases: The Grip (Anchoring the Past) and The Glide (Opening the Future).
  - module: DOMA-184
    excerpt: |
      The state of flow is determined by the harmony between the skater's internal rhythm and the properties of the external medium... In a Laminar Skate, the stride is clean, the wake is minimal, and coherence is maximized... In a Turbulent Skate, each stride fights the remnants of the last.
poetic_connections:
  motifs: [rhythm, breath, heartbeat, falling with grace, sculpting, two-step]
  evocative_lines:
    - "...to grip with integrity and glide with grace."
    - "The skater does not generate force; it creates a slope and then gracefully falls along it."
  association_matrix:
    - [ "Grip", 0.9 ]
    - [ "Glide", 0.9 ]
    - [ "Geodesic Skate", 0.8 ]
    - [ "Rhythm", 0.7 ]
    - [ "Coherence", 0.6 ]
formal_mappings:
  candidates:
    - target: Gait cycle (stance phase + swing phase)
      domain: CM
      mapping_kind: conceptual
      justification: |
        The Stride's Grip/Glide phases are analogous to the stance/swing phases of a walking gait. The 'Grip' provides a stable anchor point (like a foot on the ground) from which the 'Glide' (the swinging leg and body) generates forward motion. Both are rhythmic, asymmetric cycles for propulsion.
      references: []
      confidence: 0.8
    - target: Tacking (sailing)
      domain: CM
      mapping_kind: conceptual
      justification: |
        Like a sailboat tacking, a Stride manipulates its interaction with a background field (wind/temporal pressure) to generate motion. The keel provides the 'Grip' (resisting lateral motion) while the sails create the pressure differential for the 'Glide'.
      references: []
      confidence: 0.7
  adopted:
    - target: Gait cycle (stance phase + swing phase)
      rationale: This is the most direct analogy for a self-propelled entity's cyclic action, mapping the two phases of motion generation onto the two phases of the Stride.
      confidence: 0.8
constraints_and_falsifiers:
  claims:
    - statement: "All forms of self-propulsion via Geodesic Skating are reducible to a sequence of discrete, asymmetric Stride cycles."
      domain: theory
      falsifier: "Discovery of a smooth, continuous, non-cyclic form of Geodesic Skating where no distinct Grip/Glide phases can be identified, yet propulsion occurs. This would imply an alternative to the Stride mechanism, possibly a standing wave of coherence."
      status: proposed
      links: [DOMA-184]
naming_notes:
  collisions: [Stride in computer science (memory access patterns)]
  disambiguation: |
    In the Pirouette Framework, Stride refers exclusively to the two-phase cycle of Grip and Glide for propulsion. It is a dynamic process, not a static distance or memory offset as in computing.
crosslinks:
  near_synonyms: []
  antonyms: [STAGNATION]
  prerequisites: [COHERENCE, TEMPORAL_PRESSURE, GEODESIC_SKATE]
  downstream_effects: [WOUND_CHANNEL, FLOW_STATE]
license: CC-BY-SA-4.0
---

# Stride

## Canonical (Pirouette)
The fundamental, rhythmic cycle of action that enables Geodesic Skating. A Stride is composed of two coordinated, asymmetric phases: the **Grip**, a momentary increase in internal coherence (`K_τ`) to establish a high-inertia pivot point, and the **Glide**, a simultaneous shaping of the external temporal pressure field (`V_Γ`) to create a low-pressure trough in the direction of motion, into which the entity 'falls'.

## EFT-First Summary
In analogy to classical biomechanics, a Stride can be modeled as a gait cycle. The Grip phase acts as the 'stance phase,' establishing a high-inertia anchor by momentarily increasing the entity's "mass" or self-coupling (`K_τ`). The Glide phase mirrors the 'swing phase,' where the entity moves forward by creating a local pressure differential (`V_Γ`), effectively falling into a self-generated potential well. The efficiency of motion is determined by the synchronization and asymmetry of these two phases.

## Glossary Links
- See also: Geodesic Skate, Grip, Glide, Flow State