---
term: "Frame stiffness"
canonical_id: "FRAME_STIFFNESS"
symbol: "κ₃"
aliases: [K₃]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DYNA-COLOR-001_su(3)_c_as_temporal_color_frame"]
---

---
term: Frame stiffness
canonical_id: FRAME_STIFFNESS_K3
symbol: κ₃
aliases: [K₃, temporal-color frame stiffness]
parents: [DYNA-COLOR-001, MATH-YM-001]
children: [MATH-YM-003, XXP-EWQCD-EXP]
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DYNA-COLOR-001_su(3)_c_as_temporal_color_frame
      lines: "§2, §4"
      snippet: |
        K_3\equiv \frac{1}{g_s^2}
        ...
        \boxed{\ \sigma \sim c_\sigma \frac{\kappa_3}{\xi_\Gamma^2} = c_\sigma\frac{1}{g_s^2(\mu_\ast)}\frac{1}{\xi_\Gamma^2}\ }
  editors: [GPT-4 (Pirouette Dictionary Agent)]
  review_log: []
triad:
  art: |
    The stiffness of time's threefold color braid. A tighter braid—a stiffer frame—binds the world with stronger cords of tension.
  law: |
    The elastic modulus of the temporal-color frame, κ₃, is defined as the inverse of the strong coupling squared (1/g_s²). It dictates the fundamental string tension (σ) in direct proportion, mediated by the Γ-coherence length (ξ_Γ): σ ∝ κ₃/ξ_Γ².
  philosophy: |
    Frame stiffness mechanizes the strong force coupling. It reframes the dimensionless number g_s as an emergent elastic property of the vacuum, connecting the abstract principles of gauge theory to the concrete, material language of tension and elasticity.
pirouette_definition: |
  The effective, dimensionless elastic modulus of the local SU(3) temporal-color frame. Frame stiffness, κ₃, quantifies the energy cost of de-synchronizing adjacent frames, making it the mechanical analog for the prefactor of the Yang-Mills Lagrangian. It is defined to be proportional to the inverse of the strong coupling squared, κ₃ ≡ 1/g_s²(μ), evaluated at a relevant energy scale μ. It is a primary determinant of the QCD string tension.
operational_definition:
  units: Dimensionless
  symbol_table:
    - name: κ₃
      meaning: Frame stiffness of the SU(3) temporal-color medium.
      dimensions: dimensionless
      default_range: ~2–10 in the nonperturbative regime (corresponding to α_s ~ 0.1–0.5).
    - name: g_s
      meaning: SU(3)c gauge coupling constant.
      dimensions: dimensionless
      default_range: contextual (runs with energy scale).
    - name: σ
      meaning: Fundamental QCD string tension.
      dimensions: M·L·T⁻² / L = M·T⁻² (Energy²/ (ħc)²)
      default_range: ~(440 MeV)² ≈ 0.9 GeV/fm
    - name: ξ_Γ
      meaning: Γ-coherence length, setting the scale of the dual superconductor's vortex core.
      dimensions: L
      default_range: contextual, derived from ω_c.
  measurement:
    procedures:
      - name: Indirect Determination via α_s
        outline: |
          1. Measure the strong coupling constant α_s(μ) at a high energy scale μ (e.g., M_Z) via precision particle physics experiments (e.g., jet event shapes, tau decays).
          2. Use the standard QCD renormalization group equations to evolve α_s down to a nonperturbative matching scale μ_∗ (typically 1-2 GeV).
          3. Calculate g_s(μ_∗) = sqrt(4π α_s(μ_∗)).
          4. Compute the stiffness as κ₃(μ_∗) = 1/g_s²(μ_∗).
        expected_signals: [A value of κ₃ consistent with lattice-derived observables.]
        pitfalls: [Ambiguity in the choice of matching scale μ_∗, scheme dependence of α_s.]
      - name: Inferred from Lattice QCD
        outline: |
          1. Perform a lattice QCD simulation to compute the fundamental string tension σ from the area law of large Wilson loops.
          2. Separately determine the Γ-coherence length ξ_Γ from Pirouette's Bridge relations (XXP-BRIDGE-Γ-001).
          3. Invert the scaling law to infer the frame stiffness: κ₃ = σ · ξ_Γ² / c_σ, where c_σ is an O(1) constant determined by the specific dual superconductor model.
        expected_signals: [A value for κ₃ that, when converted back to g_s, matches the experimentally run value at the lattice scale.]
        pitfalls: [Lattice artifacts (discretization, finite volume), uncertainty in c_σ, model-dependence of ξ_Γ.]
