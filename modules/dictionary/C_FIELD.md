---
term: "C-field"
canonical_id: "C_FIELD"
symbol: "C"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-016"]
---

---
term: C-field
canonical_id: C_FIELD
symbol: C
aliases: []
parents: ['MATH-016']
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-016
      lines: "L8"
      snippet: |
        Fields: complex (C), real (Γ). Flat space first; curvature is a controlled perturbation.
  editors: [agent:llm-v1]
  review_log: []
triad:
  art: |
    A self-trapped vortex of phase, spinning at a constant rate to hold itself together against dispersal. It is the locus of conserved charge, a knot of pure coherence.
  law: |
    For a stable, spherically symmetric soliton (Q-ball) to exist, there must be a frequency ω such that the energy functional `E_ω = E - ωQ` is minimized for a fixed charge `Q`. The soliton branch is dynamically stable against small perturbations if and only if the charge is a monotonically decreasing function of the frequency (`dQ/dω < 0`).
  philosophy: |
    The C-field demonstrates emergent stability from continuous dynamics. A conserved charge (from a symmetry) allows a simple scalar field to form persistent, particle-like objects (solitons) without requiring fundamental discreteness, serving as a primary model for localized coherence.
pirouette_definition: |
  The C-field is the complex scalar field `C` whose `U(1)` phase symmetry gives rise to a conserved Noether charge `Q`. Under potentials that satisfy the Q-ball condition (`U(φ)/φ² < m_C²/2` for some `φ`), the field can form stable, non-topological solitons (Q-balls) by assuming a time-dependent phase `C(t,x) = e^(iωt)φ(x)`. These solitons are localized, finite-energy configurations stabilized by the balance between gradient energy and potential energy, a mechanism described as temporal-pressure backreaction.
operational_definition:
  units: Mass (`[M]`) or Energy (`[E]`) in natural units (`ħ=c=1`).
  symbol_table:
    - name: C
      meaning: The complex scalar field value at a spacetime point.
      dimensions: M
      default_range: contextual
    - name: Q
      meaning: Conserved U(1) Noether charge, integrated over space.
      dimensions: dimensionless
      default_range: `Q > 0`
    - name: ω
      meaning: Internal phase rotation frequency of the soliton solution.
      dimensions: M
      default_range: `0 < ω < m_C`, where `m_C` is the C-particle mass.
    - name: φ
      meaning: Real-valued radial profile of the C-field's magnitude (`φ = |C|`) in a soliton.
      dimensions: M
      default_range: contextual
  measurement:
    procedures:
      - name: Gravitational Inference
        outline: |
          Infer the existence and profile `φ(r)` of a C-field soliton (Q-ball) by observing its gravitational effects. Measure the mass distribution via gravitational lensing of background sources or the orbital dynamics of nearby test particles. The inferred profile must match solutions to the Euler-Lagrange equations for a candidate potential `V(|C|², Γ)`.
        expected_signals: [Spherically symmetric mass distribution, Specific mass-radius relation predicted by the potential]
        pitfalls: [Degeneracy with other compact objects (e.g., boson stars), Weak signals for low-mass/low-density solitons]
context_windows:
  - module: MATH-016
    excerpt: |
      Fields: complex (C), real (Γ). Flat space first; curvature is a controlled perturbation.
      Lagrangian (minimal):
      [ \mathcal L = |\partial C|^2 + \tfrac12(\partial\Gamma)^2 - V(|C|^2,\Gamma). ]
      Potential admits a Q-ball window: there exists (\omega\in(0, m_C)) such that
      [ U(\phi) \equiv \min_{\Gamma} V(\phi^2,\Gamma) \quad \text{satisfies}\quad \frac{U(\phi)}{\phi^2} < \frac{m_C^2}{2} ;\text{for some }\phi>0. ]
  - module: MATH-016
    excerpt: |
      Perturb around the Q-ball:
      (C=e^{i\omega t}[\phi(r)+\eta_1(t,\mathbf x)+i\eta_2(t,\mathbf x)],;\Gamma=\Gamma_\omega(r)+\xi(t,\mathbf x).)
      Quadratic action defines fluctuation operator (\mathcal H). **Classical stability** if (\mathcal H\ge0) on the subspace orthogonal to zero modes (translations and global phase). Equivalent criterion:
      [ \frac{dQ}{d\omega} < 0 \quad \Rightarrow \quad \text{no negative modes (stable).} ]
poetic_connections:
  motifs: [coherence, charge, vortex, self-trapping, soliton]
  evocative_lines:
    - "solitons are local knots of coherence"
    - "stabilized by temporal-pressure backreaction"
  association_matrix:
    - [ "Q_BALL", 0.9 ]
    - [ "CONSERVED_CHARGE", 1.0 ]
    - [ "TEMPORAL_PRESSURE", 0.7 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Complex scalar field (`φ` or `ψ`)
      domain: QFT
      mapping_kind: mathematical
      equation_hint: |
        L = |∂μφ|^2 - V(|φ|)
      justification: |
        The C-field is mathematically identical to a standard complex scalar field with a global U(1) symmetry, a foundational object in quantum field theory and cosmology. Its non-topological soliton solutions, Q-balls, are a well-studied phenomenon first analyzed in this context.
      references:
        - title: "Q-balls"
          where: "Nucl. Phys. B 262, 2 (1985)"
          date: 1985-09-23
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "Stable, non-dissipating C-field solitons (Q-balls) can exist in 3+1 dimensions if their charge Q is sufficiently large and the stability condition dQ/dω < 0 is met."
      domain: theory
      falsifier: "Numerical evolution showing that all localized C-field configurations, under potentials satisfying the Q-ball window condition, either disperse or collapse to a singularity, even when dQ/dω < 0 is satisfied. This would falsify the classical stability criterion."
      status: supported
      links: ['MATH-016']
naming_notes:
  collisions: ["The symbol C is commonly used for the speed of light, capacitance, or the set of complex numbers. In Pirouette, it refers exclusively to this field unless explicitly subscripted or defined otherwise."]
  disambiguation: |
    Distinguish from the Gamma-field (Γ), its real scalar partner in many models. `C` is complex and carries the conserved U(1) charge; `Γ` is real and typically acts as a mediator or provides environmental pressure.
crosslinks:
  near_synonyms: []
  antonyms: [REAL_SCALAR_FIELD]
  prerequisites: [LAGRANGIAN_MECHANICS, NOETHER_THEOREM]
  downstream_effects: [Q_BALL, SOLITON_STABILITY]
license: CC-BY-SA-4.0
---

# C-field

## Canonical (Pirouette)
The C-field is the complex scalar field `C` whose `U(1)` phase symmetry gives rise to a conserved Noether charge `Q`. Under potentials that satisfy the Q-ball condition (`U(φ)/φ² < m_C²/2` for some `φ`), the field can form stable, non-topological solitons (Q-balls) by assuming a time-dependent phase `C(t,x) = e^(iωt)φ(x)`. These solitons are localized, finite-energy configurations stabilized by the balance between gradient energy and potential energy, a mechanism described as temporal-pressure backreaction.

## EFT-First Summary
In standard effective field theory (EFT), the C-field is a complex scalar field `φ` with a global `U(1)` symmetry. Its Lagrangian is `L = |∂μφ|² - V(|φ|²)`. The conserved Noether charge associated with the `U(1)` symmetry allows the formation of non-topological solitons known as Q-balls, which are stable, localized field configurations. The existence and stability of these solutions are well-established (S. Coleman, Nucl. Phys. B 262, 1985).

## Glossary Links
- See also: [Q-ball](...), [Γ-field](...), [Conserved Charge](...)