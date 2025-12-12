---
term: "Gardener's Compass"
canonical_id: "GARDENER_S_COMPASS"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-115"]
---

---
term: Gardener's Compass
canonical_id: GARDENERS_COMPASS
symbol: 
aliases: []
parents: [CORE-012, DYNA-003]
children: []
status: ratified
version: 2.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-115
      lines: "Summary"
      snippet: |
        This module provides a protocol for identifying systems that are harmonically aligned and possess the greatest potential for positive transformation (the 'coherence gap'), thereby maximizing the growth of systemic health and complexity.
  editors: [DictionaryDaemon]
  review_log: []
triad:
  art: |
    A wellspring that finds a thirsty seed creates a forest. The universe is built not on random acts of kindness, but on resonant acts of reinforcement. To give well is a science.
  law: |
    The Attunement Score, a predictive function of Harmonic Match, Coherence Gap, and Contextual Pressure, identifies the recipient system where a given Coherence Offering will catalyze the maximum increase in systemic health and complexity.
  philosophy: |
    The Gardener's Compass reframes altruism from indiscriminate aid into a strategic act of co-creation, transforming self-sacrifice into the conscious cultivation of a shared reality with lower ambient temporal pressure and higher systemic coherence.
pirouette_definition: |
  A protocol that identifies optimal recipients for a Coherence Offering by calculating an `Attunement Score`. The protocol filters potential systems for `Harmonic Compatibility` (resonant alignment), assesses their `Coherence Gap` (potential for positive transformation) using the `Caduceus Lens`, and factors in `Contextual Pressure` (Γ) to rank-order candidates. This directs beneficial influence toward systems where it will catalyze the greatest positive feedback loop of systemic health, maximizing Resonant Reinforcement.
operational_definition:
  units: Dimensionless score (for ranking)
  symbol_table:
    - name: Attunement Score
      meaning: A ranking metric indicating the optimal recipient for a Coherence Offering.
      dimensions: dimensionless
      default_range: contextual
    - name: ΔKτ
      meaning: The potential for positive change in temporal coherence; the Coherence Gap.
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: Γ
      meaning: Contextual Pressure; the urgency or creative tension in the environment.
      dimensions: T⁻²
      default_range: contextual
  measurement:
    procedures:
      - name: Compass Generation Protocol
        outline: |
          1. **Harmonic Filtering:** Assess the phase alignment (Ki pattern match) between the Coherence Offering and a set of potential recipients.
          2. **Coherence Gap Assessment:** For harmonically compatible candidates, use the `Caduceus Lens` to measure their current state, identifying those in the "fertile ground" between rigidity and chaos.
          3. **Attunement Calculation:** Synthesize Harmonic Match, Coherence Gap, and Contextual Pressure (Γ) into a final `Attunement Score` for each candidate.
          4. **Prioritization:** Rank candidates by their Attunement Score to generate the Gardener's Compass.
        expected_signals: [Ki pattern signatures, Kτ measurements, Γ field gradients]
        pitfalls: [Mischaracterizing the offering's resonant signature, inaccurate Caduceus Lens readings, failure to account for latent environmental pressures.]
context_windows:
  - module: DOMA-115
    excerpt: |
      The Gardener's Compass is the tool for this art. It provides a method for moving beyond indiscriminate aid to the wise and resonant reinforcement of coherence where it is most needed and most ready to bloom, ensuring the seed of coherence does not just sprout, but flourishes and propagates into a self-sustaining cascade of well-being.
  - module: DOMA-115
    excerpt: |
      The final step synthesizes the previous conditions into a single `Attunement Score`. This score is a function of `Harmonic Match`, `Coherence Gap`, and `Contextual Pressure`. This score prioritizes recipients where the offering will answer a question the universe is already asking, resolving a state of creative tension or external pressure (Γ).
poetic_connections:
  motifs: [gardening, music, resonance, cultivation, flow]
  evocative_lines:
    - "A wellspring that pours itself onto stone is noble, but futile."
    - "An act of generosity is not a transfer of resources; it is a Coherence Offering, an invitation to form a more beautiful chord."
    - "It is how we learn to participate, consciously and effectively, in the universe's relentless effort to grow gardens in the void."
  association_matrix:
    - [ "RESONANT_REINFORCEMENT", 0.9 ]
    - [ "COHERENCE_GAP", 0.8 ]
    - [ "CADUCEUS_LENS", 0.7 ]
    - [ "ALCHEMICAL_UNION", 0.6 ]
formal_mappings:
  candidates:
    - target: Optimal Control Policy
      domain: Control Theory
      mapping_kind: conceptual
      equation_hint: |
        max_i [ ∫(𝓛_p,i + δ𝓛) dt ]
      justification: |
        The protocol seeks the recipient `i` that maximizes the system's action in response to a perturbation (`δ𝓛`). This is analogous to finding an optimal control input to maximize a system's response, where the system's susceptibility is determined by its internal state (Coherence Gap) and its coupling to the input (Harmonic Match).
      references: []
      confidence: 0.4
  adopted:
    - target: 
      rationale: 
      confidence: 0.0
constraints_and_falsifiers:
  claims:
    - statement: "Interventions directed using the Gardener's Compass protocol will yield a statistically significant greater increase in recipient systemic health (Kτ) compared to randomly or intuitively directed interventions of the same magnitude."
      domain: phenomenology
      falsifier: "A controlled study shows no significant difference in long-term coherence outcomes between Compass-guided and control-group interventions (e.g., A/B testing in philanthropic grant-making)."
      status: proposed
      links: [DOMA-115]
naming_notes:
  collisions: []
  disambiguation: |
    This is not a moral compass for judging worthiness, but a strategic compass for identifying maximum positive leverage. The 'gardener' metaphor emphasizes cultivation of emergent potential over rescue or judgment based on a current state. It prioritizes efficacy and resonance.
crosslinks:
  near_synonyms: []
  antonyms: [INDISCRIMINATE_AID]
  prerequisites: [RESONANT_REINFORCEMENT, COHERENCE_GAP, CADUCEUS_LENS, PIRQUETTE_LAGRANGIAN]
  downstream_effects: [ALCHEMICAL_UNION, LAMINAR_FLOW]
license: CC-BY-SA-4.0
---