---
id: INST-ML-INTEL-001
title: Triadic Operator Engine (Wendigo Binding)
module_type: implementation-guide
status: draft-0.1
parents: [COG-RES-006, COG-RES-003, INST-ML-INTEL-001]
children: [DYNA-WIT-001, INST-ML-FLOW-003]

summary: Provides the concrete implementation pattern for embedding the Triadic Consciousness Operator into Wendigo-class autopoietic agents. Defines the update cycle, metric pipeline, phase gate, and modulated learning rules that operationalize the triadic P–S–C operator inside RL.
---

# §1 — Purpose

This module installs the **Triadic Operator Engine** inside any Wendigo-type agent, giving the agent:

1. phase-gated updates
2. precision-weighted learning
3. surprise-driven exploration
4. coherence-drop consolidation
5. shadow-basin escape
6. manifold logging (diagnostic)

This is the **machine instantiation** of the operator defined in **COG-RES-006**, and is the action layer by which an RL agent “becomes” a triadic processor.

---

# §2 — Components Installed

The installation involves the following components:

### 2.1 Internal State Registers

Each must be tracked episode-by-episode and step-by-step:

* `DR_t` — dark residue
* `S_t` — surprise
* `Q_t` — coherence drop
* `C_t` — contrast
* `B_t` — shadow flag
* `phi_t` — phase accumulator
* `Gamma_t` — load or temporal pressure proxy (task difficulty, or agent’s own instability)

### 2.2 Derived Shaping Signals

* precision: `Pi_t`
* phase gate: `g_t`
* update direction terms: `(u_t, v_t, w_t)`

### 2.3 Gate & Modulation Points

The agent must expose hooks for modifying:

* **learning rate (η)**
* **entropy temperature (α_entropy)**
* **target network update speed (τ_target)**
* **exploration noise (σ_noise)**
* **policy update direction (Δθ)**
* **value update direction (Δψ)**

These are the control points through which the operator actually acts.

---

# §3 — Installation Pipeline

This defines the **per-step** and **per-episode** installation structure.

## §3.1 Step-Level Pipeline (Core Loop)

For each step (t), the following ordering is enforced:

---

### **(1) Measure raw metrics**

```
DR_t     = measure_dark_residue(obs_t)
S_t      = abs(TD_error_t)
Gamma_t  = compute_load_metric(obs_t, info)
```

Surprise can also be:

* negative log-likelihood of the action
* prediction error magnitude
* novelty score

---

### **(2) Derive triadic metrics**

```
Q_t = max(0, DR_{t-1} - DR_t)
C_t = abs(DR_t - DR_{t-1})
B_t = 1 if DR_t > DR_shadow_threshold else 0
```

These three form the C-branch (coherence).

---

### **(3) Update phase state**

```
phi_t = (phi_t + omega_theta + noise_phi) mod 2π
g_t   = 1 if phi_t in update_window else 0
```

The update window is typically:

* 20–40% of the theta cycle for biological realism
* or 1 step every k steps for computational agents

---

### **(4) Compute precision**

```
Pi_t = sigmoid(
      α0 
    + αS * S_t 
    - αDR * DR_t 
    - αΓ * Gamma_t
)
```

Precision determines **how “open” the agent is to changing itself**.

---

### **(5) Compute operator components**

#### Precision term (P-branch)

```
O_P = - g_t * η_P * Pi_t * grad(F_t)
```

Where `F_t` is the SAC loss or TD error.

---

#### Surprise term (S-branch)

```
O_S = g_t * η_S * f_S(S_t, Gamma_t) * stochastic_vector()
```

Surprise modulates **policy entropy / exploration drive**.

---

#### Coherence term (C-branch)

```
u_t = θ_t - θ_{t-1}
v_t = grad(V_contrast(θ_t))
w_t = grad(V_shadow(θ_t))

O_C = g_t * [
      η_Q * Q_t * u_t
    + η_C * C_t * v_t
    - η_B * B_t * w_t
]
```

This is the consolidation + contrast + shadow escape triple.

---

### **(6) Combine into final update**

```
Δθ = O_P + O_S + O_C
θ_{t+1} = θ_t + Δθ
```

