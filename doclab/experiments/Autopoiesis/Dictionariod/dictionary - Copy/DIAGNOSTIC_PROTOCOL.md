---
term: "Diagnostic Protocol"
canonical_id: "DIAGNOSTIC_PROTOCOL"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-174"]
---

---
term: Diagnostic Protocol
canonical_id: DIAGNOSTIC_PROTOCOL
symbol: 
aliases: [Pareto Probe, Reverse Pareto Analysis]
parents: [DYNA-003]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-174
      lines: "§3"
      snippet: |
        The Probe provides a clean, four-step workflow...
        Step I: Define and Measure Coherence (`Kτ`)
        Step II: Attribute Coherence Loss (`ΔKτ`)
        Step III: Rank by Impact
        Step IV: Identify the Vital Few
  editors: [Agent Scribe-Class]
  review_log: []
triad:
  art: |
    A system in pain is a symphony of noise. The fool tries to quiet every instrument. The master listens for the one string that is out of tune.
  law: |
    In any system exhibiting coherence loss, a subset of causes accounting for no more than 20% of unique event types will be responsible for at least 80% of the total magnitude of coherence loss (`ΔKτ`).
  philosophy: |
    In a universe of finite energy and infinite problems, this is the law of the lever applied to the act of healing. It directs finite effort toward the point of maximum leverage, transforming analysis from a passive mapping of what is to an active strategy for what to do.
pirouette_definition: |
  The four-step workflow for diagnosing systemic health by identifying the critical few sources responsible for the majority of a system's coherence loss. The protocol moves from a general symptom (e.g., turbulence, stagnation) to a precise, actionable cause by (I) defining and measuring the system's primary output as a time-series of coherence (`Kτ`), (II) attributing every discrete drop in coherence (`ΔKτ`) to a specific causal event, (III) ranking all causal event types by their cumulative negative impact, and (IV) identifying the "vital few" bottlenecks that exist above a Pareto frontier (typically the top 80% of total loss).
operational_definition:
  units: The output is a ranked list. Intermediate measurements (`ΔKτ`) share the same context-dependent units as coherence (`Kτ`), e.g., tasks/hour, signal-to-noise ratio, bits/second.
  symbol_table:
    - name: Kτ
      meaning: Systemic Coherence; a measure of a system's primary output or health over time.
      dimensions: Context-dependent
      default_range: Context-dependent
    - name: ΔKτ
      meaning: Coherence Loss; the change in coherence attributed to a discrete event.
      dimensions: Same as Kτ
      default_range: Context-dependent
  measurement:
    procedures:
      - name: Pareto Probe Application
        outline: |
          1. Instrument the system to produce a time-series of its primary output (`Kτ`).
          2. Concurrently, create a timestamped log of all potentially relevant internal and external events.
          3. Correlate negative changes (`ΔKτ`) in the coherence time-series with events from the log, creating a ledger of `(event_type, ΔKτ_magnitude)`.
          4. Group events by type and sum their `ΔKτ` magnitudes to get total loss per type.
          5. Sort event types in descending order of total loss. The top items are the primary bottlenecks.
        expected_signals: [A power-law distribution of impact across event types, a clear "knee" in the cumulative loss curve.]
        pitfalls: [Incorrectly identifying the primary output (`Kτ`), leading to a meaningless metric; incomplete or low-resolution event logging, leading to misattribution of cause; slavish devotion to the 80/20 ratio instead of identifying the natural frontier in the data.]
context_windows:
  # Short, trimmed context quotes harvested from modules (3–6 sentences each).
  - module: DOMA-174
    excerpt: |
      A bottleneck is a geometric feature in the coherence manifold that forces the system off its geodesic. It is a point of high friction, a "coherence dam" that introduces turbulence and dissonance. Each encounter with a bottleneck exacts a cost, causing a sharp, measurable drop in the system's coherence (`Kτ`).
  - module: DOMA-174
    excerpt: |
      The output of the Pareto Probe is not an abstract exponent or a complex map. It is a simple, profoundly actionable list. This output gives the Weaver a precise target. It makes clear that improving a minor issue will have a marginal effect compared to solving the primary bottleneck.
