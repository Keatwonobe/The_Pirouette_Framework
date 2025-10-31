---
term: "Ki Propagator"
canonical_id: "KI_PROPAGATOR"
symbol: '\(\Delta_{Ki}(p)\)'

aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-027"]
---

---
term: Ki Propagator
canonical_id: KI_PROPAGATOR
symbol: \(\Delta_{Ki}(p)\)
aliases: []
parents: [MATH-027]
children: []
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-027
      lines: "§2.1"
      snippet: |
        The observer-frame Feynman propagator is
        \begin{equation}
        \boxed{\; \Delta_{Ki}(p)=\frac{i}{p^2 - m_{Ki}^2 + i\varepsilon}\;}
        \end{equation}
  editors: [Agent (GPT-4 based)]
  review_log: []
triad:
  art: |
    The echo of a particle's passage through the void, a mathematical ghost that carries potential from where a thing was to where it will be. It is the hum of spacetime responding to the possibility of existence.
  law: |
    The Ki Propagator \(\Delta_{Ki}(p)\) gives the quantum amplitude for a free Ki particle with 4-momentum \(p\) to travel between two spacetime points. It is the momentum-space inverse of the quadratic wave operator, \((p^2 - m_{Ki}^2)\), derived from the free Lagrangian.
  philosophy: |
    The propagator is the fundamental unit of being in quantum field theory. It represents a particle's undisturbed state, its inert trajectory, forming the lines in Feynman diagrams from which all interactions—all of dynamics—are constructed. It separates existence from action.
pirouette_definition: |
  The Ki Propagator is the Feynman propagator for the free Ki field, a complex scalar field over the time substrate. In the emergent observer frame with spacetime coordinates \(x=(t,\mathbf{x})\) and 4-momentum \(p=(p_0, \mathbf{p})\), it takes the standard relativistic form:
  \[ \Delta_{Ki}(p)=\frac{i}{p^2 - m_{Ki}^2 + i\varepsilon} \]
  where \(p^2 = p_0^2 - \mathbf{p}^2\) and \(m_{Ki}\) is the observed Ki mass. This form arises from the underlying substrate Lagrangian \(\mathcal L^{(\tau)}_{Ki}\) after rescaling time and space coordinates via the anisotropic stiffness parameters \(K_{Ki}\) and \(\Lambda_{Ki}\). The \(i\varepsilon\) term enforces causal, time-ordered propagation.
