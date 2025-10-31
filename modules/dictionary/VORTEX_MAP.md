---
term: "Vortex Map"
canonical_id: "VORTEX_MAP"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-194"]
---

---
term: Vortex Map
canonical_id: VORTEX_MAP
symbol: M(Ω)
aliases: [Torsional Intensity Map, Confinement Map]
parents: [DOMA-194]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-194
      snippet: |
        Calculate the curl of the coherence field, `Ω = ∇ × F_c`. The output is a scalar field whose values represent the local torsional intensity. This is the **Vortex Map**.
  editors: [chain-of-thought-agent]
  review_log: []
triad:
  art: |
    A chart of invisible whirlpools in the fabric of coherence. It reveals that the most stable structures are not built on stillness, but are trapped within the eye of a perfectly contained storm.
  law: |
    A scalar field `Ω = ∇ × (-∇V_Γ)` where non-zero, positive peaks (`Ω > 0`) predict the spatial coordinates of stable, bound states. The positional accuracy and intensity of these peaks are testable against particle scattering cross-sections and binding energies.
  philosophy: |
    The Vortex Map transforms the problem of particle binding from a dynamic one of forces to a static, geometric one of topology. It asserts that to find a particle, one must first find its cage.
pirouette_definition: |
  A scalar field, `Ω`, derived from the curl of the Coherence Field (`F_c`). The map's value at any point represents the local torsional intensity of the coherence manifold. Positive peaks in this map correspond to the epicenters of Coherence Vortices, predicting the locations of all stable, confined structures such as baryons and mesons.
