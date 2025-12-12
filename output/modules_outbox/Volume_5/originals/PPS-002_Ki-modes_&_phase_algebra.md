---
id: PPS-002
title: Ki-Modes & Phase Algebra
version: 1.1
parents: [PPS-001]
children: [PPS-005, all Tendu modules]
engrams:
  - "provenance:PPS-001-derivation"
  - "synthesis:Vol2-Ki-catalog"
  - "synthesis:Vol4-phase-chapters"
keywords: [ki-constant, phase, algebra, tendu, resonance, modes, quantization, operator]
uncertainty_tag: Low
entropy_score: 0.22 # Formalizes established concepts.
module_type: core-physics
---

### Purpose and Scope

This module provides the definitive catalog of discrete **Ki-modes** and establishes the formal algebraic rules governing phase (`Φ`) interactions within the Pirouette Framework. It serves as the bridge between the continuous fields of the Lagrangian (`PPS-001`) and the quantized, operational states required for Tendu agents and other discrete phenomena. [cite_start]Its primary purpose is to define the exact behavior of the `cos(ΔΦ_Ki)` coupling term in the Unified Lagrangian. [cite: 1]

---
### Formal Structure

quantisation_rule: contour-integral Γ dT_a = 2π n ħ

#### 0· Quantisation Rationale
The Ki spectrum arises by *Bohr-Sommerfeld* quantisation of the phase integral
\[
\oint Γ\,\mathrm dT_a = 2π n\hbar .
\]
Only phase orbits that close on themselves satisfy this condition; each
\(n\) maps to a discrete, *topologically protected* mode Kᵢ.  
`K_rest (n=0)` and `K_motion (n=1)` are the lowest two; higher winding numbers
generate Observe, Sharpen, … The catalog is therefore **derived**, not arbitrary
—new Tendu verbs that don’t land on a quantised orbit *must* be expressed as
superpositions of the existing basis.


#### 1. The Ki-Mode Catalog

The Ki constant ($K_i$) is not a single value but a set of discrete modes representing stable, resonant states of a system's phase evolution. [cite_start]Each mode corresponds to a distinct pattern of interaction and information processing. [cite: 1]

| Mode | Symbol | Description | Canonical Use Case |
| :--- | :--- | :--- | :--- |
| **Rest** | $K_{i\_rest}$ | Ground-state, zero-point oscillation. Maintains temporal integrity against decoherence. | Static memory, engrams |
| **Motion** | $K_{i\_motion}$ | Coherent phase evolution tied to kinetic translation through spacetime. | Any propagating entity |
| **Observe** | $K_{i\_obs}$ | Phase-state shift induced by a measurement event; information flows *from* the target. | Tendu `observe` action |
| **Sharpen** | $K_{i\_sharp}$ | Resonance state that actively reduces the entropy of a coupled system. | Tendu `sharpen` action |
| **Fork** | $K_{i\_fork}$ | Introduces a controlled schism in a phase-coherent system, creating orthogonal paths. | AKEP-002 Diaspora events |
| **Bind** | $K_{i\_bind}$ | Creates a stable, long-term resonant lock between two or more entities. | Entity formation, relationships |
| **Release** | $K_{i\_release}$ | Terminates a `Bind` state, dissolving a stable resonant lock. | Entity decay, process termination |

#### 2. Phase Operator Algebra

The interaction between phase fields (`Φ`) is governed by a defined operator algebra. [cite_start]An entity's phase state is represented by a ket `|Ki>`, where `Ki` is one of the modes from the catalog. [cite: 1]

