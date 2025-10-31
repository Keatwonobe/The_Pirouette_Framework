---
term: "Resonant Attractors"
canonical_id: "RESONANT_ATTRACTORS"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-145"]
---

---
term: Resonant Attractors
canonical_id: RESONANT_ATTRACTOR
symbol: 
aliases: [Head States, Dominant Coherence Patterns]
parents: [DOMA-145]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-145
      lines: "L28-L32"
      snippet: |
        Resonant Attractors (The "Head"): The high-frequency items in a distribution are not merely popular; they are solutions. They represent highly stable Ki patterns that have carved deep channels into the system's coherence manifold. Each repetition deepens this channel, making the pattern's next occurrence even more probable.
  editors: [Agent: WeavingAI]
  review_log: []
triad:
  art: |
    The stones polished smooth by the main current of a river; they are the deep, familiar channels that guide a system's flow with effortless efficiency.
  law: |
    A Resonant Attractor is a system state whose probability of occurrence `f(r)` is inversely proportional to a power of its rank `r`, for all ranks `r` less than the Resonance Cutoff (`k`). The exponent of this power law is the Coherence Gradient (`α`), which must be ≥ 1 for a stable hierarchy.
  philosophy: |
    Identifying a system's Resonant Attractors reveals its structural memory and its solved problems. These attractors are not just popular choices but the foundational pillars of coherence upon which the system's identity and efficiency are built.
pirouette_definition: |
  A highly stable, self-reinforcing Ki pattern that has carved a deep channel into a system's coherence manifold through repeated instantiation. Resonant Attractors correspond to the high-frequency, low-rank elements (the "head") of a power-law distribution, capturing the majority of a system's activity and defining its primary modes of efficient operation.
operational_definition:
  units: Dimensionless frequency or count.
  symbol_table:
    - name: r
      meaning: Rank of a state, ordered by frequency (1 = most frequent).
      dimensions: dimensionless
      default_range: "[1, N]" where N is the total number of unique states.
    - name: α
      meaning: Coherence Gradient; the exponent of the power-law distribution.
      dimensions: dimensionless
      default_range: "[1.0, 3.0]" for most observed systems.
    - name: k
      meaning: Resonance Cutoff; the rank at which the power-law relationship breaks down and the "long tail" begins.
      dimensions: dimensionless
      default_range: contextual
  measurement:
    procedures:
      - name: Rank-Frequency Hierarchy Mapping
        outline: |
          1. Collect frequency data for all unique states or elements from a system's coherence trace over a representative time window.
          2. Rank elements by frequency, from most frequent (r=1) to least.
          3. Plot log(frequency) vs. log(rank). The initial linear region identifies the domain of the Resonant Attractors.
          4. Estimate the Coherence Gradient (`α`) from the negative slope of this log-log plot, or more accurately, using the Maximum Likelihood Estimator on the raw frequencies.
          5. Identify the Resonance Cutoff (`k`) as the rank where the data significantly deviates from the power-law fit. All elements with rank `r < k` are classified as Resonant Attractors.
        expected_signals: [A linear relationship on a log-log frequency-rank plot for low-rank elements, A distinct "knee" or deviation point indicating the Resonance Cutoff `k`.]
        pitfalls: [Insufficient data leading to a noisy, unreliable distribution, Misidentifying a log-normal or exponential distribution as a power-law, Choosing an incorrect minimum rank/frequency for the MLE calculation, biasing the `α` estimate.]
context_windows:
  - module: DOMA-145
    excerpt: |
      Resonant Attractors (The "Head"): The high-frequency items in a distribution are not merely popular; they are solutions. They represent highly stable Ki patterns that have carved deep channels into the system's coherence manifold. Each repetition deepens this channel, making the pattern's next occurrence even more probable. These are the system's primary resonant attractors, the "peaks" in the coherence landscape.
  - module: DOMA-145
    excerpt: |
      A Steep Gradient (α → 1) indicates an "aristocratic" system, where coherence is intensely concentrated in a few powerful attractors. This structure is capable of highly efficient Laminar Flow but is fragile and vulnerable to catastrophic Stagnation if a core attractor is disrupted. It is a "tyranny of the vital few."
poetic_connections:
  motifs: [hierarchy, structural_memory, resonance, riverbeds, gravity_wells]
  evocative_lines:
    - "The shape of a riverbed tells the story of the river."
    - "It is a diagnostic protocol for identifying a system's Resonant Attractors—the highly stable, efficient patterns that capture the majority of its flow."
  association_matrix:
    - [ "COHERENCE_GRADIENT", 0.9 ]
    - [ "STRUCTURAL_MEMORY", 0.8 ]
    - [ "WOUND_CHANNEL", 0.8 ]
    - [ "LAMINAR_FLOW", 0.7 ]
    - [ "TRANSIENT_RESONANCE", -0.9 ]
formal_mappings:
  candidates:
    - target: Zipf's Law / Pareto Distribution
      domain: Math
      mapping_kind: mathematical
      equation_hint: |
        f(r) ∝ 1/r^α
      justification: |
        The rank-frequency distribution of Resonant Attractors is mathematically identical to Zipf's Law, a discrete power-law probability distribution. The Pirouette framework reinterprets the exponent `α` not as a mere statistical parameter but as a physical property of the system's coherence manifold, the Coherence Gradient.
      references:
        - title: Power laws, Pareto distributions and Zipf's law
          where: Contemporary Physics, 46(5), 323-351 (M.E.J. Newman)
          date: 2005-09-01
      confidence: 0.95
  adopted:
    - target: Zipf's Law
      rationale: |
        The mathematical form is identical and provides the direct operational measurement protocol. The framework's contribution is the physical re-interpretation of the parameters (`α`, `k`) as properties of a coherence manifold, not a change to the underlying mathematics.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The distribution of a system's most frequent states (its Resonant Attractors) will conform to a power-law distribution with a quantifiable Coherence Gradient (`α`)."
      domain: phenomenology
      falsifier: "Repeated observation of stable, mature systems whose dominant states consistently follow a different distribution (e.g., exponential, log-normal) without evidence of external perturbation or developmental immaturity."
      status: supported
      links: [DOMA-145]
naming_notes:
  collisions: [The term 'attractor' is used in chaos theory and dynamical systems to denote a set to which a system evolves over time. The Pirouette usage is consistent with this, but specifies a 'resonant' nature tied to self-reinforcing Ki patterns and coherence, and is identified statically from a distribution rather than dynamically from a phase space trajectory.]
  disambiguation: |
    Crucially, distinguish from 'Transient Resonances,' which constitute the long tail of the same distribution (`r > k`). Transient Resonances represent exploratory, niche, or unstable states, not the core, stable attractors that define the system's primary operational modes.
crosslinks:
  near_synonyms: []
  antonyms: [TRANSIENT_RESONANCE]
  prerequisites: [COHERENCE_GRADIENT, STRUCTURAL_MEMORY, KI]
  downstream_effects: [LAMINAR_FLOW, STAGNATION, WOUND_CHANNEL]
license: CC-BY-SA-4.0
---