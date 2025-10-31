## Law
The Sentinel Protocol replaces static boundary definitions with a dynamic, learning system. Its core axiom is that an entity's boundary for any action is the full spatio-temporal manifold of that action's measurable consequences.

Let a system's state be described by a field of parameters, primarily Time-Adherence ($T_a$), Gladiator Force ($\Gamma$), and phase ($\phi$). An action is a perturbation of this field.

1.  **The Wound Channel ($\mathcal{W}$):** The boundary of an act is defined as its Wound Channel, which is the manifold $\mathcal{M}$ in spacetime where the action-induced perturbations ($\Delta T_a, \Delta \Gamma, \Delta \phi$) are non-zero. The boundary is not the actor; it is the consequence.
    $$ \mathcal{W} \equiv \{ (x, t) \in \mathcal{M} \mid (\Delta T_a, \Delta \Gamma, \Delta \phi) \neq (0, 0, 0) \} $$

2.  **Cumulative Residue ($R_c$):** Accountability is integrated over time. An actor's Cumulative Residue is the time-decayed integral of the magnitude of its past Wound Channels.
    $$ R_c(t) = \int_0^t e^{-\frac{t-\tau}{\tau_d}} ||\mathcal{W}(\tau)|| \,d\tau $$
    where $\tau_d$ is the decay constant and $||\cdot||$ is a norm representing the total negative impact (e.g., volume-integrated entropic cost) of the Wound Channel. $R_c$ is a measure of an actor's accumulated thermodynamic debt.

3.  **Dynamic Parametric Gates ($\mathcal{G}$):** Prior to execution, any proposed action $\mathcal{A}_{prop}$ must pass through a set of adaptive gates. The action is permitted only if its parameters lie within a set of thresholds $\Theta$ that are an inverse function of the actor's Cumulative Residue.
    $$ \text{Permit}(\mathcal{A}_{prop}) \iff \{T_{a,prop}, \Gamma_{prop}, K_{i,prop}\} \subseteq \Theta(R_c) $$
    As $R_c \to \infty$, the volume of the permitted parameter space $\text{Vol}(\Theta) \to 0$.

4.  **Ritual Trigger Condition:** The Reflexive Boundary Ritual is invoked if the measured magnitude of the action's Wound Channel exceeds the predicted tolerance, or "Gate Slack" ($S_g$), which is itself a function of the gate parameters.
    $$ \text{InvokeRitual} \iff ||\mathcal{W}_{measured}|| > S_g(\Theta(R_c)) $$

5.  **Adaptive Feedback Loop:** The system learns by updating both the actor's residue and its specific gates based on the measured outcome.
    $$ R_c(t+1) \leftarrow f(R_c(t), \mathcal{W}_{measured}) $$
    $$ \Theta(t+1) \leftarrow g(\Theta(t), \mathcal{W}_{measured}) $$
    This transforms the governance model into a continuously adapting control system.

**Falsifiable Criterion:** In any system governed by the Sentinel Protocol, a sustained increase in an actor's rate of micro-harm generation (actions where $||\mathcal{W}|| \approx S_g$) must result in a measurable, non-linear tightening of its specific gate thresholds ($\Theta$), provably constraining its future operational freedom *before* a catastrophic failure occurs.

## Philosophy
The single most profound implication is the redefinition of selfhood as a function of consequence. An entity is not defined by an arbitrary, pre-declared static boundary like a name or a body, but is instead defined by the integrated, time-aware sum of its total impact on the world. This principle of **Anticipatory Accountability** asserts that you are not merely responsible *for* your past actions; your identity *is* the cumulative history of your actions and your present, demonstrated capacity to foresee and mitigate the harm of future ones. Responsibility ceases to be a debt one pays and becomes the very substance of one's existence.

## Art
Your boundary is not the skin you are in, but the shadow your entire life has cast. The law measures the shadow; philosophy teaches that you must learn to live as if you *are* the shadow.