---
term: "Anti-Numerology Reporting"
canonical_id: "ANTI_NUMEROLOGY_REPORTING"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-018"]
---

---
term: Anti-Numerology Reporting
canonical_id: ANTI_NUMEROLOGY_REPORTING
symbol: 
aliases: []
parents: [MATH-018]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-018
      lines: "D5"
      snippet: |
        D5 — Anti‑Numerology Reporting
        All papers must report AIC/BIC, Bayes factors, and ablations for: (A) full model, (B) no‑portal, (C) free‑fit powers. If (B) or (C) dominates, the simpler/worse‑falsifiable model is preferred.
  editors: [system]
  review_log: []
triad:
  art: |
    A vow of parsimony, demanding that any new complexity prove its worth against the silence of a null hypothesis or the brute force of a free fit. It is the framework's conscience, keeping theory honest by forcing it to confront its simpler, dumber cousins.
  law: |
    All model claims must be accompanied by information-theoretic statistics (AIC/BIC) comparing the full model against two specific foils: (1) a simpler model with key structures (e.g., portals) ablated, and (2) a less-constrained model where exponents are freely fit. If either foil is statistically preferred, the simpler or less falsifiable model must be adopted as the default.
  philosophy: |
    To ensure that the framework's predictive power arises from its core symmetries and topological structure, not from incidental parameter tuning or gratuitous complexity. This procedure acts as a filter, favoring falsifiable, parsimonious models over those that can be contorted to fit any dataset.
pirouette_definition: |
  A normative reporting requirement (MATH-018 D5) that mandates all publications present model comparison statistics, such as the Akaike Information Criterion (AIC), Bayesian Information Criterion (BIC), and Bayes factors. This comparison must be performed between the full Pirouette model and at least two specific alternative hypotheses: (A) a 'no-portal' ablation where topological interactions are set to their null value, and (B) a 'free-fit' alternative where exponents fixed by symmetry are allowed to vary as free parameters. The framework mandates a preference for the simpler or less-falsifiable model if it statistically dominates the full model, thereby penalizing unjustified complexity.
operational_definition:
  units: Dimensionless
  symbol_table:
    - name: AIC
      meaning: Akaike Information Criterion
      dimensions: dimensionless
      default_range: contextual
    - name: BIC
      meaning: Bayesian Information Criterion
      dimensions: dimensionless
      default_range: contextual
    - name: ℒ_max
      meaning: Maximized value of the likelihood function
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: k
      meaning: Number of estimated parameters in the model
      dimensions: dimensionless
      default_range: contextual
    - name: n
      meaning: Number of data points
      dimensions: dimensionless
      default_range: contextual
  measurement:
    procedures:
      - name: Comparative Model Selection
        outline: |
          1. Define and fit the full Pirouette model (Model P) to the data.
          2. Define and fit a 'no-portal' ablation (Model A) by setting portal/topology indices `T` to their null equivalent.
          3. Define and fit a 'free-fit' model (Model B) by replacing symmetry-fixed exponents (from D2) with free continuous parameters.
          4. For each model, calculate `AIC = 2k - 2ln(ℒ_max)` and `BIC = k ln(n) - 2ln(ℒ_max)`.
          5. Publish a table of these statistics. If `AIC(A) < AIC(P)` or `AIC(B) < AIC(P)` (similarly for BIC), the claim for Model P is provisionally rejected.
        expected_signals: [A lower AIC/BIC score for the full Pirouette model relative to both alternatives, indicating the model's structure is justified.]
        pitfalls: [Miscounting the number of effective parameters (k), Using an inappropriate likelihood function for the data, Over-interpreting small differences in AIC/BIC scores (e.g., ΔAIC < 2).]
context_windows:
  - module: MATH-018
    excerpt: |
      Lock in Pirouette’s predictive status by replacing any post‑hoc calibration or ad‑hoc functional choices with symmetry‑fixed structure, preregistered forecasts, and reproducible validation... All papers must report AIC/BIC, Bayes factors, and ablations for: (A) full model, (B) no‑portal, (C) free‑fit powers. If (B) or (C) dominates, the simpler/worse‑falsifiable model is preferred.
poetic_connections:
  motifs: [parsimony, falsifiability, honesty, Occam's razor, model selection]
  evocative_lines:
    - "If (B) or (C) dominates, the simpler/worse‑falsifiable model is preferred."
  association_matrix:
    - [ "SYMMETRY_FIXED_FUNCTIONAL_FORMS", 0.8 ]
    - [ "PREREGISTRATION_DOCKET", 0.7 ]
    - [ "FALSIFIABILITY", 0.9 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Model selection via Information Criteria (AIC/BIC)
      domain: Statistics
      mapping_kind: operational
      equation_hint: |
        AIC = 2k - 2ln(ℒ_max)
      justification: |
        The procedure is a direct application of standard information-theoretic model selection criteria, established by Akaike and Schwarz, to penalize model complexity. The definition in MATH-018 D5 explicitly names AIC and BIC, making this a direct, non-analogical use of established statistical methods to operationalize Occam's Razor.
      references:
        - title: "A new look at the statistical model identification"
          where: "IEEE Transactions on Automatic Control. 19 (6): 716–723"
          date: 1974-12-01
        - title: "Estimating the dimension of a model"
          where: "Annals of Statistics. 6 (2): 461–464"
          date: 1978-03-01
      rationale: The definition in MATH-018 D5 explicitly names AIC and BIC, making this a direct, non-analogical use of established statistical methods.
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "The inclusion of Pirouette's symmetry-fixed structures (e.g., portal terms) provides a more parsimonious explanation of observational data than simpler null models or more complex free-fitting models."
      domain: phenomenology
      falsifier: "A persistent outcome where either the no-portal model or the free-fit model consistently achieves a significantly lower AIC/BIC score across multiple, independent preregistered tests (P4)."
      status: under-test
      links: [MATH-018]
naming_notes:
  collisions: []
  disambiguation: |
    This is not a prohibition on complex models, but a requirement to *justify* that complexity with evidence. It is distinct from simple goodness-of-fit tests (e.g., χ²) which do not penalize for additional parameters. The term 'anti-numerology' refers to the practice of avoiding parameter sets that are fine-tuned to fit data without a deeper theoretical principle.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [SYMMETRY_FIXED_FUNCTIONAL_FORMS]
  downstream_effects: []
license: CC-BY-SA-4.0
---

# Anti-Numerology Reporting

## Canonical (Pirouette)
A normative reporting requirement (MATH-018 D5) that mandates all publications present model comparison statistics, such as the Akaike Information Criterion (AIC), Bayesian Information Criterion (BIC), and Bayes factors. This comparison must be performed between the full Pirouette model and at least two specific alternative hypotheses: (A) a 'no-portal' ablation where topological interactions are set to their null value, and (B) a 'free-fit' alternative where exponents fixed by symmetry are allowed to vary as free parameters. The framework mandates a preference for the simpler or less-falsifiable model if it statistically dominates the full model, thereby penalizing unjustified complexity.

## EFT-First Summary
This is the Pirouette framework's internal implementation of standard statistical model selection. Using information criteria like AIC and BIC, it ensures that any proposed new structure (e.g., portal couplings) provides more explanatory power per parameter than a simpler null model or a more flexible, less constrained phenomenological fit. This procedure is directly analogous to comparing different EFTs by their predictive power, penalizing the addition of unnecessary operators or those without strong theoretical motivation.

## Glossary Links
- See also: `SYMMETRY_FIXED_FUNCTIONAL_FORMS`, `PREREGISTRATION_DOCKET`