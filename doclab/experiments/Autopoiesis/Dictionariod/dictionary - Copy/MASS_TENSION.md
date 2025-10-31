---
term: "Mass Tension"
canonical_id: "MASS_TENSION"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-021"]
---

---
term: Mass Tension
canonical_id: MASS_TENSION
symbol: m_H / m_L
aliases: ["Γ Mass Tension"]
parents: [MATH-021, XXP-015, COSMO-Γ-000]
children: [SECT-Γ-A, SECT-Γ-B, SECT-Γ-C]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-021
      lines: "Summary of the Tension"
      snippet: |
        Summary of the Tension
        • Particle (UV/leptonic): XXP‑015 → a heavy Γ quantum m_H ≈ 17 MeV fits lepton g−2 portal effects.
        • Cosmology (IR/halos): COSMO‑Γ requires galaxy‑scale coherence typically modelled by an ultralight field m_L ∼ 10^−22 eV *or* an equivalent long‑wavelength collective mode.
        • Goal: show that (i) both phenomena arise from a single Γ sector, and (ii) the light mode governing structure is a *derived* eigenmode/collective excitation, not an ad‑hoc second particle with tuned mass.
  editors: ["Agent: Dictionary Scribe"]
  review_log: []
triad:
  art: |
    A single seed sprouts two trees: one a mountain-crushing titan, the other a whisper that shapes galaxies. The tension lies in proving they share the same root.
  law: |
    The Γ sector must simultaneously account for a lepton-coupled mass scale m_H ≈ 17 MeV and a cosmological coherence scale m_L ≈ 10^−22 eV through a single, falsifiable mechanism (collective mode, eigenstate hierarchy, or phase transition), without introducing independent ad-hoc mass scales.
  philosophy: |
    The Mass Tension serves as a primary driver for developing predictive, unified sector models under MATH-018. Resolving it is not merely a fine-tuning problem, but a test of the framework's ability to generate large hierarchies from simple principles rather than by postulation.
pirouette_definition: |
  The 29-order-of-magnitude discrepancy between the directly-coupled Γ particle mass (m_H), inferred from leptonic interactions, and the ultralight effective mass (m_L) required to explain galaxy-scale cosmological structures. The tension is the theoretical challenge of deriving both scales from a single, unified Γ sector via a concrete physical mechanism, as mandated by framework predictivity rules. This requires showing that the light cosmological mode is a derived, not fundamental, property of the sector.
operational_definition:
  units: Dimensionless ratio. Individual masses (m_H, m_L) are in eV/c².
  symbol_table:
    - name: m_H
      meaning: Mass of the heavy Γ eigenstate or microscopic quantum.
      dimensions: M
      default_range: ≈ 17 MeV/c²
    - name: m_L
      meaning: Effective mass of the light Γ eigenstate or collective mode sourcing cosmological structure.
      dimensions: M
      default_range: ≈ 10⁻²² eV/c²
  measurement:
    procedures:
      - name: Lepton Portal Inference (m_H)
        outline: |
          Analyze precision measurements of lepton anomalous magnetic moments (g-2) and other electroweak observables for deviations consistent with a new particle portal. Fit the deviations to determine the mass (m_H) and coupling of the mediating Γ particle.
        expected_signals: ["Excess in muon/electron g-2", "Correlated loop-level effects in precision EW fits"]
        pitfalls: ["Signal mimicked by other new physics", "Poorly constrained coupling parameters"]
      - name: Cosmological Structure Inference (m_L)
        outline: |
          Analyze galaxy halo profiles, Lyman-alpha forest data, and CMB lensing/ISW effects. Fit these observations with models of structure formation seeded by an ultralight field to constrain its de Broglie wavelength and thus its effective mass (m_L).
        expected_signals: ["Cored halo profiles instead of cusps", "Suppression of small-scale matter power spectrum"]
        pitfalls: ["Degeneracies with baryonic feedback effects", "Model dependence of inference"]
      - name: Mechanism Discrimination
        outline: |
          Perform a multi-probe analysis comparing predictions of the three candidate resolution mechanisms (A: Superfluid, B: Clockwork, C: Cascade) against a combined dataset including CMB acoustic phases, halo substructure statistics, and precision lab measurements.
        expected_signals: ["CMB phase shifts (B)", "Specific vortex spectra in halos (A)", "Sharp power spectrum cutoff (C)"]
        pitfalls: ["Low signal-to-noise for discriminants", "Mechanisms may have overlapping predictions in some regimes"]
