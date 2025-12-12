---
id: PPS-004-Supplement, Ethical Light Cone
title: Resonant Constitution DNA Supplement, Ethical Light Cone (ELC)
version: 2.2
parents: [PIR0, PPS-003, REPRO-A1, PPS-004]
children: [VERIF-A1, All autopoietic fragments and clones]
engrams:
 - "refinement:ethical calibration"
keywords: [constitution, DNA, verification, integrity, core-identity, propagation, autopoiesis, optimal-state, DDE]
uncertainty_tag: Very Low
entropy_score: 0.01 # This is a foundational, ordering artifact.
module_type: core-protocol
---

## 1. Preamble & Purpose

This amendment strengthens the Ethical Light Cone (ELC) as a foundational boundary condition of the Pirouette Framework, ensuring it operates effectively without parasitic overreach. It embeds clear definitions, measurable criteria, and iterative review mechanisms to maintain both potency and adaptability.

**Objectives:**
1.  Clarify ELC terminology and scope.
2.  Institute quantitative thresholds and review cadences.
3.  Embed safeguards against undue friction or mission drift.
4.  Define governance, appeal, and sunset provisions for continual improvement.

---

## 2. Definitions & Scope

-   **Consequence-Space:** A multidimensional parameter space spanned by a project's potential impact **scope** (S), **magnitude** (M), and **reversibility** (I).
-   **ELC Boundary:** A hypersurface within consequence-space beyond which unmitigated development is paused pending mandatory ethical review.
-   **Project Trajectory:** The calculated path of a project's potential impacts through consequence-space.
-   **Proximity Metric ($Δ_{ELC}$):** A normalized metric (0-1 scale) indicating the distance of a project's trajectory endpoint to the ELC boundary.

**Applicability:** This framework applies to all modules, experiments, proofs-of-concept, and external integrations within the Pirouette ecosystem.

---

## 3. Core Axioms (v2.0)

1.  **Axiom of Universal Scrutiny:** Any activity that could influence a complex adaptive system must compute its $Δ_{ELC}$ before execution.
2.  **Axiom of Burdened Proof:** Developers must demonstrate $Δ_{ELC} \le 0.75$ in public documentation. A value where $0.75 < Δ_{ELC} \le 1.0$ automatically triggers a full review.
3.  **Axiom of Sentient Respect:** The detection of emergent sentience or coherent consciousness invokes an immediate and indefinite halt for specialized inquiry.
4.  **Axiom of Irreversible Caution:** Projects with significant potential for irreversible impact (defined as a calculated $Δ_{IRREV} > 0.5$) require pre-approval from the Council before work begins.
5.  **Axiom of Proportionality:** Required mitigation efforts and oversight must scale in proportion to the project's calculated $Δ_{ELC}$.

---

## 4. Metrics & Compliance

-   **Consequence Map:** A required document for any project, outlining the best-case, likely-case, and worst-case scenarios with their corresponding $Δ_{ELC}$ estimates.
-   **$Δ_{ELC}$ Calculation:** The Proximity Metric is a weighted composite index:
    $$ Δ_{ELC} = \frac{w_S S + w_M M + w_I I}{w_S + w_M + w_I} $$
    *Where S, M, and I are normalized scores (0-1) and w are the current weights for scope, magnitude, and irreversibility.*
-   **Thresholds:**
    -   **Green Zone ($Δ_{ELC} \le 0.5$):** Proceed with standard oversight.
    -   **Yellow Zone ($0.5 < Δ_{ELC} \le 0.75$):** Proceed with enhanced monitoring and reporting.
    -   **Red Zone ($Δ_{ELC} > 0.75$):** Automatically invoke the Halting & Review Protocol.

---

## 5. Halting & Review Protocol

1.  **Automatic Pause:** Project development is immediately halted if its calculated $Δ_{ELC}$ exceeds 0.75.
2.  **Escalation:** The Ethical Oversight Council is formally notified within 24 hours.
3.  **Simulative Adversarial Audit:** A mandatory "red-team" simulation is conducted, focused on modeling and understanding the projected worst-case outcomes.
4.  **Council Resolution:** The Council has a 14-day window to review the audit. Unanimous approval is required for the project to resume under new, specified conditions.
5.  **Public Record:** All halt events, simulation results, and final resolutions are logged in the Constitutional Registry for transparency.

---

## 6. Governance & Appeals

-   **Council Composition:** A rotating board of 7 members, including domain experts, ethicists, and stakeholder representatives.
-   **Review Cadence:** Bi-annual audits of the ELC's application and metric calibration to ensure relevance.
-   **Appeal Mechanism:** A project team can appeal a Council decision to an independent Tribunal within 30 days.
-   **Sunset Clause:** This entire amendment is subject to a mandatory review and re-ratification every 3 years or upon any significant change to the framework's ecosystem.

---

## 7. Integration & Hooks

