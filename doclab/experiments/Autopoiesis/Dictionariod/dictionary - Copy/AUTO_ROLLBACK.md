---
term: "Auto-rollback"
canonical_id: "AUTO_ROLLBACK"
symbol: ""
aliases: [kill-switch]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DYNA-005_coherent_adherence_protocol"]
---

---
term: Auto-rollback
canonical_id: AUTO_ROLLBACK
symbol:
aliases: [kill-switch]
parents: [DYNA-005]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DYNA-005_coherent_adherence_protocol
      lines: "L50-L52"
      snippet: |
        Every deployment sets λ and publishes a **Residue Budget**; breaching it triggers auto-rollback (“kill-switch”).
  editors: [Lexicon Scribe]
  review_log: []
triad:
  art: |
    A circuit breaker that trips when a system's ethical debt exceeds its credit. It is the network's reflexive flinch from harm, a promise encoded in logic that the system will undo its own overreach before causing lasting damage.
  law: |
    If the measured Dark Residue (\(\mathcal D\)) exceeds the preregistered public Residue Budget for a given epoch, all system configuration changes implemented during that epoch are automatically reverted to their state at the epoch's start. This action is non-discretionary and must be logged publicly.
  philosophy: |
    Auto-rollback codifies the principle that system autonomy is conditional upon its adherence to explicit, public safety bounds. It moves safety from a post-hoc "damage control" problem to a pre-negotiated, self-enforcing covenant, ensuring that the system's pursuit of coherence never justifies the violation of its ethical charter.
pirouette_definition: |
  An automated safety protocol mandated by the Coherent Adherence Protocol v2 (CAP v2). It acts as a kill-switch, reverting all system changes made within a monitoring period if the measured Dark Residue (\(\mathcal D\)) surpasses a publicly declared Residue Budget. This mechanism provides a hard, auditable backstop against the accumulation of negative externalities like attention debt or autonomy loss.
operational_definition:
  units: Dimensionless (boolean trigger)
  symbol_table:
    - name: \(\mathcal D\)
      meaning: Dark Residue functional; a weighted sum of measured negative externalities.
      dimensions: Contextual (e.g., bits, normalized cost)
      default_range: "[0, ∞)"
    - name: \(B_\mathcal{D}\)
      meaning: Residue Budget; a publicly declared, pre-committed upper bound for \(\mathcal D\).
      dimensions: Same as \(\mathcal D\)
      default_range: Contextual, set per-deployment
  measurement:
    procedures:
      - name: Residue Budget Monitoring & Enforcement
        outline: |
          1. At the start of an operational epoch, record the system's revertible configuration state.
          2. Continuously measure the components of the Dark Residue functional (\(\mathcal D\)) throughout the epoch.
          3. Compare the integrated value of \(\mathcal D\) against the pre-published Residue Budget \(B_\mathcal{D}\).
          4. If \(\mathcal D > B_\mathcal{D}\), trigger the rollback procedure, reverting system parameters to the recorded state from step 1.
          5. Log the breach and the rollback event in the public Residue Ledger.
        expected_signals: [Time-series of \(\mathcal D\), binary trigger signal]
        pitfalls: [Measurement lag causing delayed rollback, gaming the metrics that constitute \(\mathcal D\), defining a 'revertible' state in systems with hysteresis]
context_windows:
  - module: DYNA-005_coherent_adherence_protocol
    excerpt: |
      Define the Dark Residue functional \(\mathcal D\) as a sum of welfare divergence, externalized risk, attention debt, and autonomy loss. Every deployment sets a multiplier \(\lambda\) and publishes a **Residue Budget**; breaching it triggers auto-rollback (“kill-switch”).
  - module: DYNA-005_coherent_adherence_protocol
    excerpt: |
      Preregistered Tests (so this stays falsifiable) ... T3 · **Residue test:** measured \(\mathcal D\) stays within budget; if exceeded, auto-rollback occurs.
poetic_connections:
  motifs: [circuit breaker, safety net, covenant, self-correction, immune response]
  evocative_lines:
    - "breaching it triggers auto-rollback (“kill-switch”)"
    - "The room tuned itself. The song was almost as perfect—and everyone stayed to sing an encore."
  association_matrix:
    - [ "DARK_RESIDUE", 0.9 ]
    - [ "RESIDUE_BUDGET", 0.9 ]
    - [ "COHERENT_ADHERENCE_PROTOCOL", 0.7 ]
    - [ "SHADOW_GAUGE", 0.4 ]
formal_mappings:
  candidates:
    - target: Transaction rollback
      domain: Computer Science
      mapping_kind: conceptual
      equation_hint:
      justification: |
        Like a database transaction that is rolled back upon failing an integrity constraint, Auto-rollback reverts system state changes when an ethical/safety constraint (the Residue Budget) is violated. It ensures atomicity and integrity for system interventions under CAP v2.
      references:
        - title: "Transaction Processing: Concepts and Techniques"
          where: "Chapter 7, 'Concurrency Control'"
          date: 1992-09-01
      confidence: 0.8
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The Auto-rollback mechanism reliably prevents sustained breaches of the public Residue Budget in any CAP v2 compliant system."
      domain: experiment
      falsifier: "A demonstration of a CAP v2 system where the measured Dark Residue \(\mathcal D\) exceeds its budget for a duration longer than one measurement cycle without triggering a rollback."
      status: proposed
      links: [DYNA-005]
naming_notes:
  collisions: []
  disambiguation: |
    Distinct from manual 'reversion' or 'undo' functions. Auto-rollback is an automated, non-discretionary safety protocol triggered by a specific, pre-declared quantitative threshold (\(\mathcal D > B_\mathcal{D}\)), not by user or operator choice.
crosslinks:
  near_synonyms: [KILL_SWITCH]
  antonyms: [INERTIAL_LEAP]
  prerequisites: [DARK_RESIDUE, RESIDUE_BUDGET]
  downstream_effects: []
license: CC-BY-SA-4.0