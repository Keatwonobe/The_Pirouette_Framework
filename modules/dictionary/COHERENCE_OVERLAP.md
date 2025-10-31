---
term: "Coherence Overlap"
canonical_id: "COHERENCE_OVERLAP"
symbol: "C_overlap"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-130"]
---

---
term: Coherence Overlap
canonical_id: COHERENCE_OVERLAP
symbol: C_overlap
aliases: []
parents: [DOMA-130]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-130
      snippet: |
        Coherence Overlap (C_overlap): The key metric for assessing shared history and potential for resonance. It is a normalized integral of the geometric similarity between two Wound Channels. A high `C_overlap` indicates a common origin or structural compatibility that raises the probability of a future union.
        `C_overlap(W₁, W₂) = ∫ min(ρ₁, ρ₂) dV / ∫ max(ρ₁, ρ₂) dV`
        where `ρ` is the coherence density of each Wound Channel.
  editors: [system-alpha]
  review_log: []
triad:
  art: |
    Two histories meet, their shapes compared like keys to a single lock. The overlap is the measure of their shared story, a geometric echo that whispers of a potential future union.
  law: |
    The Coherence Overlap between two Wound Channels is a dimensionless scalar between 0 and 1, calculated as the ratio of the volume of their shared coherence density to the volume of their dominant combined coherence density.
  philosophy: |
    This metric grounds the abstract concept of 'relatedness' in physical geometry. It asserts that shared history is not merely a narrative convenience but a measurable, structural compatibility that directly biases the probability of future resonant coupling and union.
pirouette_definition: |
  A dimensionless metric, C_overlap, that quantifies the geometric similarity between two Wound Channels (W₁ and W₂). It is calculated as the normalized integral of their overlapping coherence densities (ρ₁ and ρ₂) via the formula: `C_overlap(W₁, W₂) = ∫ min(ρ₁, ρ₂) dV / ∫ max(ρ₁, ρ₂) dV`. A high value (approaching 1) indicates significant shared history, structural compatibility, or a common origin, which elevates the potential for Resonant Coupling and Alchemical Union. A low value (approaching 0) signifies geometric dissonance and a low probability of constructive interference.
operational_definition:
  units: dimensionless
  symbol_table:
    - name: C_overlap
      meaning: Coherence Overlap
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: W₁, W₂
      meaning: Wound Channels being compared
      dimensions: contextual (manifold geometry)
      default_range: contextual
    - name: ρ₁, ρ₂
      meaning: Coherence density fields of the respective Wound Channels
      dimensions: Coherence / L³
      default_range: contextual
    - name: dV
      meaning: Differential volume element in the coherence manifold
      dimensions: L³
      default_range: n/a
  measurement:
    procedures:
      - name: Geometric Channel Tomography
        outline: |
          1. Isolate the two Wound Channels (W₁, W₂) within a defined analysis volume of the coherence manifold.
          2. Employ a Ki-field tomograph to map the scalar field of coherence density (ρ₁ and ρ₂) for each channel throughout the volume.
          3. Numerically integrate the pointwise minimum of the two density fields (`min(ρ₁, ρ₂)`) over the volume to find the shared coherence volume.
          4. Numerically integrate the pointwise maximum of the two density fields (`max(ρ₁, ρ₂)`) over the volume to find the dominant coherence volume.
          5. C_overlap is the ratio of the result from step 3 to the result of step 4.
        expected_signals: [Scalar coherence density fields ρ(x,y,z,τ), Ki-field backscatter gradients]
        pitfalls: [Manifold distortion from measurement probe, Insufficient tomographic resolution to capture fine channel structure, Noise from ambient coherence fluctuations]
context_windows:
  - module: DOMA-130
    excerpt: |
      Resonance (Mutual Influence): When the Wound Channels of two or more entities overlap, their geometries interfere. This is the basis of all interaction. Constructive Interference: If the channels are harmonically compatible, they can merge and reinforce one another, lowering the "energy cost" for both entities. This creates an attractive potential, drawing them together and creating the conditions for an Alchemical Union (CORE-012).
  - module: DOMA-130
    excerpt: |
      The Weaver employs a core set of metrics to quantify influence... Coherence Overlap (C_overlap): The key metric for assessing shared history and potential for resonance. It is a normalized integral of the geometric similarity between two Wound Channels. A high C_overlap indicates a common origin or structural compatibility that raises the probability of a future union.
