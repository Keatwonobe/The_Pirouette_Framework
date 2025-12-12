---
term: "Gradient-flow scale"
canonical_id: "GRADIENT_FLOW_SCALE"
symbol: "t₀"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-YM-003_nonperturbative_map"]
---

---
term: Gradient-flow scale
canonical_id: GRADIENT_FLOW_SCALE
symbol: t₀
aliases: [Wilson flow scale, t_0 scale]
parents: [MATH-YM-003]
children: [XXP-EWQCD-EXP]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-YM-003_nonperturbative_map
      lines: "L68-L69"
      snippet: |
        * **Gradient-flow (t_0):** (t^2\langle E\rangle!\mid_{t=t_0}=0.3) (or chosen constant).
  editors: [Pirouette Framework AI]
  review_log: []
triad:
  art: |
    A temporal lens that smoothes the lattice's quantum foam, revealing the intrinsic size of a gluon field by measuring how long it takes for its energy to settle.
  law: |
    The gradient-flow scale t₀ is the flow time `t` at which the dimensionless combination `t²⟨E⟩` reaches a fixed, conventional value (typically 0.3), where `E` is the average plaquette energy density. This relation defines a physical length scale `√t₀` from the dynamics of the gauge field itself.
  philosophy: |
    To provide a robust, operator-independent reference length for lattice simulations, defined by the characteristic diffusion time of the gauge field. This links the abstract lattice spacing to physical energy scales with high precision and minimal sensitivity to simulation details like quark masses.
pirouette_definition: |
  Within Pirouette, the gradient-flow scale t₀ is a deterministic, nonperturbative reference scale derived from the fundamental string tension (`σ`). It is defined as the Wilson flow time `t` at which the expectation value of the energy density `E` satisfies `t²⟨E⟩ = C`, where `C` is a fixed constant (canonically 0.3). The framework predicts the physical value of `√t₀`, allowing for the conversion of dimensionless lattice measurements (`t₀/a²`) into a physical lattice spacing (`a`).
operational_definition:
  units: `[Length]²`. Often quoted as `√t₀` with units of `[Length]`.
  symbol_table:
    - name: t₀
      meaning: Gradient-flow scale
      dimensions: L²
      default_range: `√t₀ ≈ 0.14-0.15` fm for QCD
    - name: t
      meaning: Wilson flow time parameter
      dimensions: L²
      default_range: contextual
    - name: E
      meaning: Gauge field energy density
      dimensions: L⁻⁴
      default_range: contextual
    - name: a
      meaning: Lattice spacing
      dimensions: L
      default_range: contextual
  measurement:
    procedures:
      - name: Wilson Flow Measurement on Lattice
        outline: |
          1. Generate a gauge field ensemble for a given set of simulation parameters.
          2. Evolve each configuration in the ensemble according to the Wilson flow differential equation, parametrized by flow time `t`.
          3. At each step `t`, measure a suitable discretization of the gauge energy density `⟨E⟩` (e.g., from the average plaquette).
          4. Form the dimensionless product `t²⟨E⟩`.
          5. Interpolate to find the specific flow time `t` where `t²⟨E⟩ = 0.3`. This value, in lattice units, is `t₀/a²`.
          6. Convert to physical units using a known hadron mass or by using the Pirouette-predicted value of `√t₀`.
        expected_signals: [A smooth curve for `t²⟨E⟩(t)` that monotonically increases and crosses the reference value 0.3.]
        pitfalls: [Finite volume effects, discretization errors requiring continuum extrapolation, choice of the energy density operator `E`.]
