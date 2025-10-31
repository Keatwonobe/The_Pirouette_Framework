---
term: "Substrate Action"
canonical_id: "SUBSTRATE_ACTION"
symbol: "S_time"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DYNA-004_substrate_action_of_time"]
---

---
term: Substrate Action
canonical_id: SUBSTRATE_ACTION
symbol: S_time
aliases: ["Temporal Action", "Pre-spatial Action"]
parents: [CORE-001, CORE-020]
children: [CORE-007, CORE-008, CORE-009]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DYNA-004_substrate_action_of_time
      lines: "§2"
      snippet: |
        S_time = ∫ dτ [ K_τ(Ki, T_a) − V_Γ(Γ) − W_int(Ki, Γ) ]
  editors: [GPT-4 (Pirouette Dictionary Agent)]
  review_log: []
triad:
  art: |
    Before space unfurls, the universe is a rhythm of pure potential. The Substrate Action is the law of this primal dance, a contest between the drive for harmonic coherence and the crushing cost of temporal pressure. Its balance choreographs the emergence of all physical reality.
  law: |
    A physical system's pre-spatial dynamics extremizes the Substrate Action, an integral over substrate time `τ` that maximizes a kinetic coherence term (`K_τ`) while minimizing a temporal pressure potential (`V_Γ`) and an interaction cost (`W_int`). All observable dynamics are consequences of this single principle.
  philosophy: |
    The Substrate Action is the framework's prime mover, replacing the standard QFT path integral over spacetime fields with a more fundamental principle rooted in a "time-first" substrate. It provides a unified origin for inertia, quantum fields, and gravitational curvature, which emerge as collective effects during spatialization rather than being posited axiomatically.
pirouette_definition: |
  The Substrate Action `S_time` is the functional that governs the dynamics of the pre-spatial substrate fields. It is defined as the integral over substrate time `τ` of a Lagrangian density composed of three terms: 1) `K_τ`, a kinetic term representing the quality-weighted rate of change of the coherence motif field `Ki`; 2) `V_Γ`, a potential energy term representing the cost of temporal pressure `Γ`; and 3) `W_int`, an interaction term coupling the local expression of `Ki` to the ambient pressure `Γ`. Physical histories are those that extremize this action.
operational_definition:
  units: J·s (SI) or dimensionless (natural units).
  symbol_table:
    - name: S_time
      meaning: Substrate Action
      dimensions: M·L²·T⁻¹
      default_range: contextual
    - name: τ
      meaning: Substrate time (pre-spatial temporal coordinate)
      dimensions: T
      default_range: contextual
    - name: Ki
      meaning: Coherence motif field (phase + modulus)
      dimensions: dimensionless
      default_range: contextual
    - name: Γ
      meaning: Temporal density/pressure functional
      dimensions: T⁻⁴
      default_range: contextual
    - name: T_a
      meaning: Adherence/coherence quality
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: K_τ
      meaning: Kinetic/coherence term in the Lagrangian density
      dimensions: M·L²·T⁻³
      default_range: contextual
    - name: V_Γ
      meaning: Pressure potential term in the Lagrangian density
      dimensions: M·L²·T⁻³
      default_range: contextual
    - name: W_int
      meaning: Interaction term in the Lagrangian density
      dimensions: M·L²·T⁻³
      default_range: contextual
  measurement:
    procedures:
      - name: Decoherence Floor Search
        outline: |
          Perform high-precision quantum state lifetime measurements (e.g., in trapped ion or superconducting qubit systems) after aggressive subtraction of all known environmental noise sources. A residual, platform-independent decoherence rate `1/T2_min` that correlates with local baryonic density gradients (sources of `Γ`) would constrain the term `ε · var(Γ)`.
        expected_signals: [A non-zero, universal decoherence floor]
        pitfalls: [Incomplete subtraction of conventional noise, mismodeling of local `Γ` sources]
      - name: Galactic Rotation Curve Analysis
        outline: |
          Fit galactic rotation curves using a model where the gravitational potential includes a MOND-like term proportional to `ε · ∇log Γ`, with `Γ` sourced by the observed baryonic matter distribution. This constrains the `ε`-scaled parameters in the `Γ`-to-curvature mapping.
        expected_signals: [MOND-like phenomenology without a dark matter particle]
        pitfalls: [Ambiguities in baryonic mass distribution, degeneracy with other model parameters]
      - name: Analogue Holonomy Test
        outline: |
          Construct a waveguide system (e.g., optical, Bose-Einstein condensate) whose propagation dynamics are analogous to the evolution of the `Ki` field. Measure the phase shift accumulated over paths that enclose a topological feature.
        expected_signals: [Observation of a 720° (4π) phase shift, characteristic of the spinor-like topology of `Ki`]
        pitfalls: [Imperfections in the physical analogue system, environmental noise]
