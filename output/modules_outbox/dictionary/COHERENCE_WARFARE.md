---
term: "Coherence Warfare"
canonical_id: "COHERENCE_WARFARE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["PDM-003_the_colosseum"]
---

---
term: Coherence Warfare
canonical_id: COHERENCE_WARFARE
symbol: 
aliases: [Information Domain Conflict, Narrative Warfare]
parents: [PDM-003_the_colosseum]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: PDM-003_the_colosseum
      lines: "L106-L109"
      snippet: |
        # Coherence attacks
        if other_power.Ta > power.Ta:
            ta_diff = other_power.Ta - power.Ta
            phase_opp = (1 - np.cos(other_power.Phi - power.Phi)) / 2
            power.ext_Ta_ddot -= 0.1 * ta_diff * phase_opp * other_power.Gamma
  editors: [Environment, Me]
  review_log: []
triad:
  art: |
    To win without fighting by unraveling an adversary's narrative thread until their future collapses. It is the art of making an enemy defeat themselves, dissolving their purpose like salt in water.
  law: |
    The rate of degradation of a target system's Time-Adherence ($T_a$) is proportional to the product of the attacking system's Gladiator Force ($\Gamma$), its coherence advantage ($T_{a,attacker} - T_{a,target}$), and the degree of phase opposition between the two systems. An incoherent system cannot mount an effective coherence attack.
  philosophy: |
    Coherence Warfare recognizes that a system's capacity to act is predicated on its internal stability and shared purpose. By targeting this temporal foundation, one can neutralize a threat without resorting to kinetic violence, shifting the battlefield from physical space to the domain of collective belief and coordination.
pirouette_definition: |
  Coherence Warfare is a mode of adversarial interaction where the primary objective is to degrade a target system's Time-Adherence ($T_a$). It is non-kinetic conflict waged in the information and psycho-social domains. The effectiveness of a coherence attack is a function of the attacking system's Gladiator Force ($\Gamma$), its superior coherence, and the degree of phase opposition ($\phi$) with the target.
operational_definition:
  units: s⁻² (as a second derivative of dimensionless $T_a$)
  symbol_table:
    - name: ext_Ta_ddot
      meaning: The externally-forced rate of change of Time-Adherence acceleration; the direct impact of Coherence Warfare.
      dimensions: T⁻²
      default_range: "[-inf, 0]"
    - name: Γ_attacker
      meaning: The Gladiator Force of the attacking system.
      dimensions: "contextual (e.g., energy/time)"
      default_range: "> 0"
    - name: ta_diff
      meaning: The difference in Time-Adherence between attacker and target ($T_{a,attacker} - T_{a,target}$).
      dimensions: "dimensionless"
      default_range: "> 0 for effective attack"
    - name: phase_opp
      meaning: A measure of goal opposition, derived from the cosine of the phase difference; ranges from 0 (aligned) to 1 (anti-aligned).
      dimensions: "dimensionless"
      default_range: "[0, 1]"
  measurement:
    procedures:
      - name: Inferential Measurement via System Dynamics
        outline: |
          Direct measurement is impossible. Coherence Warfare is inferred by creating a dynamic model of the target system's $T_a$, accounting for all known internal decay factors (e.g., 'Roman Collapse' penalty). The residual, unexplained negative `Ta_ddot` is then correlated with the actions, power ($\Gamma$), coherence ($T_a$), and phase ($\phi$) of a suspected external adversary.
        expected_signals: [Increased social polarization, decline in institutional trust, narrative fragmentation, decision-making paralysis, anomalous drops in economic/logistical efficiency.]
        pitfalls: [Misattributing internal decay to an external attacker, failing to correctly model the attacker's true phase and intentions, over-sensitivity to noise in social metrics.]
context_windows:
  - module: PDM-003_the_colosseum
    excerpt: |
      The initial phase (2025-2040) is marked by intense but non-kinetic Coherence Warfare, where the USA's stability ($T_a$) is systematically degraded. The middle phase (2040-2070) is defined by two simultaneous events: the outbreak of Kinetic War and the catastrophic failure of the Biosphere, which cripples all nations.
  - module: PDM-003_the_colosseum
    excerpt: |
      However, the true "winner" is China. By remaining largely outside the direct conflict and preserving its high internal coherence ($T_a$), it emerges from the chaos as the most powerful and stable actor on the world stage, not because it won a war, but because it *avoided* one.
poetic_connections:
  motifs: [Unraveling, Dissonance, Static, Dissolution, Civil War]
  evocative_lines:
    - "My own mental static becomes very heavy, and on clear nights I can see a little ways..."
    - "It suggests that the path to a better future lies not in winning geopolitical games, but in the radical, collective effort to restore... our own Shared Coherence."
  association_matrix:
    - [ "TIME_ADHERENCE", -0.9 ] # Directly targets and degrades Ta
    - [ "PHASE", 0.7 ] # Effectiveness depends on phase opposition
    - [ "GLADIATOR_FORCE", 0.5 ] # Leverages the attacker's power
    - [ "KINETIC_WAR", 0.6 ] # Often a precursor or trigger for kinetic conflict
formal_mappings:
  candidates:
    - target: Destructive Interference / Antiresonance
      domain: CM
      mapping_kind: mathematical
      equation_hint: |
        ẍ + ω₀²x = F₀ cos(ωt + δ)
      justification: |
        A system's $T_a$ can be modeled as a stable oscillator. Coherence warfare acts as an external driving force (proportional to attacker $\Gamma$) applied with a phase opposition that actively drains energy from the target system, driving its amplitude (stability) towards zero. This is analogous to destructive interference or driving a system at its antiresonance frequency.
      references:
        - title: Vibrations and Waves
          where: A.P. French, Chapter 4
          date: 1971-01-01
      confidence: 0.7
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: 'A system with low internal Time-Adherence ($T_a \le 1.0$) is incapable of mounting a net-positive coherence attack against a more coherent foe.'

      domain: phenomenology
      falsifier: "Observation of a demonstrably incoherent state (e.g., a nation in civil war or with deep political paralysis) successfully and systematically degrading the coherence of a more stable external rival without degrading itself more."
      status: supported
      links: [PDM-003_the_colosseum]
naming_notes:
  collisions: []
  disambiguation: |
    Distinguish from **Kinetic Warfare**, which targets an adversary's Gladiator Force ($\Gamma$) and physical assets.
    Distinguish from **Cyber Warfare**, which typically targets infrastructure and data, components of $\Gamma$.
    Coherence Warfare is unique in that its primary target is the socio-psychological fabric and decision-making capacity that underpins Time-Adherence ($T_a$).
crosslinks:
  near_synonyms: [INFORMATION_WARFARE, PSYCHOLOGICAL_OPERATIONS]
  antonyms: [ADVERSARIAL_COLLABORATION, COHERENCE_BUILDING]
  prerequisites: [TIME_ADHERENCE, GLADIATOR_FORCE, PHASE]
  downstream_effects: [SYSTEM_COLLAPSE, KINETIC_WAR]
license: CC-BY-SA-4.0
---