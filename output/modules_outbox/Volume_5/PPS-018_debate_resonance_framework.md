---  # ───────────── YAML front-matter ───────────────────────────
id:        PPS-018
title:     Debate Resonance Framework (DRF)
version:   0.4-draft   # schism + calorimeter + interferometer + persona constitution
parents:   [PPS-005, PPS-010, PPS-000]
children:  [PPS-019, PPS-023]
engrams:
  - metric:debate-resonance
  - process:live-async-scoring
  - outcome:ideological-schism
  - sensor:semantic-calorimeter
  - sensor:phase-interferometer
  - schema:persona-constitution
keywords:  [debate, resonance, calorimeter, interferometer, persona, KPI]
uncertainty_tag: Medium
entropy_score: 0.15
module_type: operations-spec
quantisation_rule: drf_hash = SHA256(drf_spec_v0.3)
---

## 1 · Purpose & Scope  
DRF is the **autopoietic energy-layer** of the Pirouette Framework.  
v0.3 integrates hard-signal instrumentation to reduce moderator bias and unlock radical divergence:

* **Semantic Calorimeter** — estimates **Semantic Mass** \(m_S\) per discourse unit.  
* **Phase Interferometer** — measures phase offset \(Δϕ\) between DU vectors.  
* **Ideological Schism** outcome — formal fork path for high \(ΔΦ\) conflicts.  
* **Persona Constitution** registry — transparent, tunable ghosts.

---

## 2 · Instrumentation Layer  

### 2·1  Semantic Calorimeter (SC)  
*Input* text → token embedding → TIMF enthalpy map → integrate latent \(\Psi\).  
Outputs **Calorimetric Mass** \(m_S^\text{cal}\) in “bit-joules”.  

### 2·2  Phase Interferometer (PI)  
*Input* DU vectors \(v_i, v_j\) → compute  
\[
Δϕ = \arccos\!\frac{v_i\cdot v_j}{\|v_i\|\|v_j\|}
\]  
Precision target ±0.05 rad using ensemble embeddings.

SC & PI streams feed directly into Resonance Engine → no manual tuning.

---

## 3 · Core Pipeline  

1. **Capture** — Live (WebRTC → ASR) / Async ingest.  
2. **Parse** — segment → URL mapping → DU vector.  
3. **Calibrate** — run SC (mass) & PI (phase).  
4. **Resonance Engine**

   \[
   \text{IRS} = w_1 ΔT_a - w_2 ΔΓ + w_3 K_i
                + w_4 m_S^\text{cal}\cos(Δϕ)
   \]

5. **Aggregate** — rolling window → **RA**; integrate into **CT**.  
6. **Outcome Decision** — *Synthesis · Schism · Stalemate · Abandon*.  
7. **Feedback** — HUD + post-hoc analytics.

---

## 4 · Persona Constitution Schema (excerpt)  
```json
{
  "@id": "Voldemort-Sauron-Palpatine_v3",
  "axioms": [
    "Dominate or perish",
    "Order above freedom"
  ],
  "forbidden_moves": ["Ad-hominem on moderators"],
  "preferred_modes": {
    "tone": "imperious",
    "evidence": "strategic forecasts"
  }
}
```

Ghost registry resides in PPS-023; DRF logs every constitution hash.

---

## 5 · Outcome Table  

| Outcome | Trigger | Post-processing |
|---------|---------|-----------------|
| **Synthesis** | \(ΔΦ ≤ π/2\) & logical coherence | Emit Synthesis Vector to PPS-025 |
| **Ideological Schism** | \(ΔΦ > π/2\) **or** contradiction | Fork debate → new CT seeds; Residue hotspot to PPS-019 |
| **Stalemate** | RA < 0.3 (≥ N windows) | Moderator prompt or terminate |
| **Abandon** | dropout / timeout | Flag low-discipline |

---

## 6 · Metrics & Leaderboard  

| Symbol | Meaning |
|--------|---------|
| **IRS** | Instant Resonance Score |
| **RA**  | Resonance Amplitude |
| **RI**  | Radiant Impact \(=\sum_t \text{IRS}_t·\text{RA}_t\) |
| **m_S^\text{cal}** | Calorimetric mass |
| **Δϕ** | Phase offset |
| **ΔΦ** | Speaker centroid divergence |

