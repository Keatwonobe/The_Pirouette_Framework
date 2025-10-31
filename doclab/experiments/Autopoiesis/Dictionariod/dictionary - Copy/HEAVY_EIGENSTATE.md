---
term: "Heavy Eigenstate"
canonical_id: "HEAVY_EIGENSTATE"
symbol: "Γ_H"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-021"]
---

---
term: Heavy Eigenstate
canonical_id: HEAVY_EIGENSTATE
symbol: Γ_H
aliases: []
parents: [MATH-021, XXP-015]
children: [SECT-Γ-A, SECT-Γ-B, SECT-Γ-C]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-021
      lines: "L15-L16"
      snippet: |
        • Particle (UV/leptonic): XXP-015 → a heavy Γ quantum m_H ≈ 17 MeV fits lepton g−2 portal effects.
  editors: [chain-of-thought-agent]
  review_log: []
triad:
  art: |
    The visible anchor of a vast, hidden chain, its weight felt in the subtle dance of leptons, oblivious to the faint whisper of its lighter twin shaping the cosmos.
  law: |
    The existence of a particle with mass m_H ≈ 17 MeV that couples to Standard Model leptons is a necessary, but not sufficient, condition for Γ-sector unification. Its precise coupling pattern and the observational signatures of its cosmological partner (or lack thereof) must discriminate between the proposed underlying mechanisms (A, B, or C).
  philosophy: |
    Γ_H embodies the 'one-shot anchor' principle: a single, high-mass, lab-accessible particle is used to fix the parameters of an entire dark sector. This ensures that the sector's cosmological predictions are not ad-hoc but are derived, falsifiable consequences of a unified theory.
pirouette_definition: |
  The massive particle state emerging from the Γ sector, denoted Γ_H, with a mass m_H anchored by lepton portal effects at ≈ 17 MeV. Its nature depends on the underlying sector architecture:
  - In Superfluid models (Mechanism A), it is the fundamental quantum of the cosmic condensate.
  - In Clockwork models (Mechanism B), it is the heaviest mass eigenstate of a coupled scalar chain.
  - In Cascade models (Mechanism C), it is an early-universe metastable state that has since decayed.
operational_definition:
  units: MeV/c² (mass)
  symbol_table:
    - name: Γ_H
      meaning: The Heavy Eigenstate field or particle.
      dimensions: M
      default_range: contextual
    - name: m_H
      meaning: Mass of the Heavy Eigenstate.
      dimensions: M
      default_range: ≈ 17 MeV
  measurement:
    procedures:
      - name: Lepton g-2 Global Fit
        outline: |
          Perform a global fit to precision measurements of the electron and muon anomalous magnetic moments (g-2). A loop contribution from a new scalar particle (Γ_H) with lepton-flavor-dependent couplings is included in the Standard Model prediction. The particle's mass (m_H) and couplings are varied to minimize the χ² deviation from experimental data.
        expected_signals: [A statistical preference for a new particle with m_H ≈ 17 MeV, A specific non-universal coupling pattern to e, μ, τ.]
        pitfalls: [Signal may be degenerate with other new physics contributions, Theoretical uncertainties in hadronic contributions to g-2 can obscure the signal.]
      - name: Missing Mass Search in e⁺e⁻ Collisions
        outline: |
          Search for processes like e⁺e⁻ → μ⁺μ⁻ + invisible or e⁺e⁻ → γ + invisible at low-energy colliders (e.g., Belle II, BESIII). Reconstruct the four-momentum of the invisible system. A signal for Γ_H production would appear as a peak in the missing mass spectrum.
        expected_signals: [A resonance in the missing mass distribution at m_inv ≈ 17 MeV.]
        pitfalls: [Low production cross-section, Significant backgrounds from neutrino-producing processes.]
context_windows:
  - module: MATH-021
    excerpt: |
      Particle (UV/leptonic): XXP‑015 → a heavy Γ quantum m_H ≈ 17 MeV fits lepton g−2 portal effects.
      Cosmology (IR/halos): COSMO‑Γ requires galaxy‑scale coherence typically modelled by an ultralight field m_L ∼ 10^−22 eV *or* an equivalent long‑wavelength collective mode.
      Goal: show that (i) both phenomena arise from a single Γ sector...
  - module: MATH-021
    excerpt: |
      Mechanism B — Clockwork/Alignment in a Multi‑Γ Chain (Two Eigenstates from One Sector)
      Hypothesis B2. Heavy eigenstate Γ_H couples to leptons (g−2 portal) with O(1) mixing; light eigenstate Γ_L is exponentially light and weakly coupled, sourcing cosmology.
