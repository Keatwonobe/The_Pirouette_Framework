---
term: "Λ_QCD"
canonical_id: "QCD"
symbol: "Λ_QCD"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-YM-003_nonperturbative_map"]
---

---
term: Λ_QCD
canonical_id: LAMBDA_QCD
symbol: Λ_QCD
aliases: [QCD Scale Parameter]
parents: [MATH-YM-003_nonperturbative_map, MATH-YM-002, DYNA-COLOR-001]
children: [XXP-EWQCD-EXP]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-YM-003_nonperturbative_map
      lines: "§5"
      snippet: |
        Choose scheme (S\in{\overline{\rm MS},{\rm MOM},\ldots}). Define the RG-invariant scale via the β-function:
        [
        \Lambda_S = \mu,\exp!\Big(-\frac{1}{2\beta_0,\alpha_s(\mu)}\Big),
        \big(\beta_0 \alpha_s(\mu)\big)^{-\beta_1/(2\beta_0^2)}
        \Big[1+\mathcal{O}(\alpha_s)\Big].
        ]
  editors: [auto-agent-v1]
  review_log: []
triad:
  art: |
    The silent, immutable note to which the entire orchestra of the strong force is tuned. It is the scale at which perturbative whispers become a deafening, non-linear chorus of confinement.
  law: |
    Λ_QCD is the energy scale at which the perturbative running coupling, when extrapolated from high energies via the renormalization group (RG) equation, formally diverges. It is an RG-invariant constant of integration that sets the physical scale for all nonperturbative QCD phenomena.
  philosophy: |
    Λ_QCD represents the concept of dimensional transmutation: a classical theory with a dimensionless coupling constant (`g_s`) gives rise to a quantum theory with a characteristic, physical energy scale. It is the fundamental constant that emerges from the theory's dynamics, replacing the bare coupling as the primary input and anchoring all predicted masses and tensions to a measurable value.
pirouette_definition: |
  The Renormalization Group (RG) invariant energy scale of the strong interaction, deterministically derived by integrating the β-function downwards from a matching scale `μ_*`. Within Pirouette, it is not a free parameter but an output, computed from the fundamental string tension (`σ`), which itself is a function of the temporal-color frame stiffness (`κ₃`) and Γ-coherence length (`ξ_Γ`). It serves as the primary bridge between the framework's mechanical inputs and empirical hadronic scales.
operational_definition:
  units: Energy (typically MeV or GeV)
  symbol_table:
    - name: Λ_S
      meaning: The QCD scale parameter in a specific renormalization scheme 'S' (e.g., S = MS-bar).
      dimensions: M L² T⁻²
      default_range: 200–400 MeV
    - name: α_s(μ)
      meaning: The strong coupling constant at energy scale μ.
      dimensions: dimensionless
      default_range: 0.1–0.3 (at few-GeV scales)
    - name: μ
      meaning: Renormalization scale.
      dimensions: M L² T⁻²
      default_range: contextual (e.g., 2 GeV, M_Z)
    - name: β₀, β₁
      meaning: First two universal coefficients of the QCD β-function.
      dimensions: dimensionless
      default_range: β₀ = (11N-2f)/3, β₁ = (34N²-10Nf-3f(N²-1)/N)/3 for SU(N) with f flavors.
  measurement:
    procedures:
      - name: Derivation from Pirouette Low-Energy Constants
        outline: |
          1. Obtain Pirouette mechanical parameters: frame stiffness (`κ₃`) and Γ-coherence length (`ξ_Γ`).
          2. Compute the fundamental string tension via the core scaling relation: `σ = c_σ κ₃ / ξ_Γ²`. The constant `c_σ` is fixed once via a single hadronic observable (e.g., `σ¹/² = 440 MeV`).
          3. Use the empirically determined, scheme-dependent ratio `C_σ = sqrt(σ) / Λ_MS` to extract `Λ_MS`.
          4. Alternatively, use `σ` to set a lattice scale (`r₀`), match lattice data for `α_s` at that scale, and integrate the β-function to find `Λ_MS`.
        expected_signals:
          - A stable value for `Λ_MS` (~330 MeV for N_f=5) consistent with experimental determinations.
          - The derived value, when used to run `α_s` up to the Z-boson mass, reproduces the experimental `α_s(M_Z)`.
        pitfalls:
          - High sensitivity to the value of `α_s(μ)` used in the integration.
          - Ambiguity from higher-order terms in the β-function and matching procedure.
          - Strict scheme dependence; `Λ_MS` is different from `Λ_MOM`.
