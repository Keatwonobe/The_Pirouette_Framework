---
term: "Phase Inversion of Temporal Curvature"
canonical_id: "PHASE_INVERSION_OF_TEMPORAL_CURVATURE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DYNA-Γ-001_the_pressurons_identity"]
---

---
term: Phase Inversion of Temporal Curvature
canonical_id: PHASE_INVERSION_OF_TEMPORAL_CURVATURE
symbol: (⤄)
aliases: [Temporal Breathing Mode, Coherence Recoil]
parents: [DYNA-Γ-001]
children: [DYNA-Γ-002, COSMO-Γ-001]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DYNA-Γ-001
      lines: "§6"
      snippet: |
        The Γ-particle represents the *breathing mode* of time’s fabric. Its pseudoscalar nature stems from **phase inversion of temporal curvature**, mirroring the alternation of compression and rarefaction in a standing wave.
  editors: [Agent: Pirouette Knowledge Synthesis]
  review_log: []
triad:
  art: |
    The universe inhaling between heartbeats. The alternating compression and rarefaction of time's fabric gives rise to a resonant pulse, whose quantum is the Pressuron.
  law: |
    The fundamental excitation of the temporal pressure field (Γ) must transform as a pseudoscalar (Parity = -1) under temporal inversion (t → -t), resulting in a derivative coupling to matter and a narrow 17 MeV decay signature into e⁺e⁻ pairs.
  philosophy: |
    This mechanism grounds abstract quantum numbers like parity in a physical, dynamic process. It recasts the Pressuron not as a fundamental particle, but as a transient, dissipative echo of spacetime's own coherence-maintaining activity.
pirouette_definition: |
  The dynamic mechanism responsible for the pseudoscalar nature of the Pressuron (Γ). It describes the oscillatory behavior of the temporal pressure field, which, like a standing wave, alternates between phases of compression and rarefaction. This phase inversion under time reversal (t → -t) is what assigns odd parity (P=-1) to the Γ field excitation, distinguishing it from a true scalar.
operational_definition:
  units: Dimensionless (describes a transformational property)
  symbol_table:
    - name: P
      meaning: Parity operator eigenvalue under temporal inversion (t → -t)
      dimensions: dimensionless
      default_range: {-1} for the Pressuron field
  measurement:
    procedures:
      - name: Angular Correlation of Decay Products
        outline: |
          Generate Pressurons (Γ) in a beam-dump experiment and isolate the 17 MeV e⁺e⁻ resonance. Measure the angular distribution of the outgoing electron and positron relative to the Γ production axis. A pseudoscalar source produces a characteristic anisotropic distribution (e.g., proportional to sin²θ), whereas a scalar would decay isotropically.
        expected_signals: [A narrow resonance peak at 17 MeV in the e⁺e⁻ invariant mass spectrum., Anisotropic angular distribution of decay leptons consistent with a J^PC = 0⁻⁺ state.]
        pitfalls: [Insufficient statistics to resolve the angular distribution., Contamination from Standard Model backgrounds (e.g., radiative Bhabha scattering) that can mimic anisotropy.]
context_windows:
  - module: DYNA-Γ-001
    excerpt: |
      The Γ-particle represents the *breathing mode* of time’s fabric. Its pseudoscalar nature stems from **phase inversion of temporal curvature**, mirroring the alternation of compression and rarefaction in a standing wave. Decay into matter is thus the literal dissipation of coherent time-pressure into the particle sea—a physical analog to a coherence collapse.
  - module: DYNA-Γ-001
    excerpt: |
      The Pressuron is not a boson in the usual sense—it is the **phase recoil of the universe** when mass bends time faster than coherence can repair itself. To measure it is to catch the universe inhaling between its own heartbeats.
poetic_connections:
  motifs: [standing wave, breathing mode, coherence collapse, phase recoil]
  evocative_lines:
    - "We sought a particle and found a pulse of time."
    - "...to catch the universe inhaling between its own heartbeats."
  association_matrix:
    - [ "Pressuron", 0.9 ]
    - [ "Temporal_Pressure", 0.8 ]
    - [ "Pseudoscalar", 0.7 ]
    - [ "Coherence_Stress", 0.5 ]
formal_mappings:
  candidates:
    - target: Axion-like particle (ALP)
      domain: EFT
      mapping_kind: operational
      equation_hint: |
        L_int ∝ (g/m) ∂_μ(pseudoscalar) J^μ_axial
      justification: |
        Operationally, the Pressuron (Γ) behaves as a light pseudoscalar boson with derivative couplings, a defining feature of ALPs. While many ALPs couple primarily to gauge fields (like photons), the Pressuron's primary coupling is to the axial fermion current, with a strength proportional to fermion mass. Experimental searches for ALPs provide direct constraints on the Γ → γγ channel.
      references:
        - title: Axions and Other Similar Particles
          where: PDG Review of Particle Physics
          date: 2024-08-01
      confidence: 0.7
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The resonance responsible for the 17 MeV leptonic anomaly must have quantum numbers J^PC = 0⁻⁺ (pseudoscalar)."
      domain: experiment
      falsifier: "Observation of a 17 MeV resonance with J^PC = 0⁺⁺ (scalar), confirmed via isotropic decay distributions, would refute the Phase Inversion model for its origin."
      status: proposed
      links: [DYNA-Γ-001]
naming_notes:
  collisions: [General Relativity (GR)]
  disambiguation: |
    The term 'curvature' here refers to the gradient of the temporal pressure field, not the geometric curvature of spacetime described by the Ricci tensor in GR. Phase Inversion is a kinetic, oscillatory phenomenon, not a static property of the background metric.
crosslinks:
  near_synonyms: [AUTOPOIETIC_RESONANCE]
  antonyms: [SCALAR_EXCITATION]
  prerequisites: [TEMPORAL_PRESSURE]
  downstream_effects: [PRESSURON, LEPTONIC_ANOMALY]
license: CC-BY-SA-4.0
---

# Phase Inversion of Temporal Curvature

## Canonical (Pirouette)
The dynamic mechanism responsible for the pseudoscalar nature of the Pressuron (Γ). It describes the oscillatory behavior of the temporal pressure field, which, like a standing wave, alternates between phases of compression and rarefaction. This phase inversion under time reversal (t → -t) is what assigns odd parity (P=-1) to the Γ field excitation, distinguishing it from a true scalar.

## EFT-First Summary
This mechanism is operationally analogous to the dynamics of an Axion-Like Particle (ALP), a light pseudoscalar with derivative couplings. While ALPs typically couple to gauge fields, Phase Inversion sources a pseudoscalar (the Pressuron) that couples to fermion mass via the axial current. Experimental searches for ALPs in the ~17 MeV range provide strong, albeit indirect, constraints on this model, particularly for its subdominant two-photon decay channel.

## Glossary Links
- See also: Pressuron (Γ), Pseudoscalar, Temporal Pressure