---
term: "Impact"
canonical_id: "IMPACT"
symbol: "I"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-033"]
---

---
term: Impact
canonical_id: IMPACT
symbol: I
aliases: [Impact Score, Coherence Loss]
parents: [DOMA-033, CORE-006, CORE-014]
children: [dashboards]
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-033
      lines: "§3.1"
      snippet: |
        Formally, the Impact (I) of an event (fᵢ) is the magnitude of the negative change in the system's total Action (ΔSₚ) that is correlated with that event. It is the integral of the dip in the Lagrangian caused by the event: I(fᵢ) ≈ - ∫_dip Δ𝓛_p dt.
  editors: [Weaver-Agent-Alpha]
  review_log: []
triad:
  art: |
    The felt magnitude of a system's wound. It is the echo of a single jarring event that briefly silences the entire symphony.
  law: |
    The Impact of any event is the time-integral of the coherence loss (the negative dip in the Pirouette Lagrangian) it induces. All Impacts are non-negative scalars with units of Action.
  philosophy: |
    Impact translates the abstract principle of coherence into a practical diagnostic metric. It allows a Weaver to focus finite attention on the "critical few" events that truly harm a system's integrity, making intervention precise and effective.
pirouette_definition: |
  A non-negative, scalar quantity representing the magnitude of coherence lost due to a specific event. Impact is measured by the integral of the negative perturbation (the 'dip') in the Pirouette Lagrangian (𝓛_p) over the duration of the event's influence, corresponding to the total loss in the system's Action (S_p).
operational_definition:
  units: Units of Action (context-dependent; often normalized and dimensionless).
  symbol_table:
    - name: I
      meaning: Impact of a specific event.
      dimensions: Action (M L² T⁻¹)
      default_range: "[0, ∞)"
    - name: 𝓛_p
      meaning: The Pirouette Lagrangian.
      dimensions: Energy (M L² T⁻²)
      default_range: contextual
    - name: ΔSₚ
      meaning: The change in the Pirouette Action.
      dimensions: Action (M L² T⁻¹)
      default_range: contextual
    - name: fᵢ
      meaning: A discrete, causal system event.
      dimensions: dimensionless
      default_range: n/a
  measurement:
    procedures:
      - name: Impact Calculation via Correlated Integration
        outline: |
          1. Generate the Lagrangian time-series (𝓛_p(t)) via the Fractal Bridge protocol (CORE-014).
          2. Time-align a log of discrete system events (fᵢ) with the 𝓛_p(t) trace.
          3. For each event fᵢ, identify a correlated negative deviation ('dip') from the baseline 𝓛_p.
          4. Numerically integrate the area of this dip (i.e., ∫(𝓛_baseline - 𝓛_measured) dt) over its duration. This integral is the Impact, I(fᵢ).
        expected_signals: [Lagrangian time-series, timestamped event log]
        pitfalls: [Correlation-causation fallacy, ambiguity in defining the integration window (start/end of the dip), establishing a stable baseline 𝓛_p.]
context_windows:
  - module: DOMA-033
    excerpt: |
      The Auditor correlates every event in the original raw data with a corresponding dip in the Lagrangian trace. The magnitude and duration of the dip provide a precise, quantitative "impact score" for that event. This score is not an arbitrary proxy; it is a direct measure of the coherence lost.
  - module: DOMA-033
    excerpt: |
      An event has high impact if it sharply degrades the system's internal resonance or exposes it to a spike in environmental pressure, forcing it off its optimal path.
poetic_connections:
  motifs: [wound, dissonance, arrhythmia, fracture, friction]
  evocative_lines:
    - "A system in pain does not announce its wound; it simply loses its grace."
    - "touch the single thread that will mend the entire tapestry."
  association_matrix:
    - [ "LAGRANGIAN", 0.9 ]
    - [ "REVERSE_PARETO_ANALYSIS", 0.8 ]
    - [ "COHERENCE", -0.9 ]
    - [ "ACTION", 0.7 ]
formal_mappings:
  candidates:
    - target: Perturbative contribution to Action (ΔS)
      domain: CM
      mapping_kind: mathematical
      equation_hint: |
        I(fᵢ) = ΔSₚ = ∫(L_perturbed - L_unperturbed) dt
      justification: |
        Impact is explicitly defined as ΔSₚ, the change in a system's total Action due to a discrete event. In classical mechanics, perturbations (e.g., friction, external forces) are modeled as additional terms in the Lagrangian. The integral of these terms (ΔS) quantifies the total effect of the perturbation on the system's path, making it a direct analog.
      references:
        - title: Classical Mechanics
          where: Chapter 8, "Hamiltonian Mechanics"
          date: 1980-01-01
      confidence: 0.8
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "For most complex systems, the distribution of event Impacts follows a power law, enabling effective diagnosis via Reverse Pareto Analysis."
      domain: phenomenology
      falsifier: "Repeated observation of systems where coherence loss is diffuse and event Impacts are normally distributed, rendering RPA ineffective."
      status: supported
      links: [DOMA-033]
naming_notes:
  collisions: [I (electric current), I (moment of inertia), I (identity matrix), I (impulse)]
  disambiguation: |
    In the Pirouette Framework, 'Impact' (I) is always a non-negative scalar with units of Action, specifically measuring coherence loss. It should not be confused with impulse from classical mechanics (also 'I' or 'J') which has units of momentum.
crosslinks:
  near_synonyms: [COHERENCE_LOSS]
  antonyms: []
  prerequisites: [LAGRANGIAN, FRACTAL_BRIDGE, ACTION]
  downstream_effects: [REVERSE_PARETO_ANALYSIS, CRITICAL_FEW]
license: CC-BY-SA-4.0
---