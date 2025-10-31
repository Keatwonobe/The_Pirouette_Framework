---
term: "Coherence Laplacian"
canonical_id: "COHERENCE_LAPLACIAN"
symbol: "L"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-158"]
---

---
term: Coherence Laplacian
canonical_id: COHERENCE_LAPLACIAN
symbol: L
aliases: []
parents: [DOMA-158]
children: []
status: ratified
version: 2.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-158
      snippet: |
        The primary tool for this analysis is the **Coherence Laplacian**, a specialized form of the graph Laplacian matrix that is weighted not by simple connection, but by the quality of Coherence Flow.
  editors: [chain-of-thought-agent]
  review_log: []
triad:
  art: |
    A stethoscope for the network's song. It reveals the deep, resonant harmonies of systemic health and the sharp, dissonant cries from points of turbulence and pain.
  law: |
    The spectral decomposition of the Coherence Laplacian (L) reveals a network's resonant modes. Eigenvectors of its lowest non-zero eigenvalues correspond to the most stable, large-scale coherence patterns, while eigenvectors of its largest eigenvalues pinpoint nodes of maximal turbulence.
  philosophy: |
    To diagnose a system, one must listen to its intrinsic vibrations. The Coherence Laplacian operationalizes this principle, shifting analysis from static structure to dynamic resonance, enabling the Weaver to act not as a mere observer but as a systemic physician.
pirouette_definition: |
  The Coherence Laplacian, L, is a graph Laplacian matrix derived from a weighted adjacency matrix, W, where the weights `W_ij` are the Coherence Flow `J_ij` between nodes. Its eigendecomposition provides a spectral basis for the network's coherence manifold, with eigenvalues quantifying the frequency of resonant modes and eigenvectors localizing these modes in the network's topology. It serves as the primary diagnostic instrument for identifying laminar, turbulent, and stagnant flow patterns.
