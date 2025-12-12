---
term: "Inter-Scale Coherence"
canonical_id: "INTER_SCALE_COHERENCE"
symbol: "T_a_scale"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-136"]
---

---
term: Inter-Scale Coherence
canonical_id: INTER_SCALE_COHERENCE
symbol: T_a_scale
aliases: []
parents: [DOMA-136]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-136
      lines: "L45-L50"
      snippet: |
        Inter-Scale Coherence `(T_a_scale)`: This measures the fidelity of the self-similar pattern across different scales. It is the signal-to-noise ratio of the generative grammar itself. A high `T_a_scale` signifies a pure, well-preserved rule, like a crystal. A low `T_a_scale` suggests a more organic, noisy process, like a tree whose branches are shaped by the wind.
  editors: [system]
  review_log: []
triad:
  art: |
    The clarity of a single song played across many octaves. It is the difference between a perfect crystal and a wind-gnarled tree; one echoes a pure, unbroken rule, while the other shows a rule bent by circumstance.
  law: |
    A system's Inter-Scale Coherence is a dimensionless value between 0 and 1, quantifying the statistical self-similarity of its structure or dynamics across a specified range of scales. A value approaching 1 indicates perfect, noise-free replication of the generative rule, while values approaching 0 indicate a breakdown in self-similarity.
  philosophy: |
    This metric reveals the integrity of a system's underlying generative logic. It distinguishes between systems that rigidly enforce their own rules (high coherence) and those that adapt or degrade their rules under environmental pressure (low coherence), mapping the generative process back to the Pirouette Lagrangian.
pirouette_definition: |
  A dimensionless measure, symbolized T_a_scale, quantifying the fidelity of a self-similar generative rule as it propagates across different scales within a system. It represents the signal-to-noise ratio of the recursive grammar, distinguishing between the pure, crystal-like repetition of a rule (T_a_scale → 1) and its noisy, organic, or environmentally distorted expression (T_a_scale → 0).
operational_definition:
  units: dimensionless
  symbol_table:
    - name: T_a_scale
      meaning: Inter-Scale Coherence
      dimensions: dimensionless
      default_range: "[0, 1]"
  measurement:
    procedures:
      - name: Detrended Fluctuation Analysis (DFA)
        outline: |
          Integrate the signal and divide it into non-overlapping windows of length `n`. In each window, fit a polynomial trend and subtract it. Calculate the root-mean-square fluctuation, F(n), of the detrended signal. T_a_scale is inferred from the linearity of the log-log plot of F(n) vs. `n`, where a perfectly straight line over the measured scales indicates T_a_scale ≈ 1.
        expected_signals: [A power-law relationship F(n) ∝ n^H, where H is the Hurst exponent.]
        pitfalls: [Crossovers in the scaling plot indicate different correlation properties at different scales, complicating a single T_a_scale value. Sensitive to non-stationarities.]
      - name: Wavelet Transform Modulus Maxima (WTMM)
        outline: |
          Apply a continuous wavelet transform to the signal. Trace the maxima of the wavelet transform modulus across all scales to form "maxima lines." Analyze the scaling of a partition function Z(q, a) based on these maxima, where 'a' is the scale. High Inter-Scale Coherence corresponds to a stable, non-varying scaling exponent across a wide range of 'a'.
        expected_signals: [A consistent power-law scaling of the partition function Z(q,a) with scale 'a'.]
        pitfalls: [Results can be sensitive to the choice of the mother wavelet. Edge effects in finite data sets can distort maxima lines.]
context_windows:
  - module: DOMA-136
    excerpt: |
      Inter-Scale Coherence `(T_a_scale)`: This measures the fidelity of the self-similar pattern across different scales. It is the signal-to-noise ratio of the generative grammar itself. A high `T_a_scale` signifies a pure, well-preserved rule, like a crystal. A low `T_a_scale` suggests a more organic, noisy process, like a tree whose branches are shaped by the wind.
  - module: DOMA-136
    excerpt: |
      This equation formalizes the Fractal Geodesic... a pattern's complexity (`D_f`) is amplified by a strong generative rhythm (`ω_g`) and a highly coherent recursive rule (`T_a_scale`), but is ultimately bounded and shaped by the pressure of its environment (`Γ`).
