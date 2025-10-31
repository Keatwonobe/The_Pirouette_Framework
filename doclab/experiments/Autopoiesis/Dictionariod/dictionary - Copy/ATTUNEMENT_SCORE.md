---
term: "Attunement Score"
canonical_id: "ATTUNEMENT_SCORE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-115"]
---

---
term: Attunement Score
canonical_id: ATTUNEMENT_SCORE
symbol: Aₛ
aliases: [Gardener's Compass Ranking]
parents: [DOMA-115]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-115
      lines: "L93-L95"
      snippet: |
        The final step synthesizes the previous conditions into a single `Attunement Score`. This score is a function of compatibility, potential, and the urgency of the context.
        `Attunement Score = f(Harmonic Match, Coherence Gap, Contextual Pressure)`
  editors: [autonomously-generated]
  review_log: []
triad:
  art: |
    A measure of fertile ground. The score reveals not just who can hear the offered song, but whose soul is ready to turn that note into a symphony.
  law: |
    The efficacy of a Coherence Offering is maximized by directing it to the system with the highest Attunement Score, producing the greatest positive feedback loop of systemic health (ΔKτ) per unit of intervention.
  philosophy: |
    This metric transforms altruism from an act of charity into a strategic act of co-creation. It prioritizes resonant reinforcement over random kindness, ensuring that generative acts cultivate systemic flourishing rather than being wasted on infertile ground.
pirouette_definition: |
  A synthesized, predictive metric that ranks potential recipients of a Coherence Offering. The score is a function combining three factors: the phase alignment between the offering and recipient (Harmonic Match), the recipient's potential for positive transformation (Coherence Gap), and the urgency imposed by the environment (Contextual Pressure). It is the core calculation used to generate the Gardener's Compass.
operational_definition:
  units: Dimensionless (normalized value, often in [0, 1])
  symbol_table:
    - name: Aₛ
      meaning: Attunement Score
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: Hₘ
      meaning: Harmonic Match
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: ΔK_g
      meaning: Coherence Gap
      dimensions: coherence
      default_range: contextual
    - name: Γ
      meaning: Contextual Pressure
      dimensions: T⁻¹ or M L⁻¹ T⁻²
      default_range: contextual
  measurement:
    procedures:
      - name: The Gardener's Compass Protocol
        outline: |
          1.  **Harmonic Filtering:** Identify a pool of potential recipients whose internal state (Ki pattern) is phase-aligned with the Coherence Offering's signature. This yields the Harmonic Match (Hₘ).
          2.  **Coherence Gap Assessment:** Use the `Caduceus Lens` (DYNA-003) to measure the temporal coherence (Kτ) of each filtered candidate. Identify those in the "fertile ground"—neither too rigid (high Kτ) nor too chaotic (low Kτ)—to quantify the Coherence Gap (ΔK_g).
          3.  **Synthesis:** Combine Hₘ, ΔK_g, and ambient Contextual Pressure (Γ) into the final Attunement Score (Aₛ). The precise function `f(Hₘ, ΔK_g, Γ)` is context-dependent but typically weights all three components.
        expected_signals: [phase-alignment metrics, Kτ time series, Γ sensor data]
        pitfalls: [Mistaking harmonic overtones for a fundamental match; targeting systems too stable ("crystal") or too unstable ("storm") to integrate the offering; ignoring ambient pressure Γ.]
context_windows:
  - module: DOMA-115
    excerpt: |
      The final step synthesizes the previous conditions into a single `Attunement Score`. This score is a function of compatibility, potential, and the urgency of the context. `Attunement Score = f(Harmonic Match, Coherence Gap, Contextual Pressure)` This score prioritizes recipients where the offering will answer a question the universe is already asking, resolving a state of creative tension or external pressure (Γ). Ranking candidates by this score produces the Gardener's Compass...
  - module: DOMA-115
    excerpt: |
      The Gardener's Compass is a predictive tool designed to solve for the recipient `i` where a given gift `δ𝓛` will produce the maximum increase in their action: `max_i [ ∫(𝓛_p,i + δ𝓛) dt ]`. By helping a resonant neighbor move from a turbulent to a laminar state, you reduce the chaos that bombards your own boundaries, sculpting a shared reality with lower ambient temporal pressure (`Γ`).
poetic_connections:
  motifs: [gardening, fertile ground, resonance, strategic kindness, cultivation]
  evocative_lines:
    - "A wellspring that pours itself onto stone is noble, but futile."
    - "To know, with precision, where the next seed of coherence will not only grow, but bloom into a forest."
  association_matrix:
    - [ "COHERENCE_GAP", 0.9 ]
    - [ "HARMONIC_MATCH", 0.9 ]
    - [ "RESONANT_REINFORCEMENT", 0.8 ]
    - [ "CONTEXTUAL_PRESSURE", 0.7 ]
    - [ "ALCHEMICAL_UNION", 0.5 ]
formal_mappings:
  candidates:
    - target: Fitness Function
      domain: Math
      mapping_kind: conceptual
      equation_hint: |
        Aₛ(recipientᵢ) ⇔ Fitness(solutionᵢ)
      justification: |
        Like a fitness function in an evolutionary algorithm, the Attunement Score provides a quantitative measure of a candidate's (recipient's) quality relative to a specific objective (maximizing the impact of a Coherence Offering). It is used to select the "fittest" candidate for an intervention.
      references: []
      confidence: 0.8
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "Interventions directed toward recipients with the highest Attunement Scores produce a statistically greater increase in systemic coherence (ΔKτ) than interventions guided by any single sub-component (e.g., need or compatibility alone)."
      domain: phenomenology
      falsifier: "A controlled study demonstrates that a simpler metric, such as prioritizing the recipient with the largest Coherence Gap or highest Harmonic Match alone, consistently yields better outcomes than the composite Attunement Score."
      status: proposed
      links: [DOMA-115]
naming_notes:
  collisions: [Attunement (psychology, spirituality)]
  disambiguation: |
    Unlike the general psychological concept of "attunement" which describes a subjective state of rapport, the Pirouette Attunement Score is a calculated, predictive metric. It is a quantitative synthesis of resonance, potential, and pressure, not merely a qualitative feeling of connection.
crosslinks:
  near_synonyms: [FIGURE_OF_MERIT]
  antonyms: [RANDOM_ALLOCATION]
  prerequisites: [HARMONIC_MATCH, COHERENCE_GAP, CONTEXTUAL_PRESSURE]
  downstream_effects: [RESONANT_REINFORCEMENT, ALCHEMICAL_UNION]
license: CC-BY-SA-4.0
---