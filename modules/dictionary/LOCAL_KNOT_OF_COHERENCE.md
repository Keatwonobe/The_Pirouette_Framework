---
term: "Local knot of coherence"
canonical_id: "LOCAL_KNOT_OF_COHERENCE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-016"]
---

---
term: Local knot of coherence
canonical_id: LOCAL_KNOT_OF_COHERENCE
symbol: (C, Γ)_soliton
aliases: ["(C, Γ) soliton", "Pressuron-supported Q-ball"]
parents: ["MATH-016"]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-016
      lines: "L#7"
      snippet: |
        Mapping to Pirouette: solitons are **local knots of coherence** stabilized by temporal-pressure backreaction.
  editors: ["auto-agent"]
  review_log: []
triad:
  art: |
    A self-woven bubble of persistent phase, where a field's rhythmic breath pushes back against the void, creating a stable, lonely island of existence.
  law: |
    A local knot of coherence is a time-periodic, spatially localized, finite-energy solution to the coupled field equations for (C, Γ), characterized by a conserved charge Q. A knot is classically stable if and only if its charge Q is a strictly decreasing function of its internal frequency ω (`dQ/dω < 0`).
  philosophy: |
    This concept demonstrates how persistent, particle-like structures can self-organize from continuous fields without topological protection. It posits that stability is not always a static lock, but can be a dynamic equilibrium between internal coherence (phase rotation) and environmental backpressure (the Γ field's response).
pirouette_definition: |
  A localized, non-topological soliton composed of a complex scalar field, C, and a real scalar field, Γ. The knot's coherence is maintained by the uniform phase rotation (`C ∝ e^(iωt)`) of the C-field, which generates a conserved Noether charge, Q. This rotation prevents the soliton from dissipating, while the Γ-field dynamically adjusts its profile in response to the C-field's energy density, providing a stabilizing potential well. The entire structure is a self-sustaining equilibrium stabilized by this temporal-pressure backreaction.
operational_definition:
  units: Dimensionless (as an object count); properties have standard physical units.
  symbol_table:
    - name: C
      meaning: Complex coherence field
      dimensions: Energy
      default_range: contextual
    - name: Γ
      meaning: Real pressure/medium field
      dimensions: Energy
      default_range: contextual
    - name: Q
      meaning: Conserved Noether charge
      dimensions: dimensionless
      default_range: "> 1"
    - name: ω
      meaning: Internal phase frequency
      dimensions: T⁻¹
      default_range: "(0, m_C)"
    - name: E
      meaning: Total energy of the soliton
      dimensions: M L² T⁻²
      default_range: "> 0"
  measurement:
    procedures:
      - name: Soliton Profile Inference
        outline: |
          1. Identify a localized, persistent concentration of energy in a system described by (C, Γ) fields.
          2. Measure the spatial profiles of the C-field amplitude (`|C|=φ(r)`) and the Γ-field (`Γ(r)`).
          3. Measure the time-evolution of the C-field's phase to extract the internal frequency ω.
          4. Integrate the charge density `j⁰ = i(C*∂₀C - C∂₀C*)` over the volume to find total charge Q.
          5. To test stability, repeat for slightly different initial conditions to map out the `Q(ω)` curve and verify that `dQ/dω < 0`.
        expected_signals: ["Spherically symmetric, exponentially decaying field profiles (`φ(r)`, `Γ(r)`).", "A coherent, monochromatic phase oscillation of the C-field.", "A stable mass (E) and charge (Q)."]
        pitfalls: ["Distinguishing from a transient oscillon.", "Contamination from background radiation.", "Quantum tunneling effects leading to decay on very long timescales, which is not captured by the classical stability criterion."]
context_windows:
  - module: MATH-016
    excerpt: |
      Perturb around the Q-ball:
      (C=e^{i\omega t}[\phi(r)+\eta_1(t,\mathbf x)+i\eta_2(t,\mathbf x)],;\Gamma=\Gamma_\omega(r)+\xi(t,\mathbf x).)
      Quadratic action defines fluctuation operator (\mathcal H). **Classical stability** if (\mathcal H\ge0) on the subspace orthogonal to zero modes (translations and global phase). Equivalent criterion:
      [ \frac{dQ}{d\omega} < 0 \quad \Rightarrow \quad \text{no negative modes (stable).} ]
  - module: MATH-016
    excerpt: |
      At fixed (Q), minimize energy
      [ E_\omega[\phi,\Gamma]=\int d^3x,\Big[ |\nabla\phi|^2+\tfrac12|\nabla\Gamma|^2+U_\omega(\phi,\Gamma)\Big],\quad U_\omega\equiv V(\phi^2,\Gamma)-\omega^2\phi^2. ]
      ...
      Mapping to Pirouette: solitons are **local knots of coherence** stabilized by temporal-pressure backreaction.
poetic_connections:
  motifs: [coherence, stability, backreaction, self-confinement, bubble]
  evocative_lines:
    - "a Q-ball baseline, then extensions where (Γ) supplies pressure/stiffness"
    - "stabilized by temporal-pressure backreaction"
  association_matrix:
    - [ "TEMPORAL_PRESSURE", 0.9 ]
    - [ "COHERENCE", 0.8 ]
    - [ "SOLITON", 1.0 ]
formal_mappings:
  candidates:
    - target: Q-ball
      domain: EFT
      mapping_kind: mathematical
      equation_hint: |
        C(t,x) = e^(iωt)φ(r)
      justification: |
        The core mechanism of stability, a time-dependent phase evading Derrick's theorem, is identical to that of a Q-ball. The 'local knot' extends the minimal Q-ball by explicitly including the dynamics of a coupled scalar field (Γ) which mediates the self-interaction, providing a concrete physical basis for the potential `U(|C|²)`.
      references:
        - title: "Q-Balls"
          where: "Nucl. Phys. B 262, 263 (1985)"
          date: 1985-09-30
      confidence: 0.9
  adopted:
    - target: Q-ball (non-topological soliton)
      rationale: "The mapping is direct and serves as the primary mathematical foundation for the concept. The 'knot of coherence' is Pirouette's physical interpretation of the Q-ball's rotating phase, and 'temporal-pressure backreaction' is the interpretation of the stabilizing potential, here sourced by the Γ-field."
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "Stable local knots of coherence exist for a class of potentials V(|C|², Γ) that satisfy the Q-ball condition `min_Γ V(φ²,Γ) / φ² < m_C²/2` for some φ."
      domain: theory
      falsifier: "A mathematical proof (analytic or numerical) that no solutions with dQ/dω < 0 can be found for any potential in the specified class, or that all such solutions are unstable to perturbations not captured by the classical analysis."
      status: supported
      links: ["MATH-016"]
naming_notes:
  collisions: ["The term 'knot' could be confused with topological knots in field theory (e.g., from the Skyrme model), but this object is non-topological."]
  disambiguation: |
    Unlike a topological soliton, a local knot of coherence is protected by a conserved Noether charge (related to particle number), not a topological charge. Its stability is dynamic, not guaranteed by the topology of the field configuration.
crosslinks:
  near_synonyms: [Q_BALL, SOLITON]
  antonyms: [TOPOLOGICAL_SOLITON, RADIATION]
  prerequisites: [TEMPORAL_PRESSURE]
  downstream_effects: []
license: CC-BY-SA-4.0
---