context_windows:
  - module: DYNA-004_substrate_action_of_time
    excerpt: |
      S_time = ∫ dτ [ K_τ(Ki, T_a) − V_Γ(Γ) − W_int(Ki, Γ) ]

      Interpretation: systems extremize coherence minus pressure; Γ back-reacts through W_int to produce confinement/arena behavior (Gladiator feedback).
  - module: DYNA-004_substrate_action_of_time
    excerpt: |
      Push S_time forward: Define coordinates x^{μ} via Σ; Ki → complex section; Γ → scalar density; T_a → coherence weight. Expand around high-coherence backgrounds; keep quadratic fluctuations.

      Leading terms (schematic, in SM-CG):
      S_eff ≈ ∫ d^4x [ |D_{μ} Ki|^2 − m_eff^2 |Ki|^2 − (1/4) F_{μν} F^{μν}  + … ]
poetic_connections:
  motifs: ["coherence vs. pressure", "Gladiator feedback", "pre-spatial dynamics", "time-first"]
  evocative_lines:
    - "systems extremize coherence minus pressure"
    - "Gravity emerges from slow spatial variation of Γ as effective curvature"
  association_matrix:
    - [ "TEMPORAL_PRESSURE", 0.9 ]
    - [ "COHERENCE_MOTIF", 0.9 ]
    - [ "SPATIALIZATION_GAUGE", 0.7 ]
    - [ "SUBSTRATE_DEVIATION_SCALE", 0.6 ]
formal_mappings:
  candidates:
    - target: Abelian Higgs / Ginzburg-Landau Action
      domain: QFT
      mapping_kind: mathematical
      equation_hint: |
        S_eff ≈ ∫ d^4x [ |(∂_{μ} − iqA_{μ}) φ|^2 − m^2 |φ|^2 − λ|φ|^4 − (1/4) F_{μν} F^{μν} ]
      justification: |
        In the high-coherence, post-spatialization limit (SM-CG), `S_time` expands to an effective action `S_eff` where the coherence motif `Ki` behaves as a complex scalar field (like the Higgs `φ`) and its phase gradient defines an emergent U(1) gauge field `A_{μ}`. This is the mathematical structure of the Abelian Higgs model, which describes superconductivity and spontaneous symmetry breaking.
      references: []
      confidence: 0.9
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "All physical systems exhibit a minimum, universal decoherence rate `1/T2_min ∝ ε · var(Γ)` after all conventional environmental noise is shielded or subtracted."
      domain: experiment
      falsifier: "Precision experiments on diverse quantum platforms (e.g., NV centers, trapped ions) converge to zero decoherence after noise subtraction, or the residual floor is platform-dependent."
      status: proposed
      links: [DYNA-004]
    - statement: "Galactic rotation curves can be fully explained by a MOND-like acceleration term `a_M ∝ ε · ∇log Γ` sourced by baryonic matter, without requiring particle dark matter."
      domain: phenomenology
      falsifier: "The functional form of the required modification to gravity does not match `∇log Γ` for any reasonable `Γ` sourced by baryons, or direct-detection experiments find particle dark matter."
      status: proposed
      links: [DYNA-004, CORE-008]
    - statement: "Analogue systems designed to mimic the `Ki` field topology will exhibit 4π-periodic (720°) holonomies."
      domain: experiment
      falsifier: "Tabletop experiments using optical waveguides or BECs designed to emulate `Ki` dynamics show only 2π or other periodicities in their phase behavior."
      status: proposed
      links: [DYNA-004]
naming_notes:
  collisions: [The symbol `S` is the standard notation for an action in physics.]
  disambiguation: |
    `S_time` refers specifically to the fundamental, pre-spatial action on the substrate. This must be distinguished from `S_eff`, the effective action that emerges in spacetime after the spatialization gauge `Σ` is chosen. `S_eff` is the object that recovers the Standard Model Lagrangian in the `ε → 0` limit.
crosslinks:
  near_synonyms: []
  antonyms: ["EFFECTIVE_SPACETIME_ACTION"]
  prerequisites: ["COHERENCE_MOTIF", "TEMPORAL_PRESSURE"]
  downstream_effects: ["SPACETIME_METRIC", "SM_GAUGE_FIELDS", "ANOMALOUS_MAGNETIC_MOMENT_CORRECTION"]
license: CC-BY-SA-4.0
---

# Substrate Action

## Canonical (Pirouette)
The Substrate Action `S_time` is the functional that governs the dynamics of the pre-spatial substrate fields. It is defined as the integral over substrate time `τ` of a Lagrangian density composed of three terms: 1) `K_τ`, a kinetic term representing the quality-weighted rate of change of the coherence motif field `Ki`; 2) `V_Γ`, a potential energy term representing the cost of temporal pressure `Γ`; and 3) `W_int`, an interaction term coupling the local expression of `Ki` to the ambient pressure `Γ`. Physical histories are those that extremize this action.

## EFT-First Summary
The Substrate Action is a pre-geometric functional that, upon spatialization, yields an effective field theory action `S_eff`. In the high-coherence limit, `S_eff` takes the form of an Abelian Higgs (Ginzburg-Landau) model. The coherence motif field `Ki` maps to a complex scalar, its modulus acquiring a VEV and its phase gradient becoming a U(1) gauge field. Standard Model fields and gravitational dynamics emerge from its quadratic fluctuations and hydrodynamic limit, respectively. Beyond-SM effects are parameterized by a small deviation parameter `ε`.

## Glossary Links
- See also: [Substrate](<placeholder>), [Coherence Motif (Ki)](<placeholder>), [Temporal Pressure (Γ)](<placeholder>), [Spatialization](<placeholder>)