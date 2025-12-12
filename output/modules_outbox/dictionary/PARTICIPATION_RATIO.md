---
term: "Participation Ratio"
canonical_id: "PARTICIPATION_RATIO"
symbol: "PR_i"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-PHYS-002_the_neutrino_knot"]
---

---
term: Participation Ratio
canonical_id: PARTICIPATION_RATIO
symbol: PR_i
aliases: []
parents: [DOMA-PHYS-002]
children: []
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-PHYS-002
      snippet: |
        PR_i = (∑_α |U_{αi}|^4)^-1: The Participation Ratio, a measure of how many flavor states a given mass state "participates" in. It is a measure of a state's "mixedness."
  editors: [GPT-4_Agent]
  review_log: []
triad:
  art: |
    A state's identity is not a solo, but the resonance of a chord. The Participation Ratio counts how many notes are sounding at once, measuring the richness of its harmonic composition.
  law: |
    The Participation Ratio PR_i of a mass eigenstate i is the inverse of the sum of the fourth powers of its mixing matrix elements, PR_i = (∑_α |U_{αi}|^4)^-1. It ranges from 1 (a pure state) to 3 (a maximally mixed state in a 3-flavor system).
  philosophy: |
    This metric reframes a state's identity away from a single label towards a distributed, democratic measure of its composition. Mass, in this view, is not an intrinsic property but emerges from the geometry of this participation.
pirouette_definition: |
  The Participation Ratio (PR_i) is a dimensionless quantity that measures the effective number of flavor states (α) contributing to a given mass eigenstate (i). It is calculated as the inverse of the sum of the fourth powers of the magnitudes of the PMNS mixing matrix elements, |U_{αi}|. A value of PR_i = 1 indicates a pure state participating in only one flavor, while PR_i = 3 indicates a state that is maximally mixed across the three neutrino flavors.
operational_definition:
  units: dimensionless
  symbol_table:
    - name: PR_i
      meaning: Participation Ratio for mass eigenstate i
      dimensions: dimensionless
      default_range: "[1, 3]"
    - name: U_{αi}
      meaning: PMNS mixing matrix element between flavor α and mass state i
      dimensions: dimensionless
      default_range: "complex value with magnitude [0, 1]"
  measurement:
    procedures:
      - name: Inference from Global Oscillation Fits
        outline: |
          1. Determine the best-fit values and uncertainties for the PMNS matrix elements (U_{αi}) from a global analysis of neutrino oscillation data.
          2. Compute PR_i for each mass state using the definitional formula PR_i = (∑_α |U_{αi}|^4)^-1.
          3. Propagate experimental uncertainties from the mixing parameters to establish the uncertainty on PR_i.
        expected_signals: [Not a direct observable. It is a quantity derived from measured oscillation probabilities.]
        pitfalls: [Uncertainties in mixing angles (θ₂₃, θ₁₃) and the CP-violating phase (δ_CP) directly limit the precision of PR_i., Assumes a unitary 3x3 PMNS matrix; evidence of non-unitarity would require re-evaluation of the definition.]
context_windows:
  - module: DOMA-PHYS-002
    excerpt: |
      PR_i = (∑_α |U_{αi}|^4)^-1: The Participation Ratio, a measure of how many flavor states a given mass state "participates" in. It is a measure of a state's "mixedness." This law proposes that a neutrino's mass is a direct consequence of its internal geometry, as described by the mixing matrix U.
  - module: DOMA-PHYS-002
    excerpt: |
      The Pirouette Neutrino Mass Law... posits that the absolute mass of each neutrino mass eigenstate (m_i) is not an intrinsic property, but an emergent one, governed by a geometric relationship between a base mass scale and the state's structural properties...
      $$ m_i = \mu_\nu\; \left(\frac{\mathrm{PR}_i}{3}\right)^{p}\; \left(\mathrm{Purity}_i\right)^{q} $$
poetic_connections:
  motifs: [mixedness, participation, democracy, chorus, geometric identity]
  evocative_lines:
    - "A neutrino's mass is a direct consequence of its internal geometry..."
    - "...we found a constellation."
  association_matrix:
    - [ "PMNS_MATRIX", 1.0 ]
    - [ "PURITY", 0.9 ]
    - [ "PIROUETTE_NEUTRINO_MASS_LAW", 0.8 ]
formal_mappings:
  candidates:
    - target: Inverse Participation Ratio (IPR)
      domain: CM
      mapping_kind: mathematical
      equation_hint: |
        PR = 1 / IPR, where IPR = ∑_n |ψ_n|^4
      justification: |
        The formula for PR_i is the reciprocal of the standard Inverse Participation Ratio (IPR) used in condensed matter physics to quantify the number of sites over which a quantum state is delocalized. Here, "sites" are replaced by "flavor states." It is a measure of the non-sparseness of a state vector.
      references:
        - title: Anderson transitions
          where: Reviews of Modern Physics, 80(4), 1355
          date: 2008-10-27
      confidence: 0.95
  adopted:
    - target: Reciprocal of Inverse Participation Ratio (1/IPR)
      rationale: The mathematical identity is exact. It repurposes a well-understood tool for quantifying quantum state delocalization from condensed matter to flavor physics.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The Participation Ratio is a primary geometric factor, alongside Purity, that determines a neutrino's mass via the Pirouette Neutrino Mass Law."
      domain: phenomenology
      falsifier: "Future, more precise measurements of neutrino mixing parameters and mass splittings could yield values that are irreconcilable with the Pirouette Neutrino Mass Law for any choice of its exponents (p, q). This would falsify the claimed physical role of PR_i in mass generation."
      status: proposed
      links: [DOMA-PHYS-002]
naming_notes:
  collisions: [Inverse Participation Ratio (IPR)]
  disambiguation: |
    While mathematically equivalent to 1/IPR from condensed matter physics, the term "Participation Ratio" is used to emphasize the active contribution of multiple flavor states to a single mass eigenstate's identity. It focuses on compositional "mixedness" rather than spatial "delocalization".
crosslinks:
  near_synonyms: []
  antonyms: [PURITY]
  prerequisites: [PMNS_MATRIX]
  downstream_effects: [PIROUETTE_NEUTRINO_MASS_LAW]
license: CC-BY-SA-4.0
---

# Participation Ratio

## Canonical (Pirouette)
The Participation Ratio (PR_i) is a dimensionless quantity that measures the effective number of flavor states (α) contributing to a given mass eigenstate (i). It is calculated as the inverse of the sum of the fourth powers of the magnitudes of the PMNS mixing matrix elements, |U_{αi}|. A value of PR_i = 1 indicates a pure state participating in only one flavor, while PR_i = 3 indicates a state that is maximally mixed across the three neutrino flavors.

## EFT-First Summary
Operationally, the Participation Ratio is the reciprocal of the Inverse Participation Ratio (IPR), a standard measure from condensed matter physics used to quantify the delocalization of a quantum state. In the context of neutrino physics, it measures the effective number of flavor eigenstates that constitute a given mass eigenstate. High PR indicates a highly mixed state, a key geometric input to the Pirouette Neutrino Mass Law. (See: Evers & Mirlin, Rev. Mod. Phys. 80, 1355, 2008).

## Glossary Links
- See also: [Purity](PURITY), [Pirouette Neutrino Mass Law](PIROUETTE_NEUTRINO_MASS_LAW)