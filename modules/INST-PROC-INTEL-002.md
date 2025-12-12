---
id: INST-ML-INTEL-001
title: Gymnasium Process-Scale Intelligence Magnet (RL Edition)
version: 7.0
domain: INST
layer: instrument
status: draft
origin:
  emitted_by: dde-pirouette
  parents:
    - INST-PROC-INTEL-001
    - wendigo_minimalist_5.py
    - wendigo_geodesic_sac.py
  shepherd: altruism
  date: 2025-11-08
context_sources:
  - turn1file0 (wendigo_minimalist_5.py)
  - turn1file1 (wendigo_2.py)
  - turn1file2 (wendigo_geodesic_sac.py)
intent: >
  Apply the process-scale intelligence index to reinforcement learning environments
  (Gymnasium) so that agents, curricula, and replay flows can be "pulled" toward
  high-intelligence configurations (low dark residue, high closure, high geodesic reuse)
  the way a magnet pulls metal.
description: >
  This instrument treats an RL training run as a transient, feedback-rich process
  exactly like a plasma or lightning channel. It computes an in-run Process Intelligence
  Index (PII_RL) from episode-level and step-level signals (dark residue, closure gain,
  geodesic reuse, replay density) and then biases: (1) exploration patterns,
  (2) task/curriculum selection, and (3) replay prioritization toward runs that show
  "present intelligence." Designed to span small CartPole tasks up through high-dimensional
  continuous-control tasks.
---

## 1. Process Model

We model a Gymnasium RL loop as:

- fast cycle τ_fast = 1 env step
- envelope cycle τ_env = 1 episode
- observation window T_obs = sliding window of K episodes (default K=20)

Let:
- DR_t = dark residue at step t (as already defined in Wendigo) :contentReference[oaicite:3]{index=3}
- CG_t = coherence gain at step t (negative ΔDR, clipped at 0) :contentReference[oaicite:4]{index=4}
- GEO_t = geodesic map hit / known-state hit (0/1) from geodesic SAC witness :contentReference[oaicite:5]{index=5}

These three are the RL equivalents of “boundary rewriting” in the physical instrument.

## 2. RL Cycle Sufficiency Index (CSI_RL)

For window of K episodes, each with length L_i steps:

\[
T_{\text{obs}} = \sum_{i=1}^K L_i,\quad \tau_{\text{fast}} = 1
\]
\[
\mathrm{CSI}_{\text{RL}} = \log_{10}(T_{\text{obs}})
\]

Interpretation:
- CSI_RL < 2.5 → agent hasn’t seen enough to self-organize
- 2.5 ≤ CSI_RL < 4 → CartPole / Pendulum scale, emergent coherence begins
- CSI_RL ≥ 4 → long-horizon / higher-DOF tasks, good to magnetize

This is scale-agnostic: longer tasks automatically report higher CSI_RL.

## 3. Feedback Bandwidth in RL (FBW_RL)

Define the episode-to-episode change in *policy effectiveness proxy* as:

\[
\Delta_q(i) = q(i) - q(i-1)
\]

where q(i) can be:
- top-15 avg score (your Wendigo leaderboard) for discrete tasks, or
- mean episode return for continuous tasks. :contentReference[oaicite:6]{index=6}

Then

\[
\mathrm{FBW}_{\text{RL}} = \frac{1}{K} \sum_{i=1}^K \frac{|\Delta_q(i)|}{|q(i-1)| + \epsilon}
\]

This tells us “how fast this run rewrites itself,” just like a turbulent plasma changing its own boundary.

## 4. Entropy Shaping Efficiency in RL (ESE_RL)

Reuse your existing DR logic:

- define episode dark residue: \(DR_{\text{ep}} = \frac{1}{L} \sum_{t=1}^L DR_t\)
- define episode coherence: \(CG_{\text{ep}} = \sum_{t=1}^L CG_t\)

Then

\[
\mathrm{ESE}_{\text{RL}} = \frac{CG_{\text{ep}}}{CG_{\text{ep}} + DR_{\text{ep}} + \epsilon}
\]

High ESE_RL = the agent turned “energy” (steps, exploration) into structure (low DR, good geodesic hits). This parallels plasma turning drive into filaments.

