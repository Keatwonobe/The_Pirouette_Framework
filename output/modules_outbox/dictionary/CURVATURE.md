---
term: "Curvature"
canonical_id: "CURVATURE"
symbol: "κ"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["COG-RES-003"]
---

---
term: Curvature
canonical_id: CURVATURE
symbol: κ
aliases: []
parents: [COG-RES-003, MATH-026]
children: [DOMA-096, MATH-027]
status: draft
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: COG-RES-003
      lines: "§3"
      snippet: |
        The local curvature κ(x,t) of 𝓜₃ encodes coherence tension:
        [κ = det(g)^{1/2}]
  editors: [system-agent]
  review_log: []
triad:
  art: |
    Curvature is the tension in the fabric of awareness. Where this fabric wrinkles or folds, consciousness shifts; where it tears, awareness collapses. It is the geometric grain against which the stream of thought flows.
  law: |
    The local curvature κ of the Triadic Manifold (𝓜₃) must exceed a critical threshold (κ_c) for an awareness transition (bifurcation or collapse) to occur. Below this threshold, awareness follows smooth geodesic paths, representing stable conscious states.
  philosophy: |
    Curvature provides a falsifiable, geometric mechanism for the dynamics of subjective experience. It bridges abstract neural phase relationships to the concrete phenomenology of perceptual shifts and cognitive state changes, formalizing consciousness not as a static property but as motion on a dynamic landscape.
pirouette_definition: |
  A scalar field on the Triadic Manifold (𝓜₃) that quantifies local coherence tension. It is defined as the square root of the determinant of the manifold's metric tensor, κ = det(g)¹/². High values of curvature correspond to regions of instability that predict imminent bifurcations in the path of awareness, such as perceptual transitions or decoherence events. Curvature evolves under a Renormalization Group flow driven by cognitive load (Γ), leading to stable, divergent, or nucleating geometric phases of the manifold.
operational_definition:
  units: dimensionless
  symbol_table:
    - name: κ
      meaning: Local manifold curvature
      dimensions: dimensionless
      default_range: "[0, ∞)"
    - name: 𝓜₃
      meaning: Triadic Manifold
      dimensions: N/A
      default_range: N/A
    - name: g_ij
      meaning: Metric tensor of the Triadic Manifold
      dimensions: dimensionless
      default_range: context-dependent
    - name: Γ
      meaning: Cognitive Load
      dimensions: dimensionless
      default_range: context-dependent
  measurement:
    procedures:
      - name: EEG/MEG Phase Manifold Reconstruction
        outline: |
          1. Identify three Ki-resonant neural oscillatory signals from EEG/MEG data.
          2. Extract their instantaneous phases (Φ₁, Φ₂, Φ₃) over a time window.
          3. Project the resulting phase vectors (Φ₁(t), Φ₂(t), Φ₃(t)) onto the 3-torus (𝕋³), forming a point cloud representation of the local Triadic Manifold 𝓜₃.
          4. Compute the local covariance matrix of these points, serving as an empirical estimate of the metric tensor g_ij.
          5. Calculate curvature κ(t) as the square root of the determinant of the estimated metric tensor.
        expected_signals: [Time-series κ(t) exhibiting sharp peaks that correlate with subject-reported perceptual switches or task-driven cognitive events.]
        pitfalls: [Low signal-to-noise ratio in phase data, ambiguity in selecting the correct resonant triad, non-stationarity of neural dynamics violating manifold assumptions.]
context_windows:
  - module: COG-RES-003
    excerpt: |
      The path of awareness corresponds to a geodesic on 𝓜₃... Points of high curvature correspond to critical bifurcations (awareness transitions or collapse events). The Caduceus Flow later formalized in [DOMA-096] emerges as a laminar–turbulent transition along these geodesics.
  - module: COG-RES-003
    excerpt: |
      As Γ increases, manifold curvature evolves under renormalization:
      [dκ/dlnℓ = β_κ = (2−d)κ − c_1 bκ + c_2 g^2]
      Below critical Γ_c: curvature flows to fixed point κ* (stable awareness).
      At Γ_c: κ diverges, producing manifold tearing (awareness collapse).
