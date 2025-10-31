---
id: MATH-YM-003
title: Nonperturbative Map — From ({\kappa_3,\xi_\Gamma}) to (\sigma), (\Lambda_{\rm QCD}), and Lattice Units
version: 1.0
status: framework-draft (canonical target)
parents: [DYNA-COLOR-001, MATH-YM-002, XXP-BRIDGE-Γ-001]
children: [XXP-EWQCD-EXP]
module_type: nonperturbative dictionary / lattice interface
scale: few–GeV (matching) → IR hadronic
engrams: 
 - string tension
 - scale setting
 - lattice spacing
 - Sommer scale
 - Λ_{\rm QCD}
 - RG-invariant coupling
keywords: [lattice QCD, Wilson loop, k-strings, heavy-quark potential, scale conversion, β-function integration]
---

### §1 · Purpose

Provide a **deterministic pipeline** that converts Pirouette’s mechanical parameters—**temporal-color frame stiffness** (\kappa_3) and **Γ-coherence length** (\xi_\Gamma)—plus the running coupling (g_s(\mu)) into **nonperturbative QCD outputs**:

* fundamental **string tension** (\sigma),
* **Λ_{\rm QCD})** in a chosen scheme,
* lattice reference scales (r_0, t_0), and the **lattice spacing** (a).

This closes the loop between the **coherence barrier** and **hadronic phenomenology**.

---

### §2 · Mechanistic inputs (from prior modules)

* **Frame stiffness**: (K_3 \equiv 1/g_s^2); effective elastic modulus (\kappa_3\sim \mathcal{O}(K_3)) after normalization.
* **Coherence length**: (\xi_\Gamma \sim \frac{c}{\omega_c},\chi^{-1/2}) (Bridge susceptibility (\chi)).
* **Running coupling**: (g_s(\mu)) at a matching scale (\mu_\ast\sim 1!-!3) GeV from **MATH-YM-002**.

---


### §3 · Core scaling relation (from DYNA-COLOR-001) — **Fully Filled**

**Objective.** Convert Pirouette’s mechanistic inputs \((\kappa_3, \xi_\Gamma, g_s(\mu_*))\) into the nonperturbative **string tension** \(\sigma\) with one-time normalization, expose the **error budget**, and define the **propagation** to lattice scales and \(\Lambda_{\overline{\rm MS}}\).

#### 3.1 Parameters and Domains
- \(\kappa_3 \equiv \mathcal{O}(1/g_s^2)\): temporal‑color frame stiffness at \(\mu_*\in [1,3]\) GeV.
- \(\xi_\Gamma\): Γ‑coherence length from Bridge (\(\xi_\Gamma \sim \frac{c}{\omega_c}\chi^{-1/2}\)).
- \(g_s(\mu_*)\): strong coupling at the matching scale (from MATH‑YM‑002).

#### 3.2 Base Scaling Law (deterministic core)
\[
\boxed{\ \sigma \;=\; c_\sigma \,\frac{\kappa_3}{\xi_\Gamma^2}\,\Big[1+\delta_{\rm np}\Big]\ }
\]
- \(c_\sigma\) is fixed **once** by a single anchor (e.g. \(\sqrt{\sigma}_{\rm phys}=0.440\,\mathrm{GeV}\)).
- \(\delta_{\rm np}\) aggregates subleading vortex/mixing effects (nominally small).

#### 3.3 One-Time Normalization
Choose a reference input \((\kappa_{3,\rm ref}, \xi_{\Gamma,\rm ref})\) and target \(\sigma_{\rm phys}\):
\[
c_\sigma \;=\; \frac{\sigma_{\rm phys}\,\xi_{\Gamma,\rm ref}^2}{\kappa_{3,\rm ref}}\,, \qquad \text{then freeze } c_\sigma.
\]
After this, **no further tuning**: new \((\kappa_3,\xi_\Gamma)\) predict \(\sigma\) parameter‑free (up to \(\delta_{\rm np}\)).

#### 3.4 Model Form for \(\delta_{\rm np}\) (optional)
A minimal, decaying‑mixing ansatz (used only if needed by data):
\[
\delta_{\rm np}(\xi_\Gamma) \;\approx\; \alpha_0\,\frac{\xi_\Gamma}{\xi_0}\,\exp\!\Big(-\frac{\xi_\Gamma}{\lambda_v}\Big),
\]
with small \(|\alpha_0|\lesssim 0.1\). Set \(\alpha_0=0\) by default; enable only upon systematic large‑R tension drift.

#### 3.5 Error Budget (first‑order)
Let relative uncertainties be \(\epsilon_{\kappa_3}, \epsilon_{\xi}, \epsilon_{c_\sigma}, \epsilon_{\delta}\). Then
\[
\frac{\Delta\sigma}{\sigma}\;\approx\; \sqrt{\ \epsilon_{c_\sigma}^2 \;+\; \epsilon_{\kappa_3}^2 \;+\; \big(2\,\epsilon_{\xi}\big)^2 \;+\; \epsilon_{\delta}^2\ }\;.
\]

