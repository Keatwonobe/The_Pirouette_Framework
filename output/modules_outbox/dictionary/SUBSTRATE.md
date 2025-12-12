---
term: "Substrate"
canonical_id: "SUBSTRATE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DYNA-004_substrate_action_of_time"]
---

---
term: Substrate
canonical_id: SUBSTRATE
symbol: 
aliases: [pre-spatial medium, time-first substrate]
parents: [DYNA-004]
children: [CORE-007, CORE-008, CORE-009]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DYNA-004_substrate_action_of_time
      lines: "summary"
      snippet: |
        Minimal dynamics for a time-first substrate whose SM-CG limit reproduces existing results.
  editors: [writing-agent-alpha]
  review_log: []
triad:
  art: |
    Before the stage of space was built, there was only the rhythm of the play. The Substrate is this primal rhythm, a deep temporal ocean where currents of coherence contend with waves of pressure, and from whose surface our spatial world crystallizes.
  law: |
    All dynamics on the Substrate extremize the time-integral of local coherence quality minus a convex temporal pressure cost (S_time = ∫ dτ [K_τ − V_Γ]), where pressure back-reacts to confine and structure the coherence fields.
  philosophy: |
    The Substrate serves as the Framework's foundational answer to "what precedes spacetime?" It replaces a static, geometric background with a dynamic, time-first medium, positing that space and its physical laws are emergent, coarse-grained properties of underlying temporal processes.
pirouette_definition: |
  The Substrate is the fundamental, pre-spatial, and time-first dynamical medium of the Pirouette Framework. Its state is defined by fields of coherence motif (Ki), temporal pressure (Γ), and coherence adherence (T_a). Its dynamics are governed by the temporal action `S_time = ∫ dτ [ K_τ(Ki, T_a) − V_Γ(Γ) − W_int(Ki, Γ) ]`, which dictates that systems evolve to maximize coherence against a pressure-like cost. Spacetime and its associated physics emerge as the effective description of this system in a high-coherence, slowly-varying limit (the SM-CG gauge).
operational_definition:
  units: Not a quantity; a foundational medium. Its properties are described by fields with specific units.
  symbol_table:
    - name: Ki(·)
      meaning: Coherence motif field (phase and modulus) on the substrate.
      dimensions: Contextual; phase is dimensionless.
      default_range: Contextual.
    - name: Γ(·)
      meaning: Temporal density/pressure functional from superposed rhythms.
      dimensions: T⁻¹ (inverse time or frequency).
      default_range: > 0.
    - name: T_a(·)
      meaning: Adherence/coherence quality; a weighting factor.
      dimensions: Dimensionless.
      default_range: [0, 1].
    - name: ε
      meaning: Substrate deviation scale; dimensionless parameter controlling the magnitude of beyond-SM effects.
      dimensions: Dimensionless.
      default_range: << 1.
  measurement:
    procedures:
      - name: Decoherence Floor Detection
        outline: |
          In a maximally isolated quantum system (e.g., trapped ion, superconducting qubit), measure decoherence rates (1/T2) after aggressively subtracting all known environmental noise sources. A residual, persistent, and universal decoherence rate would be evidence for the substrate floor. The rate should drift with changes in ambient gravitational potential, which correlates with Γ gradients.
        expected_signals: [A non-zero minimum 1/T2 rate, 1/T2_min ∝ ε · var(Γ), slow drifts correlated with lab position in gravitational field.]
        pitfalls: [Mistaking instrumental noise floors for a fundamental effect, incomplete noise subtraction, environmental Γ fluctuations being too small to detect.]
      - name: Galactic Rotation Curve Analysis
        outline: |
          Model galactic rotation curves using only baryonic matter distributions and General Relativity, plus a single additional acceleration term derived from the substrate: a_mond ∝ ε · ∇log Γ. A successful fit across a wide range of galaxy types with a single universal constant (scaled by ε) would support the substrate hypothesis.
        expected_signals: [Consistent fits to rotation curves without a dark matter particle halo, recovery of the Baryonic Tully-Fisher relation.]
        pitfalls: [Degeneracies with baryonic physics uncertainties (e.g., stellar mass-to-light ratios), circular reasoning if ε is tuned per-galaxy.]
context_windows:
  - module: DYNA-004_substrate_action_of_time
    excerpt: |
      The minimal substrate action is S_time = ∫ dτ [ K_τ(Ki, T_a) − V_Γ(Γ) − W_int(Ki, Γ) ]. This can be interpreted as systems extremizing coherence minus pressure. The interaction term W_int allows Γ to back-react, producing confinement or arena-like behavior via "Gladiator feedback."
  - module: DYNA-004_substrate_action_of_time
    excerpt: |
      Spatialization is not fundamental; it is a choice of gauge (Σ). Pushing the S_time action forward into the SM-CG gauge, one recovers the effective action S_eff ≈ ∫ d^4x [ |D_{μ} Ki|^2 − m_eff^2 |Ki|^2 + … ]. Gravity emerges from slow spatial variation of Γ as effective curvature. Setting the substrate deviation scale ε to zero recovers strict QFT/SM.
