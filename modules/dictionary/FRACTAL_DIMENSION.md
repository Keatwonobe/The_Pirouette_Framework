---
term: "Fractal Dimension"
canonical_id: "FRACTAL_DIMENSION"
symbol: "D"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-056"]
---

---
term: Fractal Dimension
canonical_id: FRACTAL_DIMENSION
symbol: D
aliases: [Informational Compressibility, Coherence Dimension]
parents: [DOMA-056, CORE-013]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-056
      lines: "§2"
      snippet: |
        The framework posits that a system's coherence (`Kτ`) is inversely proportional to its informational entropy... This property can be quantified by measuring a system's intrinsic fractal dimension (`D`), which reveals its capacity for compression.
  editors: [system]
  review_log: []
triad:
  art: |
    The crinkle of a coastline, the branch of a tree, the rhythm of a thought—all share a common signature, a measure of how elegantly their infinite complexity is built from a simple seed.
  law: |
    A system's fractal dimension (D) is the exponent that relates its information content to its measurement scale, quantified as the slope of its rate-distortion curve in log-log space.
  philosophy: |
    D serves as a universal yardstick for coherence, revealing that the structure of a genome, a melody, and a galaxy are not just metaphorically related but are quantitatively comparable expressions of the same underlying drive toward informational order.
pirouette_definition: |
  The fractal dimension `D` is a dimensionless scalar that quantifies a system's informational coherence. It is derived from the scaling relationship between fidelity and data rate when the system's information is compressed by the ψ-collapse operator. A low `D` indicates high coherence, order, and redundancy (near-crystalline structure), while a high `D` indicates low coherence and high informational entropy (near-randomness).
operational_definition:
  units: dimensionless
  symbol_table:
    - name: D
      meaning: Fractal Dimension
      dimensions: "dimensionless"
      default_range: "[0, 1]"
    - name: Kτ
      meaning: Coherence of a system
      dimensions: "dimensionless"
      default_range: "contextual"
  measurement:
    procedures:
      - name: ψ-Collapse Rate-Distortion Analysis
        outline: |
          Apply the universal ψ-collapse compression algorithm to a system's data representation (e.g., genomic sequence, time-series, image). Generate a rate-distortion curve by plotting compressed data size against a fidelity/loss metric. The slope of the best-fit line to this curve in log-log space is the fractal dimension `D`.
        expected_signals: [A stable, linear relationship in log-log space over a significant range of scales., Characteristic `D` values for distinct classes of systems (e.g., ~0.06 for genomic, ~0.32 for semantic).]
        pitfalls: [Insufficient data to establish a clear scaling law., Contamination of the data set with noise from a different manifold, skewing the slope.]
context_windows:
  - module: DOMA-056
    excerpt: |
      The framework posits that a system's coherence (`Kτ`) is inversely proportional to its informational entropy, as described in `CORE-013`. A highly coherent system is highly ordered and redundant; a low-coherence system is chaotic and informationally dense. This property can be quantified by measuring a system's intrinsic fractal dimension (`D`), which reveals its capacity for compression.
  - module: DOMA-056
    excerpt: |
      Analysis across physically distinct domains reveals a law-like relationship. Each class of information occupies a unique, linear band of coherence, validating `D` as a fundamental measure of a system's structure. This universal signature provides the foundational tool: a way to measure the very quantity—coherence—whose maximization drives all the dynamics predicted below.
poetic_connections:
  motifs: [self-similarity, compression, scaling law, roughness, order, complexity]
  evocative_lines:
    - "The universal signature of coherence."
    - "A map is an act of trust. It claims that a pattern exists, that the territory is not random noise."
  association_matrix:
    - [ "COHERENCE", 0.9 ]
    - [ "INFORMATIONAL_ENTROPY", 0.8 ]
    - [ "PSI_COLLAPSE_OPERATOR", 0.7 ]
formal_mappings:
  candidates:
    - target: Hausdorff dimension, Box-counting dimension
      domain: Math
      mapping_kind: conceptual
      equation_hint: |
        N(ε) ∝ ε⁻ᴰ (Box-counting relation)
      justification: |
        The Pirouette `D` is an information-theoretic analogue to geometric fractal dimensions. Where methods like box-counting measure how a system's spatial 'mass' scales with resolution, `D` measures how its informational 'mass' (minimum description length) scales with compression fidelity. They are conceptually identical measures of complexity and self-similarity applied to different domains.
      references:
        - title: The Fractal Geometry of Nature
          where: B. B. Mandelbrot, W. H. Freeman and Co.
          date: 1982-01-01
      confidence: 0.9
  adopted:
    - target: Information Dimension
      rationale: The Information Dimension is a formal concept from information theory that measures how the Shannon entropy of a discrete random variable scales with the size of the partition, making it the most direct formal analog to the Pirouette `D`'s measurement via compression.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The fractal dimension `D`, measured via ψ-collapse, is a universal and consistent metric of coherence across all informational manifolds (e.g., genomic, semantic, rhythmic)."
      domain: phenomenology
      falsifier: "Discovery of a system where `D` is not a stable power-law, or where its value contradicts the system's known organizational complexity (e.g., a highly-ordered crystal having a `D` value higher than a chaotic gas)."
      status: supported
      links: [DOMA-056]
naming_notes:
  collisions: [Standard mathematical fractal dimensions (Hausdorff, box-counting, etc.).]
  disambiguation: |
    While mathematically analogous to geometric fractal dimensions, the Pirouette `D` is specifically an *informational* measure derived from compressibility, not a spatial one. It applies to any data set that can be represented as a bit stream, not just geometric shapes.
crosslinks:
  near_synonyms: [INFORMATIONAL_COMPRESSIBILITY]
  antonyms: [INFORMATIONAL_ENTROPY]
  prerequisites: [COHERENCE, CORE-013]
  downstream_effects: [MODULATED_INTERFERENCE, WOUND_CHANNEL_MEMORY, HARMONIC_RESONANCE, GRAVITATIONAL_THUMPER]
license: CC-BY-SA-4.0
---

# Fractal Dimension

## Canonical (Pirouette)
The fractal dimension `D` is a dimensionless scalar that quantifies a system's informational coherence. It is derived from the scaling relationship between fidelity and data rate when the system's information is compressed by the ψ-collapse operator. A low `D` indicates high coherence, order, and redundancy (near-crystalline structure), while a high `D` indicates low coherence and high informational entropy (near-randomness).

## EFT-First Summary
In standard mathematical terms, `D` is an information dimension. It is an information-theoretic analogue to the geometric Hausdorff or box-counting dimension, quantifying the scaling of a system's information content with respect to compression fidelity. This connects the abstract Pirouette concept of Coherence to the well-understood field of fractal geometry and information theory, providing a direct, measurable index of a system's complexity and self-similarity.

## Glossary Links
- See also: Coherence, Informational Entropy