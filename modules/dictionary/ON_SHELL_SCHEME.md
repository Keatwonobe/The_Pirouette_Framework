---
term: "On-Shell Scheme"
canonical_id: "ON_SHELL_SCHEME"
symbol: ""
aliases: [OS Scheme]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-027"]
---

---
term: On-Shell Scheme
canonical_id: ON_SHELL_SCHEME
symbol: OS
aliases: [OS Scheme]
parents: [MATH-027]
children: []
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-027
      lines: "§4"
      snippet: |
        Define counterterm Lagrangian
        \(
        \delta\mathcal L
        = \delta Z_{Ki}\,|\partial Ki|^2
        - \delta m_{Ki}^2\,|Ki|^2
        - \cdots
        \)
        with OS conditions
        \[
        \Sigma_{Ki}(p^2=m_{Ki}^2)=0,\qquad
        \left.\frac{d\Sigma_{Ki}}{dp^2}\right|_{p^2=m_{Ki}^2}=0,
        \qquad
        \Pi_{\mu\nu}(0)=0,
        \]
  editors: [GPT-4]
  review_log: []
triad:
  art: |
    The scheme is an anchor cast from the ship of theory into the harbor of measurement. It demands that the calculated mass of a particle is precisely the mass we observe, ensuring our mathematical charts describe the real world. All abstract fluctuations are pinned to this concrete, physical truth.
  law: |
    The renormalized parameters of the theory—masses and coupling constants—are defined by requiring that they match their experimentally measured values for physical, on-shell particles. For a scalar field like Ki, its physical mass \(m_{Ki}\) is defined as the pole of the full propagator, and the residue of the pole is fixed to unity. This is enforced by setting the self-energy \(\Sigma(p^2)\) and its derivative \(d\Sigma/dp^2\) to zero at \(p^2=m_{Ki}^2\).
  philosophy: |
    The On-Shell Scheme provides a physically intuitive bridge between the abstract parameters of a Lagrangian and the concrete results of experiment. It insists that core concepts like "mass" and "charge" are not floating mathematical symbols, but are defined by the very operations used to measure them. This grounds the entire perturbative expansion in empirical reality, making the theory's predictions directly testable.
pirouette_definition: |
  A set of renormalization conditions that remove divergences from loop calculations by defining the theory's parameters in terms of physically observable quantities. For the Ki field, the physical mass \(m_{Ki}\) is defined as the location of the pole in its full propagator. This is implemented by introducing counterterms (e.g., \(\delta Z_{Ki}\), \(\delta m_{Ki}^2\)) whose values are fixed by requiring the real part of the Ki self-energy \(\Sigma_{Ki}(p^2)\) and its derivative with respect to \(p^2\) to vanish at \(p^2=m_{Ki}^2\). Similarly, the physical electric charge is defined via the photon self-energy at zero momentum transfer (\(\Pi_{\mu\nu}(0)=0\)).
