---
term: "Pressuron mass"
canonical_id: "PRESSURON_MASS"
symbol: "m_p"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["XAP-007_pressuraon_constraint_atlas"]
---

---
term: Pressuron mass
canonical_id: PRESSURON_MASS
symbol: m_p
aliases: []
parents: [XAP-007, XAP-006E]
children: [XAP-008]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: XAP-007_pressuraon_constraint_atlas
      lines: "§1"
      snippet: |
        m_p=Γ_0√2λ_Γ
  editors: [GPT-4 (Pirouette Dictionary Agent)]
  review_log: []
triad:
  art: |
    The pressuron's mass is the weight of a whisper in the cosmic superfluid, a faint echo whose silence or discovery will shape our understanding of the void's true texture.
  law: |
    The pressuron mass `m_p` is a derived parameter, determined by the background coherence density `Γ_0` and the self-coupling `λ_Γ` as `m_p = Γ_0√2λ_Γ`. Current constraints place it in the 10–30 MeV range, which is testable via missing energy searches at colliders and beam-dump experiments.
  philosophy: |
    `m_p` serves as a critical bridge between the abstract Pirouette substrate (Γ-stiffness) and concrete, falsifiable particle phenomenology. It parameterizes the "cost" of localizing a coherence fluctuation, making it the primary target for experiments seeking to validate or constrain the framework's cosmological extension.
pirouette_definition: |
  The pressuron mass `m_p` is the effective mass of the composite excitation of the Γ-field, representing the energy scale of a localized fluctuation in the background coherence density `Γ_0`. It is derived from the framework's two primary stiffness parameters: the background coherence `Γ_0` and the self-coupling constant `λ_Γ`, according to the relation `m_p = Γ_0√2λ_Γ`. This mass sets the scale for pressuron production thresholds and the decay rate of its associated Yukawa potential.
operational_definition:
  units: MeV/c² (often simplified to MeV in natural units)
  symbol_table:
    - name: m_p
      meaning: Pressuron mass
      dimensions: M
      default_range: 10–30 MeV
    - name: Γ_0
      meaning: Background coherence density
      dimensions: M²
      default_range: contextual
    - name: λ_Γ
      meaning: Pressuron self-coupling constant
      dimensions: "dimensionless"
      default_range: 0.05–0.2
  measurement:
    procedures:
      - name: Missing Energy / Mass at Colliders
        outline: |
          Search for processes like `e⁺e⁻ → γ + invisible` or rare meson decays (`B → K + invisible`) where the invisible component is a pair of pressurons (`ΓΓ`). The pressuron mass `m_p` can be reconstructed from the kinematics of the visible particles, or a lower limit can be set based on the available phase space and null results from high-luminosity experiments.
        expected_signals: [An excess in the missing mass spectrum over Standard Model backgrounds, A deviation from predicted branching ratios for rare decays]
        pitfalls: [Backgrounds from neutrino production, Low signal cross-section requiring high luminosity, Model-dependence of the production mechanism via coupling κ]
context_windows:
  - module: XAP-007
    excerpt: |
      Processes e⁺e⁻→γΓΓ and B→KΓΓ yield missing-energy signatures. Cross section: σ_ΓΓ ∝ κ² α s/m_p⁴. LEP and Belle-II null results imply m_p > 10 MeV for κ > 10⁻³. Upcoming Belle-II phase-3 will probe the predicted fiducial window.
  - module: XAP-007
    excerpt: |
      Energy loss rate per unit mass: ε̇_Γ ≃ (κ²/4π)T⁴e⁻ᵐᵖ/ᵀ. HB and RG stars constrain m_p > 3 MeV or κ < 10⁻⁴. These bounds are consistent with Pirouette’s default parameters.
poetic_connections:
  motifs: [residual stiffness, cosmic superfluid, fifth force, missing energy]
  evocative_lines:
    - "Λ as Residual Γ-Stiffness"
    - "The remaining parameter window defines a decisive target for forthcoming experiments"
  association_matrix:
    - [ "GAMMA_STIFFNESS", 0.9 ]
    - [ "FIFTH_FORCE", 0.7 ]
    - [ "MISSING_ENERGY", 0.8 ]
