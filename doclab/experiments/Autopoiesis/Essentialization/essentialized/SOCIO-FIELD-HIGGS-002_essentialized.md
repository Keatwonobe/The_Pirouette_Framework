## Law
A social cascade’s observed information flow `J_obs` on a graph with incidence matrix `B` is decomposable via a renormalized Hodge projection. Let the residual flow be `r = J_obs - J_opt`, where `J_opt` is the optimal potential flow. The residual is decomposed into a potential (gradient) component `grad` and a solenoidal (curl) component `curl` such that `r = grad + curl`. These are found by first solving the regularized node-potential system `(B Bᵀ + εI)φ = B r` for the scalar potential `φ`, which yields `grad = Bᵀφ` and `curl = r - grad`.

The system exhibits at least two distinct, coexisting scaling regimes for avalanche sizes `s`, where the probability distribution follows `P(s) ~ s^α`. The observed regime is a function of the selection operator `O` applied to the decomposed field to define the active subgraph.

**1. Energy-Dominant Operator `O_E`:**
An edge `e` is selected if its curl energy dominates its gradient energy by a factor `k_Γ`.
`O_E(e) = 1` if `curl_e² > k_Γ · grad_e²`, and `0` otherwise.
This operator yields a single, steep power-law exponent:
`α_E ≈ -3.9`

**2. Γ-Shell Operator `O_Γ`:**
An edge `e` is selected if it belongs to the top quantile `q` of edges ranked by the normalized curl-to-grad ratio `|curl_e| / (|grad_e| + ε)`. When applied to temporal windows `t` of the cascade, this operator reveals a time-dependent exponent `α_Γ(t)`.
`α_Γ(t) = f(O_Γ(q,t))`
The exponent evolves systematically:
`α_Γ(t_nucleation) ≈ -0.3` → `α_Γ(t_critical) ≈ -1.0` → `α_Γ(t_saturation) ≈ -1.2`

**Falsifiable Criterion:** For any sufficiently large, synchronized social cascade, the temporal trajectory `α_Γ(t)` must exhibit a U-shaped or Γ-shaped sweep passing near the critical value `α = -1`. The vertical position of this trajectory may shift with the quantile `q`, but its characteristic shape must be conserved. The `O_E` operator must simultaneously yield a distinct, static, and significantly steeper exponent.

## Philosophy
The measurement of a complex social system is not a passive observation but an active structuration. The choice of operator—the mathematical question posed to the field—determines which of its many coexisting potential realities is rendered into a measurable, lawful phenomenon. Objective reality in such systems is therefore not a single, invariant state, but the complete spectrum of possible, internally consistent responses to all modes of interrogation.

## Art
A single roar of information contains many possible thunders. One way of listening reveals the brutal, singular crackle of raw stress. Another, tuned to the delicate edge of chaos, reveals the evolving song the system sings to itself as it breaks.