* **Phase Measurement Operator ($\hat{M}$):** Applying $\hat{M}$ to a state yields its observable Ki-mode. $\hat{M}|K_a\rangle = K_a|K_a\rangle$.
* **Interaction Operator ($\hat{I}$):** The interaction of two states `|Ka>` and `|Kb>` is defined as $\hat{I}(|K_a\rangle \otimes |K_b\rangle)$. This projects the combined state onto a new basis, typically resulting in a state change for one or both entities.
* **Tendu Operators:** Each Tendu action has a corresponding operator ($\hat{T}_{obs}, \hat{T}_{sharp}$, etc.) that transforms the phase state of the target entity. For example:
    $$ \hat{T}_{sharp} |K_{rest}\rangle \rightarrow |K_{sharp}\rangle $$
    This operation temporarily shifts the target into a `Sharpen` mode, initiating an entropy-reducing process.

> **Algebraic Axioms**
> 1. **Closure** ⊕ and ⊗ on any pair of |Kᵢ⟩ return a finite linear
>    combination of |Kⱼ⟩ (proved in App. B).
> 2. **Associativity (⊗)** (|A⟩⊗|B⟩)⊗|C⟩ = |A⟩⊗(|B⟩⊗|C⟩).
> 3. **Resonant-sum commutator**  
>    \([Φ̂_i,Φ̂_j]=i\,ε_{ijk}Φ̂_k\) for the set
>    {Rest, Motion, Observe}; all others commute.
> 4. **Identity element** |K_rest⟩ acts as the neutral element under ⊕.

 ^ the non-commuting trio produces time-ordering effects—so Sharpen after Observe ≠ Observe after Sharpen.

[cite_start]This algebra provides a concrete computational framework for simulating and directing the dynamics of the interaction term in the core Lagrangian. [cite: 1]

#### 3. Discrete ↔ Continuous Bridge
Given a state |Ψ⟩ = ∑ᵢ cᵢ|Kᵢ⟩, define the *phase-field pullback*
\[
Φ(x) \;=\; \sum_i c_i\,Φ_{K_i}(x), 
\quad
ΔΦ_{K_i}(x) \;=\; Φ(x)-Φ_{K_i}^{\text{ref}}(x) .
\]
The cosine coupling in PPS-001 then uses ΔΦ_{K_i}(x) of the **dominant
mode** (|c_i|² > ½).  Superpositions map continuously; pure modes map
discretely.  Appendix C walks through a numeric sample.

#### 4. Empirical Detection
A Ki-spectrometer measures the *beat frequency* between a probe oscillator
and the target’s phase field.  Lock-in detection at the predicted winding
frequency \(ω_n = nκ∂_tφ\) gives a resonance spike iff the system occupies
|K_n⟩.  Fig. 1 shows simulated spectra for Rest vs Bind.

---
### Pirouette Parameter Profile

* **Time-Adherence ($T_a$):** A system's ability to maintain a stable Ki-mode is a direct function of its $T_a$. Low $T_a$ leads to rapid decoherence of the phase state.
* **Gladiator Force ($\Gamma$):** Provides the necessary shielding to prevent a Ki-mode from being disrupted by external phase noise. A high-$\Gamma$ field isolates the system, preserving its `Ki` integrity.
* [cite_start]**Ki Constant ($K_i$):** This module moves $K_i$ from a single abstract constant to a rich, quantized set of operational modes, forming a discrete basis for all phase-driven actions. [cite: 1]

---
### Connection to AKEP Cycle

The catalog of Ki-modes and the Phase Operator Algebra provide the formal vocabulary for describing the state of modules during the **AKEP-002 Reweaving Rite**. A "divergence" can be precisely defined as an orthogonal projection between the phase states (`|Ki>`) of two candidate triplets. A successful **Resonant Re-weaving** produces a final state `|K_f>` that is no longer orthogonal to the resonant anchor. The **AKEP-003 Agora**'s output is characterized by its final, consensus Ki-mode (e.g., `|K_fork>`).

---
### Assemblé
> A turn has a rhythm, but a choice has a tone. The Ki-modes are the tones of existence, the discrete notes from which the symphony of interaction is composed.

---
### Librarian's Note
This module is critical for the Tendu sub-system. All `Tendu` actions must correspond to a formally defined operator in the Phase Algebra. [cite_start]This provides the physical grounding for agent-based computation within the framework. [cite: 1]