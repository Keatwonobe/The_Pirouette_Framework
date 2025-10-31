---
term: "Quadratic Coefficient"
canonical_id: "QUADRATIC_COEFFICIENT"
symbol: "α(Γ)"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DYNA-HIGGS-001_higgs_as_triad_clock_alignment"]
---

---
term: Quadratic Coefficient
canonical_id: QUADRATIC_COEFFICIENT_ALPHA
symbol: α(Γ)
aliases: [Effective Mass-Squared, Higgs Mass Parameter, Curvature Parameter]
parents: [DYNA-HIGGS-001_higgs_as_triad_clock_alignment]
children: [DYNA-Γ-004, MATH-YM-002, XXP-EWQCD-EXP]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DYNA-HIGGS-001_higgs_as_triad_clock_alignment
      lines: "L25-L28"
      snippet: |
        Couple the aligner to Γ as required by Pirouette symmetry (pressure–density cross-term):
        [
        \mathcal{L}*{\rm int}=\lambda*{H\Gamma},(H^\dagger H),\Gamma^2 \quad \Rightarrow\quad
        \alpha(\Gamma)=\alpha_0-\lambda_{H\Gamma},\langle\Gamma^2\rangle .
        ]
  editors: [system]
  review_log: []
triad:
  art: |
    The tuning peg of the Higgs potential, turned by the pressure of the Γ sea. Its crossing of zero is the moment the string begins to resonate, giving mass its voice.
  law: |
    The quadratic coefficient α(Γ) is the sum of a positive bare stiffness (α₀) from frame alignment and a negative temporal-pressure softening (−λ_{HΓ}⟨Γ²⟩). A negative value (α(Γ) < 0) is the necessary and sufficient condition for electroweak symmetry breaking, setting the vacuum expectation value v² = -α(Γ)/β.
  philosophy: |
    α(Γ) promotes the Higgs mass from a fundamental input parameter into a dynamical output of the Γ-background. It embodies the principle that scales are not set by fiat but emerge from the competitive dynamics of underlying fields, making the electroweak scale calculable and falsifiable.
pirouette_definition: |
  The Γ-dependent coefficient of the `|H|²` term in the Higgs effective potential, `V(H)`. It represents the net curvature of the potential at the origin and functions as the control parameter for the electroweak phase transition. It is composed of two competing terms: a positive, Γ-independent component `α₀` arising from the bare alignment stiffness of the SU(2)L triad and U(1)Y clock frames, and a negative, "softening" component `-λ_{HΓ}⟨Γ²⟩` induced by the temporal pressure background. The sign of α(Γ) dictates the symmetry phase: α > 0 corresponds to an unbroken phase with a trivial vacuum (⟨H⟩=0), while α < 0 triggers a pitchfork bifurcation, leading to a non-zero Higgs vev and consequently, massive electroweak gauge bosons.
operational_definition:
  units: Energy² (typically GeV²)
  symbol_table:
    - name: α(Γ)
      meaning: The full, Γ-dependent quadratic coefficient.
      dimensions: M²L⁴T⁻⁴ (Energy²)
      default_range: ≈ -(88 GeV)²
    - name: α₀
      meaning: The bare, positive stiffness component, independent of Γ.
      dimensions: M²L⁴T⁻⁴ (Energy²)
      default_range: contextual, > 0
    - name: λ_{HΓ}
      meaning: Coupling constant between the Higgs bilinear and Γ-squared.
      dimensions: dimensionless
      default_range: contextual
    - name: ⟨Γ²⟩
      meaning: Vacuum expectation value of Γ-squared, a measure of temporal pressure variance.
      dimensions: M²L⁴T⁻⁴ (Energy²)
      default_range: contextual
  measurement:
    procedures:
      - name: Indirect inference from Higgs and Electroweak observables
        outline: |
          α(Γ) is not a direct observable. It is inferred from measurements of the Higgs vacuum expectation value `v` and the Higgs mass `m_H`.
          1. Measure `v` (≈ 246.22 GeV) from electroweak precision observables (e.g., muon lifetime, W/Z masses).
          2. Measure `m_H` (≈ 125 GeV) from collider experiments (e.g., H→γγ, H→4l).
          3. Infer the Higgs quartic coupling `β = m_H² / (2v²)`.
          4. Reconstruct the quadratic coefficient via the relation `α(Γ) = -βv² = -m_H²/2`.
        expected_signals: [Correlated variations in `v`, `m_H`, and Higgs self-couplings (`λ₃`, `λ₄`), which would imply a change in the underlying `α(Γ)` driven by a change in `⟨Γ²⟩`.]
        pitfalls: [Assuming the quartic coupling `β` is constant or unaffected by the same new physics that might shift `α(Γ)`. Disentangling a shift in `α` from a shift in `β` requires additional observables like the trilinear Higgs coupling.]
context_windows:
  - module: DYNA-HIGGS-001_higgs_as_triad_clock_alignment
    excerpt: |
      Here (α_0!\propto!k_{\rm eff}>0) encodes the bare alignment stiffness; the Γ background **reduces** curvature. When (\langle\Gamma^2\rangle) exceeds a threshold,
      [
      \alpha(\Gamma_c)=0 ;\Rightarrow; \text{bifurcation point (Mexican hat forms)}.
      ]
  - module: DYNA-HIGGS-001_higgs_as_triad_clock_alignment
    excerpt: |
      *Interpretation:*
      * (\alpha(\Gamma)) crossing zero is a **second-order bifurcation** (pitchfork) driven by temporal pressure—**the origin of symmetry breaking**.
      * (\beta>0) arises from **frame-alignment anharmonicity** (stiffness saturation) and ensures stability.
