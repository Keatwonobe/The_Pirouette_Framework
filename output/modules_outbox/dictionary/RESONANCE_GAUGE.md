---
term: "Resonance Gauge"
canonical_id: "RESONANCE_GAUGE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-191"]
---

---
term: Resonance Gauge
canonical_id: RESONANCE_GAUGE
symbol: 
aliases: [Temporal Adherence Meter]
parents: [CORE-005, CORE-006]
children: []
status: ratified
version: 2.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-191
      lines: "§3"
      snippet: |
        The protocol for measuring Temporal Coherence is a two-step process of isolating a rhythm and then assessing its internal consistency. Step I: Isolate the Rhythm... Step II: Calculate the Coherence.
  editors: [weaver-lexicographer-7]
  review_log: []
triad:
  art: |
    The Resonance Gauge is a tuning fork pressed against a system's body to hear the clarity of its song. It listens for the pure note of coherence amidst the chaotic symphony of existence, judging how true the note rings.
  law: |
    A system's health and stability are quantified by its Coherence Index, the squared magnitude of the vector average of its components' phases, a dimensionless value ranging from 1 (perfect order) to 0 (total collapse).
  philosophy: |
    The Gauge reframes systemic existence from a state to be measured into a song to be judged. It provides an empirical measure of a system's health—its ability to maintain coherent form against dissipative pressure—grounding the Pirouette Lagrangian in observable reality.
pirouette_definition: |
  The Resonance Gauge is the universal diagnostic instrument and protocol for quantifying a system's Temporal Coherence. It assesses the stability and purity of a system's resonant Ki pattern by calculating the Coherence Index (`|C|^2`), a value from 0 to 1 derived from the vector average of its components' phases. This index serves as the direct, measurable input (`T_a`) for the kinetic term of the Pirouette Lagrangian.
operational_definition:
  units: dimensionless
  symbol_table:
    - name: C
      meaning: Coherence Vector
      dimensions: dimensionless
      default_range: Complex number with |C| ∈ [0, 1]
    - name: "|C|^2"
      meaning: Coherence Index
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: N
      meaning: Number of system components
      dimensions: dimensionless
      default_range: contextual, but >1
    - name: θ_j
      meaning: Phase of component j
      dimensions: dimensionless (angle)
      default_range: "[0, 2π)"
  measurement:
    procedures:
      - name: Coherence Index Calculation
        outline: |
          1.  **Isolate Rhythm:** For each of N components in the system, identify the core cyclical pattern (Ki) and extract its instantaneous phase, θ_j. For complex signals, this may use a Hilbert transform; for discrete agents, it involves observing their state within a cycle.
          2.  **Calculate Coherence:** Treat each phase as a unit vector (e^(iθ_j)) on the complex plane. Compute the complex vector average, `C = (1/N) Σ e^(iθ_j)`.
          3.  **Determine Index:** The Coherence Index is the squared magnitude of this vector, `|C|^2`.
        expected_signals: [Coherence Index ≈ 1 (Laminar Coherence), 0 < Index < 1 (Turbulent Coherence), Index ≈ 0 (Coherence Collapse)]
        pitfalls: [Incorrect identification of the system's core rhythm (Ki), Insufficient or biased sampling of components (N is too small), Confounding external signals masking the intrinsic rhythm]
context_windows:
  - module: DOMA-191
    excerpt: |
      High Coherence characterizes a system with a pure, stable, and sharply defined Ki resonance. Its rhythm is clear and predictable. This is a healthy system... Low Coherence characterizes a system with a chaotic, noisy, or decaying Ki pattern. Its rhythm is dissonant and unpredictable. This is a stressed or dying system, wasting energy in temporal friction.
  - module: DOMA-191
    excerpt: |
      This instrument provides a crucial empirical link to the framework's core mathematical engine, The Pirouette Lagrangian (CORE-006)... The Coherence Index calculated by this module is the direct, measurable value for the T_a term in the Lagrangian... With this tool, the Lagrangian ceases to be a purely theoretical construct. It becomes a predictive engine that can be fed with real-world data.
poetic_connections:
  motifs: [tuning fork, systemic health, signal vs noise, rhythm, harmony]
  evocative_lines:
    - "We sought a meter stick to measure time's straightness and were instead handed a tuning fork."
    - "In the great and chaotic symphony of existence, how true is this note?"
  association_matrix:
    - [ "TEMPORAL_COHERENCE", 0.9 ]
    - [ "KI", 0.8 ]
    - [ "PIROUETTE_LAGRANGIAN", 0.7 ]
    - [ "TEMPORAL_FORGE", 0.5 ]
formal_mappings:
  candidates:
    - target: Kuramoto order parameter `r`
      domain: Math
      mapping_kind: mathematical
      equation_hint: |
        |C| ≡ r, where `r e^(iψ) = (1/N) Σ e^(iθ_j)`
      justification: |
        The calculation of the Coherence Vector's magnitude, |C|, is identical to the formula for the Kuramoto order parameter, `r`, which measures the degree of phase synchronization in a population of coupled oscillators. The Coherence Index `|C|^2` is thus `r^2`, quantifying emergent collective behavior.
      references:
        - title: From Kuramoto to Crawford - exploring the onset of synchronization in populations of coupled oscillators
          where: Strogatz, S.H., Physica D 143, 1-20
          date: 2000-09-01
      confidence: 0.95
  adopted:
    - target: Kuramoto order parameter `r`
      rationale: The mathematical and conceptual structures are isomorphic. Both quantify the emergent phase coherence of a system's components, making it a direct and robust mapping.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "A system's Coherence Index, as a direct input (T_a) to the Pirouette Lagrangian, is predictive of that system's stability and geodesic path."
      domain: phenomenology
      falsifier: "If systems with consistently high Coherence Indices (>0.95) are observed to undergo spontaneous, unforced decoherence, while systems with low Indices (<0.1) demonstrate high stability and efficiency without intervention, the claim is falsified."
      status: supported
      links: [DOMA-191, CORE-006]
naming_notes:
  collisions: [Resonance (physics), Gauge (gauge theory)]
  disambiguation: |
    This is not a 'gauge' in the sense of gauge theory (a field-theoretic redundancy) but in its original sense as a measuring instrument or 'meter'. It measures the quality of a system's 'resonance,' not a fundamental interaction.
crosslinks:
  near_synonyms: [TEN-TAM-1.0]
  antonyms: []
  prerequisites: [KI, TEMPORAL_COHERENCE]
  downstream_effects: [PIROUETTE_LAGRANGIAN]
license: CC-BY-SA-4.0
---

# Resonance Gauge

## Canonical (Pirouette)
The Resonance Gauge is the universal diagnostic instrument and protocol for quantifying a system's Temporal Coherence. It assesses the stability and purity of a system's resonant Ki pattern by calculating the Coherence Index (`|C|^2`), a value from 0 to 1 derived from the vector average of its components' phases. This index serves as the direct, measurable input (`T_a`) for the kinetic term of the Pirouette Lagrangian.

## EFT-First Summary
The Resonance Gauge protocol is operationally equivalent to calculating the Kuramoto order parameter (`r`) for a system of coupled oscillators. Its output, the Coherence Index (`r^2`), quantifies the degree of macroscopic phase synchronization, providing a measure of emergent order analogous to a phase transition parameter in statistical mechanics. (cf. Strogatz, S.H. *Physica D*, 2000).

## Glossary Links
- See also: TEMPORAL_COHERENCE, KI, PIROUETTE_LAGRANGIAN