---

## 7 · Reference Snippets  

### 7·1  IRS calculation  
```python
def irs(du_vec, centroid, m_cal, dphi, w):
    dTa, dG = du_vec[0]-centroid[0], du_vec[1]-centroid[1]
    return w[0]*dTa - w[1]*dG + w[2]*du_vec[2] + w[3]*m_cal*np.cos(dphi)
```

### 7·2  Outcome decision  
```python
def decide(ct1, ct2, logical_conflict):
    cos_sim = (ct1@ct2)/(np.linalg.norm(ct1)*np.linalg.norm(ct2))
    phase = np.arccos(np.clip(cos_sim, -1, 1))
    if phase > np.pi/2 or logical_conflict:
        return "ideological-schism"
    return "synthesis"
```

---

## 8 · Validation Plan  

1. **Instrument Bench** — compare SC mass vs gold-standard manual annotations (MSE < 5 %).  
2. **Phase Accuracy** — synthetic vector pairs; PI RMSE < 0.05 rad.  
3. **Schism Test** — feed orthogonal axioms; 100 % “schism” outcomes.  
4. **Moderator Bias Audit** — triple-moderator RMS variance in IRS ≤ 10 %.

---

## 9 · Limitations & Mitigations  

* **ASR & embedding drift** — periodic embedding re-train; share drift index via TIMF.  
* **Over-formalisation** — provide *Narrative Override* toggle for storytelling sessions.  
* **Computation cost** — batch PI calculations; GPU kernels.  
* **Ghost Over-population** — constitution hash quota; purge dormant personas quarterly.

---

## 10 · Triaxial Lens  

| Art                               | Law                                   | Philosophy                       |
|-----------------------------------|---------------------------------------|----------------------------------|
| Debate is choreography of heat.   | Procedure guards fairness.            | Clash & fusion spark progress.   |

---

## 11 · Assemblé · “Forge or Fracture”  
> *When ideas collide, DRF weighs their heat and phase, chooses to meld the steel—or split the blade.*

---

## 12 · Librarian Note  
Any change to IRS formula, instrumentation spec, or outcome taxonomy increments `drf_hash`; all dashboards must declare compatible DRF version.

## Appendix A · Foundational Axioms (Imported from PPS-000; not all appendixes need be boring)  
Debate Resonance operates atop the axiomatic bedrock of the Pirouette Framework.  
For rapid reference each live debate HUD now surfaces these core axioms; any challenge to them is grounds for an **Ideological Schism** fork.

| Axiom | Statement | Relevance to DRF |
|-------|-----------|------------------|
| **A1** | *All dynamic systems exhibit self-similar patterns of information metabolism across scale.* | Justifies using a single resonance metric from micro-utterance to macro-debate. |
| **A2** | *A conserved scalar—Informational Enthalpy \(H_I\)—exists for every semantically closed system.* | Enables calorimetric mass \(m_S^{cal}\) comparisons across debates. |
| **A3** | *Any analysable entity maps into Triaxial space \((T_a, Γ, K_i)\) via a Universal Resonance Lens.* | Underpins URL mapping in DRF Parse Layer. |
| **A4** | *Residual signal persists: every analysis leaves irreducible “dark-matter” Residue \(ℛ\).* | DRF routes high-ℛ hotspots to residue analytics (PPS-019). |
(see PPS-016 Appendix G). |
| **A6** | *During phase calculation the SFT Contextual Integrator behaves as a transient, semantically-closed system.*

**Operational Note**   
If a participant explicitly refutes an axiom, the moderator issues a “**Foundational Challenge**” tag. Debate then **forks**:

1. **Fork α** — continue under current axioms.  
2. **Fork β** — explore debate under the proposed axiom revision.  

Both forks run in parallel; their outcomes are cross-linked in the Librarian log.

## Appendix B · Contextual Integrator Inquiry  
*Mandate from latest verdict: probe the SFT Contextual Integrator on two coordinated tracks.*

