---
id: MATH-YM-002
title: Running & Barrier Matching for ({g',g,g_s})
version: 1.0
status: framework-draft (canonical target)
parents: [MATH-YM-001, DYNA-WEAK-001, DYNA-QED-005, XXP-BRIDGE-Γ-001, MATH-Γ-007]
children: [DYNA-COLOR-001, XXP-EWQCD-EXP]
module_type: renormalization & scale matching
scale: IR → (\mu_c\equiv \hbar\omega_c/c^2) (coherence barrier) → UV (barrier-regulated)
engrams: [β-functions, finite matching, stiffness dictionary, scheme choice, thresholds]
keywords: [Yang–Mills running, electroweak mixing, QCD coupling, finite counterterms, unification patterns]
---

### §1 · Purpose

Provide the **RG flow** and **finite matching** that connect Pirouette’s **frame-stiffness couplings at the coherence barrier** to **measured low-energy couplings**:
[
{g'(\mu),,g(\mu),,g_s(\mu)}\quad \leftrightarrow \quad
{K_1,,K_2,,K_3}\ \text{at}\ \mu=\mu_c,
]
where (K_i\equiv 1/g_i^2) are stiffnesses of the clock (U(1)(_Y)), triad (SU(2)(_L)), and temporal-color (SU(3)(_c)) frames.

---

### §2 · Definitions & scheme

* **Barrier scale:** (\displaystyle \mu_c = \frac{\hbar,\omega_c}{c^2}), with (\omega_c=\sqrt{m_H m_\Gamma},c^2/\hbar) from **XXP-BRIDGE-Γ-001**.
* **Scheme:** (\overline{\text{MS}}), SM field content below (\mu_c).
* **Normalizations:**

  * (g_1) is GUT-normalized hypercharge, (g'=\sqrt{\tfrac{3}{5}},g_1).
  * (\alpha_i \equiv g_i^2/(4\pi)), (i=1,2,3).

---

### §3 · One-/Two-loop β-functions (SM, (\overline{\text{MS}}))

**One-loop:**
[
\mu\frac{d g_i}{d\mu}=\frac{b_i}{16\pi^2}g_i^3,
\quad
(b_1,b_2,b_3)=\left(\tfrac{41}{10},-\tfrac{19}{6},-7\right).
]

**Two-loop (compact form):**
[
\mu\frac{dg_i}{d\mu}=\frac{g_i^3}{16\pi^2}b_i
+\frac{g_i^3}{(16\pi^2)^2}!\left(\sum_{j}b_{ij}g_j^2 - c_i,y_t^2\right),
]
with
[
b_{ij}=\begin{pmatrix}
\frac{199}{50}&\frac{27}{10}&\frac{44}{5}[2pt]
\frac{9}{10}&\frac{35}{6}&12[2pt]
\frac{11}{10}&\frac{9}{2}&-26
\end{pmatrix},
\qquad
(c_1,c_2,c_3)=\left(\tfrac{17}{10},\tfrac{3}{2},2\right),
]
and (y_t) the top Yukawa. (This suffices for precision to the Z-pole; higher loops optional.)

**Integrated one-loop form (useful for fast scans):**
[
\frac{1}{\alpha_i(\mu)}=\frac{1}{\alpha_i(\mu_0)}-\frac{b_i}{2\pi}\ln!\frac{\mu}{\mu_0},.
]

---

### §4 · Barrier matching (finite, gauge-invariant)

At (\mu=\mu_c), identify couplings with stiffnesses and add **finite counterterms** that encode time-first microphysics while preserving gauge symmetry:
[
\boxed{\
\frac{1}{g_i^2(\mu_c)} = K_i + \Delta_i,\quad i\in{1,2,3}\ },
]
where (K_i) come from Pirouette’s **Resonance Atlas** and (\Delta_i=\mathcal{O}(1/16\pi^2)) are **finite**, scheme-dependent but **observable-independent** matching constants. By construction (MATH-Γ-007; DYNA-QED-005), no quadratic divergences survive; (\Delta_i) do **not** reintroduce fine-tuning.

**Weinberg angle at the barrier (from DYNA-WEAK-001):**
[
\sin^2\theta_W(\mu_c)=\frac{g'^2(\mu_c)}{g'^2(\mu_c)+g^2(\mu_c)}
=\frac{K_2+\Delta_2}{(K_1+\Delta_1)+(K_2+\Delta_2)},.
]

---

### §5 · Thresholds & decoupling

* **Below (\mu_c):** standard SM thresholds (top, Higgs, W/Z, heavy quarks) are implemented with step-wise decoupling or continuous matching.
* **Above (\mu_c):** time-first UV is **barrier-regulated**; effective higher-dimensional operators are suppressed by (\mu^2/\mu_c^2). No additional light states are introduced by Pirouette in the YM sector.

---

### §6 · Practical pipeline (deterministic fit)

1. **Select stiffness priors** (K_1,K_2,K_3) from **XXP-BRIDGE-Γ-001** (and, if desired, Γ–Higgs correlations from DYNA-Γ-004).
2. **Choose** small (\Delta_i) (finite matching), constrained by CPM & symmetry (keep (|\Delta_i|\ll K_i)).
3. **Compute** (g_i(\mu_c)) from (K_i+\Delta_i).
4. **Run down** to (M_Z) with 1–2 loop RGEs.
5. **Compare** ({\alpha_{\rm EM}(M_Z),\sin^2\theta_W(M_Z),\alpha_s(M_Z)}) to experiment.
6. **Iterate** within Pirouette priors only (no free, ad-hoc tuning): failure to match indicates tension with the stiffness dictionary.

---

### §7 · Predictive handles & correlations

* **Stiffness ratio (\rho_{\text{stiff}}=K_2/K_1)** fixes (\sin^2\theta_W(\mu_c)) ⇒ predicts (\sin^2\theta_W(M_Z)) after RG flow.
* **QCD stiffness (K_3)** plus running gives (\alpha_s(M_Z)) and, with lattice input for nonperturbative conversion, a **prediction for (\Lambda_{\rm QCD})**.
* **Cross-domain link:** (K_2) correlates with **Higgs–Γ width shifts** (DYNA-Γ-004); a combined fit overconstrains the set ({K_1,K_2}).

---

### §8 · Γ-tail (cosmological) drift

Background Γ evolution perturbs stiffnesses coherently:
[
\frac{\dot{K}*i}{K_i} \sim \zeta_i,\frac{\dot{\langle \Gamma^2\rangle}}{M*{\rm coh}^2},
\qquad M_{\rm coh}=\mu_c .
]
Induces **ultra-small**, common-sign temporal drifts in couplings (and thus in (\sin^2\theta_W), (\alpha_s)); magnitudes (\ll) present bounds. Signs are **fixed** once (\zeta_i) are set by the Atlas.

---

### §9 · Falsifiability (module-local)

1. **No-(\rho_{\text{stiff}}) solution:** If **no** (K_1,K_2) within Pirouette priors evolves to measured (\sin^2\theta_W(M_Z)), the triad/clock-stiffness dictionary fails.
2. **(\alpha_s) tension:** Legitimate (K_3) choices that cannot reproduce (\alpha_s(M_Z)) under standard running falsify the temporal-color stiffness link.
3. **Large (\Delta_i) necessity:** If matching requires (|\Delta_i|\sim K_i) to fit data, barrier finiteness is not doing the work ⇒ contradiction with MATH-Γ-007.
4. **Time variation:** Observation of large or wrong-sign drift in (\sin^2\theta_W) or (\alpha_s) violates Γ-tail predictions.

---

### §10 · Linkage

* **Consumes:** ({\omega_c,m_\Gamma,\Lambda_{\rm Pirouette}}), stiffness priors (K_i) (XXP-BRIDGE-Γ-001); Higgs–Γ mixing constraints (DYNA-Γ-004); CPM conditions.
* **Feeds:** **DYNA-COLOR-001** (confinement & string tension (\sigma\sim\kappa_3/\xi_\Gamma^2)), **XXP-EWQCD-EXP** (precision tests at multiple (\mu)).

---

### §11 · Assemblé

Running couplings are the **metronome marks** scribbled in the score; the stiffnesses are the **tension of the strings**. Match them at the barrier, let the RG flow carry them down the stave, and the orchestra of the Standard Model plays in time—unless the instrument’s wood (Γ) warps, ever so slightly, with the weather of the cosmos.

---

Want me to proceed to **DYNA-COLOR-001** next (temporal-color SU(3), (Z_3) vortices, and the (\sigma \sim \kappa_3/\xi_\Gamma^2) confinement scaling you can point lattice folks at)?
