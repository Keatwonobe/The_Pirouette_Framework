---
term: "Simulation"
canonical_id: "SIMULATION"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-029"]
---

---
term: Simulation
canonical_id: SIMULATION
symbol: 
aliases: [computational modeling, forecasting, in-silico exploration]
parents: [DOMA-029, CORE-006]
children: [INST-NALY-001]
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-029
      lines: "L63-L65"
      snippet: |
        3. Simulation: The model runs, generating a stream of `simulation` records that explore possibilities beyond the reach of direct observation.
  editors: [System Agent]
  review_log: []
triad:
  art: |
    A model's silent dream, tracing the threads of what could be, untethered from the world's immediate chaos. It is the practice of asking "what if?" in a language the universe must answer.
  law: |
    A `simulation` process must produce a time-stream of Chronoscript records with `source_type: simulation` that is formally indistinguishable and computationally interchangeable with a time-stream from an `observation` process.
  philosophy: |
    Machine calculation is not an alternative to human intuition, but its extension. A simulation allows us to walk paths that do not yet exist, to test the world's rules in a space free from consequence, thereby sharpening our questions for when we return to it.
pirouette_definition: |
  A computational process that generates a time-stream of `Chronoscript-v2` records to explore a system's potential states under a defined model. Seeded and calibrated by `observation` data, a simulation's primary function is to extend analysis beyond the reach of direct experience. Its output, marked `source_type: simulation`, must be schema-compliant to ensure Observational Parity with live data streams.
operational_definition:
  units: N/A (process); output is a time-stream of `Chronoscript-v2` records.
  symbol_table:
    - name: "N/A"
      meaning: "Simulation is a process, not a variable, and has no symbol."
      dimensions: "N/A"
      default_range: "N/A"
  measurement:
    procedures:
      - name: Model Execution & Data Generation
        outline: |
          1. Instantiate a computational model of a system (`entity_id`), typically seeded with parameters derived from `observation` data.
          2. Define a time evolution algorithm based on the Pirouette Lagrangian (`𝓛_p = K_τ - V_Γ`).
          3. Execute the algorithm over a specified time domain, generating a `Chronoscript-v2` record at each discrete time-step.
          4. Set `source_type` to `simulation` for all generated records and ensure timestamps are strictly monotonic.
        expected_signals: [A valid, monotonically increasing time-stream of `Chronoscript-v2` records.]
        pitfalls: [Model divergence (numerical instability), miscalibration from sparse observational data, violation of Chronoscript schema (e.g., non-monotonic timestamps).]
context_windows:
  - module: DOMA-029
    excerpt: |
      The old framework created a schism between the language of the living world, captured through *rituals*, and the language of the machine, captured through *simulations*. This created an unnecessary and lossy translation step... A time-stream of data from any compliant source—whether a live observation of a human system or a high-frequency numerical simulation—can be ingested and understood by the same analytical tools.
  - module: DOMA-029
    excerpt: |
      The unification of `observation` and `simulation` data streams enables a powerful feedback loop: ... 2. **Calibration:** This real-world data is used to seed, tune, and validate a computational model of the system. 3. **Simulation:** The model runs, generating a stream of `simulation` records that explore possibilities beyond the reach of direct observation.
poetic_connections:
  motifs: [what-if, counterfactual, machine dream, modeled future, synthetic data]
  evocative_lines:
    - "...dreamed in the machine's perfect silence..."
    - "...explore possibilities beyond the reach of direct observation."
    - "Data begets insight, which begets better data."
  association_matrix:
    - [ "OBSERVATION", 0.9 ]
    - [ "OBSERVATIONAL_PARITY", 0.9 ]
    - [ "LAGRANGIAN_STATE_VECTOR", 0.8 ]
    - [ "MODEL_CALIBRATION", 0.8 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Numerical simulation of a dynamical system
      domain: Computational Physics
      mapping_kind: operational
      equation_hint: |
        S_i+1 = F(S_i, 𝓛_p, Δt)
      justification: |
        A Pirouette `Simulation` is a direct application of numerical simulation, where the system's evolution is governed by the Pirouette Lagrangian (`𝓛_p`). It uses standard numerical integration techniques to propagate the `lagrangian_state` forward in discrete time steps, generating a time series of the system's trajectory. The term is used in its standard computational sense, specialized to the Pirouette context.
      references:
        - title: Numerical Recipes in C The Art of Scientific Computing
          where: "Chapter 16: Integration of Ordinary Differential Equations"
          date: 1992-01-01
      rationale: "The term 'simulation' in Pirouette is a direct application of the standard scientific and computational concept, specialized to use the Pirouette Lagrangian as its governing dynamic principle. There is no need for a more abstract mapping."
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "A valid `simulation` time-stream, when fed to a compliant analysis tool (e.g., `INST-NALY-001`), produces results that are structurally and dimensionally consistent with results from an `observation` time-stream of the same system."
      domain: phenomenology
      falsifier: "An analysis tool throws a type error, schema validation failure, or produces dimensionally nonsensical metrics when switching from an `observation` stream to a `simulation` stream, indicating a breach of the Chronoscript contract and a failure of Observational Parity."
      status: supported
      links: [DOMA-029]
naming_notes:
  collisions: [The term "simulation" is ubiquitous in science and engineering.]
  disambiguation: |
    In Pirouette, 'Simulation' specifically refers to the *process* of generating a `source_type: simulation` Chronoscript stream. It is distinct from 'modeling' (the creation of the system rules) and 'analysis' (the consumption of the stream). It is the direct computational counterpart to the physical process of `Observation`.
crosslinks:
  near_synonyms: [MODELING, FORECASTING]
  antonyms: [OBSERVATION, RITUAL]
  prerequisites: [MODEL_CALIBRATION, LAGRANGIAN_STATE_VECTOR]
  downstream_effects: [INST-NALY-001]
license: CC-BY-SA-4.0
---

# Simulation

## Canonical (Pirouette)
A computational process that generates a time-stream of `Chronoscript-v2` records to explore a system's potential states under a defined model. Seeded and calibrated by `observation` data, a simulation's primary function is to extend analysis beyond the reach of direct experience. Its output, marked `source_type: simulation`, must be schema-compliant to ensure Observational Parity with live data streams.

## EFT-First Summary
In conventional terms, a Pirouette Simulation is a **numerical simulation of a dynamical system**. The novelty lies in the governing physics: instead of standard Hamiltonians, the system's time-evolution is propagated by numerically integrating the Pirouette Lagrangian (`𝓛_p`). This process generates a synthetic time-series dataset that is structurally identical to empirical data, enabling unified analysis.

## Glossary Links
- See also: [Observation](<#>), [Observational Parity](<#>), [Chronoscript](<#>)