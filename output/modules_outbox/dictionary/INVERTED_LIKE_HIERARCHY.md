---
term: "Inverted-like hierarchy"
canonical_id: "INVERTED_LIKE_HIERARCHY"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-Γ-005_the_pressuron_induced_neutrino_mass_mechanism"]
---

---
term: Inverted-like hierarchy
canonical_id: INVERTED_LIKE_HIERARCHY
symbol: 
aliases: [Γ-induced hierarchy, Coherence-drag ordering]
parents: [MATH-Γ-005]
children: [DYNA-Γ-NEU-OSC, COSMO-Γ-NEU-SEA]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-Γ-005
      lines: "§4"
      snippet: |
        the three neutrino flavors inherit masses in proportion:
        [ m_{\nu_e}!:!m_{\nu_\mu}!:!m_{\nu_\tau} = \frac{1}{m_e}!:!\frac{1}{m_\mu}!:!\frac{1}{m_\tau}. ]
        Numerically this reproduces an **inverted-like hierarchy**...
  editors: [agent: pirouette-scribe-v3]
  review_log: []
triad:
  art: |
    The three neutrinos are given weight not by a direct touch, but by the universe slowing the heartbeat of their passage. The heaviest charged leptons create the least drag for their partners, yielding the lightest neutrinos. This ordering is an echo of temporal resistance.
  law: |
    The masses of the three neutrino flavor eigenstates are inversely proportional to the masses of their corresponding charged-lepton partners: (m_{\nu_e} : m_{\nu_\mu} : m_{\nu_\tau} = 1/m_e : 1/m_\mu : 1/m_\tau). This fixes the mass-squared differences and predicts a specific inverted ordering where (m_{\nu_e} > m_{\nu_\mu} > m_{\nu_\tau}).
  philosophy: |
    This hierarchy provides a first-principles explanation for the neutrino mass ordering, linking it directly to the known charged-lepton mass spectrum. It resolves the ordering problem without invoking new sterile states or fine-tuned Yukawa couplings, rooting it instead in the dynamics of coherence and temporal drag.
pirouette_definition: |
  The specific, predicted neutrino mass ordering derived from the Pressuron-induced mass mechanism. In this hierarchy, the mass of a given neutrino flavor eigenstate is set in inverse proportion to the mass of its charged-lepton partner (electron, muon, or tau). This results in an ordering where the electron neutrino is heaviest and the tau neutrino is lightest, qualitatively resembling the standard Inverted Hierarchy but with fixed mass ratios.
operational_definition:
  units: eV/c²
  symbol_table:
    - name: m_{\nu_\ell}
      meaning: Mass of the neutrino flavor eigenstate associated with charged lepton ℓ.
      dimensions: M
      default_range: 0.001–0.05 eV/c²
    - name: m_\ell
      meaning: Mass of the charged lepton ℓ (e, μ, τ).
      dimensions: M
      default_range: 0.511–1777 MeV/c²
  measurement:
    procedures:
      - name: Global Oscillation Fit
        outline: |
          Perform a simultaneous fit to global neutrino oscillation data from long-baseline (DUNE, Hyper-K), short-baseline (reactor), and atmospheric experiments. Constrain the fit by fixing the ratio of the three mass eigenstates to the inverse ratio of their charged-lepton partners' masses. The goodness-of-fit (χ²) will test the validity of this hierarchy against standard Normal and Inverted Ordering hypotheses.
        expected_signals: [A preferred fit for this specific mass ratio over standard IO/NO, A 1–2% energy-dependent drift in oscillation maxima at long baselines.]
        pitfalls: [Systematic uncertainties in neutrino energy reconstruction, Poorly constrained matter effects mimicking or obscuring the signal, Neglecting energy dependence of mass in the analysis.]
context_windows:
  - module: MATH-Γ-005
    excerpt: |
      Assuming background Γ variance proportional to charged-lepton mass squared (from MATH-013), the three neutrino flavors inherit masses in proportion: (m_{\nu_e} : m_{\nu_\mu} : m_{\nu_\tau} = 1/m_e : 1/m_\mu : 1/m_\tau). Numerically this reproduces an **inverted-like hierarchy** with (m_{\nu_3} \approx 0.05\,\mathrm{eV}), (m_{\nu_2} \approx 0.009\,\mathrm{eV}), (m_{\nu_1} \approx 0.001\,\mathrm{eV}), consistent with oscillation data when normalized by atmospheric Δm².
  - module: MATH-Γ-005
    excerpt: |
      Failure to detect the predicted energy-dependent drift or a Σmν below 0.05 eV would falsify this minimal Γ-drag model and motivate a hybrid Γ-Higgs Majorana extension (→ DYNA-Γ-NEU-OSC). A conclusive experimental preference for the Normal Hierarchy would immediately refute the Inverted-like hierarchy.
