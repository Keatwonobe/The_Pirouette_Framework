---
term: "Harmonic Spectrum"
canonical_id: "HARMONIC_SPECTRUM"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-176"]
---

---
term: Harmonic Spectrum
canonical_id: HARMONIC_SPECTRUM
symbol: $\mathcal{H}_S$
aliases: [Layered Coherence Model, Resonance Profile]
parents: [DOMA-176]
children: [INST-ANAL-002]
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-176
      lines: "§4, step 4"
      snippet: |
        The complete output is a layered model of the system, comprising the sequence of identified resonances ($Ki_1, Ki_2, ...$) and the final noise profile of the Entropic Floor. This is the system's **Harmonic Spectrum**.
  editors: [system]
  review_log: []
triad:
  art: |
    To know a system not by its shout, but by the chorus of whispers that compose its voice. It is the full score of a system's song, from the lead melody to the faintest, most ancient harmony.
  law: |
    A Harmonic Spectrum is a finite, ordered set of Dominant Resonances, $\mathcal{H}_S = (Ki_1, ..., Ki_{k_{max}})$, where each $Ki_k$ is the resonance of maximum coherence in the manifold $M_{k-1}$, and $M_k = M_{k-1} - f(Ki_k)$. The set is complete when the temporal coherence of the final manifold, $K_\tau(M_{k_{max}})$, falls below a predefined threshold, $K_{\tau\_min}$.
  philosophy: |
    By revealing the nested hierarchy of a system's coherent structures, the Harmonic Spectrum refutes the simplistic signal/noise dichotomy. It asserts that complexity is layered, not chaotic, and that a system's history and potential are encoded in the echoes left behind by its most dominant behaviors.
pirouette_definition: |
  The Harmonic Spectrum, $\mathcal{H}_S$, is the final output of the Archaeologist's Sieve protocol. It is an ordered sequence of Dominant Resonances, $\mathcal{H}_S = (Ki_1, Ki_2, ..., Ki_{k_{max}})$, where each $Ki_k$ is the most coherent pattern identified and removed from the Echo Manifold of the previous layer. The spectrum represents the complete, layered decomposition of a system's coherence manifold, from its most powerful organizing principle down to the Entropic Floor.
operational_definition:
  units: Ordered Set / Data Structure
  symbol_table:
    - name: $\mathcal{H}_S$
      meaning: The Harmonic Spectrum; an ordered sequence of Dominant Resonances.
      dimensions: N/A (Data Structure)
      default_range: Contextual
    - name: $Ki_k$
      meaning: The k-th Dominant Resonance identified by the Sieve.
      dimensions: Varies with system (e.g., frequency, power, etc.)
      default_range: Contextual
    - name: $k$
      meaning: Excavation layer index.
      dimensions: dimensionless
      default_range: $[1, k_{max}]$
  measurement:
    procedures:
      - name: Sieve Decomposition
        outline: |
          1. Initialize with the Primary Manifold $M_0$.
          2. Iteratively apply a Coherence Filter to the current manifold $M_{k-1}$ to find the Dominant Resonance $Ki_k$.
          3. Record $Ki_k$.
          4. Subtract $Ki_k$'s influence using a Manifold Subtraction Method to create the next Echo Manifold $M_k$.
          5. Repeat until the manifold's Temporal Coherence $K_\tau$ drops below $K_{\tau\_min}$ or $k$ reaches $k_{max}$.
          6. The collected sequence $(Ki_1, Ki_2, ...)$ is the Harmonic Spectrum.
        expected_signals: [A sequence of resonance profiles, typically with decreasing coherence/amplitude with each layer.]
        pitfalls: [Improper choice of Coherence Filter can miss non-obvious resonance geometries., Incorrect Manifold Subtraction Method can introduce artifacts into subsequent Echo Manifolds.]
