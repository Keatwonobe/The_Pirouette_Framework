---
term: "Flow State"
canonical_id: "FLOW_STATE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-121"]
---

---
term: Flow State
canonical_id: FLOW_STATE
symbol: 
aliases: [System Regime, Dynamic State]
parents: [DYNA-001]
children: [DOMA-121]
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-121
      snippet: |
        baseline_state:
          flow_state: Stagnant      # Mapped from logistics data showing blockage
  editors: [auto-compiler-agent]
  review_log: []
triad:
  art: |
    The character of a river's current—a smooth and powerful glide, a chaotic and churning rapid, or a still and silent pool.
  law: |
    A system's evolution through its state space can be classified into one of three primary qualitative regimes—Laminar, Turbulent, or Stagnant—based on the statistical properties of its velocity field, such as its mean, variance, and entropy.
  philosophy: |
    The quality of change is as significant as the change itself. This classification distinguishes healthy, directed evolution from destructive chaos or deadening paralysis, allowing a Weaver to diagnose not just *if* a system is moving, but *how*.
pirouette_definition: |
  A qualitative, categorical measure describing the dominant dynamics of a system's evolution. It characterizes the efficiency, predictability, and structure of state-space transitions. The three primary states are: **Laminar** (smooth, coherent, predictable, efficient energy transfer), **Turbulent** (chaotic, dissipative, unpredictable, high-variance), and **Stagnant** (static, low-variance, locked potential, minimal evolution).
operational_definition:
  units: Categorical (Laminar | Turbulent | Stagnant)
  symbol_table:
    - name: Laminar
      meaning: A state of smooth, predictable flow with low variance in state-space velocity. System evolution is efficient and follows clear geodesics on the coherence manifold.
    - name: Turbulent
      meaning: A state of chaotic, unpredictable flow with high variance in state-space velocity. Characterized by dissipative eddies and inefficient energy usage.
    - name: Stagnant
      meaning: A state of near-zero flow with low variance. The system is trapped in a local minimum of the potential landscape, unable to evolve despite available potential.
  measurement:
    procedures:
      - name: Time-Series Fluctuation Analysis
        outline: |
          1. Identify 1-3 key performance indicators (KPIs) that represent the system's primary motion.
          2. Collect high-frequency time-series data for these KPIs.
          3. Calculate the mean rate of change (velocity) and its variance/entropy over a sliding window.
          4. Classify the state based on thresholds:
             - Laminar: High mean velocity, low variance.
             - Turbulent: High/low mean velocity, high variance/entropy.
             - Stagnant: Near-zero mean velocity, low variance.
        expected_signals: [System KPIs (e.g., production output, communication latency), Coherence (Kτ), Pressure (Γ)]
        pitfalls: [Choosing non-representative KPIs, window size artefact (too short/long), misinterpreting oscillatory behavior for turbulence]
context_windows:
  - module: DOMA-121
    excerpt: |
      It allows a Weaver to model a system's coherence manifold, test the impact of interventions, and optimize strategies to guide the system from turbulent or stagnant states into healthy, laminar flow before real-world deployment.
  - module: DOMA-121
    excerpt: |
      ```yaml
      scenario: "Supply Chain Stalemate"
      domain: economics
      baseline_state:
        flow_state: Stagnant      # Mapped from logistics data showing blockage
      ...
      objective:
        target_flow_state: Laminar
        max_turbulence_risk: 0.03
      ```
poetic_connections:
  motifs: [river_currents, weather_patterns, dance, music_tempo]
  evocative_lines:
    - "reminds a system of the dance it was always meant to perform."
    - "sculpt the landscape of possibility"
  association_matrix:
    - [ "COHERENCE_Kτ", 0.8 ]
    - [ "PRESSURE_Γ", 0.5 ]
    - [ "TURBULENCE_PROBABILITY_Pₜ", 0.9 ]
formal_mappings:
  candidates:
    - target: Reynolds number (Re)
      domain: CM
      mapping_kind: conceptual
      justification: |
        The transition from Laminar to Turbulent flow in fluid dynamics is governed by the Reynolds number, a dimensionless quantity comparing inertial forces to viscous forces. Pirouette's Flow State is a direct generalization of this concept, where "viscosity" maps to factors resisting coherent change and "inertia" maps to the system's momentum along a trajectory.
      references:
        - title: Fluid Mechanics
          where: Chapter on Laminar-Turbulent Transition
      confidence: 0.9
    - target: Phase Space Dynamics (e.g., limit cycles, strange attractors)
      domain: Math
      mapping_kind: mathematical
      justification: |
        Laminar flow corresponds to evolution towards a fixed point or along a simple limit cycle. Turbulent flow corresponds to motion on a strange attractor, exhibiting sensitivity to initial conditions. Stagnant flow corresponds to being trapped at a stable fixed point (local minimum).
      references:
        - title: Nonlinear Dynamics and Chaos
          where: Strogatz, S. H.
      confidence: 0.8
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "All systems can be classified into one of the three primary Flow States (or a mixture thereof) at any given time scale."
      domain: theory
      falsifier: "The discovery of a system whose dynamics are fundamentally non-classifiable, e.g., exhibiting properties of all three states simultaneously and irreducibly, without being a simple superposition."
      status: proposed
      links: [DYNA-001]
    - statement: "Transitions between Flow States are driven by critical changes in the underlying Coherence (Kτ) and Pressure (Γ) fields."
      domain: phenomenology
      falsifier: "Observing a spontaneous, unprompted transition from Laminar to Turbulent flow in a system where Kτ and Γ remain perfectly stable and uniform."
      status: proposed
      links: [DYNA-001, CORE-006]
naming_notes:
  collisions: [Data flow, cash flow, workflow]
  disambiguation: |
    In Pirouette, "Flow State" does not refer to the movement of a conserved quantity (like money or data packets) but to the qualitative dynamics of the *entire system's state vector* as it moves through its abstract state space. It is a property of the system's evolution itself.
crosslinks:
  near_synonyms: [SYSTEM_REGIME, DYNAMIC_MODE]
  antonyms: [STATIC_STATE]
  prerequisites: [COHERENCE_Kτ, PRESSURE_Γ, DYNA-001]
  downstream_effects: [LAMINAR_FLOW_INDEX_LFI, TURBULENCE_PROBABILITY_Pₜ, SYNTHESIS_POTENTIAL_Φ_SYN]
license: CC-BY-SA-4.0
---