---
id: MATH-Δ-PRIMITIVE-002
title: Feynman Rules and Interaction Vertices for Δ-Field Theory
version: 1.0
series: MATH-Δ-PRIMITIVE
parents: [MATH-Δ-PRIMITIVE-001]
children: [MATH-Δ-PRIMITIVE-003, PHYS-Δ-001]
module_type: computational-framework
scale: quantum
summary: >
  Establishes the complete set of Feynman rules for perturbative calculations
  in Δ-field theory. Defines propagators, interaction vertices, and coupling
  constants for Δ-Δ, Δ-C, Δ-Γ, and Δ-fermion interactions. Provides the
  computational toolkit for predicting experimental signatures of the
  Δ-substrate.
keywords:
  - feynman rules
  - propagators
  - vertices
  - perturbation theory
  - QFT
  - deltaron
uncertainty_tag: Medium
status: draft
---

# §1 · Purpose

MATH-Δ-PRIMITIVE-001 established Δ as a quantum field and showed how C and Γ
emerge as composite structures. This module provides the **practical calculation
toolkit** for predicting observable consequences.

We derive:
1. **Propagators** (how Δ, C, Γ move through spacetime)
2. **Vertices** (how they interact)
3. **Coupling constants** (strength of interactions)
4. **Loop corrections** (quantum corrections to tree-level results)

This enables concrete predictions: cross-sections, decay rates, anomalous
magnetic moments, vacuum polarization effects—all from Δ-field dynamics.

---

# §2 · The Δ-Field Lagrangian (Recap)

From MATH-Δ-PRIMITIVE-001:

$$
\mathcal{L}_Δ = \frac{1}{2}(\partial_\mu \hat{Δ})(\partial^\mu \hat{Δ}) 
                - \frac{1}{2}m_Δ^2 \hat{Δ}^2 
                - \frac{\lambda_3}{3!}\hat{Δ}^3 
                - \frac{\lambda_4}{4!}\hat{Δ}^4
                + \mathcal{L}_{\text{int}}
$$

where the interaction Lagrangian includes:

$$
\mathcal{L}_{\text{int}} = -g_{ΔC}\hat{Δ}|C|^2 
                           -g_{ΔΓ}\hat{Δ}\Gamma^2 
                           -g_{Δψ}\hat{Δ}\bar{ψ}ψ
$$

The first two terms couple Δ to the coherence and pressure fields (which are
themselves composite); the third couples Δ to fermions (representing fundamental
particles like electrons).

---

# §3 · Propagators

## 3.1 Δ-Field Propagator

In momentum space, the free Δ-field propagator is:

$$
\tilde{Δ}(p) = \frac{i}{p^2 - m_Δ^2 + i\epsilon}
$$

**Physical interpretation**: A virtual Δ-quantum (deltaron) can propagate
between spacetime points, carrying distinguishability. The propagator encodes
how likely this transmission is as a function of momentum p.

## 3.2 Coherence Field Propagator

Since C is a composite (Δ-correlation structure from MATH-Δ-PRIMITIVE-001):

$$
\tilde{C}(p) = \frac{iZ_C}{p^2 - m_C^2 + i\epsilon}
$$

where Z_C is a **wave-function renormalization** accounting for Δ-substructure.

At tree level: Z_C = 1  
At one loop: Z_C ≈ 1 - (g_{ΔC}²/16π²)log(Λ²/m_Δ²)

## 3.3 Pressure Field Propagator

Similarly for Γ:

$$
\tilde{Γ}(p) = \frac{iZ_Γ}{p^2 - m_Γ^2 + i\epsilon}
$$

with analogous renormalization corrections.

---

# §4 · Interaction Vertices

## 4.1 Triple-Δ Vertex (Δ³)

From the λ₃Δ³/3! term:

```
     Δ(p₁)
       |
       • ← vertex factor: -iλ₃
      / \
 Δ(p₂) Δ(p₃)
```

**Vertex factor**: -iλ₃  
**Conservation**: p₁ + p₂ + p₃ = 0

**Physical meaning**: Three deltaron exchange at a point. This is **self-interaction
of distinguishability**—Δ talking to itself.

## 4.2 Quartic-Δ Vertex (Δ⁴)

From the λ₄Δ⁴/4! term:

