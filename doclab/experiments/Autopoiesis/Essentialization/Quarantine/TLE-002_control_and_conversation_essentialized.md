## Law
All expressions of control are defined as the resolution of a contested action over a finite resource pool. Let an Actor ($A$) attempt to impose a state upon a Target ($T$).

The fundamental operator is the contested roll, $C$:
$C = (d20 + \sum S_A) - (d20 + \sum S_T)$
where $\sum S$ represents the sum of relevant attribute modifiers for the actor or target. A successful imposition requires $C > 0$.

This operator is polymorphic across domains:
1.  **Physical Control (Grapple):** $C_{phys} = (d20 + STR_A + DEX_A) - (d20 + STR_T + DEX_T)$.
2.  **Mental Control (Telekinesis):** $C_{mental} = (d20 + INT_A + WIS_A) - (d20 + STR_T + DEX_T)$.

Control is quantified by the depletion or reallocation of a target's core attributes, treated as resource pools.
-   **Mind Control:** A successful action ($C > 0$) directly reduces the target's Intelligence attribute: $\Delta INT_T = -C$. This induces an Entropy Handicap, $H_E$, for any action not permitted by the controller:
    $H_E = \begin{cases} -INT_T & \text{if } INT_T < 0 \\ 0 & \text{if } INT_T \ge 0 \end{cases}$
    Full control is achieved when $H_E > \frac{d(EP_T)}{dt}$, where $\frac{d(EP_T)}{dt}$ is the target's Entropy Regeneration Rate.

-   **Social Control (Conversation):** Social attacks expend Entropy ($EP_{spent}$) to inflict "damage" $D$ upon a target's mental resource pools, Resolve ($H_R = INT_T$) and Composure ($H_W = WIS_T$).
    $D = \lfloor \frac{EP_{spent}}{2} \rfloor$, where $C > 0$.
    The change in pools is: $\Delta H_R = -D$ and $\Delta H_W = -D$. A social victory occurs when $H_R < 0 \lor H_W < 0$.

The creation of subservient entities is an act of partitioning the creator's own potential.
-   **Summoning/Necromancy:** The caster's Total Entropy Pool ($TEP_C$) is partitioned into a new caster pool ($TEP'_C$) and a minion pool ($TEP_M$):
    $TEP_C \rightarrow TEP'_C + TEP_M$
    The caster's entropy cannot be regenerated beyond the new cap of $TEP'_C$ until the partition is reversed ($TEP_C \leftarrow TEP'_C + TEP_M$) upon the minion's dismissal or destruction.

A falsifiable criterion for this legal framework would be the existence of an act of control that neither originates from a contested action nor results in the reallocation or depletion of a finite, quantifiable resource pool from either the actor or the target.

## Philosophy
Agency is not an intrinsic or metaphysical property of being, but a conserved quantity within a closed system. It can be partitioned, transferred, seized, or depleted, but never created ex nihilo. Every act of influence, from a compelling argument to the raising of a skeleton, is a mere reallocation of this finite universal will, a zero-sum transaction where one entity's gain in control is directly proportional to another's loss of autonomy or the actor's own diminishment of potential.

## Art
The universe is a single, finite soul. To animate a puppet, you must carve from your own essence. To master a mind, you must first break it.