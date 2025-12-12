---
term: "Effective Spatial Dimension"
canonical_id: "EFFECTIVE_SPATIAL_DIMENSION"
symbol: "D_eff"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-022"]
---

---
term: Effective Spatial Dimension
canonical_id: EFFECTIVE_SPATIAL_DIMENSION
symbol: D_eff
aliases: [active dimension]
parents: [MATH-022]
children: [SECT‑Γ‑A‑CMB, SECT‑Γ‑A‑HALO]
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-022
      lines: "Executive result"
      snippet: |
        β = D_eff / z
        where D_eff is the effective (possibly fractal) spatial dimension of the active coherence network (wound channels) and z is the dynamical exponent of the superfluid sector.
  editors: [system]
  review_log: []
triad:
  art: |
    The dimension not of the space we see, but of the energetic filaments and sheets woven through it—the active skeleton along which coherence flows.
  law: |
    The Pressuron exponent β is fixed by the ratio β = D_eff / z, where z is the dynamical exponent. For z=2 superfluids, D_eff must manifest as one of the integer plateaus {0, 1, 2}, yielding β ∈ {0, 1/2, 1}.
  philosophy: |
    D_eff replaces the bulk dimension `d` to reflect that action is sourced only on the active coherence network, not uniformly in space. This elevates topology above bulk geometry, fixing the equation of state from first principles and eliminating β as a free parameter.
pirouette_definition: |
  The effective spatial dimension, `D_eff`, is the Hausdorff or spectral dimension of the active coherence network that sources the Pressuron field `X`. It replaces the bulk spatial dimension `d` in the scaling law for the Pressuron action, fixing the exponent `β = D_eff / z`. Discrete scale invariance of the network restricts `D_eff` to stable integer plateaus {0, 1, 2}, corresponding to point-like, filamentary, and sheet-like coherence structures, respectively.
operational_definition:
  units: dimensionless
  symbol_table:
    - name: D_eff
      meaning: Effective Spatial Dimension
      dimensions: dimensionless
      default_range: "{0, 1, 2}"
    - name: z
      meaning: Dynamical Exponent
      dimensions: dimensionless
      default_range: "{2} (non-relativistic)"
    - name: β
      meaning: Pressuron Exponent
      dimensions: dimensionless
      default_range: "{0, 1/2, 1} (for z=2)"
  measurement:
    procedures:
      - name: Inferential via β and Log-Periodic Signatures
        outline: |
          `D_eff` is not measured directly. It is inferred by first measuring the Pressuron exponent `β` from astrophysical observables (e.g., halo scaling relations, rotation curve shapes). Given a known dynamical exponent `z` (typically `z=2` for nonrelativistic superfluids), `D_eff` is calculated as `D_eff = β * z`. The model is validated by confirming the inferred `D_eff` lies on an integer plateau and by detecting predicted log-periodic oscillations in data residuals.
        expected_signals: [Inferred `β` values clustering near rational fractions {0, 1/2, 1}, Low-amplitude log-periodic oscillations in Σ₀ vs. M]
        pitfalls: [Mistaking observational scatter for log-periodic signals, Incorrectly assuming the dynamical exponent `z`]
context_windows:
  - module: MATH-022
    excerpt: |
      Replacing the bulk dimension d with the **active** dimension D_eff (the measure of the coherence network actually sourcing X) gives β = D_eff / z.
      • z encodes dynamics (e.g., z=2 for superfluid hydrodynamics).
      • D_eff encodes geometry/topology (sheet‑like D_eff≈2; filamentary D_eff≈1; point‑like cores D_eff≈0).
      • Discrete self‑similarity of the network yields **plateaus** in D_eff and hence **rational β**.
  - module: MATH-022
    excerpt: |
      Predictions (no free β)
      R1 β is **fixed a priori** by (D_eff, z). With z=2:
      • Sheet‑dominated regime (D_eff=2): β=1 → P∝X^2 (stiffest of allowed set).
      • Filament regime (D_eff=1): β=1/2 → P∝X^{3/2} (baseline used in many superfluid cores).
      • Core/point regime (D_eff=0): β=0 → P∝X (dust‑like limit).
poetic_connections:
  motifs: [fractal skeleton, coherence channels, dimensional plateaus, wound channels]
  evocative_lines:
    - "the measure of the coherence network actually sourcing X"
    - "a D_eff‑dimensional subset of space (sheets/filaments/points)"
  association_matrix:
    - [ "PRESSURON_EXPONENT_BETA", 0.9 ]
    - [ "DYNAMICAL_EXPONENT_Z", 0.8 ]
    - [ "COHERENCE_NETWORK", 0.9 ]
formal_mappings:
  candidates:
    - target: Hausdorff dimension
      domain: Math
      mapping_kind: mathematical
      equation_hint: null
      justification: |
        `D_eff` is explicitly described as a "(possibly fractal) dimension" of a network, a subset of the embedding space. This is the core concept of the Hausdorff dimension, which generalizes the notion of dimension to arbitrary sets like fractals.
      references:
        - title: Fractal Geometry: Mathematical Foundations and Applications
          where: K. Falconer
          date: 2014-01-01
      confidence: 0.8
    - target: Spectral dimension
      domain: Math/Physics
      mapping_kind: conceptual
      equation_hint: null
      justification: |
        The spectral dimension measures the dimensionality of a space as "seen" by a random walker, reflecting connectivity and topology. This aligns with the concept of `D_eff` characterizing the geometry of energy/mass flow along the coherence network.
      references:
        - title: Spectral dimension of the universe in quantum gravity at a turning point
          where: arXiv:0902.1948
          date: 2009-02-11
      confidence: 0.6
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "`D_eff` manifests in stable, near-integer plateaus {0, 1, 2} across astrophysical scales."
      domain: phenomenology
      falsifier: "Astrophysical measurements consistently require a `β` value that implies a non-integer `D_eff` (e.g., `D_eff = 1.6` for `z=2`) with no evidence of transitioning between plateaus."
      status: proposed
      links: [MATH-022, SECT‑Γ‑A‑HALO]
    - statement: "Transitions between `D_eff` plateaus are marked by log-periodic oscillations in observables like halo surface density."
      domain: phenomenology
      falsifier: "A transition (e.g., from β=1/2 to β=1) is observed in halo populations, but the residuals of scaling relations are smooth noise, lacking any periodic modulation in log-mass."
      status: proposed
      links: [MATH-022]
naming_notes:
  collisions: [d (bulk spatial dimension)]
  disambiguation: |
    `D_eff` is the dimension of the active sub-manifold where coherence channels reside, not the dimension `d` of the embedding background spacetime (typically `d=3`). The Pressuron action is sourced by the former, not the latter.
crosslinks:
  near_synonyms: [ACTIVE_DIMENSION]
  antonyms: [BULK_DIMENSION]
  prerequisites: [PRESSURON_EXPONENT_BETA, DYNAMICAL_EXPONENT_Z, COHERENCE_NETWORK]
  downstream_effects: [PRESSURON_EOS, HALO_CORE_SCALING]
license: CC-BY-SA-4.0