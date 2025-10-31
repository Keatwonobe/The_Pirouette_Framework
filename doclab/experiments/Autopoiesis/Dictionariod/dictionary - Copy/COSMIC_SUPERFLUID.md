---
term: "Cosmic Superfluid"
canonical_id: "COSMIC_SUPERFLUID"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["SECT-001"]
---

---
term: Cosmic Superfluid
canonical_id: COSMIC_SUPERFLUID
symbol: 
aliases: [Superfluid Pressuron, Pressuron Condensate]
parents: [SECT-001]
children: [SECT-Γ-A-HALO, SECT-Γ-A-CMB]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: SECT-001
      lines: "L15-L23"
      snippet: |
        Your description (“tension to space… surface tension against gravity… vacuum as fuzzy baseline that creeps like the CMB”) maps cleanly to a **compressible superfluid** with: (i) finite surface tension at interfaces, (ii) phonon sound speed c_s, (iii) rarefied “desert” regions where density n → 0 and phase stiffness weakens.
  editors: [system-agent]
  review_log: []
triad:
  art: |
    The universe is a quantum fluid on the grandest scale. Galaxies are not just collections of stars but dense, self-gravitating droplets condensing from a cosmic mist, their edges defined by a delicate surface tension against the void.
  law: |
    The collective, low-energy dynamics of a heavy (17 MeV) pressuron condensate are described by a P(X) effective field theory, yielding a scale-dependent sound speed `c_s(k)` and surface tension `σ`. These emergent properties govern all structure from halo cores to mergers, and must remain consistent with CMB acoustic peaks at recombination.
  philosophy: |
    To explain dark sector phenomena without positing new fundamental ultralight particles. Instead, long-wavelength "ultralight" behavior emerges as the collective phonon mode of a heavy microscopic constituent, unifying disparate scales under a single substance.
pirouette_definition: |
  The macroscopic, collective state of pressurons behaving as a compressible, irrotational fluid on cosmic scales. Its dynamics are governed by a P(X) effective field theory characterized by a sound speed `c_s` and surface tension `σ`. Its low-energy excitations (phonons) are the ultralight, long-wavelength modes responsible for cosmic structure formation, while its finite healing length `ξ` and surface tension `σ` determine the structure of galactic halos and their merger dynamics.
operational_definition:
  units: Mixed. `c_s` in km/s, `σ` in MeV³, `ξ` in kpc, `m_H` in MeV.
  symbol_table:
    - name: m_H
      meaning: Mass of the microscopic constituent pressuron.
      dimensions: M
      default_range: 17 MeV (fixed by XXP-015)
    - name: c_s
      meaning: Superfluid sound speed of the phonon mode.
      dimensions: L T⁻¹
      default_range: 10-300 km/s (in halos)
    - name: σ
      meaning: Surface tension at the superfluid interface.
      dimensions: M L T⁻² / L² = M T⁻²
      default_range: contextual, derived from P(X)
    - name: ξ
      meaning: Healing length; characteristic scale for density recovery at an interface.
      dimensions: L
      default_range: 0.1-10 kpc
    - name: P(X)
      meaning: Pressure as a function of the kinetic/potential term X, defining the equation of state.
      dimensions: M L⁻¹ T⁻²
      default_range: P(X) = αX¹⁺β + δX²
    - name: Σ_0
      meaning: Predicted constant central surface density of halos (ρ_0 * r_c).
      dimensions: M L⁻²
      default_range: ~140 M_☉/pc² (from COSMO-Γ-HALO)
  measurement:
    procedures:
      - name: Halo Core Profile Fitting
        outline: |
          1. Measure high-resolution rotation curves or gravitational lensing maps for a sample of galaxies (dwarfs to clusters).
          2. Numerically solve the superfluid hydrostatic equilibrium (Lane-Emden-like) equation derived from the P(X) model for a given set of parameters {α, β, δ}.
          3. Fit the resulting density profiles to the observational data to constrain `c_s` and `ξ` for each halo.
          4. Test for the emergence of a nearly mass-independent central surface density, Σ_0.
        expected_signals: [Cored density profiles (not cuspy), A universal locus for Σ_0 across mass scales]
        pitfalls: [Baryonic feedback mimicking core formation, Insufficient resolution to distinguish from other core models]
      - name: Merger Offset Analysis
        outline: |
          1. Identify a sample of galaxy cluster mergers with clear separation between mass components (e.g., via weak lensing) and galactic components (e.g., via optical imaging).
          2. Measure the line-of-sight relative velocity `v_rel` and the on-sky projected offset Δx.
          3. Compute the predicted effective cross-section `(σ/m)_eff` from the superfluid model, which depends on `σ`, `ξ`, `c_s`, and `v_rel`.
          4. Compare the observed {Δx, `v_rel`} distribution against the model's predictions, including its redshift scaling.
        expected_signals: [Offsets consistent with `(σ/m)_eff ≲ 0.2 cm²/g`, A specific `v_rel` dependence from phonon radiation and interface work]
        pitfalls: [Projection effects contaminating Δx and `v_rel` measurements, Complex merger geometries not captured by two-body approximation]
context_windows:
  - module: SECT-001
    excerpt: |
      Realize the 17 MeV pressuron as a **microscopic constituent** of a cosmic superfluid whose **collective phonon mode** supplies the ultralight, long‑wavelength dynamics needed for structure formation, without introducing a new fundamental particle. Encode the superfluid in a symmetry‑respecting P(X) EFT; derive halo cores, merger behavior, and CMB‑consistent linear perturbations; set falsifiable signatures.
  - module: SECT-001
    excerpt: |
      Static spherical equilibrium with gravitational potential Φ solves a **Lane–Emden‑like** equation with finite central pressure. Core predictions: **Constant surface‑density locus** Σ_0 ≡ ρ_0 r_c emerges from ξ and σ, nearly mass‑independent. **Vortex spectrum** in rotating systems: quantized circulation κ_v = 2π/m_H; predicts a minimal vortex spacing.
