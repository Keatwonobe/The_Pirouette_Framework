---
term: "Plateaus"
canonical_id: "PLATEAUS"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-022"]
---

---
term: Plateaus
canonical_id: PLATEAUS
symbol: D_eff, β
aliases: [Rational Plateaus, D_eff Plateaus, β Plateaus]
parents: [MATH-022]
children: [SECT-Γ-A-CMB, SECT-Γ-A-HALO]
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-022
      lines: "Executive result"
      snippet: |
        In 3D spacetime with nonrelativistic superfluid scaling z=2 and plateaus D_eff∈{0,1,2}, one obtains β∈{0, 1/2, 1}—exactly the rational set allowed in SECT‑Γ‑A. No calibration needed.
  editors: [The Pirouette Dictionary Agent]
  review_log: []
triad:
  art: |
    Across the scales of cosmic structure, the chaotic weave of coherence channels settles into stable, quantized geometries. These Plateaus are like musical harmonics resonating in the fabric of spacetime, turning a cacophony of possibilities into a clean, predictable chord.
  law: |
    The Pressuron exponent β is determined by the ratio of the effective dimension D_eff of the active coherence network to the dynamical exponent z, such that β = D_eff / z. A postulate of discrete scale invariance stabilizes D_eff into integer plateaus {0,1,2}, thereby quantizing β into a predictable, rational set {0, 1/2, 1} for z=2.
  philosophy: |
    Plateaus represent the victory of symmetry over contingency, replacing data-fitted parameters with a discrete set of values derived from the geometric and dynamic structure of the system. This transforms the equation of state from an empirical curve into a predictable, falsifiable ladder of states, each corresponding to a distinct topological phase of the coherence network.
pirouette_definition: |
  Plateaus are the discrete, stable, rational values that the effective spatial dimension (D_eff) and the derived Pressuron exponent (β) are predicted to take across different physical scales. They arise from a postulate of discrete scale invariance (DSI) in the superfluid coherence network. For a given dynamical exponent (z), the β plateaus are directly determined by the D_eff plateaus via the scaling relation β = D_eff/z, corresponding to physical regimes where the network is dominated by point-like (D_eff=0), filamentary (D_eff=1), or sheet-like (D_eff=2) structures.
operational_definition:
  units: dimensionless
  symbol_table:
    - name: D_eff
      meaning: Effective spatial dimension of the coherence network
      dimensions: dimensionless
      default_range: "{0, 1, 2}"
    - name: β
      meaning: Exponent in the leading term of the Pressuron, P(X) ∝ X^{1+β}
      dimensions: dimensionless
      default_range: "{0, 1/2, 1} for z=2"
    - name: z
      meaning: Dynamical exponent for the superfluid sector
      dimensions: dimensionless
      default_range: "2 (nonrelativistic)"
  measurement:
    procedures:
      - name: Halo Profile Fitting with Quantized β
        outline: |
          Fit observed galactic halo properties (e.g., surface density Σ₀ vs. mass M) to the superfluid model. Instead of allowing β to be a free continuous parameter, test only the discrete values predicted by the plateaus (e.g., β=1/2, β=1). The best-fit model must be one of these discrete values.
        expected_signals: [Goodness-of-fit χ² values show sharp minima at β ∈ {0, 1/2, 1}, Residual scatter around the best-fit relation exhibits log-periodic oscillations]
        pitfalls: [Insufficient data resolution to distinguish between β=0.5 and β=0.6, Degeneracy with baryonic feedback models, Systematic errors in mass measurements]
      - name: Small-Scale Power Spectrum Analysis
        outline: |
          Analyze the matter power spectrum at small scales (high k) from weak lensing or Lyman-alpha forest data. Search for mild, periodic modulations in log(k), which are the predicted signature of transitions between D_eff plateaus.
        expected_signals: [A small-amplitude (ε_lp ≲ 0.05) oscillatory component superimposed on the smooth power-law spectrum]
        pitfalls: [Signal may be below the noise floor of current surveys, Astrophysical systematics from star formation or AGNs can mimic or mask the signal]
context_windows:
  - module: MATH-022
    excerpt: |
      β = D_eff / z.
      Interpretation:
      • z encodes dynamics (e.g., z=2 for superfluid hydrodynamics).
      • D_eff encodes geometry/topology (sheet‑like D_eff≈2; filamentary D_eff≈1; point‑like cores D_eff≈0).
      • Discrete self‑similarity of the network yields **plateaus** in D_eff and hence **rational β**.
  - module: MATH-022
    excerpt: |
      R1 β is **fixed a priori** by (D_eff, z). With z=2:
      • Sheet‑dominated regime (D_eff=2): β=1 → P∝X^2
      • Filament regime (D_eff=1): β=1/2 → P∝X^{3/2}
      • Core/point regime (D_eff=0): β=0 → P∝X
