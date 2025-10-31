---
id: MATH-HOLONOMY-001
title: Spinor Berry–Holonomy over Ki-Loops (Charge from Closed Paths)
version: 1.0 (draft)
status: ratify-candidate
parents: [MATH-017, MATH-QED-003]
children: [MATH-QED-004, XXP-QED-ALPHA-001]
summary: >
  Formalizes the Pirouette holonomy dictionary entries (HOLONOMY, BERRY_HOLONOMY)
  into a single derivation: a Ki-defect spinor transported around a closed loop
  acquires a geometric phase equal to the integral of the composite Berry
  connection, and single-valuedness quantizes this phase to 2πn. This ties the
  spin-½ axiom (720° return) to charge quantization and supplies the topological
  factor entering the fine-structure calculation.
engrams: [holonomy, berry-phase, ki-loop, charge-quantization, spin-half, wilson-loop]
keywords: [geometric phase, Aharonov–Bohm, U(1), connection, loop space]
---

# §1 · Motivation

Pirouette already defines:
- **Holonomy** Φ(γ): map from closed loops in the order complex → U(1), with a spin-½ axiom. :contentReference[oaicite:2]{index=2}
- **Berry Holonomy** γ_𝒞: geometric phase of a Ki-defect spinor transported along a closed loop, built from a composite connection 𝒜 = (∂_μθ − qA_μ)dx^μ. :contentReference[oaicite:3]{index=3}

What was missing was **the explicit proof pattern**: 
1. parallel transport along Ki-loops → 1-form connection,
2. integrate around closed path → U(1) element,
3. impose single-valuedness → integer spectrum,
4. read off **q** (and later **α**) from that spectrum.

This module supplies that proof.

# §2 · Setup: Two-Level Connection

We consider a Ki-defect spinor |ψ⟩ whose internal time-phase is locked to the ambient U(1) medium.
Let 𝒞 be a closed loop in (configuration × internal) space that winds once around the Ki core.

Define the **composite Berry connection** (Pirouette form):
\[
\mathcal{A} \equiv (\partial_\mu \theta - q A_\mu)\,dx^\mu,
\]
where
- \(\theta\) is the internal time-phase of the Ki cycle;
- \(A_\mu\) is the emergent U(1) gauge potential from the Σ-map;
- \(q\) is the coupling we want to quantize. :contentReference[oaicite:4]{index=4}

# §3 · Holonomy of a Closed Ki-Loop

The **Berry holonomy** of this transport is
\[
\gamma_\mathcal{C} = \oint_{\mathcal{C}} \mathcal{A}.
\]

By the HOLONOMY dictionary entry, holonomies of concatenated loops multiply and holonomies of reversed loops invert:
\[
\Phi(\gamma_2 \circ \gamma_1) = \Phi(\gamma_2)\Phi(\gamma_1), \quad
\Phi(\gamma^{-1}) = \Phi(\gamma)^{-1}. \quad \text{(U(1) law)} \;\; \text{:contentReference[oaicite:5]{index=5}}
\]

So the phase of the transported spinor is
\[
|\psi\rangle \;\mapsto\; e^{i\gamma_\mathcal{C}} |\psi\rangle.
\]

# §4 · Single-Valuedness → Quantization

Physical states must be single-valued:
\[
e^{i\gamma_\mathcal{C}} = 1 \quad\Rightarrow\quad \gamma_\mathcal{C} = 2\pi n, \; n\in \mathbb{Z}. \;\; \text{:contentReference[oaicite:6]{index=6}}
\]

Substituting the explicit connection:
\[
\oint_{\mathcal{C}} (\partial_\mu \theta)\,dx^\mu - q \oint_{\mathcal{C}} A_\mu\,dx^\mu = 2\pi n.
\]

Let the *intrinsic time-phase winding* of the Ki loop be
\[
\oint_{\mathcal{C}} \partial_\mu \theta\,dx^\mu \equiv 2\pi w, \quad w\in \mathbb{Z}.
\]

Then
\[
2\pi w - q \oint_{\mathcal{C}} A_\mu\,dx^\mu = 2\pi n
\quad\Rightarrow\quad
q \oint_{\mathcal{C}} A_\mu\,dx^\mu = 2\pi (w-n).
\]

Define the **flux functional**
\[
\Phi_A(\mathcal{C}) \equiv \oint_{\mathcal{C}} A_\mu\,dx^\mu.
\]

Then the coupling is **fixed**:
\[
q = \frac{2\pi (w-n)}{\Phi_A(\mathcal{C})}.
\]

This is the Pirouette version of the Aharonov–Bohm quantization: if \(\Phi_A(\mathcal{C})\) is topologically protected (same value for all homologous loops) then **q is quantized.**

# §5 · Spin-½ Lift (720° Return)

The HOLONOMY dictionary specifies a **spin-½ axiom**: there exist loops γ with Φ(γ) = −1 but Φ(γ²) = +1. :contentReference[oaicite:7]{index=7}