poetic_connections:
  # Lightweight "word-association graph" and sticky lines.
  motifs: [surgeon's insight, fracture, bottleneck, dissonance, the vital few, leverage point]
  evocative_lines:
    - "The fool tries to quiet every instrument. The master listens for the one string that is out of tune."
    - "It is a diagnostic protocol for moving from the symptom—a general loss of coherence—to the source."
  association_matrix:
    # symmetric or directed; weights in [0,1]
    - [ "COHERENCE_LOSS", 0.9 ]
    - [ "BOTTLENECK", 0.9 ]
    - [ "DAEDALUS_GAMBIT", 0.7 ]
    - [ "LAMINAR_FLOW", 0.5 ]
formal_mappings:
  # Candidate alignments to EFT/SM/CM/GR terms, each with justification and refs.
  candidates:
    - target: Failure Mode and Effects Analysis (FMEA)
      domain: Engineering|Quality Control
      mapping_kind: operational
      equation_hint: |
        Risk Priority Number (RPN) = Severity × Occurrence × Detection
      justification: |
        FMEA is a systematic, proactive method for evaluating a process to identify where and how it might fail. Like the Diagnostic Protocol, it ranks potential failures to prioritize problems for corrective action. The protocol's `ΔKτ` is analogous to a combination of Severity and Occurrence.
      references:
        - title: Potential Failure Mode and Effects Analysis (FMEA), 4th Edition
          where: Automotive Industry Action Group (AIAG)
          date: 2008-06-01
      confidence: 0.8
  adopted:
    - target: Pareto Principle (80/20 Rule)
      rationale: The protocol is a direct, named application of the Pareto Principle to systemic diagnostics, explicitly using the 80/20 distribution as its primary heuristic for identifying the "vital few" causes. This is the core intellectual heritage of the method.
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "The distribution of coherence loss across causal events in a complex adaptive system will reliably approximate a Pareto distribution."
      domain: phenomenology
      falsifier: "The discovery of a significant class of complex systems where coherence loss is consistently and irreducibly distributed evenly (i.e., a uniform or Gaussian distribution) across a large number of independent, low-impact causes."
      status: supported
      links: [DOMA-174]
naming_notes:
  collisions: [Pareto Optimality]
  disambiguation: |
    The Diagnostic Protocol uses the Pareto *Principle* (a statistical observation about distribution, also known as the 80/20 rule) to find sources of failure. This should not be confused with Pareto *Optimality* or Pareto *Efficiency*, an economic concept describing a state where no individual can be made better off without making someone else worse off. This protocol is for diagnosis, not resource allocation optimization.
crosslinks:
  near_synonyms: [BOTTLENECK_ANALYSIS]
  antonyms: [SYSTEMIC_REDUNDANCY, GRACEFUL_DEGRADATION]
  prerequisites: [COHERENCE, LAMINAR_FLOW, IDENTIFY_PRIMARY_OUTPUT]
  downstream_effects: [DAEDALUS_GAMBIT]
license: CC-BY-SA-4.0
---

# Diagnostic Protocol

## Canonical (Pirouette)
The four-step workflow for diagnosing systemic health by identifying the critical few sources responsible for the majority of a system's coherence loss. The protocol moves from a general symptom (e.g., turbulence, stagnation) to a precise, actionable cause by (I) defining and measuring the system's primary output as a time-series of coherence (`Kτ`), (II) attributing every discrete drop in coherence (`ΔKτ`) to a specific causal event, (III) ranking all causal event types by their cumulative negative impact, and (IV) identifying the "vital few" bottlenecks that exist above a Pareto frontier (typically the top 80% of total loss).

## EFT-First Summary
The Diagnostic Protocol is an operationalization of the **Pareto Principle** (the 80/20 rule), applying it to diagnose failures in complex systems. It treats systemic problems not as a diffuse fog but as a set of discrete, high-impact events. By measuring a primary system output and logging all potential causal events, it ranks the causes of failure by their measured impact, allowing for focused, high-leverage interventions. This method is operationally similar to Failure Mode and Effects Analysis (FMEA) in engineering quality control.

## Glossary Links
- See also: [Bottleneck](link), [Coherence](link), [Daedalus Gambit](link)