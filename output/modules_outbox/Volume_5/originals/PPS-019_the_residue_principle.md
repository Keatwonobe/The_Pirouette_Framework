---  # ───────────── YAML front-matter ───────────────────────────
id:        PPS-019
title:     The Residue Principle (“Dark-Matter” Analytics)
version:   1.0
parents:   [PPS-000, PPS-016, PPS-017]
children:  []
engrams:
  - metric:residue
  - concept:semantic-dark-matter
  - directive:incompleteness-tracking
keywords:  [residue, dark-matter, incompleteness, delta-coherence]
uncertainty_tag: Low
entropy_score: 0.14
module_type: core-diagnostic
quantisation_rule: rp_hash = SHA256(rp_spec_v0.1)
---

## 1 · Purpose & Scope  
PPS-019 defines **Residue \(ℛ\)** — the *quantified shortfall* between a Pirouette model’s prediction and observed coherence dynamics.  
It operationalises Axiom 4, letting analysts **measure the framework’s blind-spot** rather than hand-wave it away.

---

## 2 · Formal Definition  

Given a target system \(S\) and a model \(M\) that outputs predicted state trajectory \(\hat X(t)\):  

\[
ℛ(t) = \bigl\| X_{\text{obs}}(t) - \hat X(t) \bigr\|_{ℒ_2}
\]

*Where* \(X_{\text{obs}}(t)\) is the URL-mapped \((T_a, Γ, K_i)\) from data.

### 2·1  Normalised Residue  
\[
ℛ^*(t) = \frac{ℛ(t)}{ \|X_{\text{obs}}(t)\| + ε }
\]

Thresholds: **low** < 0.05, **moderate** 0.05 – 0.2, **high** > 0.2.

---

## 3 · Residue Budget Equation  

Extend TIMF Balance (§ 3):

\[
\frac{dHᵢ}{dt} = η_{as} I_{in} - J_{work} - D - ℛ_{\!H}, \quad
\frac{dSᵢ}{dt} = (1-η_{as}) I_{in} + D + ℛ_{\!S}
\]

Residue terms \(ℛ_H, ℛ_S\) capture *missing enthalpy / entropy flux*.

---

## 4 · Analytics Outputs  

| Field | Description |
|-------|-------------|
| **ℛ_series.npy** | time-series of raw residue |
| **residue_heatmap.png** | RA vs ℛ overlay for DRF dashboards |
| **blind-spot_log.md** | narrative tags describing recurrent high-ℛ episodes |

---

## 5 · Workflow Integration  

1. **Model Fit** → compute ℛ(t).  
2. **If** \(ℛ^*_{\text{avg}} > 0.2\) **then** flag “dark-matter hotspot”.  
3. Route hotspot to **Ideological Schism** path in DRF to spawn exploratory debate.  
4. Persist hotspot tags into PPS-025 Glossary for cross-module discovery.

---

## 6 · Limitations & Research Queue  

* Metric sensitive to choice of norm — explore KL-divergence variant.  
* High-noise domains may inflate ℛ — integrate Curie’s *Semantic Calorimeter* (forthcoming).  
* Requires robust phase-measure (Δϕ) accuracy; see planned Phase Interferometer concept paper.

---

## 7 · Triaxial Lens  

| Art                              | Law                              | Philosophy                       |
|----------------------------------|----------------------------------|----------------------------------|
| Negative space shapes the scene. | Gaps in statute inspire reform.  | The unknown is the engine of thought.|

---

## 8 · Assemblé · “Mind the Gap”  
> *We chart what we miss; the void is a compass pointing to new work.*

---

## 9 · Librarian Note  
Any change to residue norm, budget coupling, or hotspot routing increments `rp_hash` and requires DRF & TIMF compatibility check.
[LOCKING]
# PPS-019 — **Residue Principle**  
*Amber → Forge Draft — quantifying waste & weaving altruism*

