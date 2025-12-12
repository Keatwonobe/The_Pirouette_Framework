---
term: "Observation Sail"
canonical_id: "OBSERVATION_SAIL"
symbol: ""
aliases: [Electron Observation Sail, EOS]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-PHYS-003_the_obs_sail"]
---

---
term: Observation Sail
canonical_id: OBSERVATION_SAIL
symbol: 
aliases: [Electron Observation Sail, EOS]
parents: [DOMA-Γ-000, DOMA-SHADOW-001, MATH-011]
children: [DOMA-PHYS-OBS-SAIL-APPX, DOMA-QCOMP-001]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-PHYS-003_the_obs_sail
      lines: "§1"
      snippet: |
        Goal: Show that “mass-measure” (many small, directional measurements) can steer a system like a sail, by turning
        measurement back-action into a biased drift or recoil.
  editors: [Pirouette Framework Agent]
  review_log: []
triad:
  art: |
    Ripples from three canals meet in a pond where a paper boat floats. Two friends clap softly by two canals, choosing which waves interfere. The boat drifts, pushed not by a hand, but by a map of attention.
  law: |
    A spatially asymmetric weak measurement applied to a coherent system induces an asymmetric interference pattern. This asymmetry corresponds to a net momentum transfer, producing a directional force on a coupled mechanical element, whose sign and magnitude are controlled by the measurement geometry and information rate.
  philosophy: |
    Directed work can be extracted from a system by modulating local coherence, without applying a net conservative force. The act of observation, by shaping what can be known, becomes a tool for steering. Maps move things.
pirouette_definition: |
  An actuator that generates a net directional force by asymmetrically modulating local coherence via weak measurement. The device converts the back-action from which-way information gathering into a momentum imbalance in a coherent system (e.g., an electron beam), causing a recoil that propels a physical sail. The effect's magnitude scales with the information rate, and its direction is controlled by the geometry of the observation.
operational_definition:
  units: Newtons (N) for force, meters (m) for deflection.
  symbol_table:
    - name: Δx
      meaning: Mean cantilever deflection
      dimensions: L
      default_range: nm to μm
    - name: gᵢ
      meaning: Dimensionless weak measurement gain on arm i
      dimensions: dimensionless
      default_range: 0–1
    - name: R
      meaning: Information rate proxy (gain × bandwidth)
      dimensions: T⁻¹
      default_range: contextual
    - name: 𝒜
      meaning: Area of hysteresis loop in Δx vs g plot
      dimensions: L
      default_range: contextual
  measurement:
    procedures:
      - name: Asymmetric Gain Sweep
        outline: |
          A coherent electron beam is passed through a triadic aperture. Weak which-way sensors on two of the three paths are activated with variable gain `g`, while the third is unobserved. A nanocantilever placed in the far-field diffraction pattern measures the resulting momentum transfer as a deflection `Δx`. The gain `g` is swept up and down, and the process is repeated with different pairs of arms observed.
        expected_signals: [DC cantilever deflection `Δx`, Hysteresis loop in `Δx(g)`, Asymmetric far-field diffraction pattern]
        pitfalls: [Thermal drift, Mechanical crosstalk from measurement electronics, Beam current instability mimicking the signal]
context_windows:
  - module: DOMA-PHYS-003_the_obs_sail
    excerpt: |
      Claim: Spatially/basis-asymmetric observation (different weak which-way gains on selected arms) produces an
      asymmetric interference envelope → net momentum transfer → steady deflection of a compliant sail. No additional
      conservative force on the plant is required; energy accounting resides in the measurement chain and record handling.
  - module: DOMA-PHYS-003_the_obs_sail
    excerpt: |
      The weak meters raise V_obs on selected arms, lowering usable coherence there (ΔKτ < 0 locally).
      The triad geometry (Triadic Lock) converts that asymmetric Shadow into an asymmetric phase map.
      The far-field intensity—and thus momentum flow—follows the agreement geometry.
      The sail feels a recoil whose sign encodes “who is allowed to know” (which arms observed).
