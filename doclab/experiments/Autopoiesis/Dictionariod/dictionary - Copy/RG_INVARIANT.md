---
term: "RG Invariant"
canonical_id: "RG_INVARIANT"
symbol: "$\mathcal{I}_{\text{mass}}$"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["XAP-006D_unified_mass–curvature_correspondence"]
---

---
term: RG Invariant
canonical_id: RG_INVARIANT
symbol: $\mathcal{I}_{\text{mass}}$
aliases: [Mass-Charge Invariant, Stiffness-Curvature Invariant]
parents: [XAP-006D, MATH-026]
children: [XAP-006E]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: XAP-006D
      lines: "§6"
      snippet: |
        Integrating jointly yields an RG invariant
        \[
        \mathcal{I}_{\text{mass}} =
        \frac{\mathcal{K}_F}{\Gamma_{\mathrm{stiff}}^2}\,
        \Lambda^{-2(c_2-c_1)}
        = \text{const}.
        \]
        This invariant ensures that as the gauge coupling runs, mass and curvature remain proportionally locked...
  editors: [llm-compiler]
  review_log: []
triad:
  art: |
    A golden thread woven through the scales of reality. The roar of a gauge field's curvature must echo in the quiet stiffness of spacetime's fabric, ensuring their dance remains synchronized from the smallest particle to the cosmic horizon.
  law: |
    The ratio of the squared gauge field curvature $\mathcal{K}_F$ to the squared Γ-stiffness $\Gamma_{\mathrm{stiff}}^2$, when properly scaled by the energy cutoff $\Lambda$, is a constant quantity under renormalization group flow. Any change in one is compensated by a change in the other, preserving their fundamental proportionality.
  philosophy: |
    The existence of $\mathcal{I}_{\text{mass}}$ elevates the "mass from curvature" idea from a static correspondence to a dynamic law. It implies that mass and charge are not independent properties but two facets of the same underlying geometric dynamics, co-evolving with energy scale. This provides a deep, non-perturbative link between the Standard Model and the geometric substrate.
pirouette_definition: |
  A dimensionless quantity, constant under renormalization group (RG) flow, that links the τ-averaged Ki-fiber curvature norm ($\mathcal{K}_F$) to the Γ-stiffness ($\Gamma_{\mathrm{stiff}}^2$). Defined as $\mathcal{I}_{\text{mass}} = (\mathcal{K}_F / \Gamma_{\mathrm{stiff}}^2) \cdot \Lambda^{-2(c_2-c_1)}$, where $\Lambda$ is the energy scale and $c_1, c_2$ are beta-function coefficients. Its invariance ensures that the running of particle masses (from stiffness) is proportionally locked to the running of gauge couplings (from fiber curvature).
operational_definition:
  units: dimensionless
  symbol_table:
    - name: $\mathcal{I}_{\text{mass}}$
      meaning: RG Invariant for mass and curvature
      dimensions: dimensionless
      default_range: "constant"
    - name: $\mathcal{K}_F$
      meaning: τ-averaged Ki-fiber curvature norm, $\langle \mathrm{Tr}(F^2) \rangle_\tau$
      dimensions: $M^4 L^{-4}$ (energy density)
      default_range: contextual
    - name: $\Gamma_{\mathrm{stiff}}$
      meaning: Γ-Stiffness, effective mass from coherence field potential
      dimensions: $M$ (energy)
      default_range: 0–100s of GeV
    - name: $\Lambda$
      meaning: Renormalization energy scale cutoff
      dimensions: $M$ (energy)
      default_range: contextual
    - name: $c_1, c_2$
      meaning: Beta function coefficients for stiffness and curvature, respectively
      dimensions: dimensionless
      default_range: "O(1) constants"
  measurement:
    procedures:
      - name: Correlated Running Measurement
        outline: |
          1. In a high-energy particle collider, measure a specific gauge coupling (e.g., $\alpha_s$) and the mass of a related particle (e.g., a vector boson) at a range of interaction energies ($\Lambda$).
          2. Compute the corresponding values of $\mathcal{K}_F$ and $\Gamma_{\mathrm{stiff}}^2$.
          3. Plot $\ln(\mathcal{K}_F / \Gamma_{\mathrm{stiff}}^2)$ against $\ln(\Lambda)$.
          4. The result should be a straight line with a slope of $2(c_2 - c_1)$, confirming that $\mathcal{I}_{\text{mass}}$ is constant.
        expected_signals: [A logarithmic running of particle masses that is precisely correlated with the known running of the associated gauge coupling.]
        pitfalls: [Requires extreme experimental precision; theoretical uncertainties in calculating $c_1, c_2$; separating the effect from other higher-order radiative corrections.]
