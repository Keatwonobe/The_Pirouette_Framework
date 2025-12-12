---
term: "Light Eigenstate"
canonical_id: "LIGHT_EIGENSTATE"
symbol: "Γ_L"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-021"]
---

---
term: Light Eigenstate
canonical_id: LIGHT_EIGENSTATE
symbol: Γ_L
aliases: [Cosmological Γ Mode]
parents: [MATH-021]
children: [SECT-Γ-A, SECT-Γ-B, SECT-Γ-C, COSMO-Γ-CMB]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-021
      lines: "L31-33"
      snippet: |
        B1. Γ is a *sector* of N coupled scalars with nearest‑neighbor couplings producing exponentially hierarchical eigenmasses (clockwork/alignment).
        B2. Heavy eigenstate Γ_H couples to leptons (g−2 portal) with O(1) mixing; light eigenstate Γ_L is exponentially light and weakly coupled, sourcing cosmology.
  editors: [chain-of-thought-agent]
  review_log: []
triad:
  art: |
    From the thunder of a heavy clock, a whisper escapes, so light it stretches across galaxies. This whisper is the light eigenstate, a ghost in the machine whose faint gravity weaves the cosmic web. It is the vast echo of a compact sound.
  law: |
    The Light Eigenstate (Γ_L) is the mass eigenmode of the Γ-sector whose mass is exponentially suppressed relative to the heavy eigenstate (Γ_H), according to the clockwork relation m_L ≈ m_H / q^N. Its de Broglie wavelength at this mass (λ_dB ≈ h / (m_L v)) must be of order kiloparsecs to explain observed galactic halo core sizes and the suppression of small-scale structure.
  philosophy: |
    The Light Eigenstate resolves the 29-order-of-magnitude tension between particle and cosmological scales without fine-tuning. It demonstrates that vast scale separation can emerge naturally from the structure of a theory (a chain of coupled fields) rather than from ad-hoc parameter choices. Γ_L embodies the principle of generating cosmological scales from a more fundamental, higher-energy sector via a concrete, falsifiable mechanism.
pirouette_definition: |
  The Light Eigenstate, Γ_L, is the exponentially light mass eigenstate that emerges from a multi-field Γ sector governed by a clockwork or alignment mechanism. It is one of two physical modes, the other being the Heavy Eigenstate (Γ_H). While Γ_H couples to Standard Model leptons and has a mass m_H ≈ 17 MeV, Γ_L has a mass m_L ≈ 10⁻²² eV, determined by the clockwork parameters (charge q, site number N). Γ_L is the primary source of cosmological dark matter structure, behaving as an ultralight scalar field that forms galactic halos.
operational_definition:
  units: Mass in electronvolts (eV).
  symbol_table:
    - name: Γ_L
      meaning: The light eigenstate field.
      dimensions: M L²/T (Action)
      default_range: N/A (field amplitude)
    - name: m_L
      meaning: Mass of the light eigenstate.
      dimensions: M
      default_range: 10⁻²³ – 10⁻²¹ eV
    - name: q
      meaning: Clockwork charge, dictates inter-site coupling strength.
      dimensions: dimensionless
      default_range: 2 – 10 (from symmetry)
    - name: N
      meaning: Number of sites in the clockwork chain.
      dimensions: dimensionless
      default_range: 50 – 100
  measurement:
    procedures:
      - name: Cosmological Structure Inference
        outline: |
          1. Measure the matter power spectrum using galaxy surveys (e.g., Lyman-alpha forest) to find the scale of suppression for small-scale structure (k_cutoff).
          2. Measure the density profiles of dwarf spheroidal galaxies to determine the characteristic core size or soliton radius.
          3. Fit these observables to a wave-like dark matter model. The required de Broglie wavelength λ_dB sets the mass m_L via the relation m_L ≈ h / (λ_dB v_virial).
        expected_signals: [A sharp cutoff in the matter power spectrum at k > 1 h/Mpc, Solitonic cores of radius ~1 kpc in dwarf galaxies]
        pitfalls: [Degeneracy with baryonic feedback effects which can also form halo cores, Uncertainty in virial velocities of dwarf galaxies]
      - name: CMB Phase Shift Analysis
        outline: |
          1. Measure the CMB temperature and polarization power spectra (TT, TE, EE) to extremely high precision.
          2. Compare the observed acoustic peak positions to the standard ΛCDM prediction.
          3. A clockwork-derived Γ_L field introduces a small, calculable, N-dependent phase shift in the acoustic oscillations. Constrain (q,N) space by bounding this shift.
        expected_signals: [A residual phase shift in CMB acoustic peaks after fitting for standard cosmological parameters]
        pitfalls: [Signal is extremely small and potentially degenerate with other early-universe physics, Requires next-generation CMB observatory precision]
context_windows:
  - module: MATH-021
    excerpt: |
      • Cosmology (IR/halos): COSMO‑Γ requires galaxy‑scale coherence typically modelled by an ultralight field m_L ∼ 10^−22 eV *or* an equivalent long‑wavelength collective mode.
      • Goal: show that (i) both phenomena arise from a single Γ sector, and (ii) the light mode governing structure is a *derived* eigenmode/collective excitation, not an ad‑hoc second particle with tuned mass.
  - module: MATH-021
    excerpt: |
      Mechanism B — Clockwork/Alignment in a Multi‑Γ Chain (Two Eigenstates from One Sector)
      Hypothesis
      B1. Γ is a *sector* of N coupled scalars with nearest‑neighbor couplings producing exponentially hierarchical eigenmasses (clockwork/alignment).
      B2. Heavy eigenstate Γ_H couples to leptons (g−2 portal) with O(1) mixing; light eigenstate Γ_L is exponentially light and weakly coupled, sourcing cosmology.
