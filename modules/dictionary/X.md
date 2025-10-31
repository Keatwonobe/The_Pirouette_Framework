---
term: "X"
canonical_id: "X"
symbol: "X"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["SECT-001"]
---

---
term: X
canonical_id: X_VARIABLE
symbol: X
aliases: [Superfluid Potential, Galilean-Invariant Chemical Potential]
parents: [SECT-001, MATH-018, MATH-021]
children: [SECT-Γ-A-HALO, SECT-Γ-A-CMB]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: SECT-001
      snippet: |
        • Define X ≡ μ − (∂_t θ + (∇θ)^2/2m_H) − Φ_g  (Φ_g gravitational potential).
  editors: [GPT-4o (Dictionary Agent)]
  review_log: []
triad:
  art: |
    The fluid's will to be, a measure of its inner tension against the pull of gravity and the rush of its own motion. It is the pressure potential from which galaxies condense like dewdrops on a cold morning.
  law: |
    The quantity X is defined as the Galilean-invariant combination of the chemical potential (μ), kinetic energy per particle (K = ∂_t θ + (∇θ)²/2m_H), and gravitational potential (Φ_g), such that X ≡ μ − K − Φ_g. The local pressure (p) of the superfluid is a direct, state-dependent function of X, written as p = P(X).
  philosophy: |
    X promotes the complex interplay of quantum phase, fluid motion, and gravity into a single, Lorentz-breaking but Galilean-invariant scalar. This allows a non-relativistic EFT to describe cosmological dynamics, unifying dark matter and dark energy phenomena under a single fluidic substance without introducing a new fundamental light particle.
pirouette_definition: |
  The core variable of the P(X) effective field theory, representing the Galilean-invariant local energy available to the superfluid. It is defined as the chemical potential (μ) less the kinetic and gravitational potential energies per particle: X ≡ μ − (∂_t θ + (∇θ)²/2m_H) − Φ_g. The equation of state is given by the pressure p=P(X), making X the fundamental determinant of the fluid's thermodynamic and hydrodynamic behavior.
