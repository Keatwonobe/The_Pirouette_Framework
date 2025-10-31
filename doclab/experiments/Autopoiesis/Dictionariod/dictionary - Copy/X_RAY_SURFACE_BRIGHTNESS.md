---
term: "X-ray Surface Brightness"
canonical_id: "X_RAY_SURFACE_BRIGHTNESS"
symbol: "S_X"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["COSMO-002"]
---

---
term: X-ray Surface Brightness
canonical_id: X_RAY_SURFACE_BRIGHTNESS
symbol: S_X
aliases: []
parents: [COSMO-002]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: COSMO-002
      snippet: |
        • X‑ray surface brightness S_X∝∫ n_e² Λ(T) dl (adiabatic: proxy via ρ_g^2 √T).
  editors: [chain-of-thought-agent]
  review_log: []
triad:
  art: |
    The luminous echo of a cosmic collision, a ghostly veil of superheated gas tracing where matter has been, while the unseen bulk moves on. It is the glowing scar left by the passage of invisible mass.
  law: |
    The X-ray Surface Brightness S_X is the line-of-sight integral of the product of the electron number density squared (n_e²) and the temperature-dependent cooling function (Λ(T)), tracing the emission from hot intracluster plasma.
  philosophy: |
    S_X provides the crucial, observable foil to the collisionless Γ-condensate. Its lag behind the lensing-inferred mass peak (κ) during mergers is a direct consequence of gas hydrodynamics, offering a clean test of the Γ-condensate's non-particulate, non-interacting nature without invoking a tunable DM cross-section.
pirouette_definition: |
  A two-dimensional observable map representing the line-of-sight integral of X-ray emissivity from the hot, ionized intracluster medium (ICM). In the Pirouette framework, S_X is the primary tracer of the collisional baryonic gas component in galaxy cluster mergers. Its centroid's displacement from the lensing convergence (κ) peak is a key observable predicted by COSMO-Γ-MERGE to constrain the collisionless dynamics of Γ-condensates.
operational_definition:
  units: erg s⁻¹ cm⁻² sr⁻¹
  symbol_table:
    - name: S_X
      meaning: X-ray Surface Brightness
      dimensions: M T⁻³
      default_range: contextual
    - name: n_e
      meaning: Electron number density
      dimensions: L⁻³
      default_range: contextual
    - name: Λ(T)
      meaning: Temperature-dependent cooling function
      dimensions: L³ T⁻¹
      default_range: contextual
    - name: dl
      meaning: Path length element along line of sight
      dimensions: L
      default_range: contextual
    - name: ρ_g
      meaning: Gas mass density (used in simulation proxy)
      dimensions: M L⁻³
      default_range: contextual
  measurement:
    procedures:
      - name: Observational X-ray Mapping
        outline: |
          Observe a galaxy cluster with an X-ray telescope (e.g., Chandra, XMM-Newton) for a sufficient exposure time. Process raw photon count data, correcting for instrument response, background, and vignetting. Bin the corrected counts into a 2D spatial map, converting counts to flux units to produce S_X(x,y).
        expected_signals: [Diffuse emission peaking on the gas core, Bow shock morphology in mergers]
        pitfalls: [Point source contamination (AGN), Uncertain background subtraction, Projection effects]
      - name: Simulation Proxy Calculation
        outline: |
          From a COSMO-Γ-MERGE simulation snapshot, integrate the proxy quantity ρ_g²√T along the line-of-sight (dl) for each pixel (x,y) on a projected plane. This yields a map directly proportional to S_X under the assumption of adiabatic, bremsstrahlung-dominated cooling.
        expected_signals: [2D map tracking the densest, hottest gas regions]
        pitfalls: [Proxy breaks down in regimes with significant line or non-thermal cooling/heating]
