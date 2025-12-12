---
term: "Attractor Prior"
canonical_id: "ATTRACTOR_PRIOR"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["XAP-004_appendix_addendum_A_through_L"]
---

---
term: Attractor Prior
canonical_id: ATTRACTOR_PRIOR
symbol: P(Nₐ)
aliases: []
parents: ['PPS-042']
children: []
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: XAP-004_appendix_addendum_A_through_L
      snippet: |
        Annex F – Attractor Prior Annex
        Derived from catastrophe-map topology.
        * Upper bound N_a ≤ 4 (cusp surface).
        * Prior distribution P(N_a=k) uniform for k ∈ {1,2,3,4} absent domain-specific symmetry.
        * Dataset-specific update: Bayesian posterior once first Fork dataset logged.
  editors: ['System Agent']
  review_log: []
triad:
  art: |
    The landscape of possibility has its valleys, but not an infinite number. Before we look, we assume a handful of resting places, a small count of destinies carved by the universal folds of change.
  law: |
    The prior probability P(Nₐ=k) for a system having k stable attractors is a discrete uniform distribution over k ∈ {1, 2, 3, 4}, unless overridden by domain-specific symmetries. This prior is subject to Bayesian update upon observation.
  philosophy: |
    The Attractor Prior codifies a principle of parsimony for system complexity, grounding inference in the finite, structured possibilities dictated by catastrophe theory. It asserts that complex systems default to a small, enumerable set of stable configurations, preventing over-fitting to noise before sufficient data is gathered.
pirouette_definition: |
  A discrete, uniform probability distribution over the number of stable attractors (Nₐ) in a system, where P(Nₐ=k) = 0.25 for k ∈ {1, 2, 3, 4}. It serves as a Bayesian prior, derived from the topological constraint that a cusp catastrophe surface has at most four stable minima. The prior is updated to a posterior distribution as system state data becomes available, typically after a Fork event.
operational_definition:
  units: dimensionless
  symbol_table:
    - name: Nₐ
      meaning: Number of stable system attractors.
      dimensions: dimensionless
      default_range: "{1, 2, 3, 4}"
    - name: P(Nₐ)
      meaning: Prior probability distribution over Nₐ.
      dimensions: dimensionless
      default_range: "[0, 1]"
  measurement:
    procedures:
      - name: Bayesian Inference via State-Space Mapping
        outline: |
          1. Institute the default uniform prior: P(Nₐ=k) = 0.25 for k∈{1,2,3,4}.
          2. Collect time-series data of core system state variables (e.g., Γ, Ki).
          3. Cluster the terminal states of system trajectories to identify stable points (attractors). The number of distinct, dense clusters is the observation.
          4. Compute a likelihood function P(data|Nₐ) based on the clarity and separation of the observed clusters.
          5. Combine the prior and likelihood to calculate the posterior distribution P(Nₐ|data).
        expected_signals: ['Clustering of state-space trajectories into N ≤ 4 distinct regions.']
        pitfalls: ['Insufficiently long trajectories failing to reach an attractor.', 'Observational noise obscuring cluster boundaries.', 'System dynamics governed by a higher-order catastrophe (e.g., butterfly) not bounded by Nₐ ≤ 4.']
context_windows:
  - module: XAP-004_appendix_addendum_A_through_L
    excerpt: |
      Derived from catastrophe-map topology. Upper bound N_a ≤ 4 (cusp surface). Prior distribution P(N_a=k) uniform for k ∈ {1,2,3,4} absent domain-specific symmetry. Dataset-specific update: Bayesian posterior once first Fork dataset logged.
  - module: PPS-042
    excerpt: |
      Inference on the Fork dataset requires a well-defined prior over the system's structural parameters. The Attractor Prior (see Annex F) provides the necessary starting point for the number of expected stable states, Nₐ. This prevents the model from hypothesizing an excessive number of attractors from noisy initial data, constraining the search space for the resonance mapper.
poetic_connections:
  motifs: ["finite states", "catastrophe", "potential landscape", "Bayesian learning", "destiny"]
  evocative_lines:
    - "A small count of destinies carved by the universal folds of change."
    - "The landscape of possibility has its valleys, but not an infinite number."
  association_matrix:
    - [ "CATASTROPHE_MAP", 0.9 ]
    - [ "FORK", 0.8 ]
    - [ "RESONANCE", 0.5 ]
formal_mappings:
  candidates:
    - target: Number of minima of a potential function V(x; c₁, c₂)
      domain: Math
      mapping_kind: mathematical
      equation_hint: |
        V(x) = x⁴ + c₂x² + c₁x
      justification: |
        The Pirouette Attractor Prior directly adopts the result from cusp catastrophe theory that the potential function V(x) has at most four local minima, which correspond to the system's stable attractors. The number of minima changes as control parameters (c₁, c₂) are varied across the bifurcation set.
      references:
        - title: Catastrophe Theory
          where: V.I. Arnold, Springer (1984)
          date: 1984-01-01
      confidence: 0.95
  adopted:
    - target: Number of minima of a cusp catastrophe potential.
      rationale: "The derivation is explicitly stated in Annex F of XAP-004. This mapping provides a rigorous mathematical foundation for the prior, connecting it to the study of bifurcations and structural stability in dynamical systems."
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The number of stable system attractors, Nₐ, will not exceed 4."
      domain: phenomenology
      falsifier: "Repeatable observation of a system robustly settling into 5 or more distinct stable states under varying initial conditions. Such a finding would imply the underlying dynamics are governed by a higher-order catastrophe (e.g., butterfly, Nₐ ≤ 6) and would require revising the prior."
      status: proposed
      links: ['XAP-004_appendix_addendum_A_through_L']
naming_notes:
  collisions: ['P(N) is a generic probability notation. In context, Nₐ should be used to specify the number of *attractors*.']
  disambiguation: |
    Distinguish from priors on other parameters (e.g., Γ_thr Prior). The Attractor Prior is specifically about the *cardinality* of the set of stable states, not the properties or values associated with those states.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: ['CATASTROPHE_MAP']
  downstream_effects: ['FORK_ANALYSIS', 'BAYESIAN_STATE_ESTIMATION']
license: CC-BY-SA-4.0
---

# Attractor Prior

## Canonical (Pirouette)
A discrete, uniform probability distribution over the number of stable attractors (Nₐ) in a system, where P(Nₐ=k) = 0.25 for k ∈ {1, 2, 3, 4}. It serves as a Bayesian prior, derived from the topological constraint that a cusp catastrophe surface has at most four stable minima. The prior is updated to a posterior distribution as system state data becomes available, typically after a Fork event.

## EFT-First Summary
The Attractor Prior is a uniform distribution P(Nₐ=k) for k∈{1,2,3,4} on the number of stable system states. This is a direct application of Cusp Catastrophe Theory, where Nₐ maps to the number of minima in the potential V(x) = x⁴ + c₂x² + c₁x. This provides a principled, low-information starting point for Bayesian inference of system structure, analogous to setting a non-informative prior in statistical field theory.

## Glossary Links
- See also: [Γ_thr Prior](...), [Fork](...), [Resonance](...)