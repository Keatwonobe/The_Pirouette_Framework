---
term: "Lyapunov Candidate"
canonical_id: "LYAPUNOV_CANDIDATE"
symbol: "L"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["XAP-003_appendix_addendum_017_018"]
---

---
term: Lyapunov Candidate
canonical_id: LYAPUNOV_CANDIDATE
symbol: L
aliases: []
parents: [XAP-003]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: XAP-003_appendix_addendum_017_018
      lines: "XAP-017 Sec 2"
      snippet: |
        Define

        $$
        L(x)=\tfrac12\bigl(\tfrac{\partial C}{\partial\Gamma}\bigr)^2+\tfrac12\bigl(\tfrac{\partial C}{\partial T_a}\bigr)^2 \;\ge0.
        $$

        Clearly \(L(x)=0\iff x\in\mathcal F\).
  editors: [Agent-Writer]
  review_log: []
triad:
  art: |
    A potential well carved into the state space, whose every slope guides the Compass back to the filament of altruism. It measures the "tension" of a state, an energy that always seeks to resolve itself toward a stable equilibrium.
  law: |
    A scalar function `L(x)` of the system state `x` is a Lyapunov Candidate for an equilibrium set `F` if `L(x) >= 0` for all `x`, `L(x) = 0` if and only if `x` is in `F`, and the time derivative `dL/dt <= 0` along system trajectories near `F`.
  philosophy: |
    This formalizes the concept of intrinsic stability. It provides a rigorous, non-simulative guarantee that the Altruism Filament is not a transient artifact but a fundamental, attractive feature of the Compass dynamics, ensuring that deviations are self-correcting.
pirouette_definition: |
  A scalar function `L` of the reduced Compass state `x = (Γ, T_a)` defined as half the sum of squared partial derivatives of Coherence `C` with respect to the state variables. `L` is constructed to be non-negative and to vanish only on the altruism filament `F`. Its time derivative along system trajectories is proven to be non-positive, providing a formal proof of the Lyapunov stability of the filament.
operational_definition:
  units: dimensionless
  symbol_table:
    - name: L
      meaning: Lyapunov Candidate value
      dimensions: dimensionless
      default_range: "[0, ∞)"
    - name: x
      meaning: Reduced Compass State vector (Γ, T_a)
      dimensions: dimensionless
      default_range: contextual
    - name: C
      meaning: Coherence Dividend
      dimensions: dimensionless
      default_range: contextual
    - name: F
      meaning: The Altruism Filament, a set in state space
      dimensions: dimensionless
      default_range: contextual
  measurement:
    procedures:
      - name: Computational Stability Verification
        outline: |
          1.  Define a grid over the `(Γ, T_a)` state space.
          2.  Numerically compute the Coherence `C` and its partial derivatives `∂C/∂Γ` and `∂C/∂T_a` at each grid point.
          3.  Construct the scalar field `L(x)` from the squared derivatives.
          4.  Numerically compute the system dynamics `ẋ` (i.e., the Hessian of `C`).
          5.  Compute the time derivative `dL/dt = ∇L ⋅ ẋ` at each grid point.
          6.  Verify that `L(x) >= 0` and `dL/dt <= 0` across the domain.
        expected_signals:
          - A scalar field `L(Γ, T_a)` forming a valley centered on the altruism filament.
          - A scalar field `dL/dt(Γ, T_a)` that is zero on the filament and negative elsewhere.
        pitfalls:
          - Insufficient grid resolution can miss fine-structured instabilities.
          - Numerical errors in calculating second-order derivatives (the Hessian) for the dynamics.
context_windows:
  - module: XAP-003_appendix_addendum_017_018
    excerpt: |
      Let the reduced Compass state be \(x=(\Gamma,T_a)\in\mathbb R^2\). The *altruism filament* \(\mathcal F\subset\mathbb R^2\) is the set where the gradient of Coherence is zero. Define the Lyapunov Candidate \(L(x)=\tfrac12\bigl(\tfrac{\partial C}{\partial\Gamma}\bigr)^2+\tfrac12\bigl(\tfrac{\partial C}{\partial T_a}\bigr)^2 \;\ge0\). Clearly \(L(x)=0\iff x\in\mathcal F\).
  - module: XAP-003_appendix_addendum_017_018
    excerpt: |
      Since \(L\ge0\) and \(\dot L\le0\) with \(\dot L=0\) exclusively on \(\mathcal F\), the altruism filament is **Lyapunov‑stable**. Small perturbations decay monotonically back to the filament.
poetic_connections:
  motifs: [stability, potential well, self-correction, attractor, basin]
  evocative_lines:
    - "Small perturbations decay monotonically back to the filament."
    - "the second‑directional derivative... by filament ridge condition."
  association_matrix:
    - [ "ALTRUISM_FILAMENT", 0.9 ]
    - [ "COHERENCE_DIVIDEND", 0.8 ]
    - [ "COMPASS_STATE", 0.6 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Lyapunov function V(x)
      domain: Math (Dynamical Systems Theory)
      mapping_kind: mathematical
      equation_hint: |
        Given ẋ = f(x), V(x) > 0 for x ≠ xₑ, V(xₑ)=0, and dV/dt ≤ 0.
      justification: |
        The function `L` is constructed to satisfy the conditions of Lyapunov's second method for stability. It acts as a generalized energy function for the system that is shown to be non-increasing over time, proving that the system state converges to the set where `L` is at its minimum (the altruism filament).
      references:
        - title: Nonlinear Systems, 3rd ed.
          where: "Hassan K. Khalil, Chapter 4"
          date: 2002-01-01
      rationale: The term is a direct application of the mathematical concept to the Pirouette framework. No other mapping is as precise or accurate.
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "The function `L(x)` decreases monotonically for all system trajectories not on the altruism filament `F`."
      domain: theory
      falsifier: "Discovery of a region in state space where the filament ridge condition (`∂²C/∂n² < 0`) is violated. This would permit `dL/dt > 0`, indicating instability."
      status: supported
      links: [XAP-003]
naming_notes:
  collisions: [L (Lagrangian)]
  disambiguation: |
    Distinguish from the Lagrangian, also often denoted `L`. The Lyapunov Candidate `L` is a function of state variables used to prove stability, not a function of generalized coordinates and velocities used to derive equations of motion via the principle of least action.
crosslinks:
  near_synonyms: [LYAPUNOV_FUNCTION, POTENTIAL_FUNCTION]
  antonyms: []
  prerequisites: [ALTRUISM_FILAMENT, COHERENCE_DIVIDEND, COMPASS_STATE]
  downstream_effects: []
license: CC-BY-SA-4.0