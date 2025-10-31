---
term: "Late-ISW Effect"
canonical_id: "LATE_ISW_EFFECT"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["COSMO-Γ-001_the_early_universe"]
---

---
term: Late-ISW Effect (Pirouette)
canonical_id: LATE_ISW_EFFECT_GAMMA
symbol: δT_ISW(Γ)
aliases: [Integrated Sachs-Wolfe effect (Γ-tail), Γ-ISW]
parents: [COSMO-Γ-002]
children: [COSMO-Γ-CMB]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: COSMO-Γ-002
      lines: "L102-L104"
      snippet: |
        **Late-ISW** sign/magnitude fixed by the chosen tail (exponential vs cosine), preregistered with AIC/BIC comparisons against ΛCDM and (w_0w_a)CDM.
  editors: [auto-agent]
  review_log: []
triad:
  art: |
    The universe’s fading hum, where photons gain or lose energy passing through the shallowing gravitational valleys carved by the Γ field's slow-roll tail. It is a whisper of dark energy, heard only in the largest patches of the sky.
  law: |
    The sign and magnitude of the angular power spectrum cross-correlation between CMB temperature and gravitational potential (C_l^{TΦ}) on large scales (l < 50) is uniquely determined by the preregistered functional form of the V(Γ) tail (e.g., cosine vs. exponential) and its frozen parameters. A measurement inconsistent with the predicted sign or a >3σ deviation from the predicted magnitude falsifies the chosen tail.
  philosophy: |
    The Late-ISW Effect serves as a critical test of the Γ field's dual role, bridging its early-universe, matter-like behavior with its late-universe, dark-energy-like behavior. Its detection with the predicted characteristics would validate the unification mechanism, confirming that the same field driving structure formation is also responsible for cosmic acceleration, without requiring a separate cosmological constant.
pirouette_definition: |
  A secondary temperature anisotropy in the Cosmic Microwave Background (CMB) generated at late cosmic times (z ≲ 2). It arises as CMB photons traverse time-varying gravitational potentials, where the potential decay is driven specifically by the Γ field entering its slow-roll, dark energy-like phase, as dictated by the tail of its potential, V(Γ). The effect's sign, magnitude, and scale-dependence are a direct, non-tunable prediction of the chosen V(Γ) form, providing a key falsifiable test of the Γ-unification model against ΛCDM.
operational_definition:
  units: Dimensionless (δT/T) or temperature-squared for power spectra (μK²).
  symbol_table:
    - name: δT_ISW(Γ)
      meaning: CMB temperature fluctuation due to the Γ-driven ISW effect.
      dimensions: Temperature (Θ)
      default_range: 10⁻⁵ – 10⁻⁶ K
    - name: Φ
      meaning: Gravitational potential perturbation in the Newtonian gauge.
      dimensions: L² T⁻² (velocity squared)
      default_range: contextual
    - name: C_l^{TΦ}
      meaning: Angular power spectrum of the cross-correlation between CMB temperature and the lensing potential (a tracer of Φ).
      dimensions: Temperature (Θ)
      default_range: contextual
  measurement:
    procedures:
      - name: Large-Scale Structure Cross-Correlation
        outline: |
          1. Generate a full-sky map of CMB temperature anisotropies (e.g., from Planck satellite data).
          2. Generate a map of a large-scale structure tracer, which traces the gravitational potential Φ at low redshift (e.g., from galaxy counts in surveys like DES, Euclid, or CMB lensing reconstruction).
          3. Compute the angular cross-power spectrum C_l^{TΦ} between the two maps.
          4. Compare the detected signal at low multipoles (l < 50) against the preregistered prediction from the Γ-model's V(Γ) tail.
        expected_signals: [A statistically significant non-zero C_l^{TΦ} signal at l < 50, A specific sign (positive or negative correlation) predicted by the V(Γ) tail.]
        pitfalls: [High cosmic variance on large angular scales, Contamination from galactic foregrounds (e.g., dust), Shot noise and systematic errors in the galaxy survey data.]
context_windows:
  - module: COSMO-Γ-002
    excerpt: |
      **CMB (link to COSMO-Γ-CMB):**
      * **TT/TE/EE** and **lensing** spectra with the same freeze; require Planck-level consistency under tail choice and switch scans (<0.2%).
      * **Late-ISW** sign/magnitude fixed by the chosen tail (exponential vs cosine), preregistered with AIC/BIC comparisons against ΛCDM and (w_0w_a)CDM.
  - module: COSMO-Γ-002
    excerpt: |
      We adopt the **quadratic-plus-tail** potentials already allowed in your base module, which yield CDM-like behavior **early** and a **slow-roll** tendency **late** (addressing coincidence without post-hoc tuning):
      * Exponential-shallow or **cosine tail** remnants of shift symmetry; parameters ((\mu, f, \Gamma_*)) are **U-class** constants **frozen** by a D3 one-shot anchor.
poetic_connections:
  motifs: [fading echo, slowing drumbeat, gravitational tides, cosmic whisper]
  evocative_lines:
    - "...the tail in V(Γ) slows the drum at late times, whispering as dark energy."
    - "...they are one score, played on a single instrument."
  association_matrix:
    - [ "GAMMA_POTENTIAL_TAIL", 0.9 ]
    - [ "COSMIC_ACCELERATION_GAMMA", 0.8 ]
    - [ "COINCIDENCE_PROBLEM", 0.7 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Integrated Sachs-Wolfe (ISW) Effect
      domain: GR
      mapping_kind: mathematical
      equation_hint: |
        δT/T = 2 ∫ dη (∂Φ/∂η), where evolution of Φ is sourced by Γ.
      justification: |
        The Pirouette Late-ISW Effect is the standard general relativistic phenomenon. Its defining characteristic within the framework is that the source of potential decay (∂Φ/∂η) is not a cosmological constant or generic dark energy, but is a specific, calculable consequence of the Γ field's dynamics governed by its potential V(Γ). This maps a general effect to a specific, falsifiable cause.
      references:
        - title: "Gravitational-Potential Anisotropy of the Microwave Background"
          where: "Astrophys. J. 147, 73"
          date: 1967-01-01
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The sign of the CMB temperature-gravitational potential cross-correlation (C_l^{TΦ}) is a unique, non-tunable prediction of the chosen V(Γ) tail."
      domain: phenomenology
      falsifier: "An observation of the opposite sign, or a null detection where a >3σ signal is predicted, would falsify the specific preregistered V(Γ) tail."
      status: proposed
      links: [COSMO-Γ-002, COSMO-Γ-CMB]
naming_notes:
  collisions: [ISW Effect]
  disambiguation: |
    Distinguish from the *Early*-ISW effect, which occurs around recombination, and the standard ISW effect in ΛCDM, which is sourced by a true cosmological constant (w=-1). The Pirouette effect is dynamically sourced by the Γ field's potential and predicts a specific, non-ΛCDM evolution for w(z). The term `Late-ISW Effect (Pirouette)` or `Γ-ISW` should be used to specify this model-dependent origin.
crosslinks:
  near_synonyms: [GAMMA_DARK_ENERGY_EFFECT]
  antonyms: []
  prerequisites: [PRESSURON_FIELD_GAMMA, GAMMA_POTENTIAL_TAIL]
  downstream_effects: [COSMIC_ACCELERATION_GAMMA]
license: CC-BY-SA-4.0
---