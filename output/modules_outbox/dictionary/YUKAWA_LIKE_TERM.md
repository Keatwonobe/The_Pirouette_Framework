---
term: "Yukawa-like term"
canonical_id: "YUKAWA_LIKE_TERM"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["XAP-001_properties_&_signatures_of_the_triaxial_fields"]
---

---
term: Yukawa-like term
canonical_id: YUKAWA_LIKE_TERM
symbol: αe⁻ʳ/λ
aliases: [Short-range gravity deviation, Γ-field signature]
parents: [XAP-001]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: XAP-001
      lines: "§3"
      snippet: |
        Hypothesis: The Γ-G Correspondence Principle predicts that the simple 1/r² force law is an approximation. At very short ranges (sub-millimeter), where the underlying field structure becomes more prominent, the force should deviate from pure Newtonian gravity. The potential should include a small, additional Yukawa-like term: V(r) = -G(m₁m₂/r) * (1 + αe⁻ʳ/λ)
  editors: [LLM Agent]
  review_log: []
triad:
  art: |
    A faint, short-lived echo of the Γ-field, clinging to mass before fading into the familiar Newtonian silence. It is the texture of spacetime, felt only at the closest range.
  law: |
    The gravitational potential V(r) between two masses at sub-millimeter scales includes a dimensionless modifier (1 + αe⁻ʳ/λ) to the Newtonian term, where α and λ are experimentally measurable constants representing the strength and range of the deviation. A null result from a torsion balance experiment constrains α and λ, potentially falsifying the model.
  philosophy: |
    This term is the crucial bridge from abstract theory to physical test. It makes the existence of the Γ-field a concrete, falsifiable question, transforming the concept of emergent gravity from a mathematical convenience into a hypothesis with a unique and detectable signature.
pirouette_definition: |
  A predicted, short-range, non-Newtonian modification to the gravitational potential, expressed as an exponential decay term αe⁻ʳ/λ that multiplies the standard Newtonian potential. It is proposed as an emergent effect of the Gladiator Force (Γ) field at sub-millimeter scales and serves as its primary falsifiable signature in high-precision experiments.
operational_definition:
  units: The full term (αe⁻ʳ/λ) is dimensionless.
  symbol_table:
    - name: α
      meaning: Strength parameter of the short-range interaction.
      dimensions: dimensionless
      default_range: |
        Experimentally constrained; << 1
    - name: λ
      meaning: Characteristic range of the short-range interaction.
      dimensions: L (Length)
      default_range: |
        < 1 mm
  measurement:
    procedures:
      - name: High-Precision Torsion Balance Measurement
        outline: |
          A sensitive torsion pendulum is placed near a rotating attractor mass with precisely machined features. A laser interferometer measures the pendulum's angular displacement, detecting the torque exerted by the attractor. The experiment is performed at cryogenic temperatures in a high vacuum to minimize noise.
        expected_signals:
          - A periodic torque on the pendulum that deviates from the value predicted by the inverse-square law.
          - The magnitude and harmonic content of this deviation will be a function of the geometry and separation, allowing for the determination of α and λ.
        pitfalls:
          - Casimir effect at very short distances.
          - Electrostatic patch potentials on the surfaces.
          - Thermal gradients and seismic noise.
context_windows:
  - module: XAP-001
    excerpt: |
      Hypothesis: The Γ-G Correspondence Principle predicts that the simple 1/r² force law is an approximation. At very short ranges (sub-millimeter), where the underlying field structure becomes more prominent, the force should deviate from pure Newtonian gravity. The potential should include a small, additional Yukawa-like term: V(r)=−G(m₁m₂/r) * (1+αe⁻ʳ/λ)
  - module: XAP-001
    excerpt: |
      Falsifiability: If, within the limits of experimental sensitivity, no deviation from the inverse-square law is detected, this would place strict constraints on the parameters (α,λ) of the Γ-field, potentially falsifying this specific model of its short-range behavior. The detection of such a deviation would provide powerful, direct evidence for the framework.
poetic_connections:
  motifs: [hidden signature, short-range force, falsifiable echo, deviation from ideal]
  evocative_lines:
    - "searching for its unique echo in the fabric of spacetime."
    - "The detection of such a deviation would provide powerful, direct evidence for the framework."
  association_matrix:
    - [ "GLADIATOR_FORCE", 0.9 ]
    - [ "EMERGENT_GRAVITY", 0.8 ]
    - [ "FALSIFIABLE_EXPERIMENT", 1.0 ]
formal_mappings:
  candidates:
    - target: Yukawa potential V(r) = -g²/4π * (e⁻ᵐʳ/r)
      domain: Particle Physics
      mapping_kind: mathematical
      equation_hint: |
        V_pirouette(r) ∝ (1/r) * (1 + αe⁻ʳ/λ)
      justification: |
        The term is explicitly modeled on the mathematical form of the Yukawa potential, which describes an interaction mediated by a massive scalar boson. In the Pirouette Framework, this term represents the short-range signature of the scalar Γ-field, with the range parameter λ corresponding to the effective mass of the field mediator (λ = ħ/mc).
      references:
        - title: An Introduction to Quantum Field Theory
          where: Chapter 4
          date: 1995-10-12
      confidence: 0.95
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The gravitational force between two masses at sub-millimeter scales deviates from the inverse-square law as described by a Yukawa-like modification to the potential."
      domain: experiment
      falsifier: "A null result from a high-sensitivity torsion balance experiment, which would place an upper bound on the strength parameter α that is inconsistent with theoretical predictions for the Γ-field."
      status: proposed
      links: [XAP-001]
naming_notes:
  collisions: [Yukawa potential]
  disambiguation: |
    The term "Yukawa potential" in standard physics typically describes the entire potential mediated by a massive particle (e.g., the strong nuclear force). In Pirouette, the "Yukawa-like term" refers specifically to a *correction factor* applied to the emergent Newtonian potential, not a new, independent fundamental force. It is a signature, not the source itself.
crosslinks:
  near_synonyms: []
  antonyms: [INVERSE_SQUARE_LAW]
  prerequisites: [GLADIATOR_FORCE, EMERGENT_GRAVITY]
  downstream_effects: []
license: CC-BY-SA-4.0
---