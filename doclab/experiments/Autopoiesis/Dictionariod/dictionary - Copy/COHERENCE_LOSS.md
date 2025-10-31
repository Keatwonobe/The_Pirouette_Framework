---
term: "coherence loss"
canonical_id: "COHERENCE_LOSS"
symbol: ""
aliases: [dissonance]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-033"]
---

---
term: coherence loss
canonical_id: COHERENCE_LOSS
symbol: -ΔSₚ
aliases: [dissonance]
parents: [DOMA-033, CORE-006]
children: [dashboards]
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-033
      lines: "L72-74"
      snippet: |
        The magnitude and duration of the dip provide a precise, quantitative "impact score" for that event. This score is not an arbitrary proxy; it is a direct measure of the coherence lost.
  editors: [AI Assistant]
  review_log: []
triad:
  art: |
    A system in pain does not announce its wound; it simply loses its grace. Coherence loss is the felt sense of "wrongness"—the dissonance in a system's rhythm—made visible and measurable.
  law: |
    Coherence loss is the negative, time-integrated perturbation of a system's Pirouette Lagrangian (𝓛_p), correlated with specific causal events. The total loss for a given period is the net negative change in the system's Action (ΔSₚ < 0).
  philosophy: |
    This concept transforms a vague problem into a precise target. It asserts that systemic failures are not nebulous, but are the cumulative result of specific, identifiable fractures in coherence. To measure coherence loss is to begin the act of healing.
pirouette_definition: |
  The measurable degradation of a system's internal resonance, identified as a negative perturbation to its Action (S_p). It is quantified by integrating the dips in the Pirouette Lagrangian (𝓛_p) time-series that are correlated with specific, causal events. Coherence loss is the primary diagnostic target for a Weaver seeking to restore a system to its optimal path of maximal coherence.
operational_definition:
  units: Action (e.g., Joule-seconds)
  symbol_table:
    - name: -ΔSₚ
      meaning: Total Coherence Loss over a period. A positive scalar value representing the magnitude of the negative change in system Action.
      dimensions: M L² T⁻¹ (Action)
      default_range: "[0, ∞)"
    - name: 𝓛_p
      meaning: The Pirouette Lagrangian, representing the system's instantaneous coherence.
      dimensions: M L² T⁻² (Action/Time, or Energy)
      default_range: contextual
    - name: I(fᵢ)
      meaning: Impact of a specific event fᵢ; the coherence loss attributable to that single event.
      dimensions: M L² T⁻¹ (Action)
      default_range: contextual
  measurement:
    procedures:
      - name: Coherence Audit
        outline: |
          1.  **Project:** Use the Fractal Bridge protocol (CORE-014) to translate raw, high-dimensional system data into a single time-series of the Pirouette Lagrangian (𝓛_p).
          2.  **Correlate:** Identify all negative deviations (dips) in the 𝓛_p trace and correlate them with timestamped causal events from the raw data.
          3.  **Quantify:** For each causal event (fᵢ), calculate its Impact (I) by integrating the corresponding Lagrangian dip: I(fᵢ) ≈ - ∫_dip Δ𝓛_p dt. The total coherence loss is the sum of all Impacts.
        expected_signals: [A volatile or decaying 𝓛_p time-series, A Pareto-distributed list of high-impact events]
        pitfalls: [Misattribution of causality from mere correlation, Signal aliasing from insufficient data sampling frequency, Incorrect Fractal Bridge mapping leading to a distorted 𝓛_p trace]
context_windows:
  - module: DOMA-033
    excerpt: |
      A system in pain does not announce its wound; it simply loses its grace. The fundamental task of a Weaver is to perceive this loss of grace—this dissonance—and trace it to its source. Answering the question, "Where is the coherence being lost, and why?" is the first step toward healing, optimizing, and creating.
  - module: DOMA-033
    excerpt: |
      The Auditor correlates every event in the original raw data with a corresponding dip in the Lagrangian trace. The magnitude and duration of the dip provide a precise, quantitative "impact score" for that event. This score is not an arbitrary proxy; it is a direct measure of the coherence lost.
  - module: DOMA-033
    excerpt: |
      Every "impact" measured by RPA is a quantifiable, negative perturbation to this integral [S_p = ∫ 𝓛_p dt]. The Auditor is, therefore, a tool for empirically discovering what is preventing a system from obeying its own most fundamental drive. It translates a philosophical principle into a diagnostic engine.
poetic_connections:
  motifs: [dissonance, arrhythmia, fracture, friction, static, loss of grace]
  evocative_lines:
    - "A system in pain does not announce its wound; it simply loses its grace."
    - "The clarity to touch the single thread that will mend the entire tapestry."
  association_matrix:
    - [ "ACTION", -0.9 ]
    - [ "PIROUETTE_LAGRANGIAN", -0.8 ]
    - [ "COHERENCE_AUDITOR", 0.9 ]
    - [ "CRITICAL_FEW", 0.7 ]
formal_mappings:
  candidates:
    - target: Dissipative Work (W_diss)
      domain: CM
      mapping_kind: conceptual
      justification: |
        Coherence loss represents a system being forced off its optimal, action-maximizing path. This is analogous to how non-conservative forces like friction perform negative work on a mechanical system, dissipating energy and causing deviation from the path of least action defined by conservative forces.
      references: []
      confidence: 0.7
    - target: Entropy Production (ΔS_entropy)
      domain: SM
      mapping_kind: conceptual
      equation_hint: |
        Coherence Loss ∝ ΔS_entropy
      justification: |
        A loss of internal resonance or "grace" implies a move towards a more disordered, higher-entropy state. The irreversible events causing coherence loss are analogous to thermodynamic processes that generate entropy, representing a loss of available "work" or potential.
      references: []
      confidence: 0.6
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "For any sufficiently complex system, total coherence loss follows a Pareto distribution, where a small fraction of causal event types (~20%) accounts for the majority of the total loss (~80%)."
      domain: phenomenology
      falsifier: "Repeated observation of systems where coherence loss is broadly and evenly distributed across a wide variety of causal events, with no identifiable 'critical few', would falsify the universal applicability of Reverse Pareto Analysis as the core diagnostic method."
      status: supported
      links: [DOMA-033]
naming_notes:
  collisions: [The symbol for Action (S) is also the standard symbol for Entropy. While conceptually related in this context, care must be taken to distinguish Pirouette Action (S_p) from thermodynamic entropy (S_entropy).]
  disambiguation: |
    'Coherence loss' is a precise technical term, not a qualitative synonym for 'poor performance'. It specifically refers to the negative change in a system's total Action, a quantity derived directly from the Pirouette Lagrangian. An underperforming system might have a low but stable Action; a system experiencing coherence loss has a decreasing Action.
crosslinks:
  near_synonyms: []
  antonyms: [MAXIMAL_COHERENCE]
  prerequisites: [ACTION, PIROUETTE_LAGRANGIAN, FRACTAL_BRIDGE]
  downstream_effects: [DECOHERENCE_CASCADE, SYSTEM_FAILURE]
license: CC-BY-SA-4.0
---