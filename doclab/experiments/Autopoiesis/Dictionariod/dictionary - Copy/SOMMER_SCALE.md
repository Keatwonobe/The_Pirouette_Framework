---
term: "Sommer scale"
canonical_id: "SOMMER_SCALE"
symbol: "r₀"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-YM-003_nonperturbative_map"]
---

---
term: Sommer scale
canonical_id: SOMMER_SCALE
symbol: r₀
aliases: [static force scale]
parents: [MATH-YM-003]
children: [XXP-EWQCD-EXP]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-YM-003
      lines: "L60-L63"
      snippet: |
        * **Sommer scale (r_0)** via
          [
          r_0^2,F(r_0)=1.65,\qquad F(R)=\frac{dV}{dR}.
          ]
  editors: [System Agent (GPT-4 based)]
  review_log: []
triad:
  art: |
    A length carved from the constant pull of the void; the distance at which two captive quarks feel the universe's standard tension, defining a yardstick for the strong force.
  law: |
    The Sommer scale r₀ is the static quark-antiquark separation R where the inter-quark force F(R) satisfies the condition R²F(R) = 1.65. Any valid theory of confinement must reproduce this scale, linking the fundamental string tension σ to r₀ via r₀ ≈ √(1.65/σ).
  philosophy: |
    Provides a robust, scheme-independent physical length to set the scale of nonperturbative QCD. It anchors the abstract lattice grid to the physical world of femtometers, serving as the primary Rosetta Stone for converting dimensionless lattice results into predictions for hadronic masses and sizes.
pirouette_definition: |
  A derived reference length, determined by the framework's fundamental string tension (σ). It is the quark-antiquark separation distance where the force—itself a consequence of temporal frame stiffness (κ₃) and Γ-coherence (ξΓ)—reaches the conventional value F(r₀) = 1.65/r₀². The Sommer scale thus serves as a primary, calculable bridge from Pirouette's mechanical parameters to lattice units.
operational_definition:
  units: Length (fm, GeV⁻¹)
  symbol_table:
    - name: r₀
      meaning: Sommer scale
      dimensions: L
      default_range: ~0.5 fm
    - name: F(R)
      meaning: Force between static quarks at separation R
      dimensions: MLT⁻²
      default_range: contextual
    - name: V(R)
      meaning: Potential energy of static quarks at separation R
      dimensions: ML²T⁻²
      default_range: contextual
    - name: σ
      meaning: Fundamental string tension
      dimensions: MLT⁻²
      default_range: ~0.2 GeV² (or ~440 MeV/fm)
  measurement:
    procedures:
      - name: Lattice Wilson Loop Extraction
        outline: |
          1. Compute expectation values of large, rectangular Wilson loops `W(R,T)` on a Euclidean lattice ensemble.
          2. For large temporal extent T, extract the static quark potential via the decay `⟨W(R,T)⟩ ∝ exp[-V(R)T]`.
          3. Numerically differentiate the potential `V(R)` to obtain the force `F(R) = dV/dR`.
          4. Numerically solve the implicit equation `R²F(R) = 1.65` for `R`. The solution is `r₀` in lattice units (`r₀/a`).
        expected_signals: [Exponential decay of Wilson loop `⟨W(R,T)⟩` with `T`, Potential `V(R)` that is Coulomb-like at short distance and linear (`σR`) at long distance.]
        pitfalls: [Excited state contamination for small `T`, Discretization errors at small `R`, Statistical noise overwhelming the signal at large `R`.]
