---
term: "Coincidence problem"
canonical_id: "COINCIDENCE_PROBLEM"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["COSMO-003"]
---

---
term: Coincidence problem
canonical_id: COINCIDENCE_PROBLEM
symbol: 
aliases: ["Cosmic Coincidence Problem", "Why-now Problem"]
parents: ["COSMO-003"]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: COSMO-003
      lines: "Section 5"
      snippet: |
        Goal: explain ρ_DM ~ ρ_DE today without tuning.
        Mechanism: **tracker/attractor tail** appended to quadratic core of V(Γ), consistent with D2 (analytic, local, scale-covariant).
  editors: ["system-agent"]
  review_log: []
triad:
  art: |
    Two vast and different oceans of energy, one thinning rapidly and the other nearly constant, have mysteriously reached the same depth just as we arrived to witness them.
  law: |
    The ratio of the observed dark energy density to the dark matter density, ρ_DE / ρ_m, is of order unity (≈ 7/3) at the present cosmological epoch (z=0), despite the two components evolving at vastly different rates for most of cosmic history.
  philosophy: |
    This temporal alignment challenges the Copernican principle, suggesting either an incredible coincidence tied to our existence or a deeper, underlying dynamical law that forces the two densities to converge. The problem's resolution distinguishes between fine-tuning and physical necessity.
pirouette_definition: |
  The cosmological puzzle of why the energy densities of dark matter (ρ_m) and dark energy (ρ_DE), which scale differently with cosmic expansion (ρ_m ∝ a⁻³, ρ_DE ≈ const), are of the same order of magnitude *today*. The Pirouette Framework proposes a dynamical solution where a single scalar field (Γ) behaves as matter at early times and transitions to a dark energy-like state at late times due to a tracker/attractor mechanism in its potential, V(Γ), thus making the near-equality an inevitable outcome of cosmic evolution rather than an accident of timing.
operational_definition:
  units: Dimensionless
  symbol_table:
    - name: ρ_DE
      meaning: Energy density of dark energy
      dimensions: M L⁻¹ T⁻²
      default_range: contextual
    - name: ρ_m
      meaning: Energy density of matter (dark + baryonic)
      dimensions: M L⁻¹ T⁻²
      default_range: contextual
    - name: Ω_i
      meaning: Density parameter of species i, defined as ρ_i / ρ_crit
      dimensions: dimensionless
      default_range: 0 to 1
  measurement:
    procedures:
      - name: Cosmological Parameter Inference
        outline: |
          The values for Ω_m and Ω_DE (and thus their ratio) are inferred by fitting a cosmological model (e.g., ΛCDM) to a combination of cosmological observations. Primary probes include the Cosmic Microwave Background (CMB) power spectra, the distance-redshift relation from Type Ia Supernovae, and Baryon Acoustic Oscillation (BAO) measurements from galaxy surveys. The convergence of these independent probes on values where Ω_DE ≈ 0.7 and Ω_m ≈ 0.3 establishes the problem.
        expected_signals: ["CMB temperature and polarization anisotropy spectra", "Supernova magnitude-redshift curve", "Characteristic scale in the galaxy correlation function"]
        pitfalls: ["Systematic errors in any single observational probe", "Incorrect assumptions about the underlying cosmological model (e.g., assuming w=-1 for dark energy)", "Evolution of astrophysical sources mimicking cosmic acceleration"]
context_windows:
  - module: COSMO-003
    excerpt: |
      Goal: explain ρ_DM ~ ρ_DE today without tuning.
      Mechanism: **tracker/attractor tail** appended to quadratic core of V(Γ), consistent with D2 (analytic, local, scale-covariant). Two options: (1) Exponential tail (analytic)... (2) Cosine tail (shift-symmetry remnant)... Coincidence arises because slow-roll only turns on when the oscillation amplitude decays into the tail—set by μ, not by arbitrary time.
  - module: COSMO-003
    excerpt: |
      Falsification: if fitting CMB+BAO+SNe requires independent CDM and DE fluids once parameters are frozen, the unification fails.
