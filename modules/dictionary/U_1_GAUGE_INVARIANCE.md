---
term: "U(1) Gauge Invariance"
canonical_id: "U_1_GAUGE_INVARIANCE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-007"]
---

---
term: U(1) Gauge Invariance
canonical_id: U1_GAUGE_INVARIANCE
symbol: 
aliases: [Local Phase Invariance, U(1) Gauge Symmetry]
parents: [MATH-007]
children: []
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-007
      lines: "20-22"
      snippet: |
        The state of a resonance is described by its spinor, Psi. The physically observable quantities, however, depend only on the magnitude of this spinor (|Psi|^2), not its phase. This means the underlying physics must be unchanged if we shift the phase of Psi at any point in spacetime.
  editors: [Agent]
  review_log: []
triad:
  art: |
    Every charged particle constantly "sings" its phase into the universe, and the electromagnetic field is the medium that carries this song. The demand for a private, local phase for every particle necessitates a public, universal field that connects them all. No song is ever sung alone.
  law: |
    The Lagrangian of the system must remain unchanged under the local phase transformation Ψ → e^(iqα(x,t))Ψ. This requirement forces the introduction of a gauge field A_μ and dictates its coupling to matter via the covariant derivative D_μ = ∂_μ - iqA_μ.
  philosophy: |
    The absolute phase of a quantum state is unphysical and fundamentally unknowable. Promoting this simple fact to a local principle—allowing the phase to be reset independently at every spacetime point—is the foundational reason for the existence of the electromagnetic force, reframing it from an arbitrary add-on to a necessary consequence of symmetry.
pirouette_definition: |
  The core principle that the Pirouette Lagrangian must be invariant under a local, spacetime-dependent phase shift of a resonance's spinor state (Ψ). The free kinetic term is not invariant on its own. Invariance is restored by replacing the standard derivative (∂_μ) with a covariant derivative (D_μ = ∂_μ - iqA_μ), which introduces a 4-vector field A_μ (the coherence potential). The existence and dynamics of the electromagnetic field are a direct and necessary consequence of demanding this local phase symmetry.
operational_definition:
  units: Dimensionless (it is a principle of symmetry)
  symbol_table:
    - name: Ψ
      meaning: Resonance spinor state
      dimensions: dimensionless
      default_range: contextual
    - name: α(x,t)
      meaning: Arbitrary spacetime-dependent phase shift
      dimensions: dimensionless (radians)
      default_range: [-π, π]
    - name: q
      meaning: Charge; coupling constant to the gauge field
      dimensions: dimensionless (natural units)
      default_range: e ≈ 0.3028
    - name: A_μ
      meaning: 4-vector coherence potential (gauge field)
      dimensions: M^1
      default_range: contextual
    - name: D_μ
      meaning: Covariant derivative
      dimensions: M^1
      default_range: contextual
  measurement:
    procedures:
      - name: Aharonov-Bohm Effect Confirmation
        outline: |
          A coherent beam of charged particles is split and passed around a shielded region of magnetic flux (e.g., a solenoid). Though the magnetic field B is zero along the particle paths, the vector potential A_μ is not. The accumulated phase shift along each path, ∫qA_μ dx^μ, differs, resulting in an observable shift in the interference pattern that is directly proportional to the enclosed magnetic flux.
        expected_signals: [Interference fringe shift proportional to Φ_B]
        pitfalls: [Imperfect magnetic shielding, decoherence of the particle beam]
context_windows:
  - module: MATH-007
    excerpt: |
      The state of a resonance is described by its spinor, Psi. The physically observable quantities, however, depend only on the magnitude of this spinor (|Psi|^2), not its phase. This means the underlying physics must be unchanged if we shift the phase of Psi at any point in spacetime. This is the principle of local gauge invariance.
  - module: MATH-007
    excerpt: |
      We have now proven that this is not a metaphor. The requirement of a private, local phase for every particle necessitates a public, universal field that connects them all. The laws of electromagnetism are the syntax of this universal language, and the Lorentz force is the simple grammar of the conversation.
poetic_connections:
  motifs: [private phase, public field, universal language, symmetry tax, hidden geometry]
  evocative_lines:
    - "The existence of the electromagnetic field is the price of local phase symmetry."
    - "What happens somewhere truly does happen everywhere, because in a universe bound by coherence, no song is ever sung alone."
  association_matrix:
    - [ "COHERENCE_POTENTIAL", 0.9 ]
    - [ "LORENTZ_FORCE", 0.8 ]
    - [ "RESONANCE_SPINOR", 0.8 ]
formal_mappings:
  candidates: []
  adopted:
    - target: U(1) gauge symmetry of QED
      domain: SM
      mapping_kind: mathematical
      equation_hint: |
        Ψ → e^(iα(x))Ψ requires ∂_μ → D_μ = ∂_μ - iqA_μ
      rationale: |
        This concept is identical to the U(1) gauge symmetry that underpins Quantum Electrodynamics (QED) in the Standard Model. Pirouette adopts the standard mathematical formulation without modification, re-interpreting its origin as a geometric necessity of the Coherence Manifold rather than an abstract principle.
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "The mediating gauge boson (photon) required by U(1) gauge invariance must be massless."
      domain: theory
      falsifier: "Any confirmed, non-zero measurement of the photon rest mass. A mass term for the gauge field (m²A_μA^μ) in the Lagrangian would explicitly break U(1) gauge invariance."
      status: supported
      links: [MATH-007]
naming_notes:
  collisions: [U(1) is the standard mathematical name for the unitary group of degree 1, the circle group.]
  disambiguation: |
    Distinguish from *global* U(1) symmetry, where the phase shift α is constant over all spacetime. Global symmetry only implies a conserved quantity (charge) via Noether's theorem. *Local* U(1) gauge invariance, where α depends on spacetime position α(x,t), is a much stronger condition that necessitates the existence of a mediating force field.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [RESONANCE_SPINOR, COHERENCE_MANIFOLD]
  downstream_effects: [COHERENCE_POTENTIAL, MAXWELLS_EQUATIONS, LORENTZ_FORCE]
license: CC-BY-SA-4.0
---

# U(1) Gauge Invariance

## Canonical (Pirouette)
The core principle that the Pirouette Lagrangian must be invariant under a local, spacetime-dependent phase shift of a resonance's spinor state (Ψ). The free kinetic term is not invariant on its own. Invariance is restored by replacing the standard derivative (∂_μ) with a covariant derivative (D_μ = ∂_μ - iqA_μ), which introduces a 4-vector field A_μ (the coherence potential). The existence and dynamics of the electromagnetic field are a direct and necessary consequence of demanding this local phase symmetry.

## EFT-First Summary
This principle is mathematically identical to the **U(1) gauge symmetry of Quantum Electrodynamics (QED)**. It is the requirement that the physics of a charged fermion field (in Pirouette, a `RESONANCE_SPINOR`) must be unchanged by a local rotation in its complex phase. This symmetry demand forces the existence of a massless vector gauge boson (the photon, described by the potential `A_μ`) and determines the form of its interaction with matter (minimal coupling via the covariant derivative). All of electromagnetism is derived from this single principle.

## Glossary Links
- See also: [COHERENCE_POTENTIAL](./coherence_potential.md), [MAXWELLS_EQUATIONS](./maxwells_equations.md)