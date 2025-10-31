---
term: "Quartic Coefficient"
canonical_id: "QUARTIC_COEFFICIENT"
symbol: "β"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DYNA-HIGGS-001_higgs_as_triad_clock_alignment"]
---

---
term: Quartic Coefficient
canonical_id: QUARTIC_COEFFICIENT_BETA
symbol: β
aliases: [Higgs self-coupling, frame anharmonicity coefficient]
parents: [DYNA-HIGGS-001_higgs_as_triad_clock_alignment, DYNA-WEAK-001, MATH-Γ-007]
children: [DYNA-Γ-004, MATH-YM-002, XXP-EWQCD-EXP]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DYNA-HIGGS-001_higgs_as_triad_clock_alignment
      lines: "§3.2"
      snippet: |
        (\beta>0) arises from **frame-alignment anharmonicity** (stiffness saturation) and ensures stability.
  editors: [auto-agent]
  review_log: []
triad:
  art: |
    The resistance of a spring as it nears full compression. It's the stiffening that prevents the temporal frames from collapsing into one another, providing a stable bottom for the potential well and forming the brim of the Mexican hat.
  law: |
    The coefficient β of the |H|⁴ term in the Higgs potential V(H) is positive definite (β > 0) and directly sets the Higgs boson mass via m_H² = 2βv². It is determined by the anharmonicity of the SU(2)L–U(1)Y frame alignment energy.
  philosophy: |
    β provides the stability for electroweak symmetry breaking. Without it, the negative curvature from Γ-pressure (α < 0) would create an unstable runaway potential. β is the necessary counterbalance, the "floor" that makes the Higgs VEV finite and the universe stable.
pirouette_definition: |
  The positive, dimensionless coefficient of the quartic term (|H|⁴) in the Higgs potential, V(H). In Pirouette, β originates from the anharmonicity in the alignment energy functional of the SU(2)L triad and U(1)Y clock frames. It represents a saturation of the alignment stiffness, ensuring the potential is bounded from below and stabilizing the electroweak vacuum.
operational_definition:
  units: Dimensionless (in natural units)
  symbol_table:
    - name: β
      meaning: Quartic coefficient of the Higgs potential.
      dimensions: dimensionless
      default_range: ~0.13
    - name: H
      meaning: Higgs field (complex bi-fundamental aligner).
      dimensions: M L² T⁻² (Energy)
      default_range: contextual
    - name: v
      meaning: Higgs vacuum expectation value.
      dimensions: M L² T⁻² (Energy)
      default_range: ~246 GeV
    - name: m_H
      meaning: Higgs boson mass.
      dimensions: M L² T⁻² (Energy)
      default_range: ~125 GeV
  measurement:
    procedures:
      - name: Indirect determination via mass and VEV
        outline: |
          Measure the Higgs boson mass (m_H) via its decay products (e.g., γγ, ZZ*) at the LHC. Measure the electroweak scale (v) from W/Z boson masses or Fermi's constant. Calculate β using the relation β = m_H² / (2v²).
        expected_signals: [Higgs resonance at ~125 GeV, W/Z masses at ~80/91 GeV]
        pitfalls: [Requires precise independent measurements of m_H and v, assumes tree-level SM relation holds to a high degree.]
      - name: Direct measurement via self-coupling
        outline: |
          Measure the di-Higgs production cross-section (e.g., gg→HH) at a high-luminosity collider (HL-LHC, FCC-ee). This cross-section is sensitive to the trilinear Higgs coupling (λ₃), which is directly proportional to β and v. Extract β from a fit to λ₃ = 3βv.
        expected_signals: [An excess of di-Higgs events over background, with a rate consistent with SM predictions modified by percent-level Pirouette corrections.]
        pitfalls: [Extremely small cross-section and large backgrounds, making the measurement statistically challenging. Disentangling Pirouette deviations from other new physics effects.]
