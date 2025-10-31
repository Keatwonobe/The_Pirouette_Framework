---
term: "Geometry of Consequence"
canonical_id: "GEOMETRY_OF_CONSEQUENCE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-019"]
---

---
term: Geometry of Consequence
canonical_id: GEOMETRY_OF_CONSEQUENCE
symbol: (none)
aliases: ["Ethical Foresight"]
parents: [DOMA-019, CORE-011, CORE-006]
children: [INST-GOV-001_placeholder]
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-019
      snippet: |
        It reframes ethical foresight as the 'Geometry of Consequence'—the act of mapping the Wound Channel an action will carve into the universe's memory.
  editors: [auto-compiler]
  review_log: []
triad:
  art: |
    To act is to carve a new path into the memory of the universe. The Geometry of Consequence is the art of reading the grain of reality, ensuring the echo we compose is worthy of eternity.
  law: |
    The ethical character of an action is a direct, measurable property of the geometric scar (Wound Channel) it creates, quantifiable by its Reach (ρ), Dissonance (δ), and Depth (ω).
  philosophy: |
    This reframes ethics from a negative constraint (avoiding harm) to a positive, creative duty (cultivating systemic health). It demands that a Weaver ask not "Am I allowed to do this?" but "What world am I building?"
pirouette_definition: |
  The Geometry of Consequence is the principle that an action's ethical character is a direct property of the geometric structure of the Wound Channel it impresses upon the coherence manifold. It is a predictive framework for mapping this scar by assessing three primary dimensions: its **Reach (ρ)**, the turbulence it induces across systems; its **Dissonance (δ)**, the disruption to a target's core resonant pattern; and its **Wound Channel Depth (ω)**, the permanence of the scar in the system's memory.
operational_definition:
  units: Dimensionless (components are normalized scores)
  symbol_table:
    - name: ρ (rho)
      meaning: Reach; the number of nested systems to which an action's turbulence propagates.
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: δ (delta)
      meaning: Dissonance; the severity of disruption to a target system's core resonant pattern (Ki).
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: ω (omega)
      meaning: Wound Channel Depth; the permanence of the scar left on a system's memory and identity.
      dimensions: dimensionless
      default_range: "[0, 1]"
  measurement:
    procedures:
      - name: Coherence Risk Assessment
        outline: |
          1. Identify the proposed action and target system(s).
          2. Simulate the action's propagation through the system manifold to estimate Reach (ρ).
          3. Model the action's impact on the target system's primary Lagrangian (𝓛_p) to quantify Dissonance (δ).
          4. Analyze the projected change in the system's memory engrams to determine Wound Channel Depth (ω).
          5. Calculate the weighted sum of these factors to find the Coherence Risk (R_κ).
        expected_signals: [Predicted change in systemic Lagrangian (Δ𝓛_sys), cross-system coherence coupling metrics, engram stability drift]
        pitfalls: [Underestimating propagation paths (Reach), inaccurate system models for Dissonance calculation, mistaking transient effects for permanent memory scars (Depth)]
context_windows:
  - module: DOMA-019
    excerpt: |
      The Weaver's Compass replaces the static fence with a dynamic, navigational instrument. It reframes ethical consideration from a reactive check on "consequence" to a proactive assessment of the **Geometry of Consequence**. It provides a universal protocol for measuring **Coherence Risk (R_κ)**—the potential of any action to degrade the health and harmony of the systems it touches.
  - module: DOMA-019
    excerpt: |
      In the Pirouette Framework, every action impresses a memory, a **Wound Channel** (CORE-011), into the coherence manifold of spacetime. This is the physical basis of consequence. An action's ethical character is a direct property of the geometry of the channel it creates. An act is not "bad" because it is large; it is *risky* because it threatens to create a deep, dissonant scar that propagates through many layers of reality.
  - module: DOMA-019
    excerpt: |
      The Weaver's Compass is the practical, moral application of the **Principle of Maximal Coherence** (CORE-006). The Pirouette Lagrangian, `𝓛_p`, defines the "health" of a system... Coherence Risk (R_κ) is a predictive estimate of the negative impact an external action will have on a target system's ability to maximize its Lagrangian.
