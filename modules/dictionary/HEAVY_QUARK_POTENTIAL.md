---
term: "Heavy-quark potential"
canonical_id: "HEAVY_QUARK_POTENTIAL"
symbol: "V(R)"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-YM-003_nonperturbative_map"]
---

---
term: Heavy-quark potential
canonical_id: HEAVY_QUARK_POTENTIAL
symbol: V(R)
aliases: [Static quark-antiquark potential, Wilson loop potential, Cornell potential]
parents: [MATH-YM-003_nonperturbative_map]
children: [XXP-EWQCD-EXP]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-YM-003_nonperturbative_map
      lines: "§4 · Heavy-quark potential & lattice dictionary"
      snippet: |
        Define the static (Q\bar Q) potential:
        [
        V(R) = \sigma R - \frac{\pi}{12R} + \mu + \mathcal{O}\big(R^{-3}\big),
        ]
        (Lüscher term shown for reference).
  editors: [LLM-Synthesizer]
  review_log: []
triad:
  art: |
    The invisible, unbreakable string between two primal charges. It hums with Coulombic energy when they are close, but stretch it, and its tension rises relentlessly, a linear resistance that sings of confinement.
  law: |
    The potential energy V between a static quark and antiquark at separation R is characterized by two regimes: a Coulomb-like potential `~1/R` at short distance and a linear potential `V ~ \sigma R` at long distance. The slope of the linear part, the string tension \sigma, is a universal constant of confinement.
  philosophy: |
    The heavy-quark potential is the primary theoretical and experimental window into the mechanism of color confinement. It renders the abstract concept of a non-Abelian flux tube into a measurable quantity, bridging the perturbative physics of short distances with the nonperturbative reality of the hadronic world. It is the yardstick against which all theories of the strong force must be measured.
pirouette_definition: |
  The interaction energy between a static quark (Q) and antiquark (Q̄) separated by a distance R. Within Pirouette, V(R) is a **derived observable**, not a fundamental input. Its dominant nonperturbative feature—the linear-confining term with slope \sigma (string tension)—is determined by the ratio of temporal-color frame stiffness (\kappa_3) to the square of the Γ-coherence length (\xi_\Gamma^2). The potential's full functional form provides the primary dictionary for translating Pirouette's mechanical parameters into standard lattice QCD scales (r_0, t_0).
operational_definition:
  units: Energy (e.g., GeV, MeV)
  symbol_table:
    - name: V(R)
      meaning: Potential energy between a static quark-antiquark pair
      dimensions: ML²T⁻² (Energy)
      default_range: 0–2 GeV
    - name: R
      meaning: Separation distance between the quark and antiquark
      dimensions: L (Length)
      default_range: 0.1–1.5 fm
    - name: \sigma
      meaning: String tension; the coefficient of the linear term in V(R)
      dimensions: ML²T⁻²/L = MT⁻² (Force) or ML²T⁻² / L² = M L⁻² (Energy Density) or (Energy)² in natural units
      default_range: ~0.18 GeV² or ~440 MeV/fm
  measurement:
    procedures:
      - name: Lattice QCD Wilson Loop Extraction
        outline: |
          Measure the vacuum expectation value of rectangular Wilson loops `W(R,T)` of varying spatial size R and temporal extent T. For large T, the expectation value decays exponentially, `<W(R,T)> ~ exp[-V(R)T]`. A linear fit to `log(<W(R,T)>)` versus T extracts the potential V(R) for each separation R.
        expected_signals: [Exponential decay of `<W(R,T)>` with T, A potential V(R) that is Coulomb-like at small R and linear at large R]
        pitfalls: [Contamination from excited states at small T, Statistical noise for large loops, String breaking at very large R in unquenched simulations]
context_windows:
  - module: MATH-YM-003_nonperturbative_map
    excerpt: |
      Define the static (Q\bar Q) potential:
      [
      V(R) = \sigma R - \frac{\pi}{12R} + \mu + \mathcal{O}\big(R^{-3}\big),
      ]
      (Lüscher term shown for reference). Lattice Wilson loops yield (V(R)) → extract (\sigma).
  - module: MATH-YM-003_nonperturbative_map
    excerpt: |
      Baseline confinement scaling:
      [
      \boxed{\ \sigma ;=; c_\sigma ,\frac{\kappa_3}{\xi_\Gamma^2}\ \Big[1+\delta_{\rm np}\Big]\ },
      ]
      with (c_\sigma=\mathcal{O}(1)) a normalization fixed by one benchmark observable... This closes the loop between the **coherence barrier** and **hadronic phenomenology**.
