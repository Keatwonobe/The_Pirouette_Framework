---
term: "Pressuron Piece"
canonical_id: "PRESSURON_PIECE"
symbol: "Δa_ℓ^(Γ)"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-014"]
---

---
term: Pressuron Piece
canonical_id: PRESSURON_PIECE
symbol: Δa_ℓ^(Γ)
aliases: [Pressuron one-loop, Γ-portal contribution]
parents: [MATH-013, MATH-014]
children: [PHEN-003] # Placeholder for fitting/phenomenology modules
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-014
      snippet: |
        [
        \boxed{; \Delta a_\ell^{(\Gamma)} = \frac{\alpha}{12\pi^2},\kappa^2,\Big(\frac{m_\ell}{m_e}\Big)^{!2p}, f!\left(\frac{m_\Gamma}{m_\ell}\right),\qquad f(0)=1. ;}
        ]
  editors: [AI Assistant]
  review_log: []
triad:
  art: |
    A new, subtle echo in the lepton's self-dialogue, revealing the resonant signature of a hidden field. It is the quantifiable whisper of the Pressuron, a faint harmony added to the main QED-like song of self-interaction.
  law: |
    The Pressuron Piece is an additive, positive-definite contribution to a lepton's anomalous magnetic moment (a_ℓ). Its magnitude is designed to scale with a power of the lepton's mass, making its effect on the muon naturally greater than on the electron.
  philosophy: |
    This term embodies the framework's core strategy: introducing new physics not as an arbitrary fix, but as a structured, mass-sensitive interaction. It tests the 'wound-channel' hypothesis, where heavier particles couple more strongly, providing a falsifiable mechanism to resolve lepton-family puzzles like the g-2 anomaly.
pirouette_definition: |
  The Pressuron Piece is the finite, one-loop contribution to a lepton's anomalous magnetic moment (a_ℓ) arising from its Yukawa-type interaction with the scalar Pressuron field (Γ). It is added to the universal QED-like series to account for deviations from standard predictions, particularly the muon g-2 anomaly. Its value is determined by the Pressuron's mass (m_Γ), a fundamental dimensionless coupling (κ), and a mass-scaling exponent (p) that governs its lepton non-universality.
operational_definition:
  units: dimensionless
  symbol_table:
    - name: Δa_ℓ^(Γ)
      meaning: Contribution to lepton (ℓ) anomalous magnetic moment from Pressuron (Γ)
      dimensions: dimensionless
      default_range: 10⁻¹² – 10⁻⁹ (for muon)
    - name: α
      meaning: Fine-structure constant
      dimensions: dimensionless
      default_range: ~1/137
    - name: κ
      meaning: Base dimensionless coupling of Pressuron to electron
      dimensions: dimensionless
      default_range: 10⁻⁴ – 10⁻² (fit-dependent)
    - name: p
      meaning: Lepton mass-scaling exponent
      dimensions: dimensionless
      default_range: 0–2, often hypothesized as p=1
    - name: m_ℓ
      meaning: Mass of lepton ℓ (e, μ, τ)
      dimensions: M
      default_range: contextual
    - name: m_Γ
      meaning: Mass of the Pressuron particle
      dimensions: M
      default_range: 1 MeV – 1 GeV (typical scan range)
    - name: f(r)
      meaning: Loop shape function, where r = m_Γ / m_ℓ
      dimensions: dimensionless
      default_range: (0, 1]
  measurement:
    procedures:
      - name: Inference via Global Fit
        outline: |
          The Pressuron Piece is not measured directly. It is inferred by constructing the total theoretical prediction for the lepton g-2, `a_ℓ = a_ℓ^uni + Δa_ℓ^(Γ)`, and fitting the free parameters (κ, p, m_Γ) to high-precision experimental data for `a_μ` and `a_e`. The best-fit value of `κ` determines the size of the contribution.
        expected_signals:
          - A statistically significant non-zero value for `κ` is required to match the muon g-2 experimental value.
          - The model simultaneously fits `a_μ` and respects the tight constraints from `a_e`, demonstrating the correctness of the `(m_μ/m_e)^2p` scaling.
        pitfalls:
          - Incorrect or uncertain values for the universal coefficients (C_n) can bias the fit for κ.
          - Degeneracies in the parameter space of (κ, p, m_Γ) can make unique determination difficult without additional constraints.
