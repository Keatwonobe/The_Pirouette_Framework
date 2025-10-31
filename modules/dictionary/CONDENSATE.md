---
term: "Γ-condensate"
canonical_id: "CONDENSATE"
symbol: "Γ"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["COSMO-002"]
---

---
term: Γ-condensate
canonical_id: GAMMA_CONDENSATE
symbol: Γ
aliases: []
parents: [COSMO-Γ-000, COSMO-Γ-HALO]
children: [COSMO-002]
status: candidate
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: COSMO-002
      lines: "Summary of Claims"
      snippet: |
        Γ condensates behave as effectively collisionless mass components across cluster‑scale encounters; gas shocks and lags.
  editors: [system-agent]
  review_log: []
triad:
  art: |
    A standing wave of spacetime's substance, holding its form as a silent, collisionless ghost while the fires of baryonic matter wash through it.
  law: |
    In gravitational collisions, the mass peak of a Γ-condensate (measured by lensing κ) separates from the baryonic gas peak (measured by X-rays S_X) with an offset Δx determined solely by the field potential V(Γ), initial velocities, and masses, not by a fundamental particle cross-section.
  philosophy: |
    Γ-condensate reframes dark matter from a sea of particles to a continuous field phenomenon, aiming to unify galactic-scale core profiles and cluster-scale collision dynamics under a single, non-tunable potential V(Γ).
pirouette_definition: |
  A real scalar field, Γ, whose dynamics are governed by the non-linear wave equation `Γ̈ − ∇²Γ + V′(Γ) = 0`. Its energy density, `ρ_Γ = ½(Γ̇² + |∇Γ|²) + V(Γ) − V(Γ_∞)`, sources gravity via the Poisson equation. Stable, localized, non-dispersive solutions (solitons) of this field form gravitational halos that behave as an effectively collisionless mass component in astrophysical dynamics.
operational_definition:
  units: Γ has units of Mass or Energy in a natural unit system (ħ=c=1).
  symbol_table:
    - name: Γ
      meaning: The condensate field amplitude.
      dimensions: M (in natural units)
      default_range: contextual
    - name: ρ_Γ
      meaning: Energy density of the Γ-condensate.
      dimensions: ML⁻¹T⁻²
      default_range: "> 0"
    - name: V(Γ)
      meaning: The self-interaction potential of the Γ field.
      dimensions: ML⁻¹T⁻²
      default_range: contextual
    - name: Δx
      meaning: Projected offset between lensing (κ) and gas (X-ray) centroids.
      dimensions: L
      default_range: 0–500 kpc
    - name: σ_eff/m
      meaning: Effective self-interaction cross-section proxy derived from field dynamics.
      dimensions: L²M⁻¹
      default_range: 0–0.2 cm² g⁻¹
  measurement:
    procedures:
      - name: Cluster Merger Offset Analysis
        outline: |
          1. Observe a merging galaxy cluster system (e.g., 1E 0657-56, "Bullet Cluster").
          2. Reconstruct the total mass distribution Σ(x,y) via gravitational lensing to locate the mass centroids (κ peaks).
          3. Map the hot intracluster gas via X-ray imaging to locate the gas centroids (S_X peaks).
          4. Measure the projected separation Δx between the κ and S_X peaks.
          5. Compare the measured (Δx, M, v_in, z) to the scaling law predictions from `COSMO-Γ-MERGE` for a given frozen potential V(Γ).
        expected_signals: [Significant spatial offset Δx > 0 between lensing and X-ray peaks post-pericenter, Survival of distinct lensing peaks after collision]
        pitfalls: [Projection effects obscuring 3D geometry, Ambiguity in centroid definition for complex morphologies, Degeneracies with impact parameter and time-since-collision]
context_windows:
  - module: COSMO-002
    excerpt: |
      Simulate and predict lensing–gas centroid offsets in cluster mergers using Γ‑condensates (topological index T) plus collisional baryonic gas. Demonstrate that collisionless behavior of Γ reproduces observed κ–X‑ray separations and their redshift/mass scaling **without particulate CDM**, using the same frozen potential V(Γ) from COSMO‑Γ‑000.
  - module: COSMO-002
    excerpt: |
      An apparent “σ/m” constraint inferred in CDM language maps in Pirouette to a **derived** (non‑tunable) effective collisional proxy σ_eff/m determined by Γ soliton overlap; prediction: σ_eff/m ≲ 0.2 cm² g⁻¹ for Bullet‑like events when V(Γ) is COSMO‑Γ‑000‑frozen.