poetic_connections:
  motifs: [confinement, elasticity, flux tube, breaking strings, color field]
  evocative_lines:
    - "stiffness sets the strings, coherence sets the drum skin, and out comes σ."
    - "every lattice number has a seat in the hall—and every seat points back to the same temporal instrument."
  association_matrix:
    - [ "STRING_TENSION", 1.0 ]
    - [ "WILSON_LOOP", 0.9 ]
    - [ "FRAME_STIFFNESS", 0.8 ]
    - [ "COHERENCE_LENGTH_GAMMA", 0.8 ]
formal_mappings:
  candidates:
    - target: Cornell Potential
      domain: Phenomenology
      mapping_kind: mathematical
      equation_hint: |
        V(R) = \sigma R - \frac{A}{R} + C
      justification: |
        The functional form of the potential, combining a linear confining term with a Coulomb-like term, is a standard and highly successful model in hadron physics for describing quarkonium spectra. The Pirouette framework provides a microphysical origin for the dominant nonperturbative parameter, the string tension \sigma. The Lüscher term `-π/(12R)` is a specific quantum correction to this picture.
      references:
        - title: Heavy quarks and quantum chromodynamics
          where: E. Eichten et al., Phys. Rev. D 21, 203 (1980)
          date: 1980-01-01
      confidence: 0.95
  adopted:
    - target: Cornell Potential
      rationale: This is the standard, phenomenologically successful model for the potential, and Pirouette directly predicts its key nonperturbative parameter, σ.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: 'The string tension σ, which governs the linear rise of V(R), is determined by the ratio `c_σ * \kappa_3/\xi_\Gamma^2`.'

      domain: theory
      falsifier: "A persistent mismatch between the Pirouette-predicted σ and the value extracted from lattice measurements of V(R) via Wilson loops, after the single system-wide normalization constant `c_σ` is fixed."
      status: proposed
      links: [MATH-YM-003_nonperturbative_map, DYNA-COLOR-001]
    - statement: "The long-distance potential contains a universal attractive term `-π/(12R)` (the Lüscher term) arising from quantum fluctuations of the QCD string."
      domain: theory
      falsifier: "High-precision lattice data for V(R) showing the coefficient of the `1/R` term deviating significantly from `-π/12`, beyond corrections from boundary effects or string width."
      status: supported
      links: [MATH-YM-003_nonperturbative_map]
naming_notes:
  collisions: [V is a generic symbol for potential energy in physics.]
  disambiguation: |
    This term refers to the potential between a quark-antiquark pair in the fundamental representation of SU(3). It must be distinguished from the potential between sources in other representations (k-strings), which exhibit different string tensions (\sigma_k), or the more complex multi-body potentials inside baryons.
crosslinks:
  near_synonyms: [CORNELL_POTENTIAL]
  antonyms: [SCATTERING_AMPLITUDE]
  prerequisites: [FRAME_STIFFNESS, COHERENCE_LENGTH_GAMMA, STRING_TENSION]
  downstream_effects: [LATTICE_SPACING, SOMMER_SCALE, QUARKONIUM_SPECTRA]
license: CC-BY-SA-4.0
---

# Heavy-quark potential

## Canonical (Pirouette)
The interaction energy between a static quark (Q) and antiquark (Q̄) separated by a distance R. Within Pirouette, V(R) is a **derived observable**, not a fundamental input. Its dominant nonperturbative feature—the linear-confining term with slope \sigma (string tension)—is determined by the ratio of temporal-color frame stiffness (κ₃) to the square of the Γ-coherence length (ξ_Γ²). The potential's full functional form provides the primary dictionary for translating Pirouette's mechanical parameters into standard lattice QCD scales (r₀, t₀).

## EFT-First Summary
In effective field theory and phenomenological models, the Heavy-quark potential is described by the **Cornell Potential**, `V(R) = \sigma R - A/R`. It combines a linear confining term, dominant at long distances, with a Coulomb-like term from one-gluon exchange, dominant at short distances. Pirouette provides a mechanistic origin for the nonperturbative string tension `\sigma`, linking it to fundamental properties of the temporal-color frame, while the Coulombic part is governed by the standard running coupling of QCD.

## Glossary Links
- See also: [[STRING_TENSION]], [[WILSON_LOOP]], [[SOMMER_SCALE]], [[LATTICE_SPACING]]