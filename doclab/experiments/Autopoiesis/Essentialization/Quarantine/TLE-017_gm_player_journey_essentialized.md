## Law
Let a character's standing with a faction $F$ be a reputation value $Rep_F \in \mathbb{Z}$, constrained to the interval $[-5, 5]$. The state of the relationship is a function of this value, with $Rep_F = 5$ defined as Revered and $Rep_F = -5$ as Hated.

Let the Skazan Order's disposition be a non-negative integer Threat Level, $T_S \in \mathbb{N}_0$. The rate of change of the Threat Level is proportional to the rate of accumulation of entropic potential (TEP) by the character and their direct interference with Order operations.
$dT_S/dt \propto d(\sum{TEP_{events}})/dt$. Specific thresholds $T_S \in \{1, 6, 11\}$ trigger qualitative shifts in the Order's strategic response.

Mass combat between two sides, $S_1$ and $S_2$, is resolved as a discrete-time clash.
1.  **Potential Energy Pool ($P_i$):** For each side $S_i$, the total entropic potential is the sum of the TEP of all $N_i$ participants.
    $P_i = \sum_{j=1}^{N_i} TEP_j$
2.  **Stochastic Force Multiplier ($M_i$):** Each side generates a multiplier by sampling from a discrete uniform distribution, where the sample space is determined by the number of participants.
    $M_i \sim U\{1, N_i\}$
    This is equivalent to rolling a die with $N_i$ sides.
3.  **Total Force ($F_i$):** The effective force for the round is the product of the potential energy and the stochastic multiplier.
    $F_i = P_i \cdot M_i$
4.  **Damage Calculation ($\Delta_F$):** The magnitude of damage dealt is the absolute difference between the total force of the two sides.
    $\Delta_F = |F_1 - F_2|$
5.  **Casualty Resolution:** The side $S_L$ with the lower total force ($F_L < F_W$) suffers $\Delta_F$ TEP damage. This damage is distributed sequentially to participants, typically from front to rear ranks. A participant is eliminated if the cumulative damage assigned exceeds their individual $TEP_j$. A falsifiable criterion for tie-breaking simultaneous eliminations is a $d2$ roll, where a result of 1 mandates perishing.

## Philosophy
In the calculus of conflict, the individual is arithmetically effaced. Personal power and skill are rendered abstract, summed into a collective potential that serves only as a static coefficient. The decisive variable is not the quality of the combatants but the sheer scale of their host, which introduces a chaotic, stochastic multiplier. Thus, individual agency is dissolved into a statistical aggregate, and fate is adjudicated not by the sum of wills, but by a singular roll of the dice whose very magnitude is a function of the collective's mass. The self becomes a fungible quantum of energy, its identity irrelevant to the outcome.

## Art
They sharpen their swords and tally their strength, but the god of battle is blind and rolls dice made from their bones.