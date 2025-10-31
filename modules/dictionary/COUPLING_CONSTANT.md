---
term: "Coupling Constant"
canonical_id: "COUPLING_CONSTANT"
symbol: "κ"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["XAP-008_Leptonic_g-2_gladiator_force_fit_map"]
---

---
term: Coupling Constant
canonical_id: COUPLING_CONSTANT_KAPPA
symbol: κ
aliases: []
parents: [XAP-008_Leptonic_g-2_gladiator_force_fit_map]
children: []
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: XAP-008_Leptonic_g-2_gladiator_force_fit_map
      lines: "§1"
      snippet: |
        We scan the three-parameter space $(\kappa, p, m_\Gamma)$ for leptonic magnetic-moment shifts
        \[
        \Delta a_\ell^{(\Gamma)}=\kappa\Big(\frac{m_\ell}{m_e}\Big)^p\Big(\frac{\alpha}{\pi}\Big)^3
        \,\underbrace{\frac{m_\ell^2}{m_\ell^2+m_\Gamma^2}}_{F_\ell(m_\Gamma)},
        \]
  editors: [Pirouette Dictionary Engine]
  review_log: []
triad:
  art: |
    The volume knob for the Gladiator Force. κ dictates how loudly new physics whispers into the precise dance of leptons, tuning the strength of their secret conversation.
  law: |
    The parameter κ is the dimensionless prefactor in the one-loop Gladiator-Force correction to lepton anomalous magnetic moments, $\Delta a_\ell$. Its value is constrained by the requirement that calculated $\Delta a_e$ and $\Delta a_\mu$ values fall within specified experimental bands.
  philosophy: |
    κ quantifies our ignorance of the absolute scale of the Gladiator interaction. As a free parameter, its empirical constraint maps the boundary between the Standard Model and Pirouette's extended leptonic sector, serving as a primary target for falsification.
pirouette_definition: |
  A dimensionless coupling constant, κ, that sets the overall strength of the Gladiator Force's contribution to the anomalous magnetic moments of leptons $(\ell)$. It is determined empirically by fitting the calculated shifts, $\Delta a_\ell^{(\Gamma)}$, to experimental constraints on the electron and muon g-2 anomalies.
operational_definition:
  units: dimensionless
  symbol_table:
    - name: κ
      meaning: Gladiator Force coupling constant
      dimensions: dimensionless
      default_range: 10⁻⁴ to 10⁻³ (tight band phenomenology)
  measurement:
    procedures:
      - name: Global fit to leptonic g-2
        outline: |
          Infer the viable range of κ by performing a multi-parameter scan over the $(\kappa, p, m_\Gamma)$ space. For each point, calculate the predicted anomalous magnetic moment shifts $\Delta a_e$ and $\Delta a_\mu$. The allowed region for κ is defined by the set of points where both calculated shifts lie within experimentally determined constraint bands (e.g., bands A or B in XAP-008).
        expected_signals: [A non-zero value of κ would be signaled by a statistically significant deviation in measured g-2 values that is well-described by the Gladiator Force model, particularly a correlated deviation in both electron and muon moments.]
        pitfalls: [Degeneracies with other parameters (p, mΓ), Mismodeling of Standard Model contributions to g-2, The true source of a g-2 anomaly being a different new physics model.]
context_windows:
  # Short, trimmed context quotes harvested from modules (3–6 sentences each).
  - module: XAP-008_Leptonic_g-2_gladiator_force_fit_map
    excerpt: |
      We scan the three-parameter space $(\kappa, p, m_\Gamma)$ for leptonic magnetic-moment shifts. Tight band favors $p\!\gtrsim\!1.5$–$2.5$ with $\kappa\!\sim\!10^{-4}$–$10^{-3}$; permissive band admits smaller $p$ or lighter $m_\Gamma$ if $\kappa\!\lesssim\!10^{-4}$.
  - module: XAP-008_Leptonic_g-2_gladiator_force_fit_map
    excerpt: |
      The CSV set is designed for your “Great Plotting” API: each paper job can import the CSVs, fit contours, and render parameter wedges without re-running the scan. XAP-008 publishes the $(\kappa,p,m_\Gamma)$ regions consistent with both $e$ and $\mu$ magnetic moments.