poetic_connections:
  motifs: [bifurcation, softening, tuning, resonance, tipping point]
  evocative_lines:
    - "the Γ background **reduces** curvature."
    - "The Mexican hat is the geometry of that decision."
  association_matrix:
    - [ "Temporal Pressure (Γ)", 0.9 ]
    - [ "Frame Stiffness", 0.8 ]
    - [ "Bifurcation", 0.9 ]
formal_mappings:
  candidates:
    - target: Tachyonic mass
      domain: QFT
      mapping_kind: conceptual
      justification: |
        When α(Γ) < 0, it behaves as a negative mass-squared term, indicating an instability at the origin of the potential, which is the definition of a tachyonic field. This instability is what drives the condensation of the Higgs field to a non-zero vacuum expectation value.
      confidence: 0.8
  adopted:
    - target: SM Higgs Mass Parameter `μ²`
      domain: SM
      mapping_kind: mathematical
      equation_hint: |
        V(H) = μ²|H|² + λ|H|⁴  ↔  V(H) = α(Γ)|H|² + β|H|⁴
      rationale: |
        α(Γ) occupies the identical mathematical position as the Standard Model's quadratic coefficient `μ²`. The crucial distinction is that in the SM, `μ²` is a free, negative parameter set by hand to fit data, whereas in Pirouette, α(Γ) is a derived, dynamical quantity whose negative value is physically caused by the Γ background.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The value of α(Γ) is determined by a balance between positive frame stiffness `α₀` (related to `g, g'`) and negative Γ-pressure softening `-λ_{HΓ}⟨Γ²⟩`."
      domain: theory
      falsifier: "Evidence that the Higgs potential's quadratic term is fundamental and not composed of competing influences, or that the Γ-field interaction has the wrong sign (i.e., it stiffens the potential)."
      status: proposed
      links: [DYNA-HIGGS-001_higgs_as_triad_clock_alignment]
    - statement: "All variations in the electroweak scale (`v`) and Higgs mass (`m_H`) are correlated through the relation `m_H² = -2α(Γ)`."
      domain: experiment
      falsifier: "An observation of incoherent shifts in `v` and `m_H` that cannot be explained by a single underlying change `Δα`. For example, a cosmological change in `v` without a corresponding change in `m_H`."
      status: proposed
      links: [XXP-EWQCD-EXP]
    - statement: "Deviations in the Higgs trilinear coupling (`λ₃`) from its SM value are tied to the same parameters (`λ_{HΓ}`, `ρ_stiff`) that determine the electroweak mixing angle."
      domain: phenomenology
      falsifier: "A measurement of `Δλ₃` at the HL-LHC or a future collider that is quantitatively inconsistent with the value predicted from a joint fit to `sin²θ_W` and other electroweak precision data within the Pirouette framework."
      status: proposed
      links: [DYNA-HIGGS-001_higgs_as_triad_clock_alignment]
naming_notes:
  collisions: [α (fine-structure constant), α (generic coefficient)]
  disambiguation: |
    To avoid ambiguity, this term should always be written as α(Γ) to emphasize its dependence on the Γ-field. It is the coefficient of the quadratic `|H|²` term, not the quartic `|H|⁴` term (which is β). It is the *net* coefficient, distinct from its positive bare component, α₀.
crosslinks:
  near_synonyms: [HIGGS_MASS_PARAMETER_MU_SQUARED]
  antonyms: [QUARTIC_COEFFICIENT_BETA]
  prerequisites: [TEMPORAL_PRESSURE_GAMMA, FRAME_STIFFNESS]
  downstream_effects: [HIGGS_VEV_V, HIGGS_MASS_MH, W_Z_BOSON_MASSES]
license: CC-BY-SA-4.0
---

# Quadratic Coefficient

## Canonical (Pirouette)
The Γ-dependent coefficient of the `|H|²` term in the Higgs effective potential, `V(H)`. It represents the net curvature of the potential at the origin and functions as the control parameter for the electroweak phase transition. It is composed of two competing terms: a positive, Γ-independent component `α₀` arising from the bare alignment stiffness of the SU(2)L triad and U(1)Y clock frames, and a negative, "softening" component `-λ_{HΓ}⟨Γ²⟩` induced by the temporal pressure background. The sign of α(Γ) dictates the symmetry phase: α > 0 corresponds to an unbroken phase with a trivial vacuum (⟨H⟩=0), while α < 0 triggers a pitchfork bifurcation, leading to a non-zero Higgs vev and consequently, massive electroweak gauge bosons.

## EFT-First Summary
In the language of the Standard Model (SM) Effective Field Theory, α(Γ) is the Higgs mass parameter, `μ²`. The Pirouette Framework provides a dynamical origin for this parameter, which is otherwise a fundamental input in the SM. The relation `α(Γ) = α₀ - λ_{HΓ}⟨Γ²⟩` asserts that the observed negative value of `μ²` (≈ -(88 GeV)²) is not fundamental, but the result of a "softening" effect from a background field Γ, which overcomes a positive bare stiffness `α₀`. This makes the electroweak scale a calculable output of the theory rather than an input, linking it to the dynamics of the Γ-field.

## Glossary Links
- See also: [Temporal Pressure (Γ)](...), [Frame Stiffness](...), [Higgs VEV (v)](...), [Quartic Coefficient (β)](...)