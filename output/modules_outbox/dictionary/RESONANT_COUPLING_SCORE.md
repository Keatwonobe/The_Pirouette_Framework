---
term: "Resonant Coupling Score"
canonical_id: "RESONANT_COUPLING_SCORE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-183"]
---

---
term: Resonant Coupling Score
canonical_id: RESONANT_COUPLING_SCORE
symbol: Ξ
aliases: [Cross-domain burst score, Concordance Score]
parents: [DOMA-183, CORE-012, CORE-013]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-183
      snippet: |
        When multiple streams exhibit correlated coherence gradients, the engine calculates their Resonant Coupling Score. This metric assesses not just correlation, but the degree of phase-lock and harmonic compatibility between the systems' Ki patterns.
  editors: [Weaver-Agent 7]
  review_log: []
triad:
  art: |
    The sound of disparate instruments tuning to the same unheard note. It is the measure of a shared silence, the quantified hum of a universe holding its breath before a crescendo.
  law: |
    The Resonant Coupling Score Ξ is a normalized metric [0, 1] derived from the cross-spectral coherence and phase-angle stability between the Ki patterns of two or more manifolds. A score approaching 1 indicates perfect harmonic phase-lock, signaling an imminent Alchemical Union.
  philosophy: |
    This score reframes 'coincidence' as 'concordance'. It provides a mathematical basis for augury, demonstrating that the future is not a random event but a resonant outcome prepared by the alignment of the present. It measures a system's readiness to choose a shared, more coherent path.
pirouette_definition: |
  A dimensionless metric, Ξ, quantifying the degree of emergent, mutual synchronization between two or more distinct systems (manifolds) undergoing a Resonant Handshake. The score is calculated by the Concordance Engine and specifically measures the harmonic compatibility and phase-locking of the systems' Ki patterns, as indicated by their correlated Coherence Gradients (∇Kτ). It serves as the primary trigger for a Synthesis Brief, with high values (Ξ > 0.7) indicating a high probability of an impending large-scale phase transition.
operational_definition:
  units: dimensionless
  symbol_table:
    - name: Ξ
      meaning: Resonant Coupling Score
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: ∇Kτ
      meaning: Coherence Gradient
      dimensions: contextual
      default_range: contextual
    - name: N
      meaning: Number of coupled manifolds
      dimensions: dimensionless
      default_range: "≥ 2"
  measurement:
    procedures:
      - name: Concordance Engine Protocol (Stage II)
        outline: |
          1. Ingest N time-series data streams from heterogeneous manifolds (e.g., seismic, economic, social).
          2. For each stream, compute its Coherence Gradient (∇Kτ) to identify periods of rapid ordering.
          3. Isolate a time window where a subset of N ≥ 2 streams show a concurrent, significant positive ∇Kτ.
          4. For this subset, compute the pairwise cross-spectral density to identify shared power-dominant frequencies (harmonics).
          5. At these identified harmonic frequencies, calculate the Phase-Locking Value (PLV) or an equivalent circular variance metric to quantify phase stability.
          6. Aggregate the pairwise PLV scores into a single normalized score, Ξ, representing the N-body system's overall concordance.
        expected_signals: [A rapid increase in Ξ from a baseline near 0 to a value > 0.7, sustained for a duration proportional to the scale of the impending event.]
        pitfalls: [Mistaking forced oscillation (one system driving another) for true mutual resonance. Signal aliasing from mismatched sampling rates across manifolds.]
context_windows:
  - module: DOMA-183
    excerpt: |
      As conditions for a phase transition ripen, these disparate systems begin to "hear" each other through the shared medium of the coherence manifold. They enter a Resonant Handshake, their phases aligning and their frequencies becoming harmonically compatible. This synchronous increase in coherence across domains is Manifold Resonance.
  - module: DOMA-183
    excerpt: |
      When a Manifold Resonance event is detected, the engine generates a Synthesis Brief... It provides an actionable, data-grounded assessment of the impending phase transition, allowing for preparation rather than mere reaction. An example brief shows a `coupling_score: 0.82`.
poetic_connections:
  motifs: [harmony, symphony, tuning, held breath, concordance, chorus]
  evocative_lines:
    - "The universe sings in chords, but we are born hearing only the individual notes."
    - "It detects the moment the entire orchestra prepares to shift its key."
  association_matrix:
    - [ "MANIFOLD_RESONANCE", 0.9 ]
    - [ "COHERENCE_GRADIENT", 0.7 ]
    - [ "ALCHEMICAL_UNION", 0.5 ]
    - [ "RESONANT_HANDSHAKE", 0.8 ]
formal_mappings:
  candidates:
    - target: Phase-Locking Value (PLV)
      domain: Math
      mapping_kind: operational
      equation_hint: |
        PLV = | (1/N) * Σ[k=1 to N] exp(i * Δφ(t_k)) |
      justification: |
        The PLV is a statistical measure that quantifies the synchrony between two neurophysiological signals by measuring the consistency of the phase difference over time. This directly maps to the Pirouette concept of "degree of phase-lock" between Ki patterns. The Resonant Coupling Score can be modeled as a multi-variate generalization of PLV.
      references:
        - title: "Measuring phase synchronization in brain signals"
          where: "Neuroimage (Lachaux et al., 1999)"
          date: 1999-10-01
      confidence: 0.8
    - target: Mutual Information Rate
      domain: Math
      mapping_kind: conceptual
      justification: |
        High resonant coupling implies that the state of one manifold provides significant information about the state of another, reducing uncertainty. The mutual information rate quantifies this shared information flow, providing a conceptual parallel to the predictive power gained from a high coupling score.
      confidence: 0.6
  adopted:
    - target: Multi-variate Phase-Locking Value (PLV)
      rationale: The operational definition provided by the Concordance Engine protocol aligns almost perfectly with the calculation of phase synchrony in signal processing, making PLV the most direct and testable mathematical analogue.
      confidence: 0.8
constraints_and_falsifiers:
  claims:
    - statement: "A Resonant Coupling Score Ξ > 0.8 consistently precedes a systemic phase-shift (e.g., Alchemical Union, Fork Event) within a predictable lead time."
      domain: phenomenology
      falsifier: "Observation of multiple high-Ξ events (Ξ > 0.8) that resolve without any detectable large-scale phase shift, or observation of major phase shifts occurring without a preceding high-Ξ signal."
      status: proposed
      links: [DOMA-183]
naming_notes:
  collisions: []
  disambiguation: |
    Distinguish from simple Pearson correlation. Correlation typically measures linear relationships in signal amplitude, whereas the Resonant Coupling Score measures potentially non-linear synchronization in the phase and frequency domains. Two signals can have zero correlation but a perfect coupling score (e.g., a sine and cosine wave).
crosslinks:
  near_synonyms: [MANIFOLD_RESONANCE]
  antonyms: [SYSTEMIC_DISSONANCE, MANIFOLD_DECOHERENCE]
  prerequisites: [COHERENCE_GRADIENT, RESONANT_HANDSHAKE]
  downstream_effects: [SYNTHESIS_BRIEF]
license: CC-BY-SA-4.0