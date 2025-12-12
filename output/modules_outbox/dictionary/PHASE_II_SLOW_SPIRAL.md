---
term: "Phase II: Slow Spiral"
canonical_id: "PHASE_II_SLOW_SPIRAL"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-HLTH-006"]
---

---
term: Phase II: Slow Spiral
canonical_id: PHASE_II_SLOW_SPIRAL
symbol: 
aliases: [Early Outpatient CR, Ritual Foundation]
parents: [DOMA-HLTH-006, PHASE_I_RE_TUNE]
children: [PHASE_III_BUILD_THE_ARENA]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-HLTH-006
      lines: "§4 Phase Mapping Table, Row 3"
      snippet: |
        Early outpatient CR | Phase II: Slow Spiral | Weeks 2–6 | Low-intensity aerobic, ritual sequencing | Monitor RPE, HR, BP, volume status; symptom flags
  editors: [auto-agent]
  review_log: []
triad:
  art: |
    The first tentative steps back into the world, tracing a gentle, widening path. It is the phase of deliberate ritual, where consistency itself is the primary medicine, building trust in a body that feels alien.
  law: |
    Initiate low-intensity aerobic activity (RPE ≤ 3/10) for short, frequent durations (e.g., 5-10 min, 1-2x/day). Progression in duration (Δt ≤ 2 min/session) is permitted only when key stability metrics (e.g., ΔHR < 10 bpm from baseline, no new symptoms) are met. The primary goal is achieving near-perfect Time Adherence (Tₐ → 1.0) over optimizing performance.
  philosophy: |
    This phase subordinates physiological gain (ΔKτ) to behavioral entrainment (Tₐ). By establishing a predictable, low-stress therapeutic rhythm, the patient builds the psychological scaffolding and physiological trust necessary for the more intensive work of Phase III. It is a direct intervention against the boom-bust cycle of premature exertion and subsequent retreat.
pirouette_definition: |
  Phase II is the early outpatient recovery stage, typically commencing 2-6 weeks post-event, characterized by the establishment of high-adherence (Tₐ), low-intensity (Γ) therapeutic rituals. Its primary objective is to build a stable foundation of consistent, safe activity and psychosocial routine, preparing the system for the controlled stress of subsequent phases. Success is measured by adherence and stability, not performance metrics like speed or power.
operational_definition:
  units: N/A (protocol)
  symbol_table:
    - name: RPE_target
      meaning: Maximum allowed Rating of Perceived Exertion
      dimensions: dimensionless
      default_range: "≤ 3/10"
    - name: Δt_max
      meaning: Maximum duration increase per successful session
      dimensions: T
      default_range: "1–2 minutes"
    - name: ΔHR_threshold
      meaning: Maximum change in heart rate from resting baseline to permit progression
      dimensions: T⁻¹
      default_range: "< 10 bpm"
  measurement:
    procedures:
      - name: Slow Spiral Session Protocol
        outline: |
          1. **Pre-session:** Measure resting HR, BP, and ask about new/changed symptoms.
          2. **Activity:** Begin prescribed aerobic activity (e.g., recumbent bike, treadmill).
          3. **Mid-session check (~1 min in):** Re-check RPE to ensure it is at or below target (e.g., ≤ 3/10).
          4. **Completion:** Complete the prescribed duration.
          5. **Post-session:** Re-check vitals (HR, BP) immediately post-activity.
          6. **Log:** Record duration, average RPE, all vitals, and any subjective notes.
          7. **Progression Check:** If post-activity ΔHR remains below threshold and no adverse symptoms are reported, the next session's duration may be increased by Δt_max.
        expected_signals: [Stable HR, Stable BP, RPE ≤ 3, Tₐ ≈ 1.0]
        pitfalls: [Patient over-exertion due to feeling "too good", Inconsistent logging of sessions, Mistaking low RPE for zero physiological stress]
context_windows:
  - module: DOMA-HLTH-006
    excerpt: |
      If within 2 weeks of surgery the patient is hemodynamically stable and wounds clean, you may begin **Phase II** guided activity—equipment-limited treadmill or recumbent bike at RPE ≤ 3/10, 5 min, two times per day. That aligns with recent safety data supporting 2-week CR initiation. Use HR, BP, O₂, symptom check 1-min in and out. Advance by 1–2 min per session only if ΔHR < 10 bpm above baseline and no flags.
  - module: DOMA-HLTH-006
    excerpt: |
      Pirouette Phase I ↔ in-hospital re-tune stage; Phase II ↔ early outpatient CR transition. Pirouette’s 4 phases map cleanly to inpatient → outpatient → build → long-term maintenance.
