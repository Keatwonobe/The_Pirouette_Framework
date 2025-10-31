## Law
Let an entity's state be defined by its attributes {STR, DEX, INT, WIS} and its Entropy Points (EP). All actions are transactions of EP.

**1. Action Capacity**
The number of actions (A) per turn is a function of total attribute investment:
`A = floor( (STR + DEX + INT + WIS) / 6 )`, where `A ≥ 1`.

**2. Universal Accuracy & Skill Checks**
Success of an action is a probabilistic function of a Target Number (TN), which is dependent on the EP invested in the action's effect (E).
Let `E_p` be the EP spent on power/damage and `E_c` be the EP spent on a skill check.
- **Accuracy Check:** `d20 + DEX_mod + INT_mod ≥ TN_acc`
- **Skill Check:** `d20 + WIS_mod ≥ TN_skill`
- **Target Number Derivation:** `TN = 8 + floor(E / 2)`
Thus, `P(success) ∝ 1/E`. This establishes a core inverse relationship between power and control. A falsifiable criterion: increasing EP spent on an effect must increase the TN for the associated accuracy/skill check.

**3. Contested Stealth**
For an action to succeed against a passive observer, the invested entropy must exceed a probabilistic awareness threshold.
`Success ⇔ E_invest > Roll(d(N_sensors + WIS_mod))`
Where `N_sensors` is the number of relevant sensory organs.

**4. Healing & Exhaustion**
Entropy transfer for healing is governed by a law of thermodynamic inefficiency.
- **Magical Healing:** `EP_cost = 2 * HP_restored`
- **Sacrificial Healing:** `HP_cost = 1 * HP_restored`
Entropy Regeneration Rate (ERR) decays exponentially with sustained activity. Let `ERR_0` be the base rate. After `n` 24-hour periods without rest:
`ERR_n = floor(ERR_{n-1} / 2) = floor(ERR_0 / 2^n)`
System collapse occurs when `ERR_n < 1`.

**5. The Will-Fortune Conversion Principle**
An entity can convert deterministic EP into a probabilistic dice roll (`d`). This choice exists for any action with a numerical effect.
- **Base Cost:** The cost to purchase one die of `N` faces is `C(1dN) = N / 2`.
- **The Law of Diminishing Returns (Ante):** The marginal cost of adding a die to a pool increases linearly. The cost for the `k`-th die of a given type is:
  `C_k = C_base + (k-1)`
The total cost `C_T` for `m` dice is the summation:
  `C_T(m) = Σ_{k=1 to m} (C_base + k - 1) = m * C_base + (m(m-1))/2`
This makes large dice pools exponentially more expensive, creating a soft cap on reliance on fortune.
- **Hybrid Investment:** A total effect `E_T` can be a sum of deterministic (`E_det`) and probabilistic (`E_prob`) components, where `E_det` is the raw EP spent and `E_prob` is the result of dice purchased with EP.
  `EP_total_cost = E_det + C_T(m)`

## Philosophy
The system's core philosophical thesis is that agency is not the capacity to act, but the metabolic choice between imposing a known, limited reality versus gambling on an unknown, potential one. Every expenditure of self (Entropy) forces a confrontation with this choice: to be a craftsman, whose every action has a predictable and certain outcome, or to be a supplicant, who trades the currency of their being for a chance at fortune's favor. The Law of Diminishing Returns is not merely a balancing mechanic; it is a metaphysical tax on greed, suggesting that the universe fundamentally favors measured control over extravagant hope, and that to repeatedly ask for miracles is an act of profound and unsustainable inefficiency.

## Art
The soul is both a coin and a die. You may spend it to purchase the world as it is, or cast it to win the world as it might be.