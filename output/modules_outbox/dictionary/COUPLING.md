---
term: "Γ-coupling"
canonical_id: "COUPLING"
symbol: '\(\lambda_\Gamma, y_\Gamma\)'

aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-027"]
---

---
term: Γ-coupling
canonical_id: GAMMA_COUPLING
symbol: \(\lambda_\Gamma, y_\Gamma\)
aliases: []
parents: [MATH-027, XAP-006C]
children: []
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-027
      lines: "§3"
      snippet: |
        \(\mathcal L_{\text{int}}
        = ... - \lambda_\Gamma\big(|Ki|^2 - \xi\,\Gamma^2\big)^2
        + \bar\Psi(i\gamma^\mu D_\mu - y_\Gamma \Gamma)\Psi .\)
  editors: [Agent-Scribe]
  review_log: []
triad:
  art: |
    The whisper of the substrate made manifest as mass and repulsion. It is the friction of spacetime, the resistance matter feels from the underlying temporal medium when it attempts to change its state.
  law: |
    The Γ-coupling constants \(\lambda_\Gamma\) and \(y_\Gamma\) are dimensionless parameters that set the magnitude of the \(|Ki|^2\Gamma^2\) and \(\bar\Psi\Psi\Gamma\) interaction vertices, respectively. They are directly proportional to the cross-sections of scattering processes involving Γ-bosons (pressurons).
  philosophy: |
    Γ-coupling realizes the principle that matter is not independent of the temporal substrate. It provides the mechanism by which substrate dynamics, such as changes in temporal pressure (Γ), directly alter the properties of matter, making the substrate an active participant in physics rather than a passive backdrop.
pirouette_definition: |
  The Γ-coupling comprises a set of dimensionless constants, primarily \(\lambda_\Gamma\) and \(y_\Gamma\), that define the strength of interaction between the Γ-field (temporal pressure) and matter fields.

  - **\(\lambda_\Gamma\)** governs the quartic interaction between the complex scalar Ki-field and the Γ-field, via the term \(-\lambda_\Gamma(|Ki|^2 - \xi\,\Gamma^2)^2\). This contributes to the Ki-field's potential and induces \(Ki-Ki^\dagger-\Gamma\) and \(Ki-Ki^\dagger-\Gamma-\Gamma\) vertices.
  - **\(y_\Gamma\)** is a Yukawa-type coupling governing the interaction between a fermion field \(\Psi\) and the Γ-field, via the term \(-y_\Gamma \bar\Psi \Gamma \Psi\). This interaction directly contributes to the fermion's effective mass.
operational_definition:
  units: Dimensionless
  symbol_table:
    - name: \(\lambda_\Gamma\)
      meaning: Ki-Γ quartic coupling constant
      dimensions: dimensionless
      default_range: contextual
    - name: \(y_\Gamma\)
      meaning: Fermion-Γ Yukawa coupling constant
      dimensions: dimensionless
      default_range: contextual
    - name: \(\Gamma\)
      meaning: The Γ-field (temporal pressure)
      dimensions: \(M\)
      default_range: contextual
    - name: \(Ki\)
      meaning: The complex scalar Ki-field
      dimensions: \(M\)
      default_range: contextual
    - name: \(\Psi\)
      meaning: The fermion field
      dimensions: \(M^{3/2}\)
      default_range: contextual
  measurement:
    procedures:
      - name: Cross-Section Analysis
        outline: |
          Measure the scattering cross-sections or decay widths for processes involving Γ-bosons. The process \(Ki + Ki^\dagger \to \Gamma + \Gamma\) has a cross-section proportional to \(\lambda_\Gamma^2\), while the decay width of a heavy fermion into a lighter one plus a Γ-boson (\(\Psi_H \to \Psi_L + \Gamma\)) is proportional to \(y_\Gamma^2\). Infer coupling constants by fitting theoretical predictions to experimental data.
        expected_signals: [Resonances in scattering channels corresponding to Γ-boson production, Specific angular distributions in decay products determined by vertex structure]
        pitfalls: [Γ-bosons may be difficult to detect directly if they only couple to Pirouette-specific fields, Loop corrections can obscure the tree-level relationship between cross-sections and couplings]
context_windows:
  - module: MATH-027
    excerpt: |
      We collect the minimal interaction terms used in Pirouette EFT: ... \( - \lambda_\Gamma\big(|Ki|^2 - \xi\,\Gamma^2\big)^2 + \bar\Psi(i\gamma^\mu D_\mu - y_\Gamma \Gamma)\Psi \). The vertex factor for \(\bar\Psi \Psi \Gamma\) is \(-i y_\Gamma\), which represents the primary interaction in the torsion mass channel. The coupling \(\lambda_\Gamma\) creates more complex vertices, including a \(Ki\,Ki^\dagger\,\Gamma\) vertex proportional to \(-4 i \lambda_\Gamma \xi \Gamma_0\).
  - module: XAP-006C
    excerpt: |
      The Γ–sector contributes an effective mass to other fields. For fermions, this is realized via the Yukawa term \(-y_\Gamma \bar\Psi\Gamma\Psi\). If the Γ-field acquires a non-zero vacuum expectation value \(\Gamma_0\), this term behaves precisely as a mass term \(m_\Psi^{\text{eff}} = y_\Gamma \Gamma_0\). For scalars like Ki, the coupling \(\lambda_\Gamma\) links the Ki potential to \(\Gamma_0\), affecting its mass and vacuum stability.
