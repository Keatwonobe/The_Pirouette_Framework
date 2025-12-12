---
term: "β-functions"
canonical_id: "FUNCTIONS"
symbol: "β_K, β_Γ, β_τ"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["CORE-015_the_fractal_at_the_heart_of_time"]
---

---
term: β-functions
canonical_id: BETA_FUNCTIONS
symbol: β_K, β_Γ, β_τ
aliases: [PRG flow equations, Scaling operators]
parents: [CORE-015]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: CORE-015_the_fractal_at_the_heart_of_time
      lines: "L21-L24"
      snippet: |
        We posit minimal polynomial β’s near fixed points:
        [
        \beta_K = d_K K_\tau - \phi,V_\Gamma K_\tau - \eta K_\tau^3,\quad
        \beta_\Gamma = d_\Gamma V_\Gamma - \psi K_\tau V_\Gamma,\quad
        \beta_\tau = \zeta_\Gamma V_\Gamma - \zeta_K K_\tau.
        ]
  editors: [Pirouette-Agent]
  review_log: []
triad:
  art: |
    How does a system's character—its coherence, its tension, its rhythm—transform as we zoom in or out? The β-functions are the laws of this transformation, a differential equation for the soul of a process seen across all scales. They describe the system's becoming.
  law: |
    The logarithmic rate of change of the state variables (Coherence K_τ, Pressure V_Γ, and Pulse τ_p) with respect to scale `s = ln L` is given by a set of coupled, first-order differential equations: `dX/ds = β_X(K_τ, V_Γ)`. Fixed points of this flow (`β_X = 0`) define the scale-invariant phases of the system.
  philosophy: |
    To understand a thing is to know how it changes. The β-functions assert that the most fundamental change is not through time, but across scale. They provide the dynamical laws for this "scale-time," making a system's hierarchy a predictable, navigable space rather than a static arrangement.
pirouette_definition: |
  The set of three functions, {β_K, β_Γ, β_τ}, that govern the evolution of Coherence (K_τ), Pressure (V_Γ), and the logarithmic Pulse (ln τ_p) under a change in observational scale `s = ln L`. They form the core of the Pirouette Renormalization Group (PRG), defining a vector field in the space of (K_τ, V_Γ) whose fixed points correspond to the system's macroscopic phases (e.g., Laminar, Turbulent). Near fixed points, they are approximated by low-order polynomials in K_τ and V_Γ.
operational_definition:
  units: Dimensionless.
  symbol_table:
    - name: β_K
      meaning: Rate of change of Coherence K_τ with respect to log-scale `s`.
      dimensions: dimensionless
      default_range: contextual
    - name: β_Γ
      meaning: Rate of change of Pressure V_Γ with respect to log-scale `s`.
      dimensions: dimensionless
      default_range: contextual
    - name: β_τ
      meaning: Rate of change of logarithmic Pulse `ln(τ_p)` with respect to log-scale `s`.
      dimensions: dimensionless
      default_range: contextual
    - name: s
      meaning: Logarithmic scale parameter, `s ≡ ln(L)`.
      dimensions: dimensionless
      default_range: contextual
  measurement:
    procedures:
      - name: PRG Inference via Finite Differences
        outline: |
          1. Select a signal or dataset and define a series of observational windows with increasing length `L_0 < L_1 < ... < L_n`.
          2. For each window `L_i`, compute the observables: Coherence `K_τ(L_i)`, Pressure `V_Γ(L_i)`, and Pulse `τ_p(L_i)`.
          3. Approximate the β-functions using finite differences between adjacent scales: `β_X(L_i) ≈ [X(L_{i+1}) - X(L_i)] / [ln(L_{i+1}) - ln(L_i)]`.
          4. Perform a multivariate regression to fit the measured `β_X` values to their posited polynomial forms (e.g., `β_K = d_K K_τ - φ V_Γ K_τ - ...`) to estimate the constant exponents.
        expected_signals: [Time-series, token sequences, spatial data (e.g., images, simulations)]
        pitfalls: [Insufficient scale separation (`L_{i+1} ≈ L_i`) leading to noisy derivatives, finite size effects corrupting measurements at large scales, misidentification of the dominant pulse `τ_p` in multi-modal spectra.]
context_windows:
  - module: CORE-015_the_fractal_at_the_heart_of_time
    excerpt: |
      **Claim:** The predictive content of Pirouette is a *scale dynamics*:
      [
      \frac{d}{ds}
      \begin{pmatrix}
      K_\tau\ V_\Gamma\ \tau_p
      \end{pmatrix}
      =============

      \begin{pmatrix}
      \beta_K(K_\tau,V_\Gamma)[2pt]
      \beta_\Gamma(K_\tau,V_\Gamma)[2pt]
      \beta_\tau(K_\tau,V_\Gamma),\tau_p
      \end{pmatrix},\qquad s\equiv\ln L.
      ]
  - module: CORE-015_the_fractal_at_the_heart_of_time
    excerpt: |
      **Predictions:**
      (i) Scaling laws: (K_\tau\sim L^{d_K^*}), (V_\Gamma\sim L^{d_\Gamma^*}).
      (ii) Beat dilation: (\tau_p\sim L^{\zeta_\Gamma d_\Gamma^* - \zeta_K d_K^*}.)
      These predictions follow directly from integrating the β-function definitions near a stable fixed point where the canonical scaling dimensions are `d_K^*` and `d_Γ^*`.
