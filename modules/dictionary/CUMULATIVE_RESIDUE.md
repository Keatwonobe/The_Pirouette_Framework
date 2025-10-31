---
term: "Cumulative Residue"
canonical_id: "CUMULATIVE_RESIDUE"
symbol: "$R_c$"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["PDM-001_the_boundary_condition"]
---

---
term: Cumulative Residue
canonical_id: CUMULATIVE_RESIDUE
symbol: $R_c$
aliases: []
parents: [PDM-001-Sentinel_Protocol-v2.0]
children: [PDM-002-Simulation_Workshop_Implementation, PDM-001-Inversion_Proposal-v1.0]
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: PDM-001-Sentinel_Protocol-v2.0
      lines: "L70-L71"
      snippet: |
        Cumulative Residue ($R_c$): The integrated, time-decayed sum of the actor's past Wound Channels.
  editors: [Dictionary Generation Agent]
  review_log: []
triad:
  art: |
    A scar on the system's trust; a memory of past harms that shapes future caution. It is the stain that reveals the true character of an actor's history, never fully washing out.
  law: |
    An actor's operational freedom, defined by its Dynamic Parametric Gates, is inversely proportional to its Cumulative Residue. A higher $R_c$ value mandates tighter operational constraints.
  philosophy: |
    $R_c$ enacts the Principle of Anticipatory Accountability by making an actor's history an active governor of its present and future actions. It ensures that patterns of cumulative micro-harm are not ignored, transforming memory into a mechanism for systemic self-preservation.
pirouette_definition: |
  A scalar metric representing an actor's accumulated history of causing negative environmental perturbations (Wound Channels). It is calculated as a time-decayed integral of all past Wound Channels, ensuring that recent and significant harms weigh more heavily. This value serves as a direct input to the Sentinel Protocol, modulating an actor's future operational freedom by dynamically adjusting their Parametric Gates.
operational_definition:
  units: Dimensionless (normalized integral of Wound Channel magnitude)
  symbol_table:
    - name: $R_c$
      meaning: Cumulative Residue
      dimensions: dimensionless
      default_range: "[0, ∞)"
    - name: $W_i$
      meaning: Scalar magnitude of the i-th Wound Channel event
      dimensions: dimensionless
      default_range: "[0, ∞)"
    - name: $\tau$
      meaning: The characteristic decay time (half-life) of residue
      dimensions: T
      default_range: contextual
  measurement:
    procedures:
      - name: Cumulative Residual Logging
        outline: |
          1. Upon conclusion of an action, the resultant Wound Channel is mapped and its total spatio-temporal magnitude is integrated into a single scalar value, $W_{new}$.
          2. The actor's Cumulative Residue is updated using a leaky integrator model: $R_{c}(t_{new}) = R_{c}(t_{old})e^{-(t_{new}-t_{old})/\tau} + W_{new}$.
          3. The updated $R_c$ value is fed back into the system to recalibrate the actor's specific Dynamic Parametric Gates.
        expected_signals: [A scalar value $R_c$ that steps up after a new Wound Channel is logged, and decays exponentially over time in the absence of new harm.]
        pitfalls: [
          "Decay Rate Gaming: Setting the decay constant $\tau$ too short allows actors to evade accountability for past actions.",
          "Normalization Error: Inconsistent methods for integrating complex Wound Channels into a single scalar $W$ can be exploited."
        ]
context_windows:
  - module: PDM-001-Sentinel_Protocol-v2.0
    excerpt: |
      **Phase 1: Pre-Act Gating (The Shield)**
      Before execution, any proposed action is evaluated against a set of **Dynamic Parametric Gates**. These gates define acceptable thresholds for: Time-Adherence ($T_a$), Gladiator Force ($\Gamma$), Ki-Modulated Interaction Rate ($K_i$), and **Cumulative Residue ($R_c$)**: The integrated, time-decayed sum of the actor's past Wound Channels.
  - module: PDM-001-Sentinel_Protocol-v2.0
    excerpt: |
      **Cumulative Micro-Harm:** Many small attacks, each below the per-action detection limit.
      **Countermeasure:** **Cumulative Residual Logging ($R_c$).** The sum of the harm is tracked, ensuring the "death by a thousand cuts" vector is closed.
  - module: PDM-001-Inversion_Proposal-v1.0
    excerpt: |
      Instead of just logging **Cumulative Residue ($R_c$)**—a debt—the system now also calculates a **Cumulative Coherence Dividend ($C_D$)**—an asset. This asset is not merely abstract; it would manifest within the system as Preferential Gating: Systems with a high $C_D$ would experience wider, less restrictive Parametric Gates, granting them greater freedom and velocity of action.
