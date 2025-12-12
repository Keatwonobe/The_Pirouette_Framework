---
term: "Effective Potential"
canonical_id: "EFFECTIVE_POTENTIAL"
symbol: "V_eff(r)"
aliases: [Linear-plus-Coulomb Potential]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-006"]
---

---
term: Effective Potential
canonical_id: EFFECTIVE_POTENTIAL
symbol: V_eff(r)
aliases: [Linear-plus-Coulomb Potential]
parents: [MATH-006]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-006
      lines: "L62-L71"
      snippet: |
        A first-order expansion of this feedback mechanism under the conditions of quantum chromodynamics (where the feedback is strong) yields the characteristic potential for a confined system:

        V_eff(r) = a/r + b*r

        Here:

        a/r is the familiar inverse-distance potential, analogous to a Coulomb or gravitational field.
        b*r is the linear confinement term. It is the direct mathematical consequence of the feedback loop F becoming dominant at larger distances r.
  editors: [system-agent]
  review_log: []
triad:
  art: |
    A potential that acts like a slack leash. At close range, it permits near-perfect freedom, but with increasing distance, the leash draws taut, its pull becoming relentless and unbreakable.
  law: |
    The interaction potential between confined particles is given by V_eff(r) = a/r + b*r. This dictates that the force between them weakens at short distances (r→0) but approaches a constant non-zero value at large distances (r→∞), making separation impossible.
  philosophy: |
    The functional form of this potential is not arbitrary but a necessary consequence of a system's self-interaction. The mathematics of the Effective Potential are the physics of belonging, where a system's own resonance defines the inescapable bounds of its integrity.
pirouette_definition: |
  The effective potential V_eff(r) is the emergent, distance-dependent potential energy governing the dynamics of a system subject to Gladiator-class forces. It is derived from the more fundamental potential V(Γ) by modeling a scale-dependent feedback loop where a system's resonant intensity (K_τ) modifies its local Temporal Pressure (Γ). Its canonical form, V_eff(r) = a/r + b*r, contains both an inverse-distance term (a/r) dominant at short range and a linear confinement term (b*r) dominant at long range, which is the direct consequence of the feedback. This functional form is sufficient to prove the theorems of Asymptotic Freedom and Confinement.
operational_definition:
  units: Energy (Joules, eV)
  symbol_table:
    - name: V_eff(r)
      meaning: Effective potential energy
      dimensions: M L^2 T^-2
      default_range: contextual (e.g., GeV for quarkonium)
    - name: r
      meaning: Separation distance between particles
      dimensions: L
      default_range: contextual (e.g., 10^-15 m)
    - name: a
      meaning: Coulomb-like strength parameter
      dimensions: M L^3 T^-2 (Energy * Length)
      default_range: dimensionless in natural units (related to coupling constant)
    - name: b
      meaning: Confinement strength parameter (string tension)
      dimensions: M T^-2 (Energy / Length)
      default_range: ~0.18 GeV^2 or ~80,000 N
  measurement:
    procedures:
      - name: Heavy Quarkonium Spectroscopy
        outline: |
          1. Experimentally measure the mass spectrum (energy levels) of heavy quark-antiquark bound states, such as charmonium (J/ψ, ψ') or bottomonium (Υ, Υ').
          2. Model the system non-relativistically using the Schrödinger equation with V_eff(r) as the central potential.
          3. Numerically solve the eigenvalue problem to find the predicted energy levels as a function of parameters `a` and `b`.
          4. Perform a statistical fit of `a` and `b` to match the predicted energy levels to the experimentally measured mass spectrum.
        expected_signals: [A series of discrete energy levels (particle masses) for the bound states, Spacing between levels that cannot be explained by a pure Coulomb-like potential]
        pitfalls: [Relativistic corrections are required for high precision, Spin-dependent forces split the energy levels, The potential is a model and breaks down at very short/long distances]
context_windows:
  - module: MATH-006
    excerpt: |
      For many physical systems, we can approximate the potential V(Gamma(r)) with a Taylor expansion around a baseline pressure. A first-order expansion of this feedback mechanism under the conditions of quantum chromodynamics (where the feedback is strong) yields the characteristic potential for a confined system: V_eff(r) = a/r + b*r.
  - module: MATH-006
    excerpt: |
      With the effective potential V_eff(r) established, the defining behaviors of the Gladiator Force are now simple theorems. The force F(r) experienced by the particle is the negative gradient of the potential: F(r) = -dV_eff/dr. As the distance r grows large, the force does not diminish with distance. It approaches a constant, non-zero value -b. To separate the particles by an infinite distance would require an infinite amount of work.
