---
term: "V(Γ)"
canonical_id: "V"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["COSMO-003"]
---

---
term: Potential of the Γ Field
canonical_id: V_GAMMA
symbol: V(Γ)
aliases: [Unified Dark Sector Potential, Pressuron Potential]
parents: [COSMO-003, MATH-018, MATH-019, MATH-020, COSMO-Γ-000]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: COSMO-003
      lines: "Section 5"
      snippet: |
        V(Γ) = ½ m_Γ² Γ² + μ⁴ [1 − e^{−Γ/Γ_*}]  (μ≪m_Γ, Γ_*>0)
        • Early: quadratic dominates → CDM-like oscillations.
        • Late: as Γ amplitude redshifts, field probes the shallow exp tail; slow-roll sets in with tracker behavior...
  editors: [Pirouette Agent]
  review_log: []
triad:
  art: |
    A cosmic valley whose floor, once steep, flattens into an endless plain. This landscape guides the universe's evolution, transitioning it from a vibrant dance of matter into a slow, final, accelerating expansion.
  law: |
    The shape of the potential V(Γ), specified by its parameters {m_Γ, μ, Γ_*/f}, uniquely determines the cosmic evolution of the Γ-fluid's equation of state, w_Γ(z), and effective sound speed, c_s,eff². This evolution must simultaneously match CMB, BAO, and SNe data when the model is anchored by a single D3 constant.
  philosophy: |
    V(Γ) embodies the principle of dynamical unification. It proposes that the 'coincidence' of dark matter and dark energy densities is not an accident of time but an inevitable evolutionary stage of a single field traversing a pre-determined landscape. Its purpose is to replace the arbitrary constant Λ with a physical mechanism derived from field theory.
pirouette_definition: |
  The scalar potential governing the dynamics of the Γ field. It consists of a quadratic core (½ m_Γ² Γ²) responsible for early-universe, pressureless, CDM-like oscillations of the field. This core is appended with a shallow late-time tail (e.g., exponential or cosine form) that becomes dominant as the field's oscillation amplitude decays due to cosmic expansion. This tail initiates a slow-roll phase, causing cosmic acceleration and dynamically resolving the coincidence problem.
operational_definition:
  units: Energy density (eV⁴ in natural units).
  symbol_table:
    - name: V(Γ)
      meaning: Potential energy density of the Γ field.
      dimensions: M L⁻¹ T⁻²
      default_range: contextual
    - name: m_Γ
      meaning: Mass of the Γ quantum ("pressuron"); sets the scale of the quadratic core.
      dimensions: M
      default_range: ~10⁷ eV
    - name: μ
      meaning: Energy scale of the potential's late-time tail.
      dimensions: M
      default_range: ~10⁻³³ eV
    - name: Γ_* or f
      meaning: Field excursion scale of the tail.
      dimensions: M
      default_range: > M_pl
  measurement:
    procedures:
      - name: Cosmological Parameter Inference
        outline: |
          Constrain the potential's parameters {m_Γ, μ, Γ_*/f} by performing a joint Bayesian analysis of cosmological data sets, primarily CMB power spectra (TT, TE, EE, lensing), Baryon Acoustic Oscillations (BAO), and Type Ia Supernovae (SNe) luminosity distances. This is implemented by embedding the Γ dynamics derived from V(Γ) into a Boltzmann code (e.g., CLASS) and running MCMC chains against observational data.
        expected_signals: [A specific expansion history H(z), an equation of state w_Γ(z) that transitions from ~0 to ~-1, a characteristic scale-dependent suppression of the matter power spectrum.]
        pitfalls: [Parameter degeneracies with H₀ and Ω_b, numerical instabilities in the Boltzmann solver for stiff regimes, biased parameter reconstruction due to restrictive priors.]
context_windows:
  - module: COSMO-003
    excerpt: |
      Goal: explain ρ_DM ~ ρ_DE today without tuning.
      Mechanism: **tracker/attractor tail** appended to quadratic core of V(Γ), consistent with D2 (analytic, local, scale-covariant). Two options:
      (1) Exponential tail (analytic):
      V(Γ) = ½ m_Γ² Γ² + μ⁴ [1 − e^{−Γ/Γ_*}]
      (2) Cosine tail (shift‑symmetry remnant):
      V(Γ) = ½ m_Γ² Γ² + μ⁴ [1 − cos(Γ/f)]
  - module: COSMO-003
    excerpt: |
      If m_Γ≈O(MeV), Γ begins oscillating extremely early (T≫MeV); it behaves like CDM thereafter. Late‑time DE behavior requires a shallow tail in V(Γ) that slows the background today.
