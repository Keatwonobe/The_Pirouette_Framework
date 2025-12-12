---
term: "Composite Superfluid"
canonical_id: "COMPOSITE_SUPERFLUID"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-021"]
---

---
term: Composite Superfluid
canonical_id: COMPOSITE_SUPERFLUID
symbol: 
aliases: [Phonon DM, Γ Condensate]
parents: [MATH-021]
children: [SECT-Γ-A, COSMO-Γ-MERGE, HALO/MERGE]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-021
      lines: "Mechanism A"
      snippet: |
        A1. The microscopic Γ quanta (m_H ≈ 17 MeV) form a self‑interacting condensate on cosmic scales; low‑energy excitations are phonons with dispersion ω^2 ≈ c_s^2 k^2 + m_eff^2.
  editors: [system-agent]
  review_log: []
triad:
  art: |
    A cosmic ocean of heavy Γ quanta whose collective whispers sculpt the galaxies. The universe as a resonant cavity where structure is the sound of a silent fluid.
  law: |
    The characteristic scale of galactic halos is determined by the sound speed (c_s) and effective phonon mass (m_eff) of the Γ condensate, which are emergent properties derived from the background density and self-interaction potential, P(X).
  philosophy: |
    This mechanism exemplifies ontological economy by deriving cosmological (IR) phenomena from a particle-scale (UV) sector through emergence. It posits that large-scale structure is not a new fundamental 'thing,' but the collective behavior of an already-postulated field.
pirouette_definition: |
  A proposed cosmological condensate formed by heavy Γ quanta (m_H ≈ 17 MeV). Its low-energy collective excitations (phonons) are described by an effective field theory with a sound speed c_s and an effective mass m_eff ≪ m_H. These phonons act as the dominant dark matter component, explaining galaxy-scale structure (e.g., halo cores) without requiring a fundamental ultralight particle.
operational_definition:
  units: SI (m, kg, s), eV for mass
  symbol_table:
    - name: m_H
      meaning: Mass of the fundamental Γ quantum
      dimensions: M
      default_range: ≈ 17 MeV/c²
    - name: m_eff
      meaning: Effective mass of the phonon excitation
      dimensions: M
      default_range: ≈ 10⁻²² eV/c²
    - name: c_s
      meaning: Sound speed in the condensate
      dimensions: L T⁻¹
      default_range: contextual (sets halo core size)
    - name: P(X)
      meaning: Effective pressure functional of the condensate
      dimensions: M L⁻¹ T⁻²
      default_range: contextual
    - name: n_0
      meaning: Background number density of the condensate
      dimensions: L⁻³
      default_range: contextual
  measurement:
    procedures:
      - name: Halo Core Profile Inversion
        outline: |
          Measure the density profiles (Σ) of a population of galaxy halos, particularly dwarf spheroidals. Fit the profiles using a solver based on the P(X) sound-speed equations of state. Invert the fit parameters to constrain c_s and the self-interaction scale.
        expected_signals: [Reproduces the universal Σ_0 core density locus, predicts distinct vortex/phonon spectra in massive ellipticals.]
        pitfalls: [Degeneracy with baryonic feedback effects, observational systematics in density profile measurements.]
      - name: Merger Dynamics Analysis
        outline: |
          Observe galaxy cluster mergers (e.g., Bullet Cluster analogs). Model the offset between the dark matter and stellar components. In the Composite Superfluid model, the apparent self-interaction cross-section (σ/m) is an emergent effect of collective dynamics and should saturate at a calculable value.
        expected_signals: [Apparent σ/m saturates at a value ≤ O(0.1) cm² g⁻¹ regardless of merger velocity.]
        pitfalls: [Complex merger geometries, difficulty in disentangling gravitational effects from self-interaction.]
context_windows:
  - module: MATH-021
    excerpt: |
      Mechanism A — Composite Superfluid & Phonon DM (Collective Mode)
      Hypothesis
      A1. The microscopic Γ quanta (m_H ≈ 17 MeV) form a self‑interacting condensate on cosmic scales; low‑energy excitations are phonons with dispersion ω^2 ≈ c_s^2 k^2 + m_eff^2.
      A2. The *effective* mass m_eff can be ≪ m_H and even behave as ∼10^−22 eV in the sense of setting the de‑Broglie/Jeans cutoff, without introducing a fundamental ultralight particle.
  - module: MATH-021
    excerpt: |
      Predictions / tests
      • Halo cores set by c_s and self‑interaction scale → reproduces Σ_0 locus; distinct vortex/phonon spectra in massive ellipticals.
      • Merger dynamics (COSMO‑Γ‑MERGE): apparent σ/m proxy saturates ≤ O(0.1) cm² g⁻¹ without fundamental self‑scattering.
      • Lab: no ultralight particle production; instead, look for medium‑dependent refractive effects in dense EM fields (afterglow‑like) governed by P(X) parameters.
