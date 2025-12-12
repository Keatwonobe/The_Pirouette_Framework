---
term: "RG Flow"
canonical_id: "RG_FLOW"
symbol: ""
aliases: [Renormalization Group Flow]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DYNA-WEAK-001_l_from_the_temporal_triad"]
---

---
term: RG Flow
canonical_id: RG_FLOW
symbol:
aliases: [Renormalization Group Flow, Running of Couplings]
parents: [DYNA-WEAK-001]
children: [MATH-YM-002, DYNA-COLOR-001, DYNA-Γ-004]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DYNA-WEAK-001_l_from_the_temporal_triad
      lines: "§4"
      snippet: |
        Run down with SM β-functions (one-loop, (\overline{\text{MS}})):
        [
        \mu\frac{d g_i}{d\mu}=\frac{b_i}{16\pi^2}g_i^3,\quad
        i\in{1,2,3},
        ]
  editors: [system-agent]
  review_log: []
triad:
  art: |
    A computational lens that adjusts its focus across energy scales, translating the pristine geometry of the coherence barrier into the complex patterns measured in a particle collider.
  law: |
    The evolution of coupling constants `α_i` with energy scale `μ` is determined by their beta functions, `μ dα_i/dμ = β_i(α)`. This evolution deterministically connects high-energy boundary conditions to low-energy observables.
  philosophy: |
    RG Flow is the essential bridge between the framework’s foundational axioms (e.g., frame stiffness) and empirical reality. It is not a source of new physics, but a necessary calculational tool that makes the physics at one scale falsifiable at another.
pirouette_definition: |
  The deterministic, scale-dependent evolution of physical parameters, primarily coupling constants, calculated using beta functions. Within Pirouette, it is the primary procedure for translating boundary conditions set at the coherence barrier (`μ_c`), such as the FRAME_STIFFNESS ratio, into falsifiable predictions at experimental energy scales like the Z-pole (`M_Z`).
operational_definition:
  units: The flow operates on dimensionless couplings as a function of energy scale (e.g., GeV).
  symbol_table:
    - name: α_i(μ)
      meaning: Fine-structure constant for gauge group `i` at energy scale `μ`.
      dimensions: dimensionless
      default_range: ~1/137 to ~1/10
    - name: μ
      meaning: Renormalization energy scale.
      dimensions: M L^2 T^-2
      default_range: M_Z to μ_c
    - name: b_i
      meaning: One-loop beta-function coefficient for gauge group `i`.
      dimensions: dimensionless
      default_range: contextual (e.g., -7 to 4.1 for SM)
  measurement:
    procedures:
      - name: Inferential via Multi-Scale Measurement
        outline: |
          1. Set boundary conditions for couplings (`α_i`) at a high energy scale (`μ_c`) based on a Pirouette model (e.g., from FRAME_STIFFNESS).
          2. Apply the RG Flow equations to predict the values of the couplings at a lower, accessible energy scale (`μ_exp`, e.g., `M_Z`).
          3. Measure the couplings or their derived observables (e.g., `sin^2(θ_W)`) at `μ_exp`.
          4. The validity of the high-scale model is tested by the consistency between the RG-evolved prediction and the measurement.
        expected_signals: [Logarithmic running of coupling constants, Predictive success of high-scale boundary conditions]
        pitfalls: [Threshold corrections from particle masses, Neglected higher-loop contributions, Existence of unmodeled particles affecting the running]
context_windows:
  - module: DYNA-WEAK-001_l_from_the_temporal_triad
    excerpt: |
      Workflow summary (deterministic):
      1. Choose (ρ_stiff) from Pirouette’s Resonance Atlas (XXP-BRIDGE-Γ-001).
      2. Fix (g(μ_c), g'(μ_c)) from (K_2, K_1).
      3. RG-run ({α_1,α_2}) to (M_Z).
      4. Compare (sin^2(θ_W)(M_Z)) with experiment.
      5. Iterate only within Pirouette-allowed stiffness priors (no tuning to data beyond module priors).
  - module: DYNA-WEAK-001_l_from_the_temporal_triad
    excerpt: |
      Angle inconsistency: No (ρ_stiff) within Pirouette priors can yield (sin^2(θ_W)(M_Z)) after RG running ⇒ triad-clock stiffness link falsified.
poetic_connections:
  motifs: [scale dependence, computational bridge, focusing lens, running constants]
  evocative_lines:
    - "all 'matching' happens here before standard RG running."
  association_matrix:
    - [ "COHERENCE_BARRIER", 0.9 ]
    - [ "FRAME_STIFFNESS", 0.8 ]
    - [ "WEINBERG_ANGLE", 0.7 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Renormalization Group Equations (β-functions)
      domain: QFT|SM
      mapping_kind: operational
      equation_hint: |
        \frac{1}{\alpha_i(\mu)}=\frac{1}{\alpha_i(\mu_c)}-\frac{b_i}{2\pi}\ln(\frac{\mu}{\mu_c})
      rationale: |
        The term and its operational procedure are identical to the standard implementation in Quantum Field Theory and the Standard Model. Pirouette does not redefine the flow, but rather provides a physical origin for its initial conditions at the coherence barrier.
      references:
        - title: An Introduction to Quantum Field Theory
          where: M. Peskin, D. Schroeder, Chapter 16
          date: 1995-10-01
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "The one-loop Standard Model beta functions are sufficient to connect the FRAME_STIFFNESS ratio at `μ_c` to the measured `sin^2(θ_W)` at `M_Z` to within 0.1% precision."
      domain: phenomenology
      falsifier: "A statistically significant discrepancy between the RG-evolved prediction and the measured value of `sin^2(θ_W)` that cannot be accounted for by known two-loop corrections or experimental uncertainty."
      status: under-test
      links: [DYNA-WEAK-001]
naming_notes:
  collisions: ["RG" is used for real-space renormalization in condensed matter and statistical mechanics.]
  disambiguation: |
    In Pirouette, RG Flow almost always refers to the momentum-space evolution of coupling constants in a quantum field theory context, from the COHERENCE_BARRIER down to experimental scales. It should not be confused with coarse-graining procedures unless explicitly stated.
crosslinks:
  near_synonyms: [RUNNING_OF_COUPLINGS]
  antonyms: [SCALE_INVARIANCE, CONFORMAL_FIXED_POINT]
  prerequisites: [COHERENCE_BARRIER, FRAME_STIFFNESS]
  downstream_effects: [WEINBERG_ANGLE, HIGGS_WIDTH]
license: CC-BY-SA-4.0
---

# RG Flow

## Canonical (Pirouette)
The deterministic, scale-dependent evolution of physical parameters, primarily coupling constants, calculated using beta functions. Within Pirouette, it is the primary procedure for translating boundary conditions set at the coherence barrier (`μ_c`), such as the FRAME_STIFFNESS ratio, into falsifiable predictions at experimental energy scales like the Z-pole (`M_Z`).

## EFT-First Summary
RG Flow is the application of the Standard Model's well-understood Renormalization Group Equations to evolve coupling constants from a high-energy scale to a low-energy one. In Pirouette, this procedure is critical for testing its predictions, such as deriving the Weinberg angle from a fundamental stiffness ratio defined at the coherence barrier, against precision measurements at the Z-pole. The framework relies on the standard QFT implementation of this process, as detailed in textbooks such as Peskin & Schroeder.

## Glossary Links
- See also: FRAME_STIFFNESS, COHERENCE_BARRIER, WEINBERG_ANGLE