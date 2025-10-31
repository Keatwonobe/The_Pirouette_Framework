---
term: "Dominant Flow State"
canonical_id: "DOMINANT_FLOW_STATE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-092"]
---

---
term: Dominant Flow State
canonical_id: DOMINANT_FLOW_STATE
symbol: 
aliases: []
parents: [DYNA-001]
children: [DOMA-092]
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-092
      lines: "L34-L35"
      snippet: |
        **Dominant Flow State** | The system's macro-state from **Flow Dynamics** (DYNA-001) | How does coherence (information, resources, energy) move through the system? This diagnoses the system's operational health as **Laminar**, **Turbulent**, or **Stagnant**.
  editors: [Weaver-Agent-7]
  review_log: []
triad:
  art: |
    The river of civilization can flow as a placid, powerful current, a chaotic, churning flood, or a fetid, dying pool. The Dominant Flow State is the character of this water, revealing the health of the world it carves.
  law: |
    A system's Dominant Flow State is determined by the signal-to-noise ratio in its core logistical, informational, and economic channels. A high, stable ratio indicates Laminar flow; a low, volatile ratio, Turbulent; and a near-zero signal throughput indicates Stagnant flow.
  philosophy: |
    To diagnose a system's flow is to understand its capacity for action. A Laminar system executes its purpose, a Turbulent system frantically seeks a new one, and a Stagnant system has lost its purpose entirely. Interventions must respect this fundamental capacity, either by reinforcing, redirecting, or reigniting the flow of coherence.
pirouette_definition: |
  The Dominant Flow State is a macroscopic diagnostic category that characterizes the efficiency and coherence of systemic transport. It describes how information, resources, energy, and value move through a system's primary channels. The state is classified as one of three modes: **Laminar** (ordered, efficient, predictable), **Turbulent** (chaotic, inefficient, reconfiguring), or **Stagnant** (blocked, decaying, inert).
operational_definition:
  units: Categorical (Laminar, Turbulent, Stagnant)
  symbol_table:
    - name: Laminar
      meaning: Ordered, efficient, and predictable flow with low internal friction and high signal-to-noise ratio.
      dimensions: dimensionless
      default_range: N/A
    - name: Turbulent
      meaning: Chaotic, inefficient, and unpredictable flow with high dissipation and low signal-to-noise ratio.
      dimensions: dimensionless
      default_range: N/A
    - name: Stagnant
      meaning: Blocked, inert, or decaying flow with near-zero throughput and severe coherence erosion.
      dimensions: dimensionless
      default_range: N/A
  measurement:
    procedures:
      - name: Channel Coherence Analysis
        outline: |
          1. Identify a system's primary transport channels (e.g., supply chains, information networks, capital markets).
          2. For each channel, define a metric for "signal" (intended throughput) and "noise" (waste, error rate, transaction costs, volatility).
          3. Measure the signal-to-noise ratio (SNR) and throughput velocity over time.
          4. Classify the state: High/stable SNR indicates Laminar; Low/volatile SNR indicates Turbulent; near-zero throughput indicates Stagnant.
        expected_signals: [Supply chain delivery variance, network packet loss, market bid-ask spreads, social trust metrics]
        pitfalls: [Confusing local turbulence with a systemic state, selecting non-primary channels for analysis, ignoring time-lags in state transitions.]
context_windows:
  - module: DOMA-092
    excerpt: |
      An epoch is not a period defined by dates, but a state defined by its dynamics. We diagnose this state using three fundamental, measurable axes... The **Dominant Flow State**... asks: How does coherence (information, resources, energy) move through the system? This diagnoses the system's operational health as **Laminar**, **Turbulent**, or **Stagnant**.
  - module: DOMA-092
    excerpt: |
      **States of Laminar Flow (Ordered Progress):**
      - (High Kτ, High Γ, Laminar): *The Grand Campaign.* A highly organized, traditional society executing a major expansion with ruthless efficiency. *Example: The Roman Empire at its peak, with goods, legions, and information moving along stable channels.*
poetic_connections:
  motifs: [river, flood, blockage, artery, fever, current, channel]
  evocative_lines:
    - "History is not a story that is told; it is a river that flows."
    - "To understand an epoch is to diagnose its flow."
  association_matrix:
    - [ "COHERENCE", 0.9 ]
    - [ "COHERENCE_FEVER", 0.7 ]
    - [ "WOUND_CHANNEL", 0.6 ]
    - [ "TEMPORAL_PRESSURE", 0.5 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Reynolds number (Re) regimes
      domain: CM
      mapping_kind: conceptual
      equation_hint: |
        Re = (inertial forces) / (viscous forces) = ρuL / μ
      justification: |
        The classification directly mirrors the behavior of fluid flow, governed by the dimensionless Reynolds number. Laminar flow (low Re) is smooth and orderly, while Turbulent flow (high Re) is chaotic and dissipative. Stagnant flow corresponds to a near-zero velocity field (Re ≈ 0), representing a system dominated by internal friction or external blockage.
      references:
        - title: Fluid Mechanics, Vol. 6
          where: "Course of Theoretical Physics, §29-§33"
          date: 1959-01-01
      confidence: 0.8
constraints_and_falsifiers:
  claims:
    - statement: "A system's state transition from Laminar to Turbulent flow is accompanied by a measurable, power-law increase in systemic waste (e.g., transaction costs, energy dissipation, information loss)."
      domain: phenomenology
      falsifier: "Observation of systems undergoing a major state transition without a corresponding non-linear shift in waste/dissipation metrics, or where the shift follows a different functional form (e.g., linear)."
      status: proposed
      links: [DYNA-001, DOMA-092]
naming_notes:
  collisions: [The terms "Laminar" and "Turbulent" are intentionally adopted from fluid dynamics to leverage the robust physical analogy.]
  disambiguation: |
    This term does not describe the microscopic state of individual agents but the macroscopic, aggregate behavior of coherence flow through the system's primary channels. A system can be in a Laminar state even if it contains chaotic individuals, provided the overall transport of resources and information remains orderly and efficient.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [FLOW_DYNAMICS, COHERENCE]
  downstream_effects: [EPOCHAL_MANIFOLD, COHERENCE_ENGINE]
license: CC-BY-SA-4.0
---

# Dominant Flow State

## Canonical (Pirouette)
The Dominant Flow State is a macroscopic diagnostic category that characterizes the efficiency and coherence of systemic transport. It describes how information, resources, energy, and value move through a system's primary channels. The state is classified as one of three modes: **Laminar** (ordered, efficient, predictable), **Turbulent** (chaotic, inefficient, reconfiguring), or **Stagnant** (blocked, decaying, inert).

## EFT-First Summary
The Dominant Flow State is conceptually mapped to the regimes of classical fluid dynamics, characterized by the Reynolds number (`Re`). Laminar flow corresponds to low `Re` (smooth, viscous-dominated), Turbulent flow to high `Re` (chaotic, inertia-dominated), and Stagnant flow to a near-zero velocity field. This mapping provides a robust physical analogy for diagnosing the dissipation and efficiency of coherence transport in any complex system (see: Landau & Lifshitz, *Fluid Mechanics*).

## Glossary Links
- See also: Flow Dynamics (DYNA-001), Epochal Manifold (DOMA-092), Coherence (CORE-013)