---
term: "One-Shot Anchoring"
canonical_id: "ONE_SHOT_ANCHORING"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-018"]
---

---
term: One-Shot Anchoring
canonical_id: ONE_SHOT_ANCHORING
symbol: N/A
aliases: []
parents: [MATH-018]
children: [MATH-019]
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-018
      lines: "D3"
      snippet: |
        Exactly one anchor is permitted to set a single global scale (e.g., electron a_e). After this operation, **all** U, T are frozen. No re‑anchoring across observables or species.
  editors: [canonical-agent]
  review_log: []
triad:
  art: |
    A single pinprick of measurement anchors the entire tapestry of constants. This one act fixes the universe's measure, freezing the pattern for all subsequent predictions.
  law: |
    Exactly one universal constant may be fixed by a single empirical measurement to set the global scale. All other universal and topological constants are then frozen and must be used for prediction without further tuning.
  philosophy: |
    This rule enforces maximal predictivity by preventing post-hoc parameter tuning across different physical domains. By locking the framework's fundamental scales after a single measurement, it forces the theory's internal structure and symmetries to bear the full burden of explaining subsequent observations, making it maximally falsifiable.
pirouette_definition: |
  The procedural rule (MATH-018: D3) that permits exactly one parameter from the Universal class (U) to be fixed by a single empirical measurement. This action, called 'anchoring', sets the global physical scale for the entire framework. Immediately following this operation, all other parameters in classes U and T (Portal/topology indices) are frozen and become fixed constants for all subsequent out-of-sample predictions. Re-anchoring against different observables or particle species is forbidden.
operational_definition:
  units: Dimensionless (it is a procedural rule).
  symbol_table:
    - name: N/A
      meaning: This is a procedural rule, not a physical quantity.
      dimensions: N/A
      default_range: N/A
  measurement:
    procedures:
      - name: Freeze Protocol Execution
        outline: |
          1. Select a single, high-precision observable (e.g., electron anomalous magnetic moment, a_e).
          2. Choose the corresponding universal constant (u_k) to be the anchor.
          3. Adjust u_k until the model's prediction for the chosen observable matches its measured value.
          4. Freeze the value of u_k and all other U and T parameters.
          5. Generate and publish a signed Freeze Manifest containing the anchor choice, parameter values, and code commit hash.
        expected_signals: [A published 'Freeze Manifest' artifact, All subsequent out-of-sample predictions for other observables (e.g., a_μ, a_τ) are made without further parameter changes.]
        pitfalls: [Re-tuning parameters for a new observable after the initial anchor ('moving the goalposts')., Choosing an anchor observable with large or poorly-understood theoretical/experimental uncertainties.]
context_windows:
  - module: MATH-018
    excerpt: |
      Universal constants U = {u_k}: derivable from axioms/symmetries only; at most a single global scale may be anchored once (see D3). ... Exactly one anchor is permitted to set a single global scale (e.g., electron a_e). After this operation, all U, T are frozen. No re‑anchoring across observables or species.
  - module: MATH-018
    excerpt: |
      Perform the D3 one-shot anchor; freeze U, T; emit a signed “Freeze Manifest” (commit hash, timestamp). ... Calibrate on {a_μ} or {a_e} (but not both). Predict {a_e, a_τ, Δν_Mu, Δα_had(M_Z), d_e} strictly OOS.
poetic_connections:
  motifs: [anchoring, freezing, irrevocability, predictivity, falsifiability]
  evocative_lines:
    - "at most a single global scale may be anchored once"
    - "After this operation, all U, T are frozen."
  association_matrix:
    - [ "FREEZE_PROTOCOL", 0.9 ]
    - [ "PREDICTIVITY", 0.8 ]
    - [ "FALSIFIABILITY", 0.7 ]
formal_mappings:
  candidates:
    - target: Model Calibration / Scale Setting
      domain: EFT|Methodology
      mapping_kind: conceptual
      equation_hint: N/A
      justification: |
        This rule formalizes the common physics practice of using one precise measurement to fix a fundamental constant (e.g., fixing α from electron g−2) and then using that value to predict other phenomena. Pirouette elevates this to a strict, global, and single-use-only procedure to eliminate overfitting and ensure the model's predictive power is rigorously tested against out-of-sample data.
      references: []
      confidence: 0.95
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "Once a single universal parameter is anchored to an observable (e.g., a_e), the framework can predict a suite of other, distinct observables (e.g., a_μ, a_τ) to within their experimental uncertainties without any further parameter tuning."
      domain: phenomenology
      falsifier: "The out-of-sample predictions for other observables consistently disagree with experimental measurements beyond the stated uncertainty bounds, indicating the model's internal structure is incorrect or incomplete."
      status: proposed
      links: [MATH-018]
naming_notes:
  collisions: []
  disambiguation: |
    One-Shot Anchoring is a procedural rule, not a physical mechanism. It should be distinguished from 'calibration' or 'fitting', which often imply continuous, multi-parameter optimization against a large dataset. Anchoring is a single, discrete, and irrevocable act of scale-setting.
crosslinks:
  near_synonyms: []
  antonyms: [POST_HOC_TUNING, RECALIBRATION]
  prerequisites: [PARAMETER_CLASSES]
  downstream_effects: [FREEZE_PROTOCOL, CROSS_FAMILY_VALIDATION]
license: CC-BY-SA-4.0
---