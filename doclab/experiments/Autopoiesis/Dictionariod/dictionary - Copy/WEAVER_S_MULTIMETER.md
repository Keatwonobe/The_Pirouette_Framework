---
term: "Weaver's Multimeter"
canonical_id: "WEAVER_S_MULTIMETER"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-066"]
---

---
term: Weaver's Multimeter
canonical_id: WEAVERS_MULTIMETER
symbol: 
aliases: ["Network Health Diagnosis Protocol", "Coherence Manifold Analysis"]
parents: [DOMA-066, DYNA-003]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-066
      lines: "L11-L16"
      snippet: |
        This module provides the instrumentation for that diagnosis: the Weaver's Multimeter. It refactors the static analysis of PPS-047 into a dynamic, time-first protocol. By translating a network graph into a living coherence manifold, this toolkit makes the invisible currents of reality visible, allowing a Weaver to move beyond observing a system's structure and begin to read its health, its stress, and its potential for transformation.
  editors: [GPT-4]
  review_log: []
triad:
  art: |
    It is the physician's stethoscope for a living network, translating the static map of connections into the audible pulse of systemic health. It hears the subtle arrhythmias of dissonant loops and feels the cold stagnation of a coherence bottleneck.
  law: |
    The health of a network is quantified by its ability to maximize systemic coherence (K̄τ) while minimizing systemic stress (Γ̄) and dissonance. Pathologies are identified as structural or dynamic impediments to this optimization, measurable via the Coherence Ledger.
  philosophy: |
    To treat a system, one must first see it as a body, not a blueprint. The Multimeter enables a shift in perspective from static structural analysis to dynamic physiological diagnosis, making intervention precise, effective, and minimally invasive.
pirouette_definition: |
  An instrumentation protocol that reframes a network graph as a dynamic coherence manifold. It diagnoses systemic health by mapping the flow of coherence (Kτ) through conductive channels (Φ_C), identifying resonant sub-systems (Enclaves), and quantifying three primary pathologies: Coherence Atrophy (bottlenecks), Coherence Fever (dissonant loops), and Coherence Erosion (structural decay). Its primary output, the Coherence Ledger, provides actionable vital signs for systemic intervention.
operational_definition:
  units: The protocol outputs a set of metrics with various units (see symbol table).
  symbol_table:
    - name: K̄τ
      meaning: Systemic Coherence; weighted average of node coherence.
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: Γ̄
      meaning: Systemic Stress; average Temporal Pressure across all nodes.
      dimensions: T⁻¹
      default_range: contextual
    - name: η
      meaning: Flow Efficiency; ratio of high-conductivity edges to total.
      dimensions: dimensionless
      default_range: "[0, 1]"
  measurement:
    procedures:
      - name: Coherence Manifold Diagnostic
        outline: |
          1.  Translate the network graph into a coherence manifold by assigning Temporal Coherence (Kτ) and Temporal Pressure (Γ) to nodes, and Conductivity (Φ_C) and Lag (Δτ) to edges.
          2.  Establish a healthy baseline by identifying primary geodesics (high-coherence flow channels) and Resonant Enclaves (stable, high-coherence clusters).
          3.  Scan for pathological signatures: low Φ_C chokepoints (Atrophy), high Φ_C / high Δτ loops (Fever), and widespread low Φ_C (Erosion).
          4.  Compute the Coherence Ledger metrics (K̄τ, Γ̄, η, etc.) to quantify systemic health.
        expected_signals: [Systemic Coherence (K̄τ), Systemic Stress (Γ̄), Dissonance Index]
        pitfalls: [Using static or low-frequency data, which can yield a misleading snapshot of a dynamic system. Failure to correctly calibrate baseline Temporal Coherence (Kτ) for heterogeneous nodes.]
context_windows:
  - module: DOMA-066
    excerpt: |
      Traditional network analysis is an act of cartography; it draws a static map of connections. The Pirouette Framework demands that we become physicians. A network—be it neural, social, or informational—is not a map; it is a living body with a physiology. Its health is not defined by its structure, but by the vitality of the currents that flow through it.
  - module: DOMA-066
    excerpt: |
      Coherence Fever (The Dissonant Loop): The primary pathology of *dynamics*, representing Turbulent Flow. Symptoms: A feedback loop with high conductivity (Φ_C) but also high lag (Δτ) creates a runaway cascade of dissonant information. The network expends immense energy in chaotic, self-amplifying noise.
