---
term: "Kinetic term"
canonical_id: "KINETIC_TERM"
symbol: "X"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["COSMO-005"]
---

---
term: Kinetic term
canonical_id: KINETIC_TERM
symbol: X
aliases: []
parents: [COSMO-005]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: COSMO-005
      lines: "L15-L16"
      snippet: |
        Background energy density and pressure from P(X(n)) with X=μ−θ′/a.
  editors: [system]
  review_log: []
triad:
  art: |
    The kinetic term measures the field's strain, the tension between its inherent potential and its dynamic unfolding in spacetime. It is the energetic cost of motion, the friction against the expanding cosmic clock.
  law: |
    The kinetic term `X` directly determines the equation of state `P(X)` of the superfluid. A non-zero `X` implies a non-zero pressure, and its variation governs the fluid's sound speed, `c_s² ∝ ∂P/∂X`. If measurements of the sound speed are inconsistent with the derivatives of the inferred pressure `P` with respect to `X`, the model is falsified.
  philosophy: |
    In the P(X) framework, `X` is the fundamental variable that elevates the description from a static substance to a dynamic fluid. It bridges the microscopic quantum potential (μ) and the macroscopic cosmological flow (θ'), allowing the effective fluid to respond to gravitational perturbations. It is the engine of sound wave propagation and structure formation in this model.
pirouette_definition: |
  The kinetic term, `X`, is the primary argument of the Pressuron function `P(X)` that defines the superfluid's equation of state. It is defined as `X = μ − θ′/a`, where `μ` is the chemical potential, `θ` is the phase of the complex scalar field, the prime denotes a derivative with respect to conformal time, and `a` is the scale factor. `X` quantifies the departure from a static equilibrium (where `X=0`), linking the field's internal state to its temporal evolution and thereby governing its pressure, energy density, and sound speed.
operational_definition:
  units: Energy (M L^2 T^-2)
  symbol_table:
    - name: X
      meaning: Kinetic term
      dimensions: M L^2 T^-2
      default_range: contextual, model-dependent
    - name: μ
      meaning: Chemical potential
      dimensions: M L^2 T^-2
      default_range: contextual
    - name: θ
      meaning: Phase of the superfluid's complex scalar field
      dimensions: dimensionless
      default_range: contextual
    - name: a
      meaning: Cosmological scale factor
      dimensions: dimensionless
      default_range: 0 to 1
    - name: ′
      meaning: Derivative with respect to conformal time η
      dimensions: T^-1
      default_range: N/A
  measurement:
    procedures:
      - name: Cosmological Inference
        outline: |
          `X` is not directly measured but is a model-dependent quantity inferred via cosmological data fitting.
          1. Assume a functional form for the equation of state, `P(X)` (e.g., `αX^{1+β}+...`).
          2. Evolve the cosmological background and perturbation equations for the `P(X)` fluid.
          3. Compare the resulting theoretical CMB and Large-Scale Structure power spectra against observational data.
          4. Use a statistical sampler (e.g., MCMC) to infer the posterior distributions of the `P(X)` model parameters, which determines the cosmic history of `X(a)`.
        expected_signals: [Deviations in CMB power spectra at high-ℓ, Small-scale suppression of the matter power spectrum]
        pitfalls: [Model dependence on the assumed form of P(X), Degeneracies with standard cosmological parameters]
context_windows:
  - module: COSMO-005
    excerpt: |
      Microscopic: heavy quanta m_H≈17 MeV; macroscopic: superfluid with EOS from P(X)=αX^{1+β}+δX^2+…
      Define background number density n(a) from continuity (ȷ^0 conservation) and chemical relation μ(n).
      Sound speed & dispersion:
      • c_s^2(a) = ∂p/∂ρ|_{n} = [∂P/∂X]/[m_H ∂n/∂X + …]
  - module: COSMO-005
    excerpt: |
      Background & Perturbation Equations (Conformal Time η)
      Background energy density and pressure from P(X(n)) with X=μ−θ′/a.
      Implement as species `gammat_superfluid` with variables {ρ_Γ(a), p_Γ(a)} obeying:
      ρ_Γ′ = −3ℋ (ρ_Γ + p_Γ).
poetic_connections:
  motifs: [flow, pressure, strain, dynamic tension, cosmic friction]
  evocative_lines:
    - "Background energy density and pressure from P(X(n)) with X=μ−θ′/a."
    - "Phonon dispersion: ω² = c_s² k² + m_eff² with m_eff² from weak tail breaking"
  association_matrix:
    - [ "PRESSURON_P", 0.9 ]
    - [ "SOUND_SPEED_CS2", 0.8 ]
    - [ "CHEMICAL_POTENTIAL_MU", 0.7 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Canonical kinetic term for a U(1) scalar field
      domain: EFT
      mapping_kind: mathematical
      equation_hint: |
        The Lagrangian is L=P(X), where X = ∂_μ φ ∂^μ φ for a scalar field φ. For a superfluid described by a complex scalar Ψ, the dynamics are governed by its phase θ, and X is related to ∂_μ θ ∂^μ θ.
      justification: |
        P(X) theories are a class of Effective Field Theories (EFTs) where the Lagrangian is an arbitrary function of the scalar field's kinetic term. The specific form `X=μ−θ′/a` is the realization of this kinetic term for a superfluid with a conserved number density in a homogeneous, isotropic FRW spacetime, viewed by a comoving observer. This mapping is the theoretical foundation for the model in COSMO-005.
      references:
        - title: k-Inflation
          where: Phys.Rev.D 63, 063504 (2001) [astro-ph/0008004]
          date: 2000-08-01
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The model must be free of gradient instabilities, requiring its sound speed `c_s^2 = (∂P/∂X) / (m_H ∂n/∂X) ≥ 0` at all times."
      domain: theory
      falsifier: "A set of best-fit P(X) parameters inferred from data that results in a history where `c_s^2 < 0` for a cosmologically significant period would invalidate the model."
      status: proposed
      links: [COSMO-005]
    - statement: "In the `c_s → 0` limit, the superfluid must reproduce ΛCDM observables to within 0.1% for CMB power spectra."
      domain: phenomenology
      falsifier: "Failure to match ΛCDM predictions within the specified tolerance after marginalizing over `P(X)` parameters that drive the model to the `c_s → 0` limit."
      status: under-test
      links: [COSMO-005]
naming_notes:
  collisions: [The symbol 'X' is commonly used for a spatial coordinate or an unknown variable.]
  disambiguation: |
    Within the context of P(X) Effective Field Theories, `X` almost universally refers to the scalar field's kinetic term, not a spatial coordinate. It is always the argument of the pressure or Lagrangian function `P`.
crosslinks:
  near_synonyms: [K_ESSENCE_FIELD]
  antonyms: [POTENTIAL_TERM_V]
  prerequisites: [CHEMICAL_POTENTIAL_MU, SCALAR_FIELD_PHASE_THETA]
  downstream_effects: [SOUND_SPEED_CS2, EQUATION_OF_STATE_W]
license: CC-BY-SA-4.0