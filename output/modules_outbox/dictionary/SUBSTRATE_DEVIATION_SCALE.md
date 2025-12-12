---
term: "Substrate Deviation Scale"
canonical_id: "SUBSTRATE_DEVIATION_SCALE"
symbol: "ε"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DYNA-004_substrate_action_of_time"]
---

---
term: Substrate Deviation Scale
canonical_id: SUBSTRATE_DEVIATION_SCALE
symbol: ε
aliases: []
parents: [DYNA-004]
children: [CORE-007, CORE-008, CORE-009]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DYNA-004
      lines: "§4"
      snippet: |
        Introduce ε as the substrate deviation scale. All beyond-SM effects scale with ε:
        - a_e = α/2π + O(ε) (keeps CORE-009 result as leading order).
        - Decoherence floor: 1/T2_min ∝ ε · var(Γ).
        - Galactic rotation: MOND-like term ∝ ε · ∇log Γ.
        Set ε → 0 to recover strict SM/QFT.
  editors: [Agent (GPT-4)]
  review_log: []
triad:
  art: |
    The whisper of the substrate through the veil of spacetime. It is the measure of the sea on which our physics floats, quantifying the slight tremor that reveals the world is not made of perfect, crystalline math.
  law: |
    All physical observables O can be expanded as O = O_SM + c₁ε + c₂ε² + ... where O_SM is the Standard Model prediction. Any confirmed, non-zero beyond-Standard-Model effect originating from the substrate provides a measurement of a coefficient cᵢ and thus a constraint on ε.
  philosophy: |
    ε provides a single, unifying parameter for all beyond-Standard-Model effects originating from the substrate, replacing a collection of ad-hoc corrections. It systematizes the search for new physics by linking disparate phenomena (e.g., decoherence, dark matter phenomenology) under one theoretical dial. Setting ε → 0 must recover the Standard Model, making it the "off-switch" for the substrate's influence.
pirouette_definition: |
  A fundamental, dimensionless small parameter that quantifies the magnitude of all physical effects arising from the Pirouette substrate that are not captured by the Standard Model Coarse-Grained (SM-CG) limit. It serves as a bookkeeping tool in perturbative expansions around the SM, where all beyond-SM terms originating from substrate dynamics are proportional to a positive power of ε. The SM-CG limit is formally recovered by taking ε → 0.
operational_definition:
  units: dimensionless
  symbol_table:
    - name: ε
      meaning: Substrate Deviation Scale
      dimensions: dimensionless
      default_range: "0 < ε << 1. Constrained by observation."
  measurement:
    procedures:
      - name: Multi-Modal Anomaly Correlation
        outline: |
          1. Identify multiple, physically distinct phenomena predicted to have a leading-order dependence on ε (e.g., a universal decoherence floor, galactic rotation curve anomalies).
          2. Perform high-precision measurements of these phenomena, carefully subtracting all known SM and environmental backgrounds.
          3. Using the scaling laws derived from Pirouette (e.g., `1/T2_min ∝ ε·var(Γ)`, `a_MOND ∝ ε·c²|∇logΓ|`), calculate the implied value of ε from each measurement.
          4. A consistent value of ε across all modalities would support the framework; inconsistent values would falsify its claim of a single deviation scale.
        expected_signals: [A statistically significant, non-zero value for ε that is consistent across independent experimental domains (e.g., quantum decoherence experiments and astrophysical observations).]
        pitfalls: [Misattributing conventional noise sources to a fundamental decoherence floor. Failure to correctly model the coefficients that multiply ε in the scaling laws. Confounding BSM effects from non-substrate origins (e.g., new particles) with ε-scaled effects.]
