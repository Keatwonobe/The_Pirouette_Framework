---
term: "Double-valued holonomy"
canonical_id: "DOUBLE_VALUED_HOLONOMY"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-QED-002_spinor_ki_defects_as_dirac"]
---

term: Double-valued holonomy
canonical_id: DOUBLE_VALUED_HOLONOMY
symbol: Ψ(2π) = -Ψ
aliases: [spinor holonomy, 720° holonomy]
parents: [MATH-QED-002]
children: [MATH-QED-003]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-QED-002_spinor_ki_defects_as_dirac
      lines: "L25-L28"
      snippet: |
        A **Ki loop** is a stable, localized phase-coherence defect whose **configuration space** carries nontrivial (\pi_1) leading to **double-valued holonomy**; parallel transport gives (\Psi\to -\Psi) under (2\pi) rotation and identity under (4\pi): spin-½.
  editors: [Pirouette Framework AI Agent]
  review_log: []
triad:
  art: |
    A spinor is a knot in time, a loop of coherence whose shadow requires two full turns to look the same. It carries a memory of its own twisting.
  law: |
    Parallel transport of a spinor field Ψ around a closed loop homologous to a 2π spatial rotation induces a sign flip (Ψ → -Ψ). Transport around a 4π loop is required to restore the identity (Ψ → Ψ).
  philosophy: |
    This property is the topological origin of spin-½ behavior. It demonstrates how a fundamental quantum property (spin) emerges from the geometric structure of a Ki loop defect in the substrate, rather than being an independent, postulated axiom.
pirouette_definition: |
  The property of a spinor field (Ψ), representing the internal phase-texture of a Ki loop defect, whereby parallel transport along a path corresponding to a 2π spatial rotation induces a π phase shift (Berry phase), resulting in a sign flip (Ψ → -Ψ). The state is restored to identity only after a 4π rotation. This arises from the non-trivial first homotopy group (π₁) of the defect's configuration space, which requires lifting the local SO(3,1) frame bundle to its double-cover, Spin(3,1).
operational_definition:
  units: Dimensionless (phase factor)
  symbol_table:
    - name: Ψ
      meaning: Spinor field; internal state of a Ki loop.
      dimensions: L⁻³/²
      default_range: 4-component complex vector
    - name: γ_Berry
      meaning: Berry phase acquired during parallel transport.
      dimensions: dimensionless
      default_range: {π, 2π}
  measurement:
    procedures:
      - name: Fermion Interferometry
        outline: |
          1. Split a coherent beam of fermions (e.g., neutrons).
          2. Pass one sub-beam through a region with a precisely controlled magnetic field to induce a 2π spin rotation relative to the reference beam.
          3. Recombine the beams and measure the resulting interference pattern.
        expected_signals:
          - For a 2π rotation: Destructive interference, indicating a relative phase shift of π.
          - For a 4π rotation: Constructive interference, indicating a relative phase shift of 2π (identity).
        pitfalls:
          - Environmental decoherence breaking the phase relationship.
          - Inaccurate rotation angle due to field instability.
context_windows:
  - module: MATH-QED-002_spinor_ki_defects_as_dirac
    excerpt: |
      A **Ki loop** is a stable, localized phase-coherence defect whose **configuration space** carries nontrivial (\pi_1) leading to **double-valued holonomy**; parallel transport gives (\Psi\to -\Psi) under (2\pi) rotation and identity under (4\pi): spin-½.
  - module: MATH-QED-002_spinor_ki_defects_as_dirac
    excerpt: |
      The Ki loop defines a nontrivial mapping... the minimal noncontractible cycle forces a lift from SO(3) to **Spin(3,1)**. The **Berry phase** of transporting the clock frame around the loop is (\gamma_{\rm Berry}=\oint \mathcal{A} = \pi ;;(\text{mod }2\pi)), so a (2\pi) rotation flips (\Psi\to -\Psi) and only (4\pi) returns identity—**spinor behavior**.
poetic_connections:
  motifs: [knot in time, topological protection, two-turn shadow, Berry phase]
  evocative_lines:
    - "A spinor is a knot in time."
    - "...whose shadow requires two turns to look the same."
  association_matrix:
    - [ "KI_LOOP", 0.9 ]
    - [ "SPIN_HALF", 0.9 ]
    - [ "BERRY_PHASE", 0.8 ]
    - [ "SPIN_STATISTICS_THEOREM", 0.7 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Spinor representation of SO(3,1)
      domain: QFT/Math
      mapping_kind: mathematical
      equation_hint: |
        A 2π rotation is represented by the matrix exp(iπJ_z) = -1 in the spin-½ representation, where J_z is a generator of rotations.
      justification: |
        The defining mathematical property of a spinor is its transformation under the double-cover of the Lorentz group, Spin(3,1). A 2π rotation in spacetime corresponds to an element in the group that squares to the identity but is not the identity itself; in the fundamental representation, this element is -1. This is a direct mathematical formalization of double-valued holonomy.
      references:
        - title: An Introduction to Quantum Field Theory
          where: Peskin & Schroeder, Chapter 3.1
          date: 1995-10-12
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "Excitations identified as electrons must exhibit a 4π rotational period to return to their original quantum state."
      domain: experiment
      falsifier: "Observation of a fundamental spin-½ particle that returns to its state after only a 2π rotation, or one that exhibits bosonic exchange statistics."
      status: supported
      links: [MATH-QED-002]
naming_notes:
  collisions: []
  disambiguation: |
    This intrinsic topological holonomy should be distinguished from the dynamic holonomy of a gauge connection (e.g., Aharonov-Bohm effect). Spinor holonomy arises from the structure of the spin bundle itself, not from an enclosed field flux.
crosslinks:
  near_synonyms: [SPINOR_HOLONOMY]
  antonyms: [SINGLE_VALUED_HOLONOMY]
  prerequisites: [KI_LOOP, SPIN_CONNECTION]
  downstream_effects: [SPIN_HALF, FERMIONIC_STATISTICS]
license: CC-BY-SA-4.0
---

# Double-valued holonomy

## Canonical (Pirouette)
The property of a spinor field (Ψ), representing the internal phase-texture of a Ki loop defect, whereby parallel transport along a path corresponding to a 2π spatial rotation induces a π phase shift (Berry phase), resulting in a sign flip (Ψ → -Ψ). The state is restored to identity only after a 4π rotation. This arises from the non-trivial first homotopy group (π₁) of the defect's configuration space, which requires lifting the local SO(3,1) frame bundle to its double-cover, Spin(3,1).

## EFT-First Summary
Double-valued holonomy is the physical manifestation of the defining mathematical property of a **spinor**. In standard quantum field theory, spinors are representations of the Spin(3,1) group, the double-cover of the Lorentz group SO(3,1). This mathematical structure dictates that a 2π rotation of the reference frame results in multiplying the spinor by -1, a property confirmed experimentally in neutron interferometry. In Pirouette, this is not a postulate but an emergent consequence of the topological structure of a **Ki loop**.

## Glossary Links
- See also: [KI_LOOP](./ki_loop.md), [SPIN_HALF](./spin_half.md), [FERMIONIC_STATISTICS](./fermionic_statistics.md)