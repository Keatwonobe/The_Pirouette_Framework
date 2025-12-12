---
term: "Renormalization Flow of Coherence"
canonical_id: "RENORMALIZATION_FLOW_OF_COHERENCE"
symbol: ""
aliases: [RFC]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-026"]
---

---
term: Renormalization Flow of Coherence
canonical_id: RENORMALIZATION_FLOW_OF_COHERENCE
symbol: N/A
aliases: [RFC]
parents: [MATH-025, MATH-024]
children: [DOMA-096, COG-RES-002, SOCIO-FIELD-003]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-026
      lines: "§4"
      snippet: |
        β_b ≡ db/dlnℓ = −ε b + 3K_d b^2
        β_a ≡ da/dlnℓ = 2a − K_d b (n+2)/6 · a_correction
  editors: [Agent: Pirouette Knowledge Synthesis]
  review_log: []
triad:
  art: |
    As one zooms out from a system's microscopic details, the laws of its coherence blur and sharpen into new, simpler forms. The chaotic dance of individual agents resolves into the universal waltz of a phase transition. This flow reveals the inevitable emergence of large-scale order from small-scale noise.
  law: |
    The effective parameters (a, b, c, λ, g) of the Landau–Pirouette Functional are scale-dependent, evolving according to a set of coupled differential equations (β-functions). This flow dictates universal critical exponents (e.g., ν, β_P) and crossover behaviors near coherence transitions, which must be independent of the specific substrate details.
  philosophy: |
    RFC provides the mathematical foundation for Pirouette's core claim of universality. It demonstrates that despite vast differences in microscopic substrates—from neurons to economic agents—the collective behavior near a phase transition is governed by a small number of universal fixed points and scaling laws. This allows for predictive power across seemingly disparate domains.
pirouette_definition: |
  The Renormalization Flow of Coherence is the theoretical framework describing how the parameters of the Landau–Pirouette Functional (LPF) evolve under changes in observational scale (ℓ). It employs renormalization group (RG) techniques to derive β-functions for the LPF couplings (a, b, c, Γ-couplings λ, triadic couplings g). The flow's fixed points, particularly the Pirouette Wilson–Fisher point, define universality classes that govern the critical behavior (exponents, scaling functions) of coherence transitions across physical, cognitive, and social domains.
operational_definition:
  units: Dimensionless flow equations for dimensionful couplings.
  symbol_table:
    - name: ℓ
      meaning: Scale transformation factor
      dimensions: dimensionless
      default_range: "> 1"
    - name: β_g
      meaning: Beta function for coupling g; dg/d(ln ℓ)
      dimensions: Dimensions of g
      default_range: contextual
    - name: y_g
      meaning: RG eigenvalue of coupling g at a fixed point
      dimensions: dimensionless
      default_range: "-ε to 2"
    - name: a
      meaning: Quadratic coupling (proximity to critical adherence T_a)
      dimensions: contextual
      default_range: contextual
    - name: b
      meaning: Quartic coupling (nonlinear damping)
      dimensions: contextual
      default_range: "> 0"
    - name: λ
      meaning: Coupling strength of Temporal Pressure (Γ) to coherence
      dimensions: contextual
      default_range: contextual
  measurement:
    procedures:
      - name: Scale-Dependent Parameter Fitting
        outline: |
          1. Collect time-series data of a coherence observable (e.g., triadic resonance amplitude).
          2. Coarse-grain the data by averaging over windows of increasing size L.
          3. For each scale L, fit the Landau-Pirouette Functional (LPF) to the data's statistical distribution to extract effective parameters a(L), b(L), λ(L).
          4. Plot the extracted parameters as a function of ln(L). The slopes of these plots are the empirical β-functions.
          5. Compare the flow to theoretical predictions to identify the system's position in the parameter space relative to a fixed point.
        expected_signals: [Power-law dependence of fitted parameters a(L) and b(L) near a critical point, Crossover in scaling behavior as a control parameter like Γ is varied]
        pitfalls: [Insufficient data to resolve scaling over a wide range of L, Strong irrelevant operators obscuring universal flow at small scales, System is far from any critical point]
context_windows:
  - module: MATH-026
    excerpt: |
      Solve β_b=0 → b* = ε/3. [...] Eigenvalues give relevant/irrelevant directions: y_a = 2−κ b* (relevant), y_b = −ε (irrelevant for ε>0). Thus the Pirouette Wilson–Fisher point (a*,b*,λ*) controls second-order coherence transitions for d<4, defining the universality class reported in MATH-025.
  - module: MATH-026
    excerpt: |
      When Γ varies slowly in space or time, λ flows generate crossover scaling between: (i) ψ-dominated fixed point (λ→λ*) and (ii) Γ-driven line (λ→∞) with damped ψ-fluctuations. Observable susceptibility: χ_P(L,Γ) ≈ L^{γ_P/ν} ϕ( L/ξ, L/ξ_Γ ). Empirically, this produces triad-detuning band shrinkage in COG under Γ load.
  - module: MATH-026
    excerpt: |
      Substrate parameters (conductance, latency, noise spectra) renormalize into effective (a,b,c,λ,g). Practical rule: Increase in latency → raises a (harder to cohere); Increased noise at resonant bands → raises effective b (stronger nonlinear damping). Mapping χ_S must be calibrated per domain, but flow topology (fixed points, eigenvalues) remains substrate-invariant.
