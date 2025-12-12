---
term: "`gammat_superfluid`"
canonical_id: "GAMMAT_SUPERFLUID"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["COSMO-005"]
---

---
term: gammat_superfluid
canonical_id: GAMMAT_SUPERFLUID
symbol: '`gammat_superfluid`'
aliases: [Pressuron superfluid, Γ-superfluid]
parents: [COSMO-005]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: COSMO-005
      snippet: |
        Implement as species `gammat_superfluid` with variables {ρ_Γ(a), p_Γ(a)} obeying:
        ρ_Γ′ = −3ℋ (ρ_Γ + p_Γ).
  editors: [AI Assistant (Pirouette Dictionary Writer)]
  review_log: []
triad:
  art: |
    A cosmic whisper, cold as shadow on the grandest scales, yet buzzing with hidden warmth that hollows out the hearts of galaxies. It mimics the void's inertia but carries a repulsive core, a pressure that defines a minimum scale for collapse.
  law: |
    The cosmological impact of the Pressuron superfluid is governed by a scale-dependent effective sound speed, `c_{s,eff}²(k,a) = c_s²(a) / [1 + (k/k_ξ(a))²]`. This causes the fluid to behave as Cold Dark Matter for wavenumbers k ≪ k_ξ and as a pressure-supported fluid for k ≫ k_ξ, suppressing structure growth below the characteristic healing length ξ(a).
  philosophy: |
    To provide a concrete, falsifiable implementation of a dark matter alternative that resolves small-scale structure challenges (like the core-cusp problem) by introducing an effective pressure at galactic scales, while remaining indistinguishable from ΛCDM at cosmological scales probed by the CMB.
pirouette_definition: |
  The species identifier for a Pressuron superfluid component within cosmological Boltzmann codes (e.g., CLASS/CAMB). It is implemented as an effective fluid with background density `ρ_Γ` and pressure `p_Γ` derived from a P(X) effective field theory. Its perturbations are characterized by a scale-dependent effective sound speed `c_{s,eff}²(k,a)` that approaches zero on large scales, thereby reproducing CDM behavior, but becomes significant on small scales to suppress structure growth.
operational_definition:
  units: N/A (string identifier for a cosmological species). Associated quantities (ρ_Γ, p_Γ) use standard cosmological density/pressure units.
  symbol_table:
    - name: c_{s,eff}²
      meaning: Scale-dependent effective sound speed squared
      dimensions: dimensionless (in c=1 units)
      default_range: "[0, 1]"
    - name: c_s²
      meaning: Intrinsic background sound speed squared
      dimensions: dimensionless (in c=1 units)
      default_range: "[0, 1]"
    - name: k
      meaning: Comoving wavenumber
      dimensions: "L⁻¹"
      default_range: "[10⁻⁵, 10²] Mpc⁻¹"
    - name: k_ξ(a)
      meaning: Comoving wavenumber associated with the healing length, ξ(a)
      dimensions: "L⁻¹"
      default_range: "contextual"
    - name: w_Γ
      meaning: Equation of state parameter for the superfluid (p_Γ/ρ_Γ)
      dimensions: dimensionless
      default_range: ≈ 0 through recombination
  measurement:
    procedures:
      - name: Cosmological Simulation and Spectral Analysis
        outline: |
          1. Configure a Boltzmann code (e.g., CLASS) with `Gamma_species=superfluid` and set the `PofX` model parameters (α, β, δ).
          2. Run the code to evolve background and perturbation equations.
          3. Extract the computed CMB power spectra (TT, TE, EE) and matter power spectrum P(k).
          4. Compare the output spectra against ΛCDM predictions and observational data (e.g., from Planck, SDSS).
        expected_signals:
          - CMB angular power spectra matching ΛCDM to within ≤0.1% for ℓ≲2500.
          - A suppression in the matter power spectrum P(k) for k > k_ξ.
        pitfalls:
          - Numerical instability if the fluid-to-field switch thresholds (`switch_threshold_m_over_H`, `kappa_switch`) are improperly set.
          - Misinterpreting numerical artifacts from the `c_{s,eff}²` approximation as physical effects.
