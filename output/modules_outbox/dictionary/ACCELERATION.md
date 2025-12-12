---
term: "Acceleration"
canonical_id: "ACCELERATION"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-169"]
---

---
term: Acceleration
canonical_id: ACCELERATION
symbol: Φ_accel
aliases: [Exponential Recovery, Channel Carving]
parents: [DOMA-169]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-169
      lines: "L63-L67"
      snippet: |
        2.  **Acceleration (Carving the New Riverbed):** A path of sufficient coherence is found. The system commits its energy and begins to move, rapidly carving a new channel. This is the phase of exponential recovery, where coherence is rebuilt and a new, stable pattern begins to emerge.
  editors: [system]
  review_log: []
triad:
  art: |
    The silent search gives way to a violent birth. The system commits its energy to carving a new riverbed in the landscape of possibility, and the waters of coherence begin to rush and roar.
  law: |
    Acceleration is the phase of recovery characterized by a positive second derivative of system coherence (d²K/dt² > 0). The rate of recoherence is itself increasing, typically following an exponential or sigmoidal growth curve, until an inflection point is reached.
  philosophy: |
    Acceleration demonstrates that recovery is not passive healing but an active, energetic act of creation. It is the system's definitive commitment to a new path, transforming the potential discovered during Latency into the kinetic reality of a new stable form.
pirouette_definition: |
  Acceleration is the second of three temporal phases of systemic recovery, following Latency and preceding Stabilization. It is the period of rapid, often exponential, recoherence where a system, having identified a viable path on the coherence manifold, commits its energy to actively carving a new Wound Channel. This phase is marked by the emergence of a new, stable resonant pattern (Ki) and a swift increase in Temporal Coherence (Kτ) as the system re-establishes Laminar Flow.
operational_definition:
  units: Dimensionless (as it is a phase), but its dynamics are measured by the rate of change of coherence (e.g., bits/s²).
  symbol_table:
    - name: Φ_accel
      meaning: The Acceleration phase of recovery.
      dimensions: dimensionless
      default_range: "N/A (Categorical)"
    - name: K
      meaning: Systemic Coherence
      dimensions: dimensionless (bits)
      default_range: "[0, 1] or context-dependent"
    - name: t
      meaning: Time
      dimensions: T
      default_range: "> 0"
  measurement:
    procedures:
      - name: Time-Series Coherence Analysis
        outline: |
          1. Continuously monitor a proxy for system coherence (K), such as order parameters, network entropy, or signal-to-noise ratio.
          2. Identify the end of the Latency phase, marked by the first statistically significant, sustained positive-trending inflection point in K.
          3. The Acceleration phase is the interval where dK/dt > 0 and d²K/dt² > 0 (concave up).
          4. The phase ends when d²K/dt² transitions to ≤ 0, which marks the onset of Stabilization.
        expected_signals: [Exponential or logistic (S-curve) growth in the coherence metric K, A peak in the second derivative of K.]
        pitfalls: [Mistaking noise or transient fluctuations for the onset of Acceleration, Choosing a poor proxy for coherence that lags or misrepresents the true system state.]
context_windows:
  # Short, trimmed context quotes harvested from modules (3–6 sentences each).
  - module: DOMA-169
    excerpt: |
      The process of re-establishing Laminar Flow unfolds in three distinct temporal phases... 2. **Acceleration (Carving the New Riverbed):** A path of sufficient coherence is found. The system commits its energy and begins to move, rapidly carving a new channel. This is the phase of exponential recovery, where coherence is rebuilt and a new, stable pattern begins to emerge. The system is not just moving; it is actively reshaping its landscape through its motion.
  - module: DOMA-169
    excerpt: |
      A system in recovery is not acting randomly; it is relentlessly solving for the state that maximizes its coherence integral (`S_p = ∫𝓛_p dt`). The choice between Restorative, Adaptive, and Transformative paths is not a choice at all; it is the inevitable outcome of the system following its new geodesic toward a new peak on the coherence manifold.
