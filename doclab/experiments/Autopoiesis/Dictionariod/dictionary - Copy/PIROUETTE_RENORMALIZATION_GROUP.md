---
term: "Pirouette Renormalization Group"
canonical_id: "PIROUETTE_RENORMALIZATION_GROUP"
symbol: "PRG"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["CORE-015_the_fractal_at_the_heart_of_time"]
---

---
term: Pirouette Renormalization Group
canonical_id: PIROUETTE_RENORMALIZATION_GROUP
symbol: PRG
aliases: [Scale Dynamics]
parents: [CORE-015]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: CORE-015_the_fractal_at_the_heart_of_time
      lines: "L20-L26"
      snippet: |
        * **Claim:** The predictive content of Pirouette is a *scale dynamics*:
          [
          \frac{d}{ds}
          \begin{pmatrix}
          K_\tau\ V_\Gamma\ \tau_p
          \end{pmatrix}
          =============

          \begin{pmatrix}
          \beta_K(K_\tau,V_\Gamma)[2pt]
          \beta_\Gamma(K_\tau,V_\Gamma)[2pt]
          \beta_\tau(K_\tau,V_\Gamma),\tau_p
          \end{pmatrix},\qquad s\equiv\ln L.
          ]
  editors: [Pirouette-Agent]
  review_log: []
triad:
  art: |
    A pirouette seen from afar is a simple spin, but zooming in reveals the intricate play of muscle, balance, and momentum. The PRG is the score for this dance across scales, revealing the hidden self-similarity in the flow of time and information. It is the fractal engine at the heart of coherent systems.
  law: |
    The rate of change of a system's core properties (Coherence `K_τ`, Pressure `V_Γ`, Pulse `τ_p`) with respect to logarithmic scale (`s = ln L`) is a function of those properties themselves. This flow, described by β-operators, drives the system towards scale-invariant fixed points, which define its macroscopic phase.
  philosophy: |
    A system's nature is not found at any single scale but in the rules governing how its properties transform *between* scales. The PRG provides these rules, asserting that coherent, generalizable systems must obey a consistent scaling story. By enforcing this consistency, we can build models and theories that generalize rather than memorize, maintaining their integrity across all contexts.
pirouette_definition: |
  A mathematical framework consisting of a set of coupled, first-order differential equations that describe the evolution of a system's primary observables—Coherence (`K_τ`), Pressure (`V_Γ`), and Pulse (`τ_p`)—as a function of observational scale (`L`). The framework is defined by the β-operators, which act as vector fields in the space of observables, and their fixed points, which correspond to the stable, scale-invariant phases of the system (e.g., laminar, turbulent). The exponents governing the flow near these fixed points are predicted to be universal.
operational_definition:
  units: Dimensionless flow equations. The scale parameter `s` is dimensionless. `K_τ` is measured in bits (information), `V_Γ` is context-dependent (e.g., (signal units)²), and `τ_p` is in units of time or samples.
  symbol_table:
    - name: PRG
      meaning: Pirouette Renormalization Group; the framework itself.
      dimensions: N/A
      default_range: N/A
    - name: s
      meaning: Logarithmic scale parameter, `s ≡ ln L`.
      dimensions: dimensionless
      default_range: `(-inf, inf)`
    - name: L
      meaning: Characteristic length/time/information scale of observation.
      dimensions: contextual (T, L, etc.)
      default_range: `(0, inf)`
    - name: `K_τ`
      meaning: Coherence; information-theoretic self-similarity at scale L.
      dimensions: Information (bits)
      default_range: `[0, inf)`
    - name: `V_Γ`
      meaning: Pressure; environmental drive or fluctuation amplitude at scale L.
      dimensions: contextual
      default_range: `[0, inf)`
    - name: `τ_p`
      meaning: Pulse; dominant period or characteristic timescale at scale L.
      dimensions: Time or Samples
      default_range: `(0, inf)`
    - name: `β_X`
      meaning: Beta operator for observable X; describes `dX/ds`.
      dimensions: Same as X
      default_range: contextual
  measurement:
    procedures:
      - name: PRG Inference via Finite Differences
        outline: |
          1. Select a signal or system dataset and define a set of increasing observational windows/scales `L_0, L_1, ..., L_n`.
          2. For each scale `L_i`, compute the observables: `K_τ(L_i)` via compressibility, `V_Γ(L_i)` via driven variance, and `τ_p(L_i)` via spectral analysis.
          3. Approximate the derivative `d(observable)/ds` for each interval using the finite difference: `[X(L_{i+1}) - X(L_i)] / [ln(L_{i+1}) - ln(L_i)]`.
          4. Fit the resulting data points (`X_i`, `dX/ds|_i`) to the posited polynomial forms of the `β`-operators to estimate the universal exponents and coupling parameters (e.g., `d_K, d_Γ, φ, ψ`).
        expected_signals: [Time-series data, token sequences, spatial data (images/volumes)]
        pitfalls: [Insufficient scale separation between `L_i` and `L_{i+1}`, noisy observable estimates at small/large scales, model misspecification of the β-operator form.]
