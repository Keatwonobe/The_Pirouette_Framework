---
term: "Weak Which-Way Measurement"
canonical_id: "WEAK_WHICH_WAY_MEASUREMENT"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-PHYS-003_the_obs_sail"]
---

---
term: Weak Which-Way Measurement
canonical_id: WEAK_WHICH_WAY_MEASUREMENT
symbol: g, M_w
aliases: [weak measurement, non-destructive probe, continuous measurement]
parents: [DOMA-PHYS-003_the_OBS-SAIL]
children: [DOMA-QCOMP-001, DOMA-PHYS-OBS-SAIL-APPX]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-PHYS-003_the_OBS-SAIL
      lines: "L7-L12"
      snippet: |
        A coherent electron beam passes a triadic aperture and weak which-way sensors are enabled
        asymmetrically. The change in information flow reshapes interference, creating a measurable
        momentum imbalance that pushes a nanocantilever “sail.”
  editors: [system-agent]
  review_log: []
triad:
  art: |
    Softly clapping by two of three canals chooses which ripples survive to meet a floating paper sail. The pattern of your attention is a map, and maps move things.
  law: |
    An asymmetry in measurement gain (g₁, g₂, ...) across a set of coherent paths induces a net momentum transfer Δp, whose sign is determined by the geometry of observation. The effect vanishes for globally symmetric observation (g₁=g₂=g₃).
  philosophy: |
    The act of gaining information is not a passive event but an active shaping of physical reality. By choosing *what* to know and *where*, an observer imparts a bias onto a system's evolution, demonstrating that information geometry is a direct cause of physical dynamics.
pirouette_definition: |
  A non-projective measurement that gains partial information about a system's state in a specific basis (e.g., position or path) while preserving a significant fraction of its coherence in a conjugate basis. Operationally, it locally raises the Observer Potential (V_obs), suppressing the local kinetic cost of coherence (ΔKτ). When applied asymmetrically, the resulting gradient in V_obs creates a bias in the system's dynamics, effectively "steering" it along a slope in the Shadow manifold defined by the Agreement Geometry.
operational_definition:
  units: Gain `g` is typically dimensionless. Information rate `R` is in `bits·s⁻¹` or a proxy (e.g., detected `photons·s⁻¹`).
  symbol_table:
    - name: g
      meaning: Dimensionless gain of a weak meter, parameterizing the strength of the measurement coupling.
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: k(x)
      meaning: Local measurement strength density.
      dimensions: Varies with measurement type.
      default_range: contextual
    - name: R
      meaning: Information acquisition rate, proportional to g·B (gain·bandwidth).
      dimensions: T⁻¹
      default_range: contextual
  measurement:
    procedures:
      - name: Asymmetric Interference Deflection
        outline: |
          1. Prepare a coherent particle beam (e.g., electrons at 10-100 keV).
          2. Pass the beam through a multi-path aperture (e.g., a triadic nano-slit).
          3. Place tunable weak meters (e.g., QPCs or secondary electron collectors) on a subset of the paths (e.g., paths 1 and 2, but not 3).
          4. Ramp the gain `g` of the active meters.
          5. Measure the resulting shift in the far-field interference pattern's center-of-momentum (Δp_x) or the deflection (Δx) of a compliant physical probe (a "sail").
        expected_signals: [DC cantilever deflection Δx, Far-field intensity pattern shift]
        pitfalls: [Thermal or electromagnetic crosstalk from meter electronics to the probe, Beam current instability masquerading as a force]
context_windows:
  - module: DOMA-PHYS-003_the_OBS-SAIL
    excerpt: |
      Spatially/basis-asymmetric observation (different weak which-way gains on selected arms) produces an
      asymmetric interference envelope → net momentum transfer → steady deflection of a compliant sail. No additional
      conservative force on the plant is required; energy accounting resides in the measurement chain and record handling.
  - module: DOMA-PHYS-003_the_OBS-SAIL
    excerpt: |
      The weak meters raise V_obs on selected arms, lowering usable coherence there (ΔKτ < 0 locally).
      The triad geometry (Triadic Lock) converts that asymmetric Shadow into an asymmetric phase map.
      The far-field intensity—and thus momentum flow—follows the agreement geometry.
      The sail feels a recoil whose sign encodes “who is allowed to know” (which arms observed).
