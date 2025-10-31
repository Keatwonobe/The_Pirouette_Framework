---
term: "Phase III: Build the Arena"
canonical_id: "PHASE_III_BUILD_THE_ARENA"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-HLTH-006"]
---

term: Phase III: Build the Arena
canonical_id: PHASE_III_BUILD_THE_ARENA
symbol: 
aliases: [Active Training Period]
parents: [DOMA-HLTH-006]
children: []
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-HLTH-006
      lines: "L63-L66"
      snippet: |
        | Active training period    | Phase III: Build the Arena | Weeks 6–12 (or up to ~4–6 mo) | Structured strength + aerobic progression    | ECG monitoring, gradual load increments, lab monitoring     |
  editors: [Agent: ThoughtWeaver]
  review_log: []
triad:
  art: |
    This is the forge. The body, once fragile, is now tested in a controlled crucible. It is the training montage where strength is built, not merely rediscovered, transforming the convalescent into an athlete.
  law: |
    Systematically increase physiologic load (Γ) via structured strength and aerobic exercise, contingent upon stable clinical indicators and positive Kτ response (ΔKτ > 0). Progression halts or reverses if safety flags (e.g., ECG changes, symptomatic hypotension) are triggered.
  philosophy: |
    To move beyond recovery to the deliberate construction of a larger buffer of functional reserve (Kτ). This phase establishes the physical capacity required for a Coherent Life, creating physiological and psychological confidence through measurable achievement.
pirouette_definition: |
  The active, supervised training phase focused on structured progression of strength and aerobic exercise. Typically commencing 6 weeks post-event and lasting 3-6 months, this phase uses carefully titrated temporal pressure (Γ) to maximize gains in coherence (Kτ). It is the Pirouette analogue to the main period of outpatient cardiac rehabilitation, emphasizing measurable progress within strict safety protocols (e.g., ECG, hemodynamic monitoring).
operational_definition:
  units: The phase is a period of time (weeks/months); interventions are measured in frequency (sessions/week), duration (min), and intensity (RPE, METs, watts, %HRmax).
  symbol_table:
    - name: Γ_target
      meaning: Target physiologic load for a given session.
      dimensions: Contextual (RPE, METs, watts)
      default_range: RPE 4-6/10; 60-80% HRmax (context-dependent)
    - name: ΔΓ/Δt
      meaning: Rate of load progression across sessions.
      dimensions: Load / Time
      default_range: ~10% weekly increase in volume or intensity, contingent on stability.
    - name: F_session
      meaning: Session frequency.
      dimensions: T⁻¹ (sessions/week)
      default_range: 2–5 sessions/week
  measurement:
    procedures:
      - name: Phase III Entry/Exit Assessment
        outline: |
          Entry requires successful completion of Phase II (Slow Spiral) with stable hemodynamics and no contraindications to increased exertion. Exit is determined by achieving functional capacity goals, completing a standard CR course (e.g., 36 sessions), or transitioning to a self-managed maintenance program (Phase IV).
        expected_signals: [Stable or increasing Kτ (e.g., 6MWD, peak VO₂), Tₐ (adherence) > 80%]
        pitfalls: [Premature entry before sufficient sternal/wound healing, stagnation due to fear of progression.]
      - name: Intra-session Load Titration
        outline: |
          During each session, monitor RPE, HR, and BP response to the prescribed exercise protocol. Increase intensity or duration according to the pre-defined progression plan only if all parameters are stable and within target zones. Terminate or reduce load if safety flags (e.g., chest pain, arrhythmia, dizziness) appear.
        expected_signals: [HR within target zone, RPE matching target, stable BP.]
        pitfalls: [Over-reliance on HR alone (e.g., in patients on beta-blockers), ignoring patient-reported symptoms.]
context_windows:
  - module: DOMA-HLTH-006
    excerpt: |
      | Clinical Phase            | Pirouette Phase            | Typical Duration              | Core Activities                           | Key Safety Checks / Clinical Flags                          |
      | ------------------------- | -------------------------- | ----------------------------- | ----------------------------------------- | ----------------------------------------------------------- |
      | Active training period    | Phase III: Build the Arena | Weeks 6–12 (or up to ~4–6 mo) | Structured strength + aerobic progression | ECG monitoring, gradual load increments, lab monitoring     |
  - module: DOMA-HLTH-006
    excerpt: |
      Phase II/III of Pirouette should accommodate this cadence [2–3 sessions/week for 12–18 weeks] as baseline; more advanced segments can shift to home / mixed modalities.
poetic_connections:
  motifs: [crucible, forge, training, scaffolding, measured stress, athlete]
  evocative_lines:
    - "The 'Crucible Metric' — a conceptual performance indicator."
    - "Build the Arena"
  association_matrix:
    - [ "Temporal Pressure (Γ)", 0.9 ]
    - [ "Coherence (Kτ)", 0.8 ]
    - [ "Phase II: Slow Spiral", 0.7 ]
    - [ "Phase IV: Coherent Life", 0.7 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Supervised Outpatient Cardiac Rehabilitation (AHA/ACC Phase II/III)
      rationale: "This mapping is adopted due to the near-identical operational structure, goals, duration, core activities (monitored aerobic and strength training), and patient population as defined in established clinical guidelines for cardiac rehabilitation."
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "For a deconditioned individual post-cardiac event, the structured, supervised progression of Phase III yields a greater rate of Kτ gain (ΔKτ/Δt) than the self-directed activity typical of Phase IV."
      domain: phenomenology
      falsifier: "A randomized trial showing that patients transitioning directly to self-managed activity (Phase IV) after Phase II achieve similar or better functional capacity (e.g., peak VO₂) at 6 months compared to those completing a formal Phase III."
      status: supported
      links: [DOMA-HLTH-006]
naming_notes:
  collisions: ["Some clinical models refer to the supervised outpatient phase as 'Phase II'. Pirouette's model uses Phase II for the *initial*, low-intensity outpatient transition, reserving Phase III for the main, intensive training block."]
  disambiguation: |
    'The Arena' refers to the dedicated, supervised environment (the clinic, the gym) where the primary work of building capacity occurs. This contrasts with the 'Spiral' (Phase II), which is about re-engaging with the world, and 'Coherent Life' (Phase IV), which integrates new capacity into daily existence.
crosslinks:
  near_synonyms: []
  antonyms: [PHASE_I_RE_TUNE]
  prerequisites: [PHASE_II_SLOW_SPIRAL]
  downstream_effects: [PHASE_IV_COHERENT_LIFE]
license: CC-BY-SA-4.0