poetic_connections:
  motifs: [unification, dynamical landscape, cosmic winter, attractor]
  evocative_lines:
    - "Coincidence arises because slow-roll only turns on when the oscillation amplitude decays into the tail—set by μ, not by arbitrary time."
    - "Hubble friction freezes it (Γ̇≈0) until H≈m_Γ, after which Γ oscillates..."
  association_matrix:
    - [ "COINCIDENCE_PROBLEM", 0.9 ]
    - [ "GAMMA_FIELD", 0.9 ]
    - [ "DARK_ENERGY", 0.7 ]
formal_mappings:
  candidates:
    - target: Quintessence Potential V(ϕ)
      domain: GR
      mapping_kind: mathematical
      equation_hint: |
        S = ∫ d⁴x √-g [½ g^{μν}∂_μΓ ∂_νΓ - V(Γ)]
      justification: |
        V(Γ) is a specific model of a quintessence potential for a canonical scalar field. The two-part structure (quadratic core + shallow tail) is designed to produce a "freezing" and "thawing" behavior, where the field first acts as dark matter and later as dark energy. The tracker/attractor nature of the tail is a known feature of certain quintessence models aimed at solving the coincidence problem.
      references:
        - title: Cosmological Tracker Solutions
          where: Phys.Rev.D 59, 123504 (1999)
          date: 1999-01-20
      confidence: 0.9
    - target: Axion-like Particle (ALP) Potential
      domain: EFT
      mapping_kind: conceptual
      equation_hint: |
        V(Γ) = ½ m_Γ² Γ² + μ⁴ [1 - cos(Γ/f)]
      justification: |
        The cosine-tail variant of V(Γ) is explicitly motivated as a remnant of a spontaneously broken shift symmetry, which is the defining characteristic of an axion or ALP. In this picture, the quadratic term represents the standard mass potential, while the cosine term is a non-perturbative instanton effect.
      references: []
      confidence: 0.8
  adopted:
    - target: Quintessence Potential V(ϕ)
      rationale: The framework treats Γ as a generic classical scalar field whose dynamics are governed by a potential in the standard Lagrangian formulation. This is the definition of a quintessence field. The specific two-part structure is a model choice within this broader paradigm.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "The potential V(Γ), with parameters anchored by a single D3 one-shot measurement, can simultaneously explain the observed dark matter and dark energy content of the universe."
      domain: phenomenology
      falsifier: "A statistically significant preference (e.g., ΔBIC > 10) for a two-fluid ΛCDM model over the V(Γ) model after fitting to a combination of CMB, BAO, and SNe data."
      status: proposed
      links: [COSMO-003, MATH-018]
    - statement: "The late-time tail of V(Γ) creates a dynamical attractor solution that drives the equation of state w_Γ towards -1, independent of a wide range of early-universe initial conditions for Γ."
      domain: theory
      falsifier: "Numerical evolution showing that the late-time equation of state w_Γ is highly sensitive to the initial values (Γ_ini, Γ̇_ini), or that the late-time fixed points of the dynamical system are unstable."
      status: proposed
      links: [COSMO-003]
naming_notes:
  collisions: [Gravitational Potential (Φ, Ψ), Volume (V), V-mode CMB polarization]
  disambiguation: |
    V(Γ) is the potential energy density of the cosmological scalar field Γ. It is a function of the field amplitude and dictates its dynamics. It should not be confused with the metric potentials Φ and Ψ from cosmological perturbation theory.
crosslinks:
  near_synonyms: [QUINTESSENCE_POTENTIAL]
  antonyms: [COSMOLOGICAL_CONSTANT]
  prerequisites: [GAMMA_FIELD]
  downstream_effects: [EQUATION_OF_STATE_GAMMA, GROWTH_OF_STRUCTURE]
license: CC-BY-SA-4.0