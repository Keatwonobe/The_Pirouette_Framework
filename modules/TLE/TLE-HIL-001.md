---
id: TLE-HIL-001
title: Elemental Comparative Axes & Opposite Houses
version: 0.1
parents: ['TLE-000', 'TLE-001', 'MATH-HIL-001']
children: ['TLE-HIL-002']
uncertainty_tag: medium
purpose: >
  Give TLE a concrete way to host Pirouette’s Hilbert space so that opposed
  elements (ice/fire, rot/life, void/light) can live on the same comparative
  axis, with bounded chirality and a rule for “opposite house”.
engrams:
  - mechanic:comparative-axis
  - mechanic:bounded-chiral-winding
  - concept:opposite-house
  - bridge:pirouette-hilbert
  - system:elemental-classification
---

## §1 · Preamble: TLE on a Hilbert Spine
TLE already treats magic as EP-backed expressions of will and allows multi-element
interactions in the same 5-foot square. That implies a common coordinate system
for “fire here, frost there, steam in the middle.” We now declare that coordinate
system to be the same Hilbert space defined in `MATH-HIL-001`, but specialized
to TLE’s elemental runes. :contentReference[oaicite:1]{index=1}

We do **not** create a new magic subsystem — we just say: “every elemental or
arcane skill in TLE is a vector in 𝓗, and some of them are locked as comparative
pairs.”

---

## §2 · Comparative Axes (Fire–Ice Pattern)
1. A **Comparative Axis** is a 1D closed subspace of 𝓗 spanned by a single
   elemental conceptual basis vector `E_elem`.
2. Opposed expressions live at opposite coordinates on the same line:
   - Fire  ≡ +E_fire
   - Ice   ≡ −E_fire
   They are **not** two unrelated axes; they are one axis with opposite winding.
3. Magnitude on the axis is the **EP investment** from TLE-000/001:
   - ||Fire|| = EP_fire
   - ||Ice||  = EP_ice
   and those map directly to the norm in 𝓗.
4. Because they share a line, cross-effects (steam, thermal shock, quench) are
   just inner products and rejections on that line instead of ad-hoc tables.

**Rule (table-free interaction):**
Given two instantaneous effects a, b on the same comparative axis,
the **differential effect** is
Δ = a + b
If sign(a) ≠ sign(b), magnitude reduces (snuffing / quenching).
If sign(a) = sign(b), magnitude sums (reinforcement).

---

## §3 · Bounded Chiral Winding
You wanted: “opposite (antimatter-like) winding but **not** unbounded time
chirality that explodes into fractal energy.”

Define for any comparative axis A a chiral phase θ ∈ [0, 2π):

- θ = 0        → canonical element (e.g. fire)
- θ = π        → opposite element (e.g. ice)
- θ = π/2,3π/2 → transitional / synthesis states (steam, brittle flash-freeze)

**Bounded winding rule:**
- A spell/effect may rotate its θ at most Δθ_max per round (GM default: π/2).
- If a rotation would exceed Δθ_max, excess rotation is shaved off and converted
  to environmental residue (TLE-004’s entropic corruption) so we don’t get
  free fractal escalation. :contentReference[oaicite:2]{index=2}
- Formally: θ_{t+1} = θ_t + clamp(Δθ_req, −Δθ_max, +Δθ_max)

This keeps your “opposite winding” aesthetic while staying gameable.

---

## §4 · Opposite House Calculation
Sometimes you want to say “what’s directly across from this concept or school?”

Let an elemental / arcane style be represented by a unit vector u ∈ 𝓗 on its
comparative axis. Then:

- opposite_house(u) = −u

If you are working in the angle form:
- given θ, opposite house is θ_op = (θ + π) mod 2π

**TLE use:**
- If two casters act in the same square in the same round, and their angles
  differ by ≤ π/4 of the opposite-house angle, trigger the “violent synthesis”
  clause from TLE-001 §2 Elemental Synergy (steam, obsidian, smothered). :contentReference[oaicite:3]{index=3}

---

## §5 · Axis Spin-Up & Classification
You said: “I want to spin up an axis and have it, on becoming a certain axis,
be related to other axes in a way that classifies it.”

Here’s the rule:

1. **Axis Declaration**
   - When a GM or module defines a new elemental expression (e.g. “Ash Breath”),
     they declare a root vector r and a tag set {heat, particulates, decay}.
2. **Nearest-Neighbour Binding**
   - Project r onto all existing comparative axes {A_i}.
   - Bind r to the axis with the **largest absolute projection**.
     A_bind = argmax_i |⟨r, A_i⟩|
   - r now lives on A_bind as a chiral variant with its own θ.
3. **Contextual Emergence**
   - For every other axis A_j, compute a context weight
     w_j = |⟨r, A_j⟩| / ||r||
     and store only those w_j ≥ 0.2 (tunable).
   - Those weights are what let the spell “become clever” in context: ash bound
     to fire (main), but with 0.25 to earth → it hardens when hit by frost.
4. **System Configuration**
   - The initial list of axes (fire, frost, earth, air, life, rot, void, light)
     is the “system configuration.”
   - New axes must publish their projections against this list so auto-class
     works later.

This gives you emergent complexity without you hand-authoring pairwise tables.

---

## §6 · TLE-002 Expansion Hook (Control / Necro / Conversation)
Because TLE-002 does “contested will” and even curse-style entropy reallocation,
we let it ask “what is this target’s opposite house?” for mental / moral axes.

Add to TLE-002:

- When applying a curse, you may target the **opposite house** of the victim’s
  current elemental / moral axis. Cost: +2 EP, but the curse gains advantage on
  its TLE-002 contested roll because you’re hitting the vector-space opposite.
- Mind-control effects that align the target to your axis set θ_target = θ_caster;
  mind-break effects can set θ_target = θ_caster + π for inversion.

This way social/mental control uses the same math as fire/ice. :contentReference[oaicite:4]{index=4}

---

## §7 · Falsifiability
- **Projection sanity:** for N defined axes, a new spell must produce at least
  one projection ≥ 0.4, or it’s too orthogonal → reject or map it to VOID.
- **Opposite-house clarity:** if |θ₁ − θ₂| ∈ [3π/4, 5π/4], treat them as opposite
  house for TLE-001 synergy.
- **Chiral bound:** if a sequence of spells would rotate θ more than 2π in 1
  scene, accrue 1 level of environmental corruption per extra π. This proves
  the “no unbounded fractal release” property. :contentReference[oaicite:5]{index=5}
