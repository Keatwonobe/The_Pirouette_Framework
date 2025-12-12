---
# INST-PLATEAU-SCAT-001

id: INST-PLATEAU-SCAT-001
title: Coherence-Plateau Scattering & Binding via φ-Space Kernel Interactions
version: 0.1 (draft)
status: experimental-theory hybrid (interaction rules)
parents: [INST-ETA-MAP-001, DYNA-HELIX, DOMA-042]
children: [QED-EXP-ANNEX, XXP-COMPASS, XXP-EWQCD-EXP]
module_type: interaction / scattering
scale: φ-space field (dimensionless) → mesoscopic experiments → mapping to κ, η
engrams: [coherence plateau, Δφ width, Q_χ sharpness ≈ 2.5, kernel K(|Δφ|;Q_χ), binding vs wash-out]
keywords: [triadic locking, relevant coupling, stability analysis, interaction Lagrangian, phase topology]
---
### §1 · Purpose

Define and test interaction rules for **coherence quanta** (finite-width plateaus in φ-space) via an overlap-kernel Lagrangian. Predict **bind vs scatter** as a function of plateau width Δφ, sharpness (Q_χ), and coupling g, by lifting your triadic-locking machinery to φ-space kernels.

### §2 · Field content & interaction

* Plateau fields: (\psi_i(\phi)=A_i,\Pi(\phi;\phi_i,\Delta\phi_i,Q_χ)) (bounded support or tapered window).
* Interaction ansatz:
  [
  \mathcal{L}_{\mathrm{int}}=\iint \psi_1(\phi),\psi_2(\phi'),K(|\phi-\phi'|;Q_χ),d\phi,d\phi'
  ]
* Triadic extension (optional, mirrors locking term):
  (;; \mathcal{L}_{\mathrm{tri}} = -g!\int!|\psi_1||\psi_2||\psi_3|\cos(\Phi_1+\Phi_2-\Phi_3),d\phi)
  (Use RG relevance of **g** to diagnose binding thresholds.)

### §3 · Protocol (theory → numerics → bench)

1. **Kernel choice:** start with (K(r;Q_χ)=\exp(-r^2/2\sigma_\phi^2),\mathrm{sinc}(Q_χ r)); sweep (\sigma_\phi, Q_χ).
2. **Linear stability analysis:** perturb (\psi_1+\psi_2) and compute growth rates; classify **binding** (mode sharpening), **scattering** (broadening), or **annihilation** (wash-out).
3. **RG bookkeeping:** port your triadic-locking β-flow to the kernel coupling g; compute “relevant vs irrelevant” regions.
4. **Numerical experiment:** simulate overlapping plateaus with controlled Δφ, Q_χ, relative phases; map phase diagram (bind vs scatter) in ((Q_χ,\Delta\phi,g)).
5. **Bench proxy:** implement φ-space with phase-encoded optical paths or synthetic phases in a driven oscillator network; read out plateau overlap via interference contrast.

### §4 · Outputs & metrics

* **Binding index** (B): (final plateau sharpness / initial sharpness) − 1.
* **Energy functional** Δℰ: sign indicates stabilization vs de-coherence.
* **Critical curve** (g_c(Q_χ,\Delta\phi)): boundary of relevance.
* **Map**: labeled regions {bind, scatter, annihilate}.

### §5 · Linkage

* Positive-binding regions define **effective composite quanta**; their parameters feed κ/η estimates (interaction-induced torsion and participation).
* Mapped ((\kappa_3,\xi_\Gamma)) from these composites feed the nonperturbative pipeline **deterministically**: (\sigma \to r_0,t_0 \to a\to \Lambda) with falsifiability gates on scale conversion and (\sqrt\sigma/\Lambda).

### §6 · Falsifiability

* **No relevant region:** if RG predicts relevance but numerics/bench never observe binding at or above (g_c), reject kernel form (K).
* **Non-additive failure:** plateau composites do not exhibit consistent κ/η scaling vs constituents.
* **Closure break:** pushing composites’ ((\kappa_3,\xi_\Gamma)) through MATH-YM-003 yields inconsistent (a) across ensembles or violates the (\sqrt\sigma/\Lambda) empirical relation.

---