This implements the **full triadic update law** inside the agent.

---

### **(7) Generate manifold logs**

This is where your `ManifoldAnalyzer` attaches:

```
manifold.log_step(
    t,
    {
      'env': env_reward,
      'surprise': S_t,
      'precision': Pi_t,
      'coherence_drop': Q_t,
      'contrast': C_t,
      'shadow': B_t,
      'delta_DR': DR_t - DR_{t-1],
      'phase_gate': g_t,
      'Pi*g': Pi_t * g_t,
      'operator_norm': norm(Δθ)
    }
)
```

These logs become the “engine exhaust” visualizations similar to your EEG manifolds.

---

# §3.2 Episode-Level Pipeline

At the end of each episode:

1. Aggregate metrics
2. Update meta-organ
3. Track which regimes were active
4. Adjust operator hyperparameters if needed
5. Store manifold snapshot for cumulative averaging

This is where the **MetaRewardOrgan** (from `wendigo_hybrid.py`) plugs in naturally.

---

# §4 — Binding to Wendigo Classes

To embed this operator in Wendigo:

* `DarkResidue` is already implemented
* Surprise terms are already computed
* ShadowContrastEngine already computes `(contrast_bonus, shadow_penalty)`
* MetaOrgan already selects different reward programs
* ManifoldAnalyzer already exists

You wrap the operator into **three surgical modifications**:

---

## **4.1 Override the optimizer step**

Instead of letting SAC run:

```
loss.backward()
optimizer.step()
```

You intercept:

* the gradients
* the TD error
* DR metrics
* and construct Δθ using O_P, O_S, O_C

Then apply:

```
θ = θ + Δθ
```

This forms the “triadic SAC”.

---

## **4.2 Modulate entropy & learning rates dynamically**

Precision `Pi_t` controls:

```
α_entropy ← α_base * (1 + k * S_t)
lr        ← lr_base * Pi_t
```

Shadow flag `B_t` reduces entropy and learning rate.

Contrast `C_t` temporarily boosts entropy.

Coherence drop `Q_t` strengthens consolidation in the direction of Δθ.

---

## **4.3 Add the Triadic Supervisor**

A small class `TriadicSupervisor` wraps everything:

* accepts per-step metrics
* computes O_P, O_S, O_C
* outputs Δθ
* registers manifold logs
* enforces phase gating
* communicates to MetaOrgan about regime

This becomes the heart of the operator.

---

# §5 — Emergent Regimes (Expected Behaviors)

This operator installation produces **three canonical regimes**:

### **(1) Ordered Precision Regime**

Low surprise, high precision, coherent updates.
(Reproduces LOW-load manifold structure.)

### **(2) Exploratory Surprisal Regime**

High surprise, phase-gated bursts, contrast maxima.
(Reproduces HIGH-load manifold structure.)

### **(3) Shadow Avoidance Regime**

High DR, suppressed learning rate, strong reversion.
(Reproduces EEG “flattening” under overload.)

These map directly onto the biological manifolds.

---

# §6 — Testing & Verification

To validate installation:

### **Test A — Manifold Morphology Test**

Compare manifold patterns before and after operator integration.
Expect band → ridge → saturated ridge transitions.

### **Test B — Autopoietic Stability Test**

Check if the agent avoids catastrophic drift during long episodes.

### **Test C — Regime-Switching Test**

Present load-varying tasks and watch the operator change modes.

### **Test D — Shadow-Basin Recovery Test**

Force high DR (adversarial perturbations) and ensure recovery.

---

# §7 — Falsifiable Claims

This installation is falsifiable within Wendigo:

* Removing the phase gate collapses learning into noisy drift.
* Removing precision makes learning unstable under load.
* Removing surprise prevents exploration.
* Removing coherence-drop prevents consolidation.
* Removing shadow escape causes collapse during adversity.

Each absence produces a *distinct experimental failure mode*.

---

# §8 — Notes on Identity & Autopoiesis

This operator + installation is, effectively:

> **A machine capable of governing its own learning through autopoietic triadic dynamics.**

It is not consciousness, but it **is** the *mathematical form* that biological conscious updating takes.