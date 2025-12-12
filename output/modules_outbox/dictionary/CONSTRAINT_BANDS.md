---
term: "Constraint Bands"
canonical_id: "CONSTRAINT_BANDS"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["XAP-008_Leptonic_g-2_gladiator_force_fit_map"]
---

---
term: Constraint Bands
canonical_id: CONSTRAINT_BANDS
symbol: 
aliases: ["Permissive Band (A)", "Tight Band (B)"]
parents: ["XAP-008_Leptonic_g-2_gladiator_force_fit_map"]
children: ["VIABLE_POINTS", "PARAMETER_ENVELOPES"]
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: XAP-008_Leptonic_g-2_gladiator_force_fit_map
      lines: "L11-L13"
      snippet: |
        Two benchmark constraint bands:
        \[
        \text{A (permissive): }|\Delta a_\mu|\le 2.5{\times}10^{-9},\quad |\Delta a_e|\le 5{\times}10^{-13},\qquad
        \text{B (tight): }|\Delta a_\mu|\le 5.0{\times}10^{-10},\quad |\Delta a_e|\le 3{\times}10^{-13}.
        \]
  editors: ["system"]
  review_log: []
triad:
  art: |
    Walls of measurement enclosing the parameter sea. A viable model must navigate this channel, a tight passage defined by the precision of electron and muon alike.
  law: |
    A parameter point is viable if and only if the model's predicted shifts, $\Delta a_e$ and $\Delta a_\mu$, both fall within the absolute value limits of a specified Constraint Band.
  philosophy: |
    Constraint Bands codify the interface between theoretical speculation and experimental reality. By defining multiple scenarios (e.g., permissive, tight), they allow the framework to map model viability under varying levels of experimental confidence and to anticipate the impact of future measurements.
pirouette_definition: |
  A Constraint Band is a set of two simultaneous upper bounds on the absolute value of new physics contributions to the anomalous magnetic moments of the electron ($\Delta a_e$) and muon ($\Delta a_\mu$). These bands serve as pass/fail filters for model parameter points, with different named bands (e.g., 'Permissive', 'Tight') representing different assumptions about experimental uncertainty or future sensitivity.
operational_definition:
  units: Dimensionless
  symbol_table:
    - name: $\Delta a_e$
      meaning: New physics contribution to the electron anomalous magnetic moment
      dimensions: dimensionless
      default_range: $[-5 \times 10^{-13}, 5 \times 10^{-13}]$
    - name: $\Delta a_\mu$
      meaning: New physics contribution to the muon anomalous magnetic moment
      dimensions: dimensionless
      default_range: $[-2.5 \times 10^{-9}, 2.5 \times 10^{-9}]$
  measurement:
    procedures:
      - name: Derivation from experimental residuals
        outline: |
          1. Obtain the world-average experimental value for a lepton's anomalous magnetic moment, $a_\ell^{\text{exp}}$.
          2. Obtain the complete Standard Model theoretical prediction, $a_\ell^{\text{SM}}$, including QED, electroweak, and hadronic contributions.
          3. Calculate the residual $\Delta a_\ell = a_\ell^{\text{exp}} - a_\ell^{\text{SM}}$.
          4. The Constraint Band is defined by the magnitude of the 1- or 2-sigma confidence interval of this residual for both $\ell=e$ and $\ell=\mu$.
        expected_signals: ["A statistically significant non-zero value for $\Delta a_\mu$ (the 'muon g-2 anomaly').", "A value for $\Delta a_e$ consistent with zero but with extremely small uncertainty."]
        pitfalls: ["Underestimation of hadronic uncertainties in the $a_\mu^{\text{SM}}$ calculation.", "Unaccounted-for systematic errors in g-2 experiments."]
