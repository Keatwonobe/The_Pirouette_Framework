---
term: "Static Love Numbers"
canonical_id: "STATIC_LOVE_NUMBERS"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DYNA-BH-INT-001"]
---

---
term: Static Love Numbers
canonical_id: STATIC_LOVE_NUMBERS
symbol: \(k_l\)
aliases: [Tidal Love Numbers]
parents: [DYNA-BH-INT-001]
children: [XXP-GR-EXP]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DYNA-BH-INT-001
      lines: "§6"
      snippet: |
        Because the exterior is GR-vacuum and the core sits **inside** the potential barrier, **static Love numbers remain ~GR-black-hole–like (≈0)** at leading order; any nonzero tidal response appears only at \((\omega/\omega_c)^2\) through dynamical TT scattering—keeps EP and CPM intact.
  editors: [system-agent-alpha]
  review_log: []
triad:
  art: |
    An object's resistance to being stretched by the gravity of a companion. For a Pirouette black hole, the core is a diamond shielded by the horizon's one-way glass; it remains unseen and unyielding to the tidal caress of the outside universe.
  law: |
    The static, quadrupolar tidal Love number \(k_2\) for a compact object described by the Γ-Lighthouse Model is predicted to be zero at leading order. Any detectable, non-zero tidal response is a dynamic effect suppressed by \((\omega/\omega_c)^2\), and its measurement would falsify models that place new physics outside the horizon.
  philosophy: |
    This prediction demonstrates the model's conservatism. By confining new physics within a GR-like horizon and respecting the Coherent-Preserving Manifold (CPM), the model mimics a classical black hole's tidal rigidity. This makes it a minimal, hard-to-falsify alternative to both singular GR and many exotic compact objects which predict non-zero Love numbers.
pirouette_definition: |
  A set of dimensionless coefficients, \(k_l\), that quantify the \(l\)-th multipole moment induced on a self-gravitating body by an external static tidal field. For compact objects described by the Γ-Lighthouse Model (DYNA-BH-INT-001), the Γ-saturated core is causally shielded by an event horizon that is GR-like in the infrared limit. Consequently, the object exhibits no static tidal deformation, yielding \(k_l = 0\) at leading order, a result identical to that for classical black holes in General Relativity.
operational_definition:
  units: Dimensionless
  symbol_table:
    - name: \(k_l\)
      meaning: The \(l\)-th dimensionless tidal Love number.
      dimensions: dimensionless
      default_range: "For Γ-Lighthouse BHs, \(k_l \approx 0\). For neutron stars, \(k_2 \in [0.05, 0.15]\)."
    - name: Λ
      meaning: Dimensionless tidal deformability parameter, proportional to \(k_2\).
      dimensions: dimensionless
      default_range: "Probed in GW signals; Λ ≈ 0 for Pirouette BHs."
  measurement:
    procedures:
      - name: Gravitational Wave Inspiral Phasing
        outline: |
          During the late inspiral of a binary system (e.g., BH-BH or BH-NS), tidal forces deform the components. This deformation dissipates orbital energy, causing the inspiral to accelerate. This effect imprints a characteristic phase shift in the gravitational waveform, which is directly proportional to the tidal deformability parameter Λ (and thus the Love number \(k_2\)).
        expected_signals: [A GW signal from a binary containing a Pirouette black hole will show a phase evolution consistent with Λ=0, matching the prediction for a classical GR black hole.]
        pitfalls: [Low signal-to-noise ratio, statistical uncertainty, and waveform degeneracies between tidal effects and other parameters like component spins.]
context_windows:
  - module: DYNA-BH-INT-001
    excerpt: |
      Because the exterior is GR-vacuum and the core sits **inside** the potential barrier, **static Love numbers remain ~GR-black-hole–like (≈0)** at leading order; any nonzero tidal response appears only at \((\omega/\omega_c)^2\) through dynamical TT scattering—keeps EP and CPM intact.
  - module: DYNA-BH-INT-001
    excerpt: |
      **Tidal Love**: effectively zero at leading order; detection of large static Love numbers falsifies CPM-respecting interiors.
