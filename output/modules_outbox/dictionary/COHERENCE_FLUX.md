---
term: "Coherence Flux"
canonical_id: "COHERENCE_FLUX"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-036"]
---

---
term: Coherence Flux
canonical_id: COHERENCE_FLUX
symbol: d𝓛_p/dt
aliases: [Flux Ratio]
parents: [DOMA-036]
children: [INST-NALY-001]
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-036
      snippet: |
        | **Coherence Flux**     | `d𝓛_p/dt`                         | `Flux Ratio`          | Is the system's overall health improving or worsening? What is its trajectory?     |
  editors: [Agent-Writer]
  review_log: []
triad:
  art: |
    The velocity of vitality. It is the palpable swell or fade of a system's song, revealing whether it builds towards a crescendo or collapses into silence.
  law: |
    The time-derivative of a system's Pirouette Lagrangian (d𝓛_p/dt). A positive flux indicates improving systemic health and predicts increasing resilience; a negative flux indicates decay and predicts increasing fragility.
  philosophy: |
    To understand a system is to understand its story. Coherence Flux shifts the analysis from a static snapshot (health *now*) to a dynamic narrative (health's *trajectory*), enabling prediction and intervention before a crisis manifests.
pirouette_definition: |
  The first time-derivative of the Pirouette Lagrangian (𝓛_p), quantifying the rate of change of a system's net vitality. It serves as the primary indicator of a system's health trajectory, measuring whether its capacity to generate coherence is accelerating, decelerating, or stable relative to environmental degradation. A positive flux (d𝓛_p/dt > 0) signals growth or strengthening (anabolism), while a negative flux (d𝓛_p/dt < 0) signals decay (catabolism).
operational_definition:
  units: Coherence-units per second ([𝓛]/[T]). Dimensionally equivalent to power or information rate (e.g., bits/second).
  symbol_table:
    - name: 𝓛_p
      meaning: Pirouette Lagrangian, representing a system's net vitality or "free coherence."
      dimensions: Action or Information (context-dependent)
      default_range: contextual
    - name: t
      meaning: Time
      dimensions: T
      default_range: N/A
  measurement:
    procedures:
      - name: Time-Series Differentiation
        outline: |
          Measure the system's Lagrangian Health (𝓛_p) at a series of time points (t_1, t_2, ..., t_n). Calculate the rate of change by fitting a slope to the data over a relevant time window or by using a finite difference approximation, e.g., (𝓛_p(t_2) - 𝓛_p(t_1)) / (t_2 - t_1).
        expected_signals: [A positive, negative, or near-zero slope in the 𝓛_p timeseries.]
        pitfalls: [Selecting a time window (Δt) that is too short amplifies measurement noise. Selecting a window that is too long obscures short-term dynamics and non-linear trends.]
context_windows:
  - module: DOMA-036
    excerpt: |
      This model provides a clean, actionable set of KPIs for auditing the health of any system. **Coherence Flux (d𝓛_p/dt)** replaces the old `Flux Ratio` and answers the diagnostic question: Is the system's overall health improving or worsening? What is its trajectory?
  - module: DOMA-036
    excerpt: |
      The health of a system is not a static accounting of assets and liabilities, but the moment-to-moment outcome of a single, fundamental struggle... A healthy system is an "entropy pump," actively working to maximize its Lagrangian value over time.
poetic_connections:
  motifs: [trajectory, momentum, growth, decay, acceleration, velocity]
  evocative_lines:
    - "The universe is a constant argument between the song and the static."
    - "Our purpose is to read the score, find the instruments falling out of tune, and help the symphony play on."
  association_matrix:
    - [ "LAGRANGIAN_HEALTH", 0.9 ]
    - [ "PRESSURE_GRADIENT", 0.7 ]
    - [ "ADAPTIVE_RESILIENCE", 0.6 ]
formal_mappings:
  candidates:
    - target: dG/dt (Rate of change of Gibbs Free Energy)
      domain: Thermodynamics
      mapping_kind: conceptual
      justification: |
        In chemical thermodynamics, a negative dG/dt signifies a spontaneous process moving toward equilibrium (maximum entropy). Coherence Flux inverts this: a positive d𝓛_p/dt signifies a system's "spontaneous" autopoietic drive *away* from environmental equilibrium (noise) and toward greater internal order, which is the signature of a thriving system.
      confidence: 0.7
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "A system exhibiting a sustained positive Coherence Flux (d𝓛_p/dt > 0) will have a statistically shorter recovery time (|Δt_recovery|) from a controlled environmental shock (Γ-spike) than an equivalent system with a sustained negative flux."
      domain: phenomenology
      falsifier: "Demonstrating that systems with negative Coherence Flux consistently recover from identical shocks faster than, or equal to, systems with positive flux, all other variables being equal."
      status: proposed
      links: [DOMA-036]
naming_notes:
  collisions: [Heat flux, Magnetic flux, Particle flux (Physics)]
  disambiguation: |
    Unlike physical fluxes which measure the flow of a quantity (e.g., energy) across a surface area, Coherence Flux is a scalar quantity representing the rate of change of a system's *total* net vitality over time. It is a derivative of a potential (𝓛_p), not a flow vector.
crosslinks:
  near_synonyms: [PRESSURE_GRADIENT]
  antonyms: [HOMEOSTASIS]
  prerequisites: [LAGRANGIAN_HEALTH]
  downstream_effects: [ADAPTIVE_RESILIENCE]
license: CC-BY-SA-4.0
---

# Coherence Flux

## Canonical (Pirouette)
The first time-derivative of the Pirouette Lagrangian (𝓛_p), quantifying the rate of change of a system's net vitality. It serves as the primary indicator of a system's health trajectory, measuring whether its capacity to generate coherence is accelerating, decelerating, or stable relative to environmental degradation. A positive flux (d𝓛_p/dt > 0) signals growth or strengthening (anabolism), while a negative flux (d𝓛_p/dt < 0) signals decay (catabolism).

## EFT-First Summary
There is no adopted EFT mapping for Coherence Flux at this time. A conceptual candidate is the rate of change of Gibbs Free Energy (dG/dt) from thermodynamics. Whereas a negative dG/dt signals a process moving toward entropic equilibrium, a positive Coherence Flux signals a system successfully moving *away* from its environment's equilibrium, a hallmark of autopoietic or living systems.

## Glossary Links
- See also: Lagrangian Health, Pressure Gradient, Homeostasis, Adaptive Resilience