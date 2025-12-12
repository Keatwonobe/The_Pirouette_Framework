---
term: "Reverse Pareto Analysis (RPA)"
canonical_id: "REVERSE_PARETO_ANALYSIS_RPA"
symbol: ""
aliases: [Pareto Chisel]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-033"]
---

---
term: Reverse Pareto Analysis (RPA)
canonical_id: REVERSE_PARETO_ANALYSIS
symbol: 
aliases: [Pareto Chisel]
parents: [DOMA-033, PPS-014]
children: [dashboards]
status: ratified
version: 2.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-033
      snippet: |
        RPA is a Pareto Chisel. It inverts the classic 80/20 principle to find the "critical few"—the smallest possible set of causes responsible for the vast majority of the "effect." In this context, the "effect" is coherence loss.
  editors: [AI Assistant]
  review_log: []
triad:
  art: |
    RPA is a Pareto Chisel, an instrument that finds the critical few fractures in a system's coherence. It reveals the pressure point—the place where the least effort will produce the greatest healing. It translates the felt sense of "wrongness" to the precise knowledge of "what is broken."
  law: |
    Given a set of causal events and their quantified impacts on system coherence, RPA identifies the minimal subset of events responsible for a specified cumulative percentage (typically 80%) of the total coherence loss.
  philosophy: |
    RPA codifies the 'See, then Solve' principle by translating a complex history of system failure into a simple, actionable list of root causes. It enforces diagnostic focus, preventing wasted effort on symptoms by directing attention to the "critical few" sources of dissonance.
pirouette_definition: |
  Reverse Pareto Analysis is a diagnostic algorithm that identifies the smallest set of causal events responsible for a threshold-defined majority (e.g., 80%) of a system's total coherence loss. It operates by first quantifying the Impact of each event as the negative integral of the Pirouette Lagrangian (𝓛_p) during the event's correlated time window, then sorting events by impact and accumulating them until the threshold is met. The output is a prioritized, actionable list of the "critical few" systemic bottlenecks.
operational_definition:
  units: The output is a dimensionless list of events and a dimensionless ratio (percentage of total impact).
  symbol_table:
    - name: threshold
      meaning: The target percentage of total impact that the "critical few" must account for.
      dimensions: dimensionless
      default_range: "[0, 1], typically 0.8"
  measurement:
    procedures:
      - name: Coherence Loss Attribution via RPA
        outline: |
          1. Generate the system's Pirouette Lagrangian (𝓛_p) time-series using the Fractal Bridge protocol (CORE-014).
          2. Correlate every causal event from raw system data with discrete dips in the 𝓛_p trace.
          3. Calculate the Impact (I) for each event by integrating the negative change in 𝓛_p over the duration of the dip (I ≈ - ∫_dip Δ𝓛_p dt).
          4. Provide the list of events and their calculated impacts to the RPA algorithm with a set threshold (e.g., 0.8).
          5. The algorithm sorts events by impact (descending) and returns the smallest list of events whose cumulative impact meets or exceeds the threshold.
        expected_signals: [A short, sorted list of "critical few" causal events, A percentage value indicating the total impact accounted for by this list]
        pitfalls: [Misattribution of impact due to event correlation without causation, Poor time resolution in Lagrangian data smearing impact scores across multiple events, Setting the threshold too high (e.g., >0.95) can include an unhelpfully large number of minor causes]
context_windows:
  - module: DOMA-033
    excerpt: |
      This is the function of **Reverse Pareto Analysis (RPA)**, the core insight preserved and modernized from `PPS-014`.
      RPA is a Pareto Chisel. It inverts the classic 80/20 principle to find the "critical few"—the smallest possible set of causes responsible for the vast majority of the "effect." In this context, the "effect" is coherence loss.
  - module: DOMA-033
    excerpt: |
      The output is not a complex model, but a simple, actionable list of the critical few. This is the system's pressure point—the place where the least effort will produce the greatest healing.
poetic_connections:
  motifs: [chisel, pressure point, critical few, bottleneck, arrhythmia, fracture]
  evocative_lines:
    - "RPA is a Pareto Chisel."
    - "It grants the Weaver the clarity to touch the single thread that will mend the entire tapestry."
  association_matrix:
    - [ "IMPACT", 1.0 ]
    - [ "COHERENCE_LOSS", 0.9 ]
    - [ "PIROUETTE_LAGRANGIAN", 0.8 ]
    - [ "BOTTLENECK", 0.7 ]
formal_mappings:
  candidates:
    - target: Pareto Principle (80/20 Rule)
      domain: Quality Management
      mapping_kind: conceptual
      justification: |
        RPA is a direct, algorithmic application of the Pareto principle, used not just for description but for prescriptive diagnosis. It formalizes the search for the "vital few" causes that Juran identified as the key to quality improvement, applying it specifically to the domain of coherence loss.
      references:
        - title: Quality Control Handbook
          where: Juran, J.M.
          date: 1951
      confidence: 0.95
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "In systems governed by the Pirouette Framework, '>>80%' of coherence loss is typically concentrated in <20% of causal events."
      domain: phenomenology
      falsifier: "Demonstration of a system where coherence loss is consistently diffuse and evenly distributed across a large number of low-impact events. In such a system, RPA would fail to find a 'critical few' and would return a large fraction of the total events to meet the 80% threshold."
      status: proposed
      links: [DOMA-033]
naming_notes:
  collisions: [Pareto Analysis, Pareto Chart]
  disambiguation: |
    Standard Pareto analysis is a descriptive technique, often a visual chart, used to highlight the most significant factors in a dataset. Reverse Pareto Analysis is a specific, prescriptive algorithm that starts with the total measured effect (coherence loss) and works backward to identify the minimal set of causes for a target percentage of that effect. The "Reverse" emphasizes the goal-oriented, algorithmic nature of the process.
crosslinks:
  near_synonyms: []
  antonyms: [DIFFUSE_DECOHERENCE]
  prerequisites: [PIROUETTE_LAGRANGIAN, IMPACT, FRACTAL_BRIDGE]
  downstream_effects: [SYSTEM_INTERVENTION, BOTTLENECK_REMEDIATION]
license: CC-BY-SA-4.0
---