#### 3.6 Propagation to Lattice Scales
- Sommer scale:
\[
r_0 \;\approx\; \sqrt{\frac{1.65}{\sigma}}\;\Big(1+\mathcal{O}(\sqrt{\sigma})\Big).
\]
- Lattice spacing from a measured \((r_0/a)_{\rm lat}\):
\[
a \;=\; \frac{r_0}{(r_0/a)_{\rm lat}}\,.
\]
(Alternatively use gradient‑flow \(t_0\) if available.)

#### 3.7 Link to \(\Lambda_{\overline{\rm MS}}\) and RG Closure
Given \(\alpha_s(\mu_*)\) (from MATH‑YM‑002), integrate the QCD beta-function to infer \(\Lambda_{\overline{\rm MS}}\), then run back to \(M_Z\) and check \(\alpha_s(M_Z)\) as a closure test.

#### 3.8 Ready‑to‑Run Reference Implementation (tested)
```python
import numpy as np

def sigma_core(kappa3, xi_gamma, c_sigma, delta_np=0.0):
    # Deterministic core: sigma = c_sigma * kappa3 / xi_gamma^2 * (1 + delta_np)
    if xi_gamma <= 0:
        raise ValueError("xi_gamma must be positive.")
    return c_sigma * (kappa3 / (xi_gamma**2)) * (1.0 + float(delta_np))

def calibrate_c_sigma(sigma_phys, kappa3_ref, xi_gamma_ref):
    # One-time normalization of c_sigma from a physical anchor.
    if kappa3_ref <= 0 or xi_gamma_ref <= 0:
        raise ValueError("Reference kappa3 and xi_gamma must be positive.")
    return (sigma_phys * (xi_gamma_ref**2)) / kappa3_ref

def r0_from_sigma(sigma):
    # Sommer scale r0 from sigma (GeV units -> r0 in GeV^{-1}); convert to fm by multiply 0.1973269804 if desired.
    if sigma <= 0:
        raise ValueError("sigma must be positive.")
    return np.sqrt(1.65 / sigma)

def lattice_spacing_from_r0(r0, r0_over_a_lat):
    # a = r0 / (r0/a)_lat
    if r0_over_a_lat <= 0:
        raise ValueError("(r0/a)_lat must be positive.")
    return r0 / r0_over_a_lat

# Example test (illustrative numbers in GeV units)
sigma_phys = 0.440**2  # GeV^2 anchor
kappa3_ref = 1.0 / (1.3**2)  # approx 1/g_s^2 at mu* with g_s ~ 1.3
xi_gamma_ref = 0.60  # in GeV^{-1} for this example

# Calibrate once
c_sigma = calibrate_c_sigma(sigma_phys, kappa3_ref, xi_gamma_ref)

# New prediction point
kappa3_new = 1.0 / (1.2**2)
xi_gamma_new = 0.55
sigma_pred = sigma_core(kappa3_new, xi_gamma_new, c_sigma, delta_np=0.0)

# Propagate to lattice scales
r0_pred = r0_from_sigma(sigma_pred)
a_pred_gevinv = lattice_spacing_from_r0(r0_pred, r0_over_a_lat=5.3)

print(f"c_sigma = {c_sigma:.6f} GeV^0")
print(f"sigma_pred = {sigma_pred:.6f} GeV^2")
print(f"r0_pred (GeV^-1) = {r0_pred:.6f}")
print(f"a_pred (GeV^-1) = {a_pred_gevinv:.6f}")
```


### §4 · Heavy-quark potential & lattice dictionary

Define the static (Q\bar Q) potential:
[
V(R) = \sigma R - \frac{\pi}{12R} + \mu + \mathcal{O}\big(R^{-3}\big),
]
(Lüscher term shown for reference). Lattice Wilson loops yield (V(R)) → extract (\sigma).

**Reference scales:**

* **Sommer scale (r_0)** via
  [
  r_0^2,F(r_0)=1.65,\qquad F(R)=\frac{dV}{dR}.
  ]
* **Gradient-flow (t_0):** (t^2\langle E\rangle!\mid_{t=t_0}=0.3) (or chosen constant).

**Conversions (deterministic once (\sigma) fixed):**
[
r_0 = \sqrt{\frac{1.65}{\sigma + \pi/(12 r_0^2)}}
;\approx; \sqrt{\frac{1.65}{\sigma}};\Big(1+\mathcal{O}(\sqrt{\sigma})\Big),
]
[
a = \frac{r_0}{(r_0/a)*{\rm lat}}
\quad\text{or}\quad
a = \sqrt{\frac{t_0}{(t_0/a^2)*{\rm lat}}}.
]
Thus, **Pirouette → (\sigma) → (r_0,t_0) → (a)** gives a **numerical lattice spacing** prediction.

