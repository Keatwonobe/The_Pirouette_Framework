---
term: "Spatialization"
canonical_id: "SPATIALIZATION"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DYNA-004_substrate_action_of_time"]
---

---
term: Spatialization
canonical_id: SPATIALIZATION
symbol: Σ-pushforward
aliases: [SM-CG projection, Spacetime Emergence]
parents: [DYNA-004]
children: [CORE-007, CORE-008, CORE-009]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DYNA-004_substrate_action_of_time
      lines: "L20-L22"
      snippet: |
        §3 · Spatialization (how SM appears)
        Pick Σ (the SM-CG gauge). Push S_time forward:
        - Define coordinates x^{μ} via Σ; Ki → complex section; Γ → scalar density; T_a → coherence weight.
  editors: [ai-agent]
  review_log: []
triad:
  art: |
    Spacetime is the measured shadow of a purely temporal dance. The universe we perceive in length, width, and height is a stable projection, an organizational map drawn from the substrate's deeper rhythm.
  law: |
    The effective action for Standard Model fields is recovered by expanding the substrate action `S_time` around a high-coherence background under a specific gauge choice `Σ`, retaining quadratic fluctuations. All beyond-SM effects are suppressed by a small-deviation parameter `ε`, and vanish as `ε → 0`.
  philosophy: |
    Spatialization is the core generative principle bridging the substrate's time-first dynamics to observed relativistic physics. It asserts that spacetime is not fundamental but an emergent, effective description necessary for coherent, macroscopic observers. This explains the origin of locality and Lorentz invariance rather than assuming them.
pirouette_definition: |
  The formal procedure of projecting the substrate dynamics, described by the time-native action `S_time`, onto a 4D spacetime manifold. The process is enacted by selecting a Standard Model-Coarse Graining (SM-CG) gauge, denoted `Σ`. This gauge choice defines spacetime coordinates `x^μ` and provides a dictionary to map the substrate fields (`Ki`, `Γ`, `T_a`) to effective spacetime fields (a complex scalar, a scalar density, and a coherence weight, respectively). The procedure recovers the Lagrangian of the Standard Model in the low-deviation (`ε → 0`) limit.
operational_definition:
  units: N/A (mapping procedure)
  symbol_table:
    - name: S_time
      meaning: Substrate Action of Time
      dimensions: Action (M·L²·T⁻¹)
      default_range: contextual
    - name: Σ
      meaning: SM-CG gauge choice
      dimensions: dimensionless (operator)
      default_range: N/A
    - name: x^μ
      meaning: Emergent spacetime coordinates
      dimensions: Length
      default_range: contextual
    - name: ε
      meaning: Substrate deviation scale
      dimensions: dimensionless
      default_range: small, positive
  measurement:
    procedures:
      - name: Theoretical Derivation
        outline: |
          1. Start with the substrate action `S_time = ∫ dτ [ K_τ − V_Γ − W_int ]`.
          2. Select a gauge `Σ` that defines a mapping from the substrate's parameter space to spacetime coordinates `x^μ`.
          3. Push the integration measure and fields forward: `dτ → d^4x`, `Ki(τ) → Ki(x)`, `Γ(τ) → Γ(x)`.
          4. Expand the resulting action `S_eff` around a high-coherence background solution, keeping terms up to second order in fluctuations.
          5. Identify the resulting terms with the kinetic, mass, and gauge terms of the Standard Model and metric dynamics.
        expected_signals: [A Klein-Gordon-like term `|D_μ Ki|^2`, a Maxwell-like term `F_μν F^μν`, and a Ricci-scalar-like term from variations in `Γ(x)`.]
        pitfalls: [Assuming `Σ` is unique or physical (it is a gauge choice), performing the expansion in a low-coherence regime where it is not valid.]
context_windows:
  - module: DYNA-004_substrate_action_of_time
    excerpt: |
      §3 · Spatialization (how SM appears)
      Pick Σ (the SM-CG gauge). Push S_time forward:
      - Define coordinates x^{μ} via Σ; Ki → complex section; Γ → scalar density; T_a → coherence weight.
      - Expand around high-coherence backgrounds; keep quadratic fluctuations.
      Leading terms (schematic, in SM-CG):
      S_eff ≈ ∫ d^4x [ |D_{μ} Ki|^2 − m_eff^2 |Ki|^2 − (1/4) F_{μν} F^{μν}  + … ]
  - module: DYNA-004_substrate_action_of_time
    excerpt: |
      Gravity emerges from slow spatial variation of Γ as effective curvature in the hydrodynamic limit (CORE-008 path).
      ...
      Introduce ε as the substrate deviation scale. All beyond-SM effects scale with ε... Set ε → 0 to recover strict SM/QFT.
