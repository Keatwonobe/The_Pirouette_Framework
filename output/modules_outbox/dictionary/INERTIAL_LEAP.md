---
term: "Inertial Leap"
canonical_id: "INERTIAL_LEAP"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-149"]
---

---
term: Inertial Leap
canonical_id: INERTIAL_LEAP
symbol: 
aliases: [snap, state snap]
parents: [CORE-004, CORE-006, CORE-011, DYNA-001]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-149
      lines: "L12-14"
      snippet: |
        The Inertial Leap is not a change *in* a parameter, but a phase transition *between* two stable harmonies. This leap is governed by the inertia of a system's own history, a memory physically encoded in the geometry of its Wound Channel.
  editors: [System Agent]
  review_log: []
triad:
  art: |
    To change is not merely to move, but to become. Every new state of being must first overcome the ghost of what was.
  law: |
    The transition from a static (`Ki_static`) to a dynamic (`Ki_dynamic`) state is a hysteretic, non-linear phase transition occurring at a critical velocity `v_c`. The energy required for this transition (activation energy) and the hysteresis loop (`v_c↑` > `v_c↓`) are determined by the geometry of the system's Wound Channel.
  philosophy: |
    The Inertial Leap reframes inertia not as a property of mass, but as the memory of a system's history. It demonstrates that states of being (e.g., rest vs. motion) are distinct, stable solutions to maximizing coherence, where stability is a self-reinforced 'well' that must be energetically overcome to permit change.
pirouette_definition: |
  The Inertial Leap is the non-linear, hysteretic phase transition between a system's two primary coherence solutions: the stable, internally-focused `Ki_static` (rest) and the propagating, externally-focused `Ki_dynamic` (motion). This transition is not a smooth interpolation but a discrete jump over an activation energy barrier (the 'Coherence Dam') created by the system's own history as encoded in its Wound Channel.
operational_definition:
  units: The transition is characterized by a critical velocity `v_c` (m/s) and an activation energy `P_inertia` (J).
  symbol_table:
    - name: Ki_static
      meaning: The system's Temporal Resonance pattern at rest.
      dimensions: Contextual (often dimensionless or frequency-based).
      default_range: contextual
    - name: Ki_dynamic
      meaning: The system's Temporal Resonance pattern in motion.
      dimensions: Contextual (often dimensionless or frequency-based).
      default_range: contextual
    - name: v_c↑
      meaning: Critical velocity to initiate the leap from static to dynamic.
      dimensions: L T⁻¹
      default_range: >0
    - name: v_c↓
      meaning: Critical velocity to snap back from dynamic to static.
      dimensions: L T⁻¹
      default_range: 0 to v_c↑
    - name: P_inertia
      meaning: Perturbation term for the activation energy barrier.
      dimensions: M L² T⁻²
      default_range: >0, non-zero only during initial acceleration from v=0.
  measurement:
    procedures:
      - name: Hysteresis Loop Spectroscopy
        outline: |
          1. Start with the system in a stable, static state (`v=0`).
          2. Apply a slowly increasing driving force while monitoring system velocity (`v`) and coherence pattern (`Ki`).
          3. Record the velocity `v_c↑` at which `Ki` abruptly transitions from `Ki_static` to `Ki_dynamic`.
          4. Once in a stable dynamic state, slowly decrease the driving force.
          5. Record the velocity `v_c↓` at which `Ki` abruptly snaps back to `Ki_static`.
          6. The difference `v_c↑ - v_c↓` quantifies the hysteresis.
        expected_signals: [A sharp discontinuity in the `Ki` vs. `v` plot at two distinct points, forming a loop.]
        pitfalls: [Driving force ramp is too fast, overshooting `v_c` and blurring the transition. Environmental noise prematurely triggering the leap.]
context_windows:
  - module: DOMA-149
    excerpt: |
      A system at rest has, over time, carved a deep and stable "well" for itself in the coherence manifold. This geometric indentation acts as a **Coherence Dam**: a potential well that creates a powerful inertia. To initiate motion, the system must be supplied with enough energy to "climb out" of this self-made well and begin carving a new, dynamic channel. This required energy is the physical basis for **activation energy**.
  - module: DOMA-149
    excerpt: |
      Hysteresis—the fact that the path from rest-to-motion is different from the path from motion-to-rest—is a natural and inevitable consequence of the Wound Channel's memory. To move from rest, the system must overcome the deep, established static well... The leap to the `Ki_dynamic` state therefore occurs at a higher critical velocity (`v_c↑`).