context_windows:
  - module: DYNA-HIGGS-001_higgs_as_triad_clock_alignment
    excerpt: |
      Let (K_2!=!1/g^2) (triad stiffness) and (K_1!=!1/g'^2) (clock stiffness). The *misalignment* angle costs energy. Promoting (θ) to a complex 2-component order parameter with the correct gauge action gives the **quadratic** and **quartic** pieces of (V(H)) with *positive* coefficients at zero Γ.
  - module: DYNA-HIGGS-001_higgs_as_triad_clock_alignment
    excerpt: |
      Minimization gives |H|² = -α(Γ) / (2β) ≡ v²/2, and m_H² = 2βv². Interpretation: (\alpha(\Gamma)) crossing zero is a **second-order bifurcation** driven by temporal pressure. (\beta>0) arises from **frame-alignment anharmonicity** (stiffness saturation) and ensures stability.
poetic_connections:
  motifs: [stiffness saturation, anharmonicity, stability, potential floor, brim of the hat]
  evocative_lines:
    - "(\beta>0) arises from **frame-alignment anharmonicity** (stiffness saturation) and ensures stability."
    - "The Mexican hat is the geometry of that decision."
  association_matrix:
    - [ "Quadratic Coefficient (α)", 0.9 ]
    - [ "Higgs VEV (v)", 0.8 ]
    - [ "Frame Stiffness (K)", 0.7 ]
formal_mappings:
  candidates: []
  adopted:
    - target: λ_SM, the Standard Model Higgs self-coupling constant
      rationale: |
        The coefficient β is mathematically and operationally identical to the SM self-coupling λ_SM in the potential V(H) ⊃ λ|H|⁴. Both parameters are positive, dimensionless, ensure vacuum stability, and relate the Higgs mass to its VEV. The Pirouette framework provides a physical origin for this term (frame anharmonicity), but its role in the effective potential is the same.
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "β is positive definite and its magnitude is determined by the anharmonic terms of the SU(2)L–U(1)Y frame alignment energy."
      domain: theory
      falsifier: "Experimental evidence of vacuum instability (β ≤ 0), or a confirmed measurement of β that is fundamentally inconsistent with an origin tied to the SU(2)xU(1) gauge structure."
      status: proposed
      links: [DYNA-HIGGS-001_higgs_as_triad_clock_alignment]
    - statement: "The value of β is quantitatively linked to the frame stiffness ratio (ρ_stiff) that also sets the weak mixing angle, sin²θ_W."
      domain: phenomenology
      falsifier: "A joint experimental fit of the Higgs trilinear coupling (λ₃ ∝ βv) and the weak mixing angle (sin²θ_W) shows a statistically significant deviation from the correlated relationship predicted by the frame alignment model."
      status: proposed
      links: [DYNA-HIGGS-001_higgs_as_triad_clock_alignment]
naming_notes:
  collisions: [The symbol β is common in physics (relativistic velocity, β-functions, thermodynamic beta). Context is required.]
  disambiguation: |
    Within Pirouette's electroweak dynamics, β always refers to the Higgs quartic coefficient. It is often used interchangeably with the Standard Model symbol λ. When discussing renormalization group flow, the term "beta function" (e.g., β_g) will be used explicitly.
crosslinks:
  near_synonyms: [HIGGS_SELF_COUPLING_LAMBDA]
  antonyms: [QUADRATIC_COEFFICIENT_ALPHA]
  prerequisites: [FRAME_STIFFNESS_K, HIGGS_AS_ALIGNER]
  downstream_effects: [HIGGS_MASS_MH, HIGGS_VEV_V, ELECTROWEAK_PHASE_TRANSITION]
license: CC-BY-SA-4.0
---

# Quartic Coefficient (β)

## Canonical (Pirouette)
The positive, dimensionless coefficient of the quartic term (|H|⁴) in the Higgs potential, V(H). In Pirouette, β originates from the anharmonicity in the alignment energy functional of the SU(2)L triad and U(1)Y clock frames. It represents a saturation of the alignment stiffness, ensuring the potential is bounded from below and stabilizing the electroweak vacuum.

## EFT-First Summary
The coefficient β is the Pirouette equivalent of the Standard Model Higgs self-coupling constant, λ, in the potential V(H) = -μ²|H|² + λ|H|⁴. It is a positive, dimensionless parameter that stabilizes the electroweak vacuum. In Pirouette, its physical origin is the anharmonicity of the alignment energy between the SU(2)L and U(1)Y temporal frames, providing a direct link between the value of β (and thus the Higgs mass) and the gauge coupling constants g and g'.

## Glossary Links
- See also: [Quadratic Coefficient (α)](...), [Higgs VEV (v)](...), [Frame Stiffness (K)](...)