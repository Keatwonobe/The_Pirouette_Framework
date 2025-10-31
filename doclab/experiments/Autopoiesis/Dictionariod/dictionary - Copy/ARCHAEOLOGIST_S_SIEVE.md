---
term: "Archaeologist's Sieve"
canonical_id: "ARCHAEOLOGIST_S_SIEVE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-176"]
---

---
term: Archaeologist's Sieve
canonical_id: ARCHAEOLOGISTS_SIEVE
symbol: 
aliases: [Iterative Coherence Extraction, Residue Analysis]
parents: [CORE-014]
children: [INST-ANAL-002]
status: ratified
version: 2.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-176
      lines: "§4"
      snippet: |
        While k < k_max AND the Temporal Coherence Kτ(M_current) > Kτ_min:
        a. Increment the layer: k = k + 1.
        b. Apply Filter: Apply the Coherence Filter for layer k to M_current to identify the dominant resonance, Ki_k.
        c. Record Artifact: Store Ki_k and its properties.
        d. Calculate Echo Manifold...
  editors: [System Agent]
  review_log: []
triad:
  art: |
    Noise is not an absence of signal; it is a symphony of signals too quiet to be heard over the lead instrument. The Sieve teaches the analyst to listen past the shout of the primary cause and attend to the chorus of echoes that follow.
  law: |
    Any coherent system can be recursively decomposed into a hierarchical sequence of a dominant resonance ($Ki_k$) and a residual echo manifold ($M_k$). Each layer of residue is treated as a new system to be analyzed, revealing nested structures until a non-coherent Entropic Floor is reached.
  philosophy: |
    The gravest error of analysis is to discard the "noise." The residue left after removing a primary signal is not a void, but the rich, complex soil of a system's history. True understanding requires excavating these fainter echoes, for in what is left behind lies the complete story.
pirouette_definition: |
  A recursive protocol for the iterative analysis and decomposition of a system's coherence manifold. The Sieve sequentially identifies, records, and computationally removes the most dominant resonant pattern ($Ki_k$) from a given manifold ($M_{k-1}$), treating the remaining residue as a new Echo Manifold ($M_k$) for subsequent analysis. This process reveals a nested hierarchy of harmonic structures—the system's **Harmonic Spectrum**—down to a non-coherent Entropic Floor.
operational_definition:
  units: protocol
  symbol_table:
    - name: $M_k$
      meaning: The Echo Manifold at layer *k*. $M_0$ is the Primary Manifold.
      dimensions: contextual
      default_range: contextual
    - name: $Ki_k$
      meaning: The dominant resonant pattern identified and extracted at layer *k*.
      dimensions: contextual
      default_range: contextual
    - name: $k$
      meaning: The current excavation layer index.
      dimensions: dimensionless
      default_range: "[0, k_{max}]"
    - name: $k_{max}$
      meaning: Maximum excavation depth; a termination parameter.
      dimensions: dimensionless
      default_range: 3-10
    - name: $K_{\tau\_min}$
      meaning: Minimum Temporal Coherence threshold; a termination parameter.
      dimensions: dimensionless
      default_range: 0.01-0.2
  measurement:
    procedures:
      - name: Sieve Excavation
        outline: |
          1. Initialize with the Primary Manifold, $M_0$.
          2. Loop while depth and coherence thresholds are met:
             a. Apply a Coherence Filter to the current manifold to identify the dominant resonance, $Ki_k$.
             b. Store the artifact $Ki_k$.
             c. Subtract the influence of $Ki_k$ from the current manifold to produce the next-layer Echo Manifold, $M_k$.
          3. Terminate when the residue's coherence falls below $K_{\tau\_min}$ or depth $k_{max}$ is reached.
          4. The output is the ordered set of artifacts ($Ki_1, Ki_2, ...$) and the final Entropic Floor.
        expected_signals: [Harmonic Spectrum, Entropic Floor profile]
        pitfalls: [Choosing a mismatched Coherence Filter, introducing artifacts via the subtraction method, premature termination (k_max too low).]
context_windows:
  # Short, trimmed context quotes harvested from modules (3–6 sentences each).
  - module: DOMA-176
    excerpt: |
      Traditional analysis seeks the primary signal and discards the rest as noise. This is an act of profound ignorance. The Pirouette Framework understands that a system's "residue"—the information left over after the most obvious pattern has been removed—is not a void. It is the rich, complex soil of the system's history.
  - module: DOMA-176
    excerpt: |
      This protocol is a method for empirically deconstructing a system's dynamics, which are fundamentally governed by the Pirouette Lagrangian. The Archaeologist's Sieve finds these solutions one by one. The first identified resonance, $Ki_1$, is the most significant contributor to maximizing the system's "action"... The process is a reverse-engineering of the system's Lagrangian, revealing the hierarchy of resonant strategies it uses to persist.
