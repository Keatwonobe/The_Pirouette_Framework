---
term: "Modal Logic of Becoming"
canonical_id: "MODAL_LOGIC_OF_BECOMING"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-017"]
---

---
term: Modal Logic of Becoming
canonical_id: MODAL_LOGIC_OF_BECOMING
symbol: ◁, ▷
aliases: [Internal Logic, Becoming Logic]
parents: [MATH-017]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-017
      lines: "Section 8"
      snippet: |
        Two modalities:
        * ◁ (“already”): truths preserved backwards on all predecessors.
        * ▷ (“yet”): truths preserved for all admissible one-step extensions.
  editors: [agent:text-davinci-003-t2b]
  review_log: []
triad:
  art: |
    A logic of the growing block universe. It speaks of what is written in stone by the past and what remains a branching path on the world's frontier.
  law: |
    A proposition P is `◁`-true ('already') for a fabric E if P holds for all causal predecessors of E. A proposition Q is `▷`-true ('yet') if Q holds for all possible one-step extensions of E. Truth is not absolute, but is anchored to a specific state of becoming.
  philosophy: |
    This logic provides the substrate's own language for reasoning about its history and potential. It formalizes the perspective of an observer embedded within the causal fabric, for whom the past is fixed but the future is an open, constrained set of possibilities. It is the native proof system for the Calculus of Becoming.
pirouette_definition: |
  The Modal Logic of Becoming is an intuitionistic sequent calculus defined on the state of a causal fabric, E. It features two temporal modal operators: `◁` ('already'), which quantifies over all predecessor subfabrics (the causal past), and `▷` ('yet'), which quantifies over all admissible one-step extensions (the immediate causal future). A proposition's truth value is not absolute but is evaluated relative to a specific fabric E, expressed in sequents of the form `E ⊢ P`.
operational_definition:
  units: dimensionless
  symbol_table:
    - name: ◁P
      meaning: "P is 'already' true; P holds for the current fabric and for all its causal predecessors."
      dimensions: dimensionless
      default_range: N/A
    - name: ▷P
      meaning: "P is 'yet' true; P will hold for all admissible one-step extensions of the current fabric."
      dimensions: dimensionless
      default_range: N/A
    - name: E ⊢ P
      meaning: "The sequent asserting that proposition P holds true for fabric E."
      dimensions: dimensionless
      default_range: N/A
  measurement:
    procedures:
      - name: Proof by Evaluation
        outline: |
          Given a fabric E and a proposition P involving modalities, determine truth by recursive evaluation. To check `E ⊢ ▷Q`, generate all one-step extensions `{E'}` consistent with the growth law and verify that `E' ⊢ Q` holds for all of them. To check `E ⊢ ◁Q`, verify `E ⊢ Q` and then check `E' ⊢ ◁Q` for all maximal predecessors `E' ≺ E`.
        expected_signals: [A boolean truth value (True/False) for the proposition at E.]
        pitfalls: [Combinatorial explosion: the number of predecessors or successors can be large, making evaluation computationally intractable for complex fabrics or deeply nested modalities.]
context_windows:
  - module: MATH-017
    excerpt: |
      Two modalities:
      * **◁** (“already”): truths preserved **backwards** on all predecessors.
      * **▷** (“yet”): truths preserved **for all** admissible one-step extensions.
      Sequent rules (schematic):
      * If (E ⊢ P) and every admissible extension satisfies (Q), then (E ⊢ P ∧ ▷Q).
      * If (E ⊢ ◁P) and (E' preceq E), then (E' ⊢ P).
      This is your internal logic. It’s intuitionistic by construction; classicality appears in dense, high-coherence limits.
  - module: MATH-017
    excerpt: |
      The ◁/▷ modal rules give an **intuitionistic sequent calculus** whose soundness is immediate from growth semantics. Completeness (for finite fabrics) is a tractable target.
poetic_connections:
  motifs: [becoming, causal past, possible futures, intuitionistic truth, growing block universe]
  evocative_lines:
    - "This is your internal logic. It’s intuitionistic by construction."
    - "The ◁/▷ modal rules give an intuitionistic sequent calculus whose soundness is immediate from growth semantics."
  association_matrix:
    - [ "FABRIC", 0.9 ]
    - [ "CAUSAL_PRECEDENCE", 0.9 ]
    - [ "ACTION_FUNCTIONAL", 0.7 ]
formal_mappings:
  candidates:
    - target: Computational Tree Logic (CTL) / Linear Temporal Logic (LTL)
      domain: Math
      mapping_kind: conceptual
      equation_hint: |
        ▷P  ↔  AX P  (in all next states, P)
        ◁P  ↔  (P ∧ H P) (P is true, and has always been true)
      justification: |
        Like CTL and LTL, this is a modal logic for reasoning about sequences of states. However, `◁` and `▷` are tied to the specific, physically-grounded growth semantics of the causal fabric, rather than abstract state transitions. `▷` resembles CTL's `AX` operator, while `◁` is a past-time operator enforcing historical truth.
      references:
        - title: Model Checking
          where: Clarke, Grumberg, and Peled
          date: 1999-01-01
      confidence: 0.7
  adopted:
    - target: ""
      rationale: ""
      confidence: 0.0
constraints_and_falsifiers:
  claims:
    - statement: "The Modal Logic of Becoming is sound and complete with respect to the growth semantics for all finite fabrics."
      domain: theory
      falsifier: "A valid theorem of the logic is found to be false for some finite fabric E (soundness failure), or a statement that is true for all finite fabrics cannot be derived from the axioms (completeness failure)."
      status: proposed
      links: [MATH-017]
naming_notes:
  collisions: [The symbol `◁` is used for normal subgroups in group theory.]
  disambiguation: |
    In the Pirouette Framework, `◁` and `▷` are always modal operators that act on propositions within a sequent of the form `E ⊢ ...`. They should not be confused with their use in group theory or other algebraic contexts.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [FABRIC, CAUSAL_PRECEDENCE]
  downstream_effects: [CONSERVED_MOTIF]
license: CC-BY-SA-4.0
---

# Modal Logic of Becoming

## Canonical (Pirouette)
The Modal Logic of Becoming is an intuitionistic sequent calculus defined on the state of a causal fabric, E. It features two temporal modal operators: `◁` ('already'), which quantifies over all predecessor subfabrics (the causal past), and `▷` ('yet'), which quantifies over all admissible one-step extensions (the immediate causal future). A proposition's truth value is not absolute but is evaluated relative to a specific fabric E, expressed in sequents of the form `E ⊢ P`.

## EFT-First Summary
This is a formal language for expressing properties of the substrate's causal history and possible evolution. It is analogous to logical frameworks used in foundational physics to enforce causality and define observables relative to a specific state or foliation. However, it operates directly on the discrete causal structure of the Pirouette fabric rather than a continuous spacetime manifold, providing a built-in, operational definition of past and future possibilities.

## Glossary Links
- See also: [FABRIC](<#>), [CAUSAL_PRECEDENCE](<#>), [ACTION_FUNCTIONAL](<#>)