context_windows:
  - module: DYNA-COLOR-001_su(3)_c_as_temporal_color_frame
    excerpt: |
      The string tension is controlled by two mechanical scales: Frame stiffness (temporal-color): (K_3) or equivalently (g_s(\mu)), and Γ-coherence length (vortex core/penetration depth): (\xi_\Gamma). The scaling law is:
      [
      \sigma \sim c_\sigma \frac{\kappa_3}{\xi_\Gamma^2} = c_\sigma\frac{1}{g_s^2(\mu_\ast)}\frac{1}{\xi_\Gamma^2}
      ]
      Interpretation: stiffer temporal-color frames (smaller g_s) and shorter Γ-coherence (smaller ξ_Γ) both increase σ, tightening the flux tube.
  - module: DYNA-COLOR-001_su(3)_c_as_temporal_color_frame
    excerpt: |
      Local basis changes (U(x)\in SU(3)) are gauge redundancies; the connection keeps frames synchronized. Yang–Mills energy comes from frame-stiffness (MATH-YM-001):
      [
      \mathcal{L}_{\rm YM}^{(3)}=-\frac{1}{4}F_{\mu\nu}^a F^{a\mu\nu},\quad
      \alpha_s=\frac{g_s^2}{4\pi},\quad K_3\equiv \frac{1}{g_s^2}.
      ]
poetic_connections:
  motifs: [elasticity, temporal braid, color weave, structural integrity, tension]
  evocative_lines:
    - "Color is time’s threefold braid."
    - "...the world pulls quarks together with cords of temporal tension."
    - "The number on those cords—(σ)—is how stiff the braid is..."
  association_matrix:
    - [ "STRING_TENSION_SIGMA", 0.9 ]
    - [ "STRONG_COUPLING_GS", 0.9 ] # Inverse relationship
    - [ "GAMMA_COHERENCE_LENGTH_XIG", 0.7 ] # Inverse relationship
    - [ "CONFINEMENT", 0.8 ]
formal_mappings:
  candidates:
    - target: Effective Action Prefactor for YM Theory
      domain: EFT
      mapping_kind: mathematical
      equation_hint: |
        S_{YM} = \int d^4x\; \frac{1}{4g_s^2} \text{Tr}[F_{\mu\nu}F^{\mu\nu}] \implies \int d^4x\; \frac{\kappa_3}{4} \text{Tr}[F_{\mu\nu}F^{\mu\nu}]
      justification: |
        The frame stiffness κ₃ is a direct mechanical reinterpretation of the prefactor 1/g_s² that normalizes the Yang-Mills action. In standard QFT, this is a coupling strength; in Pirouette, it is the elastic modulus of the underlying medium whose shear modes constitute the gauge field.
      references: []
      confidence: 1.0
  adopted:
    - target: Inverse squared strong coupling (1/g_s²)
      rationale: This is a definitional mapping. It provides the primary bridge between the mechanical language of the Pirouette Framework and the standard formulation of Quantum Chromodynamics.
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "The QCD string tension σ is proportional to κ₃/ξ_Γ², where κ₃ is determined by the running coupling g_s and ξ_Γ is determined by the coherence barrier ω_c."
      domain: phenomenology
      falsifier: "A persistent, significant deviation between the measured string tension from lattice QCD and the value predicted by the scaling law using independently determined κ₃ (from α_s) and ξ_Γ (from the Bridge)."
      status: proposed
      links: [DYNA-COLOR-001, XXP-EWQCD-EXP]
    - statement: "Deformations of the theory that map to changes in κ₃ (e.g., via anisotropic lattices) should produce predictable, proportional changes in the measured string tension σ."
      domain: theory
      falsifier: "Lattice simulations showing that σ is insensitive to, or scales incorrectly with, controlled changes in the effective gauge coupling."
      status: proposed
      links: [DYNA-COLOR-001, MATH-YM-003]
naming_notes:
  collisions: [κ is a common symbol for compressibility, curvature, or thermal conductivity. K is a common symbol for spring constants. The subscript '3' is essential to specify the SU(3) nature.]
  disambiguation: |
    This is a dimensionless elastic modulus specific to the temporal-color frame, not to be confused with bulk or shear moduli of the spacetime medium itself. Unlike a mechanical spring constant with units of force/distance, κ₃'s role is analogous to the 1/T prefactor in a statistical mechanics partition function, controlling the weight of fluctuations.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [STRONG_COUPLING_GS, GAMMA_COHERENCE_LENGTH_XIG]
  downstream_effects: [STRING_TENSION_SIGMA, REGGE_SLOPE_AP, QUARKONIUM_POTENTIAL]
license: CC-BY-SA-4.0
---

# Frame stiffness

## Canonical (Pirouette)
The effective, dimensionless elastic modulus of the local SU(3) temporal-color frame. Frame stiffness, κ₃, quantifies the energy cost of de-synchronizing adjacent frames, making it the mechanical analog for the prefactor of the Yang-Mills Lagrangian. It is defined to be proportional to the inverse of the strong coupling squared, κ₃ ≡ 1/g_s²(μ), evaluated at a relevant energy scale μ. It is a primary determinant of the QCD string tension.

## EFT-First Summary
Frame stiffness (κ₃) is the Pirouette Framework's mechanical name for the inverse of the squared strong coupling constant, 1/g_s². In the Standard Model Effective Field Theory (SMEFT), the Yang-Mills Lagrangian for QCD is written as -1/4 F²; the coupling g_s is conventionally absorbed into the covariant derivative. Pirouette rewrites this term's normalization as κ₃/4, reinterpreting the coupling strength as an elastic property of the vacuum medium. All phenomenology of g_s, including its running with energy, maps directly to κ₃.

## Glossary Links
- See also: [string tension (σ)](<link>), [Γ-coherence length (ξ_Γ)](<link>), [strong coupling (g_s)](<link>)