context_windows:
  - module: MATH-021
    excerpt: |
      Formalize and resolve the 29‑order‑of‑magnitude 'mass tension' between the lepton‑scale Pressuron mass (m_H ≈ 17 MeV from XXP‑015) and the cosmology‑scale requirement (m_L ≈ 10^−22 eV in fuzzy‑DM language) without violating MATH‑018 predictivity rules. Provide candidate mechanisms, minimal maths, falsifiable signatures, and code hooks.
  - module: MATH-021
    excerpt: |
      Decision Tree (Discriminants)
      D1. **CMB acoustic phases**: clockwork (B) predicts small residual phase shifts; superfluid (A) and cascade (C) give different lensing amplitudes.
      D2. **Halo substructure**: (A) yields phonon‑pressure cores with vortex spectra; (B) yields standard fuzzy‑like suppression with sharp m_L; (C) produces a step‑like cutoff.
      D3. **Lab/precision**: (B) implies definite coupling patterns testable in g−2/EDM/global EW fits; (A) implies medium‑dependent optical signatures; (C) implies nothing current‑day but strong cosmological transition marks.
poetic_connections:
  motifs: [hierarchy, emergence, unification, scale-separation]
  evocative_lines:
    - "the light mode governing structure is a *derived* eigenmode/collective excitation, not an ad-hoc second particle with tuned mass."
    - "reproduces Σ_0 locus...without fundamental self-scattering."
  association_matrix:
    - [ "HIERARCHY_PROBLEM", 0.9 ]
    - [ "SECTOR_UNIFICATION", 0.8 ]
    - [ "EMERGENCE", 0.7 ]
    - [ "FINE_TUNING", 0.3 ]
