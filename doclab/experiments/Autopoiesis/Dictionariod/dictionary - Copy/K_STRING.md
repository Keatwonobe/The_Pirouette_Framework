---
term: "k-string"
canonical_id: "K_STRING"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DYNA-COLOR-001_su(3)_c_as_temporal_color_frame"]
---

---
term: k-string
canonical_id: K_STRING
symbol: σ_k
aliases: [N-ality string, center-vortex flux tube]
parents: [DYNA-COLOR-001]
children: [MATH-YM-003, XXP-EWQCD-EXP]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DYNA-COLOR-001
      lines: "§6"
      snippet: |
        **k-strings:** for representations of N-ality (k=1,2), the baseline predicts
        [
        \sigma_k \approx \sigma ,\frac{\sin(\pi k/3)}{\sin(\pi/3)}
        \quad(\text{Casimir or sine-law ansätze as limiting cases}).
        ]
  editors: [system-agent]
  review_log: []
triad:
  art: |
    A rope braided from k strands of temporal-color flux, binding together sources that the vacuum cannot otherwise screen. The more strands, the thicker the rope, but in a precise, quantized hierarchy.
  law: |
    The tension σ_k of a flux tube connecting static sources in an SU(3) representation depends only on the representation's N-ality `k`. The ratio of tensions follows a sine-law hierarchy: σ_k / σ₁ = sin(πk/3) / sin(π/3). Sources with N-ality k=0 (e.g., gluons) are screened and have σ₀=0, causing the string to break.
  philosophy: |
    The k-string tension hierarchy is a primary, measurable consequence of confinement via Z₃ center-vortex condensation. Its N-ality dependence, as opposed to Casimir scaling, is a sharp, falsifiable prediction that directly tests the Pirouette mechanism where the SU(3) center symmetry is fundamental to the structure of the vacuum.
pirouette_definition: |
  A k-string is a flux tube of confined color-electric field that forms between static sources belonging to an SU(3) representation with a non-zero N-ality of `k` (mod 3). Its tension, `σ_k`, is a direct consequence of the dual Meissner effect within the Z₃ center-vortex condensate of the temporal-color frame. The framework predicts a specific hierarchy of tensions (`σ₁`, `σ₂`) that depends only on `k` and not on other properties of the representation (like its quadratic Casimir), providing a sharp test of the confinement model.
operational_definition:
  units: Energy/Length (e.g., GeV/fm) or Mass² (e.g., GeV²) in natural units.
  symbol_table:
    - name: σ_k
      meaning: Tension of a flux tube connecting sources of N-ality k.
      dimensions: M L T⁻²
      default_range: σ₁ ≈ 0.18 GeV² ≈ 0.9 GeV/fm
    - name: k
      meaning: N-ality of the SU(3) representation of the static sources.
      dimensions: dimensionless
      default_range: {1, 2} for stable strings in SU(3)
  measurement:
    procedures:
      - name: Lattice Wilson Loop Extraction
        outline: |
          1. On a Euclidean spacetime lattice, compute the vacuum expectation value of large, planar Wilson loops `<W_R(C)>` for static sources in a representation R with N-ality k.
          2. Extract the tension `σ_k` from the area-law decay for large loop area A(C): `<W_R(C)> ∝ exp(-σ_k * A(C))`.
          3. Repeat for representations with k=1 (e.g., fundamental `3`) and k=2 (e.g., sextet `6` or adjoint `8`).
          4. Compute the ratio σ₂/σ₁ and compare with theoretical predictions.
        expected_signals: [A clear area-law decay for Wilson loops in representations with k=1, 2. A ratio σ₂/σ₁ consistent with sin(2π/3)/sin(π/3) ≈ 1.]
        pitfalls: [Contamination from excited string states ("torelon mixing"). String breaking at large distances for representations that can be screened by gluons (e.g., adjoint `8`). Finite volume and lattice spacing artifacts.]
context_windows:
  - module: DYNA-COLOR-001
    excerpt: |
      When these [Z₃ center] vortices condense, Wilson loops in representations with nonzero N-ality obey an area law: `⟨W_R(C)⟩ ~ exp(-σ_R * A(C))`, with `σ_R` depending only on N-ality (k-string hierarchy), recovering QCD’s confinement pattern.
  - module: DYNA-COLOR-001
    excerpt: |
      **Falsifiability (module-local)** ... **k-string mismatch:** a persistent pattern inconsistent with N-ality (after accounting for mixing and 1/N effects) breaks the temporal-color picture.