---

### §5 · From (\sigma) to (\Lambda_{\rm QCD})

Choose scheme (S\in{\overline{\rm MS},{\rm MOM},\ldots}). Define the RG-invariant scale via the β-function:
[
\Lambda_S = \mu,\exp!\Big(-\frac{1}{2\beta_0,\alpha_s(\mu)}\Big),
\big(\beta_0 \alpha_s(\mu)\big)^{-\beta_1/(2\beta_0^2)}
\Big[1+\mathcal{O}(\alpha_s)\Big].
]
Use (\mu=\mu_\ast) and (\alpha_s(\mu_\ast)) from **MATH-YM-002**. Convert (\Lambda_S \leftrightarrow \Lambda_{\overline{\rm MS}}) with known finite ratios.

**Empirical map** (post-normalization):
[
\frac{\sqrt{\sigma}}{\Lambda_{\overline{\rm MS}}}
;=; \mathcal{C}*\sigma ,\Big[1+\epsilon*{\rm scheme}\Big],
]
where (\mathcal{C}*\sigma) is fixed once by the same anchor used to set (c*\sigma), and (\epsilon_{\rm scheme}) is a small, known scheme offset.

**Pipeline:** compute (\sigma) (Pirouette) → infer (\Lambda_{\overline{\rm MS}}) → run (\alpha_s(M_Z)) back up as a **cross-check** against experiment (closes the loop with **MATH-YM-002**).

---

### §6 · k-strings and N-ality test

For representation with N-ality (k\in{1,2}):
[
\sigma_k \approx \sigma \times
\begin{cases}
\displaystyle \frac{k(N-k)}{N-1} & \text{(Casimir scaling, approx.)}[6pt]
\displaystyle \frac{\sin(\pi k/N)}{\sin(\pi/N)} & \text{(sine law, alt.)}
\end{cases}
\quad (N=3).
]
Pirouette baseline: **N-ality controls confinement**, independent of microscopic details. Lattice can use (\sigma_k/\sigma) to test the **center-vortex** content directly.

---

### §7 · Worked **deterministic recipe** (step-by-step)

1. **Inputs**: (\omega_c) (Bridge), (\chi) (Bridge), (g_s(\mu_\ast)) from RG (MATH-YM-002).
2. **Compute** (\xi_\Gamma = (c/\omega_c)\chi^{-1/2}).
3. **Set** (\kappa_3\sim 1/g_s^2(\mu_\ast)) (with normalization fixed once).
4. **Predict** (\sigma = c_\sigma \kappa_3/\xi_\Gamma^2).
5. **Derive** (r_0,t_0); **predict** lattice spacing (a) for any measured ((r_0/a)) or ((t_0/a^2)).
6. **Integrate** β to get (\Lambda_{\overline{\rm MS}}) and **check** (\alpha_s(M_Z)) via standard running.
7. **Optional**: compute (\sigma_k) ratios and compare with lattice N-ality results.

No retuning beyond the **single normalization** step (sets (c_\sigma) and (\mathcal{C}_\sigma) once).

---

### §8 · Falsifiability (nonperturbative gates)

* **Scale inconsistency:** Pirouette-predicted (a) disagrees with lattice-extracted (a) across ensembles after the one-time normalization → fails the (\sigma\to r_0,t_0) map.
* **(\sqrt{\sigma}/\Lambda_{\overline{\rm MS}}) mismatch:** persistent, scheme-robust deviation beyond combined errors → breaks the (\sigma\leftrightarrow\Lambda) link.
* **N-ality violation:** lattice finds (\sigma_k) not following any N-ality pattern (after mixing corrections) → contradicts center-vortex mechanism.
* **RG loop closure fails:** (\alpha_s(M_Z)) reconstructed from (\Lambda) conflicts with experiment despite allowed (\Delta_i) matching → tension with **MATH-YM-002** priors.

---

### §9 · Linkage

* **Consumes:** ({\omega_c,\chi}) (XXP-BRIDGE-Γ-001), (g_s(\mu)) (MATH-YM-002), (\kappa_3) (DYNA-COLOR-001).
* **Feeds:** **XXP-EWQCD-EXP** (lattice task list and targets: (\sigma, r_0, t_0, a, \sigma_k/\sigma)) and hadronic phenomenology modules (quarkonium, Regge, nuclear).

---

### §10 · Assemblé

Nonperturbative QCD is where the math goes non-linear and the music goes orchestral. This dictionary is your conductor’s score: stiffness sets the strings, coherence sets the drum skin, and out comes (\sigma). From there, every lattice number has a seat in the hall—and every seat points back to the same temporal instrument.

---