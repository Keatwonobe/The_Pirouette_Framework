## Law
Let the state of a biological system be defined by a vector `X(t) = [C(t), B(t)]`, where `C(t)` is endogenous adaptive capacity (Coherence) and `B(t)` is allostatic load (Burden). The system's objective is to maximize `C(t)` while minimizing `B(t)`.

System dynamics are governed by a controlled hormetic process. A therapeutic stressor, `σ(t) ≥ 0`, is applied to the system. The evolution of the state is described by the coupled differential equations:

1.  `dC/dt = α·σ(t)·(1 - B(t)/B_max) - β·σ(t)² - γ·C(t)`
    *   `α·σ(t)`: Adaptive response to stress. This term is attenuated as Burden `B(t)` approaches a maximum tolerance `B_max`.
    *   `-β·σ(t)²`: Damage from excessive stress.
    *   `-γ·C(t)`: Atrophic decay in the absence of stress.

2.  `dB/dt = δ·σ(t) - ε·B(t) + Ση_i·A_i`
    *   `δ·σ(t)`: Load induced by the stressor.
    *   `-ε·B(t)`: Natural homeostatic recovery.
    *   `Ση_i·A_i`: Load reduction from specific restorative interventions (e.g., sleep, nutrition).

The system is observable through a measurement vector `Y(t) = [M_obj(t), M_subj(t)]`, where `M_obj` is an objective biomarker (e.g., Resting Heart Rate, where `M_obj ∝ B/C`) and `M_subj` is a subjective report of systemic wellness (e.g., a Likert scale "flow" score, where `M_subj ∝ C/B`).

The core control law is to modulate the stressor `σ(t)` to maintain a state of optimal adaptation. Let `Δσ` be the change in stress for the next time interval. The control policy is:

`Δσ(t+1) = f(∇M_obj(t), M_subj(t))`

*   IF `∇M_obj(t) ≤ 0` (objective markers stable or improving) AND `M_subj(t) > θ` (subjective state is above a wellness threshold `θ`), THEN `Δσ ≥ 0` (Maintain or increase challenge).
*   IF `∇M_obj(t) > 0` OR `M_subj(t) ≤ θ`, THEN `Δσ < 0` (Reduce challenge).

**Falsifiable Criterion:** A system governed by this dual-feedback control law will converge to a state of high `C` and low `B` more rapidly and with lower risk of systemic failure (`B(t) > B_max`) than a system controlled by a pre-scheduled `σ(t)` or by a law referencing only `M_obj` or `M_subj` in isolation.

## Philosophy
The subjective, first-person experience of wellness is not an epiphenomenon of health, but a computationally necessary input for the optimal regulation of a complex biological system. In the cybernetics of healing, conscious feeling is revealed to be a data stream as critical and non-redundant as any objective biomarker, collapsing the Cartesian partition between the felt self and the functioning body into a single, indivisible control loop.

## Art
A bell is struck by crisis. The physics of its vibration is the law of its recovery. But to find its truest resonance, the bell must listen not only to the sound it makes in the world, but to the feeling of the ringing within itself.