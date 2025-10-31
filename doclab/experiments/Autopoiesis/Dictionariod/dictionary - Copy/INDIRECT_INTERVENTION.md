---
term: "Indirect Intervention"
canonical_id: "INDIRECT_INTERVENTION"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-098"]
---

---
term: Indirect Intervention
canonical_id: INDIRECT_INTERVENTION
symbol: 
aliases: [Rebuilding the Riverbed, Autopoietic Solution]
parents: [DOMA-098]
children: [RIT-RESTORATION-PROTOCOL-2.0]
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-098
      lines: "L102-L107"
      snippet: |
        Indirect Intervention (Rebuilding the Riverbed): This is the more profound, autopoietic solution. Instead of just supplying the key, we rebuild the system's own capacity to produce it. This means fostering the conditions for a healthy Alchemical Union (CORE-012)... This gambit does not just fix the problem; it teaches the system how to prevent the problem from recurring.
  editors: [chain-of-thought-agent]
  review_log: []
triad:
  art: |
    To heal a river, one does not attack the stillness. One rebuilds the riverbed and teaches the water to flow again on its own.
  law: |
    An Indirect Intervention is successful if and only if, after the intervention is withdrawn, the target system autonomously maintains production of the formerly absent coherent signal above a pre-defined homeostatic baseline.
  philosophy: |
    This concept shifts the therapeutic focus from combative replacement to generative cultivation. It reframes healing as the restoration of a system's innate capacity for self-sufficiency and health, rather than a sustained dependency on external inputs.
pirouette_definition: |
  A therapeutic tactic, typically a Daedalus Gambit, that restores a system's endogenous capacity to generate a specific, missing coherent signal. Unlike a Direct Intervention, which supplies the signal exogenously, an Indirect Intervention repairs the underlying generative process (e.g., an Alchemical Union) to ensure durable, autopoietic self-regulation and a lasting increase in the system's internal coherence (`K_τ`).
operational_definition:
  units: Dimensionless (process class). Its effects are measured by the rate of change of a target signal's production (e.g., mol/s).
  symbol_table: []
  measurement:
    procedures:
      - name: Longitudinal Signal Restoration Assay
        outline: |
          1. Establish a stable baseline measurement of the target coherent signal (e.g., fecal butyrate concentration) in a system exhibiting Coherence Atrophy.
          2. Administer the Indirect Intervention (e.g., a specific prebiotic fiber regimen) for a defined period `T_intervention`.
          3. Cease the intervention and observe the system through a washout period of `T_washout` (e.g., >3 half-lives of the system's signal-producing components).
          4. Measure the target signal at `T_washout`. A successful intervention is marked by a sustained signal level significantly above the initial baseline.
        expected_signals: [Sustained elevation of target coherent signal post-washout, Reduction in downstream pathology markers (e.g., inflammatory cytokines)]
        pitfalls: [Incorrect identification of the limiting substrate or process, Confounding environmental variables (e.g., diet), Insufficient intervention duration to induce systemic adaptation]
context_windows:
  - module: DOMA-098
    excerpt: |
      Indirect Intervention (Rebuilding the Riverbed): This is the more profound, autopoietic solution. Instead of just supplying the key, we rebuild the system's own capacity to produce it. This means fostering the conditions for a healthy Alchemical Union (CORE-012) within the biological forge of the microbiome, using prebiotics (the "raw materials") and probiotics (the "skilled workers"). This gambit does not just fix the problem; it teaches the system how to prevent the problem from recurring.
  - module: DOMA-098
    excerpt: |
      It teaches us that the most profound act of healing is often not an act of war, but an act of cultivation. For generations, we have practiced the medicine of the battlefield... But we have forgotten the medicine of the garden, which asks a quieter question: not "What must be killed?" but "What is thirsty?" The Antidote of Coherence is the wisdom to know when to put down the sword and pick up the seed.
poetic_connections:
  motifs: [cultivation, gardening, teaching, autopoiesis, restoring flow, rebuilding the riverbed]
  evocative_lines:
    - "What is thirsty?"
    - "put down the sword and pick up the seed"
    - "This gambit does not just fix the problem; it teaches the system..."
  association_matrix:
    - [ "DIRECT_INTERVENTION", 0.9 ]
    - [ "ALCHEMICAL_UNION", 0.8 ]
    - [ "COHERENCE_ATROPHY", 0.7 ]
    - [ "DAEDALUS_GAMBIT", 0.6 ]
formal_mappings:
  candidates:
    - target: System Identification & Adaptive Control
      domain: CM
      mapping_kind: conceptual
      equation_hint:
      justification: |
        Whereas Direct Intervention acts as a simple forcing function in an open-loop system, Indirect Intervention is analogous to adaptive control. It is a meta-intervention that modifies the parameters of the system's own internal "plant" (the signal generator), improving its autonomous, closed-loop performance.
      references:
        - title: Adaptive Control
          where: K.J. Åström & B. Wittenmark, Section 1.1
          date: 2008-01-01
      confidence: 0.5
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "For a system diagnosed with Coherence Atrophy, a successful Indirect Intervention will durably restore target signal production to >75% of a healthy homeostatic baseline, a state that persists for >3 turnover cycles of the generative components after the intervention ceases."
      domain: phenomenology
      falsifier: "If, after the intervention and washout period, the signal production rate reverts to the pre-intervention baseline, the intervention was either ineffective or merely a masked Direct Intervention with a long decay constant."
      status: proposed
      links: [DOMA-098]
naming_notes:
  collisions: []
  disambiguation: |
    Critically distinct from Direct Intervention. Direct Intervention *supplies* a missing signal (giving a fish), temporarily alleviating a symptom. Indirect Intervention *restores the capacity to produce* the signal (teaching to fish), correcting the root pathology.
crosslinks:
  near_synonyms: []
  antonyms: [DIRECT_INTERVENTION]
  prerequisites: [COHERENCE_ATROPHY, ALCHEMICAL_UNION]
  downstream_effects: [COHERENCE_RESTORATION]
license: CC-BY-SA-4.0