poetic_connections:
  motifs: ["cosmic choreography", "attractor", "temporal alignment", "why now?"]
  evocative_lines:
    - "explain ρ_DM ~ ρ_DE today without tuning"
    - "Coincidence arises because slow-roll only turns on when the oscillation amplitude decays into the tail"
  association_matrix:
    - [ "PRESSURON_FIELD_GAMMA", 0.9 ]
    - [ "D2_SYMMETRY", 0.7 ]
    - [ "ONE_SHOT_ANCHOR", 0.5 ]
formal_mappings:
  candidates:
    - target: "Cosmic Coincidence Problem"
      domain: GR
      mapping_kind: conceptual
      equation_hint: |
        Ω_DE(z=0) / Ω_m(z=0) ≈ 7/3
      justification: |
        This is the standard name in scientific literature for the puzzle that the energy densities of matter and dark energy are comparable today, despite their different evolutionary histories. It questions why we happen to live in the specific, brief epoch where this is true.
      references:
        - title: The Cosmological Constant and the Coincidence Problem
          where: P.J. Steinhardt, in *Critical Problems in Physics*, Princeton University Press, 1997
          date: 1997-01-01
      confidence: 1.0
  adopted:
    - target: "Cosmic Coincidence Problem"
      rationale: Direct, one-to-one correspondence with the established term in the field.
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "The observed O(1) ratio of ρ_DE/ρ_m is not a temporal coincidence but an inevitable result of the tracker/attractor dynamics of a unified Γ field."
      domain: phenomenology
      falsifier: "If a global fit of the Γ model to cosmological data (CMB, BAO, SNe) yields a significantly worse fit (e.g., high ΔAIC) than a model with independent Dark Matter and Dark Energy components, or requires fine-tuning of its potential parameters beyond the D3 one-shot anchor."
      status: proposed
      links: ["COSMO-003"]
naming_notes:
  collisions: []
  disambiguation: |
    This term refers specifically to the temporal alignment of *energy densities* at z=0. It should not be confused with other cosmological puzzles like the flatness problem or the horizon problem, though all point towards significant gaps in the standard cosmological model.
crosslinks:
  near_synonyms: ["WHY_NOW_PROBLEM"]
  antonyms: ["FINE_TUNING_ARGUMENT"]
  prerequisites: ["DARK_ENERGY", "DARK_MATTER"]
  downstream_effects: ["GAMMA_FIELD_POTENTIAL"]
license: CC-BY-SA-4.0
---

# Coincidence problem

## Canonical (Pirouette)
The cosmological puzzle of why the energy densities of dark matter (ρ_m) and dark energy (ρ_DE), which scale differently with cosmic expansion (ρ_m ∝ a⁻³, ρ_DE ≈ const), are of the same order of magnitude *today*. The Pirouette Framework proposes a dynamical solution where a single scalar field (Γ) behaves as matter at early times and transitions to a dark energy-like state at late times due to a tracker/attractor mechanism in its potential, V(Γ), thus making the near-equality an inevitable outcome of cosmic evolution rather than an accident of timing.

## EFT-First Summary
The Coincidence Problem is a well-established puzzle in standard cosmology (General Relativity). It notes that the energy density of matter, which dilutes as the universe expands, is currently of the same order of magnitude as the energy density of the cosmological constant (or dark energy), which does not dilute. This implies we are living in a special epoch; in the past, matter dominated completely, and in the future, dark energy will. Models that attempt to solve this, such as quintessence or the Pirouette Γ-field, often postulate a dynamical dark energy component whose evolution is linked to the background matter density, making the present-day near-equality a natural outcome.

## Glossary Links
- See also: Dark Energy, Dark Matter, Pressuron (Γ) Field, Fine-tuning