---
term: "Centroid Offset"
canonical_id: "CENTROID_OFFSET"
symbol: "Δx"
aliases: [κ–X-ray offset]
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["COSMO-002"]
---

---
term: Centroid Offset
canonical_id: CENTROID_OFFSET
symbol: Δx
aliases: [κ–X-ray offset]
parents: [COSMO-Γ-MERGE, COSMO-Γ-HALO]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: COSMO-Γ-MERGE
      snippet: |
        The peak offset Δx ≡ |x_κ − x_X| follows a universal scaling law Δx ≃ 𝔽(M_1,M_2,b,v_in,z; V(Γ)) determined by the Γ halo structure, not by an elastic DM cross-section.
  editors: [Pirouette-Agent]
  review_log: []
triad:
  art: |
    A silent ghost of gravity passes through a storm of its own making. Its true position is betrayed by the lingering, shocked tempest of baryonic gas left in its wake.
  law: |
    The peak offset Δx between the total mass centroid (traced by lensing κ) and the baryonic gas centroid (traced by X-ray emission S_X) is a deterministic, predictable function of the initial merger parameters (M₁, M₂, b, v_in, z) and the frozen Γ-potential V(Γ), with no tunable particle cross-section.
  philosophy: |
    The Centroid Offset is the primary observable for differentiating collisionless and collisional components of the universe on large scales. Within Pirouette, it serves as a critical test of the non-particulate, field-like nature of Γ-condensates, transforming a constraint on a particle property (σ/m) into a sharp prediction of the underlying field dynamics.
pirouette_definition: |
  The Centroid Offset, Δx, is the time-dependent physical separation vector between the centroid of the total mass surface density (Σ), traced by gravitational lensing (κ), and the centroid of the hot, X-ray emitting intracluster medium (ICM), traced by X-ray surface brightness (S_X). In the context of galaxy cluster mergers, Δx arises because the collisionless Γ-condensate halos pass through each other while the baryonic gas components collide, shock, and lag behind. Its magnitude and evolution are direct consequences of the Γ-field equations and the Euler equations for the gas, governed by the frozen potential V(Γ).
operational_definition:
  units: kiloparsecs (kpc)
  symbol_table:
    - name: Δx
      meaning: Centroid Offset vector magnitude, |x_κ - x_X|.
      dimensions: L
      default_range: 0–500 kpc
    - name: x_κ
      meaning: Position vector of the peak of the lensing convergence map.
      dimensions: L
      default_range: contextual
    - name: x_X
      meaning: Position vector of the peak of the X-ray surface brightness map.
      dimensions: L
      default_range: contextual
  measurement:
    procedures:
      - name: Lensing-X-ray Overlay
        outline: |
          1. Obtain deep, wide-field optical/IR imaging of a merging galaxy cluster to construct a gravitational lensing convergence map (κ), which traces the projected total mass.
          2. Obtain deep X-ray observations (e.g., Chandra, XMM-Newton) of the same system to create a surface brightness map (S_X) of the hot intracluster gas.
          3. Register both maps to a common astrometric coordinate system.
          4. Identify the coordinates of the primary peak(s) in both the κ map and the S_X map.
          5. Calculate the angular separation on the sky between the corresponding peaks.
          6. Convert the angular separation to a physical distance (Δx) using the angular diameter distance to the cluster's redshift.
        expected_signals: [A significant spatial offset between a smooth, regular κ peak and a shocked, often cometary-shaped S_X peak., A bow shock in the X-ray map ahead of the gas peak, aligned with the direction of motion relative to the κ peak.]
        pitfalls: [Projection effects can mask a true 3D offset if the merger axis is close to the line of sight., Misidentification of peaks due to noise, substructure, or astrophysical foreground/background sources., Uncertainty in the mass-to-light ratio for peak identification in noisy lensing maps.]
context_windows:
  - module: COSMO-Γ-MERGE
    excerpt: |
      Γ condensates behave as effectively collisionless mass components across cluster-scale encounters; gas shocks and lags. The peak offset Δx ≡ |x_κ − x_X| follows a universal scaling law ... determined by the Γ halo structure, not by an elastic DM cross-section.
  - module: COSMO-Γ-MERGE
    excerpt: |
      An apparent “σ/m” constraint inferred in CDM language maps in Pirouette to a **derived** (non-tunable) effective collisional proxy σ_eff/m determined by Γ soliton overlap; prediction: σ_eff/m ≲ 0.2 cm² g⁻¹ for Bullet-like events when V(Γ) is COSMO-Γ-000-frozen.