poetic_connections:
  motifs: [quantization, stability, emergent simplicity, fractal, resonance, harmonics]
  evocative_lines:
    - "β emerges from symmetry + geometry, not a fit."
    - "stabilizes D_eff on rational plateaus"
  association_matrix:
    - [ "EFFECTIVE_DIMENSION", 0.9 ]
    - [ "DISCRETE_SCALE_INVARIANCE", 0.9 ]
    - [ "PRESSURON", 0.7 ]
    - [ "FRACTAL_OF_TIME", 0.6 ]
formal_mappings:
  candidates:
    - target: Universality classes
      domain: CM
      mapping_kind: conceptual
      equation_hint: ~
      justification: |
        In statistical physics, systems near a critical point fall into universality classes characterized by a small set of rational critical exponents. Plateaus function analogously, grouping diverse astrophysical systems into classes defined by a discrete geometric exponent (D_eff), which in turn fixes the dynamic exponent (β) and thus the equation of state.
      references:
        - title: "Lectures on Phase Transitions and the Renormalization Group"
          where: "Chapter 5"
          date: 1992-01-01
      confidence: 0.8
  adopted:
    - target: Universality classes
      rationale: |
        The mapping to universality classes correctly captures the core idea: complex microphysics (coherence channels) gives rise to simple, universal macroscopic behavior described by a few rational exponents, independent of system-specific details.
      confidence: 0.8
constraints_and_falsifiers:
  claims:
    - statement: "The Pressuron exponent β, when inferred from halo populations, is restricted to a discrete set of rational values {0, 1/2, 1} for z=2."
      domain: phenomenology
      falsifier: "A large, clean sample of halo profiles is best fit by a continuous distribution of β values, or a single value of β that is robustly non-rational (e.g., β = 0.71 ± 0.02)."
      status: proposed
      links: [MATH-022, SECT-Γ-A-HALO]
    - statement: "Residuals from fits using a fixed plateau value for β should exhibit log-periodic oscillations, a fingerprint of discrete scale invariance."
      domain: phenomenology
      falsifier: "Residuals are best fit by a smooth, monotonic function or are purely random noise, with no statistically significant evidence of periodic modulation in log-mass or log-radius."
      status: proposed
      links: [MATH-022]
naming_notes:
  collisions: ["Sachs-Wolfe plateau (CMB)"]
  disambiguation: |
    In Pirouette, 'Plateaus' specifically refers to the quantized, stable values of the effective dimension D_eff and the resulting Pressuron exponent β. This should not be confused with generic flat regions in data plots, such as the Sachs-Wolfe plateau, which arise from different physical mechanisms and are not indicative of a discrete, underlying parameter.
crosslinks:
  near_synonyms: []
  antonyms: [CONTINUOUS_PARAMETER, FREE_PARAMETER]
  prerequisites: [EFFECTIVE_DIMENSION, DISCRETE_SCALE_INVARIANCE, DYNAMICAL_EXPONENT]
  downstream_effects: [LOG_PERIODIC_OSCILLATIONS, HALO_CORE_SCALING]
license: CC-BY-SA-4.0
---

# Plateaus

## Canonical (Pirouette)
Plateaus are the discrete, stable, rational values that the effective spatial dimension (D_eff) and the derived Pressuron exponent (β) are predicted to take across different physical scales. They arise from a postulate of discrete scale invariance (DSI) in the superfluid coherence network. For a given dynamical exponent (z), the β plateaus are directly determined by the D_eff plateaus via the scaling relation β = D_eff/z, corresponding to physical regimes where the network is dominated by point-like (D_eff=0), filamentary (D_eff=1), or sheet-like (D_eff=2) structures.

## EFT-First Summary
The concept of Plateaus maps conceptually to **universality classes** in condensed matter and statistical physics. Just as systems near a critical point are governed by a small set of rational critical exponents regardless of their microphysical details, the dark matter fluid's equation of state is governed by a small, discrete set of exponents (β). These exponents are not free parameters to be fitted but are instead fixed by the underlying geometry (D_eff) and dynamics (z) of the system. This provides a powerful, predictive framework where halo structure falls into distinct classes based on its dominant coherence topology.

## Glossary Links
- See also: [EFFECTIVE_DIMENSION](...), [DISCRETE_SCALE_INVARIANCE](...), [LOG_PERIODIC_OSCILLATIONS](...)