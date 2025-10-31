---
term: "Observation Gain"
canonical_id: "OBSERVATION_GAIN"
symbol: "g"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-PHYS-003_the_obs_sail"]
---

---
term: Observation Gain
canonical_id: OBSERVATION_GAIN
symbol: g
aliases: [Measurement Strength]
parents: [DOMA-PHYS-003_the_obs_sail]
children: [DOMA-PHYS-OBS-SAIL-APPX, DOMA-QCOMP-001]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-PHYS-003_the_obs_sail
      lines: "L100-L101"
      snippet: |
        Control Knobs
        - Observation gain g₁, g₂ on two arms; g₃ = 0 on the third.
  editors: [LLM-Curator]
  review_log: []
triad:
  art: |
    Your quiet attention is a choice of which ripples live long enough to meet the sail. That choice is a map, and maps move things. The gain is how intently you watch.
  law: |
    The directed force on a system under asymmetric weak measurement is proportional to the gradient of the observation gain. Its sign is determined by the geometry of observation. A spatially uniform gain (g₁=g₂=g₃) produces no net force.
  philosophy: |
    Observation is not passive reception but an active, world-shaping intervention. The Observation Gain is the control knob for this intervention, demonstrating that the flow of information itself, when structured, can perform directed work, turning "knowing" into "pushing".
pirouette_definition: |
  A dimensionless, tunable parameter, `g`, that sets the strength of a weak measurement on a specific path, subsystem, or basis state. It directly controls the rate of information extraction and the magnitude of the measurement back-action. In the Pirouette formalism, `g` scales the local Observation Potential (`V_obs`), creating a `Shadow` that suppresses coherence and, when applied asymmetrically, generates a net drift or force.
operational_definition:
  units: Dimensionless (control parameter)
  symbol_table:
    - name: g
      meaning: Observation Gain
      dimensions: dimensionless
      default_range: [0, 1] (normalized)
    - name: Δx
      meaning: Cantilever deflection (proxy for force)
      dimensions: L
      default_range: contextual
    - name: B
      meaning: Observation bandwidth
      dimensions: T⁻¹
      default_range: contextual
    - name: R
      meaning: Information rate proxy (R ≈ g⋅B)
      dimensions: T⁻¹
      default_range: contextual
  measurement:
    procedures:
      - name: Asymmetric Gain Sweep (Observation Sail)
        outline: |
          1. Prepare a coherent system with multiple paths (e.g., tri-slit electron beam).
          2. Place a compliant force sensor (e.g., nanocantilever) to intercept an output lobe.
          3. Zero the sensor with all observation gains set to zero (g_i = 0).
          4. Apply weak measurement to a subset of paths (e.g., g₁, g₂ > 0; g₃ = 0).
          5. Slowly sweep `g` from zero to a maximum value and back to zero, recording the sensor's mean deflection Δx as a function of `g`.
          6. The value of `g` is the control voltage or current applied to the weak meter, calibrated against the information extracted (e.g., signal-to-noise ratio of the which-way measurement).
        expected_signals: [Mean deflection Δx(g), Hysteresis loop in Δx vs g (Agreement Curve), Asymmetric shift in far-field interference pattern]
        pitfalls: [Thermal drift mimicking deflection, Beam current fluctuations, Mechanical/electrical crosstalk from the meter to the sensor, Invariant deflection indicating a classical force]
context_windows:
  - module: DOMA-PHYS-003_the_obs_sail
    excerpt: |
      In the Wigner picture, this yields diffusion D(x) ∝ k(x) and an effective drift μ(x) ∝ ∂x D(x). Asymmetric k(x) ⇒ ∂x D ≠ 0 ⇒ net drift. In Pirouette terms, a gradient in V_obs(x) skews (ΔKτ - ΔV_obs), and the system “slides” along the Shadow slope. The Observation Gain `g` is the experimental knob controlling the measurement strength k(x).
  - module: DOMA-PHYS-003_the_obs_sail
    excerpt: |
      KPI-2 (Info Scaling): |Δx| increases with information rate (gain·bandwidth), not merely with detector power draw. KPI-3 (Hysteresis): Clear loop in Δx vs g when ramped up/down—lock-break asymmetry (Handshake signature). This confirms `g` is not just a proxy for dissipated power but for the rate of coherence collapse.
