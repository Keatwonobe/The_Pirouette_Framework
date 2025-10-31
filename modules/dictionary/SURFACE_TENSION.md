---
term: "Surface Tension"
canonical_id: "SURFACE_TENSION"
symbol: "σ"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["COSMO-006"]
---

---
term: Surface Tension
canonical_id: SURFACE_TENSION
symbol: σ
aliases: []
parents: [COSMO-006]
children: []
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: COSMO-006
      lines: "8-10"
      snippet: |
        Euler (with quantum pressure Q and surface tension σ):
        ∂*t v + (v·∇)v = −∇h(n) − ∇Φ + ∇Q/m_H + (σ/ρ) κ_s  n̂*⊥  (interface curvature term)
  editors: [auto-generator]
  review_log: []
triad:
  art: |
    A cosmic fluid's skin, taut against the void. It resists the shredding of tidal forces, holding halos together like drops of dew on a spider's web.
  law: |
    The surface tension `σ` induces an effective drag force during halo mergers, producing a velocity-dependent spatial offset `Δ_x` between dark matter and baryonic components, scaling with the effective surface-tension-to-mass ratio `(σ/m)_eff`.
  philosophy: |
    Surface tension introduces non-gravitational, collective physics to dark matter dynamics, transforming halos from simple potential wells into complex fluid objects with internal structure and boundaries. It is a primary mechanism for dissipating energy and generating observable offsets in mergers, a direct probe of the dark matter's self-interaction.
pirouette_definition: |
  An energy penalty per unit area at interfaces of fluid density, `σ`, implemented as a force term `(σ/ρ) κ_s n̂*⊥` in the superfluid Euler equation. It acts perpendicular to iso-density surfaces, proportional to their mean curvature `κ_s`, regularizing sharp gradients and driving halo cores toward spherical configurations. This term governs merger dynamics by creating an effective drag and is a configurable parameter (`sigma_surface`) of the superfluid hydrodynamics solver.
operational_definition:
  units: M T⁻² (e.g., N/m)
  symbol_table:
    - name: σ
      meaning: Surface Tension
      dimensions: M T⁻²
      default_range: Contextual, set by `sigma_surface` in simulation config
    - name: ρ
      meaning: Fluid mass density
      dimensions: M L⁻³
      default_range: contextual
    - name: κ_s
      meaning: Mean curvature of an iso-density surface
      dimensions: L⁻¹
      default_range: contextual
    - name: (σ/m)_eff
      meaning: Effective surface-tension-to-mass ratio from mergers
      dimensions: L² T⁻²
      default_range: contextual
  measurement:
    procedures:
      - name: Halo Merger Offset Analysis
        outline: |
          Simulate a binary halo merger using the `SECT-Γ-A-HALO` solver across a range of initial velocities and impact parameters. Track the separation vector `Δ_x` between the halo cores post-merger. Infer `(σ/m)_eff` by fitting the observed offset to the model prediction `Δ_x(v_rel, n, σ, ξ)`.
        expected_signals: [Post-merger core spatial offset, Dissipative signatures in merger remnants]
        pitfalls: [Degeneracy with other self-interaction terms (e.g., mutual friction), Numerical dissipation mimicking physical effects, Ambiguity in defining core centers in highly disturbed systems]
context_windows:
  - module: COSMO-006
    excerpt: |
      Euler (with quantum pressure Q and surface tension σ):
      ∂*t v + (v·∇)v = −∇h(n) − ∇Φ + ∇Q/m_H + (σ/ρ) κ_s  n̂*⊥  (interface curvature term)
      where Q= −(κ/2) ∇²√n/√n and κ_s is mean curvature of iso‑n surfaces.
  - module: COSMO-006
    excerpt: |
      Hydro‑Poisson + interface tracking (level set). Effective drag from interface work and phonon radiation → (σ/m)_eff prediction as a function of (v_rel, n, σ, ξ).
      YAML config (excerpt):
      superfluid:
        sigma_surface: ...
