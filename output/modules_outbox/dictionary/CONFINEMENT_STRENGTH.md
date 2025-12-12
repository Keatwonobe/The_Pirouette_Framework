---
term: "Confinement Strength"
canonical_id: "CONFINEMENT_STRENGTH"
symbol: "κ_G"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-140"]
---

---
term: Confinement Strength
canonical_id: CONFINEMENT_STRENGTH
symbol: κ_G
aliases: []
parents: [DOMA-140]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-140
      lines: "§3"
      snippet: |
        To provide a clear, practical metric, the instrument's output is defined as Confinement Strength (κ_G). The subscript `G` signifies that this is an inferred quantity derived from the geometric effects of the Gladiator Force. The core mechanic is an elegant product of two key metrics.

        **Confinement Strength (κ_G) = Path Density (δ) × Coherence Curvature (γ)**
  editors: [autogenerator-p1, Weaver.A]
  review_log: []
triad:
  art: |
    A measure of the steepness of an arena's walls. It is the surveyor's tool for mapping the invisible architecture of control, revealing the cage not by its bars, but by the frantic, curved paths of those trapped within.
  law: |
    Confinement Strength is the product of Path Density (the inverse of mean-free path) and Coherence Curvature (the rate of change in a trajectory's direction). A high value indicates paths are both short and sharply bent, the geometric signature of a strong confining potential.
  philosophy: |
    To measure confinement is not to measure a force, but to survey the landscape forged by that force. Making the structures of stability and control visible is the first and necessary step toward navigating, reinforcing, or dismantling them. It transforms abstract forces into a concrete map.
pirouette_definition: |
  The primary metric output by the Gladiator Compass, Confinement Strength (κ_G) is a dimensionless or inverse-area quantity that measures the local intensity of a confinement well (i.e., the Gladiator effect). It is an inferred geometric property derived from system trajectories, calculated as the product of Path Density (δ) and Coherence Curvature (γ). A high κ_G value is the signature of a deep potential well in the Pirouette Lagrangian, indicating that a system's geodesics are being tightly constrained by a strong, self-reinforcing feedback loop.
operational_definition:
  units: Dimensionless or inverse area (e.g., L⁻²). The specific units depend on whether path divergence and windowing are measured over space, time, or a semantic manifold.
  symbol_table:
    - name: κ_G
      meaning: Confinement Strength
      dimensions: "L⁻² or T⁻² or dimensionless"
      default_range: "[0, ∞), with values > 1 indicating significant confinement"
    - name: δ
      meaning: Path Density, the inverse of mean path divergence.
      dimensions: "L⁻¹ or T⁻¹ or dimensionless"
      default_range: "contextual"
    - name: γ
      meaning: Coherence Curvature, the gradient of the coherence metric.
      dimensions: "L⁻¹ or T⁻¹ or dimensionless"
      default_range: "contextual"
  measurement:
    procedures:
      - name: Gladiator Compass Protocol
        outline: |
          1. Ingest an ordered stream of system states and vectorize them.
          2. Within a sliding window, calculate the mean divergence between consecutive states. Path Density (δ) is the inverse of this value.
          3. Within the same window, calculate the rate of change of the trajectory's direction. This is the Coherence Curvature (γ).
          4. Compute κ_G = δ × γ for the window.
          5. Plot the κ_G-field over the system's state space to identify local maxima, which correspond to the centers of confinement wells.
        expected_signals: [Local maxima in the κ_G field, steep gradients at the edges of confinement wells.]
        pitfalls: [Choosing an inappropriate window size (too large blurs features, too small amplifies noise), poor vectorization that misses the relevant dynamics, noisy data creating spurious curvature signals.]
context_windows:
  - module: DOMA-140
    excerpt: |
      A high κ_G value emerges where paths are both short (high δ) and sharply bent (high γ). This is the unambiguous signature of a confinement well—the heart of an arena.
  - module: DOMA-140
    excerpt: |
      The Gladiator Compass does not measure the fundamental Temporal Pressure (Γ) of the Temporal Forge (`CORE-003`). Instead, it functions as an **inverse solver for the Pirouette Lagrangian (`CORE-006`)**. A high inferred Confinement Strength (κ_G) implies the presence of a deep "potential well" (a high V_Γ) in the Lagrangian.
poetic_connections:
  motifs: [arena walls, gravity well, surveying, geodesic, cage, map, chains]
  evocative_lines:
    - "We sought to measure the strength of the cage and instead learned how to draw a map of its walls."
    - "It does not infer a force; it surveys the landscape forged by that force."
  association_matrix:
    - [ "GLADIATOR_FORCE", 0.9 ]
    - [ "PIROUETTE_LAGRANGIAN", 0.8 ]
    - [ "COGNITIVE_GRAVITY_WELL", 0.7 ]
    - [ "TEMPORAL_PRESSURE", 0.4 ]
formal_mappings:
  candidates:
    - target: Ricci scalar curvature (R)
      domain: GR
      mapping_kind: conceptual
      equation_hint: |
        κ_G ∝ R
      justification: |
        Both quantities measure the intrinsic curvature of a manifold which dictates the behavior of geodesics. In GR, mass-energy curves spacetime (high R), forcing particles to follow curved paths. In Pirouette, a Gladiator Force warps the coherence manifold (high κ_G), forcing systems along curved trajectories.
      references:
        - title: General Relativity
          where: Carroll, S. M., Chapter 3
          date: 2004-01-01
      confidence: 0.7
    - target: Laplacian of a potential (∇²V)
      domain: CM
      mapping_kind: mathematical
      equation_hint: |
        κ_G ∝ ∇²V
      justification: |
        In potential theory (e.g., Poisson's equation ∇²Φ = 4πGρ), the Laplacian of the potential is proportional to the source density. κ_G similarly measures the intensity of the "source" of confinement by observing its effect on trajectories, analogous to how a test particle's acceleration reveals ∇V.
      references: []
      confidence: 0.6
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "Systems or regions exhibiting high, stable κ_G values will demonstrate lower rates of state-space exploration and novelty generation than those with low κ_G."
      domain: phenomenology
      falsifier: "The discovery of a system that consistently generates high rates of novel behavior (e.g., high innovation output, rapid evolution) while simultaneously being measured to have a high and stable Confinement Strength."
      status: proposed
      links: [DOMA-140]
naming_notes:
  collisions: [The symbol κ is commonly used for curvature in differential geometry and for thermal/hydraulic conductivity in physics. The subscript `G` is essential to specify the Gladiator-derived context.]
  disambiguation: |
    Distinguish κ_G from the Gladiator Force itself. κ_G is not the force, but a geometric *effect* of the force on system trajectories. It is an inferred property of the *landscape*, not a direct measurement of the "charge" or "field" creating it.
crosslinks:
  near_synonyms: [COGNITIVE_GRAVITY_WELL]
  antonyms: [TRAJECTORY_FREEDOM, CREATIVE_FLATNESS]
  prerequisites: [PATH_DENSITY, COHERENCE_CURVATURE, PIROUETTE_LAGRANGIAN, GLADIATOR_FORCE]
  downstream_effects: [SYSTEM_STABILITY, IDEOLOGICAL_ENTRENCHMENT, COHERENCE_LOCK]
license: CC-BY-SA-4.0
---

# Confinement Strength

## Canonical (Pirouette)
The primary metric output by the Gladiator Compass, Confinement Strength (κ_G) is a dimensionless or inverse-area quantity that measures the local intensity of a confinement well (i.e., the Gladiator effect). It is an inferred geometric property derived from system trajectories, calculated as the product of Path Density (δ) and Coherence Curvature (γ). A high κ_G value is the signature of a deep potential well in the Pirouette Lagrangian, indicating that a system's geodesics are being tightly constrained by a strong, self-reinforcing feedback loop.

## EFT-First Summary
Confinement Strength is conceptually analogous to the Ricci scalar curvature (R) in General Relativity. Where R measures the curvature of spacetime induced by mass-energy, κ_G measures the curvature of a system's coherence manifold induced by a Gladiator Force. Both quantities are inferred from the observed deviation of geodesics from straight paths, providing a local measure of how intensely a system's behavior is constrained by the geometry of its environment. High κ_G, like high R, signifies a deep "gravity well" that traps trajectories.

## Glossary Links
- See also: Gladiator Compass, Gladiator Force, Pirouette Lagrangian, Path Density, Coherence Curvature