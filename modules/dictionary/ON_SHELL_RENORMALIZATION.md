---
term: "On-shell Renormalization"
canonical_id: "ON_SHELL_RENORMALIZATION"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-015"]
---

---
term: On-shell Renormalization
canonical_id: ON_SHELL_RENORMALIZATION
symbol: OS
aliases: [On-shell scheme]
parents: [MATH-015]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-015
      lines: "§0"
      snippet: |
        Counterterms obey
        \[
        \Sigma(\slashed p=m)=0,\qquad \left.\frac{\partial\Sigma}{\partial \slashed p}\right|_{\slashed p=m}=0 .
        \]
  editors: [GPT-4 (Pirouette Dictionary Agent)]
  review_log: []
triad:
  art: |
    A theory is tuned to the universe's pitch. The properties of a real, isolated particle serve as the tuning fork, ensuring all calculated harmonies correspond to physical reality.
  law: |
    The renormalization counterterms of a theory are fixed by demanding that the pole of the renormalized two-point Green's function for a particle occurs at its physically measured mass (m) with a residue of exactly one.
  philosophy: |
    This scheme anchors the abstract parameters of a quantum field theory to concrete, measurable observables. It enforces from first principles that the theory's description of a single, stable particle matches its observed physical properties, making scattering predictions manifestly physical.
pirouette_definition: |
  A renormalization procedure where counterterms for mass ($\delta_m$) and field strength ($\delta_Z$) are determined by imposing conditions on the 1PI self-energy function, $\Sigma(p)$. Specifically, the conditions ensure that the renormalized propagator has a simple pole at the physical mass $p^2=m^2$ with residue $i$, corresponding to a stable, observable particle. This is the default scheme for relating fundamental parameters to experimental inputs like the electron mass.
operational_definition:
  units: scheme (dimensionless procedure)
  symbol_table:
    - name: $\Sigma(\slashed p)$
      meaning: Fermion 1PI self-energy function
      dimensions: M L T⁻¹
      default_range: contextual
    - name: $m$
      meaning: Physical, measured mass of the particle
      dimensions: M
      default_range: contextual
    - name: $Z_2$
      meaning: Field strength renormalization constant (wavefunction renormalization)
      dimensions: dimensionless
      default_range: "≈ 1"
    - name: $Z_m$
      meaning: Mass renormalization constant
      dimensions: dimensionless
      default_range: "≈ 1"
  measurement:
    procedures:
      - name: Fixing Counterterms
        outline: |
          1. Calculate the unrenormalized 1-particle irreducible (1PI) self-energy, $\Sigma(\slashed p)$, to a given loop order in dimensional regularization.
          2. Define the renormalized self-energy $\Sigma_R(\slashed p)$ by introducing mass and field strength counterterms: $\Sigma_R = \Sigma + \delta_Z(\slashed p - m) - \delta_m$.
          3. Impose the two on-shell conditions on the renormalized self-energy:
             a. $\Sigma_R(\slashed p=m) = 0$
             b. $\left.\frac{\partial \Sigma_R(\slashed p)}{\partial \slashed p}\right|_{\slashed p=m} = 0$
          4. Solve these two equations to determine the finite parts of the counterterms $\delta_Z$ and $\delta_m$ order by order in the coupling constant.
        expected_signals:
          - A fully renormalized propagator for the particle that has a simple pole at $p^2=m^2$ with residue 1.
          - Finite, regulator-independent predictions for physical observables like scattering cross-sections.
        pitfalls:
          - Forgetting to include all diagrams contributing to $\Sigma$ at a given order.
          - Incorrectly evaluating the derivative of $\Sigma$ with respect to $\slashed p$.
          - Applying the on-shell conditions to unstable particles, which requires a more complex pole structure treatment.
context_windows:
  # Short, trimmed context quotes harvested from modules (3–6 sentences each).
  - module: MATH-015
    excerpt: |
      Metric signature $((+,-,-,-))$, $(c=\hbar=1)$. On-shell renormalization; electron mass $(m)$ defines the scale. Normalization: $(a_\ell\equiv (g_\ell-2)/2)$.
  - module: MATH-015
    excerpt: |
      Dimensional regularization: compute divergent and finite parts; apply on-shell renormalization conditions $(\Sigma(\slashed p=m)=0)$, $(\partial\Sigma/\partial\slashed p|_{\slashed p=m}=0)$. The finite sum yields $C_2^{\rm QED}=+0.328478965\ldots$. The sign is fixed by the background Ward identities and the counterterm algebra; spurious sign flips trace to inconsistent metric/$\gamma^5$ or to missing on-shell subtractions.
