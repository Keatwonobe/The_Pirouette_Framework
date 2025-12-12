---
term: "Clockwork Mechanism"
canonical_id: "CLOCKWORK_MECHANISM"
symbol: ""
aliases: [Alignment]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-021"]
---

---
term: Clockwork Mechanism
canonical_id: CLOCKWORK_MECHANISM
symbol: 
aliases: [Alignment]
parents: [MATH-021]
children: [SECT-Γ-A, SECT-Γ-B, SECT-Γ-C]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-021
      lines: "Section 'Mechanism B'"
      snippet: |
        L = Σ_i ½(∂ϕ_i)^2 − ½ m^2(ϕ_i − q ϕ_{i+1})^2 − V_tail(ϕ_N)
        Diagonalize M^2 → eigenvalues {m_H ≈ m, …, m_L ≈ m/q^{N}}; eigenvectors fix couplings.
  editors: [GPT-4 (Pirouette Dictionary Agent)]
  review_log: []
triad:
  art: |
    A chain of identical gears, each a tiny bit faster than the last, where the gentle turn of the first becomes an imperceptible crawl at the end. The hierarchy is not a trick of scale, but the architecture of connection itself.
  law: |
    A sector of `N` scalar fields with nearest-neighbor mass-mixing `m^2(ϕ_i - q ϕ_{i+1})^2` generates one heavy eigenstate with mass `m_H ≈ m` and one exponentially light eigenstate with mass `m_L ≈ m/q^N`. The light state's coupling to the first field (the SM portal) is likewise suppressed by `~q^(1-N)`.
  philosophy: |
    To demonstrate that vast hierarchies are not signs of fine-tuning but can be natural, calculable outcomes of simple, repeated symmetries. An exponential gap is achieved through linear, local steps, resolving apparent tension without introducing new fundamental scales.
pirouette_definition: |
  A candidate mechanism for resolving the Γ Mass Tension by postulating that the Γ sector consists of `N` scalar fields, `ϕ_i`, with a nearest-neighbor mass-mixing term of the form `m^2(ϕ_i - q ϕ_{i+1})^2`. This structure, arising from a discrete shift symmetry, generates a mass spectrum with one heavy eigenstate (Γ_H) of mass `~m` and one exponentially light eigenstate (Γ_L) of mass `~m/q^N`. Γ_H couples to the Standard Model with `O(1)` strength to explain lepton-scale phenomena, while Γ_L is naturally ultralight and very weakly coupled, sourcing cosmological effects.
operational_definition:
  units: Key parameters `N` and `q` are dimensionless.
  symbol_table:
    - name: N
      meaning: Number of scalar fields in the chain.
      dimensions: dimensionless
      default_range: Integer > 1, typically O(10-100)
    - name: q
      meaning: Inter-field coupling ratio.
      dimensions: dimensionless
      default_range: Real > 1, typically O(2-10)
    - name: m
      meaning: Intrinsic mass scale of the sector.
      dimensions: M
      default_range: ~17 MeV (anchored to m_H)
    - name: m_H
      meaning: Mass of the heavy eigenstate.
      dimensions: M
      default_range: ~17 MeV
    - name: m_L
      meaning: Mass of the light eigenstate.
      dimensions: M
      default_range: ~10⁻²² eV
  measurement:
    procedures:
      - name: Cosmological & Precision Constraint Analysis
        outline: |
          Simultaneously fit cosmological and precision laboratory data. Use CMB acoustic phase shifts and large-scale structure to constrain the `(q,N)` parameter space via the light eigenstate `Γ_L`. Independently, use precision measurements (e.g., lepton g-2, EDMs) to constrain the heavy eigenstate `Γ_H` and its loop-level interference. A consistent solution for `(m, q, N)` across both domains supports the mechanism.
        expected_signals: [Small residual in CMB acoustic phase shifts, Specific coupling ratios g_e:g_μ:g_τ for Γ_H, Equivalence Principle violation signal suppressed by q⁻ᴺ]
        pitfalls: [Degeneracies with standard cosmological parameters, Loop-level effects in lab tests below current sensitivity]