context_windows:
  - module: MATH-YM-003_nonperturbative_map
    excerpt: |
      **Pipeline:** compute (σ) (Pirouette) → infer (Λ_{\overline{\rm MS}}) → run (α_s(M_Z)) back up as a **cross-check** against experiment (closes the loop with **MATH-YM-002**).
  - module: MATH-YM-003_nonperturbative_map
    excerpt: |
      **(\sqrt{\sigma}/\Lambda_{\overline{\rm MS}}) mismatch:** persistent, scheme-robust deviation beyond combined errors → breaks the (\sigma\leftrightarrow\Lambda) link.
poetic_connections:
  motifs: [dimensional transmutation, confinement scale, emergent mass, infrared slavery]
  evocative_lines:
    - "closes the loop between the coherence barrier and hadronic phenomenology."
    - "every seat in the hall—and every seat points back to the same temporal instrument."
  association_matrix:
    - [ "STRING_TENSION", 0.9 ]
    - [ "RUNNING_COUPLING_GS", 0.8 ]
    - [ "FRAME_STIFFNESS_K3", 0.6 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Λ_QCD (QCD Scale Parameter)
      domain: SM
      mapping_kind: mathematical
      equation_hint: |
        Λ_S = μ exp[ -∫^α_s(μ) dα' / β(α') ]
      rationale: |
        The Pirouette term `Λ_QCD` is defined to be mathematically and operationally identical to the standard QCD scale parameter found in textbooks and the Particle Data Group (PDG) review. It is not an analogy but a direct adoption of the standard definition, with the novel claim being its deterministic origin in more fundamental Pirouette parameters.
      references:
        - title: Review of Particle Physics
          where: Particle Data Group, "Quantum Chromodynamics" section
          date: 2024-08-01
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "The ratio `sqrt(σ)/Λ_MS` is a predicted constant (up to small, known corrections) derived from Pirouette inputs (`κ₃`, `ξ_Γ`)."
      domain: phenomenology
      falsifier: "A persistent, scheme-robust deviation between the Pirouette-predicted ratio and the value extracted from lattice QCD simulations, beyond combined errors."
      status: proposed
      links: [MATH-YM-003_nonperturbative_map]
    - statement: "The value of `Λ_QCD` derived from low-energy Pirouette inputs correctly reproduces the experimental value of `α_s(M_Z)` via standard RG evolution."
      domain: experiment
      falsifier: "The reconstructed `α_s(M_Z)` conflicts with the world average, even after accounting for matching uncertainties at the scale `μ_*`."
      status: proposed
      links: [MATH-YM-003_nonperturbative_map, MATH-YM-002]
naming_notes:
  collisions: [Cosmological Constant (Λ), Lambda baryons (Λ_c, Λ_b)]
  disambiguation: |
    Must be subscripted with 'QCD' and often a scheme (e.g., `Λ_MS`) to distinguish from other physical constants using the symbol Λ. It is an emergent energy scale, not a particle mass, and is a parameter of the theory itself rather than the state of a system.
crosslinks:
  near_synonyms: [QCD_SCALE]
  antonyms: [UV_CUTOFF]
  prerequisites: [FRAME_STIFFNESS_K3, COHERENCE_LENGTH_XIG, RUNNING_COUPLING_GS]
  downstream_effects: [STRING_TENSION, LATTICE_SPACING, HADRON_MASS]
license: CC-BY-SA-4.0
---

# Λ_QCD

## Canonical (Pirouette)
The Renormalization Group (RG) invariant energy scale of the strong interaction, deterministically derived by integrating the β-function downwards from a matching scale `μ_*`. Within Pirouette, it is not a free parameter but an output, computed from the fundamental string tension (`σ`), which itself is a function of the temporal-color frame stiffness (`κ₃`) and Γ-coherence length (`ξ_Γ`). It serves as the primary bridge between the framework's mechanical inputs and empirical hadronic scales.

## EFT-First Summary
Λ_QCD is the fundamental, renormalization-group-invariant energy scale of Quantum Chromodynamics (QCD), identical to the standard parameter defined in the literature (e.g., in the MS-bar scheme). It emerges from dimensional transmutation, where the dimensionless bare coupling `g_s` is traded for a physical scale that governs all non-perturbative phenomena like confinement and hadron masses. Its value is a key prediction and consistency check for any fundamental theory of the strong force. (Ref: Particle Data Group, "Quantum Chromodynamics" review).

## Glossary Links
- See also: String Tension (σ), Running Coupling (α_s)