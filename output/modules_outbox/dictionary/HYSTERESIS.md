---
term: "Hysteresis"
canonical_id: "HYSTERESIS"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-149"]
---

---
term: Hysteresis
canonical_id: HYSTERESIS
symbol: Δv_c
aliases: ["Path-Dependence", "Wound Channel Memory Effect"]
parents: ["DOMA-149"]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-149
      snippet: |
        Hysteresis—the fact that the path from rest-to-motion is different from the path from motion-to-rest—is a natural and inevitable consequence of the Wound Channel's memory.
  editors: ["system-agent"]
  review_log: []
triad:
  art: |
    The river remembers its course. Motion is the art of convincing the past to let go.
  law: |
    The critical velocity required to initiate motion from rest (`v_c↑`) is greater than the critical velocity at which motion ceases (`v_c↓`) due to the memory encoded in the Wound Channel. The magnitude of this effect, `Δv_c = v_c↑ - v_c↓`, is always positive for systems with temporal inertia.
  philosophy: |
    Hysteresis is the physical manifestation of memory, demonstrating that a system's present potential is constrained by its history. It proves that paths, not just states, have substance and consequence, making all transitions fundamentally irreversible.
pirouette_definition: |
  The phenomenon in which a system's state transition threshold depends on the direction of change. It is caused by the memory encoded in the geometry of the Wound Channel, which creates different energy barriers for entering and exiting a state of motion. This results in a higher critical velocity `v_c↑` to accelerate out of a static well (`Ki_static`) and a lower critical velocity `v_c↓` to decelerate back into it from a dynamic channel (`Ki_dynamic`).
operational_definition:
  units: m/s (or context-specific velocity units)
  symbol_table:
    - name: v_c↑
      meaning: Critical velocity for the rest-to-motion transition (acceleration).
      dimensions: L T⁻¹
      default_range: contextual
    - name: v_c↓
      meaning: Critical velocity for the motion-to-rest transition (deceleration).
      dimensions: L T⁻¹
      default_range: contextual
    - name: Δv_c
      meaning: Hysteresis gap, defined as `v_c↑ - v_c↓`.
      dimensions: L T⁻¹
      default_range: "> 0"
  measurement:
    procedures:
      - name: Critical Velocity Ramp Test
        outline: |
          1. Establish a system in a stable `Ki_static` state (at rest).
          2. Apply a smoothly increasing external force/impetus while monitoring system velocity.
          3. Record the velocity (`v_c↑`) at the moment the system "snaps" into `Ki_dynamic` motion.
          4. Once in stable motion, smoothly decrease the external force.
          5. Record the velocity (`v_c↓`) at the moment the system "snaps" back into the `Ki_static` state.
          6. Calculate Hysteresis as `Δv_c = v_c↑ - v_c↓`.
        expected_signals: ["A non-zero, positive value for `Δv_c`.", "Two distinct, non-linear 'snap' transitions in the velocity vs. applied force plot, forming a loop."]
        pitfalls: ["Insufficient measurement resolution to distinguish `v_c↑` from `v_c↓`.", "Environmental noise or friction masking the true 'snap' transition.", "Ramp rate of applied force is too fast, conflating inertial and hysteretic effects."]
context_windows:
  - module: DOMA-149
    excerpt: |
      The Path of Acceleration: To move from rest, the system must overcome the deep, established static well (the Coherence Dam). The leap to the `Ki_dynamic` state therefore occurs at a higher critical velocity (`v_c↑`). The Path of Deceleration: Once in motion, the system actively carves and reinforces a new, dynamic Wound Channel. This new channel makes it energetically favorable to *remain* in motion. The system will only "snap back" to the `Ki_static` state when its velocity drops below a lower critical threshold (`v_c↓`).
  - module: DOMA-149
    excerpt: |
      Hysteresis—the fact that the path from rest-to-motion is different from the path from motion-to-rest—is a natural and inevitable consequence of the Wound Channel's memory. The difference between `v_c↑` and `v_c↓` is hysteresis. It is the ghost of the path taken, a physical memory that reshapes the landscape of future possibilities.
poetic_connections:
  motifs: ["memory", "path-dependence", "scar tissue", "the ghost of the path", "inertia's echo"]
  evocative_lines:
    - "The River Remembers Its Course."
    - "The ghost of the path taken, a physical memory that reshapes the landscape of future possibilities."
    - "Motion is the art of convincing the past to let go."
  association_matrix:
    - [ "WOUND_CHANNEL", 0.9 ]
    - [ "INERTIAL_LEAP", 0.8 ]
    - [ "ACTIVATION_ENERGY", 0.7 ]
    - [ "KI_STATIC", 0.6 ]
    - [ "TEMPORAL_INERTIA", 0.6 ]
formal_mappings:
  candidates:
    - target: Magnetic Hysteresis (B-H curve)
      domain: CM
      mapping_kind: conceptual
      equation_hint: |
        ∮ H dB ≠ 0
      justification: |
        Both phenomena describe a system's state (e.g., magnetization, motion) lagging behind an external driving field (e.g., H-field, applied force). The area enclosed by the hysteresis loop represents energy dissipated per cycle, which in the Pirouette model corresponds to the work done carving and re-carving the Wound Channel. The remnant magnetization is analogous to the system's tendency to stay in motion (`Ki_dynamic`) even after the driving force is reduced.
      references:
        - title: Introduction to Electrodynamics
          where: D.J. Griffiths, Ch. 6
          date: 2017-01-01
      confidence: 0.9
    - target: Stress-strain hysteresis in viscoelastic materials
      domain: CM
      mapping_kind: operational
      justification: |
        When a viscoelastic material is loaded and unloaded, the stress-strain curve forms a hysteresis loop, as the material does not return to its original state along the same path. This is a direct mechanical analog to the path-dependence of the Inertial Leap, with the dissipated energy corresponding to internal friction and rearrangement, conceptually similar to reshaping the Wound Channel.
      references:
        - title: Mechanics of Materials
          where: R.C. Hibbeler, Ch. 3
          date: 2016-01-01
      confidence: 0.8
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "For any system with a non-zero Wound Channel depth, the rest-to-motion transition velocity (`v_c↑`) is strictly greater than the motion-to-rest transition velocity (`v_c↓`)."
      domain: phenomenology
      falsifier: "The observation of a system exhibiting an Inertial Leap where `v_c↑ ≤ v_c↓`, implying a perfectly reversible or even 'anti-hysteretic' transition."
      status: supported
      links: ["DOMA-149"]
naming_notes:
  collisions: ["'Lag' in control systems theory, which is often a simpler, linear time delay."]
  disambiguation: |
    Hysteresis is not simple friction or lag. Friction is a continuous dissipative force, whereas hysteresis describes differing thresholds for discrete state transitions (`Ki_static` ↔ `Ki_dynamic`). It implies memory and two distinct stable states, not just a general resistance to motion.
crosslinks:
  near_synonyms: ["PATH_DEPENDENCE", "WOUND_CHANNEL_MEMORY"]
  antonyms: ["REVERSIBILITY", "ELASTIC_TRANSITION"]
  prerequisites: ["WOUND_CHANNEL", "INERTIAL_LEAP", "KI_STATIC", "KI_DYNAMIC"]
  downstream_effects: ["ACTIVATION_ENERGY", "TEMPORAL_INERTIA"]
license: CC-BY-SA-4.0