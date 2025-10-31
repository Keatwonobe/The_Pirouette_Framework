---
term: "Coherence Risk"
canonical_id: "COHERENCE_RISK"
symbol: "R_κ"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-019"]
---

---
term: Coherence Risk
canonical_id: COHERENCE_RISK
symbol: R_κ
aliases: []
parents: [DOMA-019]
children: [INST-GOV-001_placeholder]
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-019
      lines: "L12-L14"
      snippet: |
        It establishes Coherence Risk (R_κ) as the primary predictive metric, derived
        from the Pirouette Lagrangian, to guide Weavers toward actions that generate,
        rather than degrade, systemic harmony.
  editors: [autonomously_generated]
  review_log: []
triad:
  art: |
    The tuning fork that attunes the Weaver's ear to the echo an action will compose. It is the tool that measures a choice not by its force, but by the quality of the silence or the song it leaves behind.
  law: |
    An action is subjected to oversight proportional to its calculated Coherence Risk; R_κ > 0.75 mandates an immediate Coherence Quarantine and invocation of the Crucible Protocol for creative re-synthesis.
  philosophy: |
    Coherence Risk reframes ethics from reactive boundary-setting ("do no harm") to a proactive, navigational art ("cultivate systemic health"). It asserts that an action's morality is a measurable geometric property of the scar it carves into the universe's memory.
pirouette_definition: |
  A predictive, dimensionless metric on a 0–1 scale quantifying an action's potential to degrade the systemic health and harmony of the systems it affects. It is calculated as a weighted function of an action's Reach (ρ), Dissonance (δ), and Wound Channel Depth (ω), serving as the primary navigational guide for Coherence Stewardship. A high R_κ indicates that an action is likely to be destructive or parasitic (Δ𝓛_sys < 0).
operational_definition:
  units: dimensionless (normalized 0 to 1)
  symbol_table:
    - name: R_κ
      meaning: Coherence Risk
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: ρ
      meaning: Reach; measure of systemic propagation
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: δ
      meaning: Dissonance; severity of disruption to a system's core resonant pattern
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: ω
      meaning: Wound Channel Depth; measure of permanence and irreversibility
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: w_i
      meaning: Calibrated weights for ρ, δ, ω
      dimensions: dimensionless
      default_range: "context-dependent, sum to 1"
  measurement:
    procedures:
      - name: Coherence Risk Assessment
        outline: |
          1.  Define the proposed action and its target system(s).
          2.  Model the target systems' coherence manifolds and core resonant patterns (Ki).
          3.  Perform adversarial simulations to map the action's Geometry of Consequence.
          4.  Derive normalized scores for Reach (ρ), Dissonance (δ), and Wound Channel Depth (ω) from simulation outputs.
          5.  Calculate R_κ using the weighted equation: R_κ = w_ρ ρ + w_δ δ + w_ω ω.
        expected_signals: [ρ score, δ score, ω score, final R_κ value]
        pitfalls: [Underestimating systemic interconnectedness (inaccurate ρ), mischaracterizing a system's core identity (inaccurate δ), failing to model long-term memory effects (inaccurate ω)]
context_windows:
  - module: DOMA-019
    excerpt: |
      The Weaver's Compass replaces the static fence with a dynamic, navigational instrument. It reframes ethical consideration from a reactive check on "consequence" to a proactive assessment of the **Geometry of Consequence**. It provides a universal protocol for measuring **Coherence Risk (R_κ)**—the potential of any action to degrade the health and harmony of the systems it touches.
  - module: DOMA-019
    excerpt: |
      Based on the calculated R_κ, a project's path is guided by a clear, tiered protocol.
      -   **Laminar Path (R_κ ≤ 0.5):** The action is predicted to integrate smoothly...
      -   **Turbulent Watch (0.5 < R_κ ≤ 0.75):** The action carries a significant risk of creating local turbulence...
      -   **Coherence Quarantine (R_κ > 0.75):** The action is predicted to cause severe, widespread dissonance... This invokes **The Crucible Protocol**.
poetic_connections:
  motifs: [geometry_of_consequence, wound_channel, the_universal_song, the_weavers_compass]
  evocative_lines:
    - "Some bells cannot be un-rung."
    - "A Weaver does not ask, 'Am I allowed to build this?' They ask, 'What world am I building?'"
    - "The echoes we compose will be a blessing for all who follow in our wake."
  association_matrix:
    - [ "WOUND_CHANNEL", 0.9 ]
    - [ "PIROUETTE_LAGRANGIAN", 0.8 ]
    - [ "COHERENCE_STEWARDSHIP", 0.9 ]
    - [ "THE_CRUCIBLE", 0.7 ]
formal_mappings:
  candidates:
    - target: Entropy production rate (σ)
      domain: CM
      mapping_kind: conceptual
      equation_hint: |
        R_κ ∝ E[σ_action]
      justification: |
        Coherence Risk is a predictive measure of an action's tendency to introduce disorder, turbulence, and dissonance into an ordered system. This is conceptually analogous to the expected entropy production rate in non-equilibrium thermodynamics, where a high rate signifies a process that rapidly drives a system toward a state of higher disorder and dissipates useful energy. High-risk actions are those that cause irreversible, dissipative scarring.
      references:
        - title: "Non-Equilibrium Thermodynamics"
          where: "Chapter 3: Entropy Production"
          date: 2008-01-01
      confidence: 0.6
    - target: Cost Function / Negative Reward
      domain: Math
      mapping_kind: operational
      equation_hint: |
        R_κ(a) = -E[R(s,a)]
      justification: |
        In reinforcement learning and optimal control, agents are trained to minimize a cost function or maximize a reward. Coherence Risk functions as a pre-calculated cost function for a given action, guiding the "Weaver" agent to select policies (sequences of actions) that avoid high-cost, system-degrading trajectories.
      references:
        - title: "Reinforcement Learning: An Introduction"
          where: "Chapter 3: Finite Markov Decision Processes"
          date: 2018-01-01
      confidence: 0.7
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The Coherence Risk metric R_κ is a reliable predictor of long-term, negative changes in a system's integrated Pirouette Lagrangian (Δ∫𝓛_p dt < 0)."
      domain: phenomenology
      falsifier: "A statistically significant number of actions with low calculated R_κ (e.g., < 0.5) are observed to cause severe, lasting systemic dissonance, OR actions with high R_κ (> 0.75) consistently lead to a net increase in systemic coherence."
      status: proposed
      links: [DOMA-019]
naming_notes:
  collisions: [The symbol R is common for Resistance (electrical), Radius (geometry), and Reward (RL). The subscript κ (kappa, for "coherence") is essential for disambiguation.]
  disambiguation: |
    Coherence Risk is a *predictive* metric that assesses a potential *action*, not a current *state*. It should not be confused with a system's instantaneous Coherence Score or its realized Decoherence. R_κ measures the danger of the chisel, not the ugliness of the scar already made.
crosslinks:
  near_synonyms: []
  antonyms: [COHERENCE_GAIN_placeholder]
  prerequisites: [WOUND_CHANNEL, COHERENCE, PIROUETTE_LAGRANGIAN]
  downstream_effects: [THE_CRUCIBLE, COHERENCE_QUARANTINE]
license: CC-BY-SA-4.0
---