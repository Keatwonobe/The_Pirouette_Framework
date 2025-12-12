---
term: "Phonon DM"
canonical_id: "PHONON_DM"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-021"]
---

---
term: Phonon DM
canonical_id: PHONON_DM
symbol: π_DM
aliases: [Collective Mode DM, Superfluid DM, Γ Phonon DM]
parents: [MATH-021, MATH-018, COSMO-Γ-CMB]
children: [SECT-Γ-A, COSMO-Γ-MERGE]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-021
      snippet: |
        Mechanism A — Composite Superfluid & Phonon DM (Collective Mode)
        Hypothesis
        A1. The microscopic Γ quanta (m_H ≈ 17 MeV) form a self‑interacting condensate on cosmic scales; low‑energy excitations are phonons with dispersion ω^2 ≈ c_s^2 k^2 + m_eff^2.
        A2. The *effective* mass m_eff can be ≪ m_H and even behave as ∼10^−22 eV in the sense of setting the de‑Broglie/Jeans cutoff, without introducing a fundamental ultralight particle.
  editors: [System Agent]
  review_log: []
triad:
  art: |
    The cosmos is not a void filled with dust, but a silent ocean of condensed energy. Dark matter is not a lost particle, but the whisper of a sound wave propagating through this cosmic superfluid.
  law: |
    The observed dark matter is the energy of collective phonon modes (π) in a Γ-superfluid; its effective mass (m_eff ≈ 10⁻²² eV) and sound speed (c_s) are emergent properties set by the condensate's equation of state P(X), not by a fundamental particle mass.
  philosophy: |
    To resolve the mass tension in the Γ sector by positing that cosmological structure arises from an emergent, collective phenomenon (a "many-body" solution) rather than a fine-tuned fundamental particle (a "one-body" solution), upholding parsimony at the level of the fundamental Lagrangian.
pirouette_definition: |
  A candidate mechanism (Mechanism A in MATH-021) for resolving the Γ Mass Tension. It hypothesizes that dark matter is not a fundamental particle, but consists of the collective, quantized sound-wave excitations (phonons) within a cosmic superfluid. This superfluid is a Bose-Einstein condensate of the heavy Γ quanta (m_H ≈ 17 MeV). The cosmologically-relevant mass scale (m_eff ≈ 10⁻²² eV) that governs structure formation is an emergent property derived from the superfluid's equation of state, not an ad-hoc elementary particle mass.
operational_definition:
  units: m_eff in eV/c², c_s in m/s, π_DM field in energy units.
  symbol_table:
    - name: π_DM
      meaning: The emergent phonon field; its quanta are the dark matter.
      dimensions: M L² T⁻² (Energy)
      default_range: contextual
    - name: m_H
      meaning: Mass of the fundamental Γ quantum forming the condensate.
      dimensions: M
      default_range: ≈ 17 MeV/c²
    - name: m_eff
      meaning: Effective mass of the phonon mode, setting the Jeans scale.
      dimensions: M
      default_range: ≈ 10⁻²² eV/c²
    - name: c_s
      meaning: Sound speed of the Γ superfluid, a function of density.
      dimensions: L T⁻¹
      default_range: contextual (e.g., 10s–100s km/s in halos)
  measurement:
    procedures:
      - name: Halo Core Profile Analysis
        outline: |
          Measure the density profiles of dark matter halos across a range of masses (especially dwarf spheroidals). Fit the profiles to a fluid model governed by the P(X) equation of state. The core size is determined by the balance of gravity and the effective pressure from the sound speed c_s, not a single de Broglie wavelength.
        expected_signals: [Solitonic halo cores with a core radius vs. halo mass relation set by c_s(ρ), Quantized vortex line signatures in massive, relaxed halos]
        pitfalls: [Baryonic feedback effects can mimic core formation, Observational resolution limits for detecting vortex fine-structure]