context_windows:
  - module: MATH-021
    excerpt: |
      Mechanism B — Clockwork/Alignment in a Multi‑Γ Chain (Two Eigenstates from One Sector)
      Hypothesis B1. Γ is a *sector* of N coupled scalars with nearest‑neighbor couplings producing exponentially hierarchical eigenmasses (clockwork/alignment).
      Hypothesis B2. Heavy eigenstate Γ_H couples to leptons (g−2 portal) with O(1) mixing; light eigenstate Γ_L is exponentially light and weakly coupled, sourcing cosmology.
  - module: MATH-021
    excerpt: |
      Decision Tree (Discriminants)
      D1. **CMB acoustic phases**: clockwork (B) predicts small residual phase shifts...
      D2. **Halo substructure**: ... (B) yields standard fuzzy‑like suppression with sharp m_L...
      D3. **Lab/precision**: (B) implies definite coupling patterns testable in g−2/EDM/global EW fits...
poetic_connections:
  motifs: [hierarchy, chain, gear-train, echo, alignment, suppression]
  evocative_lines:
    - "exponentially hierarchical eigenmasses (clockwork/alignment)"
    - "natural evasion with a calculable residual"
  association_matrix:
    - [ "MASS_TENSION", 0.9 ]
    - [ "DISCRETE_SYMMETRY", 0.8 ]
    - [ "COMPOSITE_SUPERFLUID", 0.2 ]
formal_mappings:
  candidates:
    - target: Clockwork Mechanism / Linear Dilaton
      domain: EFT
      mapping_kind: mathematical
      equation_hint: |
        L ⊃ Σ m² |ϕ_i - q ϕ_{i+1}|²
      justification: |
        The Pirouette formulation is a direct application of the clockwork mechanism from the particle physics literature, used to generate exponential hierarchies between mass scales. The chain of scalar fields with nearest-neighbor interactions is the defining feature, leading to a "zeroth" mode whose mass and couplings are exponentially suppressed.
      references:
        - title: A Clockwork Axion
          where: arXiv:1511.01827
          date: 2015-11-04
        - title: A Clockwork Theory
          where: arXiv:1610.07962
          date: 2016-10-25
      confidence: 0.95
  adopted:
    - target: Clockwork Mechanism (BSM)
      rationale: "The mechanism in MATH-021 is mathematically and conceptually identical to the 'Clockwork' construction in the BSM literature, providing a clear bridge to existing theoretical work."
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The Γ mass tension is resolved by a clockwork sector with a single set of parameters (m, q, N)."
      domain: theory
      falsifier: "No single set of (m, q, N) can simultaneously fit both cosmological data (CMB phases, halo structure) and laboratory constraints (g-2, fifth-force tests)."
      status: proposed
      links: [MATH-021, COSMO-Γ-CMB, XXP-015]
    - statement: "The light cosmological field Γ_L has couplings to matter suppressed by ~q⁻ᴺ relative to the heavy field Γ_H."
      domain: phenomenology
      falsifier: "Equivalence Principle tests observe a fifth force with a strength incompatible with the (q, N) values inferred from cosmology."
      status: proposed
      links: [MATH-021]
naming_notes:
  collisions: [The term "clockwork" is used in systems biology (circadian rhythms), but confusion is contextually unlikely.]
  disambiguation: |
    Distinguish from the 'Composite Superfluid' (Mechanism A), which generates a light *collective mode* (a phonon) from a single heavy particle species, rather than a fundamental light *eigenstate*. The clockwork mechanism predicts a discrete, sharp mass `m_L`, whereas the superfluid's effective mass can be environment-dependent.
crosslinks:
  near_synonyms: [ALIGNMENT_MECHANISM]
  antonyms: [COMPOSITE_SUPERFLUID, PHASE_CASCADE]
  prerequisites: [GAMMA_MASS_TENSION]
  downstream_effects: [FUZZY_DARK_MATTER, FIFTH_FORCE_SIGNATURES]
license: CC-BY-SA-4.0
---