poetic_connections:
  motifs: [time-first, emergent space, coherence vs. pressure, Gladiator feedback]
  evocative_lines:
    - "systems extremize coherence minus pressure"
    - "Gravity emerges from slow spatial variation of Γ as effective curvature."
  association_matrix:
    - [ "COHERENCE_MOTIF", 0.9 ]
    - [ "TEMPORAL_PRESSURE", 0.9 ]
    - [ "SPATIALIZATION", 0.7 ]
formal_mappings:
  candidates:
    - target: Spacetime manifold with metric g_μν
      domain: GR
      mapping_kind: conceptual
      equation_hint: |
        g_μν_eff ≈ η_μν + h(Γ, ∂Γ)
      justification: |
        The substrate is the pre-geometric foundation from which the spacetime manifold of General Relativity emerges. The effective metric is a function of the underlying temporal pressure field Γ and its variations in the hydrodynamic limit (see CORE-008).
      references:
        - title: Substrate Action of Time
          where: DYNA-004, §3
          date: 2025-10-18
      confidence: 0.8
    - target: Quantum Field Theory (QFT) Lagrangian
      domain: SM
      mapping_kind: mathematical
      equation_hint: |
        S_time → S_eff ≈ ∫ d^4x [ |D_{μ} Ki|^2 − m_eff^2 |Ki|^2 − (1/4) F_{μν} F^{μν} + … ]
      justification: |
        In the SM-CG (Standard Model Coarse-Grained) limit, the substrate's temporal action S_time can be expanded. The leading quadratic terms reproduce the form of a standard QFT action for a complex scalar field (Ki) coupled to a gauge field (A_μ), demonstrating how SM field theory emerges from substrate dynamics.
      references:
        - title: Substrate Action of Time
          where: DYNA-004, §3
          date: 2025-10-18
      confidence: 0.9
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "A universal, non-zero decoherence floor, scaling as 1/T2_min ∝ ε · var(Γ), exists for all quantum systems after all other noise sources are eliminated."
      domain: experiment
      falsifier: "Demonstration that decoherence in an ideal, isolated system can be suppressed to an arbitrarily low level, below any predicted universal floor."
      status: proposed
      links: [DYNA-004]
    - statement: "Galactic rotation curves are fully explained by baryonic matter plus a single, universal MOND-like term derived from substrate pressure gradients (a ∝ ε · ∇log Γ)."
      domain: phenomenology
      falsifier: "Direct detection of a non-baryonic dark matter particle, or failure of the substrate model to fit a broad sample of galactic data with one universal parameter."
      status: proposed
      links: [DYNA-004]
naming_notes:
  collisions: [Substrate (condensed matter), Substrate (biochemistry)]
  disambiguation: |
    In Pirouette, "Substrate" refers to the fundamental, pre-spatial medium, not a physical material layer upon which a process occurs (as in condensed matter) or a molecule acted upon by an enzyme (as in biochemistry). It is the ontological ground floor of reality.
crosslinks:
  near_synonyms: []
  antonyms: [SPACETIME_MANIFOLD]
  prerequisites: [TEMPORAL_PRESSURE, COHERENCE_MOTIF]
  downstream_effects: [SPATIALIZATION, GRAVITY_EMERGENCE, MOND_ANALOGY]
license: CC-BY-SA-4.0
---

# Substrate

## Canonical (Pirouette)
The Substrate is the fundamental, pre-spatial, and time-first dynamical medium of the Pirouette Framework. Its state is defined by fields of coherence motif (Ki), temporal pressure (Γ), and coherence adherence (T_a). Its dynamics are governed by the temporal action `S_time = ∫ dτ [ K_τ(Ki, T_a) − V_Γ(Γ) − W_int(Ki, Γ) ]`, which dictates that systems evolve to maximize coherence against a pressure-like cost. Spacetime and its associated physics emerge as the effective description of this system in a high-coherence, slowly-varying limit (the SM-CG gauge).

## EFT-First Summary
The Substrate is a pre-geometric medium whose effective field theory, in the high-coherence limit, reproduces the Lagrangian of the Standard Model and the geometry of General Relativity. The substrate's fundamental fields (Ki, Γ) manifest as familiar QFT fields after a gauge choice for spatialization. For example, the substrate action `S_time` expands to the effective action `S_eff ≈ ∫ d^4x [ |D_{μ} Ki|^2 - ... ]`, directly mapping substrate dynamics to a standard QFT kinetic term. All beyond-SM effects, such as a MOND-like acceleration and a universal decoherence floor, are suppressed by a small parameter `ε`.

## Glossary Links
- See also: [COHERENCE_MOTIF](link), [TEMPORAL_PRESSURE](link), [SPATIALIZATION](link)