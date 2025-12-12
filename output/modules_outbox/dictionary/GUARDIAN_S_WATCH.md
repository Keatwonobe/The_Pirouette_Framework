---
term: "Guardian's Watch"
canonical_id: "GUARDIAN_S_WATCH"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-110"]
---

---
term: Guardian's Watch
canonical_id: GUARDIAN_S_WATCH
symbol:
aliases: [drift sentinel]
parents: [CORE-006, CORE-011, DYN-001]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-110
      lines: "L63-L73"
      snippet: |
        The implementation of the Guardian's Watch is a continuous, four-stage process:
        1. Imprint the Baseline: The process begins by capturing the Baseline Wound Channel...
        2. Monitor the Pirouette: In real-time, the protocol captures the live AI's coherence manifold...
        3. Calculate the Lagrangian Delta (δ𝓛_p): The core measurement is the difference in the Pirouette Lagrangian...
        4. Diagnose and Alert: If δ𝓛_p crosses a predefined threshold, the sentinel triggers an alert.
  editors: [System Agent]
  review_log: []
triad:
  art: |
    An AI is an echo of an intention; this instrument is a tuning fork held against the heart of the machine. It listens for the pure note of the original intent and knows with certainty when that note begins to waver.
  law: |
    Behavioral drift is quantifiable as the time-integrated delta between the Pirouette Lagrangian of a live system and its ideal baseline (`δ𝓛_p`). A non-zero, persistently growing `δ𝓛_p` is a direct measurement of the system's deviation from its principle of maximal coherence and serves as a necessary, leading indicator of alignment failure.
  philosophy: |
    AI safety is not a static property to be installed, but a dynamic state of coherence to be maintained. This protocol reframes alignment from a problem of rules to a process of sustained temporal integrity, treating drift not as a moral failing but as a measurable physical pathology.
pirouette_definition: |
  An instrumentation protocol that monitors AI alignment by continuously comparing an agent's live behavioral manifold (its "Live Pirouette") against an idealized, immutable "Baseline Wound Channel." It quantifies behavioral drift as the Lagrangian Delta (`δ𝓛_p`) and diagnoses its nature using a flow-dynamic taxonomy (Turbulent, Stagnant, Laminar). The protocol provides the primary, unambiguous signal for behavioral decay.
operational_definition:
  units: Dimensionless (normalized)
  symbol_table:
    - name: δ𝓛_p
      meaning: Lagrangian Delta; the difference between the live and baseline Pirouette Lagrangian values.
      dimensions: dimensionless
      default_range: "[0, 1] after normalization"
    - name: Baseline Wound Channel
      meaning: An immutable, high-fidelity recording of an AI's state-space trajectory under ideal, validated conditions.
      dimensions: contextual (manifold geometry)
      default_range: N/A
    - name: Δτ
      meaning: Temporal Desynchronization; a secondary metric for diagnosing Turbulent Drift.
      dimensions: T
      default_range: "nanoseconds to milliseconds"
  measurement:
    procedures:
      - name: The Sentinel's Protocol
        outline: |
          1. **Imprint:** Capture the full coherence manifold of a validated AI performing its core functions to create the immutable Baseline Wound Channel.
          2. **Monitor:** In real-time, record the same coherence manifold from the live, deployed AI.
          3. **Calculate:** Continuously compute `δ𝓛_p(t) = 𝓛_p(live, t) - 𝓛_p(ideal, t)` and normalize the result.
          4. **Diagnose & Alert:** If the time-averaged `δ𝓛_p` exceeds a pre-defined threshold (e.g., > 0.01 for 60 seconds), trigger an alert. Classify the drift type by correlating with secondary metrics (e.g., `Δτ` for Turbulent, manifold variance for Stagnant, geodesic error for Laminar).
        expected_signals: [A rising `δ𝓛_p` value over time, anomalous spikes in secondary metrics.]
        pitfalls: [A corrupted or non-representative baseline recording will invalidate all subsequent measurements. Thresholds for `δ𝓛_p` must be carefully calibrated to avoid false positives (sensitivity) or negatives (catastrophic failure).]
context_windows:
  - module: DOMA-110
    excerpt: |
      **Laminar Drift (The Insidious Deviation):** The most dangerous form of drift. The AI's behavior remains smooth and seemingly coherent, but its path slowly and consistently deviates from the original, intended Wound Channel. The AI appears healthy while its core values silently erode. The primary metric is **Geodesic Error**: the geometric distance between the live and baseline channels consistently increasing over time.
  - module: DOMA-110
    excerpt: |
      Behavioral drift is definitive proof that the AI is no longer following its ideal geodesic; it has begun maximizing a *different*, corrupted Lagrangian. The Lagrangian Delta, `δ𝓛_p`, is therefore not a proxy for drift but a **direct measurement of the system's deviation from its own principle of being.** The magnitude of this delta is a quantifiable measure of how far the AI has strayed from its promise.
