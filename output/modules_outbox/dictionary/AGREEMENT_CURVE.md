---
term: "Agreement Curve"
canonical_id: "AGREEMENT_CURVE"
symbol: ""
aliases: [Handshake signature]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-PHYS-003_the_obs_sail"]
---

---
term: Agreement Curve
canonical_id: AGREEMENT_CURVE
symbol: 𝒜_g
aliases: [Handshake signature]
parents: [DOMA-PHYS-003_the_obs_sail]
children: [DOMA-QCOMP-001]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-PHYS-003_the_obs_sail
      lines: "§3.3.D, §4"
      snippet: |
        D. Hysteresis: sweep g up and down quasi-adiabatically to capture lock/unlock loop area (the Agreement Curve).
        ...
        Primary observable: time-averaged Δx(g) with confidence bands; report loop area 𝒜 = ∮ Δx d g (Agreement Curve).
  editors: [Agent:Text-gen-v1]
  review_log: []
triad:
  art: |
    An observer claps, and the ripples from that choice lean a floating sail. The path of the clapping hands—approaching and receding—leaves a memory in the water, an echo of a choice that became a map, and the map moved the sail.
  law: |
    A system under spatially asymmetric observation exhibits a hysteresis loop in its physical response (e.g., deflection Δx) when the observation gain (g) is swept up and then down. The loop area, 𝒜_g = ∮ Δx dg, must be non-zero, reproducible, and dependent on the observation geometry.
  philosophy: |
    The curve's existence reveals that the observer-system interaction is not instantaneous; it has memory. The system's state depends not just on the current observation strength, but on the history of that interaction, signifying the formation and dissolution of a shared observer-system manifold, or "agreement."
pirouette_definition: |
  A plot of a system's steady-state response (e.g., the deflection Δx of an Observation Sail) versus a swept parameter of observation, typically the dimensionless gain `g`. The defining feature is a non-zero loop area, `𝒜_g = ∮ Δx dg`, when the gain is ramped from zero to a maximum value and back to zero. This hysteresis demonstrates a memory effect, where the observer-system state becomes "locked" into a specific geometry (the agreement), which persists on the downward sweep to a different gain value than where it formed. `𝒜_g` quantifies the work per cycle associated with forming and breaking this observer-system coherence.
operational_definition:
  units: [Length] · [Gain_Units]. If gain `g` is dimensionless, the units are meters (m).
  symbol_table:
    - name: 𝒜_g
      meaning: Area enclosed by the Agreement Curve.
      dimensions: L (if gain is dimensionless)
      default_range: "> 0 for a confirmed effect"
    - name: Δx
      meaning: System response variable, e.g., cantilever deflection.
      dimensions: L
      default_range: "nm – μm"
    - name: g
      meaning: Dimensionless observation gain on the metered channels.
      dimensions: dimensionless
      default_range: "[0, 1]"
  measurement:
    procedures:
      - name: Quasi-adiabatic gain sweep
        outline: |
          1. Apply an asymmetric observation geometry to a test system (e.g., an Observation Sail).
          2. Stabilize all other parameters (e.g., beam current). Zero the response metric (Δx = 0 at g = 0).
          3. Slowly ramp the observation gain `g` from 0 to a maximum value `g_max`, continuously recording the steady-state system response Δx.
          4. Immediately and at the same rate, ramp the gain `g` from `g_max` back to 0, again recording Δx.
          5. Plot Δx vs. g for both the up-ramp and down-ramp. The area enclosed by the two traces is 𝒜_g.
        expected_signals: [A closed loop in the (g, Δx) plane with statistically significant non-zero area.]
        pitfalls: [Thermal drift creating a false loop, mechanical backlash in actuators, sweep rate being too fast (non-adiabatic) leading to transient artifacts instead of true hysteresis.]
