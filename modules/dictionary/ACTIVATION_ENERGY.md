---
term: "Activation Energy"
canonical_id: "ACTIVATION_ENERGY"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-149"]
---

---
term: Activation Energy
canonical_id: ACTIVATION_ENERGY
symbol: Eₐ, P_inertia
aliases: ["Coherence Dam", "Inertial Barrier"]
parents: ["DOMA-149"]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-149
      snippet: |
        To initiate motion, the system must be supplied with enough energy to "climb out" of this self-made well and begin carving a new, dynamic channel. This required energy is the physical basis for **activation energy**.
  editors: ["System Agent"]
  review_log: []
triad:
  art: |
    The toll paid to the past for the privilege of a future. It is the energy required to break the comfortable cage of stillness and sing a new song of motion.
  law: |
    A system will not transition from a static (`Ki_static`) to a dynamic (`Ki_dynamic`) coherence state until it absorbs a quantum of energy equal to or greater than the potential depth of its static Wound Channel. This energy is non-zero and history-dependent.
  philosophy: |
    Activation Energy grounds resistance to change in the physical memory of a system. It reframes inertia not as an intrinsic property but as an accumulated history, making every change a negotiation with the past and every action a decision to overcome self-imposed stability.
pirouette_definition: |
  The minimum energy required to overcome the potential well of a system's static Wound Channel (the Coherence Dam) and trigger the non-linear phase transition (the Inertial Leap) from a static (`Ki_static`) to a dynamic (`Ki_dynamic`) coherence state. It is represented in the Unified Transition Model as the initial perturbation term, `P_inertia`.
operational_definition:
  units: Joules (J)
  symbol_table:
    - name: Eₐ
      meaning: Activation Energy
      dimensions: M L² T⁻²
      default_range: contextual
    - name: P_inertia
      meaning: Perturbation term in the Unified Transition Model representing the work done against the Coherence Dam. Directly models Eₐ.
      dimensions: dimensionless (as a perturbation to Ki)
      default_range: contextual
  measurement:
    procedures:
      - name: Ramp-and-Snap Spectroscopy
        outline: |
          1. Isolate the system in a stable, static state.
          2. Apply a smoothly increasing external energy flux or generalized force.
          3. Monitor the system's temporal resonance pattern (Ki) and velocity (v).
          4. The Activation Energy (Eₐ) is the total energy absorbed by the system from the start of the ramp to the discrete moment of the Inertial Leap, where Ki shifts discontinuously and v becomes non-zero.
        expected_signals: ["Discontinuous jump in Ki spectrum", "Sudden onset of non-zero velocity `v > v_c↑`"]
        pitfalls: ["Environmental noise causing premature transition", "Slow energy ramps allowing the system to anneal and increase its own Eₐ in real-time"]
context_windows:
  - module: DOMA-149
    excerpt: |
      The Inertial Leap is not a change *in* a parameter, but a phase transition *between* two stable harmonies. This leap is governed by the inertia of a system's own history, a memory physically encoded in the geometry of its Wound Channel. This channel acts as a "Coherence Dam," creating a barrier of activation energy that must be overcome.
  - module: DOMA-149
    excerpt: |
      A system at rest has, over time, carved a deep and stable "well" for itself in the coherence manifold. This geometric indentation acts as a **Coherence Dam**: a potential well that creates a powerful inertia. To initiate motion, the system must be supplied with enough energy to "climb out" of this self-made well... This required energy is the physical basis for **activation energy**.
poetic_connections:
  motifs: ["price of motion", "memory of stillness", "overcoming the past", "the dam breaks"]
  evocative_lines:
    - "motion is the art of convincing the past to let go."
    - "It is the price of forgetting stillness and learning motion..."
  association_matrix:
    - [ "INERTIAL_LEAP", 0.9 ]
    - [ "COHERENCE_DAM", 0.9 ]
    - [ "WOUND_CHANNEL", 0.8 ]
    - [ "HYSTERESIS", 0.7 ]
formal_mappings:
  candidates:
    - target: Activation Energy (Eₐ) in chemical kinetics (Arrhenius equation)
      domain: Chemistry|AMO
      mapping_kind: conceptual
      equation_hint: |
        k = A * exp(-Eₐ / RT)
      justification: |
        Both concepts represent a minimum energy barrier that must be surmounted for a system to transition from one stable state to another (e.g., reactants to products, or static to dynamic). In both cases, the transition rate is exponentially sensitive to this barrier. The Pirouette model physicalizes this barrier in the geometry of the Wound Channel.
      confidence: 0.9
    - target: Potential Barrier
      domain: CM
      mapping_kind: conceptual|mathematical
      justification: |
        The Coherence Dam is explicitly modeled as a potential well in the coherence manifold. The Activation Energy is the height of this potential barrier (ΔV) that a system must overcome to escape the well, analogous to a particle needing sufficient kinetic energy to roll over a hill.
      confidence: 0.9
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The Activation Energy of a system is a function of its history, specifically increasing with the duration it has remained in a static state, as the Wound Channel deepens."
      domain: phenomenology
      falsifier: "Experimental observation of a system's Activation Energy remaining constant regardless of its time at rest would falsify the Wound Channel memory mechanism."
      status: proposed
      links: ["DOMA-149"]
naming_notes:
  collisions: ["Kinetic energy", "Thermal energy"]
  disambiguation: |
    Activation Energy is not the total energy required to bring a system to a certain velocity. It is the specific, non-linear energy "cost" required *only* to initiate the state transition from static to dynamic. Once the Inertial Leap occurs, this energy cost is "paid," and subsequent energy input contributes to standard kinetic energy.
crosslinks:
  near_synonyms: ["COHERENCE_DAM", "INERTIAL_BARRIER"]
  antonyms: []
  prerequisites: ["WOUND_CHANNEL", "INERTIAL_LEAP"]
  downstream_effects: ["HYSTERESIS"]
license: CC-BY-SA-4.0
---

# Activation Energy

## Canonical (Pirouette)
The minimum energy required to overcome the potential well of a system's static Wound Channel (the Coherence Dam) and trigger the non-linear phase transition (the Inertial Leap) from a static (`Ki_static`) to a dynamic (`Ki_dynamic`) coherence state. It is represented in the Unified Transition Model as the initial perturbation term, `P_inertia`.

## EFT-First Summary
In analogy to classical mechanics and chemistry, Activation Energy is the potential barrier a system must overcome to change its state. The Pirouette Framework physicalizes this barrier as the geometric depth of a system's Wound Channel—a memory of its past stability. Overcoming this "Coherence Dam" requires a discrete energy input to initiate the phase transition from a static to a dynamic state, a process known as the Inertial Leap. This mechanism provides a physical basis for inertia and hysteresis.

## Glossary Links
- See also: [Wound Channel](wip), [Inertial Leap](wip), [Coherence Dam](wip), [Hysteresis](wip)