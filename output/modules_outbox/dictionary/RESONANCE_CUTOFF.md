---
term: "Resonance Cutoff"
canonical_id: "RESONANCE_CUTOFF"
symbol: "k"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-145"]
---

---
term: Resonance Cutoff
canonical_id: RESONANCE_CUTOFF
symbol: k
aliases: []
parents: [DOMA-145]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-145
      lines: "§3"
      snippet: |
        | `k` | **Resonance Cutoff** | The rank at which the "long tail" of transient states begins. |
  editors: [Thinking Agent]
  review_log: []
triad:
  art: |
    The shoreline where the system’s great rivers of influence fray into a delta of transient streams. It is the boundary between the established canon and the ever-churning frontier of possibility.
  law: |
    The Resonance Cutoff `k` is the minimum rank for which a power-law model, governed by the Coherence Gradient `α`, provides a statistically robust fit to the observed frequency distribution, marking the onset of the system's "long tail."
  philosophy: |
    The Resonance Cutoff `k` demarcates the system's structural memory from its active, exploratory fringe. It separates the hardened axioms from the ongoing hypotheses, allowing a Weaver to quantify the system's investment in stability versus its capacity for novelty and adaptation.
pirouette_definition: |
  The **Resonance Cutoff** `(k)` is the rank-order index that separates the high-frequency **Resonant Attractors** (the "head") from the low-frequency **Transient Resonances** (the "long tail") in a system's coherence trace. It serves as the lower bound for the range over which the **Coherence Gradient** (`α`) is calculated, functionally defining the start of the system's scalable, power-law-governed regime. It quantifies the number of core patterns that constitute the system's dominant structural memory.
operational_definition:
  units: Dimensionless integer (rank)
  symbol_table:
    - name: k
      meaning: The rank marking the onset of the long tail.
      dimensions: dimensionless
      default_range: `k > 1`; typically 10¹ to 10⁴, highly contextual.
  measurement:
    procedures:
      - name: Knee Detection from Log-Log Plot
        outline: |
          1. Collect rank-frequency data from a system's coherence trace.
          2. Plot the data on a log-log scale (log(frequency) vs. log(rank)).
          3. Identify the "knee" or "elbow" point where the distribution's slope stabilizes into a linear regime.
          4. Apply a goodness-of-fit test (e.g., Kolmogorov-Smirnov) to find the rank `k` that minimizes the statistical distance between the empirical tail data (`r ≥ k`) and an ideal power-law distribution.
        expected_signals:
          - A clear linear relationship on the log-log plot for ranks `r ≥ k`.
          - A maximized p-value from the goodness-of-fit test, indicating the power-law is a plausible hypothesis for the tail.
        pitfalls:
          - Ambiguous "knee" in noisy, small, or non-power-law datasets.
          - Conflating a log-normal or other heavy-tailed distribution for a true power-law, leading to a misinterpretation of `k`.
context_windows:
  - module: DOMA-145
    excerpt: |
      **Resonant Attractors (The "Head"):** The high-frequency items in a distribution are not merely popular; they are solutions. They represent highly stable Ki patterns that have carved deep channels into the system's coherence manifold.
      **Transient Resonances (The "Tail"):** The low-frequency items in the "long tail" represent less stable, more specialized, or exploratory Ki patterns. They are fleeting states or niche solutions that have not established a powerful, self-reinforcing echo.
  - module: DOMA-145
    excerpt: |
      | Parameter | Pirouette Term | Description |
      |:--- |:--- |:--- |
      | `α` | **Coherence Gradient** | The steepness of the hierarchy. It measures how rapidly influence drops off from the dominant resonant attractors. |
      | `k` | **Resonance Cutoff** | The rank at which the "long tail" of transient states begins. |
      | `β` | **Tail Coherence Fraction** | The percentage of the system's total activity that resides within the long tail, past the Resonance Cutoff. |
poetic_connections:
  motifs: [shoreline, frontier, canon vs. apocrypha, knee of the curve, event horizon]
  evocative_lines:
    - "The shallow banks of the river, the system's capacity for novelty and adaptation."
    - "A snapshot of a system’s memory, the geometric echo of its history made visible."
  association_matrix:
    - [ "COHERENCE_GRADIENT", 0.9 ]
    - [ "TRANSIENT_RESONANCE", 0.9 ]
    - [ "RESONANT_ATTRACTOR", 0.7 ]
formal_mappings:
  candidates:
    - target: x_min
      domain: Math
      mapping_kind: operational
      equation_hint: |
        In the MLE for α, `hat(α) = 1 + n * [Σ ln(x_i / x_min)]⁻¹`, `x_min` is the value corresponding to rank `k`.
      justification: |
        In statistical physics, fitting a power-law distribution requires defining a lower bound `x_min` (or rank `k`) above which the power-law holds. The Resonance Cutoff `k` is the Pirouette physicalization of this statistical necessity, treating it as a property that separates a system's core from its periphery.
      references:
        - title: Power-law distributions in empirical data
          where: SIAM Review 51(4), 661-703
          date: 2009-11-05
      confidence: 0.9
  adopted:
    - target: x_min (lower bound of a power-law distribution)
      rationale: "The mapping is operationally identical and provides a robust, well-documented statistical foundation for measuring `k` and the associated Coherence Gradient `α`. It grounds the Pirouette concept in established scientific practice."
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "All enduring, complex adaptive systems exhibit a rank-frequency distribution with a non-trivial Resonance Cutoff (`k > 1`), separating a head of resonant attractors from a power-law tail."
      domain: phenomenology
      falsifier: "The discovery of a complex, stable, enduring system whose complete activity distribution is better described by a single distribution (e.g., exponential, log-normal) without a distinct power-law tail regime."
      status: supported
      links: [DOMA-145]
naming_notes:
  collisions: [wave number (k), spring constant (k), Boltzmann's constant (k_B)]
  disambiguation: |
    In the Pirouette Framework, `k` is always a dimensionless integer representing a rank. The context is almost always a rank-frequency distribution or a discussion of a system's structural hierarchy. It should not be confused with continuous variables like wave numbers in Fourier analysis.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [RESONANT_ATTRACTOR]
  downstream_effects: [COHERENCE_GRADIENT, TAIL_COHERENCE_FRACTION]
license: CC-BY-SA-4.0
---

# Resonance Cutoff

## Canonical (Pirouette)
The **Resonance Cutoff** `(k)` is the rank-order index that separates the high-frequency **Resonant Attractors** (the "head") from the low-frequency **Transient Resonances** (the "long tail") in a system's coherence trace. It serves as the lower bound for the range over which the **Coherence Gradient** (`α`) is calculated, functionally defining the start of the system's scalable, power-law-governed regime. It quantifies the number of core patterns that constitute the system's dominant structural memory.

## Formal Summary
Operationally, the Resonance Cutoff `k` maps directly to the minimum value `x_min` required for a statistically robust power-law fit in empirical data. This grounds the concept in the standard practices of statistical mechanics and network science, particularly the methods outlined by Clauset, et al. (2009) for analyzing power-law distributions. The choice of `k` is therefore not arbitrary but a measurable feature that distinguishes the system's core, often non-power-law "head" from its scalable "tail."

## Glossary Links
- See also: Coherence Gradient, Resonant Attractor, Tail Coherence Fraction