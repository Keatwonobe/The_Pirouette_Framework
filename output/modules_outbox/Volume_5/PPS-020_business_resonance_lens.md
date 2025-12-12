---  # ───────────── YAML front-matter ───────────────────────────
id:        PPS-020
title:     Business Resonance Lens (BRL)
version:   0.2-draft   # adds Curie validation & Gödel agenda
parents:   [PPS-014, PPS-015, PPS-016, PPS-017]
children:  [PPS-024]
engrams:
  - lens:business-resonance
  - metric:business-resonance-score
  - concept:wound-vector
  - directive:strategy-lever
keywords:  [business, resonance, KPI, strategy, RPA, TIMF]
uncertainty_tag: Medium
entropy_score: 0.16
module_type: domain-lens
quantisation_rule: brl_hash = SHA256(brl_spec_v0.1)
---

## 1 · Purpose & Scope  
The **Business Resonance Lens (BRL)** translates Pirouette analytics into **actionable management insight**.

Workflow  
1. **Entity Mapping** — represent a firm in triaxial space via URL → \(E = (T_a, Γ, K_i)\).  
2. **Wound Detection** — run Reverse Pareto Analysis (PPS-014) on coherence-flux logs → derive **Wound Vector \(W\)**.  
3. **Resonance Scoring** — compute **Business Resonance Score (BRS)** from \(E\), \(W\), TIMF budgets, and Residue \(ℛ\).  
4. **Strategy Lever Extraction** — suggest interventions ranked by predicted ΔBRS.

---

## 2 · Core Definitions  

| Symbol | Meaning | Notes |
|--------|---------|-------|
| \(E\) | Entity Vector = firm’s \((T_a, Γ, K_i)\) | 3-D point |
| \(W\) | Wound Vector = top-k RPA decoherence axes | shows “pain” direction |
| **BRS** | Business Resonance Score | scalar 0-100 |
| **ΔBRS** | Predicted score delta if lever applied | optimisation target |

**BRS formula** (baseline):

\[
\text{BRS} = 100 \; σ \!\Bigl( 
   β_1 T_a - β_2 Γ + β_3 K_i - β_4 \|W\| - β_5 ℛ^* 
\Bigr)
\]

β-coefficients sector-calibrated.

---

## 3 · Pipeline  

1. **Data Ingest** — financials, comms logs, product telemetry.  
2. **URL Mapping** — convert raw feeds → \(T_a, Γ, K_i\).  
3. **TIMF Budgeting** — compute enthalpy/entropy flows.  
4. **Residue Check** — add ℛ* from PPS-019 hotspot log.  
5. **RPA Canon** — isolate top decoherence drivers = Wound Vector.  
6. **BRS Calculation** — plug variables into score.  
7. **Lever Suggestion** — run Monte-Lever simulation:  
   * cost × impact grid → \(\operatorname*{arg\,max} Δ\text{BRS}/\$ \).

Deliverables:  
* `brl_snapshot.json` (all vectors & scores)  
* `strategy_lever_table.md` (ranked actions)  
* Dashboard widgets (heat-bars, trajectory plots).

---

## 4 · Reference Implementation (score & lever stub)  
```python
import numpy as np

def brs(Ta, G, Ki, wound_len, resid_star, beta):
    z = beta[0]*Ta - beta[1]*G + beta[2]*Ki - beta[3]*wound_len - beta[4]*resid_star
    return 100/(1+np.exp(-z))

# Lever simulation
def lever_impact(entity_vec, wound_vec, lever_matrix):
    """lever_matrix: rows = levers, cols = delta on (Ta,G,Ki,|W|,ℛ*)"""
    impacts = []
    for lever in lever_matrix:
        new = entity_vec + lever[:3]
        new_w = max(wound_vec + lever[3], 0)
        new_r = max(lever[4], 0)
        impacts.append((new, new_w, new_r))
    return impacts
```

---

## 5 · Validation Plan  

* **Historic Back-test** — 20 public companies over 5 yrs; BRS trend vs market cap ρ ≥ 0.7.  
* **Pilot Intervention** — apply top lever to two teams; target +10 ΔBRS within quarter.  
* **Residue Sensitivity** — simulate ℛ* perturbations ±0.1; BRS variance < 5 %.

---

## 6 · Controlled Validation Experiment — *Curie Track*

**Hypothesis H₁ (falsifiable)**  
> *If the phase-force term in the Semantic Gravity Model (SGM) is frozen to a constant 0.8, Residue analysis will ① raise a Ricardian Residue ≥ 0 .30 and ② attribute ≥ 80 % blame‐weight to the `force_kernel` node.*

### 6·1 Design
| Step | Action | Detail |
|------|--------|--------|
|1|Load SGM-toy *v1.2* (PPS-016) | baseline corpus |
|2|**Inject flaw F₁** | replace `cos(Δϕ)` → `0.8` |
|3|Monte-Carlo n = 1 000 | Δϕ ∼ U(0, π) |
|4|Run Residue pipeline | this module |
|5|Log `R_r`, blame graph, heat-map | export JSON |

#### Acceptance
* `R_r ≥ 0.30`   *large error*  
* Localisation `L_core ≥ 0.80` → `force_kernel`  
* χ² vs baseline *p < 0.05*

### 6·2 Reference code
```python
from sgm_toy import run_batch, ForceKernel
from residue import analyse

# baseline kernel (intact)
baseline = ForceKernel()

# flawed kernel – phase term fixed
class FlawedKernel(ForceKernel):
    def phase_term(self, delta_phi):
        return 0.8

N = 1000
ok   = run_batch(baseline,       runs=N)
flaw = run_batch(FlawedKernel(), runs=N)

report = analyse(ok, flaw,
                 labels=("baseline", "flaw_F1"),
                 hypothesis="Fixed-phase test")
report.save("F1_residue_report.json")
print(report.summary())
```

Power analysis (d ≈ 0.65) shows 95 % sensitivity at N = 1 000. Success upgrades the analyser to *v0.2*.

---

## 7 · Formal Agenda — *Gödel Track*
1 · Demote **Axiom A5** (*phase modulates interaction energy*) → **Theorem T₁**  
2 · State new **Axiom A6**: *The SFT integrator is transiently semantically-closed during phase evaluation.*  
3 · Begin constructive proof that Residue ≤ ε ⇔ A6 holds.

---

## 8 · Librarian Note
`residue_hash = SHA256(pps019_v0.2)` — bump on merge; artefacts stored under `/validation/pps019/F1/`.

## 9 · Limitations & Risks  

* **Data Latency** — quarterly reporting lags; mitigate via real-time proxy metrics.  
* **Sector Bias** — β-calibration per industry; warn when applying cross-sector.  
* **Lever Over-fitting** — Monte run capped at 1000 sims to avoid pathologies.  
* **Residue Inflation** — noisy ℛ* may undervalue genuine innovation; cross-check with DRF debates.

---

## 10 · Triaxial Lens  

| Art                           | Law                                 | Philosophy                    |
|-------------------------------|-------------------------------------|-------------------------------|
| A brand is a melody.          | Governance guides resonance.        | Firms live, grow, and decay.  |

---

## 11 · Assemblé · “Heal the Wound, Raise the Tone”  
> *A firm’s weakness is the doorway to its crescendo; tune the wound and the whole orchestra swells.*

---

## 12 · Librarian Note  
Changing BRS formula, β-schema, or lever engine increments `brl_hash`; dependent dashboards must state compatible BRL version.