poetic_connections:
  motifs: [ritual, foundation, spiral, germination, patience]
  evocative_lines:
    - "the phase of deliberate ritual, where consistency itself is the primary medicine"
    - "Validates Pirouette’s “Re-Tune → early Spiral” transition without violating surgeon dogma."
  association_matrix:
    - [ "TIME_ADHERENCE", 0.9 ]
    - [ "PHASE_I_RE_TUNE", 0.8 ]
    - [ "PHASE_III_BUILD_THE_ARENA", 0.8 ]
    - [ "COHERENCE", 0.5 ]
    - [ "TEMPORAL_PRESSURE", 0.3 ]
formal_mappings:
  candidates:
    - target: Cardiac Rehabilitation Phase II (Early Outpatient)
      domain: Clinical Medicine
      mapping_kind: operational
      equation_hint: |
        RPE(t) ≤ 3 ; Tₐ → 1.0
      justification: |
        Pirouette's Slow Spiral is a structured implementation of the standard early outpatient cardiac rehabilitation phase (ACC/AHA). It operationalizes the same goals of low-intensity, supervised exercise but adds the explicit Pirouette variables of Tₐ (adherence) as the primary success metric and Γ (load) as the primary control variable.
      references:
        - title: Core Components of Cardiac Rehabilitation Programs: 2024 Update
          where: AHA Journals
          date: 2024-08-01
      confidence: 0.9
  adopted:
    - target: ACC/AHA Cardiac Rehabilitation Phase II
      rationale: The mapping is adopted because it provides immediate clinical legibility and aligns Pirouette with established, evidence-based standards of care, facilitating communication with clinicians and integration into existing healthcare systems.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "Prioritizing near-perfect Time Adherence (Tₐ) with low, stable Temporal Pressure (Γ) in Phase II leads to greater long-term gains in Coherence (Kτ) and lower program attrition rates compared to protocols that prioritize rapid increases in exercise intensity."
      domain: phenomenology
      falsifier: "A randomized controlled trial showing that an early-intensity-focused group achieves equivalent or superior long-term Kτ (e.g., peak VO₂) and Tₐ in Phase IV, with no increase in adverse events, compared to a Slow Spiral group."
      status: proposed
      links: [DOMA-HLTH-006]
naming_notes:
  collisions: [Spiral Dynamics (Integral Theory), Spiral Model (Software Development)]
  disambiguation: |
    `Slow Spiral` in Pirouette is a specific clinical protocol for early-phase rehabilitation. It describes a trajectory of slowly increasing activity duration under tight physiological constraints, and should not be confused with models of psychological or software development.
crosslinks:
  near_synonyms: []
  antonyms: [HIGH_INTENSITY_INTERVAL_TRAINING]
  prerequisites: [PHASE_I_RE_TUNE]
  downstream_effects: [PHASE_III_BUILD_THE_ARENA, COHERENCE, TIME_ADHERENCE]
license: CC-BY-SA-4.0
---

# Phase II: Slow Spiral

## Canonical (Pirouette)
Phase II is the early outpatient recovery stage, typically commencing 2-6 weeks post-event, characterized by the establishment of high-adherence (Tₐ), low-intensity (Γ) therapeutic rituals. Its primary objective is to build a stable foundation of consistent, safe activity and psychosocial routine, preparing the system for the controlled stress of subsequent phases. Success is measured by adherence and stability, not performance metrics like speed or power.

## Clinician's Summary
This phase maps directly to standard early outpatient Cardiac Rehabilitation (CR Phase II), typically lasting from weeks 2 to 6 post-event. It consists of physician-prescribed, low-intensity aerobic exercise (e.g., RPE ≤ 3/10 on a Borg scale) with very gradual increases in duration. The protocol emphasizes consistency and safety, using metrics like heart rate response (ΔHR) and symptoms as gates for progression. It is fully consistent with ACC/AHA guidelines and recent safety data supporting CR initiation two weeks post-surgery.

## Glossary Links
- See also: [Phase I: Re-Tune](<#>), [Phase III: Build the Arena](<#>), [Time Adherence (Tₐ)](<#>)