---
term: "Mass-measure"
canonical_id: "MASS_MEASURE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-PHYS-003_the_obs_sail"]
---

---
term: Mass-measure
canonical_id: MASS_MEASURE
symbol: μ_obs
aliases: [Observation Sail principle, Measurement-induced drift]
parents: [DOMA-PHYS-003_the_OBS-SAIL]
children: [DOMA-PHYS-OBS-SAIL-APPX, DOMA-QCOMP-001]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-PHYS-003_the_obs_sail
      lines: "L15-L17"
      snippet: |
        Goal: Show that “mass-measure” (many small, directional measurements) can steer a system like a sail, by turning
        measurement back-action into a biased drift or recoil.
  editors: [System Agent]
  review_log: []
triad:
  art: |
    The clapping of two friends by two canals—but not a third—chooses which ripples live to meet a floating sail. The choice is a map, and maps move things.
  law: |
    Spatially asymmetric weak measurement of a coherent system induces a net momentum transfer whose direction is determined by the measurement geometry and whose magnitude scales with the information acquisition rate.
  philosophy: |
    Directed work can be produced by modulating local coherence and observer geometry, without adding a net classical force. This reframes measurement not as a passive disturbance but as an active, steerable actuator, where the 'cost' of work is paid in the information-processing chain.
pirouette_definition: |
  The principle of steering a system's dynamics by applying a multitude of small, directional measurements to induce a biased drift or recoil. By asymmetrically raising V_obs (observation potential) across a system's configuration space, a gradient is created in the Shadow landscape. The system's evolution is then biased to 'slide' along this gradient, converting information flow into directed momentum or work.
operational_definition:
  units: m/s (drift velocity) or N (induced force)
  symbol_table:
    - name: μ(x)
      meaning: Measurement-induced drift velocity at position x
      dimensions: L T⁻¹
      default_range: nm/s to μm/s (contextual)
    - name: k(x)
      meaning: Spatially-dependent weak measurement strength (gain)
      dimensions: dimensionless
      default_range: 0 to 1
    - name: R
      meaning: Information acquisition rate
      dimensions: T⁻¹
      default_range: contextual (e.g., bits/s)
  measurement:
    procedures:
      - name: Electron Observation Sail (EOS) Method
        outline: |
          A coherent electron beam is passed through a triadic aperture. Weak, tunable which-way measurements (gain g₁, g₂) are applied to two of the three paths, with the third unobserved. A nanocantilever "sail" intercepts a far-field interference lobe. The mean deflection of the cantilever (Δx) is recorded as a function of the asymmetric gain `g`. The sign of the deflection must flip when the pair of observed arms is swapped.
        expected_signals: [Mean cantilever deflection Δx, Asymmetric shift in far-field diffraction pattern, Hysteresis loop in Δx vs. g]
        pitfalls: [Thermal/mechanical crosstalk from detectors, Deflection tracking beam power instead of measurement geometry, Lack of sign-flip when swapping observed arms]
context_windows:
  - module: DOMA-PHYS-003_the_obs_sail
    excerpt: |
      Goal: Show that “mass-measure” (many small, directional measurements) can steer a system like a sail, by turning
      measurement back-action into a biased drift or recoil.
      Claim: Spatially/basis-asymmetric observation (different weak which-way gains on selected arms) produces an
      asymmetric interference envelope → net momentum transfer → steady deflection of a compliant sail. No additional
      conservative force on the plant is required.
  - module: DOMA-PHYS-003_the_obs_sail
    excerpt: |
      In Pirouette terms, a gradient in V_obs(x) skews (ΔKτ - ΔV_obs),
      and the system “slides” along the Shadow slope. The weak meters raise V_obs on selected arms, lowering usable coherence there (ΔKτ < 0 locally). The triad geometry (Triadic Lock) converts that asymmetric Shadow into an asymmetric phase map.
