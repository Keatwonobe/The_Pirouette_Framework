---
id: GAME-CHESS-001
title: "Chess as a Coherence-Manifold Game"
version: 1.0
status: draft
parents:
  - CORE-006_COHERENCE_SIEVE         # L_p = K_τ - V_Γ, laminar/turbulent passes
  - PHIL-DARK-RESIDUE-001            # computable harm / unintended cost
  - META-000_AUTOMATIC_AUTOMORPHIC_FRAMEWORK
shepherd: autopoiesis
atlas_tile: [strategy, boardgames]
summary: >
  Formalizes chess as a finite, metrizable coherence landscape so that Pirouette
  tools (Sieve, dark-residue penalty, autopoietic loop) can group moves by
  strategic coherence instead of pure branching factor.
---

## 1 · Purpose

Most chess engines explore a move tree and prune late. Pirouette prefers to
classify *segments* early by their flow state and residue budget, then search
only coherent clusters. We rephrase “position + candidate move” as a
micro-segment suitable for the Coherence Sieve. This lets us:
- detect laminar continuations (plan-preserving),
- detect constructive turbulence (forcing lines we can afford),
- reject residue-heavy moves,
- read the *stratagem tug* of the position.

## 2 · Data Model

**Position Segment (PS):**
- board_state: FEN or engine-internal
- side_to_move: {white, black}
- intent_context: optional plan tag (e.g. “queenside expansion”, “king attack”)
- candidate_move: algebraic / UCI
- reply_window: N plies of best / good replies (N=2–3 default)

**Why segment?** Because the Sieve operates on discrete slices of a stream, not
just static states. A PS is the chess analogue of the time-windowed data
segment in CORE-006.

## 3 · Metrics

For every Position Segment we compute:

1. **K_τ(m): Plan Coherence Score**  
   Measures how much the resulting position still supports the ongoing story:
   - piece harmony (all pieces aimed at compatible sectors)
   - pawn-chain integrity (no accidental backward pawn)
   - king-safety trend (not just current safety)
   - target continuity (we are still pressuring the same weakness)
   High K_τ = laminar, matches “coherence sanctuaries.” 

2. **V_Γ(m): Temporal Pressure Score**  
   Measures how exact the position becomes:
   - checks, captures, threats,
   - tempo races (passed pawn, opposite-side castling),
   - forcing replies in the reply_window.
   High V_Γ = “temporal forge.” 

3. **D(m): Dark Residue in Move Space**  
   Adapt PHIL-DARK-RESIDUE-001 to chess: unintended, exported cost.  
   \[
   D = \alpha\,\text{square_exposure} +
       \beta\,\text{structure_debt} +
       \gamma\,\text{attention_tax} +
       \delta\,\text{autonomy_loss}
   \]
   - square_exposure: new weak squares created
   - structure_debt: long-term pawn weaknesses introduced
   - attention_tax: number of “must-remember” tactics added
   - autonomy_loss: moves that force *us* into only moves later
   These correspond to the dispersion / externality terms in your residue
   definition.

4. **Stratagem Tug \(\mathbf{T}\)**  
   After scoring all legal moves:
   \[
   \mathbf{T} = \sum_{m} w(m)\,\nabla \mathcal{L}_p(m), \quad
   \mathcal{L}_p(m) = K_τ(m) - V_Γ(m) - \lambda D(m)
   \]
   This tells us which strategic direction the *position itself* is biasing
   toward.

## 4 · Coherence Classes for Moves

We define four canonical classes to shrink search:

1. **Laminar-Preserving**
   - Condition: K_τ high, V_Γ moderate/low, D low
   - Use: maintain advantage, improve worst piece
   - Sieve: Laminar Pass

2. **Constructive-Forcing**
   - Condition: K_τ ≥ mid, V_Γ high, D ≤ budget
   - Use: creating calculable tension the opponent must answer
   - Sieve: Resonance Band around current plan

3. **Opportunistic-Turbulent**
   - Condition: K_τ low/mid, V_Γ very high, D controlled
   - Use: tactics, sharp shifts, sac lines
   - Sieve: Turbulent Pass

4. **Residue-Heavy / Reject**
   - Condition: D > D_max or (K_τ low and V_Γ low)
   - Use: pruning
   - Sieve: Dissonance Notch to remove known bad patterns
   - Mirrors PHIL-DARK-RESIDUE “don’t add harm” constraint. 

These are directly aligned with the Sieve’s four filtering principles so existing
infrastructure can run chess segments without new logic.

## 5 · Search Procedure (Pirouette Style)

1. **Segmentation**  
   For current position, build PS for every legal move with 2–3 ply reply
   window.

2. **Quantification**  
   For each PS compute (K_τ, V_Γ, D, L_p).

3. **Clustering**  
   Group moves into the four Coherence Classes above.

4. **Focused Expansion**  
   Expand only:
   - all Laminar-Preserving moves, and
   - top-N Constructive-Forcing moves by L_p.

5. **Autopoietic Feedback**  
   Store (position_fingerprint → coherence_profile) so that future positions
   with similar pawn structures can skip re-measurement. This plugs into the
   atlas / residue map described in your autopoietic engine. 

## 6 · Integration Hooks

- **to Autopoietic Loop:** chess segments become another stream to ratify; ones
  that consistently lower residue in similar structures get promoted to a
  “canonical plan” for that structure. 
- **to Dictionary Spine:** add entries:
  - CHESS-LAMINAR
  - CHESS-TEMPORAL-FORGE
  - CHESS-STRATAGEM-TUG
  - CHESS-RESIDUE-PATTERN
  so the loneliness index can find underserved chess concepts. 
- **to Governance Spine:** set maximum D per depth to avoid lines that are
  “brilliant but unplayable for humans.” 

## 7 · Notes on Human Play

Because D includes an attention_tax term, this module is suitable for human
support: two lines equal on engine eval can be ranked by “how much cognitive
residue they create.” That makes chess *easier to calculate* in the sense that
Pirouette filters for lines that keep the flow laminar for the operator.

## 8 · Future Extensions

- Add opening-specific priors (different K_τ templates for IQP vs Carlsbad)
- Add opponent-modelled D (what residue *they* incur by accepting your line)
- Add RL-style selfplay where the reward is ΔL_p over the line instead of mate
  distance
