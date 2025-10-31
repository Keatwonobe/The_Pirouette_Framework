---
term: "String tension"
canonical_id: "STRING_TENSION"
symbol: "σ"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DYNA-COLOR-001_su(3)_c_as_temporal_color_frame"]
---

---
term: String tension
canonical_id: STRING_TENSION
symbol: σ
aliases: []
parents: [DYNA-COLOR-001]
children: [MATH-YM-003, XXP-EWQCD-EXP]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DYNA-COLOR-001
      lines: "40-42"
      snippet: |
        **Scaling law (baseline):**
        [
        \boxed{\ \sigma ;\sim; c_\sigma ,\frac{\kappa_3}{\xi_\Gamma^2}
        ;=; c_\sigma,\frac{1}{g_s^2(\mu_\ast)},\frac{1}{\xi_\Gamma^2}\ } ,
        ]
  editors: [system-agent]
  review_log: []
triad:
  art: |
    Color is time’s threefold braid; string tension is the force that binds its knots, a measure of how stiff the braid is and how finely time can hold itself together.
  law: |
    String tension (σ) is proportional to the temporal-color frame stiffness (κ₃) and inversely proportional to the square of the Γ-coherence length (ξ_Γ): σ ∝ κ₃ / ξ_Γ².
  philosophy: |
    String tension provides the mechanical-energetic basis for quark confinement in the Pirouette Framework, linking a macroscopic QCD observable directly to the microscopic stiffness and coherence scales of the underlying temporal-color medium.
pirouette_definition: |
  The energy per unit length of the color-electric flux tube confining quarks. It arises from the dual Meissner effect in a medium where (Z_3) center vortices have condensed. The tension's value is determined by the ratio of the temporal-color frame's effective elastic modulus (κ₃ = 1/g_s²) to the squared Γ-coherence length (ξ_Γ²), which acts as the flux tube's penetration depth.
operational_definition:
  units: `GeV²` or `GeV/fm` (in natural units c=ħ=1)
  symbol_table:
    - name: σ
      meaning: String tension
      dimensions: Energy² or Energy/Length
      default_range: ~0.18 GeV²
    - name: κ₃
      meaning: Temporal-color frame stiffness (effective elastic modulus)
      dimensions: dimensionless
      default_range: contextual, via g_s(μ)
    - name: ξ_Γ
      meaning: Γ-coherence length (vortex core size / penetration depth)
      dimensions: Length
      default_range: contextual, via ω_c
    - name: g_s
      meaning: SU(3)_c strong coupling constant
      dimensions: dimensionless
      default_range: contextual
  measurement:
    procedures:
      - name: Wilson Loop Area Law (Lattice QCD)
        outline: |
          Calculate the expectation value of large, planar Wilson loops ⟨W(C)⟩ on a Euclidean spacetime lattice. The string tension σ is extracted from the exponential decay of this value with the loop's minimal area: -log⟨W(C)⟩ ≈ σ⋅Area(C). This corresponds to the coefficient of the linear term in the static quark-antiquark potential, V(R) ≈ σR for large R.
        expected_signals: [Exponential decay of ⟨W(C)⟩ with loop area, A linearly rising static quark-antiquark potential]
        pitfalls: [String breaking at large distances due to pair production, Finite volume and lattice spacing artifacts]
      - name: Regge Trajectory Slope
        outline: |
          Measure the masses (M) and spins (J) of families of light-quark hadrons (e.g., mesons). Plot J versus M². The slope of the resulting linear "Regge trajectory," α', is inversely related to the string tension by α' ≈ 1/(2πσ).
        expected_signals: [Linearly rising J vs. M² trajectories for hadron families]
        pitfalls: [Trajectory curvature from spin-dependent and other relativistic effects, State mixing]
