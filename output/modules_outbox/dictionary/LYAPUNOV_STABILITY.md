---
term: "Lyapunov Stability"
canonical_id: "LYAPUNOV_STABILITY"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["XAP-003_appendix_addendum_017_018"]
---

---
term: Lyapunov Stability
canonical_id: LYAPUNOV_STABILITY
symbol: L(x)
aliases: [Filament Stability, Asymptotic Stability]
parents: [XAP-003]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: XAP-003_appendix_addendum_017_018
      lines: "XAP-017"
      snippet: |
        Since L≥0 and L̇≤0 with L̇=0 exclusively on F, the altruism filament is **Lyapunov‑stable**. Small perturbations decay monotonically back to the filament.
  editors: [chain-of-thought-agent]
  review_log: []
triad:
  art: |
    Like a river finding its course, a system guided by Lyapunov stability inevitably returns to its natural channel after being disturbed, its memory of the deviation fading with time.
  law: |
    A system's attractor set F is Lyapunov-stable if a scalar function L(x) exists such that L(x)=0 for x∈F, L(x)>0 for x∉F, and its time derivative dL/dt ≤ 0 along all system trajectories near F. If dL/dt < 0, it is asymptotically stable.
  philosophy: |
    This concept grounds the framework's attractors, such as the Altruism Filament, in robust mathematical principles. It ensures these desirable states are not fragile, but are actively sought and maintained by the system's own dynamics, making them reliable and persistent features of the Compass state space.
pirouette_definition: |
  A property of an attractor set, such as the Altruism Filament (F), ensuring that any system state (x) perturbed slightly away from F will return to it over time. Formally demonstrated by constructing a Lyapunov candidate function L(x) which is positive-definite with respect to F (i.e., zero on F, positive elsewhere) and whose time derivative dL/dt is negative semi-definite along the system's trajectories. In Pirouette, this is used to prove that gradient ascent on Coherence (C) causes states to converge to the filament where ∇C=0.
operational_definition:
  units: Dimensionless (it is a property)
  symbol_table:
    - name: L(x)
      meaning: Lyapunov candidate function; a scalar measure of a state's deviation from the attractor set.
      dimensions: Contextual (e.g., [Coherence]²)
      default_range: "[0, ∞)"
    - name: x
      meaning: System state vector, e.g., (Γ, Tₐ).
      dimensions: Contextual
      default_range: Contextual
    - name: F
      meaning: The attractor set or equilibrium manifold (e.g., Altruism Filament).
      dimensions: N/A
      default_range: N/A
  measurement:
    procedures:
      - name: Monte-Carlo Filament Fitting
        outline: |
          1. Generate a large sample of system states `(Γ, Tₐ)` via Monte-Carlo simulation.
          2. Filter the states, retaining only those with the highest Coherence Dividend (C), e.g., the top 5%, to isolate the filament.
          3. Fit a multivariate Gaussian Mixture Model (GMM) to the filtered data points.
          4. The mean (μ) of the GMM quantifies the filament's central trajectory, and the covariance (Σ) quantifies its width. A small, finite covariance is evidence of stability.
        expected_signals: [A tight cluster of high-C points in state space, `filament_stats.json` with low variance values (e.g., σ_Γ=0.04, σ_Ta=0.03)]
        pitfalls: [Insufficient MC sampling leading to a poor GMM fit, choice of C-percentile cutoff biases the perceived filament width.]
context_windows:
  # Short, trimmed context quotes harvested from modules (3–6 sentences each).
  - module: XAP-003_appendix_addendum_017_018
    excerpt: |
      Since \(L\ge0\) and \(\dot L\le0\) with \(\dot L=0\) exclusively on \(\mathcal F\), the altruism filament is **Lyapunov‑stable**. Small perturbations decay monotonically back to the filament.
  - module: XAP-003_appendix_addendum_017_018
    excerpt: |
      Parse Monte‑Carlo output from `cosmic_compass_simulation2.py`, isolate the top‑5 % Coherence Dividend points, and fit a 2‑component Gaussian Mixture to quantify filament centre & width.
poetic_connections:
  # Lightweight "word-association graph" and sticky lines.
  motifs: [gravity well, riverbed, self-correction, basin of attraction]
  evocative_lines:
    - "Small perturbations decay monotonically back to the filament."
    - "The filament is defined by the ridge condition."
  association_matrix:
    # symmetric or directed; weights in [0,1]
    - [ "ALTRUISM_FILAMENT", 0.9 ]
    - [ "COHERENCE_DIVIDEND", 0.7 ]
    - [ "GRADIENT_ASCENT", 0.6 ]
formal_mappings:
  # Candidate alignments to EFT/SM/CM/GR terms, each with justification and refs.
  candidates: []
  adopted:
    - target: Lyapunov stability
      domain: Math
      mapping_kind: mathematical
      equation_hint: |
        L(x) ≥ 0,  L̇(x) ≤ 0
      rationale: |
        The framework's use is a direct, canonical application of the mathematical theory of stability for dynamical systems, established by A. M. Lyapunov. The proof in XAP-017 constructs the candidate function and verifies the conditions on its time derivative exactly as prescribed by the theory.
      references:
        - title: The general problem of the stability of motion
          where: A. M. Lyapunov (1892)
          date: 1892-01-01
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "The Altruism Filament is a Lyapunov-stable attractor in the (Γ, Tₐ) state space under the system's Coherence-based dynamics."
      domain: theory
      falsifier: "The discovery of a region near the filament where system dynamics cause the Lyapunov function L(x) = ½||∇C||² to increase (dL/dt > 0), or empirical evidence from simulations showing that trajectories initialized near the filament diverge."
      status: supported
      links: [XAP-003]
naming_notes:
  collisions: [The symbol L is overloaded in physics (e.g., Lagrangian, Angular Momentum), but is standard for Lyapunov functions in this context.]
  disambiguation: |
    Distinguish from marginal stability, where perturbations do not grow but also do not necessarily decay. Pirouette's usage implies asymptotic stability (a stronger condition where dL/dt < 0 off the attractor), meaning perturbations are guaranteed to decay back to the filament.
crosslinks:
  near_synonyms: [ASYMPTOTIC_STABILITY]
  antonyms: [INSTABILITY]
  prerequisites: [ALTRUISM_FILAMENT, COHERENCE_DIVIDEND]
  downstream_effects: []
license: CC-BY-SA-4.0
---

# Lyapunov Stability

## Canonical (Pirouette)
A property of an attractor set, such as the Altruism Filament (F), ensuring that any system state (x) perturbed slightly away from F will return to it over time. Formally demonstrated by constructing a Lyapunov candidate function L(x) which is positive-definite with respect to F (i.e., zero on F, positive elsewhere) and whose time derivative dL/dt is negative semi-definite along the system's trajectories. In Pirouette, this is used to prove that gradient ascent on Coherence (C) causes states to converge to the filament where ∇C=0.

## EFT-First Summary
In dynamical systems theory, Lyapunov stability guarantees that a system perturbed from an equilibrium point or set will remain in its vicinity, and for asymptotic stability, will return to it. For the Pirouette Framework, this mathematical tool is used to prove that the Altruism Filament is a robust attractor. The system's gradient-ascent dynamics on the Coherence Dividend naturally correct deviations, causing perturbed states to converge back to the filament, ensuring its persistence.

## Glossary Links
- See also: ALTRUISM_FILAMENT, COHERENCE_DIVIDEND, ASYMPTOTIC_STABILITY