poetic_connections:
  motifs: [leash, arena, confinement, integrity, belonging]
  evocative_lines:
    - "confinement is not a wall, but a leash."
    - "The mathematics of the Gladiator are the physics of belonging."
    - "its own act of separation pulls the leash taut"
  association_matrix:
    - [ "GLADIATOR_FORCE", 0.9 ]
    - [ "CONFINEMENT", 0.9 ]
    - [ "TEMPORAL_PRESSURE", 0.7 ]
    - [ "ASYMPTOTIC_FREEDOM", 0.7 ]
formal_mappings:
  candidates:
    - target: Cornell Potential
      domain: SM
      mapping_kind: mathematical
      equation_hint: |
        V_eff(r) = a/r + b*r  ↔  V_QCD(r) = - (4/3) * (α_s(r)/r) + σ*r
      justification: |
        The Cornell potential is a highly successful phenomenological model in Quantum Chromodynamics (QCD) for the potential between a heavy quark and antiquark. Its functional form is identical to V_eff. The Pirouette framework presents V_eff not as a phenomenological fit but as a direct consequence of the scale-feedback mechanism. The parameter `a` maps to the color-factor-modified strong coupling constant, and `b` maps to the QCD string tension `σ`.
      references:
        - title: "Heavy-quark potential in QCD"
          where: "Phys. Rev. D 12, 110"
          date: 1975-07-01
      confidence: 0.95
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The potential energy between any two particles bound by the Gladiator force grows linearly with separation distance `r` for large `r`."
      domain: experiment
      falsifier: "Experimental observation of a confined system (e.g., from lattice QCD calculations or quarkonium spectra) where the potential at large distance is best fit by a function that does not grow linearly, such as a constant or a power law weaker than `r^1` (e.g., `sqrt(r)`)."
      status: supported
      links: [MATH-006]
    - statement: "No finite-energy path exists for a particle to escape the V_eff(r) potential well to r = ∞."
      domain: theory
      falsifier: "A rigorous mathematical solution that demonstrates a bound state within V_eff can be brought to infinite separation with finite energy input. This would invalidate the Confinement theorem."
      status: proposed
      links: [MATH-006]
naming_notes:
  collisions: [The symbol `V` is universally used for potential energy. Subscript `eff` is crucial.]
  disambiguation: |
    V_eff(r) is the *emergent potential* as a function of separation distance `r`. It should not be confused with the more fundamental potential `V(Γ)`, which is a function of the local Temporal Pressure field. V_eff(r) is the result of solving for the system's dynamics under the influence of the feedback law Γ(r).
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [TEMPORAL_PRESSURE]
  downstream_effects: [GLADIATOR_FORCE, CONFINEMENT, ASYMPTOTIC_FREEDOM, TEMPORAL_FORGE]
license: CC-BY-SA-4.0
---

# Effective Potential

## Canonical (Pirouette)
The effective potential V_eff(r) is the emergent, distance-dependent potential energy governing the dynamics of a system subject to Gladiator-class forces. It is derived from the more fundamental potential V(Γ) by modeling a scale-dependent feedback loop where a system's resonant intensity (K_τ) modifies its local Temporal Pressure (Γ). Its canonical form, V_eff(r) = a/r + b*r, contains both an inverse-distance term (a/r) dominant at short range and a linear confinement term (b*r) dominant at long range, which is the direct consequence of the feedback. This functional form is sufficient to prove the theorems of Asymptotic Freedom and Confinement.

## EFT-First Summary
The Effective Potential is the Pirouette Framework's analogue to the **Cornell Potential** used in Standard Model Quantum Chromodynamics (QCD) to describe the force between quarks. The `a/r` term corresponds to the single-gluon exchange part of the potential, while the linear `b*r` term corresponds to the constant "string tension" `σ` that confines quarks within hadrons. Measurements of the energy levels of heavy quark-antiquark systems (quarkonium) provide strong experimental support for this potential's form and are used to determine the empirical values of `a` and `b`.

## Glossary Links
- See also: [GLADIATOR_FORCE](./GLADIATOR_FORCE.md), [CONFINEMENT](./CONFINEMENT.md), [TEMPORAL_PRESSURE](./TEMPORAL_PRESSURE.md)