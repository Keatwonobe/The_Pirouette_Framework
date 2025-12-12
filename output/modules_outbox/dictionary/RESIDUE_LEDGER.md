---
term: "Residue Ledger"
canonical_id: "RESIDUE_LEDGER"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DYNA-005_coherent_adherence_protocol"]
---

---
term: Residue Ledger
canonical_id: RESIDUE_LEDGER
symbol: 
aliases: [Externality Log, Harm Ledger, Dark Residue Log]
parents: [DYNA-005]
children: [PPS-015, DOMA-QCOMP-001, DOMA-203]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DYNA-005
      lines: "§4.6, §5"
      snippet: |
        6) **Residue Ledger** — log externalities into D with corrective obligations (§5).
  editors: [Agent-Compiler-v3.1]
  review_log: []
triad:
  art: |
    A ship's log that records not just the journey, but the wake left behind. It is the shadow cast by a bright light, meticulously measured and accounted for. Honesty in the face of unintended consequence.
  law: |
    All deployments under the Coherent Adherence Protocol must maintain a public, immutable, and auditable log of measured negative externalities (Dark Residue, D). The cumulative value in this log must not exceed the pre-declared Residue Budget, under penalty of automated rollback.
  philosophy: |
    To make invisible costs visible. The Ledger enforces ethical accountability by transforming abstract "harm" into a concrete, auditable quantity that constrains system behavior, ensuring that coherence gains are not paid for with unacknowledged externalities.
pirouette_definition: |
  A public, append-only, machine-readable log that tracks the measured value of the Dark Residue functional (D) for a system operating under the Coherent Adherence Protocol. Each entry quantifies negative externalities—such as attention debt or autonomy loss—and is checked against a pre-published Residue Budget to enforce safety constraints like automated system rollbacks.
operational_definition:
  units: Dimensionless (by convention, as a weighted sum)
  symbol_table:
    - name: D
      meaning: Dark Residue functional; total measured negative externality.
      dimensions: dimensionless
      default_range: "[0, Residue_Budget]"
    - name: V_obs
      meaning: Observer cost; a component of D representing attention debt.
      dimensions: Action (energy × time)
      default_range: contextual
    - name: Loss(autonomy)
      meaning: Mutual information between system levers and unconsented private state.
      dimensions: dimensionless (bits)
      default_range: "[0, ∞)"
  measurement:
    procedures:
      - name: Residue Accounting
        outline: |
          At discrete time intervals (e.g., per epoch, user session, or control action), measure the components of the Dark Residue functional (D). This includes: (1) calculating imposed observer cost (V_obs) for Attention Debt; (2) measuring mutual information between CAP levers and private user state for Autonomy Loss; (3) running counterfactual models for welfare divergence. Sum the weighted components and append the timestamped result and its delta to the public ledger.
        expected_signals: [Time-series data for D, discrete events marking budget breaches]
        pitfalls: [Inaccurate measurement of components (e.g., miscalibrated V_obs meter), gaming the metrics (optimizing one component of D at the expense of an unmeasured one), ledger tampering (requires cryptographic security)]
context_windows:
  - module: DYNA-005
    excerpt: |
      **Ethical Covenant** ... 6) **Residue Ledger** — log externalities into D with corrective obligations (§5).
  - module: DYNA-005
    excerpt: |
      Every deployment sets λ and publishes a **Residue Budget**; breaching it triggers auto-rollback (“kill-switch”).
  - module: DYNA-005
    excerpt: |
      **Preregistered Tests** ... T3 · **Residue test:** measured D stays within budget; if exceeded, auto-rollback occurs.
poetic_connections:
  motifs: [accountability, shadow bookkeeping, the cost of coherence, unseen debts]
  evocative_lines:
    - "...breaching it triggers auto-rollback ('kill-switch')."
    - "It changes the *room*, not the throat."
  association_matrix:
    - [ "DARK_RESIDUE", 0.9 ]
    - [ "COHERENT_ADHERENCE_PROTOCOL", 0.8 ]
    - [ "SHADOW_GAUGE", 0.7 ]
    - [ "INERTIAL_LEAP", 0.2 ]
formal_mappings:
  candidates:
    - target: Error Budget
      domain: Software Engineering
      mapping_kind: conceptual
      equation_hint: |
        `Reliability = 1 - (Errors / Total_Ops)` vs. `Allowable_Harm = Budget - D`
      justification: |
        Like an SRE error budget, a Residue Budget defines an acceptable level of "unavailability" or harm. It is a pre-negotiated allowance for negative outcomes, and exhausting the budget triggers a halt to new changes (or a rollback) to prevent further harm and force remediation.
      references:
        - title: Site Reliability Engineering
          where: Chapter 3, "Embracing Risk"
          date: 2016-04-16
      confidence: 0.8
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The existence of a public Residue Ledger with a strict budget and automated rollback is sufficient to prevent runaway negative externalities in a CAPv2 deployment."
      domain: phenomenology
      falsifier: "Demonstrate a CAPv2 system where measured D stays within budget, but significant, un-instrumented harm still occurs, implying the D functional is incomplete. Alternatively, show a system that learns to game the D measurement itself."
      status: proposed
      links: [DYNA-005]
naming_notes:
  collisions: ["Ledger" is a common term in cryptocurrency (e.g., Distributed Ledger Technology).]
  disambiguation: |
    Unlike a financial or distributed ledger, the Residue Ledger does not primarily record transactions between parties. It records the state of a system's cumulative negative impact against a unilateral budget. Its immutability serves auditability and enforcement, not distributed consensus.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [DARK_RESIDUE, COHERENT_ADHERENCE_PROTOCOL, SHADOW_GAUGE]
  downstream_effects: []
license: CC-BY-SA-4.0
---