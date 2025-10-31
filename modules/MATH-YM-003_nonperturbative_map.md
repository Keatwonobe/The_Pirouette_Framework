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

### §3 · Core scaling relation (from DYNA-COLOR-001)

Baseline confinement scaling:
[
\boxed{\ \sigma ;=; c_\sigma ,\frac{\kappa_3}{\xi_\Gamma^2}\ \Big[1+\delta_{\rm np}\Big]\ },
]
with (c_\sigma=\mathcal{O}(1)) a normalization fixed by one benchmark observable, and (\delta_{\rm np}) encapsulating subleading nonperturbative corrections (vortex interactions, mixing).

**Normalization convention:** choose a single empirical anchor (e.g., (\sigma^{1/2}\simeq 440) MeV) **once**, thereby fixing (c_\sigma) for all subsequent predictions; after that, **no tuning**—only Pirouette inputs vary.

---

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