poetic_connections:
  motifs: [attention, choice, shadow, ratchet, steering]
  evocative_lines:
    - "The sail feels a recoil whose sign encodes 'who is allowed to know'."
    - "Your clapping *chose* which ripples live long enough to meet me."
  association_matrix:
    - [ "OBSERVATION_POTENTIAL", 0.9 ]
    - [ "SHADOW", 0.8 ]
    - [ "AGREEMENT_CURVE", 0.7 ]
    - [ "WEAK_MEASUREMENT", 0.9 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Measurement strength/rate `k` or `γ` in Lindblad master equations
      domain: AMO|Quantum Optics
      mapping_kind: mathematical
      equation_hint: |
        dρ/dt = -i/ħ [H, ρ] + g·D[c]ρ
        where D[c]ρ is the Lindblad dissipator for the measured observable `c`.
      justification: |
        The source module's formalism (§2) explicitly models the effect of observation with a Lindblad term where the pre-factor `k(x)` represents the measurement strength. The experimental control parameter `g` is directly proportional to `k(x)`, making it a direct operational analog to the measurement rate in the theory of open quantum systems.
      references:
        - title: Quantum Measurement and Control
          where: Wiseman & Milburn, Cambridge University Press, Ch. 4
          date: 2009-01-01
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "The magnitude of the force induced by asymmetric observation, |Δx|, scales monotonically with the Observation Gain `g` (at fixed bandwidth B)."
      domain: experiment
      falsifier: "The observed deflection |Δx| is invariant to `g`, or scales only with detector power draw, not the product `g⋅B`."
      status: proposed
      links: [DOMA-PHYS-003_the_obs_sail]
    - statement: "Swapping which subsystem is observed (at constant `g`) reverses the sign of the induced force."
      domain: experiment
      falsifier: "The sign of deflection Δx is independent of the observation geometry; no sign flip occurs when swapping observed arms."
      status: proposed
      links: [DOMA-PHYS-003_the_obs_sail]
naming_notes:
  collisions: [The symbol `g` is overloaded in physics (gravitational acceleration, metric tensor, Landé g-factor). Context is critical.]
  disambiguation: |
    Within the Pirouette Framework, `g` as a standalone, lowercase italic symbol almost always refers to Observation Gain. It is a dimensionless control parameter, not a fundamental constant. In equations, it typically appears as a pre-factor to a dissipative or measurement-related term.
crosslinks:
  near_synonyms: [MEASUREMENT_STRENGTH]
  antonyms: [COHERENCE, ISOLATION]
  prerequisites: [WEAK_MEASUREMENT, OBSERVATION_POTENTIAL]
  downstream_effects: [AGREEMENT_CURVE, SHADOW, OBSERVATION_SAIL]
license: CC-BY-SA-4.0
---

# Observation Gain

## Canonical (Pirouette)
A dimensionless, tunable parameter, `g`, that sets the strength of a weak measurement on a specific path, subsystem, or basis state. It directly controls the rate of information extraction and the magnitude of the measurement back-action. In the Pirouette formalism, `g` scales the local Observation Potential (`V_obs`), creating a `Shadow` that suppresses coherence and, when applied asymmetrically, generates a net drift or force.

## EFT-First Summary
Observation Gain `g` is the operational realization of the measurement strength or rate parameter (`k` or `γ`) in the Lindblad master equation formalism for open quantum systems. It functions as the coupling constant between a system and a measurement device's environment. An asymmetric spatial distribution of `g` introduces a non-Hamiltonian, dissipative term that breaks translational symmetry, resulting in a directed force or drift analogous to a ratchet mechanism. This provides a direct link between the information-theoretic concept of measurement and a physical, momentum-transferring effect. (Ref: Wiseman & Milburn, *Quantum Measurement and Control*).

## Glossary Links
- See also: [Weak Measurement](<#>), [Observation Potential](<#>), [Shadow](<#>), [Agreement Curve](<#>)