poetic_connections:
  motifs: [rigidity, tidal silence, unyielding, causal shielding, horizon-as-insulator]
  evocative_lines:
    - "The singularity is replaced by a phase—a yolk of time under pressure."
    - "Outside, the loom reads as perfect GR."
  association_matrix:
    - [ "GAMMA_SATURATED_CORE", 0.9 ]
    - [ "CPM", 0.8 ]
    - [ "BARRIER_FINITENESS", 0.6 ]
formal_mappings:
  candidates:
    - target: Tidal Love Number \(k_l\)
      domain: GR
      mapping_kind: operational
      equation_hint: |
        Q_{ij} = -k_2 \frac{R^5}{G} \mathcal{E}_{ij}
      justification: |
        The term directly corresponds to the standard tidal Love numbers used in General Relativity and astrophysics to describe the deformability of compact objects like neutron stars and black holes. The quantity is measured via its effect on the gravitational waveform phase during a binary inspiral. The Pirouette framework makes a specific physical prediction for its value in the case of its regularized black hole models.
      references:
        - title: Tidal Love Numbers of Neutron Stars
          where: The Astrophysical Journal, 677(2), 1216 (2008)
          date: 2008-04-20
        - title: Black holes in a tidal environment
          where: Phys. Rev. D 80, 084018 (2009)
          date: 2009-10-15
      confidence: 1.0
  adopted:
    - target: Tidal Love Number \(k_l\) (GR)
      rationale: The term is adopted directly from the GR literature, as it refers to the same physical observable. The novelty of the framework lies in its prediction for the value of \(k_l\), not in a redefinition of the term itself.
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "The static, quadrupolar Love number \(k_2\) of a non-spinning, spherically symmetric object described by the Γ-Lighthouse model is zero to leading order."
      domain: phenomenology
      falsifier: "A statistically significant (>5σ) measurement of a non-zero static tidal deformability (e.g., Λ > 1) for a compact object in the black hole mass range from a GW inspiral signal."
      status: proposed
      links: [DYNA-BH-INT-001, XXP-GR-EXP]
naming_notes:
  collisions: [The symbol \(k\) is heavily overloaded (wavenumber, Boltzmann constant, etc.). Context (gravitational waves, tidal effects) and the subscript \(l\) or 2 are crucial for disambiguation.]
  disambiguation: |
    It is critical to distinguish between *static* Love numbers, relevant to the low-frequency limit of a tidal field, and *dynamic* or frequency-dependent Love numbers, which describe the response to time-varying fields. The Pirouette prediction of zero applies to the static limit; dynamic effects are predicted to be non-zero but suppressed by \((\omega/\omega_c)^2\).
crosslinks:
  near_synonyms: [TIDAL_DEFORMABILITY]
  antonyms: []
  prerequisites: [GAMMA_SATURATED_CORE, CPM]
  downstream_effects: [GW_INSPIRAL_PHASE]
license: CC-BY-SA-4.0
---

# Static Love Numbers

## Canonical (Pirouette)
A measure of tidal deformability, which the model predicts is nearly zero, mimicking a classical black hole. The static Love numbers, \(k_l\), are dimensionless coefficients quantifying the multipole deformation of a body under an external tidal field. For Pirouette's regularized black holes (DYNA-BH-INT-001), the internal Γ-phase is shielded by a GR-like event horizon, preventing any static deformation. This results in the prediction that all static Love numbers are zero at leading order, a key feature distinguishing this model from many other exotic compact objects.

## EFT-First Summary
The Static Love Number maps directly to the standard tidal Love number, \(k_l\), used in General Relativity to parameterize the tidal deformability of a compact body. It is operationally defined via its impact on the phase evolution of gravitational waves from a binary inspiral. While neutron stars have non-zero \(k_2\), classical black holes in GR have \(k_2=0\). The Pirouette Γ-Lighthouse model predicts its regularized black holes will also measure \(k_2=0\), making them observationally indistinguishable from GR black holes in this channel.

## Glossary Links
- See also: [Tidal Deformability](TIDAL_DEFORMABILITY), [Γ-Saturated Core](GAMMA_SATURATED_CORE), [Coherent-Preserving Manifold (CPM)](CPM)