context_windows:
  - module: MATH-014
    excerpt: |
      We model the lepton anomalous magnetic moment as `a_ℓ = a_ℓ^uni(α) + Δa_ℓ^(Γ)(κ,p,m_Γ;m_ℓ) + δa_ℓ^rem`. The Pressuron piece (Δa_ℓ^(Γ)) is the one-loop Yukawa portal result from MATH-013v2. The combination is numerically stable, dimensionally correct, and fit-ready.
  - module: MATH-014
    excerpt: |
      For `p=1` and light (Γ), `Δa_μ^(Γ) / Δa_e^(Γ) ≈ (m_μ/m_e)²`, giving natural muon enhancement while respecting electron bounds. This scaling is a critical sanity check. Adding `Δa_ℓ^(Γ)` should reduce residuals `(a_ℓ^th − a_ℓ^exp)` without wild parameter swings.
poetic_connections:
  motifs: [resonant leak, asymptotic refinement, wound-channel, mass-scaling]
  evocative_lines:
    - "The anatomy of an echo."
    - "...letting the wound-channel hypothesis be tested against (e/μ) data without dimensional landmines."
  association_matrix:
    - [ "PRESSURON", 0.9 ]
    - [ "LEPTON_G_MINUS_2", 0.9 ]
    - [ "UNIVERSAL_PIECE", 0.7 ]
formal_mappings:
  candidates:
    - target: One-loop contribution to lepton g-2 from a new scalar particle
      domain: BSM
      mapping_kind: mathematical
      equation_hint: |
        Δa_ℓ ~ (g_ℓ² / 4π²) * ∫dx...  (Generic loop integral form)
      justification: |
        The derivation of Δa_ℓ^(Γ) follows the standard Feynman diagram calculation for a vertex correction involving a fermion loop with a new scalar. The resulting mathematical structure, including the loop integral function f(r), is a canonical result in Beyond the Standard Model physics for particles with Yukawa-type couplings.
      references:
        - title: An Introduction to Quantum Field Theory
          where: Peskin & Schroeder, Chapter 6
          date: 1995-10-01
      confidence: 0.95
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The Pressuron Piece is positive-definite, `Δa_ℓ^(Γ) > 0`."
      domain: theory
      falsifier: "A revised calculation reveals a sign error, or a more complete model (e.g., pseudoscalar coupling) introduces a negative sign."
      status: supported
      links: [MATH-014]
    - statement: "The term can account for the observed muon g-2 anomaly for some `(κ, p, m_Γ)` without violating experimental bounds on electron g-2."
      domain: phenomenology
      falsifier: "A global fit demonstrates that no point in the parameter space can simultaneously satisfy the experimental constraints for both the electron and muon."
      status: under-test
      links: []
naming_notes:
  collisions: [The symbol `Δa` is standard notation for any contribution to the anomalous magnetic moment. The superscript `(Γ)` is essential for disambiguation.]
  disambiguation: |
    The Pressuron Piece `Δa_ℓ^(Γ)` is the specific new physics contribution from the Pressuron. It must be distinguished from the `Universal Piece` `a_ℓ^uni`, which contains the Pirouette framework's equivalent of QED contributions, and from the `remainder` `δa_ℓ^rem`, which tracks higher-order terms or external inputs.
crosslinks:
  near_synonyms: []
  antonyms: [UNIVERSAL_PIECE]
  prerequisites: [PRESSURON, LEPTON_G_MINUS_2]
  downstream_effects: []
license: CC-BY-SA-4.0
---