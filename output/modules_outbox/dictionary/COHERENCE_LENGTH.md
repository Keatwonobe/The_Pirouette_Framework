---
term: "Γ-coherence length"
canonical_id: "COHERENCE_LENGTH"
symbol: "ξ_Γ"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DYNA-COLOR-001_su(3)_c_as_temporal_color_frame"]
---

---
term: Γ-coherence length
canonical_id: GAMMA_COHERENCE_LENGTH
symbol: ξ_Γ
aliases: [vortex core radius, color-electric penetration depth]
parents: [DYNA-COLOR-001, XXP-BRIDGE-Γ-001]
children: [MATH-YM-003, XXP-EWQCD-EXP]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DYNA-COLOR-001_su(3)_c_as_temporal_color_frame
      snippet: |
        Γ-coherence length:
        [
        \xi_\Gamma ;\sim; \frac{c}{\omega_c};\times;\chi^{-1/2},
        ]
        with (\chi) a dimensionless susceptibility of the Γ field (fixed by XXP-BRIDGE-Γ-001).
  editors: [GPT-4 via Pirouette Agent]
  review_log: []
triad:
  art: |
    The fineness of the weave of spacetime; the radius of a knot in the temporal braid below which color-electric fields cannot penetrate.
  law: |
    The QCD string tension (σ) is inversely proportional to the square of the Γ-coherence length, σ ∝ 1/ξ_Γ². A smaller coherence length results in a stronger confining force.
  philosophy: |
    ξ_Γ represents the fundamental scale at which the Γ-field's vacuum structure resists deformation by gauge fields. It bridges the microscopic dynamics of the Γ-field (via ω_c) to the macroscopic, nonperturbative phenomena of QCD confinement, making it a critical link between the Pirouette UV and the Standard Model IR.
pirouette_definition: |
  The Γ-coherence length (ξ_Γ) is the characteristic length scale defining the core size of a condensed (Z₃) center vortex in the temporal-color frame. In the dual superconductor analogy for QCD confinement, it acts as the penetration depth for color-electric fields, determining the radius of the flux tube. It is set by the coherence barrier frequency (ω_c) and Γ-field susceptibility (χ), and directly controls the QCD string tension (σ) via the relation σ ∝ 1/(g_s² ξ_Γ²).