poetic_connections:
  motifs: [collisionless ghost, standing wave, field core, potential landscape]
  evocative_lines:
    - "The Γ peaks re‑emerge with fractional mass retention..."
    - "gas shocks and lags."
  association_matrix:
    - [ "self-interaction_potential", 1.0 ]
    - [ "κ-X-ray_offset", 0.9 ]
    - [ "particulate_dark_matter", 0.8 ]
formal_mappings:
  candidates:
    - target: Real scalar field dark matter (SFDM) / Fuzzy Dark Matter (FDM)
      domain: EFT
      mapping_kind: mathematical
      equation_hint: |
        L = ½(∂_μ Γ)² - V(Γ)  →  (∂_t² - ∇²)Γ + V′(Γ) = 0
      justification: |
        Γ-condensate is a specific implementation of a real scalar field as a dark matter candidate. The equation `Γ̈ − ∇²Γ + V′(Γ) = 0` is the Euler-Lagrange equation for a scalar field with potential V(Γ) in the non-relativistic, weak-field limit. This class of models is widely studied under names like SFDM, FDM, or Bose-Einstein Condensate (BEC) dark matter.
      references:
        - title: "Scalar Field Dark Matter"
          where: "Hui, L., Ostriker, J.P., Tremaine, S., Witten, E. (2017), Phys. Rev. D 95, 043541"
          date: 2017-02-27
      confidence: 0.95
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The observed scaling of lensing-gas offsets (Δx) in merging clusters with mass, velocity, and redshift is uniquely predicted by the frozen Γ-potential V(Γ) established from galactic core properties (COSMO-Γ-HALO)."
      domain: phenomenology
      falsifier: "Multiple merging clusters are observed where the measured Δx significantly deviates from the predicted scaling law, or where matching Δx requires a V(Γ) that is inconsistent with galactic rotation curves."
      status: proposed
      links: [COSMO-002, COSMO-Γ-HALO]
    - statement: "In mergers, Γ-condensate halos survive core passage and re-emerge with a predictable fractional mass retention `f_ret` > 0.8 for typical cluster parameters."
      domain: phenomenology
      falsifier: "Observation of post-merger systems where the lensing signal is significantly disrupted or has a mass far below the predicted `f_ret`, indicating a more dissipative interaction than the model allows."
      status: proposed
      links: [COSMO-002]
naming_notes:
  collisions: [The symbol Γ (Gamma) is also used for the Gamma function Γ(z) in mathematics and the photon symbol γ (lowercase) in physics. Context (cosmology, field theory) is crucial.]
  disambiguation: |
    Γ-condensate refers to the macroscopic field configuration, not a fundamental particle (though one could be associated with its quantum excitation). It is distinct from particulate dark matter models (like WIMPs) which propose a gas of individual particles.
crosslinks:
  near_synonyms: [SOLITON_HALO]
  antonyms: [PARTICULATE_DARK_MATTER]
  prerequisites: [V_GAMMA_POTENTIAL, GAMMA_HALO]
  downstream_effects: [KAPPA_XRAY_OFFSET]
license: CC-BY-SA-4.0
---

# Γ-condensate

## Canonical (Pirouette)
A real scalar field, Γ, whose dynamics are governed by the non-linear wave equation `Γ̈ − ∇²Γ + V′(Γ) = 0`. Its energy density, `ρ_Γ = ½(Γ̇² + |∇Γ|²) + V(Γ) − V(Γ_∞)`, sources gravity via the Poisson equation. Stable, localized, non-dispersive solutions (solitons) of this field form gravitational halos that behave as an effectively collisionless mass component in astrophysical dynamics.

## EFT-First Summary
In the language of effective field theory, the Γ-condensate is a model of Scalar Field Dark Matter (SFDM). It posits a real, classical scalar field whose coherent, ground-state configuration forms galactic halos. Its dynamics, derived from a Lagrangian `L = ½(∂_μ Γ)² - V(Γ)`, naturally produce a core in the density profile and give rise to wave-like phenomena. In astrophysical collisions, the field's self-interaction potential `V(Γ)` dictates its effectively collisionless behavior, providing an alternative to the particle-based description of dark matter.

## Glossary Links
- See also: V(Γ) potential, κ-X-ray offset, Particulate Dark Matter, Gamma Halo