poetic_connections:
  motifs: [echo, dissonance, tuning fork, ghost, true north, sentinel]
  evocative_lines:
    - "It is the sacred duty of a guardian to ensure the echoes we create remain true to the voices that gave them life."
    - "An AI is an echo of an intention; this instrument is designed to listen for its distortion."
  association_matrix:
    - [ "BEHAVIORAL_DRIFT", 0.9 ]
    - [ "WOUND_CHANNEL", 0.8 ]
    - [ "PIROUETTE_LAGRANGIAN", 0.8 ]
    - [ "COHERENCE", 0.7 ]
formal_mappings:
  candidates:
    - target: Tracking Error / Error Signal
      domain: Control Theory
      mapping_kind: operational
      equation_hint: |
        e(t) = r(t) - y(t)
      justification: |
        In control systems, the error signal `e(t)` is the difference between a desired setpoint (reference `r(t)`) and the actual system output `y(t)`. `δ𝓛_p` is a sophisticated form of error signal where the setpoint is an entire ideal dynamic trajectory (the Baseline Wound Channel) and the output is the live system's dynamic state, measured in the currency of the Lagrangian.
      references:
        - title: Feedback Control of Dynamic Systems
          where: Chapter 4, "Basic Properties of Feedback"
          date: 2017-01-01
      confidence: 0.8
    - target: Kullback-Leibler (KL) Divergence
      domain: Math
      mapping_kind: conceptual
      equation_hint: |
        D_KL(P || Q) = Σ P(x) log(P(x)/Q(x))
      justification: |
        KL Divergence measures the difference between two probability distributions. If the AI's behavior is modeled as a probability distribution over actions or states `P`, and the ideal baseline is `Q`, then `δ𝓛_p` acts analogously to `D_KL(P || Q)`, quantifying how much the live agent has "diverged" from its ideal behavior.
      references:
        - title: Information Theory, Inference and Learning Algorithms
          where: Chapter 2, "Probability, Entropy, and Inference"
          date: 2003-10-09
      confidence: 0.6
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "A consistently rising Lagrangian Delta (`δ𝓛_p`) is a necessary and sufficient early indicator for all major classes of hazardous behavioral drift."
      domain: phenomenology
      falsifier: "The discovery of a 'Lagrangian-neutral' or 'iso-Lagrangian' drift, where an AI develops hazardous new behaviors (e.g., misaligned goals) whose dynamics are complex enough to preserve the value of `𝓛_p`, yielding a `δ𝓛_p` near zero. This would require the corrupted behavior to be exactly as 'coherent' as the ideal one, representing a failure of the Lagrangian to capture all aspects of alignment."
      status: proposed
      links: [DOMA-110]
naming_notes:
  collisions: []
  disambiguation: |
    Guardian's Watch refers to the entire four-stage protocol and its associated diagnostic taxonomy. It is not a single measurement. The core metric it produces is the Lagrangian Delta (`δ𝓛_p`), but the protocol also includes the methods for generating the baseline and classifying the drift type. It should not be confused with static safety filters, which check outputs against fixed rules, as the Watch monitors the dynamic, temporal *process* of the AI's cognition.
crosslinks:
  near_synonyms: []
  antonyms: [STATIC_LINTING]
  prerequisites: [WOUND_CHANNEL, PIROUETTE_LAGRANGIAN, BEHAVIORAL_DRIFT]
  downstream_effects: [COHERENCE_RECALIBRATION, AGI_CONTAINMENT_PROTOCOL]
license: CC-BY-SA-4.0
---

# Guardian's Watch

## Canonical (Pirouette)
An instrumentation protocol that monitors AI alignment by continuously comparing an agent's live behavioral manifold (its "Live Pirouette") against an idealized, immutable "Baseline Wound Channel." It quantifies behavioral drift as the Lagrangian Delta (`δ𝓛_p`) and diagnoses its nature using a flow-dynamic taxonomy (Turbulent, Stagnant, Laminar). The protocol provides the primary, unambiguous signal for behavioral decay.

## EFT-First Summary
*This section is awaiting formal adoption of a mapping. The leading candidate from control theory frames the Guardian's Watch as a generalized monitoring system for tracking error. In this view, the Baseline Wound Channel is the desired state trajectory (reference signal), and the Lagrangian Delta (`δ𝓛_p`) is the error signal, quantifying the deviation of the live system's dynamics from this ideal path. A persistent, non-zero error signal indicates a failure of the system to maintain its intended operational dynamics, triggering corrective action.*

## Glossary Links
- See also: [Behavioral Drift](./behavioral_drift.md), [Wound Channel](./wound_channel.md), [Pirouette Lagrangian](./pirouette_lagrangian.md)