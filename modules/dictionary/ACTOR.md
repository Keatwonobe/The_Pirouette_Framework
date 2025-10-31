---
term: "Actor"
canonical_id: "ACTOR"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["PDM-003_the_colosseum"]
---

---
term: Actor
canonical_id: ACTOR
symbol:
aliases: [PirouetteEngine, Player, Entity, System]
parents: [PDM-003_the_colosseum]
children: [all future autopoietic agents]
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: PDM-003_the_colosseum
      snippet: |
        * **The Actors:**

            * **USA:** Modeled with the internal vulnerabilities of a late-stage empire (the "Rome" overlay).
            * **China:** A highly coherent, rising power focused on its own ascendancy.
            * **Multipolar Bloc:** A new entity representing Russia, India, Brazil, and other powers...
            * **The Biosphere:** The planetary system, whose health is a critical variable affecting all human actors.
            * **Human Innovation:** A special, non-political actor representing humanity's collective technological and problem-solving ability. This is the "wild card."
  editors: [Environment]
  review_log: []
triad:
  art: |
    An Actor is a resonant system on the planetary stage, a player in a grand diorama. It is a nation, a planet, or even an idea, given form and agency to dance with others in the unfolding of history.
  law: |
    An Actor is any entity fully described by the state vector (Γ, Ta, Φ) and its time derivatives, whose dynamics are governed by the PirouetteEngine equations of motion. Its behavior is determined entirely by its internal state and its interactions with other Actors in the simulation.
  philosophy: |
    The Actor formalism allows for the reification of complex, multi-scale systems (from nations to abstract concepts like 'Innovation') into discrete, interacting entities. This enables the simulation of otherwise intractable dynamics by abstracting away internal complexity in favor of capturing essential external interactions and systemic resonance.
pirouette_definition: |
  An Actor is a fundamental, dynamical entity within a Pirouette simulation, instantiated by the `PirouetteEngine`. Each Actor is defined by a state vector composed of Gladiator Force (Γ), Time-Adherence (Ta), and Phase (Φ). Its evolution is governed by a set of differential equations that account for internal dynamics and external forces exerted by other Actors, allowing for the modeling of complex systems like nation-states (USA), planetary systems (Biosphere), or abstract concepts (Innovation).
operational_definition:
  units: State-vector container; not a physical unit.
  symbol_table:
    - name: Γ
      meaning: Gladiator Force, representing system power/capacity.
      dimensions: dimensionless
      default_range: "[0, ∞)"
    - name: Ta
      meaning: Time-Adherence, representing system stability/coherence.
      dimensions: dimensionless
      default_range: "[0, ∞), typically normalized around 1.0"
    - name: Φ
      meaning: Phase, representing goal alignment or strategic orientation.
      dimensions: angle (radians)
      default_range: "[0, 2π)"
  measurement:
    procedures:
      - name: Simulation State Extraction
        outline: |
          Within a running Pirouette simulation, an Actor's state is measured by directly querying the `PirouetteEngine` instance at a given time step `t`. The procedure involves accessing the actor's `history` attribute, which stores the time-series data for its core state variables (Γ, Ta, Φ).
        expected_signals: [Time-series data for Γ(t), Ta(t), Φ(t)]
        pitfalls: [Mistaking the abstract Actor model for the full complexity of the real-world entity it represents (reification fallacy)., Ignoring the specific interaction rules defined in the `SimulationManager` which give the Actor its contextual behavior.]
context_windows:
  - module: PDM-003_the_colosseum
    excerpt: |
      You cannot model a country as a single person, but you *can* model it as a resonant system, which is precisely what we have done. Now you ask the most important questions of all. You introduce a new player—not a nation, not an empire, but a *possibility*. Let's call them the **Weavers**.
  - module: PDM-003_the_colosseum
    excerpt: |
      The questions we want to answer are these: What does the future hold? When does the next major powers conflict break out into kinetic war, and who ultimately wins according to the simulation? Does human innovation outpace the climate crisis or do we crumble?
poetic_connections:
  motifs: [diorama, gladiator, resonance, player, system]
  evocative_lines:
    - "Too many players in my mental model."
    - "I can make each country a person, but that makes me give them personalities like their leadership, which is always too simplistic to work."
    - "You *can* model it as a resonant system, which is precisely what we have done."
  association_matrix:
    - [ "GLADIATOR_FORCE", 0.9 ]
    - [ "TIME_ADHERENCE", 0.9 ]
    - [ "PHASE", 0.9 ]
    - [ "PIRROUETTE_ENGINE", 1.0 ]
formal_mappings:
  candidates:
    - target: Quasiparticle
      domain: CM
      mapping_kind: conceptual
      justification: |
        Like a quasiparticle (e.g., phonon), a Pirouette Actor is an emergent entity that simplifies the dynamics of a complex, many-body system. It abstracts away microscopic details (e.g., individual citizens) to describe the collective excitations and interactions of the system as a whole.
      confidence: 0.6
  adopted:
    - target: Agent (Agent-Based Modeling)
      rationale: |
        The term 'Agent' from ABM most closely captures the role of an Actor as a discrete, interacting entity in a simulation. The key distinction is Pirouette's use of continuous, physics-inspired state variables instead of discrete behavioral rules.
      confidence: 0.8
constraints_and_falsifiers:
  claims:
    - statement: "Any complex adaptive system, from a nation-state to a planetary climate system, can be meaningfully represented as a Pirouette Actor without critical loss of predictive power for macro-scale interactions."
      domain: phenomenology
      falsifier: "A scenario where the internal, microscopic dynamics of a system (not captured by the Γ, Ta, Φ state vector) become the dominant driver of its external behavior, causing simulation results to consistently diverge from observed reality in a way that cannot be corrected by refining Actor interaction laws."
      status: proposed
      links: [PDM-003_the_colosseum]
naming_notes:
  collisions: [Actor Model (Computer Science)]
  disambiguation: |
    A Pirouette Actor is a stateful, continuous-variable entity in a simulation, distinct from the 'Actor' in concurrent computing, which is a primitive for message-passing. While both handle interactions, the Pirouette Actor is defined by its physical state (Γ, Ta, Φ), not its computational behavior or mailbox.
crosslinks:
  near_synonyms: [PIRROUETTE_ENGINE]
  antonyms: []
  prerequisites: [GLADIATOR_FORCE, TIME_ADHERENCE, PHASE]
  downstream_effects: [SIMULATION_MANAGER]
license: CC-BY-SA-4.0
---

# Actor

## Canonical (Pirouette)
An Actor is a fundamental, dynamical entity within a Pirouette simulation, instantiated by the `PirouetteEngine`. Each Actor is defined by a state vector composed of Gladiator Force (Γ), Time-Adherence (Ta), and Phase (Φ). Its evolution is governed by a set of differential equations that account for internal dynamics and external forces exerted by other Actors, allowing for the modeling of complex systems like nation-states (USA), planetary systems (Biosphere), or abstract concepts (Innovation).

## EFT-First Summary
In the language of Agent-Based Modeling (ABM), a Pirouette Actor can be understood as a sophisticated Agent. Unlike traditional agents defined by discrete rules, an Actor's behavior emerges from a set of continuous, physics-inspired state variables—Gladiator Force (Γ), Time-Adherence (Ta), and Phase (Φ)—that evolve according to differential equations. This allows it to represent a complex system as a single, resonant entity whose interactions govern the simulation's macro-dynamics.

## Glossary Links
- See also: [[GLADIATOR_FORCE]], [[TIME_ADHERENCE]], [[PHASE]], [[PIRROUETTE_ENGINE]]