---
term: "Viable Points"
canonical_id: "VIABLE_POINTS"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["XAP-008_Leptonic_g-2_gladiator_force_fit_map"]
---

---
term: Viable Points
canonical_id: VIABLE_POINTS
symbol: N/A
aliases: [Allowed Region, Consistent Parameter Set]
parents: [XAP-008_Leptonic_g-2_gladiator_force_fit_map]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: XAP-008_Leptonic_g-2_gladiator_force_fit_map
      lines: "§2"
      snippet: |
        - **Viable points:** $(\kappa,p,m_\Gamma)$ satisfying both $e$ and $\mu$ bands.
  editors: [auto-agent]
  review_log: []
triad:
  art: |
    The scattered islands of truth in a vast sea of possibility, where a model's predictions align with the sharp constraints of experiment. They are the model's first empirical footprint.
  law: |
    A point in the parameter space $(\kappa, p, m_\Gamma)$ is viable if and only if the predicted anomalous magnetic moments for the electron and muon, $\Delta a_e$ and $\Delta a_\mu$, both fall within their experimentally-defined constraint bands. Any point failing one or more constraints is non-viable.
  philosophy: |
    Viable points demarcate a model's living territory. They are not merely a filtered dataset, but a map of where a new theory can operate without being falsified, guiding future searches by focusing attention on the most promising parameter regions.
pirouette_definition: |
  A viable point is a specific tuple of model parameters $(\kappa, p, m_\Gamma)$ for which the calculated leptonic magnetic-moment shifts, $\Delta a_e$ and $\Delta a_\mu$, simultaneously satisfy all specified experimental constraints. The set of all such points constitutes the viable parameter space for a given set of constraints (e.g., "permissive" or "tight").
operational_definition:
  units: Mixed parameter tuple (dimensionless, dimensionless, MeV)
  symbol_table:
    - name: κ
      meaning: Dimensionless coupling constant for the Γ-lepton interaction.
      dimensions: dimensionless
      default_range: $10^{-4}$ – $10^{-2}$
    - name: p
      meaning: Mass-scaling exponent in the Γ-lepton interaction.
      dimensions: dimensionless
      default_range: 0 – 4
    - name: m_Γ
      meaning: Mass of the Γ-field quantum.
      dimensions: M (energy units)
      default_range: 1 – 100 MeV
    - name: Δa_ℓ
      meaning: Predicted shift in the anomalous magnetic moment for lepton ℓ.
      dimensions: dimensionless
      default_range: $10^{-14}$ – $10^{-8}$
  measurement:
    procedures:
      - name: Parameter Scan and Constraint Filtering
        outline: |
          1. Define the model prediction $\Delta a_\ell^{(\Gamma)}(\kappa, p, m_\Gamma)$ for $\ell \in \{e, \mu\}$.
          2. Define the upper and lower experimental bounds for $\Delta a_e$ and $\Delta a_\mu$.
          3. Scan a grid of points in the $(\kappa, p, m_\Gamma)$ parameter space.
          4. For each point, calculate both $\Delta a_e$ and $\Delta a_\mu$.
          5. A point is retained as "viable" if and only if both calculated values fall within their respective constraint bands. The collection of retained points is the set of viable points.
        expected_signals: [A machine-readable list of $(\kappa, p, m_\Gamma)$ tuples, e.g., a CSV file.]
        pitfalls: [Incomplete scan grid missing small "islands of viability", using outdated experimental constraints, numerical precision errors in calculating $\Delta a_\ell$.]
context_windows:
  - module: XAP-008_Leptonic_g-2_gladiator_force_fit_map
    excerpt: |
      We provide three machine-readable tables for the module→paper pipeline: Viable points: $(\kappa,p,m_\Gamma)$ satisfying both $e$ and $\mu$ bands.
  - module: XAP-008_Leptonic_g-2_gladiator_force_fit_map
    excerpt: |
      The electron bound dominates the viable set; decoupling $F_e(m_\Gamma)$ pushes solutions toward $m_\Gamma\!\gtrsim\!10$–$30$ MeV *or* larger $p$. Tight band favors $p\!\gtrsim\!1.5$–$2.5$ with $\kappa\!\sim\!10^{-4}$–$10^{-3}$; permissive band admits smaller $p$ or lighter $m_\Gamma$ if $\kappa\!\lesssim\!10^{-4}$.
poetic_connections:
  motifs: [filtering, constraint satisfaction, allowed region, parameter space, falsification]
  evocative_lines:
    - "The electron bound dominates the viable set"
    - "minimal κ saturating the tight μ bound while passing the e bound"
  association_matrix:
    - [ "Pressuron Constraint Atlas", 0.9 ]
    - [ "Γ-stiffness", 0.5 ]
    - [ "Falsification", 0.7 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Allowed Parameter Region
      domain: EFT|phenomenology
      mapping_kind: conceptual
      equation_hint: N/A
      justification: |
        In particle physics model building and phenomenology, theoretical parameters are confronted with experimental data. The set of parameter points that are not ruled out by one or more experiments is called the "allowed region" or "viable parameter space." This is conceptually and operationally identical to the Pirouette Framework's "Viable Points." The boundary of this region is an exclusion limit.
      references:
        - title: Review of Particle Physics
          where: Particle Data Group, section on "Searches for New Physics"
          date: 2024-08-01
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "The set of viable points is non-empty under the 'tight' constraint scenario B."
      domain: phenomenology
      falsifier: 'A future, more precise measurement of $\Delta a_e$ or $\Delta a_\mu$ could shrink the allowed bands such that no point in the $(\kappa, p, m_\Gamma)$ space can satisfy both simultaneously, rendering the set empty and falsifying the model.'

      status: supported
      links: [XAP-008_Leptonic_g-2_gladiator_force_fit_map]
naming_notes:
  collisions: []
  disambiguation: |
    A set of Viable Points is distinct from a "Best-fit Point," which is the single point that minimizes a statistical measure (e.g., χ²). The viable set includes all parameter tuples that are merely *consistent* with the data within a given tolerance, not just the single point providing the "best" explanation.
crosslinks:
  near_synonyms: []
  antonyms: [EXCLUDED_REGION]
  prerequisites: [PRESSURON_CONSTRAINT_ATLAS]
  downstream_effects: [PARAMETER_SPACE_VISUALIZATION]
license: CC-BY-SA-4.0
---

# Viable Points

## Canonical (Pirouette)
A viable point is a specific tuple of model parameters $(\kappa, p, m_\Gamma)$ for which the calculated leptonic magnetic-moment shifts, $\Delta a_e$ and $\Delta a_\mu$, simultaneously satisfy all specified experimental constraints. The set of all such points constitutes the viable parameter space for a given set of constraints (e.g., "permissive" or "tight").

## EFT-First Summary
In particle physics phenomenology, Viable Points correspond to the **Allowed Parameter Region**. This is the set of a model's free parameters (here, $\kappa, p, m_\Gamma$) that are consistent with experimental constraints, such as measurements of the electron and muon anomalous magnetic moments ($g-2$). The boundary of this region defines the experimental exclusion limit on the model.

## Glossary Links
- See also: Pressuron Constraint Atlas, Γ-stiffness