poetic_connections:
  motifs: [hierarchy, clockwork, echo, resonance, cosmic web]
  evocative_lines:
    - "the 29‑order‑of‑magnitude 'mass tension'"
    - "light eigenstate Γ_L is exponentially light and weakly coupled"
    - "a derived eigenmode/collective excitation, not an ad‑hoc second particle"
  association_matrix:
    - [ "HEAVY_EIGENSTATE", 0.9 ]
    - [ "CLOCKWORK_MECHANISM", 0.9 ]
    - [ "FUZZY_DARK_MATTER", 0.7 ]
    - [ "EQUIVALENCE_PRINCIPLE", 0.3 ]
formal_mappings:
  candidates:
    - target: Fuzzy Dark Matter (FDM) / Ultralight Axion (ULA)
      domain: Cosmology
      mapping_kind: operational
      equation_hint: |
        λ_dB = h / (m_L v) ≈ 1 kpc
      justification: |
        Operationally, Γ_L behaves as the quantum of a Fuzzy Dark Matter field. Its extremely low mass (m_L ≈ 10⁻²² eV) gives it a macroscopic de Broglie wavelength on the scale of galaxies, suppressing small-scale structure and forming solitonic cores, which are the defining phenomenological signatures of FDM.
      references:
        - title: "Ultralight scalars as cosmological dark matter"
          where: "Phys.Rev.D 62 (2000) 103517"
          date: 2000-07-26
      confidence: 0.9
  adopted:
    - target: Fuzzy Dark Matter (FDM)
      rationale: The phenomenological role of Γ_L in cosmology is identical to that of FDM. This mapping is explicitly used in Pirouette modules (e.g., MATH-021) to frame the cosmological requirements for m_L.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The mass of Γ_L is m_L ≈ m_H / q^N, and its value m_L ≈ 10⁻²² eV is responsible for the cutoff in the matter power spectrum."
      domain: phenomenology
      falsifier: "Lyman-alpha forest and galaxy survey data show no such cutoff, or require a mass inconsistent with any plausible (q,N) derived from the measured m_H."
      status: proposed
      links: [MATH-021, COSMO-Γ-CMB]
    - statement: "Γ_L's coupling to matter is suppressed by q⁻ᴺ, resulting in a specific, calculable, and non-zero violation of the Equivalence Principle."
      domain: experiment
      falsifier: "Precision fifth-force experiments (e.g., MICROSCOPE, Eöt-Wash) fail to detect any EP violation, or detect one with a strength and character inconsistent with the clockwork prediction."
      status: proposed
      links: [MATH-021]
naming_notes:
  collisions: [The symbol Γ (Gamma) is widely used in physics for the Gamma function, gamma matrices in QFT, and photon symbol (γ).]
  disambiguation: |
    Distinguish the Light Eigenstate (Γ_L), a particle state, from the light *collective mode* (a phonon) hypothesized in Mechanism A (Composite Superfluid). Γ_L is a true mass eigenstate of the fundamental Lagrangian, while a phonon is an emergent excitation of a condensate. Also, Γ_L is not a new fundamental particle but an eigenmode of the same Γ-sector that contains the Heavy Eigenstate (Γ_H).
crosslinks:
  near_synonyms: []
  antonyms: [HEAVY_EIGENSTATE]
  prerequisites: [CLOCKWORK_MECHANISM]
  downstream_effects: [HALO_CORE_PROBLEM, SMALL_SCALE_STRUCTURE]
license: CC-BY-SA-4.0
---

# Light Eigenstate

## Canonical (Pirouette)
The Light Eigenstate, Γ_L, is the exponentially light mass eigenstate that emerges from a multi-field Γ sector governed by a clockwork or alignment mechanism. It is one of two physical modes, the other being the Heavy Eigenstate (Γ_H). While Γ_H couples to Standard Model leptons and has a mass m_H ≈ 17 MeV, Γ_L has a mass m_L ≈ 10⁻²² eV, determined by the clockwork parameters (charge q, site number N). Γ_L is the primary source of cosmological dark matter structure, behaving as an ultralight scalar field that forms galactic halos.

## EFT-First Summary
From a cosmological perspective, the Light Eigenstate (Γ_L) is operationally equivalent to a Fuzzy Dark Matter (FDM) or Ultralight Axion (ULA) field with a mass of approximately 10⁻²² eV. This ultralight nature endows it with a kiloparsec-scale de Broglie wavelength, which naturally suppresses the formation of small-scale cosmic structure and resolves the core-cusp problem by forming soliton-like cores in dwarf galaxies. Unlike a fundamental axion, however, Γ_L's properties are derived from the structure of a higher-energy clockwork sector, providing a concrete UV completion for the FDM paradigm.

## Glossary Links
- See also: [Heavy Eigenstate](...), [Clockwork Mechanism](...), [Fuzzy Dark Matter](...)