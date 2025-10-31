---
term: "Stress-Energy Tensor"
canonical_id: "STRESS_ENERGY_TENSOR"
symbol: "T_μν"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-025"]
---

---
term: Stress-Energy Tensor
canonical_id: STRESS_ENERGY_TENSOR
symbol: T_μν
aliases: ["Energy-Momentum Tensor"]
parents: ["DOMA-025"]
children: ["CORE-007"]
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-025
      lines: "L102-L105"
      snippet: |
        By varying the Action with respect to the spacetime metric g_μν, we derive the system's stress-energy tensor. This tensor describes how the energy and momentum of the Coherence and Pressure fields act as the source of gravity, sculpting the geometry of spacetime itself. The dance shapes the stage.
  editors: ["GPT-4 (Pirouette Dictionary Agent)"]
  review_log: []
triad:
  art: |
    The dance shapes the stage. It is the weight and rhythm of the dancer's performance made manifest as the stage's warp and weft, telling spacetime itself how to curve in response.
  law: |
    The Stress-Energy Tensor `T_μν` is the functional derivative of the total Pirouette Action `S` with respect to the inverse spacetime metric `g^μν`, where `T_μν = (2/√-g) δS/δg^μν`. Its covariant divergence vanishes, `∇^μ T_μν = 0`, enforcing local conservation of energy and momentum for the fundamental fields.
  philosophy: |
    This tensor makes the framework's autopoietic nature concrete: the fields do not exist *in* spacetime, they *generate* it. `T_μν` closes the loop where the dynamics of Coherence and Pressure dictate the geometry, which in turn governs their propagation. There is no external, inert stage; only the self-creating dance.
pirouette_definition: |
  A symmetric rank-2 tensor that describes the density and flux of energy and momentum of the Coherence `(C)` and Temporal Pressure `(Γ)` fields. It is derived by variation of the invariant Action `S` with respect to the metric tensor `g_μν` and serves as the source term in the field equations for gravity. `T_μν` quantifies how the 'dance' of the fundamental fields shapes the 'stage' of spacetime.
operational_definition:
  units: Energy Density (J/m³), or Pressure (Pa). In natural units, `M L⁻¹ T⁻²`.
  symbol_table:
    - name: T_μν
      meaning: Stress-Energy Tensor
      dimensions: M L⁻¹ T⁻²
      default_range: contextual
    - name: C
      meaning: Coherence Field
      dimensions: M^(1/2) L^(-1/2)
      default_range: contextual
    - name: Γ
      meaning: Temporal Pressure Field
      dimensions: M^(1/2) L^(-1/2)
      default_range: contextual
    - name: g_μν
      meaning: Spacetime Metric Tensor
      dimensions: dimensionless
      default_range: contextual
  measurement:
    procedures:
      - name: Gravitational Lensing Inversion
        outline: |
          Observe the distortion of light (e.g., from the CMB or distant galaxies) as it passes through a region of spacetime. Use general relativistic inversion models to reconstruct the spacetime metric `g_μν` that produced the observed lensing. Calculate the Einstein tensor `G_μν` from the reconstructed metric. The Stress-Energy Tensor is then inferred via the field equations, `T_μν = G_μν / (8πG)`.
        expected_signals: ["Anisotropic shear patterns in galaxy shapes", "Characteristic distortions in CMB temperature and polarization maps"]
        pitfalls: ["Degeneracies with alternative gravity models", "Assumptions about the composition of the source (e.g., perfect fluid model)"]
context_windows:
  - module: DOMA-025
    excerpt: |
      With this invariant Action established, the derivation of all physical laws becomes a direct mathematical consequence. The Stress-Energy Tensor (`T_μν`): By varying the Action with respect to the spacetime metric `g_μν`, we derive the system's stress-energy tensor. This tensor describes how the energy and momentum of the Coherence and Pressure fields act as the source of gravity, sculpting the geometry of spacetime itself. The dance shapes the stage.