poetic_connections:
  motifs: [observer effect, ratchet, sail, shadow_gauge, agreement_geometry]
  evocative_lines:
    - "Your clapping *chose* which ripples live long enough to meet me."
    - "That choice is a map. Maps move things."
  association_matrix:
    - [ "SHADOW_GAUGE", 0.9 ]
    - [ "AGREEMENT_GEOMETRY", 0.8 ]
    - [ "ZENO_WALL", 0.5 ]
formal_mappings:
  candidates:
    - target: Fokker-Planck drift μ(x)
      domain: Math|CM
      mapping_kind: mathematical
      equation_hint: |
        μ(x) ∝ ∂x D(x)
      justification: |
        In a phase-space representation like the Wigner picture, the effect of continuous weak measurement can be described by a Fokker-Planck equation. The gradient of the measurement-induced diffusion coefficient D(x) generates a non-conservative drift force, which is the classical manifestation of the mass-measure principle.
      references:
        - title: Quantum Measurement and Control
          where: "H. M. Wiseman & G. J. Milburn, Ch. 4"
          date: 2009-12-10
      confidence: 0.9
    - target: Lindblad dissipator D[c]ρ
      domain: Math|AMO
      mapping_kind: mathematical
      equation_hint: |
        dρ/dt = ... + ∫ dx k(x)·(c(x)ρc(x)† - ½{c(x)†c(x), ρ})
      justification: |
        The Lindblad master equation describes the unconditional evolution of an open quantum system. Mass-measure arises from a Lindblad term where the measurement operator `c(x)` and its strength `k(x)` are spatially dependent, making the decoherence inhomogeneous and thus directional.
      references:
        - title: "As above"
          where: "As above"
          date: 2009-12-10
      confidence: 0.9
  adopted:
    []
constraints_and_falsifiers:
  claims:
    - statement: "Asymmetric weak measurement induces a directional force whose sign flips when the measurement geometry is swapped."
      domain: experiment
      falsifier: "The measured force is invariant to the choice of which subsystems are measured (e.g., swapping observed arms produces no sign flip in deflection)."
      status: proposed
      links: [DOMA-PHYS-003_the_obs_sail]
    - statement: "The magnitude of the induced force scales with the information acquisition rate, not merely with the power dissipated by the measurement apparatus."
      domain: experiment
      falsifier: "The force correlates only with the total power drawn by the detectors, irrespective of how that power is used to gain information."
      status: proposed
      links: [DOMA-PHYS-003_the_obs_sail]
naming_notes:
  collisions: [Mass (physics), Measure (mathematics)]
  disambiguation: |
    The term 'Mass-measure' does not refer to the measurement of mass. 'Mass' is used in the sense of 'a large quantity' or 'in the aggregate', referring to the multitude of small quantum measurements. The effect is a recoil from the 'mass' of many weak observations.
crosslinks:
  near_synonyms: [MEASUREMENT_INDUCED_RATCHET, QUANTUM_ZENO_PUMP]
  antonyms: [CONSERVATIVE_FORCE, UNITARY_EVOLUTION]
  prerequisites: [SHADOW_GAUGE, TRIADIC_LOCK, AGREEMENT_GEOMETRY]
  downstream_effects: [FORCE_FREE_ACTUATION]
license: CC-BY-SA-4.0
---

# Mass-measure

## Canonical (Pirouette)
The principle of steering a system's dynamics by applying a multitude of small, directional measurements to induce a biased drift or recoil. By asymmetrically raising V_obs (observation potential) across a system's configuration space, a gradient is created in the Shadow landscape. The system's evolution is then biased to 'slide' along this gradient, converting information flow into directed momentum or work.

## Formal-First Summary
Mass-measure is the net drift induced by a spatially inhomogeneous measurement process. Mathematically, it arises from a Lindblad master equation with a position-dependent measurement strength `k(x)`. In a phase-space representation, this generates a drift velocity `μ(x)` proportional to the spatial gradient of the measurement-induced diffusion, `∂x D(x)`, as described in standard theories of quantum measurement and control.

## Glossary Links
- See also: [Measurement-Induced Ratchet](<#>), [Shadow Gauge](<#>), [Triadic Lock](<#>)