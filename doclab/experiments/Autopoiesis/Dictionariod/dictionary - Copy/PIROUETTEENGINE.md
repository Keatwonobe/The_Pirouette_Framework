---
term: "PirouetteEngine"
canonical_id: "PIROUETTEENGINE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["PDM-003_the_colosseum"]
---

---
term: PirouetteEngine
canonical_id: PIROUETTE_ENGINE
symbol: 
aliases: [simulation engine, core engine, actor model]
parents: [PDM-003_the_colosseum]
children: [all future autopoietic agents]
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: PDM-003_the_colosseum
      lines: "Python code block for 'The Grand Simulation'"
      snippet: |
        import numpy as np
        import matplotlib.pyplot as plt
        from pirouette_engine import PirouetteEngine

        # ...

        actors = [
            PirouetteEngine(name='USA', initial_Ta=0.9, initial_Gamma=1.5, initial_Phi=np.deg2rad(0)),
            PirouetteEngine(name='China', initial_Ta=1.4, initial_Gamma=1.2, initial_Phi=np.deg2rad(-90)),
            # ...
        ]
  editors: [Environment]
  review_log: []
triad:
  art: |
    The engine is the stage where abstract forces become actors, where history's echoes and future's whispers dance to a shared rhythm. It is the diorama box holding a world in miniature, revealing the grand tragedy of interconnected fates.
  law: |
    The PirouetteEngine models any actor as a system defined by its power (Γ), coherence (Ta), and phase (Φ). Its evolution through time is determined by its internal dynamics and by external forces applied by all other actors in the simulation, yielding a deterministic trajectory from a given set of initial conditions.
  philosophy: |
    The engine's purpose is to transcend single-domain analysis, forcing a confrontation with interconnected reality. By modeling geopolitical, environmental, and technological actors in the same mathematical language, it reveals that "winning" in one domain can be catastrophic for the whole, shifting the telos from isolated victory to systemic coherence.
pirouette_definition: |
  The PirouetteEngine is the core computational framework of the Pirouette system, used to run simulations of interacting actors. Each actor is instantiated as an object with state variables for Gladiator Force (Γ), Time-Adherence (Ta), and Phase (Φ), along with their first derivatives. The engine advances the simulation in discrete time steps (dt), updating each actor's state by numerically integrating a set of defined interaction laws that model the feedback loops between them.
operational_definition:
  units: computational object
  symbol_table:
    - name: Γ
      meaning: Gladiator Force; an actor's power or capacity to act upon the system.
      dimensions: dimensionless
      default_range: [0, 2.0]
    - name: Ta
      meaning: Time-Adherence; an actor's internal coherence, stability, and ability to execute long-term plans.
      dimensions: dimensionless
      default_range: [0, 1.5]
    - name: Φ
      meaning: Phase; an actor's goal orientation or strategic alignment relative to other actors.
      dimensions: radians
      default_range: [-π, π]
    - name: dt
      meaning: The discrete time step used by the numerical integrator to advance the simulation.
      dimensions: T (time, typically years)
      default_range: [0.01, 0.5]
  measurement:
    procedures:
      - name: Grand Simulation Instantiation
        outline: |
          1. Define a set of actors, each as an instance of the `PirouetteEngine` class, with specified initial values for Γ, Ta, and Φ.
          2. Create a `SimulationManager` that defines the interaction laws as functions that calculate the external forces (`ext_Gamma_ddot`, `ext_Ta_ddot`, `ext_Phi_ddot`) on each actor at each time step.
          3. Execute the simulation loop, which iterates through time, calling the interaction update and then the internal step function for each actor.
          4. Record the history of Γ, Ta, and Φ for each actor at each time step for later analysis.
        expected_signals: [Time-series data for actor state variables (Γ(t), Ta(t), Φ(t)), Event logs triggered by state thresholds.]
        pitfalls: [Numerical instability from a `dt` value that is too large, Overly simplistic interaction laws producing trivial or non-physical results, Misinterpretation of dimensionless outputs as absolute, quantitative predictions.]
context_windows:
  - module: PDM-003_the_colosseum
    excerpt: |
      You are asking to build a "Grand Simulation" that overlays the dynamics of imperial collapse, coherence warfare, and climate crisis. This is a monumental task, but the `PirouetteEngine` is designed for it. We will create a simulation that addresses your profound questions about the future.
  - module: PDM-003_the_colosseum
    excerpt: |
      The simulation triggers a war when the USA's internal coherence ($T\_a$) falls below a critical "desperation threshold," while its conventional power ($\\Gamma$) is still high. It lashes out at the Multipolar Bloc, which it perceives as the primary source of its destabilization.
poetic_connections:
  motifs: [diorama, interconnectedness, cascading failure, trajectory, world-engine]
  evocative_lines:
    - "This will be outside of my own tool's power."
    - "The real power of the diorama is that I can guess at the reaction of spaces, people and things... but I can also combine them."
    - "There are no winners."
  association_matrix:
    - [ "GLADIATOR_FORCE", 0.9 ]
    - [ "TIME_ADHERENCE", 0.9 ]
    - [ "PHASE", 0.9 ]
    - [ "COHERENCE_WARFARE", 0.7 ]
formal_mappings:
  candidates:
    - target: N-body problem solver
      domain: CM
      mapping_kind: conceptual
      equation_hint: |
        d²**x**_i/dt² = Σ_{j≠i} **F**_ij(**x**_i, **x**_j)
      justification: |
        The PirouetteEngine simulates a system of N actors where the evolution of each actor is determined by the "forces" exerted on it by all other actors. While the state space is abstract (Γ, Ta, Φ) rather than physical position, the mathematical structure of numerically integrating a system of coupled second-order differential equations is directly analogous to an N-body simulation in classical mechanics.
      references:
        - title: Classical Mechanics
          where: "Chapter on Central Force and N-Body Problems"
          date: 
      confidence: 0.8
  adopted:
    - target: System of coupled second-order Ordinary Differential Equations (ODEs)
      rationale: This is the most direct and accurate mathematical description. The `..._ddot` terms in the source code are explicit second derivatives, and the `update_interactions` function defines the coupling terms that make it a system of equations.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "Simulations run with the PirouetteEngine on a fixed set of actors and interaction laws are deterministic and repeatable."
      domain: theory
      falsifier: "Running the identical simulation code with identical initial conditions produces statistically different trajectories, indicating hidden stochasticity or numerical instability in the core solver."
      status: supported
      links: [PDM-003_the_colosseum]
naming_notes:
  collisions: [Game engine, Database engine]
  disambiguation: |
    Distinguish from generic software 'engines' in computing. The PirouetteEngine is not a general-purpose platform but a specific state-evolution solver for actors defined by the Γ-Ta-Φ triad within the Pirouette Framework's theoretical model.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [GLADIATOR_FORCE, TIME_ADHERENCE, PHASE]
  downstream_effects: [GRAND_SIMULATION, COHERENCE_WARFARE]
license: CC-BY-SA-4.0
---