poetic_connections:
  motifs: [autopoiesis, self-creation, curvature, weight, rhythm, stagecraft]
  evocative_lines:
    - "The dance shapes the stage."
    - "A melody that bends when you run is no melody of truth."
  association_matrix:
    - [ "GRAVITY", 0.9 ]
    - [ "ACTION", 0.8 ]
    - [ "COHERENCE_FIELD", 0.7 ]
    - [ "TEMPORAL_PRESSURE_FIELD", 0.7 ]
formal_mappings:
  candidates:
    - target: T_μν (Hilbert Stress-Energy Tensor)
      domain: GR
      mapping_kind: mathematical
      equation_hint: |
        T_μν = 2(∂_μ C)^*(∂_ν C) + (∂_μ Γ)(∂_ν Γ) - g_μν 𝓛
      justification: |
        The Pirouette `T_μν` is defined identically to the standard Hilbert stress-energy tensor in General Relativity, derived by varying the matter action with respect to the metric. It represents the total energy-momentum contribution from the framework's fundamental scalar fields, `C` and `Γ`.
      references:
        - title: General Relativity
          where: Robert M. Wald, Chapter 4.3 and Appendix E
          date: 1984-01-01
      confidence: 1.0
  adopted:
    - target: T_μν (Hilbert Stress-Energy Tensor)
      rationale: |
        The term is adopted directly from General Relativity, as its definition, role as the source of gravity, and property of local conservation (`∇^μ T_μν = 0`) are identical. Pirouette simply specifies the content of `T_μν` in terms of its own fundamental fields.
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "The cosmological evolution of the universe (e.g., the values of Ω_M, Ω_Λ) can be fully described by the spatially-averaged components of `T_μν` derived from the `C` and `Γ` fields, without requiring ad-hoc dark matter or dark energy."
      domain: phenomenology
      falsifier: "Cosmological observations (e.g., from Planck, DESI, Euclid) show an expansion history or large-scale structure formation that is irreconcilable with the equation of state derived from the effective fluid of the `C` and `Γ` fields."
      status: proposed
      links: ["DOMA-025"]
naming_notes:
  collisions: ["`T` is often used for Temperature or Tension. The indexed form `T_μν` is unambiguous."]
  disambiguation: |
    Distinguish from the canonical Noether stress-energy tensor, which may not be symmetric or gauge-invariant. The Pirouette `T_μν` is always the symmetric Hilbert tensor derived from variation of the metric, as this is the quantity that sources gravity.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [ACTION, LAGRANGIAN_DENSITY, COHERENCE_FIELD, TEMPORAL_PRESSURE_FIELD]
  downstream_effects: [GRAVITY, SPACETIME_METRIC]
license: CC-BY-SA-4.0
---

# Stress-Energy Tensor

## Canonical (Pirouette)
A symmetric rank-2 tensor that describes the density and flux of energy and momentum of the Coherence `(C)` and Temporal Pressure `(Γ)` fields. It is derived by variation of the invariant Action `S` with respect to the metric tensor `g_μν` and serves as the source term in the field equations for gravity. `T_μν` quantifies how the 'dance' of the fundamental fields shapes the 'stage' of spacetime.

## EFT-First Summary
In General Relativity, the Stress-Energy Tensor `T_μν` describes the distribution of energy and momentum that acts as the source for spacetime curvature. The Pirouette Framework adopts this definition directly, specifying that `T_μν` arises from the dynamics of its two fundamental scalar fields: the Coherence Field `C` and the Temporal Pressure Field `Γ`. The specific form of the tensor is standard for a complex and a real scalar field, linking Pirouette's dynamics directly to measurable gravitational effects like cosmic expansion and gravitational lensing. (Ref: Wald, *General Relativity*).

## Glossary Links
- See also: [Action](<...>), [Lagrangian Density](<...>), [Gravity](<...>)