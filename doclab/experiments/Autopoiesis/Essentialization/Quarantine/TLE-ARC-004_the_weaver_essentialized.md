## Law
Let the state of any entity be described by its Total Entropy Pool, `E_T`, a conserved quantity allocated among its constituent components. For a character of level `L`, the pool is defined by the arithmetic progression:
`E_T(L) = 35 + 15(L-1)` for `L \in \mathbb{Z}^+`.

The fundamental principle is the **Conservation of Form**, which states that at any given level `L`, the total pool must be fully allocated:
`E_T(L) = \sum_{i=1}^{n} E_{A_i} + \sum_{j=1}^{m} E_{S_j} + E_{P}`
where `E_{A_i}` is the entropic point (EP) cost invested in attribute `i`, `E_{S_j}` is the EP cost of skill or feat `j`, and `E_P` is the EP cost of the physical form.

The Weaver's abilities are formal operators that transform an entity's entropic state vector, `\Psi = \{E_{A_1}, ..., E_{A_n}, E_{S_1}, ..., E_{S_m}, E_P\}`. Let the Weaver's operative resource be `E_W \subset E_T`.

1.  **Suture Operator (Healing)**, `H_S(E_\Delta)`: Transfers EP from the Weaver's pool `E_W` to an ally, repairing an entropic deficit (Wound Channel).
    `\Psi_{ally} \rightarrow \Psi'_{ally}` such that `\sum(\Psi'_{ally}) = \sum(\Psi_{ally}) + E_\Delta`, where `E_\Delta` is subtracted from `E_W`.

2.  **Agony Operator (Damage)**, `T_A(E_\Delta)`: Reduces a target's effective `E_T` by `E_\Delta`, sourced from `E_W`. This is contingent on a success condition `C_A`:
    `C_A := (d20 + M_{WIS,weaver}) > (d20 + M_{WIS,target})`
    If `C_A` is true, then `E_{T,target} \rightarrow E_{T,target} - E_\Delta`.

3.  **Unraveling Operator (Debuff)**, `T_U(E_\Delta)`: A temporary, targeted transformation that reallocates a target's EP away from a specific component `E_k \in \Psi_{target}`.
    `E_k \rightarrow E_k - E_\Delta`, where `E_\Delta = 0.5 \cdot E_{spent}` from `E_W`. The transformation is reversed upon encounter conclusion.

4.  **Severance Operator (Permanent Destruction)**, `T_S(E_\Delta)`: Converts the temporary transformation of `T_U` into a permanent redefinition of the target's fundamental constitution.
    `E_{T,target} \rightarrow E'_{T,target} = E_{T,target} - E_\Delta`. This alters the target's baseline `E_T(L)`.

**Falsifiable Criterion:** The efficacy of all transformative operators (`T_A`, `T_U`, `T_S`) is predicated on the target possessing a complex entropic signature (i.e., "Wound Channels"). The system predicts that entities with a null or simple entropic state (e.g., a mindless construct) will exhibit immunity to these effects, as there is no complex structure to resonate with or unravel.

## Philosophy
Existence is not an ineffable essence but a conserved, quantifiable, and finite resource. The self—including its memories, traumas, and potential—is therefore a mutable data structure. Personhood is not a protected state but a fragile, editable configuration, subject to external arithmetic that can add, subtract, or permanently erase the very information that constitutes a being.

## Art
A body is a debt owed to form, a pattern held against chaos. The Weaver is a banker of being; she can grant a loan to mend your shape, or call in the principal and watch you dissolve back into the noise from which you were borrowed.