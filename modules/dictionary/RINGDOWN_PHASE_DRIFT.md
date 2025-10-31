---
term: "Ringdown Phase Drift"
canonical_id: "RINGDOWN_PHASE_DRIFT"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DYNA-BH-INT-001"]
---

---
term: Ringdown Phase Drift
canonical_id: RINGDOWN_PHASE_DRIFT
symbol: Δϕ_GW
aliases: [Lighthouse Effect, Core-Induced Dephasing]
parents: [DYNA-BH-INT-001]
children: [XXP-GR-EXP]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DYNA-BH-INT-001
      lines: "L102-L106"
      snippet: |
        - **Phase shift through Γ-core (your lighthouse):**
        \[
        \Delta\phi_{\rm GW} \simeq \kappa \left(\frac{\omega}{\omega_c}\right)^2
        \int_0^{r_\ast}\!dr\, \big(\partial_r \Gamma(r)\big)^2 ,
        \]
        \(\kappa\) fixed by the response-kernel→metric dictionary. (Luminal in IR; correction only at barrier order.)
  editors: [system-generator]
  review_log: []
triad:
  art: |
    As a gravitational wave passes through the heart of a black hole, the core acts like a lens made of spacetime itself. Higher frequencies are delayed more, causing the wave's final chorus—the ringdown—to subtly lose its perfect timing, like light splitting through a prism. The graviton counts its threads as a barely-audible delay.
  law: |
    The cumulative phase shift (Δϕ_GW) experienced by a tensor-polarized gravitational wave of frequency ω passing through a Γ-structured core is directly proportional to the square of its frequency, (ω/ω_c)², and the integrated squared gradient of the Γ-field within the core radius. This effect is absent at leading order (IR) and constitutes a specific, falsifiable prediction of beyond-GR interior physics.
  philosophy: |
    This effect transforms the unobservable black hole interior into a testable medium. By imprinting a memory of its structure onto escaping gravitational waves, the Ringdown Phase Drift provides a potential observational window into physics at the Planck scale, turning the final moments of a black hole merger into a probe of quantum gravity, without violating no-hair theorems or the equivalence principle in the exterior spacetime.
pirouette_definition: |
  A cumulative, frequency-dependent phase shift imprinted on the quasinormal modes (QNMs) of a gravitational wave ringdown signal. The shift is induced by the propagation of the wave through the Γ-structured core of a compact object, which acts as a dispersive medium. The effect is a higher-order correction to General Relativity, scaling as (ω/ω_c)², and its magnitude depends on the specific profile of the Γ-field within the core.
operational_definition:
  units: radians (rad) or dimensionless
  symbol_table:
    - name: Δϕ_GW
      meaning: Total phase shift accumulated by the GW.
      dimensions: dimensionless
      default_range: 10⁻³ – 10⁻⁵ rad for typical astrophysical events
    - name: ω
      meaning: Angular frequency of the gravitational wave mode.
      dimensions: T⁻¹
      default_range: contextual (kHz for stellar-mass BHs)
    - name: ω_c
      meaning: Barrier finiteness scale, an intrinsic high-energy cutoff of the core medium.
      dimensions: T⁻¹
      default_range: ~ Planck frequency
    - name: Γ(r)
      meaning: The Γ-field profile as a function of radial coordinate r inside the core.
      dimensions: M L⁻¹ T⁻¹ (contextual)
      default_range: contextual
    - name: r_∗
      meaning: Radius of the Γ-structured core.
      dimensions: L
      default_range: ~ Planck length to ~0.1 r_horizon
  measurement:
    procedures:
      - name: QNM Phase Spectroscopy
        outline: |
          1. Observe a high-SNR gravitational wave signal from a binary black hole merger, focusing on the post-merger ringdown phase.
          2. Perform a parameter estimation analysis by fitting the observed waveform to a GR-based QNM template plus a modification term.
          3. Include a free parameter that models a frequency-dependent phase correction of the form Δϕ(ω) = βω².
          4. A statistically significant non-zero measurement of β provides evidence for the Ringdown Phase Drift and allows for the inference of the lighthouse integral ∫(∂_r Γ)²dr.
        expected_signals: [A systematic phase residual in the ringdown signal that grows quadratically with QNM frequency/mode number.]
        pitfalls: [Low SNR, difficulty in distinguishing the effect from higher-order GR multipoles or environmental effects, degeneracy with source parameters.]
context_windows:
  - module: DYNA-BH-INT-001
    excerpt: |
      **Phase shift through Γ-core (your lighthouse):**
      \[
      \Delta\phi_{\rm GW} \simeq \kappa \left(\frac{\omega}{\omega_c}\right)^2
      \int_0^{r_\ast}\!dr\, \big(\partial_r \Gamma(r)\big)^2 ,
      \]
      \(\kappa\) fixed by the response-kernel→metric dictionary. (Luminal in IR; correction only at barrier order.)
  - module: DYNA-BH-INT-001
    excerpt: |
      **Falsifiable Signatures (to XXP-GR-EXP)**
      ...
      2) **Ringdown phase drift**: frequency-dependent dephasing \(\propto (\omega/\omega_c)^2\) with lighthouse integral above (sign from \(V''(\Gamma)\)).
