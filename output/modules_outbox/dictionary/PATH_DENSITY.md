---
term: "Path Density"
canonical_id: "PATH_DENSITY"
symbol: "δ"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-140"]
---

---
term: Path Density
canonical_id: PATH_DENSITY
symbol: δ
aliases: []
parents: [DOMA-140]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-140
      snippet: |
        **Path Density (δ):** The inverse of an entity's "mean-free path." A high path density signifies a region of intense interaction where movement is restricted and paths are short.
  editors: [Weaver-Agent-7]
  review_log: []
triad:
  art: |
    Where paths tangle and footsteps overwrite one another, the world grows thick with presence. It is the measure of a system's claustrophobia, the friction of being.
  law: |
    Path Density (δ) is the reciprocal of the mean divergence between consecutive states in a trajectory. It quantifies the frequency of interaction or significant change per unit of path length.
  philosophy: |
    Path Density reveals the texture of a system's confinement; it quantifies not the walls themselves, but the crowdedness of the space between them. A high δ indicates a space where every step is a negotiation, and freedom of movement is sacrificed for local coherence.
pirouette_definition: |
  A component of Confinement Strength (κ_G) that measures the degree of path restriction and interaction frequency within a given region of state space. Path Density is calculated as the inverse of the mean path divergence (the system's "mean-free path") between consecutive states in a trajectory. A high value (δ → ∞) indicates short, tightly constrained paths and frequent interactions, while a low value (δ → 0) indicates long, unrestricted paths with infrequent interactions.
operational_definition:
  units: Inverse length [L⁻¹] or inverse semantic distance [S⁻¹]
  symbol_table:
    - name: δ
      meaning: Path Density
      dimensions: L⁻¹ or S⁻¹
      default_range: (0, ∞)
    - name: mean_path_divergence
      meaning: The average distance (spatial or semantic) between consecutive states in a trajectory.
      dimensions: L or S
      default_range: (0, ∞)
    - name: ε
      meaning: A small positive constant to prevent division by zero, representing a minimal resolvable path length.
      dimensions: L or S
      default_range: "> 0, implementation-dependent"
  measurement:
    procedures:
      - name: Sliding Window Divergence Inversion
        outline: |
          1. Vectorize an ordered stream of events (e.g., particle positions, word embeddings) into a state space.
          2. Define a sliding window of N events.
          3. Within the window, calculate the divergence (e.g., Euclidean distance, cosine distance) between each consecutive pair of state vectors.
          4. Compute the mean of these N-1 divergence values.
          5. Calculate δ as the reciprocal of this mean, adding a small regularization constant ε to the denominator: `δ = 1 / (mean_path_divergence + ε)`.
        expected_signals: [High δ in ideological echo chambers, particle-in-a-box systems, or high-friction environments. Low δ during free-fall, open-ended exploration, or low-interaction regimes.]
        pitfalls: [The choice of window size (N) can smooth or exaggerate density features. The vectorization method and divergence metric must be appropriate for the domain to yield meaningful results.]
context_windows:
  - module: DOMA-140
    excerpt: |
      **Path Density (δ):** The inverse of an entity's "mean-free path." A high path density signifies a region of intense interaction where movement is restricted and paths are short.
  - module: DOMA-140
    excerpt: |
      Calculate Path Density (δ): Within a sliding window, compute the average semantic or spatial divergence between consecutive events. The inverse of this value (plus a small epsilon to prevent division by zero) is the Path Density, δ.
poetic_connections:
  motifs: [friction, viscosity, entanglement, claustrophobia, crowdedness, maze]
  evocative_lines:
    - "We sought to measure the strength of the cage and instead learned how to draw a map of its walls."
  association_matrix:
    - [ "CONFINEMENT_STRENGTH", 0.9 ]
    - [ "COHERENCE_CURVATURE", 0.5 ]
    - [ "MEAN_PATH_DIVERGENCE", -1.0 ]
    - [ "TEMPORAL_PRESSURE", 0.3 ]
formal_mappings:
  candidates:
    - target: Inverse mean free path (1/λ)
      domain: CM
      mapping_kind: operational
      equation_hint: |
        δ ≡ 1 / ⟨divergence⟩ ≈ 1 / λ = nσ
      justification: |
        Path Density is operationally defined as the inverse of the mean path length between interactions (divergence events). This is a direct conceptual and mathematical analogue to the inverse of the mean free path (λ) in condensed matter physics, which represents the probability of a scattering event per unit path length. A high δ signifies a short mean free path.
      references:
        - title: "Introduction to Solid State Physics"
          where: "Ch. 5: Phonons I. Crystal Vibrations"
          date: 2004-11-11
      confidence: 0.9
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "In any bounded system, an increase in the number of interacting agents or the strength of their interaction potential will produce a corresponding increase in the system's average Path Density (δ)."
      domain: phenomenology
      falsifier: "An observation of a system where agent count or interaction strength increases but the mean path divergence between state transitions remains constant or increases."
      status: proposed
      links: [DOMA-140]
naming_notes:
  collisions: [The symbol δ is overloaded in physics and mathematics (e.g., Kronecker delta, Dirac delta function, variation operator). Context is critical.]
  disambiguation: |
    Path Density (δ) measures the *frequency* of steps, not their change in direction. It must be distinguished from Coherence Curvature (γ), its partner in calculating Confinement Strength. A trajectory can have high δ and low γ (e.g., a random walk with tiny steps) or low δ and high γ (e.g., a planet in a wide, stable orbit).
crosslinks:
  near_synonyms: [INTERACTION_FREQUENCY]
  antonyms: [MEAN_PATH_DIVERGENCE]
  prerequisites: [VECTORIZATION, STATE_SPACE_MODEL]
  downstream_effects: [CONFINEMENT_STRENGTH]
license: CC-BY-SA-4.0
---

# Path Density

## Canonical (Pirouette)
A component of Confinement Strength (κ_G) that measures the degree of path restriction and interaction frequency within a given region of state space. Path Density is calculated as the inverse of the mean path divergence (the system's "mean-free path") between consecutive states in a trajectory. A high value (δ → ∞) indicates short, tightly constrained paths and frequent interactions, while a low value (δ → 0) indicates long, unrestricted paths with infrequent interactions.

## EFT-First Summary
Path Density (δ) is operationally analogous to the inverse mean free path (1/λ) in condensed matter physics or statistical mechanics. It quantifies the probability of a scattering-like event (a significant state change) per unit of path length in a system's state space. A high δ indicates a system where trajectories are short and frequently interrupted, akin to a particle moving through a dense medium with a high scattering cross-section. It is a direct measure of how "crowded" or "viscous" a local region of state space is.

## Glossary Links
- See also: Confinement Strength, Coherence Curvature, Gladiator Compass