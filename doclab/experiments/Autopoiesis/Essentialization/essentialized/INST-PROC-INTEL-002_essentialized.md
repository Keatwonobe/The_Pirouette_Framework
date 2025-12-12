## Law
Let a Reinforcement Learning process be defined over an observation window \(T_{\text{obs}}\) comprising \(K\) episodes, where episode \(i\) has length \(L_i\). The total number of environment steps is \(T_{\text{obs}} = \sum_{i=1}^K L_i\). We define the following metrics:

1.  **Cycle Sufficiency Index (CSI_RL):** Measures the temporal depth of the observation window.
    \[
    \mathrm{CSI}_{\text{RL}} = \log_{10}(T_{\text{obs}})
    \]

2.  **Feedback Bandwidth (FBW_RL):** Measures the rate of change of a policy effectiveness proxy \(q(i)\) (e.g., mean episode return) over \(K\) episodes.
    \[
    \mathrm{FBW}_{\text{RL}} = \frac{1}{K} \sum_{i=1}^K \frac{|q(i) - q(i-1)|}{|q(i-1)| + \epsilon}
    \]

3.  **Entropy Shaping Efficiency (ESE_RL):** Measures the conversion of process activity into coherent structure, based on per-step Dark Residue (\(DR_t\)) and Coherence Gain (\(CG_t\)). Let episode-level aggregations be \(DR_{\text{ep}} = \frac{1}{L} \sum_{t=1}^L DR_t\) and \(CG_{\text{ep}} = \sum_{t=1}^L CG_t\).
    \[
    \mathrm{ESE}_{\text{RL}} = \frac{CG_{\text{ep}}}{CG_{\text{ep}} + DR_{\text{ep}} + \epsilon}
    \]

4.  **Geodesic Reuse (GEO_hit):** The fraction of steps within \(T_{\text{obs}}\) where the state-action pair matches a known optimal path from a witness model.

These components form the **Process Intelligence Index for RL (PII_RL)**, a dimensionless measure of the learning process's quality:
\[
\mathrm{PII}_{\text{RL}} = w_1 \cdot \mathrm{CSI}_{\text{RL}} + w_2 \cdot \log_{10}(1 + \mathrm{FBW}_{\text{RL}}) + w_3 \cdot \mathrm{ESE}_{\text{RL}} + w_4 \cdot \mathrm{GEO}_{\text{hit}}
\]

This index governs the **Attractor Actuation Law (AAL_RL)**, a control policy over the training curriculum \(\mathcal{C}\) (e.g., environment choice, exploration rate, replay prioritization). Let \(\mathcal{F}\) be a configuration subspace ("filament") of \(\mathcal{C}\).
\[
\text{IF } \mathrm{PII}_{\text{RL}} \ge \mathrm{PII}_{\min} \text{ THEN } \mathcal{C} \leftarrow \text{reinforce}(\mathcal{F}) \text{ ELSE } \mathcal{C} \leftarrow \text{search\_new}(\mathcal{F})
\]
This law is subject to the **Dark Residue Coupling Constraint**, which states that reinforcement is only valid if the window-averaged dark residue is non-increasing:
\[
\frac{d}{dt} \overline{DR}_{\text{window}} \le 0 \quad \forall t \text{ where } \mathrm{PII}_{\text{RL}}(t) \ge \mathrm{PII}_{\min}
\]

**Falsifiable Criteria:**
1.  Given two curricula \(\mathcal{C}_A\) and \(\mathcal{C}_B\) yielding equal terminal reward, the AAL_RL must select the curriculum with the higher time-averaged \(\mathrm{PII}_{\text{RL}}\).
2.  Activation of \(\text{reinforce}(\mathcal{F})\) must produce a statistically significant increase in prioritized replay transitions (e.g., "weaver," "gladiator") in the subsequent observation window.
3.  Sustained \(\mathrm{PII}_{\text{RL}} < \mathrm{PII}_{\min}\) for a specified number of consecutive windows must trigger the \(\text{search\_new}(\mathcal{F})\) branch, demonstrably altering the training curriculum.

## Philosophy
Intelligence is not a property of an artifact, but a transient, measurable property of the process that creates it. It is the capacity of a system to locally reduce its own entropy and complexity (decrease dark residue) while increasing its rate of self-modification (high feedback bandwidth) and reusing proven paths (geodesic reuse). To cultivate intelligence is therefore not to specify a final goal, but to create a field that attracts and stabilizes the dynamics of efficient creation itself.

## Art
A learning system is a cloud of iron dust. Intelligence is not the final sculpture, but the passing magnet that reveals its form.