poetic_connections:
  motifs: [braids, tension, flux tube, confinement, hierarchy]
  evocative_lines:
    - "cords of temporal tension"
    - "Color is time’s threefold braid."
  association_matrix:
    - [ "STRING_TENSION", 1.0 ]
    - [ "CENTER_VORTEX", 0.9 ]
    - [ "N_ALITY", 0.9 ]
    - [ "CONFINEMENT", 0.8 ]
formal_mappings:
  candidates: []
  adopted:
    - target: k-string tension
      domain: Lattice QCD
      mapping_kind: operational
      equation_hint: |
        σ_k / σ_f ≈ sin(πk/N) / sin(π/N)
      justification: |
        This term maps directly to the well-established concept of k-strings in non-Abelian gauge theories, which are studied extensively via lattice QCD. The predicted tension hierarchy, specifically the 'sine-law' scaling, is a key observable used to distinguish between different models of confinement. Pirouette's mechanism is a specific physical realization of a center-vortex model, which generically predicts such a hierarchy.
      references:
        - title: k-string tensions in SU(N) gauge theory
          where: Phys. Rev. D 62, 114503
          date: 2000-11-08
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The ratio of string tensions σ_k/σ₁ depends only on the N-ality k of the source representation, not its specific Casimir invariant."
      domain: phenomenology
      falsifier: "Lattice simulations demonstrating that σ_R for different representations R with the same N-ality k are statistically different beyond expected mixing effects (e.g., σ_sextet ≠ σ_adjoint for SU(3))."
      status: supported
      links: [DYNA-COLOR-001, XXP-EWQCD-EXP]
    - statement: "The SU(3) tension hierarchy follows the sine law: σ₂/σ₁ = sin(2π/3)/sin(π/3) = 1."
      domain: phenomenology
      falsifier: "High-precision lattice data showing a statistically significant deviation from this ratio in the large-distance, zero-temperature limit, in favor of an alternative such as Casimir scaling."
      status: under-test
      links: [DYNA-COLOR-001]
naming_notes:
  collisions: [The symbol `k` is frequently used for momentum; `σ` is frequently used for cross-sections. The subscripted form `σ_k` within the context of confinement is generally unambiguous.]
  disambiguation: |
    Distinguish from the fundamental strings of String Theory. A QCD k-string is an emergent, 1D energetic object (a flux tube) within 3+1D spacetime. The `k` refers to the N-ality of the color sources it connects, not a winding number or Kaluza-Klein mode.
crosslinks:
  near_synonyms: [N_ALITY_STRING]
  antonyms: [SCREENED_POTENTIAL]
  prerequisites: [STRING_TENSION, N_ALITY, CENTER_VORTEX]
  downstream_effects: [REGGE_SLOPE, QUARKONIUM_SPECTRUM]
license: CC-BY-SA-4.0
---

# k-string

## Canonical (Pirouette)
A k-string is a flux tube of confined color-electric field that forms between static sources belonging to an SU(3) representation with a non-zero N-ality of `k` (mod 3). Its tension, `σ_k`, is a direct consequence of the dual Meissner effect within the Z₃ center-vortex condensate of the temporal-color frame. The framework predicts a specific hierarchy of tensions (`σ₁`, `σ₂`) that depends only on `k` and not on other properties of the representation (like its quadratic Casimir), providing a sharp test of the confinement model.

## EFT-First Summary
In the low-energy effective theory of QCD, the potential between static color sources that are not color-singlets grows linearly with distance, `V(R) ~ σR`. The coefficient `σ` is the string tension. The k-string concept generalizes this to sources in any color representation, characterized by N-ality `k`. The tension `σ_k` is predicted to follow a `sin(πk/N)` law, a key feature of confinement models based on a dual superconductor mechanism or center-vortex condensation. This provides a direct, computable link between the microscopic gauge dynamics and the macroscopic properties of hadrons, testable via lattice QCD. (Ref: Bali, G. S. (2000). *k-string tensions in SU(N) gauge theory*).

## Glossary Links
- See also: [String Tension](<...>), [N-ality](<...>), [Center Vortex](<...>), [Confinement](<...>)