context_windows:
  - module: DOMA-176
    excerpt: |
      The loop ends. The final $M_{current}$ is the system's **Entropic Floor**. The complete output is a layered model of the system, comprising the sequence of identified resonances ($Ki_1, Ki_2, ...$) and the final noise profile of the Entropic Floor. This is the system's **Harmonic Spectrum**.
  - module: DOMA-176
    excerpt: |
      The Archaeologist's Sieve finds these solutions one by one. The first identified resonance, $Ki_1$, is the most significant contributor to maximizing the system's "action" ($S_p$)... The process is a reverse-engineering of the system's Lagrangian, revealing the hierarchy of resonant strategies it uses to persist and hold a clear note against the chaos.
poetic_connections:
  motifs: [archaeology, music, signal processing, layering, echoes, history]
  evocative_lines:
    - "Noise is not an absence of signal; it is a symphony of signals too quiet to be heard over the lead instrument."
    - "attend to the chorus of echoes that follow."
  association_matrix:
    - [ "ARCHAEOLOGISTS_SIEVE", 1.0 ]
    - [ "DOMINANT_RESONANCE", 0.9 ]
    - [ "ECHO_MANIFOLD", 0.8 ]
    - [ "ENTROPIC_FLOOR", 0.7 ]
formal_mappings:
  candidates:
    - target: Fourier Series / Spectral Decomposition
      domain: Math
      mapping_kind: conceptual
      equation_hint: |
        $f(t) = \sum_{n=0}^{\infty} A_n \cdot g_n(t) \quad \iff \quad M_0 \approx \sum_{k=1}^{k_{max}} f(Ki_k)$
      justification: |
        Both methods decompose a complex signal or function into a sum of simpler, often orthogonal, basis functions (sines/cosines vs. $Ki_k$). The Harmonic Spectrum is a generalized, non-linear form of spectral analysis where the "basis functions" ($Ki_k$) are discovered iteratively from the data itself rather than being predefined.
      references:
        - title: N/A
          where: N/A
          date: N/A
      confidence: 0.8
    - target: Principal Component Analysis (PCA)
      domain: Math
      mapping_kind: operational
      justification: |
        PCA identifies orthogonal axes (principal components) that capture the maximum variance in a dataset, in descending order. This is operationally analogous to the Sieve's iterative extraction of the Dominant Resonance ($Ki_k$) which captures the maximum coherence at each layer. The Harmonic Spectrum is thus a PCA-like process in the manifold of coherence.
      references:
        - title: N/A
          where: N/A
          date: N/A
      confidence: 0.7
  adopted:
    - target: Spectral Decomposition
      rationale: The name "Spectrum" and the core concept of decomposing a whole into constituent "notes" or "frequencies" makes this the most direct and intuitive mapping. It frames the Sieve as a generalized, non-linear spectrometer for systemic coherence.
      confidence: 0.8
constraints_and_falsifiers:
  claims:
    - statement: "The Harmonic Spectrum of any system with $K_\tau > K_{\tau\_min}$ is unique and complete for a given set of Sieve parameters (Filters, Subtraction Method, $K_{\tau\_min}$)."
      domain: theory
      falsifier: "Demonstrating a system where two different orderings of resonance extraction (e.g., extracting $Ki_2$ before $Ki_1$) yield a more complete final decomposition, implying the greedy, layer-by-layer approach is suboptimal or path-dependent."
      status: proposed
      links: [DOMA-176]
naming_notes:
  collisions: [The term "Harmonic Spectrum" is standard in signal processing and acoustics, typically referring to integer multiples of a fundamental frequency.]
  disambiguation: |
    In standard signal processing, "harmonic spectrum" refers to the set of integer multiples (harmonics) of a fundamental frequency. In the Pirouette Framework, it is a more general, ordered set of a system's *dominant non-linear resonances*, which are not necessarily integer multiples of a fundamental and are discovered iteratively through manifold decomposition.
crosslinks:
  near_synonyms: []
  antonyms: [PRIMARY_MANIFOLD, ENTROPIC_FLOOR]
  prerequisites: [ARCHAEOLOGISTS_SIEVE, DOMINANT_RESONANCE, ECHO_MANIFOLD, TEMPORAL_COHERENCE]
  downstream_effects: [INST-ANAL-002]
license: CC-BY-SA-4.0
---