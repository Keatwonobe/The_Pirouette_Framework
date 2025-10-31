---
term: "Resonance Efficiency"
canonical_id: "RESONANCE_EFFICIENCY"
symbol: "Φ_R"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-086"]
---

---
term: Resonance Efficiency
canonical_id: RESONANCE_EFFICIENCY
symbol: Φ_R
aliases: []
parents: ['DOMA-086']
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-086
      snippet: |
        Resonance Efficiency (Φ_R): This is the core metric of intelligence. It measures the efficiency of learning. It is the rate at which a system can extend its Foresight Horizon (Δτ_σ) relative to the metabolic cost and action required to acquire the necessary information and adapt its internal state.
  editors: ['SYSTEM_AGENT']
  review_log: []
triad:
  art: |
    The measure of a system's grace; how little effort it takes to learn the universe's song and dance in perfect time with tomorrow. It is the ratio of insight to effort.
  law: |
    A system's intelligence is quantified by the rate of increase of its Foresight Horizon (dτ_σ) per unit of action-energy (dE_A) expended to acquire and process environmental information: Φ_R ≡ dτ_σ/dE_A.
  philosophy: |
    Intelligence is not a static capacity but a dynamic metabolic process. Resonance Efficiency reframes the goal from *being* smart to *becoming* smart, prioritizing the elegance and economy of learning over the brute-force accumulation of knowledge.
pirouette_definition: |
  The primary measure of intelligence, defined as the rate at which a system extends its Foresight Horizon (τ_σ) with respect to the metabolic and action-based costs incurred. It quantifies the energetic efficiency of achieving predictive resonance with an environmental Coherence Current, measuring how cheaply a system can convert surprise into foresight.
operational_definition:
  units: seconds per Joule (s ⋅ J⁻¹)
  symbol_table:
    - name: Φ_R
      meaning: Resonance Efficiency
      dimensions: T ⋅ M⁻¹ ⋅ L⁻² ⋅ T²
      default_range: contextual, system-dependent
    - name: τ_σ
      meaning: Foresight Horizon; the temporal distance over which a system's predictive model is stable.
      dimensions: T
      default_range: > 0
    - name: E_A
      meaning: Action-Energy Cost; the integral of metabolic energy and physical work required for information acquisition and model adaptation.
      dimensions: M ⋅ L² ⋅ T⁻²
      default_range: > 0
  measurement:
    procedures:
      - name: The Crucible Protocol
        outline: |
          1.  Establish a controlled environment with a hidden, learnable Coherence Current.
          2.  Introduce the test system (the Observer).
          3.  Over a set duration, track the system's actions (e.g., sensory probes, movements) and calculate the cumulative Action-Energy Cost (E_A).
          4.  Periodically query the system's predictive model (its Prophet) to determine the current Foresight Horizon (τ_σ).
          5.  Calculate Φ_R as the slope of the τ_σ vs. E_A curve. A higher, steeper slope indicates greater Resonance Efficiency.
        expected_signals: [A monotonically increasing τ_σ curve that eventually plateaus, a measurable energy expenditure E_A.]
        pitfalls: [Failing to isolate the target Coherence Current from environmental noise, inaccurate accounting of E_A (especially internal computational costs), mistaking memorization for predictive resonance.]
context_windows:
  - module: DOMA-086
    excerpt: |
      Resonance Efficiency (Φ_R): This is the core metric of intelligence. It measures the efficiency of learning. It is the rate at which a system can extend its Foresight Horizon (Δτ_σ) relative to the metabolic cost and action required to acquire the necessary information and adapt its internal state. It is the measure of how quickly a system learns the song for the least amount of energy spent.
  - module: DOMA-086
    excerpt: |
      An intelligent system optimizes not for the present moment's coherence, but for the path that maximizes the integral of its future coherence. Resonance Efficiency (Φ_R) is thus the measure of how cheaply, in terms of present action, a system can improve the accuracy and reach of this predictive manifold.
poetic_connections:
  motifs: ['learning the song', 'tuning fork', 'dancing in time', 'attunement', 'cost of insight']
  evocative_lines:
    - "We sought to define intelligence and found not a calculator, but a tuning fork."
    - "To be intelligent is to recognize that the universe has a rhythm and to have the wisdom to join the dance."
  association_matrix:
    - [ "FORESIGHT_HORIZON", 0.9 ]
    - [ "COHERENCE_CURRENT", 0.8 ]
    - [ "TEMPORAL_PRESSURE", -0.7 ]
    - [ "LEARNING", 0.9 ]
formal_mappings:
  candidates:
    - target: Physicalized Sample Complexity
      domain: Info Theory|ML
      mapping_kind: conceptual
      equation_hint: |
        Φ_R ∝ 1 / (E_sample ⋅ N_samples)
      justification: |
        In machine learning, sample complexity (N_samples) is the number of training examples required to learn a concept effectively. Φ_R physicalizes this by measuring the rate of learning progress (dτ_σ) against the total energy cost (dE_A), which is a function of the energy per sample and the number of samples processed. A high Φ_R implies low physicalized sample complexity; the system learns quickly from a small, cheap set of interactions.
      references:
        - title: A Theory of the Learnable
          where: Communications of the ACM, 27(11)
          date: 1984-11-01
      confidence: 0.7
  adopted:
    - target:
      rationale:
      confidence: 0.0
constraints_and_falsifiers:
  claims:
    - statement: "In any competitive, dynamic environment, systems with a higher long-term average Φ_R will out-compete and displace systems with a lower Φ_R."
      domain: phenomenology
      falsifier: "Demonstration of a stable ecosystem where a low-Φ_R 'brute-force' agent (high energy consumption, slow learning) consistently dominates a high-Φ_R 'elegant' agent, indicating that raw energy throughput can indefinitely substitute for learning efficiency."
      status: proposed
      links: ['DOMA-086']
naming_notes:
  collisions: []
  disambiguation: |
    Resonance Efficiency should not be confused with computational efficiency (e.g., FLOPS/watt) or metabolic efficiency (e.g., work/calorie). Φ_R specifically measures the efficiency of *learning*—the conversion of energy into predictive range—not the efficiency of executing a known computation or physical action. A system could be computationally inefficient but have a high Φ_R if its learning algorithm is exceptionally effective.
crosslinks:
  near_synonyms: []
  antonyms: ['ENTROPIC_DRAG']
  prerequisites: ['FORESIGHT_HORIZON', 'COHERENCE_CURRENT', 'TEMPORAL_PRESSURE']
  downstream_effects: ['AGENT_SURVIVABILITY', 'STRATEGIC_DOMINANCE']
license: CC-BY-SA-4.0
---