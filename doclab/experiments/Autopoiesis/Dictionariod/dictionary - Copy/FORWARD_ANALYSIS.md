---
term: "Forward Analysis"
canonical_id: "FORWARD_ANALYSIS"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-145"]
---

---
term: Forward Analysis
canonical_id: FORWARD_ANALYSIS
symbol: 
aliases: [Reading the Echo]
parents: [DOMA-145]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-145
      lines: "L65-L68"
      snippet: |
        ### 4.1 · Forward Analysis: Reading the Echo

        This protocol measures the system's current state to diagnose its structural character.
  editors: [Weaver-Core-Indexer]
  review_log: []
triad:
  art: |
    To read the shape of a riverbed and know the story of the river without having seen it flow; to diagnose a system's soul from the geometric echo of its collective choices.
  law: |
    A system's rank-frequency distribution, when measured, reveals its Coherence Gradient (α), quantifying the concentration of influence in its resonant attractors. The value of α directly correlates to the system's structural stability, fragility, and efficiency.
  philosophy: |
    History is not past; it is embodied in present structure. Forward Analysis asserts that a system's current state is a readable map of its accumulated coherence-seeking behavior, allowing a Weaver to diagnose its health and predict its future without needing a complete temporal record.
pirouette_definition: |
  A diagnostic protocol for quantifying a system's current structural character by measuring the Coherence Gradient (α) from its rank-frequency distribution. The analysis proceeds 'forward' from an observed coherence trace (a log of system activity) to an interpretation of its underlying coherence dynamics, such as its efficiency, stability, and the dominance of its Resonant Attractors.
operational_definition:
  units: Dimensionless parameters
  symbol_table:
    - name: α
      meaning: Coherence Gradient
      dimensions: dimensionless
      default_range: contextual, typically (1, 3]
  measurement:
    procedures:
      - name: Coherence Gradient Estimation
        outline: |
          1.  Collect rank-frequency data from a system's coherence trace.
          2.  Apply a Maximum Likelihood Estimator (MLE) to the data to calculate α.
          3.  Interpret the resulting α value against known baselines for the system type (e.g., steep vs. shallow gradient).
        expected_signals: [A rank-frequency distribution that approximates a power law.]
        pitfalls: [Insufficient data leading to inaccurate α estimation, Misidentifying the distribution type (e.g., log-normal instead of power-law).]
context_windows:
  # Short, trimmed context quotes harvested from modules (3–6 sentences each).
  - module: DOMA-145
    excerpt: |
      This protocol measures the system's current state to diagnose its structural character.
      1.  **Map Resonances:** Collect rank-frequency data from the system's activity log (its "coherence trace").
      2.  **Estimate Gradient:** Calculate the Coherence Gradient (`α`), typically using the robust Maximum Likelihood Estimation (MLE) method.
      3.  **Interpret Structure:** The value of `α` is a critical indicator of systemic health...
  - module: DOMA-145
    excerpt: |
      A list of cities by population, of words by frequency, of websites by traffic—these are not random assortments. They are snapshots of a system’s memory, the geometric echo of its history made visible. This module provides the instrument to map this invisible architecture. It reframes the statistical phenomenon of a power-law (or Zipfian) distribution as the tangible footprint of a system's underlying coherence dynamics.
poetic_connections:
  # Lightweight "word-association graph" and sticky lines.
  motifs: [scrying, reading echoes, structural memory, riverbed geometry]
  evocative_lines:
    - "The shape of a riverbed tells the story of the river."
    - "By measuring this one number, α, we are not just fitting a curve; we are taking a core sample of the system's soul."
  association_matrix:
    # symmetric or directed; weights in [0,1]
    - [ "COHERENCE_GRADIENT", 1.0 ]
    - [ "STRUCTURAL_MEMORY", 0.9 ]
    - [ "RESONANT_ATTRACTOR", 0.8 ]
formal_mappings:
  # Candidate alignments to EFT/SM/CM/GR terms, each with justification and refs.
  candidates: []
  adopted:
    - target: Power-law exponent (α)
      domain: Statistical Mechanics|Complex Systems
      mapping_kind: operational
      equation_hint: |
        $$ \hat\alpha = 1 + n\biggl[\sum_{i=1}^n\ln\frac{x_i}{x_{\min}}\biggr]^{-1} $$
      rationale: |
        The mathematical and procedural basis is identical to standard statistical methods for analyzing power-law distributions. The Pirouette Framework re-contextualizes the exponent as a physical property ('Coherence Gradient') emerging from Lagrangian dynamics, but the measurement protocol is a direct adoption of the robust Maximum Likelihood Estimation method.
      references:
        - title: "Power-law distributions in empirical data"
          where: "SIAM Review 51(4), 661-703"
          date: 2009-11-10
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The Coherence Gradient (α) of a stable system is a conserved quantity under a static set of environmental pressures (V_Γ)."
      domain: phenomenology
      falsifier: "Observing significant, unprompted drift in α for a system believed to be in equilibrium, or observing that α fails to shift predictably when V_Γ is deliberately altered."
      status: proposed
      links: [DOMA-145, CORE-006]
naming_notes:
  collisions: [The term "Forward Analysis" is used in program analysis and finance.]
  disambiguation: |
    In Pirouette, 'Forward' specifically means reasoning from an observed data trace *forward* to a structural conclusion. This is in contrast to 'Inverse Analysis,' which reasons from a desired structural outcome *backward* to the required system parameters.
crosslinks:
  near_synonyms: []
  antonyms: [INVERSE_ANALYSIS]
  prerequisites: [COHERENCE_GRADIENT, RESONANT_ATTRACTOR, COHERENCE_TRACE]
  downstream_effects: [LAMINAR_FLOW, TURBULENT_FLOW, STAGNATION]
license: CC-BY-SA-4.0
---

# Forward Analysis

## Canonical (Pirouette)
A diagnostic protocol for quantifying a system's current structural character by measuring the Coherence Gradient (α) from its rank-frequency distribution. The analysis proceeds 'forward' from an observed coherence trace (a log of system activity) to an interpretation of its underlying coherence dynamics, such as its efficiency, stability, and the dominance of its Resonant Attractors.

## EFT-First Summary
Forward Analysis is the Pirouette protocol for measuring the power-law exponent (`α`) of a system's rank-frequency distribution. The procedure uses a standard Maximum Likelihood Estimator (see Clauset et al., 2009) to quantify the "Coherence Gradient," which is interpreted as a physical property reflecting the system's structural memory and stability.

## Glossary Links
- See also: [Inverse Analysis](INVERSE_ANALYSIS), [Coherence Gradient](COHERENCE_GRADIENT), [Resonant Attractor](RESONANT_ATTRACTOR)