---
id: INST-SAND-001
title: Sand Hemispheric Agent (Navigator–Sampler Brain)
Version: 0.1.0
Status: Experimental / Engram seed
Parents:

 INST-CORE-000 (generic agent scaffolding)
 DYNA-DR-GAMMA-001 (Dark Residue & Temporal Pressure)
 MATH-LAGRANGIAN-Γτ-001 (K_τ − V_Γ lagrangian)
Children (planned):

  INST-SAND-PEND-001 (Pendulum brain)
  INST-SAND-ANT-001 (Ant brain)
  INST-SAND-AUTO-001 (autopoietic hyper-param scheduler)
---

### §1. Intent

**Purpose:**
Use the fitted Sand landscape as a **drop-in “brain manifold”** for RL agents. Each RL step is not just “state→action,” but “state→(hemisphere, basin, operator)→action / learning rule.”

**Core idea:**

1. Sand Agent already samples a **coherence state**:
   [
   { \text{DR}, S, \Gamma, \pi, O_P, O_S, O_C, |O|, \text{strategy}, \text{hemisphere}, \text{basin} }
   ]
2. Treat that as a **meta-state** coupled to any environment (Pendulum, Ant, …).
3. Map those meta-states into **control knobs** for the RL algorithm:

   * exploration vs exploitation
   * learning rate / target update stiffness
   * entropy bonus / noise scale
   * when to freeze or store a policy snapshot
4. Preserve **interhemispheric transfers** and basin topology so the RL agent literally “thinks with” this two-hemisphere field.

---

### §2. Engram: Structural Definition

**Engram label:** `ENGRAM:SAND_BRAIN_CORE`

**State components (per time-step t):**

* `H_t ∈ {left, right}` — hemisphere
* `B_t ∈ {0,…,6}` — basin ID
* `strategy_t ∈ {navigator, sampler}`
* `DR_t ∈ [0,1]`
* `S_t ≥ 0`
* `Γ_t ∈ [0,2]`
* `π_t ∈ (0,1)` — precision
* `O_t = (O_P, O_S, O_C)` — triadic operator
* `||O_t||` — operator magnitude

**Dynamics prototype:**

* `(H_t, B_t)` follow the empirically measured **transition kernel** from your landscape (including ~50% cross-hemispheric transfers).
* Within a basin, `DR, S, Γ, π, O` are sampled from the fitted distributions per basin & hemisphere (using the CSV or a small conditional VAE later).

**Interpretation:**

* High-Γ, high-DR, high-π, navigator-heavy hemisphere ≈ **stability / consolidation mode**.
* More moderate Γ, higher S, more sampler weight hemisphere ≈ **exploratory / remapping mode**.
* `O_P` biases **policy stability**, `O_S` biases **curiosity / surprise-seeking**, `O_C` biases **coherence / pruning**; `||O||` is “how hard the brain pushes” this step.

---

### §3. RL Interface Spec

We define a minimal interface so any RL script can mount this brain.

**Inputs to Sand brain at step t:**

* Environment state `s_t` (raw or encoded)
* Reward `r_t`
* Episode time `t`, global step `k`
* Current policy summary (optional): e.g. running DR, success rate, etc.

**Outputs from Sand brain:**

1. **Mode selection**

   * `hemisphere_t, basin_t, strategy_t`

2. **Control knobs**
   Suggested default mappings:

   * **Exploration temperature**
     [
     \text{temp}_t = f_T(\Gamma_t, S_t) \quad \text{(higher Γ/S → higher temp / noise)}
     ]
   * **Learning rate multiplier**
     [
     \eta_t = f_\eta(\pi_t, DR_t) \quad \text{(higher π & DR → lower LR; consolidation)}
     ]
   * **Entropy bonus / KL weight**
     [
     \beta^\text{entropy}*t = f*\beta(O_S, O_C)
     ]
   * **Snapshot / checkpoint gate**
     If `||O_t||` above threshold and DR dropping, trigger “save this policy as a basin exemplar.”

3. **Meta-labels (for logging)**

   * `brain_mode_t` ∈ {“left-navigator”, “left-sampler”, “right-navigator”, …}
   * `transfer_event_t` ∈ {none, L→R, R→L}

**Operational rule of thumb:**

* **Navigator hemisphere:** depress exploration, shrink LR, strengthen value update; treat as “exploit current good basin.”
* **Sampler hemisphere:** raise exploration, enlarge LR (or TD λ), push replay to emphasize novel transitions.

This keeps the **chirality**: one side stabilizes, the other perturbs.

---

### §4. Minimal Implementation Plan

**Phase 1 – Offline brain, online body**

1. Use `sand_landscape_incremental.csv` as a huge prior and build a tiny **`SandBrainSampler` class**:

   * loads a compact KDE / histogram for `(H, B, strategy, DR, S, Γ, π, O)`
   * exposes `.step()` → returns a new Sand state following empirical transition rules (including hemisphere transfers).

2. Wrap existing RL agents (Pendulum, Ant) with a **BrainAdapter**:

   ```pseudo
   for each env step t:
       sand_state = sand_brain.step()
       knobs = map_sand_to_hyperparams(sand_state)
       action = policy.act(s_t, temp=knobs.temp)
       loss = compute_loss(..., entropy_weight=knobs.beta_entropy)
       optimizer.lr = base_lr * knobs.lr_mult
       update(loss)
   ```

3. Log `(sand_state, env_state, reward)` triples to see where each task likes to live in the coherence landscape.

**Phase 2 – Online coupling**

* Learn a small mapping from env features → *preferred* Sand basins, so the RL agent can “steer itself” into hemispheric modes (e.g., struggle → sampler; plateau → navigator).

**Phase 3 – Autopoiesis**

* Let the Sand brain not only modulate hyper-params but **write back** into its own basin prior (slightly reweight basins that correlate with high long-term reward), turning it into a **self-tuning meta-brain**.

---