---
term: "Gamma Potential"
canonical_id: "GAMMA_POTENTIAL"
symbol: "V(Γ)"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["COSMO-004"]
---

---
term: Gamma Potential
canonical_id: GAMMA_POTENTIAL
symbol: V(Γ)
aliases: []
parents: [COSMO-004]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: COSMO-004
      lines: "A1"
      snippet: |
        Γ′′ + 2ℋ Γ′ + a² V_{,Γ}(Γ) = 0
  editors: ["Agent [U-88]"]
  review_log: []
triad:
  art: |
    The potential is the unseen landscape that sculpts the Γ field, carving its path through cosmic history. It is the field's character, defining its mass, its ambition, and its ultimate quiescence.
  law: |
    The dynamics of the Γ field are determined by the first and second derivatives of its potential: the force `−V_{,Γ}` drives its evolution, while the curvature `V_{,ΓΓ}` defines its effective mass squared.
  philosophy: |
    The Gamma Potential is the axiomatic core of the Γ-sector cosmology. Specifying its form is equivalent to declaring the fundamental theory of this dark sector, with all cosmological consequences flowing deterministically from this choice.
pirouette_definition: |
  A scalar function `V` of the Γ field that defines its self-interaction energy and serves as a source term in its Klein-Gordon equation of motion. In the Pirouette Framework, its form is typically specified as `quadratic_plus_tail`, parameterized by a mass `m_Γ`, a quartic coupling `λ₄`, and a late-time exponential tail defined by scales `μ` and `Γ*`. The parameters for a given simulation are fixed by a Freeze Manifest.
operational_definition:
  units: Energy Density (e.g., eV⁴ or M_Pl⁴)
  symbol_table:
    - name: V(Γ)
      meaning: Gamma Potential
      dimensions: M L⁻¹ T⁻²
      default_range: contextual
    - name: Γ
      meaning: Gamma Field
      dimensions: M¹/² L¹/² T⁻¹
      default_range: contextual
    - name: V_{,Γ}
      meaning: First derivative of potential w.r.t. Γ
      dimensions: M¹/² L⁻³/² T⁻¹
      default_range: contextual
    - name: V_{,ΓΓ}
      meaning: Second derivative of potential w.r.t. Γ (effective mass-squared)
      dimensions: L⁻²
      default_range: contextual
  measurement:
    procedures:
      - name: Cosmological Parameter Inference
        outline: |
          The parameters of V(Γ) are not measured directly but are inferred via statistical comparison of theoretical predictions with cosmological data. A functional form for V(Γ) is implemented in a Boltzmann solver (e.g., CLASS, CAMB) to predict observables such as CMB power spectra and the matter power spectrum. An MCMC analysis is then used to find the posterior probability distribution for the potential's parameters (`m_Γ_eV`, `lambda4`, etc.) given observational datasets (e.g., Planck, BAO, weak lensing).
        expected_signals: [CMB angular power spectra (TT, TE, EE, lensing), Matter Power Spectrum P(k,z), growth rate fσ₈(z)]
        pitfalls: [Parameter degeneracies (e.g., with H₀, nₛ), Model dependency on the chosen potential form, Numerical instability in stiff regimes (m_Γ ≫ H)]
context_windows:
  - module: COSMO-004
    excerpt: |
      Γ′′ + 2ℋ Γ′ + a² V_{,Γ}(Γ) = 0
      ρ_Γ = (Γ′²)/(2 a²) + V(Γ)
      p_Γ = (Γ′²)/(2 a²) − V(Γ)
      Conformal Friedmann: ℋ² = (8πG/3) a² (ρ_r + ρ_b + ρ_Γ)
  - module: COSMO-004
    excerpt: |
      # Gamma sector

      Gamma_species=on
      Gamma_potential=quadratic_plus_tail
      m_Gamma_eV=1.7e7
      lambda4=0.0
      V_tail_type=exp_shallow
      V_tail_mu_eV=1.0e-33
      V_tail_Gamma_star_Mpl=1.0
poetic_connections:
  motifs: ["cosmic landscape", "potential well", "field dynamics", "self-interaction"]
  evocative_lines:
    - "Γ′′ + 2ℋ Γ′ + a² V_{,Γ}(Γ) = 0"
    - "Omega_gamma_auto=on"
  association_matrix:
    - [ "GAMMA_FIELD", 0.9 ]
    - [ "GAMMA_DENSITY", 0.8 ]
    - [ "FREEZE_MANIFEST", 0.7 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Scalar Field Potential
      domain: QFT|GR|Cosmology
      mapping_kind: mathematical
      equation_hint: |
        L_Γ = (1/2) g^{μν} (∂_μ Γ) (∂_ν Γ) - V(Γ)
      justification: |
        V(Γ) is the potential energy term in the Lagrangian for a canonical scalar field in a general relativistic context. It dictates the field's mass (m_Γ² = V_{,ΓΓ}) and self-interactions, which is standard practice for models of inflation, quintessence, or scalar dark matter.
      references:
        - title: Modern Cosmology
          where: Dodelson & Schmidt, 2nd Ed., Chapter 7
          date: 2020-01-01
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "The Γ field's dynamics are governed by a `quadratic_plus_tail` potential whose parameters are fixed by the `COSMO-004` Freeze Manifest (m_Γ_eV=1.7e7, etc.)."
      domain: phenomenology
      falsifier: "Future cosmological surveys (e.g., CMB-S4, Euclid) measure a matter power spectrum, growth rate, or lensing signal whose likelihood decisively disfavors this specific potential form and its frozen parameters compared to the ΛCDM model or an alternative Γ-sector theory."
      status: supported
      links: [COSMO-004]
naming_notes:
  collisions: ["The symbol 'V' is commonly used for electrostatic potential or gravitational potential Φ, Ψ."]
  disambiguation: |
    Within the Pirouette Framework, V(Γ) refers exclusively to the self-interaction potential of the Γ scalar field. Gravitational potentials are denoted by Φ and Ψ, following standard cosmological notation.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [GAMMA_FIELD]
  downstream_effects: [GAMMA_DENSITY, GAMMA_PRESSURE, EFFECTIVE_SOUND_SPEED_GAMMA]
license: CC-BY-SA-4.0