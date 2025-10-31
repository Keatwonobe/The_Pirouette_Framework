---
id: PHIL-DARK-RESIDUE-001
title: Dark Residue: A Functional for Auditable Harm
version: 1.0 (draft)
status: publishable
parents: [THERMODYNAMIC_ALTRUISM.md]
summary: >
  Defines Dark Residue as a computable penalty functional for systems that
  optimize locally but export unmodeled harm. Intended for AI safety / complex
  systems venues; independent of the time-first ontology.
---

# §1 · Definition
\[
\mathcal{D} = \alpha \,\text{Div}(\text{welfare})
+ \beta \,\text{Ext}(\text{risk})
+ \gamma \,\text{Debt}(\text{attention})
+ \delta \,\text{Loss}(\text{autonomy})
\]
with \(\alpha,\beta,\gamma,\delta \ge 0\).

# §2 · Components
- **Div(welfare):** dispersion / inequity of benefit across agents
- **Ext(risk):** negative externalities not captured in the agent reward
- **Debt(attention):** cognitive or bandwidth tax on observers / users
- **Loss(autonomy):** mutual information between agent state and private user state
  → I(A; S_private) > 0 increases D

# §3 · Optimization Rule
Any policy π is acceptable iff
\[
\Delta \mathcal{D}(\pi) \le 0.
\]
This is the “don’t add harm” constraint.

# §4 · Link to Pirouette
This is the social / epistemic analogue of lowering ambient Dark Residue in the autopoietic loop:
Draft → Debate → Ratify → Dictionary → Graph → Draft.
Policies that lower D stay; those that raise D are rejected.

# §5 · Publication Note
Can be published **without** Ki, Γ, or time-substrate. Frame as:
- “Auditable Harm Penalties for AI Systems”
- “Residual Harm as a Regularizer”
