---
term: "Nuisance parameters"
canonical_id: "NUISANCE_PARAMETERS"
symbol: "N"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-018"]
---

---
term: Nuisance parameters
canonical_id: NUISANCE_PARAMETERS
symbol: N
aliases: []
parents: [MATH-018]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-018
      lines: "D1"
      snippet: |
        • Nuisance parameters N = {n_m}: experimental or environmental; may be taken from external literature but **never tuned** to improve fit.
  editors: [pirouette-doc-agent]
  review_log: []
triad:
  art: |
    The grit in the oyster; the fixed, unyielding constants of the outside world that the theory must accommodate without alteration. They are the rigid, non-negotiable scaffold for genuine prediction.
  law: |
    Nuisance parameters (N) are imported from external, independent measurements and are **never** used as free parameters in a fit to improve a model's agreement with data. Their values and uncertainties are propagated, not optimized.
  philosophy: |
    To maintain predictive integrity, the framework strictly separates theoretical parameters (U, T) from experimental inputs (N). This enforced separation prevents the absorption of theoretical failures into pliable 'nuisance' knobs, ensuring that disagreement with data is a genuine signal of falsification, not a failure of tuning.
pirouette_definition: |
  In the Pirouette Framework, Nuisance parameters (N) are a class of input variables representing quantities determined by experimental context, environmental conditions, or external measurements (e.g., beam energy, detector efficiencies, or literature values for certain constants not derived from the core theory). They are distinct from Universal constants (U) and Portal indices (T). Per `MATH-018:D1`, nuisance parameters are treated as fixed inputs with associated uncertainties; they are **prohibited** from being tuned, fitted, or otherwise adjusted to improve a model's goodness-of-fit for a given observable.
operational_definition:
  units: Contextual (depends on the specific parameter)
  symbol_table:
    - name: N
      meaning: The set of all nuisance parameters, {n_m}.
      dimensions: Contextual
      default_range: Contextual
    - name: n_m
      meaning: An individual nuisance parameter.
      dimensions: Contextual
      default_range: Contextual
  measurement:
    procedures:
      - name: External Value Import & Propagation
        outline: |
          1. Identify an experimental or environmental input `n_m` required for a calculation.
          2. Locate the best available measurement of `n_m` from an external source (e.g., a Particle Data Group review, a dedicated experimental paper).
          3. Record the central value and uncertainty for `n_m` and list it in the module's parameter table with `Class=N` and `Status=external`.
          4. Propagate this value and its uncertainty through the Pirouette calculation without any modification or fitting.
        expected_signals:
          - A quantified sensitivity of the final prediction to the uncertainty of `n_m`.
        pitfalls:
          - Using a stale or superseded literature value.
          - Incorrectly propagating asymmetric uncertainties.
          - Subtly 'tuning' by choosing a favorable value from multiple conflicting external measurements.
context_windows:
  - module: MATH-018
    excerpt: |
      D1 — Parameter Classes and Allowable Operations
      • Universal constants U = {u_k}: derivable from axioms/symmetries only...
      • Portal/topology indices T = {t_j}: integer or signed indices attached to spinorial/topological class...
      • Nuisance parameters N = {n_m}: experimental or environmental; may be taken from external literature but **never tuned** to improve fit.
  - module: MATH-018
    excerpt: |
      Minimal Edits Required Elsewhere...
      Parameter tables: add columns {Class ∈ {U,T,N}, Status ∈ {derived/anchored/external}, Source}.
poetic_connections:
  motifs: [fixed-inputs, external-truth, scaffold, non-negotiable, environmental-imprint]
  evocative_lines:
    - "...may be taken from external literature but **never tuned** to improve fit."
    - "Lock in Pirouette’s predictive status..."
  association_matrix:
    - [ "ONE_SHOT_ANCHORING", 0.7 ]
    - [ "FREEZE_PROTOCOL", 0.8 ]
    - [ "UNIVERSAL_CONSTANTS", 0.3 ]
formal_mappings:
  candidates:
    []
  adopted:
    - target: Nuisance parameter (Statistics/HEP)
      domain: Statistics|HEP
      mapping_kind: conceptual
      equation_hint: |
        L(θ, ν), where θ are parameters of interest and ν are nuisance parameters. In Pirouette, ∂L/∂ν is never used for optimization.
      justification: |
        Pirouette adopts the term directly from its common usage in statistics and High Energy Physics, where it refers to parameters necessary for a model but not of primary interest. However, Pirouette applies a stricter, normative constraint: these parameters cannot be marginalized over or fitted. They must be imported as fixed external priors with uncertainty.
      references:
        - title: Review of Particle Physics
          where: Statistical Methods section
          date: 2024-08-01
      confidence: 1.0
      rationale: |
        The term is adopted directly from common scientific practice but is sharpened by the `MATH-018:D1` non-tuning constraint, which is a core guardrail of the Pirouette Framework.
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "A parameter classified as a Nuisance Parameter (N) is never optimized, fitted, or tuned in any Pirouette-compliant analysis."
      domain: phenomenology
      falsifier: "Discovering a Pirouette-compliant publication or module where a parameter labeled 'N' is varied to minimize a χ² or maximize a likelihood against target data. This would violate `MATH-018:D1`."
      status: proposed
      links: [MATH-018]
naming_notes:
  collisions: [The symbol N is common (e.g., for number of particles, Neutrons). Context (e.g., the parameter set N = {n_m}) is required for disambiguation.]
  disambiguation: |
    Unlike in some statistical contexts where nuisance parameters are integrated out (marginalized), in Pirouette they are treated as fixed inputs with propagated uncertainty. They are knobs that are measured externally and then locked, not dials to be turned during a fit.
crosslinks:
  near_synonyms: []
  antonyms: [UNIVERSAL_CONSTANTS, PORTAL_INDICES, FREE_PARAMETER]
  prerequisites: []
  downstream_effects: [FREEZE_PROTOCOL, PREREGISTERED_PREDICTION_DOCKET]
license: CC-BY-SA-4.0