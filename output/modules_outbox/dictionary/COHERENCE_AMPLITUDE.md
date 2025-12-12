---
term: "Coherence Amplitude"
canonical_id: "COHERENCE_AMPLITUDE"
symbol: "ψ"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-026"]
---

---
term: Coherence Amplitude
canonical_id: COHERENCE_AMPLITUDE
symbol: ψ
aliases: [order parameter, complex coherence amplitude]
parents: [MATH-025, MATH-024]
children: [DOMA-096, COG-RES-002, SOCIO-FIELD-003]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-026
      lines: "§2"
      snippet: |
        LPF:
        F[ψ] = ∫ [ a(T_a−T_c)|ψ|^2 + (b/2)|ψ|^4 + c|∇ψ|^2 + U(Γ,S) ] d^d x
        ...
        Order parameter: ψ(x,t) (complex coherence amplitude).
  editors: [Pirouette Framework AI]
  review_log: []
triad:
  art: |
    The quiet hum of agreement, a wave rising from the noise of many thoughts to crest as a single, shared moment. It is the phase-lock of minds, the emergent pattern in the static, the shared breath of a system waking up to itself.
  law: |
    The Coherence Amplitude is a complex field, ψ = |ψ|e^(iΦ), whose magnitude squared |ψ|^2 measures the local density of ordered activity and whose gradient energy c|∇ψ|^2 penalizes spatial variations. Its dynamics are governed by the minimization of the Landau–Pirouette Functional, and near a continuous phase transition, its fluctuations exhibit universal scaling behavior determined by the Pirouette Wilson–Fisher fixed point.
  philosophy: |
    Coherence Amplitude posits that the emergence of order—in minds, markets, or matter—is a fundamental, field-like phenomenon. By treating coherence as a measurable quantity, ψ provides a unified mathematical language to describe phase transitions across disparate domains. It makes the intangible organization of a system tangible, computable, and predictive.
pirouette_definition: |
  A complex-valued field, ψ(x, t) = |ψ|e^(iΦ), that serves as the order parameter for coherent activity in the Pirouette Framework. Its magnitude, |ψ|, quantifies the local intensity or density of phase-locked behavior, while its phase, Φ, represents the local timing, orientation, or reference frame of that coherence. The dynamics of ψ are governed by the Landau–Pirouette Functional, and its statistical properties describe the macroscopic state of the system, including its proximity to a phase transition between incoherent and coherent regimes.
operational_definition:
  units: Contextual. Often normalized to be dimensionless near a critical point. Can be related to domain-specific units (e.g., √[activity_density] in COG).
  symbol_table:
    - name: ψ
      meaning: Coherence Amplitude (complex)
      dimensions: Contextual, e.g., M^0 L^(-d/2) T^0 in normalized RG flow
      default_range: Contextual
    - name: |ψ|^2
      meaning: Coherence Density (real, non-negative)
      dimensions: Contextual, e.g., M^0 L^(-d) T^0 in normalized RG flow
      default_range: [0, 1] after normalization
    - name: Φ
      meaning: Coherence Phase (real)
      dimensions: dimensionless
      default_range: [0, 2π] radians
  measurement:
    procedures:
      - name: Inferential Fitting to Fluctuation Spectra
        outline: |
          1. Collect high-resolution spatio-temporal data from the substrate (e.g., EEG grid, social network message flux, fluid velocity field).
          2. Compute the static structure factor S(k), the spatial Fourier transform of the two-point correlation function.
          3. Near a transition, S(k) is proportional to the theoretical susceptibility, ⟨ψ(k)ψ*(−k)⟩ ∼ 1/(a + ck^2).
          4. Fit the observed S(k) to this Ornstein-Zernike form to extract the effective LPF parameters 'a' and 'c'.
          5. The mean coherence |ψ|^2 can be inferred from the LPF parameters, particularly the value of 'a' relative to the nonlinear term 'b'.
        expected_signals: [Lorentzian-like peaks in the power spectrum, divergence of the zero-momentum (k=0) susceptibility as `a` approaches 0.]
        pitfalls: [System is far from equilibrium, invalidating LPF assumptions; dominant noise sources obscure the collective mode; insufficient spatial resolution to accurately measure the k-dependence.]
