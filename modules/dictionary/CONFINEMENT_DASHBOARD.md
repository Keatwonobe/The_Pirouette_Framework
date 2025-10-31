---
term: "Confinement Dashboard"
canonical_id: "CONFINEMENT_DASHBOARD"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-010"]
---

---
term: Confinement Dashboard
canonical_id: CONFINEMENT_DASHBOARD
symbol: 
aliases: [Regge Trajectory Validator]
parents: [MATH-006, MATH-010]
children: [XXP-001, XXP-003]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-010
      lines: "§3, item 1"
      snippet: |
        The Confinement Dashboard (from MATH-006): Input: Experimental data from particle accelerators (e.g., hadron spectroscopy). Prediction: The framework predicts that the mass-squared of families of bound states (like mesons) should fall on straight lines ("Regge trajectories") when plotted against their angular momentum. ... Falsification: The theory is falsified if these trajectories are not linear...
  editors: [System Agent]
  review_log: []
triad:
  art: |
    A celestial string, pulled taut through the chaotic spray of particle collisions, revealing the simple, linear tension that binds quarks together.
  law: |
    The squared mass (m²) of a family of confined states is a linear function of its total angular momentum (J), with a universal slope determined by the confinement tension parameter (b).
  philosophy: |
    The dashboard transforms the abstract concept of a confining potential into a direct, visual, and falsifiable test against the entire catalog of known particles, proving that a single rule governs the structure of all bound states.
pirouette_definition: |
  A validation tool mandated by MATH-010 that plots the squared mass (m²) against the angular momentum (J) for families of bound states. It is designed to test the Pirouette Framework's core prediction from MATH-006 that these plots, known as Regge trajectories, must be linear, with a slope directly related to the universal confinement tension parameter `b`.
operational_definition:
  units: The plot has axes of GeV² (for m²) versus dimensionless spin J. The slope α' has units of GeV⁻².
  symbol_table:
    - name: m²
      meaning: Squared mass of the bound state.
      dimensions: "[Energy]²"
      default_range: 0.5–10 GeV²
    - name: J
      meaning: Total angular momentum quantum number.
      dimensions: dimensionless
      default_range: "[0, 1, 2, ...]"
    - name: α'
      meaning: Regge slope, the slope of the m² vs. J plot.
      dimensions: "[Energy]⁻²"
      default_range: ~0.9 GeV⁻²
  measurement:
    procedures:
      - name: Regge Trajectory Analysis
        outline: |
          1. Compile mass `m` and spin `J` quantum numbers for a given hadron family (e.g., ρ-mesons) from the Particle Data Group (PDG) or new experimental results.
          2. Plot `m²` on the y-axis versus `J` on the x-axis.
          3. Perform a linear regression on the data points.
          4. Compare the slope `α'` to the value predicted from the confinement parameter `b` and test for linearity using a chi-squared test.
        expected_signals: [A set of approximately parallel straight lines for different hadron families, each with a goodness-of-fit R² > 0.98.]
        pitfalls: [Misidentification of particle quantum numbers, scarcity of data for high-spin states, resonance mixing between particle families.]
context_windows:
  - module: MATH-010
    excerpt: |
      The Confinement Dashboard... Input: Experimental data from particle accelerators (e.g., hadron spectroscopy). Prediction: The framework predicts that the mass-squared of families of bound states (like mesons) should fall on straight lines ("Regge trajectories") when plotted against their angular momentum... Falsification: The theory is falsified if these trajectories are not linear or if the required b parameter is inconsistent across different families of particles.
  - module: MATH-006
    excerpt: |
      The linear term `b*r` in the effective potential `V_eff` dominates at large distances, creating a flux tube with constant energy density. This 'string-like' tension is not merely an analogy; it has a direct physical consequence. The quantized vibrational and rotational modes of this string predict that the squared mass of the bound state should increase linearly with its angular momentum, a relationship that must hold universally for all confined systems.
poetic_connections:
  motifs: [linearity, tension, family, resonance, string, order]
  evocative_lines:
    - "This is the moment the framework shows its teeth."
    - "...the mass-squared of families of bound states...should fall on straight lines."
  association_matrix:
    - [ "CONFINEMENT_POTENTIAL", 0.9 ]
    - [ "HADRON_SPECTROSCOPY", 0.8 ]
    - [ "FALSIFIABLE_PREDICTION", 0.7 ]
formal_mappings:
  candidates:
    - target: Regge Trajectory
      domain: SM
      mapping_kind: operational
      equation_hint: |
        J = α(0) + α' m²
      justification: |
        The dashboard is a direct implementation of plotting Regge trajectories, a standard analysis in hadron spectroscopy. The observed linearity of these trajectories for mesons and baryons is a primary piece of phenomenological evidence for the string-like model of QCD confinement. The slope `α'` is the Regge slope.
      references:
        - title: Introduction to High Energy Physics
          where: Perkins, D. H. (4th ed.), Chapter 5
          date: 2000-01-01
      confidence: 0.99
  adopted:
    - target: Regge Trajectory
      rationale: The mapping is a 1-to-1 identity in concept, procedure, and expected outcome. The term "Confinement Dashboard" frames this existing analysis as a direct, go/no-go test of a core Pirouette principle.
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "The m² vs. J plots for all hadron families are linear and exhibit a near-universal slope."
      domain: phenomenology
      falsifier: "The discovery of a hadron family whose Regge trajectory is robustly non-linear (e.g., quadratic), or the finding that slopes vary unsystematically between families, would falsify the universality of the confinement potential described in MATH-006."
      status: supported
      links: [MATH-006, MATH-010]
naming_notes:
  collisions: []
  disambiguation: |
    The term "Dashboard" is used to emphasize that this is not a static, historical plot, but a live validation tool that should be continuously updated with new experimental data from accelerators. It serves as an ongoing health check on the theory's core confinement model.
crosslinks:
  near_synonyms: [REGGE_VALIDATOR]
  antonyms: [DECONFINEMENT_SIGNATURE]
  prerequisites: [CONFINEMENT_POTENTIAL]
  downstream_effects: [XXP_HADRON_SPECTROSCOPY]
license: CC-BY-SA-4.0
---

# Confinement Dashboard

## Canonical (Pirouette)
A validation tool mandated by MATH-010 that plots the squared mass (m²) against the angular momentum (J) for families of bound states. It is designed to test the Pirouette Framework's core prediction from MATH-006 that these plots, known as Regge trajectories, must be linear, with a slope directly related to the universal confinement tension parameter `b`.

## EFT-First Summary
The Confinement Dashboard is the Pirouette Framework's operational name for the analysis of **Regge Trajectories** in hadron spectroscopy. This standard technique in QCD phenomenology plots hadron squared-mass (m²) against spin (J), revealing striking linear relationships. Within Pirouette, the linearity and near-universal slope of these trajectories are not just empirical observations but a direct, falsifiable prediction stemming from the `b*r` term in the framework's universal confinement potential.

## Glossary Links
- See also: [CONFINEMENT_POTENTIAL]