operational_definition:
  units: Energy density (J·m⁻³)
  symbol_table:
    - name: Ω
      meaning: Torsional Intensity; the scalar value of the Vortex Map at a point.
      dimensions: M L⁻¹ T⁻²
      default_range: ≥ 0
    - name: F_c
      meaning: Coherence Field; the negative gradient of the temporal pressure.
      dimensions: M L T⁻²
      default_range: contextual
    - name: V_Γ
      meaning: Temporal Pressure term from the Pirouette Lagrangian.
      dimensions: M L² T⁻²
      default_range: contextual
  measurement:
    procedures:
      - name: Indirect Inference via Scattering Tomography
        outline: |
          1. Perform high-energy particle scattering experiments (e.g., deep inelastic scattering) on a target structure (e.g., a proton).
          2. Reconstruct the internal momentum and spatial distribution of the constituents from scattering data.
          3. Numerically solve for the local Pirouette Lagrangian (`𝓛_p`) and its temporal pressure term (`V_Γ`) that reproduces the observed dynamics.
          4. Compute `Ω = ∇ × (-∇V_Γ)` from the derived `V_Γ`. The resulting scalar field is the experimentally inferred Vortex Map for the target.
        expected_signals: [Sharp, localized peaks in the reconstructed `Ω` field corresponding to constituent locations, A direct correlation between the integrated intensity `∫Ω dV` of a peak and the binding energy of the structure.]
        pitfalls: [Insufficient probe resolution blurring the map's features, Non-uniqueness in inverting scattering data to find a single valid `𝓛_p`.]
context_windows:
  - module: DOMA-194
    excerpt: |
      This protocol provides a direct path from the foundational laws of the framework to a predictive map of stable structures.
      1. **Define the Manifold**: Begin with the Pirouette Lagrangian (`𝓛_p`)...
      2. **Calculate the Coherence Field**: Compute the vector field `F_c` by taking the negative gradient of the Lagrangian's temporal pressure term (`V_Γ`).
      3. **Map the Torsion**: Calculate the curl of the coherence field, `Ω = ∇ × F_c`. The output is a scalar field whose values represent the local torsional intensity. This is the **Vortex Map**.
      4. **Identify Bound States**: Peaks on the Vortex Map correspond to the epicenters of stable Coherence Vortices.
  - module: DOMA-194
    excerpt: |
      **Baryons (Protons, Neutrons):** A baryon is a stable, three-body vortex. The three quarks are not connected by strings of force; they are three dancers in a perfectly synchronized, violent, and eternal pirouette, each tracing a path from which there is no coherent escape. The profound stability of the proton is the stability of this geometric knot.
poetic_connections:
  motifs: [contained chaos, geometric prison, turbulent stability, eye of the storm]
  evocative_lines:
    - "We sought the chains that bind the world and found not a force, but a shape."
    - "The walls of the prison are made of the prisoner's own desire to be."
  association_matrix:
    - [ "COHERENCE_VORTEX", 0.9 ]
    - [ "GLADIATOR_FORCE", 0.8 ]
    - [ "GEOMETRIC_CONFINEMENT", 0.8 ]
    - [ "PIRQUETTE_LAGRANGIAN", 0.6 ]
formal_mappings:
  candidates:
    - target: Vorticity field (ω = ∇ × v)
      domain: CM
      mapping_kind: mathematical
      justification: |
        The Vortex Map's definition as the curl of a vector field (`F_c`) is mathematically identical to the definition of vorticity in fluid dynamics. This suggests that the Coherence Field acts like a velocity field for a conceptual "coherence fluid," and bound states are particles trapped in its whirlpools.
      confidence: 0.6
    - target: MIT Bag Model "Bag" region
      domain: SM
      mapping_kind: conceptual
      justification: |
        The Vortex Map provides a first-principles, dynamical origin for the phenomenological "bag" in QCD models. A region where `Ω` exceeds a critical threshold (`Ω > Ω_c`) can be defined as the interior of the "bag," replacing a sharp, artificial boundary with a smooth, physically-motivated potential well.
      confidence: 0.4
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The number and location of stable, positive peaks on a system's Vortex Map must equal the number and location of its observed bound states."
      domain: phenomenology
      falsifier: "The discovery of a stable bound particle (e.g., a glueball or stable pentaquark) in a spatial region where the calculated Vortex Map shows no corresponding stable peak (`Ω ≈ 0`)."
      status: proposed
      links: [DOMA-194]
    - statement: "The volume integral of torsional intensity, ∫Ω dV, over a vortex region is directly proportional to the binding energy of the confined particle(s)."
      domain: theory
      falsifier: "A statistically significant lack of correlation between the integrated intensity and experimentally measured binding energies across different particle families (e.g., protons, neutrons, pions)."
      status: proposed
      links: [DOMA-194]
naming_notes:
  collisions: [The symbol `Ω` is used for the cosmological density parameter and for solid angle. Context must be used for disambiguation.]
  disambiguation: |
    `Ω` refers to the scalar value of torsional intensity at a point. "Vortex Map" refers to the entire scalar field `M(Ω)` over a region of space, often as a visualization or data set.
crosslinks:
  near_synonyms: []
  antonyms: [LAMINAR_COHERENCE_REGION]
  prerequisites: [COHERENCE_FIELD, TEMPORAL_PRESSURE, PIRQUETTE_LAGRANGIAN]
  downstream_effects: [GEOMETRIC_CONFINEMENT, GLADIATOR_FORCE, BARYON_STABILITY]
license: CC-BY-SA-4.0
---

# Vortex Map

## Canonical (Pirouette)
A scalar field, `Ω`, derived from the curl of the Coherence Field (`F_c`). The map's value at any point represents the local torsional intensity of the coherence manifold. Positive peaks in this map correspond to the epicenters of Coherence Vortices, predicting the locations of all stable, confined structures such as baryons and mesons.

## EFT-First Summary
The Vortex Map provides a geometric analogue to phenomenological confinement models in QCD, such as the MIT Bag Model. It identifies a scalar field, `Ω`, whose value can be interpreted as a confinement potential. Peaks in this field define stable regions analogous to 'bags' where quarks are trapped, replacing a hard boundary condition with a smooth, dynamically generated potential well derived from the system's underlying Lagrangian. This approach is mathematically similar to mapping vorticity in fluid dynamics.

## Glossary Links
- See also: [Coherence Vortex](<#>), [Geometric Confinement](<#>), [Gladiator Force](<#>)