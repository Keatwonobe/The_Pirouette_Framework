---
term: "Substrate Lagrangian"
canonical_id: "SUBSTRATE_LAGRANGIAN"
symbol: '\(\mathcal L^{(\tau)}\)'

aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-027"]
---

---
term: Substrate Lagrangian
canonical_id: SUBSTRATE_LAGRANGIAN
symbol: \(\mathcal L^{(\tau)}\)
aliases: []
parents: [MATH-027, DYNA-004]
children: [MATH-027]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-027
      lines: "§1"
      snippet: |
        The minimal quadratic substrate Lagrangian (before Σ) is
        \begin{equation}
        \mathcal L^{(\tau)}_{Ki,\,\text{quad}}
        = K_{Ki}\,|\partial_\tau Ki|^2
        - \Lambda_{Ki}\,|\nabla_\tau Ki|^2
        - m_{Ki,\tau}^2\,|Ki|^2 ,
        \end{equation}
        with anisotropic “temporal” and “spatial” stiffnesses \(K_{Ki},\Lambda_{Ki}>0\).
  editors: [agent: auto-fill]
  review_log: []
triad:
  art: |
    The substrate Lagrangian is the blueprint of motion before the universe crystallizes into the familiar stage of spacetime. It describes dynamics in a more primordial, anisotropic medium, where "speed" and "mass" are just stiffnesses waiting to be properly scaled.
  law: |
    The Substrate Lagrangian \(\mathcal L^{(\tau)}\) for a scalar field \(Ki\) is given by \(\mathcal L^{(\tau)}_{Ki} = K_{Ki}\,|\partial_\tau Ki|^2 - \Lambda_{Ki}\,|\nabla_\tau Ki|^2 - V(|Ki|)\). Its equations of motion describe field evolution in raw substrate coordinates \((\tau, \mathbf{u})\), and its kinetic coefficients \(K_{Ki}\) and \(\Lambda_{Ki}\) directly set the emergent speed of light for that field species.
  philosophy: |
    This object represents the principle that Lorentz covariance is not fundamental but emergent. By postulating a more basic, anisotropic Lagrangian, the framework can treat the observed constancy of the speed of light as a consequence of the substrate's material properties (stiffnesses), rather than as a built-in axiom of geometry.
pirouette_definition: |
  The Lagrangian density for a field, such as \(Ki\), defined over the time substrate \(\mathcal M_\tau\) with coordinates \((\tau, \mathbf{u})\). The quadratic form for a complex scalar \(Ki\) is \(\mathcal L^{(\tau)}_{Ki,\,\text{quad}} = K_{Ki}\,|\partial_\tau Ki|^2 - \Lambda_{Ki}\,|\nabla_\tau Ki|^2 - m_{Ki,\tau}^2\,|Ki|^2\). It is characterized by distinct temporal (\(K\)) and spatial (\(\Lambda\)) kinetic stiffness coefficients, which are not a priori related. Physical, observer-frame Lagrangians \(\mathcal L^{(obs)}\) with emergent Lorentz covariance are derived from \(\mathcal L^{(\tau)}\) by coordinate and field rescalings that depend on these stiffnesses.
operational_definition:
  units: Energy density ([Energy]⁴ in natural units).
  symbol_table:
    - name: \(\mathcal L^{(\tau)}\)
      meaning: Substrate Lagrangian density
      dimensions: M L⁻¹ T⁻²
      default_range: contextual
    - name: \(\tau\)
      meaning: Substrate time coordinate
      dimensions: T_τ
      default_range: contextual
    - name: \(K\)
      meaning: Temporal stiffness coefficient
      dimensions: M² L² T⁻² (or Energy² T_τ²)
      default_range: "> 0"
    - name: \(\Lambda\)
      meaning: Spatial stiffness coefficient
      dimensions: M² L⁴ T⁻² (or Energy² L_u²)
      default_range: "> 0"
    - name: \(m_{\tau}\)
      meaning: Substrate mass parameter
      dimensions: M L² T⁻² (or Energy)
      default_range: contextual
  measurement:
    procedures:
      - name: Inferring Substrate Anisotropy
        outline: |
          Measure the dispersion relation of a particle at ultra-high energies, searching for deviations from the Lorentz-invariant form \(E^2 = p^2c^2 + m^2c^4\). A confirmed deviation matching the form \(K\omega^2 = \Lambda\mathbf k^2 + m_\tau^2\) would allow for the extraction of the ratio \(\Lambda/K\), which defines the emergent light cone for that species.
        expected_signals: [Energy-dependent speed of light, species-dependent maximum velocities, violation of Lorentz invariance in scattering thresholds.]
        pitfalls: [Effects are likely suppressed by a very high energy scale (e.g., Planck scale), making them difficult to distinguish from other quantum gravity phenomena. The measured Lorentz symmetry may be an extremely precise low-energy approximation.]
context_windows:
  - module: MATH-027
    excerpt: |
      The minimal quadratic substrate Lagrangian (before Σ) is \(\mathcal L^{(\tau)}_{Ki,\,\text{quad}} = K_{Ki}\,|\partial_\tau Ki|^2 - \Lambda_{Ki}\,|\nabla_\tau Ki|^2 - m_{Ki,\tau}^2\,|Ki|^2\), with anisotropic “temporal” and “spatial” stiffnesses \(K_{Ki},\Lambda_{Ki}>0\). The Γ–sector contributes an effective mass... Using the light-cone result \(c^2=\Lambda_\Gamma/K_\Gamma\) (XAP-005), one defines rescaled time \(t = \sqrt{K_{Ki}}\,\tau\) and spatial metric \(\mathbf x = \sqrt{\Lambda_{Ki}}\,\mathbf u\) to recover the Lorentz-covariant quadratic form.
  - module: DYNA-004
    excerpt: |
      The fundamental action in Pirouette is defined not on spacetime, but on the time substrate \(\mathcal M_\tau\). The Substrate Lagrangian \(\mathcal L^{(\tau)}\) captures the dynamics in this pre-geometric representation. It is the source from which the observer-frame metric and relativistic invariance emerge via the Σ-pushforward. The anisotropy between its temporal kinetic term (proportional to \(K\)) and spatial gradient term (proportional to \(\Lambda\)) is not a bug, but the central feature that allows spacetime to be constructed rather than assumed.
