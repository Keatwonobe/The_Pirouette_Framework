---
term: "Ki Expectation Value"
canonical_id: "KI_EXPECTATION_VALUE"
symbol: "\(\langle Ki\rangle\)"
aliases: [Order Parameter]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["XAP-006_yang–mills_from_Σ-pushforward_internal_symmetry_of_ki"]
---

---
term: Ki Expectation Value
canonical_id: KI_EXPECTATION_VALUE
symbol: \(\langle Ki\rangle\)
aliases: [Order Parameter]
parents: [XAP-006, CORE-021]
children: [XAP-006B, XAP-006C]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: XAP-006
      lines: "L93-L96"
      snippet: |
        Critical points where $\det h_{ab}=0$ define spontaneous symmetry breaking surfaces:
        \[
        \mathrm{SU}(2)\times \mathrm{U}(1)\xrightarrow{\;\langle Ki\rangle\neq0\;}\mathrm{U}(1)_{EM}.
        \]
        This reproduces electroweak unification without introducing an explicit scalar field:
        the modulus of Ki serves as the order parameter...
  editors: [GPT-4 (Pirouette Dictionary Agent)]
  review_log: []
triad:
  art: |
    In the silent, fertile void, a compass needle freezes, choosing a direction. That singular alignment becomes the grain of reality, giving weight and form to the forces that flow from it. The universe's fundamental asymmetries are born from this first, quiet choice.
  law: |
    A non-zero vacuum expectation value \(\langle Ki\rangle \neq 0\) spontaneously breaks the internal symmetry group \(G\) of the fiber \(\mathcal{F}\) to a residual subgroup \(H\), defined by the stabilizers of \(\langle Ki\rangle\). The squared modulus \(|\langle Ki\rangle|^2\) is proportional to the energy scale of the breaking, setting the masses of the associated gauge bosons. Its direction in \(\mathcal{F}\) determines which symmetries remain unbroken.
  philosophy: |
    This term embodies the principle that physical laws are not imposed but emergent. The specific structure of observed forces is a consequence of the Ki field settling into a stable, energetically-favorable ground state. The vacuum is not empty but is a structured medium whose orientation dictates phenomenology.
pirouette_definition: |
  The Ki Expectation Value, \(\langle Ki\rangle\), is the non-zero, stable ground-state value of the Ki field in its internal fiber space \(\mathcal{F}\). This spontaneous orientation breaks the internal isometry group \(G\) of the fiber (e.g., SU(2)×U(1)) down to a smaller, unbroken subgroup (e.g., U(1)<sub>EM</sub>). After Σ-pushforward, this process manifests as spontaneous symmetry breaking in observer spacetime, with the modulus \(|\langle Ki\rangle|\) setting the mass scale for the gauge bosons corresponding to the broken generators.
operational_definition:
  units: Energy (typically GeV)
  symbol_table:
    - name: \(\langle Ki\rangle\)
      meaning: Ki Expectation Value; a constant vector in the fiber \(\mathcal{F}\).
      dimensions: M L² T⁻²
      default_range: ~246 GeV (when mapped to the electroweak scale)
    - name: \(v\)
      meaning: Higgs vacuum expectation value (Standard Model correspondence).
      dimensions: M L² T⁻²
      default_range: 246.22 GeV
    - name: \(\mathcal{F}\)
      meaning: Internal fiber space over which Ki is valued.
      dimensions: dimensionless
      default_range: \(\mathbb{C}^2\) for electroweak theory
  measurement:
    procedures:
      - name: Electroweak Scale Inference
        outline: |
          1. Measure the masses of the W and Z bosons (\(m_W, m_Z\)) and the weak coupling constant \(g_W\) via particle scattering experiments.
          2. Use the Standard Model relations, e.g., \(m_W = g_W v / 2\), to calculate the Higgs VEV, \(v\).
          3. Invoke the operational mapping between the Higgs VEV and the modulus of the Ki Expectation Value, \(|\langle Ki\rangle| \leftrightarrow v\).
        expected_signals: [W-boson mass ≈ 80.4 GeV, Z-boson mass ≈ 91.2 GeV]
        pitfalls: [Requires precise accounting of radiative corrections; assumes the Pirouette-to-SM mapping is exact at the measured energy scale.]