context_windows:
  - module: MATH-021
    excerpt: |
      Halo cores set by c_s and self‑interaction scale → reproduces Σ_0 locus; distinct vortex/phonon spectra in massive ellipticals. Merger dynamics (COSMO‑Γ‑MERGE): apparent σ/m proxy saturates ≤ O(0.1) cm² g⁻¹ without fundamental self‑scattering. Lab: no ultralight particle production; instead, look for medium‑dependent refractive effects in dense EM fields (afterglow‑like) governed by P(X) parameters.
  - module: MATH-021
    excerpt: |
      Decision Tree (Discriminants) ... D2. Halo substructure: (A) yields phonon‑pressure cores with vortex spectra; (B) yields standard fuzzy‑like suppression with sharp m_L; (C) produces a step‑like cutoff.
poetic_connections:
  motifs: [superfluidity, emergence, collective excitation, cosmic sound]
  evocative_lines:
    - "the light mode governing structure is a *derived* eigenmode/collective excitation"
    - "apparent σ/m proxy saturates"
  association_matrix:
    - [ "GAMMA_SECTOR", 0.9 ]
    - [ "MASS_TENSION", 0.8 ]
    - [ "HALO_CORES", 0.7 ]
formal_mappings:
  candidates:
    - target: Superfluid Dark Matter
      domain: EFT|CM
      mapping_kind: mathematical
      equation_hint: |
        L_eff = P(X), where X = μ − m_H Φ − (∂θ)²/2m_H − …
      justification: |
        The module explicitly models the Γ condensate using a P(X) effective field theory, the standard description for a non-relativistic superfluid. The dark matter degrees of freedom are the phonons (Goldstone modes) of this system. This provides a direct mathematical and conceptual link to the superfluid DM literature.
      references:
        - title: Theory of dark matter superfluidity
          where: Phys. Rev. D 93, 103509
          date: 2016-05-10
      confidence: 0.95
  adopted:
    - target: Superfluid Dark Matter
      rationale: The mapping is definitional within MATH-021, which uses the standard P(X) EFT formalism for superfluids to describe this mechanism.
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "Dark matter halo cores are supported by phonon pressure, with properties determined by the sound speed c_s and the condensate's equation of state."
      domain: phenomenology
      falsifier: "Observation of cored halos whose properties are inconsistent with any plausible P(X) equation of state, or are better explained by a single de Broglie wavelength from a fundamental particle (as in Fuzzy DM)."
      status: proposed
      links: [MATH-021, HALO/MERGE]
    - statement: "The apparent self-interaction cross-section σ/m is an emergent, velocity-dependent effect of collective forces that saturates at ≤ O(0.1) cm²/g."
      domain: phenomenology
      falsifier: "Observation of dark matter interactions in cluster mergers (e.g., halo offsets) that unambiguously require a fundamental, constant σ/m > 0.1 cm²/g."
      status: proposed
      links: [MATH-021, COSMO-Γ-MERGE]
    - statement: "No fundamental ultralight particle (~10⁻²² eV) corresponding to dark matter exists."
      domain: experiment
      falsifier: "Direct detection of a ~10⁻²² eV particle in a haloscope or other axion-like particle search experiment."
      status: proposed
      links: [MATH-021]
naming_notes:
  collisions: [The symbol π is standard for pions in the Standard Model. Here it is specified as π_DM to denote the phonon dark matter field.]
  disambiguation: |
    Phonon DM posits dark matter is a *collective mode* of a condensate made of *heavy* (≈17 MeV) particles. This contrasts with Fuzzy DM (Mechanism B), which posits dark matter is a *fundamental* ultralight (≈10⁻²² eV) particle. The "lightness" of Phonon DM is an emergent, low-energy property, not a fundamental one.
crosslinks:
  near_synonyms: [SUPERFLUID_DM]
  antonyms: [CLOCKWORK_DM, PARTICLE_DM]
  prerequisites: [GAMMA_SECTOR, MASS_TENSION]
  downstream_effects: [HALO_CORES]
license: CC-BY-SA-4.0
---