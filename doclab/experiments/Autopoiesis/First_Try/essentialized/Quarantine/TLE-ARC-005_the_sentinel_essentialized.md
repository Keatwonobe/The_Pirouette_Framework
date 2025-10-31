## Law
Let `L` be character level, where `L ∈ ℤ, L ≥ 1`.
Let `TEP(L)` be the Total Entropy Pool, a conserved resource. The governing equation for its accumulation is:
`TEP(L) = 35 + 15(L-1)`

The allocation of `TEP` is a zero-sum distribution across all character components. Let `E_i` be the Entropy cost of component `i`. The fundamental constraint of the system is the law of conservation of Entropy:
`TEP(L) = Σ E_i(L) = E_Attributes(L) + E_Form(L) + E_Feats(L) + E_Skills(L)`
For any valid build, `Remaining TEP = 0`.

The primary derived statistics are governed by specific Entropy investments. Let `E_CON` be the Entropy invested in the Constitution attribute, which yields a Constitution Score `S_CON = f(E_CON)`. The Constitution Modifier `M_CON` is derived as `M_CON = g(S_CON)`.
Maximum Health Points (`HP_MAX`) are a direct function of Entropy invested into the physical form's torso (`E_Torso`) and limbs (`E_Limbs`):
`HP_MAX = E_Torso + ⌊0.5 * E_Limbs⌋`

Key abilities are formal transactional systems:
1.  **Resonant Barricade:** `create_wall(E_cost) → Wall(HP = E_cost)`. `E_cost` is deducted from a dedicated sub-pool, `E_ShellWeaving`.
2.  **Aegis of Coherence (Capstone):**
    *   **Activation Cost:** `1 Action ∧ 20 E_ShellWeaving`
    *   **Condition:** `use_count ≤ 1 per rest_cycle`
    *   **Effect:** `create_sphere(radius=15ft, duration=M_CON rounds, boundary_permeability=0)`

A primary falsifiable criterion of this system is that no entity can manifest an ability or statistic whose total Entropy cost `Σ E_i` exceeds `TEP(L)`. The existence of a Level 20 Sentinel with `HP_MAX > 91` would falsify the `HP_MAX` derivation or imply a violation of the `TEP(L)` conservation law.

## Philosophy
The single most profound implication is that a coherent self is not an inherent property but a deliberate, costly construction. Existence is a zero-sum budget of potential ("Entropy"). To become a protector—an anchor of order for others—one must systematically sacrifice vast domains of personal potential (mobility, intellect, aggression) not merely to enhance resilience, but to actively transmute one's own being into a static, externalized law. The ultimate act of selfhood is to spend oneself down to a single function, becoming a living boundary against chaos, defining one's existence entirely by the inviolable space one creates for others.

## Art
The universe granted a budget of boundless chaos; I chose to spend it all on a single, perfect silence.