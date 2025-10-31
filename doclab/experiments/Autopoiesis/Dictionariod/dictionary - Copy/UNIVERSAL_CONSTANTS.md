---
term: "Universal constants"
canonical_id: "UNIVERSAL_CONSTANTS"
symbol: "U"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-018"]
---

---
term: Universal constants
canonical_id: UNIVERSAL_CONSTANTS
symbol: U
aliases: []
parents: [MATH-018]
children: [MATH-019, MATH-020]
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-018
      lines: "D1"
      snippet: |
        • Universal constants U = {u_k}: derivable from axioms/symmetries only; at most a single global scale may be anchored once (see D3).
  editors: [Framework Lexicographer]
  review_log: []
triad:
  art: |
    The framework's immutable DNA, derived from first principles. These constants are not chosen but discovered, the frozen echo of the system's deepest symmetries. They represent the architecture, not the decoration.
  law: |
    Universal constants (U) are a class of parameters whose values are fixed by the framework's axioms and symmetries. Exactly one member of U (or a derived quantity) may be anchored to a single experimental measurement to set a global scale; thereafter, all other members of U are frozen predictions. Any subsequent tuning is a violation.
  philosophy: |
    To enforce falsifiable predictivity and eliminate the researcher degrees of freedom associated with post-hoc parameter tuning. Universal constants replace a landscape of ad-hoc knobs with a rigid, derivable structure, making theoretical claims brittle and subject to sharp empirical tests.
pirouette_definition: |
  A set of dimensionless parameters, U = {u_k}, whose values are derived from the framework's foundational axioms or symmetry principles (MATH-018 D2). U is distinct from topological indices (T) and nuisance parameters (N). The entire set is fixed by a mandatory 'one-shot anchoring' (MATH-018 D3) to a single experimental observable, after which all members of U are frozen and cannot be retuned to fit other data.
operational_definition:
  units: Dimensionless
  symbol_table:
    - name: U
      meaning: The set of all universal constants {u_k}.
      dimensions: dimensionless
      default_range: contextual
    - name: u_k
      meaning: A specific, indexed universal constant.
      dimensions: dimensionless
      default_range: contextual
  measurement:
    procedures:
      - name: Derivation from Symmetry
        outline: |
          Derive the functional relationships and dimensionless ratios between all u_k based on the framework's symmetry principles (MATH-018 D2). This establishes a self-consistent web of parameters with only one remaining global scale degree of freedom.
        expected_signals: [A complete, self-consistent set of inter-parameter ratios.]
        pitfalls: [Incorrectly identified symmetries, algebraic errors in derivation, mistaking a nuisance parameter for a universal one.]
      - name: One-Shot Anchoring
        outline: |
          Select a single, high-precision experimental observable (e.g., electron g−2). Use its measured value to fix the one free global scale in the system, thereby setting the numerical values for all u_k simultaneously and permanently. This operation is recorded in a signed Freeze Manifest (MATH-018 P2).
        expected_signals: [A Freeze Manifest with committed numerical values for all U.]
        pitfalls: [Choosing a poorly measured or theoretically contaminated anchor, re-anchoring on a different observable (violates MATH-018 D3), arithmetic errors in scale setting.]
context_windows:
  - module: MATH-018
    excerpt: |
      D1 — Parameter Classes and Allowable Operations
      • Universal constants U = {u_k}: derivable from axioms/symmetries only; at most a single global scale may be anchored once (see D3).
      • Portal/topology indices T = {t_j}: integer or signed indices attached to spinorial/topological class...
      • Nuisance parameters N = {n_m}: experimental or environmental; may be taken from external literature but **never tuned** to improve fit.
  - module: MATH-018
    excerpt: |
      D3 — One‑Shot Anchoring Rule
      Exactly one anchor is permitted to set a single global scale (e.g., electron a_e). After this operation, **all** U, T are frozen. No re‑anchoring across observables or species.
