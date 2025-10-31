---
term: "Coherence Height"
canonical_id: "COHERENCE_HEIGHT"
symbol: "𝓛_p,m"
aliases: [Ta]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-185"]
---

---
term: Coherence Height
canonical_id: COHERENCE_HEIGHT
symbol: 𝓛_p,m
aliases: [Ta]
parents: [DOMA-185, CORE-006]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-185
      snippet: |
        | **Coherence Height (𝓛_p,m)** | The absolute value of the Pirouette Lagrangian at the mode's peak. This measures the instantaneous quality, efficiency, and purity of the state's resonance. | `Ta` |
  editors: [Weaver-Alpha]
  review_log: []
triad:
  art: |
    The brilliance of a state's song, measured by how high its peak rises from the landscape of possibility. It is the clarity of a bell's tone, the focus of a mind, the unwavering flame in the dark.
  law: |
    For any stable mode `m` identified as a local maximum on the Coherence Manifold, its Coherence Height 𝓛_p,m is the absolute value of the Pirouette Lagrangian 𝓛_p evaluated at that maximum. A higher 𝓛_p,m corresponds to greater instantaneous efficiency and lower intrinsic dissonance for that mode.
  philosophy: |
    Coherence Height separates a state's transient perfection from its historical inertia. It asserts that not all stable states are equal; some are simply better, more efficient solutions to the prevailing conditions. This measure allows the Weaver to assess not just a system's habits, but the quality of those habits.
pirouette_definition: |
  The Coherence Height is a scalar quantity representing the absolute value of the Pirouette Lagrangian (𝓛_p) evaluated at the peak of a stable mode (`m`) on the Coherence Manifold. It is a direct measure of the instantaneous quality, resonant purity, and operational efficiency of that mode, independent of its stability against perturbations. A higher value signifies a more coherent, well-defined, and less internally dissonant state.
operational_definition:
  units: Dimensionless (by convention, 𝓛_p is normalized)
  symbol_table:
    - name: 𝓛_p,m
      meaning: Coherence Height of a specific mode `m`.
      dimensions: dimensionless
      default_range: "[0, ∞)"
    - name: 𝓛_p
      meaning: The Pirouette Lagrangian.
      dimensions: dimensionless
      default_range: "(-∞, +∞)"
    - name: m
      meaning: Index identifying a unique stable mode in the system's Resonant Repertoire.
      dimensions: N/A
      default_range: contextual
  measurement:
    procedures:
      - name: Manifold Peak Evaluation
        outline: |
          1. Construct the system's Coherence Manifold by evaluating the Pirouette Lagrangian `𝓛_p` over the relevant dimensions of the system's state space. This can be done empirically via system probing or analytically from a model.
          2. Identify local maxima on this manifold, corresponding to the system's stable modes (`m`).
          3. The Coherence Height `𝓛_p,m` is the absolute value of `𝓛_p` at the coordinates of each identified maximum.
        expected_signals: [Time-series data of core state variables, spectral analysis peaks indicating Ki_m patterns, low-variance plateaus in state-space plots.]
        pitfalls: [Insufficient state-space sampling leading to missed or aliased modes. High manifold dimensionality obscuring clear peaks. Conflating sensor noise with intrinsic mode dissonance.]
context_windows:
  - module: DOMA-185
    excerpt: |
      A crucial distinction is made between a state's instantaneous quality and its historical, ingrained stability. **Coherence Height (𝓛_p,m)**: The absolute value of the Pirouette Lagrangian at the mode's peak. This measures the instantaneous quality, efficiency, and purity of the state's resonance.
  - module: DOMA-185
    excerpt: |
      A system's state does not move on a landscape of energy, but on a **Coherence Manifold**, where the "elevation" at any point is the value of its **Pirouette Lagrangian (𝓛_p)**. A system naturally seeks to climb this landscape to maximize its coherence over time. Modal Basins: Each stable mode is a peak or a high plateau on this manifold...
  - module: DOMA-185
    excerpt: |
      Weaver's Protocol: Cartography of Resonance.
      1. Identify the Repertoire...
      2. Measure Coherence Height: For each identified mode, quantify its internal efficiency and stability (`𝓛_p,m`). This measures the "quality" of each state.
      3. Gauge Stability & Inertia...