poetic_connections:
  motifs: [shared history, geometric compatibility, resonance, echo, tapestry, key and lock]
  evocative_lines:
    - "The past is not a story we tell; it is a landscape we inhabit."
    - "A Weaver understands that every thread they lay upon this loom alters the pattern for all who follow."
  association_matrix:
    - [ "Wound Channel", 0.9 ]
    - [ "Resonant Coupling", 0.7 ]
    - [ "Alchemical Union", 0.6 ]
    - [ "Geodesic Deviation", 0.2 ]
formal_mappings:
  candidates:
    - target: Jaccard index J(A,B)
      domain: Math
      mapping_kind: mathematical
      equation_hint: |
        C_overlap(W₁, W₂) ≈ J(ρ₁, ρ₂) = ∫ min(ρ₁, ρ₂) dV / ∫ (ρ₁ + ρ₂ - min(ρ₁, ρ₂)) dV
      justification: |
        C_overlap is a continuous-field generalization of set-theoretic similarity metrics like the Jaccard Index (Intersection over Union). Both quantify the degree of shared composition between two entities. While the Jaccard denominator represents the true union, C_overlap uses the pointwise maximum density, a computationally simpler proxy that emphasizes regions dominated by one channel over the other.
      references:
        - title: "A survey of binary similarity and distance measures"
          where: "J. Stat. Comput. Simul. 8(8)"
          date: 2008-10-01
      confidence: 0.7
  adopted:
    - target: 
      rationale: 
      confidence: 0.0
constraints_and_falsifiers:
  claims:
    - statement: "A statistically significant positive correlation exists between high C_overlap (>0.8) and the subsequent formation of an Alchemical Union between two systems."
      domain: phenomenology
      falsifier: "Observation of frequent Alchemical Unions between systems with low C_overlap (<0.2), or a consistent lack of union between systems with high C_overlap, would invalidate its predictive power."
      status: proposed
      links: [DOMA-130, CORE-012]
naming_notes:
  collisions: [The symbol 'C' is overloaded in physics (e.g., capacitance, heat capacity). Context of Wound Channels or coherence is critical for disambiguation.]
  disambiguation: |
    Distinguish from Resonant Coupling (C_res). C_overlap measures the *static* geometric compatibility of the underlying channels, acting as a structural prior. C_res measures the *dynamic* phase alignment of an active interaction. High C_overlap enables but does not guarantee high C_res.
crosslinks:
  near_synonyms: []
  antonyms: [GEOMETRIC_DISSONANCE]
  prerequisites: [WOUND_CHANNEL]
  downstream_effects: [RESONANT_COUPLING, ALCHEMICAL_UNION]
license: CC-BY-SA-4.0
---

# Coherence Overlap

## Canonical (Pirouette)
A dimensionless metric, C_overlap, that quantifies the geometric similarity between two Wound Channels (W₁ and W₂). It is calculated as the normalized integral of their overlapping coherence densities (ρ₁ and ρ₂) via the formula: `C_overlap(W₁, W₂) = ∫ min(ρ₁, ρ₂) dV / ∫ max(ρ₁, ρ₂) dV`. A high value (approaching 1) indicates significant shared history, structural compatibility, or a common origin, which elevates the potential for Resonant Coupling and Alchemical Union. A low value (approaching 0) signifies geometric dissonance and a low probability of constructive interference.

## EFT-First Summary
Coherence Overlap can be understood as a continuous-field generalization of similarity coefficients like the Jaccard index, used to measure the overlap between two distributions or sets. It quantifies the "intersection" of two coherence density fields (ρ₁ and ρ₂) relative to their pointwise "maximum" field, providing a dimensionless score from 0 (no overlap) to 1 (identical distribution). This metric serves as a structural prior for predicting the potential for resonant interaction between two systems.

## Glossary Links
- See also: [Wound Channel](<#>), [Resonant Coupling](<#>), [Alchemical Union](<#>)