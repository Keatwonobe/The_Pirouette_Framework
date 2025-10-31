---
term: "Field Form"
canonical_id: "FIELD_FORM"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["COSMO-004"]
---

---
term: Field Form
canonical_id: FIELD_FORM
symbol: 
aliases: [Full Field, Direct Integration]
parents: [COSMO-004]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: COSMO-004
      lines: "A1"
      snippet: |
        A1. Background (FIELD FORM)
        Γ′′ + 2ℋ Γ′ + a² V_{,Γ}(Γ) = 0
  editors: [pirouette-agent-v1]
  review_log: []
triad:
  art: |
    The field dances to its own inner law, its motion a direct response to the stretching cosmos and the shape of its own potential. It is the raw wave, not yet coarse-grained into the sea.
  law: |
    The evolution of the scalar field Γ and its perturbation δΓ is determined by direct numerical integration of their second-order Klein-Gordon equations, without approximation as a fluid.
  philosophy: |
    To capture the full dynamics of a scalar field, especially during transitions or on small scales, one must solve its equation of motion directly. The Field Form embodies this principle of fidelity, treating the field as a fundamental degree of freedom rather than a simplified fluid, ensuring accuracy at the cost of computational expense.
pirouette_definition: |
  The method of evolving a scalar field component, Γ, by directly integrating its fundamental second-order partial differential equations for both the homogeneous background and the linear perturbations. This approach contrasts with effective fluid approximations, treating Γ as a fundamental degree of freedom at all times and scales. It is the default, high-fidelity evolution method in Pirouette cosmological solvers, as specified in COSMO-004 sections A1 and A2.
operational_definition:
  units: Dimensionless (within solver context, e.g., M_pl = 1)
  symbol_table:
    - name: Γ
      meaning: Homogeneous scalar field value
      dimensions: M
      default_range: "contextual, ~M_pl"
    - name: Γ′
      meaning: Conformal-time derivative of Γ
      dimensions: M
      default_range: contextual
    - name: δΓ
      meaning: First-order perturbation to Γ
      dimensions: M
      default_range: contextual
    - name: V(Γ)
      meaning: Scalar field potential
      dimensions: M⁴
      default_range: contextual
    - name: ℋ
      meaning: Conformal Hubble parameter, a′/a
      dimensions: L⁻¹
      default_range: contextual
    - name: k
      meaning: Comoving wavenumber
      dimensions: L⁻¹
      default_range: 1e-5 – 10 Mpc⁻¹
  measurement:
    procedures:
      - name: Boltzmann Code Integration
        outline: |
          Implement the background equation `Γ′′ + 2ℋ Γ′ + a² V,Γ = 0` and the perturbation equation `δΓ′′ + 2ℋ δΓ′ + (k² + a² V,ΓΓ)δΓ = 4Γ′Φ′ − 2a²V,ΓΦ` into a numerical cosmological solver (e.g., CLASS, CAMB). The solver integrates this system of coupled ODEs from super-horizon initial conditions to produce observables.
        expected_signals: [Modified CMB power spectra (TT, TE, EE), Modified matter power spectrum P(k)]
        pitfalls: [Numerical stiffness when the field oscillates rapidly (m_Γ ≫ H), requiring small step sizes or a switch to a fluid approximation. Incorrect implementation of coupling terms to metric potentials.]
context_windows:
  - module: COSMO-004
    excerpt: |
      A1. Background (FIELD FORM)
      Γ′′ + 2ℋ Γ′ + a² V_{,Γ}(Γ) = 0
      ...
      A2. Perturbations (Newtonian Gauge, FULL FIELD)
      δΓ′′ + 2ℋ δΓ′ + (k² + a² V_{,ΓΓ}) δΓ = 4 Γ′ Φ′ − 2 a² V_{,Γ} Φ
  - module: COSMO-004
    excerpt: |
      /* perturbations_derivs.c */
      /* u[delta_gamma] = δΓ, u[delta_gamma_p] = δΓ′ */
      udot[delta_gamma]    = u[delta_gamma_p];
      udot[delta_gamma_p]  = -2*H_conf*u[delta_gamma_p]
      - (k2 + a*a*Vsecond(gamma)) * u[delta_gamma]
      + 4*gamma_p*phi_p - 2*a*a*Vprime(gamma)*phi;
poetic_connections:
  motifs: [fundamental dynamics, direct integration, wave mechanics, field-fluid duality]
  evocative_lines:
    - "σ_Γ = 0 (canonical scalar)"
    - "Omega_gamma_auto=on"
  association_matrix:
    - [ "FLUID_MAPPING", 0.9 ]
formal_mappings:
  candidates:
    - target: Klein-Gordon Equation
      domain: GR
      mapping_kind: mathematical
      equation_hint: |
        ∇ᵤ∇ᵘΦ + V'(Φ) = 0
      justification: |
        The Field Form equations for Γ and δΓ are the Klein-Gordon equation for a canonical scalar field in a perturbed Friedmann-Lemaître-Robertson-Walker metric, expressed in conformal time and Newtonian gauge. The background equation governs the homogeneous mode, while the perturbation equation governs the evolution of Fourier modes.
      references:
        - title: Cosmological Perturbation Theory
          where: Mukhanov, Feldman, & Brandenberger, Phys.Rept. 215 (1992)
          date: 1992-06-01
      confidence: 1.0
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The Field Form provides a more accurate description of Γ dynamics than the Fluid Mapping, especially during slow-roll-to-oscillation transitions and for modes with k ~ a*m_Γ."
      domain: theory
      falsifier: "Demonstrating a scenario where the Fluid Mapping with its effective sound speed reproduces the full Field Form results to within numerical precision across all relevant regimes, rendering the more expensive Field Form redundant."
      status: supported
      links: [COSMO-004]
naming_notes:
  collisions: []
  disambiguation: |
    Distinguish from 'Fluid Mapping' (or 'Fluid Form'), which is an effective approximation of the Field Form valid only in highly oscillatory regimes (m_Γ ≫ H). Field Form is the exact, fundamental evolution method.
crosslinks:
  near_synonyms: []
  antonyms: [FLUID_MAPPING]
  prerequisites: [SCALAR_FIELD_GAMMA]
  downstream_effects: [CMB_POWER_SPECTRA, MATTER_POWER_SPECTRUM]
license: CC-BY-SA-4.0