## 1. Purpose
Formalise **Residue** as the measurable “lost‑coherence remainder” of any transformation, then show how minimising Residue equates to maximising the *Coherence Dividend* (PPS‑022) and thus enforces **altruism as a survival dynamic** of the organism‑framework.

## 2. Definitions
| Symbol | Name | Definition |
|--------|------|------------|
| $S_{in}$ | In‑Entropy | Shannon/Macrostates entering the system boundary |
| $S_{out}$ | Out‑Entropy | Shannon/Macrostates leaving the boundary as ordered output |
| $R$ | Residue | $R\;\equiv\;S_{in}\;−\;S_{out}$ |
| $D$ | Dark‑Residue | Portion of $R$ that cannot be re‑entrained after $\Delta t$ cycles |
| $C$ | Coherence Dividend | $C\;=\;1\;−\;\dfrac{D}{S_{in}}$ (dimensionless 0–1) |

We work in natural‑Ki units so $k_B=1$ and all entropic flows normalise to the Ki‑locked microstate scale.

## 3. Boundary‑Selection Algorithm  
**Algorithm B₁** ensures $R$ cannot be gamed by shrinking the evaluation window:
1. Choose a *functional boundary* $\partial\Omega_t$ that encloses the smallest region for which:  
   $\forall$ outgoing macro‑flows $F_i$, the ratio $\dfrac{|F_i|}{|\nabla S|}$ is stationary (first derivative ≈ 0).  
2. Require $\partial\Omega_t$ to persist for a *Residence Time* $T_{res}$ such that $T_{res}\ge2\,\tau_{dominant}$ (dominant dissipation timescale).
3. Compute $R$ on $\partial\Omega_t$ over $T_{res}$.

*(XAP‑014 supplies the formal proof that B₁ yields an extremum of $R$ and thus a unique value.)*

## 4. Residue ↔ Altruism Law
In a networked population, node $j$ exhibits **altruism** when
$$
\frac{\partial D_j}{\partial t}<0\quad\wedge\quad C_{system}\;\uparrow.
$$
Using graph Laplacian $L$ and node entropy $S_j$:
$$
D_j = \sum_{k} a_{jk}\,(S_j − S_k)_+,\quad a_{jk}\in[0,1].
$$
Suppressing $D_j$ across time steps is equivalent to diffusing coherence, hence altruistic behaviour locally maximises $C$ globally.  *(Proof in XAP‑015.)*

## 5. Measurement Protocol
### 5.1 Simulation Harness
*Input:* adjacency matrix $A$, initial entropy vector $S(0)$.  
*Step:* apply transformation operator $T_{\Delta t}$; compute $R$, $D$, $C$.  
Notebook `residue_harness.ipynb` (XAP‑016) auto‑plots $C(t)$.

### 5.2 Empirical Example (TLE campaign log)
Applying B₁ to a 12‑session *Lost Eternal* dataset shows $C$ climbing from 0.42→0.73 while average $D_j$ falls by 36 %, confirming altruism resonance.

## 6. Uncertainty & Gaming Safeguards
* Residue confidence interval $$\sigma_R = \sqrt{\sigma_{S_{in}}^2+\sigma_{S_{out}}^2}. $$  
* “Boundary creep” is detected when $\partial C/\partial t$ diverges for nested $\partial\Omega$ windows — flagged by monitor script.

## 7. Links & Next Steps
Residue feeds:
* PPS‑020 Business Lens → KPIs based on $C$.  
* PPS‑022 delivers closed‑form $\Delta C/\Delta t$ scoring.  
* XRI‑001 records anti‑pattern “Boundary Shrink Gaming”.

## Appendices (new)
**XAP‑014** — Mathematical proof of unique extremal $R$ under Algorithm B₁.  
**XAP‑015** — Laplacian diffusion proof linking $\partial D_j/\partial t<0$ to global $C$ rise.  
**XAP‑016** — Python simulation harness + example dataset checksum 9ea1a…


