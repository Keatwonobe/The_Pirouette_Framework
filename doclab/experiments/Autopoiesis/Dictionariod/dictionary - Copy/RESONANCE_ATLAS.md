---
term: "Resonance Atlas"
canonical_id: "RESONANCE_ATLAS"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-YM-002_running_barrier_matching"]
---

---
term: Resonance Atlas
canonical_id: RESONANCE_ATLAS
symbol: 
aliases: [stiffness dictionary, stiffness priors catalog]
parents: [XXP-BRIDGE-Γ-001]
children: [MATH-YM-002, DYNA-COLOR-001]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-YM-002_running_barrier_matching
      lines: "L#51-L#55"
      snippet: |
        where (K_i) come from Pirouette’s Resonance Atlas and (\Delta_i=\mathcal{O}(1/16\pi^2)) are finite, scheme-dependent but observable-independent matching constants.
  editors: [GPT-4]
  review_log: []
triad:
  art: |
    A luthier's reference book, detailing the specific woods and tensions that produce harmonious, stable tones. It maps the resonant properties of the underlying Γ-field to the required stiffness of the gauge frames built upon it.
  law: |
    The Atlas provides a discrete or continuous set of allowed prior values for the stiffness couplings {K₁, K₂, K₃}. Any viable Pirouette model must select a {Kᵢ} set from this Atlas which, after RG evolution from the coherence barrier μ_c, reproduces low-energy gauge couplings within experimental error.
  philosophy: |
    The Atlas replaces arbitrary high-scale boundary conditions with a physically motivated, constrained set of priors derived from Γ-field microphysics. It enforces internal consistency, turning gauge unification from a search into a look-up, making the framework predictive and falsifiable.
pirouette_definition: |
  The Pirouette framework's canonical catalog of allowed prior values for the dimensionless frame-stiffness couplings (K₁, K₂, K₃). These values are derived from the resonant mode structure of the underlying Γ-field at the Pirouette scale (Λ_Pirouette), as specified in XXP-BRIDGE-Γ-001. The Atlas provides the fundamental boundary conditions for gauge coupling renormalization group evolution from the coherence barrier (μ_c).
operational_definition:
  units: Dimensionless
  symbol_table:
    - name: Kᵢ
      meaning: Frame-stiffness coupling for the i-th gauge group (i=1,2,3 for U(1)Y, SU(2)L, SU(3)c).
      dimensions: dimensionless
      default_range: ~20–100
  measurement:
    procedures:
      - name: Indirect Inference via Barrier Matching
        outline: |
          1. Select a candidate set of {K₁, K₂, K₃} from the Atlas.
          2. At the coherence barrier μ_c, set the initial gauge couplings via the matching relation 1/gᵢ²(μ_c) = Kᵢ + Δᵢ.
          3. Evolve these couplings down to the Z-pole mass (M_Z) using 2-loop Standard Model RGEs.
          4. Compare the resulting values of {α_EM(M_Z), sin²θ_W(M_Z), α_s(M_Z)} with their experimentally measured values.
        expected_signals: [A successful {Kᵢ} set reproduces all three low-energy observables simultaneously to within experimental and theoretical precision.]
        pitfalls: [Mismatch due to incorrect Δᵢ (finite matching constants), higher-loop uncertainties in RGE running, experimental uncertainty in low-energy inputs (e.g., top mass).]
context_windows:
  - module: MATH-YM-002_running_barrier_matching
    excerpt: |
      At μ=μ_c, identify couplings with stiffnesses and add finite counterterms that encode time-first microphysics while preserving gauge symmetry: [1/gᵢ²(μ_c) = Kᵢ + Δᵢ]. Here, Kᵢ come from Pirouette’s Resonance Atlas and Δᵢ are finite, scheme-dependent but observable-independent matching constants.
  - module: MATH-YM-002_running_barrier_matching
    excerpt: |
      The practical pipeline begins with selecting stiffness priors (K₁,K₂,K₃) from XXP-BRIDGE-Γ-001. One then iterates within these Pirouette priors only, with no free, ad-hoc tuning. A failure to match experimental data indicates a fundamental tension with the stiffness dictionary.