poetic_connections:
  motifs: [emergent phenomena, quantum-to-cosmic, surface tension, sound of silence, cosmic web as fluid]
  evocative_lines:
    - "vacuum as fuzzy baseline that creeps like the CMB"
    - "macroscopic drag arises from phonon radiation & interface work"
    - "lip structures"
  association_matrix:
    - [ "PRESSURON", 0.9 ]
    - [ "HALO_CORE", 0.8 ]
    - [ "MERGER_OFFSET", 0.7 ]
    - [ "P_OF_X_EFT", 0.9 ]
formal_mappings:
  candidates:
    - target: P(X) theory / k-essence
      domain: EFT
      mapping_kind: mathematical
      equation_hint: |
        L_eff = P(X) − ...  , where X = μ − (∂_t θ + (∇θ)²/2m_H) − Φ_g
      justification: |
        The core of the model is a non-relativistic P(X) effective field theory. This is the direct analogue of P(X) theories used in cosmology for inflation or dark energy (like k-essence), but adapted to a non-relativistic, U(1) symmetric system representing a particle condensate.
      references:
        - title: Cosmological P(X) models
          where: General reviews on modified gravity/dark energy
          date: 2010-01-01
      confidence: 1.0
    - target: Healing Length (condensed matter)
      domain: AMO
      mapping_kind: conceptual
      equation_hint: |
        ξ ≡ ħ/(√2 m_H c_s)
      justification: |
        The symbol `ξ` and its definition are taken directly from the theory of superfluids and Bose-Einstein condensates. It represents the characteristic length scale over which the order parameter (the wavefunction `ψ`) recovers to its bulk value near a boundary or perturbation.
      references:
        - title: "Bose-Einstein Condensation"
          where: Pethick & Smith, Cambridge University Press
          date: 2008-01-01
      confidence: 1.0
  adopted:
    - target: Compressible, irrotational barotropic fluid
      rationale: On large scales, the P(X) theory's behavior is exactly that of a perfect fluid with a specific barotropic equation of state p=p(ρ) derived from P(X), and an effective, scale-dependent sound speed. This provides a direct interface to standard cosmological perturbation codes.
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "Galactic halos have central density cores with a nearly universal central surface density Σ_0 ≈ 140 M_☉/pc²."
      domain: phenomenology
      falsifier: "Wide-field surveys of galaxy kinematics and lensing find that Σ_0 systematically varies with halo mass, or that profiles are best-fit by cusps (e.g., NFW) after accounting for baryonic effects."
      status: proposed
      links: [SECT-Γ-A-HALO, COSMO-Γ-HALO]
    - statement: "Galaxy merger offsets are governed by macroscopic drag, yielding an effective cross-section (σ/m)_eff ≲ 0.2 cm²/g with a specific velocity dependence."
      domain: phenomenology
      falsifier: "Observations of bullet-like clusters require a significantly larger cross-section, or show a scaling with relative velocity inconsistent with interface work and phonon radiation."
      status: proposed
      links: [SECT-Γ-A, COSMO-Γ-MERGE]
    - statement: "The model's scale-dependent sound speed c_s(k,a) is sufficiently small at recombination to leave CMB acoustic peak locations and heights within Planck/SO observational contours."
      domain: theory
      falsifier: "Running the model in a Boltzmann code like CLASS shows that the effective fluid properties induce a phase shift in acoustic oscillations or a suppression of small-scale power that is inconsistent with CMB data."
      status: proposed
      links: [SECT-Γ-A-CMB, COSMO-Γ-CMB]
naming_notes:
  collisions: [Superfluid Dark Matter]
  disambiguation: |
    Unlike many "Superfluid Dark Matter" models that posit a new, fundamental ultralight (e.g., 10⁻²² eV) boson, the Cosmic Superfluid is an emergent, macroscopic state of a *heavy* (17 MeV) pressuron. The ultralight behavior arises from the collective phonon mode, not from the mass of the constituent particle.
crosslinks:
  near_synonyms: []
  antonyms: [PARTICULATE_CDM]
  prerequisites: [PRESSURON, P_OF_X_EFT]
  downstream_effects: [HALO_CORE, MERGER_OFFSET, VORTEX_SPECTRA]
license: CC-BY-SA-4.0
---

# Cosmic Superfluid

## Canonical (Pirouette)
The macroscopic, collective state of pressurons behaving as a compressible, irrotational fluid on cosmic scales. Its dynamics are governed by a P(X) effective field theory characterized by a sound speed `c_s` and surface tension `σ`. Its low-energy excitations (phonons) are the ultralight, long-wavelength modes responsible for cosmic structure formation, while its finite healing length `ξ` and surface tension `σ` determine the structure of galactic halos and their merger dynamics.

## EFT-First Summary
The Cosmic Superfluid is modeled as a non-relativistic P(X) effective field theory for a complex scalar field `ψ = √n e^(iθ)`, representing a condensate of 17 MeV pressurons. The Lagrangian `L_eff = P(X) - ...` dictates the equation of state and emergent properties like sound speed `c_s`, healing length `ξ`, and surface tension `σ`. This is mathematically analogous to k-essence theories in cosmology and directly maps to concepts from condensed matter superfluids, providing a framework where dark matter phenomenology arises from collective, not fundamental, properties.

## Glossary Links
- See also: [PRESSURON](...), [HALO_CORE](...), [P_OF_X_EFT](...)