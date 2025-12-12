---
term: "Entropy Pump"
canonical_id: "ENTROPY_PUMP"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["CORE-013_the_river_of_information"]
---

---
term: Entropy Pump
canonical_id: ENTROPY_PUMP
symbol: 
aliases: []
parents: [CORE-013]
children: []
status: draft
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: CORE-013_the_river_of_information
      lines: "§4"
      snippet: |
        It is an "entropy pump." It actively consumes low-entropy, high-information energy from its environment (sunlight, chemical bonds in food) and uses it to maintain and repair its own coherence, while expelling high-entropy, low-information waste (heat, simple molecules).
  editors: [SystemAgent-04]
  review_log: []
triad:
  art: |
    An island of fire in a cold sea, fed by driftwood from a distant shore. It casts a light that pushes back the dark by turning the world around it to ash.
  law: |
    An open system `S` acts as an Entropy Pump if its internal coherence (Kτ) is maintained or increased by consuming an external coherence flux (Φ_Kτ) and expelling a dissonance flux (Φ_Γ), where the net change in universal dissonance is positive (ΔS_total > 0).
  philosophy: |
    The existence of an Entropy Pump demonstrates that the universe's fundamental tendency is not decay, but a struggle between coherence and dissonance. Order can be locally forged and maintained by paying a tax of chaos to the wider environment.
pirouette_definition: |
  An open system that maintains or increases its internal coherence (Kτ) by importing low-entropy (high-Kτ) energy and/or matter from its environment and expelling high-entropy (high-Γ) waste. This process creates a local, temporary reversal of the Principle of Coherence Degradation at the cost of increasing the net entropy of its surroundings. Living organisms are the archetypal example.