context_windows:
  - module: XAP-006D
    excerpt: |
      MATH-026 gives $\beta$-functions for both stiffness and gauge curvature. Integrating jointly yields an RG invariant, $\mathcal{I}_{\text{mass}}$. This invariant ensures that as the gauge coupling runs, mass and curvature remain proportionally locked—a quantitative expression of “mass from curvature.”
  - module: XAP-006D
    excerpt: |
      **Mass–Charge Correlation:** Particles with larger fiber curvature (stronger coupling) possess higher stiffness-derived mass.
      **Running Mass Predictions:** As curvature renormalizes with energy, rest masses should shift logarithmically—an avenue for precision tests in high-energy scattering.
poetic_connections:
  motifs: [scale invariance, dynamic equilibrium, co-evolution, geometric lock]
  evocative_lines:
    - "mass and curvature remain proportionally locked"
    - "a quantitative expression of 'mass from curvature'"
  association_matrix:
    - [ "Γ-Stiffness", 0.9 ]
    - [ "Ki-Fiber Curvature", 0.9 ]
    - [ "Renormalization Flow", 0.8 ]
    - [ "Mass-Charge Correlation", 0.7 ]
formal_mappings:
  candidates:
    - target: Scheme-independent RG relation
      domain: SM
      mapping_kind: mathematical
      equation_hint: |
        $\frac{d}{d\ln\Lambda} \left( \frac{g^2(\Lambda)}{m^2(\Lambda)} \right) = \beta_{g/m^2} \implies \frac{g^2}{m^2} \sim \Lambda^{\text{const}}$
      justification: |
        The quantity $\mathcal{I}_{\text{mass}}$ is constructed to be constant under the RG flow defined by the provided $\beta$-functions. This is analogous to constructing scheme-independent relations between couplings in QFT, such as those that appear in supersymmetry. It creates a direct, calculable relationship between the running of a mass parameter and the running of a gauge coupling.
      references: []
      confidence: 0.8
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The running of a particle's rest mass with energy is directly proportional to the running of its associated gauge coupling constant, with a proportionality constant fixed by the beta-function coefficients."
      domain: phenomenology
      falsifier: "High-precision measurements at a future collider show that particle rest masses are constant with energy, or that their running is completely uncorrelated with the running of the associated gauge coupling constant."
      status: proposed
      links: [XAP-006D]
naming_notes:
  collisions: [The symbol $\mathcal{I}$ is commonly used for action, information, or the identity operator. The "mass" subscript is critical for disambiguation.]
  disambiguation: |
    This is an invariant under a change of energy scale (renormalization group flow), not a symmetry of spacetime (like a Lorentz invariant). It dictates how parameters *co-vary* under a change of scale, rather than being static quantities.
crosslinks:
  near_synonyms: []
  antonyms: [SCALE_DEPENDENT_RATIO]
  prerequisites: [RENORMALIZATION_FLOW, GAMMA_STIFFNESS, KI_FIBER_CURVATURE]
  downstream_effects: [MASS_CHARGE_CORRELATION, RUNNING_MASS]
license: CC-BY-SA-4.0
---

# RG Invariant

## Canonical (Pirouette)
An RG Invariant ($\mathcal{I}_{\text{mass}}$) is a dimensionless quantity, constant under renormalization group (RG) flow, that links the τ-averaged Ki-fiber curvature norm ($\mathcal{K}_F$) to the Γ-stiffness ($\Gamma_{\mathrm{stiff}}^2$). Defined as $\mathcal{I}_{\text{mass}} = (\mathcal{K}_F / \Gamma_{\mathrm{stiff}}^2) \cdot \Lambda^{-2(c_2-c_1)}$, where $\Lambda$ is the energy scale and $c_1, c_2$ are beta-function coefficients. Its invariance ensures that the running of particle masses (from stiffness) is proportionally locked to the running of gauge couplings (from fiber curvature).

## EFT-First Summary
The RG Invariant $\mathcal{I}_{\text{mass}}$ is a scheme-independent quantity that links the beta function for a particle's mass (derived from Γ-stiffness) to the beta function for its gauge charge (derived from Ki-fiber curvature). Its constancy implies that any change in a particle's effective mass with energy scale is directly proportional to the change in its interaction strength. This provides a testable, non-perturbative prediction for the running of masses in the Standard Model.

## Glossary Links
- See also: [Γ-Stiffness](...), [Ki-Fiber Curvature](...), [Renormalization Flow](...)