operational_definition:
  units: meters (m)
  symbol_table:
    - name: ξ_Γ
      meaning: Γ-coherence length
      dimensions: L
      default_range: contextual (~10⁻¹⁵ m)
    - name: σ
      meaning: Fundamental QCD string tension
      dimensions: M T⁻²
      default_range: ~0.9 GeV/fm
    - name: κ₃
      meaning: Temporal-color frame stiffness
      dimensions: dimensionless (in natural units)
      default_range: 1/g_s²(μ)
    - name: ω_c
      meaning: Coherence barrier frequency
      dimensions: T⁻¹
      default_range: contextual (UV scale)
  measurement:
    procedures:
      - name: Indirect determination via string tension
        outline: |
          1. Measure the fundamental QCD string tension (σ) from lattice QCD simulations of the static quark potential or phenomenologically from hadron Regge slopes (α' ≈ 1/(2πσ)).
          2. Determine the strong coupling g_s(μ) at a matching scale μ* via independent measurements and renormalization group evolution.
          3. Invert the scaling relation σ ≈ c_σ · κ₃/ξ_Γ² = c_σ · (1/g_s²(μ*)) · (1/ξ_Γ²) to solve for ξ_Γ.
        expected_signals: [A value for ξ_Γ on the order of Λ_QCD⁻¹, consistent with lattice-derived flux tube radii.]
        pitfalls: [Ambiguity in the matching scale μ*, uncertainty in the O(1) non-perturbative coefficient c_σ, contamination from string breaking effects.]
context_windows:
  - module: DYNA-COLOR-001_su(3)_c_as_temporal_color_frame
    excerpt: |
      The string tension is controlled by two mechanical scales: Frame stiffness (temporal-color): (K_3) or equivalently (g_s(\mu)), and Γ-coherence length (vortex core/penetration depth): (ξ_Γ).
      Scaling law (baseline):
      [
      \boxed{\ \sigma ;\sim; c_\sigma ,\frac{\kappa_3}{\xi_\Gamma^2}
      ;=; c_\sigma,\frac{1}{g_s^2(\mu_\ast)},\frac{1}{\xi_\Gamma^2}\ }
      ]
  - module: DYNA-COLOR-001_su(3)_c_as_temporal_color_frame
    excerpt: |
      Coherence barrier: (\mu_c = \hbar\omega_c/c^2) sets the UV anchor; below (\mu_c), use standard QCD running (MATH-YM-002).
      Γ-coherence length:
      [
      \xi_\Gamma ;\sim; \frac{c}{\omega_c};\times;\chi^{-1/2},
      ]
      with (\chi) a dimensionless susceptibility of the Γ field (fixed by XXP-BRIDGE-Γ-001).
poetic_connections:
  motifs: [vortex core, penetration depth, temporal braid, stiffness, flux tube]
  evocative_lines:
    - "how finely time can hold itself together."
    - "Color is time’s threefold braid."
  association_matrix:
    - [ "STRING_TENSION", 0.9 ]
    - [ "CENTER_VORTEX", 0.8 ]
    - [ "COHERENCE_BARRIER", 0.7 ]
    - [ "FRAME_STIFFNESS", 0.6 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Ginzburg-Landau coherence length (ξ)
      domain: CM
      mapping_kind: conceptual
      equation_hint: |
        In superconductivity, the magnetic penetration depth is λ_L and the coherence length is ξ. In the dual picture for QCD, the color-magnetic penetration depth is ~ξ_Γ and the color-electric penetration depth is the dual quantity ~λ.
      justification: |
        In the dual superconductor model of confinement, the QCD vacuum is analogous to a Type-II superconductor where magnetic monopoles have condensed. The Γ-coherence length ξ_Γ plays the role of the Ginzburg-Landau coherence length, defining the size of the "normal-conducting" core of a vortex—in this case, a (Z₃) center vortex tube that confines color-electric flux.
      rationale: This is the central analogy used in DYNA-COLOR-001 to give a mechanical interpretation to confinement.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The QCD string tension σ must scale with the inverse square of ξ_Γ, where ξ_Γ is independently constrained by the coherence barrier frequency ω_c."
      domain: theory|phenomenology
      falsifier: "Lattice simulations or other non-perturbative methods show that σ is independent of parameters controlling ω_c, or scales in a way inconsistent with σ ∝ 1/ξ_Γ²."
      status: proposed
      links: [DYNA-COLOR-001, XXP-BRIDGE-Γ-001]
naming_notes:
  collisions: [The symbol ξ is standard for coherence and correlation lengths in condensed matter and statistical physics. The Γ subscript is crucial to distinguish this specific Pirouette quantity.]
  disambiguation: |
    Distinguish from the QCD *correlation length*, which is the inverse of the lightest glueball mass (~1/m_G). ξ_Γ describes the *transverse* size of a confining flux tube, while the correlation length describes the *longitudinal* scale over which vacuum fluctuations (like glueballs) are correlated.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [COHERENCE_BARRIER, FRAME_STIFFNESS]
  downstream_effects: [STRING_TENSION, REGGE_SLOPE, K_STRING_HIERARCHY]
license: CC-BY-SA-4.0
---

# Γ-coherence length

## Canonical (Pirouette)
The Γ-coherence length (ξ_Γ) is the characteristic length scale defining the core size of a condensed (Z₃) center vortex in the temporal-color frame. In the dual superconductor analogy for QCD confinement, it acts as the penetration depth for color-electric fields, determining the radius of the flux tube. It is set by the coherence barrier frequency (ω_c) and Γ-field susceptibility (χ), and directly controls the QCD string tension (σ) via the relation σ ∝ 1/(g_s² ξ_Γ²).

## EFT-First Summary
In the effective dual superconductor model for QCD, the Γ-coherence length ξ_Γ is the direct analogue of the **Ginzburg-Landau coherence length** from condensed matter physics. It defines the radius of the 'normal' core of a (Z₃) center vortex, inside which the color-electric field is strong, and outside of which the vacuum condensate expels the field. This length scale, along with the frame stiffness (inverse coupling squared), sets the string tension and thus the fundamental scale of quark confinement.

## Glossary Links
- See also: [String Tension](<#STRING_TENSION>), [Center Vortex](<#CENTER_VORTEX>), [Frame Stiffness](<#FRAME_STIFFNESS>), [Coherence Barrier](<#COHERENCE_BARRIER>)