---
term: "Temporal Triad"
canonical_id: "TEMPORAL_TRIAD"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DYNA-HIGGS-001_higgs_as_triad_clock_alignment"]
---

---
term: Temporal Triad
canonical_id: TEMPORAL_TRIAD
symbol: SU(2)L
aliases: [SU(2) Frame, Weak Isospin Frame]
parents: [DYNA-WEAK-001, MATH-YM-001]
children: [DYNA-HIGGS-ORIG-001, MATH-YM-002, DYNA-Γ-004]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DYNA-HIGGS-001_higgs_as_triad_clock_alignment
      lines: "§2.1-2.2"
      snippet: |
        Treat the Higgs as the minimal aligner between the triad and clock frames...
        Let (K_2!=!1/g^2) (triad stiffness) and (K_1!=!1/g'^2) (clock stiffness). The *misalignment* angle costs energy...
  editors: [AI Assistant]
  review_log: []
triad:
  art: |
    A three-pronged scaffold within the temporal substrate, providing the directional axes against which the rhythms of electroweak change are measured. It is one of the two fundamental tunings of time's internal clockwork.
  law: |
    The Temporal Triad is a dynamical SU(2) frame whose dynamics are governed by a stiffness K₂ = 1/g². Its misalignment relative to the U(1) Clock costs energy, sourcing the positive curvature of the Higgs potential. This stiffness is softened by temporal pressure (Γ), driving the condensation that sets the electroweak scale.
  philosophy: |
    The Triad reframes the weak interaction not as a force mediated by abstract particles, but as a geometric feature of the temporal substrate. It posits that 'isospin' is an internal rotational degree of freedom in the flow of time, and its locking into a specific orientation gives the universe a stable electroweak vacuum.
pirouette_definition: |
  The Temporal Triad is the SU(2)L component of the dynamical frame of the temporal substrate. It is characterized by a dimensionless stiffness, K₂, which is physically manifest as the inverse squared gauge coupling (K₂ = 1/g²). The Higgs field is the order parameter that measures the relative alignment between the Temporal Triad and the U(1) Temporal Clock, and the dynamics of this alignment, under softening from temporal pressure Γ, constitute the Higgs mechanism.
operational_definition:
  units: Dimensionless frame orientation
  symbol_table:
    - name: SU(2)L
      meaning: The Temporal Triad itself; a dynamical frame.
      dimensions: dimensionless
      default_range: N/A
    - name: K₂
      meaning: Stiffness of the Temporal Triad frame.
      dimensions: dimensionless
      default_range: ~2.37 (at electroweak scale)
    - name: g
      meaning: Coupling constant associated with Triad dynamics.
      dimensions: dimensionless
      default_range: ~0.65 (at electroweak scale)
    - name: Waμ
      meaning: Gauge fields mediating changes in the Triad's orientation.
      dimensions: M¹L¹T⁻¹Q⁻¹ (in natural units M¹)
      default_range: contextual
  measurement:
    procedures:
      - name: Triad Stiffness Inference
        outline: |
          1. Measure the W boson mass (m_W) and the Higgs vacuum expectation value (v ≈ 246 GeV) via precision electroweak and Higgs measurements.
          2. Calculate the SU(2)L gauge coupling using the tree-level relation g = 2m_W/v.
          3. Infer the Triad stiffness as K₂ = 1/g².
          4. Cross-validate this value against measurements of the weak mixing angle and Higgs potential shape, which depend on the stiffness ratio K₂/K₁.
        expected_signals: [W boson mass, g_V/g_A from neutron decay, sin²θ_W, Higgs trilinear coupling]
        pitfalls: [Dependence on tree-level relations that require radiative corrections, Ambiguity from new physics affecting precision observables]
context_windows:
  - module: DYNA-HIGGS-001_higgs_as_triad_clock_alignment
    excerpt: |
      The Higgs field (H) is the **complex bi-fundamental aligner** of the SU(2)(_L) temporal triad and the U(1)(_Y) clock; its potential arises from the **competition** between (i) *frame-alignment energy* (positive curvature) and (ii) *temporal-pressure softening* from Γ (negative curvature). When (α(Γ)!<!0), alignment condenses ((⟨H⟩≠0))—this is the Higgs mechanism.
  - module: DYNA-HIGGS-001_higgs_as_triad_clock_alignment
    excerpt: |
      Let (K_2!=!1/g^2) (triad stiffness) and (K_1!=!1/g'^2) (clock stiffness). The *misalignment* angle costs energy. Promoting (θ) to a complex 2-component order parameter with the correct gauge action gives the **quadratic** and **quartic** pieces of (V(H)) with *positive* coefficients at zero Γ.
poetic_connections:
  motifs: [frame stiffness, temporal tuning, geometric key, alignment energy]
  evocative_lines:
    - "The Higgs is not an add-on—it’s how time chooses a key."
    - "The triad and clock tune the chords..."
  association_matrix:
    - [ "TEMPORAL_CLOCK", 0.9 ]
    - [ "HIGGS_FIELD", 0.9 ]
    - [ "FRAME_STIFFNESS", 0.8 ]
    - [ "TEMPORAL_PRESSURE", 0.7 ]
formal_mappings:
  candidates: []
  adopted:
    - target: SU(2)L gauge symmetry
      domain: SM
      mapping_kind: mathematical|conceptual
      equation_hint: |
        Dμ = ∂μ - i g Wμa (σa/2)
      rationale: |
        This is a foundational mapping in Pirouette, re-grounding the electroweak sector in the dynamics of a temporal substrate. The Triad is the physical origin of the Standard Model's SU(2)L gauge group. The mapping is mathematically exact at the Lagrangian level, with the Triad's stiffness K₂ identified with the inverse squared gauge coupling 1/g², providing a physical origin for the gauge structure.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The ratio of Triad stiffness to Clock stiffness, ρ_stiff = K₂/K₁, simultaneously determines the weak mixing angle (sin²θ_W) and contributes to the shape of the Higgs potential V(H)."
      domain: theory|phenomenology
      falsifier: "A joint fit of electroweak precision observables (determining sin²θ_W) and Higgs self-couplings (λ₃, λ₄) yields inconsistent values for the underlying stiffness parameters (K₁, K₂), falsifying the shared origin."
      status: proposed
      links: [DYNA-HIGGS-001_higgs_as_triad_clock_alignment]
    - statement: "The Temporal Triad's inherent alignment energy with the Temporal Clock provides the positive (m² > 0) quadratic term for the Higgs potential, which is then driven negative by temporal pressure Γ."
      domain: theory
      falsifier: "Experimental evidence that the bare quadratic term is negative, or that increasing Γ-variance *increases* the potential's curvature at the origin, would contradict the pressure-softening postulate."
      status: proposed
      links: [DYNA-HIGGS-001_higgs_as_triad_clock_alignment]
naming_notes:
  collisions: [SU(2) (general group theory), Triad/Dreibein (General Relativity)]
  disambiguation: |
    Distinguish from the 'triad' (or 'dreibein') of General Relativity, which relates local inertial frames to a global coordinate system. The Temporal Triad is an *internal* SU(2) frame within the temporal substrate itself, defining the 'directions' of weak isospin, not a spacetime frame.
crosslinks:
  near_synonyms: [SU2L_FRAME]
  antonyms: [TEMPORAL_CLOCK]
  prerequisites: [TEMPORAL_SUBSTRATE, FRAME_STIFFNESS]
  downstream_effects: [HIGGS_MECHANISM, WEAK_MIXING_ANGLE, W_Z_BOSON_MASS]
license: CC-BY-SA-4.0
---

# Temporal Triad

## Canonical (Pirouette)
The Temporal Triad is the SU(2)L component of the dynamical frame of the temporal substrate. It is characterized by a dimensionless stiffness, K₂, which is physically manifest as the inverse squared gauge coupling (K₂ = 1/g²). The Higgs field is the order parameter that measures the relative alignment between the Temporal Triad and the U(1) Temporal Clock, and the dynamics of this alignment, under softening from temporal pressure Γ, constitute the Higgs mechanism.

## EFT-First Summary
Within the Standard Model Effective Field Theory (SMEFT), the Temporal Triad is the physical reinterpretation of the SU(2)L gauge symmetry group. Its degrees of freedom are the W bosons, and its 'stiffness' K₂ is simply the inverse of the squared gauge coupling, K₂ = 1/g². The Pirouette framework proposes that the origin of the Higgs potential lies in the energy cost of misaligning this SU(2)L frame with the U(1)Y frame (the Temporal Clock), a mechanism that directly links the value of g to the parameters of the Higgs potential before symmetry breaking.

## Glossary Links
- See also: [Temporal Clock](<#>), [Frame Stiffness](<#>), [Higgs Mechanism](<#>)