context_windows:
  - module: MATH-026
    excerpt: |
      Order parameter: ψ(x,t) (complex coherence amplitude). ... F[ψ] = ∫ [ a(T_a−T_c)|ψ|^2 + (b/2)|ψ|^4 + c|∇ψ|^2 + U(Γ,S) ] d^d x
  - module: MATH-026
    excerpt: |
      For triadic fields ψ1,ψ2,ψ3 with constraint f3=f1+f2 (COG-RES-001), add F_tri = − g ∫ |ψ1||ψ2||ψ3| cos(Φ1+Φ2−Φ3) d^d x. ... At the WF point, small g is marginally relevant if y_g>0, yielding a locked-triad fixed surface with reduced fluctuations in the resonant subspace.
  - module: MATH-026
    excerpt: |
      Define scale transformation with factor ℓ>1: x → x' = x/ℓ,   ψ(x) → ψ'(x') = ℓ^{ζ} ψ(x). Choose ζ so that the gradient term remains form-invariant... This yields ζ = (2−d)/2.
poetic_connections:
  motifs: [crystallization, resonance, phase-locking, shared-thought, emergent-pattern, consensus]
  evocative_lines:
    - "the consciousness triad as an RG-selected manifold"
    - "crossover scaling between ψ-dominated fixed point and Γ-driven line with damped ψ-fluctuations"
  association_matrix:
    - [ "ADHERENCE", 0.9 ]
    - [ "TEMPORAL_PRESSURE", 0.8 ]
    - [ "TRIADIC_LOCKING", 0.7 ]
    - [ "LANDAU_PIROUETTE_FUNCTIONAL", 1.0 ]
formal_mappings:
  candidates:
    - target: Ginzburg-Landau Order Parameter `ψ`
      domain: CM
      mapping_kind: mathematical
      equation_hint: |
        F_GL[ψ] = ∫ [ α(T−T_c)|ψ|^2 + (β/2)|ψ|^4 + (1/2m*)|(-iħ∇ - q*A)ψ|^2 ] d^d x
      justification: |
        The Pirouette LPF is a direct mathematical generalization of the Ginzburg-Landau free energy functional, which describes second-order phase transitions in condensed matter systems like superconductors and superfluids. The terms `a|ψ|^2`, `b|ψ|^4`, and `c|∇ψ|^2` map directly to the corresponding terms in the G-L theory. Pirouette extends this formalism to cognitive and social domains.
      references:
        - title: Statistical Physics of Fields
          where: Chapter 8, Kardar, Mehran
          date: 2007-01-01
      confidence: 0.95
  adopted:
    - target: Ginzburg-Landau Order Parameter `ψ`
      rationale: The mapping is a direct, intentional generalization. The entire RG formalism in MATH-026 is built upon the field-theoretic methods developed for G-L theories, making this the foundational analogy.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "Near a continuous coherence transition, system observables (e.g., susceptibility, correlation length) scale with universal critical exponents predicted by the Pirouette Wilson–Fisher fixed point."
      domain: phenomenology
      falsifier: "Experimental measurement of critical exponents (β_P, γ_P, ν) that are inconsistent with the ε-expansion values derived from the RFC or that violate RG hyperscaling identities like γ_P = (2−η)ν."
      status: proposed
      links: [MATH-026]
    - statement: "The Coherence Amplitude ψ is a non-conserved field, leading to dynamic critical scaling with an exponent z_P ≈ 2 (Model A dynamics)."
      domain: theory
      falsifier: "Observation of conservative dynamics, such as diffusion, in the long-wavelength limit, or measurement of a dynamic exponent z_P significantly different from 2 in systems without other slow-moving conserved quantities."
      status: proposed
      links: [MATH-026]
naming_notes:
  collisions: [The symbol ψ is the standard notation for the quantum mechanical wave function.]
  disambiguation: |
    Pirouette's Coherence Amplitude ψ is a classical (or semi-classical) macroscopic field representing the average behavior of a statistical ensemble. It is an order parameter, not a probability amplitude for a single quantum particle. While both are complex fields, the Pirouette ψ emerges from collective dynamics and its magnitude is directly observable, whereas the QM wavefunction's magnitude squared is a probability density for a fundamental entity.
crosslinks:
  near_synonyms: [ORDER_PARAMETER]
  antonyms: [INCOHERENCE, NOISE_AMPLITUDE]
  prerequisites: [LANDAU_PIROUETTE_FUNCTIONAL, ADHERENCE]
  downstream_effects: [TRIADIC_LOCKING, CRITICAL_SLOWING_DOWN, CADUCEUS_LENS]
license: CC-BY-SA-4.0
---

# Coherence Amplitude

## Canonical (Pirouette)
A complex-valued field, ψ(x, t) = |ψ|e^(iΦ), that serves as the order parameter for coherent activity in the Pirouette Framework. Its magnitude, |ψ|, quantifies the local intensity or density of phase-locked behavior, while its phase, Φ, represents the local timing, orientation, or reference frame of that coherence. The dynamics of ψ are governed by the Landau–Pirouette Functional, and its statistical properties describe the macroscopic state of the system, including its proximity to a phase transition between incoherent and coherent regimes.

## EFT-First Summary
The Coherence Amplitude `ψ` is the Pirouette Framework's generalization of the Ginzburg-Landau order parameter. It is a classical complex field whose dynamics are governed by a `ψ^4`-type Landau-Pirouette Functional. Its magnitude squared, `|ψ|^2`, represents the local density of emergent order, and its phase encodes the spatiotemporal alignment of the system's components. The Renormalization Group flow of the LPF couplings determines the universal scaling behavior of `ψ` near critical points, analogous to the Wilson-Fisher fixed point in statistical field theory.

## Glossary Links
- See also: [ORDER_PARAMETER](<...>), [LANDAU_PIROUETTE_FUNCTIONAL](<...>), [TEMPORAL_PRESSURE](<...>)