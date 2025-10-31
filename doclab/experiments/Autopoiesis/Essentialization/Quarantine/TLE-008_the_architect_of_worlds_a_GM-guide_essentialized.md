## Law
Let a party consist of `n` characters, where the `i`-th character has a Total Entropic Power `TEP_i`. The Party Average Entropic Power is defined as:
`TEP_avg = (Σ TEP_i) / n` for `i = 1 to n`

Any challenge (a creature, trap, or social encounter) is defined by its Entropic Budget, `EB`. The `EB` is a function of `TEP_avg` and a difficulty scalar `k`:
`EB = k * TEP_avg`

The scalar `k` is defined by the intended encounter difficulty:
- Trivial: `k = 0.5`
- Normal: `k = 1.0`
- Hard: `k = 1.25`
- Very Hard: `k = 1.5`
- Legendary: `k ≥ 2.0`

The total `EB` of a challenge is a conserved quantity allocated to its constituent pools. For any challenge `C`:
`EB_C = Σ EB_pool`

**Challenge Sub-Types:**

1.  **Creature (Combat):**
    `EB_Creature = EB_Health + EB_Attack`
    Health Pool (`HP`) `≡ EB_Health`
    Attack Potential `≡ EB_Attack`
    Entropy Regeneration Rate (`ERR`) per round is defined as: `ERR = ⌊0.10 * EB_Creature⌋`

2.  **Hazard/Trap (Environmental):**
    `EB_Trap = EB_Damage`
    A hazard is a single-expenditure system. Upon activation, its state transitions from Armed to Inert.
    `Damage_output = EB_Trap`
    `∫ EB_Trap dt = 0` after activation.

3.  **NPC (Social):**
    `EB_Social = EB_Resolve + EB_Composure + EB_Influence`
    Mental Health Pool 1 (Resolve) `≡ EB_Resolve` (derived from INT)
    Mental Health Pool 2 (Composure) `≡ EB_Composure` (derived from WIS)
    Social Attack Potential `≡ EB_Influence`

**Falsifiable Criterion:** The system's central hypothesis is that `k` is a reliable predictor of challenge. This model is falsified if there is no statistically significant correlation between the assigned `k`-value of an encounter and the measured party resource expenditure required to overcome it across a large dataset of play sessions.

## Philosophy
The system posits an ontological monism of challenge, asserting that all forms of opposition—physical violence, environmental danger, or social conflict—are not distinct categories of reality but are isomorphic, fungible manifestations of a single, conserved metaphysical substance. A dragon's fire and a king's decree are commensurable quantities, differing only in allocation, not in essence.

## Art
The universe is a ledger. A dragon's roar and a liar's whisper are but different entries, their cost calculated in the same ink.