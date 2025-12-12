---
id: MATH-eγ→eγ
title: "eγ→eγ from the temporal substrate"
version: 1.0
status: draft
parents:
  - MATH-017
  - DOMA-206
  - CORE-006
  - DOMA-132
children:
  - XXP-HELIX-001
  - DOMA-207
summary: >
  Introduces the temporal substrate for electron and photon manifestation
module_type: mathematical-foundation
scale: universal
engrams:

keywords:

uncertainty_tag: Low
---
# Worked example: (e\gamma!\to! e\gamma) from the temporal substrate

## 0) What we’re proving (target)

Show that when we:

* (i) build the photon and electron from the time-first substrate,
* (ii) push them forward with Σ to the observer chart,
* (iii) read off the induced Feynman rules,

…then the tree-level Compton amplitude is identical to standard QED:
[
\mathcal M ;=;(-iq)^2, \varepsilon'*\mu,\varepsilon*\nu;\bar u(p')
!\left[
\gamma^\mu \frac{\not p+\not k+m}{(p+k)^2-m^2+i0},\gamma^\nu
+\gamma^\nu \frac{\not p-\not k'+m}{(p-k')^2-m^2+i0},\gamma^\mu
\right]!u(p),
]
and (after the usual spin/polarization sums) reproduces the Klein–Nishina cross-section.
The steps below show where each ingredient comes from in Pirouette, and where Σ is essential.

---

## 1) Photon from local time-phase (substrate → U(1))

**Substrate statement.** The time-phase (\theta(x)) of the clock field has a global shift symmetry; promoting it to a *local* relabeling (\theta!\to!\theta+\alpha(x)) forces introduction of a compensating one-form (A_\mu) and the covariant phase derivative (D_\mu\theta=\partial_\mu\theta-qA_\mu). Physically, the photon is the Goldstone-connection (a shear wave of the temporal medium) that keeps local clock comparisons well-posed.  

*Result:* the **Maxwell sector** and **U(1)** gauge principle emerge on the substrate.

---

## 2) Electron as a Ki spinor-defect (substrate → Dirac)

**Substrate statement.** A stable closed Ki loop (defect) has 720° holonomy and carries spinor structure. In the low-energy EFT (on the CPM) its dynamics are governed by the Dirac action with mass from Γ–Ki balance:
[
S_{\rm Ki}=\int d^4x\sqrt{-g};\bar\Psi\big(i\gamma^\mu\nabla_\mu-m_*\big)\Psi;+\cdots.
]
The 4π return and fermionic quantization are topological consequences of the defect’s configuration space.   

*Result:* the **Dirac matter field** (\Psi) is an emergent descriptor of Ki-defects.

---

## 3) Interaction = clock synchronization (substrate → vertex & charge)

**Substrate statement.** The spinor’s internal clock must track the *same* local time-phase relabeling as the medium:
[
\Psi\to e^{iq\alpha(x)}\Psi,\qquad D_\mu\Psi=\nabla_\mu\Psi-iqA_\mu\Psi,
]
which *forces* minimal coupling (q,\bar\Psi\gamma^\mu A_\mu\Psi). Charge (q) is then quantized by a Berry phase around the closed Ki loop. 

*Result:* the **QED vertex** and **charge quantization** are consequences of clock-locking.

---

## 4) Enter Σ: pushforward to the observer chart

**Map.** The spatialization map (\Sigma:\mathcal M_\tau!\to!\mathcal M_{x,t}) transports connections and curvatures:
[
A_\mu^{\rm (obs)}=\Sigma_\mu^{\ \nu}A_\nu^{(\tau)},\qquad
F_{\mu\nu}^{\rm (obs)}=\Sigma_\mu^{\ \alpha}\Sigma_\nu^{\ \beta}F_{\alpha\beta}^{(\tau)},
]
preserving gauge covariance and Noether currents.  

