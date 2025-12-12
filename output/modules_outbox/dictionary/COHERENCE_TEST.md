---
term: "Coherence Test"
canonical_id: "COHERENCE_TEST"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-031"]
---

---
term: Coherence Test
canonical_id: COHERENCE_TEST
symbol: Kτ ≥ 0.95 ∧ dKτ/dt ≥ 0
aliases: [Maximal Coherence Test, Stability & Consensus Test]
parents: [DOMA-031]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-031
      lines: "55-65"
      snippet: |
        Once the Temporal Stability Clause is satisfied, the proposed synthesis must pass a formal measurement of its coherence potential. The motion is ratified only if it satisfies two conditions simultaneously:
        1. High Coherence (Kτ): ... Threshold: `Kτ ≥ 0.95`
        2. Positive Coherence Stability (dKτ/dt): ... Threshold: `dKτ/dt ≥ 0`.
  editors: [auto-scribe v4.1]
  review_log: []
triad:
  art: |
    A change must prove its stillness before it is allowed to move the whole. It is a test not only of the height of a wave of consensus, but of the quiet, stable depth of the ocean beneath it.
  law: |
    A motion for Constitutional Reforging is ratified if and only if it achieves both High Coherence (Kτ ≥ 0.95 support from the Weaver's Conclave) and Positive Coherence Stability (dKτ/dt ≥ 0) over a 30-day deliberation period.
  philosophy: |
    To protect the framework's core identity from reactive, transient pressures and ensure evolution proceeds only through insights that are both deeply resonant and stably supported. It selects for persistence and wisdom over fleeting popularity, embodying the principle that the most profound changes must be made in the quietest moments.
pirouette_definition: |
  The Coherence Test is the formal, two-part validation protocol required to ratify a motion for *Constitutional Reforging*. Applied after the Temporal Stability Clause is met, the test mandates that a proposal simultaneously satisfy a condition of high consensus and a condition of stable consensus. The test is passed if and only if both the High Coherence threshold (`Kτ ≥ 0.95`) and the Positive Coherence Stability threshold (`dKτ/dt ≥ 0`) are met over a standardized 30-day deliberation period.
operational_definition:
  units: Dimensionless (for Kτ) and T⁻¹ (for dKτ/dt).
  symbol_table:
    - name: Kτ
      meaning: High Coherence; the instantaneous level of consensus for a proposal, measured as the fraction of approving members in the Weaver's Conclave.
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: dKτ/dt
      meaning: Positive Coherence Stability; the time-derivative of the consensus level, measuring whether support is growing, stable, or decaying.
      dimensions: T⁻¹
      default_range: "contextual"
  measurement:
    procedures:
      - name: Consensus Measurement (Kτ)
        outline: |
          At the conclusion of the 30-day deliberation period, a formal vote is held among the Weaver's Conclave. Kτ is calculated as `approvals / (approvals + rejections)`. The final value must be ≥ 0.95.
        expected_signals: [A final fractional value for Kτ.]
        pitfalls: [Miscounting abstentions, ambiguity in the motion text leading to voter confusion.]
      - name: Stability Measurement (dKτ/dt)
        outline: |
          Throughout the 30-day deliberation period, intent-to-vote or support `Kτ(t)` is polled at regular intervals. The time-derivative `dKτ/dt` is calculated from the time series, typically via the slope of a linear regression. The final calculated slope must be non-negative.
        expected_signals: [A time series of support values, a final slope value.]
        pitfalls: [Insufficient polling frequency yielding a noisy derivative, last-minute campaigning creating artificial non-stationarity.]
context_windows:
  - module: DOMA-031
    excerpt: |
      The motion is ratified only if it satisfies two conditions simultaneously: High Coherence (Kτ), measured by a vote of the Weaver's Conclave, and Positive Coherence Stability (dKτ/dt), where the consensus must be stable and not actively decaying over a 30-day deliberation period. This two-fold test ensures the framework evolves through changes that are both deeply resonant and demonstrably stable.
  - module: DOMA-031
    excerpt: |
      Membership in the Weaver's Conclave is not a title; it is an active function. To maintain their position, each Weaver must, within each major version cycle, successfully author or sponsor a motion that passes a Coherence Test. This is a grounding ritual ensuring that the guardians of the framework are also its most active and dedicated cultivators.
poetic_connections:
  motifs: [stillness, stability, resonance, consensus, crucible, quiet depths]
  evocative_lines:
    - "The most profound changes must be made in the quietest moments."
    - "This two-fold test ensures the framework evolves through changes that are both deeply resonant and demonstrably stable."
  association_matrix:
    - [ "TEMPORAL_STABILITY_CLAUSE", 0.9 ]
    - [ "PRINCIPLE_OF_MAXIMAL_COHERENCE", 0.8 ]
    - [ "CONSTITUTIONAL_REFORGING", 0.9 ]
    - [ "WEAVERS_CONCLAVE", 0.7 ]
formal_mappings:
  candidates:
    - target: Proportional-Derivative (PD) stability criterion
      domain: CM
      mapping_kind: conceptual
      equation_hint: |
        System Response ∝ K_p * e(t) + K_d * de/dt
      justification: |
        The Coherence Test functions analogously to a PD controller's stability check. The high consensus requirement (Kτ) is like the proportional term, ensuring the system is close to its target state (full consensus). The stability requirement (dKτ/dt) is like the derivative term, ensuring the system's velocity is not destabilizing (i.e., consensus is not actively collapsing), thus damping oscillations and preventing ratification based on transient peaks.
      references:
        - title: Feedback Control of Dynamic Systems
          where: "Chapter 4: Basic Properties of Feedback"
          date: 2010-01-01
      confidence: 0.3
  adopted:
    - target: null
      rationale: null
      confidence: 0.0
constraints_and_falsifiers:
  claims:
    - statement: "The `dKτ/dt ≥ 0` condition prevents the ratification of proposals that achieve high but transient consensus (i.e., 'flash-in-the-pan' agreement)."
      domain: phenomenology
      falsifier: "Historical analysis demonstrates that a majority of proposals rejected solely on the `dKτ/dt < 0` condition are later re-proposed and ratified with stable support, indicating the clause primarily introduces bureaucratic lag rather than improving long-term decision quality."
      status: proposed
      links: [DOMA-031]
naming_notes:
  collisions: [Kτ may be confused with symbols for kinetic energy (K) or a time constant/torque (τ).]
  disambiguation: |
    In the context of Pirouette governance, `Kτ` exclusively denotes the Coherence score, a dimensionless measure of consensus. `dKτ/dt` is not a physical velocity but a measure of the rate of change of this consensus. It is distinct from Temporal Pressure (Γ).
crosslinks:
  near_synonyms: []
  antonyms: [SIMPLE_MAJORITY_VOTE]
  prerequisites: [TEMPORAL_STABILITY_CLAUSE]
  downstream_effects: [CONSTITUTIONAL_REFORGING]
license: CC-BY-SA-4.0
---