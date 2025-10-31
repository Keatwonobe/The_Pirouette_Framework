---
term: "Fiber Metric"
canonical_id: "FIBER_METRIC"
symbol: '\(h_{ab}\)'

aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["XAP-006_yang–mills_from_Σ-pushforward_internal_symmetry_of_ki"]
---

---
term: Fiber Metric
canonical_id: FIBER_METRIC
symbol: \(h_{ab}\)
aliases: []
parents: ['XAP-006']
children: ['XAP-006B', 'XAP-006C']
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: XAP-006
      lines: "§6"
      snippet: |
        Renormalization flow from MATH-026 implies a scale-dependent deformation of the fiber metric \(h_{ab}(\Lambda)\). Critical points where \(\det h_{ab}=0\) define spontaneous symmetry breaking surfaces...
  editors: ['AI Assistant (claude-3.5-sonnet-20240620)']
  review_log: []
triad:
  art: |
    The unseen landscape of internal space, whose hills and valleys determine the strength of forces felt in the world. It is the geometric soul of interaction, shaping the rules of engagement between fundamental entities before they are projected into spacetime.
  law: |
    The inverse-square of an observed gauge coupling constant \(g_N\) is proportional to the trace-averaged volume of the corresponding internal fiber, as defined by \(h_{ab}\). A vanishing determinant, \(\det h_{ab}(\Lambda)=0\) at a scale Λ, operationally defines a point of spontaneous symmetry breaking.
  philosophy: |
    The Fiber Metric replaces the arbitrary, experimentally-fitted coupling constants of the Standard Model with a single, dynamic geometric object. This elevates interaction strengths from mere parameters to consequences of the substrate's internal topology, fulfilling the Pirouette Framework's goal of deriving physics from first geometric principles.
pirouette_definition: |
  The Fiber Metric \(h_{ab}\) is a Riemannian metric defined on the internal fiber \(\mathcal{F}\) over which the Ki field takes its values. Its geometry dictates the dynamics of the internal symmetries, with its volume element setting the magnitude of the gauge coupling constants \(g_N\) upon Σ-pushforward to observer spacetime. Scale-dependent deformations \(h_{ab}(\Lambda)\) under renormalization flow (MATH-026) drive hierarchical symmetry breaking at critical points where \(\det h_{ab} = 0\).
operational_definition:
  units: Dimensionless
  symbol_table:
    - name: \(h_{ab}\)
      meaning: Component of the Fiber Metric tensor
      dimensions: dimensionless
      default_range: "Contextual; positive-definite components"
    - name: \(g_N\)
      meaning: Gauge coupling for the group SU(N)
      dimensions: dimensionless
      default_range: "~0.1 to ~1.2"
    - name: Λ
      meaning: Renormalization energy scale
      dimensions: M L² T⁻² (Energy)
      default_range: "> 1 GeV"
  measurement:
    procedures:
      - name: Coupling Constant Inversion
        outline: |
          Measure the gauge coupling constants \(g_N\) of the Standard Model at a reference energy scale Λ. Using the Σ-pushforward correspondence that links \(g_N^{-2}\) to the effective volume of the fiber \(\mathcal{F}\), invert this relation to determine geometric properties of \(h_{ab}\). Reconstruct the scale-dependent deformation \(h_{ab}(\Lambda)\) by measuring the running of the couplings.
        expected_signals: [Precise values for \(g_1, g_2, g_3\) at multiple energy scales, The energy scale of electroweak symmetry breaking (~246 GeV)]
        pitfalls: [The inversion from \(g_N\) to \(h_{ab}\) is model-dependent on the exact form of the Σ map, Assumes the Pirouette correspondence is exact and complete]
context_windows:
  - module: XAP-006
    excerpt: |
      Confinement arises geometrically because the internal metric \(h_{ab}\) is positive-definite and compact, enforcing vanishing total color flux through the Σ-image of closed τ-loops.
  - module: XAP-006
    excerpt: |
      Renormalization flow from MATH-026 implies a scale-dependent deformation of the fiber metric \(h_{ab}(\Lambda)\). Critical points where \(\det h_{ab}=0\) define spontaneous symmetry breaking surfaces:
      \[
      \mathrm{SU}(2)\times \mathrm{U}(1)\xrightarrow{\;\langle Ki\rangle\neq0\;}\mathrm{U}(1)_{EM}.
      \]
      This reproduces electroweak unification without introducing an explicit scalar field...
