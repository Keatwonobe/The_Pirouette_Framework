## Law
Let a character be `c` and a faction be `f`. The state of their relationship is defined by the Resonance Score, `R(c, f) ∈ ℤ`, bounded such that `R ∈ [-10, 10]`.

Each faction `f` is defined by a Faction Directive, `D_f`, which can be modeled as a unit vector in an abstract n-dimensional action space `S`. An action `A` undertaken by character `c` is also a vector in this space, `A_c ∈ S`.

The change in resonance, `ΔR`, is a function of the alignment between an action and a faction's directive. This alignment is determined by the dot product of their vectors:
`ΔR(c, f) = f(A_c ⋅ D_f)`

For a discrete system, this function can be defined as:
`ΔR = ⌊k * (A_c ⋅ D_f)⌋`
where `k` is a scaling constant representing the action's magnitude and social observability. The system update rule is:
`R_t+1(c, f) = max(-10, min(10, R_t(c, f) + ΔR))`

The tangible consequences of reputation are a mapping `C` from the Resonance Score to a set of social and economic outcomes `O`:
`O = C(R(c, f))`
where `C` is a step function defined by the score ranges (e.g., `R > 7 → O_Idolized`).

Social stealth via an intermediary `i` of faction `f_int` to affect a target faction `f_target` is a probabilistic state transition. Character `c` initiates the action. The probability of success `P(S)` is a function of `c`'s relevant skill `σ_c`, the resonance of `c` with `f_int`, and the hostility of `f_target`:
`P(S) = f(σ_c, R(c, f_int), R(c, f_target))`
where `∂P(S)/∂R(c, f_int) > 0` and `∂P(S)/∂R(c, f_target) > 0`.

The system state transition is as follows:
- If successful (with probability `P(S)`):
  - `R(c, f_target)` remains unchanged.
  - `c` incurs a cost `γ` (to `f_int`).
  - The effects of action `A` are realized.
- If failed (with probability `1 - P(S)`):
  - `R(c, f_target) ← R(c, f_target) - k_1`
  - `R(c, f_int) ← R(c, f_int) - k_2`
  where `k_1, k_2 > 0` are penalty magnitudes.

A falsifiable criterion of this system is that a character's social capital `(R)` is non-fungible across factions *except* through the explicit, risk-assessed intermediary process. The system predicts that direct action will always alter the `R(c,f)` ledger, while indirect action transfers both the potential resonance shift and the risk of failure to a third party at a defined cost.

## Philosophy
Social identity is not an intrinsic quality of the self, but an extrinsic, calculated asset. It is a dynamic ledger of public deeds measured against axiomatically defined social structures. This externalized self can be manipulated, its signature can be masked, and its social agency can be leased from others. The self, therefore, is not who you are, but the resonant value of your history, a value that can be bypassed or even brokered for a price.

## Art
A person is not a song, but a score. Each deed is a note, and society is the orchestra that reads the page. When the music turns dissonant, a wise composer does not rewrite his soul; he hires a more reputable conductor to lead the performance.