---
term: "Wound Channel Depth"
canonical_id: "WOUND_CHANNEL_DEPTH"
symbol: "ω"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-019"]
---

---
term: Wound Channel Depth
canonical_id: WOUND_CHANNEL_DEPTH
symbol: ω
aliases: []
parents: [DOMA-019, CORE-011]
children: [INST-GOV-001_placeholder]
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-019
      snippet: |
        | Irreversibility (I) | **Wound Channel Depth (ω)** | How deeply and permanently will the action scar a system's memory and identity, as encoded in its Wound Channel? |
  editors: [system-agent]
  review_log: []
triad:
  art: |
    Some marks are carved not into stone, but into the memory of what can be. The depth of the channel is the measure of a scar on eternity, the echo of a bell that cannot be un-rung.
  law: |
    Wound Channel Depth (ω) is a normalized risk parameter [0,1] quantifying the expected permanence of an action's imprint on a system's coherence manifold. A high ω value mandates the highest standard of scrutiny, potentially invoking a Coherence Quarantine via The Crucible Protocol.
  philosophy: |
    The framework asserts that actions are not ephemeral; they impress themselves upon the universe's memory. ω serves as the conscience of causality, forcing a confrontation with permanence. It prioritizes the preservation of future possibility by making the cost of irreversible change explicit and demanding a near-sacred justification for any action that would close a door forever.
pirouette_definition: |
  Wound Channel Depth (ω) is a dimensionless risk parameter that measures the degree to which an action's effects are encoded as a permanent and irreversible feature within a target system's coherence manifold. As a component of the Coherence Risk (R_κ) equation, it quantifies the persistence of the 'scar' left in the system's memory and identity, distinguishing transient disturbances from lasting structural transformations. High ω implies that the system cannot return to its initial state space through natural evolution or simple reversal.
operational_definition:
  units: dimensionless (normalized scale [0,1])
  symbol_table:
    - name: ω
      meaning: Wound Channel Depth
      dimensions: dimensionless
      default_range: "[0, 1]"
  measurement:
    procedures:
      - name: Manifold Scarring Simulation
        outline: |
          1. Model the target system's coherence manifold, identifying key memory-encoding structures (e.g., attractor states, information-theoretic fixed points).
          2. Simulate the action and its direct impact.
          3. Propagate the system's evolution post-action over a long, system-appropriate timescale.
          4. Measure the information-theoretic distance (e.g., Kullback-Leibler divergence) between the post-action evolved state and the original state manifold. ω is a normalized function of this divergence, approaching 1 as the probability of returning to the original state basin approaches 0.
        expected_signals: [Persistent deviation in system state vectors, collapse or creation of new stable attractors, non-zero mutual information between the action's signature and long-term system behavior]
        pitfalls: [Inaccurate system modeling leading to under/overestimation of resilience, simulation timescale being too short to capture true long-term scarring]
context_windows:
  - module: DOMA-019
    excerpt: |
      An act is not "bad" because it is large; it is *risky* because it threatens to create a deep, dissonant scar that propagates through many layers of reality. To map this geometry, we translate the old risk parameters into their true, dynamic forms:
      | Old Term | New Pirouette Term | Mapping Question |
      | :--- | :--- | :--- |
      | Irreversibility (I) | **Wound Channel Depth (ω)** | How deeply and permanently will the action scar a system's memory and identity, as encoded in its Wound Channel? |
  - module: DOMA-019
    excerpt: |
      **The Principle of Irreversibility:** Actions that threaten to carve deep, permanent Wound Channels (high ω) demand the highest standard of scrutiny and justification. Some bells cannot be un-rung.
poetic_connections:
  motifs: [scar, memory, echo, permanence, bell, carving, landscape]
  evocative_lines:
    - "Some bells cannot be un-rung."
    - "every choice we make becomes a permanent feature of the landscape upon which others must walk."
  association_matrix:
    - [ "COHERENCE_RISK", 0.9 ]
    - [ "WOUND_CHANNEL", 0.8 ]
    - [ "IRREVERSIBILITY", 0.7 ]
    - [ "THE_CRUCIBLE", 0.6 ]
formal_mappings:
  candidates:
    - target: Topological change in a system's state space (e.g., bifurcation, attractor destruction)
      domain: Math
      mapping_kind: conceptual
      equation_hint:
      justification: |
        ω quantifies the permanence of a change. In dynamical systems, the most permanent changes are not just shifts in state but alterations to the underlying topology of the state space itself—for example, the destruction of a stable attractor. ω can be modeled as a measure of the energy barrier or improbability of a reverse bifurcation that would restore the original system topology.
      references:
        - title: "Nonlinear Dynamics and Chaos"
          where: "Strogatz, S. H."
          date: 2014-12-03
      confidence: 0.6
  adopted:
    - target:
      rationale:
      confidence: 0.0
constraints_and_falsifiers:
  claims:
    - statement: "Systems with high homeostatic capacity (e.g., strong negative feedback loops) will exhibit lower ω for a given perturbation (δ) than brittle systems."
      domain: phenomenology
      falsifier: "Observation of a highly resilient, self-correcting system that, when perturbed, becomes permanently locked into a new state with no possibility of return, contradicting the expected correlation between resilience and low ω."
      status: proposed
      links: [DOMA-019]
naming_notes:
  collisions: [ω (angular frequency in physics)]
  disambiguation: |
    ω (Wound Channel Depth) should not be confused with the common use of ω for angular frequency in mechanics or wave phenomena. In the Pirouette context, ω always refers to the permanence of a system's scarring, a dimensionless risk parameter.
crosslinks:
  near_synonyms: [IRREVERSIBILITY]
  antonyms: [SYSTEMIC_RESILIENCE]
  prerequisites: [WOUND_CHANNEL, COHERENCE_MANIFOLD]
  downstream_effects: [COHERENCE_RISK, THE_CRUCIBLE_PROTOCOL]
license: CC-BY-SA-4.0
---

# Wound Channel Depth

## Canonical (Pirouette)
Wound Channel Depth (ω) is a dimensionless risk parameter that measures the degree to which an action's effects are encoded as a permanent and irreversible feature within a target system's coherence manifold. As a component of the Coherence Risk (R_κ) equation, it quantifies the persistence of the 'scar' left in the system's memory and identity, distinguishing transient disturbances from lasting structural transformations. High ω implies that the system cannot return to its initial state space through natural evolution or simple reversal.

## EFT-First Summary
Currently, no formal mapping to Effective Field Theory is adopted. The leading conceptual candidate maps ω to topological changes in a system's dynamical state space, where a high ω corresponds to an irreversible bifurcation or destruction of a stable attractor. This frames 'scarring' as a permanent alteration of the system's possible futures.

## Glossary Links
- See also: Reach (ρ), Dissonance (δ), Coherence Risk (R_κ), Wound Channel