poetic_connections:
  motifs: [internal geometry, force cartography, emergent parameters, geometric stiffness]
  evocative_lines:
    - "Confinement arises geometrically because the internal metric ... is positive-definite and compact"
    - "gauge couplings are geometric averages over τ-space curvature densities"
  association_matrix:
    - [ "COUPLING_CONSTANT", 0.9 ]
    - [ "SYMMETRY_BREAKING", 0.8 ]
    - [ "KI_FIELD", 0.7 ]
    - [ "SIGMA_PUSHFORWARD", 0.6 ]
formal_mappings:
  candidates:
    - target: Gauge kinetic function f(ϕ)
      domain: EFT
      mapping_kind: mathematical
      equation_hint: |
        \(\mathcal{L} \supset -f(\phi) \frac{1}{4} F_{\mu\nu}F^{\mu\nu}\), where \(f(\phi)^{-1} \approx g^2\)
      justification: |
        In many theories (e.g., string theory, SUSY), the gauge coupling is not a constant but is set by the vacuum expectation value of a scalar field (a dilaton or modulus). The Fiber Metric \(h_{ab}\) plays this role in Pirouette, with its geometric properties setting the effective value of \(g^{-2}\).
      references:
        - title: String Theory Vol. 1
          where: "J. Polchinski, Section 6.5 (D-brane actions)"
          date: 1998-01-01
      confidence: 0.8
  adopted:
    - target: Inverse-square gauge coupling, \(g^{-2}\)
      rationale: XAP-006 provides a direct mathematical derivation where the normalization of the Yang-Mills kinetic term, which corresponds to \(g^{-2}\), is an average over the fiber geometry defined by \(h_{ab}\). This is the most direct and operational mapping.
      confidence: 0.85
constraints_and_falsifiers:
  claims:
    - statement: 'The running of the SU(3), SU(2), and U(1) coupling constants with energy scale Λ is described by the geometric flow of a single underlying fiber metric \(h_{ab}(\Lambda)\).'

      domain: phenomenology
      falsifier: "If the measured beta functions for the three gauge couplings cannot be simultaneously fitted by the flow equations of a single, well-behaved Riemannian metric, the claim is false."
      status: proposed
      links: ['XAP-006', 'MATH-026']
    - statement: 'The electroweak symmetry breaking scale is determined by a critical point of the SU(2) fiber metric, where \(\det h_{ab}(\Lambda_{EW}) = 0\).'

      domain: theory
      falsifier: 'If a self-consistent model of \(h_{ab}(\Lambda)\) that correctly reproduces coupling constant running does not feature a vanishing determinant at or near 246 GeV.'

      status: proposed
      links: ['XAP-006']
naming_notes:
  collisions: [\(g_{\mu\nu}\) (spacetime metric), \(\eta_{ab}\) (Minkowski metric)]
  disambiguation: |
    Note that \(h_{ab}\) is a metric on the internal fiber \(\mathcal{F}\), not on the spacetime manifold \(\mathcal{M}_{x,t}\) (which uses \(g_{\mu\nu}\)). Its indices \(a,b,...\) run over the dimensions of the fiber (e.g., 1 to N for \(\mathbb{C}^N\)), not spacetime dimensions.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [KI_FIELD, SIGMA_PUSHFORWARD, INTERNAL_SYMMETRY]
  downstream_effects: [COUPLING_CONSTANT, SYMMETRY_BREAKING, CONFINEMENT]
license: CC-BY-SA-4.0
---

# Fiber Metric

## Canonical (Pirouette)
The Fiber Metric \(h_{ab}\) is a Riemannian metric defined on the internal fiber \(\mathcal{F}\) over which the Ki field takes its values. Its geometry dictates the dynamics of the internal symmetries, with its volume element setting the magnitude of the gauge coupling constants \(g_N\) upon Σ-pushforward to observer spacetime. Scale-dependent deformations \(h_{ab}(\Lambda)\) under renormalization flow (MATH-026) drive hierarchical symmetry breaking at critical points where \(\det h_{ab} = 0\).

## EFT-First Summary
The Fiber Metric \(h_{ab}\) serves as the Pirouette Framework's geometric origin for the inverse-square gauge couplings, \(g^{-2}\). Instead of being fundamental constants, the strengths of the Standard Model forces are determined by the volume and curvature of a compact internal manifold, governed by \(h_{ab}\). The running of couplings with energy is mapped to the deformation of this metric, and phase transitions (like electroweak symmetry breaking) occur where the metric becomes degenerate (\(\det h_{ab}=0\)).

## Glossary Links
- See also: Coupling Constant, Internal Symmetry, Σ-Pushforward