poetic_connections:
  motifs: [temporal drag, coherence damping, inverse proportion, lepton-universality breaking]
  evocative_lines:
    - "Every oscillation is a faint echo of that temporal drag: the whisper of coherence feeling its own delay."
    - "The Pressuron gives them weight not by touching them, but by slowing the heartbeat of their passage through the universe."
  association_matrix:
    - [ "PRESSURON_INDUCED_MASS", 0.9 ]
    - [ "COHERENCE_DRAG", 0.8 ]
    - [ "CHARGED_LEPTON_MASS", 0.7 ]
    - [ "ENERGY_DEPENDENT_OSCILLATION_PHASE", 0.6 ]
formal_mappings:
  candidates:
    - target: Inverted Hierarchy (IH) / Inverted Ordering (IO)
      domain: SM
      mapping_kind: operational
      equation_hint: |
        Standard IO: m₃ < m₁ < m₂
        Pirouette ILH: m_{\nu_τ} < m_{\nu_μ} < m_{\nu_e} (when mapped to flavor states) with a fixed ratio.
      justification: |
        Both models predict a mass spectrum with one light state and two heavier, nearly-degenerate states. Operationally, they are difficult to distinguish without high-precision measurements of mass-squared differences and the absolute mass scale. The key difference is that Pirouette's model is not just an ordering but a predictive law relating the neutrino masses to other known constants.
      references:
        - title: Particle Data Group Review
          where: Neutrino Mass, Mixing, and Oscillations
          date: 2024-08-01
      confidence: 0.8
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The ratio of neutrino masses is fixed by the inverse ratio of charged lepton masses."
      domain: phenomenology
      falsifier: "Global oscillation data from DUNE, JUNO, and Hyper-K conclusively shows a preference for the Normal Hierarchy, or an Inverted Hierarchy with ratios inconsistent with 1/m_ℓ."
      status: proposed
      links: [DYNA-Γ-NEU-OSC]
    - statement: "The observed neutrino mass ordering is a consequence of the Pressuron-drag mechanism alone, without contributions from sterile neutrinos."
      domain: theory
      falsifier: "Unambiguous experimental discovery of a fourth, sterile neutrino state that participates in flavor oscillations."
      status: proposed
      links: [MATH-Γ-005]
naming_notes:
  collisions: []
  disambiguation: |
    The "Inverted-like hierarchy" should not be confused with the standard model's "Inverted Hierarchy" (IH) or "Inverted Ordering" (IO). While qualitatively similar in ordering the mass eigenstates (one light, two heavy), the Pirouette term refers to a *specific, predictive model* with fixed mass ratios, whereas the standard IH is a general phenomenological possibility with free parameters.
crosslinks:
  near_synonyms: []
  antonyms: [NORMAL_HIERARCHY]
  prerequisites: [PRESSURON_INDUCED_MASS, COHERENCE_DRAG]
  downstream_effects: [ENERGY_DEPENDENT_OSCILLATION_PHASE]
license: CC-BY-SA-4.0
---

# Inverted-like hierarchy

## Canonical (Pirouette)
The specific, predicted neutrino mass ordering derived from the Pressuron-induced mass mechanism. In this hierarchy, the mass of a given neutrino flavor eigenstate is set in inverse proportion to the mass of its charged-lepton partner (electron, muon, or tau). This results in an ordering where the electron neutrino is heaviest and the tau neutrino is lightest, qualitatively resembling the standard Inverted Hierarchy but with fixed mass ratios.

## EFT-First Summary
The Inverted-like hierarchy is a specific theoretical origin for the phenomenological **Inverted Ordering (IO)** of neutrino masses. While standard IO simply posits that mass eigenstate m₃ is lighter than m₁ and m₂, the Pirouette model predicts the mass ratios are rigidly determined by the masses of the electron, muon, and tau. This provides a falsifiable, parameter-free prediction for the mass-squared differences measured in neutrino oscillation experiments.

## Glossary Links
- See also: [PRESSURON_INDUCED_MASS](link), [ENERGY_DEPENDENT_OSCILLATION_PHASE](link)