poetic_connections:
  motifs: [substrate friction, medium resistance, mass generation, potential shaping]
  evocative_lines:
    - "Torsion mass channel."
    - "The Γ–sector contributes an effective mass."
  association_matrix:
    - [ "MASS", 0.9 ]
    - [ "TEMPORAL_PRESSURE", 0.8 ]
    - [ "FEYNMAN_VERTEX", 0.7 ]
formal_mappings:
  candidates:
    - target: Quartic coupling \(\lambda\)
      domain: QFT
      mapping_kind: mathematical
      equation_hint: |
        \(V(\phi_1, \phi_2) \supset \lambda(\phi_1^2 - c \phi_2^2)^2\)
      justification: |
        The term \(-\lambda_\Gamma(|Ki|^2 - \xi\,\Gamma^2)^2\) is a mixed quartic coupling between two scalar fields, Ki and Γ. This form is common in models with multiple scalar sectors, such as two-Higgs-doublet models or scalar dark matter models, where it governs the interaction and potential mixing between the fields.
      references: []
      confidence: 0.8
  adopted:
    - target: Yukawa coupling (\(y\))
      rationale: |
        The term \(-y_\Gamma \bar\Psi \Gamma \Psi\) is a direct mathematical analog of the Standard Model Yukawa interaction, which is responsible for fermion mass generation via coupling to the Higgs scalar field. This mapping is operationally precise and conceptually central, as the Γ-field's VEV directly imparts mass to fermions.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: 'The Yukawa coupling \(y_\Gamma\) is universal for all fundamental fermions.'

      domain: phenomenology
      falsifier: 'Observation of fermion masses that cannot be explained by a single VEV \(\Gamma_0\) and a universal \(y_\Gamma\), implying flavor-dependent couplings \(y_{\Gamma,f}\).'

      status: proposed
      links: [XAP-006C]
    - statement: 'The couplings \(\lambda_\Gamma\) and \(y_\Gamma\) are fundamental constants that do not run with energy scale.'

      domain: theory
      falsifier: 'Calculating one-loop corrections to Γ-scattering processes reveals non-zero beta functions for \(\lambda_\Gamma\) and \(y_\Gamma\), requiring renormalization and implying they are scale-dependent.'

      status: proposed
      links: [MATH-027]
naming_notes:
  collisions: [The symbol \(\lambda\) is a standard notation for any quartic coupling (\(\lambda_{Ki}\) is also used). The symbol \(y\) is standard for Yukawa couplings. The subscript Γ is crucial for disambiguation.]
  disambiguation: |
    Distinguish the Γ-coupling \(\lambda_\Gamma\) from the Ki-field's self-interaction coupling \(\lambda_{Ki}\). Similarly, distinguish the fermion-Γ coupling \(y_\Gamma\) from any other Yukawa couplings in the full theory. The subscript Γ always indicates an interaction with the Γ-field.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [TEMPORAL_PRESSURE, KI_FIELD, FEYNMAN_VERTEX]
  downstream_effects: [MASS]
license: CC-BY-SA-4.0
---

# Γ-coupling

## Canonical (Pirouette)
The Γ-coupling comprises a set of dimensionless constants, primarily \(\lambda_\Gamma\) and \(y_\Gamma\), that define the strength of interaction between the Γ-field (temporal pressure) and matter fields.

- **\(\lambda_\Gamma\)** governs the quartic interaction between the complex scalar Ki-field and the Γ-field, via the term \(-\lambda_\Gamma(|Ki|^2 - \xi\,\Gamma^2)^2\). This contributes to the Ki-field's potential and induces \(Ki-Ki^\dagger-\Gamma\) and \(Ki-Ki^\dagger-\Gamma-\Gamma\) vertices.
- **\(y_\Gamma\)** is a Yukawa-type coupling governing the interaction between a fermion field \(\Psi\) and the Γ-field, via the term \(-y_\Gamma \bar\Psi \Gamma \Psi\). This interaction directly contributes to the fermion's effective mass.

## EFT-First Summary
In the language of effective field theory, Γ-couplings are analogous to standard particle physics interactions. The \(y_\Gamma\) coupling is a direct analog of a Yukawa coupling, where the Γ-field (temporal pressure) plays the role of the Higgs boson in giving mass to fermions. The \(\lambda_\Gamma\) coupling is a mixed-quartic scalar coupling, linking the potential energy and vacuum structure of the Ki-field to the state of the Γ-field.

## Glossary Links
- See also: Temporal Pressure (Γ), Ki-Field, Mass