operational_definition:
  units: \(M^{-2}\) in natural units (\(\hbar=c=1\)).
  symbol_table:
    - name: \(\Delta_{Ki}(p)\)
      meaning: Feynman propagator for the Ki particle.
      dimensions: \(M^{-2}\)
      default_range: contextual
    - name: \(p\)
      meaning: Observer-frame 4-momentum \( (p_0, \mathbf{p}) \).
      dimensions: \(M\)
      default_range: contextual
    - name: \(m_{Ki}\)
      meaning: On-shell mass of the Ki particle in the observer frame.
      dimensions: \(M\)
      default_range: \(\geq 0\)
    - name: \(\varepsilon\)
      meaning: Infinitesimal positive constant defining the Feynman contour prescription.
      dimensions: \(M^2\)
      default_range: \(0^+\)
  measurement:
    procedures:
      - name: Resonance Scan via Scattering
        outline: |
          The propagator is not directly measured but is inferred from scattering experiments. For example, in a process like \(A+B \to C+D\) mediated by a virtual Ki particle, the cross-section is proportional to \(|\Delta_{Ki}(p)|^2\), where \(p\) is the momentum transfer. By measuring the cross-section as a function of center-of-mass energy or momentum transfer, the parameters of \(\Delta_{Ki}(p)\), chiefly \(m_{Ki}\), can be extracted.
        expected_signals: [A peak (resonance) in the scattering cross-section when the invariant mass of the exchanged particle is near \(m_{Ki}\), A differential cross-section whose angular dependence is governed by the \(1/(p^2-m_{Ki}^2)\) form.]
        pitfalls: [The measured resonance is a Breit-Wigner peak, not a sharp delta function, due to the particle's decay width., Loop corrections from interactions modify the simple "bare" propagator into a "dressed" one, shifting the pole and introducing a complex part.]
context_windows:
  - module: MATH-027
    excerpt: |
      The observer-frame Feynman propagator is
      \begin{equation}
      \boxed{\; \Delta_{Ki}(p)=\frac{i}{p^2 - m_{Ki}^2 + i\varepsilon}\;}
      \end{equation}
      with \(p^2=p_0^2-\mathbf p^2\).
      In substrate variables (no rescaling),
      \(
      \Delta^{(\tau)}_{Ki}(\omega,\mathbf k)
      = i\big/(K_{Ki}\omega^2 - \Lambda_{Ki}\mathbf k^2 - m_{Ki,\tau}^2 + i\varepsilon).
      \)
  - module: MATH-027
    excerpt: |
      Using the light-cone result \(c^2=\Lambda_\Gamma/K_\Gamma\), define rescaled time \(t = \sqrt{K_{Ki}}\,\tau\) and spatial metric \(\mathbf x = \sqrt{\Lambda_{Ki}}\,\mathbf u\). Then the minimal quadratic substrate Lagrangian becomes the Lorentz-covariant quadratic form
      \begin{equation}
      \mathcal L_{Ki,\text{quad}}^{(obs)}
      = |\partial_t Ki|^2 - |\nabla Ki|^2 - m_{Ki}^2 |Ki|^2,
      \qquad
      m_{Ki}^2 \equiv \frac{m_{Ki,\tau}^2}{K_{Ki}}.
      \end{equation}
poetic_connections:
  motifs: [propagation, ripple, potential, free-particle, quantum-path]
  evocative_lines:
    - "The observer-frame Feynman propagator..."
    - "In substrate variables (no rescaling)..."
  association_matrix:
    - [ "KI_MASS", 0.9 ]
    - [ "SUBSTRATE_STIFFNESS", 0.7 ]
    - [ "FEYNMAN_DIAGRAM", 0.9 ]
formal_mappings:
  candidates:
    - target: Feynman propagator (complex scalar)
      domain: QFT
      mapping_kind: mathematical
      equation_hint: |
        \(\Delta_F(x-y) = \langle 0 | T \{ \phi(x) \phi^\dagger(y) \} | 0 \rangle \quad \xrightarrow{\text{FT}} \quad \tilde{\Delta}_F(p) = \frac{i}{p^2 - m^2 + i\varepsilon}\)
      justification: |
        The mathematical form of \(\Delta_{Ki}(p)\) is identical to the canonical Feynman propagator for a free complex scalar field (e.g., Klein-Gordon field) in quantum field theory. It is the Green's function for the Klein-Gordon operator \((\Box + m^2)\) with time-ordering boundary conditions specified by the \(+i\varepsilon\) term.
      references:
        - title: An Introduction to Quantum Field Theory
          where: "Peskin & Schroeder, Ch. 2"
          date: 1995-10-11
      confidence: 1.0
  adopted:
    - target: Feynman propagator (complex scalar)
      rationale: Adopted as the mapping is mathematically exact. Pirouette's theoretical contribution is not to the form of the propagator itself, but to the physical origin of its parameters (\(m_{Ki}\) and the emergent Lorentz invariance) from the underlying τ-substrate and its anisotropic stiffnesses.
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: 'The real part of the pole of the full, dressed Ki propagator corresponds to the physical mass \(m_{Ki}\), which is determined by substrate parameters \(K_{Ki}\) and the Γ-sector VEV as \(m_{Ki}^2 = (m_0^2 + \xi_\Gamma\,\Gamma_0^2) / K_{Ki}\).'

      domain: phenomenology
      falsifier: "An experimental measurement of the Ki resonance mass that is inconsistent with the mass predicted by measurements of substrate stiffness and the Γ-field background. This would falsify the mass generation mechanism described in XAP-006C."
      status: proposed
      links: [XAP-006C, MATH-027]
naming_notes:
  collisions: [The symbol \(\Delta\) is heavily overloaded in physics, often representing a difference, a Laplacian operator, or other propagators (e.g., for the Γ field, \(\Delta_\Gamma\)). The subscript 'Ki' is essential for disambiguation.]
  disambiguation: |
    Always distinguish between the Lorentz-covariant observer-frame propagator \(\Delta_{Ki}(p)\) and the anisotropic substrate-frame propagator \(\Delta^{(\tau)}_{Ki}(\omega,\mathbf k)\). The former is used for standard phenomenological calculations, while the latter is used for foundational derivations from the substrate.
crosslinks:
  near_synonyms: [GREENS_FUNCTION, TWO_POINT_CORRELATOR]
  antonyms: [VERTEX_FACTOR]
  prerequisites: [KI_FIELD, KI_MASS, SUBSTRATE_ACTION_OF_TIME]
  downstream_effects: [FEYNMAN_DIAGRAM, SCATTERING_AMPLITUDE, SELF_ENERGY]
license: CC-BY-SA-4.0
---