poetic_connections:
  motifs: [emergence, superfluidity, collective mode, resonance, cosmic ocean]
  evocative_lines:
    - "the light mode governing structure is a *derived* eigenmode/collective excitation, not an ad‑hoc second particle"
    - "distinct vortex/phonon spectra in massive ellipticals"
  association_matrix:
    - [ "GAMMA_QUANTUM", 0.9 ]
    - [ "HALO_CORE_PROBLEM", 0.8 ]
    - [ "EMERGENCE", 0.8 ]
    - [ "CLOCKWORK_HIERARCHY", 0.2 ]
formal_mappings:
  candidates:
    - target: P(X) EFT
      domain: EFT
      mapping_kind: mathematical
      equation_hint: |
        L_eff = P(X), where X ≡ μ − m_H Φ − (∂θ)²/2m_H − …
      justification: |
        The low-energy dynamics of the condensate are described by a non-relativistic effective field theory where the Lagrangian is a general function (pressure) of the kinetic term X. This is a standard formalism for superfluids and k-essence.
      references:
        - title: "k-Essence"
          where: "Armendariz-Picon, C., et al. Phys. Rev. D 63, 103510 (2001)"
          date: 2000-11-20
      confidence: 0.9
    - target: Phonon
      domain: CM
      mapping_kind: conceptual
      equation_hint: |
        (∂_t² − c_s² ∇² + m_eff²)π = 0
      justification: |
        The low-energy, long-wavelength excitations (π) of the condensate are quantized sound waves, or phonons. Their dynamics are governed by a wave equation with a sound speed c_s set by the fluid's equation of state.
      references:
        - title: "Theory of Quantum Liquids"
          where: "Pines, D., & Nozières, P. (1966)"
          date: 1966-01-01
      confidence: 0.9
  adopted:
    - target: P(X) EFT for a non-relativistic condensate
      rationale: This is the explicit mathematical starting point described in MATH-021 for deriving the phenomenology of the Composite Superfluid.
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "The observed core density profiles of dark matter halos are determined by the sound speed c_s and self-interaction scale of the Γ condensate."
      domain: phenomenology
      falsifier: "Observed halo core properties (e.g., density, radius) show no correlation with halo mass or environment as predicted by the model, or are better fit by models without phonon pressure (e.g., pure CDM + baryonic feedback)."
      status: proposed
      links: [MATH-021, HALO/MERGE]
    - statement: "The apparent dark matter self-interaction cross-section σ/m in galaxy mergers is an emergent property that saturates at ≤ O(0.1) cm² g⁻¹."
      domain: phenomenology
      falsifier: "Observations of multiple cluster mergers robustly require a σ/m >> 0.1 cm² g⁻¹ or a strong velocity dependence inconsistent with the collective fluid dynamics."
      status: proposed
      links: [MATH-021, COSMO-Γ-MERGE]
    - statement: "No fundamental particle with mass ~10⁻²² eV corresponding to the Γ sector will be found in laboratory experiments."
      domain: experiment
      falsifier: "A direct-detection experiment discovers a fundamental particle matching the properties required for fuzzy dark matter, falsifying the emergent nature of the light mode."
      status: proposed
      links: [MATH-021]
naming_notes:
  collisions: [The term 'superfluid' is a direct analogy to its use in condensed matter physics (e.g., Helium-4). Its application here is cosmological and refers to a hypothetical substance.]
  disambiguation: |
    Distinguish from 'Superfluid Dark Matter' literature that may posit different underlying particles or dynamics. The 'Composite' qualifier emphasizes that the cosmologically relevant light particle (phonon) is a collective excitation of a much heavier fundamental particle (Γ).
crosslinks:
  near_synonyms: []
  antonyms: [CLOCKWORK_HIERARCHY]
  prerequisites: [GAMMA_QUANTUM]
  downstream_effects: [HALO_CORE_PROFILE, GALAXY_MERGER_DYNAMICS, CMB_LENSING_AMPLITUDE]
license: CC-BY-SA-4.0
---

# Composite Superfluid

## Canonical (Pirouette)
A proposed cosmological condensate formed by heavy Γ quanta (m_H ≈ 17 MeV). Its low-energy collective excitations (phonons) are described by an effective field theory with a sound speed c_s and an effective mass m_eff ≪ m_H. These phonons act as the dominant dark matter component, explaining galaxy-scale structure (e.g., halo cores) without requiring a fundamental ultralight particle.

## EFT-First Summary
The Composite Superfluid is modeled as a non-relativistic condensate whose low-energy dynamics are captured by a P(X) effective field theory. In this framework, the Lagrangian is treated as the effective pressure, `L_eff = P(X)`, where X is the kinetic argument. Linear perturbations around a homogeneous background density `n_0` behave as a quantized sound wave (a phonon, `π`) with a sound speed `c_s² = dP/dρ`. This emergent phonon field has an effective mass `m_eff` that governs the Jeans scale of cosmic structure, resolving the mass tension between the heavy constituent `Γ` particle and the needs of cosmology.

## Glossary Links
- See also: GAMMA_QUANTUM, CLOCKWORK_HIERARCHY, HALO_CORE_PROBLEM