---
term: "Ki_static"
canonical_id: "KI_STATIC"
symbol: ""
aliases: [The Inward Song]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-149"]
---

---
term: Ki_static
canonical_id: KI_STATIC
symbol: `K_{i,static}`
aliases: ["The Inward Song"]
parents: [DOMA-149, CORE-006, CORE-011]
children: []
status: ratified
version: 2.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-149
      lines: "§2"
      snippet: |
        Ki_static (The Inward Song): This is the resonant pattern that maximizes a system's coherence when it is at rest relative to its local environment. It is an internally-focused harmony, optimized for stability and self-reinforcement within the deep "well" of its own static Wound Channel.
  editors: [auto-compiler]
  review_log: []
triad:
  art: |
    The quiet hum of a stone or a sleeping seed. It is the resonance of being perfectly itself, a self-contained world deaf to the call of motion, finding maximal harmony in stillness.
  law: |
    For a system at rest (`v=0`) relative to its local frame, its Temporal Resonance `K_i` converges to the constant `K_{i,static}`. This value quantifies the potential well depth that must be overcome to initiate motion (the activation energy).
  philosophy: |
    Ki_static represents the coherence of pure being, separate from doing. It is the Framework's ground state, the stable foundation against which all dynamics are measured, embodying the principle that stability is a powerful, self-reinforcing attractor.
pirouette_definition: |
  The stable Temporal Resonance pattern (`K_i`) that maximizes the coherence of a system at rest. As a distinct, stable solution to the Pirouette Lagrangian (CORE-006), it is an internally-focused harmony optimized for self-reinforcement within the potential well of its own static Wound Channel (CORE-011). It is the baseline coherence from which the activation energy for motion is calculated.
operational_definition:
  units: Dimensionless
  symbol_table:
    - name: `K_{i,static}`
      meaning: The static Temporal Resonance; the baseline coherence of a system at rest.
      dimensions: Dimensionless
      default_range: Contextual; often normalized in [0, 1]
  measurement:
    procedures:
      - name: Quiescent Resonance Spectroscopy
        outline: |
          1. Isolate the system in a stable, quiescent environment to minimize external perturbations.
          2. Apply a low-amplitude, broad-spectrum coherence probe.
          3. Measure the system's full response spectrum using a Coherence Spectrometer.
          4. `K_{i,static}` is identified as the dominant, narrow resonance peak with the highest Q-factor, corresponding to the ground state. The width of the peak relates to the depth of the Wound Channel well.
        expected_signals: [Dominant, narrow spectral peak, high Q-factor]
        pitfalls: [External vibrations exciting dynamic modes, probe field exceeding activation energy, insufficient signal-to-noise]
context_windows:
  - module: DOMA-149
    excerpt: |
      **Ki_static (The Inward Song):** This is the resonant pattern that maximizes a system's coherence when it is at rest relative to its local environment. It is an internally-focused harmony, optimized for stability and self-reinforcement within the deep "well" of its own static Wound Channel. It minimizes interaction to preserve its form; it is the resonance of being *in a place*.
  - module: DOMA-149
    excerpt: |
      Once in motion, the system actively carves and reinforces a new, dynamic Wound Channel. This new channel makes it energetically favorable to *remain* in motion. The system will only "snap back" to the `Ki_static` state when its velocity drops below a lower critical threshold (`v_c↓`), at which point the attraction of the old, static well finally overcomes the momentum of the new, dynamic channel.
poetic_connections:
  motifs: [stillness, foundation, depth, inertia, self-containment, ground state]
  evocative_lines:
    - "It is the resonance of being *in a place*."
    - "The universe remembers, and motion is the art of convincing the past to let go."
    - "stability is both a comfort and a cage."
  association_matrix:
    - [ "WOUND_CHANNEL_MEMORY", 0.9 ]
    - [ "ACTIVATION_ENERGY", 0.8 ]
    - [ "COHERENCE_DAM", 0.9 ]
formal_mappings:
  candidates:
    - target: Rest Mass (`m_0`)
      domain: SM|GR
      mapping_kind: conceptual
      equation_hint: |
        `E_activation ∝ K_{i,static}` maps to `E_rest = m_0 c^2`
      justification: |
        Rest mass is an intrinsic property that quantifies a particle's inertia at rest. Similarly, `K_{i,static}` is an intrinsic property that quantifies a system's temporal inertia (resistance to state change), which manifests as a required activation energy. Both represent a fundamental barrier to acceleration from a state of rest.
      references: []
      confidence: 0.7
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The activation energy required to transition a system from rest to motion is a monotonically increasing function of its `K_{i,static}` magnitude."
      domain: phenomenology
      falsifier: "Discovering a class of systems where higher `K_{i,static}` correlates with lower activation energy, or where the relationship is non-monotonic."
      status: proposed
      links: [DOMA-149]
naming_notes:
  collisions: []
  disambiguation: |
    Distinct from `Ki_dynamic`, the resonance of motion. `Ki_static` describes the coherence of *being*, measured at `v=0` and defining the depth of the stability well. `Ki_dynamic` describes the coherence of *becoming* or *doing*, a separate stable state accessible only after overcoming the activation energy barrier defined by `Ki_static`.
crosslinks:
  near_synonyms: [GROUND_STATE_COHERENCE]
  antonyms: [KI_DYNAMIC]
  prerequisites: [TEMPORAL_RESONANCE, WOUND_CHANNEL, PIROUETTE_LAGRANGIAN]
  downstream_effects: [INERTIA, ACTIVATION_ENERGY, HYSTERESIS]
license: CC-BY-SA-4.0
---