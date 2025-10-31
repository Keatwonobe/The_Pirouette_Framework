---
term: "Phonon effective fluid"
canonical_id: "PHONON_EFFECTIVE_FLUID"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["COSMO-005"]
---

---
term: Phonon effective fluid
canonical_id: PHONON_EFFECTIVE_FLUID
symbol: 
aliases: [gammat_superfluid]
parents: [COSMO-005]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: COSMO-005
      lines: "14-16"
      snippet: |
        Scale‑dependent effective sound speed used in Boltzmann evolution:
        c_{s,eff}²(k,a) = c_s²(a) / [1 + (k/k_ξ(a))²],  with k_ξ(a)≡1/ξ(a),  ξ(a)=(2 m_H c_s(a))^{−1}.
  editors: [system]
  review_log: []
triad:
  art: |
    The collective whisper of a cosmic superfluid, treated as a tangible river shaping the growth of structure. It flows like cold dust across the cosmos, but recoils from disturbances smaller than its own quantum coherence.
  law: |
    The propagation speed of density perturbations within the fluid is suppressed on scales smaller than the coherence length ξ(a)=(2 m_H c_s(a))^{−1}, following the dispersion relation c_{s,eff}²(k,a) = c_s²(a) / [1 + (k/k_ξ(a))²].
  philosophy: |
    To provide a computationally efficient description of a superfluid dark sector for cosmological Boltzmann codes. This captures its macroscopic, long-wavelength dynamics without simulating the full quantum field theory, thereby enabling falsifiable predictions for CMB and LSS observables.
pirouette_definition: |
  A perfect fluid representation of the collective excitations (phonons) of the Pressuron superfluid, used for cosmological perturbation theory in Boltzmann codes like CLASS/CAMB. It is characterized by a scale-dependent effective sound speed, `c_{s,eff}²(k,a)`, which interpolates between the macroscopic sound speed `c_s²(a)` on large scales and zero on small scales. This feature suppresses structure growth below the coherence length `ξ(a)`, providing a potential solution to small-scale structure challenges while remaining consistent with ΛCDM on large scales.
operational_definition:
  units: Dimensionless (in natural units where c=1).
  symbol_table:
    - name: c_{s,eff}²
      meaning: Scale-dependent effective sound speed squared.
      dimensions: dimensionless
      default_range: "[0, 10⁻⁶]"
    - name: c_s²
      meaning: Macroscopic (background) sound speed squared of the superfluid.
      dimensions: dimensionless
      default_range: "[0, 10⁻⁶]"
    - name: k_ξ
      meaning: Wavenumber corresponding to the coherence length.
      dimensions: L⁻¹
      default_range: contextual
    - name: ξ
      meaning: Coherence length of the superfluid phonons.
      dimensions: L
      default_range: contextual
    - name: δ_Γ
      meaning: Density perturbation of the phonon fluid.
      dimensions: dimensionless
      default_range: contextual
    - name: θ_Γ
      meaning: Velocity divergence of the phonon fluid.
      dimensions: L⁻¹
      default_range: contextual
  measurement:
    procedures:
      - name: Cosmological Inference via Boltzmann Code
        outline: |
          The fluid's properties are not measured directly but are inferred.
          1. Implement the fluid's background and perturbation equations (for `δ_Γ`, `θ_Γ`) into a Boltzmann code (e.g., CLASS) as a new species (`gammat_superfluid`).
          2. The fluid's behavior is dictated by parameters of the underlying P(X) theory (e.g., `PofX_alpha`, `PofX_beta`).
          3. Run the code to compute theoretical CMB and matter power spectra for a grid of these parameters.
          4. Compare these theoretical predictions to observational data (e.g., from Planck, DES, Euclid) using a statistical sampler (e.g., MCMC) to find the best-fit parameters and their constraints.
        expected_signals: ["Suppression of the matter power spectrum on small scales (high k) relative to ΛCDM.", "Characteristic acoustic oscillations in the fluid's power spectrum, potentially visible in CMB lensing or galaxy clustering.", "A specific value for fσ₈(z) consistent with the model's modified growth history."]
        pitfalls: ["Degeneracies with other cosmological parameters, such as massive neutrinos or baryonic feedback effects, which also suppress small-scale power.", "Numerical instability in the Boltzmann code if the switch criteria between the full field and effective fluid descriptions are poorly implemented.", "The fluid approximation breaking down in non-linear regimes or on scales near the coherence length."]