poetic_connections:
  motifs: [heavy anchor, visible twin, leptonic portal, clockwork's end]
  evocative_lines:
    - "a heavy Γ quantum m_H ≈ 17 MeV"
    - "Heavy eigenstate Γ_H couples to leptons"
  association_matrix:
    - [ "Light Eigenstate (Γ_L)", 0.9 ]
    - [ "Lepton Portal", 0.8 ]
    - [ "Clockwork", 0.7 ]
formal_mappings:
  candidates:
    - target: Light scalar mediator
      domain: EFT
      mapping_kind: mathematical
      equation_hint: |
        L_int = g_l Γ_H l̄l
      justification: |
        Phenomenologically, the role of Γ_H in explaining lepton g-2 anomalies is captured by a generic, light scalar field that couples directly to Standard Model leptons via a Yukawa-type interaction. This provides the most direct and model-independent description of its laboratory signatures.
      references:
        - title: New Physics Contributions to the Muon Anomalous Magnetic Moment
          where: Review of Particle Physics
          date: 2024-08-01
      confidence: 0.9
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "A particle state Γ_H with mass m_H ≈ 17 MeV exists and couples to leptons."
      domain: experiment
      falsifier: "Null results from direct searches (e.g., missing mass) and indirect fits (g-2) that conclusively exclude this mass and its required coupling strengths."
      status: proposed
      links: [XXP-015]
    - statement: "If Mechanism B is correct, the couplings of Γ_H to e, μ, and τ follow a specific, non-universal pattern predicted by the clockwork eigenvector structure."
      domain: phenomenology
      falsifier: "Precision measurement of the Γ_H coupling ratios that are inconsistent with the clockwork predictions, for any valid choice of (q,N)."
      status: proposed
      links: [MATH-021]
    - statement: "If Mechanism C is correct, Γ_H does not exist as a stable or long-lived particle in the present-day universe."
      domain: experiment
      falsifier: "The definitive discovery of a stable particle at m_H ≈ 17 MeV with the expected properties."
      status: proposed
      links: [MATH-021]
naming_notes:
  collisions: [The symbol Γ is commonly used for the Gamma function in mathematics and for decay widths in particle physics. The subscript H is crucial for disambiguation.]
  disambiguation: |
    Distinguish Γ_H, the massive particle state (≈17 MeV), from its potential partner, the Light Eigenstate Γ_L (≈10⁻²² eV), which governs cosmology. Within the framework, Γ refers to the entire sector, while Γ_H and Γ_L refer to specific mass eigenstates.
crosslinks:
  near_synonyms: []
  antonyms: [LIGHT_EIGENSTATE]
  prerequisites: [MATH-018, XXP-015]
  downstream_effects: [SECT-Γ-A, SECT-Γ-B, SECT-Γ-C, COSMO-Γ-CMB]
license: CC-BY-SA-4.0
---

# Heavy Eigenstate (Γ_H)

## Canonical (Pirouette)
The massive particle state emerging from the Γ sector, denoted Γ_H, with a mass m_H anchored by lepton portal effects at ≈ 17 MeV. Its nature depends on the underlying sector architecture:
- In Superfluid models (Mechanism A), it is the fundamental quantum of the cosmic condensate.
- In Clockwork models (Mechanism B), it is the heaviest mass eigenstate of a coupled scalar chain.
- In Cascade models (Mechanism C), it is an early-universe metastable state that has since decayed.

## EFT-First Summary
The Heavy Eigenstate, Γ_H, is a proposed new particle whose experimental signatures are best described in Effective Field Theory as a **light scalar mediator**. With a mass of approximately 17 MeV, it interacts with Standard Model leptons (electrons, muons) via a direct coupling, contributing to their anomalous magnetic moments (g-2). This interaction is the primary anchor for its existence and mass, providing a concrete experimental target for both precision measurements and direct searches at low-energy colliders.

## Glossary Links
- See also: [Light Eigenstate (Γ_L)](<link-to-light-eigenstate>), [Clockwork Mechanism](<link-to-clockwork>)