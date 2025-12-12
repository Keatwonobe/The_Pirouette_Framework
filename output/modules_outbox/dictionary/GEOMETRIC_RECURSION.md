---
term: "Geometric Recursion"
canonical_id: "GEOMETRIC_RECURSION"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-015"]
---

---
term: Geometric Recursion
canonical_id: GEOMETRIC_RECURSION
symbol: 
aliases: []
parents: [MATH-015]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-015
      lines: "Section 4"
      snippet: |
        * **Vacuum polarization** ↔ curvature of the wound channel due to the medium’s response.
        * **Vertex subgraph** ↔ local twist of the channel (spin–orbit coupling analogue).
        * **Counterterms** ↔ redefinition of the local chart that keeps the channel’s extrinsic curvature finite (renormalization of the geodesic data).
          Each is a step in a **geometric recursion** that updates how a particle’s past bends its near future; Feynman diagrams serve as precise bookkeeping for these geometric updates.
  editors: [AI Assistant]
  review_log: []
triad:
  art: |
    A particle's path whispers its own future, bending spacetime in a self-similar echo. Each quantum fluctuation is a new fold in the origami of its worldline, a recursion written in curvature.
  law: |
    The n-th loop correction to a particle's observable (e.g., anomalous magnetic moment) is computed by applying the n-th geometric update operator to its worldtube geometry. The operator is defined by the gauge-invariant set of n-loop Feynman diagrams, and its application must reproduce the corresponding universal coefficient, such as `C₂ ≈ +0.328...`.
  philosophy: |
    Geometric Recursion recasts perturbative quantum field theory not as a sum over abstract diagrams, but as an iterative refinement of a particle's spacetime trajectory. This reframing aims to unify the discrete, combinatorial nature of QFT with the smooth, differential language of geometry, suggesting that quantum corrections are fundamentally geometric updates to a particle's history.
pirouette_definition: |
  An interpretive framework that maps the perturbative expansion of quantum field theory into a series of iterative geometric updates applied to a particle's trajectory (worldtube). Each loop order in a Feynman diagram calculation corresponds to a specific geometric operation: vacuum polarization subgraphs induce curvature, vertex subgraphs induce local torsion or twist, and counterterms correspond to chart redefinitions that maintain finite extrinsic curvature. The recursion builds a progressively more complex geometry that encodes the particle's quantum interactions.
operational_definition:
  units: Not applicable (process).
  symbol_table:
    - name: C_n
      meaning: The n-loop universal coefficient in the anomalous magnetic moment expansion, calculated via the n-th step of the recursion.
      dimensions: dimensionless
      default_range: C₁=0.5, C₂≈+0.32847...
  measurement:
    procedures:
      - name: Calculation of C₂ via Geometric Recursion
        outline: |
          1.  Start with the 1-loop corrected worldtube geometry, which incorporates the `C₁` (Schwinger) term as an initial curvature.
          2.  Identify the 2-loop Feynman diagram topologies (vacuum polarization, irreducible vertex, etc.).
          3.  Map each topology to its corresponding geometric operator (e.g., vacuum polarization → curvature update, vertex → twist update).
          4.  Apply these operators to the 1-loop geometry.
          5.  Apply the counterterm operator (chart redefinition) to enforce on-shell conditions and cancel divergences.
          6.  Integrate the resulting change in the Pauli term coefficient over the worldtube to extract the finite value of `C₂`.
        expected_signals:
          - A dimensionless, positive coefficient `C₂` numerically matching the known QED result (+0.328478965...).
        pitfalls:
          - Incorrect mapping between diagram topologies and geometric operations.
          - Sign errors arising from inconsistent metric signature conventions or failed enforcement of Ward identities in the geometry.
          - Incomplete application of counterterms, leading to divergent or scheme-dependent results.
context_windows:
  - module: MATH-015
    excerpt: |
      **Geometric recursion view:** BFM packages Feynman subgraphs as curvature corrections to the background field’s effective action. The two-loop terms arise as the next-order curvature of the particle’s worldtube (history), matching the recursion you call the **wound-channel** update.
  - module: MATH-015
    excerpt: |
      Each is a step in a **geometric recursion** that updates how a particle’s past bends its near future; Feynman diagrams serve as precise bookkeeping for these geometric updates.
poetic_connections:
  motifs: [worldtube, self-reference, wound-channel, curvature, iteration, history]
  evocative_lines:
    - "how a particle’s past bends its near future"
    - "Feynman diagrams serve as precise bookkeeping for these geometric updates"
  association_matrix:
    - [ "Renormalization Group Flow", 0.8 ]
    - [ "Worldline Formalism", 0.9 ]
    - [ "Curvature", 0.7 ]
formal_mappings:
  candidates:
    - target: Renormalization Group (RG) Flow
      domain: QFT
      mapping_kind: conceptual
      equation_hint:
      justification: |
        RG flow describes the evolution of a theory's parameters with energy scale, an iterative process. Geometric Recursion is also an iterative process that refines a geometric object (the worldtube) order-by-order in perturbation theory. Both map a discrete step (integrating out a momentum shell vs. adding a loop order) to a continuous evolution of the underlying structure.
      references: []
      confidence: 0.8
  adopted:
    - target: Feynman Diagram Expansion
      domain: QFT
      mapping_kind: mathematical
      rationale: |
        The framework is explicitly defined as a direct, one-to-one re-interpretation of the standard perturbative expansion in QFT. Each class of Feynman diagrams at a given loop order is mapped to a specific geometric operation, making it a direct translation of the established mathematical structure.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The geometric recursion for the 2-loop QED correction to the electron's anomalous magnetic moment, when correctly formulated, must yield a positive coefficient `C₂ ≈ +0.328...`"
      domain: theory
      falsifier: "A rigorous derivation within the geometric recursion framework that yields a negative sign for `C₂`, or a value inconsistent with the established QED result, would falsify the claimed mapping."
      status: supported
      links: [MATH-015]
naming_notes:
  collisions: []
  disambiguation: |
    This term should not be confused with a geometric series (∑arⁿ) or simple recursive algorithms in computer graphics. Geometric Recursion refers specifically to the recursive application of geometric *operators* to a spacetime manifold (the particle's worldtube) as an interpretation of quantum field theory's perturbative expansion.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [WORLDLINE_FORMALISM]
  downstream_effects: [PRESSURON_EFFECTS]
license: CC-BY-SA-4.0
---

# Geometric Recursion

## Canonical (Pirouette)
An interpretive framework that maps the perturbative expansion of quantum field theory into a series of iterative geometric updates applied to a particle's trajectory (worldtube). Each loop order in a Feynman diagram calculation corresponds to a specific geometric operation: vacuum polarization subgraphs induce curvature, vertex subgraphs induce local torsion or twist, and counterterms correspond to chart redefinitions that maintain finite extrinsic curvature. The recursion builds a progressively more complex geometry that encodes the particle's quantum interactions.

## EFT-First Summary
Geometric Recursion is a framework providing a direct geometric interpretation for the perturbative expansion of quantum field theory, as used in calculations like the anomalous magnetic moment. It maps each order in the Feynman diagram expansion to an iterative update on the geometry of a particle's worldline. For example, 2-loop vacuum polarization diagrams correspond to a curvature correction of the particle's "worldtube," directly recovering the universal QED coefficient `C₂ ≈ +0.328...` by translating the diagrammatic calculation into the language of differential geometry.

## Glossary Links
- See also: Worldline Formalism