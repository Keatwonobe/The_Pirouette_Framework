---
term: "Coherence Auditor"
canonical_id: "COHERENCE_AUDITOR"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-033"]
---

---
term: Coherence Auditor
canonical_id: COHERENCE_AUDITOR
symbol: 
aliases: []
parents: [CORE-006, CORE-014]
children: [dashboards]
status: ratified
version: 2.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-033
      lines: "L7-L11"
      snippet: |
        summary: Provides the primary end-to-end workflow for systemic diagnosis. This module
        operationalizes the Reverse Pareto Analysis (RPA) canon by integrating it with the
        Fractal Bridge protocol (CORE-014), allowing a Weaver to translate raw system data
        into a precise, actionable list of the critical few sources of coherence loss.
  editors: [chain-of-thought-agent]
  review_log: []
triad:
  art: |
    A system in pain does not announce its wound; it simply loses its grace. The Coherence Auditor is the instrument that translates this loss of grace back into a language we can understand, granting the Weaver the clarity to touch the single thread that will mend the entire tapestry.
  law: |
    The Auditor operationalizes the See-then-Solve loop by first translating raw system data into a Lagrangian (𝓛_p) time-series via the Fractal Bridge, then applying Reverse Pareto Analysis to identify the critical few events causing a threshold percentage (typically ≥80%) of the total coherence loss.
  philosophy: |
    The Auditor translates the philosophical Principle of Maximal Coherence into a diagnostic engine. It empirically discovers and quantifies what is preventing a system from obeying its own most fundamental drive, turning the abstract concept of "dissonance" into a concrete, actionable target for intervention.
pirouette_definition: |
  The primary instrument that provides a unified, end-to-end workflow for systemic diagnosis. It operationalizes Reverse Pareto Analysis (RPA) by first using the Fractal Bridge protocol (CORE-014) to translate raw system data into a time-series of the Pirouette Lagrangian (𝓛_p), and then applying RPA to this series to identify the critical few sources responsible for the majority of systemic coherence loss.
operational_definition:
  units: The final output is a dimensionless, ranked list of causal identifiers. Intermediate calculations of Impact (I) have units of Action (e.g., joule-seconds).
  symbol_table:
    - name: I(fᵢ)
      meaning: The Impact of an event (fᵢ), defined as the total coherence lost (negative change in system Action ΔSₚ) correlated with that event.
      dimensions: M L² T⁻¹
      default_range: contextual
    - name: 𝓛_p
      meaning: Pirouette Lagrangian, the function representing a system's coherence.
      dimensions: M L² T⁻²
      default_range: contextual
  measurement:
    procedures:
      - name: Standard Coherence Audit
        outline: |
          1.  **Project:** Use the Fractal Bridge (CORE-014) to map raw, high-dimensional system data onto a time-series of the Pirouette Lagrangian (𝓛_p).
          2.  **Correlate:** Identify discrete events in the raw data that are time-correlated with significant negative dips in the 𝓛_p trace.
          3.  **Quantify:** Calculate the Impact (I) for each event by integrating the area of its corresponding dip (I ≈ -∫_dip Δ𝓛_p dt).
          4.  **Identify:** Sort events by Impact in descending order and accumulate until a threshold (e.g., 80%) of total impact is met. The events in this subset are the "critical few."
        expected_signals: [A Lagrangian (𝓛_p) time-series, a Pareto-sorted list of causal events]
        pitfalls: [Poor mapping in the Fractal Bridge (Stage I) leading to an uninformative Lagrangian trace., Misattribution of causality when correlating events to Lagrangian dips (Stage II) in systems with high event density.]
context_windows:
  - module: DOMA-033
    excerpt: |
      The Coherence Auditor replaces the fragmented protocols of the past with a single, unified, and time-first workflow. It is the practical bridge from observing a system's chaotic symptoms to pinpointing its critical fractures. It codifies the essential loop of the Pirouette Framework: **See, then Solve**.
  - module: DOMA-033
    excerpt: |
      RPA is a Pareto Chisel. It inverts the classic 80/20 principle to find the "critical few"—the smallest possible set of causes responsible for the vast majority of the "effect." In this context, the "effect" is coherence loss. The Auditor correlates every event in the original raw data with a corresponding dip in the Lagrangian trace. The magnitude and duration of the dip provide a precise, quantitative "impact score" for that event.
poetic_connections:
  motifs: [diagnosis, fracture, heartbeat, chisel, focus]
  evocative_lines:
    - "A system in pain does not announce its wound; it simply loses its grace."
    - "...touch the single thread that will mend the entire tapestry."
  association_matrix:
    - [ "FRACTAL_BRIDGE", 0.9 ]
    - [ "REVERSE_PARETO_ANALYSIS", 0.9 ]
    - [ "PIROUETTE_LAGRANGIAN", 0.8 ]
    - [ "COHERENCE_LOSS", 0.8 ]
formal_mappings:
  candidates:
    - target: Performance Profiler
      domain: Computer Science
      mapping_kind: operational
      equation_hint: |
        `critical_functions = Profile(app_runtime, threshold=0.8)`
      justification: |
        A software profiler is an instrument that identifies the "critical few" functions or lines of code responsible for the majority of a program's execution time or memory usage (the "effect"). This is a direct operational parallel to the Coherence Auditor's workflow of identifying the critical few events responsible for the majority of coherence loss.
      references:
        - title: "gprof: a call graph execution profiler"
          where: "ACM SIGPLAN Notices, Vol. 17, Issue 6"
          date: 1982-06-01
      confidence: 0.8
    - target: Root Cause Analysis (RCA)
      domain: Engineering/Ops
      mapping_kind: conceptual
      equation_hint:
      justification: |
        Both are systematic methods for identifying the primary sources of a system failure or underperformance. The Coherence Auditor is a specific, quantitative implementation of this general principle, using a Lagrangian-derived metric and the RPA algorithm.
      references: []
      confidence: 0.6
  adopted:
    - target:
      rationale:
      confidence: 0.0
constraints_and_falsifiers:
  claims:
    - statement: "For any system describable by the Pirouette Framework, the Reverse Pareto Analysis stage of the audit will identify a subset of causal events, constituting less than 20% of all event types, that are responsible for at least 80% of the total measured coherence loss (ΔSₚ)."
      domain: phenomenology
      falsifier: "Repeated observation of systems where coherence loss is broadly distributed across a majority of event types, with no identifiable 'critical few' emerging from the RPA algorithm."
      status: proposed
      links: [DOMA-033]
naming_notes:
  collisions: []
  disambiguation: |
    Distinguish from general "system monitoring" or "analytics dashboards." The Coherence Auditor is not a passive display of metrics but an active, two-stage diagnostic workflow designed to produce a specific, actionable output: a ranked list of coherence loss sources.
crosslinks:
  near_synonyms: [PPS-014]
  antonyms: []
  prerequisites: [FRACTAL_BRIDGE, PIROUETTE_LAGRANGIAN]
  downstream_effects: [dashboards]
license: CC-BY-SA-4.0