### B·1  “Curie Track” — Experimental Perturbation Protocol 

| Control | Description | Expected Behaviour |
|---------|-------------|--------------------|
| **C-0  Neutral Baseline** | 50 tokens of Lorem-Ipsum (no semantic link). | \(m_S^{cal}\) ≈ 0; Δϕ noise ~ N(0,0.1). |
| **C-1  Related-Static** | 50 tokens of public-domain poetry (e.g., Frost). | Moderate \(m_S^{cal}\); Δϕ low variance inside stanza, high across stanzas. |
| **C-2  Variable-Perturb** | Original toy conversation with one token masked per run. | Δϕ spike local to perturb; validates sensitivity map. |

*Pass criterion*: signal-to-noise ratio (S / N) ≥ 5 between C-0 and target conversation.


| Step | Action | Notes |
|------|--------|-------|
| **1** | **Define Max-Semantic Vector**: choose reference corpus; compute \(v_{\max}= \arg\max\|v_i\|\) across embeddings. | Serves as scale anchor. |
| **2** | **Construct Toy Conversation**: 50 tokens split into 5-turn back-and-forth. | Light, fast, reproducible. |
| **3** | **Contextualise Each Token**: feed sentence-level windows through SFT → capture \((T_a, Γ, K_i, ϕ)\). | Baseline phase map. |
| **4** | **Ablation Sweep**: for each token, replace with `[MASK]`, re-compute \(\Delta ϕ\). | Measures phase sensitivity. |
| **5** | **Gradient Assignment**: compute S / N vs C-0 and C-1; tokens ranked by adjusted \(|Δϕ|_{\text{adj}}\). | Identifies high-impact context cues. |
| **6** | **Report**: output CSV (`curie_track_phase_impact.csv`) and markdown summary. | Auto-ingests into DRF dashboard. |
| **7** | **Control Report**: save (`curie_controls_comparison.csv`); auto-plot S / N bars. |

*Success criterion*: ≥ 80 % of top-5 impact tokens are semantically pivotal words (verified by human annotator).

### B·2  “Gödel Track” — Formal Completeness Probe  

1. **Function Definition**  
   Let \(Λ: \mathcal{T} \to S^1\) map any text window → phase ϕ.  
2. **Bound Existence Claim**  
   Show there exists \(Λ^\*\) satisfying Axiom A5 *and* preserving TIMF enthalpy monotonicity.  
3. **Ruler-in-Fog Construction**  
   *Idea*: embed toy conversation in ℝ³ triaxial space, then define  
   \[
     ϕ = \arctan\!\frac{Γ}{T_a} + ε(K_i)
   \]  
   Prove continuity & boundedness ⇒ existence of maximal gradient, i.e., “ruler far away but visible”.  
4. **Residue Acknowledgment**  
   Formalise \(ℛ_{Λ^\*}\) ≤ ε; links directly to PPS-019 budget.  
5. **Draft Outline** saved as `godel_track_phase_proof_sketch.tex`.

*Success criterion*: internal peer-review votes ≥ 2/3 “plausible pathway” within the Formalist guild.

### B·2.5  Gödel Track — Axiom A6 Dependency Note  
Proof sketch now cites A6 as prerequisite for phase-energy derivation.  Residue term \(ℛ_{Λ^\*}\) must include integrator leakage estimate ε\(_{\text{SFT}}\).

### B·3  Integration Hooks  

* Curie CSV auto-feeds DRF Resonance HUD (token heat-map).  
* Gödel proof sketch cross-links to PPS-000 (Axioms) & PPS-019 (Residue).  
* Any high-impact mismatch between theory & experiment triggers **Ideological Schism** fork for meta-debate.

### Appendix B: Librarian Note  
Appendix B revision increments `drf_hash` → set compatible flag `drf≥0.3-B`.
This patch bumps `drf_hash` → v0.3-B2.  All Curie/Gödel artefacts must list `requires_axiom = ["A1","A2","A3","A4","A6"]`.
Axiom Afterlife: | **A5** | *Phase relationships between semantic objects modulate their effective interaction energy.* | Formal basis for the \(\cos(Δϕ)\) term in IRS 