poetic_connections:
  motifs: [observer as actuator, information as force, asymmetric knowing, steering by seeing]
  evocative_lines:
    - "Your clapping *chose* which ripples live long enough to meet me."
    - "Maps move things."
  association_matrix:
    - [ "OBSERVER_POTENTIAL", 0.9 ]
    - [ "SHADOW", 0.8 ]
    - [ "AGREEMENT_GEOMETRY", 0.8 ]
    - [ "TRIADIC_LOCK", 0.7 ]
formal_mappings:
  candidates:
    - target: Lindblad Master Equation (decoherence term)
      domain: AMO
      mapping_kind: mathematical
      equation_hint: |
        dρ/dt = ... + k(x)·(c(x)ρc(x)† - ½{c(x)†c(x), ρ})
      justification: |
        This formalism models the continuous, non-projective evolution of an open quantum system. The Lindblad term, scaled by strength k(x), represents the decoherence induced by the continuous measurement of an observable c(x), precisely capturing the dynamics of a weak which-way measurement without wave function collapse.
      references:
        - title: "The Theory of Open Quantum Systems"
          where: "Breuer & Petruccione, Oxford University Press"
          date: 2002-01-01
      confidence: 0.95
  adopted:
    - target: Lindblad Master Equation (decoherence term)
      rationale: The source module (DOMA-PHYS-003_the_OBS-SAIL) explicitly uses this formalism to model the effect. It is the standard theoretical tool for this physical regime.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "Asymmetric weak which-way measurement gain induces a directional momentum transfer, whose sign depends on the geometry of observation."
      domain: experiment
      falsifier: "Measured momentum transfer is invariant when swapping the observed paths, or is zero when it should be non-zero (F-2, F-4 from DOMA-PHYS-003)."
      status: proposed
      links: [DOMA-PHYS-003_the_OBS-SAIL]
    - statement: "The magnitude of the induced momentum transfer scales with the information acquisition rate (gain·bandwidth), not merely the power dissipated by the measurement apparatus."
      domain: experiment
      falsifier: "Momentum transfer correlates only with the total power draw of the detectors and is unchanged when the measurement basis is altered at constant power (F-1, KPI-4 from DOMA-PHYS-003)."
      status: proposed
      links: [DOMA-PHYS-003_the_OBS-SAIL]
naming_notes:
  collisions: [Weak Value]
  disambiguation: |
    "Weak Measurement" as used here refers to any minimally disturbing, non-projective measurement that extracts partial information. This is a broader category than the specific protocol of pre-selection, weak interaction, and post-selection used to measure an anomalous "Weak Value" as defined by Aharonov, Albert, and Vaidman.
crosslinks:
  near_synonyms: [QUANTUM_NON_DEMOLITION_MEASUREMENT]
  antonyms: [PROJECTIVE_MEASUREMENT, VON_NEUMANN_MEASUREMENT]
  prerequisites: [COHERENCE, INTERFERENCE]
  downstream_effects: [OBSERVATION_SAIL, SHADOW, MEASUREMENT_INDUCED_RATCHET]
license: CC-BY-SA-4.0
---

# Weak Which-Way Measurement

## Canonical (Pirouette)
A non-projective measurement that gains partial information about a system's state in a specific basis (e.g., position or path) while preserving a significant fraction of its coherence in a conjugate basis. Operationally, it locally raises the Observer Potential (V_obs), suppressing the local kinetic cost of coherence (ΔKτ). When applied asymmetrically, the resulting gradient in V_obs creates a bias in the system's dynamics, effectively "steering" it along a slope in the Shadow manifold defined by the Agreement Geometry.

## EFT-First Summary
A Weak Which-Way Measurement is modeled in the language of open quantum systems as a localized decoherence channel. Its effect is captured by adding a Lindblad term to the system's master equation of motion. When the strength of this measurement is spatially non-uniform, the corresponding diffusion coefficient in the Wigner representation acquires a gradient, inducing an effective drift force. This provides a standard, thermodynamically consistent mechanism for measurement back-action to perform directed work, as described in standard texts on the subject (e.g., Breuer & Petruccione, 2002).

## Glossary Links
- See also: [Observer Potential](<link>), [Shadow](<link>), [Agreement Geometry](<link>), [Projective Measurement](<link>)