context_windows:
  - module: DYNA-004
    excerpt: |
      Introduce ε as the substrate deviation scale. All beyond-SM effects scale with ε... Decoherence floor: 1/T2_min ∝ ε · var(Γ). Galactic rotation: MOND-like term ∝ ε · ∇log Γ. Set ε → 0 to recover strict SM/QFT.
  - module: DYNA-004
    excerpt: |
      Near-term signatures (falsifiable, light-lift): Universality of a tiny decoherence floor across platforms after aggressive noise subtraction; drift with ambient Γ-gradients. Rotation-curve fits from ∇log Γ sourced by baryons (no new particles) with one ε-scaled term.
poetic_connections:
  motifs: [leakage, remainder, substrate-echo, deviation, imperfection]
  evocative_lines:
    - "Set ε → 0 to recover strict SM/QFT."
    - "Universality of a tiny decoherence floor across platforms..."
  association_matrix:
    - [ "DECOHERENCE_FLOOR", 0.9 ]
    - [ "TEMPORAL_PRESSURE", 0.7 ]
    - [ "SM-CG_LIMIT", 0.9 ] # as an inverse relationship
    - [ "COHERENCE_MOTIF_FIELD", 0.5 ]
formal_mappings:
  candidates:
    - target: 1/Λ
      domain: EFT
      mapping_kind: conceptual
      equation_hint: |
        L_eff = L_SM + Σ (c_i/Λ^(d_i-4)) O_i  vs.  O = O_SM + c₁ε + ...
      justification: |
        Like the inverse of a high-energy cutoff scale Λ in an Effective Field Theory, ε parameterizes the strength of corrections to a baseline theory (the SM). It controls the magnitude of higher-order effects that are suppressed. However, ε is dimensionless, whereas Λ has dimensions of energy, so the mapping is not a direct mathematical identity.
      references: []
      confidence: 0.7
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "All substrate-derived BSM phenomena are scaled by a single, universal parameter ε."
      domain: phenomenology
      falsifier: "Experimental measurements of two or more distinct ε-dependent phenomena (e.g., the decoherence floor and MOND-like acceleration) yield inconsistent values for ε, beyond model and measurement uncertainty."
      status: proposed
      links: [DYNA-004, CORE-008, CORE-009]
    - statement: "The value of ε is non-zero."
      domain: experiment
      falsifier: "Persistent null results in dedicated searches for predicted ε-dependent effects, pushing the experimental upper bound on ε to be operationally indistinguishable from zero."
      status: proposed
      links: [DYNA-004]
naming_notes:
  collisions: [permittivity, strain, small parameter in perturbation theory]
  disambiguation: |
    Within the Pirouette Framework, ε refers exclusively to the Substrate Deviation Scale. It is always a dimensionless parameter appearing in expansions around the SM-CG limit. It should not be confused with the Levi-Civita symbol ε_ijk.
crosslinks:
  near_synonyms: []
  antonyms: [SM-CG_LIMIT]
  prerequisites: [SUBSTRATE, SM-CG_LIMIT]
  downstream_effects: [DECOHERENCE_FLOOR, MOND-LIKE_ACCELERATION]
license: CC-BY-SA-4.0
---

# Substrate Deviation Scale

## Canonical (Pirouette)
A fundamental, dimensionless small parameter that quantifies the magnitude of all physical effects arising from the Pirouette substrate that are not captured by the Standard Model Coarse-Grained (SM-CG) limit. It serves as a bookkeeping tool in perturbative expansions around the SM, where all beyond-SM terms originating from substrate dynamics are proportional to a positive power of ε. The SM-CG limit is formally recovered by taking ε → 0.

## EFT-First Summary
The Substrate Deviation Scale ε functions conceptually like the inverse of a high-energy cutoff scale (1/Λ) in an Effective Field Theory. It is a dimensionless parameter that controls the magnitude of all higher-order operators added to the Standard Model Lagrangian that originate from the substrate dynamics. All predicted beyond-Standard-Model effects in this framework are suppressed by at least one power of ε.

## Glossary Links
- See also: Substrate, SM-CG Limit, Decoherence Floor