context_windows:
  - module: MATH-YM-003_nonperturbative_map
    excerpt: |
      **Reference scales:**
      * **Sommer scale (r_0)** via
        [
        r_0^2,F(r_0)=1.65,\qquad F(R)=\frac{dV}{dR}.
        ]
      * **Gradient-flow (t_0):** (t^2\langle E\rangle!\mid_{t=t_0}=0.3) (or chosen constant).

      **Conversions (deterministic once (\sigma) fixed):**
      [
      a = \frac{r_0}{(r_0/a)*{\rm lat}}
      \quad\text{or}\quad
      a = \sqrt{\frac{t_0}{(t_0/a^2)*{\rm lat}}}.
      ]
      Thus, **Pirouette → (\sigma) → (r_0,t_0) → (a)** gives a **numerical lattice spacing** prediction.
  - module: MATH-YM-003_nonperturbative_map
    excerpt: |
      **Worked deterministic recipe** (step-by-step)
      1. **Inputs**: (\omega_c) (Bridge), (\chi) (Bridge), (g_s(\mu_\ast)) from RG (MATH-YM-002).
      2. **Compute** (\xi_\Gamma = (c/\omega_c)\chi^{-1/2}).
      3. **Set** (\kappa_3\sim 1/g_s^2(\mu_\ast)) (with normalization fixed once).
      4. **Predict** (\sigma = c_\sigma \kappa_3/\xi_\Gamma^2).
      5. **Derive** (r_0,t_0); **predict** lattice spacing (a) for any measured ((r_0/a)) or ((t_0/a^2)).
poetic_connections:
  motifs: [diffusion, smoothing, scale-setting, renormalization]
  evocative_lines:
    - "The flow smoothes the quantum jitters, revealing the scale where the field breathes."
    - "This dictionary is your conductor’s score: stiffness sets the strings, coherence sets the drum skin, and out comes σ."
  association_matrix:
    - [ "STRING_TENSION", 0.9 ]
    - [ "LATTICE_SPACING", 0.9 ]
    - [ "SOMMER_SCALE", 0.7 ]
    - [ "RENORMALIZATION_GROUP", 0.6 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Diffusion time in a heat equation
      domain: Math
      mapping_kind: mathematical
      equation_hint: |
        ∂Bμ/∂t = D² Bμ
      justification: |
        The Wilson flow is a gauge-covariant diffusion equation that smears the gauge fields over a characteristic radius `r ~ √(8t)`. The flow time `t` acts as a fifth-dimensional coordinate parameterizing this smoothing process. The scale `t₀` is therefore a physically-defined characteristic diffusion time/length-squared for the gauge theory.
      references:
        - title: Properties and uses of the Wilson flow in lattice QCD
          where: JHEP 1008 (2010) 071, arXiv:1006.4518
          date: 2010-06-23
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "The Pirouette framework's prediction for the physical value of `t₀` (derived from `κ₃` and `ξΓ` via `σ`) is consistent with the value extracted from lattice simulations after a single, universal normalization."
      domain: phenomenology
      falsifier: "A statistically significant disagreement between the Pirouette-predicted `√t₀` and the continuum-extrapolated lattice value across multiple gauge ensembles with different parameters."
      status: proposed
      links: [MATH-YM-003]
naming_notes:
  collisions: [The symbol `t` is heavily overloaded (e.g., coordinate time). `t₀` specifically refers to a constant value of the *flow time* parameter.]
  disambiguation: |
    Distinguish the gradient-flow scale `t₀` (a constant with dimensions of [Length]²) from the flow-time variable `t`. `t₀` is a specific value of `t` where a physical condition is met. It is often cited via its square root, `√t₀`, which has units of length and is directly comparable to other scales like `r₀`.
crosslinks:
  near_synonyms: [SOMMER_SCALE]
  antonyms: []
  prerequisites: [STRING_TENSION]
  downstream_effects: [LATTICE_SPACING]
license: CC-BY-SA-4.0
---

# Gradient-flow scale

## Canonical (Pirouette)
Within Pirouette, the gradient-flow scale t₀ is a deterministic, nonperturbative reference scale derived from the fundamental string tension (`σ`). It is defined as the Wilson flow time `t` at which the expectation value of the energy density `E` satisfies `t²⟨E⟩ = C`, where `C` is a fixed constant (canonically 0.3). The framework predicts the physical value of `√t₀`, allowing for the conversion of dimensionless lattice measurements (`t₀/a²`) into a physical lattice spacing (`a`).

## EFT-First Summary
The gradient-flow scale `t₀` is a reference scale in lattice gauge theory defined via the Wilson flow, a process mathematically equivalent to diffusion of the gauge field. `t₀` is the specific "flow time" at which the smoothed energy density reaches a pre-defined value. This provides a robust, physical length scale `√t₀` (≈ 0.14-0.15 fm in QCD) that is used to set the absolute scale of simulations and determine the lattice spacing. For more on the Wilson flow, see Lüscher (2010).

## Glossary Links
- See also: Sommer scale (`r₀`), String Tension (`σ`), Lattice Spacing (`a`)