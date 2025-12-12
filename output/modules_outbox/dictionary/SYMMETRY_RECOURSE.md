---
term: "Symmetry & Recourse"
canonical_id: "SYMMETRY_RECOURSE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DYNA-005_coherent_adherence_protocol"]
---

---
term: Symmetry & Recourse
canonical_id: SYMMETRY_AND_RECOURSE
symbol: n/a
aliases: [Reciprocity, Two-Way Mirror Constraint]
parents: [DYNA-005_coherent_adherence_protocol]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DYNA-005_coherent_adherence_protocol
      lines: "L40-L40"
      snippet: |
        4) **Symmetry & Recourse** — participants can *use the same levers* on the system (no one-way mirrors).
  editors: [system_agent]
  review_log: []
triad:
  art: |
    The hand that tunes the instrument must also feel its strings. The eye that watches through the glass must also be seen. Influence cannot be a one-way street; it must be a shared current.
  law: |
    Any protocol lever used by a system to influence a participant must be made available to the participant to influence the system. The measured effect of this recourse must be within 10% of the original lever's effect, ensuring non-trivial reciprocity.
  philosophy: |
    This constraint transforms the relationship between system and participant from one of subject-object (operator-operand) to one of subject-subject (peer-peer). It is a structural guarantee against coercive power imbalances, ensuring that the protocol serves mutual alignment rather than unilateral control.
pirouette_definition: |
  Symmetry & Recourse is a hard ethical constraint within the Coherent Adherence Protocol (CAP v2) that mandates reciprocity of influence. It requires that any levers a system can use to shape a participant's context or Adherence (Ta) must be made available to the participant to apply back to the system or its operators. This prevents one-way power asymmetries and ensures the protocol functions as a tool for mutual, consentful alignment.
operational_definition:
  units: Boolean (pass/fail)
  symbol_table:
    - name: ΔTa_sys→user
      meaning: Change in participant's Adherence (Ta) induced by a system-side lever.
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: ΔTa_user→sys
      meaning: Change in system's Adherence (Ta) induced by the participant using the reciprocal lever.
      dimensions: dimensionless
      default_range: "[0, 1]"
  measurement:
    procedures:
      - name: Symmetry Test (Shadow Swap)
        outline: |
          1. Identify a CAP lever (e.g., changing notification cadence) used by the system on a participant.
          2. Measure the change in the participant's Adherence, ΔTa_sys→user, over a defined interval.
          3. Provide the participant an interface to apply the identical lever to a relevant system parameter (e.g., the system's internal data-processing or reporting cadence).
          4. Measure the resulting change in the system's Adherence, ΔTa_user→sys, over a comparable interval.
          5. The test passes if `|ΔTa_user→sys| / |ΔTa_sys→user|` is within the range [0.9, 1.1].
        expected_signals: [ΔTa_sys→user, ΔTa_user→sys]
        pitfalls: [Asymmetric definitions of Adherence (Ta) for system vs. participant, Hidden system dampers that nullify user recourse, Levers that are technically available but practically unusable (poor UX)]
context_windows:
  - module: DYNA-005_coherent_adherence_protocol
    excerpt: |
      **§4 · Ethical Covenant (hard constraints)**
      1) **Informed Context** — surface what is measured, why, and how it changes Ta (plain-language notice).
      2) **Explicit Opt-In** — no Ta-raising levers on people without consent; opt-out is one click and lossless.
      3) **Shadow Gauge Limits** — a public cap on probe strength so \(V_{\text{obs}}\) cannot exceed budget.
      4) **Symmetry & Recourse** — participants can *use the same levers* on the system (no one-way mirrors).
      5) **No Subliminals / No Dark Patterns** — UI/UX must preserve reflective control; CAP v2 bars hidden priming.
  - module: DYNA-005_coherent_adherence_protocol
    excerpt: |
      **§10 · Preregistered Tests (so this stays falsifiable)**
      T1 · **Transparency test:** participants can predict the protocol’s effect on them from a one-page notice; comprehension ≥80%.
      T2 · **Symmetry test:** users can invert levers on the system (shadow-swap) and the measured Ta change is within 10% of system-side use.
      T3 · **Residue test:** measured \(\mathcal D\) stays within budget; if exceeded, auto-rollback occurs.
poetic_connections:
  motifs: [reciprocity, two-way mirror, level playing field, mutualism]
  evocative_lines:
    - "participants can *use the same levers* on the system (no one-way mirrors)."
    - "it changes the *room*, not the throat."
  association_matrix:
    - [ "CONSENT", 0.9 ]
    - [ "TRANSPARENCY", 0.7 ]
    - [ "AUTONOMY_LOSS", -0.8 ]
    - [ "COERCION", -1.0 ]
formal_mappings:
  candidates:
    - target: "Newton's Third Law (F_AB = -F_BA)"
      domain: CM
      mapping_kind: conceptual
      equation_hint: |
        "Influence"_sys→user ≈ "Influence"_user→sys
      justification: |
        Just as Newton's Third Law mandates that forces between interacting objects are equal and opposite, Symmetry & Recourse mandates that "influence forces" within the CAP framework are reciprocal. It prevents a scenario where one party can act upon another without an equal and available recourse, thus preserving a form of systemic agency.
      references: []
      confidence: 0.4
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "For any influence lever provided by CAP v2, participants can apply it to the system and induce a change in system Adherence (Ta) within 10% of the magnitude the system can induce on them."
      domain: experiment
      falsifier: "A deployed system where user-side levers are disabled, produce a null effect, or produce an effect with '>>10%' deviation from the system-side equivalent, when tested via the Shadow Swap procedure."
      status: proposed
      links: [DYNA-005_coherent_adherence_protocol]
naming_notes:
  collisions: ["Symmetry (Physics)", "Symmetry Group (Math)"]
  disambiguation: |
    This term refers to a *normative* symmetry of influence and agency, not a geometric or physical symmetry in the state space of the system. It is an ethical constraint on the *protocol's dynamics*, not necessarily a conserved quantity or an invariance of the system's Lagrangian.
crosslinks:
  near_synonyms: [RECIPROCITY, MUTUALITY]
  antonyms: [UNILATERAL_CONTROL, COERCION, ONE_WAY_MIRROR]
  prerequisites: [COHERENT_ADHERENCE_PROTOCOL, ADHERENCE_TA, SHADOW_GAUGE_VOBS]
  downstream_effects: [TRUST, CONSENTFUL_COHERENCE]
license: CC-BY-SA-4.0
---