poetic_connections:
  motifs: [peak, height, purity, clarity, resonance, efficiency, brilliance]
  evocative_lines:
    - "A system naturally seeks to climb this landscape to maximize its coherence over time."
    - "...the collection of viable, self-sustaining songs it has learned to sing."
    - "The Atlas reveals the repertoire of a system's possible futures..."
  association_matrix:
    - [ "PIRUOUETTE_LAGRANGIAN", 0.9 ]
    - [ "COHERENCE_MANIFOLD", 0.8 ]
    - [ "MODAL_KI", 0.7 ]
    - [ "STABILITY_DEPTH", 0.6 ]
formal_mappings:
  candidates:
    - target: Q-factor (Quality factor)
      domain: CM
      mapping_kind: conceptual
      justification: |
        The Q-factor of a resonator measures the sharpness of its resonance, indicating low energy dissipation and thus a "high-quality" oscillation. Coherence Height similarly quantifies the "purity" and "efficiency" of a system's resonant mode, representing its intrinsic performance quality.
      confidence: 0.6
    - target: -V(φ_min)
      domain: EFT
      mapping_kind: mathematical
      equation_hint: |
        𝓛_p,m ⇔ -V(φ_min)
      justification: |
        In QFT, stable vacua are local minima of an effective potential V(φ). The value of V at a minimum is a fundamental parameter of that vacuum state (e.g., related to vacuum energy). Coherence Height is analogously the value of the governing function (the Lagrangian) at a local maximum (as Pirouette maximizes 𝓛_p), defining a core property of that state.
      references:
        - title: An Introduction To Quantum Field Theory
          where: Chapter 11, "Spontaneous Symmetry Breaking"
          date: 1995-10-11
      confidence: 0.7
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "A mode with a higher Coherence Height `𝓛_p,m` will exhibit lower intrinsic energy dissipation (higher efficiency) per cycle compared to a mode with a lower `𝓛_p,m`, all other factors being equal."
      domain: phenomenology
      falsifier: "Observing a system where a mode identified with a high `𝓛_p,m` is demonstrably less efficient (e.g., requires more energy input to sustain, or has a faster un-driven decay rate) than another mode with a lower `𝓛_p,m`."
      status: proposed
      links: [DOMA-185, CORE-006]
naming_notes:
  collisions: [The historical alias 'Ta' is generic and deprecated to avoid collision with terms for Temperature (T) or time constants (τ).]
  disambiguation: |
    Coherence Height (`𝓛_p,m`) is an *absolute* measure of a mode's peak value on the Coherence Manifold, indicating its instantaneous quality. Do not confuse it with Stability Depth (`Δ𝓛_p`), which is a *relative* measure—the height of the peak relative to the surrounding saddles—indicating its resistance to perturbation. A state can possess very high quality (high `𝓛_p,m`) but be very unstable (low `Δ𝓛_p`).
crosslinks:
  near_synonyms: []
  antonyms: [DISSONANCE, TURBULENT_FLOW]
  prerequisites: [PIROUETTE_LAGRANGIAN, COHERENCE_MANIFOLD, MODAL_KI]
  downstream_effects: [STABILITY_DEPTH, STATE_TRANSITION]
license: CC-BY-SA-4.0
---

# Coherence Height

## Canonical (Pirouette)
The Coherence Height is a scalar quantity representing the absolute value of the Pirouette Lagrangian (𝓛_p) evaluated at the peak of a stable mode (`m`) on the Coherence Manifold. It is a direct measure of the instantaneous quality, resonant purity, and operational efficiency of that mode, independent of its stability against perturbations. A higher value signifies a more coherent, well-defined, and less internally dissonant state.

## EFT-First Summary
Conceptually analogous to the negative value of an effective potential `-V(φ)` at a local minimum (a stable vacuum) in Effective Field Theory. While EFTs minimize a potential, the Pirouette framework maximizes the Lagrangian; thus, Coherence Height is the value of `𝓛_p` at a stable maximum. It quantifies a key intrinsic property of a system's mode, much like the potential's value at a vacuum sets fundamental scales or energy densities for that state of the system.

## Glossary Links
- See also: Stability Depth (Δ𝓛_p), Coherence Manifold, Pirouette Lagrangian (𝓛_p)