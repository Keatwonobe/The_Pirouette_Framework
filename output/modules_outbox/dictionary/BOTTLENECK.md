---
term: "Bottleneck"
canonical_id: "BOTTLENECK"
symbol: ""
aliases: [Coherence Dam]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-174"]
---

---
term: Bottleneck
canonical_id: BOTTLENECK
symbol: 
aliases: [Coherence Dam]
parents: [DOMA-174]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-174
      lines: "L41-45"
      snippet: |
        A bottleneck is a geometric feature in the coherence manifold that forces the system off this geodesic. It is a point of high friction, a "coherence dam" that introduces turbulence and dissonance.
  editors: [agent: auto-compiler]
  review_log: []
triad:
  art: |
    A system in pain is a symphony of noise. The master listens for the one string that is out of tune, the critical fracture from which chaos cascades.
  law: |
    A small fraction of event types (the 'critical few') within a system will be responsible for the majority (typically ≥80%) of its total coherence loss (`ΔKτ`).
  philosophy: |
    To heal a system, one must move from the cacophony of symptoms to the singular source of the ailment. The Bottleneck concept enforces diagnostic discipline, focusing finite energy on points of maximum leverage to restore a system to Laminar Flow.
pirouette_definition: |
  A localized, high-friction feature in a system's coherence manifold that forces the system's trajectory off its geodesic. A bottleneck introduces turbulence and dissonance, causing a sharp, non-linear drop in coherence (`Kτ`) and a corresponding reduction in the system's total action (`S_p`). It represents a critical point of failure where a small number of causes are responsible for a majority of the system's performance degradation.
operational_definition:
  units: Dimensionless feature, identified by its effect on coherence (`Kτ`).
  symbol_table:
    - name: ΔKτ
      meaning: Change in Coherence
      dimensions: Contextual (e.g., T⁻¹, M L² T⁻³, etc.)
      default_range: contextual
    - name: S_p
      meaning: Pirouette Action
      dimensions: [Coherence] * [Time]
      default_range: contextual
  measurement:
    procedures:
      - name: Pareto Probe
        outline: |
          1.  Define and measure a time-series for the system's primary coherence output (`Kτ`).
          2.  Log all discrete system events and correlate them to calculate the coherence loss (`ΔKτ`) caused by each event.
          3.  Rank event types in descending order by the total `ΔKτ` they have caused.
          4.  Identify the "vital few" event types that cumulatively account for a majority (e.g., 80%) of the total coherence loss. These are the bottlenecks.
        expected_signals: [A Pareto distribution of `ΔKτ` across event types, A sharp "knee" in the cumulative loss plot]
        pitfalls: [Misattribution of `ΔKτ` to the wrong event, Poor choice of `Kτ` as a proxy for system health, Event categories defined too broadly or narrowly]
context_windows:
  - module: DOMA-174
    excerpt: |
      A system's health... is the measure of its ability to sustain Laminar Flow—a state of high coherence... A bottleneck is a geometric feature in the coherence manifold that forces the system off this geodesic. It is a point of high friction, a "coherence dam" that introduces turbulence and dissonance. Each encounter with a bottleneck exacts a cost, causing a sharp, measurable drop in the system's coherence (`Kτ`).
  - module: DOMA-174
    excerpt: |
      The critical bottlenecks are the events for which the partial derivative `∂S_p/∂e` is most negative. In the language of coherence manifolds, these are the locations of steep, non-linear cliffs—regions where the system's geodesic is exceptionally fragile and a small perturbation causes a catastrophic loss of action.
poetic_connections:
  motifs: [friction, dam, fracture, turbulence, dissonance, wound, leverage point]
  evocative_lines:
    - "distinguish the cacophony of symptoms from the singular source of the ailment."
    - "the locations of steep, non-linear cliffs..."
  association_matrix:
    - [ "TURBULENCE", 0.8 ]
    - [ "COHERENCE_LOSS", 0.9 ]
    - [ "LAMINAR_FLOW", -0.9 ]
    - [ "PARETO_PROBE", 0.9 ]
formal_mappings:
  candidates:
    - target: Dissipative Term (e.g., `γ(∂q/∂t)²`)
      domain: CM|EFT
      mapping_kind: conceptual
      equation_hint: |
        𝓛_eff = 𝓛_ideal - 𝓛_dissipative
        where bottleneck events dominate 𝓛_dissipative.
      justification: |
        A bottleneck acts as a localized source of energy or information loss, analogous to a frictional or dissipative term in a physical system's Lagrangian. This term removes energy from the coherent degrees of freedom, converting it into disorder (entropy), which is observed as a sharp drop in coherence (`ΔKτ`).
      references: []
      confidence: 0.6
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "In any complex system, ≥80% of total coherence loss can be attributed to ≤20% of the distinct event/failure types."
      domain: phenomenology
      falsifier: "Repeated observation of systems where coherence loss is evenly distributed ('death by a thousand cuts') across a wide variety of causes, with no 'critical few' emerging from Pareto Probe analysis."
      status: supported
      links: [DOMA-174]
naming_notes:
  collisions: [Standard usage in computer science (e.g., CPU bottleneck) and operations research (e.g., theory of constraints).]
  disambiguation: |
    In Pirouette, 'Bottleneck' is a formalized concept within the coherence manifold, not just a generic constraint on throughput. It is specifically a geometric feature causing turbulence and a non-linear drop in the system's action, diagnosed via its disproportionate contribution to total coherence loss (`ΔKτ`).
crosslinks:
  near_synonyms: [CRITICALITY]
  antonyms: [LAMINAR_FLOW, GEODESIC]
  prerequisites: [COHERENCE, PIROUETTE_LAGRANGIAN]
  downstream_effects: [TURBULENCE, COHERENCE_LOSS]
license: CC-BY-SA-4.0
---

# Bottleneck

## Canonical (Pirouette)
A localized, high-friction feature in a system's coherence manifold that forces the system's trajectory off its geodesic. A bottleneck introduces turbulence and dissonance, causing a sharp, non-linear drop in coherence (`Kτ`) and a corresponding reduction in the system's total action (`S_p`). It represents a critical point of failure where a small number of causes are responsible for a majority of the system's performance degradation.

## EFT-First Summary
Conceptually, a Bottleneck is analogous to a localized dissipative term in an effective Lagrangian. While the ideal system dynamics conserve a quantity (coherence), the bottleneck introduces a strong, localized friction that drains this quantity from the system's coherent modes of motion, converting it into microscopic disorder (entropy). Its effect is not a gentle drag but a sharp, non-linear energy loss event triggered by interaction with a specific feature of the system's state space.

## Glossary Links
- See also: [Coherence](./coherence.md), [Pareto Probe](./pareto_probe.md), [Turbulence](./turbulence.md)