context_windows:
  - module: CORE-015_the_fractal_at_the_heart_of_time
    excerpt: |
      We posit minimal polynomial β’s near fixed points:
      [
      \beta_K = d_K K_\tau - \phi,V_\Gamma K_\tau - \eta K_\tau^3,\quad
      \beta_\Gamma = d_\Gamma V_\Gamma - \psi K_\tau V_\Gamma,\quad
      \beta_\tau = \zeta_\Gamma V_\Gamma - \zeta_K K_\tau.
      ]
      Predictions: (i) Scaling laws: (K_\tau\sim L^{d_K^*}), (V_\Gamma\sim L^{d_\Gamma^*}). (ii) Beat dilation: (\tau_p\sim L^{\zeta_\Gamma d_\Gamma^* - \zeta_K d_K^*}.)
  - module: CORE-015_the_fractal_at_the_heart_of_time
    excerpt: |
      Given model predictions (\hat x) over a horizon and multiscale features (\mathcal F_L(\hat x)), define
      [
      \mathcal L_{\text{pirouette}} = -\underbrace{\Delta K_\tau}_{\text{coherence gain}}
      
      * \lambda_\Gamma\underbrace{,V_\Gamma}_{\text{pressure cost}}
      * \lambda_\tau\underbrace{,\big(\partial_s\ln\tau_p - (\zeta_\Gamma V_\Gamma - \zeta_K K_\tau)\big)^2}_{\text{PRG beat consistency}}
      * \lambda_{\rm task},\mathcal L_{\rm task}.
      ]
      Interpretation: maximize compressive structure while minimizing environmental friction and enforcing PRG-consistent beat scaling.
poetic_connections:
  motifs: [fractal, scaling, hierarchy, self-similarity, flow, fixed point, universality]
  evocative_lines:
    - "The Fractal at the Heart of Time."
    - "...baking it into AI objectives yields models that keep their story straight across scales—and that’s where generalization lives."
  association_matrix:
    - [ "COHERENCE_K_TAU", 0.9 ]
    - [ "PRESSURE_V_GAMMA", 0.9 ]
    - [ "FIXED_POINT", 0.8 ]
    - [ "WOUND_CHANNEL", 0.5 ]
formal_mappings:
  candidates:
    - target: Renormalization Group (RG) flow
      domain: EFT|StatMech
      mapping_kind: mathematical
      equation_hint: |
        `d g_i / d(ln μ) = β_i(g_1, g_2, ...)`
      justification: |
        The PRG is a direct generalization of the Wilsonian Renormalization Group. It replaces physical coupling constants (`g_i`) and energy scale (`μ`) with Pirouette's information-theoretic observables (`K_τ`, `V_Γ`) and observational scale (`L`). The mathematical structure, a set of coupled differential equations describing flow towards scale-invariant fixed points, is identical.
      references:
        - title: The renormalization group and the ε expansion
          where: Physics Reports, 12(2), 75-199
          date: 1974-06-01
      confidence: 0.95
  adopted:
    - target: Renormalization Group (RG) flow
      rationale: The name, mathematical form, and conceptual purpose (describing physics across scales) are a direct and intentional mapping. PRG is RG applied to Pirouette's ontology.
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "Systems belonging to the same PRG universality class will exhibit identical scaling exponents (`d_K*`, `d_Γ*`, Jacobian eigenvalues `λ_i`) at their critical fixed points, regardless of their microscopic implementation details."
      domain: phenomenology
      falsifier: "Demonstrating two systems that flow to the same PRG fixed point (e.g., the turbulent saddle) but which consistently yield statistically different critical exponents when measured."
      status: proposed
      links: [CORE-015]
naming_notes:
  collisions: [RG]
  disambiguation: |
    Distinguish from the conventional Renormalization Group (RG) in quantum field theory and statistical mechanics. While mathematically isomorphic, PRG operates on information-theoretic observables (`K_τ`, `V_Γ`) derived from arbitrary signals or systems, not just physical coupling constants. PRG is a generalization of the RG concept, not a direct application to a specific physical Lagrangian.
crosslinks:
  near_synonyms: []
  antonyms: [SINGLE_SCALE_ANALYSIS]
  prerequisites: [COHERENCE_K_TAU, PRESSURE_V_GAMMA, PULSE_TAU_P]
  downstream_effects: [COHERENCE_AI, PRG_FIXED_POINT]
license: CC-BY-SA-4.0
---

# Pirouette Renormalization Group

## Canonical (Pirouette)
A mathematical framework consisting of a set of coupled, first-order differential equations that describe the evolution of a system's primary observables—Coherence (`K_τ`), Pressure (`V_Γ`), and Pulse (`τ_p`)—as a function of observational scale (`L`). The framework is defined by the β-operators, which act as vector fields in the space of observables, and their fixed points, which correspond to the stable, scale-invariant phases of the system (e.g., laminar, turbulent). The exponents governing the flow near these fixed points are predicted to be universal.

## EFT-First Summary
The Pirouette Renormalization Group (PRG) is a direct application of the Renormalization Group (RG) formalism from effective field theory and statistical mechanics. Instead of tracking how physical coupling constants `g_i` flow with changing energy scale `μ`, the PRG tracks how the Pirouette observables `K_τ` (Coherence) and `V_Γ` (Pressure) flow with changing observational length scale `L`. The core equations `d(Observable)/d(ln L) = β(Observables)` are structurally identical to standard RG equations, and the resulting fixed points and universal scaling exponents are interpreted as the stable, macroscopic phases of the system.

## Glossary Links
- See also: COHERENCE_K_TAU, PRESSURE_V_GAMMA, PRG_FIXED_POINT