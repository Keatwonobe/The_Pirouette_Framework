---
term: "Heavy quanta"
canonical_id: "HEAVY_QUANTA"
symbol: "m_H"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["COSMO-005"]
---

---
term: Heavy quanta
canonical_id: HEAVY_QUANTA
symbol: m_H
aliases: []
parents: [COSMO-005]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: COSMO-005
      lines: "SECT‑Γ‑A‑CMB, Effective Fluid Mapping, L1"
      snippet: |
        Microscopic: heavy quanta m_H≈17 MeV; macroscopic: superfluid with EOS from P(X)=αX^{1+β}+δX^2+…
  editors: [AetherScribe-9]
  review_log: []
triad:
  art: |
    A silent, heavy sea whose collective sigh—the phonon—sculpts the cosmic web. On the largest scales, it is an ocean of calm; up close, its quantum depths stir, smoothing the sharp edges of galaxies.
  law: |
    The mass of the heavy quantum, `m_H`, sets the scale-dependent sound speed `c_{s,eff}²(k,a)` via the coherence length `ξ(a)=(2 m_H c_s(a))^{−1}`, directly dictating the onset of small-scale power suppression in the matter power spectrum.
  philosophy: |
    To posit a heavy quantum is to declare that dark matter's apparent simplicity on cosmic scales is an emergent phenomenon masking a rich, microscopic quantum reality. Its mass is the fundamental parameter linking the quantum world (coherence length) to astrophysical observables (halo cores).
pirouette_definition: |
  The fundamental, massive particle (`m_H ≈ 17 MeV/c²`) that constitutes the Pirouette superfluid condensate. These quanta are non-relativistic at late times, and their collective quantum state is described macroscopically by an effective fluid with a non-trivial equation of state `P(X)`. The mass `m_H` directly sets the superfluid's coherence length `ξ`, which in turn governs the scale `k_ξ` at which the effective sound speed deviates from the background value, leading to suppression of small-scale structure.
operational_definition:
  units: MeV/c²
  symbol_table:
    - name: m_H
      meaning: Mass of the heavy quantum
      dimensions: M
      default_range: ≈ 17 MeV/c²
  measurement:
    procedures:
      - name: Small-scale structure suppression
        outline: |
          Infer `m_H` by fitting the matter power spectrum from galaxy surveys (e.g., DESI, Euclid) and Lyman-alpha forest data to the Pirouette model. The suppression scale `k_ξ` is inversely proportional to `m_H`, so the turnover position in the power spectrum directly constrains the mass.
        expected_signals: [A sharp suppression in the matter power spectrum for wavenumbers `k > k_ξ(a)`, Correlated flattening of dark matter halo density profiles (cores) relative to ΛCDM]
        pitfalls: [Degeneracies with other cosmological parameters (e.g., neutrino mass, warm dark matter models), Baryonic feedback effects mimicking suppression on similar scales]
context_windows:
  - module: COSMO-005
    excerpt: |
      Microscopic: heavy quanta m_H≈17 MeV; macroscopic: superfluid with EOS from P(X)=αX^{1+β}+δX^2+… Define background number density n(a) from continuity (ȷ^0 conservation) and chemical relation μ(n).
  - module: COSMO-005
    excerpt: |
      Scale‑dependent effective sound speed used in Boltzmann evolution:
      c_{s,eff}²(k,a) = c_s²(a) / [1 + (k/k_ξ(a))²], with k_ξ(a)≡1/ξ(a), ξ(a)=(2 m_H c_s(a))^{−1}.
  - module: COSMO-005
    excerpt: |
      Use fluid mapping when m_H/H>50 and k/a<κ_switch m_H (default κ_switch=0.5). Fall back to full field if either condition fails.
poetic_connections:
  motifs: [condensate, quantum fluid, microscopic origin, coherence]
  evocative_lines:
    - "Microscopic: heavy quanta... macroscopic: superfluid"
    - "...reproduces CDM on CMB scales while generating small‑scale suppression and halo cores."
  association_matrix:
    - [ "sound_speed_cs", 0.9 ]
    - [ "coherence_length_xi", 0.9 ]
    - [ "pressuron", 0.7 ]
formal_mappings:
  candidates:
    - target: Axion-like particle (ALP) mass
      domain: EFT
      mapping_kind: conceptual
      equation_hint: ~
      justification: |
        `m_H` is the mass of a hypothetical boson that forms a cold, non-relativistic condensate, behaving as dark matter. This is conceptually identical to models of axion or ALP dark matter, though the specific potential (`P(X)`) differs. The mass range (~MeV) is distinct from typical QCD axions (~µeV-meV) but falls within the broader ALP parameter space.
      references: []
      confidence: 0.7
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The heavy quantum has a mass of approximately 17 MeV/c²."
      domain: phenomenology
      falsifier: "The scale of small-scale structure suppression measured by galaxy surveys and Lyman-alpha forest data implies a coherence length inconsistent with an `m_H` of 17 MeV/c², or no suppression is found where predicted by the model."
      status: proposed
      links: [COSMO-005]
naming_notes:
  collisions: [m_h (Higgs boson mass), M_H (Hubble mass), M_h (halo mass)]
  disambiguation: |
    `m_H` refers to the mass of the heavy quantum, not the Higgs boson (`m_h`) or a halo/Hubble mass. The context is always cosmological and related to the superfluid's microscopic properties.
crosslinks:
  near_synonyms: []
  antonyms: [phonon]
  prerequisites: [superfluid_condensate, pressuron]
  downstream_effects: [coherence_length_xi, effective_sound_speed_cs_eff]
license: CC-BY-SA-4.0
---