poetic_connections:
  motifs: [scar tissue, system memory, karmic debt, persistent stain]
  evocative_lines:
    - "The sum of the harm is tracked, ensuring the 'death by a thousand cuts' vector is closed."
    - "An entity is accountable not only for the measurable residue of its past actions..."
  association_matrix:
    - [ "WOUND_CHANNEL", 0.9 ]
    - [ "DYNAMIC_PARAMETRIC_GATES", 0.8 ]
    - [ "ANTICIPATORY_ACCOUNTABILITY", 0.7 ]
formal_mappings:
  candidates:
    - target: Leaky integrator / Time-decaying accumulator
      domain: Control Theory|Signal Processing
      mapping_kind: mathematical|operational
      equation_hint: |
        $\frac{dR_c}{dt} = -\frac{1}{\tau}R_c + \sum_i W_i \delta(t - t_i)$
      justification: |
        The operational definition of $R_c$—a value that accumulates discrete inputs ($W_i$) and decays exponentially over time—is a canonical example of a leaky integrator. This is a fundamental model for systems that exhibit memory where the influence of past events fades over time.
      references:
        - title: Feedback Control of Dynamic Systems
          where: Chapter 3, Franklin, Powell, Emami-Naeini
          date: 2018-01-01
      confidence: 0.8
  adopted:
    - target:
      rationale:
      confidence: 0.0
constraints_and_falsifiers:
  claims:
    - statement: "A sustained high $R_c$ value will result in progressively tighter Dynamic Parametric Gates for an actor, measurably reducing their operational velocity and scope."
      domain: phenomenology
      falsifier: "An actor maintains a high $R_c$ without any observable, functionally significant change to its Gate parameters, allowing it to continue causing harm."
      status: proposed
      links: [PDM-002-Simulation_Workshop_Implementation]
naming_notes:
  collisions: [$R$ is common for Resistance, Radius; subscript $c$ is crucial.]
  disambiguation: |
    Distinguish from a physical residue. $R_c$ is an *informational* construct representing a history of consequence. It is the chronic, accumulated record, whereas a Wound Channel is the acute, individual event of harm from which $R_c$ is derived.
crosslinks:
  near_synonyms: []
  antonyms: [COHERENCE_DIVIDEND]
  prerequisites: [WOUND_CHANNEL]
  downstream_effects: [DYNAMIC_PARAMETRIC_GATES]
license: CC-BY-SA-4.0
---

# Cumulative Residue

## Canonical (Pirouette)
Cumulative Residue ($R_c$) is a core accountability metric within the Sentinel Protocol. It quantifies an actor's history of creating harm by maintaining a time-decaying sum of all past Wound Channels. This "system memory" ensures that even minor, repeated transgressions accumulate into a significant record. A high $R_c$ acts as a debt, automatically tightening an actor's future operational boundaries and thus preventing patterns of cumulative negative impact.

## EFT-First Summary
In the language of systems dynamics, Cumulative Residue ($R_c$) is implemented as a leaky integrator. It functions as a memory state, accumulating the magnitude of discrete harm events (Wound Channels) while exhibiting exponential decay over a characteristic time, $\tau$. This ensures that an actor's history of negative impacts fades but is never entirely forgotten, creating a direct feedback mechanism that modulates future permissions and enforces long-term accountability.

## Glossary Links
- See also: [Wound Channel](<link>), [Dynamic Parametric Gates](<link>), [Coherence Dividend](<link>)