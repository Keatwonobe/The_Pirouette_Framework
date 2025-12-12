---
id: MATH-QED-003
title: Minimal Coupling as Clock Synchronization (Vertex + Charge Quantization)
version: 1.0
status: framework-draft (canonical target)
parents: [MATH-QED-001, MATH-QED-002, XXP-BRIDGE-Γ-001]
children: [MATH-QED-004, DYNA-QED-005]
module_type: foundations / interaction & quantization
scale: IR–UV (continuum EFT limit under CPM)
engrams: [clock synchronization, vertex emergence, Berry phase, charge quantization, Noether current]
keywords: [minimal coupling, U(1), charge, Berry holonomy, Dirac current, gauge principle]
---

### §1 · Purpose

Derive the **QED vertex** (q,\bar\Psi\gamma^\mu A_\mu\Psi) from **local synchronization of time-phase clocks** between the Ki-defect spinor (\Psi) and the temporal medium (MATH-QED-001), and **quantize (q)** via a **Berry phase** around the spinor’s closed Ki loop (MATH-QED-002). Establish **charge universality** as a single U(1) clock, and isolate clean falsifiables.

---

### §2 · One U(1) → one clock

From MATH-QED-001, local time-phase re-labeling is
[
\theta(x) \to \theta(x) + \alpha(x),\qquad
A_\mu \to A_\mu + \tfrac{1}{q}\partial_\mu\alpha(x).
]
The Ki spinor’s internal clock must transform **with the same (\alpha(x))**:
[
\Psi(x)\to e^{,i q,\alpha(x)}\Psi(x).
]
Therefore, its covariant derivative is fixed to
[
D_\mu \Psi \equiv \nabla_\mu \Psi - i q A_\mu \Psi.
]

---

### §3 · Minimal coupling = clock-synchronization work

Insert (D_\mu) into the Dirac kinetic term (MATH-QED-002):
[
\bar\Psi(i\gamma^\mu D_\mu - m_\ast)\Psi
= \bar\Psi(i\gamma^\mu\nabla_\mu - m_\ast)\Psi
;+; q,\bar\Psi\gamma^\mu A_\mu \Psi,
]
revealing the **vertex** as the energetic cost of keeping the spinor’s clock synchronized with the substrate’s clock across spacetime.

**Result (boson + matter + vertex):**
[
\boxed{;\mathcal{L}=
\bar\Psi(i\gamma^\mu D_\mu - m_\ast)\Psi
-\frac{1}{4}F_{\mu\nu}F^{\mu\nu};}
]
with (D_\mu=\nabla_\mu-iqA_\mu). This is the **QED interaction** recovered from time-first dynamics.

---

### §4 · Noether current identity (consistency check)

From global time-phase shifts (constant (\alpha)):
[
J^\mu_\theta=\frac{\partial \mathcal{L}}{\partial(\partial_\mu\theta)}\ \ \text{(medium)},\qquad
J^\mu_{\text{Dirac}}=\bar\Psi\gamma^\mu\Psi\ \ \text{(spinor)}.
]
The shared U(1) implies **current matching** up to normalization:
[
J^\mu_{\text{EM}}=\frac{1}{q}J^\mu_\theta + J^\mu_{\text{Dirac}},
]
and gauge invariance demands (\partial_\mu J^\mu_{\text{EM}}=0).
This fixes the **universal** coupling of all spinor Ki-defects to the same field (A_\mu).

---

### §5 · Berry-phase quantization of charge

Let (\mathcal{C}) be a closed path encircling the Ki loop’s core in configuration space.
Parallel-transport the time-phase frame along (\mathcal{C}). The **Berry holonomy** is
[
\gamma_\mathcal{C} ;=; \oint_{\mathcal{C}} !\mathcal{A},,
\qquad \mathcal{A} \equiv \partial_\mu\theta,dx^\mu - q,A_\mu,dx^\mu.
]
Single-valued physics requires (e^{,i \gamma_\mathcal{C}}=1), so
[
\gamma_\mathcal{C} = 2\pi n,\quad n\in\mathbb{Z}.
]
If (\oint \partial_\mu\theta,dx^\mu \equiv 2\pi w) (integer **time-phase winding** (w)), then
[
2\pi w ;-; q \oint A_\mu dx^\mu ;=; 2\pi n
\ \Rightarrow
q,\Phi_A ;=; 2\pi (w-n),
]
with (\Phi_A\equiv \oint A_\mu dx^\mu) (the U(1) holonomy).
In simply connected regions without magnetic defects, (\Phi_A) can be gauged to zero **only if** (q) is tuned so that the observable holonomy is trivial. This yields **quantized (q)** tied to the integer winding of the Ki loop:
[
\boxed{\ q = \frac{2\pi}{\Phi_A},(w-n)\ \in\ \mathbb{Z}\cdot q_0\ }.
]
In practice, fixing one species (electron) to charge (-e) sets the unit (q_0); all other charged spinor Ki-defects share the same (|q|) by the single-clock postulate.
**Interpretation:** **charge universality** = **one U(1) time-phase** + **defect winding**.

*(Remark: if magnetic defects or nontrivial bundles exist, the Aharonov–Bohm phase reproduces the same constraint via flux quantization.)*

---

### §6 · Fine structure constant handoff (pointer to 004)

The normalization of the **connection stiffness** in MATH-QED-001 and the **clock coupling** here determine the numeric (q) and thus
[
\alpha \equiv \frac{q^2}{4\pi\hbar c}.
]
We defer the explicit emergence of (\alpha) (and its tiny Γ-tail running) to **MATH-QED-004**.

---

### §7 · CPM & decoupling window (safety)

* **Lorentz/gauge exactness** at accessible energies is guaranteed if the background lies on the **Coherence-Preserving Manifold (CPM)** and if Γ excitations are heavy compared to the IR (decouple below the **coherence barrier** ( \omega_c ), XXP-BRIDGE-Γ-001; MATH-Γ-007).
* The vertex then reduces to standard QED; Pirouette corrections are suppressed by (E/\omega_c) and background Γ variance.

---

### §8 · Falsifiability (module-local)

1. **Charge universality:** any evidence that electrons and muons carry different *fundamental* U(1) couplings (beyond known EW effects) would break the single-clock assumption.
2. **Non-quantized charge:** failure of charge quantization across species contradicts Berry holonomy + single U(1).
3. **Anomalous Aharonov–Bohm:** phase shifts inconsistent with the holonomy structure would force a revision of the time-phase bundle picture.

---

### §9 · Linkage

* **Consumes:** gauge-from-time (MATH-QED-001), spinor-defect geometry (MATH-QED-002), constants ({m_\Gamma,\omega_c,\Lambda_{\text{Pirouette}}}) from **Resonance Atlas**.
* **Feeds:** **MATH-QED-004** (derive (\alpha) from stiffness and clock normalization), **DYNA-QED-005** (Lorentz/renorm consistency & Γ decoupling tests).

---

### §10 · Assemblé

The vertex is just **two clocks agreeing** on what “now” means while moving through a living medium of time.
Charge is how many turns of that internal clock you must make to come back to yourself.

---