context_windows:
  - module: COSMO-002
    excerpt: |
      Observables:
      • Lensing κ(x,y) from Σ(x,y)=∫(ρ_Γ+ρ_g+ρ_*) dl.
      • X‑ray surface brightness S_X∝∫ n_e² Λ(T) dl (adiabatic: proxy via ρ_g^2 √T).
      • Centroid offset Δx(t) between κ peak(s) and S_X peak(s).
  - module: COSMO-002
    excerpt: |
      "kappa_map": "path/to/κ.fits",
      "xray_map": "path/to/SX.fits",
      "sz_map": "path/to/y.fits",
      "commit": "<git>",
      "freeze_manifest": "path/to/manifest.yaml"
poetic_connections:
  motifs: [collision, lag, shockwave, afterglow, baryonic tracer]
  evocative_lines:
    - "gas shocks and lags"
    - "The peak offset Δx ≡ |x_κ − x_X|"
  association_matrix:
    - [ "KAPPA", 0.9 ]
    - [ "CENTROID_OFFSET", 0.8 ]
    - [ "GAMMA_CONDENSATE", 0.5 ]
formal_mappings:
  candidates:
    - target: X-ray surface brightness
      domain: Astrophysics
      mapping_kind: operational
      equation_hint: |
        S_X = (1/4π) ∫ ε_X dl , where ε_X ≈ n_e n_H Λ(T) is the X-ray emissivity.
      justification: |
        This term is the standard observable used in astrophysics to map the hot Intracluster Medium (ICM) via its thermal bremsstrahlung and line emission. The Pirouette definition and operational calculation directly correspond to the standard astronomical quantity measured by space-based X-ray observatories.
      references:
        - title: X-ray Emission from Clusters of Galaxies
          where: Sarazin, C. L. (Cambridge University Press, 1988)
          date: 1988-01-01
      confidence: 1.0
  adopted:
    - target: X-ray surface brightness (Astrophysics)
      rationale: The term is adopted directly from observational astrophysics, as it serves as the primary observational tracer for the collisional gas component which Pirouette models.
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "The morphology and centroid of S_X in merging clusters, when compared to the lensing convergence κ, will produce an offset Δx that scales with merger parameters as predicted by COSMO-Γ-MERGE."
      domain: phenomenology
      falsifier: "Observed cluster mergers show a κ–S_X offset that is inconsistent with the universal scaling law predicted from the frozen V(Γ) potential, or requires an effective self-interaction cross-section outside the bounds predicted by Γ-soliton overlap (σ_eff/m ≲ 0.2 cm² g⁻¹)."
      status: proposed
      links: [COSMO-002]
naming_notes:
  collisions: [S can refer to entropy in other contexts; S_X is unambiguous.]
  disambiguation: |
    Distinguish from the Sunyaev-Zel'dovich (SZ) effect, which also traces the ICM but with a different dependence on gas properties (∫ P_e dl for the thermal y-parameter), making it sensitive to different gas physics. S_X is proportional to density squared, while the SZ effect is linear in density.
crosslinks:
  near_synonyms: []
  antonyms: [LENSING_CONVERGENCE]
  prerequisites: [GAMMA_CONDENSATE, GAS_DENSITY]
  downstream_effects: [CENTROID_OFFSET]
license: CC-BY-SA-4.0
---

# X-ray Surface Brightness

## Canonical (Pirouette)
A two-dimensional observable map representing the line-of-sight integral of X-ray emissivity from the hot, ionized intracluster medium (ICM). In the Pirouette framework, S_X is the primary tracer of the collisional baryonic gas component in galaxy cluster mergers. Its centroid's displacement from the lensing convergence (κ) peak is a key observable predicted by COSMO-Γ-MERGE to constrain the collisionless dynamics of Γ-condensates.

## Astrophysics-First Summary
In observational astrophysics, X-ray Surface Brightness is the standard method for mapping the hot, diffuse gas in galaxy clusters via its thermal emission. The Pirouette framework adopts this observable directly, using the standard formula S_X ∝ ∫ n_e² Λ(T) dl as the observational target for the collisional gas component in simulations. Its primary role is to serve as a foil for the collisionless Γ-condensate, whose position is traced by gravitational lensing (κ).

## Glossary Links
- See also: Lensing Convergence (κ), Centroid Offset (Δx), Γ-Condensate