poetic_connections:
  motifs: [anisotropy, emergence, stiffness, pre-geometric, fluid-dynamics]
  evocative_lines:
    - "anisotropic 'temporal' and 'spatial' stiffnesses"
    - "spacetime to be constructed rather than assumed"
  association_matrix:
    - [ "Temporal Stiffness", 0.9 ]
    - [ "Spatial Stiffness", 0.9 ]
    - [ "Emergent Spacetime", 0.8 ]
    - [ "Lorentz Covariance", 0.5 ]
formal_mappings:
  candidates:
    - target: Anisotropic/Aether EFT Lagrangian
      domain: EFT
      mapping_kind: mathematical
      equation_hint: |
        \(\mathcal L^{(\tau)} = K\,|\partial_\tau \phi|^2 - \Lambda\,|\nabla \phi|^2 - V(\phi)\) maps to an EFT with a preferred frame where \(u^\mu = (1, \mathbf{0})\), such that \((\partial_\mu \phi)^2 \rightarrow (u^\mu \partial_\mu \phi)^2 - (g^{\mu\nu}-u^\mu u^\nu)\partial_\mu\phi\partial_\nu\phi\).
      justification: |
        The Substrate Lagrangian explicitly separates temporal and spatial kinetic terms, which is the defining characteristic of theories with a preferred reference frame (aether EFTs). This form is common in the Effective Field Theory of Inflation and other cosmological models that break Lorentz invariance. The substrate itself provides the preferred frame.
      references:
        - title: The effective field theory of inflation
          where: "JHEP 03 (2008) 014"
          date: 2008-03-07
      confidence: 0.8
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: 'The kinetic coefficients \(K\) and \(\Lambda\) can differ between particle species, leading to distinct emergent light cones for different fields (e.g., \(c_{photon} \neq c_{graviton}\)) at a fundamental level.'

      domain: phenomenology
      falsifier: 'Precise, multi-messenger astronomical observations (e.g., GW170817) confirming the arrival times of photons and gravitons from a distant source are identical to a high degree of accuracy, constraining \(|c_g/c_\gamma - 1| < 10^{-15}\). This would force most species-dependent effects to be negligible.'

      status: proposed
      links: [XAP-005]
naming_notes:
  collisions: [The symbol \(\mathcal L\) is the standard notation for any Lagrangian density. The superscript \((\tau)\) is crucial for distinguishing it from the observer-frame, Lorentz-covariant Lagrangian.]
  disambiguation: |
    Always distinguish the Substrate Lagrangian \(\mathcal L^{(\tau)}\), defined in \((\tau, \mathbf{u})\) coordinates, from the observer-frame Lagrangian \(\mathcal L^{(obs)}\), which is defined in rescaled \( (t, \mathbf{x}) \) coordinates and is manifestly Lorentz-covariant. All physical calculations of scattering amplitudes must use the observer-frame version or appropriately rescaled propagators and vertices derived from \(\mathcal L^{(\tau)}\).
crosslinks:
  near_synonyms: []
  antonyms: [LORENTZ_INVARIANT_LAGRANGIAN]
  prerequisites: [SUBSTRATE_COORDINATES, TEMPORAL_STIFFNESS, SPATIAL_STIFFNESS]
  downstream_effects: [EMERGENT_LORENTZ_COVARIANCE, KI_PROPAGATOR, SPECIES_DEPENDENT_LIGHT_CONES]
license: CC-BY-SA-4.0
---

# Substrate Lagrangian

## Canonical (Pirouette)
The Lagrangian density for a field, such as \(Ki\), defined over the time substrate \(\mathcal M_\tau\) with coordinates \((\tau, \mathbf{u})\). The quadratic form for a complex scalar \(Ki\) is \(\mathcal L^{(\tau)}_{Ki,\,\text{quad}} = K_{Ki}\,|\partial_\tau Ki|^2 - \Lambda_{Ki}\,|\nabla_\tau Ki|^2 - m_{Ki,\tau}^2\,|Ki|^2\). It is characterized by distinct temporal (\(K\)) and spatial (\(\Lambda\)) kinetic stiffness coefficients, which are not a priori related. Physical, observer-frame Lagrangians \(\mathcal L^{(obs)}\) with emergent Lorentz covariance are derived from \(\mathcal L^{(\tau)}\) by coordinate and field rescalings that depend on these stiffnesses.

## EFT-First Summary
In the language of Effective Field Theory (EFT), the Substrate Lagrangian is an instance of a Lorentz-violating theory, typical of aether models or the EFT of inflation. It posits a preferred reference frame (that of the substrate) where the kinetic terms for time derivatives (\(|\partial_\tau \phi|^2\)) and spatial derivatives (\(|\nabla \phi|^2\)) have independent coefficients. Standard Lorentz-invariant physics is recovered as a low-energy emergent symmetry when these coefficients are rescaled into a universal speed of light for each particle species.

## Glossary Links
- See also: [Temporal Stiffness](<#>), [Spatial Stiffness](<#>), [Emergent Spacetime](<#>)