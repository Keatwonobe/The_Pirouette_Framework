---
term: "Dual superconductor"
canonical_id: "DUAL_SUPERCONDUCTOR"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DYNA-COLOR-001_su(3)_c_as_temporal_color_frame"]
---

---
term: Dual Superconductor
canonical_id: DUAL_SUPERCONDUCTOR
symbol: 
aliases: ["Dual Meissner effect", "Center-vortex condensate vacuum"]
parents: [`DYNA-COLOR-001`]
children: [`MATH-YM-003`, `XXP-EWQCD-EXP`]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DYNA-COLOR-001
      lines: "§4"
      snippet: |
        Color-electric flux is expelled from the condensed vortex medium (dual Meissner effect); it bundles into tubes.
  editors: [pirouette-ai-textgen]
  review_log: []
triad:
  art: |
    Color is time’s threefold braid. When the strands knot together into a condensed sea of vortices, the world confines color charges with cords of temporal tension.
  law: |
    The vacuum expels color-electric fields into flux tubes with a string tension (`σ`) proportional to the temporal-color frame stiffness (`κ_3`) and inversely proportional to the square of the Γ-coherence length (`ξ_Γ`): `σ ∝ κ_3 / ξ_Γ²`.
  philosophy: |
    This concept mechanizes QCD confinement, reframing a non-perturbative strong force phenomenon as a tangible property of the vacuum medium. It translates the abstract mathematics of gauge theory into the physical language of stiffness, coherence, and condensation, making confinement a calculable consequence of the medium's structure.
pirouette_definition: |
  The physical state of the Pirouette vacuum where condensed (Z₃) center vortices create a medium that exhibits a dual Meissner effect. This medium is impermeable to color-electric fields, forcing them into narrow flux tubes between color sources. The energy per unit length of these tubes is the string tension (`σ`), which materializes the linear, long-range confining potential of the strong force. The magnitude of `σ` is determined by the mechanical properties of the underlying temporal-color frame (`κ_3`) and the Γ-coherence length (`ξ_Γ`).
operational_definition:
  units: Energy/Length (`GeV/fm`) or `GeV²` in natural units.
  symbol_table:
    - name: `σ`
      meaning: String tension; the energy per unit length of a color-flux tube.
      dimensions: `M T⁻²`
      default_range: `~0.18 GeV²` or `~0.9 GeV/fm`
    - name: `κ_3`
      meaning: Effective elastic modulus (stiffness) of the temporal-color frame. Related to the strong coupling constant: `κ_3 = 1/g_s²`.
      dimensions: dimensionless
      default_range: contextual, depends on energy scale `μ`
    - name: `ξ_Γ`
      meaning: Γ-coherence length, setting the scale for the vortex core size and the color-electric field penetration depth.
      dimensions: `L`
      default_range: `~1 fm`
  measurement:
    procedures:
      - name: Lattice Gauge Theory Simulation
        outline: |
          1. Compute the expectation value of large, rectangular Wilson loops `W(R, T)` on a Euclidean spacetime lattice.
          2. Extract the static quark-antiquark potential `V(R)` from the long-time behavior: `V(R) = -lim(T→∞) (1/T) ln⟨W(R,T)⟩`.
          3. Fit the potential at large separation `R` to the form `V(R) = σR - (π/12R) + C`. The linear coefficient is `σ`.
        expected_signals: ["A potential `V(R)` that grows linearly for `R > ~0.5 fm`."]
        pitfalls: ["Finite volume effects.", "Lattice discretization errors.", "Excited state contamination."]
      - name: Hadron Spectroscopy (Regge Trajectories)
        outline: |
          1. Plot the squared mass (`M²`) versus the spin (`J`) for families of light-quark hadrons (e.g., ρ mesons).
          2. For large `J`, these points form a nearly straight line, a Regge trajectory.
          3. The slope of this line, `α'`, is related to the string tension by `α' ≈ 1/(2πσ)`.
        expected_signals: ["Linear `M²` vs `J` plots for hadron families."]
        pitfalls: ["String breaking effects at large distances.", "Deviations from the simple relativistic string model."]
