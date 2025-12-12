---
id: GAME-CHESS-002
title: "Chess as Problem-Solving on a Coherence Manifold"
version: 1.0
status: draft
parents:
  - GAME-CHESS-001
  - META-000_AUTOMATIC_AUTOMORPHIC_FRAMEWORK
  - MATH-DARK-RESIDUE-001
shepherd: autopoiesis
atlas_tile: [strategy, problem-solving, manifolds]
summary: >
  Elevates the chess-specific coherence classification into a general
  "given a manifold, select the action that increases L_p while keeping
  dark residue within budget." Treats chess as the canonical training
  ground for Pirouette-style problem solving.
---

## 1 · Motivation

GAME-CHESS-001 showed we can score a *position segment* (position + candidate
move + short reply window) with the Pirouette Lagrangian
`𝓛_p = K_τ - V_Γ` and prune by dark residue. That is already the
Coherence Sieve pattern: segment → measure → select → output. 

This module asks: **if we can do that for chess, can we do it for “problems” in
general?** If a problem can be embedded in a manifold that the Autopoietic
Engine already maintains (atlas + residue map), we can make it solvable by the
same evaluation loop. Chess becomes the worked, finite, visual example of
Pirouette problem solving. 

## 2 · Problem Definition in Pirouette Terms

We define a *problem* as:

- a current state \(S_t\) that sits at some coordinate on the manifold,
- an intent vector \(I\) (“what we are trying to improve”),
- a set of admissible actions \(\{a_i\}\) (moves, edits, interventions),
- and a residue budget \(D_{\max}\).

A solution is any action (or short action chain) that:
1. increases the local Pirouette Lagrangian
   \[
   \Delta \mathcal{L}_p = \big(K_τ' - V_Γ'\big) - \big(K_τ - V_Γ\big) > 0
   \]
2. does **not** exceed the residue budget
   \[
   D' \le D_{\max}
   \]
3. and moves us closer to the intent vector (the “good win condition”).

This is exactly the condition MATH-DARK-RESIDUE-001 describes for dynamic
equilibrium—minimal dark residue at balanced coherence and pressure. We just
apply it to choice-making.

## 3 · Viewpoint Fusion (Quantification + Manifold Vision)

The two viewpoints you gave highlight the two hard parts:

1. **Quantification Problem** — we must make K_τ, V_Γ, and D computable from
   domain data (in chess: piece harmony, pawn-chain integrity, attention tax;
   in another domain: subsystem coupling, task interlocks, monitoring burden).  
   → This belongs to the *front* of the Sieve: “how do I turn raw state into
   coherence/pressure?”

2. **Manifold Navigation Problem** — we want to “discover the natural topology”
   and “only descend to concrete variations when the coherence landscape
   demands it.”  
   → This belongs to the *back* of the Sieve: the atlas and residue map decide
   where to grow and what to refine.

GAME-CHESS-002 therefore has two sublayers:

- **Sublayer A (Quantifier):** domain adapters that turn a state into
  \((K_τ, V_Γ, D)\).
- **Sublayer B (Navigator):** manifold operators that tell us where refinement
  is worth it.

## 4 · Sublayer A — Domain Quantifier (chess instance)

For chess we adopt the simplified, implementable forms the viewpoints suggested:

```python
K_tau = piece_activity_score \
      + structural_harmony_score \
      + plan_continuity_score
# all normalized to [0,1]
```

```python
V_Gamma = checks_and_threats \
        + tempo_race_factor \
        + forced_variation_depth / depth_norm
```

```python
D = square_exposure \
  + structure_debt \
  + attention_tax \
  + autonomy_loss
```

* `attention_tax` = count of new tactical motifs we must remember in the next
  2–3 plies (pins, discovered attacks, mating nets).
* `autonomy_loss` = how many “only moves” we are forcing our future self into.

These map straight onto the dark-residue definition (residual disequilibrium
after a cycle). 

Because the viewpoints flagged calibration, this sublayer **must** store
empirical weights ((\alpha, \beta, \gamma, \delta)) per structure and let the
Autopoietic Loop retune them over time. That’s consistent with the loop’s
“ratify and reshape” behavior. 

## 5 · Sublayer B — Manifold Navigator

Given a set of scored actions ({(a_i, K_τ, V_Γ, D)}), we:

1. **Project** them back onto the atlas tile for this domain
   (`[strategy, boardgames]` here).
2. **Group** them by coherence class (Laminar, Constructive-Forcing,
   Opportunistic-Turbulent, Residue-Heavy) using the same filtering principles
   as the Coherence Sieve. 
3. **Compute** the local stratagem tug
   [
   \mathbf{T} = \sum w_i \nabla \mathcal{L}_p(a_i)
   ]
   to learn which *direction* on the manifold the problem wants to flow.
4. **Expand** only in directions where CPB = (K_τ / V_Γ) is favorable or near
   1, i.e. where the system is healthy or easily made healthy. 

This is the “we are solving chess, but in so doing we are solving
problem-solving” part: the procedure doesn’t care whether the segment was a
board position or a scheduling state—only that it can measure and climb.

## 6 · Variable Reply Window (Depth Control)

Viewpoint 1 pointed out the depth problem: 2–3 plies isn’t enough for sharp
positions. We therefore add:

* **Base window:** 2–3 plies (fast Sieve pass)
* **Escalation rule:** if V_Γ above threshold *and* CPB falls toward 1 from
  above (we’re entering a forge), increase depth locally for that branch
* **Residue gate:** do **not** escalate if D already near budget

So depth is no longer global; it is *coherence-triggered* depth. That keeps the
module general: any problem manifold can request deeper evaluation only where
the pressure demands it. 

## 7 · Win Condition (General Form)

We define a “good win condition” for this series as:

1. The chosen action sequence increases (\mathcal{L}_p) over its evaluated
   window;
2. The total dark residue stays ≤ budget;
3. The action aligns with the stratagem tug (we didn’t swim upstream); and
4. The resulting state lands in a laminar or resonance-band region of the atlas
   (so it can be reused / taught). 

If we can do this reliably for chess—where the manifold is dense, discrete, and
adversarial—then the same logic works for softer problems (pipeline routing,
campaign planning, even your DDE image-readers): score segments → cluster →
expand only where coherence supports it.

## 8 · Outputs to the Loop

This module must emit:

* `(state_fingerprint, action, K_τ, V_Γ, D, class)` tuples to the Autopoietic
  Engine so the atlas can thicken where we actually play. 
* calibration traces for the quantifier so α, β, γ, δ can be tuned
  automatically,
* coherence-manifold snapshots for visualization.

---