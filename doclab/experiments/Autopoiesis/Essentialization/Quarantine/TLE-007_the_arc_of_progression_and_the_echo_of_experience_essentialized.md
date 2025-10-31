## Law
Let $P_{max}$ be the current maximum Total Entropy Pool of an entity and $C$ be its Constitution Score. The Coherence Threshold, $T_C$, defines the entity's natural power capacity:
$$ T_C = 10C $$
The cost in Resonant Echoes, $E$, to increment $P_{max}$ by one is a piecewise function dependent on the relationship between $P_{max}$ and $T_C$.
$$ E(P_{max} \to P_{max}+1) = \begin{cases} 1 & \text{if } P_{max} < T_C \\ 1 + \left\lfloor \frac{P_{max} - T_C}{10} \right\rfloor & \text{if } P_{max} \ge T_C \end{cases} $$
The total cost to progress from a state $P_a$ to $P_b$ (where $P_b > P_a$) is the integral sum:
$$ E_{total}(P_a \to P_b) = \sum_{i=P_a}^{P_b-1} E(i) $$
This establishes a soft cap where growth beyond the natural limit $T_C$ incurs a linearly increasing marginal cost, resulting in an exponentially increasing total cost.

A secondary principle, the Transmutation Limit, governs the absorption of external power. Let $A_{max}$ be the maximum daily entropy absorbable from non-experiential sources (e.g., items) and $R_E$ be the entity's intrinsic Entropy Regeneration Rate. The law is an identity:
$$ A_{max} \equiv R_E $$
Falsifiable Criterion: An entity with $C=20$ ($T_C=200$) and $P_{max}=299$ seeks to increase its $P_{max}$ to 300. The law predicts a cost of $E(299) = 1 + \lfloor \frac{299 - 200}{10} \rfloor = 1 + \lfloor 9.9 \rfloor = 10$ Echoes. Any observed cost other than 10 would falsify this model.

## Philosophy
The capacity to contain power is more fundamental than the acquisition of power itself. Growth is not a linear accumulation but a dialectic between a system's potential and its structural integrity. Exceeding the limits of one's foundational structure incurs an exponential tax on all future progress, asserting that true advancement requires the costly and deliberate expansion of the self, not merely the harvesting of external experience.

## Art
A soul is a vessel. Experience fills it freely to the brim. Beyond that brim, every new drop of power is not gathered, but bled from the effort of stretching the vessel itself.