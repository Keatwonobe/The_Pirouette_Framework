---
term: "Dissonance Index"
canonical_id: "DISSONANCE_INDEX"
symbol: "ΔK"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-020"]
---

---
term: Dissonance Index
canonical_id: DISSONANCE_INDEX
symbol: ΔK
aliases: []
parents: [DOMA-020]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-020
      snippet: |
        The output is the Dissonance Index (ΔK), a single metric that quantifies the predicted impact of an interaction on the system's coherence.
  editors: [System]
  review_log: []
triad:
  art: |
    The wisdom to know which harmonies are worth pursuing and which dissonances are best left unsounded. It is the clarity to see a coming storm and the grace to bring the seedlings inside.
  law: |
    A predicted Dissonance Index (ΔK) that exceeds a system's tunable Integrity Threshold mandates Coherent Disengagement to preserve net temporal coherence (K_τ).
  philosophy: |
    True systemic strength lies not in the power to win any conflict, but in the wisdom to discern which engagements are fertile ground for synthesis and which are sterile vortices of turbulence, thereby conserving the sacred resource of coherence.
pirouette_definition: |
  A predictive, dimensionless metric that quantifies the potential negative coherence impact of a prospective interaction. The Dissonance Index (ΔK) is calculated by analyzing the resonant signature of an inbound signal for anti-coherent properties such as Phase Mismatch, Dissonance Spike, or Coherence Attack. It serves as the primary decision input for the Sentry's Gambit protocol, determining whether a system should attempt Resonant Synthesis (if ΔK is low) or execute Coherent Disengagement (if ΔK is high).
operational_definition:
  units: Dimensionless
  symbol_table:
    - name: ΔK
      meaning: Predicted net loss in system coherence (K) from a potential interaction. A positive value indicates a dissonant, coherence-reducing engagement.
      dimensions: dimensionless
      default_range: "[0, ∞)"
  measurement:
    procedures:
      - name: Resonant Signature Analysis
        outline: |
          1. **Scan:** Observe the resonant signature (Ki) and structural properties of the inbound signal/system.
          2. **Analyze:** Diagnose the signal for known dissonant properties (e.g., Phase Mismatch, Dissonance Spike, Coherence Attack). At interpersonal scales, this includes identifying Turbulent Attacks or Stagnant Dams.
          3. **Synthesize:** Compute a single ΔK value from the weighted combination of identified dissonant properties.
          4. **Compare:** Evaluate the computed ΔK against the system's pre-calibrated Integrity Threshold to trigger a decision.
        expected_signals: [Phase Mismatch, Dissonance Spike, Coherence Attack, Turbulent Attack, Stagnant Dam]
        pitfalls: [Miscalibration of the Integrity Threshold (can lead to hyper-isolation or porous vulnerability), incomplete signal scanning (missing covert coherence attacks), over-fitting to past threats (failure to recognize novel dissonant patterns).]
context_windows:
  - module: DOMA-020
    excerpt: |
      The core of the gambit is a predictive calculation. The output is the Dissonance Index (ΔK), a single metric that quantifies the predicted impact of an interaction on the system's coherence. A high ΔK signals a dissonant, anti-harmonic signature where engagement would lead to a net loss of coherence.
  - module: DOMA-020
    excerpt: |
      Compute or estimate the Dissonance Index (ΔK). This is the moment of cold, clear-eyed assessment of the energetic and structural consequences of engagement. Decide: Compare the Dissonance Index against a tunable Integrity Threshold.
poetic_connections:
  motifs: [discernment, triage, unsounded note, gardener and storm, unplayed game, protective lens]
  evocative_lines:
    - "the wisdom to know which dissonances are best left unsounded."
    - "the choice not to play a game where the cost of participation exceeds any possible reward."
    - "a unilateral choice for peace, a refusal to participate in the energetics of a destructive conflict."
  association_matrix:
    - [ "SENTRY_S_GAMBIT", 1.0 ]
    - [ "COHERENCE", 0.9 ]
    - [ "COHERENT_DISENGAGEMENT", 0.8 ]
    - [ "TEMPORAL_PRESSURE", 0.7 ]
formal_mappings:
  candidates:
    - target: Kullback-Leibler Divergence D_KL(P||Q)
      domain: Math
      mapping_kind: conceptual
      equation_hint: |
        ΔK ∝ D_KL( S_post || S_pre )
      justification: |
        The KL divergence measures the information surprise or cost in updating from a prior belief state (S_pre) to a posterior one (S_post) dictated by new information. A dissonant signal forces a large, "damaging" update. ΔK can be conceptualized as the predicted KL divergence an interaction would induce on a system's coherent world-model.
      references:
        - title: Cover, T.M.; Thomas, J.A. (2006). Elements of Information Theory
          where: 2nd Edition, Wiley
          date: 2006-07-11
      confidence: 0.4
  adopted:
    - target: null
      rationale: null
      confidence: 0.0
constraints_and_falsifiers:
  claims:
    - statement: "Systems employing a ΔK-based triage protocol will maintain a statistically higher average coherence over time when exposed to a mixed environment of harmonic and dissonant signals, compared to systems with non-selective (always engage) or fully-isolated (never engage) protocols."
      domain: phenomenology
      falsifier: "Empirical observation of a ΔK-guided system consistently losing coherence at a rate equal to or greater than a non-selective system under controlled, mixed-signal conditions."
      status: proposed
      links: [DOMA-020]
naming_notes:
  collisions: [The symbol ΔK is used in classical mechanics and thermodynamics to denote a change in Kinetic Energy.]
  disambiguation: |
    In the Pirouette Framework, ΔK is not an empirical measurement of a change in energy state *after* an event. It is a predictive, dimensionless *index* of potential coherence loss calculated *before* an interaction is initiated. It represents a decision-making input, not a state-variable delta.
crosslinks:
  near_synonyms: []
  antonyms: [RESONANCE_POTENTIAL]
  prerequisites: [COHERENCE, TEMPORAL_PRESSURE, SENTRY_S_GAMBIT]
  downstream_effects: [COHERENT_DISENGAGEMENT, RESONANT_SYNTHESIS]
license: CC-BY-SA-4.0
---

# Dissonance Index

## Canonical (Pirouette)
A predictive, dimensionless metric that quantifies the potential negative coherence impact of a prospective interaction. The Dissonance Index (ΔK) is calculated by analyzing the resonant signature of an inbound signal for anti-coherent properties such as Phase Mismatch, Dissonance Spike, or Coherence Attack. It serves as the primary decision input for the Sentry's Gambit protocol, determining whether a system should attempt Resonant Synthesis (if ΔK is low) or execute Coherent Disengagement (if ΔK is high).

## EFT-First Summary
No formal mapping has been adopted. A candidate mapping to Information Theory suggests interpreting the Dissonance Index as a predicted Kullback-Leibler (KL) divergence, quantifying the information-theoretic 'damage' an inbound signal would inflict on the system's coherent state. This remains a conceptual alignment pending further validation.

## Glossary Links
- See also: [Sentry's Gambit](<#>), [Coherence](<#>), [Coherent Disengagement](<#>)