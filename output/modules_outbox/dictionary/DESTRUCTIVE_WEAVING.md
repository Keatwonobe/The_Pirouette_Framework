---
term: "Destructive Weaving"
canonical_id: "DESTRUCTIVE_WEAVING"
symbol: ""
aliases: [Dissonance Injection]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-049"]
---

---
term: Destructive Weaving
canonical_id: DESTRUCTIVE_WEAVING
symbol: I < 0
aliases: [Dissonance Injection]
parents: [DOMA-049, CORE-006, DYNA-001]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-049
      lines: "§2"
      snippet: |
        A Destructive Weaving (I < 0): The action has decreased the Target's coherence, increasing its internal dissonance and pushing it towards a state of chaotic, turbulent flow. This is the formal definition of harm.
  editors: [Dictionary Generation Agent]
  review_log: []
triad:
  art: |
    To sever threads in the systemic tapestry, introducing a dissonant note that unravels harmony into noise. It is the act of turning a clear stream muddy, replacing flow with friction.
  law: |
    An action is a Destructive Weaving if and only if it measurably decreases the target system's action integral over a characteristic cycle (I < 0), indicating a net loss of coherence.
  philosophy: |
    By defining harm as a measurable reduction in a system's coherence, Destructive Weaving grounds ethics in physics. It recasts malevolence not as an abstract evil, but as a concrete, inefficient process that increases universal friction and pushes systems toward chaotic dissolution.
pirouette_definition: |
  A Destructive Weaving is an intervention by an Actor that results in a negative change in the Target system's Pirouette Action (`I = ΔS_p < 0`). This indicates a net decrease in the system's coherence, pushing it toward Turbulent or Stagnant Flow by increasing its temporal potential energy (`V_Γ`) or degrading its stable, resonant kinetic pattern (`K_τ`). It is the formal definition of harm within the Pirouette Framework.
operational_definition:
  units: The fundamental measure, Influence (I), has units of action (Joule-seconds, J·s). The practical proxy, Coherence Impact (CI), is dimensionless.
  symbol_table:
    - name: I
      meaning: Influence; the change in a target system's Pirouette Action.
      dimensions: M L^2 T^-1
      default_range: contextual
    - name: S_p
      meaning: The Pirouette Action; integral of the Pirouette Lagrangian over a cycle.
      dimensions: M L^2 T^-1
      default_range: contextual
    - name: CI
      meaning: Coherence Impact; a dimensionless proxy for Influence.
      dimensions: dimensionless
      default_range: "[-1, 1]"
  measurement:
    procedures:
      - name: Coherence Impact (CI) Approximation
        outline: |
          A Destructive Weaving is inferred when the Coherence Impact (CI) score is negative. The score is calculated by an Observer via an Echo Record, assessing: 1) The ratio of change in stable, resonant information (ΔKτ) to generated noise (ΔΓ_noise). 2) The phase-alignment between intervener and target (ξ_c). 3) The durability of the resulting state change (σ_s).
        expected_signals: [Negative CI score, observed transition to Turbulent/Stagnant flow, increase in system error rate or friction.]
        pitfalls: [The Observer's Shadow distorting measurements; misidentifying the system's true resonant pattern; difficulty isolating the action's effects from background noise.]
context_windows:
  - module: DOMA-049
    excerpt: |
      A Destructive Weaving (`I < 0`): The action has decreased the Target's coherence, increasing its internal dissonance and pushing it towards a state of chaotic, turbulent flow. This is the formal definition of harm.
  - module: DOMA-049
    excerpt: |
      Negative Radiance (A Dissonance Injection): This is the signature of a destructive act (`I < 0`). It is an action that pushes another system into Turbulent or Stagnant Flow by increasing ambient pressure, introducing chaos, or blocking a channel of coherence. Example: Spreading misinformation that causes panic and chaos within a community.
poetic_connections:
  motifs: [dissonance, friction, turbulence, tearing, static, chaos, severing]
  evocative_lines:
    - "It is an action that pushes another system into Turbulent or Stagnant Flow..."
    - "...the echo is carved into spacetime forever."
  association_matrix:
    - [ "TURBULENT_FLOW", 0.9 ]
    - [ "WOUND_CHANNEL", 0.7 ]
    - [ "OBSERVER_SHADOW", 0.5 ]
    - [ "TEMPORAL_PRESSURE", 0.8 ]
formal_mappings:
  candidates:
    - target: Entropy Generation (ΔS_gen > 0)
      domain: Statistical Mechanics
      mapping_kind: conceptual
      equation_hint: |
        I < 0  ⇔  ΔS_gen > 0
      justification: |
        A Destructive Weaving increases a system's internal disorder and reduces its ability to perform organized work (maintain its resonant pattern). This is conceptually equivalent to the generation of entropy in an irreversible process, which corresponds to a loss of free energy and an increase in microscopic disorder.
      references:
        - title: Nonequilibrium Thermodynamics
          where: Chapter 3, "Entropy Production"
          date: 2008-01-01
      confidence: 0.7
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "Any action that qualifies as a Destructive Weaving (`I < 0`) will result in a measurable increase in the target system's information-theoretic entropy."
      domain: phenomenology
      falsifier: "An observation of a confirmed Destructive Weaving that leads to a net decrease in the target system's entropy, or an increase in its organizational complexity without a corresponding coherence cost elsewhere."
      status: proposed
      links: [DOMA-049]
naming_notes:
  collisions: [The term "Weaving" has common usage in textiles, narrative theory, and programming.]
  disambiguation: |
    Distinguish from simple 'damage' or 'disruption'. A Destructive Weaving specifically refers to a decrease in *coherence*—the system's ability to express its resonant pattern. An action might be disruptive (e.g., a necessary surgery) but ultimately Constructive if it restores greater coherence.
crosslinks:
  near_synonyms: [DISSONANCE_INJECTION]
  antonyms: [CONSTRUCTIVE_WEAVING]
  prerequisites: [COHERENCE, PIROUETTE_LAGRANGIAN, FLOW_DYNAMICS]
  downstream_effects: [WOUND_CHANNEL, TURBULENT_FLOW, STAGNANT_FLOW]
license: CC-BY-SA-4.0
---

# Destructive Weaving

## Canonical (Pirouette)
A Destructive Weaving is an intervention by an Actor that results in a negative change in the Target system's Pirouette Action (`I = ΔS_p < 0`). This indicates a net decrease in the system's coherence, pushing it toward Turbulent or Stagnant Flow by increasing its temporal potential energy (`V_Γ`) or degrading its stable, resonant kinetic pattern (`K_τ`). It is the formal definition of harm within the Pirouette Framework.

## EFT-First Summary
In thermodynamic terms, a Destructive Weaving is analogous to an irreversible process that generates entropy within a target system. By increasing internal friction and chaotic motion, it reduces the system's available free energy, diminishing its capacity to maintain an organized, low-entropy state and pushing it toward thermal equilibrium or structural collapse. This provides a physical basis for harm as an act that actively degrades a system's capacity to exist.

## Glossary Links
- See also: [Constructive Weaving](<./constructive_weaving.md>), [Turbulent Flow](<./turbulent_flow.md>), [Coherence](<./coherence.md>), [Pirouette Lagrangian](<./pirouette_lagrangian.md>)