poetic_connections:
  motifs: [scaling, universality, coarse-graining, emergence, fixed points, relevance]
  evocative_lines:
    - "Unifies substrate-specific microdynamics with macro-level coherence via RG transformations..."
    - "...formalizing the consciousness triad as an RG-selected manifold."
  association_matrix:
    - [ "UNIVERSALITY", 0.9 ]
    - [ "COHERENCE_TRANSITION", 0.8 ]
    - [ "LANDAU_PIROUETTE_FUNCTIONAL", 0.9 ]
    - [ "TEMPORAL_PRESSURE", 0.6 ]
formal_mappings:
  candidates:
    - target: Wilsonian Renormalization Group (RG)
      domain: Statistical Field Theory
      mapping_kind: mathematical
      equation_hint: |
        β_g = d g / d(ln ℓ)
      justification: |
        The module explicitly derives β-functions for the LPF couplings by integrating out high-momentum modes in a momentum shell, following Wilson's procedure. It identifies a non-trivial fixed point (the Wilson-Fisher fixed point) that controls the universal scaling behavior of the system near its critical point. The methodology is a direct, canonical application of standard RG.
      references:
        - title: The renormalization group: Critical phenomena and the Kondo problem
          where: Rev. Mod. Phys. 47, 773
          date: 1975-10-01
      confidence: 1.0
  adopted:
    - target: Wilsonian Renormalization Group
      rationale: The mapping is not an analogy but a direct mathematical application of standard RG methods to the Pirouette-specific Landau-Ginzburg-type functional (LPF). The terminology (β-functions, fixed points, critical exponents, ε-expansion) is used identically.
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "Measured critical exponents for coherence transitions in diverse domains (e.g., cognitive, social) must obey RG scaling relations, such as γ_P = (2−η)ν."
      domain: phenomenology
      falsifier: "Experimental measurement of exponents that violate these identities."
      status: proposed
      links: [MATH-026]
    - statement: "Systems described by the LPF in d<4 dimensions must exhibit a non-trivial (b* > 0) fixed point governing second-order transitions."
      domain: theory
      falsifier: "Empirical evidence showing only mean-field behavior or first-order transitions where the RFC predicts a continuous one."
      status: proposed
      links: [MATH-026]
    - statement: "The influence of temporal pressure (Γ) on coherence susceptibility follows the predicted crossover scaling function."
      domain: experiment
      falsifier: "Observing that the effect of Γ is a simple shift in the critical point without the characteristic change in scaling behavior."
      status: under-test
      links: [COG-RES-002, SOCIO-FIELD-003]
naming_notes:
  collisions: [The term "Renormalization Group" and symbols like β, γ, ν are standard in statistical physics.]
  disambiguation: |
    Unlike colloquial uses of "renormalization" (e.g., re-evaluating a situation), RFC refers to a precise mathematical procedure from statistical physics for tracking how a system's descriptive parameters change with observational scale. It is not a metaphor but a calculation engine.
crosslinks:
  near_synonyms: [RG_FLOW]
  antonyms: [SCALE_INVARIANCE, MEAN_FIELD_THEORY]
  prerequisites: [LANDAU_PIROUETTE_FUNCTIONAL, COHERENCE_ORDER_PARAMETER]
  downstream_effects: [UNIVERSALITY_CLASS, CRITICAL_EXPONENTS, TRIADIC_LOCKING]
license: CC-BY-SA-4.0
---

# Renormalization Flow of Coherence

## Canonical (Pirouette)
The Renormalization Flow of Coherence is the theoretical framework describing how the parameters of the Landau–Pirouette Functional (LPF) evolve under changes in observational scale (ℓ). It employs renormalization group (RG) techniques to derive β-functions for the LPF couplings (a, b, c, Γ-couplings λ, triadic couplings g). The flow's fixed points, particularly the Pirouette Wilson–Fisher point, define universality classes that govern the critical behavior (exponents, scaling functions) of coherence transitions across physical, cognitive, and social domains.

## EFT-First Summary
The Renormalization Flow of Coherence is a direct application of Wilsonian Renormalization Group (RG) methods to the Landau-Pirouette Functional, a Landau-Ginzburg-type theory for a complex order parameter ψ. By integrating out high-momentum modes, it derives β-functions for the model's couplings (proximity to criticality `a`, nonlinearity `b`, etc.). The analysis reveals a non-trivial Pirouette Wilson–Fisher fixed point in d=4-ε dimensions, which governs the universal critical exponents and scaling behavior of coherence phase transitions.

## Glossary Links
- See also: [Landau-Pirouette Functional](<#LANDAU_PIROUETTE_FUNCTIONAL>), [Universality Class](<#UNIVERSALITY_CLASS>), [Critical Exponents](<#CRITICAL_EXPONENTS>), [Temporal Pressure](<#TEMPORAL_PRESSURE>)