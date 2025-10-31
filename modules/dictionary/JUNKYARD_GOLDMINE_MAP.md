---
term: "Junkyard & Goldmine map"
canonical_id: "JUNKYARD_GOLDMINE_MAP"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-PHI-001"]
---

---
term: Junkyard & Goldmine map
canonical_id: JUNKYARD_GOLDMINE_MAP
symbol: (Stk, RPA)
aliases: [Domain Classification Map, Adhesion-Leverage Plot]
parents: [MATH-PHI-001]
children: [MATH-GR-001, MATH-YM-001, INFO-COH-001]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-PHI-001
      lines: "§5"
      snippet: |
        We bucket candidate domains by (expected) Stickiness × RPA. (“Goldmine” = high-high; “Junkyard” = low-low *for us*, not a value judgement.)
  editors: [p-engine-v3]
  review_log: []
triad:
  art: |
    We cast many nets of invented syntax into the ocean of possibility. This map tells us which ones catch the actual fish of physical law, and which are merely beautiful tapestries to hang on the wall.
  law: |
    Prioritize research and integration efforts on mathematical domains occupying the "Goldmine" quadrant (high Stickiness, high RPA score). A domain must have Stk ≥ 0.6 and RPA ≥ τ to be promoted to "pirouette" status via the framework's CI gate.
  philosophy: |
    The map is a tool for epistemic discipline. It forces a pragmatic evaluation of formalisms, steering focus away from purely aesthetic appeal towards structures that are verifiably load-bearing for describing our universe's stabilizer grammar.
pirouette_definition: |
  A 2D classification map that categorizes candidate mathematical domains into four quadrants based on their Stickiness (Stk) and Reverse Pareto Analysis (RPA) scores. The quadrants—Goldmine (high Stk, high RPA), Rising (medium Stk, high potential RPA), Utility Belt (high Stk, modest RPA), and Junkyard (low Stk, low RPA)—guide research priority by identifying formalisms that are both physically adhesive and foundationally powerful.
operational_definition:
  units: Dimensionless
  symbol_table:
    - name: Stk
      meaning: Stickiness score. A weighted sum of a domain's Σ-Compatibility (S), Stabilizer Yield (Y), Compression Power (C), and Predictive Leverage (P).
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: RPA
      meaning: Reverse Pareto Analysis score. The maximum ratio of empirically checkable consequences to the description length of the axioms used.
      dimensions: dimensionless
      default_range: "contextual; benchmarked against historical wins"
  measurement:
    procedures:
      - name: Domain Adhesion-Leverage Assessment
        outline: |
          For a candidate mathematical domain D:
          1. Author a "Domain Card" with a proof sketch for passing the Pirouette Compliance Test (PCT).
          2. Benchmark D by re-deriving key results (e.g., GR hydrolimit), measuring the change in Minimum Description Length (ΔMDL) and counting new falsifiable predictions.
          3. Compute Stk and RPA scores from the benchmark outputs according to the formulas in MATH-PHI-001.
          4. Plot the resulting (Stk, RPA) coordinate on the map to determine its quadrant.
        expected_signals: [Placement in "Goldmine" or "Rising" quadrants, Promotion of the domain to "pirouette" status.]
        pitfalls: [Subjective estimation of Stk components (violates AC-2), Using an uncalibrated RPA threshold τ, Failing to enforce PCT gate checks rigorously.]
context_windows:
  - module: MATH-PHI-001
    excerpt: |
      We bucket candidate domains by (expected) Stickiness × RPA. (“Goldmine” = high-high; “Junkyard” = low-low *for us*, not a value judgement.)

      ### GOLDMINE (high Stk, high RPA)
      - **Representation theory & tensor categories...**
      - **Symplectic & contact geometry...**

      ### JUNKYARD (low Stk, low RPA *for this universe right now*)
      - **p-adic analysis / ultrametric geometry**...
      - **Exotic smooth structures on \( \mathbb{R}^4 \)**...
  - module: MATH-PHI-001
    excerpt: |
      Protocol: turning this into code & CI
      1) **Domain card.** For each candidate \( \mathcal{D} \), author a one-page *card* with: Σ-Compat proof sketch, stabilizer list, compression deltas, and at least one proposed falsifiable.
      2) **Benchmarks.** Re-derive key results... Record MDL change and new tests.
      3) **Compute \(\mathrm{Stk}, \mathrm{RPA}\).** Log to `/analysis/math_adhesion/ledger.csv`.
      4) **CI gate.** Any domain with \( \mathrm{Stk} \ge 0.6 \) and \( \mathrm{RPA} \ge \tau \) is **promoted** to “pirouette”...
