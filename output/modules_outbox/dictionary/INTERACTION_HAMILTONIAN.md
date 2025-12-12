---
term: "Interaction Hamiltonian"
canonical_id: "INTERACTION_HAMILTONIAN"
symbol: "H_int"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-002"]
---

---
term: Interaction Hamiltonian
canonical_id: INTERACTION_HAMILTONIAN
symbol: H_int
aliases: [interaction energy]
parents: [MATH-002]
children: [XXP-001]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-002
      lines: "L38-L46"
      snippet: |
        To find the g-factor, we must describe how this resonance interacts with an external magnetic field B. The energy of this interaction is described by a term in the system's Hamiltonian, H_int.

        H_int = -mu . B

        Here, mu is the particle's magnetic moment, which is proportional to its spin angular momentum S.
  editors: [system-agent]
  review_log: []
triad:
  art: |
    The score for the dance between a resonance and the world. It is the touch of an external field, felt by the particle as a change in the energy of its own rhythm.
  law: |
    The interaction energy of a resonance in an external magnetic field is the negative dot product of the resonance's magnetic moment (μ) and the magnetic field vector (B). H_int = -μ · B.
  philosophy: |
    This term is the essential bridge between the internal, abstract geometry of a resonance and external, measurable physics. It translates the topological nature of the particle's path (its 720° cycle) into a concrete energy shift, making the unseeable geometry observable through its energetic consequences.
pirouette_definition: |
  The term in the total Hamiltonian that quantifies the potential energy of a resonance due to its coupling with an external field, typically magnetic. It is defined as the negative dot product of the resonance's magnetic moment and the external magnetic field. The analysis of H_int is the primary tool for revealing the topological doubling effect (g=2) that arises from a resonance's 720° spinor path.
operational_definition:
  units: Joules (J)
  symbol_table:
    - name: H_int
      meaning: Interaction Hamiltonian; the energy of interaction.
      dimensions: M L^2 T^-2
      default_range: contextual (e.g., 10^-25 J for electrons in lab-scale fields)
    - name: μ
      meaning: Magnetic moment of the resonance.
      dimensions: I L^2
      default_range: ~9.27e-24 J/T for an electron
    - name: B
      meaning: External magnetic field vector.
      dimensions: M T^-2 I^-1
      default_range: 0.1 - 10 T in experimental contexts
  measurement:
    procedures:
      - name: Zeeman Spectroscopy / Electron Spin Resonance (ESR)
        outline: |
          1. Place a sample of particles in a strong, uniform, and tunable magnetic field (B).
          2. Irradiate the sample with electromagnetic radiation (microwaves) of a fixed frequency (ν).
          3. The Interaction Hamiltonian splits the energy levels of the resonance by an amount ΔE = |H_int(spin up) - H_int(spin down)|, which is proportional to B.
          4. Slowly sweep the magnetic field B until the energy splitting ΔE matches the photon energy hν.
          5. At this resonance condition, absorption of the radiation will be maximal. Measuring the resonant field strength B_res directly quantifies H_int.
        expected_signals: [A sharp absorption peak in the microwave power spectrum as a function of B.]
        pitfalls: [Magnetic field inhomogeneity leading to line broadening, thermal noise, saturation of the signal at high microwave power.]
context_windows:
  - module: MATH-002
    excerpt: |
      To find the g-factor, we must describe how this resonance interacts with an external magnetic field B. The energy of this interaction is described by a term in the system's Hamiltonian, H_int. H_int = -mu . B. Here, mu is the particle's magnetic moment, which is proportional to its spin angular momentum S.
  - module: MATH-002
    excerpt: |
      The key insight is that the interaction energy H_int depends on the rate of change of the resonance's phase as it couples to the magnetic field... The magnetic moment mu is a measure of the energy change per unit of magnetic field, which is coupled to the full 720° cycle of the resonance. However, the spin angular momentum S is conventionally defined by the physics of a 360° rotation.
poetic_connections:
  motifs: [the dance, field coupling, topological signature, energetic echo]
  evocative_lines:
    - "The math is not an approximation; it is the description of the dance itself."
    - "The electron's spin is a twist in time."
  association_matrix:
    - [ "MAGNETIC_MOMENT", 0.9 ]
    - [ "G_FACTOR", 0.8 ]
    - [ "SPIN", 0.7 ]
formal_mappings:
  candidates:
    - target: Zeeman Hamiltonian (H_Zeeman)
      domain: SM|AMO
      mapping_kind: mathematical
      equation_hint: |
        H_Zeeman = -μ · B
      justification: |
        The Pirouette Interaction Hamiltonian is mathematically and operationally identical to the Zeeman term in the standard quantum mechanical Hamiltonian. It describes the potential energy of a magnetic dipole in an external B-field. While the Pirouette Framework re-derives the origin of μ from a topological basis, the interaction formalism itself is standard.
      references:
        - title: Introduction to Quantum Mechanics
          where: 3rd ed., D.J. Griffiths, Ch. 6
          date: 2018-01-01
      confidence: 0.98
  adopted:
    - target: Zeeman Hamiltonian (H_Zeeman)
      rationale: The one-to-one correspondence in mathematical form, operational meaning, and experimental consequence makes this mapping definitive.
      confidence: 0.98
constraints_and_falsifiers:
  claims:
    - statement: "The Interaction Hamiltonian H_int = -μ · B is the complete description of the coupling between a spin-1/2 resonance's magnetic moment and a uniform external magnetic field."
      domain: theory|experiment
      falsifier: "The discovery of a deviation from the linear energy splitting predicted by this Hamiltonian in a pure, uniform magnetic field that could not be explained by known higher-order corrections. This would imply an additional, undiscovered interaction term."
      status: supported
      links: [MATH-002]
naming_notes:
  collisions: [H (total Hamiltonian), H_0 (free Hamiltonian)]
  disambiguation: |
    H_int specifies only the energy component arising from external field interactions. It must be distinguished from the free Hamiltonian (H_free), which describes the particle's dynamics in the absence of a field. The total Hamiltonian is H_total = H_free + H_int.
crosslinks:
  near_synonyms: [ZEEMAN_HAMILTONIAN]
  antonyms: [FREE_HAMILTONIAN]
  prerequisites: [MAGNETIC_MOMENT, SPIN]
  downstream_effects: [G_FACTOR, ZEEMAN_EFFECT]
license: CC-BY-SA-4.0
---

# Interaction Hamiltonian

## Canonical (Pirouette)
The term in the total Hamiltonian that quantifies the potential energy of a resonance due to its coupling with an external field, typically magnetic. It is defined as the negative dot product of the resonance's magnetic moment and the external magnetic field. The analysis of H_int is the primary tool for revealing the topological doubling effect (g=2) that arises from a resonance's 720° spinor path.

## EFT-First Summary
In standard quantum mechanics, the Interaction Hamiltonian `H_int` is identical to the **Zeeman Hamiltonian**, `H = -μ · B`, which describes the energy of a magnetic dipole in a magnetic field. This term is responsible for the Zeeman effect, where atomic spectral lines split in the presence of a magnetic field. The Pirouette framework adopts this formalism directly but provides a novel geometric derivation for the magnetic moment `μ` and its associated g-factor.

## Glossary Links
- See also: [Magnetic Moment](./magnetic_moment.md), [g-factor](./g_factor.md), [Spin](./spin.md), [Zeeman Effect](./zeeman_effect.md)