poetic_connections:
  motifs: [catalog, resonance, priors, tuning fork, dictionary, lookup table]
  evocative_lines:
    - "the stiffnesses are the tension of the strings."
    - "failure to match indicates tension with the stiffness dictionary."
  association_matrix:
    - [ "FRAME_STIFFNESS", 0.9 ]
    - [ "COHERENCE_BARRIER", 0.7 ]
    - [ "TEMPORAL_PRESSURE", 0.5 ]
formal_mappings:
  candidates:
    - target: GUT-scale boundary conditions (e.g., α_i = α_GUT at M_GUT)
      domain: EFT
      mapping_kind: conceptual
      equation_hint: |
        Pirouette: 1/gᵢ²(μ_c) = Kᵢ vs. GUT: g₁(M_GUT) = g₂(M_GUT) = g₃(M_GUT)
      justification: |
        Both the Resonance Atlas and GUT boundary conditions provide the high-scale starting values for the RGE evolution of gauge couplings. However, the Atlas does not require the couplings to unify to a single value; instead, it provides a constrained set of three distinct priors {Kᵢ} derived from underlying Γ-field microphysics.
      references:
        - title: A simple introduction to grand unification
          where: arXiv:0904.1556
          date: 2009-04-10
      confidence: 0.7
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The set of stiffness priors {Kᵢ} contained in the Resonance Atlas is sufficient to reproduce the measured low-energy gauge couplings {α_EM(M_Z), sin²θ_W(M_Z), α_s(M_Z)} via RGE running from the coherence barrier μ_c."
      domain: phenomenology
      falsifier: "If no combination of {Kᵢ} from the Atlas, for any allowed finite matching Δᵢ, can successfully reproduce the experimental values at the Z-pole, the Atlas is falsified."
      status: proposed
      links: [MATH-YM-002, XXP-BRIDGE-Γ-001]
naming_notes:
  collisions: []
  disambiguation: |
    The Resonance Atlas is not a catalog of particle resonances like those in the Particle Data Group (PDG) tables. It catalogs the allowed resonant *stiffnesses* of spacetime frames, which are precursors to gauge couplings, not a list of massive states.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [FRAME_STIFFNESS, COHERENCE_BARRIER, TEMPORAL_PRESSURE]
  downstream_effects: [WEINBERG_ANGLE, STRONG_COUPLING_CONSTANT, QCD_SCALE]
license: CC-BY-SA-4.0
---

# Resonance Atlas

## Canonical (Pirouette)
The Pirouette framework's canonical catalog of allowed prior values for the dimensionless frame-stiffness couplings (K₁, K₂, K₃). These values are derived from the resonant mode structure of the underlying Γ-field at the Pirouette scale (Λ_Pirouette), as specified in XXP-BRIDGE-Γ-001. The Atlas provides the fundamental boundary conditions for gauge coupling renormalization group evolution from the coherence barrier (μ_c).

## EFT-First Summary
The Resonance Atlas functions as a set of UV boundary conditions for the Standard Model gauge couplings. Instead of assuming unification to a single value as in a traditional GUT, it provides a specific, constrained list of allowed values for the inverse-square couplings (1/gᵢ²) at the Pirouette framework's "coherence barrier" scale (μ_c). These values are theoretically derived, not freely chosen, making the low-energy values of α_s, α_EM, and sin²θ_W predictions of the framework.

## Glossary Links
- See also: [FRAME_STIFFNESS](/FRAME_STIFFNESS), [COHERENCE_BARRIER](/COHERENCE_BARRIER), [TEMPORAL_PRESSURE](/TEMPORAL_PRESSURE), [WEINBERG_ANGLE](/WEINBERG_ANGLE)