poetic_connections:
  motifs: [membrane, skin, interface, bubble, droplet, cohesion]
  evocative_lines:
    - "...(σ/ρ) κ_s n̂*⊥ (interface curvature term)"
    - "Effective drag from interface work..."
    - "regularization by Q and σ"
  association_matrix:
    - [ "QUANTUM_PRESSURE", 0.8 ]
    - [ "HALO_MERGER", 0.9 ]
    - [ "HEALING_LENGTH", 0.7 ]
formal_mappings:
  candidates:
    - target: Classical fluid surface tension
      domain: CM
      mapping_kind: conceptual
      equation_hint: |
        Δp = σ (1/R₁ + 1/R₂)
      justification: |
        The term `(σ/ρ) κ_s n̂*⊥` is a direct mathematical analogue of the Laplace pressure in classical fluid dynamics, which describes the pressure difference across a curved interface due to surface tension. In both cases, it represents a force that minimizes the interface's surface area.
      references:
        - title: Fluid Mechanics, Vol. 6
          where: Landau & Lifshitz, §61
          date: 1959-01-01
      confidence: 0.9
    - target: Higher-derivative operators in a scalar field EFT
      domain: EFT
      mapping_kind: mathematical
      equation_hint: |
        L ⊃ c₄ (∂_μ |φ|²)²
      justification: |
        In the low-energy effective field theory of a complex scalar field `φ`, terms with four or more derivatives, such as `(∂|φ|²)²`, generate pressure-like terms in the equations of motion that are active in regions of high gradients (i.e., at interfaces), corresponding to surface tension.
      references: []
      confidence: 0.7
  adopted:
    - target: Classical fluid surface tension
      rationale: The operational definition and mathematical form in the Pirouette Euler equation are a direct lift from classical fluid mechanics. This provides the clearest physical intuition and serves as the basis for the `SECT-Γ-A-HALO` solver's implementation.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "The observed spatial offsets in merging galaxy clusters are primarily caused by dark matter surface tension, and the magnitude of the offset is predictive of `(σ/m)_eff`."
      domain: phenomenology
      falsifier: "A large sample of mergers shows no correlation between merger velocity and offset magnitude, or the required `(σ/m)_eff` is inconsistent with constraints from halo shapes and dwarf galaxy stability."
      status: proposed
      links: [COSMO-006]
naming_notes:
  collisions: [`σ` is commonly used for velocity dispersion in astronomy and cross-section in particle physics.]
  disambiguation: |
    Within Pirouette's hydrodynamics modules (`SECT-Γ-A-*`), `σ` exclusively refers to surface tension. For scattering cross-section, use `σ_scat`. For velocity dispersion, use `σ_v`.
crosslinks:
  near_synonyms: [INTERFACE_ENERGY_DENSITY]
  antonyms: []
  prerequisites: [SUPERFLUID_HYDRODYNAMICS, DENSITY, QUANTUM_PRESSURE]
  downstream_effects: [HALO_MERGER_OFFSET, HALO_CORE_PROFILE]
license: CC-BY-SA-4.0
---

# Surface Tension

## Canonical (Pirouette)
An energy penalty per unit area at interfaces of fluid density, `σ`, implemented as a force term `(σ/ρ) κ_s n̂*⊥` in the superfluid Euler equation. It acts perpendicular to iso-density surfaces, proportional to their mean curvature `κ_s`, regularizing sharp gradients and driving halo cores toward spherical configurations. This term governs merger dynamics by creating an effective drag and is a configurable parameter (`sigma_surface`) of the superfluid hydrodynamics solver.

## EFT-First Summary
Adopting the conceptual mapping to classical fluids, Surface Tension `σ` manifests as an energy cost for creating density boundaries in the dark matter superfluid. This behavior can be sourced in an underlying effective field theory from higher-order gradient terms in the Lagrangian. Phenomenologically, this term is crucial for modeling non-dissipative drag forces in halo mergers and for regularizing the density profiles of static halos, preventing them from developing unphysical cusps.

## Glossary Links
- See also: [Quantum Pressure](<link>), [Halo Merger Offset](<link>)