## Law
Let an entity's state be defined by its Total Entropy Pool, TEP, a conserved quantity at any given Level, L.

`TEP(L) = A(L) + P(L)`
where `A(L)` is the total EP invested in attributes and `P(L)` is the total EP invested in physical form and skills.

The progression of TEP is a monotonically increasing, piecewise linear function of L:
`TEP(L) =`
  `35 + 15(L-1)` for `1 ≤ L ≤ 15`
  `245 + 18(L-15)` for `15 < L ≤ 20`

The core axiom of the Drifter archetype is the Asymmetry of Investment, which dictates a trade-off between static resilience (HP) and dynamic agency (represented by Dexterity, `DEX`, and Chaos Weaving, `C`). HP is a static function of the initial form investment `P(1)` and is invariant with respect to subsequent investments in the Constitution attribute (`EP_CON`) or increases in Level (`L`).

`HP = f(P(1))`, where `∂(HP) / ∂(EP_CON) = 0` and `∂(HP) / ∂L = 0`.

For the Drifter, `HP` is fixed at 7. Viability is therefore a function of maximizing dynamic capability investment relative to static attributes (`STR`, `CON`). Let `R_d` be the ratio of dynamic to static attribute investment:

`R_d(L) = (EP_DEX(L) + EP_WIS(L) + EP_INT(L)) / (EP_STR(L) + EP_CON(L))`

The Drifter model mandates that `R_d(L)` must be a strictly increasing function of `L`.
`R_d(1) = (8+4+1)/(2+2) = 3.25`
`R_d(20) = (90+50+25)/(5+20) = 6.6`
`∴ d(R_d)/dL > 0`

**Falsifiable Criterion:** The model is falsified if any entity operating under these principles demonstrates `HP(L_n) > HP(L_1)` where `n>1`, without a discrete change in the foundational `P(1)` form investment.

## Philosophy
The self is not a noun, but a verb. The system mandates that the vessel's capacity to endure damage is fixed at its origin. All subsequent growth must be allocated to action, perception, and manipulation of the external world. Existence, therefore, is not a state of being but a continuous, successful process of acting. The entity does not persist by becoming more durable, but by becoming more adept at ensuring reality never puts its durability to the test. To fail to act with perfect efficacy is to be annihilated; to exist is to successfully *do*.

## Art
A body of glass, containing a storm. It does not learn to endure the shattering, but to become the wind that guides the stone.