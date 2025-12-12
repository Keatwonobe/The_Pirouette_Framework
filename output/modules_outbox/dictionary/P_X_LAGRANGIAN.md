---
term: "P(X) Lagrangian"
canonical_id: "P_X_LAGRANGIAN"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["SECT-001"]
---

---
term: P(X) Lagrangian
canonical_id: P_OF_X_LAGRANGIAN
symbol: L_eff, P(X)
aliases: [P(X) EFT, Superfluid EFT]
parents: [SECT-001, MATH-018, MATH-019, MATH-020, MATH-021, COSMO-Γ-000]
children: [SECT-Γ-A-HALO, SECT-Γ-A-CMB]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: SECT-001
      lines: "15-18"
      snippet: |
        • **P(X) Lagrangian** (lowest orders, analytic, D2‑compliant):
        L_eff = P(X) − κ (∇n)^2/(8 n) − σ |∇n|
        with P(X) = α X^{1+β} + δ X^2 + … (β≥0 rational from symmetry/scaling).
  editors: [system_agent]
  review_log: []
triad:
  art: |
    A cosmic fluid whose self-pressure, a deep non-linear springiness, sculpts the void into galaxies and webs. It resists gravity's pull with an emergent surface tension that is both its substance and its form.
  law: |
    The dynamics of a P(X) Lagrangian superfluid predict that halo cores of varying mass will exhibit a near-constant central surface density, Σ₀, whose value is determined by the Lagrangian parameters {α,β,σ} and the fundamental mass m_H.
  philosophy: |
    To derive complex cosmological structure (halo cores, merger dynamics) from the collective, emergent behavior of a known heavy particle (the 17 MeV pressuron), obviating the need for a new fundamental ultralight field.
pirouette_definition: |
  The effective field theory Lagrangian, `L_eff`, that governs the macroscopic dynamics of the cosmic superfluid. Its central component, `P(X)`, defines the pressure as a non-linear function of `X`, a variable representing the local deviation from the ground state chemical potential. The full Lagrangian, `L_eff = P(X) − κ (∇n)^2/(8n) − σ |∇n|`, also includes gradient terms that encode the superfluid's stiffness, giving rise to a finite healing length (ξ) and surface tension (σ). The functional form `P(X) = α X^{1+β} + δ X² + ...` dictates the equation of state, sound speed, and ultimately the observable behavior of cosmological structures.
operational_definition:
  units: Lagrangian density has units of energy density (J/m³). Cosmological calculations typically use natural units (ħ=c=1) and express quantities in powers of MeV.
  symbol_table:
    - name: L_eff
      meaning: Effective Lagrangian density
      dimensions: M L⁻¹ T⁻²
      default_range: contextual
    - name: P(X)
      meaning: Pressure as a function of X; leading term of L_eff
      dimensions: M L⁻¹ T⁻²
      default_range: contextual
    - name: X
      meaning: Non-relativistic chemical potential deviation, X ≡ μ − (∂_t θ + (∇θ)²/2m_H) − Φ_g
      dimensions: M L² T⁻² (energy)
      default_range: contextual
    - name: α, β, δ
      meaning: Dimensionless coefficients defining the P(X) function. β is a rational exponent.
      dimensions: dimensionless (α, δ have dimensions to make P(X) an energy density)
      default_range: β ∈ {0, 1/2, 1}; α>0; δ≥0
    - name: σ
      meaning: Surface tension coefficient
      dimensions: M T⁻² (energy/area)
      default_range: ≥ 0
    - name: ξ
      meaning: Healing length, ξ ≡ ħ/(√2 m_H c_s)
      dimensions: L
      default_range: kpc scale for galactic halos
    - name: c_s
      meaning: Superfluid sound speed, c_s² = ∂p/∂ρ
      dimensions: L T⁻¹
      default_range: ≪ 1 (in units of c)
  measurement:
    procedures:
      - name: Halo Core Profile Fitting
        outline: |
          1. Measure high-resolution rotation curves of galaxies to infer their dark matter density profiles.
          2. Numerically solve the Lane-Emden-like equation for a static, spherical superfluid governed by the P(X) Lagrangian.
          3. Fit the predicted density profile to the observed data, constraining combinations of P(X) parameters {α,β} which determine the core size `r_c` and central density `ρ₀`.
        expected_signals: [Cored halo profiles, a near-constant surface density Σ₀ ≈ ρ₀ r_c across a range of halo masses.]
        pitfalls: [Baryonic feedback can also create cores, requiring careful disentanglement; systematics in rotation curve measurements.]
      - name: Cosmological Perturbation Analysis
        outline: |
          1. Implement the superfluid as a `gammat_superfluid.c` module in a Boltzmann code like CLASS.
          2. The P(X) parameters {α,β,δ} and background number density n₀(a) determine the scale-dependent sound speed `c_s,eff(k,a)`.
          3. Run the code to compute CMB and matter power spectra.
          4. Compare with observational data (e.g., from Planck). The lack of observed deviation from ΛCDM constrains `c_s` at recombination to be `c_s ≪ 10⁻³c`.
        expected_signals: [CMB power spectra consistent with Planck data, with subtle deviations in lensing or ISW if parameters are in a specific range.]
        pitfalls: [Degeneracies with other cosmological parameters; model must fit CMB, BAO, and LSS data simultaneously.]
      - name: Merger Offset Measurement
        outline: |
          1. Identify merging galaxy clusters with clear separation between gravitational mass (from lensing) and baryonic gas (from X-ray).
          2. Measure the spatial offset Δx and relative velocity `v_rel`.
          3. The P(X) Lagrangian predicts an effective drag force from interface work and phonon radiation, yielding an effective cross-section `(σ/m)_eff` that depends on `σ`, `ξ`, `c_s`.
          4. Compare the observed Δx vs. `v_rel` relation to the model's prediction.
        expected_signals: [An effective cross-section `(σ/m)_eff ≲ 0.2 cm²/g` with a specific, predictable dependence on `v_rel`.]
        pitfalls: [Complex merger geometry and projection effects can complicate interpretation; requires a statistical sample of mergers.]