poetic_connections:
  motifs: [inertia as memory, motion as forgetting, stability as a cage, hysteresis as a ghost]
  evocative_lines:
    - "motion is the art of convincing the past to let go."
    - "stability is both a comfort and a cage."
  association_matrix:
    - [ "WOUND_CHANNEL", 0.9 ]
    - [ "HYSTERESIS", 0.8 ]
    - [ "ACTIVATION_ENERGY", 0.8 ]
    - [ "COHERENCE", 0.5 ]
formal_mappings:
  candidates:
    - target: First-order phase transition
      domain: Thermodynamics
      mapping_kind: conceptual
      justification: |
        The leap is modeled as a discontinuous jump between two distinct, stable states (`Ki_static`, `Ki_dynamic`), separated by an energy barrier. This is analogous to transitions like boiling or melting, which can exhibit hysteresis (superheating/supercooling) and require latent heat (activation energy).
      confidence: 0.7
    - target: Activation Energy (E_a)
      domain: Chemistry
      mapping_kind: conceptual
      justification: |
        The "Coherence Dam" is explicitly framed as an energy barrier that must be overcome for a state change to occur. This directly maps to the concept of activation energy in chemical reactions, which governs the rate of transition between reactant and product states.
      confidence: 0.9
  adopted:
    - target: Static vs. Kinetic Friction (μ_s > μ_k)
      domain: CM
      mapping_kind: operational
      rationale: |
        This is the most direct and mechanically observable analogue. The greater force required to start an object moving (overcoming static friction, `μ_s`) versus keeping it moving (kinetic friction, `μ_k`) perfectly models the hysteretic leap. `P_inertia` maps to the work done against static friction, `v_c↑` is the point where applied force overcomes `F_s,max`, and the lower `v_c↓` reflects the drop to the kinetic friction regime.
      confidence: 0.85
constraints_and_falsifiers:
  claims:
    - statement: "Systems with deeper or older static Wound Channels will exhibit a larger hysteresis loop (greater difference between `v_c↑` and `v_c↓`) and require a higher activation energy (`P_inertia`) to initiate motion."
      domain: phenomenology
      falsifier: "Observation of a system where a longer time at rest leads to a smaller activation energy, or if the transition is always smooth and non-hysteretic (`v_c↑ = v_c↓`) regardless of system history."
      status: proposed
      links: [DOMA-149]
naming_notes:
  collisions: []
  disambiguation: |
    The Inertial Leap is not acceleration itself, but the discrete state-change that *enables* sustained dynamic motion. It should be distinguished from the continuous change in velocity governed by standard dynamics *after* the leap has occurred. It is the "un-sticking" event, not the subsequent slide.
crosslinks:
  near_synonyms: [ACTIVATION_EVENT, STATE_SNAP]
  antonyms: [ADIABATIC_TRANSITION, SMOOTH_ACCELERATION]
  prerequisites: [WOUND_CHANNEL, KI, PIROUETTE_LAGRANGIAN]
  downstream_effects: [HYSTERESIS, TEMPORAL_INERTIA]
license: CC-BY-SA-4.0
---

# Inertial Leap

## Canonical (Pirouette)
The Inertial Leap is the non-linear, hysteretic phase transition between a system's two primary coherence solutions: the stable, internally-focused `Ki_static` (rest) and the propagating, externally-focused `Ki_dynamic` (motion). This transition is not a smooth interpolation but a discrete jump over an activation energy barrier (the 'Coherence Dam') created by the system's own history as encoded in its Wound Channel.

## EFT-First Summary
In classical mechanics, the Inertial Leap is operationally analogous to the transition from static to kinetic friction. The higher activation energy required to initiate motion mirrors the static friction coefficient (`μ_s`) being greater than the kinetic friction coefficient (`μ_k`), resulting in a measurable hysteresis loop. This phenomenon arises from the system overcoming a potential energy barrier to transition between two stable states (rest vs. uniform motion).

## Glossary Links
- See also: [WOUND_CHANNEL](...), [KI](...), [HYSTERESIS](...)