operational_definition:
  units: Dimensionless (a set of procedural conditions).
  symbol_table:
    - name: \(m_{Ki}\)
      meaning: Physical (renormalized) mass of the Ki particle.
      dimensions: M
      default_range: Contextual; defined by experiment.
    - name: \(\Sigma_{Ki}(p^2)\)
      meaning: The one-particle-irreducible (1PI) self-energy of the Ki field.
      dimensions: M²L⁻²T² (or M² in natural units).
      default_range: Calculated from loop diagrams.
    - name: \(\delta Z_{Ki}\)
      meaning: Wavefunction renormalization counterterm for the Ki field.
      dimensions: Dimensionless.
      default_range: Calculated to cancel divergences.
    - name: \(\delta m_{Ki}^2\)
      meaning: Mass counterterm for the Ki field.
      dimensions: M²L⁻²T² (or M² in natural units).
      default_range: Calculated to cancel divergences.
  measurement:
    procedures:
      - name: Mass and Coupling Renormalization
        outline: |
          1.  Calculate the 1PI self-energy \(\Sigma_{Ki}(p^2)\) for the Ki field to a desired loop order using the bare Lagrangian. The result will typically be divergent.
          2.  Introduce counterterms \(\delta Z_{Ki}\) and \(\delta m_{Ki}^2\). The full propagator becomes \(i / (p^2 - m_{0}^2 - \Sigma_{Ki}(p^2) + \delta Z_{Ki} p^2 - \delta m_{Ki}^2)\).
          3.  Impose the two On-Shell conditions:
              a. The real part of the self-energy plus counterterms must vanish at the physical mass: \(\text{Re}[\Sigma_{Ki}(p^2=m_{Ki}^2)] - \delta m_{Ki}^2 + \delta Z_{Ki} m_{Ki}^2 = 0\). This defines \(m_{Ki}\) as the pole.
              b. The derivative of the real part of the self-energy plus counterterms must vanish at the physical mass: \(\text{Re}\left[\frac{d\Sigma_{Ki}}{dp^2}\right]_{p^2=m_{Ki}^2} + \delta Z_{Ki} = 0\). This ensures the pole has residue 1.
          4.  Solve these two equations to fix the finite parts of the counterterms \(\delta Z_{Ki}\) and \(\delta m_{Ki}^2\).
          5.  Use these renormalized parameters in calculations of physical observables, such as scattering cross-sections.
        expected_signals: [A sharp resonance peak in scattering cross-sections at an energy corresponding to the particle's physical mass \(m_{Ki}\).]
        pitfalls: [The scheme is cumbersome for theories with massless charged particles (e.g., QED electrons) due to infrared divergences that complicate the definition of an on-shell state. It is also less practical than scale-dependent schemes (like MS-bar) in theories like QCD where the fundamental fields are not asymptotic states.]
context_windows:
  - module: MATH-027
    excerpt: |
      Define counterterm Lagrangian
      \( \delta\mathcal L = \delta Z_{Ki}\,|\partial Ki|^2 - \delta m_{Ki}^2\,|Ki|^2 - \delta\lambda_{Ki}\,|Ki|^4 - \delta Z_e\, e\, A\!\cdot\!J_{Ki} \cdots \)
      with OS conditions
      \[ \Sigma_{Ki}(p^2=m_{Ki}^2)=0,\qquad \left.\frac{d\Sigma_{Ki}}{dp^2}\right|_{p^2=m_{Ki}^2}=0, \qquad \Pi_{\mu\nu}(0)=0, \]
      and analogous for \(\Gamma\) when...
  - module: MATH-027
    excerpt: |
      The observer-frame Feynman propagator is
      \[ \Delta_{Ki}(p)=\frac{i}{p^2 - m_{Ki}^2 + i\varepsilon} \]
      The on-shell scheme ensures that \(m_{Ki}\) in this expression is the true, experimentally measured mass, after all quantum corrections encapsulated in the self-energy \(\Sigma_{Ki}(p^2)\) have been absorbed into the definition of the mass and field normalization.
poetic_connections:
  motifs: [anchoring, physical reality, tuning, pole definition, empirical grounding]
  evocative_lines:
    - "with OS conditions"
  association_matrix:
    - [ "SELF_ENERGY", 0.9 ]
    - [ "RENORMALIZATION_GROUP", 0.7 ]
    - [ "PHYSICAL_MASS", 0.9 ]
    - [ "COUNTERTERM", 0.8 ]
formal_mappings:
  candidates: []
  adopted:
    - target: On-Shell Renormalization Scheme
      domain: QFT
      mapping_kind: mathematical
      equation_hint: |
        Full Propagator: \( \Delta(p) = \frac{i Z}{p^2 - m^2} \) near the pole.
        OS Conditions: \( \text{Re}[\Sigma(p^2=m^2)] = 0 \) and \( \text{Re}\left[\frac{d\Sigma}{dp^2}\right]_{p^2=m^2} = 0 \). (Note: Pirouette module combines counterterms with \(\Sigma\)).
      justification: |
        The conditions defined in MATH-027 are a direct implementation of the standard On-Shell (OS) renormalization scheme used in Quantum Field Theory, particularly in QED and the Standard Model's electroweak sector. It defines the physical mass as the pole of the two-point function and fixes the field normalization (residue) to one. This is a textbook procedure for connecting theoretical parameters to measurable quantities.
      references:
        - title: An Introduction to Quantum Field Theory
          where: "Chapter 10, Peskin & Schroeder"
          date: 1995-10-01
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: 'The parameters defined by the OS scheme, such as \(m_{Ki}\) and the physical charge \(e\), are consistent across all scattering experiments and decay processes calculated within the Pirouette EFT.'

      domain: phenomenology
      falsifier: "A persistent, statistically significant discrepancy between the measured value of a particle mass (e.g., from a kinematic resonance peak) and the mass parameter required to make OS-renormalized calculations match other observables (e.g., cross-sections at different energies) would falsify the underlying theory, not the definitional scheme."
      status: proposed
      links: [MATH-027]
naming_notes:
  collisions: [OS can also stand for Operating System; context is sufficient for disambiguation.]
  disambiguation: |
    The On-Shell (OS) scheme should be distinguished from mass-independent schemes like Minimal Subtraction (MS) or Modified Minimal Subtraction (\(\overline{\text{MS}}\)). MS-bar absorbs only the divergent parts of loop corrections into counterterms, leaving the renormalized parameters dependent on an arbitrary energy scale \(\mu\). The OS scheme absorbs both divergent and specific finite parts to fix parameters at a physical, scale-independent value (the mass pole).
crosslinks:
  near_synonyms: []
  antonyms: [MINIMAL_SUBTRACTION_SCHEME]
  prerequisites: [COUNTERTERM, SELF_ENERGY, RENORMALIZATION_GROUP]
  downstream_effects: [PHYSICAL_MASS, RENORMALIZED_COUPLING]
license: CC-BY-SA-4.0
---

# On-Shell Scheme

## Canonical (Pirouette)
A set of renormalization conditions that remove divergences from loop calculations by defining the theory's parameters in terms of physically observable quantities. For the Ki field, the physical mass \(m_{Ki}\) is defined as the location of the pole in its full propagator. This is implemented by introducing counterterms (e.g., \(\delta Z_{Ki}\), \(\delta m_{Ki}^2\)) whose values are fixed by requiring the real part of the Ki self-energy \(\Sigma_{Ki}(p^2)\) and its derivative with respect to \(p^2\) to vanish at \(p^2=m_{Ki}^2\). Similarly, the physical electric charge is defined via the photon self-energy at zero momentum transfer (\(\Pi_{\mu\nu}(0)=0\)).

## EFT-First Summary
The On-Shell (OS) scheme is a standard method in Quantum Field Theory (QFT) for renormalization. It defines the mass and coupling parameters appearing in the Lagrangian to be the actual, experimentally measured values. For example, an electron's mass parameter is set to its measured value of 0.511 MeV. This is achieved by defining the mass as the exact location of the pole in the particle's propagator after all quantum loop corrections are included. The procedure is physically intuitive but can be computationally complex, especially in theories like QCD where fundamental particles are not observed freely (see Peskin & Schroeder, Ch. 10).

## Glossary Links
- See also: [Renormalization Group](<#>), [Self-Energy](<#>), [Minimal Subtraction Scheme](<#>)