poetic_connections:
  motifs: [emergence, projection, coarse-graining, shadow-play, hydrodynamics]
  evocative_lines:
    - "Pick Σ (the SM-CG gauge). Push S_time forward."
    - "Gravity emerges from slow spatial variation of Γ."
  association_matrix:
    - [ "SUBSTRATE_ACTION_OF_TIME", 0.9 ]
    - [ "TEMPORAL_PRESSURE", 0.7 ]
    - [ "COHERENCE_MOTIF", 0.7 ]
    - [ "STANDARD_MODEL", 0.8 ]
formal_mappings:
  candidates:
    - target: Standard Model Lagrangian (`L_SM`)
      domain: QFT
      mapping_kind: mathematical
      equation_hint: |
        S_time  --[Σ-pushforward]-->  S_eff ≈ ∫ d^4x L_SM + O(ε)
      justification: |
        Spatialization is a specific coarse-graining procedure that generates the kinetic and interaction terms of QFT from a more fundamental, pre-geometric action. The mapping is explicitly constructive, identifying the SM Lagrangian as the leading-order effective description of substrate fluctuations.
      references:
        - title: Substrate Action of Time
          where: DYNA-004 §3
          date: 2025-10-18
      confidence: 0.95
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The MOND-like acceleration scale in galactic rotation curves is sourced by baryon-induced gradients in the temporal pressure `Γ` and scales with `ε`."
      domain: phenomenology
      falsifier: "Observation of galactic dynamics that cannot be fit by `∇log Γ` sourced only by baryons, requiring a new particle (dark matter)."
      status: proposed
      links: [DYNA-004]
    - statement: "All physical systems exhibit a minimum, universal decoherence rate proportional to `ε` and the local variance of `Γ`."
      domain: experiment
      falsifier: "Sufficiently isolated quantum systems showing no evidence of a decoherence floor after all known environmental noise sources are eliminated."
      status: proposed
      links: [DYNA-004]
naming_notes:
  collisions: [Audio Engineering (3D sound spatialization)]
  disambiguation: |
    In Pirouette, Spatialization is not the act of placing an object in pre-existing space. It is the formal, mathematical procedure by which the very concepts of space, distance, and locality are generated from a non-spatial substrate.
crosslinks:
  near_synonyms: []
  antonyms: [SUBSTRATE_NATIVITY]
  prerequisites: [SUBSTRATE_ACTION_OF_TIME]
  downstream_effects: [STANDARD_MODEL, EFFECTIVE_GRAVITY, MOND_ANALOGUE, DECOHERENCE_FLOOR]
license: CC-BY-SA-4.0
---

# Spatialization

## Canonical (Pirouette)
The formal procedure of projecting the substrate dynamics, described by the time-native action `S_time`, onto a 4D spacetime manifold. The process is enacted by selecting a Standard Model-Coarse Graining (SM-CG) gauge, denoted `Σ`. This gauge choice defines spacetime coordinates `x^μ` and provides a dictionary to map the substrate fields (`Ki`, `Γ`, `T_a`) to effective spacetime fields (a complex scalar, a scalar density, and a coherence weight, respectively). The procedure recovers the Lagrangian of the Standard Model in the low-deviation (`ε → 0`) limit.

## EFT-First Summary
Spatialization is the mechanism that generates the Standard Model (SM) Lagrangian as a low-energy, effective field theory. By expanding the fundamental substrate action around a stable, high-coherence background, the process yields the familiar kinetic (`|D_μ φ|^2`), mass (`m^2|φ|^2`), and gauge (`F_μν F^μν`) terms of quantum field theory. This procedure formally identifies the SM as the leading-order description of the substrate's dynamics, with all beyond-SM physics suppressed by a small parameter `ε`.

## Glossary Links
- See also: SUBSTRATE_ACTION_OF_TIME, STANDARD_MODEL, EFFECTIVE_GRAVITY