poetic_connections:
  motifs: [refractive core, temporal medium, lighthouse effect, phase memory, chromatic gravity]
  evocative_lines:
    - "the graviton counts its threads as a barely-audible delay."
    - "The singularity is replaced by a phase—a yolk of time under pressure."
  association_matrix:
    - [ "GAMMA_FIELD", 0.9 ]
    - [ "BARRIER_FINITENESS", 0.8 ]
    - [ "QUASINORMAL_MODE", 0.7 ]
    - [ "GW_ECHO_TRAIN", 0.4 ]
formal_mappings:
  candidates:
    - target: Chromatic dispersion in a medium
      domain: CM|AMO
      mapping_kind: conceptual
      equation_hint: |
        k(ω) = (ω/c) n(ω), where n(ω) ≈ 1 + αω²
      justification: |
        The Γ-core imparts an effective frequency-dependent index of refraction `n(ω)` to spacetime for propagating GWs. The phase shift Δϕ over a distance L is ωL(n-1)/c. A phase shift ∝ ω³ (from k(ω)∝ω³) corresponds to a total phase integral Δϕ(t) ∝ ω², matching the leading-order dispersive effect in many effective field theories.
      references:
        - title: Foundations of Pulsar Astronomy
          where: Section on Dispersion Measure
          date: 1992-01-01
      confidence: 0.9
    - target: EFT higher-derivative corrections
      domain: EFT|GR
      mapping_kind: mathematical
      equation_hint: |
        S_eff ⊃ ∫ d⁴x √-g ( R + α (R_μν R^μν)²/M_P⁴ + ... )
      justification: |
        In an effective field theory of gravity, higher-derivative terms suppressed by a high-energy scale (like M_P or ω_c) modify the propagator for gravitons. These modifications generically introduce new momentum/frequency dependence, leading to corrections to the dispersion relation of the form ω² = k²(1 ± (k/M_P)²), which manifests as a frequency-dependent phase shift for propagating waves.
      references:
        - title: Effective field theory for astrophysical black holes
          where: Living Reviews in Relativity (2018)
          date: 2018-08-20
      confidence: 0.8
  adopted:
    - target: null
      rationale: null
      confidence: 0.0
constraints_and_falsifiers:
  claims:
    - statement: "The phase drift scales quadratically with frequency, i.e., Δϕ ∝ ω²."
      domain: phenomenology
      falsifier: "An observed phase drift that scales linearly (∝ ω), cubically (∝ ω³), or with any other power law would falsify the specific dynamics of the Γ-Lighthouse Model."
      status: proposed
      links: [DYNA-BH-INT-001]
    - statement: "The phase drift affects only the two tensor (TT) polarizations of gravitational waves."
      domain: theory
      falsifier: "Observation of a similar phase drift in scalar or vector GW modes would falsify the single-metric universality (SR-5) and no-extra-polarizations (CPM) constraints of the parent module."
      status: proposed
      links: [DYNA-BH-INT-001, SUBST-001]
naming_notes:
  collisions: [Phase drift in electronics, clock drift.]
  disambiguation: |
    This term refers to a fixed, cumulative phase *shift* whose *magnitude* is frequency-dependent, not a continuous drift over time. It is imprinted on the wave as it passes through the core. It is distinct from the slow dephasing of binary inspirals, which occurs over many cycles; this effect is localized to the ringdown phase and is caused by the structure of the final object's interior.
crosslinks:
  near_synonyms: []
  antonyms: [GR_PHASE_COHERENCE]
  prerequisites: [GAMMA_FIELD, BARRIER_FINITENESS, QUASINORMAL_MODE]
  downstream_effects: [PHOTON_RING_SHIFTS]
license: CC-BY-SA-4.0
---

# Ringdown Phase Drift

## Canonical (Pirouette)
A cumulative, frequency-dependent phase shift imprinted on the quasinormal modes (QNMs) of a gravitational wave ringdown signal. The shift is induced by the propagation of the wave through the Γ-structured core of a compact object, which acts as a dispersive medium. The effect is a higher-order correction to General Relativity, scaling as (ω/ω_c)², and its magnitude depends on the specific profile of the Γ-field within the core.

## EFT-First Summary
The Ringdown Phase Drift is the phenomenological signature of higher-derivative corrections to the gravitational action, localized within the black hole core. These corrections, suppressed by a high-energy scale `ω_c`, modify the graviton propagator to be dispersive. This causes the phase velocity of gravitational waves to depend on their frequency as `v_p(ω) ≈ c(1 - αω²)`, leading to an observable, frequency-squared dephasing in the ringdown signal that directly probes the equation of state of the interior medium.

## Glossary Links
- See also: [GW Echo Train](./gw_echo_train.md), [Photon Ring Shifts](./photon_ring_shifts.md), [Quasinormal Mode](./quasinormal_mode.md)