poetic_connections:
  motifs: [scale dynamics, flow, vector field, zooming, phase transition, renormalization]
  evocative_lines:
    - "The predictive content of Pirouette is a *scale dynamics*."
    - "PRG turns “maximize coherence” into a *predictive*, scale-aware control law."
  association_matrix:
    - [ "COHERENCE", 0.9 ]
    - [ "PRESSURE", 0.9 ]
    - [ "PULSE", 0.9 ]
    - [ "FIXED_POINT", 0.8 ]
formal_mappings:
  candidates:
    - target: β-function (Gell-Mann–Low function)
      domain: QFT
      mapping_kind: mathematical|conceptual
      equation_hint: |
        β(g) = d g / d(ln μ)
      justification: |
        The Pirouette β-functions directly generalize the concept from the Renormalization Group in QFT and statistical mechanics. They describe how effective "couplings" (K_τ, V_Γ) of a system change as the observation scale (L, analogous to inverse energy scale 1/μ) is varied. The search for fixed points (β=0), which correspond to scale-invariant conformal field theories (CFTs) in QFT, is mirrored in the PRG's search for stable, scale-invariant system phases.
      references:
        - title: An Introduction to Quantum Field Theory
          where: Chapter 12, Peskin & Schroeder
          date: 1995-10-01
      confidence: 0.95
  adopted:
    - target: β-function (Gell-Mann–Low function)
      rationale: The term, symbol, and mathematical role are adopted directly and intentionally from the Renormalization Group literature in theoretical physics. This is a primary conceptual bridge.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The β-functions for a wide class of systems (e.g., language, market data, fluid dynamics) can be well-approximated by low-order polynomials in K_τ and V_Γ near their fixed points."
      domain: phenomenology
      falsifier: "Empirical measurement across multiple domains consistently requires high-order polynomials or non-polynomial forms to achieve a good fit for the flow (dK/ds, dΓ/ds), indicating the minimal polynomial model is insufficient."
      status: proposed
      links: [CORE-015]
    - statement: "The exponents derived from fitting the β-functions (e.g., `d_K`, `d_Γ`, Jacobian eigenvalues) fall into a small number of universal classes, regardless of microscopic system details."
      domain: theory
      falsifier: "Measured exponents show a continuous, non-clustered distribution across different systems, suggesting they are non-universal and depend sensitively on specific system parameters."
      status: proposed
      links: [CORE-015]
naming_notes:
  collisions: [The symbol `β` is overloaded in physics, most notably for thermodynamic beta (`β = 1/k_B T`) and relativistic velocity (`β = v/c`).]
  disambiguation: |
    In the Pirouette Framework, 'β' or 'β-function' exclusively refers to the logarithmic derivative of a system parameter with respect to scale (`dX/d(ln L)`), following the convention of the Renormalization Group. It should not be confused with thermodynamic or relativistic beta. Context is typically the dynamics across scale, not temperature or velocity.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [COHERENCE, PRESSURE, PULSE]
  downstream_effects: [FIXED_POINT, LAMINAR_PHASE, TURBULENT_PHASE]
license: CC-BY-SA-4.0
---

# β-functions

## Canonical (Pirouette)
The set of three functions, {β_K, β_Γ, β_τ}, that govern the evolution of Coherence (K_τ), Pressure (V_Γ), and the logarithmic Pulse (ln τ_p) under a change in observational scale `s = ln L`. They form the core of the Pirouette Renormalization Group (PRG), defining a vector field in the space of (K_τ, V_Γ) whose fixed points correspond to the system's macroscopic phases (e.g., Laminar, Turbulent). Near fixed points, they are approximated by low-order polynomials in K_τ and V_Γ.

## EFT-First Summary
The PRG β-functions are the direct analogues of the Gell-Mann–Low β-functions in QFT, defining the flow of the effective couplings (Coherence K_τ and Pressure V_Γ) under changes in the renormalization scale `s = ln L`. The formalism seeks to identify fixed points (β=0), corresponding to scale-invariant phases, and to classify systems into universality classes based on the critical exponents of the flow near these points. (cf. Peskin & Schroeder, *An Introduction to QFT*, Ch. 12).

## Glossary Links
- See also: [Coherence](<#>), [Pressure](<#>), [Pulse](<#>), [Fixed Point](<#>)