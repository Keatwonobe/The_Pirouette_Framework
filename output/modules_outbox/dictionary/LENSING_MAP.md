---
term: "Lensing κ map"
canonical_id: "LENSING_MAP"
symbol: "κ"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["COSMO-002"]
---

---
term: Lensing κ map
canonical_id: LENSING_KAPPA_MAP
symbol: κ
aliases: ["gravitational convergence", "kappa map"]
parents: [COSMO-002]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: COSMO-002
      snippet: |
        Observables:
        • Lensing κ(x,y) from Σ(x,y)=∫(ρ_Γ+ρ_g+ρ_*) dl.
  editors: [Pirouette Framework Agent]
  review_log: []
triad:
  art: |
    A celestial inkblot test, where the universe's unseen gravity bends light, revealing the true shape of cosmic leviathans. It is the silhouette cast by mass itself, indifferent to how brightly its components shine.
  law: |
    The lensing κ map is the dimensionless projected surface mass density (Σ/Σ_crit), directly proportional to the Laplacian of the gravitational lensing potential. Its peaks trace the centroids of total mass, irrespective of composition or collisional state.
  philosophy: |
    The κ map provides the ground truth for mass distribution, acting as an incorruptible ledger against which the dynamics of luminous or collisional matter (e.g., X-ray gas) are judged. In Pirouette, its separation from gas centroids in mergers is a primary, falsifiable test of the Γ-condensate's effectively collisionless nature.
pirouette_definition: |
  A 2D scalar field, κ(x,y), representing the projected surface mass density Σ(x,y) in units of the critical surface density Σ_crit. It is a direct observable derived from gravitational lensing shear and/or magnification. In the context of COSMO-Γ-MERGE, the κ map's peaks are used to locate the center of total mass (Γ-condensate + baryons) and quantify its offset from the centroid of collisional X-ray emitting gas.
operational_definition:
  units: Dimensionless
  symbol_table:
    - name: κ
      meaning: Lensing convergence
      dimensions: dimensionless
      default_range: "[−0.05, 1.5] for clusters"
    - name: Σ
      meaning: Projected surface mass density
      dimensions: M L⁻²
      default_range: "contextual"
    - name: Σ_crit
      meaning: Critical surface density for lensing
      dimensions: M L⁻²
      default_range: "contextual; depends on source/lens redshifts"
  measurement:
    procedures:
      - name: Weak Lensing Shear Inversion
        outline: |
          Measure the statistical distortion (shear, γ) of background galaxy shapes across a field. Invert the shear field using a reconstruction algorithm (e.g., Kaiser-Squires) to recover the convergence field κ. Peaks in the reconstructed κ map indicate concentrations of projected mass.
        expected_signals: [Coherent alignment of background galaxy ellipticities, Signal-to-noise > 3 peaks co-located with galaxy clusters]
        pitfalls: [PSF anisotropy, Intrinsic galaxy alignments, Mass-sheet degeneracy, Projection effects from uncorrelated foreground/background structures]
context_windows:
  - module: COSMO-002
    excerpt: |
      Demonstrate that collisionless behavior of Γ reproduces observed κ–X‑ray separations and their redshift/mass scaling **without particulate CDM**, using the same frozen potential V(Γ) from COSMO‑Γ‑000.
  - module: COSMO-002
    excerpt: |
      Observables:
      • Lensing κ(x,y) from Σ(x,y)=∫(ρ_Γ+ρ_g+ρ_*) dl.
      • X‑ray surface brightness S_X∝∫ n_e² Λ(T) dl.
      • Centroid offset Δx(t) between κ peak(s) and S_X peak(s).
poetic_connections:
  motifs: [gravity's silhouette, mass truth, cosmic cartography, collisionless witness]
  evocative_lines:
    - "The survival of κ peaks after core passage..."
    - "κ–X‑ray separations and their redshift/mass scaling..."
  association_matrix:
    - [ "XRAY_SURFACE_BRIGHTNESS", 0.9 ]
    - [ "LENSING_GAS_OFFSET", 0.9 ]
    - [ "GAMMA_CONDENSATE", 0.7 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Gravitational lensing convergence, κ
      domain: GR
      mapping_kind: mathematical
      equation_hint: |
        κ = Σ / Σ_crit = (1/2) ∇²ψ, where ψ is the 2D lensing potential.
      justification: |
        The Pirouette κ is identical to the standard gravitational lensing convergence in cosmology. It is a direct consequence of the deflection of light by the total projected mass-energy as described by General Relativity.
      references:
        - title: "Gravitational Lensing: Strong, Weak and Micro"
          where: "Saas-Fee Advanced Course 33. Springer-Verlag Berlin Heidelberg, 2006."
          date: 2006-01-01
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "In energetic cluster mergers, the peaks of the κ map (total mass) are spatially offset from the peaks of X-ray surface brightness (collisional gas)."
      domain: phenomenology
      falsifier: "Consistent observation of zero offset (Δx ≈ 0) between κ and X-ray peaks in a statistical sample of post-pericenter merging clusters, implying the dominant mass component is as collisional as the intracluster medium."
      status: supported
      links: [COSMO-002]
    - statement: "The survival and fractional mass retention of κ peaks post-merger is a direct, predictable consequence of the Γ-condensate's potential V(Γ)."
      domain: theory
      falsifier: "Observed κ peaks in post-merger systems are systematically weaker or more disrupted than predicted by the `f_ret(M,b,v_in)` function derived from the frozen V(Γ) potential."
      status: proposed
      links: [COSMO-002]
naming_notes:
  collisions: ["κ is used for spatial curvature in FRW cosmology (k=0,±1), but context (2D field, lensing) prevents ambiguity."]
  disambiguation: |
    Distinct from maps of the Sunyaev-Zel'dovich (SZ) effect, which trace the projected gas *pressure* (Compton-y parameter), not the total mass. While spatially correlated in relaxed systems, κ and y maps trace physically distinct quantities that separate during mergers.
crosslinks:
  near_synonyms: [SURFACE_MASS_DENSITY]
  antonyms: [XRAY_SURFACE_BRIGHTNESS]
  prerequisites: [GAMMA_CONDENSATE]
  downstream_effects: [LENSING_GAS_OFFSET]
license: CC-BY-SA-4.0
---

# Lensing κ map

## Canonical (Pirouette)
A 2D scalar field, κ(x,y), representing the projected surface mass density Σ(x,y) in units of the critical surface density Σ_crit. It is a direct observable derived from gravitational lensing shear and/or magnification. In the context of COSMO-Γ-MERGE, the κ map's peaks are used to locate the center of total mass (Γ-condensate + baryons) and quantify its offset from the centroid of collisional X-ray emitting gas.

## EFT-First Summary
In the weak-field limit of GR, the lensing κ map is the primary observational probe of the total projected energy-momentum tensor, T₀₀. It is sourced by all gravitating components (Σ = ∫(ρ_Γ+ρ_g+ρ_*) dl), making it the definitive tracer of the mass distribution described in a low-energy effective theory of cosmology. Its behavior in dynamical situations, such as cluster mergers, directly constrains the self-interaction properties of the theory's dark sector.

## Glossary Links
- See also: [SURFACE_MASS_DENSITY](<#>), [LENSING_GAS_OFFSET](<#>), [XRAY_SURFACE_BRIGHTNESS](<#>)