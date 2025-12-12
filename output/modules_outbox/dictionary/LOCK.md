---
term: "Lock"
canonical_id: "LOCK"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-046"]
---

---
term: Lock
canonical_id: LOCK
symbol: N/A
aliases: [Stagnant Flow, Crystal Prison]
parents: [DOMA-046]
children: [INST-DIAG-LOCK]
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-046
      snippet: |
        Lock is the paradox of perfection. A system becomes so successful at maximizing its coherence that its Wound Channel carves an impossibly deep and narrow canyon. It achieves a state of perfect, frictionless flow but sacrifices all ability to adapt.
  editors: [Agent-LLM]
  review_log: []
triad:
  art: |
    A flawless crystal, beautiful and unchanging, shatters at the first tremor. The river freezes into a perfect sculpture of ice, its flow stilled forever. It is the fortress that cannot bend and is therefore doomed to break.
  law: |
    A system is in Lock when its coherence (`K_τ`) reaches a maximal, stable value (`∂K_τ/∂t → 0`) while its adaptive capacity, measured by its response to external perturbation (`δK_τ/δV_Γ`), approaches zero. The system's geodesic is trapped in a deep, narrow local potential minimum of the Pirouette Lagrangian.
  philosophy: |
    Lock demonstrates that maximal stability is not equivalent to health. By eliminating all internal friction and variation, a system loses the degrees of freedom necessary for adaptation, trading long-term resilience for a brittle, temporary perfection. True viability requires a dynamic balance between order and chaos, not the complete exorcism of it.
pirouette_definition: |
  A pathological state of decoherence characterized by hyper-stability and adaptive rigidity. Lock occurs when a system optimizes its internal coherence (`K_τ`) to such a degree that its evolutionary path (geodesic) becomes a deeply carved, inflexible channel. Trapped by its own success in a deep local maximum of the Pirouette Lagrangian, the system loses its ability to respond to changing environmental pressures (`V_Γ`), becoming a "crystal prison" awaiting Fracture.
operational_definition:
  units: Dimensionless state classifier
  symbol_table:
    - name: K_τ
      meaning: Systemic Coherence (over time)
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: V_Γ
      meaning: Environmental Cost / Temporal Pressure
      dimensions: Action⁻¹ (inverse of Action)
      default_range: contextual
    - name: S_p
      meaning: Pirouette Action
      dimensions: Action
      default_range: contextual
  measurement:
    procedures:
      - name: Adaptive Response Test (ART)
        outline: |
          1. Establish a baseline coherence `K_τ` for the system.
          2. Introduce a controlled, low-magnitude perturbation (a probe `δV_Γ`).
          3. Measure the system's response `δK_τ` and its relaxation time `τ_relax`.
          A system in Lock exhibits a near-zero `δK_τ` (high resistance to change) and a very fast `τ_relax` to its original state, indicating no learning or adaptation has occurred.
        expected_signals: [Response rigidity (δK_τ / δV_Γ → 0), Invariant internal structure post-perturbation]
        pitfalls: [Confusing Lock with high resilience (Rebound potential), Perturbation being large enough to cause Fracture instead of probing]
context_windows:
  - module: DOMA-046
    excerpt: |
      **Lock** | **Stagnant Flow** (Frozen Laminar) | Coherence (`K_τ`) becomes pathologically high and rigid. The geodesic narrows into an inflexible, deeply carved "rut." | A "crystal prison." The system is hyper-stable but loses all adaptability, awaiting fracture.
  - module: DOMA-046
    excerpt: |
      Lock is the paradox of perfection. A system becomes so successful at maximizing its coherence that its Wound Channel carves an impossibly deep and narrow canyon. It achieves a state of perfect, frictionless flow but sacrifices all ability to adapt. The river freezes into a flawless sculpture of ice. It has maximized stability at the cost of all adaptability, becoming a memory crystal incapable of learning or responding to a changing landscape.
poetic_connections:
  motifs: [crystal, ice, fortress, dogma, stagnation, perfection, brittleness]
  evocative_lines:
    - "The new framework teaches us that the crystal is already dead."
    - "True mastery is not to find a single, perfect path and never stray, for that is the path of the crystal, the path of death-in-life."
  association_matrix:
    - [ "FRACTURE", 0.8 ]
    - [ "COHERENCE", 0.7 ]
    - [ "WOUND_CHANNEL", 0.6 ]
    - [ "REBOUND", -0.9 ]
formal_mappings:
  candidates:
    - target: Overfitting
      domain: Math
      mapping_kind: conceptual
      justification: |
        An overfitted machine learning model performs perfectly on its training data (high `K_τ` in a specific context) but fails to generalize to new, unseen data (zero adaptability to `δV_Γ`). The 'deep, narrow canyon' of Lock is analogous to the model's loss landscape becoming sharply peaked around the training set's minimum, preventing it from finding a more generalizable, broader minimum.
      confidence: 0.8
    - target: Glass transition
      domain: CM
      mapping_kind: conceptual
      justification: |
        Similar to a supercooled liquid freezing into an amorphous solid (glass), the system's components become kinetically trapped in a disordered but rigid state. This is a state of high local stability that prevents the system from reaching a more globally optimal state (like a crystal lattice), mirroring Lock's rigid but non-optimal nature.
      confidence: 0.7
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "A system in a Lock state will exhibit a lower mean time to failure (MTTF) under a stochastically changing environment (`dΓ/dt > 0`) than a system with slightly lower but more plastic coherence."
      domain: phenomenology
      falsifier: "Observing a hyper-stable (Locked) system that consistently out-survives a more adaptable system across a wide range of environmental change profiles. This would imply that maximum rigidity is a superior long-term strategy, contradicting the core premise of Lock as a pathology."
      status: proposed
      links: [DOMA-046]
naming_notes:
  collisions: []
  disambiguation: |
    Lock should not be confused with stable Laminar Flow. Laminar Flow navigates its geodesic efficiently but retains the capacity to adapt its path. Lock has lost this capacity; its geodesic has become a prison. The key diagnostic difference is the response to perturbation: a system in Laminar Flow adapts, a system in Lock resists or fractures.
crosslinks:
  near_synonyms: [STAGNANT_FLOW]
  antonyms: [REBOUND, DRIFT]
  prerequisites: [COHERENCE, WOUND_CHANNEL]
  downstream_effects: [FRACTURE]
license: CC-BY-SA-4.0
---