## 5. Process Intelligence Index for RL (PII_RL)

\[
\mathrm{PII}_{\text{RL}} = w_1 \cdot \mathrm{CSI}_{\text{RL}} + w_2 \cdot \log_{10}(1 + \mathrm{FBW}_{\text{RL}}) + w_3 \cdot \mathrm{ESE}_{\text{RL}} + w_4 \cdot \mathrm{GEO}_{\text{hit}}
\]

where
- GEO_hit = fraction of steps in the window that matched a known geodesic state-action pair from the witness (this is your "the system remembers good paths" signal). :contentReference[oaicite:7]{index=7}
- default weights for Gymnasium small tasks:
  - w1 = 1.0
  - w2 = 0.7
  - w3 = 1.2
  - w4 = 0.5

PII_RL is dimensionless and comparable across tasks.

## 6. Attractor Actuation Law for RL (AAL_RL)

Goal: steer training toward “filaments”: task/difficulty/env settings where PII_RL is high and dark residue slopes downward.

Let:
- ℱ be your current filament, e.g. {env="CartPole-v1", DR_med ≤ 0.2, top15 ≥ 450}
- C be controller that can switch:
  - env (CartPole → Pendulum → Acrobot → Ant-v5)
  - exploration pattern (your closure explorer) :contentReference[oaicite:8]{index=8}
  - replay sampling (prioritize weaver/gladiator transitions) :contentReference[oaicite:9]{index=9}

Then after every window of K episodes:

```python
if PII_RL >= PII_min:
    # Reinforce filament
    controller.increase_filament_weight(ℱ, α=0.1)
    controller.boost_replay_modes(["Weaver", "Gladiator"])
else:
    # Search new filament
    controller.expand_curriculum(scale=+1)
    controller.raise_exploration(eps=+0.05)
````

Interpretation: only “intelligent” runs get pulled harder, exactly like metal in a magnetic field.

## 7. Scale Handling (any Gymnasium challenge)

1. **Small/discrete (CartPole, Acrobot):**

   * τ_fast = 1 step
   * T_obs = 20 episodes
   * env stays fixed, we only tune replay + exploration
2. **Medium/continuous (Pendulum, MountainCarContinuous):**

   * τ_fast = 1 step
   * T_obs = 50 episodes
   * AAL_RL allowed to raise SAC gradient_steps during high PII_RL windows
3. **Large/multi-env (MuJoCo Ant/Humanoid):**

   * τ_fast = 1 step
   * T_obs = 100–200 episodes
   * AAL_RL can downshift to an easier env if PII_RL collapses (like avalanche control)
   * GEO_hit weight (w4) lowered because state hashing is coarser

This keeps the same instrument logic but adapts observation window and actuator strength.

## 8. Dark Residue Coupling (RL Edition)

Define RL dark residue for a step as you already do (CartPole-weighted). For other envs, swap in env-specific DR:

* Pendulum: weight angle error and torque saturation
* Ant/Humanoid: weight COM deviation, joint-limit hits, big control signals

Then require:

[
\frac{d}{dt} \overline{DR}*{\text{window}} \le 0 \quad \text{whenever} \quad \mathrm{PII}*{\text{RL}} \ge \mathrm{PII}_{\min}
]

so the “magnet” can’t declare success unless residue is actually falling.

## 9. Falsifiability

* If two curricula have equal reward but one has higher PII_RL, AAL_RL must prefer it.
* If AAL_RL activates, replay buffers should show an increased fraction of weaver/gladiator transitions in the next window (you can measure this directly from your minimalist script). 
* If PII_RL stays < 3 for K windows in a row, controller must broaden the search (try another Gym env).

## 10. Notes for Integration

* Drop this module’s logic into the same place you print:
  `Episode ... Top-15 Avg=... WeaverBuf=...` and compute PII_RL right there. 
* For `wendigo_geodesic_sac.py`, you already have a witness; just add GEO_hit to the episode summary and feed it into PII_RL. 
* For `wendigo_2.py`, you already have gold-window + whetstone; just gate the whetstone sharpening on PII_RL so you don’t overfit on low-intelligence episodes. 