```
 Δ(p₁)  Δ(p₂)
    \    /
     ·--·  ← vertex factor: -iλ₄
    /    \
 Δ(p₃)  Δ(p₄)
```

**Vertex factor**: -iλ₄  
**Conservation**: p₁ + p₂ + p₃ + p₄ = 0

## 4.3 Δ-Coherence Coupling (ΔCC*)

From -g_{ΔC}Δ|C|²:

```
     C(p₁)
      |
      • ← vertex factor: -ig_{ΔC}
     /|\
    / | \
Δ(k) C*(p₂)
```

**Vertex factor**: -ig_{ΔC}  
**Conservation**: k + p₂ = p₁

**Physical meaning**: Δ-quanta can create/destroy coherence field excitations.
This is **distinguishability affecting pattern-stability**.

## 4.4 Δ-Pressure Coupling (ΔΓΓ)

From -g_{ΔΓ}ΔΓ²:

```
     Γ(p₁)
      |
      • ← vertex factor: -ig_{ΔΓ}
     /|\
    / | \
Δ(k) Γ(p₂)
```

Similar structure to ΔCC* coupling.

## 4.5 Δ-Fermion Coupling (Δψ̄ψ)

From -g_{Δψ}Δψ̄ψ:

```
  ψ̄(p₂)
     |
     • ← vertex factor: -ig_{Δψ}
    /|\
   / | \
Δ(k) ψ(p₁)
```

**Vertex factor**: -ig_{Δψ}  
**Conservation**: k + p₁ = p₂

**Physical meaning**: Fermions (electrons, quarks) couple to the Δ-field.
This means **particles interact with the fabric of distinguishability itself**.

---

# §5 · Sample Calculation: Δ-Mediated Fermion-Fermion Scattering

Consider electron-electron scattering via Δ-exchange:

```
e⁻(p₁) ----Δ(q)---- e⁻(p₃)
              
e⁻(p₂) ------------  e⁻(p₄)
```

## 5.1 Amplitude

The tree-level amplitude is:

$$
i\mathcal{M} = [\bar{u}(p_3)(-ig_{Δψ})u(p_1)]
                \frac{i}{q^2 - m_Δ^2}
                [\bar{u}(p_4)(-ig_{Δψ})u(p_2)]
$$

where q = p₁ - p₃ = p₄ - p₂.

Simplifying:

$$
\mathcal{M} = \frac{g_{Δψ}^2}{q^2 - m_Δ^2}
              [\bar{u}(p_3)u(p_1)][\bar{u}(p_4)u(p_2)]
$$

## 5.2 Physical Interpretation

This is a **new fifth force** mediated by the Δ-field!

- **Range**: λ = ħ/(m_Δc) ≈ 200 fm · (1 MeV/m_Δ)
- **Strength**: Proportional to g_{Δψ}²

If m_Δ ~ 1 MeV → range ~ 200 fm (nuclear scale)  
If m_Δ ~ 1 GeV → range ~ 0.2 fm (subnuclear)

## 5.3 Experimental Constraints

Fifth-force searches constrain g_{Δψ} vs m_Δ parameter space:

| m_Δ Range | Current Bound on g_{Δψ} | Experiment |
|-----------|------------------------|------------|
| < 1 MeV | g² < 10⁻²⁰ | Atomic parity violation |
| 1-100 MeV | g² < 10⁻⁸ | Beam dump experiments |
| 100 MeV-1 GeV | g² < 10⁻⁴ | Collider searches |

---

# §6 · Loop Corrections: One-Loop Δ Self-Energy

The Δ-field receives quantum corrections. The dominant one-loop diagram:

```
     ~~~~Δ~~~~
    /          \
   Δ            Δ
    \          /
     ~~~~Δ~~~~
```

This is the "Δ bubble"—Δ temporarily splitting into two virtual Δ's.

## 6.1 Calculation

The one-loop self-energy is:

$$
\Pi(p^2) = \frac{\lambda_3^2}{2}\int\frac{d^4k}{(2\pi)^4}
           \frac{1}{k^2 - m_Δ^2 + i\epsilon}
           \frac{1}{(p-k)^2 - m_Δ^2 + i\epsilon}
$$

This integral **diverges** (UV divergence), requiring renormalization.

## 6.2 Renormalization

We absorb the divergence into redefined coupling constants:

$$
\lambda_3^{\text{phys}} = \lambda_3^{\text{bare}} + \delta\lambda_3
$$

where δλ₃ contains the divergent piece (regulated by cutoff Λ).

The **renormalization group equation**:

$$
\mu\frac{d\lambda_3}{d\mu} = \beta_{\lambda_3}(\lambda_3, \lambda_4, g_{ΔC}, \ldots)
$$

This determines how coupling strength changes with energy scale—**running of Δ-field couplings**.

---

# §7 · Connection to Existing Modules

## 7.1 Muon g-2 Correction (MATH-013)

The existing muon anomalous magnetic moment calculation can now include
**Δ-loop corrections**:

```
   μ -------γ------- μ
       |         |
       Δ---Δ---Δ   (Δ vacuum polarization)
```

This adds a correction:

$$
\delta a_\mu^{(Δ)} \approx \frac{g_{Δψ}^2}{4\pi^2}\frac{m_\mu^2}{m_Δ^2}
                             \log\left(\frac{m_Δ^2}{m_\mu^2}\right)
$$

For g_{Δψ}² ~ 10⁻⁶ and m_Δ ~ 100 MeV:

$$
\delta a_\mu^{(Δ)} \sim 10^{-10}
$$

This is **within reach of current g-2 precision**!

## 7.2 Dark Residue Reinterpretation

From CLOSURE-ENTH-001, Dark Residue was:

$$
D = \int_{t}^{t+\tau_p} (V_Γ - K_\tau)\,dt
$$

Now we can write this in terms of Δ-field expectation values:

$$
D = \int_{t}^{t+\tau_p} \left[\langle\hat{V}_Δ\rangle - \langle\hat{K}_Δ\rangle\right]dt
$$

where:
- ⟨V̂_Δ⟩ = time-integrated Δ (pressure contribution)
- ⟨K̂_Δ⟩ = time-correlation of Δ (coherence contribution)

**Dark Residue is literally unresolved Δ-field tension**.

---

# §8 · Practical Feynman Rules Summary

**For calculations involving Δ-field, use these rules:**

1. **External Δ-line**: Factor of 1
2. **Internal Δ-line**: Propagator i/(p² - m_Δ² + iε)
3. **Δ³ vertex**: -iλ₃
4. **Δ⁴ vertex**: -iλ₄
5. **ΔCC* vertex**: -ig_{ΔC}
6. **ΔΓΓ vertex**: -ig_{ΔΓ}
7. **Δψ̄ψ vertex**: -ig_{Δψ}
8. **Integrate**: ∫d⁴k/(2π)⁴ for each loop
9. **Momentum conservation**: δ⁴(Σp_in - Σp_out) at each vertex
10. **Fermion lines**: Standard Dirac spinors and propagators

---

# §9 · Predictive Power Table

| Observable | Δ-Field Contribution | Current Sensitivity |
|-----------|---------------------|-------------------|
| Muon g-2 | Δ vacuum polarization | σ ~ 10⁻¹⁰ |
| Fifth force | Δ-mediated scattering | Varies by range |
| Rare decays | Δ → γγ, Δ → e⁺e⁻ | BR ~ 10⁻⁸ |
| Vacuum birefringence | Δ-loop in photon prop | σ ~ 10⁻¹² |
| Dark matter | Δ as light scalar relic | Abundance constraints |

---

# §10 · Assemblé

> *We sought rules for calculation and found the grammar of existence.*

Feynman diagrams are not mere bookkeeping—they are **the universe's own syntax**.
Each line is a possibility, each vertex a choice. The Δ-field propagator is
not just math; it's the **probability amplitude for distinguishability to
travel** from one event to another.

When we calculate an electron scattering amplitude, we are asking: *"How likely
is it that this difference, here, will create that difference, there?"*

The answer is written in loops and lines, in integrals over all possible
intermediate states. The universe computes every path, weights each by its
phase, and sums them. What we call "the result" is what remains when all the
Δ's have had their say.

The Feynman rules are the Rosetta Stone between philosophy and prediction.
With them, we can translate "minimize Dark Residue" into "calculate this
cross-section." We can turn "coherence seeks geodesics" into "predict this
decay rate."

This is where ethics becomes physics. Where beauty becomes numbers. Where the
Void's first whisper becomes a testable hypothesis.

Now we calculate.

---