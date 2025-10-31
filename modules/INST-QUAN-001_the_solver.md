---
id: INST-QUAN-001
title: The Solver (Pirouette Quantum Solver, PQS)
version: 2.0
status: Validated
parents: [CORE-006, DOMA-042, DOMA-083]
children: [INST-QUAN-002, INST-QUAN-003]
authors: [Keaton Smith]
summary: >
  Re-defines the Pirouette Quantum Solver as a quantized geodesic instrument.
  Integrates experimental confirmation of the helical-ramp plateau (PHA-χ),
  where coherence becomes discretized into bounded manifolds — coherence quanta.
  Demonstrates that optimization is not pointwise but occurs across
  finite, particle-like plateaus of maximal coherence.

keywords:
  - quantum solver
  - Pirouette Hamiltonian
  - coherence plateau
  - helical ramp
  - chiral quantization
  - geodesic stability
  - Ki–Γ equilibrium
  - PHA-χ ansatz
  - resonance curvature
  - coherence quanta
---

# **INST-QUAN-001 — The Solver**

## **1. Law**
The **Pirouette Quantum Solver (PQS)** translates the **Pirouette Lagrangian** (CORE-006) into a
**quantized Hamiltonian manifold**, treating optimization as the emergence of a *plateau of coherent stability*
bounded by intrinsic geometric limits in phase space.

\[
S_p = \int (K_{\tau} - V_{\Gamma})\,dt
\quad\Longleftrightarrow\quad
H_p = H_{V\Gamma} - H_{K\tau}.
\]

Each quantum state |ψ⟩ represents a local coherence manifold; its ground state |ψ₀⟩ is the maximal equilibrium
between **temporal pressure** (V_Γ) and **internal resonance** (K_τ).

| Term | Mapping | Meaning |
|:--|:--|:--|
| V\_Γ | Σ hᵢ σᶻᶦ | External constraint / temporal potential |
| K\_τ | Σ Jᵢⱼ σᶻᶦ σᶻʲ | Internal Ki resonance / coherent coupling |

---

## **2. The Helical Resonance Mapping (PHA-χ)**
Experimental validation shows that a **two-layer helical-ramp ansatz (L = 2)** forms the *minimal chiral manifold*.
For N = 6, this geometry yields near-perfect coherence (median overlap ≈ 0.976) and a **quantized plateau**
in the phase-ramp parameter φ:

\[
\phi_L < \phi^* < \phi_R.
\]

This *plateau* is the **geodesic stability corridor** where
\(H_{V\Gamma} \approx H_{K\tau}\).

| Symbol | Meaning | Physical Analogy |
|:--|:--|:--|
| φₗ | under-twist boundary | coherence slip; Γ dominates |
| φᵣ | over-twist boundary | torsion/kink; Ki dominates |
| φ\* | plateau center | chiral equilibrium |
| Qχ = φ\*/(φᵣ − φₗ) | resonance sharpness | degree of quantization |

Measured (N = 6, L = 2):  
φ\* ≈ 0.15 rad Δφ ≈ 0.06 Qχ ≈ 2.5 Curvature ≈ +0.12 (convex).

---

## **3. Scaling Law**
The plateau obeys a predictive quantization:

\[
\boxed{\phi^\*(N,L)\;\approx\;0.7\,\frac{\pi}{(N-1)\,L(L+1)/2}}
\]

with safe tolerance ± 0.2 φ\*.  
As N or L increase, φ\* contracts ∝ 1/(N L²): the coherence packet sharpens into a *smaller particle*.

---

## **4. Physical Interpretation**
The plateau’s finite width reveals **quantized chirality**:
coherence is discrete — a topological bound on continuous phase space.

- Inside [φₗ, φᵣ] → field-like regime: smooth coherent evolution.  
- Outside [φₗ, φᵣ] → particle jump: discrete geodesic transition.

Thus, the PQS identifies **quantum optimization as a topological resonance**, not mere scalar minimization.
Each plateau is a *coherence quantum*, the tangible unit of the Pirouette Field.

---

## **5. Experimental Protocol**
1. Sweep φ ∈ [0, 0.3] rad → locate (φₗ, φᵣ).  
2. Compute σ\_MAD and define plateau where gap(φ) ≤ gₘᵢₙ + σ\_MAD.  
3. Record φ\*, Δφ, Qχ, and curvature at min.  
4. Verify persistence across random instances.  
5. Compare φ\*(N,L) to scaling law for validation.

---

## **6. Significance**
This establishes the **boundary quantization principle**:

\[
\text{Temporal continuum} \;\longleftrightarrow\;
\text{Discrete coherence quanta}.
\]

Optimization therefore synthesizes *particles of coherence* — finite, self-bounded regions of maximal Ki–Γ balance.
Within these plateaus the solver “becomes” the problem’s own stable manifold.

---

## **7. Successor Instruments**
- **INST-QUAN-002 – Helical Field Sampler**: maps φ-space curvature directly.  
- **INST-QUAN-003 – Resonance Thermostat**: measures plateau persistence under decoherence and temperature drift.

---

## **8. Epilogue**
A classical computer chisels a million paths through stone, seeking the weakest point.  
A quantum solver built under this law *becomes the fault line itself* —  
and the mountain reveals its own cleavage plane.  
We once shouted at the universe through brute force;  
now, for the first time, we whisper in its native tongue.