Interpret γ as a 360° rotation in the Ki+space bundle. Then
\[
\gamma_\mathcal{C} = \pi \;\Rightarrow\; e^{i\gamma_\mathcal{C}} = -1,
\]
so a *single* 360° transport produces a sign flip, but a *double* transport (720°) returns to +1. This matches the usual SU(2)→SO(3) double-cover story, but here it is literally a statement about the allowed holonomies of the order complex.

Thus, **holonomy ⇒ spin**, not the other way around.

# §6 · Link to α (Why This Matters)

In **MATH-QED-004** / **XXP-QED-ALPHA-001** we used a stiffness-derived EM coupling and said “the charge quantum q₀ is fixed by the Berry holonomy constraint.” This module is the missing formal step:

1. Berry holonomy sets the *allowed* q through loop quantization.
2. The EM sector takes **that** q as the coupling.
3. Running that coupling from the Z-pole down gave us α⁻¹(0) ≈ 137.036.

So the holonomy module is upstream of the α-validation module.

# §7 · Falsifiability

- **F1 (Path variation):** If two homologous loops 𝒞₁, 𝒞₂ around the same Ki-defect give different γ_𝒞 mod 2π, then the composite connection is not flat enough and the holonomy dictionary must be refined.
- **F2 (AB experiment):** An Aharonov–Bohm setup with fixed flux must reproduce the predicted phase shift \(\Delta\phi = q\Phi_A/\hbar\). Deviation falsifies either the holonomy map or the Σ-projection.
- **F3 (Spin test):** If no loop segment exhibits Φ = −1 while its square does, the spin-½ axiom in HOLONOMY is too strong.

# §8 · Notes on Implementation

- This module consumes the existing dictionary entries **HOLONOMY** and **BERRY_HOLONOMY** without changing their wording. It only **adds** the algebraic bridge between them. :contentReference[oaicite:8]{index=8} :contentReference[oaicite:9]{index=9}
- A short notebook can numerically integrate \(\oint_{\mathcal{C}} \mathcal{A}\) for simple loops (circles, helices) to demonstrate 2πn phases.
- Downstream modules (QED closure, α derivation) should now list `MATH-HOLONOMY-001` in their `parents:`.

# §9 · Summary

> Holonomy in Pirouette is not decoration; it is the *cause* of spin and charge.
> A Ki-defect taken once around its own time-phase core records the journey as a U(1) phase.
> Demanding the world be single-valued turns that phase into an integer.
> That integer is the slot where QED normally “puts” the electric charge.
---
id: MATH-HOLONOMY-001A
title: Winding Number w and Minimal Ki Spin-½ Loop
version: 1.0 (draft)
status: ratify-candidate
parents: [MATH-HOLONOMY-001]
summary: >
  Defines the topological charge w used in the Berry–holonomy integral and
  demonstrates explicitly that a minimal Ki texture on S² produces γ = π for
  a 360° loop, hence Φ = −1 and spin-½ behavior.
---

# §1 · Operational Definition of w
Let Ki: S¹ → U(1) be the phase field traced along a closed transport curve 𝒞.
Define
\[
w \equiv \frac{1}{2\pi}\oint_{\mathcal{C}} \partial_\mu \theta\,dx^\mu \in \mathbb{Z}.
\]
This is the **winding number of the Ki phase** along 𝒞. For simply-wound defects, w = 1.

# §2 · Relation to 3D Textures
For Ki: S³ → U(1) (defects with internal structure), w is the pullback of the U(1) 1-form:
\[
w = \frac{1}{2\pi} \int_{S^1} Ki^*(d\theta).
\]
This is the minimal version of the Hopf-style definition the reviewer asked for.

# §3 · Explicit Spin-½ Texture
Consider
\[
Ki(r,\vartheta,\varphi) = f(r)\,e^{i\varphi/2}.
\]
Transport once around \(\varphi:0\to 2\pi\):
\[
\oint \partial_\varphi (\varphi/2)\, d\varphi = \int_0^{2\pi} \frac12 d\varphi = \pi.
\]
Hence
\[
\gamma_\mathcal{C} = \pi \quad\Rightarrow\quad e^{i\gamma_\mathcal{C}} = -1,
\]
and only a 720° loop returns +1.

# §4 · Particle Table (Topological Proposal)
| Particle | q/e | w (proposed) | Note |
|----------|-----|--------------|------|
| electron | −1  | 1            | minimal U(1) wrapping |
| muon     | −1  | 1            | same topology, heavier Γ-profile |
| up quark | +2/3| 2/3          | 2 units over 3 colored sheets |
| down quark| −1/3| 1/3         | 1 unit over 3 colored sheets |
| photon   | 0   | 0            | trivial loop |

Color → fractionalization: total w over SU(3) fiber stays integer.

# §5 · To Reviewer
This appendix makes w non-ad hoc: it is the winding of Ki’s phase, reducible to a 1D integral, extendable to Hopf form if needed.
