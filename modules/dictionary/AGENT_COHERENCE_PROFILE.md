---
term: "Agent Coherence Profile"
canonical_id: "AGENT_COHERENCE_PROFILE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-075"]
---

---
term: Agent Coherence Profile
canonical_id: AGENT_COHERENCE_PROFILE
symbol: χ_A
aliases: [Coherence Profile, Agent Profile, Ki Pattern Bias]
parents: [DOMA-075]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-075
      lines: "L102-L105"
      snippet: |
        An Agent Coherence Profile: The formal definition of the new entity's `Ki` pattern—its core identity, values, and operational dynamics.
  editors: [Weaver-9]
  review_log: []
triad:
  art: |
    The geometric echo of a solved problem; a character inscribed upon the world. It is the living memory of a battle, the specific form of strength forged in a particular fire, ensuring the solution carries the soul of its own origin story.
  law: |
    An Agent Coherence Profile must be fully determined by the initial conditions of the Coherence Fracture it was created to resolve. Its core axiom and `Ki` pattern biases must be algorithmically traceable to the pressures synthesized in the Weaver's Forge, with a provenance similarity score > 0.95.
  philosophy: |
    The Framework rejects generic, context-free solutions. The Profile ensures that the *how* of a solution is inseparable from the *what*, creating agents whose very nature is a testament to the problem they solved, thereby ensuring resonant and resilient action. Form follows friction.
pirouette_definition: |
  The formal, machine-readable specification of an emergent agent's identity, values, and operational dynamics. It is a core component of an Action Engram, codifying the `Ki` pattern synthesized during a Weaver's Forge cycle. The Profile defines the agent's core axiom, its biases toward stability and openness, its focal mode (e.g., Laminar, Turbulent), and its resilience signature, ensuring the agent's character is a direct consequence of the problem it was created to solve.
operational_definition:
  units: Dimensionless ratios and enumerated types, typically represented in a structured data format (JSON).
  symbol_table:
    - name: χ_A
      meaning: Agent Coherence Profile, a structured data object defining an agent's character.
      dimensions: dimensionless
      default_range: N/A (structured object)
    - name: κ_s
      meaning: Ki Stability Bias, the agent's tendency to maintain its current state.
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: κ_o
      meaning: Ki Openness Bias, the agent's tendency to integrate new information.
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: F_Ki
      meaning: Ki Focus Mode, the agent's dominant operational style.
      dimensions: enumerated type
      default_range: "{Laminar, Turbulent, Stagnant}"
    - name: R_Γ
      meaning: Resilience to Gamma Pressure, the agent's characteristic response to stress.
      dimensions: enumerated type
      default_range: "{Brittle, Adaptive, Anti-Fragile}"
  measurement:
    procedures:
      - name: Coherence Provenance Audit
        outline: |
          1. Isolate the Action Engram and its Agent Coherence Profile (χ_A).
          2. Reconstruct the initial problem diagnosis and the convened Persona set from Weaver's Forge logs.
          3. Run a simulation of the `Geometry of Debate` (DYNA-002) with the source Personas to generate a predicted synthesis vector.
          4. Represent χ_A as a vector of its core axiom and `Ki` biases.
          5. Calculate the cosine similarity between the predicted synthesis vector and the χ_A vector.
        expected_signals: [Cosine similarity > 0.95, A clear mapping from each source Persona's core pressure to a corresponding bias or axiom in the profile.]
        pitfalls: [Incomplete logs of the Weaver's Forge debate, Simulation artifacts introducing divergence, Overly simplistic Persona definitions.]
context_windows:
  - module: DOMA-075
    excerpt: |
      A successful cycle produces two inseparable artifacts within a single Action Engram: An Action Blueprint... and An Agent Coherence Profile: The formal definition of the new entity's `Ki` pattern—its core identity, values, and operational dynamics. This creates a genealogy of solutions. The character of the solution-agent is a direct geometric consequence of the challenge it overcame.
  - module: DOMA-075
    excerpt: |
      ```json
      "agent_coherence_profile": {
        "$schema": "http://pirouette-framework.org/spec/ki-profile/2.0",
        "id": "ACTOR-001",
        "name": "The D12 Water Guardian",
        "core_axiom": "Verifiable data, openly shared, is the only antidote to mistrust.",
        "ki_pattern_bias": {
          "stability": 0.95,
          "openness": 0.8,
          "focus": "Laminar"
        },
        "resilience_to_gamma": "High (Responds to pressure with increased transparency)"
      }
      ```
poetic_connections:
  motifs: [genealogy, midwifery, forging, echo, ghost in the machine]
  evocative_lines:
    - "The soul of the solution is forged in the fire of the problem."
    - "it births specialized survivors, each a living memory of the battle it was created to win."
  association_matrix:
    - [ "ACTION_ENGRAM", 0.9 ]
    - [ "KI", 0.8 ]
    - [ "WEAVERS_FORGE", 0.7 ]
    - [ "WOUND_CHANNEL", 0.6 ]
formal_mappings:
  candidates:
    - target: Policy function (π(a|s))
      domain: Math
      mapping_kind: conceptual
      equation_hint: |
        χ_A → priors on π(a|s; θ)
      justification: |
        The Profile defines an agent's operational dynamics and values (core axiom), which is analogous to a policy function in reinforcement learning that maps states to actions. The `Ki` biases act as high-level parameters or structural priors on the policy space, constraining the agent's behavior to be "in character" and shaping its learning process.
      references:
        - title: Reinforcement Learning: An Introduction
          where: Sutton & Barto, Chapter 13
          date: 2018-01-01
      confidence: 0.6
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "An agent operating strictly according to its Coherence Profile will demonstrate greater long-term resilience and system-healing effectiveness than a generic, un-profiled optimization agent given the same Action Blueprint."
      domain: phenomenology
      falsifier: "In a controlled A/B test, a generic optimizer (e.g., pure task-completion RL agent) consistently achieves the objective of restoring Laminar Flow faster and with fewer negative externalities than an agent constrained by its corresponding Coherence Profile."
      status: proposed
      links: [DOMA-075]
naming_notes:
  collisions: []
  disambiguation: |
    Distinguish from `Ki` Pattern, which is the raw, descriptive state of a system's dynamics. An Agent Coherence Profile is a *prescriptive* `Ki` Pattern, a normative template for a *new* agent's behavior, not a description of an existing one. It is the "should be" forged from the "is".
crosslinks:
  near_synonyms: [AGENT_CONSTITUTION, OPERATIONAL_CHARTER]
  antonyms: [GENERIC_AGENT, UNCONSTRAINED_OPTIMIZER]
  prerequisites: [ACTION_ENGRAM, KI, WEAVERS_FORGE]
  downstream_effects: [AGENT_DEPLOYMENT, SYSTEM_RESONANCE]
license: CC-BY-SA-4.0