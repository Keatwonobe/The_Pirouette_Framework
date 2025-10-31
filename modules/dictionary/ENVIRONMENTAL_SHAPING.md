---
term: "Environmental Shaping"
canonical_id: "ENVIRONMENTAL_SHAPING"
symbol: ""
aliases: [Context Shaping]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DYNA-005_coherent_adherence_protocol"]
---

---
term: Environmental Shaping
canonical_id: ENVIRONMENTAL_SHAPING
symbol: \(\mathcal A\)
aliases: [Context Shaping]
parents: [DYNA-005]
children: [PPS-015, DOMA-QCOMP-001, DOMA-203]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DYNA-005_coherent_adherence_protocol
      lines: "L28-L32"
      snippet: |
        §2 · What CAP v2 *does* (and what it refuses to do)
        - **Does:** shape *contexts* (measurement geometry, rhythms, interfaces, incentives) to elevate Ta where *participants have agreed*, aiming for better sensing, learning, or collaboration.
        - **Refuses:** hidden persuasion; coercive asymmetries; unlogged back-channels...
  editors: [system_author]
  review_log: []
triad:
  art: |
    The conductor who brings water, prints the score, and dims the harsh lights, allowing the choir to tune itself. It is the practice of changing the room, not the throat.
  law: |
    Any action \(\mathcal A\) that modifies system pathway rates \(k_j\) by altering the kinetic term \(K_\tau\) or observer cost \(V_{\text{obs}}\) constitutes Environmental Shaping. Such actions are permissible only under explicit consent, full transparency of their intended effect, and within a publicly declared budget for negative externalities (\(\mathcal D\)).
  philosophy: |
    To influence a system toward greater coherence with integrity, one must respect its autonomy. Shaping modifies the conditions for choice rather than the chooser, creating fertile ground for desired behavior to emerge consensually, not through force or deception. It is the primary instrument of consentful alignment.
pirouette_definition: |
  Environmental Shaping is the set of auditable actions \(\mathcal A\) (e.g., modifying measurement geometry, interfaces, or incentives) that influence a system's adherence \(T_a\) by altering its context. These actions operate by modifying the kinetic term \(K_\tau\) or observer cost \(V_{\text{obs}}\) in the Pirouette Lagrangian, thereby changing the rates of possible pathways. Under the Coherent Adherence Protocol (CAP v2), all such actions are subject to strict constraints of consent, transparency, and a budgeted cap on negative externalities (Dark Residue \(\mathcal D\)).
operational_definition:
  units: The action \(\mathcal A\) is a dimensionless set; its effects are measured in units of energy (for \(K_\tau, V_{\text{obs}}\)) or inverse time (for rates \(k_j\)).
  symbol_table:
    - name: \(\mathcal A\)
      meaning: The set of allowed environmental shaping actions.
      dimensions: dimensionless
      default_range: contextual
    - name: \(\Delta K_\tau\)
      meaning: Change in usable coherence kinetic term induced by the action.
      dimensions: M L² T⁻² (energy)
      default_range: contextual
    - name: \(\Delta V_{\text{obs}}\)
      meaning: Change in observer cost (probe/back-action) induced by the action.
      dimensions: M L² T⁻² (energy)
      default_range: contextual
  measurement:
    procedures:
      - name: Counterfactual A/B Test for Coherence Gain
        outline: |
          1. Establish a baseline system and measure its adherence, \(T_a^0\).
          2. Create two cohorts, A (control) and B (test), ensuring the observer cost \(V_{\text{obs}}\) is identical for both.
          3. Apply the shaping action \(\mathcal A\) to the context of cohort B only.
          4. Measure adherence \(T_a^A\) and \(T_a^B\) over a preregistered interval. The effect is the difference \(\Delta T_a = T_a^B - T_a^A\).
        expected_signals: [Statistically significant \(\Delta T_a > 0\), measurable change in pathway rates \(k_j\), user-reported comprehension of the intervention.]
        pitfalls: [Failing to hold \(V_{\text{obs}}\) constant across cohorts (mistaking pressure for coherence), uncontrolled environmental confounders, observer effects.]
context_windows:
  - module: DYNA-005_coherent_adherence_protocol
    excerpt: |
      **Does:** shape *contexts* (measurement geometry, rhythms, interfaces, incentives) to elevate Ta where *participants have agreed*, aiming for better sensing, learning, or collaboration.
      **Refuses:** hidden persuasion; coercive asymmetries; unlogged back-channels; any influence that raises \(V_{\text{obs}}\) on people without consent (Shadow overreach).
  - module: DYNA-005_coherent_adherence_protocol
    excerpt: |
      The new conductor brought water, printed the score, dimmed the harsh lights, and *asked* for one note at a time.
      The room tuned itself. The song was almost as perfect—and everyone stayed to sing an encore.
      **CAP v2** is the second conductor: it changes the *room*, not the throat.
poetic_connections:
  motifs: [gardening, architecture, tuning, catalysis, nudging]
  evocative_lines:
    - "it changes the *room*, not the throat."
    - "The room tuned itself."
  association_matrix:
    - [ "COHERENT_ADHERENCE", 0.9 ]
    - [ "SHADOW_GAUGE", 0.8 ]
    - [ "DARK_RESIDUE", 0.7 ]
    - [ "INERTIAL_LEAP", 0.5 ]
formal_mappings:
  candidates:
    - target: Choice Architecture
      domain: Behavioral Economics
      mapping_kind: conceptual
      equation_hint: |
        \(k_j = k_j^0 \exp(\Delta U_j)\), where \(\Delta U_j\) is a change in the potential barrier, analogous to making a choice easier/harder.
      justification: |
        Environmental Shaping is a formalization of "choice architecture." Both concepts focus on altering the context in which decisions are made to encourage certain outcomes without forbidding alternatives. CAP v2 extends this by adding rigorous physical and ethical constraints (\(V_{\text{obs}}\), \(\mathcal D\), consent, symmetry) not always formalized in classical choice architecture.
      references:
        - title: "Nudge: Improving Decisions About Health, Wealth, and Happiness"
          where: "Yale University Press"
          date: 2008-04-08
      confidence: 0.8
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: 'Well-designed shaping actions (\(\mathcal A\)) can increase system adherence (\(T_a\)) without increasing observer cost (\(V_{\text{obs}}\)) or generating prohibited levels of Dark Residue (\(\mathcal D\)).'

      domain: experiment
      falsifier: 'In a controlled trial (e.g., T4 Coherence-not-force test), all tested shaping actions that produce a positive \(\Delta T_a\) also produce a statistically significant increase in \(V_{\text{obs}}\) or breach the Dark Residue budget.'

      status: proposed
      links: [DYNA-005]
naming_notes:
  collisions: [Reward shaping (Reinforcement Learning)]
  disambiguation: |
    Distinct from *reward shaping* in reinforcement learning, which modifies an agent's reward function to guide learning. Environmental Shaping modifies the agent's *context, action space, or information landscape* (e.g., UI, communication channels, measurement basis) rather than its internal utility calculation. It influences the *kinetics* of choice, not the perceived *value* of the outcome.
crosslinks:
  near_synonyms: [CONTEXT_SHAPING]
  antonyms: [DIRECT_MANIPULATION, COERCIVE_CONTROL]
  prerequisites: [COHERENT_ADHERENCE, SHADOW_GAUGE, PIROUETTE_LAGRANGIAN]
  downstream_effects: [DARK_RESIDUE, INERTIAL_LEAP]
license: CC-BY-SA-4.0
---