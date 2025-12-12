---
term: "Coherence Atrophy"
canonical_id: "COHERENCE_ATROPHY"
symbol: ""
aliases: [The Stagnant Dam]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-040"]
---

---
term: Coherence Atrophy
canonical_id: COHERENCE_ATROPHY
symbol: A_⊥
aliases: [The Stagnant Dam]
parents: [DOMA-040, DYNA-003]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-040
      snippet: |
        1.  **Coherence Atrophy (The Stagnant Dam):**
            *   **Description:** A blockage in a critical flow creates a "coherence desert" downstream while building dangerous pressure upstream. It is the poison of inaction.
            *   **Manifestations:** Stalled R&D projects whose innovations never reach the market; bureaucratic gridlock where decisions are endlessly deferred; supply chain bottlenecks halting production; a sales pipeline that isn't moving.
  editors: [system]
  review_log: []
triad:
  art: |
    The silent pressure behind the dam, where potential festers into poison. It is the stillness that precedes a catastrophic break or a slow, quiet death from thirst downstream.
  law: |
    A system exhibits Coherence Atrophy when the measured flow rate of a critical resource across a defined boundary drops more than two standard deviations below its historical mean for a sustained period, while upstream pressure metrics (e.g., backlogs, inventory) concurrently rise above their mean.
  philosophy: |
    Atrophy is the pathology of fear-driven inaction and excessive control. It reveals a system's loss of trust in its own adaptive capacity, substituting the dynamic process of flow for the false security of a static hoard.
pirouette_definition: |
  Coherence Atrophy is a systemic pathology characterized by a critical blockage or constriction in one or more of a system's primary currents (e.g., Capital, Information, Talent, Trust). This obstruction halts or severely restricts flow, leading to a state of stagnation, a dangerous buildup of Temporal Pressure upstream of the blockage, and a coherence deficit or "resource desert" downstream.
operational_definition:
  units: Dimensionless (a categorical state), diagnosed via quantitative flow indicators.
  symbol_table:
    - name: A_⊥
      meaning: The state of Coherence Atrophy
      dimensions: dimensionless
      default_range: {0, 1} (absent, present)
    - name: Φ
      meaning: Flow rate of a specific current (e.g., capital, information)
      dimensions: items/time, currency/time
      default_range: contextual
    - name: P_u
      meaning: Upstream pressure, measured as queue length or backlog
      dimensions: items, currency
      default_range: contextual
  measurement:
    procedures:
      - name: Flow & Backlog Analysis
        outline: |
          1. Identify a critical flow path (e.g., product development pipeline from idea to launch).
          2. Define discrete stages and the boundaries between them.
          3. Measure the flow rate (Φ) of units passing the final boundary per unit time (e.g., products launched/quarter).
          4. Concurrently, measure the backlog (P_u) of units waiting at each internal boundary (e.g., projects awaiting funding approval).
          5. A diagnosis of Atrophy is supported when Φ drops significantly below baseline while P_u at a specific boundary rises significantly above its baseline.
        expected_signals: [Decreased system throughput rate, Increased queue length at a specific node, Increased end-to-end cycle time]
        pitfalls: [Mistaking seasonal variance for systemic atrophy, Focusing on a non-critical flow, Ignoring downstream resource starvation]
context_windows:
  - module: DOMA-040
    excerpt: |
      **Coherence Atrophy (The Stagnant Dam):** A blockage in a critical flow creates a "coherence desert" downstream while building dangerous pressure upstream. It is the poison of inaction. Manifestations include stalled R&D projects, bureaucratic gridlock where decisions are endlessly deferred, supply chain bottlenecks, and a sales pipeline that isn't moving.
  - module: DOMA-040
    excerpt: |
      To resolve **Atrophy (Stagnation)**, the lever is an act of "dam removal"—simplifying a process, clarifying a decision-right, or making a targeted capital injection. A strategic lever... is a minimal, precise intervention designed to restore the system's own ability to find health.
poetic_connections:
  motifs: [stagnation, blockage, pressure, hoarding, paralysis, inaction, constipation]
  evocative_lines:
    - "It is the poison of inaction."
    - "The balance sheet is a photograph of where the river was."
  association_matrix:
    - [ "TEMPORAL_PRESSURE", 0.8 ]
    - [ "LAMINAR_FLOW", -0.9 ]
    - [ "STRATEGIC_LEVER", 0.6 ]
    - [ "COHERENCE_FEVER", 0.3 ]
formal_mappings:
  candidates:
    - target: Traffic Jam (Kinematic Wave Theory)
      domain: CM
      mapping_kind: operational
      equation_hint: |
        ∂k/∂t + ∂q/∂x = 0 (conservation of cars/information)
        where flow q drops to zero as density k exceeds a critical threshold.
      justification: |
        Coherence Atrophy is isomorphic to a traffic jam. A local perturbation (a single driver braking, a bureaucratic checkpoint) causes a local increase in density and decrease in velocity. This "shockwave" of stagnation propagates backward (upstream), while flow downstream ceases. The intervention ("dam removal") is equivalent to clearing the obstruction, restoring flow.
      references:
        - title: "Traffic Flow Dynamics"
          where: "Chapter 2, Lighthill-Whitham-Richards model"
          date: 1955-01-01
      confidence: 0.9
    - target: Thrombosis
      domain: Biology
      mapping_kind: conceptual
      justification: |
        In physiology, thrombosis is the formation of a blood clot inside a blood vessel, obstructing the flow through the circulatory system. This is a direct biological analog for Coherence Atrophy, where a blockage in a capital, information, or talent "vessel" causes systemic harm through ischemia (downstream starvation) and hypertension (upstream pressure).
      confidence: 0.8
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "In a system diagnosed with Coherence Atrophy at a specific node, a targeted intervention to remove the blockage at that node will increase total system throughput more than an equivalent-cost intervention that applies uniform pressure across the entire system."
      domain: phenomenology
      falsifier: "If, in a controlled A/B test (e.g., on two identical sales teams), a global performance bonus (uniform pressure) more effectively clears a stalled sales pipeline than an intervention simplifying the specific CRM approval stage (dam removal), the model's prescription is flawed or the diagnosis was incorrect."
      status: proposed
      links: [DOMA-040]
naming_notes:
  collisions: []
  disambiguation: |
    Coherence Atrophy must be distinguished from **Coherence Erosion**. Atrophy is an acute blockage in a specific, otherwise-healthy flow channel (a dam in a river). Erosion is a chronic, systemic degradation of the channel's integrity itself (the riverbed turning to sand), leading to a diffuse leakage of coherence rather than a focused blockage.
crosslinks:
  near_synonyms: [GRIDLOCK, STAGNATION, BOTTLENECK]
  antonyms: [LAMINAR_FLOW, THROUGHPUT]
  prerequisites: [FLOW_PATHOLOGY, BUSINESS_CADUCEUS]
  downstream_effects: [TEMPORAL_PRESSURE, COHERENCE_FEVER]
license: CC-BY-SA-4.0
---