operational_definition:
  units: Energy (Joules or electron-Volts).
  symbol_table:
    - name: X
      meaning: Galilean-invariant superfluid potential
      dimensions: M L² T⁻²
      default_range: contextual; positive in gravitationally bound structures
    - name: μ
      meaning: Chemical potential
      dimensions: M L² T⁻²
      default_range: contextual
    - name: θ
      meaning: Superfluid phase angle
      dimensions: dimensionless
      default_range: "[0, 2π)"
    - name: m_H
      meaning: Mass of the microscopic constituent pressuron
      dimensions: M
      default_range: ≈17 MeV/c²
    - name: Φ_g
      meaning: Gravitational potential
      dimensions: L² T⁻²
      default_range: contextual
  measurement:
    procedures:
      - name: Reconstruction from Halo Hydrostatic Equilibrium
        outline: |
          1. Observationally determine the density profile ρ(r) and enclosed mass profile M(<r) for a galactic halo (e.g., from stellar kinematics, lensing).
          2. Calculate the gravitational potential Φ_g(r) from the mass profile.
          3. Assume hydrostatic equilibrium (∇p = -ρ∇Φ_g) and integrate to find the pressure profile p(r).
          4. Invert the calibrated equation of state p = P(X) to solve for the radial profile of the superfluid potential, X(r).
        expected_signals: [A reconstructed X(r) profile that is positive and finite at r=0, leading to a cored density profile, A derived constant surface density Σ₀ from the profile's properties.]
        pitfalls: [Model-dependence on the chosen form of P(X) (i.e., α, β), Contamination from baryonic physics in the inner halo, Observational uncertainties in ρ(r) and stellar kinematics.]
context_windows:
  - module: SECT-001
    excerpt: |
      Non‑relativistic EFT (Galilean, U(1) phase symmetry):
      • Field ψ = √n e^{iθ}; chemical potential μ.
      • Define X ≡ μ − (∂_t θ + (∇θ)^2/2m_H) − Φ_g (Φ_g gravitational potential).
      • **P(X) Lagrangian** (lowest orders, analytic, D2‑compliant):
      L_eff = P(X) − κ (∇n)^2/(8 n) − σ |∇n|
      with P(X) = α X^{1+β} + δ X^2 + …
  - module: SECT-001
    excerpt: |
      Static spherical equilibrium with gravitational potential Φ:
      • Euler: ∇p = −ρ ∇Φ  → dP/dn · dn/dr = −ρ dΦ/dr.
      • With P(X)=α X^{1+β} and X≈μ−Φ−(∇θ)^2/2m_H, the core solves a **Lane–Emden‑like** equation with finite central pressure.
poetic_connections:
  motifs: [superfluidity, potential energy, condensation, emergent structure, tension]
  evocative_lines:
    - "tension to space… surface tension against gravity…"
    - "vacuum as fuzzy baseline that creeps like the CMB"
  association_matrix:
    - [ "PRESSURE", 0.9 ]
    - [ "SOUND_SPEED_CS", 0.7 ]
    - [ "SURFACE_TENSION_SIGMA", 0.6 ]
    - [ "CHEMICAL_POTENTIAL", 0.8 ]
formal_mappings:
  candidates:
    - target: P(X) / k-essence theories
      domain: EFT
      mapping_kind: mathematical
      equation_hint: |
        L_eff = P(X) + ...
      justification: |
        The theory's Lagrangian L_eff = P(X) is mathematically analogous to P(X) or k-essence models in cosmology. However, this X is constructed to be Galilean-invariant for a non-relativistic fluid, representing a chemical potential, rather than the Lorentz-invariant kinetic term X = -½(∂μφ)(∂^μ φ) of a fundamental scalar field.
      references:
        - title: k-essence
          where: Armendariz-Picon, C.; Mukhanov, V. F.; Steinhardt, P. J. Phys. Rev. Lett. 85, 4438 (2000)
          date: 2000-11-20
      confidence: 0.9
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The function P(X) determines the equation of state, which predicts galactic halo cores with a nearly universal constant surface density Σ₀."
      domain: phenomenology
      falsifier: "Observational surveys of halos from dwarfs to clusters fail to find a constant Σ₀ locus, or its measured value is inconsistent with the frozen parameters {α,β,δ} required to fit CMB data."
      status: proposed
      links: [SECT-Γ-A, COSMO-Γ-HALO]
    - statement: "As the argument of the pressure, X governs the sound speed c_s(X), which must be c_s ≪ 10⁻³c at recombination to preserve CMB acoustic peaks."
      domain: phenomenology
      falsifier: "The parameter set {α,β,δ} that fits low-redshift structure (e.g., halo cores) implies a sound speed at z≈1100 that is large enough to erase or distort CMB acoustic peaks beyond Planck/future survey limits."
      status: proposed
      links: [SECT-Γ-A, SECT-Γ-A-CMB]
naming_notes:
  collisions: ["X in P(X) cosmology literature", "X-boson (GUTs)"]
  disambiguation: |
    This 'X' is not a fundamental particle. It is a specific Galilean-invariant scalar variable in a non-relativistic EFT, representing an effective chemical potential. It is functionally analogous to the kinetic term 'X' in cosmological P(X) k-essence models, but it is not Lorentz-invariant and has a different physical origin related to a fluid's internal and kinetic energy.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [CHEMICAL_POTENTIAL, GALILEAN_INVARIANCE, LAGRANGIAN_MECHANICS]
  downstream_effects: [HALO_CORE, SURFACE_TENSION_SIGMA, SOUND_SPEED_CS, VORTEX_SPECTRUM]
license: CC-BY-SA-4.0
---

# X

## Canonical (Pirouette)
The core variable of the P(X) effective field theory, representing the Galilean-invariant local energy available to the superfluid. It is defined as the chemical potential (μ) less the kinetic and gravitational potential energies per particle: X ≡ μ − (∂_t θ + (∇θ)²/2m_H) − Φ_g. The equation of state is given by the pressure p=P(X), making X the fundamental determinant of the fluid's thermodynamic and hydrodynamic behavior.

## EFT-First Summary
In the language of effective field theory, X is the central variable in a P(X)-type model for a non-relativistic cosmic superfluid. Analogous to the kinetic term in k-essence theories, X is a Galilean-invariant combination of chemical, kinetic, and potential energies. The Lagrangian, and thus the pressure, is a direct function P(X), which defines the fluid's equation of state and its emergent cosmological dynamics, from CMB-scale perturbations to galactic halo cores.

## Glossary Links
- See also: HALO_CORE, SURFACE_TENSION_SIGMA, SOUND_SPEED_CS