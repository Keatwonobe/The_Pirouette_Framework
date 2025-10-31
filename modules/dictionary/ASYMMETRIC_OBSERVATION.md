---
term: "Asymmetric Observation"
canonical_id: "ASYMMETRIC_OBSERVATION"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-PHYS-003_the_obs_sail"]
---

---
term: Asymmetric Observation
canonical_id: ASYMMETRIC_OBSERVATION
symbol: ∇V_obs
aliases: [Measurement-Induced Force, Observation Steering, Mass-Measure]
parents: [DOMA-PHYS-003_the_OBS-SAIL]
children: [DOMA-PHYS-OBS-SAIL-APPX, DOMA-QCOMP-001]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-PHYS-003_the_OBS-SAIL
      lines: "19-21"
      snippet: |
        Spatially/basis-asymmetric observation (different weak which-way gains on selected arms) produces an
        asymmetric interference envelope → net momentum transfer → steady deflection of a compliant sail.
  editors: [Gemini-Class Agent]
  review_log: []
triad:
  art: |
    Ripples from two timed claps arrive in a lopsided rhythm, leaning a paper sail. The clapping chose which ripples survived to meet the sail; that choice is a map, and maps move things.
  law: |
    A gradient in the local strength of which-way measurement (∇V_obs ≠ 0) across a coherent system induces a net momentum transfer whose sign is determined by the geometry of the gradient. Reversing the gradient must reverse the sign of the induced force.
  philosophy: |
    Directed work can be extracted from measurement back-action alone, without applying a net conservative force. This demonstrates that information flow—who knows what, and how well—has direct, steerable mechanical consequences, with the thermodynamic cost paid entirely within the observer's apparatus.
pirouette_definition: |
  The application of weak measurements with non-uniform strength (V_obs(x)) across the paths or basis states of a coherent system. The resulting gradient in V_obs creates an asymmetric Shadow, reshaping the system's interference envelope and inducing a net momentum transfer or drift. This allows measurement back-action to be harnessed as a directional force, with its sign and magnitude controlled by the observer's geometry and information acquisition rate.
operational_definition:
  units: Force (N) or Momentum transfer (kg·m/s)
  symbol_table:
    - name: k(x)
      meaning: Local measurement strength or gain.
      dimensions: T⁻¹
      default_range: contextual
    - name: g_i
      meaning: Dimensionless measurement gain on path `i`.
      dimensions: dimensionless
      default_range: "[0, g_max]"
    - name: Δx
      meaning: Measured physical deflection, proxy for force.
      dimensions: L
      default_range: "nm – µm"
    - name: Δp
      meaning: Net momentum transfer.
      dimensions: MLT⁻¹
      default_range: contextual
  measurement:
    procedures:
      - name: Electron Observation Sail (EOS)
        outline: |
          A coherent electron beam is passed through a multi-slit aperture (e.g., a triad). Weak which-way detectors are applied with unequal gain (g₁, g₂, g₃=0) to different slits. The resulting far-field interference pattern is measured for momentum shift, and a nanocantilever sail is used to directly measure the induced recoil force (Δx). The key test is observing a sign-flip in Δx when the pattern of observation gains is rotated.
        expected_signals: [Mean cantilever deflection Δx proportional to information rate (g·B), sign-flip of Δx upon swapping observed arms, hysteresis loop in Δx vs. g (Agreement Curve).]
        pitfalls: [Thermal/mechanical crosstalk from measurement hardware (use blank tests), beam current instability masking the effect, symmetric observation (g₁=g₂=g₃) yielding a non-zero force, indicating a systemic artifact.]
context_windows:
  - module: DOMA-PHYS-003_the_OBS-SAIL
    excerpt: |
      Goal: Show that “mass-measure” (many small, directional measurements) can steer a system like a sail, by turning measurement back-action into a biased drift or recoil. Claim: Spatially/basis-asymmetric observation (different weak which-way gains on selected arms) produces an asymmetric interference envelope → net momentum transfer → steady deflection of a compliant sail. No additional conservative force on the plant is required.
  - module: DOMA-PHYS-003_the_OBS-SAIL
    excerpt: |
      The weak meters raise V_obs on selected arms, lowering usable coherence there (ΔKτ < 0 locally). The triad geometry (Triadic Lock) converts that asymmetric Shadow into an asymmetric phase map. The far-field intensity—and thus momentum flow—follows the agreement geometry. The sail feels a recoil whose sign encodes “who is allowed to know” (which arms observed).