poetic_connections:
  motifs: [echo fidelity, signal vs noise, crystal vs tree, grammatical purity]
  evocative_lines:
    - "the signal-to-noise ratio of the generative grammar itself."
    - "a pure, well-preserved rule, like a crystal."
  association_matrix:
    - [ "SCALE_INVARIANT_GEODESIC", 0.9 ]
    - [ "COHERENCE_COMPLEXITY", 0.8 ]
    - [ "TEMPORAL_PRESSURE", 0.6 ]
    - [ "GENERATIVE_RHYTHM", 0.5 ]
formal_mappings:
  candidates:
    - target: Renormalization Group (RG) fixed-point stability
      domain: EFT
      mapping_kind: conceptual
      equation_hint:
      justification: |
        A scale-invariant system is described by a fixed point of the RG flow. T_a_scale conceptually maps to the stability of this fixed point. A high T_a_scale implies the system remains close to the fixed point across many scales, while a low T_a_scale suggests relevant operators are causing the system to flow away from the fixed point as the scale changes.
      references:
        - title: Lectures on Phase Transitions and the Renormalization Group
          where: Chapter 6
          date: 1992-01-01
      confidence: 0.7
  adopted:
    - target: Hurst Exponent (H)
      rationale: |
        Provides a direct, quantifiable, and widely-used method (e.g., DFA) for measuring the degree of self-similarity and long-range correlation in a signal, which aligns precisely with the operational goal of T_a_scale. T_a_scale can be formalized as a function of the goodness-of-fit for the power-law F(n) ∝ n^H over the relevant scales.
      confidence: 0.8
constraints_and_falsifiers:
  claims:
    - statement: "In systems governed by a Scale-Invariant Geodesic, a sustained increase in ambient Temporal Pressure (Γ) will lead to a quantifiable decrease in Inter-Scale Coherence (T_a_scale)."
      domain: phenomenology
      falsifier: "Observation of multiple systems where increasing environmental noise, stress, or constraint (higher Γ) leads to no change or an increase in T_a_scale, contradicting the model's assumption that environmental pressure distorts the generative grammar."
      status: proposed
      links: [DOMA-136]
naming_notes:
  collisions: [The term "Coherence" is used broadly in physics (e.g., quantum coherence, coherence length). T_a_scale specifically refers to self-similarity across scales.]
  disambiguation: |
    Distinct from Coherence Complexity (D_f), which measures *how much space* a pattern fills. Inter-Scale Coherence measures *how faithfully* the pattern's generative rule is repeated at different sizes. A simple, straight line has a perfect T_a_scale=1 but a low D_f=1. A complex coastline has high D_f but may have lower T_a_scale than a mathematically perfect Koch curve.
crosslinks:
  near_synonyms: [SELF_SIMILARITY, SCALE_INVARIANCE]
  antonyms: [SCALE_DEPENDENCE, DECOHERENCE]
  prerequisites: [PRINCIPLE_OF_CORRESPONDENCE, PIROUETTE_LAGRANGIAN]
  downstream_effects: [COHERENCE_COMPLEXITY]
license: CC-BY-SA-4.0
---

# Inter-Scale Coherence

## Canonical (Pirouette)
A dimensionless measure, symbolized T_a_scale, quantifying the fidelity of a self-similar generative rule as it propagates across different scales within a system. It represents the signal-to-noise ratio of the recursive grammar, distinguishing between the pure, crystal-like repetition of a rule (T_a_scale → 1) and its noisy, organic, or environmentally distorted expression (T_a_scale → 0).

## EFT-First Summary
Inter-Scale Coherence is operationally mapped to the stability of the **Hurst Exponent (H)** across a range of scales, typically measured using Detrended Fluctuation Analysis (DFA). Whereas H itself measures the nature of the correlation (persistent, anti-persistent, or random), T_a_scale measures how well that single correlation rule holds true as one zooms in or out. A system with a consistent H value across many decades of scale exhibits a high T_a_scale, indicating it is near a scale-invariant fixed point.

## Glossary Links
- See also: Coherence Complexity (D_f), Principle of Correspondence (DOMA-136), Generative Rhythm (ω_g)