---
term: "Reverse Pareto Analysis"
canonical_id: "REVERSE_PARETO_ANALYSIS"
symbol: "RPA"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-051"]
---

---
term: Reverse Pareto Analysis
canonical_id: REVERSE_PARETO_ANALYSIS
symbol: RPA
aliases: []
parents: [DOMA-051]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-051
      snippet: |
        Second, use Reverse Pareto Analysis (RPA) to find where the system's actual history deviates most sharply from its geodesic. By quantifying the "coherence loss" associated with each event in the time-series, the Scalpel isolates the "critical few" events responsible for the vast majority (e.g., 80%) of the system's dissonance.
  editors: [canonical-agent]
  review_log: []
triad:
  art: |
    To find the one cracked pillar that threatens the whole cathedral. It is the art of tracing a cacophony back to the single string that snapped.
  law: |
    For any system deviating from its geodesic, a small fraction of historical events (typically <20%) will be responsible for a large majority (typically >80%) of the total cumulative coherence loss.
  philosophy: |
    RPA operationalizes the principle of causal leverage. It transforms a complex, noisy history of systemic underperformance into a short, actionable list of primary wounds, shifting focus from treating diffuse symptoms to healing the critical injuries.
pirouette_definition: |
  A diagnostic procedure within the Coherence Auditor's "Scalpel" stage that identifies the minimal set of historical events responsible for the majority of a system's cumulative deviation from its ideal coherence geodesic. It does so by quantifying the coherence loss contribution of each event in a time-series and ranking them by impact.
operational_definition:
  units: The primary metric, coherence loss, is dimensionless (as coherence is typically normalized) or measured in units of Kτ.
  symbol_table:
    - name: ΔKτ_i
      meaning: The total coherence loss attributed to a discrete event `i`.
      dimensions: dimensionless
      default_range: "[0, ∞)"
    - name: Kτ_actual(t)
      meaning: The measured coherence of the system at time `t`.
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: Kτ_geodesic(t)
      meaning: The ideal coherence of the system at time `t`, as calculated by the Pirouette Lagrangian.
      dimensions: dimensionless
      default_range: "[0, 1]"
  measurement:
    procedures:
      - name: Critical Fracture Isolation
        outline: |
          1. Acquire the complete, time-indexed history of the system's coherence, `Kτ_actual(t)`.
          2. Calculate the system's ideal coherence trajectory, `Kτ_geodesic(t)`.
          3. For each identifiable event `i` in the system's history, calculate its coherence loss contribution, `ΔKτ_i`, by integrating the absolute difference `|Kτ_geodesic(t) - Kτ_actual(t)|` over the event's duration.
          4. Rank all events by `ΔKτ_i` in descending order.
          5. Sum the `ΔKτ_i` values cumulatively until a target threshold (e.g., 80% of total loss) is reached. The events in this set are the "critical fractures."
        expected_signals: [A power-law or L-shaped distribution of `ΔKτ_i` values, where a few events dominate the total loss.]
        pitfalls: [Miscalculating the geodesic, poor event segmentation (smearing a single shock's effect over time), and mistaking temporal correlation for causality.]
context_windows:
  - module: DOMA-051
    excerpt: |
      The Scalpel is a diagnostic tool that uses the Pirouette Lagrangian (CORE-006) to move from transcription to prescription. First, locate the Geodesic... Second, use Reverse Pareto Analysis (RPA) to find where the system's actual history deviates most sharply from its geodesic... The output is a short, actionable list of the system's primary wounds.
  - module: DOMA-051
    excerpt: |
      By analyzing historical data, it might reveal that 85% of the ecosystem's deviation from this path—its loss of coherence—was caused by a single, severe drought year, highlighting a critical vulnerability.
poetic_connections:
  motifs: [critical fracture, dissonance, root cause, leverage point, the vital few]
  evocative_lines:
    - "listen for the sour notes"
    - "The output is a short, actionable list of the system's primary wounds."
  association_matrix:
    - [ "coherence_loss", 0.9 ]
    - [ "wound_channel", 0.6 ]
    - [ "geodesic", 0.8 ]
    - [ "coherence_auditor", 0.9 ]
formal_mappings:
  candidates:
    - target: Root Cause Analysis (RCA)
      domain: Systems Engineering
      mapping_kind: conceptual
      justification: |
        Both are diagnostic processes aimed at identifying primary causes rather than symptoms. RPA is a specific, quantitative form of RCA applied to the Pirouette Framework's coherence metric.
      confidence: 0.7
  adopted:
    - target: Pareto Principle (80/20 Rule)
      rationale: |
        RPA is a direct, named application of the Pareto principle. It formalizes the search for the ~20% of causes (events) that lead to ~80% of the negative effects (coherence loss). The "Reverse" in the name signifies the analytical direction: starting from the total effect and working backwards to find the minimal set of causes.
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "Coherence loss in most complex adaptive systems follows a Pareto-like distribution, being dominated by a few critical events rather than a uniform accumulation of small deviations."
      domain: phenomenology
      falsifier: "Demonstration of a class of complex systems where coherence loss is consistently and primarily caused by a diffuse, homogeneous process (e.g., 'death by a thousand cuts'), with no identifiable high-impact events ever emerging."
      status: proposed
      links: [DOMA-051]
naming_notes:
  collisions: [Robotic Process Automation, Real Property Administrator]
  disambiguation: |
    Within the Pirouette Framework, RPA is not a statistical law but a diagnostic *procedure*. It applies the well-known Pareto principle to a specific, calculated quantity: coherence loss relative to a geodesic. The analysis is "reverse" because it begins with the total observed deficit and identifies the smallest set of historical causes.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [COHERENCE, GEODESIC, COHERENCE_AUDITOR]
  downstream_effects: []
license: CC-BY-SA-4.0