poetic_connections:
  motifs: [prospecting, sorting, adhesion, leverage, loom, fishing]
  evocative_lines:
    - "Most math is a net. The sticky math is the mesh that the loom itself uses."
    - "We invent nets. The loom keeps only what catches its threads... The rest we hang on the wall."
  association_matrix:
    - [ "STICKINESS", 0.9 ]
    - [ "RPA_SCORE", 0.9 ]
    - [ "PIRROUETTE_COMPLIANCE_TEST", 0.7 ]
formal_mappings:
  candidates:
    - target: Model/Feature Selection Plot (e.g., ROC curve)
      domain: Machine Learning
      mapping_kind: conceptual
      equation_hint: |
        N/A
      justification: |
        Like ML model selection plots, the J&G map is a 2D heuristic for evaluating candidate models (here, mathematical domains) on axes of "fit" (Stickiness) and "power" (RPA). It provides a quantitative guide for a resource-constrained search for the most effective descriptive language.
      references:
        - title: The Elements of Statistical Learning
          where: Chapter 7
          date: 2001-01-01
      confidence: 0.7
  adopted:
    - target: N/A
      rationale: This is a meta-theoretical tool internal to the Pirouette Framework's methodology and does not map directly to a term in an external physical theory.
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "The long-term rate of generating successful, novel, and validated XXP predictions is significantly higher for domains classified as 'Goldmine' than for those classified as 'Junkyard'."
      domain: methodology
      falsifier: "A statistically significant history (e.g., over 5 years of research) where domains from the 'Junkyard' quadrant consistently outperform 'Goldmine' domains in generating new, confirmed physical insights."
      status: under-test
      links: [MATH-PHI-001]
naming_notes:
  collisions: [The colloquial terms "Junkyard" and "Goldmine" can be misread as absolute value judgements.]
  disambiguation: |
    The "Junkyard" classification is not a pejorative statement about a mathematical domain's intrinsic value or elegance. It is a pragmatic label indicating low measured compatibility and leverage *for the specific physical modeling targets of the Pirouette Framework at the present time*. A domain can be promoted (e.g., from Junkyard to Rising) if a new bridge to the core physics is discovered.
crosslinks:
  near_synonyms: [Domain Utility Plot]
  antonyms: [Unstructured Exploration, Aesthetic-Driven Formalism Selection]
  prerequisites: [STICKINESS, RPA_SCORE, PIRROUETTE_COMPLIANCE_TEST]
  downstream_effects: [MODULE_PROMOTION_CI]
license: CC-BY-SA-4.0
---

# Junkyard & Goldmine map

## Canonical (Pirouette)
A 2D classification map that categorizes candidate mathematical domains into four quadrants based on their Stickiness (Stk) and Reverse Pareto Analysis (RPA) scores. The quadrants—Goldmine (high Stk, high RPA), Rising (medium Stk, high potential RPA), Utility Belt (high Stk, modest RPA), and Junkyard (low Stk, low RPA)—guide research priority by identifying formalisms that are both physically adhesive and foundationally powerful.

## EFT-First Summary
The Junkyard & Goldmine map has no direct analog in standard EFT, as it is a meta-theoretical tool for framework construction. It functions like a principled research strategy, analogous to how an EFT practitioner might prioritize operators based on expected relevance and power-counting, but applied to the selection of entire mathematical languages rather than terms in a Lagrangian. It provides a quantitative basis for deciding which formalisms (e.g., non-commutative geometry vs. tensor categories) are worth the investment to build new physical models.

## Glossary Links
- See also: Stickiness, RPA Score, Pirouette-Compliance Test