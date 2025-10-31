---
term: "Low-Frequency Modes"
canonical_id: "LOW_FREQUENCY_MODES"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-158"]
---

---
term: Low-Frequency Modes
canonical_id: LOW_FREQUENCY_MODES
symbol: λ_small, v_Fiedler
aliases: [foundational harmonies, fundamental chord, collective song]
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
        Low-Frequency Modes (Small Eigenvalues): These are the network's deep, foundational harmonies. They describe the most stable, large-scale patterns of coherence. The Fiedler vector (eigenvector of the second-smallest eigenvalue) reveals the network's most natural fault line—the division across which coherence flows most weakly. A healthy network has a strong, well-defined fundamental chord.
  editors: [System Agent]
  review_log: []
triad:
  art: |
    The deep, resonant bass notes of a network's collective song. They sing of its fundamental unity, its most stable and effortless ways of being coherent.
  law: |
    Small eigenvalues of the Coherence Laplacian correspond to eigenvectors that vary slowly across the network, revealing large-scale, stable patterns of Coherence Flow. The second-smallest eigenvalue measures the network's overall flow connectivity.
  philosophy: |
    These modes reveal the network's inherent structure and identity, the path of least resistance for system-wide coherence. They represent the "kinetic" term of the Pirouette Lagrangian—the system's capacity for productive, unified action.
pirouette_definition: |
  The set of eigenvectors of the Coherence Laplacian (`L`) corresponding to the smallest non-zero eigenvalues (`λ`). These eigenvectors represent the most stable, large-scale patterns of synchronous activity (Coherence Flow) in a network. They change slowly across the graph, defining broad regions of shared phase and high mutual coherence, and are the primary indicators of systemic health and laminar flow.
operational_definition:
  units: Dimensionless
  symbol_table:
    - name: λ_i
      meaning: The i-th eigenvalue of the Coherence Laplacian.
      dimensions: dimensionless
      default_range: "[0, N] where N is number of nodes"
    - name: v_i
      meaning: The i-th eigenvector of the Coherence Laplacian.
      dimensions: dimensionless
      default_range: "N-dimensional vector"
    - name: λ_2
      meaning: The Fiedler Value; the second-smallest eigenvalue, indicating algebraic connectivity.
      dimensions: dimensionless
      default_range: contextual
  measurement:
    procedures:
      - name: Spectral Analysis of the Coherence Laplacian
        outline: |
          1. Translate raw network data into node (`Kτ`, `φ`) and channel (`Γ`) parameters.
          2. Calculate the directed Coherence Flow `J_ij` for all connected nodes `i, j`.
          3. Construct the weighted adjacency matrix `W` where `W_ij = J_ij`.
          4. Construct the Coherence Laplacian `L` from `W`.
          5. Compute the eigendecomposition of `L`.
          6. The low-frequency modes are the eigenvectors corresponding to the smallest non-zero eigenvalues.
        expected_signals: [A spectral gap after the first few eigenvalues, A bipolar Fiedler vector partitioning the network]
        pitfalls: [Poor normalization of the Laplacian matrix, Insufficient temporal resolution in source data to define phase `φ`]
context_windows:
  - module: DOMA-158
    excerpt: |
      Low-Frequency Modes (Small Eigenvalues): These are the network's deep, foundational harmonies. They describe the most stable, large-scale patterns of coherence. The Fiedler vector (eigenvector of the second-smallest eigenvalue) reveals the network's most natural fault line—the division across which coherence flows most weakly. A healthy network has a strong, well-defined fundamental chord.
  - module: DOMA-158
    excerpt: |
      Assess overall health by examining the strength and shape of the low-frequency modes. A strong fundamental harmony indicates efficient, system-wide coherence. ... The "kinetic" term is the sum of the network's productive, laminar flows. It is the useful work the network is doing, represented by the low-frequency modes of the Laplacian.
poetic_connections:
  motifs: [harmony, resonance, foundation, unity, ground state, bass note]
  evocative_lines:
    - "These are the network's deep, foundational harmonies."
    - "The low notes sing of its unity."
    - "A healthy network has a strong, well-defined fundamental chord."
  association_matrix:
    - [ "COHERENCE_LAPLACIAN", 0.9 ]
    - [ "LAMINAR_FLOW", 0.8 ]
    - [ "SYSTEM_HEALTH", 0.8 ]
    - [ "HIGH_FREQUENCY_MODES", -0.9 ]
    - [ "TURBULENCE", -0.8 ]
formal_mappings:
  candidates:
    - target: Fiedler vector (eigenvector of λ₂)
      domain: Math
      mapping_kind: mathematical
      justification: |
        The Fiedler vector is mathematically defined as the eigenvector of the second-smallest eigenvalue of a graph Laplacian. It is provably optimal for partitioning a graph into two components with minimal edge cuts, directly corresponding to the Pirouette claim of revealing the "most natural fault line."
      references:
        - title: Algebraic connectivity of graphs
          where: Czechoslovak Mathematical Journal, 1973
          date: 1973-01-01
      confidence: 1.0
    - target: Acoustic Phonons
      domain: CM
      mapping_kind: conceptual
      justification: |
        In a crystal lattice, acoustic phonons are low-energy, long-wavelength collective excitations where adjacent atoms move in phase. This is a direct physical analog to low-frequency graph modes, where adjacent nodes share a similar phase/value, representing a low-energy, stable, collective pattern of coherence.
      references:
        - title: Solid State Physics
          where: Ashcroft & Mermin, Ch. 22
          date: 1976-01-01
      confidence: 0.8
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The Fiedler vector of the Coherence Laplacian identifies the partition across which a network will most likely fracture or divide under systemic stress."
      domain: phenomenology
      falsifier: "A longitudinal study of networks (e.g., companies, social groups) shows that observed schisms, reorganizations, or failures consistently occur along partitions *not* predicted by the Fiedler vector calculated from pre-stress Coherence Flow data."
      status: proposed
      links: [DOMA-158]
naming_notes:
  collisions: []
  disambiguation: |
    The term "low-frequency" refers to low *spatial* frequency—the mode's value changes slowly from node to node across the network topology, corresponding to a low eigenvalue. It does not directly refer to low temporal frequency, although stable, large-scale patterns often exhibit slow temporal dynamics.
crosslinks:
  near_synonyms: []
  antonyms: [HIGH_FREQUENCY_MODES]
  prerequisites: [COHERENCE_LAPLACIAN, COHERENCE_FLOW]
  downstream_effects: [LAMINAR_FLOW, SYSTEM_HEALTH]
license: CC-BY-SA-4.0