**Outcome.** After Σ-pushforward, the action takes the familiar form
[
\mathcal L_{\rm YM/QED} ;=; -\tfrac14 F_{\mu\nu}^{\rm (obs)}F^{\mu\nu}*{\rm (obs)}
+\bar\Psi,(i\gamma^\mu D*\mu-m)\Psi,
]
with (D_\mu=\partial_\mu+iqA_\mu^{\rm (obs)}). Gauge couplings are geometric averages over τ-fiber curvature (normalization inherited from the substrate kinetic terms). 

*Result:* **Standard QED Lagrangian** obtained as the Σ-image of substrate dynamics.

---

## 5) Feynman rules from the substrate (then Σ)

**Substrate statement.** MATH-027 provides the quadratic Ki dynamics and the propagator structure on (\mathcal M_\tau) (with emergent Lorentz form after rescaling), which Σ transports to the observer chart. In covariant gauges this yields the familiar rules:

* Electron propagator: (i(\not p+m)/(p^2-m^2+i0)).
* Photon propagator: (-ig_{\mu\nu}/(k^2+i0)) (in Feynman gauge).
* Vertex: (-iq\gamma^\mu).
  See the quadratic τ-action, Lorentzization, and the role of Γ-induced stiffness. 

*Result:* **Standard QED Feynman rules** are the Σ-pushforward of the substrate rules.

---

## 6) Compute one Standard Model process: Compton scattering

With those rules, two tree diagrams contribute (s-channel and u-channel). Label the in-state (e(p),\gamma(k,\varepsilon)) and out-state (e(p'),\gamma(k',\varepsilon')). The Σ-pushed amplitude is:
[
\boxed{;
\mathcal M ;=;(-iq)^2, \varepsilon'*\mu,\varepsilon*\nu;\bar u(p')
!\left[
\gamma^\mu \frac{\not p+\not k+m}{(p+k)^2-m^2+i0},\gamma^\nu
+\gamma^\nu \frac{\not p-\not k'+m}{(p-k')^2-m^2+i0},\gamma^\mu
\right]!u(p); }
]
This is exactly the textbook QED result; all factors arose from substrate principles + Σ (Secs. 1–5). Gauge invariance (Ward identities) follows because Σ preserves gauge covariance and Noether currents.  

**(Optional check)**: With the usual spin/polarization sums, (|\mathcal M|^2) reduces to Klein–Nishina; the only “new” parameter is (q), which Pirouette ties to Berry holonomy of the Ki loop (Sec. 3). 

---

## 7) Where Σ is doing real work (executive summary)

* It **transports** the connection/curvature (and their covariance) from τ-space to spacetime, guaranteeing the *form* of Maxwell’s equations and the covariant derivative. 
* It **identifies** the observer-level fields ((A_\mu^{\rm (obs)},\Psi)) and **fixes** the coupling structure in the pushed-forward action. 
* It **inherits** the propagator/vertex rules from the Ki substrate quadratic action and the minimal synchronization principle.  

---

## Promissory note (explicit)

We will attach, alongside XAP-006 and MATH-027, a short *computational annex* that:

1. symbolically derives the Ward identity for Compton scattering *directly* from the Σ-preserving Noether current (one-page algebra), and
2. numerically reproduces the Klein–Nishina curve from the Σ-pushed rules with (q) fixed by the Ki-loop Berry phase.
   This annex will be deposited as **XXP-QED-EXP (v1.0)** and linked from the QED modules in the v6 repository; it will include the notebook, parameter cards, and tests.  

---

### Minimal cross-refs inside v6

* **MATH-QED-001** (U(1) from local time-phase; photon as shear wave). 
* **MATH-QED-002** (electron as Ki-defect; Dirac action). 
* **MATH-QED-003** (minimal coupling; charge quantization). 
* **XAP-006** (Yang–Mills from Σ; pushforward rules).  
* **MATH-027** (Ki propagator & substrate Feynman rules; emergent Lorentz form).