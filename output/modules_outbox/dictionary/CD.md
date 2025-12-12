---
term: "CD"
canonical_id: "CD"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["XAP-004_appendix_addendum_A_through_L"]
---

---
term: CD
canonical_id: CONSOLIDATED_DELIVERABLE
symbol: 
aliases: [Consolidated Deliverable]
parents: [PPS-044]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: XAP-004_appendix_addendum_A_through_L
      snippet: |
        • Energy Footprint (EF): kWh consumed per unit CD.
        • Social Footprint (SF): Person-hours externalised per unit CD (derived from Fair-Work index).
  editors: [Atlas Wolf]
  review_log: []
triad:
  art: |
    The final, countable chime of the bell, marking the end of one cycle of work. It is the minted coin of a system's labor, holding the ghost-imprint of the energy and attention it consumed.
  law: |
    A CD is a discrete, auditable unit of system output against which resource consumption (energy, labor) must be normalized. Any change to the definition of a CD unit requires a mandatory, corresponding re-baselining of all associated efficiency and externality metrics (e.g., EF, SF).
  philosophy: |
    To make the invisible costs of systemic operation visible and accountable. By tying externalities to a countable unit of output, the CD forces an ethical and economic reckoning for every action, preventing the silent accumulation of entropic or social debt.
pirouette_definition: |
  A discrete, quantifiable unit of system work or output, serving as the fundamental denominator for measuring operational efficiency and external impact. All externalities, such as the Energy Footprint (EF) and Social Footprint (SF), are normalized per unit CD to ensure auditable, comparable accounting of a system's true cost.
operational_definition:
  units: Dimensionless (unit count)
  symbol_table:
    - name: CD
      meaning: A single unit of a Consolidated Deliverable.
      dimensions: Dimensionless
      default_range: Integer > 0
  measurement:
    procedures:
      - name: Output Normalization & Externality Tagging
        outline: |
          1. Define the specific, auditable criteria for one CD unit for a given system (e.g., one completed simulation, one resolved governance query).
          2. Aggregate total resource consumption over a reporting period (e.g., kWh from power grids, person-hours from labor logs).
          3. Divide total resource consumption by the total number of CD units produced in the period to calculate metrics like EF and SF.
          4. Flag anomalous rates of CD production via governance hooks to detect potential metric manipulation.
        expected_signals: [Stable EF and SF ratios over time for a mature system, "CD manipulation flag" trigger]
        pitfalls: [Gaming the metric by redefining what constitutes a CD to artificially inflate efficiency, inaccurate data from external sources for labor or energy.]
context_windows:
  - module: XAP-004_appendix_addendum_A_through_L
    excerpt: |
      **Externality Footprint Tag**
      **Metrics:**
      • **Energy Footprint (EF):** kWh consumed per unit CD.
      • **Social Footprint (SF):** Person-hours externalised per unit CD (derived from Fair-Work index).
  - module: XAP-004_appendix_addendum_A_through_L
    excerpt: |
      **Governance Hook Outline**
      1. **Supervisory Nodes:** Three-layer oversight (Ops, Ethics, Public).
      2. **Trigger Metrics:** Γ_thr exceedance, CD manipulation flag, Externality Tag > threshold.
poetic_connections:
  motifs: [accountability, work, cost, output, footprint]
  evocative_lines:
    - "Person-hours externalised per unit CD"
    - "CD manipulation flag"
  association_matrix:
    - [ "Energy Footprint", 0.9 ]
    - [ "Social Footprint", 0.9 ]
    - [ "Governance", 0.7 ]
formal_mappings:
  candidates:
    - target: FLOP (Floating Point Operation)
      domain: CS
      mapping_kind: conceptual
      equation_hint: |
        Efficiency = CD / FLOPs
      justification: |
        CD serves as a standardized, abstract unit of "work done" by the system, analogous to how FLOPs measure computational work. It allows for efficiency comparisons by abstracting the specific nature of a task into a countable output, against which physical resources are measured.
      references: []
      confidence: 0.7
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "Normalizing resource consumption by CD provides a stable and non-manipulable measure of system efficiency."
      domain: phenomenology
      falsifier: "System operators could alter the definition of a 'completed' task to produce more CD units for the same amount of work, artificially lowering the per-CD cost. This would render the metric unstable without strict, external auditing of the CD definition itself."
      status: under-test
      links: [PPS-044]
naming_notes:
  collisions: [Compact Disc, Certificate of Deposit, Continuous Delivery]
  disambiguation: |
    Within the Pirouette Framework, CD refers exclusively to a Consolidated Deliverable, a unit of work, not a physical medium, financial instrument, or software practice. It is always used in the context of efficiency metrics like Energy Footprint (EF) or Social Footprint (SF).
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: []
  downstream_effects: [ENERGY_FOOTPRINT, SOCIAL_FOOTPRINT, GOVERNANCE_HOOK]
license: CC-BY-SA-4.0