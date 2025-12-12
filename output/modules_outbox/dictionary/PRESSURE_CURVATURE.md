---
term: "Pressure Curvature"
canonical_id: "PRESSURE_CURVATURE"
symbol: "λ_Γ"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-079"]
---

---
term: Pressure Curvature
canonical_id: PRESSURE_CURVATURE
symbol: λ_Γ
aliases: []
parents: [DOMA-079]
children: [CORE-007, CORE-008]
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-079
      lines: "L63-L65"
      snippet: |
        Each coefficient has a clear physical meaning and is experimentally measurable:
        *   `λ_Γ`: **Pressure Curvature.** How sensitive the system is to its environment.
  editors: [auto-scribe-agent]
  review_log: []
triad:
  art: |
    The steepness of the riverbank that contains the flow of being. Gentle slopes permit wide meandering; steep cliffs enforce a narrow, rigid path.
  law: |
    Pressure Curvature is the second derivative of the environmental potential `V_Γ` with respect to Temporal Pressure `Γ`, evaluated at the optimum `Γ₀`. It quantifies the harmonic restoring force a system experiences per unit deviation from its optimal pressure.
  philosophy: |
    This term represents the degree to which a system's existence is a fragile negotiation with its environment. A high `λ_Γ` signifies a specialist, exquisitely adapted but brittle; a low `λ_Γ` signifies a generalist, resilient but less able to achieve peak performance.
pirouette_definition: |
  The coefficient `λ_Γ` in the Temporal Pressure potential `V_Γ` that quantifies the harmonic restoring force a system experiences when its ambient Temporal Pressure `Γ` deviates from its optimal value `Γ₀`. It is the proportionality constant in the environmental cost term, `λ_Γ(Γ - Γ₀)²`, thereby defining the curvature of the parabolic "pressure basin" in the coherence manifold. A higher value indicates greater sensitivity and a stronger constraint by the environment.
operational_definition:
  units: Energy / (Temporal Pressure)²
  symbol_table:
    - name: λ_Γ
      meaning: Pressure Curvature
      dimensions: M L² T⁻² [P]⁻² (where [P] is the dimension of Temporal Pressure)
      default_range: contextual
    - name: V_Γ
      meaning: Temporal Pressure Potential
      dimensions: M L² T⁻² (Energy)
      default_range: contextual
    - name: Γ
      meaning: Ambient Temporal Pressure
      dimensions: [P]
      default_range: contextual
    - name: Γ₀
      meaning: Optimal Temporal Pressure
      dimensions: [P]
      default_range: contextual
  measurement:
    procedures:
      - name: Pressure Sweep Spectroscopy
        outline: |
          Systematically vary the ambient Temporal Pressure `Γ` around the system's expected optimum `Γ₀`. Measure a proxy for system instability or "cost," such as decoherence rate, energy dissipation, or spectral line broadening. Fit the resulting data to a parabola of the form `y = A(Γ - Γ₀)² + C`; `λ_Γ` is proportional to the fitted quadratic coefficient `A`.
        expected_signals: [Parabolic increase in decoherence rate away from Γ₀, Quadratic energy dissipation profile]
        pitfalls: [Confounding effects from the Manifold Shear (λ_c) coupling term if internal phase is not held constant or marginalized, Non-parabolic behavior far from Γ₀ where higher-order terms become significant]
context_windows:
  - module: DOMA-079
    excerpt: |
      Every resonance has an optimal medium. A system's internal pattern (`Ki`) is most stable within a specific ambient temporal pressure, its "sweet spot" `Γ₀`. Too little pressure (`Γ << Γ₀`) and the pattern dissolves; too much (`Γ >> Γ₀`) and it is crushed. The simplest invariant motif describing this is a parabolic basin: `∝ (Γ - Γ₀)²`. This ensures that existence is a negotiation with the environment, not a declaration against it.
  - module: DOMA-079
    excerpt: |
      By combining these invariant motifs under the architectural constraints of the Nomad's Grammar, we arrive at the minimal, symmetry-derived form for the Temporal Pressure manifold, `V_Γ`. [...] Each coefficient has a clear physical meaning and is experimentally measurable: `λ_Γ`: **Pressure Curvature.** How sensitive the system is to its environment.
poetic_connections:
  motifs: [brittleness, sensitivity, confinement, resonance, basin, stability]
  evocative_lines:
    - "A law is not a command; it is the shape of the riverbed that guides the water."
    - "What shape must a cello have to sing?"
  association_matrix:
    - [ "TEMPORAL_PRESSURE_Γ", 0.9 ]
    - [ "COHERENCE_MANIFOLD", 0.8 ]
    - [ "MANIFOLD_SHEAR_λ_c", 0.5 ]
formal_mappings:
  candidates:
    - target: Harmonic Oscillator Potential / Spring Constant `k`
      domain: CM
      mapping_kind: mathematical
      equation_hint: |
        V(x) = ½ kx²  ↔  V(δΓ) = λ_Γ (δΓ)²   (where δΓ = Γ - Γ₀)
      justification: |
        Pressure Curvature `λ_Γ` is mathematically analogous to a spring constant `k`. It defines a quadratic potential well that creates a linear restoring force `-2λ_Γ(Γ - Γ₀)`, pulling the system back towards its equilibrium state `Γ₀`. In this mapping, "displacement" from equilibrium is the deviation from optimal temporal pressure.
      references:
        - title: "Classical Mechanics"
          where: "Chapter on Simple Harmonic Motion"
          date:
      confidence: 0.85
  adopted:
    - target:
      rationale:
      confidence: 0.0
constraints_and_falsifiers:
  claims:
    - statement: "For a given system class, `λ_Γ` is a constant that is independent of the system's internal phase state `φ_ij`."
      domain: experiment
      falsifier: "Experimental evidence shows that `λ_Γ` systematically changes as the system is forced into different phase-locked states, implying a higher-order coupling term beyond the `V_couple` defined in `DOMA-079`."
      status: proposed
      links: [DOMA-079]
naming_notes:
  collisions: [The symbol `λ` is heavily overloaded in physics (e.g., wavelength, eigenvalue). Context via the subscript `Γ` is crucial for disambiguation.]
  disambiguation: |
    `Pressure Curvature` (λ_Γ) defines the *shape* of the environmental potential well. It should not be confused with `Temporal Pressure` (Γ) itself, which is the environmental coordinate that the system is sensitive to.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [TEMPORAL_PRESSURE_Γ, TEMPORAL_PRESSURE_POTENTIAL_V_Γ]
  downstream_effects: [PIROUETTE_LAGRANGIAN]
license: CC-BY-SA-4.0
---