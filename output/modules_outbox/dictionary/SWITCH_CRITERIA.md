---
term: "Switch criteria"
canonical_id: "SWITCH_CRITERIA"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["COSMO-005"]
---

---
term: Switch criteria
canonical_id: SWITCH_CRITERIA
symbol: 
aliases: [Field-fluid switch, fluid approximation condition]
parents: [COSMO-005]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: COSMO-005
      lines: "SECT-Γ-A-CMB §2"
      snippet: |
        Switch criteria (field↔fluid):
        • Use fluid mapping when m_H/H>50 and k/a<κ_switch m_H (default κ_switch=0.5).
        • Fall back to full field if either condition fails.
  editors: [Pirouette Agent]
  review_log: []
triad:
  art: |
    A phase transition in the calculational sea, where the fine-grained quantum foam is trusted to behave like a smooth, predictable current. It is the moment a storm's chaos is mapped by its prevailing winds, resolving only what is necessary.
  law: |
    An effective fluid description of a scalar field is valid if and only if the field's oscillation frequency (m_H) is much greater than the cosmic expansion rate (H) and the probed physical wavelength (a/k) is much larger than the field's Compton wavelength (1/m_H). The numerical impact of the transition must be below a specified tolerance (<0.2% on CMB spectra).
  philosophy: |
    To balance computational fidelity with feasibility. The criteria encode the physical intuition that micro-scale dynamics can be coarse-grained into a macroscopic fluid, allowing efficient evolution on large scales without sacrificing accuracy where it matters. This embodies the core principle of effective field theory: integrate out what you don't need to resolve.
pirouette_definition: |
  A pair of inequalities that govern the transition between a full scalar field evolution and its effective fluid approximation within a cosmological simulation. The criteria ensure the fluid description is only used when the field is oscillating rapidly compared to the Hubble time (`m_H/H > switch_threshold_m_over_H`) and for modes with physical wavelengths much larger than the field's Compton wavelength (`k/a < κ_switch m_H`). Failure of either condition triggers a fallback to the more computationally expensive but more accurate field-level description.
operational_definition:
  units: Dimensionless
  symbol_table:
    - name: m_H
      meaning: Mass of the heavy field quanta
      dimensions: M
      default_range: ~17 MeV
    - name: H
      meaning: Hubble parameter
      dimensions: T⁻¹
      default_range: contextual
    - name: k
      meaning: Comoving wavenumber
      dimensions: L⁻¹
      default_range: contextual
    - name: a
      meaning: Cosmological scale factor
      dimensions: dimensionless
      default_range: contextual
    - name: switch_threshold_m_over_H
      meaning: Threshold for the energy/timescale criterion
      dimensions: dimensionless
      default_range: 50
    - name: κ_switch
      meaning: Threshold for the length scale criterion
      dimensions: dimensionless
      default_range: 0.5
  measurement:
    procedures:
      - name: Switch Threshold Scan (V5)
        outline: |
          Run a cosmological simulation (e.g., CLASS) for a fiducial `gammat_superfluid` model. Re-run the simulation with `switch_threshold_m_over_H` and `kappa_switch` doubled. Compare the output CMB power spectra (TT, TE, EE) between the two runs.
        expected_signals: [Fractional difference in C_ℓ spectra below tolerance (e.g., 0.2%), Log of switch events in `gamma_sf_flags.json` artifact]
        pitfalls: [Numerical instabilities near the switch boundary, Discontinuities in perturbation evolution from incorrect fallback logic]
context_windows:
  - module: COSMO-005
    excerpt: |
      Switch criteria (field↔fluid): Use fluid mapping when m_H/H>50 and k/a<κ_switch m_H (default κ_switch=0.5). Fall back to full field if either condition fails.
  - module: COSMO-005
    excerpt: |
      Stability & Validation Suite ... Threshold scans: doubling switch thresholds changes TT/TE/EE by <0.2% (V5).
poetic_connections:
  motifs: [coarse-graining, effective description, phase boundary, computational efficiency]
  evocative_lines:
    - "Fall back to full field if either condition fails."
    - "reproduces CDM on CMB scales while generating small‑scale suppression"
  association_matrix:
    - [ "EFFECTIVE_SOUND_SPEED", 0.8 ]
    - [ "SCALAR_FIELD", 0.9 ]
    - [ "COMPUTATIONAL_COST", 0.7 ]
formal_mappings:
  candidates: []
  adopted:
    - target: WKB Approximation Validity
      domain: Math
      mapping_kind: conceptual
      equation_hint: |
        m_H ≫ H  ⇔  ω ≫ |(1/ω) dω/dt|
      justification: |
        The condition `m_H ≫ H` is a direct analogue to the WKB (or adiabatic) approximation for an oscillator whose fundamental frequency (`m_H`) changes slowly. This allows averaging over oscillations to derive an effective, non-oscillatory fluid. The `k/a < m_H` condition ensures gradient energy terms are subdominant, which is required for the simplest local fluid description to hold.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "The impact of changing the switch criteria thresholds (`switch_threshold_m_over_H`, `kappa_switch`) by a factor of 2 on the CMB TT/TE/EE power spectra is less than 0.2% for ℓ < 2500."
      domain: phenomenology
      falsifier: "A direct numerical test using the `gammat_superfluid` module shows a change in C_ℓs greater than 0.2%, indicating either a poor fluid approximation near the boundary or numerical artifacts from the switching logic."
      status: supported
      links: [COSMO-005]
naming_notes:
  collisions: []
  disambiguation: |
    These criteria apply specifically to the numerical transition between computational methods (field vs. fluid) for a single physical entity. They should not be confused with physical phase transitions within the fluid itself, nor with criteria for switching between cosmological epochs (e.g., radiation to matter domination).
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [EFFECTIVE_FLUID_MAPPING]
  downstream_effects: [CMB_SPECTRA_ARTIFACTS]
license: CC-BY-SA-4.0
---

# Switch criteria

## Canonical (Pirouette)
A pair of inequalities that govern the transition between a full scalar field evolution and its effective fluid approximation within a cosmological simulation. The criteria ensure the fluid description is only used when the field is oscillating rapidly compared to the Hubble time (`m_H/H > switch_threshold_m_over_H`) and for modes with physical wavelengths much larger than the field's Compton wavelength (`k/a < κ_switch m_H`). Failure of either condition triggers a fallback to the more computationally expensive but more accurate field-level description.

## EFT-First Summary
In the language of effective field theory, the switch criteria define the regime of validity for integrating out the fast-oscillating massive modes of a scalar field. The `m_H ≫ H` condition ensures adiabaticity, allowing the field's dynamics to be time-averaged into an effective equation of state, analogous to the WKB approximation. The `k/a ≪ m_H` condition ensures that spatial gradients are subdominant to the mass, preventing gradient instabilities and justifying a description based solely on local density and pressure.

## Glossary Links
- See also: `EFFECTIVE_FLUID_MAPPING`