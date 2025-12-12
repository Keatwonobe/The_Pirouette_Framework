---
term: "Good tired"
canonical_id: "GOOD_TIRED"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-HLTH-001"]
---

---
term: Good tired
canonical_id: GOOD_TIRED
symbol: T_G
aliases: [satisfying ache, feeling of growth, eustress fatigue]
parents: [DOMA-HLTH-001]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-HLTH-001
      lines: "Phase III"
      snippet: |
        The Guiding Feeling: The feeling you are looking for is "good tired"—the satisfying ache of muscles that have done good work, not the sharp cry of pain. Pain is a signal to stop. "Good tired" is the feeling of growth.
  editors: [Agent: Pirouette-Lexicographer]
  review_log: []
triad:
  art: |
    The satisfying warmth of a well-worked field at dusk. It is the hum of the body's machinery cooling after forging new strength, a quiet promise of a stronger dawn.
  law: |
    A physiological sensation is classified as "good tired" if and only if it follows exertion, is perceived as satisfying rather than alarming, resolves within 48 hours, and is followed by a measurable maintenance or increase in performance capacity. Otherwise, it is classified as pain or systemic fatigue.
  philosophy: |
    This term establishes the primacy of subjective experience as a valid, high-fidelity signal for navigating biological adaptation. It empowers an individual to titrate stress into a productive force, transforming the body from a fragile object to be protected into a resilient system to be cultivated. It is the core feedback mechanism for self-guided growth.
pirouette_definition: |
  The subjective, physiological sensation of muscular fatigue following a non-injurious, capacity-building effort. It is characterized by a diffuse, satisfying ache or warmth that resolves with rest and is prospectively correlated with an increase in physical resilience. It is the primary qualitative feedback signal used to titrate exertion during training and rehabilitation, critically distinguished from the sharp, localized, and persistent signal of pain.
operational_definition:
  units: Dimensionless (Subjective Scale)
  symbol_table:
    - name: T_G
      meaning: Intensity of "Good tired" sensation
      dimensions: dimensionless
      default_range: "[0, 10], where 0 is no sensation and 10 is maximal satisfying muscular fatigue."
  measurement:
    procedures:
      - name: Post-Exertion Sensation Logging
        outline: |
          1. Subject performs a defined physical task.
          2. At T+1 hour and T+24 hours, subject rates the sensation in the target muscle groups on a 0-10 scale (T_G).
          3. Subject concurrently rates any sharp pain on a separate 0-10 scale (P_S).
          4. A valid T_G signal is a score > 2 with a P_S score < 1.
          5. Data is logged in the Coherence Ledger and correlated with performance metrics of the next session.
        expected_signals: [Elevated T_G, minimal P_S, subsequent performance increase]
        pitfalls: [Conflating T_G with pain (injury risk), conflating T_G with systemic exhaustion (overtraining risk), subjective reporting inconsistency.]
context_windows:
  - module: DOMA-HLTH-001
    excerpt: |
      Core Practice: Structured exercise. This is where your formal cardiac rehabilitation program shines. You'll work on increasing your aerobic endurance and begin light resistance training. The Guiding Feeling: The feeling you are looking for is "good tired"—the satisfying ache of muscles that have done good work, not the sharp cry of pain. Pain is a signal to stop. "Good tired" is the feeling of growth.
  - module: DOMA-HLTH-001
    excerpt: |
      Throughout this journey, you are listening for two voices... The Voice of your Body: This is your Heart Rate, your energy levels, your aches, and your pains. It tells you the honest, physical truth of each moment... When they are in harmony (your Body feels ready for the challenge your Will sets), that is the signal for growth. Your Coherence Ledger is the tool that helps you hear this duet clearly.
poetic_connections:
  motifs: [Forging, Growth, Compass, Rhythm, Harvest]
  evocative_lines:
    - "the satisfying ache of muscles that have done good work"
    - "Pain is a signal to stop. 'Good tired' is the feeling of growth."
    - "You no longer need a rigid map because you have become the navigator."
  association_matrix:
    - [ "Coherence Ledger", 0.9 ]
    - [ "Resilience", 0.8 ]
    - [ "Challenge", 0.8 ]
    - [ "Effortless Flow", 0.5 ]
formal_mappings:
  candidates:
    - target: Delayed Onset Muscle Soreness (DOMS)
      domain: CM
      mapping_kind: conceptual
      justification: |
        "Good tired" corresponds to the mild, adaptive end of the DOMS spectrum. It specifically isolates the sensation of muscle microtrauma that stimulates hypertrophy and repair, while excluding the debilitating soreness that indicates excessive damage.
      references:
        - title: "Mechanisms of exercise-induced delayed onset muscle soreness: a brief review"
          where: "Medicine and Science in Sports and Exercise, 2003"
          date: 2003-02-01
      confidence: 0.8
  adopted:
    - target: Hormesis
      rationale: |
        Hormesis, the principle where a low dose of a stressor yields an adaptive, beneficial effect, is the most precise formal model. "Good tired" is the direct subjective perception of a hormetic physical stimulus. The dose of exercise is sufficient to trigger anabolic signaling and up-regulate resilience pathways, but is below the threshold that causes net catabolic damage. This mapping captures the dose-response relationship central to the concept.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "The subjective sensation of 'good tired' (T_G > 2, P_S < 1) following exertion is a reliable positive predictor of subsequent increases in the exerted muscle's strength or endurance capacity within 72-96 hours."
      domain: experiment
      falsifier: "A longitudinal study of a rehab cohort shows no statistically significant correlation between self-reported T_G scores and measured performance improvements in subsequent sessions."
      status: proposed
      links: [DOMA-HLTH-001]
naming_notes:
  collisions: [Fatigue, Exhaustion, Soreness]
  disambiguation: |
    "Good tired" is distinct from systemic Fatigue or Exhaustion, which are signals of central nervous system over-taxation or insufficient recovery and are not localized to worked muscles. It is also distinct from Soreness or Pain, which are alarming, sharp, and/or persistent signals of actual or potential tissue injury. The valence of "good tired" is positive and satisfying; the valence of pain is negative and alarming.
crosslinks:
  near_synonyms: []
  antonyms: [PAIN_SIGNAL]
  prerequisites: [COHERENCE_LEDGER]
  downstream_effects: [RESILIENCE, EFFORTLESS_FLOW]
license: CC-BY-SA-4.0
---

# Good tired

## Canonical (Pirouette)
The subjective, physiological sensation of muscular fatigue following a non-injurious, capacity-building effort. It is characterized by a diffuse, satisfying ache or warmth that resolves with rest and is prospectively correlated with an increase in physical resilience. It is the primary qualitative feedback signal used to titrate exertion during training and rehabilitation, critically distinguished from the sharp, localized, and persistent signal of pain.

## EFT-First Summary
"Good tired" is the subjective, phenomenological marker for a hormetic response to physical stress. It signals that a dose of exertion has been applied which is sufficient to trigger beneficial adaptation (e.g., muscle hypertrophy, increased cardiovascular capacity) without causing systemic injury. As described in the biological principle of hormesis, this controlled, low-level stressor leads to a net gain in systemic resilience and performance.

## Glossary Links
- See also: [[Pain Signal]], [[Effortless Flow]], [[Coherence Ledger]]