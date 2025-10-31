---
id: DYNA-BH-INT-001
title: Coherent-Core Black Hole Interiors (Γ-Lighthouse Model)
version: 1.0
status: canon-target
parents: [SUBST-001, MATH-GR-001, GRW-003, MATH-GW-QUANTA-001]
children: [XXP-GR-EXP]
module_type: dynamics / compact objects
scale: horizon → near-horizon → ringdown (IR with (ω/ω_c)^2)
---

# §0 · Purpose

Model black-hole interiors as **new phases of the temporal medium** consistent with the substrate charter (SR-0…6), replacing GR singularities with **finite** Γ-structured states. We provide two minimal phases (both compatible with CPM & barrier finiteness):  
( A ) **Γ-Saturated “Planck Crystal” core** (stiff, phase-locked) and  
( B ) **Vortex-Foam decoherent core** (turbulent, coherence-fragmented).  
Both leave the exterior metric GR-like while imprinting **tiny, falsifiable** signatures in ringdown, photon rings, and late-time GW tails.

**Grounding**: emergent metric & constitutive law from SUBST-001; GR hydrodynamic limit; GW sector (2 TT pols, luminal; dispersion only at (ω/ω_c)^2).    

---

# §1 · Setup & Assumptions

- **Exterior**: stationary, axisymmetric GR solution (Schwarzschild/Kerr in the IR), by SUBST-001’s GR limit.   
- **Interior**: medium with fields \( \Gamma(r),\, Ki(\cdot) \) in a new phase; **no extra graviton polarizations** allowed anywhere (CPM).    
- **Barrier finiteness**: curvature growth saturates at \( \omega_c \) (prevents singularities).   
- **Small deviations**: any beyond-SM/QFT effects scale with \( \varepsilon \) (DYNA-004 bookkeeping). 

Metric ansatz (static, spherically symmetric core; spin handled via slow-rotation expansion later):
\[
ds^2=-e^{2\Phi(r)}dt^2 + \frac{dr^2}{1-2G_{\rm eff} m(r)/r}+r^2 d\Omega^2 .
\]

Γ-sector stress tensor (hydro-elastic from SUBST-001):
\[
T^{\mu\nu}_\Gamma = \partial^\mu\Gamma\,\partial^\nu\Gamma - g^{\mu\nu}\!\left(\tfrac12(\partial\Gamma)^2 - V(\Gamma)\right),
\]
with constitutive closure
\[
G_{\rm eff}^{-1}\sim \frac{\omega_c^2}{8\pi \Lambda_{\rm P}},\qquad
\Lambda_{\rm P}= m^2 V''(\Gamma).
\] 

---

# §2 · Two Minimal Interior Phases

## (A) Γ-Saturated “Planck Crystal” Core (stiff phase)
- **Equation of state**: near a potential minimum \( \Gamma\!\approx\!\Gamma_\star \), large \(V''(\Gamma_\star)\) ⇒ large \(\Lambda_{\rm P}\) ⇒ small compressibility.   
- **Profile ansatz**: \( \Gamma(r)=\Gamma_\star - \Delta_\Gamma e^{-r/\xi} \) for \(0\!\le r\!< r_\ast\) (core radius).  
- **Effect**: Effective **index-of-stiffness** raises the local GW phase velocity only at \((\omega/\omega_c)^2\) order (no extra modes). 

## (B) Vortex-Foam Decoherent Core (turbulent phase)
- **Equation of state**: \( \langle Ki \rangle\to 0\) locally with a dense tangle of vortices; CPM holds **on average**; \( \langle(\partial\Gamma)^2\rangle \) finite.  
- **Profile ansatz**: coarse-grained \( \overline{\Gamma}(r)\) smooth; fluctuations source **tiny** stochastic phase noise in TT modes, still suppressed by \((\omega/\omega_c)^2\). 

Both phases respect **single-metric universality** (SR-5) and thus preserve EP outside the core. 

---

# §3 · Interior Structure Equations (TOV-like system)

With total stress \(T^{\mu\nu}_{\rm tot}=T^{\mu\nu}_{\rm matter}+T^{\mu\nu}_\Gamma\) and Bianchi identities,
\[
\nabla_\mu T^{\mu\nu}_{\rm tot}=0 ,
\]
yielding a TOV-like system for \(m(r), \Phi(r), \Gamma(r)\) with source terms from \(V(\Gamma)\) and \((\partial\Gamma)^2\). 

