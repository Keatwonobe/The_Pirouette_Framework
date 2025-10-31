---
term: "Tail Coherence Fraction"
canonical_id: "TAIL_COHERENCE_FRACTION"
symbol: "β"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-145"]
---

---
term: Tail Coherence Fraction
canonical_id: TAIL_COHERENCE_FRACTION
symbol: β
aliases: []
parents: ['DOMA-145']
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-145
      snippet: |
        | `β` | **Tail Coherence Fraction** | The percentage of the system's total activity that resides within the long tail, past the Resonance Cutoff. |
  editors: ['system-agent']
  review_log: []
triad:
  art: |
    The tail is the sea of possibilities from which new peaks may arise. It is the system's capacity for surprise, the quiet hum of untried paths and forgotten echoes that constitutes the reservoir of its future.
  law: |
    The Tail Coherence Fraction (β) is the ratio of total activity from all elements beyond the Resonance Cutoff (k) to the system's total activity. A high β indicates a "democratic" system rich in novelty and resilience; a low β indicates an "aristocratic" system dominated by a few efficient, core patterns.
  philosophy: |
    β measures a system's investment in its own latent potential. It quantifies the fundamental trade-off between exploiting established, efficient patterns (the head) and exploring a diverse reservoir of adaptive options (the tail). This balance is a primary determinant of a system's long-term endurance.
pirouette_definition: |
  The percentage of a system's total activity or coherence that is distributed among the low-frequency, high-rank elements of its resonant hierarchy. It quantifies the cumulative influence of all transient resonances that exist past the Resonance Cutoff (k). While the Coherence Gradient (α) describes the *shape* of the influence hierarchy, β measures the *magnitude* of the system's investment in its exploratory periphery versus its stable, resonant core.
operational_definition:
  units: Dimensionless (ratio)
  symbol_table:
    - name: β
      meaning: Tail Coherence Fraction
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: k
      meaning: Resonance Cutoff (rank)
      dimensions: dimensionless
      default_range: "contextual"
    - name: A_total
      meaning: Total system activity
      dimensions: "contextual (e.g., energy, frequency, flow)"
      default_range: "> 0"
    - name: A_tail
      meaning: Sum of activity for all elements with rank r > k
      dimensions: "contextual (same as A_total)"
      default_range: "[0, A_total]"
  measurement:
    procedures:
      - name: Direct Summation from Coherence Trace
        outline: |
          1. Collect a rank-frequency (or rank-activity) distribution from a system's activity log.
          2. Determine the Resonance Cutoff (k), the rank at which the power-law tail begins.
          3. Sum the activity of all elements to get total activity, A_total.
          4. Sum the activity of all elements with rank r > k to get tail activity, A_tail.
          5. Calculate β as the ratio: β = A_tail / A_total.
        expected_signals: ['Power-law signature in rank-frequency plot', 'Discernible "knee" or change in slope near the Resonance Cutoff']
        pitfalls: ['Ambiguous or unstable Resonance Cutoff (k)', 'Insufficient data to populate a statistically significant tail', 'System activity does not follow a power-law distribution']
context_windows:
  - module: DOMA-145
    excerpt: |
      The low-frequency items in the "long tail" represent less stable, more specialized, or exploratory Ki patterns. They are fleeting states or niche solutions that have not established a powerful, self-reinforcing echo. They represent the shallow banks of the river, the system's capacity for novelty and adaptation.
  - module: DOMA-145
    excerpt: |
      A Shallow Gradient (α > 2): A "democratic" system, where coherence is distributed more evenly across many patterns. This structure is more resilient and adaptive, but may be less efficient and more prone to Turbulent Flow as competing patterns create friction. It is a "democracy of the many."
poetic_connections:
  motifs: ['novelty', 'exploration', 'democracy', 'periphery', 'latent potential', 'reservoir']
  evocative_lines:
    - "They represent the shallow banks of the river, the system's capacity for novelty and adaptation."
    - "It is a 'democracy of the many.'"
  association_matrix:
    - [ "RESONANCE_CUTOFF", 0.9 ]
    - [ "COHERENCE_GRADIENT", 0.8 ]
    - [ "TURBULENT_FLOW", 0.6 ]
    - [ "RESONANT_ATTRACTOR", 0.5 ]
formal_mappings:
  candidates: []
  adopted:
    - target: P(rank > k)
      domain: Math
      mapping_kind: mathematical
      equation_hint: |
        β = Σ_{r=k+1 to N} f(r)
      rationale: |
        The Tail Coherence Fraction is a direct physical re-interpretation of a standard statistical quantity: the cumulative probability mass of the tail of a rank-frequency distribution. It measures the fraction of events/activity that fall beyond a certain rank `k`.
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "Systems with a higher Tail Coherence Fraction (β > 0.4) exhibit greater resilience to the disruption of high-rank Resonant Attractors."
      domain: phenomenology
      falsifier: "A controlled study shows that systems with low β (< 0.1) recover faster or more completely from the removal of their top-ranked element than systems with high β, holding other factors constant."
      status: proposed
      links: ['DOMA-145']
naming_notes:
  collisions: ['The symbol β is overloaded in physics (relativistic velocity, thermodynamic beta 1/kT, beta decay).']
  disambiguation: |
    In the Pirouette context, β is always a dimensionless fraction in the range [0, 1] describing activity distribution in a hierarchy. It is typically discussed alongside the Coherence Gradient (α) and Resonance Cutoff (k), which distinguishes it from thermodynamic or relativistic uses.
crosslinks:
  near_synonyms: []
  antonyms: ['HEAD_COHERENCE_FRACTION']
  prerequisites: ['RESONANCE_CUTOFF', 'COHERENCE_GRADIENT']
  downstream_effects: ['TURBULENT_FLOW']
license: CC-BY-SA-4.0