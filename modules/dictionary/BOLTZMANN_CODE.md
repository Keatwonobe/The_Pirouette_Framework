---
term: "Boltzmann Code"
canonical_id: "BOLTZMANN_CODE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["COSMO-Γ-001_the_early_universe"]
---

---
term: Boltzmann Code
canonical_id: BOLTZMANN_CODE
symbol: N/A
aliases: [Cosmological Evolution Code, CLASS, CAMB]
parents: [COSMO-Γ-001_the_early_universe, COSMO-Γ-CMB]
children: [COSMO-Γ-HALO]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: COSMO-Γ-001_the_early_universe
      lines: "§5 · Boltzmann Hooks and Artifacts"
      snippet: |
        * **Species:** `gammat` with params `{m_Gamma, lambda4, V_tail_parameters, Gamma_ini, dGamma_ini}`.
  editors: [Pirouette-Agent-v2]
  review_log: []
triad:
  art: |
    The numerical orchestra that performs the universe's score, translating the fundamental dynamics of fields into the symphony of observable structures, from the first acoustic peaks to the final cosmic silence.
  law: |
    A Boltzmann code integrates the coupled, linearized Einstein-Boltzmann equations for a given cosmological model to predict the statistical properties of cosmic observables (e.g., CMB/matter power spectra). A valid implementation must recover ΛCDM predictions to within 0.1% in appropriate limits and demonstrate ≤0.2% numerical stability across solver thresholds.
  philosophy: |
    To serve as the definitive bridge from theoretical postulate to empirical test, enforcing the discipline of falsifiability. It ensures that a model is not merely a set of equations, but a concrete, predictive machine whose output can be directly compared to astronomical data.
pirouette_definition: |
  The numerical framework used to compute the evolution of cosmological perturbations (metric and fluid) from initial conditions to the present day. In the Γ-Cosmology context, it is the specific CLASS/CAMB branch that incorporates the Pressuron field's dynamics, including its stiff pre-oscillatory phase, averaged oscillatory (CDM-like) phase, and late-time slow-roll (DE-like) tail, to generate falsifiable predictions for CMB, BBN, and LSS observables from a single, unified physical model.
operational_definition:
  units: N/A (computational framework)
  symbol_table:
    - name: m_Γ
      meaning: Mass of the Pressuron field, sets the onset of oscillation.
      dimensions: M
      default_range: contextual
    - name: V_tail_parameters
      meaning: Parameters defining the late-time, slow-roll potential.
      dimensions: contextual
      default_range: contextual
    - name: Γ_ini, dΓ_ini
      meaning: Initial field value and velocity (misalignment conditions).
      dimensions: contextual
      default_range: contextual
    - name: ΔN_eff
      meaning: Effective number of relativistic species; a key BBN/CMB constraint.
      dimensions: dimensionless
      default_range: [-0.5, 0.5]
  measurement:
    procedures:
      - name: Generate Cosmological Observables
        outline: |
          1. Define a model and its parameters in a `freeze_manifest.yaml`.
          2. Integrate the background equations of motion from the radiation era to z=0.
          3. Evolve the full system of linearized Einstein-Boltzmann equations for all species.
          4. Compute and output derived quantities like CMB angular power spectra and the matter power spectrum.
        expected_signals: [CMB TT/TE/EE power spectra, matter power spectrum P(k), fσ₈(z), predicted ΔN_eff]
        pitfalls: [Numerical instability at solver switch points (e.g., stiff to averaged fluid), violation of frozen parameter constraints (re-tuning), improper limit-checking against ΛCDM.]
context_windows:
  # Short, trimmed context quotes harvested from modules (3–6 sentences each).
  - module: COSMO-Γ-001_the_early_universe
    excerpt: |
      Formalize the thermal history of the Γ field from inflationary initial conditions through BBN and recombination, specify how its background and perturbations enter a Boltzmann code (CLASS/CAMB branch), and define falsifiable targets in ΔN_eff, CMB spectra, and late-time equation-of-state evolution.
  - module: COSMO-Γ-001_the_early_universe
    excerpt: |
      The early universe sets the tempo: Γ begins frozen, takes its first breath when (H \sim m_\Gamma), and then beats like a hidden metronome that matter can’t hear—until the tail in (V(\Gamma)) slows the drum at late times, whispering as dark energy. These stages are not stitched together; they are one score, played on a single instrument.
poetic_connections:
  # Lightweight "word-association graph" and sticky lines.
  motifs: [numerical orchestra, cosmic metronome, predictive machine, score-to-symphony]
  evocative_lines:
    - "beats like a hidden metronome that matter can’t hear..."
    - "one score, played on a single instrument."
  association_matrix:
    # symmetric or directed; weights in [0,1]
    - [ "PRESSURON_FIELD", 0.9 ]
    - [ "FALSIFIABLE_TARGET", 0.8 ]
    - [ "FREEZE_MANIFEST", 0.7 ]
formal_mappings:
  # Candidate alignments to EFT/SM/CM/GR terms, each with justification and refs.
  candidates: []
  adopted:
    - target: CAMB (Code for Anisotropies in the Microwave Background) / CLASS (Cosmic Linear Anisotropy Solving System)
      domain: Cosmology/Computational Physics
      mapping_kind: operational
      equation_hint: N/A
      justification: |
        The Pirouette Boltzmann Code is specified as a direct branch of the public CLASS or CAMB codes. These are the community-standard tools for solving the linearized Einstein-Boltzmann equations to compute cosmological observables. The Pirouette implementation extends these codes with modules for Γ-field dynamics.
      references:
        - title: The Cosmic Linear Anisotropy Solving System (CLASS)
          where: JCAP 1107 (2011) 034
          date: 2011-07-20
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "The Boltzmann code, when run with a single frozen parameter set (`freeze_manifest.yaml`), must simultaneously produce CMB spectra consistent with Planck data (e.g., within the cosmic variance limit) and a ΔN_eff value consistent with BBN constraints."
      domain: phenomenology
      falsifier: "An empirical result where Planck and BBN data require statistically discrepant parameter regions for the Γ field, invalidating the 'one-shot anchor' unification principle."
      status: proposed
      links: [COSMO-Γ-001_the_early_universe, COSMO-Γ-CMB]
    - statement: "The code must recover ΛCDM predictions to ≤0.1% accuracy in the V_tail→0 and m_Γ/H→∞ limits."
      domain: theory
      falsifier: "A numerical result showing the Γ-field implementation fails this limit check, indicating a fault in the code logic or fluid-averaging approximation."
      status: proposed
      links: [COSMO-Γ-001_the_early_universe]
naming_notes:
  collisions: [Boltzmann's Equation]
  disambiguation: |
    Not to be confused with the foundational Boltzmann equation of statistical mechanics, though this is the core component being solved for each particle species. In this context, 'Boltzmann Code' refers to the entire numerical apparatus for cosmological perturbation theory, including the Einstein field equations and fluid dynamics.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [PRESSURON_FIELD, COSMOLOGICAL_PERTURBATION_THEORY]
  downstream_effects: [FALSIFIABLE_TARGET, COSMO-Γ-HALO]
license: CC-BY-SA-4.0
---