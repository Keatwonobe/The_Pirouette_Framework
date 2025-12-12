---
term: "Mass Retention"
canonical_id: "MASS_RETENTION"
symbol: "f_ret"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["COSMO-002"]
---

---
term: Mass Retention
canonical_id: MASS_RETENTION
symbol: f_ret
aliases: []
parents: [COSMO-002]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: COSMO-002
      lines: "Section 3, P2"
      snippet: |
        P2 — Survivability of κ peaks
        Post‑pericenter, the Γ peaks re‑emerge with fractional mass retention f_ret(M,b,v_in) prescribed by the Γ halo binding; gas lags with an arc‑like shock.
  editors: [pirouette-v1-agent]
  review_log: []
triad:
  art: |
    A ghost in the machine, the essence of a halo that endures the violence of a cosmic collision. It is the memory of mass, the core integrity that does not scatter when galaxies clash.
  law: |
    The mass retention `f_ret` is the ratio of a Γ-halo's central peak mass measured after pericenter passage to its initial mass, M_peak(t > t_peri) / M_peak(t→−∞). For a given potential V(Γ), `f_ret` is a deterministic function of the merger's initial conditions (masses, impact parameter, relative velocity).
  philosophy: |
    Mass retention quantifies the resilience of a Γ-condensate core, acting as a direct test of its quasi-solitonic nature. Unlike a cloud of particles that can be tidally stripped, a high `f_ret` demonstrates that the halo's core integrity is an emergent feature of the underlying field dynamics, not a statistical survival of individual constituents.
pirouette_definition: |
  The fraction of a Γ-halo's mass, M_Γ, that remains gravitationally bound to its central density peak following a merger event. It is calculated for each progenitor halo after they have passed pericenter and begun to separate. `f_ret` is a primary observable in `COSMO-Γ-MERGE` simulations, predicted to be a deterministic function of the Γ-potential and the encounter's orbital parameters (M₁, M₂, b, v_in).
operational_definition:
  units: dimensionless
  symbol_table:
    - name: f_ret
      meaning: Mass retention fraction
      dimensions: dimensionless
      default_range: "[0, 1]; typically 0.8–0.95 for major mergers"
    - name: M_peak(t_final)
      meaning: Mass of the surviving Γ-halo core peak at a late time after pericenter.
      dimensions: M
      default_range: contextual
    - name: M_peak(t_initial)
      meaning: Initial mass of the Γ-halo core peak at t→−∞.
      dimensions: M
      default_range: contextual
  measurement:
    procedures:
      - name: Simulated Merger Analysis
        outline: |
          1. Initialize a two-halo merger simulation (`COSMO-Γ-MERGE`) with specified masses (M₁, M₂), impact parameter (b), and relative velocity (v_in).
          2. Identify the central mass M_peak for each halo (e.g., mass within a fixed radius `r_c`) at `t→−∞`. This is `M_peak(t_initial)`.
          3. Run the simulation past pericenter passage (`t_peri`).
          4. At a late time `t_final > t_peri` when the two cores are clearly separated again, identify and measure the mass `M_peak(t_final)` of each surviving peak.
          5. Calculate `f_ret` for each progenitor as `M_peak(t_final) / M_peak(t_initial)`.
        expected_signals: [Lensing convergence (κ) map showing two distinct peaks post-merger, Γ field energy density map]
        pitfalls: [Ambiguous peak identification if the merger is highly disruptive or results in rapid coalescence, dependence of M_peak on the chosen aperture definition, numerical dissipation artificially lowering f_ret]
context_windows:
  - module: COSMO-002
    excerpt: |
      Post‑pericenter, the Γ peaks re‑emerge with fractional mass retention f_ret(M,b,v_in) prescribed by the Γ halo binding; gas lags with an arc‑like shock.
  - module: COSMO-002
    excerpt: |
      Falsification: ...κ peaks do not survive with observed strengths for real systems at given (M,b,v), contradicting f_ret predictions.
  - module: COSMO-002
    excerpt: |
      "f_ret_1": 0.86,
      "f_ret_2": 0.84
      # from merge_result.json artifact for a Bullet-like merger simulation.
poetic_connections:
  motifs: [resilience, core-survival, collisionless-memory, solitonic-rebound]
  evocative_lines:
    - "Γ peaks re‑emerge with fractional mass retention..."
    - "The survival of κ peaks after core passage..."
  association_matrix:
    - [ "KAPPA_PEAK", 0.9 ]
    - [ "GAMMA_POTENTIAL", 0.8 ]
    - [ "EFFECTIVE_CROSS_SECTION", 0.7 ]
formal_mappings:
  candidates:
    - target: Subhalo survivability / core disruption fraction
      domain: CM
      mapping_kind: conceptual
      justification: |
        `f_ret` quantifies the same physical phenomenon as the survival fraction of a dark matter subhalo core after a merger. In particle dark matter models, this survival is governed by tidal stripping and, for Self-Interacting Dark Matter (SIDM), by the self-interaction cross-section. A low `f_ret` in a standard model would correspond to significant disruption or a high effective cross-section.
      references:
        - title: "The Bullet Cluster: A Direct Constraint on the Cross-Section of Dark Matter"
          where: "Astrophys.J.Lett. 648 (2006) L109-L113"
          date: 2006-03-20
      confidence: 0.8
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The mass retention `f_ret` is a deterministic function of V(Γ) and orbital parameters, and is typically > 0.8 for high-velocity, off-axis major mergers (e.g., Bullet Cluster analogs)."
      domain: phenomenology
      falsifier: "Observing a population of post-merger clusters where the lensing-inferred surviving core masses are systematically and significantly lower than predicted by `COSMO-Γ-MERGE` simulations for the inferred orbital parameters."
      status: proposed
      links: [COSMO-002]
naming_notes:
  collisions: [`f_ret` is a common symbol for "retention fraction" in many fields; context is key.]
  disambiguation: |
    Distinguish from the *gas* retention fraction, which is typically much lower in mergers due to shock-stripping and ram pressure. Mass Retention `f_ret` refers specifically to the collisionless Γ-condensate component, traced operationally by gravitational lensing (κ maps).
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [GAMMA_HALO, KAPPA_PEAK]
  downstream_effects: [EFFECTIVE_CROSS_SECTION]
license: CC-BY-SA-4.0
---

# Mass Retention

## Canonical (Pirouette)
The fraction of a Γ-halo's mass, M_Γ, that remains gravitationally bound to its central density peak following a merger event. It is calculated for each progenitor halo after they have passed pericenter and begun to separate. `f_ret` is a primary observable in `COSMO-Γ-MERGE` simulations, predicted to be a deterministic function of the Γ-potential and the encounter's orbital parameters (M₁, M₂, b, v_in).

## EFT-First Summary
In cosmological contexts, Mass Retention `f_ret` is the Pirouette Framework's analog for the survival fraction of a dark matter halo core after a merger. A high `f_ret` (>0.8) is predicted for the collisionless Γ-condensate, corresponding to a very low effective self-interaction cross-section (`σ_eff/m`), consistent with observations of systems like the Bullet Cluster (Clowe et al. 2006).

## Glossary Links
- See also: Γ-Halo, κ Peak, Effective Cross-Section