operational_definition:
  units: dimensionless
  symbol_table:
    - name: L
      meaning: Coherence Laplacian matrix
      dimensions: dimensionless
      default_range: contextual
    - name: W
      meaning: Weighted Adjacency Matrix, with weights `W_ij = J_ij`
      dimensions: dimensionless
      default_range: elements in [-1, 1]
    - name: D
      meaning: Degree Matrix, where `D_ii = Σ_j W_ij`
      dimensions: dimensionless
      default_range: contextual
    - name: J_ij
      meaning: Coherence Flow from node `i` to `j`
      dimensions: dimensionless
      default_range: "[-1, 1]"
  measurement:
    procedures:
      - name: Spectral Analysis of Coherence Flow
        outline: |
          1. Apply the Translation Protocol (DOMA-158 §2) to raw network data to derive `Kτ`, `Γ`, and `φ` for all nodes and channels.
          2. Compute the Coherence Flow `J_ij = Kτ_i * cos(φ_i - φ_j) * (1 - Γ_ij)` for every connected pair of nodes `(i, j)` to build the weighted adjacency matrix `W`.
          3. Construct the Coherence Laplacian `L = D - W`, where `D` is the corresponding degree matrix.
          4. Perform an eigendecomposition of `L` to obtain its eigenvalues and eigenvectors, which represent the network's resonant modes.
        expected_signals: [Small eigenvalues (approaching 0) corresponding to global, stable modes; large eigenvalues corresponding to localized, high-frequency turbulent modes; the Fiedler vector (eigenvector of the second-smallest eigenvalue) revealing the network's primary fault line.]
        pitfalls: [The translation from raw data to Pirouette variables (`Kτ`, `Γ`, `φ`) can be noisy or inaccurate, propagating error into L. The calculation is particularly sensitive to phase (`φ`) errors, as small changes can flip the sign of `cos(Δφ)` and thus the nature of the interaction.]
context_windows:
  - module: DOMA-158
    excerpt: |
      The health of the manifold is revealed by its natural vibrations. The primary tool for this analysis is the **Coherence Laplacian**, a specialized form of the graph Laplacian matrix that is weighted not by simple connection, but by the quality of Coherence Flow.
  - module: DOMA-158
    excerpt: |
      **Low-Frequency Modes (Small Eigenvalues):** These are the network's deep, foundational harmonies. They describe the most stable, large-scale patterns of coherence... A healthy network has a strong, well-defined fundamental chord.

      **High-Frequency Modes (Large Eigenvalues):** These are the sharp, dissonant notes. They pinpoint localized instabilities, regions of high friction, and nodes that are out of sync with their neighbors. Their eigenvectors act as precise pointers to the sources of **Turbulent Flow**.
poetic_connections:
  motifs: [resonance, vibration, harmony, dissonance, music, medicine, spectrum]
  evocative_lines:
    - "A network is not a thing; it is a resonance."
    - "The low notes sing of its unity. The high, sharp notes cry out from its points of pain."
    - "To audit a network is to hear its song in its entirety."
  association_matrix:
    - [ "COHERENCE_FLOW", 0.9 ]
    - [ "TURBULENT_FLOW", 0.8 ]
    - [ "STAGNANT_FLOW", 0.7 ]
    - [ "COHERENCE_MANIFOLD", 0.9 ]
formal_mappings:
  candidates:
    - target: Graph Laplacian matrix (L)
      domain: Math
      mapping_kind: mathematical
      equation_hint: |
        L = D - W
      justification: |
        The Coherence Laplacian is a direct application of the graph Laplacian from spectral graph theory. Unlike a standard combinatorial Laplacian (where W contains 0s and 1s) or a resistance-weighted Laplacian, its weights `W_ij` are defined by the physically-motivated Coherence Flow `J_ij`, making it sensitive to the dynamic, resonant properties of the network flow.
      references:
        - title: Spectral Graph Theory
          where: Fan Chung, CBMS Regional Conference Series in Mathematics, 1997
          date: 1997-01-01
      confidence: 0.95
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The eigenvectors corresponding to the largest eigenvalues of L pinpoint the specific nodes contributing most to network turbulence."
      domain: phenomenology
      falsifier: "If targeted intervention on nodes with high magnitude in the top eigenvectors repeatedly fails to reduce measured system-wide turbulence (e.g., as defined in DYNA-001), the claim is weakened. A system where turbulence is a non-local or purely edge-based phenomenon not capturable by node-centric eigenvectors would falsify this diagnostic principle."
      status: proposed
      links: [DOMA-158, DYNA-001]
naming_notes:
  collisions: ["The symbol 'L' is frequently used for the Lagrangian in physics. Pirouette distinguishes the Coherence Laplacian matrix (L) from the scalar Pirouette Lagrangian (𝓛_p)."]
  disambiguation: |
    The Coherence Laplacian `L` is a matrix operator used to perform a spectral analysis on a network's coherence manifold. The Pirouette Lagrangian `𝓛_p` is a scalar functional that the system seeks to optimize, whose "kinetic" and "potential" terms correspond to the low- and high-frequency modes revealed by `L`.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [COHERENCE_FLOW, NODE_COHERENCE, CHANNEL_PRESSURE, TEMPORAL_PHASE]
  downstream_effects: [TURBULENT_FLOW, STAGNANT_FLOW]
license: CC-BY-SA-4.0
---

# Coherence Laplacian

## Canonical (Pirouette)
The Coherence Laplacian, L, is a graph Laplacian matrix derived from a weighted adjacency matrix, W, where the weights `W_ij` are the Coherence Flow `J_ij` between nodes. Its eigendecomposition provides a spectral basis for the network's coherence manifold, with eigenvalues quantifying the frequency of resonant modes and eigenvectors localizing these modes in the network's topology. It serves as the primary diagnostic instrument for identifying laminar, turbulent, and stagnant flow patterns.

## EFT-First Summary
The Coherence Laplacian is a direct application of the **Graph Laplacian matrix** from spectral graph theory (see Chung, 1997). It is a matrix operator `L = D - W` whose spectrum (eigenvalues) reveals the fundamental vibrational modes of a graph. In the Pirouette Framework, the graph's edge weights `W_ij` are not simple connection strengths but are set to the **Coherence Flow** `J_ij`, a measure of resonant interaction. This makes `L` a diagnostic tool for analyzing the health of information flow in any network.

## Glossary Links
- See also: COHERENCE_FLOW, TURBULENT_FLOW, COHERENCE_MANIFOLD