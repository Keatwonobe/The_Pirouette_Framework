## Law
Let `L` be character level, where `L ∈ ℤ, 1 ≤ L ≤ 20`.
The Total Entropy Pool, `TEP(L)`, is a piecewise function:
`TEP(L) = 35 + 15(L - 1)` for `1 ≤ L ≤ 15`
`TEP(L) = 245 + 18(L - 15)` for `15 < L ≤ 20`

Character construction adheres to a conservation law, where all potential is allocated. Let `EP_A` be the set of all attribute expenditures, `EP_P` be physical form expenditures, `EP_F` be feat expenditures, and `EP_S` be skill expenditures. For any valid build at level `L`:
`TEP(L) - (Σ EP_A + Σ EP_P + Σ EP_F + Σ EP_S) = 0`

An Attribute Modifier `A_M` is derived from its corresponding Attribute Score `A_S` by the floor function:
`A_M = ⌊A_S / 4⌋`

The Phantom archetype is defined by a primary growth vector `V_g` that maximizes investment in Dexterity `(DEX)` and Intelligence `(INT)` while minimizing investment in Constitution `(CON)` and Strength `(STR)`. This is subject to the invariant constraint of Hit Points `(HP)`:
`∀L, HP(L) = 7`
This value is a constant derived from the `Humanoid, Standard` template `(C=18 EP)` and is not a function of `L` or `CON`.

The core combat algorithm is defined by the feat *Wound Channel Analyst*. Let `T` be a target entity with a set of vulnerabilities `{v_1, v_2, ..., v_n}`. Let `I_c` be the result of an Intelligence check. Let `D_b` be bonus damage.
`Action_1: OBSERVE`
`IF (I_c ≥ Difficulty(v_i))`
`THEN Action_2(Attack): Damage_final = Damage_base + D_b`
`WHERE D_b = A_M(INT)`

Falsifiable Criterion: Any character instance where `HP > 7` or where `Σ EP_invested ≠ TEP(L)` for a given `L` invalidates the archetype's core model.

## Philosophy
True mastery is not the accumulation of force to withstand reality, but the cultivation of insight to render reality's threats irrelevant. The system demonstrates that survival and supremacy are achieved by optimizing an abstract, predictive model of the world, allowing for the precise application of minimal force to exploit inherent systemic flaws, thereby making physical resilience a null variable.

## Art
To become a ghost is to solve the equation of the world so completely that your own body becomes a forgotten variable.