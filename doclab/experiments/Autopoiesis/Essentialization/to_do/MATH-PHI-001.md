---
id: MATH-PHI-001
title: Math as Stabilizer Grammar — Stickiness, Reverse Pareto, and the Pirouette Test
version: 1.0
status: canon-target
parents: [SUBST-001, DYNA-004]
children: [MATH-YM-001, MATH-GR-001, INFO-COH-001]
module_type: philosophy / methodology
scale: meta
---

# §0 · Thesis

Mathematics is **invented syntax** exploring many possible grammars.  
**Pirouette** selects the fragments whose invariants *stabilize* the temporal medium: these fragments behave like a **stabilizer grammar** for SR-0…6.  
We call this selective adhesion **stickiness**. It is *not* a theological claim that “all math exists”; it’s a **diagnostic** for which invented formalisms become **physically load-bearing**.

> Slogan: *“Most math is a net. The sticky math is the mesh that the loom itself uses.”*

---

# §1 · Stickiness: a measurable property

Let a math domain \( \mathcal{D} \) be a set of objects, morphisms, and rules.  
We define **stickiness** \( \mathrm{Stk}(\mathcal{D}) \) as an operational score composed of four observables:

1. **Σ-Compatibility (S):** Does \( \mathcal{D} \) commute with the **spatialization map** Σ from DYNA-004 (time → effective fields/geometry)? Binary + partial credit.
2. **Stabilizer Yield (Y):** How many **conserved quantities / symmetries / gauge structures** in SUBST-001 are *natively* expressible in \( \mathcal{D} \) with *low description length*?
3. **Compression Power (C):** By how much does \( \mathcal{D} \) **reduce the Kolmogorov/MDL cost** of our best derivations (GR hydrolimit, YM emergence, barrier finiteness)?
4. **Predictive Leverage (P):** How many **new, falsifiable relations** (bounds, scaling, spectral features) does \( \mathcal{D} \) produce when grafted into active XXP tests?

We normalize each to \([0,1]\) and define
\[
\mathrm{Stk}(\mathcal{D}) = w_S S + w_Y Y + w_C C + w_P P, \quad \sum w_i = 1.
\]
House default: \( w_S=0.25, w_Y=0.25, w_C=0.25, w_P=0.25 \).

**Interpretation.** Invented formalisms with high \(\mathrm{Stk}\) are those our substrate can *actually use*.

---

# §2 · The Pirouette-Compliance Test (PCT)

A domain is **Pirouette** iff it passes all three gates:

- **PCT-1 (SR Gate):** There exists an embedding of \( \mathcal{D} \) whose invariants are stable under **SR-0…6** *and* preserve CPM (no forbidden polarizations, no IR Lorentz violation).
- **PCT-2 (Σ Gate):** Under Σ pushforward, the images of \( \mathcal{D} \) support **U(1)/SU(2)/SU(3)** frame relabelings or the GR constitutive law **without** inflating the constant ledger (no ad-hoc knobs).
- **PCT-3 (Falsifiability Gate):** The graft produces at least one **testable** prediction at \(\mathcal{O}((\omega/\omega_c)^2)\) or better, with a clear kill-switch condition.

If **any** gate fails ⇒ domain is “non-pirouette” (still useful for thought, not load-bearing here).

---

# §3 · Reverse Pareto Analysis (RPA) for **completeness**

**Goal.** Detect when our current stabilizer grammar is *complete enough* for a target phenomenon by quantifying **few→many leverage**.

We form a bipartite graph \(G=(\mathsf{Axioms} \leftrightarrow \mathsf{Consequences})\) at the module level (SUBST-001, MATH-GR-001, MATH-YM-001, …).

Define:
- \(k\): number of axioms actually invoked in a derivation set,
- \(M(k)\): number of distinct, empirically checkable consequences supported by those \(k\) axioms,
- \(L(k)\): description length (MDL) of all proofs using those \(k\) axioms.

**RPA score** for a domain graft \( \mathcal{D} \):
\[
\mathrm{RPA}(\mathcal{D}) \equiv \max_{k}\; \frac{M(k)}{L(k)}\quad \text{s.t.}\quad \text{PCT holds and constants remain read-only.}
\]

