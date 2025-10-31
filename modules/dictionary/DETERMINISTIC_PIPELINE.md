---
term: "Deterministic pipeline"
canonical_id: "DETERMINISTIC_PIPELINE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-YM-003_nonperturbative_map"]
---

---
term: Deterministic Pipeline
canonical_id: DETERMINISTIC_PIPELINE
symbol: 
aliases: [Nonperturbative map, No-tuning pipeline]
parents: [DYNA-COLOR-001, MATH-YM-002, XXP-BRIDGE-Γ-001]
children: [XXP-EWQCD-EXP]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-YM-003_nonperturbative_map
      lines: "§1"
      snippet: |
        Provide a **deterministic pipeline** that converts Pirouette’s mechanical parameters—**temporal-color frame stiffness** (\kappa_3) and **Γ-coherence length** (\xi_\Gamma)—plus the running coupling (g_s(\mu)) into **nonperturbative QCD outputs**:

        * fundamental **string tension** (\sigma),
        * **Λ_{\rm QCD})** in a chosen scheme,
        * lattice reference scales (r_0, t_0), and the **lattice spacing** (a).
  editors: [AI Assistant (claude-3-opus)]
  review_log: []
triad:
  art: |
    This is the conductor’s score for the nonperturbative orchestra. Frame stiffness sets the pitch of the strings, Γ-coherence sets the tension of the drum skin, and together they produce the fundamental note of confinement, the string tension σ. From that single note, the entire harmonic structure of the hadronic world unfolds.
  law: |
    A fixed, algorithmic procedure that converts mechanical inputs (κ₃, ξ_Γ) into the fundamental string tension (σ) via the core scaling relation σ = c_σ (κ₃/ξ_Γ²). The normalization constant c_σ is fixed once against a single empirical anchor. All subsequent nonperturbative scales (r₀, t₀, Λ_QCD) are derived from σ without further tuning.
  philosophy: |
    To provide a rigid, falsifiable bridge between the abstract mechanics of the Pirouette framework and the concrete, measurable world of hadronic phenomenology. It enforces discipline by replacing parameter tuning with direct prediction, closing the loop between the coherence barrier and observable reality.
pirouette_definition: |
  A fixed, step-by-step computational procedure that converts the framework's core mechanical parameters into a suite of nonperturbative QCD observables. It takes as input the temporal-color frame stiffness (κ₃), the Γ-coherence length (ξ_Γ), and the running coupling (g_s(μ)) at a matching scale. It outputs the fundamental string tension (σ), the QCD scale (Λ_QCD), standard lattice reference scales (r₀, t₀), and a prediction for the lattice spacing (a). The entire pipeline is fixed by a single, one-time normalization constant, after which it operates without any further tuning.
operational_definition:
  units: The pipeline outputs multiple quantities with standard physical units. σ: [Energy]², σ¹/² & Λ_QCD: [Energy], r₀ & t₀¹/² & a: [Length].
  symbol_table:
    - name: σ
      meaning: Fundamental string tension
      dimensions: M L T⁻² (Force) or M T⁻² (Energy/Length)
      default_range: (440 MeV)² ≈ 0.9 GeV/fm
    - name: κ₃
      meaning: Temporal-color frame stiffness
      dimensions: M L² T⁻² (Energy × Length)
      default_range: contextual
    - name: ξ_Γ
      meaning: Γ-coherence length
      dimensions: L (Length)
      default_range: contextual
    - name: Λ_S
      meaning: RG-invariant QCD scale in scheme S
      dimensions: M L T⁻² (Energy)
      default_range: 200–400 MeV
    - name: r₀, t₀¹/²
      meaning: Sommer and gradient-flow reference scales
      dimensions: L (Length)
      default_range: r₀ ≈ 0.5 fm
    - name: a
      meaning: Lattice spacing
      dimensions: L (Length)
      default_range: 0.05–0.1 fm
  measurement:
    procedures:
      - name: Standard Nonperturbative Map
        outline: |
          1.  Provide inputs: (ω_c, χ) from the Bridge module and g_s(μ_*) from RG running.
          2.  Compute mechanical parameters: ξ_Γ from (ω_c, χ) and κ₃ from g_s(μ_*).
          3.  Predict string tension: σ = c_σ κ₃/ξ_Γ², where c_σ is a pre-calibrated universal constant.
          4.  Derive lattice scales: calculate r₀ and t₀ from the predicted σ.
          5.  Predict lattice spacing: For a given lattice calculation reporting (r₀/a), predict the physical spacing 'a'.
          6.  Derive Λ_QCD: Integrate the β-function from α_s(μ_*) to obtain Λ_QCD in a chosen scheme.
          7.  Cross-check: Use the derived Λ_QCD to run α_s up to M_Z and compare with experimental values.
        expected_signals: [A numerical prediction for σ, r₀, t₀, a, Λ_MS-bar]
        pitfalls: [Scale inconsistency between derived (r₀, t₀) and lattice results, mismatch in the σ/Λ_QCD ratio, failure to reproduce α_s(M_Z) in the RG loop closure test.]
context_windows:
  - module: MATH-YM-003_nonperturbative_map
    excerpt: |
      Provide a **deterministic pipeline** that converts Pirouette’s mechanical parameters—**temporal-color frame stiffness** (κ₃) and **Γ-coherence length** (ξ_Γ)—plus the running coupling (g_s(μ)) into **nonperturbative QCD outputs**. This closes the loop between the **coherence barrier** and **hadronic phenomenology**.
  - module: MATH-YM-003_nonperturbative_map
    excerpt: |
      **Falsifiability (nonperturbative gates)**

      *   **Scale inconsistency:** Pirouette-predicted (a) disagrees with lattice-extracted (a) across ensembles after the one-time normalization → fails the (σ→r₀,t₀) map.
      *   **(\sqrt{σ}/\Lambda_{\overline{\rm MS}}) mismatch:** persistent, scheme-robust deviation beyond combined errors → breaks the (σ↔Λ) link.
