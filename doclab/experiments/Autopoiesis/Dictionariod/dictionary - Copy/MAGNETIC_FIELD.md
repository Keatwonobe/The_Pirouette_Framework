---
term: "Magnetic Field"
canonical_id: "MAGNETIC_FIELD"
symbol: "B"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["CORE-007_the_current_and_the_compass"]
---

---
term: Magnetic Field
canonical_id: MAGNETIC_FIELD
symbol: B
aliases: []
parents: [CORE-007_the_current_and_the_compass]
children: [CORE-008_placeholder]
status: draft
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: CORE-007_the_current_and_the_compass
      lines: "L68-L72"
      snippet: |
        When a charged particle moves, its Lagrangian becomes velocity-dependent. The act of moving through regions of varying temporal phase creates a rotational or torsional stress in its local coherence manifold. This "curl" in the manifold is the magnetic field (B).
  editors: [GPT-4_Pirouette_Agent]
  review_log: []
triad:
  art: |
    A compass feels not a force, but the twist in the fabric of coherence. The magnetic field is a temporal vortex, a silent whirlpool in the flow of resonance that guides the moving charge along a curved path to stability.
  law: |
    The magnetic field (B) is a vector field defined as the rotational shear in the coherence manifold, proportional to the curl of the Pirouette vector potential (B ∝ ∇ × A_p). Any moving charged system will experience a force perpendicular to both its velocity and the local B-field vector, as it navigates this curl to maximize coherence.
  philosophy: |
    The magnetic field is not a fundamental entity but an emergent, relativistic effect of charge in motion. Its existence as a geometric curl, rather than a simple gradient, demonstrates that forces arise from the complex topology of the coherence manifold, providing a unified origin for the seemingly disparate electric and magnetic phenomena.
pirouette_definition: |
  A vector field representing a rotational shear or curl within the coherence manifold. This shear is induced by the motion of a charged particle, which makes its Pirouette Lagrangian (𝓛_p) velocity-dependent. The magnetic field B is mathematically defined as being proportional to the curl of the Pirouette vector potential, B ∝ ∇ × A_p. It manifests as an influence that deflects moving charges along a path perpendicular to both their velocity and the field vector, which represents the geodesic for maximizing coherence within this torsional stress.
