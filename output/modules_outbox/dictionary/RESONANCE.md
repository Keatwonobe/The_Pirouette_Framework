---
term: "Resonance"
canonical_id: "RESONANCE"
symbol: "R"
aliases: [Song, K_τ]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-094"]
---

---
term: Resonance
canonical_id: RESONANCE
symbol: R, K_τ
aliases: [Song, K_τ]
parents: [DOMA-094]
children: [DOMA-SPORTS-001, INST-NALY-001]
status: ratified
version: 2.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-094
      snippet: |
        Temporal Coherence (K_τ): This "kinetic" term represents the quality, intensity, and stability of the system's expressed resonant solution—its Ki pattern in motion. In the Auditor's Lens, this is measured as Resonance (R).
  editors: [Lexicographer-AI]
  review_log: []
triad:
  art: |
    The clarity of a system's song; the grace of its motion. It is the active, dynamic release of tension into coherent, beautiful form.
  law: |
    A system's Resonance must functionally correlate with its Pressure; sustained, high Pressure without a corresponding increase in Resonance is the canonical signature of impending coherence collapse.
  philosophy: |
    Resonance is the measure of a system's *being-in-action*. It asserts that a system's health is not defined by the absence of stress (Pressure), but by its capacity to transform that stress into coherent, purposeful expression.
pirouette_definition: |
  The kinetic term, `K_τ`, of the Pirouette Lagrangian (`𝓛_p = K_τ - V_Γ`). Resonance quantifies the coherence, intensity, and stability of a system's dynamic expression. Operationally, it is the measure of a system's active transformation of potential energy (Pressure) into organized action.
operational_definition:
  units: Dimensionless
  symbol_table:
    - name: R
      meaning: Resonance; the operational measurement of Temporal Coherence.
      dimensions: dimensionless
      default_range: "[0, ∞)"
    - name: K_τ
      meaning: Temporal Coherence; the formal kinetic term in the Pirouette Lagrangian.
      dimensions: dimensionless
      default_range: "[0, ∞)"
  measurement:
    procedures:
      - name: Proxy Monitoring (Tier 0 Audit)
        outline: |
          Identify one or more Key Performance Indicators (KPIs) that represent the system's primary coherent output (e.g., product shipment velocity, signal-to-noise ratio, athlete's power output). Measure the rate, stability, and quality of these KPIs over time. High, stable values indicate high Resonance.
        expected_signals: ["Laminar Flow: high, stable R tightly correlated with Pressure.", "Turbulence: high, erratic R.", "Coherence Collapse: R stagnates or drops to zero as Pressure rises."]
        pitfalls: ["Goodhart's Law: choosing a proxy that can be easily gamed, leading to a false signal of high Resonance while true coherence declines.", "Signal aliasing: misinterpreting periodic fluctuations as stable Resonance."]
context_windows:
  - module: DOMA-094
    excerpt: |
      Temporal Coherence (`K_τ`): This "kinetic" term represents the quality, intensity, and stability of the system's expressed resonant solution—its Ki pattern in motion. In the Auditor's Lens, this is measured as **Resonance (R)**. It is the active, dynamic release of tension into coherent form; it is the *clarity of the system's song*.
  - module: DOMA-094
    excerpt: |
      Laminar Flow | **P** and **R** are high, stable, and tightly correlated. | The system is in a healthy, high-performance state ("in the zone"). Identify and reinforce the conditions.
poetic_connections:
  motifs: [song, flow, clarity, grace, action, expression]
  evocative_lines:
    - "It is the clarity of the system's song."
    - "one note is the pressure of its struggle, the other is the resonance of its grace."
  association_matrix:
    - [ "PRESSURE", 0.9 ]
    - [ "COHERENCE", 0.95 ]
    - [ "ACTION", 0.8 ]
formal_mappings:
  candidates:
    - target: Kinetic Energy (T)
      domain: CM
      mapping_kind: mathematical
      equation_hint: |
        L = T - V  <=>  𝓛_p = K_τ - V_Γ
      justification: |
        Resonance (K_τ) occupies the same position in the Pirouette Lagrangian (𝓛_p) as kinetic energy (T) does in the classical Lagrangian (L). Both represent the energy of motion and change, as opposed to stored potential energy. This is the foundational isomorphism for the Auditor's Lens.
      references:
        - title: The Auditor's Lens
          where: DOMA-094 §2, §5
          date: 2025-10-18
      confidence: 0.95
  adopted:
    - target: Kinetic Energy (T)
      rationale: The source module (DOMA-094) explicitly grounds the P/R lens in the Pirouette Lagrangian, which is itself a direct application of the principle of least action from classical mechanics. The mapping of Resonance to the kinetic term is foundational to the entire diagnostic model.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "An increase in a system's Resonance is always preceded by or concurrent with an increase in its available potential energy (Pressure)."
      domain: phenomenology
      falsifier: "Observing a system generate sustained, high-quality Resonance (e.g., high-velocity, coherent output) from a state of demonstrably zero or decreasing Pressure. This would violate the conservation-of-energy-like principles implied by the Lagrangian."
      status: supported
      links: [DOMA-094]
naming_notes:
  collisions: ["R is used for Resistance in electronics and the gas constant in thermodynamics. K is a common symbol for constants."]
  disambiguation: |
    Within the Pirouette Framework, R always refers to Resonance unless explicitly subscripted. It is the kinetic counterpart to P (Pressure). The alias 'Song' emphasizes its expressive, informational quality, while 'K_τ' links it to the formal Lagrangian.
crosslinks:
  near_synonyms: [TEMPORAL_COHERENCE]
  antonyms: [TEMPORAL_PRESSURE]
  prerequisites: [TEMPORAL_PRESSURE, PIROUETTE_LAGRANGIAN]
  downstream_effects: [LAMINAR_FLOW, COHERENCE_COLLAPSE]
license: CC-BY-SA-4.0
---

# Resonance

## Canonical (Pirouette)
The kinetic term, `K_τ`, of the Pirouette Lagrangian (`𝓛_p = K_τ - V_Γ`). Resonance quantifies the coherence, intensity, and stability of a system's dynamic expression. Operationally, it is the measure of a system's active transformation of potential energy (Pressure) into organized action.

## Classical Mechanics Summary
Resonance (R) is the Pirouette Framework's analogue to the kinetic energy term (`T`) in a classical Lagrangian (`L = T - V`). It quantifies the energy of a system's coherent motion or organized action, representing the transformation of stored potential energy (Pressure, `V`) into expressive output. Monitoring Resonance provides a direct measure of a system's dynamic health and performance.

## Glossary Links
- See also: [Pressure](Pressure), [Pirouette Lagrangian](Pirouette_Lagrangian), [Coherence Collapse](Coherence_Collapse)