poetic_connections:
  # Lightweight "word-association graph" and sticky lines.
  motifs: [calibration, physicality, tuning-fork, grounding, reality-check]
  evocative_lines:
    - "On-shell renormalization; electron mass (m) defines the scale."
    - "Counterterms ↔ redefinition of the local chart that keeps the channel’s extrinsic curvature finite."
  association_matrix:
    # symmetric or directed; weights in [0,1]
    - [ "PHYSICAL_MASS", 0.9 ]
    - [ "COUNTERTERM", 0.8 ]
    - [ "SELF_ENERGY", 0.8 ]
    - [ "S_MATRIX", 0.6 ]
formal_mappings:
  # Candidate alignments to EFT/SM/CM/GR terms, each with justification and refs.
  candidates: []
  adopted:
    - target: On-shell renormalization scheme (QFT)
      domain: SM
      mapping_kind: mathematical
      equation_hint: |
        $\hat{\Sigma}(\slashed{p}=m_\text{phys}) = 0 \quad \text{and} \quad \left.\frac{\partial \hat{\Sigma}(\slashed{p})}{\partial \slashed{p}}\right|_{\slashed{p}=m_\text{phys}} = 0$
      rationale: |
        The Pirouette Framework adopts the standard on-shell renormalization scheme from Quantum Field Theory without modification. It is the definitional procedure for relating bare Lagrangian parameters to the observed physical mass and charge of particles like the electron, ensuring S-matrix elements are directly comparable to experiment. MATH-015's calculation of C₂ relies entirely on this standard procedure.
      references:
        - title: An Introduction to Quantum Field Theory
          where: Peskin & Schroeder, Chapter 7
          date: 1995-10-01
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "The on-shell scheme defines the physical mass as the real part of the pole of the full propagator, and fixes counterterms to enforce this definition at each order in perturbation theory."
      domain: theory
      falsifier: "This is a definitional statement. An error would be a misapplication of the scheme, not a falsification of it. It can be contrasted with other schemes (like MS-bar) where the renormalized mass does not directly correspond to the pole mass."
      status: supported
      links: [MATH-015]
naming_notes:
  collisions: [on-shell particle]
  disambiguation: |
    "On-shell" can refer to a particle state satisfying the relativistic energy-momentum relation ($p^2=m^2$). "On-shell Renormalization" is the *procedure* that uses the properties of such physical particle states to fix the free parameters (counterterms) in the theory. It should not be confused with the MS-bar scheme, which subtracts only the universal divergent poles and does not impose conditions related to physical observables.
crosslinks:
  near_synonyms: []
  antonyms: [MINIMAL_SUBTRACTION_SCHEME]
  prerequisites: [COUNTERTERM, SELF_ENERGY, RENORMALIZATION]
  downstream_effects: [PHYSICAL_MASS, S_MATRIX]
license: CC-BY-SA-4.0
---

# On-shell Renormalization

## Canonical (Pirouette)
A renormalization procedure where counterterms for mass ($\delta_m$) and field strength ($\delta_Z$) are determined by imposing conditions on the 1PI self-energy function, $\Sigma(p)$. Specifically, the conditions ensure that the renormalized propagator has a simple pole at the physical mass $p^2=m^2$ with residue $i$, corresponding to a stable, observable particle. This is the default scheme for relating fundamental parameters to experimental inputs like the electron mass.

## EFT-First Summary
The On-shell (OS) scheme is a standard method in Quantum Field Theory for fixing the renormalization conditions. It defines the renormalized mass and coupling constants of a theory in terms of physically measurable quantities. For example, the electron's mass is defined as the pole of the electron propagator, and the fine-structure constant is defined in the Thomson limit ($q^2 \to 0$). This ensures a direct link between the theory's parameters and experimental data. (See, e.g., Peskin & Schroeder, Ch. 7).

## Glossary Links
- See also: [COUNTERTERM](COUNTERTERM), [PHYSICAL_MASS](PHYSICAL_MASS), [MINIMAL_SUBTRACTION_SCHEME](MINIMAL_SUBTRACTION_SCHEME)