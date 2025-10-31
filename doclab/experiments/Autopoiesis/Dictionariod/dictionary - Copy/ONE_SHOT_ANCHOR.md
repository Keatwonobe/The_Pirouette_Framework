---
term: "One-Shot Anchor"
canonical_id: "ONE_SHOT_ANCHOR"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["COSMO-000"]
---

---
term: One-Shot Anchor
canonical_id: ONE_SHOT_ANCHOR
symbol: N/A
aliases: [Single-Measurement Calibration, D3 Anchoring]
parents: [MATH-018, COSMO-000]
children: [COSMO-Γ-HALO, COSMO-Γ-MERGE]
status: candidate
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: COSMO-000
      lines: "Section 3"
      snippet: |
        Anchor choice (pick exactly one per D3): {Ω_m0, H0, or a_e in QED sector with proven bridge}. Once chosen, derive U‑class parameter set {m_Γ, λ_4, …} via symmetry constraints and freeze.
  editors: [GPT-4]
  review_log: []
triad:
  art: |
    From a single keystone, the entire arch is set, its form immutable. All subsequent load-bearing is an unfolding of this initial commitment, not a refitting of stones.
  law: |
    All fundamental (U-class) parameters of a model must be uniquely determined by a single, preregistered experimental measurement (the anchor). Once fixed, these parameters are frozen and may not be re-tuned when comparing the model to any other out-of-sample data.
  philosophy: |
    To maximize falsifiability and prevent overfitting. This rule forces a theory to make maximally risky and specific predictions from minimal empirical input, shifting the burden of proof from post-hoc fitting to a priori prediction. It enforces a strict separation between model construction and model testing.
pirouette_definition: |
  A methodological constraint (D3) requiring a model's set of free, fundamental (U-class) parameters, `P_U`, to be uniquely determined by a single, well-defined, high-precision measurement, `O_anchor`. After this anchoring event, the parameters are permanently frozen and documented in a version-controlled Freeze Manifest. The model's validity is then tested against a battery of preregistered, out-of-sample predictions (P4) without further adjustment.
operational_definition:
  units: N/A (Methodological rule)
  symbol_table:
    - name: P_U
      meaning: The set of U-class (fundamental) free parameters of a model, e.g., `{m_Γ, λ_4}`.
      dimensions: contextual
      default_range: contextual
    - name: O_anchor
      meaning: The single, preregistered observable chosen for calibration.
      dimensions: contextual
      default_range: e.g., `H0`, `Ω_m0`
    - name: V_anchor
      meaning: The measured value of the anchor observable, with uncertainties.
      dimensions: contextual
      default_range: e.g., `67.4 ± 0.5 km/s/Mpc`
  measurement:
    procedures:
      - name: Model Anchoring and Freezing
        outline: |
          1. Preregister a single, high-precision observable `O_anchor` as the model's anchor.
          2. Establish the functional relationship `V_anchor = f(P_U)`.
          3. Analytically or numerically solve this system for the set of U-class parameters `P_U`. The solution must be unique.
          4. Record the resulting values of `P_U`, the anchor choice, and the software commit hash in a `Freeze Manifest` file.
          5. Use this frozen parameter set in all subsequent calculations and preregistered out-of-sample predictions (P4).
        expected_signals: [A unique, well-defined set of values for `P_U`, A generated `Freeze Manifest` (YAML)]
        pitfalls: [The chosen `O_anchor` lacks sufficient constraining power, leading to degenerate `P_U` solutions., The measurement `V_anchor` has large or poorly understood systematic errors., The function `f(P_U)` is non-invertible, yielding no unique solution.]
context_windows:
  - module: COSMO-000
    excerpt: |
      Anchor choice (pick exactly one per D3): {Ω_m0, H0, or a_e in QED sector with proven bridge}. Once chosen, derive U‑class parameter set {m_Γ, λ_4, …} via symmetry constraints and freeze. Emit a Freeze Manifest (YAML) with commit hash, anchor, U/T values, and seeds.
  - module: COSMO-000
    excerpt: |
      All functional choices obey MATH‑018 D2 (local, analytic, scale‑covariant), with one‑shot anchoring (D3) and preregistered, out‑of‑sample predictions (P4).
poetic_connections:
  motifs: [keystone, seed, immutability, first principles, baptism]
  evocative_lines:
    - "Once chosen, derive U-class parameter set … and freeze."
    - "Falsification conditions are met if any of the above require an extra fluid..."
  association_matrix:
    - [ "FREEZE_MANIFEST", 0.9 ]
    - [ "PREREGISTRATION_P4", 0.8 ]
    - [ "FALSIFIABILITY", 0.7 ]
    - [ "U_CLASS_PARAMETER", 0.9 ]
formal_mappings:
  candidates:
    - target: Popperian Falsification
      domain: Philosophy of Science
      mapping_kind: conceptual
      equation_hint: N/A
      justification: |
        The One-Shot Anchor rule is a direct implementation of the principle of falsifiability. By forbidding re-tuning after the initial calibration, it forces the model to make bold, specific, and risky predictions that can be decisively tested against new data, maximizing its exposure to refutation.
      references:
        - title: The Logic of Scientific Discovery
          where: Karl Popper
          date: 1934-01-01
      confidence: 0.9
  adopted:
    - target: Popperian Falsification
      rationale: This mapping best captures the methodological purpose (`telos`) of the rule within the Pirouette Framework, which prioritizes predictive power and testability over accommodating existing data.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "The One-Shot Anchor methodology reduces overfitting and researcher bias compared to multi-parameter posterior fitting."
      domain: phenomenology
      falsifier: "A rigorous model comparison (e.g., using Bayesian evidence) consistently shows that a one-shot anchored model is less predictive and more frequently disfavored than a traditionally fitted equivalent across multiple problem domains."
      status: proposed
      links: [COSMO-000]
    - statement: "For any D2-compliant theory, a unique U-class parameter set `P_U` can be derived from a single, well-chosen observable `O_anchor`."
      domain: theory
      falsifier: "Demonstrate a D2-compliant model where the function `f(P_U) = O_anchor` is non-injective for all viable anchor choices, leading to degenerate parameter solutions."
      status: proposed
      links: [MATH-018]
naming_notes:
  collisions: []
  disambiguation: |
    "One-Shot Anchor" should not be confused with "one-shot learning" in machine learning. This rule refers to a single *measurement event* used to permanently fix a physical theory's fundamental parameters, not to training a statistical model on a single data example. The "shot" is the measurement; the "anchor" is the resulting fixed-point in parameter space.
crosslinks:
  near_synonyms: [FREEZE_MANIFEST]
  antonyms: [PARAMETER_FITTING, FINE_TUNING]
  prerequisites: [U_CLASS_PARAMETER]
  downstream_effects: [PREREGISTRATION_P4]
license: CC-BY-SA-4.0
---