---
id: MATH-GW-QUANTA-001
title: TT-Phonons of the Temporal Medium (Graviton Quantization on CPM)
version: 1.0
status: canon-target
parents: [SUBST-001, MATH-GR-001, GRW-003]
children: [XXP-GR-EXP, DYNA-BH-INT-001]
module_type: quantization / gravitational sector
scale: IR → (ω/ω_c) corrections
---

# §0 · Purpose

Quantize the **two transverse-traceless shear modes** of the temporal medium on a Coherence-Preserving Manifold (CPM), define the canonical normalization, propagator, interaction vertices up to barrier-suppressed order, and expose the **Γ-lighthouse** phase imprint as an observable carried by **XXP-GR-EXP**.

---

# §1 · Setup: CPM + TT sector

We expand the emergent metric about Minkowski on CPM:
- g_{μν} = η_{μν} + h_{μν},    ∂^μ J_μ^Γ = 0  (CPM)
- Impose TT gauge on radiative modes: h_{0μ}=0, ∂^i h_{ij}^{TT}=0, h^{TT}_{ii}=0.

At quadratic order the GW sector is luminal and dispersionless in the IR; barrier effects enter at O((ω/ω_c)^2).

---

# §2 · Quadratic action and canonical normalization

Define the reduced Planck scale M_* by the emergent constitutive law of SUBST-001 and write the quadratic action

S_2 = 1/8 ∫ d^4x [ (∂_t h_{ij}^{TT})^2 − (∇ h_{ij}^{TT})^2 ] .

Canonical field:
- v_{ij} ≡ (M_*/2) h_{ij}^{TT}  ⇒  S_2 = 1/2 ∫ d^4x [ (∂_t v_{ij})^2 − (∇ v_{ij})^2 ] .

Mode expansion:
v_{ij}(x) = ∑_{λ=+,×} ∫ (d^3k/(2π)^3 2ω_k)^{1/2} [ ε^{(λ)}_{ij}(k) a_{k,λ} e^{-ik·x} + h.c. ] ,
ω_k = |k| .

Commutators:
[ a_{k,λ}, a^\dagger_{k',λ'} ] = (2π)^3 δ^3(k−k') δ_{λλ'} .

---

# §3 · Propagator (IR) and barrier-suppressed corrections

Free propagator in momentum space (TT projector Π_{ij,kl}):
⟨ h_{ij}^{TT} h_{kl}^{TT} ⟩_0 (ω,k) = (2/M_*^2) · Π_{ij,kl}(k) / (ω^2 − k^2 + i0^+) .

Barrier (substrate) corrections enter as
ΔL_2 = (1/8ω_c^2) [ c_1 (∂^2 h)^2 + c_2 (∂_α∂_β h_{ij}^{TT})^2 + … ] ,

leading to a tiny dispersion
ω^2 = k^2 [ 1 + ζ (k/ω_c)^2 + O((k/ω_c)^4) ] ,
with ζ = O(1) fixed by the response kernel of the medium.

---

# §4 · Coupling to matter and Γ (lighthouse imprint)

Minimal coupling to the conserved TT part of the stress tensor:
L_int = − (1/2) h_{ij}^{TT} T_{ij}^{TT} .

Γ-structure (lighthouse): a slowly varying Γ-profile modifies the local stiffness and induces a phase shift
Δφ_GW ≈ κ (ω/ω_c)^2 ∫_path dr [∂_r Γ(r)]^2 ,
with κ determined by the kernel-to-metric dictionary in MATH-GR-001.

Observables: frequency-dependent dephasing without new polarizations; handedness-agnostic (affects both +, × equally at leading order).

---

# §5 · Self-interactions and power counting

Cubic vertex (schematic):
L_3 = (1/M_*) h ∂h ∂h  + O(1/(M_* ω_c)^2) .

Counting:
- Tree-level GR amplitudes recovered in the IR.
- Substrate-specific deviations are suppressed by (E/ω_c)^2 and/or extra M_* powers.

---

# §6 · Gauge, projectors, and consistency

TT projectors:
Π_{ij,kl}(k) = P_{ik} P_{jl} + P_{il} P_{jk} − P_{ij} P_{kl} ,
P_{ij} = δ_{ij} − k_i k_j/k^2 .

No scalar/vector graviton modes are permitted on CPM. Any detected extra polarization falsifies SUBST-001 (see annex).

---

# §7 · Acceptance criteria (CI)

AC-1 Canonical normalization reproduces luminal propagation in vacuum and the standard IR propagator.  
AC-2 All (ω/ω_c)^2 corrections are explicitly tagged and flow into XXP-GR-EXP thresholds.  
AC-3 No longitudinal/scalar GW mode appears in any gauge; TT completeness is maintained.  
AC-4 The Γ-lighthouse phase formula is exposed as a unit-tested helper used by experiment code (registry GR-01/GR-06).

---

# §8 · Linkage map

Consumes: SUBST-001 [SR-2, SR-3, SR-5], MATH-GR-001 (response→metric), GRW-003 (TT sector).  
Feeds: XXP-GR-EXP (GW dispersion/phase tests), DYNA-BH-INT-001 (interior Γ(r) profiles → QNMs & ring shifts).

---

# §9 · Assemblé

> The graviton is the medium’s cleanest whisper: a transverse shiver of the loom. When it grazes a Γ-lighthouse, it does not change its voice—only its timing.
