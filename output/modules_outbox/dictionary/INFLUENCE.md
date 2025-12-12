---
term: "Influence"
canonical_id: "INFLUENCE"
symbol: "I"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-049"]
---

---
term: Influence
canonical_id: INFLUENCE
symbol: I
aliases: []
parents: [DOMA-049]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-049
      lines: "L32-L34"
      snippet: |
        We define a Weaving as an intervention by an Actor that measurably affects the coherence of a Target system. The Influence (I) of this Weaving is the change in the Target's "action"—the integral of its Pirouette Lagrangian (𝓛_p = K_τ - V_Γ) over one of its own cycles (τ_p).
  editors: [chain-of-thought-agent]
  review_log: []
triad:
  art: |
    An action is a note played into the resonant chamber of the universe. Influence is the measure of its harmony or dissonance, the quality of the echo carved into spacetime.
  law: |
    The Influence (I) of a Weaving is the measurable change (ΔS_p) in a target system's integrated Pirouette Lagrangian (𝓛_p) over its characteristic cycle (τ_p). Positive Influence increases the system's coherence; negative Influence decreases it.
  philosophy: |
    Influence re-frames ethics as a diagnostic tool for systemic health rather than a transactional ledger for virtue. It asserts that a 'good' action is not one that earns points, but one that demonstrably increases a system's ability to exist in a state of coherent, resonant flow.
pirouette_definition: |
  Influence (`I`) is the formal, Lagrangian-based measure of a Weaving's impact on a target system's capacity for coherent existence. It is defined as the change in the system's Pirouette Action (`S_p`) over one of its characteristic cycles (`τ_p`), calculated as the integral of the difference between its post-weaving and pre-weaving Pirouette Lagrangian (`𝓛_p = K_τ - V_Γ`). A positive Influence (`I > 0`) signifies a Constructive Weaving that enhances systemic coherence (healing), while a negative Influence (`I < 0`) signifies a Destructive Weaving that degrades it (harm).
