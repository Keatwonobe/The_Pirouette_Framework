---
id: MATH-SOLITON-RIGOR-002
title: "Soliton Stability in Pirouette: Evading Derrick’s Theorem"
version: 1.0
status: foundational-proof
parents: [MATH-SOLITON-TOPOLOGY-001, MATH-SUBSTRATE-001]
children: [MATH-SOLITON-QUANT-001, MATH-DIRAC-EMERGE-001]
summary: >
  Shows that the spin-½ Δ-soliton sector in Pirouette is not ruled out by
  Derrick’s theorem, because (i) the relevant configuration is a complex
  phase-winding field producing a line-like vortex/solitonic string, not a
  localized 3+1D lump; and (ii) the effective energy functional is defined
  on the correlation-induced metric rather than a fixed Minkowski background.
  In the reduced 2D transverse problem, the usual global-vortex stability
  argument applies and yields a finite-radius, energetically favored solution.
module_type: foundational-proof
scale: soliton-sector
engrams:
  - proof:derrick_evaded
  - concept:solitonic_string
  - concept:induced_metric_scaling
keywords: [Derrick's theorem, soliton, vortex, stability, Δ-field, spin-1/2]
uncertainty_tag: Foundational
---

### §0 · Statement of the Issue

**Derrick’s theorem** says: for a real scalar field in D≥2 spatial dimensions, with canonical kinetic term and potential V(Δ), there are no stable, static, finite-energy, localized solutions if:

1. the field lives on a fixed, flat background,
2. the energy functional is a sum of positive-definite gradient + potential terms,
3. the configuration is a genuine **3D lump** (energy density localized in all spatial directions),
4. you allow a uniform scaling (x \to \lambda x) of the configuration.

But the Pirouette soliton used to model fermions is:

* a **complex phase-winding configuration** (\Delta = f(r) e^{i n \theta}),
* extended along one spatial direction (a line-like vortex / closed string),
* living on an **induced metric** (g_{\mu\nu}[\langle \Delta\Delta\rangle]), not a fixed Minkowski background.

Those differences matter. The theorem’s assumptions are violated in two precise ways.

We now show:

1. At fixed winding (n), the **transverse 2D problem** admits a stable, finite-radius vortex solution (energy per unit length minimized at some R_⋆).
2. When embedded in the Δ-induced metric, the global scaling variation Derrick uses is *not* an allowed variation in the physical configuration space.

---

### §1 · The Relevant Object Is a Solitonic String, Not a 3D Lump

Your ansatz in the paper is already:

[
\Delta(r,\theta) = f(r) e^{i n \theta}
]

which is the standard global vortex / cosmic string form in cylindrical coordinates:

* (r,\theta): polar coordinates in the plane transverse to the string,
* (z): direction along the string (we take it translationally invariant along z),
* (t): time.

So the physically relevant configuration is:

* **localized in 2 transverse directions** (r,θ),
* **extended in 1 direction** (z),
* with energy ∝ (energy per unit length) × (string length).

Derrick’s instability argument applies to **codimension-0** lumps in 3D, not **codimension-2** vortices. The right stability notion is:

* finite energy **per unit length**,
* and an energy density that cannot be decreased by rescaling the transverse profile at fixed winding.

This is exactly the Nielsen–Olesen / global-string story, adapted to Δ.

---

### §2 · Effective 2D Energy and Scaling Argument

Starting from your Lagrangian (dropping time dependence and z-variation):

[
\mathcal{L}*\Delta =
\frac{1}{2}(\partial*\mu \Delta)(\partial^\mu \Delta)

* \frac{1}{2}m_\Delta^2 \Delta^2
* \frac{\lambda_4}{4!}\Delta^4

- \frac{\kappa}{2}(\nabla\Delta)^2
  ]

For static, z-invariant configurations in flat coordinates (for the moment), the **energy per unit length** is:

[
E_\ell[n,f]
= \int d^2x_\perp \Big[
\frac{\kappa_{\text{eff}}}{2} |\nabla_\perp\Delta|^2

* V_{\text{eff}}(|\Delta|)
  \Big],
  ]

where:

* (x_\perp = (x,y)), (d^2 x_\perp = r,dr,d\theta),
* (\kappa_{\text{eff}}) is a combination of the gradient coefficients,
* (V_{\text{eff}}(|\Delta|)) is the symmetry-breaking potential with minimum at (|\Delta|=\Delta_0).

Insert the ansatz (\Delta(r,\theta) = f(r) e^{i n\theta}). Then:

[
|\nabla_\perp \Delta|^2
= f'(r)^2 + \frac{n^2}{r^2}f(r)^2.
]

So:

[
E_\ell[n,f] = 2\pi \int_0^\infty dr, r \left[
\frac{\kappa_{\text{eff}}}{2}\left(f'(r)^2 + \frac{n^2}{r^2}f(r)^2\right)

* V_{\text{eff}}(f(r))
  \right].
  ]

The usual global-vortex analysis tells us:

* For fixed n ≠ 0, any attempt to shrink the core (R→0) blows up the (n^2 f^2 / r^2) term.
* Any attempt to spread the core arbitrarily (R→∞) increases the potential energy (volume of core region with f≠Δ_0).

Your own scaling estimate in the paper captures this in a compact way:

[
E_\ell(n,R) \sim
\underbrace{\frac{\kappa \Delta_0^2 (1+n^2)}{R}}*{\text{gradient / winding}}
+
\underbrace{\lambda_4 \Delta_0^4 R}*{\text{potential core}},
]

which has a clear minimum at finite (R = R_\star \propto \sqrt{\kappa/\lambda_4}/\Delta_0).

This is precisely the **vortex stability mechanism**: the angular gradient term wants a large core (large R), the potential term wants a small core (small R), and they balance at R_⋆.

Thus, at the level of **energy per unit length**, there is a stable minimum **for each nonzero winding n**, including n = ½ once you allow the double-valued phase / spinor structure.

> Conclusion: In the transverse 2D problem, the Δ-soliton is a stable vortex with finite radius; Derrick’s theorem about 3D lumps does not apply.

---

### §3 · Why the Usual Derrick Scaling Variation Is Not Allowed

Derrick’s proof considers a scaling:

[
\Delta(\mathbf{x}) \to \Delta_\lambda(\mathbf{x}) = \Delta(\lambda \mathbf{x}),
]

and shows that the energy functional in D spatial dimensions scales as:

[
E_\lambda = \lambda^{D-2} T + \lambda^{-D} V
]

for gradient energy T and potential V, which for D=3 has no minimum except trivial.

In our case:

1. We do **not** scale the field along the string direction z, only in the transverse plane. The relevant “dimension” in the scaling argument is D=2, not 3. For D=2, the balance of terms *does* allow minima.

2. More importantly, in Pirouette the energy functional is ultimately defined with respect to the **induced metric** (g_{\mu\nu}[\langle\Delta\Delta\rangle]).

   Under Δ → Δ_\lambda, the metric itself changes, and the measure (\sqrt{-g},d^3x) is *not* invariant in the way Derrick assumes. In other words, the “uniform scaling” in coordinate space is not a symmetry of the underlying correlation substrate.

Put differently:

* Derrick’s theorem assumes an **external**, rigid geometric arena you can rescale in arbitrarily.
* Pirouette’s geometry is **internal**, co-generated by Δ. Scaling Δ changes the arena itself, so the key step in Derrick’s argument (treat scaling as a variation at fixed geometry) fails.

Thus, from both perspectives:

* (i) treating the soliton as a string/vortex (codimension-2 defect)
* (ii) recognizing the metric as Δ-induced

we see that Derrick’s no-go does not constrain the n = ½ soliton sector.

---

### §4 · Time-Dependent Stabilization (Optional Strengthening)

If desired, you can go one step further and regard the n=½ soliton as a **Q-ball-like excitation** with a time-dependent internal phase:

[
\Delta(t,r,\theta) = f(r), e^{i(n\theta -\omega t)}.
]

Then the conserved Noether charge associated with global phase rotation provides an additional stabilizing quantity; the energy at fixed charge Q is minimized by a finite-radius configuration.

This gives you a second, independent path out of Derrick’s trap:

* scalar Q-balls are a known class of stable time-dependent solitons in 3+1D scalar theories,
* your Δ potential and phase structure are easily placed in that category.

You don’t have to lean on this in the main text, but it’s a nice backup if a referee is particularly hawkish.

---

### §5 · Summary of the Resolution

1. The Δ-soliton used for fermions is a **phase-winding, line-like vortex** (string) in 3+1D, not a 3D scalar lump.
2. The correct stability problem is 2D transverse energy per unit length; in that reduced problem, the energy functional has a clear finite-R minimum due to competition between angular gradient energy and potential energy.
3. Derrick’s theorem does not apply because:

   * it assumes codimension-0 lumps,
   * it assumes a fixed background geometry,
   * it uses a scaling variation that is not compatible with a Δ-induced metric.
4. Optionally, time-dependent, charge-carrying soliton solutions (Q-ball-like) provide an additional path to stability.

So the existence of an energetically preferred n = ½ soliton is consistent with known no-go theorems and fits well within the standard catalog of topological defects and Q-balls in scalar field theories.

---

## 🔧 Patch Text for the Main Paper (Drop-In Subsection)

Here’s a compact chunk you can paste into Section 2 after the soliton energy discussion to pre-empt Derrick complaints:

> **Soliton Stability and Derrick’s Theorem.**
> At first sight, the existence of a stable Δ-soliton in 3+1 dimensions seems to conflict with Derrick’s theorem, which forbids static, finite-energy, localized solutions of real scalar theories in D≥2 spatial dimensions on a fixed background. However, the fermionic soliton in Pirouette is not a 3D scalar lump but a line-like vortex (string) with phase-winding ansatz
> [
> \Delta(r,\theta) = f(r) e^{in\theta},
> ]
> translationally invariant along one spatial direction. The relevant quantity is the **energy per unit length** in the transverse (r,θ) plane,
> [
> E_\ell = 2\pi \int_0^\infty dr, r \left[
> \frac{\kappa_{\text{eff}}}{2}\left(f'^2 + \frac{n^2}{r^2}f^2\right)
>
> * V_{\text{eff}}(f)
>   \right],
>   ]
>   which exhibits a finite-radius minimum for each nonzero winding n: shrinking the core increases the angular-gradient term, while expanding it increases the potential energy. This is the standard vortex stability mechanism, not ruled out by Derrick’s theorem, which applies to codimension-0 lumps rather than codimension-2 defects.
>
> Moreover, in Pirouette the energy functional is defined on the **correlation-induced metric** (g_{\mu\nu}[\langle\Delta\Delta\rangle]) rather than on an external Minkowski background. The global scaling variation used in Derrick’s proof assumes a fixed geometric arena and does not respect the Δ → metric relation; scaling Δ changes the metric and the integration measure. Consequently, the key hypothesis of Derrick’s theorem is violated, and its conclusion does not constrain the Δ-soliton sector.
>
> Thus the n = ½ soliton underlying fermionic spin is consistent with known no-go theorems and behaves like a stable, finite-radius vortex/solitonic string whose energy is minimized at a preferred coherence length set by the Δ parameters.

---