poetic_connections:
  motifs: [measurement as a rudder, shadow steering, information force, choice as a map]
  evocative_lines:
    - "Your clapping *chose* which ripples live long enough to meet me."
    - "Maps move things."
    - "The sail feels a recoil whose sign encodes 'who is allowed to know'."
  association_matrix:
    - [ "SHADOW_GAUGE", 0.9 ]
    - [ "TRIADIC_LOCK", 0.8 ]
    - [ "AGREEMENT_GEOMETRY", 0.8 ]
    - [ "ZENOS_WALL", 0.5 ]
formal_mappings:
  candidates:
    - target: Measurement-induced drift in a Lindblad master equation
      domain: AMO|Math
      mapping_kind: mathematical
      equation_hint: |
        μ(x) ∝ ∂x D(x), where D(x) is a position-dependent diffusion rate set by the local measurement strength k(x).
      justification: |
        The force on the sail is a manifestation of the drift term that arises in the Wigner function dynamics for a system under continuous, spatially-varying weak measurement. An asymmetric measurement strength `k(x)` creates a non-zero gradient in the induced diffusion `D(x)`, which generates a net drift velocity `μ(x)` or force.
      references:
        - title: "Observation Sail: Converting Measurement Back-Action into Directed Motion"
          where: DOMA-PHYS-003_the_obs_sail, §2
          date: 2025-10-18
      confidence: 0.95
  adopted:
    - target: Measurement-induced drift in a Lindblad master equation
      rationale: The source module explicitly derives the sail's propulsion from this mechanism. It provides a direct, falsifiable mathematical and physical basis for the observed effect.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "Mean cantilever deflection is non-zero and its sign flips when the observed pair of arms is swapped."
      domain: experiment
      falsifier: "Deflection is zero, or its sign is invariant under the swapping of observed arms at matched gains."
      status: proposed
      links: [DOMA-PHYS-003_the_obs_sail]
    - statement: "Deflection magnitude increases with information rate (gain × bandwidth) at constant beam power."
      domain: experiment
      falsifier: "Deflection only tracks detector power draw or beam current, independent of information-theoretic parameters."
      status: proposed
      links: [DOMA-PHYS-003_the_obs_sail]
    - statement: "A plot of deflection vs. measurement gain (ramped up and down) exhibits a finite hysteresis loop."
      domain: experiment
      falsifier: "No hysteresis loop is detectable above the noise floor."
      status: proposed
      links: [DOMA-PHYS-003_the_obs_sail]
naming_notes:
  collisions: [Solar sail, Light sail]
  disambiguation: |
    An Observation Sail is not a radiation pressure sail. It is propelled by the back-action of information acquisition, not by direct momentum transfer from a particle beam. Its thrust can be steered by changing the measurement geometry while holding beam power constant.
crosslinks:
  near_synonyms: [MEASUREMENT_INDUCED_RATCHET, QUANTUM_ZENO_PUMP]
  antonyms: [CONSERVATIVE_FORCE_FIELD]
  prerequisites: [SHADOW_GAUGE, TRIADIC_LOCK, WEAK_MEASUREMENT]
  downstream_effects: [AGREEMENT_GEOMETRY]
license: CC-BY-SA-4.0
---

# Observation Sail

## Canonical (Pirouette)
An actuator that generates a net directional force by asymmetrically modulating local coherence via weak measurement. The device converts the back-action from which-way information gathering into a momentum imbalance in a coherent system (e.g., an electron beam), causing a recoil that propels a physical sail. The effect's magnitude scales with the information rate, and its direction is controlled by the geometry of the observation.

## EFT-First Summary
The Observation Sail is an experimental realization of a measurement-induced drift force, formally described by the Lindblad master equation for a system under continuous, spatially-dependent weak measurement. The applied force `F` is proportional to the spatial gradient of the measurement-induced diffusion `D(x)`, which is in turn set by the asymmetric geometry of the weak which-way detectors. This provides a direct link between information acquisition and mechanical work.

## Glossary Links
- See also: [SHADOW_GAUGE](./SHADOW_GAUGE.md), [TRIADIC_LOCK](./TRIADIC_LOCK.md), [AGREEMENT_GEOMETRY](./AGREEMENT_GEOMETRY.md)