poetic_connections:
  motifs: [confinement, scale setting, no tuning, conductor's score, bridge to reality]
  evocative_lines:
    - "stiffness sets the strings, coherence sets the drum skin, and out comes σ."
    - "every lattice number has a seat in the hall—and every seat points back to the same temporal instrument."
  association_matrix:
    - [ "FRAME_STIFFNESS", 0.9 ]
    - [ "GAMMA_COHERENCE_LENGTH", 0.9 ]
    - [ "STRING_TENSION", 0.8 ]
    - [ "LATTICE_SPACING", 0.7 ]
formal_mappings:
  candidates: []
  adopted:
    - target: String Tension (σ)
      domain: Lattice QCD
      mapping_kind: operational
      equation_hint: |
        V(R) = σR - (π/12R) + ...
      justification: |
        The pipeline's output σ is defined to be operationally identical to the string tension extracted from the linear part of the static heavy-quark potential, a standard observable in lattice QCD calculations.
      confidence: 1.0
    - target: Λ_QCD
      domain: SM
      mapping_kind: mathematical
      equation_hint: |
        Λ = μ exp[-1/(2β₀α_s(μ))] ...
      justification: |
        The derived Λ_S is the standard RG-invariant scale of QCD, defined via integration of the perturbative β-function. It maps directly to the Λ_MS-bar parameter used in high-energy phenomenology.
      confidence: 1.0
    - target: Sommer scale (r₀) & Gradient-flow scale (t₀)
      domain: Lattice QCD
      mapping_kind: operational
      justification: |
        The pipeline derives r₀ and t₀ using their standard implicit definitions from the static potential and the gradient flow, respectively. These are used as direct inputs for setting the scale (i.e., determining the lattice spacing 'a') in lattice simulations.
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "The pipeline's predicted lattice spacing 'a' will match the value determined by lattice practitioners for a given ensemble, after the single universal calibration."
      domain: phenomenology
      falsifier: "A statistically significant disagreement between the predicted 'a' and the lattice-determined 'a' across multiple lattice gauge ensembles and spacings."
      status: proposed
      links: [MATH-YM-003_nonperturbative_map]
    - statement: "The predicted ratio sqrt(σ)/Λ_MS-bar is a constant of nature, matching the empirically determined value."
      domain: theory
      falsifier: "The pipeline produces a value for this ratio that is inconsistent with the value extracted from combined lattice and experimental data, beyond scheme-conversion uncertainties."
      status: proposed
      links: [MATH-YM-003_nonperturbative_map]
    - statement: "The RG loop closes: Λ_QCD derived from low-energy σ correctly evolves to the experimental α_s(M_Z)."
      domain: phenomenology
      falsifier: "The value of α_s(M_Z) derived by running the coupling up from the pipeline's Λ_QCD value disagrees with the world average, even after accounting for matching uncertainties at quark thresholds."
      status: proposed
      links: [MATH-YM-002]
naming_notes:
  collisions: [The term "pipeline" is common in data science and CI/CD workflows.]
  disambiguation: |
    Unlike a data analysis or machine learning pipeline, the Deterministic Pipeline is a fixed physical model. Its structure is not subject to training or optimization; it is a rigid, first-principles calculation pathway from a mechanical model to nonperturbative observables. The key property is "deterministic" and "no-tuning".
crosslinks:
  near_synonyms: [NONPERTURBATIVE_MAP]
  antonyms: [TUNABLE_PHENOMENOLOGICAL_MODEL]
  prerequisites: [FRAME_STIFFNESS, GAMMA_COHERENCE_LENGTH, RUNNING_COUPLING]
  downstream_effects: [LATTICE_SPACING, HADRONIC_SPECTRUM, QUARKONIUM_PROPERTIES]
license: CC-BY-SA-4.0
---

# Deterministic Pipeline

## Canonical (Pirouette)
A fixed, step-by-step computational procedure that converts the framework's core mechanical parameters into a suite of nonperturbative QCD observables. It takes as input the temporal-color frame stiffness (κ₃), the Γ-coherence length (ξ_Γ), and the running coupling (g_s(μ)) at a matching scale. It outputs the fundamental string tension (σ), the QCD scale (Λ_QCD), standard lattice reference scales (r₀, t₀), and a prediction for the lattice spacing (a). The entire pipeline is fixed by a single, one-time normalization constant, after which it operates without any further tuning.

## EFT-First Summary
The Deterministic Pipeline provides a direct, operational mapping from Pirouette's mechanical parameters to standard nonperturbative QCD observables. The core output, the string tension (σ), is identical to that measured in lattice QCD and used in the Cornell potential for heavy quarkonia. The derived QCD scale (Λ_QCD) is the standard RG-invariant scale in a chosen scheme (e.g., MS-bar), and the reference scales (r₀, t₀) are precisely the Sommer and gradient-flow scales used by lattice practitioners for setting the lattice spacing 'a' in their simulations.

## Glossary Links
- See also: [Frame Stiffness](...), [Γ-Coherence Length](...), [String Tension](...), [Λ_QCD](...), [Lattice Spacing](...)