formal_mappings:
  candidates:
    - target: Axion-Like Particle (ALP) mass
      domain: EFT
      mapping_kind: operational
      equation_hint: |
        L ⊃ (1/2)(∂_μ a)² - (1/2)m_a² a² + ...
      justification: |
        Operationally, the pressuron behaves as a light, weakly interacting scalar particle. Its mass `m_p` is constrained by the same classes of experiments—missing energy, beam dumps, and stellar cooling—used to constrain the mass of ALPs. This mapping allows for direct translation of experimental limits, though the pressuron's origin from a substrate stiffness differs fundamentally from the typical ALP origin in a spontaneously broken global symmetry.
      references:
        - title: "Axion Cosmology"
          where: "Annu. Rev. Nucl. Part. Sci. 2010. 60:405-40"
          date: 2010-01-01
      confidence: 0.8
  adopted:
    - target: Axion-Like Particle (ALP) mass
      rationale: The experimental search strategies (missing energy, fifth force, stellar cooling) and phenomenological role as a light, weakly-coupled boson provide a direct and fruitful operational mapping to the well-established ALP paradigm, allowing Pirouette to leverage existing experimental limits and search strategies.
      confidence: 0.8
constraints_and_falsifiers:
  claims:
    - statement: "The pressuron mass `m_p` lies in the 10–30 MeV range."
      domain: phenomenology
      falsifier: "A confirmed signal for a pressuron-like particle with a mass outside this range (e.g., at 1 MeV or 100 MeV), or definitive null results from experiments like Belle-II and FASER2 that exclude the entire predicted (m_p, κ) parameter space."
      status: under-test
      links: [XAP-007]
    - statement: "The pressuron mass `m_p` is a derived quantity, determined by the background coherence `Γ_0` and self-coupling `λ_Γ`."
      domain: theory
      falsifier: "An experimental measurement where the pressuron mass is observed to be independent of parameters controlling the fifth-force range (related to `λ_Γ`) or the effective cosmological constant (related to `Γ_0`)."
      status: proposed
      links: [XAP-007, XAP-006E]
naming_notes:
  collisions: [The symbol `m_p` is the standard notation for the proton mass. Context within the Pirouette framework is required for disambiguation.]
  disambiguation: |
    Within Pirouette, `m_p` refers exclusively to the pressuron mass. When interfacing with Standard Model physics, use `m_pressuron` or explicitly state `m_p (pressuron)` if ambiguity with the proton mass `m_p (proton)` is possible.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [GAMMA_STIFFNESS, BACKGROUND_COHERENCE_DENSITY]
  downstream_effects: [FIFTH_FORCE, STELLAR_COOLING, LEPTON_ANOMALY]
license: CC-BY-SA-4.0
---

# Pressuron mass

## Canonical (Pirouette)
The pressuron mass `m_p` is the effective mass of the composite excitation of the Γ-field, representing the energy scale of a localized fluctuation in the background coherence density `Γ_0`. It is derived from the framework's two primary stiffness parameters: the background coherence `Γ_0` and the self-coupling constant `λ_Γ`, according to the relation `m_p = Γ_0√2λ_Γ`. This mass sets the scale for pressuron production thresholds and the decay rate of its associated Yukawa potential.

## EFT-First Summary
The pressuron mass, `m_p`, is operationally analogous to the mass of an Axion-Like Particle (ALP), constrained by astrophysical, cosmological, and collider data to a fiducial range of 10–30 MeV. It is searched for primarily via missing energy signatures in fixed-target experiments and B-factories. Its existence at this mass scale is a key testable prediction of the Pirouette framework's cosmological sector [Ref: XAP-007].

## Glossary Links
- See also: Γ-Stiffness, Background Coherence Density, Fifth Force