poetic_connections:
  motifs: [Symmetry, Anchoring, Predictivity, Foundational, Frozen]
  evocative_lines:
    - "Lock in Pirouette’s predictive status..."
    - "derivable from axioms/symmetries only"
    - "all U, T are frozen"
  association_matrix:
    - [ "ONE_SHOT_ANCHORING", 0.9 ]
    - [ "SYMMETRY_FIXED_FORMS", 0.8 ]
    - [ "NUISANCE_PARAMETER", -0.9 ] # Antonym
formal_mappings:
  candidates:
    - target: GUT coupling unification
      domain: EFT
      mapping_kind: conceptual
      equation_hint: |
        α_1(M_G) = α_2(M_G) = α_3(M_G)
      justification: |
        In Grand Unified Theories (GUTs), relationships between gauge couplings are predicted by a higher symmetry. The values are not arbitrary but are linked, and their running is fixed once a single scale (e.g., M_GUT) and value is set. This mirrors the concept of a web of derived parameters fixed by a single anchor.
      references:
        - title: "Gauge coupling unification"
          where: "Georgi, H., Quinn, H. R., & Weinberg, S. (1974). Physical Review Letters, 33(7), 451."
          date: 1974-08-12
      confidence: 0.8
  adopted:
    - target: Dimensionless physical constants (aspirational)
      rationale: |
        The Pirouette Framework's U are conceptually what the Standard Model's ~26 dimensionless constants (e.g., fine-structure constant, Yukawa couplings) are hoped to one day become: outputs of a deeper theory rather than inputs to be measured. The key distinction is that SM constants are currently empirical inputs, whereas Pirouette's U are, by definition, derived outputs locked by a single measurement.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "After one-shot anchoring on observable O₁, the values of U predict out-of-sample observables O₂, O₃, ... within their specified uncertainties."
      domain: phenomenology
      falsifier: "An out-of-sample prediction for a high-precision observable (e.g., a_μ) derived from an anchor on a different observable (e.g., a_e) disagrees with experimental measurement by >5σ, assuming all uncertainties are correctly propagated."
      status: proposed
      links: [MATH-018#D3, MATH-018#D4, MATH-018#P3]
naming_notes:
  collisions: [U for Unitary Operator, Potential Energy, internal energy]
  disambiguation: |
    These are not the fundamental constants of the Standard Model, which are treated as empirical inputs. Pirouette's U are derived parameters whose inter-relations are fixed by theory, with only a single overall scale anchored to experiment. They are strictly distinct from tunable Nuisance Parameters (N).
crosslinks:
  near_synonyms: []
  antonyms: [NUISANCE_PARAMETER]
  prerequisites: [SYMMETRY_FIXED_FORMS]
  downstream_effects: [ONE_SHOT_ANCHORING, PREDICTIVITY_GUARDRAILS]
license: CC-BY-SA-4.0
---

# Universal constants

## Canonical (Pirouette)
A set of dimensionless parameters, U = {u_k}, whose values are derived from the framework's foundational axioms or symmetry principles (MATH-018 D2). U is distinct from topological indices (T) and nuisance parameters (N). The entire set is fixed by a mandatory 'one-shot anchoring' (MATH-018 D3) to a single experimental observable, after which all members of U are frozen and cannot be retuned to fit other data.

## EFT-First Summary
Universal constants (U) are analogous to the dimensionless physical constants of the Standard Model (like α or Yukawa couplings), but with a crucial difference. While the SM's constants are measured inputs, Pirouette's U are derived outputs from a deeper, symmetry-based theory. Their internal relationships are fixed, and their absolute values are locked in by a single experimental measurement (the "one-shot anchor"), after which the framework makes concrete, falsifiable predictions for other observables. This approach is conceptually similar to how a Grand Unified Theory predicts relationships between the SM gauge couplings.

## Glossary Links
- See also: [Symmetry-Fixed Forms](<#>), [One-Shot Anchoring](<#>), [Nuisance Parameter](<#>)