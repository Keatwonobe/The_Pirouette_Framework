## Law
Let a **Run** be a vector `r \in \mathbb{R}^3` defined by `r = (s, p, d)`, representing score, span, and dark residue, respectively. All components are normalized to `[0,1]`.

Let the **Witness** be the total history of runs, a set `W_t = \{r_1, r_2, ..., r_t\}` at time `t`.

Define a linear functional, the **Coherence** `C: \mathbb{R}^3 \to \mathbb{R}`, as the projection of a run onto a coherence vector `w = (w_s, w_{sp}, -w_{dr})`:
`C(r) = w \cdot r = w_s \cdot s + w_{sp} \cdot p - w_{dr} \cdot d`
This induces a total ordering `\leq_C` on `W_t`.

The **Gallery** `G` is a partition of the ordered set `W_t` into three disjoint subsets `(G_{top}, G_{mid}, G_{worst})` based on fixed cardinality thresholds `k_{top}` and `k_{worst}`.
- `G_{top} := \{ r \in W_t \mid \text{rank}_{<_C}(r) > |W_t| - k_{top} \}`
- `G_{worst} := \{ r \in W_t \mid \text{rank}_{<_C}(r) \le k_{worst} \}`
- `G_{mid} := W_t \setminus (G_{top} \cup G_{worst})`

The **Ecology** is a sampling policy `\mathcal{P}` for selecting a run `r^* \in W_t` to inform the next process iteration. It is parameterized by a probability vector `\pi = (p_{top}, p_{mid}, p_{worst})` where `\sum p_i = 1`. The probability of selecting a run from a given partition is:
`P(\text{select from } G_i) = p_i`
Within a partition, sampling is uniform. Thus, for `r \in G_i`, the probability of selection is `P(r^* = r) = p_i / |G_i|`. A canonical policy is `\pi = (0.1, 0.7, 0.2)`.

**Falsifiable Criterion:** An optimization process governed by this ecology will achieve a higher maximum coherence `\max_{r \in W_t} C(r)` over time `t` than processes that sample exclusively from `G_{top}` (`\pi = (1,0,0)`) or uniformly from `W_t`.

## Philosophy
Progress is not the amplification of prior success, but the strategic cultivation of promising imperfection. The system's capacity to improve is maximized by focusing not on its perfected outputs or its absolute failures, but on the malleable frontier of its partial successes. It is a formal assertion that the future is discovered by interrogating that which can still be bent, not that which is already crystallized or entirely broken.

## Art
Do not worship the finished sword, nor obsess over the pile of cold slag. The shape of victory is found only in the glowing, yielding steel that is neither.