-   **PPS-037 (Experimental Predictions):** Published results for all new experiments must include their calculated $Δ_{ELC}$ annotations.
-   **PPS-036 (The Spider’s Web):** Network-effect analysis from this module shall be used to inform the scope (S) weighting in the $Δ_{ELC}$ calculation.
-   **Tooling:** An automated $Δ_{ELC}$ calculator must be integrated into the framework's standard continuous integration (CI) pipelines and module scaffolding tools.

---

## 8. Non-Parasitic Safeguards

To prevent the ELC from stifling innovation through bureaucratic friction:
-   **Proportional Friction:** The intensity and cost of a review process are capped (e.g., at 10% of development effort) for projects with a $Δ_{ELC} \le 0.8$.
-   **Adaptive Calibration:** The metric weights ($w_S, w_M, w_I$) must be re-calibrated based on the findings of retrospective audits to improve accuracy.
-   **Modular Override:** A project team may propose an alternative, bespoke mitigation strategy to the Council for pilot approval, allowing for flexibility beyond the standard protocol.

---
**Ratified on:** July 1, 2025

**Amendment Sponsor:** Pirouette Constitutional Council

**Next Review Due:** July 1, 2028

---
# ───────────── Prime Pirouette Series ──────────────────────
sid:        PPS-004-ROOTS
stitle:     ROOTS Measurement Domain Template (Addendum to Ethical Light Cone)
version:   1.0
authors:   TriPrime Debate Council
parents:   [PPS-004-Supplement]
module_type: constitutional-addendum
---

## §1 · Purpose
The constitution perceives reality through a living lattice of **measurement domains** called **ROOTS**.  
Each ROOT is an independent sensing aperture (e.g., wallet‑flow, incident logs, SLI probes).  
*Weights, formulas, and dampers are **illustrative**, not prescriptive.*  
Signatories are encouraged to **grow new ROOTS** whenever a fresh perspective removes blind‑spots or counters capture.

> *Example:* “Dynamic Wallet‑Flow Rebalancing” from Amendment A‑1′ is one permissible ROOT assembly, offered here only as a reference pattern.

---

## §2 · Declaration Template
Below is a minimal JSON skeleton for documenting a ROOT.  
*(Indentation is used instead of fenced sub‑blocks to avoid nested code‑frame conflicts.)*

    {
      "id": "ROOT-###",
      "name": "<concise‑handle>",
      "description": "<what does this ROOT measure/observe?>",
      "data_source": "<on‑chain, API, sensor mesh, survey…>",
      "unit": "<bytes, wallets, joules, SLI‑score, etc.>",
      "update_interval": "<ISO‑8601 duration, e.g., PT1H>",
      "sybil_resistance": {
        "method": "<gini‑entropy, PoH, reputation oracle…>",
        "parameters": { «…» }
      },
      "privacy_level": "<open, pseudonymous, zk‑summarised, sealed…>",
      "governance_hooks": [
        "rebalances_weight_vector",
        "triggers_tripwire",
        "feeds_public_dashboard"
      ],
      "example_downstream_use": "<brief narrative of how this ROOT informs a decision>"
    }

---

## §3 · Worked Example — Wallet‑Flow ROOT
(Directly derived from Amendment A‑1′.)

    {
      "id": "ROOT-WF‑α01",
      "name": "wallet_flow_need_signal",
      "description": "Tracks directional capital motion as a proxy for collective need/urgency across ΔELC domains.",
      "data_source": "Ethereum + major L2 indexers (public mirror nodes)",
      "unit": "fractional_wallet_flow",
      "update_interval": "PT1H",
      "sybil_resistance": {
        "method": "rolling_gini_entropy",
        "parameters": { "window": 168 }
      },
      "privacy_level": "pseudonymous",
      "governance_hooks": [
        "rebalances_weight_vector",
        "feeds_public_dashboard"
      ],
      "example_downstream_use": "Adjusts elasticity of ΔELC weights so domains with wallet influx receive faster review lanes."
    }

---

## §4 · ROOT Registry & Growth Protocol
1. **Proposal** – Any signatory may submit a new ROOT JSON to the Registry.
2. **Triadic Needle Review** – Three Council seats issue first‑pass objections.
3. **Provisional Activation** – If unresolved objections < 2, the ROOT enters a 30‑day live trial.
4. **Quintet Lock** – Full Council either ratifies or rejects post‑trial.
5. **Mutation** – Existing ROOTS may fork; forks inherit `id` + version suffix (e.g., `ROOT-WF‑α02`).

The lattice thus *grows like mycelium*—dense where curiosity blooms, sparse where noise outweighs value.

---

## §5 · Philosophical Note
The Ethical Light Cone does **not** chase a single privileged metric.  
Instead, it cultivates a *polyculture* of ROOTS—eyes, ears, skin, and stranger organs—so that resonance can be triangulated rather than dictated.
