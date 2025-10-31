## Law
The Arcanist is a system governed by the Law of Conservation of Potential. All properties of the entity are derived from a finite, level-dependent Total Entropy Pool, `TEP(L)`.

1.  **Total Potential Function:** The TEP is a piecewise linear function of level `L`.
    *   For `1 ≤ L ≤ 15`: `TEP(L) = 35 + 15(L-1)`
    *   For `15 < L ≤ 20`: `TEP(L) = 245 + 18(L-15)`

2.  **Conservation Equation:** At any level `L`, the sum of all invested Entropy Points (`EP_i`) must equal the total available pool. Potential is a conserved quantity; it is allocated, not created.
    *   `TEP(L) = Σ EP_i`
    *   Where `Σ EP_i = EP_attributes + EP_physical_form + EP_skills`

3.  **State Derivations:** Key character states are deterministic functions of EP investment.
    *   Attribute Score `S_attr` is a function of its invested EP, `E_attr`: `S_attr = f(E_attr)`. This function is non-linear and exhibits diminishing returns for higher-cost attributes (e.g., Intelligence), while following `S_attr = E_attr / 2` for others (e.g., Constitution).
    *   Attribute Modifier `M_attr` is a non-linear, monotonically increasing step-function of the Attribute Score `S_attr`: `M_attr = g(S_attr)`.
    *   Maximum Health `HP_max` is derived from physical form investment: `HP_max = EP_torso + floor(0.5 * EP_limbs)`.

4.  **Falsifiable Criteria:** The model is falsified if any of the following conditions are met:
    *   `Σ EP_i ≠ TEP(L)` for a given entity.
    *   An entity designated "Arcanist" is observed with `E_STR > 0`.
    *   A measured state (e.g., `HP_max`) does not match the output of its corresponding derivation function given the EP inputs.

## Philosophy
The single most cogent implication is that specialization is an act of erasure. An entity's identity is defined not by the potential it accumulates, but by the vast swathes of alternative selves it has irrevocably sacrificed. The Arcanist's immense power is thus inseparable from its immense fragility; the strength of its mind is precisely measured by the weakness of the body that was forfeited to create it.

## Art
To forge a mind that can set the world ablaze, one must grind the rest of the self down to the thinnest, most fragile pane of glass.