## Law
Let the state of a system be defined by a character `P` and a world environment `W`. The environment possesses a Resonant State `S` and a global Residue pool `R ∈ ℕ₀`. The party possesses a shared Coherence Dividend pool `H ∈ ℕ₀`. An action `A` has an Energy Point cost `C(A)` and an effect `E(A)`.

**Principle of Resonance:**
For any action `A` performed by `P` in an environment with state `S`:
- **Coherence Condition:** If `A` is aligned with `S` (denoted `A ~ S`), the expected value of its effect is increased: `E'(A) > E(A)`. Specifically, for any `n`-sided die roll `d_n` contributing to `E(A)`, the probability of rolling a 1 becomes zero: `P(d_n=1) = 0`.
- **Dissonance Condition:** If `A` is opposed to `S` (denoted `A ⊥ S`), the cost of the action is increased: `C'(A) = ⌈1.25 * C(A)⌉`.
- **Falsifiable Criterion:** An action `A ~ S` that fails to grant the effect modification, or an action `A ⊥ S` that fails to incur the cost increase, violates this principle.

**Principle of Narrative Injury (The Wound Channel):**
A critical event `C_crit` (Critical Hit or HP → 0) transforms a character `P` into a new state `P'`. This transformation introduces a persistent Wound Channel `W`, defined as an ordered pair of conditional modifiers `W = (V, I)`.
- **Vulnerability `V`:** A set of narrative triggers `{v_1, v_2, ..., v_n}` such that if `v_i` is present, the probability of failure for a related action `A_V` increases. `P(Success(A_V) | v_i) < P(Success(A_V))`.
- **Insight `I`:** A set of narrative triggers `{i_1, i_2, ..., i_n}` such that if `i_j` is present, the probability of success for a related action `A_I` increases. `P(Success(A_I) | i_j) > P(Success(A_I))`.
- **Falsifiable Criterion:** A character `P'` with wound `W` who is exposed to trigger `v_i` without suffering the corresponding disadvantage falsifies the existence of the wound.

**The Law of Moral Thermodynamics:**
The world-system `W` is subject to a conservation-and-conversion dynamic between two opposing potentials: Residue (`R`) and Coherence (`H`).
1.  **Entropic Generation:** A significant action `A_Σ` increases the world's Residue. The change in `R` is a stochastic function of the action's magnitude: `ΔR = f(A_Σ)`, where `f(A_Σ)` typically resolves to a `d4` roll or greater.
    `R → R + f(A_Σ)`
2.  **Negentropic Generation (Altruism):** An action `A_α` tagged as [Altruistic] performed by a character `P_i` with Constitution modifier `M_CON` generates a temporary Coherence Dividend `H`.
    `H = M_CON(P_i)`
    This pool `H` is accessible by all members of the party `{P_1, ..., P_n}` and decays to zero at the start of `P_i`'s next turn.
3.  **Coherence Conversion:** The party may execute a "world-healing" action `A_ω` at any time, which has no cost other than the expenditure of Coherence. This action reduces `R` by the amount of `H` spent.
    `R → R - H_spent` where `0 ≤ H_spent ≤ H`
- **Falsifiable Criterion:** An [Altruistic] action that fails to generate `H = M_CON` for the party, or an expenditure of `H` that fails to reduce `R` on a 1-to-1 basis, would falsify this law.

## Philosophy
The universe is not a morally neutral stage upon which actors perform, but a reactive medium governed by a form of moral thermodynamics. Every action imparts energy into this medium, increasing its entropy (Residue) and contributing to systemic chaos. Altruism is not merely a social or ethical preference; it is a fundamental, negentropic force. It is the only mechanism capable of generating a coherent energy (Coherence) that can actively reduce the system's ambient entropy. Therefore, the struggle for existence is not between good and evil as abstract concepts, but between the physical realities of cosmic decay and the localized, intentional acts of kindness that are the sole counter-agents to it.

## Art
A scar is the tuning fork of the soul; it teaches the hand that was burned not only the memory of fire, but the precise frequency of the world's healing song.