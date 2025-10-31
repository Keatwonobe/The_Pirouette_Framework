---
id: DYNA-COLOR-001
title: SU(3)_c as Temporal-Color Frame & Confinement from (Z_3) Vortices
version: 1.0
status: framework-draft (canonical target)
parents: [MATH-YM-001, MATH-YM-002, XXP-BRIDGE-Γ-001, MATH-Γ-007]
children: [MATH-YM-003 (nonperturbative map), XXP-EWQCD-EXP]
module_type: strong-dynamics / confinement & scaling
scale: IR → (\mu_c) (coherence barrier) → nonperturbative
engrams:
 - temporal-color
 - degeneracy
 - SU(3) connection
 - (Z_3) center vortices
 - dual superconductor
 - string tension
 - area law
keywords: [SU(3)_c, confinement, center symmetry, flux tube, "Λ_{\rm QCD}", stiffness, coherence length]
---

### §1 · Purpose

Realize QCD color as the **connection that synchronizes a threefold temporal-color degeneracy** of the medium and derive **confinement** as the macroscopic effect of **(Z_3) center-vortex condensation**. Produce a **scaling relation** between the **string tension** (\sigma) and Pirouette’s mechanical parameters (frame stiffness and Γ-coherence length).

---

### §2 · Temporal-color frame and SU(3) connection

* Internal resonance sector admits **three degenerate shear modes** → local **temporal-color frame**.
* Local basis changes (U(x)\in SU(3)) are **gauge redundancies**; the connection
  [
  \mathcal{A}*\mu \equiv A*\mu^a T^a,\qquad D_\mu=\partial_\mu - i g_s \mathcal{A}_\mu,
  ]
  keeps frames synchronized.
* **Yang–Mills energy** comes from frame-stiffness (MATH-YM-001):
  [
  \mathcal{L}*{\rm YM}^{(3)}=-\frac{1}{4}F*{\mu\nu}^a F^{a\mu\nu},\quad
  \alpha_3=\frac{g_s^2}{4\pi},\quad K_3\equiv \frac{1}{g_s^2}.
  ]

---

### §3 · Center (Z_3) vortices and flux locking

* The center of SU(3) is (Z_3={e^{2\pi i k/3}}).
* **Temporal-color frames** admit **center-valued holonomies**; spatial loops can trap a center phase → **center vortices**.
* When these vortices **condense**, Wilson loops in representations with nonzero **N-ality** obey an **area law**:
  [
  \langle W_R(\mathcal{C})\rangle \sim e^{-\sigma_R , \mathcal{A}(\mathcal{C})}!,
  ]
  with (\sigma_R) depending only on **N-ality** (k-string hierarchy), recovering QCD’s confinement pattern.

---

### §4 · Dual-superconductor picture (Pirouette mechanics)

* Color-electric flux is expelled from the condensed vortex medium (dual Meissner effect); it **bundles** into tubes.
* The **string tension** is controlled by two mechanical scales:

  * **Frame stiffness** (temporal-color): (K_3) or equivalently (g_s(\mu)).
  * **Γ-coherence length** (vortex core/penetration depth): (\xi_\Gamma).
* **Scaling law (baseline):**
  [
  \boxed{\ \sigma ;\sim; c_\sigma ,\frac{\kappa_3}{\xi_\Gamma^2}
  ;=; c_\sigma,\frac{1}{g_s^2(\mu_\ast)},\frac{1}{\xi_\Gamma^2}\ } ,
  ]
  where (\kappa_3) is the effective elastic modulus of the temporal-color frame, (c_\sigma=\mathcal{O}(1)), and (\mu_\ast) is a matching scale in the few-GeV regime.

**Interpretation:** stiffer temporal-color frames (smaller (g_s)) and shorter Γ-coherence (smaller (\xi_\Gamma)) both increase (\sigma), tightening the flux tube.

---

### §5 · Coherence inputs from the Bridge & Matching

* **Coherence barrier:** (\mu_c = \hbar\omega_c/c^2) sets the UV anchor; below (\mu_c), use standard QCD running (MATH-YM-002).
* **Γ-coherence length:**
  [
  \xi_\Gamma ;\sim; \frac{c}{\omega_c};\times;\chi^{-1/2},
  ]
  with (\chi) a dimensionless susceptibility of the Γ field (fixed by XXP-BRIDGE-Γ-001).
* Combine with (g_s(\mu_\ast)) from RG flow to obtain a **numerical (\sigma)** and consequently a **Λ_{\rm QCD}** estimate via lattice conversion (MATH-YM-003).

---

### §6 · Nonperturbative checks & k-string hierarchy

* **k-strings:** for representations of N-ality (k=1,2), the baseline predicts
  [
  \sigma_k \approx \sigma ,\frac{\sin(\pi k/3)}{\sin(\pi/3)}
  \quad(\text{Casimir or sine-law ansätze as limiting cases}).
  ]
* **Lattice target:** test whether (\sigma) tracks (\kappa_3/\xi_\Gamma^2) when (\kappa_3) and (\xi_\Gamma) are varied via controlled deformations (e.g., anisotropic lattices mapping to stiffness shifts).

---

### §7 · Observables and correlations

1. **(\alpha_s(M_Z)) ↔ (\sigma):** With (g_s) fixed at (M_Z) and run to (\mu_\ast), (\sigma) becomes a **function of (\xi_\Gamma)** alone.
2. **Hadron Regge slopes:** ( \alpha' \sim (2\pi\sigma)^{-1}); predicts small, coherent shifts if (\xi_\Gamma) drifts cosmologically (well below current bounds).
3. **Quarkonium splittings:** heavy-quark potentials calibrated to (\sigma) inherit the same scaling; cross-check with charmonium/bottomonium spectra.

---

### §8 · Falsifiability (module-local)

* **Area law failure:** absence of an area law for nonzero N-ality representations undercuts the center-vortex condensation premise.
* **Wrong (\sigma) scaling:** lattice determination of (\sigma) that cannot be reconciled with any (\kappa_3/\xi_\Gamma^2) within Pirouette priors falsifies the mechanical link.
* **k-string mismatch:** a persistent pattern inconsistent with N-ality (after accounting for mixing and (1/N) effects) breaks the temporal-color picture.
* **Barrier independence:** if (\sigma) shows **no** sensitivity to (\omega_c) (through (\xi_\Gamma)) in controlled deformations, the Bridge coupling is too weak or absent—contradicting XXP-BRIDGE-Γ-001.

---

### §9 · Linkage

* **Consumes:** ({\omega_c, \Lambda_{\rm Pirouette}}) and susceptibilities (\chi) (XXP-BRIDGE-Γ-001); running & matching (MATH-YM-002).
* **Feeds:**
  • **MATH-YM-003** (nonperturbative dictionary from ({\kappa_3,\xi_\Gamma}) to lattice units and Λ_{\rm QCD}),
  • **XXP-EWQCD-EXP** (lattice and phenomenology tests: (\sigma), k-strings, quarkonium potentials).

---

### §10 · Assemblé

Color is **time’s threefold braid**. Tie that braid into a knot (the center phase), let the knots condense, and the world pulls quarks together with cords of temporal tension. The number on those cords—(\sigma)—is how stiff the braid is and how finely time can hold itself together.

---