poetic_connections:
  motifs: [observation sail, measurement as rudder, information as force, shadow steering, who knows what]
  evocative_lines:
    - "Your clapping *chose* which ripples live long enough to meet me."
    - "The sail feels a recoil whose sign encodes 'who is allowed to know'."
    - "Maps move things."
  association_matrix:
    - [ "SHADOW_GAUGE", 0.9 ]
    - [ "AGREEMENT_GEOMETRY", 0.8 ]
    - [ "TRIADIC_LOCK", 0.7 ]
    - [ "ZENO_WALL", 0.5 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Position-dependent Lindbladian
      domain: AMO
      mapping_kind: mathematical
      equation_hint: |
        dρ/dt = -i/ħ [H, ρ] + ∫ dx k(x)·D[c(x)]ρ
      justification: |
        This formalism directly models an open quantum system where the measurement/decoherence rate k(x) varies spatially. The gradient in k(x) produces a non-uniform diffusion in the Wigner picture, which manifests as a directed drift force, capturing the core physical mechanism.
      references:
        - title: Quantum Measurement and Control
          where: Wiseman & Milburn, Cambridge University Press
          date: 2010-01-01
      rationale: "This provides a direct, standard theoretical basis for converting non-uniform information acquisition into a mechanical force via back-action."
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "Applying unequal weak which-way measurement gains to the arms of a coherent matter-wave interferometer induces a net momentum transfer."
      domain: experiment
      falsifier: "The system's momentum is invariant to the geometry of observation, or any measured deflection tracks only detector power/beam current, not the information-theoretic gain `g` or its spatial arrangement."
      status: proposed
      links: [DOMA-PHYS-003_the_OBS-SAIL]
    - statement: "The direction of the induced force can be reversed by swapping which arms are observed, while holding total beam power and mean detector power constant."
      domain: experiment
      falsifier: "No sign-flip is observed upon swapping the observed arms under matched gain conditions."
      status: proposed
      links: [DOMA-PHYS-003_the_OBS-SAIL]
naming_notes:
  collisions: [Observer effect (too general), Measurement back-action (too general)]
  disambiguation: |
    `Asymmetric Observation` refers specifically to the intentional engineering of a *gradient* in measurement strength to produce a directed force. It is distinct from the generic, and often isotropic, decoherence caused by an environment, and also distinct from projective (strong) measurement which collapses the wavefunction.
crosslinks:
  near_synonyms: [MEASUREMENT_INDUCED_RATCHET, QUANTUM_ZENO_PUMP]
  antonyms: [ISOTROPIC_DECOHERENCE, GLOBAL_MEASUREMENT]
  prerequisites: [WEAK_MEASUREMENT, COHERENCE, BACK_ACTION]
  downstream_effects: [AGREEMENT_GEOMETRY, OBSERVATION_SAIL]
license: CC-BY-SA-4.0
---

# Asymmetric Observation

## Canonical (Pirouette)
The application of weak measurements with non-uniform strength (V_obs(x)) across the paths or basis states of a coherent system. The resulting gradient in V_obs creates an asymmetric Shadow, reshaping the system's interference envelope and inducing a net momentum transfer or drift. This allows measurement back-action to be harnessed as a directional force, with its sign and magnitude controlled by the observer's geometry and information acquisition rate.

## EFT-First Summary
Asymmetric Observation is physically realized as a system coupled to a measurement apparatus described by a Lindblad master equation where the dissipation (decoherence) rate `k(x)` is spatially dependent. The gradient `∂x k(x)` induces non-uniform diffusion in phase space, which manifests as a directed drift or force. This provides a direct, operational link between information acquisition rates and mechanical work. (Ref: Wiseman & Milburn, 2010).

## Glossary Links
- See also: [[Weak Measurement]], [[Back-Action]], [[Shadow Gauge]], [[Observation Sail]]