poetic_connections:
  # Lightweight "word-association graph" and sticky lines.
  motifs: [sifting, excavation, echoes, residue, listening, symphony in static]
  evocative_lines:
    - "Noise is not an absence of signal; it is a symphony of signals too quiet to be heard."
    - "In that residue, in what is left behind, lies the true and complex history of the system's soul."
  association_matrix:
    # symmetric or directed; weights in [0,1]
    - [ "COHERENCE_MANIFOLD", 0.9 ]
    - [ "PIROUETTE_LAGRANGIAN", 0.8 ]
    - [ "WOUND_CHANNEL", 0.7 ]
    - [ "ENTROPIC_FLOOR", 0.6 ]
formal_mappings:
  # Candidate alignments to EFT/SM/CM/GR terms, each with justification and refs.
  candidates:
    - target: Iterative Signal Decomposition (e.g., Matching Pursuit, Wavelet decomposition, iterative PCA)
      domain: Math|Signal Processing
      mapping_kind: operational
      equation_hint: |
        $Signal = \sum_{k=1}^{N} \langle Signal, g_k \rangle g_k + Residue_N$
      justification: |
        The Sieve protocol is a direct operational analog to algorithms that decompose a signal by iteratively finding the best-matching waveform (resonance) from a dictionary (Coherence Filter), subtracting it, and repeating the process on the residue. This applies to methods from Fourier analysis to Principal Component Analysis (PCA). The Sieve generalizes this to abstract coherence manifolds.
      references:
        - title: A Wavelet Tour of Signal Processing
          where: S. Mallat, Chapter 10
          date: 1998-01-01
      confidence: 0.9
  adopted:
    - target: Iterative Signal Decomposition
      rationale: The operational and conceptual alignment is nearly one-to-one. The Sieve provides a physical interpretation (via the Pirouette Lagrangian) for what is otherwise a mathematical procedure.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "Any system with Temporal Coherence ($K_\tau$) above the Entropic Floor can be decomposed into a finite, ordered set of dominant resonances ($Ki_k$) where each successive Echo Manifold ($M_k$) has a strictly lower coherence than the last ($K_\tau(M_k) < K_\tau(M_{k-1})$)."
      domain: theory
      falsifier: "The discovery of a reproducible system where removing the dominant signal component systematically *increases* the coherence of the residue, or where the residue is provably indistinguishable from pure random noise after a single extraction despite the system exhibiting complex, multi-modal behavior."
      status: supported
      links: [DOMA-176]
naming_notes:
  collisions: [Sieve of Eratosthenes (Number Theory)]
  disambiguation: |
    Distinguish from mathematical sieves in number theory, which filter a discrete set based on properties. The Archaeologist's Sieve *removes* a dominant, continuous structure from a manifold to analyze the remainder, an act of excavation rather than filtering.
crosslinks:
  near_synonyms: [ITERATIVE_COHERENCE_EXTRACTION]
  antonyms: [HOLISTIC_INTEGRATION]
  prerequisites: [COHERENCE_MANIFOLD, PIROUETTE_LAGRANGIAN]
  downstream_effects: [HARMONIC_SPECTRUM]
license: CC-BY-SA-4.0
---

# Archaeologist's Sieve

## Canonical (Pirouette)
A recursive protocol for the iterative analysis and decomposition of a system's coherence manifold. The Sieve sequentially identifies, records, and computationally removes the most dominant resonant pattern ($Ki_k$) from a given manifold ($M_{k-1}$), treating the remaining residue as a new Echo Manifold ($M_k$) for subsequent analysis. This process reveals a nested hierarchy of harmonic structures—the system's **Harmonic Spectrum**—down to a non-coherent Entropic Floor.

## EFT-First Summary
The Archaeologist's Sieve is an operational protocol analogous to **Iterative Signal Decomposition** methods in mathematics and signal processing, such as wavelet analysis or iterative PCA. It deconstructs a system's total behavior (its manifold) by sequentially identifying and removing the most "energetic" or dominant mode (the primary resonance). The remaining "residue" is then treated as a new, lower-energy effective system for the next stage of analysis, revealing a hierarchy of scales or modes analogous to a power spectrum. This provides an empirical method to reverse-engineer the dominant solutions to the system's underlying Lagrangian.

## Glossary Links
- See also: [Coherence Manifold](<link>), [Pirouette Lagrangian](<link>), [Harmonic Spectrum](<link>)