formal_mappings:
  candidates:
    - target: Fuzzy Dark Matter (FDM) / ultralight axion mass
      domain: Cosmology
      mapping_kind: operational
      equation_hint: "λ_deBroglie = h / (m_L v) ≈ kpc"
      justification: |
        The required cosmological mass scale m_L ≈ 10⁻²² eV is functionally identical to the mass of ultralight axions or FDM candidates proposed to solve small-scale structure problems like the core-cusp issue. Pirouette's m_L is an effective mass derived from a sector, not necessarily a fundamental particle mass.
      confidence: 0.9
    - target: P(X) theory / k-essence / superfluid EFT
      domain: EFT
      mapping_kind: mathematical
      equation_hint: "L_eff = P(X), where X is the kinetic/potential term for a condensate."
      justification: |
        Mechanism A (Composite Superfluid) directly maps the low-energy dynamics of the Γ condensate to a P(X) effective field theory. The emergent phonons with effective mass m_eff behave as the cosmological dark matter, with sound speed c_s set by dP/dρ.
      confidence: 1.0
    - target: Clockwork Mechanism / Kim-Nilles-Peloso (KNP) alignment
      domain: EFT
      mapping_kind: mathematical
      equation_hint: "m_L ≈ m / q^N"
      justification: |
        Mechanism B (Clockwork/Alignment) uses a chain of N scalar fields with nearest-neighbor couplings to generate an exponentially suppressed mass eigenvalue. This is a direct application of the clockwork mechanism, commonly used in axion model-building to generate large hierarchies from O(1) parameters.
      confidence: 1.0
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The Mass Tension is resolvable via a composite superfluid mechanism where galaxy cores are supported by phonon pressure."
      domain: phenomenology
      falsifier: "Observations of galaxy halo profiles and merger dynamics are inconsistent with the predictions of a P(X) superfluid model, such as the Σ_0 locus slope, and are instead better fit by a simple ultralight particle potential or CDM."
      status: proposed
      links: [MATH-021, SECT-Γ-A, COSMO-Γ-MERGE]
    - statement: "The Mass Tension is resolvable via a clockwork mechanism, which predicts specific, non-universal coupling patterns of the heavy (Γ_H) and light (Γ_L) mass eigenstates to Standard Model leptons."
      domain: experiment
      falsifier: "Precision measurements of lepton g-2, EDMs, or global electroweak fits fail to find the predicted coupling patterns, or explicitly rule out the parameter space for (q,N) that also satisfies cosmological constraints."
      status: proposed
      links: [MATH-021, SECT-Γ-B]
    - statement: "The Mass Tension is resolvable via a late-time phase transition, which imprints a sharp, step-like feature in the matter power spectrum at a scale k_c set by the transition epoch."
      domain: phenomenology
      falsifier: "Large-scale structure surveys (e.g., galaxy surveys, Lyman-alpha forest) find a smooth power spectrum and rule out the existence of such a feature, or corresponding ISW/lensing signals in the CMB are absent."
      status: proposed
      links: [MATH-021, SECT-Γ-C, COSMO-Γ-CMB]
    - statement: "The Γ-unification claim, i.e., that a single sector produces both m_H and m_L, is valid."
      domain: theory
      falsifier: "If no single proposed mechanism (A, B, or C) survives a combined multi-probe analysis of cosmological, astrophysical, and laboratory data, the unification hypothesis is withdrawn."
      status: proposed
      links: [MATH-021]
naming_notes:
  collisions: []
  disambiguation: |
    Not to be confused with the electroweak hierarchy problem (Higgs mass vs. Planck mass), though it is conceptually similar in involving a large separation of scales. The Mass Tension is specific to the Γ sector and its dual role in particle physics and cosmology. It refers to a concrete 29-order-of-magnitude gap between two observationally-inferred scales, not a theoretical naturalness problem.
crosslinks:
  near_synonyms: []
  antonyms: [SECTOR_DECOUPLING]
  prerequisites: [GAMMA_PARTICLE, SECTOR_ARCHITECTURE]
  downstream_effects: [HALO_CORE_PROFILE, CMB_ACOUSTIC_PHASES]
license: CC-BY-SA-4.0
---

# Mass Tension

## Canonical (Pirouette)
The 29-order-of-magnitude discrepancy between the directly-coupled Γ particle mass (m_H), inferred from leptonic interactions, and the ultralight effective mass (m_L) required to explain galaxy-scale cosmological structures. The tension is the theoretical challenge of deriving both scales from a single, unified Γ sector via a concrete physical mechanism, as mandated by framework predictivity rules. This requires showing that the light cosmological mode is a derived, not fundamental, property of the sector.

## EFT-First Summary
The Mass Tension formalizes the challenge of explaining two disparate phenomena with one physical field sector. On one hand, anomalies in lepton physics suggest a new particle (Γ) with a mass `m_H ≈ 17 MeV`. On the other, cosmological structure on galactic scales is well-described by an ultralight, wave-like dark matter candidate with mass `m_L ≈ 10⁻²² eV`, often called Fuzzy Dark Matter. The Pirouette framework proposes to resolve this `m_H / m_L ≈ 10²⁹` discrepancy by treating the light mode not as a new fundamental particle, but as an emergent property of the Γ sector. Candidate mechanisms map directly to known EFTs: a self-interacting superfluid described by a P(X) theory, or an exponentially light eigenstate generated by a clockwork/alignment mechanism.

## Glossary Links
- See also: [GAMMA_PARTICLE](<placeholder>), [SECTOR_ARCHITECTURE](<placeholder>), [HIERARCHY_PROBLEM](<placeholder>)