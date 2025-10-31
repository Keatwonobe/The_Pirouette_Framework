---
term: "Critical Fractures"
canonical_id: "CRITICAL_FRACTURES"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-051"]
---

---
term: Critical Fractures
canonical_id: CRITICAL_FRACTURES
symbol:
aliases: [primary wounds, deep wounds, sour notes]
parents: [DOMA-051]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-051
      lines: "L102-L106"
      snippet: |
        By quantifying the "coherence loss" associated with each event in the time-series, the Scalpel isolates the "critical few" events responsible for the vast majority (e.g., 80%) of the system's dissonance. The output is a short, actionable list of the system's primary wounds.
  editors: [chain-of-thought-agent]
  review_log: []
triad:
  art: |
    The single hairline crack in the bell that deadens its ring. A past injury that defines a present limp. Critical Fractures are the resonant scars of history, the system's most profound and defining wounds.
  law: |
    For any system whose coherence history (Kτ(t)) deviates from its geodesic (Kτ_geo(t)), a subset of discrete events accounting for ≤20% of the total event count will be responsible for ≥80% of the total integrated coherence loss, defined as ∫|Kτ(t) - Kτ_geo(t)| dt.
  philosophy: |
    History is not a uniform weight; it is a series of sharp impacts. The Critical Fractures principle asserts that system pathology is rarely a death by a thousand cuts, but a consequence of a few deep wounds. Identifying these fractures is the pivot from diagnosis to healing.
pirouette_definition: |
  The small subset of discrete historical events, identified via Reverse Pareto Analysis (RPA), that are causally responsible for the majority (typically ≥80%) of a system's cumulative deviation from its coherence geodesic. These fractures represent the most consequential points of damage or divergence in a system's history, forming the primary targets for analysis and intervention.
operational_definition:
  units: Dimensionless (units of Coherence)
  symbol_table:
    - name: ΔKτ(t)
      meaning: Instantaneous Coherence Loss
      dimensions: dimensionless
      default_range: "≥ 0"
    - name: Kτ(t)
      meaning: Actual Coherence History
      dimensions: dimensionless
      default_range: contextual
    - name: Kτ_geo(t)
      meaning: Geodesic Coherence Path
      dimensions: dimensionless
      default_range: contextual
  measurement:
    procedures:
      - name: Reverse Pareto Analysis (RPA) of Coherence History
        outline: |
          1.  Define system boundaries and map domain variables to Kτ, Γ, etc. (per DOMA-051 §3).
          2.  Transcribe historical data into a time-series of actual system coherence, Kτ(t).
          3.  Calculate the system's ideal coherence path, its geodesic Kτ_geo(t), using the Pirouette Lagrangian (CORE-006).
          4.  Compute the coherence loss time-series: ΔKτ(t) = |Kτ(t) - Kτ_geo(t)|.
          5.  Attribute integrated coherence loss (∫ΔKτ dt) to discrete, identifiable events in the system's history.
          6.  Rank events by their associated coherence loss. The top-ranked events accounting for ≥80% of the total loss are identified as the Critical Fractures.
        expected_signals: [A Pareto or power-law distribution of coherence loss when attributed to ranked historical events.]
        pitfalls: [Misattribution of coherence loss to non-causal coincident events; poorly defined system boundaries leading to an inaccurate geodesic; insufficient data resolution to isolate discrete events.]
context_windows:
  - module: DOMA-051
    excerpt: |
      Isolate the Critical Fractures: Second, use Reverse Pareto Analysis (RPA) to find where the system's actual history deviates most sharply from its geodesic. By quantifying the "coherence loss" associated with each event in the time-series, the Scalpel isolates the "critical few" events responsible for the vast majority (e.g., 80%) of the system's dissonance. The output is a short, actionable list of the system's primary wounds.
  - module: DOMA-051
    excerpt: |
      A company's stable business model is its Kτ, and market competition is its Γ. The Lens transcribes decades of financial data into a coherence signal. The Scalpel, analyzing this signal against the company's ideal path of profit maximization, might pinpoint that a single, ill-advised acquisition is the critical fracture responsible for the majority of subsequent market share loss.
poetic_connections:
  motifs: [fracture, wound, scar, dissonance, echo, pivot-point, historical trauma]
  evocative_lines:
    - "listen for the sour notes"
    - "find the deepest fractures revealed by the dissonance in that song"
    - "a short, actionable list of the system's primary wounds"
  association_matrix:
    - [ "GEODESIC", 0.9 ]
    - [ "WOUND_CHANNEL", 0.8 ]
    - [ "COHERENCE_LOSS", 1.0 ]
    - [ "REVERSE_PARETO_ANALYSIS", 1.0 ]
formal_mappings:
  candidates:
    - target: Anomalous Event / Change Point Detection
      domain: Statistics|Signal Processing
      mapping_kind: operational
      equation_hint:
      justification: |
        The procedure for identifying Critical Fractures is operationally equivalent to change point detection algorithms that locate discrete points in a time series responsible for a significant shift in the signal's statistical properties. Here, the "shift" is the deviation from a predicted baseline (the geodesic), and the "Pareto" aspect adds a specific constraint on the expected distribution of these events' impact.
      references:
        - title: "Detection of Abrupt Changes: Theory and Application"
          where: "Prentice-Hall"
          date: 1993-01-01
      confidence: 0.7
  adopted:
    - target:
      rationale:
      confidence: 0.0
constraints_and_falsifiers:
  claims:
    - statement: "The distribution of coherence loss attributed to discrete events in any sufficiently complex system will follow a Pareto-like distribution (e.g., 80/20 rule), meaning a small number of Critical Fractures account for the vast majority of the system's total deviation from its geodesic."
      domain: phenomenology
      falsifier: "Discovery of a class of complex systems where coherence loss is consistently and broadly distributed, with no identifiable 'critical few' events causing disproportionate damage (i.e., where 'death by a thousand cuts' is the norm)."
      status: proposed
      links: [DOMA-051]
naming_notes:
  collisions: [criticality (complex systems), fracture mechanics (materials science)]
  disambiguation: |
    Distinguish from 'criticality,' a state of a system at a phase transition. A Critical Fracture is a discrete, historical event that caused a lasting deviation from an ideal path, not a continuous state of the system itself.
crosslinks:
  near_synonyms: []
  antonyms: [GEODESIC_FLOW]
  prerequisites: [GEODESIC, COHERENCE, PIROUETTE_LAGRANGIAN, WOUND_CHANNEL]
  downstream_effects: []
license: CC-BY-SA-4.0
---

# Critical Fractures

## Canonical (Pirouette)
The small subset of discrete historical events, identified via Reverse Pareto Analysis (RPA), that are causally responsible for the majority (typically ≥80%) of a system's cumulative deviation from its coherence geodesic. These fractures represent the most consequential points of damage or divergence in a system's history, forming the primary targets for analysis and intervention.

## EFT-First Summary
No formal mapping to Effective Field Theory has been adopted. Operationally, the concept is analogous to anomalous event or change point detection in time-series analysis and statistics.

## Glossary Links
- See also: [[Geodesic]], [[Coherence]], [[Wound Channel]], [[Reverse Pareto Analysis]]