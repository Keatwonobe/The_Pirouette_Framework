## Law
The foundational principle is the permanent conversion of a universal potential, the Total Entropy Pool (TEP), into a localized, rule-bound system within an object. This conversion is an irreversible investment.
Let $I$ be an item.
Let $TEP_C$ be the TEP of the creator.
The enchantment process is a function $E: (\mathbb{R}^+, I) \rightarrow I'$ where:
$E(\delta, I) = I'$ such that $TEP_C \rightarrow TEP_C - \delta$, and $I'$ gains an internal Entropy Pool $EP_I = \delta$ and a unique rule-set $R_I$.

**Minigame Formalisms:**

1.  **Weapon Containment (Overload Mechanic):**
    A weapon $W$ has an intrinsic structural integrity represented by its TEP, $TEP_W$. An attack channels an amount of entropy $EP_A$.
    *   Standard Attack: $EP_A \le TEP_W$. The attack resolves without risk to $W$.
    *   Overload Attack: $EP_A > TEP_W$. An overload check is initiated.
        *   Let $\Delta_{OL} = EP_A - TEP_W$ be the overload magnitude.
        *   The weapon must make a Constitution check against a Difficulty Class (DC):
            $DC = 10 + \Delta_{OL}$
        *   The weapon's roll is $R_W = d20 + CON_W$, where $CON_W$ is a function of $TEP_W$.
        *   Outcome:
            If $R_W \ge DC$, the attack succeeds and $W$ is unharmed.
            If $R_W < DC$, the attack succeeds but $W$ is destroyed, such that $TEP_W \rightarrow 0$.
    *   *Falsifiable Criterion:* The system is falsified if a weapon can be overloaded ($EP_A > TEP_W$) without any probabilistic risk of permanent destruction ($TEP_W \rightarrow 0$).

2.  **Ward (Recharging Buffer):**
    A ward $D$ provides a Temporary Hit Point pool, $HP_{Temp}$, with a maximum capacity $HP_{Max}$ and a recharge rate $RR$.
    *   Let $Dmg_{in}$ be incoming damage in a round. The damage is absorbed as:
        $HP_{Temp} \rightarrow \max(0, HP_{Temp} - Dmg_{in})$
    *   Recharge is conditional. Let $C_t$ be the condition for recharge at the start of round $t$.
        $C_t = (Dmg_{in, t-1} > 0) \land (HP_{Temp, t-1} < HP_{Max})$
        The recharge condition is that damage was taken in the previous round, and the ward is not at full capacity. The recharge itself only begins on the round *after* taking damage.
    *   The recharge function $f_R$ is applied at the start of a round $t$ if no damage was taken in round $t-1$:
        $HP_{Temp, t} = \min(HP_{Max}, HP_{Temp, t-1} + RR)$
    *   *Falsifiable Criterion:* The system is falsified if a ward can recharge in the same discrete time unit (round) that it absorbs damage.

## Philosophy
The single most cogent philosophical implication is that power is not a static quantity to be possessed, but a dynamic system of negotiated risk. By embedding rules and failure states directly into the instruments of power, the framework transforms agency from a simple act of will into a dialogue with the tool itself. Mastery is therefore redefined not as the accumulation of force, but as the intimate understanding of, and skillful navigation within, a set of imposed, unforgiving constraints. True power lies in the wisdom to know when a tool's internal logic demands restraint, and when it permits a final, shattering exertion.

## Art
An artifact is not a sword to be swung, but a bell to be rung. You may strike it softly to hear its patient, protective chime, or you may strike it with all your might for a single, world-altering thunderclap that cracks it from rim to crown.