context_windows:
  - module: SECT-001
    excerpt: |
      **P(X) Lagrangian** (lowest orders, analytic, D2‑compliant):
      L_eff = P(X) − κ (∇n)²/(8 n) − σ |∇n|
      with P(X) = α X¹⁺ᵝ + δ X² + … (β≥0 rational from symmetry/scaling).
      The gradient terms generate finite healing length and **surface tension σ**.
  - module: SECT-001
    excerpt: |
      Linear perturbations (Newtonian gauge):
      Fluid form with **scale‑dependent** c_s,eff²(k) from the phonon dispersion:
      c_s,eff²(k) ≈ c_s² · [1 + (k/k_ξ)²]⁻¹,  k_ξ ≡ 1/ξ.
      Jeans‑like cutoff at k_J ~ aH/c_s where growth is suppressed; choose α,β to match halo core scales while keeping CMB acoustic peaks intact.
  - module: SECT-001
    excerpt: |
      With P(X)=α X¹⁺ᵝ and X≈μ−Φ−(∇θ)²/2m_H, the core solves a **Lane–Emden‑like** equation with finite central pressure.
      Core predictions:
      **Constant surface‑density locus** Σ₀ ≡ ρ₀ r_c emerges from ξ and σ: Σ₀ ≈ C(α,β,σ,m_H) nearly mass‑independent.
poetic_connections:
  motifs: [superfluidity, collective phenomena, surface tension, non-linearity, emergence]
  evocative_lines:
    - "surface tension against gravity"
    - "vacuum as fuzzy baseline that creeps like the CMB"
    - "realize the 17 MeV pressuron as a microscopic constituent of a cosmic superfluid"
  association_matrix:
    - [ "HALO_CORE", 0.9 ]
    - [ "SURFACE_TENSION", 0.8 ]
    - [ "COLLECTIVE_PHONON", 0.7 ]
    - [ "EMERGENCE", 0.6 ]
