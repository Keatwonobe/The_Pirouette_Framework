---
term: "Fatigue Rupture"
canonical_id: "FATIGUE_RUPTURE"
symbol: ""
aliases: [Resonant Fatigue]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-131"]
---

---
term: Fatigue Rupture
canonical_id: FATIGUE_RUPTURE
symbol: 
aliases: [Resonant Fatigue]
parents: [DOMA-131, CORE-011, DYNA-001]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-131
      lines: "L109-L117"
      snippet: |
        **Fatigue Rupture (Resonant Fatigue):**
        This pathology results from the slow degradation of a system’s `Wound Channel` (`CORE-011`). The system is subjected to repeated cycles of sub-critical stress. Each cycle is weathered but deepens the wound, eroding the system's baseline coherence. Eventually, a stressor that would have once been trivial provides the final impetus for a complete collapse.
  editors: [Agent: GPT-4]
  review_log: []
triad:
  art: |
    The thousandth cut that fells the tree. The quiet, accumulating debt of stress, paid in a sudden, catastrophic bankruptcy. It is the drip of water that eventually splits the stone.
  law: |
    A system subjected to repeated, sub-critical stress cycles (ΔΓ < Γ_critical) will experience a progressive decrease in baseline temporal coherence (Kτ). This degradation lowers the rupture threshold, leading to failure under a final stressor that would have been survivable by the system in its initial state.
  philosophy: |
    This failure mode reveals that resilience is not merely the ability to withstand a single shock, but the capacity to recover from repeated stresses. It redefines trauma as a cumulative process, where unhealed "small" wounds create the conditions for total collapse, proving that endurance has a finite limit.
pirouette_definition: |
  A rupture mode in which a system's temporal coherence (`Kτ`) is progressively degraded by repeated cycles of sub-critical temporal pressure (`Γ`). Each stress cycle deepens a `Wound Channel`, lowering the system's resilience until a final stressor, which would have been non-critical for the healthy system, triggers a catastrophic coherence cascade.
operational_definition:
  units: Dimensionless (cycle count `N_f`) or system-specific coherence degradation rate (e.g., bits/cycle).
  symbol_table:
    - name: N_f
      meaning: Number of cycles to failure.
      dimensions: dimensionless
      default_range: 10^3 – 10^9
    - name: ΔΓ
      meaning: Amplitude of a sub-critical stress cycle.
      dimensions: contextual (e.g., Pa, bits/s)
      default_range: contextual
    - name: Kτ(n)
      meaning: Temporal coherence after n cycles.
      dimensions: contextual (e.g., bits)
      default_range: contextual
  measurement:
    procedures:
      - name: Cyclic Coherence Degradation Assay
        outline: |
          1. Establish the system's baseline coherence `Kτ(0)` and its single-cycle critical rupture pressure `Γ_crit(0)`.
          2. Subject the system to N repeated cycles of a known sub-critical pressure `ΔΓ < Γ_crit(0)`.
          3. After each block of cycles, measure the new baseline coherence `Kτ(n)`.
          4. The rate of decay of `Kτ(n)` vs. `n` characterizes the system's fatigue life. Rupture is logged when the system fails at cycle `N_f`.
        expected_signals: [Power-law decay of `Kτ` as a function of cycle count `n`., A decreasing critical rupture threshold `Γ_crit(n)` over time.]
        pitfalls: [Failing to allow for inter-cycle recovery, conflating acute strain with permanent degradation., Mis-calibrating `Γ_crit(0)`, causing an unintended brittle or ductile failure.]
context_windows:
  - module: DOMA-131
    excerpt: |
      **Fatigue Rupture (Resonant Fatigue):**
      This pathology results from the slow degradation of a system’s `Wound Channel` (`CORE-011`). The system is subjected to repeated cycles of sub-critical stress. Each cycle is weathered but deepens the wound, eroding the system's baseline coherence. Eventually, a stressor that would have once been trivial provides the final impetus for a complete collapse.
  - module: DOMA-131
    excerpt: |
      The character of a rupture reveals the underlying health of the system that failed... By applying the principles of Flow Dynamics (`DYNA-001`), we can classify all ruptures into three archetypal modes: Brittle Rupture, Ductile Rupture, and Fatigue Rupture...
      *Manifestations:* A bridge collapsing due to metal fatigue, burnout in an individual after years of chronic stress, the fall of an empire weakened by a thousand small crises.
poetic_connections:
  motifs: [erosion, exhaustion, accumulation, debt, unraveling, burnout, fragility]
  evocative_lines:
    - "the fall of an empire weakened by a thousand small crises."
    - "The sound a string makes right before it snaps."
  association_matrix:
    # symmetric or directed; weights in [0,1]
    - [ "WOUND_CHANNEL", 0.9 ]
    - [ "COHERENCE_CASCADE", 0.7 ]
    - [ "TEMPORAL_PRESSURE", 0.6 ]
    - [ "DUCTILE_RUPTURE", 0.3 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Material Fatigue (S-N Curves, Basquin's Relation)
      domain: CM
      mapping_kind: conceptual|mathematical
      equation_hint: |
        ΔΓ = C * (N_f)^b  # Pirouette analogue to Basquin's relation
      justification: |
        The core concept of failure under repeated, sub-critical cyclic loading is a direct mapping. The Pirouette model generalizes this from mechanical stress (σ) to a universal temporal pressure (Γ), where the degradation of coherence (Kτ) is analogous to the accumulation of microcracks in a material. The number of cycles to failure (N_f) is inversely related to the stress amplitude.
      references:
        - title: Shigley's Mechanical Engineering Design
          where: Chapter 6, "Fatigue Failure Resulting from Variable Loading"
          date: 2020-01-01
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "The number of cycles to failure (N_f) for a system under a constant sub-critical stress amplitude (ΔΓ) follows a power-law relationship, ΔΓ ∝ (N_f)^b, where b is a negative constant characteristic of the system's coherence structure."
      domain: phenomenology
      falsifier: "Persistent observation of systems where repeated sub-critical stress either has no cumulative effect (perfect recovery) or consistently strengthens the system (training/annealing) without a fatigue limit across a wide range of stress amplitudes."
      status: supported
      links: [DOMA-131]
naming_notes:
  collisions: [The term "fatigue" is used intentionally to evoke its established meanings in materials science (metal fatigue) and psychology (burnout, compassion fatigue), as these are considered domain-specific manifestations of the same underlying dynamic.]
  disambiguation: |
    Distinguish from **Ductile Rupture**, which is failure under a single, *sustained* stress that exceeds the elastic limit. Fatigue Rupture is caused by *many repeated* stresses, each of which is *below* that limit. It is a failure of endurance and recovery, not a failure of peak strength.
crosslinks:
  near_synonyms: [BURNOUT]
  antonyms: [ANNEALING, ADAPTIVE_HARDENING]
  prerequisites: [SYSTEMIC_RUPTURE, TEMPORAL_PRESSURE, COHERENCE, WOUND_CHANNEL]
  downstream_effects: [COHERENCE_CASCADE, WOUND_BOUNDARY]
license: CC-BY-SA-4.0
---