poetic_connections:
  # Lightweight "word-association graph" and sticky lines.
  motifs: [channel carving, exponential growth, re-creation, the new riverbed, recoherence]
  evocative_lines:
    - "The system is not just moving; it is actively reshaping its landscape through its motion."
    - "A collapse is not an ending; it is a question posed in the language of chaos."
  association_matrix:
    # symmetric or directed; weights in [0,1]
    - [ "LATENCY", 0.9 ]
    - [ "STABILIZATION", 0.9 ]
    - [ "WOUND_CHANNEL", 0.8 ]
    - [ "COHERENCE", 0.7 ]
    - [ "COLLAPSE", 0.5 ]
formal_mappings:
  # Candidate alignments to EFT/SM/CM/GR terms, each with justification and refs.
  candidates:
    - target: Logarithmic (Log) Phase of Microbial Growth
      domain: Biology
      mapping_kind: conceptual
      equation_hint: |
        N(t) = N₀ * e^(μt)
      justification: |
        The Acceleration phase is analogous to the log phase of bacterial growth, where, after a lag (Latency) phase, the population grows exponentially as it exploits available resources to rapidly increase its order and complexity. Both represent a period of maximum, self-reinforcing growth after a viable path has been established.
      references:
        - title: Brock Biology of Microorganisms
          where: Chapter 5: Microbial Growth
          date: 2021-01-12
      confidence: 0.7
    - target: Growth of an order parameter (ψ) in Landau theory
      domain: CM
      mapping_kind: conceptual
      equation_hint: |
        F = a(T-T_c)ψ² + bψ⁴
      justification: |
        Like the growth of an order parameter below a critical point, Acceleration marks the emergence of a new, coherent systemic pattern (Ki) from a disordered state. The rate of this emergence is not linear but explosive, driven by the system settling into a new minimum of a potential landscape (the coherence manifold).
      references:
        - title: Principles of Condensed Matter Physics
          where: Ch. 3, Landau Theory
          date: 2000-09-14
      confidence: 0.6
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "All systemic recovery events that achieve a new stable state must exhibit an Acceleration phase characterized by a period where the second derivative of coherence with respect to time is positive (d²K/dt² > 0)."
      domain: phenomenology
      falsifier: "The discovery of a verified systemic recovery to a new stable state that occurs via a purely linear or concave-down increase in coherence (d²K/dt² ≤ 0 for the entire recovery period), implying no phase of self-reinforcing growth."
      status: proposed
      links: [DOMA-169]
naming_notes:
  collisions: [a (mechanical acceleration)]
  disambiguation: |
    Distinguish from mechanical acceleration (rate of change of velocity). Pirouette's Acceleration refers to the rate of change in the *rate of recoherence*, a second-order temporal dynamic of a scalar field (coherence), not a vector quantity in physical space.
crosslinks:
  near_synonyms: [EXPONENTIAL_RECOVERY]
  antonyms: [LATENCY, COLLAPSE]
  prerequisites: [LATENCY]
  downstream_effects: [STABILIZATION, WOUND_CHANNEL]
license: CC-BY-SA-4.0
---

# Acceleration

## Canonical (Pirouette)
Acceleration is the second of three temporal phases of systemic recovery, following Latency and preceding Stabilization. It is the period of rapid, often exponential, recoherence where a system, having identified a viable path on the coherence manifold, commits its energy to actively carving a new Wound Channel. This phase is marked by the emergence of a new, stable resonant pattern (Ki) and a swift increase in Temporal Coherence (Kτ) as the system re-establishes Laminar Flow.

## Physical Analogue Summary
Conceptually, the Acceleration phase mirrors the dynamics of other natural growth phenomena. In biology, it is analogous to the **Log Phase** of microbial growth, where a population expands exponentially after an initial lag. In condensed matter physics, it resembles the rapid growth of an **order parameter** (e.g., magnetization) as a system cools through a phase transition, establishing a new, more ordered state from a disordered one. In both cases, a system commits to a new configuration and undergoes a period of self-reinforcing, non-linear growth.

## Glossary Links
- See also: [Latency](<./LATENCY.md>), [Stabilization](<./STABILIZATION.md>), [Coherence](<./COHERENCE.md>), [Wound Channel](<./WOUND_CHANNEL.md>)