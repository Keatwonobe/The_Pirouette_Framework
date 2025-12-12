---
term: "Internal Fiber"
canonical_id: "INTERNAL_FIBER"
symbol: '\(\mathcal{F}\)'

aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["XAP-006_yang–mills_from_Σ-pushforward_internal_symmetry_of_ki"]
---

---
term: Internal Fiber
canonical_id: INTERNAL_FIBER
symbol: \(\mathcal{F}\)
aliases: []
parents: [XAP-006, CORE-021]
children: [XAP-006B, XAP-006C]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: XAP-006
      lines: "§2"
      snippet: |
        Let
        \[
        Ki : \mathcal{M}_\tau \rightarrow \mathcal{F},\qquad 
        \mathcal{F}=\mathbb{C}^N,\quad N\in\{1,2,3\},
        \]
        where \(\mathcal{M}_\tau\) is the time-substrate manifold.
        The fiber’s isometry group \(G=\mathrm{U}(N)\) acts by \(Ki\mapsto U Ki\), \(U\in G\).
  editors: [Dictionary Agent]
  review_log: []
triad:
  art: |
    An unseen, internal garden whose symmetries dictate the dances of observed particles. Its structure is the blueprint for the forces that shape reality, a geometric shadow cast upon spacetime.
  law: |
    The isometry group \(G\) of the Internal Fiber \(\mathcal{F}\) is isomorphic to the observed physical gauge group after Σ-pushforward. An N-dimensional complex fiber \(\mathcal{F} \cong \mathbb{C}^N\) generates a U(N) gauge symmetry, whose couplings are determined by the fiber's metric.
  philosophy: |
    The Internal Fiber geometrizes gauge symmetry, replacing the axiomatic insertion of symmetry groups in the Standard Model with a derivable consequence of the Ki field's internal structure. It posits that fundamental forces are not arbitrary rules, but are the necessary geometric features of a deeper, unified substrate.
pirouette_definition: |
  The Internal Fiber, \(\mathcal{F}\), is the target space of the Ki field, a complex vector space \(\mathbb{C}^N\) over which Ki is defined. The isometry group of \(\mathcal{F}\), \(G = \mathrm{U}(N)\), acts on Ki via the transformation \(Ki \mapsto U Ki\). Under the Σ-pushforward, this group \(G\) and its associated connection become the observed gauge group and gauge potential of Yang–Mills theory in spacetime. The dimension \(N\) of the fiber determines the specific gauge group: \(N=1\) for U(1), \(N=2\) for SU(2), and \(N=3\) for SU(3).
operational_definition:
  units: dimensionless
  symbol_table:
    - name: \(\mathcal{F}\)
      meaning: The internal fiber manifold
      dimensions: dimensionless
      default_range: \(\mathbb{C}^N\)
    - name: N
      meaning: Dimension of the fiber
      dimensions: dimensionless
      default_range: \{1, 2, 3\}
    - name: G
      meaning: Isometry group of the fiber
      dimensions: dimensionless
      default_range: U(N)
    - name: h_{ab}
      meaning: Metric tensor of the fiber
      dimensions: dimensionless
      default_range: contextual, scale-dependent
  measurement:
    procedures:
      - name: Gauge Group Inference
        outline: |
          The structure of the Internal Fiber is inferred from the observed gauge group structure of fundamental interactions. The dimension \(N\) is determined by identifying the rank and generators of the symmetry (e.g., electroweak SU(2) implies \(N=2\)). The scale-dependent fiber metric \(h_{ab}(\Lambda)\) is inferred by measuring the running of the corresponding gauge coupling constants \(g_N\).
        expected_signals: [Observation of U(1), SU(2), and SU(3) gauge groups, Measured running of coupling constants consistent with a scale-dependent metric \(h_{ab}(\Lambda)\).]
        pitfalls: [Mistaking an effective symmetry for a fundamental fiber structure, Inability to distinguish between a single fiber with a product group structure and nested fibers.]
context_windows:
  - module: XAP-006
    excerpt: |
      Let \(Ki : \mathcal{M}_\tau \rightarrow \mathcal{F}\), where \(\mathcal{F}=\mathbb{C}^N, N\in\{1,2,3\}\). The fiber’s isometry group \(G=\mathrm{U}(N)\) acts by \(Ki\mapsto U Ki\), \(U\in G\). Decompose \(G\) into its determinant-free and phase parts: \(G=\mathrm{SU}(N)\times \mathrm{U}(1)\). The associated connection one-form \(A_\mu = Ki^{-1}\partial_\mu Ki\) defines the curvature that becomes the Yang-Mills field strength.
  - module: XAP-006
    excerpt: |
      The choice of fiber dimension dictates the physical interaction. The U(1) fiber (\(N=1\)) reproduces electromagnetism. The SU(2) fiber (\(N=2\)) yields electroweak structure, where spontaneous orientation of Ki’s expectation value defines the Higgs direction. The SU(3) fiber (\(N=3\)) encodes color, with confinement arising geometrically from the compact, positive-definite internal metric.
