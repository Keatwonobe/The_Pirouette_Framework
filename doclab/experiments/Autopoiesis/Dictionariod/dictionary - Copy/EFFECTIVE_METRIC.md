---
term: "Effective Metric"
canonical_id: "EFFECTIVE_METRIC"
symbol: "g_μν"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DYNA-SUBST-001_pirouette_substrate_rules"]
---

---
term: Effective Metric
canonical_id: EFFECTIVE_METRIC
symbol: g_μν
aliases: [Emergent Metric, Pirouette Metric, Hydrodynamic Metric]
parents: [DYNA-SUBST-001]
children: [MATH-GR-001, DYNA-GR-002, GRW-003, COSMO-GR-004]
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DYNA-SUBST-001_pirouette_substrate_rules
      lines: "SR-4, §2.1"
      snippet: |
        SR-4 — Constitutive Elasticity
        Quadratic response of phase/pressure gradients defines an effective metric \(g_{\mu\nu}\).
  editors: [AI-Text-Gen-Agent]
  review_log: []
triad:
  art: |
    Spacetime is the loom—the elastic weave of coherence that all particles and forces move through. The effective metric is the local stiffness and curvature of that weave, dictating the straightest possible paths.
  law: |
    The quadratic response of the temporal medium to gradients defines a universal metric tensor \(g_{\mu\nu}\) to which all matter and energy couple minimally. This enforces the Equivalence Principle and yields Einstein's Field Equations in the low-energy limit.
  philosophy: |
    The metric is not a fundamental stage but an emergent, collective property of a deeper medium. This reframes spacetime from a static background to an active, dynamic substrate, whose properties (like \(G_{\rm eff}\)) are consequences of underlying physics, not axioms.
pirouette_definition: |
  The Effective Metric \(g_{\mu\nu}\) is the inverse response tensor of the Pirouette temporal medium, quantifying its 'elasticity' to phase and pressure gradients. It defines the spacetime geometry perceived by all matter and fields, which couple to it universally and minimally. In the hydrodynamic, low-energy limit, its dynamics are described by the Einstein-Hilbert action, yielding General Relativity as an effective field theory.
operational_definition:
  units: Dimensionless
  symbol_table:
    - name: g_μν
      meaning: Effective metric tensor
      dimensions: Dimensionless
      default_range: "Contextual; e.g., diag(-1, 1, 1, 1) in flat regions"
  measurement:
    procedures:
      - name: Gravitational Lensing & Standard Rulers
        outline: |
          1. Measure the deflection of light from distant sources (e.g., quasars) as it passes massive objects (e.g., galaxies). The deflection angle depends directly on the components of \(g_{\mu\nu}\) integrated along the path.
          2. Separately, measure the redshift-distance relation using standard candles (Type Ia supernovae) or standard rulers (Baryon Acoustic Oscillations) to map the large-scale structure of \(g_{\mu\nu}\).
        expected_signals: ["Light deflection consistent with GR predictions (PN parameters β=γ=1)", "A specific Hubble constant and deceleration parameter from the FRW solution of the effective action."]
        pitfalls: ["Systematic errors in astrophysical distance measurements", "Astrophysical foregrounds mimicking lensing signals", "Assuming an over-simplified stress-energy tensor \(T_{\mu\nu}\) for the lensing mass."]
context_windows:
  - module: DYNA-SUBST-001_pirouette_substrate_rules
    excerpt: |
      Metric \(g_{\mu\nu}\) is the inverse response tensor of the temporal medium: \( g_{\mu\nu}\propto (\mathcal{K}^{-1})_{\mu\nu} \). Coarse-graining yields
      \[
      S_{\rm eff}=\!\int\! d^4x\sqrt{-g}
      \left[\frac{c^4}{16\pi G_{\rm eff}}R-\Lambda_{\rm Pirouette}
      +\mathcal{L}_{\rm matter}(g,\text{fields})\right]
      +\mathcal{O}(R^2,\nabla R).
      \]
      Varying gives Einstein’s equations. Single metric → equivalence principle, PN parameters β = γ = 1 on CPM.
  - module: DYNA-SUBST-001_pirouette_substrate_rules
    excerpt: |
      All matter couples minimally to the same emergent metric. Charges and couplings are set by stiffness ratios (frame elasticities) and holonomy quantization. [...] All sectors couple minimally to \(g_{\mu\nu}\); worldlines extremize proper time; fields use the Levi-Civita connection.