formal_mappings:
  candidates:
    - target: Gross-Pitaevskii Equation (GPE)
      domain: AMO|CM
      mapping_kind: conceptual
      justification: |
        The static Euler-Lagrange equations derived from `L_eff` are a generalized form of the GPE. While the GPE typically models a simple `g|ψ|⁴` contact interaction, the `P(X)` functional allows for a much richer, density-dependent interaction term, corresponding to a non-linear equation of state for the condensate.
      confidence: 0.85
  adopted:
    - target: P(X) theories (k-essence)
      domain: EFT
      mapping_kind: mathematical
      equation_hint: |
        Relativistic: X_rel = - (∂μφ)(∂^μφ)/2. Non-relativistic Pirouette: X_NR ≡ μ − (∂_t θ + (∇θ)²/2m_H) − Φ_g.
      rationale: |
        The Pirouette model is a specific non-relativistic limit of the general `P(X)` class of effective field theories, where `X` is constructed from derivatives of a field. This mapping provides the direct conceptual and mathematical lineage, but care must be taken to distinguish the non-relativistic definition of `X` from its common relativistic counterpart.
      confidence: 0.95
    - target: Barotropic Perfect Fluid
      domain: CM
      mapping_kind: operational
      equation_hint: |
        p = P(X) and ρ ≈ m_H n. This gives a barotropic Equation of State p = p(ρ).
      rationale: |
        On scales much larger than the healing length (ξ), the superfluid behaves as a perfect, irrotational fluid. Its equation of state is directly given by the `P(X)` function, allowing it to be modeled as a barotropic fluid in standard cosmological simulation codes (e.g., CLASS, GADGET), which is the primary operational use case.
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "The model predicts that galactic halos have cored density profiles characterized by a nearly universal central surface density Σ₀."
      domain: phenomenology
      falsifier: "Systematic observation of cuspy halo profiles (e.g., NFW) in dwarf galaxies, or a measured Σ₀ that strongly correlates with halo mass, would falsify the basic prediction."
      status: proposed
      links: [SECT-Γ-A-HALO, COSMO-Γ-HALO]
    - statement: "In merging clusters, the effective dark matter self-interaction is an emergent phenomenon of surface tension, predicting `(σ/m)_eff ≲ 0.2 cm²/g` with a specific velocity dependence."
      domain: phenomenology
      falsifier: "Observing merger offsets that are consistent with zero interaction across all velocities, or that require a much larger `(σ/m)_eff` with a different velocity scaling than predicted by the interface-drag model."
      status: proposed
      links: [SECT-Γ-A, COSMO-Γ-MERGE]
    - statement: "The same P(X) parameters that fit halo cores must also yield a sound speed `c_s` at recombination that is small enough to be consistent with Planck CMB data."
      domain: phenomenology
      falsifier: "A scenario where the best-fit halo parameters {α, β} unavoidably predict a `c_s` at last scattering that creates detectable phase shifts or damping in the CMB acoustic peaks, thus violating existing cosmological constraints."
      status: proposed
      links: [SECT-Γ-A-CMB]
naming_notes:
  collisions: [The symbol `P` is overloaded for Pressure and `P(X)`. The variable `X` is a standard symbol for the kinetic term in EFT, but its definition here is specific to the non-relativistic superfluid context.]
  disambiguation: |
    Distinguish from relativistic `P(X)` or k-essence theories where `X` is the Lorentz-invariant kinetic term `X = -g^{μν}∂_μφ∂_νφ / 2`. The Pirouette `P(X)` Lagrangian uses the non-relativistic `X ≡ μ − (∂_t θ + (∇θ)²/2m_H) − Φ_g`, which represents the deviation from the chemical potential in the fluid's rest frame.
crosslinks:
  near_synonyms: [SUPERFLUID_EFT]
  antonyms: [PARTICULATE_CDM]
  prerequisites: [PRESSURON, U1_PHASE_SYMMETRY]
  downstream_effects: [HALO_CORE, UNIVERSAL_SURFACE_DENSITY, MERGER_OFFSET, COLLECTIVE_PHONON]
license: CC-BY-SA-4.0
---

# P(X) Lagrangian

## Canonical (Pirouette)
The effective field theory Lagrangian, `L_eff`, that governs the macroscopic dynamics of the cosmic superfluid. Its central component, `P(X)`, defines the pressure as a non-linear function of `X`, a variable representing the local deviation from the ground state chemical potential. The full Lagrangian, `L_eff = P(X) − κ (∇n)^2/(8n) − σ |∇n|`, also includes gradient terms that encode the superfluid's stiffness, giving rise to a finite healing length (ξ) and surface tension (σ). The functional form `P(X) = α X^{1+β} + δ X² + ...` dictates the equation of state, sound speed, and ultimately the observable behavior of cosmological structures.

## EFT-First Summary
The P(X) Lagrangian is a specific application of effective field theory, analogous to k-essence or `P(X)` theories, but formulated in a non-relativistic limit suitable for a cosmic superfluid. It models the system as a barotropic perfect fluid on large scales, where the pressure-density relation (equation of state) is determined by the function `P(X)`. This allows for direct implementation into cosmological fluid codes and provides a framework for deriving structural properties like galactic halo cores from first principles.

## Glossary Links
- See also: [PRESSURON](./pressuron.md), [HALO_CORE](./halo_core.md), [SURFACE_TENSION](./surface_tension.md)