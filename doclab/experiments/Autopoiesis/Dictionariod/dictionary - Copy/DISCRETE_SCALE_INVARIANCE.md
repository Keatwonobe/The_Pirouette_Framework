---
term: "Discrete Scale Invariance"
canonical_id: "DISCRETE_SCALE_INVARIANCE"
symbol: "DSI"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-022"]
---

---
term: Discrete Scale Invariance
canonical_id: DISCRETE_SCALE_INVARIANCE
symbol: DSI
aliases: [Discrete Self-Similarity]
parents: [MATH-022]
children: [SECT-Γ-A-CMB, SECT-Γ-A-HALO]
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-022
      lines: "Fractal-of-Time Postulate"
      snippet: |
        The coherence network exhibits **discrete scale invariance** (DSI) across finite bands: Λ→qΛ with q>1 produces statistically similar channel geometry.
  editors: [GPT-4]
  review_log: []
triad:
  art: |
    The universe's fine structure echoes itself at preferred magnifications, like a crystal lattice in the space of scales, leaving faint, rhythmic ripples on observables.
  law: |
    A system with DSI is statistically invariant not under all scaling transformations, but only under discrete steps `x → q^n x` for integer `n` and a preferred ratio `q`. This necessarily implies that scaling observables `O(x)` contain small log-periodic corrections of the form `O(x) ∝ x^α [1 + ε cos(ω log x + φ)]`.
  philosophy: |
    DSI replaces arbitrary, data-fitted scaling exponents with rational values derived from geometry and dynamics. It posits that nature's symmetries can be discrete and hierarchical, providing a non-numerological origin for the Pressuron's equation of state and its stability.
pirouette_definition: |
  Discrete Scale Invariance is a core postulate stating that the coherence network is statistically self-similar not under continuous scaling, but under discrete transformations by a preferred scaling factor `q > 1`. This broken symmetry stabilizes the network's effective spatial dimension `D_eff` onto rational plateaus, thereby fixing the Pressuron exponent `β = D_eff / z` to specific rational values (e.g., {0, 1/2, 1} for z=2). The primary observable consequence of DSI is the presence of small, log-periodic oscillations in physical quantities as a function of scale.
operational_definition:
  units: Dimensionless (a symmetry property).
  symbol_table:
    - name: q
      meaning: Preferred scaling ratio of the DSI symmetry.
      dimensions: dimensionless
      default_range: "1 < q < 10"
    - name: D_eff
      meaning: Effective (possibly fractal) spatial dimension of the active coherence network.
      dimensions: dimensionless
      default_range: "{0, 1, 2}"
    - name: z
      meaning: Dynamical exponent of the superfluid sector.
      dimensions: dimensionless
      default_range: "2 (nonrelativistic)"
    - name: ε_lp
      meaning: Amplitude of log-periodic corrections.
      dimensions: dimensionless
      default_range: "≲ 0.05"
  measurement:
    procedures:
      - name: Log-Periodic Residual Analysis
        outline: |
          1. Measure an observable quantity over a wide range of scales (e.g., dark matter surface density Σ₀ vs. halo mass M).
          2. Fit the data to a pure power-law model where the exponent is fixed to a rational value predicted by DSI (e.g., from `β = D_eff / z`).
          3. Analyze the fractional residuals of the fit as a function of the logarithm of the scale variable (e.g., `log M`).
          4. Perform a Fourier or spectral analysis on the log-residuals to search for a peak at a characteristic frequency `ω`, which corresponds to the scaling ratio `q`.
        expected_signals: [A statistically significant sinusoidal oscillation in fit residuals vs. log(scale), A sharp peak in the power spectrum of the log-residuals.]
        pitfalls: [The signal amplitude `ε_lp` is small and can be lost in observational noise or systematic errors., The analysis requires high-quality data over a wide dynamic range (several decades in scale) to resolve oscillations.]
context_windows:
  - module: MATH-022
    excerpt: |
      The coherence network exhibits **discrete scale invariance** (DSI) across finite bands: Λ→qΛ with q>1 produces statistically similar channel geometry. DSI implies **log‑periodic** corrections to scaling observables and stabilizes D_eff on rational plateaus. Consequence: β takes rational values tied to (D_eff, z); transitions between plateaus produce small, oscillatory features...
  - module: MATH-022
    excerpt: |
      β emerges from **symmetry + geometry**, not a fit: Eq. (1) is a Ward‑identity–like relation from scaling of the action with an active‑dimension measure... Log‑periodic corrections are a universal fingerprint of DSI, not an extra dial.