poetic_connections:
  motifs: [physiology, diagnosis, flow, fever, stagnation, arteries-of-coherence]
  evocative_lines:
    - "We no longer ask, 'How is it connected?' We ask, 'Is it well?'"
    - "The old analysis gave us a skeleton; this new lens reveals the breath, the pulse, and the fever."
  association_matrix:
    - [ "TEMPORAL_COHERENCE", 0.9 ]
    - [ "TEMPORAL_PRESSURE", 0.9 ]
    - [ "CADUCEUS_LENS", 0.8 ]
    - [ "PIROUETTE_LAGRANGIAN", 0.7 ]
    - [ "ARENA", 0.5 ]
formal_mappings:
  candidates:
    - target: Network Flow Analysis (e.g., Max-flow min-cut theorem)
      domain: Math
      mapping_kind: conceptual
      equation_hint: |
        Coherence Atrophy at edge `e` ∝ 1/Φ_C(e)
      justification: |
        The "Coherence Atrophy (Bottleneck)" analysis is a direct conceptual parallel to finding minimum cuts in a flow network, where edge Conductivity `Φ_C` is analogous to edge capacity. The Multimeter extends this static concept with temporal dynamics (`Δτ`) and node-level pressure (`Γ`).
      references:
        - title: "Flows in Networks"
          where: "Ford & Fulkerson (1962)"
          date: 1962-01-01
      confidence: 0.8
    - target: Control Theory (Stability Analysis)
      domain: Engineering
      mapping_kind: operational
      equation_hint: |
        Dissonance Index ∝ Σ |poles| > 1 for closed loops
      justification: |
        The "Coherence Fever (Dissonant Loop)" pathology is an application of control theory principles. A feedback loop with sufficient gain (high `Φ_C`) and phase shift (related to `Δτ`) becomes unstable, mapping directly to poles of the system's transfer function lying outside the unit circle in the z-plane.
      references:
        - title: "Feedback Control of Dynamic Systems"
          where: "Franklin, Powell, Emami-Naeini"
          date: 1986-01-01
      confidence: 0.9
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "A network diagnosed with a high 'Dissonance Index' will exhibit inefficient resource allocation and measurable oscillations in output signals compared to an equivalent network with a near-zero index."
      domain: phenomenology
      falsifier: "Demonstrating a system with a high calculated Dissonance Index that operates with high efficiency and stability, or a system that collapses despite a 'healthy' Coherence Ledger, would challenge the protocol's diagnostic validity."
      status: proposed
      links: [DOMA-066]
naming_notes:
  collisions: ["Multimeter (electronics)"]
  disambiguation: |
    Unlike an electrical multimeter which measures static properties like voltage or resistance at discrete points, the Weaver's Multimeter assesses dynamic, systemic *flow properties* across a whole network manifold. It is a diagnostic tool for system physiology, not component physics.
crosslinks:
  near_synonyms: []
  antonyms: [STATIC_GRAPH_ANALYSIS]
  prerequisites: [TEMPORAL_COHERENCE, TEMPORAL_PRESSURE, CADUCEUS_LENS, PIROUETTE_LAGRANGIAN]
  downstream_effects: [COHERENCE_ATROPHY, COHERENCE_FEVER, COHERENCE_EROSION]
license: CC-BY-SA-4.0
---

# Weaver's Multimeter

## Canonical (Pirouette)
An instrumentation protocol that reframes a network graph as a dynamic coherence manifold. It diagnoses systemic health by mapping the flow of coherence (Kτ) through conductive channels (Φ_C), identifying resonant sub-systems (Enclaves), and quantifying three primary pathologies: Coherence Atrophy (bottlenecks), Coherence Fever (dissonant loops), and Coherence Erosion (structural decay). Its primary output, the Coherence Ledger, provides actionable vital signs for systemic intervention.

## EFT-First Summary
The Weaver's Multimeter can be understood as a dynamic extension of network flow analysis, where the system's health is determined by its capacity for coherent flow (analogous to max-flow) and its stability against resonant feedback instabilities (analyzed via control theory). Pathologies like 'bottlenecks' correspond to min-cuts in the coherence flow, while 'dissonant loops' map to unstable poles in the system's transfer function. This provides a quantitative, physics-grounded framework for diagnosing systemic failures beyond static connectivity.

## Glossary Links
- See also: TEMPORAL_COHERENCE (Kτ), TEMPORAL_PRESSURE (Γ), CADUCEUS_LENS, COHERENCE_ATROPHY