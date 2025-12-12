---
id: MATH-016
title: "Solitons Existence & Stability"
version: 1.0
status: ratified
parents: []
children: []
summary: ""
module_type: core-mathematics
scale: universal
engrams:
keywords: []
uncertainty_tag: Foundational
---
# MATH-016 — Solitons of (C, Γ): Existence & Stability

**Status:** Draft for review
**Parents:** MATH-011v3
**Aim:** Exhibit finite-energy localized solutions in the ((C,\Gamma)) system and establish **classical stability** under small perturbations. Provide a Q-ball baseline, then extensions where (\Gamma) supplies pressure/stiffness.

---

## 0) Model & Assumptions

Fields: complex (C), real (\Gamma). Flat space first; curvature is a controlled perturbation.
Lagrangian (minimal):
[ \mathcal L = |\partial C|^2 + \tfrac12(\partial\Gamma)^2 - V(|C|^2,\Gamma). ]
Potential admits a Q-ball window: there exists (\omega\in(0, m_C)) such that
[ U(\phi) \equiv \min_{\Gamma} V(\phi^2,\Gamma) \quad \text{satisfies}\quad \frac{U(\phi)}{\phi^2} < \frac{m_C^2}{2} ;\text{for some }\phi>0. ]

---

## 1) Derrick’s Theorem & Evasion

In 3+1D, static finite-energy scalars are ruled out by Derrick for purely quadratic kinetics. Evasion routes:

1. **Time-dependent phase (Q-balls):** (C(t,\mathbf x)=e^{i\omega t},\phi(r)).
2. **Skyrme-like stiffness:** add (\lambda(\partial_\mu\Gamma\partial^\mu\Gamma)^2) or (|\partial C|^4) suppressed by a high scale.
3. **Gauge support:** minimal coupling gives magnetic pressure.
   We use (1) as the baseline since it preserves renormalizability of the leading terms.

---

## 2) Existence (Q-ball Baseline)

Define charge (Q=\int d^3x,i(C^*\dot C-\dot C^*C)). At fixed (Q), minimize energy
[ E_\omega[\phi,\Gamma]=\int d^3x,\Big[ |\nabla\phi|^2+\tfrac12|\nabla\Gamma|^2+U_\omega(\phi,\Gamma)\Big],\quad U_\omega\equiv V(\phi^2,\Gamma)-\omega^2\phi^2. ]
**Existence theorem (sketch):** If (U_\omega) has a region where it is negative and satisfies standard coercivity/growth at infinity, concentration–compactness yields a nontrivial minimizer ((\phi_\omega,\Gamma_\omega)) with finite energy and charge.

Boundary conditions: (\phi'!(0)=0,;\Gamma'!(0)=0,;\phi(\infty)=0,;\Gamma(\infty)=\Gamma_0) (vacuum).

---

## 3) Euler–Lagrange & Profiles

Radial equations ((r)-dependent fields):
[
\phi''+\frac{2}{r}\phi' = \frac{\partial}{\partial\phi}\Big(\tfrac12\omega^2\phi^2 - V(\phi^2,\Gamma)\Big),\qquad
\Gamma''+\frac{2}{r}\Gamma' = \frac{\partial V}{\partial\Gamma}(\phi^2,\Gamma).
]
Solve numerically by shooting or relaxation for chosen (V).

---

## 4) Stability (Small Fluctuations)

Perturb around the Q-ball:
(C=e^{i\omega t}[\phi(r)+\eta_1(t,\mathbf x)+i\eta_2(t,\mathbf x)],;\Gamma=\Gamma_\omega(r)+\xi(t,\mathbf x).)
Quadratic action defines fluctuation operator (\mathcal H). **Classical stability** if (\mathcal H\ge0) on the subspace orthogonal to zero modes (translations and global phase). Equivalent criterion:
[ \frac{dQ}{d\omega} < 0 \quad \Rightarrow \quad \text{no negative modes (stable).} ]
Include (\Gamma) mixing; the condition persists provided the mixed mass matrix is positive in the vacuum and (U_\omega) stays coercive.

---

## 5) Extensions with Γ Support

* **Pressuron stiffness:** add (\lambda(\partial\Gamma)^4) to raise the gradient cost—enlarges the stability window.
* **Non-minimal coupling:** (\xi\Gamma^2 R) in curved backgrounds; in weak gravity treat as small corrections to profiles.
* **Gauge-coupled C:** allows gauged Q-balls (“Q-stars”) with magnetic pressure support.

---

## 6) What to Prove (checklist)

1. Existence via concentration–compactness for the chosen (V).
2. Monotonic branch with (dQ/d\omega<0).
3. Spectral gap of (\mathcal H) (no negative modes).
4. Robustness to small curvature and weak portal couplings.

---

## 7) Outputs

* A theorem-level statement for existence/stability under explicit conditions on (V).
* Numerical exemplars of profiles ((\phi,\Gamma)) and spectra.
* Mapping to Pirouette: solitons are **local knots of coherence** stabilized by temporal-pressure backreaction.