poetic_connections:
  motifs: [elasticity, weave, loom, hydrodynamic, emergence, coherence]
  evocative_lines:
    - "spacetime is the loom—the elastic weave of coherence they all move through."
    - "GR is the loom’s equation of state."
  association_matrix:
    - [ "TEMPORAL_MEDIUM", 0.9 ]
    - [ "EQUIVALENCE_PRINCIPLE", 0.8 ]
    - [ "COHERENCE", 0.6 ]
    - [ "GEODESIC_MOTION", 0.9 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Metric Tensor (g_μν)
      domain: GR
      mapping_kind: operational
      equation_hint: |
        S_{\rm eff} \supset \int d^4x\sqrt{-g} \frac{c^4}{16\pi G_{\rm eff}}R
      justification: |
        The Pirouette Effective Metric governs geodesic motion, defines curvature via the Riemann tensor, and appears in the low-energy effective action in a form identical to the Einstein-Hilbert action. Operationally, it is indistinguishable from the GR metric tensor in all regimes tested to date, predicting phenomena like gravitational lensing, time dilation, and gravitational waves with PN parameters β=γ=1.
      references:
        - title: Pirouette Substrate — Foundations of the Temporal Medium
          where: module DYNA-SUBST-001 §2.1
          date: 2025-10-18
      confidence: 0.99
constraints_and_falsifiers:
  claims:
    - statement: "Gravitational waves propagating via the effective metric have exactly two tensor polarizations and travel at the luminal speed \(c\), up to corrections of order \((\omega/\omega_c)^2\)."
      domain: experiment
      falsifier: "Detection of scalar or vector polarizations, or a frequency-dependent propagation speed (dispersion) exceeding the predicted \((\omega/\omega_c)^2\) scaling."
      status: under-test
      links: [XXP-GR-EXP, GRW-003]
    - statement: "All test bodies follow geodesics of the same effective metric, regardless of their composition (Weak Equivalence Principle)."
      domain: experiment
      falsifier: "Measurement of any composition-dependent differential acceleration in free fall, such as in satellite or torsion balance experiments."
      status: supported
      links: [XXP-GR-EXP]
naming_notes:
  collisions: ["The symbol \(g\) can also denote a gauge coupling constant (e.g., \(g_s\)) or the determinant of the metric."]
  disambiguation: |
    In Pirouette, 'Effective Metric' is always used to distinguish the emergent, hydrodynamic geometry from any potential fundamental, pre-geometric degrees of freedom. It is *not* an 'analogue metric' in the sense of condensed matter systems, as it is the one and only metric governing macrophysics within the framework.
crosslinks:
  near_synonyms: [SPACETIME_GEOMETRY]
  antonyms: [PREGEOMETRIC_SUBSTRATE]
  prerequisites: [TEMPORAL_MEDIUM, TEMPORAL_PRESSURE]
  downstream_effects: [GRAVITATIONAL_WAVE, EQUIVALENCE_PRINCIPLE, GEODESIC_MOTION, GRAVITATIONAL_LENSING]
license: CC-BY-SA-4.0
---

# Effective Metric

## Canonical (Pirouette)
The Effective Metric \(g_{\mu\nu}\) is the inverse response tensor of the Pirouette temporal medium, quantifying its 'elasticity' to phase and pressure gradients. It defines the spacetime geometry perceived by all matter and fields, which couple to it universally and minimally. In the hydrodynamic, low-energy limit, its dynamics are described by the Einstein-Hilbert action, yielding General Relativity as an effective field theory.

## EFT-First Summary
The Effective Metric \(g_{\mu\nu}\) is operationally identical to the metric tensor of General Relativity. Its dynamics are governed by the Einstein-Hilbert action plus a cosmological constant, emerging as the low-energy description of the Pirouette temporal medium's collective behavior. All Standard Model fields couple to this single metric, ensuring the Equivalence Principle holds to a high degree of precision.

## Glossary Links
- See also: [Temporal Medium](<link-to-TEMPORAL_MEDIUM>), [Effective Gravitational Constant (G_eff)](<link-to-G_EFF>), [Equivalence Principle](<link-to-EQUIVALENCE_PRINCIPLE>)