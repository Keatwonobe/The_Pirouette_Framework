---
term: "Log-Periodic Corrections"
canonical_id: "LOG_PERIODIC_CORRECTIONS"
symbol: ""
aliases: [log-periodic wiggles]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-022"]
---

---
term: Log-Periodic Corrections
canonical_id: LOG_PERIODIC_CORRECTIONS
symbol: 1 + ε_lp cos(ω ln X + φ)
aliases: ['log-periodic wiggles']
parents: ['MATH-022']
children: ['SECT-Γ-A-CMB', 'SECT-Γ-A-HALO']
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-022
      lines: "Code Hooks"
      snippet: |
        P=α X^{1+β}[1+ε_lp cos(ω ln X + φ)]
  editors: ['System Agent']
  review_log: []
triad:
  art: |
    A fractal hum resonating through spacetime, where the structure of the cosmos at one scale is a faint but precise echo of another. These are the interference fringes from the universe observing its own self-similar geometry.
  law: |
    A physical system exhibiting Discrete Scale Invariance (DSI) with a preferred scaling ratio `q` will display observables with power-law scaling modulated by a correction periodic in the logarithm of the scale, with frequency proportional to `1/ln(q)`. Absence of these corrections falsifies the DSI hypothesis.
  philosophy: |
    Log-periodic corrections are the unique, observable fingerprint of a discrete, rather than continuous, scaling symmetry. They elevate DSI from a mathematical curiosity to a falsifiable physical principle, providing a direct observational window into the fractal geometry of the underlying coherence network.
pirouette_definition: |
  Small, oscillatory, multiplicative corrections to a primary power-law scaling relation in a physical observable. These corrections are periodic in the logarithm of the scaling variable (e.g., mass, length, or wavenumber) and are a direct physical consequence of an underlying Discrete Scale Invariance (DSI) in the system's dynamics or geometry, such as the fractal coherence network.
operational_definition:
  units: Dimensionless (a fractional correction).
  symbol_table:
    - name: ε_lp
      meaning: Amplitude of the log-periodic correction
      dimensions: dimensionless
      default_range: ~0.01 - 0.05
    - name: ω
      meaning: Angular frequency in log-space
      dimensions: dimensionless
      default_range: 2π / ln(q)
    - name: q
      meaning: Preferred scaling factor of the DSI
      dimensions: dimensionless
      default_range: '> 1'
    - name: X
      meaning: Primary scaling variable (e.g., halo mass, wavenumber)
      dimensions: contextual
      default_range: contextual
    - name: φ
      meaning: Phase offset
      dimensions: dimensionless
      default_range: contextual
  measurement:
    procedures:
      - name: Residual Analysis of Scaling Relations
        outline: |
          Fit an observable (e.g., halo central surface density Σ₀ vs. mass M) to its expected power-law form, P(X) ∝ X^(1+β). Plot the residuals of the fit against the logarithm of the independent variable (ln M). Perform a Fourier analysis or fit a sinusoidal function to the residuals to extract ε_lp and ω.
        expected_signals: ['A statistically significant sinusoidal pattern in the log-space residuals.', 'A distinct peak in the periodogram of the log-space residuals at a frequency corresponding to ln(q).']
        pitfalls: ['Observational noise or selection biases can obscure the small-amplitude signal.', 'Systematics in data processing could introduce spurious periodicities.', 'The DSI might only hold over a finite range of scales, limiting the number of observable oscillations.']
context_windows:
  - module: MATH-022
    excerpt: |
      DSI implies log‑periodic corrections to scaling observables and stabilizes D_eff on rational plateaus. ...Transitions between plateaus produce small, oscillatory features (log‑periodic) in halo core scaling and small‑scale power.
  - module: MATH-022
    excerpt: |
      Fit Σ₀(M) with a single β fixed by chosen (D_eff,z); observe allowed log‑periodic residuals with frequency log q. If smooth power law without oscillations ... falsify the postulate.
poetic_connections:
  motifs: ['fractal echo', 'scaling resonance', 'geometric interference', 'discrete beat']
  evocative_lines:
    - '"the Fractal of Time"'
    - '"small, oscillatory features (log‑periodic) in halo core scaling"'
  association_matrix:
    - [ "DISCRETE_SCALE_INVARIANCE", 0.9 ]
    - [ "COHERENCE_NETWORK", 0.7 ]
    - [ "BETA_PARAMETER", 0.5 ]
formal_mappings:
  candidates:
    - target: Log-periodic oscillations in critical phenomena
      domain: CM
      mapping_kind: mathematical
      equation_hint: |
        f(x) ≈ x^α [1 + c₁ cos(c₂ ln x)]
      justification: |
        In statistical mechanics, systems with DSI (e.g., defined on hierarchical lattices) exhibit complex critical exponents. A complex exponent `a + ib` leads directly to a scaling behavior of the form `x^a * cos(b ln x)`, which is mathematically identical to the corrections predicted in Pirouette.
      references:
        - title: Discrete scale invariance and complex exponents
          where: Physics Reports 324 (2000) 1–100
          date: 1999-12-01
      confidence: 0.9
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The Σ₀-M relation for superfluid halos is modulated by a log-periodic correction with a universal frequency `q` and small amplitude ε_lp."
      domain: phenomenology
      falsifier: "A high-precision survey of halo cores shows residuals from the best-fit β=D_eff/z power law are consistent with noise or a smooth, non-oscillatory function."
      status: proposed
      links: ['MATH-022', 'SECT-Γ-A-HALO']
    - statement: "The small-scale matter power spectrum contains a subtle, periodic modulation in log(k)."
      domain: phenomenology
      falsifier: "Future weak-lensing or galaxy surveys measure a smooth power spectrum at small scales, placing upper limits on ε_lp that are inconsistent with DSI predictions."
      status: proposed
      links: ['MATH-022', 'SECT-Γ-A-CMB']
naming_notes:
  collisions: []
  disambiguation: |
    Distinct from Baryon Acoustic Oscillations (BAO). BAO are periodic in wavenumber `k` and arise from plasma sound waves in the early universe. Log-periodic corrections are periodic in `log(k)` and arise from a fundamental discrete scaling symmetry.
crosslinks:
  near_synonyms: ['LOG_PERIODIC_WIGGLES']
  antonyms: []
  prerequisites: ['DISCRETE_SCALE_INVARIANCE']
  downstream_effects: ['HALO_CORE_SCALING', 'MATTER_POWER_SPECTRUM']
license: CC-BY-SA-4.0
---

# Log-Periodic Corrections

## Canonical (Pirouette)
Small, oscillatory, multiplicative corrections to a primary power-law scaling relation in a physical observable. These corrections are periodic in the logarithm of the scaling variable (e.g., mass, length, or wavenumber) and are a direct physical consequence of an underlying Discrete Scale Invariance (DSI) in the system's dynamics or geometry, such as the fractal coherence network.

## EFT-First Summary
Log-periodic corrections are analogous to the oscillatory scaling behaviors seen in condensed matter systems at critical points that possess Discrete Scale Invariance. In these systems, a complex critical exponent `a+ib` emerges, leading to observables that scale as `x^a * cos(b ln x)`. In Pirouette, this phenomenon is not just an analogy but a direct prediction from the fractal geometry of the coherence network, providing a "smoking-gun" signature for DSI in cosmological data.

## Glossary Links
- See also: Discrete Scale Invariance, Coherence Network, β Parameter