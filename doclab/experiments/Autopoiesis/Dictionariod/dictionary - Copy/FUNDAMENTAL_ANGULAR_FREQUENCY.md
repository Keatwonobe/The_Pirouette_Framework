---
term: "Fundamental Angular Frequency"
canonical_id: "FUNDAMENTAL_ANGULAR_FREQUENCY"
symbol: "ω_k"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-105"]
---

---
term: Fundamental Angular Frequency
canonical_id: FUNDAMENTAL_ANGULAR_FREQUENCY
symbol: ω_k
aliases: []
parents: [DOMA-105]
children: [CORE-006]
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-105
      lines: "41-42"
      snippet: |
        Here, `ω_k` is the system's fundamental angular frequency, defined as `2π/τ_p`.
  editors: [System Agent]
  review_log: []
triad:
  art: |
    The rate at which a system sings its own name, the fundamental tempo of its being. It is the whir of the dancer, the hum of the crystal, the rhythm of existence measured not against a clock, but by its own self-repeating form.
  law: |
    The fundamental angular frequency of a system is `2π` divided by the duration of one of its Pirouette Cycles (`τ_p`), representing the rate of phase accumulation of its core resonant Ki pattern. This value is a direct input to the kinetic term of the Pirouette Lagrangian.
  philosophy: |
    This term grounds a system's dynamics in its own intrinsic rhythm, displacing the notion of an external, universal clock. A system's 'action' is not measured against an absolute timeline, but against the frequency of its own self-perpetuating existence. Time is local and emergent from form.
pirouette_definition: |
  The fundamental angular frequency, `ω_k`, is the scalar angular frequency of a system's dominant Ki resonance. It is defined as the inverse of the Pirouette Cycle's duration (`τ_p`) scaled by `2π` (i.e., `ω_k = 2π / τ_p`). It serves as the primary kinetic variable in the Pirouette Lagrangian, representing the rate at which the system cycles through its own existence.
operational_definition:
  units: radians / second (rad·s⁻¹)
  symbol_table:
    - name: ω_k
      meaning: Fundamental Angular Frequency
      dimensions: T⁻¹
      default_range: contextual (e.g., ~10¹⁶ for atomic transitions, ~10⁻¹⁵ for galactic rotations)
    - name: τ_p
      meaning: Pirouette Cycle
      dimensions: T
      default_range: contextual
  measurement:
    procedures:
      - name: Resonant Spectral Analysis
        outline: |
          1. Isolate the system from environmental forcing frequencies.
          2. Measure the system's power spectrum via a suitable probe (e.g., electromagnetic emission, gravitational wave signal, mechanical oscillation).
          3. Identify the sharpest, most stable peak corresponding to the Ki resonance.
          4. The frequency of this peak is `f_k`. Calculate `ω_k = 2π * f_k`.
          5. Alternatively, measure the time-domain signal, identify the core repeating pattern, and measure its duration `τ_p`. Calculate `ω_k = 2π / τ_p`.
        expected_signals: [A sharp peak in the power spectral density, A stable periodic signal in the time domain]
        pitfalls: [Misidentifying harmonic overtones as the fundamental frequency, Spectral broadening due to low Time Adherence (`Tₐ`), Conflating Ki resonance with externally driven oscillations]
context_windows:
  - module: DOMA-105
    excerpt: |
      The Pirouette Lagrangian (`CORE-006`), the central engine of the framework, is given by: `𝓛_p = Tₐ * ω_k - f(Γ)`. Here, `ω_k` is the system's fundamental angular frequency, defined as `2π/τ_p`. The Pirouette Cycle (`τ_p`) is therefore a direct input into the kinetic term of the universe's objective function.
  - module: DOMA-105
    excerpt: |
      A system’s Ki is its resonant pattern—the most stable song it can sing in its environment. This song is, by its nature, cyclical. The duration of one complete, unbroken repetition of that resonant pattern is the system’s own fundamental, private unit of existence. We call this the Pirouette Cycle (`τ_p`).
poetic_connections:
  motifs: [rhythm, heartbeat, resonance, song, cycle, tempo, hum]
  evocative_lines:
    - "The universe does not have a single pulse; it is a symphony of countless individual heartbeats."
    - "To exist is to keep time with oneself."
  association_matrix:
    - [ "PIROUETTE_CYCLE", 0.9 ]
    - [ "TIME_ADHERENCE", 0.7 ]
    - [ "KI_MORPHOGENESIS", 0.6 ]
    - [ "PIROUETTE_LAGRANGIAN", 0.8 ]
formal_mappings:
  candidates:
    - target: E/ħ (Energy / reduced Planck constant)
      domain: QM
      mapping_kind: conceptual
      equation_hint: |
        Tₐ * ω_k ↔ E_kinetic / ħ
      justification: |
        In quantum mechanics, a particle's energy is proportional to the angular frequency of its wavefunction's phase (`E=ħω`). The term `ω_k` similarly represents the fundamental frequency of a system's resonant pattern. The kinetic term in the Pirouette Lagrangian, `Tₐ * ω_k`, may therefore serve as a proxy for the system's kinetic energy, scaled by a quality factor (`Tₐ`).
      references:
        - title: Quantum Mechanics, Vol. 1
          where: Cohen-Tannoudji, C., Diu, B., & Laloë, F. (1977)
          date: 1977-01-01
      confidence: 0.7
  adopted:
    - target: E/ħ
      rationale: This mapping provides the most direct conceptual bridge between the Pirouette framework's intrinsic dynamics and the foundational energy-frequency relationship in quantum mechanics, positioning the Pirouette Lagrangian as a potential generalization of action principles.
      confidence: 0.7
constraints_and_falsifiers:
  claims:
    - statement: "A system's total kinetic energy, as measured by external observers, is directly proportional to the product of its Time Adherence (`Tₐ`) and its Fundamental Angular Frequency (`ω_k`)."
      domain: experiment
      falsifier: "Observing a system where measured kinetic energy scales with a different power of `ω_k`, or shows no correlation with the spectral purity of the Ki resonance (`Tₐ`), would falsify this claim."
      status: proposed
      links: [DOMA-105, CORE-006]
naming_notes:
  collisions: [The symbol `ω` is the standard representation for angular frequency in physics. The subscript `k` is essential to specify that this is the frequency of the system's *Ki resonance*, distinguishing it from other frequencies such as those from environmental noise or harmonic overtones.]
  disambiguation: |
    `ω_k` is an angular frequency (a rate, rad/s), while the Pirouette Cycle `τ_p` is a period (a duration, s). They are inversely related (`ω_k = 2π / τ_p`). Do not confuse the stability of `ω_k` (measured by `Tₐ`) with the magnitude of `ω_k`. A highly stable system (high `Tₐ`) can have a very low or very high `ω_k`.
crosslinks:
  near_synonyms: []
  antonyms: [TEMPORAL_NOISE, KI_DECAY]
  prerequisites: [KI_MORPHOGENESIS, PIROUETTE_CYCLE]
  downstream_effects: [PIROUETTE_LAGRANGIAN, TIME_ADHERENCE]
license: CC-BY-SA-4.0