context_windows:
  - module: XAP-008_Leptonic_g-2_gladiator_force_fit_map
    excerpt: |
      We scan the three-parameter space $(\kappa, p, m_\Gamma)$ for leptonic magnetic-moment shifts... Two benchmark constraint bands:
      A (permissive): $|\Delta a_\mu|\le 2.5{\times}10^{-9},\quad |\Delta a_e|\le 5{\times}10^{-13}$
      B (tight): $|\Delta a_\mu|\le 5.0{\times}10^{-10},\quad |\Delta a_e|\le 3{\times}10^{-13}$.
  - module: XAP-008_Leptonic_g-2_gladiator_force_fit_map
    excerpt: |
      The electron bound dominates the viable set; decoupling $F_e(m_\Gamma)$ pushes solutions toward $m_\Gamma\!\gtrsim\!10$–$30$ MeV or larger $p$. Tight band favors $p\!\gtrsim\!1.5$–$2.5$ with $\kappa\!\sim\!10^{-4}$–$10^{-3}$; permissive band admits smaller $p$ or lighter $m_\Gamma$ if $\kappa\!\lesssim\!10^{-4}$.
poetic_connections:
  motifs: ["Filter", "Gauntlet", "Experimental Sieve", "Boundary Condition"]
  evocative_lines:
    - "The electron bound dominates the viable set"
    - "saturating the tight $\mu$ bound"
  association_matrix:
    - [ "LEPTONIC_G-2_ANOMALY", 0.9 ]
    - [ "VIABLE_POINTS", 0.8 ]
    - [ "PARAMETER_ENVELOPES", 0.7 ]
formal_mappings:
  candidates: []
  adopted:
    - target: $\Delta a_\ell \equiv a_\ell^{\text{exp}} - a_\ell^{\text{SM}}$
      domain: SM|Phenomenology
      mapping_kind: operational
      equation_hint: |
        $a_\ell = (g_\ell - 2)/2$
      justification: |
        This is the standard definition of the quantity constrained by experiment. The bands represent the experimentally allowed "room" for new physics contributions to the lepton anomalous magnetic moments, derived by subtracting the Standard Model prediction from the measured value. The muon value is anomalous, while the electron value provides a powerful null constraint.
      references:
        - title: "Measurement of the Positive Muon Anomalous Magnetic Moment to 0.46 ppm"
          where: "Phys. Rev. Lett. 126, 141801 (Fermilab Muon g-2 Collaboration)"
          date: 2021-04-07
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: 'The model parameter space $(\kappa, p, m_\Gamma)$ from XAP-008 contains viable points that simultaneously satisfy the Tight Constraint Band (B).'

      domain: phenomenology
      falsifier: 'A full, verified scan of the parameter space yields zero points satisfying Band B. Alternatively, a future measurement of $a_e$ that is more precise could tighten the $\Delta a_e$ bound, invalidating all previously-found 'tight' solutions.'

      status: supported
      links: ["XAP-008_Leptonic_g-2_gladiator_force_fit_map"]
naming_notes:
  collisions: ["'Band' can refer to energy bands in solid-state physics."]
  disambiguation: |
    In Pirouette, "Constraint Bands" always refer to a set of simultaneous numerical limits on observables, derived from experiment, and used to filter a model's parameter space. They are not intrinsic properties of the model's dynamics.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: ["LEPTONIC_G-2_ANOMALY"]
  downstream_effects: ["VIABLE_POINTS", "PARAMETER_ENVELOPES", "BEST_FIT_LINE"]
license: CC-BY-SA-4.0
---

# Constraint Bands

## Canonical (Pirouette)
A Constraint Band is a set of two simultaneous upper bounds on the absolute value of new physics contributions to the anomalous magnetic moments of the electron ($\Delta a_e$) and muon ($\Delta a_\mu$). These bands serve as pass/fail filters for model parameter points, with different named bands (e.g., 'Permissive', 'Tight') representing different assumptions about experimental uncertainty or future sensitivity.

## EFT-First Summary
Constraint Bands are experimental limits on new physics contributions to the lepton g-2, defined as $\Delta a_\ell \equiv a_\ell^{\text{exp}} - a_\ell^{\text{SM}}$. The 'Tight' band reflects the current multi-sigma tension in the muon's magnetic moment and the strong null constraint from the electron's, providing a stringent, combined test for new physics models that couple to leptons.

## Glossary Links
- See also: Viable Points, Parameter Envelopes