context_windows:
  - module: DYNA-COLOR-001
    excerpt: |
      The center of SU(3) is (Z_3). Temporal-color frames admit center-valued holonomies; spatial loops can trap a center phase → center vortices. When these vortices condense, Wilson loops in representations with nonzero N-ality obey an area law... Color-electric flux is expelled from the condensed vortex medium (dual Meissner effect); it bundles into tubes.
  - module: DYNA-COLOR-001
    excerpt: |
      With (g_s) fixed at (M_Z) and run to a matching scale (\mu_\ast), the string tension (\sigma) becomes a function of the Γ-coherence length (\xi_\Gamma) alone. Hadron Regge slopes, given by (\alpha' \sim (2\pi\sigma)^{-1}), are predicted to have small, coherent shifts if (\xi_\Gamma) drifts cosmologically. Heavy-quark potentials calibrated to (\sigma) inherit the same scaling.
poetic_connections:
  motifs: [`vortex condensate`, `flux tube`, `expelled field`, `temporal tension`, `Meissner effect`]
  evocative_lines:
    - "Color is time’s threefold braid."
    - "...pulls quarks together with cords of temporal tension."
  association_matrix:
    - [ "CENTER_VORTEX", 0.9 ]
    - [ "STRING_TENSION", 0.9 ]
    - [ "CONFINEMENT", 1.0 ]
    - [ "TEMPORAL_COLOR_FRAME", 0.7 ]
formal_mappings:
  candidates:
  adopted:
    - target: Dual superconductor model of confinement ('t Hooft-Mandelstam picture)
      domain: QFT
      mapping_kind: conceptual
      equation_hint: |
        `⟨W(C)⟩ ~ exp(-σ Area(C))` (Area Law) implies condensation of chromo-magnetic monopoles (or Z_N vortices) in the vacuum.
      justification: |
        The Pirouette model provides a specific mechanical origin for the dual superconductor vacuum. It identifies the condensing topological defects as Z_3 center vortices arising from the temporal-color frame, and it maps the resulting string tension (`σ`) to the medium's stiffness (`κ_3`) and coherence length (`ξ_Γ`). This aligns directly with the established QFT picture where a magnetic condensate confines electric charges.
      references:
        - title: "A property of electric and magnetic flux in a non-abelian gauge theory"
          where: "Nucl. Phys. B 156, 426 (1979)"
          date: 1979-01-01
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The QCD vacuum confines color via center-vortex condensation, leading to an area law for Wilson loops of non-zero N-ality."
      domain: theory
      falsifier: "Lattice simulations demonstrating that removing center vortices from gauge configurations eliminates the string tension is shown to be an artifact, or that another mechanism (e.g., monopoles) is the dominant driver without a link to vortices."
      status: supported
      links: [`DYNA-COLOR-001`]
    - statement: "The string tension scales with Pirouette's mechanical parameters as `σ ∝ κ_3 / ξ_Γ²`."
      domain: theory
      falsifier: "Lattice simulations with controlled deformations (e.g., anisotropic lattices mapping to stiffness shifts) reveal a scaling law for `σ` inconsistent with this relation across a reasonable parameter space."
      status: proposed
      links: [`DYNA-COLOR-001`, `XXP-EWQCD-EXP`]
naming_notes:
  collisions: []
  disambiguation: |
    Refers to a *dual* (Type-II) superconductor, where the roles of electric and magnetic fields and charges are interchanged relative to an ordinary electronic superconductor. In this model, the vacuum is a condensate of chromo-magnetic defects (center vortices) which confines color-*electric* flux, whereas a standard superconductor is a condensate of electric charges (Cooper pairs) which confines magnetic flux (Meissner effect).
crosslinks:
  near_synonyms: []
  antonyms: [`DECONFINED_PHASE`, `PERTURBATIVE_VACUUM`]
  prerequisites: [`TEMPORAL_COLOR_FRAME`, `CENTER_VORTEX`]
  downstream_effects: [`STRING_TENSION`, `CONFINEMENT`, `K_STRING_HIERARCHY`]
license: CC-BY-SA-4.0