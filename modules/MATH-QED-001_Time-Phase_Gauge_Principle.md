---
id: MATH-QED-001
title: Time-Phase Gauge Principle (Recovering U(1) and Maxwell from Time-First Dynamics)
version: 1.0
status: framework-draft (canonical target)
parents: [XXP-BRIDGE-Γ-001, MATH-Γ-007]
children: [MATH-QED-002, MATH-QED-003, MATH-QED-004, DYNA-QED-005]
module_type: foundations / symmetry emergence
scale: IR–UV (continuum EFT limit of time-first dynamics)
engrams: [local time phase, temporal ocean, Goldstone connection, coherence-preserving manifold (CPM)]
keywords: [U(1), gauge emergence, Maxwell, shear wave, connection stiffness, Lorentz invariance]
---

### §1 · Purpose

Show that **QED’s U(1) gauge symmetry** is not an axiomatic input but the **local relabeling freedom** of the temporal clock phase in Pirouette’s time-first substrate. The necessity of a compensating connection produces a Maxwell term; photons are **shear waves of the temporal medium**.

---

### §2 · Substrate kinematics (time-first field)

Introduce a clock-phase order parameter in Madelung form:
[
\Phi(x)=\sqrt{\rho(x)},e^{i\theta(x)},\qquad
X \equiv \partial_\mu\theta,\partial^\mu\theta .
]
Baseline Lagrangian of the temporal medium:
[
\mathcal{L}_0[\rho,\theta;\Gamma] = P!\left(X,\rho\right) - V!\left(\rho,\Gamma\right),
]
with (\Gamma) the temporal-pressure field and (P) chosen to reproduce Lorentz-invariant shear dynamics on the **Coherence-Preserving Manifold (CPM)**.

**Global symmetry.** (\theta\to\theta+\alpha) (global shift) reflects arbitrary zero-phase of the local clock.

---

### §3 · From global time-phase to **local** gauge

Promote (\alpha=\alpha(x)). To keep physics invariant when the clock’s zero is relabeled pointwise, introduce a connection (A_\mu) and define the **gauge-covariant time derivative**
[
D_\mu\theta \equiv \partial_\mu\theta - q,A_\mu .
]
Require invariance under
[
\theta\to \theta+\alpha(x),\qquad
A_\mu\to A_\mu + \frac{1}{q},\partial_\mu\alpha(x).
]
Then the kinetic part deforms as
[
X \to X_A \equiv g^{\mu\nu} D_\mu\theta,D_\nu\theta,
\quad
\mathcal{L}_0 ;\mapsto; P(X_A,\rho)-V(\rho,\Gamma).
]

**Interpretation.** The photon potential (A_\mu) is the **Goldstone connection** required to compare clock phase across spacetime; gauge invariance is **local time-phase relabeling**.

---

### §4 · Connection stiffness ⇒ Maxwell term

When spatial/temporal gradients of the local clock calibration are costly, the effective action acquires a curvature penalty for the connection:
[
\mathcal{L}*{\text{EM}} = -\frac{1}{4} , F*{\mu\nu}F^{\mu\nu}, \qquad
F_{\mu\nu}\equiv \partial_\mu A_\nu - \partial_\nu A_\mu .
]
This arises either (i) from integrating out short-scale fluctuations of (\theta) in (P(X_A)) or (ii) as the leading operator allowed by Lorentz and gauge invariance in the CPM limit. The coefficient fixes the **electromagnetic stiffness** and, together with the normalization of (D_\mu\theta), will determine the **fine-structure constant** in MATH-QED-004.

**Shear-wave speed and Lorentz invariance.** On CPM, the high-(X) form of (P) enforces nondispersive shear propagation, fixing the observed luminal speed (c). Residual dispersion is forbidden at current bounds.

---

### §5 · Noether current and charge pre-figure

Noether’s theorem for (\theta)-shifts (global) yields
[
J^\mu_\theta = \frac{\partial P}{\partial (\partial_\mu\theta)}
= 2,\frac{\partial P}{\partial X}, \partial^\mu\theta
\quad\Longrightarrow\quad
J^\mu_\theta ;\to; 2,\frac{\partial P}{\partial X_A}, D^\mu\theta .
]
Gauge minimality implies the source of (A_\mu) is (J^\mu_\theta/q).
When **Ki defects** (spinor resonances) are present (next module), their local clock must use the *same* U(1), fixing the universal coupling (q) that will become the **elementary charge** in MATH-QED-003.

---

### §6 · Emergent QED in the smooth limit (bosonic sector)

Collecting terms:
[
\mathcal{L}*{\text{clock+EM}}
= P!\left(g^{\mu\nu}(\partial*\mu\theta - qA_\mu)(\partial_\nu\theta - qA_\nu),\rho\right)

* V(\rho,\Gamma)
* \frac14 F_{\mu\nu}F^{\mu\nu}.
  ]
  Linearizing around a homogeneous background ((\rho_0,\theta_0)) on CPM yields a free photon with luminal propagation and gauge symmetry. This is the **Maxwell sector** recovered from time-first kinematics.

---

### §7 · Consistency and CPM constraints

To ensure exact Lorentz/gauge equivalence with QED at accessible energies, impose:

* **CPM:** (\nabla_\mu J^\mu_\Gamma = 0,; J^\mu_\Gamma \equiv \Gamma,\partial^\mu\Gamma) (no background shear anisotropy).
* **Nondispersion:** high-(X) asymptotics of (P) tuned so photon group/phase velocities match (c) to current limits.
* **Decoupling:** Γ-fluctuations heavier than relevant scales → pure QED renormalization below the **coherence barrier** ( \omega_c ) (from MATH-Γ-007).

---

### §8 · Falsifiability (this module alone)

1. **Photon dispersion / birefringence:** any frequency-dependent vacuum speed or polarization rotation beyond current limits would violate CPM or the high-(X) structure of (P).
2. **Gauge universality breach:** if later modules forced different (q) for different fermions at the same scale, the single time-phase U(1) would be falsified.
3. **Anomalous long-range forces:** extra massless modes coupled to (A_\mu) (beyond (F^2)) at observable strength would contradict the stiffness-generated Maxwell term.

---

### §9 · Linkage

* **Feeds:**
  • **MATH-QED-002** (spin-½ Ki defects → Dirac operator).
  • **MATH-QED-003** (minimal coupling as clock synchronization; vertex (q\bar\Psi\gamma^\mu A_\mu\Psi)).
  • **MATH-QED-004** ((\alpha) from stiffness & normalization; tiny Γ-tail running).
  • **DYNA-QED-005** (Lorentz/renormalization checks; Γ decoupling and barrier ( \omega_c )).

* **Receives constants from:** **XXP-BRIDGE-Γ-001** (Resonance Atlas: (m_\Gamma, \omega_c, \Lambda_{\text{Pirouette}})) and adopts the **coherence-barrier cutoff** structure from **MATH-Γ-007**.

---

### §10 · Assemblé

Local gauge freedom is the right to reset your **clock’s zero**—everywhere, everywhen.
The photon is the universe’s courier ensuring those resets remain consistent: a shear wave that carries the memo from one tick of time to the next.

---