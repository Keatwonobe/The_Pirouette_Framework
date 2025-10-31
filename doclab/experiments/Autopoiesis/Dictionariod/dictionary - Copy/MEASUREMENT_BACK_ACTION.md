---
term: "Measurement Back-Action"
canonical_id: "MEASUREMENT_BACK_ACTION"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-PHYS-003_the_obs_sail"]
---

---
term: Measurement Back-Action
canonical_id: MEASUREMENT_BACK_ACTION
symbol: ΔKτ|obs
aliases: [Observer Effect, Quantum Back-Action, Measurement Disturbance]
parents: [DOMA-PHYS-003_the_obs_sail, DOMA-SHADOW-001]
children: [DOMA-QCOMP-001, MEASUREMENT_INDUCED_RATCHET]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-PHYS-003_the_obs_sail
      lines: "§1"
      snippet: |
        Claim: Spatially/basis-asymmetric observation (different weak which-way gains on selected arms) produces an
        asymmetric interference envelope → net momentum transfer → steady deflection of a compliant sail. No additional
        conservative force on the plant is required...
  editors: [GPT-4_CDE_Agent]
  review_log: []
triad:
  art: |
    A paper sail floats where three canals meet. Clapping softly by two canals but not the third chooses which ripples live long enough to meet the sail. The choice is a map, and maps move things.
  law: |
    Spatially or basis-asymmetric measurement of a coherent quantum system induces a net momentum transfer whose direction and magnitude are functions of the observer's geometry and the rate of information extraction. The system recoils from the act of being known.
  philosophy: |
    The act of gaining information is a physical interaction that necessarily disturbs the subject. This disturbance is not random noise but a structured, non-local recoil that can be engineered to perform directed work, demonstrating that information flow has direct mechanical consequences.
pirouette_definition: |
  The unavoidable physical recoil inflicted on a quantum system by a measurement. In Pirouette, this is modeled as the local imposition of an observation potential (`V_obs`) which creates a `Shadow`, degrading local coherence (`ΔKτ < 0`). Gradients in `V_obs` across a coherent system produce asymmetric interference and a net momentum imbalance, causing the system to "slide" along the gradient of agreement.
operational_definition:
  units: Net momentum transfer (kg⋅m/s) or resulting force (N). Measurement strength is often dimensionless gain `g` or a rate `k(x)` in Hz.
  symbol_table:
    - name: k(x)
      meaning: Local measurement strength/rate of an observable.
      dimensions: T⁻¹
      default_range: contextual
    - name: g
      meaning: Dimensionless gain of a weak which-way detector.
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: Δx
      meaning: Physical displacement of a test object (e.g., cantilever) due to integrated momentum transfer.
      dimensions: L
      default_range: "nm to μm"
    - name: Δp_x
      meaning: Net momentum transferred to the system, inferred from far-field pattern shifts or target deflection.
      dimensions: M L T⁻¹
      default_range: contextual
  measurement:
    procedures:
      - name: Electron Observation Sail (EOS)
        outline: |
          1. Pass a monoenergetic, coherent electron beam through a tri-slit aperture.
          2. Place weak which-way detectors with tunable gain `g` on two of the three paths. Leave the third path unobserved.
          3. Place a sensitive nanocantilever in the far-field interference pattern to act as a "sail."
          4. Sweep the detector gain `g` and record the cantilever's mean deflection `Δx`.
          5. The resulting deflection is a direct measure of the momentum imbalance induced by the asymmetric observation.
        expected_signals: [DC cantilever deflection `Δx(g)`, center-of-momentum shift in far-field diffraction pattern.]
        pitfalls: [Thermal/mechanical detector crosstalk, beam current instability, environmental vibration, conflating information-rate effects with simple power dissipation.]
context_windows:
  - module: DOMA-PHYS-003_the_obs_sail
    excerpt: |
      Goal: Show that “mass-measure” (many small, directional measurements) can steer a system like a sail, by turning
      measurement back-action into a biased drift or recoil. Claim: Spatially/basis-asymmetric observation produces an
      asymmetric interference envelope → net momentum transfer → steady deflection of a compliant sail. No additional
      conservative force on the plant is required; energy accounting resides in the measurement chain and record handling.
  - module: DOMA-PHYS-003_the_obs_sail
    excerpt: |
      The weak meters raise V_obs on selected arms, lowering usable coherence there (ΔKτ < 0 locally).
      The triad geometry (Triadic Lock) converts that asymmetric Shadow into an asymmetric phase map.
      The far-field intensity—and thus momentum flow—follows the agreement geometry.
      The sail feels a recoil whose sign encodes “who is allowed to know” (which arms observed).