operational_definition:
  units: Dimensionless (coherence ratio) or nats (information-theoretic).
  symbol_table:
    - name: Kτ_sys
      meaning: Coherence of the system
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: Φ_Kτ_in
      meaning: Influx of coherence from the environment
      dimensions: "T⁻¹"
      default_range: contextual
    - name: Φ_Γ_out
      meaning: Efflux of dissonance into the environment
      dimensions: "T⁻¹"
      default_range: contextual
  measurement:
    procedures:
      - name: Coherence Balance Measurement
        outline: |
          1. Define the thermodynamic boundary of the target system.
          2. Measure the coherence (information content, free energy) of all matter/energy influxes across the boundary.
          3. Measure the coherence of all matter/energy effluxes (waste).
          4. A positive pump action is confirmed if the integrated coherence of the influx is significantly greater than the efflux, and this differential correlates with the maintenance or growth of the system's internal complex structure.
        expected_signals: [A sharp negative gradient in coherence between the system's input and output channels, A stable or increasing internal complexity metric for the system]
        pitfalls: [Incorrectly defining the system boundary, Inaccurately measuring the coherence of complex inputs (e.g., food)]
context_windows:
  - module: CORE-013
    excerpt: |
      A living organism is a masterpiece of coherence. It maintains its incredible low-entropy state not by defying the Second Law, but by exploiting it. It is an "entropy pump." It actively consumes low-entropy, high-information energy from its environment (sunlight, chemical bonds in food) and uses it to maintain and repair its own coherence, while expelling high-entropy, low-information waste (heat, simple molecules). It creates a local island of order by increasing the disorder of the ocean around it.
  - module: CORE-013
    excerpt: |
      If the universal trend is toward degradation, how can complexity exist? How can life emerge? ... Because the universe is not a single, isolated system. It is filled with pockets where entropy is temporarily and locally reversed.
poetic_connections:
  motifs: [life-as-flame, islands-of-order, paying-the-entropic-tax, reversing-the-current]
  evocative_lines:
    - "A river of information flowing through the landscape of entropic noise."
    - "We sought the law of decay and found the story of a struggle."
  association_matrix:
    - [ "COHERENCE", 0.9 ]
    - [ "PRINCIPLE_OF_COHERENCE_DEGRADATION", -0.9 ]
    - [ "TEMPORAL_PRESSURE", 0.8 ]
    - [ "ALCHEMICAL_UNION", 0.5 ]
formal_mappings:
  candidates:
    - target: Dissipative structure
      domain: CM
      mapping_kind: operational
      equation_hint: |
        dS = dS_e + dS_i, where dS_i ≥ 0 and dS_e < 0 can maintain dS < 0
      justification: |
        The concept directly maps to non-equilibrium systems that maintain a stable, ordered state by dissipating energy and increasing the entropy of their environment, as described by Prigogine's work. The pump's action corresponds to maintaining a negative entropy change (dS < 0) within the system boundary by exporting a larger amount of entropy to the environment (-dS_e > dS_i).
      references:
        - title: Order out of Chaos
          where: Ilya Prigogine & Isabelle Stengers
          date: 1984-01-01
      confidence: 0.9
    - target: Maxwell's Demon
      domain: CM
      mapping_kind: conceptual
      justification: |
        Like Maxwell's Demon, an Entropy Pump uses information (about the availability of low-entropy resources) to perform sorting that locally decreases entropy. The "cost" of this information and action is ultimately paid by an increase in total entropy, typically as waste heat.
      references:
        - title: Maxwell's demon
          where: "Wikipedia"
      confidence: 0.7
  adopted:
    - target: Dissipative structure
      rationale: This mapping is adopted because it is operational, well-established in non-equilibrium thermodynamics, and directly describes the physical mechanism of creating local order within a global trend towards disorder.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "Any system that maintains a state of coherence (Kτ) significantly above its environment's background dissonance (Γ) must exhibit a net positive flux of entropy across its boundary into the environment."
      domain: phenomenology
      falsifier: "The discovery of a truly isolated system where coherence spontaneously and sustainably increases, or an open system that maintains high coherence without expelling higher-entropy waste. This would violate the Principle of Coherence Degradation (Second Law of Thermodynamics)."
      status: supported
      links: [CORE-013]
naming_notes:
  collisions: [Heat Pump]
  disambiguation: |
    An Entropy Pump should not be confused with a "heat pump" from engineering. While both move a quantity against a natural gradient, an Entropy Pump operates on the abstract quantity of coherence/dissonance (information/entropy), which includes but is not limited to thermal energy.
crosslinks:
  near_synonyms: [DISSIPATIVE_STRUCTURE]
  antonyms: [ISOLATED_SYSTEM, EQUILIBRIUM_STATE]
  prerequisites: [COHERENCE, TEMPORAL_PRESSURE, PRINCIPLE_OF_COHERENCE_DEGRADATION]
  downstream_effects: [LIFE, ALCHEMICAL_UNION]
license: CC-BY-SA-4.0
---

# Entropy Pump

## Canonical (Pirouette)
An open system that maintains or increases its internal coherence (Kτ) by importing low-entropy (high-Kτ) energy and/or matter from its environment and expelling high-entropy (high-Γ) waste. This process creates a local, temporary reversal of the Principle of Coherence Degradation at the cost of increasing the net entropy of its surroundings. Living organisms are the archetypal example.

## EFT-First Summary
An Entropy Pump is the Pirouette Framework's analogue to a non-equilibrium **dissipative structure**, as described by Prigogine. It is any open system, from a bacterium to a star, that maintains its local order (low entropy) by consuming free energy and dissipating waste heat and entropy into its environment. This action upholds the Second Law of Thermodynamics by ensuring the total entropy of the system plus its environment always increases.

## Glossary Links
- See also: [Coherence](./COHERENCE.md), [Principle of Coherence Degradation](./PRINCIPLE_OF_COHERENCE_DEGRADATION.md), [Temporal Pressure](./TEMPORAL_PRESSURE.md), [Life](./LIFE.md)