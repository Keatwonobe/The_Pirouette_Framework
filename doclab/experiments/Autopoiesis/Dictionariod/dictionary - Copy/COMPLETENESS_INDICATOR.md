---
term: "Completeness indicator"
canonical_id: "COMPLETENESS_INDICATOR"
symbol: "𝒞_proj"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-PHI-001"]
---

---
term: Completeness indicator
canonical_id: COMPLETENESS_INDICATOR
symbol: 𝒞_proj
aliases: []
parents: [MATH-PHI-001]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-PHI-001
      lines: "L102-L108"
      snippet: |
        **Completeness indicator (project level):**
        \[
        \mathcal{C}_\mathrm{proj} = \frac{\sum_{\text{targets}} \mathbf{1}\{\mathrm{RPA} \ge \tau\}}{\#\text{targets}},
        \]
        with default threshold \( \tau \) set by the median of historical “wins” (e.g., when GR+YM derivations achieved new XXP hits).
  editors: [lexicon-agent-alpha]
  review_log: []
triad:
  art: |
    A gauge on the project's dashboard measuring the sufficiency of its maps. It signals when the toolbox of laws is sharp enough for the current territory, or if the search for new wrenches must continue.
  law: |
    The completeness indicator 𝒞_proj is the fraction of a project's target phenomena for which the currently adopted stabilizer grammar achieves a Reverse Pareto Analysis (RPA) score greater than or equal to a historically calibrated threshold τ.
  philosophy: |
    To prevent the infinite regress of mathematical exploration, 𝒞_proj provides a pragmatic stopping condition. It signals when an axiomatic base has saturated its explanatory power for a given problem set, focusing effort on empirical validation over further abstraction.
pirouette_definition: |
  A project-level metric that quantifies the functional sufficiency of the current stabilizer grammar for a defined set of target phenomena. It is the fraction of targets whose derivations meet or exceed a benchmark Reverse Pareto Analysis (RPA) score, τ, which is set by the median performance of historically successful theoretical advances. Formally:
  
  $$ \mathcal{C}_\mathrm{proj} = \frac{\sum_{\text{targets}} \mathbf{1}\{\mathrm{RPA} \ge \tau\}}{\#\text{targets}} $$
  
  A value of 𝒞_proj approaching 1 indicates that adding more mathematical machinery is likely to yield diminishing returns for the current project scope.
operational_definition:
  units: Dimensionless ratio
  symbol_table:
    - name: 𝒞_proj
      meaning: Project-level completeness indicator
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: RPA
      meaning: Reverse Pareto Analysis score
      dimensions: dimensionless (consequences/bits)
      default_range: contextual
    - name: τ
      meaning: RPA threshold for deeming a derivation "sufficient"
      dimensions: dimensionless
      default_range: calibrated from `/analysis/math_adhesion/ledger.csv`
    - name: "1{...}"
      meaning: Indicator function (1 if condition is true, 0 if false)
      dimensions: dimensionless
      default_range: "{0, 1}"
  measurement:
    procedures:
      - name: Calculate project completeness
        outline: |
          1. Enumerate the project's current set of "target phenomena" (e.g., GR hydrolimit, YM emergence).
          2. For each target, identify the set of derivations and the stabilizer grammar (axioms, mathematical domains) used.
          3. For each derivation set, compute its RPA score by maximizing the ratio of verified consequences to description length (M(k)/L(k)).
          4. Retrieve the benchmark threshold τ from the historical ledger of "wins".
          5. Count the number of targets where RPA ≥ τ.
          6. Divide this count by the total number of targets to find 𝒞_proj.
        expected_signals: ["A rising 𝒞_proj value over project milestones", "A value near 1.0 signaling a pivot from theoretical development to focused empirical validation."]
        pitfalls: ["Mis-calibrating the threshold τ (too high prevents progress, too low encourages premature closure)", "Inconsistent measurement of description length (L(k)) across different formalisms", "Poorly scoped 'target phenomena' list."]
context_windows:
  - module: MATH-PHI-001
    excerpt: |
      **Completeness indicator (project level):**
      \[
      \mathcal{C}_\mathrm{proj} = \frac{\sum_{\text{targets}} \mathbf{1}\{\mathrm{RPA} \ge \tau\}}{\#\text{targets}},
      \]
      with default threshold \( \tau \) set by the median of historical “wins” (e.g., when GR+YM derivations achieved new XXP hits).
      
      **Reading it.** When \(\mathcal{C}_\mathrm{proj}\to 1\), we’re close to *functional completeness* for our present scope; adding more math yields diminishing returns unless it opens *new* falsifiables.
poetic_connections:
  motifs: [diminishing returns, map vs. territory, tool-making, good-enough]
  evocative_lines:
    - "Most math is a net. The sticky math is the mesh that the loom itself uses."
    - "We invent nets. The loom keeps only what catches its threads with less and less mesh."
  association_matrix:
    - [ "REVERSE_PARETO_ANALYSIS", 0.9 ]
    - [ "STABILIZER_GRAMMAR", 0.7 ]
    - [ "STICKINESS", 0.5 ]
formal_mappings:
  candidates:
    - target: Model Adequacy
      domain: Philosophy of Science
      mapping_kind: conceptual
      justification: |
        Both concepts address when a theoretical framework is "good enough" to describe a set of empirical facts, without claiming it is a final, absolute truth. 𝒞_proj operationalizes this philosophical notion into a computable metric.
      confidence: 0.7
  adopted:
    - target: Akaike/Bayesian Information Criterion (AIC/BIC)
      domain: Statistics/Info Theory
      mapping_kind: conceptual
      equation_hint: |
        RPA ∝ M(k) / L(k)  vs.  AIC ∝ k - ln(L)
      rationale: |
        Like AIC/BIC, 𝒞_proj (via its core component RPA) provides a principled trade-off between model complexity and explanatory power. RPA's `L(k)` term is analogous to the complexity penalty (number of parameters `k` or description length) and `M(k)` is analogous to the model's likelihood or fit to data. 𝒞_proj is a project-level aggregate of this model selection principle.
      confidence: 0.8
constraints_and_falsifiers:
  claims:
    - statement: "A project with 𝒞_proj approaching 1.0 will yield diminishing returns from the addition of new mathematical formalisms to its stabilizer grammar."
      domain: phenomenology
      falsifier: "A project with 𝒞_proj ≈ 1.0 consistently generates novel, high-leverage predictions by grafting small, new mathematical structures, showing that the RPA metric failed to capture true predictive potential."
      status: proposed
      links: [MATH-PHI-001]
    - statement: "The historical RPA threshold τ is a stable parameter for a given research paradigm (e.g., for phenomena within the scope of SUBST-001 and DYNA-004)."
      domain: theory
      falsifier: "The value of τ required to signal 'completeness' fluctuates wildly between successfully closed sub-projects, indicating it is an unreliable, context-dependent benchmark rather than a stable parameter."
      status: proposed
      links: [MATH-PHI-001]
naming_notes:
  collisions: ["The symbol 𝒞 is overloaded (e.g., Capacitance, Curvature). The `proj` subscript is non-optional for clarity."]
  disambiguation: |
    This is a measure of *functional completeness* for a specific project scope, not logical completeness in the sense of Gödel. It does not claim the stabilizer grammar is the "one true math"; it claims the grammar is sufficient for the current set of problems.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [REVERSE_PARETO_ANALYSIS, STABILIZER_GRAMMAR]
  downstream_effects: []
license: CC-BY-SA-4.0
---