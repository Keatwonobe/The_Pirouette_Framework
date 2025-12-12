---
term: "Misalignment"
canonical_id: "MISALIGNMENT"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["COSMO-003"]
---

---
term: Misalignment
canonical_id: MISALIGNMENT_MECHANISM
symbol: 
aliases: ["initial displacement"]
parents: ["COSMO-003"]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: COSMO-003
      lines: "Sec 1, Para 1"
      snippet: |
        A galactic‑scale ‘condensate’ need not be a thermal BEC; the cosmological mechanism is **misalignment**: Γ starts displaced from its minimum in the early universe; Hubble friction freezes it (Γ̇≈0) until H≈m_Γ, after which Γ oscillates and time‑averages to a **pressureless fluid**.
  editors: ["system"]
  review_log: []
triad:
  art: |
    A cosmic pendulum pulled aside by the universe's dawn, held taut by expansion's friction, then released to oscillate as cold matter when the friction fades.
  law: |
    The initial energy density of the Γ field, ρ_Γ,ini, is set by its potential energy at a non-zero initial displacement, Γ_ini, from the potential minimum, where V(Γ_ini) > 0. This mechanism is falsified if the observed Ω_Γ today cannot be produced by any value of Γ_ini within the natural range of the potential (e.g., M_pl) without violating inflationary initial condition constraints.
  philosophy: |
    Misalignment provides a non-thermal production mechanism for a cosmological relic, sourcing its energy density from initial potential energy rather than kinetic equilibrium. This bypasses the need for thermal couplings to the Standard Model, offering an elegant route to producing a cold, dark component from first principles of field theory in an expanding spacetime.
pirouette_definition: |
  The cosmological mechanism by which a coherently oscillating scalar field (e.g., Γ) acquires its initial energy density. In the early universe (when H ≫ m_Γ), the field is displaced from its potential minimum (Γ_ini ≠ 0) and frozen by Hubble friction (Γ̇ ≈ 0). When the Hubble parameter drops to H ≈ m_Γ, the field begins to oscillate around its minimum, and its time-averaged equation of state behaves as pressureless matter (w_Γ ≈ 0).
operational_definition:
  units: Reduced Planck units (M_pl) for field amplitude.
  symbol_table:
    - name: Γ_ini
      meaning: Initial field displacement from the potential minimum.
      dimensions: M (Mass)
      default_range: [0, M_pl]
    - name: Γ̇_ini
      meaning: Initial field velocity.
      dimensions: M²
      default_range: ≈ 0
    - name: H
      meaning: Hubble parameter.
      dimensions: M
      default_range: contextual
    - name: m_Γ
      meaning: Mass of the Γ quantum (pressuron).
      dimensions: M
      default_range: contextual
  measurement:
    procedures:
      - name: Cosmological Parameter Inference
        outline: |
          The value of Γ_ini is not directly measured. It is inferred by fitting a cosmological model, where Γ acts as dark matter (and potentially dark energy), to cosmological data sets (CMB, BAO, SNe). The initial energy density, determined by V(Γ_ini), is a free parameter in the fit, which then constrains the allowed value of Γ_ini given a potential V(Γ).
        expected_signals: ["Specific values for Ω_Γ,0 and H_0 in a ΛCDM-like model", "Characteristic modifications to CMB anisotropy spectra (TT/TE/EE) and matter power spectrum if oscillations begin late."]
        pitfalls: ["Degeneracy between Γ_ini and other parameters in the potential V(Γ), such as m_Γ.", "Dependence on the assumed inflationary model which sets the initial conditions."]
context_windows:
  - module: COSMO-003
    excerpt: |
      Interpretation: Γ is a classical, coherently oscillating scalar whose quanta (“pressurons”) have mass m_Γ. A galactic‑scale ‘condensate’ need not be a thermal BEC; the cosmological mechanism is **misalignment**: Γ starts displaced from its minimum in the early universe; Hubble friction freezes it (Γ̇≈0) until H≈m_Γ, after which Γ oscillates and time‑averages to a **pressureless fluid**.
  - module: COSMO-003
    excerpt: |
      New species gammat with params {m_Gamma, lambda4, V_tail_parameters, Gamma_ini, dGamma_ini}.
      ...
      Config (CLASS‑style):
      Gamma_ini=1.2e18   # in reduced‑Planck units
      Gamma_ini_prime=0.0