context_windows:
  - module: MATH-YM-003
    excerpt: |
      **Reference scales:**

      * **Sommer scale (r_0)** via
        [
        r_0^2,F(r_0)=1.65,\qquad F(R)=\frac{dV}{dR}.
        ]
      * **Gradient-flow (t_0):** (t^2\langle E\rangle!\mid_{t=t_0}=0.3) (or chosen constant).

      **Conversions (deterministic once (\sigma) fixed):**
      [
      r_0 = \sqrt{\frac{1.65}{\sigma + \pi/(12 r_0^2)}}
      ;\approx; \sqrt{\frac{1.65}{\sigma}};\Big(1+\mathcal{O}(\sqrt{\sigma})\Big),
      ]
  - module: MATH-YM-003
    excerpt: |
      **Worked deterministic recipe (step-by-step)**
      ...
      4. **Predict** (\sigma = c_\sigma \kappa_3/\xi_\Gamma^2).
      5. **Derive** (r_0,t_0); **predict** lattice spacing (a) for any measured ((r_0/a)) or ((t_0/a^2)).
      6. **Integrate** β to get (\Lambda_{\overline{\rm MS}}) and **check** (\alpha_s(M_Z)) via standard running.
poetic_connections:
  motifs: [reference scale, yardstick, confinement force, standard tension]
  evocative_lines:
    - "stiffness sets the strings, coherence sets the drum skin, and out comes σ."
    - "every lattice number has a seat in the hall—and every seat points back to the same temporal instrument."
  association_matrix:
    - [ "STRING_TENSION", 0.9 ]
    - [ "LATTICE_SPACING", 0.8 ]
    - [ "GRADIENT_FLOW_SCALE", 0.7 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Sommer scale r₀
      domain: Lattice QCD
      mapping_kind: operational
      equation_hint: |
        r₀² F(r₀) = 1.65, where F(R) = dV(R)/dR
      justification: |
        The Pirouette Framework adopts the standard lattice QCD definition of r₀ without modification. This definition provides a physical scale from the heavy quark potential that is less sensitive to short-distance physics than other scales, making it a robust choice for setting the absolute scale of simulations.
      references:
        - title: A new way to set the scale in lattice gauge theories and its applications to the static force and alpha_s in SU(2) Yang-Mills theory
          where: Nucl. Phys. B 411 (1994) 839-854
          date: 1994-01-01
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "The value of the Sommer scale r₀ is a deterministic consequence of the temporal-color frame stiffness (κ₃) and Γ-coherence length (ξΓ), via the relation r₀ ≈ √(1.65/σ) where σ ∝ κ₃/ξΓ²."
      domain: phenomenology
      falsifier: "After a single, one-time normalization, lattice QCD simulations yield values for r₀ and σ that show a statistically significant deviation from the predicted Pirouette scaling relation across multiple ensembles."
      status: proposed
      links: [MATH-YM-003]
naming_notes:
  collisions: [The symbol `r` with a subscript is common for radii in physics (e.g., Bohr radius `a₀`, classical electron radius `rₑ`). The context of nonperturbative QCD is typically sufficient for disambiguation.]
  disambiguation: |
    Distinguish `r₀` from other lattice reference scales like `t₀` (from gradient flow) or scales derived from hadron masses (e.g., `1/m_ρ`). While physically correlated, they have different systematic uncertainties and probe different aspects of the underlying dynamics. `r₀` is defined directly from the static quark force.
crosslinks:
  near_synonyms: [GRADIENT_FLOW_SCALE]
  antonyms: [LAMBDA_QCD]
  prerequisites: [STRING_TENSION]
  downstream_effects: [LATTICE_SPACING, HADRON_MASSES]
license: CC-BY-SA-4.0
---

# Sommer scale

## Canonical (Pirouette)
A derived reference length, determined by the framework's fundamental string tension (σ). It is the quark-antiquark separation distance where the force—itself a consequence of temporal frame stiffness (κ₃) and Γ-coherence (ξΓ)—reaches the conventional value F(r₀) = 1.65/r₀². The Sommer scale thus serves as a primary, calculable bridge from Pirouette's mechanical parameters to lattice units.

## EFT-First Summary
The Sommer scale `r₀` is a standard reference length in lattice QCD, used to set the absolute scale of simulations and convert dimensionless lattice results into physical units like femtometers or MeV. It is defined implicitly as the distance between two static quarks where the force between them reaches a specific, conventional value. Its robustness against short-distance artifacts makes it a reliable observable for connecting theoretical calculations to hadronic phenomenology.

## Glossary Links
- See also: String Tension (σ), Lattice Spacing (a), Gradient Flow Scale (t₀)