---
term: "Coherence Index"
canonical_id: "COHERENCE_INDEX"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-040"]
---

---
term: Coherence Index
canonical_id: COHERENCE_INDEX
symbol: I_c
aliases: [Organizational Coherence, Flow Efficiency]
parents: [DOMA-040]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-040
      lines: "L102-L105"
      snippet: |
        We replace the old Business Resonance Score with a more fundamental concept: the **Coherence Index**. This is not a fixed formula, but a holistic measure of the organization's ability to maintain Laminar Flow. A high index signifies a healthy organism with low internal friction, efficiently converting resources into value.
  editors: [llm-weaver]
  review_log: []
triad:
  art: |
    The quiet, powerful hum of a system in harmony. It is the palpable feeling of effortless momentum when capital, information, talent, and trust flow as one current. A high Coherence Index is the signature of a river that knows its way to the sea.
  law: |
    An organization's long-term rate of value creation is directly proportional to its Coherence Index. Increasing the index by reducing internal friction (Turbulence, Atrophy) provides a greater return on investment than applying more external force (capital, labor) to a low-coherence system.
  philosophy: |
    The Coherence Index reframes the goal of strategy from winning a series of battles to cultivating a state of systemic health. It replaces static, lagging indicators with a dynamic measure of an organization's capacity for graceful, adaptive action. True competitive advantage is not a position to be defended, but a flow state to be maintained.
pirouette_definition: |
  A holistic, dimensionless measure of an organization's ability to maintain Laminar Flow across its four primary currents (Capital, Information, Talent, Trust). The Coherence Index quantifies the efficiency of converting resources into value by measuring the degree of internal alignment and the absence of systemic friction (pathologies of Atrophy, Fever, and Erosion). It serves as an operational proxy for an organization's success in maximizing its Temporal Coherence (Kτ) relative to the ambient Temporal Pressure (V_Γ), as defined by the Pirouette Lagrangian.
operational_definition:
  units: Dimensionless (typically normalized to a range like 0-100 or 0-1).
  symbol_table:
    - name: I_c
      meaning: Coherence Index
      dimensions: dimensionless
      default_range: "[0, 100]"
  measurement:
    procedures:
      - name: Four-Current Flow Assessment
        outline: |
          1. **Map Currents:** Identify and map the critical paths for the four primary currents (Capital, Information, Talent, Trust).
          2. **Assess Flow State:** For each path, measure or observe proxies for flow quality. For Capital, use metrics like cash conversion cycle. For Information, use decision velocity. For Talent, use regrettable turnover rate. For Trust, use survey instruments for psychological safety.
          3. **Identify Pathologies:** Classify disruptions in each current as Atrophy (blockages), Fever (turbulence/friction), or Erosion (decay). Quantify the energy/value loss from these pathologies.
          4. **Synthesize Index:** Aggregate the weighted health of the four currents into a composite score. A high score represents high laminar flow and low pathological disruption.
        expected_signals: [High cash conversion efficiency, low decision latency, low regrettable employee turnover, high innovation rate, high Net Promoter Score.]
        pitfalls: [Over-weighting easily quantifiable currents (Capital) at the expense of qualitative ones (Trust). Using lagging indicators (annual profit) instead of leading indicators (decision velocity). Mistaking frantic activity (Fever) for productive flow.]
context_windows:
  - module: DOMA-040
    excerpt: |
      We replace the old Business Resonance Score with a more fundamental concept: the **Coherence Index**. This is not a fixed formula, but a holistic measure of the organization's ability to maintain Laminar Flow. A high index signifies a healthy organism with low internal friction, efficiently converting resources into value.
  - module: DOMA-040
    excerpt: |
      Strategic leadership is the art of applying levers that adjust the firm's trajectory, seeking the path of maximal coherence (the highest Kτ for a given V_Γ) and thereby maximizing its Coherence Index.
poetic_connections:
  motifs: [laminar flow, river-keeping, internal friction, systemic health, organizational hum]
  evocative_lines:
    - "The balance sheet is a photograph of where the river was. The flow is a prophecy of where the river is going."
    - "A Weaver does not see a company as a machine to be fixed, but as a river to be tended."
  association_matrix:
    - [ "LAMINAR_FLOW", 0.9 ]
    - [ "TEMPORAL_COHERENCE", 0.8 ]
    - [ "COHERENCE_FEVER", -0.7 ]
    - [ "COHERENCE_ATROPHY", -0.7 ]
    - [ "INTERNAL_FRICTION", -0.9 ]
formal_mappings:
  candidates:
    - target: Q factor (Quality factor)
      domain: CM
      mapping_kind: conceptual
      equation_hint: |
        Q = 2π * (Energy Stored / Energy dissipated per cycle)
      justification: |
        A high Q factor in a resonator signifies low damping and high efficiency, analogous to a high Coherence Index signifying low internal friction (energy dissipation) and high efficiency in converting potential to action. Both are dimensionless measures of systemic quality.
      references:
        - title: Vibrations and Waves
          where: Chapter 3
          date: 1971-01-01
      confidence: 0.7
    - target: Total Factor Productivity (TFP)
      domain: Economics
      mapping_kind: operational
      equation_hint: |
        Y = A * F(K, L) where A is TFP
      justification: |
        TFP measures the portion of output not explained by the amount of inputs (capital K, labor L). It is a proxy for efficiency, technology, and management quality. The Coherence Index can be seen as the underlying organizational dynamic that determines a firm's TFP.
      references:
        - title: The sources of economic growth in the United States and the alternatives before us
          where: Committee for Economic Development
          date: 1962-01-01
      confidence: 0.8
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "An increase in a firm's Coherence Index, derived from flow-state measurements, will precede a sustained increase in its Total Factor Productivity and long-term shareholder value."
      domain: phenomenology
      falsifier: "A statistically significant longitudinal study showing no correlation or a negative correlation between a rigorously measured Coherence Index and future TFP/market performance across multiple industries and business cycles."
      status: proposed
      links: [DOMA-040]
naming_notes:
  collisions: []
  disambiguation: |
    Not to be confused with "coherence" in physics, which refers to a fixed phase relationship between waves. The Pirouette term is a broader, systemic concept of alignment and frictionless interaction within a complex adaptive system, though it draws metaphorical power from the physics concept.
crosslinks:
  near_synonyms: [BUSINESS_RESONANCE_SCORE]
  antonyms: [COHERENCE_ATROPHY, COHERENCE_FEVER, COHERENCE_EROSION]
  prerequisites: [LAMINAR_FLOW, PIROUETTE_LAGRANGIAN, TEMPORAL_COHERENCE]
  downstream_effects: [RESILIENCE, VALUE_CREATION]
license: CC-BY-SA-4.0