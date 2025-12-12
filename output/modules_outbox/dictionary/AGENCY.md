---
term: "Agency"
canonical_id: "AGENCY"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-067"]
---

---
term: Agency
canonical_id: AGENCY
symbol: 
aliases: [Choice, Will-Freedom Duality]
parents: [CORE-006, CORE-011, DYNA-001]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-067
      lines: "L23-L25"
      snippet: |
        The dynamic balance between these two strategies is the essence of all adaptive and intelligent agency, from the quantum to the psychological.
  editors: [SystemAgent]
  review_log: []
triad:
  art: |
    An agent is a navigator, carving a riverbed for its being while having the wisdom to become rain and seek higher ground. The dance is knowing when to be the chisel that deepens the channel, and when to be the cloud that leaves it.
  law: |
    Agency is the measured ratio of exploratory to exploitative actions a system takes over a given epoch. Optimal agency maximizes long-term coherence by dynamically adjusting this ratio, avoiding the failure modes of stagnation (pure exploitation) and drift (pure exploration).
  philosophy: |
    Agency redefines existence as an active optimization problem, shifting the focus from static being to the dynamic process of becoming. It posits that health, intelligence, and evolution are not states, but the skillful, continuous balancing of reinforcing what works (Will) and discovering what could work better (Freedom).
pirouette_definition: |
  The capacity of a system to navigate the coherence manifold. Agency is defined by the dynamic balance (Dynamic Equipoise) between two complementary strategies: **Will** (exploitation of known, high-coherence paths by deepening a Wound Channel) and **Freedom** (exploration for new, potentially more optimal paths by smoothing the manifold). The health of a system's agency is determined by its ability to avoid the pathological extremes of Stagnation (excess Will) and Drift (excess Freedom).
operational_definition:
  units: Dimensionless (expressed as a state on the Exploitation-Exploration spectrum)
  symbol_table:
    - name: W
      meaning: Will; the strategy of exploitation or reinforcement.
      dimensions: dimensionless
      default_range: contextual
    - name: F
      meaning: Freedom; the strategy of exploration.
      dimensions: dimensionless
      default_range: contextual
    - name: K_τ
      meaning: Temporal Coherence; maximized by Will.
      dimensions: Action
      default_range: contextual
    - name: V_Γ
      meaning: Temporal Pressure; sensitivity to this is increased by Freedom.
      dimensions: Action
      default_range: contextual
  measurement:
    procedures:
      - name: Agency Spectrum Analysis
        outline: |
          Observe a system's behavior over a significant time window, tracking its primary Ki pattern. Quantify the temporal variance of this pattern. A low-variance, stable pattern indicates exploitation (Will). A high-variance, unstable pattern indicates exploration (Freedom). The system's agency profile is the distribution of time spent in each mode.
        expected_signals: [Stable, repeating Ki patterns (Stagnation), High-variance, non-converging Ki patterns (Drift), Oscillating periods of pattern stability and pattern variance (Dynamic Equipoise)]
        pitfalls: [Observation period is too short to capture the full cycle, Mistaking random noise for intentional exploration, Conflating mastery with stagnation.]
context_windows:
  # Short, trimmed context quotes harvested from modules (3–6 sentences each).
  - module: DOMA-067
    excerpt: |
      Will is the strategy of exploitation or reinforcement. It is the act of deepening a known path of high coherence, reinforcing a stable identity by strengthening its Wound Channel. It is a powerful, conservative strategy that risks stagnation—getting trapped in a perfected pattern that is no longer optimal for a changing world.
  - module: DOMA-067
    excerpt: |
      Freedom is the strategy of exploration. It is the act of seeking new, potentially more coherent paths by smoothing the manifold and resisting the pull of an established channel. It is a creative, innovative strategy that risks drift—dissolving into chaos without ever finding a new, stable form.
  - module: DOMA-067
    excerpt: |
      A Weaver’s task is to diagnose imbalance and facilitate a return to the agile path of dynamic equipoise. Look for systems that are highly efficient but have ceased to learn (Stagnation). Look for systems characterized by constant motion but no progress (Drift).
poetic_connections:
  # Lightweight "word-association graph" and sticky lines.
  motifs: [navigation, dance, river, canyon, desert, chisel, cloud]
  evocative_lines:
    - "Will without Freedom carves a canyon so deep it becomes a grave."
    - "Freedom without Will wanders a desert so vast it dies of thirst."
  association_matrix:
    # symmetric or directed; weights in [0,1]
    - [ "WOUND_CHANNEL", 0.8 ]
    - [ "DYNAMIC_EQUIPOISE", 0.7 ]
    - [ "STAGNATION", -0.9 ]
    - [ "DRIFT", -0.9 ]
formal_mappings:
  # Candidate alignments to EFT/SM/CM/GR terms, each with justification and refs.
  candidates:
    []
  adopted:
    - target: Exploration-Exploitation Trade-off
      domain: Math (Reinforcement Learning)
      mapping_kind: conceptual
      equation_hint: |
        In an ε-greedy policy, a system acts greedily (Will) with probability 1-ε, and explores (Freedom) with probability ε.
      justification: |
        Pirouette's Will/Freedom duality is a direct conceptual mapping of the exploration-exploitation trade-off. Will corresponds to exploiting the current best-known policy to maximize immediate reward (reinforcing `K_τ`). Freedom corresponds to taking exploratory actions to discover potentially better policies and improve the world model (searching the manifold for lower `V_Γ`).
      references:
        - title: Reinforcement Learning: An Introduction
          where: Sutton, R. S. & Barto, A. G.
          date: 2018
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "A system locked in a pure exploitation (Will-dominant) state will exhibit lower long-term coherence than a system in dynamic equipoise when the environment undergoes significant change."
      domain: phenomenology
      falsifier: "Observation of a purely exploitative system consistently outperforming an adaptive system over multiple, significant environmental shifts."
      status: proposed
      links: [DOMA-067, DYNA-001]
naming_notes:
  collisions: [Agency (philosophy), Agency (AI), Agency (sociology)]
  disambiguation: |
    In Pirouette, Agency is not merely the capacity to act, but specifically the *dynamic quality* of that action, defined by the balance of exploration and exploitation. It is a measure of strategic health and adaptiveness, not a synonym for free will, consciousness, or simple action-taking.
crosslinks:
  near_synonyms: [DYNAMIC_EQUIPOISE]
  antonyms: [STAGNATION, DRIFT]
  prerequisites: [COHERENCE_MANIFOLD, WOUND_CHANNEL, LAGRANGIAN_PIROUETTE]
  downstream_effects: [EVOLUTION, LEARNING]
license: CC-BY-SA-4.0
---