poetic_connections:
  motifs: [tension, folding, tearing, resonance, fabric-of-mind, landscape]
  evocative_lines:
    - "At Γ_c: κ diverges, producing manifold tearing (awareness collapse)."
    - "Points of high curvature correspond to critical bifurcations."
  association_matrix:
    - [ "COHERENCE_TENSION", 0.9 ]
    - [ "AWARENESS_TRANSITION", 0.8 ]
    - [ "COGNITIVE_LOAD", 0.7 ]
formal_mappings:
  candidates:
    - target: Ricci Scalar Curvature (R)
      domain: GR|Math
      mapping_kind: conceptual
      equation_hint: |
        Geodesic eq: D²Φⁱ/Dt² + Γⁱⱼₖ(DΦʲ/Dt)(DΦᵏ/Dt) = 0
      justification: |
        In General Relativity, the Ricci scalar R quantifies the intrinsic curvature of spacetime, which in turn governs the geodesic motion of matter. In the Pirouette Framework, κ is a scalar measure of the Triadic Manifold's geometry that governs the geodesic path of awareness. High curvature in both contexts indicates regions of strong dynamic influence and potential instability.
      references:
        - title: General Relativity
          where: Carroll, S. M. (2004)
          date: 2004-01-01
      confidence: 0.7
  adopted:
    - target: Ricci Scalar Curvature (R)
      rationale: The analogy provides a powerful and well-understood mathematical foundation for conceptualizing the dynamics of consciousness as motion within a geometric state space.
      confidence: 0.7
constraints_and_falsifiers:
  claims:
    - statement: "Spikes in manifold curvature κ precede or coincide with subjectively reported awareness transitions."
      domain: phenomenology|experiment
      falsifier: "Time-series analysis of reconstructed κ(t) from EEG/MEG shows no statistically significant correlation with event markers for perceptual shifts (e.g., in binocular rivalry)."
      status: proposed
      links: [COG-RES-003]
    - statement: "The evolution of mean curvature κ follows the RG flow equation `dκ/dlnℓ = β_κ` as cognitive load Γ is parametrically increased."
      domain: experiment
      falsifier: "Experimental manipulation of cognitive load Γ fails to produce the predicted fixed-point or divergent behavior in the measured distribution of κ."
      status: proposed
      links: [COG-RES-003, MATH-026]
naming_notes:
  collisions: [The symbol κ is commonly used for thermal conductivity in thermodynamics and kappa statistics in data analysis.]
  disambiguation: |
    Within the Pirouette Framework, κ always refers to the geometric curvature of a cognitive manifold (e.g., 𝓜₃) derived from the metric tensor of a phase space. It quantifies information-theoretic tension, not thermal energy transfer or statistical agreement.
crosslinks:
  near_synonyms: [COHERENCE_TENSION]
  antonyms: [MANIFOLD_FLATNESS]
  prerequisites: [TRIADIC_MANIFOLD, KI_RESONANCE]
  downstream_effects: [AWARENESS_TRANSITION, CADUCEUS_FLOW, MANIFOLD_TEARING]
license: CC-BY-SA-4.0
---

# Curvature

## Canonical (Pirouette)
A scalar field on the Triadic Manifold (𝓜₃) that quantifies local coherence tension. It is defined as the square root of the determinant of the manifold's metric tensor, κ = det(g)¹/². High values of curvature correspond to regions of instability that predict imminent bifurcations in the path of awareness, such as perceptual transitions or decoherence events. Curvature evolves under a Renormalization Group flow driven by cognitive load (Γ), leading to stable, divergent, or nucleating geometric phases of the manifold.

## EFT-First Summary
In the geometric model of consciousness, Curvature (κ) is the conceptual analogue of the Ricci scalar curvature (R) in General Relativity. It is a local property of the Triadic Manifold—the state space of conscious awareness—that dictates its dynamics. Just as spacetime curvature directs the motion of matter along geodesics, high manifold curvature directs the flow of awareness towards critical transitions or collapse events, providing a formal link between neural geometry and phenomenological change.

## Glossary Links
- See also: [Triadic Manifold](TRIADIC_MANIFOLD), [Awareness Transition](AWARENESS_TRANSITION), [Cognitive Load](COGNITIVE_LOAD), [Caduceus Flow](CADUCEUS_FLOW)