poetic_connections:
  motifs: [internal space, geometric shadow, symmetry source, color garden]
  evocative_lines:
    - "Yang–Mills structure emerges as the Σ-shadow of internal τ-space holonomy."
    - "Confinement arises geometrically because the internal metric is positive-definite and compact."
  association_matrix:
    - [ "KI_FIELD", 0.9 ]
    - [ "SIGMA_PUSHFORWARD", 0.8 ]
    - [ "GAUGE_GROUP", 1.0 ]
    - [ "COUPLING_CONSTANT", 0.7 ]
formal_mappings:
  candidates:
    - target: Target space of a nonlinear sigma model / Fiber of a principal bundle
      domain: Math|EFT
      mapping_kind: mathematical
      equation_hint: |
        \( Ki: \mathcal{M}_\tau \to \mathcal{F} \)
      justification: |
        In field theory, fields are maps from a base space to a target space. The Internal Fiber \(\mathcal{F}\) serves this role for the Ki field. Its structure as the fiber in a principal bundle over the time-substrate \(\mathcal{M}_\tau\) is the source of the connection form that becomes the gauge field.
      references:
        - title: Geometry, Topology and Physics
          where: Nakahara, M. (2003)
          date: 2003-01-01
      confidence: 0.9
  adopted:
    - target: Internal symmetry space of a gauge theory
      rationale: |
        This is the most direct physical interpretation. Standard Model gauge groups like SU(3), SU(2), and U(1) act on internal vector spaces. The Pirouette Internal Fiber provides a geometric origin for these spaces, identifying them with the target manifold of the Ki field.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The observed gauge groups of the Standard Model (U(1), SU(2), SU(3)) correspond directly to the isometry groups of internal fibers of dimension N=1, N=2, and N=3, respectively."
      domain: phenomenology
      falsifier: "Discovery of a fundamental gauge group that is not U(N) or a subgroup thereof for small N. For example, the discovery of a fundamental E8 gauge symmetry would falsify this simple correspondence."
      status: supported
      links: [XAP-006]
    - statement: 'Gauge coupling constants are determined by the scale-dependent metric \(h_{ab}(\Lambda)\) of the Internal Fiber.'

      domain: theory
      falsifier: "If the running of the gauge couplings, as described by renormalization group equations, cannot be modeled by the evolution of a geometric metric on a complex manifold."
      status: proposed
      links: [XAP-006, MATH-026]
naming_notes:
  collisions: [The symbol \(\mathcal{F}\) is sometimes used for field strength in other contexts, but in Pirouette it is reserved for the fiber, while the field strength tensor is \(F_{\mu\nu}\).]
  disambiguation: |
    Distinguish the Internal Fiber \(\mathcal{F}\), a manifold, from the gauge field strength tensor \(F_{\mu\nu}\) derived from its connection. The Internal Fiber is the *source* space of the symmetry, while the field strength is a *consequence* of that symmetry in spacetime.
crosslinks:
  near_synonyms: [INTERNAL_SYMMETRY_SPACE]
  antonyms: [SPACETIME_MANIFOLD]
  prerequisites: [KI_FIELD, TIME_SUBSTRATE]
  downstream_effects: [GAUGE_GROUP, GAUGE_FIELD, COUPLING_CONSTANT, HIGGS_MECHANISM]
license: CC-BY-SA-4.0
---

# Internal Fiber (\(\mathcal{F}\))

## Canonical (Pirouette)
The Internal Fiber, \(\mathcal{F}\), is the target space of the Ki field, a complex vector space \(\mathbb{C}^N\) over which Ki is defined. The isometry group of \(\mathcal{F}\), \(G = \mathrm{U}(N)\), acts on Ki via the transformation \(Ki \mapsto U Ki\). Under the Σ-pushforward, this group \(G\) and its associated connection become the observed gauge group and gauge potential of Yang–Mills theory in spacetime. The dimension \(N\) of the fiber determines the specific gauge group: \(N=1\) for U(1), \(N=2\) for SU(2), and \(N=3\) for SU(3).

## EFT-First Summary
In effective field theory (EFT), the Internal Fiber corresponds to the internal symmetry space associated with a gauge group. The Standard Model's U(1)×SU(2)×SU(3) structure is modeled in Pirouette as arising from the isometry group of a \(\mathbb{C}^N\) target space for the fundamental Ki field. The properties of this space, such as its metric, determine observable quantities like gauge coupling constants, and its vacuum orientation determines Higgs-like symmetry breaking.

## Glossary Links
- See also: [Ki Field](<./KI_FIELD.md>), [Gauge Group](<./GAUGE_GROUP.md>), [Σ-Pushforward](<./SIGMA_PUSHFORWARD.md>)