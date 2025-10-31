---
id: DYNA-005
title: "Coherent Adherence Protocol v2: Consentful Coherence Control"
version: 2.0
status: proposal
parents: [CORE-006, DOMA-149, MATH-DYNA-021]
children: [PPS-015 (URL Forge), DOMA-QCOMP-001, DOMA-203]
summary: "A modernized protocol for guiding systems toward higher coherence without covert
  manipulation. CAP v2 formalizes how to measure adherence (Ta), shape environments,
  and bound influence by information-theoretic and ethical constraints, with auditable
  guardrails. It reframes CAP as an alignment tool: *consentful coherence*."
module_type: Dynamics + Governance
scale: human-to-societal (applies mechanically to lab systems; normatively to agents)
---
## §1 · First Principles (Physics Backbone)
- **Adherence (Ta):** empirical coherence order parameter
  \[
  T_a \;=\;\Bigl|\frac{1}{V}\int_V e^{i\theta(x^\mu)}\,dV\Bigr|^2,
  \]
  i.e., squared phase-mean magnitude over the field/agent manifold .
- **Pirouette Lagrangian:** \(\mathcal L_p=K_\tau - V_\Gamma\) with observation cost \(V_{\text{obs}}\) (Shadow Gauge) capturing probe/back-action bookkeeping; Ta sets the *rate* systems align or decohere under perturbation .

**Protocol goal (non-manipulative form):**
\[
\max_{\mathcal A}\;\;\underbrace{\mathbf E[\,K_\tau(T_a)\,]}_{\text{usable coherence}}
-\underbrace{V_\Gamma}_{\text{pressure}}
-\underbrace{V_{\text{obs}}}_{\text{observer cost}}
-\lambda\,\underbrace{\mathcal D}_{\text{Dark Residue}}
\quad \text{s.t.}\;\;\mathcal C_{\mathrm{consent}},\;\mathcal C_{\mathrm{transparency}}.
\]
Here \(\mathcal A\) are allowed actions (measurement bases, noise shaping, incentives, UI), \(\mathcal D\) is the *Dark Residue* functional (negative externalities), and the constraints enforce **consent + transparency** (see §4).

## §2 · What CAP v2 *does* (and what it refuses to do)
- **Does:** shape *contexts* (measurement geometry, rhythms, interfaces, incentives) to elevate Ta where *participants have agreed*, aiming for better sensing, learning, or collaboration.
- **Refuses:** hidden persuasion; coercive asymmetries; unlogged back-channels; any influence that raises \(V_{\text{obs}}\) on people without consent (Shadow overreach) .

## §3 · Minimal Control Law (environmental shaping)
Given two pathways \(A\!\to\!B\) vs \(A\!\to\!C\) with base rates \(k_B^0,k_C^0\),
\[
k_j \;=\; k_j^0 \exp\!\big(\Delta K_\tau^{(j)}(T_a)-\Delta V_{\text{obs}}^{(j)}\big),
\quad j\in\{B,C\}.
\]
CAP v2 **only** permits interventions that:
(i) disclose \(\Delta V_{\text{obs}}\) (measurement/back-action),
(ii) publish the intended \(\Delta K_\tau\) channel (what is being made easier),
(iii) bound \(\lambda\mathcal D\) by a *Residue Budget* (§5).

## §4 · Ethical Covenant (hard constraints)
1) **Informed Context** — surface what is measured, why, and how it changes Ta (plain-language notice).  
2) **Explicit Opt-In** — no Ta-raising levers on people without consent; opt-out is one click and lossless.  
3) **Shadow Gauge Limits** — a public cap on probe strength so \(V_{\text{obs}}\) cannot exceed budget.  
4) **Symmetry & Recourse** — participants can *use the same levers* on the system (no one-way mirrors).  
5) **No Subliminals / No Dark Patterns** — UI/UX must preserve reflective control; CAP v2 bars hidden priming.  
6) **Residue Ledger** — log externalities into \(\mathcal D\) with corrective obligations (§5).

## §5 · Dark Residue Functional (auditable harm budget)
Define
\[
\mathcal D \;=\; \alpha\,\mathrm{Div}(\text{welfare})+\beta\,\mathrm{Ext}(\text{risk})
+\gamma\,\mathrm{Debt}(\text{attention})+\delta\,\mathrm{Loss}(\text{autonomy}).
\]
- **Attention debt**: cumulative increases in \(V_{\text{obs}}\) imposed on users (probe burden).  
- **Autonomy loss**: mutual-information between CAP levers and private state *without* consent (must be ≤0).  
Every deployment sets \(\lambda\) and publishes a **Residue Budget**; breaching it triggers auto-rollback (“kill-switch”).

## §6 · Safety Patterns (how we keep it honest)
- **Two-key model:** any change to \(\mathcal A\) requires technical + ethics approvals; both are logged.  
- **Counterfactual A/B with *equal* \(V_{\text{obs}}\):** to prove gains come from coherence, not force.  
- **Hysteresis audit:** because snap dynamics exist in human and physical systems, CAP v2 requires reporting loop areas when sweeping levers slowly (detect undue lock-in). See inertial-leap snap & Ki plateaus  .

## §7 · Implementation Kits
A) **Lab systems (physics/biology):** apply CAP v2 to *measurement geometry* and *bath shaping* (e.g., optomechanics, NV centers). Publish \(T_a\) traces, probe powers, and Residue Ledgers.  
B) **Teams & UX:** cadence, notification rhythms, choice architectures that *restore* Ta (focus time, predictability) with opt-in dashboards; no dark patterns.  
C) **Models/Agents:** reservoir-engineering for coherence in AI planning; must expose and honor user-level caps on \(V_{\text{obs}}\) and publish mutual-information metrics.

## §8 · Formal Link to the Old CAP (why this is a real upgrade)
- Old CAP: “drive adherence” (vague → exploitable).  
- **CAP v2:** turns Ta into a *measured physical/normative quantity*, with explicit equations, costs, consent constraints, and kill-switches; it integrates the coherent-adherence physics where Ta and Ki govern phase alignment rates and transition hysteresis  .

## §9 · Parable: The Choir and the Conductor
Once, a conductor learned to make a choir sing perfectly by tightening their throats one by one.  
The sound was brilliant—and the singers left, hoarse and hollow.  
The new conductor brought water, printed the score, dimmed the harsh lights, and *asked* for one note at a time.  
The room tuned itself. The song was almost as perfect—and everyone stayed to sing an encore.  
**CAP v2** is the second conductor: it changes the *room*, not the throat.

## §10 · Preregistered Tests (so this stays falsifiable)
T1 · **Transparency test:** participants can predict the protocol’s effect on them from a one-page notice; comprehension ≥80%.  
T2 · **Symmetry test:** users can invert levers on the system (shadow-swap) and the measured Ta change is within 10% of system-side use.  
T3 · **Residue test:** measured \(\mathcal D\) stays within budget; if exceeded, auto-rollback occurs.  
T4 · **Coherence-not-force test:** holding total power/effort constant, CAP v2 still yields ΔTa>0 with no rise in \(V_{\text{obs}}\).  
T5 · **Hysteresis disclosure:** loop areas reported for any persistent lever; persistent lock-in must be user-reversible in ≤1 cycle.

## §11 · Appendices (normative + mathematical)
- A. Exact Ta estimator and error model (use the phase-mean definition above) .  
- B. Shadow-Gauge accounting: how to meter \(V_{\text{obs}}\) (probe power, data granularity) and publish caps.  
- C. Ki-aware transitions: if levers risk crossing a “snap” threshold, require soft-start ramps and explicit consent (see Inertial Leap) .