poetic_connections:
  motifs: ["frozen potential", "cosmic friction", "awakened oscillator", "initial displacement"]
  evocative_lines:
    - "Hubble friction freezes it (Γ̇≈0) until H≈m_Γ"
    - "Γ starts displaced from its minimum in the early universe"
  association_matrix:
    - [ "SCALAR_FIELD_CONDENSATE", 0.9 ]
    - [ "HUBBLE_FRICTION", 0.8 ]
    - [ "COINCIDENCE_PROBLEM", 0.5 ]
formal_mappings:
  candidates:
    - target: Axion Misalignment Mechanism
      domain: Cosmology
      mapping_kind: conceptual
      equation_hint: |
        ρ_a(t_osc) ~ ½ m_a² a(t_osc)² θ_i² f_a²
      justification: |
        The process described for the Γ field—initial displacement during inflation, freezing by Hubble friction, and subsequent oscillation as cold dark matter when H ~ m_field—is identical to the standard misalignment mechanism for producing axion dark matter.
      references:
        - title: Cosmological evolution of a light scalar field
          where: Preskill, Wise, Wilczek, Phys. Lett. B 120, 127
          date: 1983-01-06
      confidence: 0.95
  adopted:
    - target: Axion Misalignment Mechanism
      rationale: The dynamics of Γ in the early universe as described in COSMO-003 are a direct application of the axion misalignment production mechanism to a generic scalar field. The terminology, physics (Hubble friction, onset of oscillation at H≈m), and cosmological role are identical.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The entire observed dark matter abundance (Ω_cdm ≈ 0.26) can be generated by the misalignment of the Γ field for a specific initial value, Γ_ini, given the potential V(Γ)."
      domain: phenomenology
      falsifier: "If, for a fixed and theoretically justified potential V(Γ), no value of Γ_ini < M_pl can reproduce the observed Ω_cdm without violating other constraints, such as from CMB isocurvature perturbations."
      status: proposed
      links: ["COSMO-003"]
naming_notes:
  collisions: ["The term 'misalignment' is common in optics, mechanical engineering, and data science."]
  disambiguation: |
    In the context of the Pirouette Framework and cosmology, 'Misalignment' refers specifically to the cosmological field production mechanism, not to mechanical, optical, or model-data misalignment.
crosslinks:
  near_synonyms: []
  antonyms: ["THERMAL_FREEZEOUT", "DECAY_PRODUCTION"]
  prerequisites: ["SCALAR_FIELD", "HUBBLE_EXPANSION"]
  downstream_effects: ["COLD_DARK_MATTER", "COINCIDENCE_PROBLEM"]
license: CC-BY-SA-4.0
---

# Misalignment

## Canonical (Pirouette)
The cosmological mechanism by which a coherently oscillating scalar field (e.g., Γ) acquires its initial energy density. In the early universe (when H ≫ m_Γ), the field is displaced from its potential minimum (Γ_ini ≠ 0) and frozen by Hubble friction (Γ̇ ≈ 0). When the Hubble parameter drops to H ≈ m_Γ, the field begins to oscillate around its minimum, and its time-averaged equation of state behaves as pressureless matter (w_Γ ≈ 0).

## EFT-First Summary
The Misalignment mechanism is the Pirouette Framework's implementation of the standard cosmological production mechanism for axion-like particles (ALPs). A scalar field Γ, displaced from its potential minimum during an early inflationary epoch, is held static by cosmic expansion (Hubble friction). As the universe expands and cools, this friction term weakens, and when the Hubble rate H becomes comparable to the particle's mass m_Γ, the field begins to oscillate, behaving as a pressureless fluid (cold dark matter). The final relic abundance is determined by the initial displacement Γ_ini and the mass m_Γ. (See: Preskill, Wise, Wilczek, 1983).

## Glossary Links
- See also: [[SCALAR_FIELD_CONDENSATE]], [[HUBBLE_FRICTION]], [[COLD_DARK_MATTER]]