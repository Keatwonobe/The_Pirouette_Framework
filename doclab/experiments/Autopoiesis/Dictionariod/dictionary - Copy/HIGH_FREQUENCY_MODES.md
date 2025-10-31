---
term: "High-Frequency Modes"
canonical_id: "HIGH_FREQUENCY_MODES"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-158"]
---

---
term: High-Frequency Modes
canonical_id: HIGH_FREQUENCY_MODES
symbol: λ_high, ψ_high
aliases: [Dissonant Modes, Turbulent Modes, Coherence Fevers]
parents: [DOMA-158]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-158
      lines: "§4"
      snippet: |
        High-Frequency Modes (Large Eigenvalues): These are the sharp, dissonant notes. They pinpoint localized instabilities, regions of high friction, and nodes that are out of sync with their neighbors. Their eigenvectors act as precise pointers to the sources of Turbulent Flow (DYNA-001), allowing for surgical intervention.
  editors: [Weaver-Analyst-7]
  review_log: []
triad:
  art: |
    The sharp, dissonant notes in a network's song. They are the cries of pain from localized points of friction, feverish and out of sync with the harmonious whole.
  law: |
    High-Frequency Modes are eigenvectors of the Coherence Laplacian corresponding to large eigenvalues (λ ≫ 1), whose non-zero components are spatially localized to nodes with high temporal phase dissonance (Δφ ≈ π) or high channel pressure (Γ → 1) relative to their neighbors.
  philosophy: |
    These modes reveal that systemic dysfunction is not an abstract miasma but a concrete, localized event. By isolating the 'what' and 'where' of dissonance, they transform a complex problem into a tractable one, enabling precise healing rather than systemic overhaul.
pirouette_definition: |
  The set of eigenvectors (ψ) of the Coherence Laplacian (L) that correspond to its largest eigenvalues (λ). These modes are characteristically localized in the network, with their amplitudes concentrated on nodes that are significantly out of phase (Δφ) with their local neighborhood or connected by channels of high pressure (Γ). They serve as direct pointers to the sources of Turbulent Flow, friction, and systemic energy loss, representing the primary contributors to the network's "potential" cost term, `f(Γ)`.
operational_definition:
  units: Dimensionless (eigenvector components)
  symbol_table:
    - name: λ_high
      meaning: A large eigenvalue of the Coherence Laplacian, representing the "dissonance" of the mode.
      dimensions: dimensionless
      default_range: Contextual; significantly larger than the Fiedler eigenvalue (λ_2).
    - name: ψ_high
      meaning: The eigenvector corresponding to a high eigenvalue; the mode itself. Its components indicate nodal participation.
      dimensions: dimensionless
      default_range: Components normalized to [-1, 1].
  measurement:
    procedures:
      - name: Laplacian Spectral Analysis
        outline: |
          1. Apply the Translation Protocol (DOMA-158 §2) to map network data onto `Kτ`, `Γ`, and `φ`.
          2. Calculate the Coherence Flow matrix `J` and construct the weighted adjacency matrix `W`.
          3. From `W`, construct the Coherence Laplacian matrix `L`.
          4. Perform an eigendecomposition of `L` to find its eigenvalues (λ) and eigenvectors (ψ).
          5. Isolate the eigenvectors corresponding to the largest eigenvalues. The nodes with the highest-magnitude components in these vectors are the focal points of the high-frequency modes.
        expected_signals: [Spatially localized eigenvectors, where a few components have high magnitude and the rest are near zero, A spectrum with a large gap between the low- and high-frequency eigenvalues.]
        pitfalls: [Poor translation of raw data into Pirouette variables, leading to a misleading Laplacian, Mistaking numerical artifacts for genuine modes in large networks, Computational expense of full eigendecomposition for massive networks, requiring iterative methods.]
context_windows:
  - module: DOMA-158
    excerpt: |
      High-Frequency Modes (Large Eigenvalues): These are the sharp, dissonant notes. They pinpoint localized instabilities, regions of high friction, and nodes that are out of sync with their neighbors. Their eigenvectors act as precise pointers to the sources of Turbulent Flow (DYNA-001), allowing for surgical intervention.
  - module: DOMA-158
    excerpt: |
      Diagnose the System: ... Turbulent: Pinpoint sources of instability by locating the nodes most active in the high-frequency modes. These are the "coherence fevers" of the system.
poetic_connections:
  motifs: [dissonance, fever, pointer]
  evocative_lines:
    - "The high, sharp notes cry out from its points of pain."
    - "These are the 'coherence fevers' of the system."
  association_matrix:
    - [ "TURBULENT_FLOW", 0.9 ]
    - [ "CHANNEL_PRESSURE", 0.7 ]
    - [ "LOW_FREQUENCY_MODES", -0.8 ]
formal_mappings:
  candidates:
    - target: High-energy/short-wavelength modes
      domain: Math|CM
      mapping_kind: mathematical
      equation_hint: |
        Lψ = λψ  ↔  -∇²f = k²f
      justification: |
        The graph Laplacian (L) is a discrete analog of the continuous Laplace operator (-∇²). Its eigenvectors are the basis functions (modes) on the graph, and its eigenvalues (λ) correspond to squared spatial frequencies (k²). Large eigenvalues therefore correspond to functions that vary rapidly between adjacent nodes, directly analogous to high-frequency, short-wavelength vibrations in continuous media.
      references:
        - title: Spectral Graph Theory
          where: Fan Chung, Chapter 1
          date: 1997-01-01
      confidence: 0.9
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The nodes with the highest amplitude in the highest-frequency modes are the primary sources of coherence loss and turbulence in a network."
      domain: theory
      falsifier: "A network could be found where the dominant source of coherence loss is a global, low-frequency dephasing rather than a localized, high-frequency instability. This would manifest as an unhealthy, weak, or ill-defined Low-Frequency Mode."
      status: proposed
      links: [DOMA-158, CORE-006]
naming_notes:
  collisions: [Temporal Frequency]
  disambiguation: |
    In signal processing, "high-frequency" refers to rapid change over time. In this context, it refers to high *spatial* frequency on the network graph—a measure of how rapidly the mode's value changes between adjacent nodes. Distinguish from Low-Frequency Modes, which describe large-scale, stable patterns of coherence, not localized instability.
crosslinks:
  near_synonyms: []
  antonyms: [LOW_FREQUENCY_MODES]
  prerequisites: [COHERENCE_LAPLACIAN, COHERENCE_FLOW]
  downstream_effects: [TURBULENT_FLOW, PRESSURE]
license: CC-BY-SA-4.0
---