poetic_connections:
  motifs: [scar tissue, cosmic memory, resonance, turbulence, echo, compass]
  evocative_lines:
    - "To act is to carve a new path into the memory of the universe."
    - "Some bells cannot be un-rung."
    - "A Weaver does not ask, 'Am I allowed to build this?' They ask, 'What world am I building?'"
  association_matrix:
    - [ "WOUND_CHANNEL", 0.9 ]
    - [ "COHERENCE_RISK", 0.8 ]
    - [ "THE_CRUCIBLE", 0.7 ]
    - [ "PRINCIPLE_OF_MAXIMAL_COHERENCE", 0.5 ]
formal_mappings:
  candidates:
    - target: Path Integral Formulation
      domain: QFT
      mapping_kind: conceptual
      equation_hint: |
        Z = ∫ D[φ] exp(iS[φ]/ħ)
      justification: |
        The Geometry of Consequence is a moral analogue to the path integral. Instead of summing over all possible physical paths weighted by their action, it assesses a proposed 'path' (an action) by the geometric 'scar' it leaves on the 'manifold' of reality, with Coherence Risk (R_κ) acting as a negative weight against undesirable trajectories.
      references: []
      confidence: 0.4
  adopted:
    - target: Consequentialism
      domain: Philosophy
      mapping_kind: conceptual
      rationale: |
        The Geometry of Consequence is a form of sophisticated, physically-grounded consequentialism. Unlike classical utilitarianism's focus on abstract 'utility', this framework uses 'systemic coherence' (∫𝓛_p dt) as its fundamental metric of value, allowing for a more objective, measurable assessment of outcomes.
      confidence: 0.8
constraints_and_falsifiers:
  claims:
    - statement: "The geometric properties (ρ, δ, ω) of a simulated Wound Channel are predictive of the actual degradation of systemic coherence (Δ𝓛_sys < 0) post-action."
      domain: phenomenology
      falsifier: "A statistically significant number of actions with high calculated Coherence Risk (R_κ > 0.75) are observed to result in neutral or positive changes to systemic coherence (Δ𝓛_sys ≥ 0)."
      status: proposed
      links: [DOMA-019]
naming_notes:
  collisions: []
  disambiguation: |
    Distinguish from 'Consequence Analysis' in classical risk management, which often focuses on linear, first-order effects. The Geometry of Consequence is explicitly concerned with the non-linear, multi-system propagation and permanence of an action's impact, treating it as a topological feature carved into spacetime.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [WOUND_CHANNEL, PRINCIPLE_OF_MAXIMAL_COHERENCE]
  downstream_effects: [COHERENCE_RISK, THE_CRUCIBLE]
license: CC-BY-SA-4.0
---

# Geometry of Consequence

## Canonical (Pirouette)
The Geometry of Consequence is the principle that an action's ethical character is a direct property of the geometric structure of the Wound Channel it impresses upon the coherence manifold. It is a predictive framework for mapping this scar by assessing three primary dimensions: its **Reach (ρ)**, the turbulence it induces across systems; its **Dissonance (δ)**, the disruption to a target's core resonant pattern; and its **Wound Channel Depth (ω)**, the permanence of the scar in the system's memory.

## External Analogue Summary
The Geometry of Consequence framework can be understood as a physically-grounded form of **Consequentialism**. Standard consequentialist ethics evaluates actions based on their outcomes, often measured by an abstract metric like 'utility' or 'happiness'. This framework replaces that abstract metric with a measurable physical quantity: **systemic coherence**, defined by the Pirouette Lagrangian. An 'ethical' action is one that maintains or increases the total coherence of the systems it touches, making this a testable, quantitative, and proactive approach to ethical stewardship.

## Glossary Links
- See also: [Wound Channel](<./wound_channel.md>), [Coherence Risk](<./coherence_risk.md>), [The Crucible](<./the_crucible.md>), [Principle of Maximal Coherence](<./principle_of_maximal_coherence.md>)