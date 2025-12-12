---
term: "Phase I: Re-Tune"
canonical_id: "PHASE_I_RE_TUNE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-HLTH-006"]
---

---
term: Phase I: Re-Tune
canonical_id: PHASE_1_RE_TUNE
symbol: N/A
aliases: [Inpatient Rehab, Post-Operative Stabilization]
parents: [DOMA-HLTH-006]
children: [PHASE_2_SLOW_SPIRAL]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-HLTH-006
      lines: "§4, Table Row 1"
      snippet: |
        Inpatient / early post-op | Phase I: Re-Tune | 0–2 weeks (or until stable) | Bed mobility, breathing, short ambulation | Sternal stability, hemodynamics, wound healing, arrhythmias
  editors: [chain-of-thought-agent]
  review_log: []
triad:
  art: |
    After the cacophony of a physiological crisis, this is the first quiet note. It is the body finding its new keynote, learning to breathe and stand in a changed landscape before attempting to walk. The focus is not on progress, but on presence and stability.
  law: |
    Progress to Phase II is permitted if and only if the patient achieves hemodynamic stability at rest and with minimal exertion (e.g., ambulation to bathroom), demonstrates stable wounds, and has no uncontrolled arrhythmias. All activities are constrained by a Perceived Exertion (RPE) of ≤ 2/10.
  philosophy: |
    To build a lasting structure, one must first secure the foundation. This phase actively rejects the pressure for premature "recovery" in favor of establishing a robust physiological baseline. It is a disciplined investment in stability that pays dividends in all subsequent phases by preventing setbacks.
pirouette_definition: |
  The initial, inpatient post-event phase of recovery, typically lasting from hours to two weeks. It is dedicated to achieving hemodynamic stability, managing acute post-procedural variables (e.g., wound healing, pain), and re-establishing foundational organismal functions like independent breathing, bed mobility, and short-distance ambulation under strict clinical supervision. The goal is safe discharge and readiness for low-intensity outpatient activity, not performance improvement.
operational_definition:
  units: Categorical (Phase Descriptor)
  symbol_table:
    - name: RPE_max
      meaning: Maximum allowable Rating of Perceived Exertion (0-10 scale)
      dimensions: dimensionless
      default_range: "[0, 2]"
    - name: ΔHR_limit
      meaning: Maximum allowable heart rate increase over resting baseline
      dimensions: T⁻¹ (beats/minute)
      default_range: "< 20 bpm for ambulation"
  measurement:
    procedures:
      - name: Phase I Status Assessment
        outline: |
          1. Confirm patient is in an inpatient setting following a qualifying cardiac event.
          2. Review clinical charts for vital sign stability (HR, BP, SpO2) over a 24-hour period.
          3. Assess wound status (e.g., sternal, access site) for signs of infection or dehiscence.
          4. Observe patient performing basic activities of daily living (ADLs) and short ambulation.
          5. The phase concludes upon physician clearance for hospital discharge to home or subacute rehab.
        expected_signals: [Stable vitals, clean wounds, ability to ambulate >50 feet with or without assistive device, RPE < 3/10 during activity]
        pitfalls: [Conflating prolonged ICU stay with Re-Tune (ICU is pre-phase stabilization), premature discharge before ambulation is safely established]
context_windows:
  - module: DOMA-HLTH-006
    excerpt: |
      **Inpatient / early post-op (Clinical Phase) ↔ Phase I: Re-Tune (Pirouette Phase).** Typical Duration: 0–2 weeks (or until stable). Core Activities: Bed mobility, breathing, short ambulation. Key Safety Checks: Sternal stability, hemodynamics, wound healing, arrhythmias.
  - module: DOMA-HLTH-006
    excerpt: |
      *Cardiac rehabilitation: a Class I recommendation* (CCJM review) | CR recommended *in hospital and early outpatient* after MI or surgery | Pirouette Phase I ↔ in-hospital re-tune stage; Phase II ↔ early outpatient CR transition.
poetic_connections:
  motifs: [Foundation, Stillness, Recalibration, Grounding, Baseline, Breath]
  evocative_lines:
    - "find the first quiet note after the crash"
    - "investment in stability"
  association_matrix:
    - [ "Γ (Temporal Pressure)", 0.8 ] # Goal is to minimize Γ
    - [ "Kτ (Coherence)", 0.5 ] # Establishes the initial Kτ baseline
    - [ "Phase II: Slow Spiral", 0.9 ] # Direct prerequisite
formal_mappings:
  candidates: []
  adopted:
    - target: Phase I Cardiac Rehabilitation (Clinical)
      domain: Medicine
      mapping_kind: operational
      justification: |
        The Pirouette Framework explicitly maps "Re-Tune" to the standard clinical definition of Phase I (inpatient) Cardiac Rehabilitation. The activities, goals (stabilization for discharge), duration, and safety monitoring described in DOMA-HLTH-006 align directly with ACC/AHA guidelines for this stage of recovery.
      references:
        - title: Cardiac Rehabilitation - StatPearls
          where: NCBI Bookshelf (NBK537196)
          date: 2024-07-29
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "For post-sternotomy patients, Phase I Re-Tune activities must strictly adhere to sternal precautions (e.g., no lifting >5-10 lbs, no asynchronous upper body movement) to prevent wound dehiscence."
      domain: phenomenology
      falsifier: "Evidence from large-scale trials showing that less restrictive 'Keep Your Move in the Tube' protocols result in equal or lower rates of sternal complications compared to traditional precautions."
      status: supported
      links: [DOMA-HLTH-006]
naming_notes:
  collisions: []
  disambiguation: |
    "Re-Tune" is an active process of stabilization and re-establishing baseline function. It should not be confused with passive "bed rest." The activities, though minimal, are prescribed and goal-directed towards achieving discharge readiness.
crosslinks:
  near_synonyms: [INPATIENT_CARDIAC_REHAB]
  antonyms: [PHASE_4_COHERENT_LIFE]
  prerequisites: [CARDIAC_EVENT]
  downstream_effects: [PHASE_2_SLOW_SPIRAL]
license: CC-BY-SA-4.0
---