context_windows:
  - module: XAP-006
    excerpt: |
      **SU(2)** (\(N=2\)): The doublet fiber yields electroweak structure. The coupling \(g_W\) appears as the curvature magnitude at the critical radius \(r_W=\Gamma^{-1/2}\) in the Ki manifold. Spontaneous orientation of Ki’s expectation value defines the Higgs direction in internal space.
  - module: XAP-006
    excerpt: |
      Renormalization flow from MATH-026 implies a scale-dependent deformation of the fiber metric \(h_{ab}(\Lambda)\). Critical points where \(\det h_{ab}=0\) define spontaneous symmetry breaking surfaces: \(\mathrm{SU}(2)\times \mathrm{U}(1)\xrightarrow{\;\langle Ki\rangle\neq0\;}\mathrm{U}(1)_{EM}\). This reproduces electroweak unification without introducing an explicit scalar field: the modulus of Ki serves as the order parameter, and Γ-pressure gives the Higgs mass scale.
poetic_connections:
  motifs: [broken symmetry, vacuum structure, emergent mass, frozen compass, phase transition]
  evocative_lines:
    - "Spontaneous orientation of Ki’s expectation value defines the Higgs direction in internal space."
    - "the modulus of Ki serves as the order parameter"
  association_matrix:
    - [ "INTERNAL_SYMMETRY_OF_KI", 0.9 ]
    - [ "Σ-PUSHFORWARD", 0.7 ]
    - [ "Γ-PRESSURE", 0.6 ]
    - [ "GAUGE_BOSON_MASS", 0.9 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Higgs Vacuum Expectation Value (VEV), \(v\)
      domain: SM
      mapping_kind: operational
      equation_hint: |
        \(|\langle Ki\rangle|^2 \leftrightarrow v^2\) where the Higgs potential is \(V(H) = \lambda(|H|^2-v^2)^2\)
      justification: |
        The functional role of \(\langle Ki\rangle\) in Pirouette—breaking SU(2)×U(1) to U(1)<sub>EM</sub> and setting the mass scale for the W/Z bosons via its non-zero modulus—is a direct geometric analogue to the role of the Higgs VEV in the Standard Model. The source module XAP-006 explicitly identifies \(\langle Ki\rangle\) with the "Higgs vacuum" and "order parameter" of electroweak symmetry breaking.
      references:
        - title: An Introduction to Quantum Field Theory
          where: Chapter 20, Peskin & Schroeder
          date: 1995-10-01
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "The non-zero value of \(\langle Ki\rangle\) is the sole origin of electroweak symmetry breaking and the masses of the W and Z bosons."
      domain: theory|phenomenology
      falsifier: "Experimental discovery of an alternative EWSB mechanism (e.g., technicolor) or finding that W/Z boson masses have contributions from sources other than a single order parameter."
      status: proposed
      links: [XAP-006, XAP-006C]
naming_notes:
  collisions: [The bracket notation \(\langle \cdot \rangle\) is standard for expectation values in quantum mechanics. Care is required to distinguish.]
  disambiguation: |
    The Ki Expectation Value \(\langle Ki\rangle\) is the value of the *classical* Ki field in the theory's vacuum (ground state). It is a constant background value, not a quantum mechanical expectation value which represents an average over measurement outcomes on a quantum state.
crosslinks:
  near_synonyms: [ORDER_PARAMETER]
  antonyms: []
  prerequisites: [KI_FIELD, INTERNAL_SYMMETRY_OF_KI, Σ-PUSHFORWARD]
  downstream_effects: [GAUGE_BOSON_MASS, FERMION_MASS]
license: CC-BY-SA-4.0