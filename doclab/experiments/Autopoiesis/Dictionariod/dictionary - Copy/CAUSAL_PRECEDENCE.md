---
term: "Causal Precedence"
canonical_id: "CAUSAL_PRECEDENCE"
symbol: "≺"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-017"]
---

---
term: Causal Precedence
canonical_id: CAUSAL_PRECEDENCE
symbol: ≺
aliases: []
parents: [MATH-017]
children: [DYNA-004, CORE-020]
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-017
      lines: "L15-L16"
      snippet: |
        * **Causal precedence**: a strict partial order “u ≺ v”.
  editors: [GPT-4]
  review_log: []
triad:
  art: |
    The arrow of becoming, etched into the fabric of what is. What is done cannot be undone; each event is a footprint whose direction is forever fixed by what came before it.
  law: |
    For any two distinct events *u* and *v*, either *u ≺ v* (u precedes v), *v ≺ u* (v precedes u), or they are incomparable. The relation is transitive (*u ≺ v* and *v ≺ w* implies *u ≺ w*) and strictly acyclic (if *u ≺ v*, then *v ⊀ u*).
  philosophy: |
    Causal precedence is the sole primitive for expressing relationship and history in the fabric, replacing the coordinate-based continuum of General Relativity. It asserts that the universe is built from a web of 'before' and 'after' relations, not a grid of 'where' and 'when'. All of physics, from geometry to dynamics, must be derivable from this fundamental ordering.
pirouette_definition: |
  The fundamental relation between events, denoted *u ≺ v*, establishing a strict partial order on the set of all events *V*. A fabric *E* is formally the set of events equipped with this relation, *E = (V, ≺)*. This order is locally finite, meaning any event has a finite number of predecessors and successors. It is the basis for the fabric's causal structure, defining which events can influence which others.
operational_definition:
  units: Dimensionless
  symbol_table:
    - name: ≺
      meaning: The binary relation of causal precedence. "u ≺ v" is read as "event u causally precedes event v."
      dimensions: Dimensionless
      default_range: N/A (Boolean relation)
  measurement:
    procedures:
      - name: Causal Reconstruction from Growth History
        outline: |
          Given a complete sequence of creation operators (C⁺_P) that generated a fabric E, the precedence relation u ≺ v holds if and only if there is a path of parent-child relationships from u to v. Specifically, if v was created with parent set P, then p ≺ v for all p ∈ P. The full relation is the transitive closure of these direct parent links.
        expected_signals: [A directed acyclic graph (DAG) structure in event correlations, Conservation of motif counts (martingales) implying stable underlying causal structures]
        pitfalls: [Mistaking correlation for causation in coarse-grained views of the fabric, Incomplete observation of the growth history leading to an incorrectly inferred poset]
context_windows:
  - module: MATH-017
    excerpt: |
      **Ontology (what exists)**
      * **Events**: atomic “creations.”
      * **Causal precedence**: a strict partial order “u ≺ v”.
      * **Fabric**: a *locally finite* poset (E = (V, \prec)).
      * **Motifs**: finite induced subposets up to isomorphism (the “letters” of your alphabet).

      No coordinates. Just order and finiteness.
  - module: MATH-017
    excerpt: |
      **Minimal axiom set (portable and testable)**
      A1 **Poset substrate**: (E) is a locally-finite strict poset.
      A2 **Creation**: only (C^+_P) with acyclicity and locality are admissible.
      A3 **Action weighting**: growth law uses (\exp(-\Delta S)).
poetic_connections:
  motifs: [Becoming, Arrow of Time, Acyclicity, Partial Order, History]
  evocative_lines:
    - "No coordinates. Just order and finiteness."
    - "histories of becoming weighted by action increments."
  association_matrix:
    - [ "EVENT", 0.9 ]
    - [ "FABRIC", 0.9 ]
    - [ "ACYCLICITY", 1.0 ]
formal_mappings:
  candidates:
    - target: Chronological Past I⁻(p)
      domain: GR
      mapping_kind: mathematical
      equation_hint: |
        u ≺ v  ⟶  u ∈ I⁻(v)
      justification: |
        In General Relativity, the causal structure is defined by the metric tensor's light cones. The chronological past I⁻(v) of an event v is the set of all events that can influence v via timelike curves. Causal precedence is the discrete, pre-geometric analogue of this relation, which is recovered in the hydrodynamic limit of the fabric (Axiom A7).
      references:
        - title: General Relativity
          where: Robert M. Wald, Chapter 8
          date: 1984-01-01
      confidence: 0.9
  adopted:
    - target: Chronological Past I⁻(p)
      rationale: The mapping is central to the framework's goal of recovering General Relativity in a suitable limit, as stated in Axiom A7. It provides the primary "bridge functor" from the order-theoretic substrate to continuum geometry.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "The fundamental causal structure of the universe is a locally finite strict partial order."
      domain: theory
      falsifier: "Empirical observation of a closed timelike curve (a causal cycle, e.g., v ≺ ... ≺ v), or evidence that the structure is not discrete/locally finite at the Planck scale."
      status: proposed
      links: [MATH-017]
naming_notes:
  collisions: [The symbol ≺ is a standard mathematical symbol for a strict order relation.]
  disambiguation: |
    Causal Precedence (≺) is a strict relation (an event cannot precede itself) and a partial order (not all pairs of events are comparable). It should be distinguished from the non-strict partial order `⪯` (where `u ⪯ u` is true), and from total orders (where for any distinct u, v, either u ≺ v or v ≺ u must hold). Events not related by ≺ are said to be causally incomparable or "spacelike separated".
crosslinks:
  near_synonyms: []
  antonyms: [CAUSAL_INCOMPARABILITY]
  prerequisites: [EVENT]
  downstream_effects: [FABRIC, MOTIF, CAUSAL_DIAMOND, ACTION_FUNCTIONAL]
license: CC-BY-SA-4.0
---

# Causal Precedence

## Canonical (Pirouette)
The fundamental relation between events, denoted *u ≺ v*, establishing a strict partial order on the set of all events *V*. A fabric *E* is formally the set of events equipped with this relation, *E = (V, ≺)*. This order is locally finite, meaning any event has a finite number of predecessors and successors. It is the basis for the fabric's causal structure, defining which events can influence which others.

## EFT-First Summary
Causal Precedence (≺) is the Pirouette Framework's pre-geometric foundation for the causal structure of spacetime. In the large-scale, hydrodynamic limit, the partial order of events (*u ≺ v*) recovers the chronological ordering of events within a Lorentzian manifold, where *u* lies in the past light cone of *v* (*u* ∈ I⁻(*v*)). This emergent structure arises from a discrete, acyclic growth process governed by the Action Functional.

## Glossary Links
- See also: `EVENT`, `FABRIC`, `MOTIF`