operational_definition:
  units: Tesla (T)  [M·T⁻²·I⁻¹]
  symbol_table:
    - name: B
      meaning: Magnetic Field vector
      dimensions: M·T⁻²·I⁻¹
      default_range: contextual
    - name: A_p
      meaning: Pirouette vector potential
      dimensions: M·L·T⁻²·I⁻¹
      default_range: contextual
  measurement:
    procedures:
      - name: Test Charge Deflection Mapping
        outline: |
          1. Isolate a region of space, shielding it from known electric fields (coherence gradients).
          2. Propel a test particle of known charge (q) and velocity (v) through the region.
          3. Measure the vector of deflection (force, F_m) on the test particle.
          4. The magnetic field B is solved from the relation F_m = q(v × B). By varying the initial velocity vector v, the full B vector at a point can be determined.
        expected_signals: [A force vector F_m measured to be consistently perpendicular to the velocity vector v.]
        pitfalls: [Failure to completely shield external electric fields, which would add a non-perpendicular force component. Perturbation of the target field by the test charge's own field.]
context_windows:
  - module: CORE-007_the_current_and_the_compass
    excerpt: |
      When a charged particle moves, its Lagrangian becomes velocity-dependent. The act of moving through regions of varying temporal phase creates a rotational or torsional stress in its local coherence manifold. This "curl" in the manifold is the magnetic field (B).
  - module: CORE-007_the_current_and_the_compass
    excerpt: |
      This geometric origin instantly explains the Lorentz force law's peculiar perpendicularity. A moving charge interacting with a magnetic field experiences a force perpendicular to both its velocity and the field itself. This is because the path of maximal coherence in a rotationally sheared manifold is not straight ahead, but a curve. The magnetic force is the system's attempt to navigate this temporal vortex to maintain its own resonant stability.
poetic_connections:
  motifs: [vortex, shear, curl, navigation, guidance, perpendicularity, twist]
  evocative_lines:
    - "the shear of the current."
    - "the universe's right-hand rule for staying coherent."
    - "The Compass is the geometry of the landscape it must navigate."
  association_matrix:
    - [ "ELECTRIC_FIELD", 0.8 ]
    - [ "CHARGE", 0.9 ]
    - [ "PIROUETTE_LAGRANGIAN", 0.7 ]
    - [ "PIROUETTE_VECTOR_POTENTIAL", 1.0 ]
formal_mappings:
  candidates:
    - target: Magnetic B-field
      domain: SM|CM
      mapping_kind: mathematical|operational
      equation_hint: |
        B = ∇ × A
      justification: |
        The Pirouette B-field is defined as the curl of a vector potential (A_p) and produces a force perpendicular to a charge's velocity. This is mathematically and operationally identical to the standard magnetic B-field in classical and relativistic electrodynamics, which is defined as the curl of the magnetic vector potential A.
      references:
        - title: Introduction to Electrodynamics
          where: D.J. Griffiths, Chapter 5
          date: 2017-01-01
      confidence: 0.95
  adopted:
    - target: Magnetic B-field (as in Maxwell's Equations / Lorentz Force Law)
      rationale: The Pirouette definition directly reproduces the mathematical structure and operational consequences of the standard B-field, merely providing a deeper geometric origin story within the coherence manifold.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The magnetic field B is divergenceless (∇ ⋅ B = 0) because it is defined as the curl of a vector potential."
      domain: theory|experiment
      falsifier: "The confirmed, reproducible observation of a magnetic monopole, which would act as a source or sink for B-field lines, necessitating that ∇ ⋅ B ≠ 0."
      status: supported
      links: [CORE-007_the_current_and_the_compass]
    - statement: "The force exerted by a pure magnetic field on a moving charged particle is always perpendicular to the particle's velocity vector."
      domain: experiment
      falsifier: "Observation of a component of force parallel to the velocity vector in a region with a confirmed pure magnetic field (no electric field)."
      status: supported
naming_notes:
  collisions: [The symbol 'H' is used for Magnetic Field Strength in materials, which is distinct from the fundamental Magnetic Field B that exerts force. Pirouette's B maps directly to the fundamental B-field.]
  disambiguation: |
    Within Pirouette, "Magnetic Field" always refers to the fundamental rotational shear B. It is a geometric property of the coherence manifold itself, not a response of a medium.
crosslinks:
  near_synonyms: []
  antonyms: [ELECTRIC_FIELD]
  prerequisites: [CHARGE, PIROUETTE_VECTOR_POTENTIAL]
  downstream_effects: [LORENTZ_FORCE, MAXWELL_EQUATIONS]
license: CC-BY-SA-4.0
---

# Magnetic Field

## Canonical (Pirouette)
A vector field representing a rotational shear or curl within the coherence manifold. This shear is induced by the motion of a charged particle, which makes its Pirouette Lagrangian (𝓛_p) velocity-dependent. The magnetic field B is mathematically defined as being proportional to the curl of the Pirouette vector potential, B ∝ ∇ × A_p. It manifests as an influence that deflects moving charges along a path perpendicular to both their velocity and the field vector, which represents the geodesic for maximizing coherence within this torsional stress.

## EFT-First Summary
The Pirouette Magnetic Field (B) is operationally and mathematically identical to the magnetic B-field of standard electromagnetism. It is defined as the curl of a potential field (B = ∇ × A), which guarantees it is divergenceless and accounts for the perpendicular nature of the magnetic force. The Pirouette framework provides a microphysical origin for this geometry, identifying it as a torsional stress in a "coherence manifold" created by moving charges.

## Glossary Links
- See also: [Charge](...), [Electric Field](...), [Lorentz Force](...)