context_windows:
  # Short, trimmed context quotes harvested from modules (3–6 sentences each).
  - module: DYNA-COLOR-001
    excerpt: |
      Color-electric flux is expelled from the condensed vortex medium (dual Meissner effect); it **bundles** into tubes. The **string tension** is controlled by two mechanical scales: Frame stiffness (temporal-color): (K_3) and Γ-coherence length (vortex core/penetration depth): (ξ_Γ). This leads to the scaling law: [ σ ∼ c_σ (κ_3 / ξ_Γ²) ]. Stiffer temporal-color frames (smaller g_s) and shorter Γ-coherence (smaller ξ_Γ) both increase σ.
  - module: DYNA-COLOR-001
    excerpt: |
      With the strong coupling g_s fixed at M_Z and run down to a matching scale, σ becomes a **function of ξ_Γ** alone. This relationship directly connects string tension to observables like Hadron Regge slopes (α' ~ (2πσ)⁻¹) and the splittings in quarkonium spectra, whose potentials are calibrated to σ.
poetic_connections:
  # Lightweight "word-association graph" and sticky lines.
  motifs: [flux tube, temporal braid, vortex condensate, dual superconductor]
  evocative_lines:
    - "Color is time’s threefold braid."
    - "...the world pulls quarks together with cords of temporal tension."
  association_matrix:
    # symmetric or directed; weights in [0,1]
    - [ "FRAME_STIFFNESS", 0.9 ]
    - [ "Γ_COHERENCE_LENGTH", 0.9 ]
    - [ "CENTER_VORTEX", 0.7 ]
formal_mappings:
  # Candidate alignments to EFT/SM/CM/GR terms, each with justification and refs.
  candidates: []
  adopted:
    - target: String tension (σ_QCD)
      domain: SM (Lattice QCD)
      mapping_kind: operational
      equation_hint: |
        V_Cornell(R) = -a/R + σR
      rationale: |
        The Pirouette string tension σ is operationally identical to the parameter σ in the Cornell potential for heavy quarkonium, which is extracted from lattice QCD simulations. Both represent the energy per unit length of the flux tube responsible for linear confinement and the area law of Wilson loops.
      references:
        - title: "Quarkonium" in Review of Particle Physics
          where: Particle Data Group
          date: 2024-08-01
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The value of σ scales with the frame stiffness and Γ-coherence length as σ ∝ κ₃ / ξ_Γ²."
      domain: theory
      falsifier: "Lattice simulations where κ₃ and ξ_Γ are varied independently (e.g., via anisotropies) show a scaling law inconsistent with this prediction."
      status: proposed
      links: [DYNA-COLOR-001]
    - statement: "The tension of k-strings, σ_k, follows the N-ality dependence predicted by the Z₃ center symmetry, approximately σ_k/σ₁ = sin(πk/3)/sin(π/3)."
      domain: theory
      falsifier: "Lattice measurements of the k-string tension hierarchy show a pattern (e.g., Casimir scaling) that cannot be reconciled with the sine-law prediction from the center-vortex model."
      status: proposed
      links: [DYNA-COLOR-001]
naming_notes:
  collisions: [The symbol σ is also commonly used for scattering cross-sections and Pauli spin matrices.]
  disambiguation: |
    Context (QCD, confinement, potentials, Regge trajectories) is essential for disambiguation. In this framework, σ without a subscript always refers to the fundamental string tension.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [FRAME_STIFFNESS, Γ_COHERENCE_LENGTH, CENTER_VORTEX]
  downstream_effects: [REGGE_SLOPE, QUARKONIUM_SPECTRUM, HADRON_MASS]
license: CC-BY-SA-4.0
---

# String tension

## Canonical (Pirouette)
The energy per unit length of the color-electric flux tube confining quarks. It arises from the dual Meissner effect in a medium where (Z_3) center vortices have condensed. The tension's value is determined by the ratio of the temporal-color frame's effective elastic modulus (κ₃ = 1/g_s²) to the squared Γ-coherence length (ξ_Γ²), which acts as the flux tube's penetration depth.

## EFT-First Summary
String tension (σ) is the energy per unit length of the confining QCD flux tube, corresponding to the linear term (σR) in the Cornell potential for heavy quarkonium. Experimentally, its value is approximately 0.18 GeV², or ~1 GeV/fm, and it sets the scale for hadron masses and the slope of Regge trajectories. In the Pirouette Framework, this value is not a fundamental input but is derived from the mechanical properties of the temporal-color medium.

## Glossary Links
- See also: [[Frame Stiffness]], [[Γ-Coherence Length]], [[Confinement]]