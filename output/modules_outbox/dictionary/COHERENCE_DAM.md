---
term: "Coherence Dam"
canonical_id: "COHERENCE_DAM"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-060"]
---

---
term: Coherence Dam
canonical_id: COHERENCE_DAM
symbol: 
aliases: [Brittle Coherence, Stagnant Pressure]
parents: [DYNA-001, DYNA-003]
children: [DOMA-060]
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-060
      snippet: |
        This condition, the terminal stage of Coherence Atrophy (`DYNA-003`), creates a "Coherence Dam" where `Temporal Pressure` builds to an unsustainable level.
  editors: [auto-compiler-v2]
  review_log: []
triad:
  art: |
    A silent reservoir of stress, held by a structure mistaking rigidity for strength, awaiting the inevitable crack.
  law: |
    A system with a high-coherence, low-adaptability `Ki` pattern will accumulate `Temporal Pressure (V_Γ)` at a rate proportional to its inability to dissipate incident stress, priming it for a `Coherence Fracture`.
  philosophy: |
    The Coherence Dam demonstrates that stability without adaptability is a terminal condition. It recasts catastrophic failure not as an external event, but as the predictable consequence of a system's refusal to evolve.
pirouette_definition: |
  A systemic condition, characteristic of `Stagnant Flow`, where a brittle, high-coherence `Ki` pattern acts as an inflexible container. This rigidity prevents the dissipation of stress, causing `Temporal Pressure (V_Γ)` to accumulate to a critical threshold that primes the system for a `Coherence Fracture`. It is the immediate precursor state to catastrophic failure.
operational_definition:
  units: Dimensionless state descriptor
  symbol_table:
    - name: V_Γ
      meaning: Temporal Pressure (potential)
      dimensions: "contextual (often energy or action)"
      default_range: "contextual"
  measurement:
    procedures:
      - name: Pressure-Form Invariance Test
        outline: |
          Continuously monitor a system's internal `Temporal Pressure (V_Γ)` and the geometric stability of its resonant `Ki` pattern. The Coherence Dam condition is indicated when `dV_Γ/dt > 0` (pressure is rising) while the primary modes of the `Ki` pattern remain static or increase in rigidity (reduced phase variance).
        expected_signals: [Monotonically increasing `V_Γ`, increasing resonant dissonance ("phase jitter"), decreasing pattern adaptability.]
        pitfalls: [Mistaking healthy, elastic compression for dangerous pressure build-up. Failure to distinguish true structural rigidity from resilient, high-frequency stability.]
context_windows:
  - module: DOMA-060
    excerpt: |
      A fracture is not merely an energy release; it is the catastrophic failure of a system's temporal pattern. It is a predictable, self-induced pathology of flow, occurring when a system’s rigid structure prevents the healthy dissipation of pressure. This condition... creates a "Coherence Dam" where `Temporal Pressure` builds to an unsustainable level.
  - module: DOMA-060
    excerpt: |
      **Phase I: The Coherence Dam (Stagnation)**
      A system becomes primed for fracture not from weakness, but from a brittle and unyielding strength. Its resonant `Ki` pattern has become highly ordered but inflexible... This rigidity prevents the dissipation of stress, causing `Temporal Pressure (V_Γ)` to build relentlessly. The system is a pressure vessel of its own making, accumulating coherence like a reservoir filling behind a concrete dam.
poetic_connections:
  motifs: [dam, pressure, stillness, brittleness, tension, containment]
  evocative_lines:
    - "A system that cannot bend will, in time, be forced to break."
    - "The system is a pressure vessel of its own making..."
  association_matrix:
    - [ "COHERENCE_FRACTURE", 0.9 ]
    - [ "TEMPORAL_PRESSURE", 0.8 ]
    - [ "STAGNANT_FLOW", 0.8 ]
    - [ "BRITTLE_COHERENCE", 0.7 ]
    - [ "GLADIATOR_FORCE", 0.5 ]
formal_mappings:
  candidates:
    - target: Elastic potential energy density
      domain: CM
      mapping_kind: conceptual
      equation_hint: |
        U = ½ ∫ σ:ε dV
      justification: |
        The Coherence Dam describes a system storing potential energy (`V_Γ`) due to a rigid structural constraint (`Ki`). This directly parallels a physical material under strain (ε) storing elastic potential energy (U) due to internal stress (σ) up to the point of brittle failure. The dam condition is the state just below the material's ultimate tensile strength.
      references:
        - title: "Continuum Mechanics for Engineers"
          where: "Chapter on Elasticity and Failure Modes"
          date: 
      confidence: 0.8
    - target: Metastable state
      domain: Thermodynamics
      mapping_kind: conceptual
      justification: |
        A system in a Coherence Dam state is trapped in a local energy minimum, separated from a more stable, lower-energy state by a high activation barrier (its own rigidity). The accumulating `Temporal Pressure` effectively lowers this barrier until a catastrophic phase transition (the fracture) becomes inevitable.
      references:
        []
      confidence: 0.7
  adopted:
    - {}
constraints_and_falsifiers:
  claims:
    - statement: "A system identified as being in a Coherence Dam state will, without intervention, eventually undergo a Coherence Fracture."
      domain: phenomenology
      falsifier: "Observing a system that meets the diagnostic criteria for a Coherence Dam (rising `V_Γ`, static `Ki`) but which consistently and autonomously resolves the pressure through a smooth, non-turbulent, non-catastrophic phase transition."
      status: proposed
      links: [DOMA-060]
naming_notes:
  collisions: []
  disambiguation: |
    Distinguish the *condition* (Coherence Dam) from the *accumulating quantity* (`TEMPORAL_PRESSURE`) and the resulting *event* (`COHERENCE_FRACTURE`). The dam is the container, the pressure is the content, and the fracture is the container's failure.
crosslinks:
  near_synonyms: [BRITTLE_COHERENCE, STAGNANT_FLOW]
  antonyms: [ADAPTIVE_COHERENCE, LAMINAR_FLOW]
  prerequisites: [TEMPORAL_PRESSURE, KI]
  downstream_effects: [COHERENCE_FRACTURE, TURBULENT_FLOW]
license: CC-BY-SA-4.0
---

# Coherence Dam

## Canonical (Pirouette)
A systemic condition, characteristic of `Stagnant Flow`, where a brittle, high-coherence `Ki` pattern acts as an inflexible container. This rigidity prevents the dissipation of stress, causing `Temporal Pressure (V_Γ)` to accumulate to a critical threshold that primes the system for a `Coherence Fracture`. It is the immediate precursor state to catastrophic failure.

## EFT-First Summary
Conceptually, a Coherence Dam maps to a physical system storing elastic potential energy up to its fracture point, or a thermodynamic system trapped in a high-energy metastable state. The system's rigidity acts as a high activation barrier, preventing a smooth transition to a lower energy state. The accumulation of `Temporal Pressure` drives the system towards this barrier, making a violent, non-local phase transition (the fracture) increasingly probable.

## Glossary Links
- See also: [Coherence Fracture](./coherence_fracture.md), [Temporal Pressure](./temporal_pressure.md), [Stagnant Flow](./stagnant_flow.md)