context_windows:
  - module: COSMO-005
    excerpt: |
      Implement the superfluid Pressuron (P(X) EFT) in CLASS/CAMB with a phonon effective fluid that reproduces CDM on CMB scales while generating small‑scale suppression and halo cores. Provide exact mappings, stability thresholds, and artifact schemas.
  - module: COSMO-005
    excerpt: |
      Perturbations (Newtonian gauge, effective fluid):
      δ_Γ′ = −(1+w_Γ)(θ_Γ − 3Φ′) − 3ℋ (c_{s,eff}² − w_Γ) δ_Γ
      θ_Γ′ = −ℋ θ_Γ + k² Ψ + k² c_{s,eff}² δ_Γ/(1+w_Γ)
      with w_Γ≈0 through recombination (ensure c_{s,eff}² ≪ 10^{−6} on k relevant to ℓ≲2500).
poetic_connections:
  motifs: [superfluidity, collective excitation, cosmic acoustics, scale-dependent physics, emergent phenomena]
  evocative_lines:
    - "reproduces CDM on CMB scales while generating small‑scale suppression"
    - "Fall back to full field if either condition fails."
  association_matrix:
    - [ "Pressuron", 0.9 ]
    - [ "Coherence Length", 0.8 ]
    - [ "P(X) EFT", 0.9 ]
    - [ "Cold Dark Matter", 0.5 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Effective Fluid in Cosmology
      domain: GR
      mapping_kind: operational
      equation_hint: |
        δ′ = −(1+w)(θ − 3Φ′) − 3ℋ (cₛ² − w) δ
        θ′ = −ℋ(1-3w)θ − w′/(1+w) θ + k²cₛ²/(1+w) δ + k²Ψ
      justification: |
        The Phonon effective fluid is explicitly defined by its stress-energy tensor components (ρ_Γ, p_Γ) and a set of linear perturbation equations for its density contrast (δ_Γ) and velocity divergence (θ_Γ). This formulation is designed to be directly implemented into standard cosmological Boltzmann codes, where it acts as a new dark matter component alongside baryons, photons, and neutrinos. Its primary distinction from standard CDM is a non-zero, scale-dependent sound speed `c_{s,eff}²`.
      references:
        - title: Cosmological Perturbation Theory
          where: Ma, C.-P. & Bertschinger, E. (1995), ApJ, 455, 7.
          date: 1995-12-10
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "In the c_s→0 limit, the Phonon effective fluid reproduces the CMB TT, TE, and EE power spectra of ΛCDM to within 0.1% for ℓ≲2500."
      domain: phenomenology
      falsifier: "A robust numerical implementation shows deviations >0.1% from ΛCDM spectra in this limit, implying a failure of the fluid approximation or an unaccounted-for interaction."
      status: supported
      links: [COSMO-005]
    - statement: "The fluid description is numerically stable and accurate when the heavy quanta mass is large compared to the Hubble rate (m_H/H > 50) and the wave number is below a fraction of the mass (k/a < 0.5 m_H)."
      domain: theory
      falsifier: "Demonstrating that doubling the switching thresholds (e.g., m_H/H > 100) results in >0.2% changes to CMB observables, indicating that the transition region introduces significant numerical artifacts."
      status: supported
      links: [COSMO-005]
naming_notes:
  collisions: [The species name `gammat_superfluid` and subscript `_Γ` may be confused with photons (gamma, `γ`) in other contexts. The 't' in `gammat` is used for disambiguation within the CLASS code.]
  disambiguation: |
    This is an *effective* description of the collective motion of phonons, not a fundamental fluid. It is the long-wavelength, macroscopic limit of the underlying Pressuron superfluid field theory. On small scales or when the fluid approximation criteria are not met, a full field description is required.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [PRESSURON_SUPERFLUID, P_OF_X_EFT]
  downstream_effects: [COHERENCE_LENGTH]
license: CC-BY-SA-4.0
---

# Phonon effective fluid

## Canonical (Pirouette)
A perfect fluid representation of the collective excitations (phonons) of the Pressuron superfluid, used for cosmological perturbation theory in Boltzmann codes like CLASS/CAMB. It is characterized by a scale-dependent effective sound speed, `c_{s,eff}²(k,a)`, which interpolates between the macroscopic sound speed `c_s²(a)` on large scales and zero on small scales. This feature suppresses structure growth below the coherence length `ξ(a)`, providing a potential solution to small-scale structure challenges while remaining consistent with ΛCDM on large scales.

## EFT-First Summary
The Phonon effective fluid is the cosmological realization of the Goldstone boson (phonon) of a Pressuron superfluid dark matter model, described by a P(X) theory. Its properties, such as the scale-dependent sound speed `c_{s,eff}²`, are derived directly from the EFT Lagrangian `P(X)=αX^{1+β}+...`. This fluid approximation allows the EFT's predictions for large-scale structure and the CMB to be computed efficiently in standard Boltzmann codes, connecting the microphysics of the dark sector to observable cosmology.

## Glossary Links
- See also: Pressuron, P(X) EFT, Coherence Length, Cold Dark Matter