---
term: "Propagating Force"
canonical_id: "PROPAGATING_FORCE"
symbol: ""
aliases: [Electromagnetism]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-001"]
---

---
term: Propagating Force
canonical_id: PROPAGATING_FORCE
symbol: Fₚ
aliases: [Electromagnetism]
parents: [MATH-001, CORE-006, CORE-007]
children: [MATH-002]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-001
      lines: "§4"
      snippet: |
        This proves that the electrostatic force is a direct consequence of a system seeking to minimize its potential in a coherence gradient.
  editors: [anthropic/claude-v3-sonnet]
  review_log: []
triad:
  art: |
    A ripple on the lake of coherence, spreading outward. It is the universe's long-distance call, the influence of a system's rhythm felt across the void. This force is the principle of reach.
  law: |
    The magnitude of the Propagating Force on a test system is proportional to the local gradient of the coherence manifold potential, Fₚ = -∇V. In the simple case of a static point source, this force decays with the square of the distance.
  philosophy: |
    Unlike the self-trapping Gladiator Force, the Propagating Force is the engine of communication and long-range order. It enables distinct systems to influence one another without being consumed, creating the possibility for complex, non-local structure.
pirouette_definition: |
  The component of the unified force derived from a simple, non-feedback-dominated gradient in the coherence manifold potential. It manifests as a restoring force compelling a system toward a state of minimal potential (maximal coherence) relative to an external source. Mathematically, it is the `Q * A * sin(phi)` term in the equation of motion derived from the Pirouette Lagrangian, which for small phase deviations approximates a `1/r²` inverse-square law.
operational_definition:
  units: Newtons (kg⋅m⋅s⁻²)
  symbol_table:
    - name: Fₚ
      meaning: Propagating Force
      dimensions: M L T⁻²
      default_range: contextual
    - name: V
      meaning: Coherence manifold potential
      dimensions: M L² T⁻²
      default_range: contextual
    - name: Q
      meaning: Charge (magnitude of coherence asymmetry)
      dimensions: dimensionless (in this derivation)
      default_range: contextual
    - name: φ
      meaning: System phase relative to potential
      dimensions: dimensionless
      default_range: [0, 2π]
  measurement:
    procedures:
      - name: Test Charge Coherence Oscillation
        outline: |
          Introduce a calibrated test system (with known charge `Q` and phase `φ`) into the field of a source. Measure the frequency and amplitude of the test system's phase oscillations. The restoring force Fₚ is inferred from the second time derivative of the phase, Fₚ ∝ d²φ/dt².
        expected_signals: [Sinusoidal phase oscillations `φ(t)`, force proportional to `sin(φ)`]
        pitfalls: [Isolating from Gladiator Force effects at short range, ensuring the test system doesn't significantly alter the source gradient]
context_windows:
  - module: MATH-001
    excerpt: |
      Let's model a static charge. As per CORE-007, a charge is an asymmetry that creates a gradient in the coherence manifold. This gradient is encoded in the potential V... We have thus derived the existence of a force from the gradient of the potential. For small oscillations, sin(phi) approx phi, and we recover a linear force law analogous to Coulomb's Law.
  - module: MATH-001
    excerpt: |
      This proves that the electrostatic force is a direct consequence of a system seeking to minimize its potential in a coherence gradient.
poetic_connections:
  motifs: [gradient, ripple, broadcast, influence, light, reach]
  evocative_lines:
    - "force is simply the geometry of the coherence manifold."
    - "This proves that the universe does not have a separate law for motion..."
  association_matrix:
    - [ "GLADIATOR_FORCE", -0.8 ]
    - [ "TEMPORAL_COHERENCE", 0.7 ]
    - [ "CHARGE", 0.9 ]
formal_mappings:
  candidates:
    - target: Electromagnetism (Coulomb Force)
      domain: CM
      mapping_kind: mathematical
      equation_hint: |
        Fₚ ∝ Q⋅A⋅sin(φ)  ↔  Fₑ = (k⋅q₁⋅q₂)/r²
      justification: |
        The derivation in MATH-001 explicitly recovers a force law analogous to Coulomb's Law by taking the gradient of a potential created by a source charge. The `Q⋅A` term maps to the product of charges and the coupling constant, while the geometric falloff of the potential gradient maps to the inverse-square relationship.
      references:
        - title: Physics for Scientists and Engineers
          where: Chapter on Electrostatics
          date: 2020-01-01
      confidence: 0.9
  adopted:
    - target: Electromagnetic Force
      rationale: The derivation in MATH-001 is constructed to demonstrate this equivalence. The Propagating Force is the Pirouette Framework's geometric origin story for the electromagnetic force.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The force between two static charges follows a pure inverse-square law at distances where Gladiator Force effects are negligible."
      domain: experiment
      falsifier: "Precise measurement showing a deviation from a pure `1/r²` force law in a vacuum that cannot be accounted for by known Standard Model corrections (e.g., vacuum polarization) or predicted Gladiator-force influence at short range."
      status: supported
      links: [MATH-001]
naming_notes:
  collisions: [The symbol `F` is generic for force; the subscript `p` is used for clarity.]
  disambiguation: |
    Distinguish from the Gladiator Force, which arises from self-referential feedback and dominates at small scales, leading to confinement. The Propagating Force is "leaky" and long-range; the Gladiator Force is self-binding.
crosslinks:
  near_synonyms: []
  antonyms: [GLADIATOR_FORCE]
  prerequisites: [PIROUETTE_LAGRANGIAN, TEMPORAL_COHERENCE, CHARGE]
  downstream_effects: []
license: CC-BY-SA-4.0
---