**Completeness indicator (project level):**
\[
\mathcal{C}_\mathrm{proj} = \frac{\sum_{\text{targets}} \mathbf{1}\{\mathrm{RPA} \ge \tau\}}{\#\text{targets}},
\]
with default threshold \( \tau \) set by the median of historical “wins” (e.g., when GR+YM derivations achieved new XXP hits).

**Reading it.** When \(\mathcal{C}_\mathrm{proj}\to 1\), we’re close to *functional completeness* for our present scope; adding more math yields diminishing returns unless it opens *new* falsifiables.

---

# §4 · Autopoiesis of Mathematics (why sticky math emerges)

Your lens: *“math is invented; the sticky pieces feed back with the geometry that uses them.”* We model this with an **autopoietic learning dynamic**:

Let \( \pi_t(\mathcal{D}) \) be the weight our program assigns to domain \( \mathcal{D} \) after round \(t\). Update rule:
\[
\pi_{t+1}(\mathcal{D}) \propto \pi_t(\mathcal{D})\;\exp\big(\lambda_1\,\mathrm{Stk}(\mathcal{D}) + \lambda_2\,\mathrm{RPA}(\mathcal{D}) - \lambda_3\,\Delta\mathrm{MDL}(\mathcal{D})\big),
\]
with temperature set so exploration never vanishes.  
Interpretation: **marketing of the mind**—attention hovers on structures with resonance; those structures, once in use, *reduce* future description length and therefore attract *more* attention. That’s stickiness formalized.

---

# §5 · Where to fish: the **Junkyard & Goldmine** map

We bucket candidate domains by (expected) Stickiness × RPA. (“Goldmine” = high-high; “Junkyard” = low-low *for us*, not a value judgement.)

### GOLDMINE (high Stk, high RPA)
- **Representation theory & tensor categories (fusion, modular, braided):** tight with SU(2)/SU(3) holonomies; likely boosts Σ-compatibility and quantization clarity.
- **Symplectic & contact geometry; microlocal analysis:** natural with phase/characteristic sets; promises sharper GW/Γ phase control and scattering maps.
- **Geometric measure theory / varifolds:** minimal-surface style tools for **least-residue** flows; fits SR-6 closure.
- **Operator algebras & von Neumann factors (Type III):** good candidates for coarse-grained time flows and barrier-tamed renormalization.

### RISING (medium Stk, high potential RPA if bridged)
- **Non-commutative geometry (Connes-style):** could re-encode Bridge constants as spectral data; Σ-compatibility is the open gate.
- **Geometric Langlands / higher gauge:** may unify YM emergence proofs; needs a careful PCT-2 pass (knob discipline).

### UTILITY BELT (high Stk, modest RPA)
- **Tropical geometry / polyhedral combinatorics:** powerful for MDL-light existence proofs and asymptotics (great in the pipeline, limited ontic bite).
- **Optimal transport / information geometry:** near-perfect for AMDP and Minimum Dark Residue variational forms; strong compression, few new falsifiables.

### JUNKYARD (low Stk, low RPA *for this universe right now*)
- **p-adic analysis / ultrametric geometry** (without a spectral bridge): elegant but fails Σ-gate presently; can be a sandbox for speculative cosmology modules.
- **Exotic smooth structures on \( \mathbb{R}^4 \)** (as primary ontology): beautiful, but PCT-1/2 typically fail unless kept as calculational scaffolds.

---

# §6 · Protocol: turning this into code & CI

1) **Domain card.** For each candidate \( \mathcal{D} \), author a one-page *card* with: Σ-Compat proof sketch, stabilizer list, compression deltas, and at least one proposed falsifiable.
2) **Benchmarks.** Re-derive: (i) GR hydrolimit, (ii) YM frame relabeling, (iii) GW dispersion bound with/without \( \mathcal{D} \). Record MDL change and new tests.
3) **Compute \(\mathrm{Stk}, \mathrm{RPA}\).** Log to `/analysis/math_adhesion/ledger.csv`.
4) **CI gate.** Any domain with \( \mathrm{Stk} \ge 0.6 \) and \( \mathrm{RPA} \ge \tau \) is **promoted** to “pirouette” and may modify children modules; else remains a helper.

---

# §7 · Acceptance Criteria

- **AC-1**: PCT passes for any domain marked “pirouette”.  
- **AC-2**: Stickiness components (S,Y,C,P) are computed from explicit proofs/derivations, not vibes.  
- **AC-3**: RPA threshold \( \tau \) is anchored to historical wins and listed in the ledger.  
- **AC-4**: Any elevated domain yields at least one **XXP** falsifiable bound, wired to tests.

---

# §8 · Assemblé

> We invent nets. The loom keeps only what catches its threads with less and less mesh. The rest we hang on the wall—beautiful, instructive, and waiting for another ocean.

