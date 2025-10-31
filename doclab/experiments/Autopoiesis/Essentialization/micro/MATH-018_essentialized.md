## Law
Let a physical model `M` be a tuple `(U, T, N, {f_i})`, where `U={u_k}` are universal constants derived from symmetry, `T={t_j}` are integer-valued topological indices, `N={n_m}` are non-tunable external nuisance parameters, and `{f_i}` are the set of functional forms governing the system's dynamics.

**Axiom 1 (Admissibility of Functions):** Any function `f(Γ) ∈ {f_i}` is admissible if and only if it satisfies the following constraints simultaneously:
1.  **Locality:** `f = f(Γ, ∂Γ)` in the low-energy limit.
2.  **Symmetry:** The power series expansion of `f` around `Γ=0` contains only even powers of `Γ` under background T-symmetry: `f(Γ) = c_0 + c_2 Γ² + c_4 Γ⁴ + ...`.
3.  **Scale Covariance:** Under a scale transformation `Γ → λΓ`, the action `S = ∫ d⁴x ℒ(f(Γ))` must transform as `S → S + ΔS_boundary`, uniquely fixing the leading exponent.

**Axiom 2 (Predictive Fixation):** The model `M` is fixed by a one-shot anchor `A`.
1.  Select a single observable `O_anchor` from the set of all observables `{O}`.
2.  Calibrate `M` against `O_anchor` to fix the values of all `u_k ∈ U` and `t_j ∈ T`. This yields the frozen parameter sets `U*` and `T*`. `A: M(U, T) | O_anchor → M_frozen(U*, T*)`.
3.  Post-anchoring, any modification of `U*` or `T*` constitutes the definition of a new, distinct model `M'`.

**Falsification Criteria:** `M_frozen` is falsified if any of the following conditions are met for a preregistered, out-of-sample set of target observables `{O_target}`:
1.  **Predictive Failure:** For any `O_k ∈ {O_target}`, the model prediction `P(O_k)` lies outside the `nσ` experimental uncertainty band of the measured value `O_k^exp`.
2.  **Simplicity Failure:** The model evidence `Z(M_frozen)` does not decisively exceed that of a simpler, nested model `M_simple` (e.g., a no-portal `T=0` case) or a less-constrained model `M_fit` (e.g., with free-fit exponents), as adjudicated by Bayes factors or information criteria (AIC/BIC).
3.  **Ratio Failure:** A parameter-free, hadron-insulating ratio `R`, such as `R = (a_μ − r² a_e) / (a_τ − r⁻² a_μ)` where `r = m_μ/m_e`, is predicted incorrectly. The model must provide at least one such falsifiable ratio.

## Philosophy
The epistemological legitimacy of a physical theory is defined not by its capacity to accommodate existing data, but by its pre-committed, structural refusal to do so. A theory's value resides in its predictive rigidity—its vulnerability to being decisively broken by a single future measurement. By replacing the freedom to tune parameters and functional forms with inviolable constraints derived from symmetry and topology, science transitions from an exercise in post-hoc explanation to a mechanism for generating high-risk, non-negotiable forecasts about reality. True understanding is demonstrated not by drawing the target around the arrow, but by firing the arrow from a fixed position and allowing reality to judge its aim.

## Art
Science must not be a sculptor, who freely carves marble to fit a preconceived image. It must be a locksmith, who forges a single, rigid key from first principles and then, in a moment of truth, dares to turn it in the unforgiving lock of reality.