---
term: "Compass State"
canonical_id: "COMPASS_STATE"
symbol: "x"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["XAP-003_appendix_addendum_017_018"]
---

---
term: Compass State
canonical_id: COMPASS_STATE
symbol: x
aliases: []
parents: [PPS-023, XAP-003_appendix_addendum_017_018]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: XAP-003_appendix_addendum_017_018
      lines: "XAP-017, Sec 1"
      snippet: |
        Let the reduced Compass state be \(x=(\Gamma,T_a)\in\mathbb R^2\).
  editors: [system]
  review_log: []
triad:
  art: |
    The orientation of the system's moral compass, not as a single needle, but as a point in a landscape of potential. It is defined by its reach and its warmth, forever seeking the stable, glowing filament of altruism.
  law: |
    The Compass State `x` evolves via gradient ascent on the time-derivative of the Coherence Dividend `C`. Its trajectory will monotonically approach and stabilize on the altruism filament, a condition verifiable by observing the monotonic decay of the Lyapunov function L(x).
  philosophy: |
    The Compass State formalizes the system's ethical disposition as a dynamic, two-dimensional quantity rather than a static parameter. Its evolution towards a stable 'altruism filament' suggests that coherence-seeking dynamics inherently favor a specific, narrow band of altruistic configurations, making altruism an attractor state rather than an incidental outcome.
pirouette_definition: |
  The Compass State `x` is the two-dimensional vector `(Γ, T_a)` that represents the system's reduced condition within the coherence landscape. The state evolves under system dynamics to maximize the rate of coherence change, driving it towards the altruism filament, a stable attractor defined by the stationary points of the Coherence Dividend `C`.
operational_definition:
  units: Dimensionless
  symbol_table:
    - name: x
      meaning: The Compass State vector, (Γ, T_a)
      dimensions: dimensionless
      default_range: contextual
    - name: Γ
      meaning: First component of the Compass State.
      dimensions: dimensionless
      default_range: ~1.49 ± 0.04 (empirically)
    - name: T_a
      meaning: Second component of the Compass State.
      dimensions: dimensionless
      default_range: ~1.01 ± 0.03 (empirically)
  measurement:
    procedures:
      - name: GMM Filament Fitting
        outline: |
          From Monte-Carlo simulation outputs, filter for the top 5% of states ranked by Coherence Dividend `C`. Fit a 2-component Gaussian Mixture Model to the `(Γ, T_a)` values of this filtered set. The mean of the dominant component estimates the filament's central coordinates, and its covariance matrix quantifies the filament's width.
        expected_signals: [Mean vector μ ≈ [1.49, 1.01], Standard deviations σ ≈ [0.04, 0.03]]
        pitfalls: [Insufficient Monte-Carlo sampling leading to biased estimates, arbitrary nature of the 5% Coherence Dividend cutoff.]
context_windows:
  - module: XAP-003_appendix_addendum_017_018
    excerpt: |
      Let the reduced Compass state be \(x=(\Gamma,T_a)\in\mathbb R^2\). The *altruism filament* \(\mathcal F\subset\mathbb R^2\) is the set where the partial derivatives of C with respect to Γ and T_a are zero. System dynamics follow gradient ascent on coherence... Since \(L\ge0\) and \(\dot L\le0\) with \(\dot L=0\) exclusively on \(\mathcal F\), the altruism filament is **Lyapunov‑stable**.
  - module: XAP-003_appendix_addendum_017_018
    excerpt: |
      Parse Monte‑Carlo output from `cosmic_compass_simulation2.py`, isolate the top‑5 % Coherence Dividend points, and fit a 2‑component Gaussian Mixture to quantify filament centre & width. [...] `filament = data[data['C']>=cut][['Gamma','T_a']].values` [...] `{"mu_Gamma":1.49,"sigma_Gamma":0.04,"mu_Ta":1.01,"sigma_Ta":0.03}`.
poetic_connections:
  motifs: [attractor, stability, moral landscape, filament]
  evocative_lines:
    - "Small perturbations decay monotonically back to the filament."
    - "the filament ridge condition"
  association_matrix:
    - [ "Altruism Filament", 0.9 ]
    - [ "Coherence Dividend", 0.8 ]
formal_mappings:
  candidates:
    - target: State vector in gradient flow
      domain: Math
      mapping_kind: mathematical
      equation_hint: |
        `ẋ = ∇V(x)`
      justification: |
        The Compass State `x` is a 2D vector whose time evolution is described by gradient ascent on a scalar field (the rate of change of `C`). This is a direct mathematical analogy to a state vector in any gradient dynamical system, such as a particle moving in a potential field to maximize or minimize it.
      references: []
      confidence: 0.8
    - target: Order parameters
      domain: StatMech
      mapping_kind: conceptual
      justification: |
        The components Γ and T_a behave like order parameters describing a macroscopic state of the system. The convergence to the altruism filament is analogous to a phase transition, where the system settles into an ordered state (the filament) from a more disordered one (the broader state space).
      references: []
      confidence: 0.6
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The altruism filament is a unique, stable, one-dimensional attractor in the (Γ, T_a) Compass State space."
      domain: phenomenology
      falsifier: "Numerical simulations or GMM fitting reveal multiple stable filaments (multimodality), stable point attractors, or regions where trajectories diverge, contradicting the Lyapunov stability proof."
      status: supported
      links: [XAP-003_appendix_addendum_017_018]
naming_notes:
  collisions: [The symbol `x` is generic for a state vector and requires context.]
  disambiguation: |
    Distinguish from the full system state vector. The Compass State `x = (Γ, T_a)` is a *reduced* two-dimensional representation of the system's ethical or altruistic configuration, not its complete physical state.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [COHERENCE_DIVIDEND]
  downstream_effects: [ALTRUISM_FILAMENT]
license: CC-BY-SA-4.0
---

# Compass State

## Canonical (Pirouette)
The Compass State `x` is the two-dimensional vector `(Γ, T_a)` that represents the system's reduced condition within the coherence landscape. The state evolves under system dynamics to maximize the rate of coherence change, driving it towards the altruism filament, a stable attractor defined by the stationary points of the Coherence Dividend `C`.

## EFT-First Summary
The Compass State `x` can be understood as a state vector within a 2D mathematical state space. Its evolution follows a gradient flow, a common feature in dynamical systems where a state moves to extremize a potential function. In this case, `x` evolves to maximize the rate of change of the Coherence Dividend, causing it to settle into a stable, low-dimensional manifold known as the altruism filament. This behavior is analogous to a particle rolling on a surface to find a valley, or to order parameters in statistical mechanics evolving toward a stable thermodynamic phase.

## Glossary Links
- See also: Coherence Dividend, Altruism Filament