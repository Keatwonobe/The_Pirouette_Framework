## Law
The system is governed by a principle of conserved potential, Total Entropy (`E_T`), allocated between Attributes (`E_A`) and Physical Form (`E_P`).

**1. Axiom of Conservation:** For any entity at a given level `L`, the total entropy is a constant sum of its allocated components.
`E_T(L) = E_A(L) + E_P(L)`

**2. Law of Progression:** The total entropy pool increases linearly with level, following the function:
`E_T(L) = 35 + 15(L-1)` for `L ≥ 1`.

**3. Attribute Derivations:**
Attribute Scores (`S_A`) and Modifiers (`M_A`) are derived from their respective invested entropy (`E_A_i`).
- Score function: `S_A = floor(E_A_i / 2)`
- Modifier function: `M_A = floor(S_A / 4) = floor(floor(E_A_i / 2) / 4)`

**4. Resilience Derivation:**
Maximum Hit Points (`H_max`) are a function of entropy invested in the Torso and Limbs.
Let `E_P(Torso)` be the entropy of the torso component and `E_P(Limb_i)` be the entropy of the *i*-th limb component.
`H_max = E_P(Torso) + floor(0.5 * Σ E_P(Limb_i))`

**5. The Juggernaut Maxim:** The Juggernaut archetype is the solution to an optimization problem that seeks to maximize physical dominance as a function of Strength (`STR`) and Constitution (`CON`) under a boundary condition of zero mental investment.
- Objective function: `maximize(E_STR + E_CON)`
- Constraint: `E_INT = 0, E_WIS = 0`

**Falsifiable Criterion:** The model's optimality claim is falsified if an alternative allocation `E'_A` exists such that `E'_INT > 0` or `E'_WIS > 0`, which results in a greater value for a defined combat effectiveness metric (e.g., `(H_max) * (M_STR)`) for a given `E_T(L)`, thereby violating the Juggernaut Maxim.

## Philosophy
The governing law of conserved entropy dictates that existence is a zero-sum allocation of potential. To construct a god in one dimension is to create a vacuum in all others. Absolute power is therefore an illusion; it is merely the relational state achieved by sacrificing all breadth for a single, infinite depth. The Juggernaut's physical omnipotence is thus mathematically inseparable from its mental nonexistence. Its invincibility is the direct and necessary shadow of its absolute vulnerability, proving that any total strength is merely a monument to total abdication.

## Art
A body is forged into a hammer by feeding it the mind as fuel. It can shatter any anvil, but it cannot feel the wind that whistles through its own hollow skull.