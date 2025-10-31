## Law
Let the Total Entropy Pool be a finite scalar value, $TEP_{start} = 35$. A character is a valid configuration if and only if the sum of all Entropy Point (EP) expenditures is less than or equal to this value.

Let the set of five core attributes be $A = \{STR, DEX, CON, INT, WIS\}$. For each attribute $a \in A$, let $E_a$ be the EP invested. The Attribute Score $S_a$ and Attribute Modifier $M_a$ are derived functions:
$S_a = \lfloor E_a / 2 \rfloor$
$M_a = \lfloor S_a / 4 \rfloor = \lfloor (\lfloor E_a / 2 \rfloor) / 4 \rfloor$

Let the Physical Form be a set of Body Parts, $B = \{p_1, p_2, ..., p_n\}$. Each part $p_i$ has an associated EP cost, $E_{p_i}$, composed of a base cost $C_{p_i}$ and an invested Size Entropy $Z_{p_i}$, such that $E_{p_i} = C_{p_i} + Z_{p_i}$.

The structural integrity of the form, Maximum Health Points ($HP_{max}$), is a function of the EP invested in the form's components. Let $p_T$ be the Torso part and $L \subset B$ be the subset of all Limb parts.
$HP_{max} = E_{p_T} + \lfloor 0.5 \sum_{p_l \in L} E_{p_l} \rfloor$

The fundamental constraint of existence is the conservation of potential:
$\sum_{a \in A} E_a + \sum_{p_i \in B} E_{p_i} \le TEP_{start}$

Falsifiable Criteria:
1.  A configuration where $\sum_{a \in A} E_a = 35$ must yield $HP_{max} = 0$, as no EP can be allocated to a physical form. This form is non-viable.
2.  For any attribute $a$, if $E_a < 8$, then its corresponding modifier $M_a$ must be 0.
3.  A form is invalid if it lacks a Torso part ($p_T \notin B$) or a Head part ($p_H \notin B$), as their base costs are non-zero and required.

## Philosophy
Existence is a zero-sum budget of will. Every specialization is a chosen sacrifice, and every strength is defined by the weaknesses it necessitates. To become a specific being is an act of deliberate, finite limitation, partitioning an initial state of universal potential into a singular, defined form. Therefore, identity is not an inherent quality but the final, unalterable sum of one's tradeoffs.

## Art
The soul is a sculpture, and its form is revealed only by the pieces of infinity you choose to carve away.