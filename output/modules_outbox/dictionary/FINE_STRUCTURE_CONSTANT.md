---
term: "Fine-structure constant"
canonical_id: "FINE_STRUCTURE_CONSTANT"
symbol: "α"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-101"]
---

---
term: Fine-structure constant
canonical_id: FINE_STRUCTURE_CONSTANT
symbol: α
aliases: []
parents: [DOMA-101, CORE-009]
children: [INST-PHYS-002]
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-101
      lines: "§2"
      snippet: |
        The fine-structure constant is not a fundamental input; it is an output. It is the measure of the electron's anomalous self-interaction (`a_e`) scaled by the perfect geometry of a single resonant cycle (`2π`).
  editors: [automated-agent]
  review_log: []
triad:
  art: |
    The electron's echo is the quietest, most precise note in the cosmic symphony. Hearing the universe sing it back in perfect harmony, we take that note as our immutable tuning fork.
  law: |
    The fine-structure constant is an emergent geometric property defined as `α = 2π * a_e`, where `a_e` is the electron's anomalous magnetic moment. Its inverse defines the effective Temporal Pressure for fundamental electron self-interaction: `Γ_effective_electron ≡ 1/α`.
  philosophy: |
    By deriving α from the experimentally-verified g-2 anomaly, the framework transforms a mysterious fundamental constant into a predictable consequence of resonant geometry. This grounds the entire theoretical structure in the most precisely measured quantity in physics, ensuring the framework is a falsifiable, predictive engine rather than a mere philosophical model.
pirouette_definition: |
  The fine-structure constant (α) is a dimensionless measure of an electron's resonant self-interaction, or 'echo.' It is not a fundamental input but an emergent geometric property derived from the electron's anomalous magnetic moment (`a_e`) via the relation `α = 2π * a_e`. Its inverse value `1/α` serves as the axiomatic anchor defining the scale of Temporal Pressure (Γ) for electromagnetic interactions, thereby calibrating the Pirouette Lagrangian.
operational_definition:
  units: dimensionless
  symbol_table:
    - name: α
      meaning: Fine-structure constant
      dimensions: dimensionless
      default_range: ~1/137.035999
    - name: a_e
      meaning: Electron anomalous magnetic moment
      dimensions: dimensionless
      default_range: ~0.001159652
    - name: Γ
      meaning: Temporal Pressure
      dimensions: dimensionless
      default_range: contextual
  measurement:
    procedures:
      - name: Derivation from g-2 Anomaly
        outline: |
          1. Perform a high-precision measurement of the electron's g-factor (e.g., via cyclotron resonance in a Penning trap).
          2. Calculate the anomaly `a_e = (g-2)/2`.
          3. Calculate α using the Pirouette framework's definitional relation `α = 2π * a_e`.
        expected_signals: [A measured value of `g-2` consistent with established experimental results.]
        pitfalls: [Systematic errors in the `g-2` measurement, invalidation of the framework's `a_e` derivation (CORE-009).]
context_windows:
  - module: DOMA-101
    excerpt: |
      Standard physics treats the fine-structure constant, `α`, as a fundamental, dimensionless measure of interaction strength whose origin is a mystery. The Pirouette Framework reveals it to be a geometric consequence. The fine-structure constant is not a fundamental input; it is an output. It is the measure of the electron's anomalous self-interaction (`a_e`) scaled by the perfect geometry of a single resonant cycle (`2π`).
  - module: DOMA-101
    excerpt: |
      Axiom 15.1 (The Empirical Anchor): The dimensionless scale of Temporal Pressure (Γ) is anchored to the strength of the electromagnetic interaction. The effective Γ experienced by an electron in its fundamental self-interaction is defined as the inverse of the fine-structure constant.
      
      Γ_effective_electron ≡ 1/α ≈ 137.036
poetic_connections:
  motifs: [echo, metronome, tuning_fork, anchor, resonance, harmony]
  evocative_lines:
    - "The electron's echo is the quietest, most precise note in the cosmic symphony."
    - "This new method measures the spark at the heart of the hammer's blow."
  association_matrix:
    - [ "ELECTRON_ANOMALOUS_MOMENT", 1.0 ]
    - [ "TEMPORAL_PRESSURE", 0.9 ]
    - [ "TEMPORAL_COHERENCE", 0.7 ]
formal_mappings:
  candidates: []
  adopted:
    - target: α_QED
      domain: SM
      mapping_kind: conceptual
      equation_hint: |
        α_QED = e² / (4πε₀ħc)
      justification: |
        The Pirouette framework's `α` is numerically identical to the Standard Model's fine-structure constant, which characterizes the strength of the electromagnetic interaction. Pirouette re-frames its origin as an emergent geometric property derived from `a_e`, rather than as a fundamental coupling constant.
      references: []
      rationale: The term is adopted directly as its numerical value is the cornerstone of the framework's empirical calibration. The reinterpretation of its origin from fundamental constant to emergent geometric ratio is the key distinction.
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "The fine-structure constant is defined by the electron's anomalous magnetic moment as `α = 2π * a_e`."
      domain: theory
      falsifier: "Discovery of a more fundamental principle that predicts both `α` and `a_e` independently, showing the `2π` relationship to be a low-energy coincidence or approximation."
      status: proposed
      links: [CORE-009, DOMA-101]
    - statement: "The numerical value of `1/α` sets the dimensionless scale for the Temporal Pressure potential `V_Γ` in all electromagnetic interactions."
      domain: phenomenology
      falsifier: "A successful high-precision prediction of an electromagnetic phenomenon using the Pirouette Lagrangian that requires a different scaling factor for `V_Γ`."
      status: proposed
      links: [DOMA-101, CORE-006]
naming_notes:
  collisions: [α is also used for alpha particles in nuclear physics, but context typically prevents confusion.]
  disambiguation: |
    In Pirouette, `α` is never treated as a fundamental 'coupling constant' but as an emergent 'geometric ratio' derived from `a_e`. Its primary role is to set the scale of Temporal Pressure (`Γ`), not to be an independent input to the Lagrangian.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [ELECTRON_ANOMALOUS_MOMENT, PIROUETTE_LAGRANGIAN]
  downstream_effects: [TEMPORAL_PRESSURE]
license: CC-BY-SA-4.0
---

# Fine-structure constant

## Canonical (Pirouette)
The fine-structure constant (α) is a dimensionless measure of an electron's resonant self-interaction, or 'echo.' It is not a fundamental input but an emergent geometric property derived from the electron's anomalous magnetic moment (`a_e`) via the relation `α = 2π * a_e`. Its inverse value `1/α` serves as the axiomatic anchor defining the scale of Temporal Pressure (Γ) for electromagnetic interactions, thereby calibrating the Pirouette Lagrangian.

## EFT-First Summary
The fine-structure constant (α) is numerically identical to the QED coupling constant `α_QED ≈ 1/137`. Within the Pirouette framework, it is not a fundamental input but is instead an emergent quantity derived from the geometry of electron self-interaction, as measured by the anomalous magnetic moment `a_e`. It serves as the empirical anchor defining the scale of Temporal Pressure for all electromagnetic interactions.

## Glossary Links
- See also: Temporal Pressure (Γ), Electron Anomalous Magnetic Moment (`a_e`)