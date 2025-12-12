---
term: "Preregistered Prediction Docket"
canonical_id: "PREREGISTERED_PREDICTION_DOCKET"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-018"]
---

---
term: Preregistered Prediction Docket
canonical_id: PREREGISTERED_PREDICTION_DOCKET
symbol: N/A
aliases: [preregistration docket, prediction docket]
parents: [MATH-018]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-018
      lines: "P4"
      snippet: |
        P4 — Preregistered Prediction Docket (min contents)
        • Targets: tau g−2; muonium hyperfine shift; running α(M_Z) correction; electron EDM sign & order; one hadron‑insulating ratio (D8).
        • Methods: solver choice, tolerance, priors, sampling plan.
        • Code: repository URL + commit + environment lockfile; random seeds.
        • Uncertainty: propagate from U, T; state 68%/95% bands.
  editors: [Pirouette Framework AI]
  review_log: []
triad:
  art: |
    A vow made to the future, a sealed letter sent to oneself before the battle. It binds the theorist to their predictions, turning the chaotic art of discovery into a disciplined act of falsifiable science.
  law: |
    Before evaluating a model on new data, a public docket must be published containing immutable code hashes, locked parameters from the Freeze Manifest, and specific, quantitative out-of-sample targets. The model's success is judged solely against these preregistered predictions.
  philosophy: |
    To enforce intellectual honesty and predictive power over post-hoc rationalization. By freezing the model's state *before* seeing the outcome, the docket separates genuine prediction from flexible fitting, ensuring Pirouette's claims are rigorously testable.
pirouette_definition: |
  A version-controlled, time-stamped, and public document that freezes the complete predictive state of a Pirouette model prior to an out-of-sample evaluation. It serves as an immutable contract for falsification. The docket must contain: (1) a precise list of quantitative OOS targets; (2) a complete description of methods, including solver choices, priors, and sampling plans; (3) verifiable and reproducible code via a repository URL, commit hash, environment lockfile, and random seeds; and (4) the specified procedure for propagating and reporting uncertainty.
operational_definition:
  units: N/A (document)
  symbol_table:
    - name: N/A
      meaning: This is a procedural artifact, not a physical quantity.
      dimensions: N/A
      default_range: N/A
  measurement:
    procedures:
      - name: Docket Compliance Verification
        outline: |
          1. Retrieve the public docket and verify its publication timestamp precedes the release of the target data.
          2. Clone the specified code repository at the given commit hash.
          3. Re-create the computational environment using the provided lockfile.
          4. Execute the analysis with the specified seeds and inputs.
          5. Confirm that the generated predictions and uncertainty bands bit-for-bit match those published in the docket.
        expected_signals: [A fully reproducible forecast that matches the docket's claims, A passing P5 checklist in the associated module.]
        pitfalls: [Code rot (unreproducible environment), Ambiguous target definitions (e.g., unspecified experimental inputs), Data leakage (use of target data before the docket's publication date).]
context_windows:
  - module: MATH-018
    excerpt: |
      D4 — Preregistration & Out‑of‑Sample Tests
      Before evaluation, publish a docket (see P4) with code hash, seeds, priors, and locked targets. Results are scored strictly out‑of‑sample.
  - module: MATH-018
    excerpt: |
      APPENDIX B — Template Artifacts
      • Freeze Manifest (YAML): commit, anchor choice, U/T values, seeds.
      • Prereg Docket (Markdown): targets, priors, solver tolerances, uncertainty recipe.
      • Ratio Test Sheet: list of admissible hadron‑insulating ratios with derivations.
poetic_connections:
  motifs: [binding, falsification, honesty, sealed-letter, contract]
  evocative_lines:
    - "Lock in Pirouette’s predictive status..."
    - "Results are scored strictly out‑of‑sample."
  association_matrix:
    - [ "FREEZE_MANIFEST", 0.9 ]
    - [ "ANTI_NUMEROLOGY_REPORTING", 0.7 ]
    - [ "ONE_SHOT_ANCHORING_RULE", 0.6 ]
formal_mappings:
  candidates:
    - target: Preregistration
      domain: Methodology
      mapping_kind: operational
      equation_hint: N/A
      justification: |
        The Preregistered Prediction Docket is a direct, formalized application of the scientific preregistration paradigm, widely used in clinical trials and psychology. It serves the identical purpose: to prevent p-hacking and HARKing (Hypothesizing After the Results are Known) by forcing a commitment to the analysis plan and predictions before the data are observed.
      references:
        - title: The Preregistration Revolution
          where: PNAS 115 (11) 2600-2606
          date: 2018-03-13
      confidence: 0.95
  adopted:
    - target: Scientific Preregistration
      rationale: The term and procedure are a direct import of the preregistration concept from the open science movement into theoretical physics, serving the identical purpose of enforcing predictive, falsifiable claims over post-hoc accommodation.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "Adherence to the Preregistered Prediction Docket protocol prevents post-hoc tuning of model parameters or functional forms to fit new out-of-sample data."
      domain: methodology
      falsifier: "Discovery of a published Pirouette result where the analysis code's commit hash does not match the preregistered docket, or where the docket was published after the release date of the data it claims to predict."
      status: proposed
      links: [MATH-018]
naming_notes:
  collisions: ["docket" is a common term in legal systems, but context prevents ambiguity.]
  disambiguation: |
    Distinguish from the `Freeze Manifest`, which is a machine-readable artifact listing frozen parameters *before* a prediction campaign. The Docket is a human-readable document that *consumes* the manifest and adds specific predictive targets, methods, and code pointers for a full, reproducible forecast.
crosslinks:
  near_synonyms: []
  antonyms: [POST_HOC_CALIBRATION, FREE_FIT_POWERS]
  prerequisites: [FREEZE_MANIFEST, ONE_SHOT_ANCHORING_RULE]
  downstream_effects: [ANTI_NUMEROLOGY_REPORTING]
license: CC-BY-SA-4.0
---