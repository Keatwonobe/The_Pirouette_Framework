---
term: "Ki_rest"
canonical_id: "KI_REST"
symbol: "K_i,rest"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-023"]
---

---
term: Ki_rest
canonical_id: KI_REST
symbol: K_i,rest
aliases: []
parents: [MATH-023]
children: [COSMO-Γ-DE-TAILS, DYNA-001, PPS-002]
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-023
      lines: "§8"
      snippet: |
        | Ki_rest | 4π manifold | π + 1 ≈ 4.14159 | Low-energy, unlocked topology |
  editors: [chain-of-thought-agent]
  review_log: []
triad:
  art: |
    The universe's quiet hum, a topological spring coiled but at ease. It is the memory of motion held in stillness, the silent tempo before the beat drops.
  law: |
    In the zero-velocity limit (v→0), the effective Ki constant converges to the fundamental value K_i,rest = π + 1 ≈ 4.14159. This value represents the ground-state phase coherence rate in the unlocked 4π manifold.
  philosophy: |
    Ki_rest is the geometric ground state of coherence, the universe's default tempo before motion forces a change in rhythm. It is the measure of potential, the stillness from which all dynamic "snaps" and transformations arise.
pirouette_definition: |
  The value of the Ki constant (π + 1) when a system is in the low-energy, unlocked 4π manifold topological state. It is typically observed in the laboratory frame or at non-relativistic velocities (v << c) and serves as the baseline value in the tether-snap dynamic, representing the "tethered" state before a topological transition to Ki_motion.
operational_definition:
  units: dimensionless
  symbol_table:
    - name: K_i,rest
      meaning: The Ki constant in the low-energy, zero-velocity limit.
      dimensions: dimensionless
      default_range: π + 1 ≈ 4.14159
  measurement:
    procedures:
      - name: Low-Energy Fringe Metrology
        outline: |
          Conduct a high-precision interferometry experiment (e.g., a variant of the Aharonov-Bohm effect) on a system maintained at low kinetic energy (v << c). The spiral Lagrangian term, ∝ K_i, introduces a path-dependent phase shift. K_i,rest is derived from the magnitude of this shift as the system's velocity approaches zero.
        expected_signals: [A static phase shift in the interference pattern distinct from standard electromagnetic effects, Absence of the hysteresis loop characteristic of the Ki_rest ↔ Ki_motion transition.]
        pitfalls: [Thermal noise obscuring the subtle phase shift, Confounding effects from other topological terms in the Lagrangian, Failure to achieve a true zero-velocity limit, leading to a measured value slightly higher than π+1.]
context_windows:
  - module: MATH-023
    excerpt: |
      Evaluating limits gives K_{i,rest}=π+1≈4.14159 (laboratory frame) and K_{i,motion}=4π/3≈4.18879 (co-moving tri-loop, red-shift corrected). The tiny ΔKi≈0.0472 encodes the geometric cost of triadic locking.
  - module: MATH-023
    excerpt: |
      Define the effective Ki as K_i^eff(v,Γ,T_a) = K_{i,rest} + ΔK_i σ[α(Ξ-Ξ_c)], with logistic switch σ and composite driver Ξ(φ̇,Γ,T_a). Crossing Ξ_c triggers the snap—a topological shift from the 4π manifold to the 2π triadic manifold.
poetic_connections:
  motifs: [stillness, potential, tether, ground state, unwound spring]
  evocative_lines:
    - "Ki is the frequency of the universe remembering itself—the angular measure of coherence realignment."
    - "The tether binds rest and motion; the snap is their reconciliation."
  association_matrix:
    - [ "KI_MOTION", 0.9 ]
    - [ "TETHER_SNAP", 0.8 ]
    - [ "4PI_MANIFOLD", 1.0 ]
formal_mappings:
  candidates:
    - target: α_cs (generic Chern-Simons coupling)
      domain: EFT
      mapping_kind: mathematical
      equation_hint: |
        L ⊃ (α_cs/4π) Fμν F̃μν vs. L_spiral ⊃ (K_i/λ_*) εF∂A
      justification: |
        Ki_rest is the low-energy value of a dimensionless coupling constant in a topological term added to the electromagnetic Lagrangian. This is mathematically analogous to Chern-Simons-like terms where a constant couples the field strength to a related topological quantity. However, the Pirouette term's structure (εF∂A) is non-standard and distinct from the conventional axion-photon form (εFAF).
      references: []
      confidence: 0.3
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The fundamental constant Ki_rest has the precise value π + 1."
      domain: experiment
      falsifier: "High-precision, low-velocity interferometry experiments yielding a limiting value for Ki that is statistically inconsistent with π + 1."
      status: proposed
      links: [MATH-023]
naming_notes:
  collisions: [Kinetic energy (K, KE), Wave number (k)]
  disambiguation: |
    Ki_rest is not a measure of kinetic energy. It is the dimensionless, low-energy value of the Ki constant, contrasted with its high-energy counterpart, Ki_motion. The "rest" refers to the zero-velocity limit, not rest mass energy.
crosslinks:
  near_synonyms: []
  antonyms: [KI_MOTION]
  prerequisites: [KI_CONSTANT]
  downstream_effects: [TETHER_SNAP, ACTIVATION_TICK]
license: CC-BY-SA-4.0
---

# Ki_rest

## Canonical (Pirouette)
The value of the Ki constant (π + 1) when a system is in the low-energy, unlocked 4π manifold topological state. It is typically observed in the laboratory frame or at non-relativistic velocities (v << c) and serves as the baseline value in the tether-snap dynamic, representing the "tethered" state before a topological transition to Ki_motion.

## EFT-First Summary
Ki_rest is the low-energy value (π+1) of a dimensionless coupling constant, Ki, in a novel topological term in the spiral-extended Lagrangian. Mathematically, it is analogous to a generic Chern-Simons coupling constant (`α_cs`) but appears in a non-standard `εF∂A` term. This constant defines the baseline for phase coherence in the 4π manifold before a topological transition "snaps" the system to the higher-energy `Ki_motion` state. See Ref: `MATH-023`.

## Glossary Links
- See also: `Ki_motion`, `Tether-Snap`, `Activation Tick`, `4π Manifold`