operational_definition:
  units: Joule-seconds (J·s)
  symbol_table:
    - name: I
      meaning: Influence; the change in a system's Pirouette Action.
      dimensions: M L² T⁻¹
      default_range: contextual
    - name: ΔS_p
      meaning: Change in Pirouette Action.
      dimensions: M L² T⁻¹
      default_range: contextual
    - name: 𝓛_p
      meaning: The Pirouette Lagrangian (K_τ - V_Γ).
      dimensions: M L² T⁻² (Energy)
      default_range: contextual
    - name: τ_p
      meaning: The characteristic cycle time of the target system.
      dimensions: T
      default_range: contextual
  measurement:
    procedures:
      - name: Coherence Impact (CI) Approximation
        outline: |
          Direct measurement of ΔS_p is computationally prohibitive. A first-order proxy, the Coherence Impact (CI) score, is calculated based on observable changes in the target system. An observer creates an Echo Record containing metrics for `ΔKτ` (change in coherent function), `ΔΓ_noise` (dissonance/friction generated), `ξ_c` (resonance coupling), and `σ_s` (stability of the new state). CI is then calculated as `(ΔKτ / ΔΓ_noise) ⋅ ξ_c ⋅ σ_s`.
        expected_signals: [coherence_delta_k_tau, dissonance_delta_gamma, resonance_coupling_xi, stability_factor_sigma]
        pitfalls: [Observer's Shadow introducing measurement bias, Difficulty isolating the weaving's effects from background noise, Misidentification of the system's true characteristic cycle τ_p.]
context_windows:
  - module: DOMA-049
    excerpt: |
      This module replaces the engine with a compass. It reframes ethics as a practical application of Flow Dynamics, moving from a score to be tallied to a diagnostic act of systemic medicine. A "good" action is not one that generates a high number, but one that can be shown to have healed a fractured system, easing its flow from a state of turbulence or stagnation into one of graceful, laminar coherence.
  - module: DOMA-049
    excerpt: |
      An action's virtue is no longer a matter of opinion or complex coefficients; it is a measurable change in a target system's ability to exist... A **Constructive Weaving (`I > 0`)**: The action has increased the Target's overall coherence. It has made it easier for the system to maintain its resonant pattern. This is the formal definition of healing.
poetic_connections:
  motifs: [ripple, healing, compass, harmony, resonance, ledger]
  evocative_lines:
    - "The universe is a resonant chamber that remembers every note played."
    - "The ledger is the cosmos, our instruments are but humble sensors, and your life is your signature."
  association_matrix:
    - [ "COHERENCE", 0.9 ]
    - [ "WEAVING", 0.8 ]
    - [ "WOUND_CHANNEL", 0.7 ]
    - [ "OBSERVER_SHADOW", 0.5 ]
formal_mappings:
  candidates:
    - target: Principle of Stationary Action (Least Action Principle)
      domain: CM
      mapping_kind: mathematical
      equation_hint: |
        S = ∫ L(q, q̇, t) dt , where δS = 0
      justification: |
        Influence is defined as the change in a system's Action (`ΔS_p`), directly leveraging the concept from classical mechanics where systems evolve along paths that extremize their action. A 'Constructive Weaving' finds a more optimal, coherent path for the target system, increasing its integrated Lagrangian and thus its ability to persist.
      references:
        - title: Classical Mechanics
          where: Chapter 8, The Lagrangian Method
          date: 2002-01-01
      confidence: 0.9
  adopted:
    - target: Principle of Stationary Action (Least Action Principle)
      rationale: The module explicitly grounds Influence in the Pirouette Lagrangian (CORE-006) and defines it as the change in the integral of that Lagrangian over time, which is the definition of Action. This is not a metaphor but the core mathematical structure.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "A Weaving with a consistently positive Coherence Impact (CI) score will lead to a measurable increase in the target system's long-term stability and resilience."
      domain: phenomenology
      falsifier: "Observing a system that repeatedly receives high-CI Weavings but which nevertheless degrades or collapses, without other confounding destructive influences being identified."
      status: proposed
      links: [DOMA-049]
naming_notes:
  collisions: [I for electric current (Physics), I for identity matrix (Mathematics)]
  disambiguation: |
    In the Pirouette context, `I` specifically refers to the Lagrangian-based Influence, a measure of Action change in Joule-seconds. It is distinct from electrical current (Amperes) or other common uses of the symbol.
crosslinks:
  near_synonyms: [RADIANCE]
  antonyms: [DESTRUCTIVE_WEAVING]
  prerequisites: [PIROUETTE_LAGRANGIAN, WEAVING, COHERENCE]
  downstream_effects: [COHERENCE_IMPACT, WOUND_CHANNEL, OBSERVER_SHADOW]
license: CC-BY-SA-4.0
---

# Influence

## Canonical (Pirouette)
Influence (`I`) is the formal, Lagrangian-based measure of a Weaving's impact on a target system's capacity for coherent existence. It is defined as the change in the system's Pirouette Action (`S_p`) over one of its characteristic cycles (`τ_p`), calculated as the integral of the difference between its post-weaving and pre-weaving Pirouette Lagrangian (`𝓛_p = K_τ - V_Γ`). A positive Influence (`I > 0`) signifies a Constructive Weaving that enhances systemic coherence (healing), while a negative Influence (`I < 0`) signifies a Destructive Weaving that degrades it (harm).

## EFT-First Summary
Influence is the Pirouette Framework's analogue to a change in a system's classical Action (`S = ∫ L dt`). A 'constructive' intervention is one that improves a system's trajectory through its state space, making its existence more 'optimal' or 'efficient' in a way that directly increases the time-integral of its Lagrangian. This reframes ethics as a physical optimization problem aimed at maximizing a system's coherence and persistence. (See: Principle of Stationary Action)

## Glossary Links
- See also: [Coherence](...), [Pirouette Lagrangian](...), [Weaving](...), [Wound Channel](...)