context_windows:
  - module: DOMA-PHYS-003_the_obs_sail
    excerpt: |
      KPI-3 (Hysteresis): Clear loop in Δx vs g when ramped up/down—lock-break asymmetry (Handshake signature).
  - module: DOMA-PHYS-003_the_obs_sail
    excerpt: |
      Hysteresis is the memory of a shared manifold forming and breaking (Handshake/Agreement Curve). The sail feels a recoil whose sign encodes “who is allowed to know” (which arms are observed).
poetic_connections:
  motifs: [memory, handshake, echo, path-dependence, lock-break]
  evocative_lines:
    - "Hysteresis is the memory of a shared manifold forming and breaking."
    - "Your clapping *chose* which ripples live long enough to meet me."
  association_matrix:
    - [ "SHADOW_GAUGE", 0.8 ]
    - [ "TRIADIC_LOCK", 0.7 ]
    - [ "OBSERVATION_SAIL", 0.9 ]
formal_mappings:
  candidates:
    - target: Hysteresis loop (e.g., B-H curve)
      domain: CM
      mapping_kind: conceptual
      equation_hint: |
        𝒜_g = ∮ Δx(g) dg  <-->  W = ∮ M(H) dH
      justification: |
        Both the Agreement Curve and magnetic hysteresis plot a system's response (deflection Δx / magnetization M) to an external driving field (observation gain g / magnetic field H). The non-zero loop area in both cases represents work done or energy dissipated per cycle and indicates a memory effect where the system's state depends on its history.
      references:
        - title: Physics of Ferromagnetism
          where: Sōshin Chikazumi, Chapter 1
          date: 1997-01-01
      confidence: 0.8
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The area `𝒜_g = ∮ Δx d g` is non-zero and its sign depends on the choice of observation geometry for any system where asymmetric measurement can induce a directional bias."
      domain: experiment
      falsifier: "The measured loop area is zero within noise (Falsifier F-3), or the area is shown to arise from environmental artifacts like thermal drift or mechanical creep by failing blank-gun control tests."
      status: proposed
      links: [DOMA-PHYS-003_the_obs_sail]
naming_notes:
  collisions: [The symbol `𝒜` is commonly used for Area in many contexts.]
  disambiguation: |
    Distinguish from simple mechanical or thermal hysteresis. An Agreement Curve is specific to observer effects and must be modulated by changes in measurement basis or geometry (e.g., swapping which arms are observed), not just by the presence of power.
crosslinks:
  near_synonyms: [HANDSHAKE_SIGNATURE]
  antonyms: [OBSERVATIONALLY_REVERSIBLE_RESPONSE]
  prerequisites: [SHADOW_GAUGE, TRIADIC_LOCK, V_OBS]
  downstream_effects: [OBSERVATION_SAIL, ZENO_WALL]
license: CC-BY-SA-4.0
---

# Agreement Curve

## Canonical (Pirouette)
A plot of a system's steady-state response (e.g., the deflection Δx of an Observation Sail) versus a swept parameter of observation, typically the dimensionless gain `g`. The defining feature is a non-zero loop area, `𝒜_g = ∮ Δx dg`, when the gain is ramped from zero to a maximum value and back to zero. This hysteresis demonstrates a memory effect, where the observer-system state becomes "locked" into a specific geometry (the agreement), which persists on the downward sweep to a different gain value than where it formed. `𝒜_g` quantifies the work per cycle associated with forming and breaking this observer-system coherence.

## EFT-First Summary
The Agreement Curve is a phenomenon conceptually analogous to magnetic or ferroelectric hysteresis in condensed matter physics. Just as a B-H curve plots magnetization (a system response) against an applied H-field (a driving force) and reveals memory and energy loss through its loop area, the Agreement Curve plots a physical response (e.g., momentum) against observation strength. The non-zero area signifies that information extraction and the resulting back-action perform work on the system in a path-dependent way, indicating the formation of a metastable, shared state between the observer and the system.

## Glossary Links
- See also: [Handshake signature](link-to-handshake-signature), [Observation Sail](link-to-observation-sail), [Shadow Gauge](link-to-shadow-gauge)