poetic_connections:
  motifs: [gravitational slipstream, baryonic lag, ghost and storm, collisionless passage]
  evocative_lines:
    - "Γ condensates behave as effectively collisionless mass components... gas shocks and lags."
    - "The survival of κ peaks after core passage are fixed by the same parameters that set galactic cores."
  association_matrix:
    - [ "GAMMA_CONDENSATE", 0.9 ]
    - [ "GAMMA_HALO", 0.8 ]
    - [ "FROZEN_POTENTIAL_V_GAMMA", 0.7 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Dark Matter–Baryon Separation
      domain: CM
      mapping_kind: operational
      justification: |
        The Centroid Offset is the direct observational analogue of the separation between the dark matter component (traced by lensing) and the baryonic gas (traced by X-rays) in merging galaxy clusters. In standard cosmology, this observable is a key tool for constraining the self-interaction cross-section of dark matter (σ/m). Pirouette recasts this measurement as a direct prediction of Γ-field dynamics.
      references:
        - title: "A Direct Empirical Proof of the Existence of Dark Matter"
          where: "Astrophys.J. 648 (2006) L109–L113"
          date: 2006-09-20
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The maximum offset Δx_max in a merger scales as a power law with initial velocity, mass, and redshift: Δx_max ≈ A(v_in)^α (M)^β (1+z)^γ, where A, α, β, γ are fixed by the frozen potential V(Γ)."
      domain: phenomenology
      falsifier: "A statistical sample of observed cluster mergers shows a scaling relation for Δx inconsistent with the prediction from the frozen V(Γ), or exhibits scatter that can only be explained by a stochastic, particle-like cross-section."
      status: proposed
      links: [COSMO-Γ-MERGE]
    - statement: "For any merger, the Centroid Offset can be explained with an effective self-interaction cross-section σ_eff/m that is derived from V(Γ) and does not exceed a model-predicted maximum (e.g., ≲ 0.2 cm²/g for Bullet-like systems)."
      domain: theory
      falsifier: "A robustly measured Centroid Offset in a merging system requires an equivalent σ/m significantly larger than the maximum value permitted by the frozen V(Γ) to be explained."
      status: proposed
      links: [COSMO-Γ-MERGE]
naming_notes:
  collisions: [Δx is a common symbol for a position difference in many fields of physics; context is critical.]
  disambiguation: |
    This term specifically refers to the bulk offset between the total mass and the hot intracluster gas on ~100 kpc scales in cluster mergers. It should be distinguished from other astrophysical offsets, such as the separation between a central galaxy and its host dark matter halo (e.g., from splashback), or stellar-gas offsets within individual galaxies.
crosslinks:
  near_synonyms: []
  antonyms: [HYDROSTATIC_EQUILIBRIUM]
  prerequisites: [GAMMA_CONDENSATE, GAMMA_HALO]
  downstream_effects: [FROZEN_POTENTIAL_V_GAMMA]
license: CC-BY-SA-4.0
---

# Centroid Offset

## Canonical (Pirouette)
The Centroid Offset, Δx, is the time-dependent physical separation vector between the centroid of the total mass surface density (Σ), traced by gravitational lensing (κ), and the centroid of the hot, X-ray emitting intracluster medium (ICM), traced by X-ray surface brightness (S_X). In the context of galaxy cluster mergers, Δx arises because the collisionless Γ-condensate halos pass through each other while the baryonic gas components collide, shock, and lag behind. Its magnitude and evolution are direct consequences of the Γ-field equations and the Euler equations for the gas, governed by the frozen potential V(Γ).

## EFT-First Summary
The Centroid Offset is the Pirouette Framework's operational analogue for the observed separation between dark matter and baryonic gas in merging galaxy clusters, exemplified by the Bullet Cluster. This separation, measured via gravitational lensing and X-ray imaging, is used in standard cosmology to place upper limits on the self-interaction cross-section of dark matter (σ/m). In Pirouette, this offset is not determined by a tunable particle cross-section but is a predictable, deterministic outcome of the field dynamics of the Γ-condensate. This provides a sharp, falsifiable test of the underlying frozen potential V(Γ) that governs the Γ-field's behavior.

## Glossary Links
- See also: `GAMMA_CONDENSATE`, `GAMMA_HALO`