poetic_connections:
  motifs: [observation as a sail, information as force, asymmetric knowing, clapping ripples]
  evocative_lines:
    - "Your clapping *chose* which ripples live long enough to meet me."
    - "That choice is a map. Maps move things."
  association_matrix:
    - [ "SHADOW", 0.9 ]
    - [ "AGREEMENT_GEOMETRY", 0.8 ]
    - [ "TRIADIC_LOCK", 0.7 ]
    - [ "HANDSHAKE", 0.6 ]
formal_mappings:
  candidates:
    - target: Lindblad Master Equation (dissipator term)
      domain: AMO
      mapping_kind: mathematical
      equation_hint: |
        dρ/dt = ... + ∫ dx k(x)·(c(x)ρc(x)† - ½{c(x)†c(x), ρ})
      justification: |
        The module explicitly models the effect of weak continuous measurement using a Lindblad dissipator. The measurement strength `k(x)` controls the rate of decoherence and induces both diffusion and a directed drift, which mathematically represents the back-action.
      references:
        - title: Quantum Measurement and Control
          where: Wiseman & Milburn, Ch. 4
          date: 2009-01-01
      confidence: 0.95
  adopted:
    - target: Lindblad Master Equation (dissipator term)
      rationale: This formalism is used directly in the source module's mathematical description (§2) and is the standard tool for modeling the dynamics of open quantum systems under continuous measurement.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "Spatially asymmetric weak measurement of a coherent system induces a directional, non-conservative force."
      domain: experiment
      falsifier: "Measured deflection is invariant to the geometry of observation (i.e., which paths are measured), or its sign does not flip when the observed paths are swapped."
      status: proposed
      links: [DOMA-PHYS-003_the_obs_sail]
    - statement: "The magnitude of the induced force scales with the rate of information extraction, not merely with the power dissipated by the measurement apparatus."
      domain: experiment
      falsifier: "The effect is shown to be purely thermal or electromagnetic crosstalk from detector electronics. For example, the effect persists in a 'blank test' where detectors are powered on but decoupled from the quantum system."
      status: proposed
      links: [DOMA-PHYS-003_the_obs_sail]
naming_notes:
  collisions: [The term "Observer Effect" is used broadly in popular science and can be confused with simple classical disturbance (e.g., a thermometer altering the temperature of a small liquid sample).]
  disambiguation: |
    Distinguish from classical disturbance, where a probe physically contacts and perturbs a system. Quantum Measurement Back-Action is an intrinsic consequence of information gain mandated by quantum mechanics. It can be non-local and is proportional to the information extracted, not necessarily the energy exchanged in the interaction.
crosslinks:
  near_synonyms: [OBSERVER_EFFECT]
  antonyms: [QUANTUM_NON_DEMOLITION_MEASUREMENT]
  prerequisites: [COHERENCE, WEAK_MEASUREMENT, SHADOW]
  downstream_effects: [AGREEMENT_CURVE, ZENO_WALL, MEASUREMENT_INDUCED_RATCHET]
license: CC-BY-SA-4.0
---

# Measurement Back-Action

## Canonical (Pirouette)
The unavoidable physical recoil inflicted on a quantum system by a measurement. In Pirouette, this is modeled as the local imposition of an observation potential (`V_obs`) which creates a `Shadow`, degrading local coherence (`ΔKτ < 0`). Gradients in `V_obs` across a coherent system produce asymmetric interference and a net momentum imbalance, causing the system to "slide" along the gradient of agreement.

## EFT-First Summary
Measurement Back-Action is the physical disturbance a quantum system experiences when measured, as described in the theory of open quantum systems. It is formally modeled by the dissipator (or Lindblad) term in a quantum master equation. This term describes how the system's density matrix `ρ` evolves due to coupling with a measurement apparatus, leading to both decoherence (loss of quantum properties) and often a systematic drift. In the context of the Observation Sail, this drift term generates a real, measurable force.

## Glossary Links
- See also: [Observer Effect](<#>), [Weak Measurement](<#>), [Shadow](<#>), [Agreement Geometry](<#>)