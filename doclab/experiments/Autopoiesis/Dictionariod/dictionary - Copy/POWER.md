---
term: "Power"
canonical_id: "POWER"
symbol: "Γ"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["XCM-000_crucible_template"]
---

---
term: Power
canonical_id: POWER
symbol: Γ
aliases: [Resource Leverage, Exertion]
parents: [XCM-000]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: XCM-000
      lines: "L63-L67"
      snippet: |
        | Axis       | Description                             | Example Measures                                               |
        | ---------- | --------------------------------------- | -------------------------------------------------------------- |
        | Γ          | Power exerted / tools leveraged         | Total force used, energy consumed, resources spent             |
  editors: [Crucible Architect]
  review_log: []
triad:
  art: |
    The flash of a striking hammer, the steady burn of a star, or the silent weight of a decision. Power is the potential for change made manifest, the currency of action in a world of inertia. It is the river that can either carve canyons or flood civilizations.
  law: |
    Power (Γ) is the time-integrated magnitude of all energy, resources, and influence deployed by a system during a trial. Its application is measured independently of its outcome. A high-Γ action that fails is recorded with the same magnitude as one that succeeds.
  philosophy: |
    Power is the capacity to alter a system's state. Within the Pirouette framework, it is a neutral tool, not an intrinsic good. Its value is derived entirely from its alignment with purpose (φ) and its effect on systemic coherence (Tₐ). Unfocused Power creates residue and fragmentation; aligned Power creates resonance.
pirouette_definition: |
  Power (Γ) is a primary axis of the triaxial lens for evaluating a Crucible trial, representing the total quantity of force, energy, resources, or influence exerted by a participant. It measures the scale of the intervention—*how much* was done—distinct from its temporal stability (Tₐ) or its alignment with intent (φ). Γ is a scalar quantity, aggregated over the duration of the trial, and is agnostic to the success or failure of the action.
operational_definition:
  units: Context-dependent (e.g., Joules, Newtons, CPU-hours, currency) or dimensionless (normalized against a baseline).
  symbol_table:
    - name: Γ
      meaning: Total power exerted or resources consumed over a trial's duration.
      dimensions: Contextual. Often ML²T⁻² for energy.
      default_range: "[0, ∞)"
  measurement:
    procedures:
      - name: Resource Expenditure Audit
        outline: |
          1. Identify all channels of resource or energy expenditure available to the agent.
          2. Instrument or log the flow through each channel over the trial's duration (t₀ to tƒ).
          3. Integrate each channel's expenditure over time.
          4. Sum the integrated totals, using normalization factors if units are heterogeneous.
        expected_signals: [A non-decreasing cumulative expenditure curve over the trial duration, spikes in the derivative corresponding to intense actions.]
        pitfalls: [Failure to account for intangible assets like social capital, inaccurate conversion factors between different resource types, defining a zero-expenditure baseline.]
context_windows:
  - module: XCM-000
    excerpt: |
      A Crucible is not a competition—it is a trial of alignment. It tests... Whether coherence can be maintained under pressure; whether purpose (φ) can remain phase-locked despite divergent challenges; whether power (Γ) is deployed responsibly and effectively.
  - module: XCM-000
    excerpt: |
      Describe a few likely outcomes and their implications: "Crash and fragment", "Success by force but low Tₐ", "High-φ reframe that resolves without conflict", "Unexpected innovation under constraint".
poetic_connections:
  motifs: [Force, Expenditure, Leverage, Impact, Consumption, Fuel]
  evocative_lines:
    - "Whether power (Γ) is deployed responsibly and effectively."
    - "Success by force but low Tₐ."
    - "Cooperation > domination."
  association_matrix:
    - [ "TIME_ADHERENCE", 0.8 ]
    - [ "PHASE", 0.8 ]
    - [ "COHERENCE", 0.7 ]
    - [ "RESIDUE", 0.6 ]
formal_mappings:
  candidates:
    - target: Work (W) / Total Energy Expended (E_total)
      domain: CM
      mapping_kind: operational
      equation_hint: |
        Γ ∝ W = ∫ P(t) dt
      justification: |
        The source explicitly cites "energy consumed" and "total force used" as example measures for Γ. In classical mechanics, the integral of instantaneous power P(t) over a duration is the total work done (W) or energy expended, providing a direct and measurable physical analog.
      references:
        - title: Classical Mechanics
          where: "Chapter on Work and Energy"
          date: 
      confidence: 0.9
  adopted:
    - target: Work (W)
      rationale: This mapping is directly supported by the source's "Example Measures," is operationally clear, and provides a robust, falsifiable way to quantify Γ in physical crucibles.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "In any given Crucible, there exists a Γ_max threshold beyond which any increase in Power expenditure produces a negative return on Phase (φ) alignment."
      domain: phenomenology
      falsifier: "Demonstration of a Crucible scenario where goal alignment (φ) remains perfectly correlated or improves with arbitrarily high levels of Power (Γ), indicating no diminishing returns or decoupling effect."
      status: proposed
      links: [XCM-000]
naming_notes:
  collisions: [Γ is the Lorentz factor in special relativity, the Gamma function in mathematics, and the symbol for a photon. Context is critical.]
  disambiguation: |
    In the Pirouette Framework, Γ is always a scalar integral quantity representing total exertion in a trial. It should be distinguished from instantaneous power (P or dΓ/dt). Unlike the Lorentz factor, it is not a dimensionless velocity-dependent multiplier.
crosslinks:
  near_synonyms: [RESOURCE_EXPENDITURE]
  antonyms: [QUIESCENCE, INACTION]
  prerequisites: [CRUCIBLE]
  downstream_effects: [TIME_ADHERENCE, PHASE, COHERENCE_RESIDUE]
license: CC-BY-SA-4.0
---

# Power

## Canonical (Pirouette)
Power (Γ) is a primary axis of the triaxial lens for evaluating a Crucible trial, representing the total quantity of force, energy, resources, or influence exerted by a participant. It measures the scale of the intervention—*how much* was done—distinct from its temporal stability (Tₐ) or its alignment with intent (φ). Γ is a scalar quantity, aggregated over the duration of the trial, and is agnostic to the success or failure of the action.

## EFT-First Summary
Operationally, Pirouette Power (Γ) is best mapped to the classical mechanics concept of Work (W) or total energy expended. It represents the integrated magnitude of forces applied or resources consumed over a trial's duration (Γ ∝ ∫ P(t) dt). This quantity measures the sheer scale of an agent's interaction with the scenario's environment, serving as the raw input against which coherence and alignment are judged.

## Glossary Links
- See also: [Phase (φ)](...), [Time-Adherence (Tₐ)](...), [Crucible (...)](...)