context_windows:
  - module: COSMO-005
    excerpt: |
      Perturbations (Newtonian gauge, effective fluid):
      δ_Γ′ = −(1+w_Γ)(θ_Γ − 3Φ′) − 3ℋ (c_{s,eff}² − w_Γ) δ_Γ
      θ_Γ′ = −ℋ θ_Γ + k² Ψ + k² c_{s,eff}² δ_Γ/(1+w_Γ)
      with w_Γ≈0 through recombination (ensure c_{s,eff}² ≪ 10^{−6} on k relevant to ℓ≲2500).
  - module: COSMO-005
    excerpt: |
      Stability & Validation Suite
      • Positivity: ρ_Γ>0, c_s²≥0, c_{s,eff}²≥0; enforce α>0, β∈{0,1/2,1}.
      • CMB limit: when c_s→0 and m_eff→0, spectra must match ΛCDM to ≤0.1% (V1).
      • Threshold scans: doubling switch thresholds changes TT/TE/EE by <0.2% (V5).
poetic_connections:
  motifs: [superfluidity, scale-dependent pressure, halo cores, cosmic phonon]
  evocative_lines:
    - "reproduces CDM on CMB scales while generating small‑scale suppression and halo cores."
    - "Phonon dispersion: ω² = c_s² k² + m_eff² with m_eff² from weak tail breaking"
  association_matrix:
    - [ "c_s^2", 0.9 ]
    - [ "HEALING_LENGTH", 0.8 ]
    - [ "HALO_CORE", 0.7 ]
formal_mappings:
  candidates:
    - target: Effective Fluid for P(X) Theory
      domain: EFT
      mapping_kind: operational
      equation_hint: |
        c_{s,eff}²(k,a) = c_s²(a) / [1 + (k/k_ξ(a))²]
      justification: |
        The `gammat_superfluid` is not a fundamental field but a numerical implementation of an effective fluid description for a Pressuron P(X) theory. The scale-dependent sound speed is the key operational mapping that captures the essential low-energy phonon dynamics without evolving the full field equations in the valid regime.
      references:
        - title: Superfluid Phonons in Boltzmann Codes (CLASS/CAMB)
          where: Pirouette Framework Module COSMO-005
          date: 2025-10-18
      confidence: 1.0
  adopted:
    - target: Effective Fluid for P(X) Theory
      rationale: This is the explicit purpose and definition of the term within the source module.
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "In the c_s→0 limit, the `gammat_superfluid` component produces CMB angular power spectra that match the standard ΛCDM model to within 0.1%."
      domain: phenomenology
      falsifier: "A CLASS/CAMB run with parameters set to the c_s→0 limit yields TT/TE/EE spectra that deviate from the ΛCDM baseline by more than 0.1% for ℓ≲2500."
      status: supported
      links: [COSMO-005]
    - statement: "The model's inherent small-scale pressure, via c_{s,eff}², suppresses the matter power spectrum sufficiently to form cored dark matter halos, in contrast to the cuspy halos of standard CDM."
      domain: theory
      falsifier: "High-resolution N-body simulations incorporating the `gammat_superfluid` effective pressure fail to produce halo density profiles with flat cores, or the required suppression level is ruled out by Lyman-alpha forest or weak lensing data."
      status: proposed
      links: [COSMO-005]
naming_notes:
  collisions: [The prefix 'gamma' or symbol Γ is standardly used for photons in cosmology.]
  disambiguation: |
    `gammat_superfluid` is a specific string identifier for a dark matter species in Boltzmann codes, derived from the Pirouette Framework's 'Gammat' (Γ) sector. It is entirely unrelated to the electromagnetic photon (γ). Context is typically clear as it appears in code configuration files or species lists.
crosslinks:
  near_synonyms: [PRESSURON_SUPERFLUID]
  antonyms: [COLD_DARK_MATTER]
  prerequisites: [P_OF_X_EFT]
  downstream_effects: [HALO_CORE_FORMATION, SMALL_SCALE_STRUCTURE_SUPPRESSION]
license: CC-BY-SA-4.0
---