poetic_connections:
  motifs: [fractal of time, scale crystal, log-periodic rhythm, geometric quantization]
  evocative_lines:
    - "DSI implies **log‑periodic** corrections to scaling observables and stabilizes D_eff on rational plateaus."
    - "Transitions between regimes imprint **log‑periodic wiggles** in Σ₀ vs. mass."
  association_matrix:
    - [ "EFFECTIVE_DIMENSION", 0.9 ]
    - [ "PRESSURON_EOS_BETA", 0.9 ]
    - [ "LOG_PERIODIC_CORRECTIONS", 0.8 ]
    - [ "SCALE_COVARIANCE", 0.5 ]
formal_mappings:
  candidates:
    - target: Discrete scale invariance in complex systems
      domain: CM|Math
      mapping_kind: conceptual|mathematical
      equation_hint: |
        V(r) = r^α * [A_0 + A_1 cos(ω ln(r) + δ)]
      justification: |
        The concept of DSI as a broken continuous scale symmetry leading to log-periodic oscillations is well-established in the physics of critical phenomena, turbulence, and rupture mechanics. The mathematical formalism is identical, identifying a preferred scaling ratio `q` from complex critical exponents. This provides a theoretical precedent for applying DSI to the coherence network.
      references:
        - title: "Discrete scale invariance and complex exponents"
          where: "Physics Reports 267, 195-304 (1996)"
          date: 1996-04-01
      confidence: 0.8
  adopted:
    - target:
      rationale:
      confidence: 0.0
constraints_and_falsifiers:
  claims:
    - statement: "The Pressuron exponent `β` is fixed to rational values from the set `{D_eff/z | D_eff ∈ {0,1,2}, z=2}`."
      domain: theory|phenomenology
      falsifier: "An empirical fit to halo profiles or other phenomena robustly requires a `β` value that is irrational or not in the predicted set {0, 1/2, 1}, and the data show no evidence of log-periodic corrections that would signal a transition region."
      status: proposed
      links: [MATH-022]
    - statement: "Observables like the central surface density Σ₀(M) and the small-scale matter power spectrum exhibit small, periodic modulations as a function of log(Mass) or log(k)."
      domain: phenomenology
      falsifier: "High-precision measurements over a wide dynamic range show a smooth, pure power-law scaling with residuals consistent with random noise, and place upper limits on the amplitude of any log-periodic component `ε_lp` that are far below the predicted range."
      status: proposed
      links: [MATH-022, SECT-Γ-A-HALO]
naming_notes:
  collisions: []
  disambiguation: |
    Discrete Scale Invariance (DSI) must not be confused with standard, continuous scale invariance. In continuous scale invariance, a system looks the same after rescaling by *any* factor `λ`. In DSI, this symmetry is broken down to a discrete subgroup of scalings by factors of `q^n`, where `q` is a single preferred number. This distinction is crucial, as DSI predicts log-periodic phenomena absent in continuously scale-invariant theories.
crosslinks:
  near_synonyms: [DISCRETE_SELF_SIMILARITY]
  antonyms: [CONTINUOUS_SCALE_INVARIANCE]
  prerequisites: [SCALE_COVARIANCE, COHERENCE_NETWORK, EFFECTIVE_DIMENSION]
  downstream_effects: [PRESSURON_EOS_BETA, LOG_PERIODIC_CORRECTIONS, VORTEX_LATTICE_SPECTRA]
license: CC-BY-SA-4.0
---

# Discrete Scale Invariance

## Canonical (Pirouette)
Discrete Scale Invariance is a core postulate stating that the coherence network is statistically self-similar not under continuous scaling, but under discrete transformations by a preferred scaling factor `q > 1`. This broken symmetry stabilizes the network's effective spatial dimension `D_eff` onto rational plateaus, thereby fixing the Pressuron exponent `β = D_eff / z` to specific rational values (e.g., {0, 1/2, 1} for z=2). The primary observable consequence of DSI is the presence of small, log-periodic oscillations in physical quantities as a function of scale.

## EFT-First Summary
In the language of effective field theory, Discrete Scale Invariance is a breaking of the continuous scaling symmetry `x → λ x` down to a discrete subgroup `x → q^n x`. This is analogous to the formation of a crystal, which breaks continuous translational symmetry down to a discrete lattice symmetry. The consequence of this symmetry breaking is the appearance of complex critical exponents, which manifest physically as log-periodic corrections to correlation functions and other observables. This phenomenon is known in condensed matter and statistical physics and provides a formal basis for the predicted rational exponents and oscillatory signals in the Pirouette Framework.

## Glossary Links
- See also: [Effective Dimension](<#>), [Pressuron EOS](<#>), [Log-Periodic Corrections](<#>)