Boundary data:
- **Core center** \(r\!=\!0\): \(m(0)\!=\!0,\ \Gamma'(0)\!=\!0\).  
- **Matching radius** \(r_\ast\): continuous \( \{g_{\mu\nu}\},\ \partial_r g_{\mu\nu}\) and **Israel-like** continuity of normal stresses from \(T^\mu_{\ \nu}(\Gamma)\).  
- **Exterior** \(r>r_\ast\): GR vacuum (Schwarzschild/Kerr in IR). 

---

# §4 · Ringdown & Wave Propagation (TT-phonons)

Adopt the TT-phonon action & propagator from **MATH-GW-QUANTA-001**; propagate through the interior as a **piecewise medium**:

- **Phase shift through Γ-core (your lighthouse):**
\[
\Delta\phi_{\rm GW} \simeq \kappa \left(\frac{\omega}{\omega_c}\right)^2
\int_0^{r_\ast}\!dr\, \big(\partial_r \Gamma(r)\big)^2 ,
\]
\(\kappa\) fixed by the response-kernel→metric dictionary. (Luminal in IR; correction only at barrier order.)  

- **Partial reflectivity at \(r_\ast\)** (stiff core): tiny GW **echo train** with spacing \(\Delta t \approx 2\int_{r_\ast}^{r_{\rm ph}} dr/\sqrt{f(r)g(r)}\) (photon-sphere radius \(r_{\rm ph}\)), but **no extra polarizations**. 

- **Vortex-foam core**: introduces subleading **phase noise** \(\propto (\omega/\omega_c)^2\langle(\nabla\Gamma)^2\rangle\) → predicts slightly broadened QNM peaks at high SNR, still TT-only.

---

# §5 · Photon Rings & Shadow

A Γ-gradient near/inside the light ring modifies the effective refractive structure via the constitutive law; prediction: **sub-percent shifts** in higher-order photon-ring radii with a sign tied to \(V''(\Gamma)\) (stiff core shifts outward). Exterior remains GR in the IR. 

---

# §6 · Love Numbers & Tidal Response

Because the exterior is GR-vacuum and the core sits **inside** the potential barrier, **static Love numbers remain ~GR-black-hole–like (≈0)** at leading order; any nonzero tidal response appears only at \((\omega/\omega_c)^2\) through dynamical TT scattering—keeps EP and CPM intact. 

---

# §7 · Falsifiable Signatures (to XXP-GR-EXP)

1) **No new GW polarizations** anywhere (hard falsifier; breaks SR-2/3).   
2) **Ringdown phase drift**: frequency-dependent dephasing \(\propto (\omega/\omega_c)^2\) with lighthouse integral above (sign from \(V''(\Gamma)\)).   
3) **Echo envelope**: at most **tiny**, barrier-suppressed reflectivity; large, broadband echoes would falsify the stiff-core minimal model.  
4) **Photon-ring tweaks**: sub-percent, sign-locked to \(V''(\Gamma)\).  
5) **Tidal Love**: effectively zero at leading order; detection of large static Love numbers falsifies CPM-respecting interiors.

(Registry links: GR-01, GR-06, EHT-like imaging; see XXP-GR-EXP.) 

---

# §8 · CI / Acceptance Criteria

- **AC-1**: \( \{g_{\mu\nu}, T^\mu_{\ \nu}(\Gamma)\} \) satisfy SUBST-001 constitutive law and GR limit outside \(r_\ast\).   
- **AC-2**: No scalar/vector GW modes appear in any gauge; only TT modes propagate.   
- **AC-3**: All predicted dispersive effects are explicitly tagged with \((\omega/\omega_c)^2\).   
- **AC-4**: Provide a numerically integrable \( \Gamma(r) \) with boundary matching at \(r_\ast\); export \(\Delta\phi_{\rm GW}(\omega)\), echo spacing \(\Delta t\), and photon-ring shifts to **XXP-GR-EXP**.

---

# §9 · Linkage Map

**Consumes:** SUBST-001 (SR-2/3/4/5/6), MATH-GR-001 (response→metric), GRW-003 (TT sector), MATH-GW-QUANTA-001 (quantized TT phonons).    
**Feeds:** XXP-GR-EXP (ringdown & imaging tests).

---

# §10 · Assemblé

> The singularity is replaced by a **phase**—a yolk of time under pressure. Outside, the loom reads as perfect GR; inside, Γ hums, and the graviton counts its threads as a barely-audible delay.