poetic_connections:
  # Lightweight "word-association graph" and sticky lines.
  motifs: [interaction strength, dimensionless constant, phenomenological fitting, new physics scale]
  evocative_lines:
    - "The volume knob for the Gladiator Force..."
    - "mapping the boundary between the Standard Model and Pirouette's extended leptonic sector"
  association_matrix:
    # symmetric or directed; weights in [0,1]
    - [ "LEPTON_MASS_SCALING_P", 0.8 ]
    - [ "GLADIATOR_MASS_M_GAMMA", 0.8 ]
formal_mappings:
  # Candidate alignments to EFT/SM/CM/GR terms, each with justification and refs.
  candidates:
    - target: New Physics Coupling Constant (e.g., $g_{NP}$)
      domain: EFT
      mapping_kind: conceptual
      equation_hint: |
        $\mathcal{L}_{int} \sim g_{NP} \bar{\psi} \phi \psi$
      justification: |
        κ is a dimensionless parameter that, like a generic coupling constant in an effective field theory, sets the overall interaction strength of a new force. It is not derived from a deeper principle within the model excerpt but is instead a free parameter to be constrained by experiment.
      references: []
      confidence: 0.9
  adopted:
    - target: Generic EFT Coupling Constant
      rationale: |
        This mapping is adopted because κ functions identically to a free coupling parameter in a bottom-up EFT model: it is dimensionless, sets the strength of a new interaction, and its value is determined by fitting to low-energy observables rather than being predicted by the theory's structure.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: 'A non-zero value of κ (specifically in the range $10^{-4}$ to $10^{-3}$ for $p \gtrsim 1.5$) is required to explain the muon g-2 anomaly within the Gladiator Force model while respecting electron g-2 constraints.'

      domain: phenomenology
      falsifier: 'Future, more precise measurements of $\Delta a_\mu$ and $\Delta a_e$ could shrink the allowed parameter space to the empty set, or a confirmed Standard Model calculation that agrees with experiment would eliminate the need for any non-zero κ.'

      status: proposed
      links: [XAP-008_Leptonic_g-2_gladiator_force_fit_map]
naming_notes:
  collisions: [κ is sometimes used for curvature in general relativity or thermal conductivity in thermodynamics. Context (leptonic physics, Gladiator Force) is critical for disambiguation.]
  disambiguation: |
    This κ is specific to the Gladiator Force interaction. Distinguish from other Pirouette couplings, which may be denoted by different symbols (e.g., g, λ) and pertain to different sectors of the theory.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [LEPTON_ANOMALOUS_MOMENT]
  downstream_effects: [GLADIATOR_FORCE, LEPTON_MASS_SCALING_P, GLADIATOR_MASS_M_GAMMA]
license: CC-BY-SA-4.0
---

# Coupling Constant

## Canonical (Pirouette)
A dimensionless coupling constant, κ, that sets the overall strength of the Gladiator Force's contribution to the anomalous magnetic moments of leptons $(\ell)$. It is determined empirically by fitting the calculated shifts, $\Delta a_\ell^{(\Gamma)}$, to experimental constraints on the electron and muon g-2 anomalies.

## EFT-First Summary
In the language of effective field theory (EFT), the Pirouette coupling constant κ is a generic, dimensionless parameter setting the interaction strength of the new Gladiator Force. Its value is not predicted but must be inferred from experiment, analogous to other free parameters in a bottom-up EFT model. Current constraints from lepton anomalous magnetic moments place κ in the approximate range of $10^{-4}$ to $10^{-3}$.

## Glossary Links
- See also: Gladiator Force, Lepton Mass Scaling (p), Gladiator Mass (mΓ)