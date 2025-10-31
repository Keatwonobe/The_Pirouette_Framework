---
term: "Freeze Manifest"
canonical_id: "FREEZE_MANIFEST"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["COSMO-000"]
---

---
term: Freeze Manifest
canonical_id: FREEZE_MANIFEST
symbol: (none)
aliases: [anchor manifest, frozen parameters, reproducibility manifest]
parents: [COSMO-000]
children: [COSMO-Γ-HALO, COSMO-Γ-MERGE]
status: candidate
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: COSMO-000
      lines: "Section 3"
      snippet: |
        Emit a Freeze Manifest (YAML) with commit hash, anchor, U/T values, and seeds.
  editors: [system]
  review_log: []
triad:
  art: |
    A universe crystallized in code. Its initial conditions and constants of nature are etched into a permanent record, from which all subsequent history must deterministically flow.
  law: |
    A version-controlled, machine-readable artifact (typically YAML) that immutably binds a specific computational pipeline (via commit hash) to a complete set of anchored U-class and T-class parameters, including all necessary initial conditions and random seeds.
  philosophy: |
    To enforce the principle of one-shot anchoring (D3) and enable preregistered, out-of-sample predictions (P4). It serves as the non-negotiable contract between a theoretical model and its empirical test, eliminating post-hoc tuning and ensuring computational reproducibility.
pirouette_definition: |
  A version-controlled, machine-readable data artifact, typically in YAML format, that serves as the single source of truth for a reproducible scientific prediction. It is generated once following a one-shot anchor (D3) procedure. The manifest must contain: the specific software version (e.g., git commit hash), the chosen anchor parameter and its value, all derived U-class and T-class parameters, and all seeds for any stochastic processes. Any subsequent computational artifact (e.g., a power spectrum, a background evolution table) must reference the manifest that generated it.
operational_definition:
  units: N/A (data structure/file format)
  symbol_table:
    - name: anchor
      meaning: The single observational input and its value used to fix the theory's free parameters.
      dimensions: contextual
      default_range: e.g., `{name: Omega_m0, value: 0.315}`
    - name: commit
      meaning: The version control hash identifying the exact state of the computational source code.
      dimensions: dimensionless
      default_range: e.g., SHA-1 or SHA-256 hash
    - name: U_parameters
      meaning: The set of derived, universal (U-class) parameters for the theory.
      dimensions: contextual
      default_range: e.g., `{m_Gamma: 1.0e-27, lambda4: 0.0}`
    - name: seeds
      meaning: A list of seeds for all pseudo-random number generators used in the pipeline.
      dimensions: dimensionless
      default_range: list of integers
  measurement:
    procedures:
      - name: Manifest Generation
        outline: |
          1. Select a single, D3-compliant anchor observable (e.g., `Ω_m0`).
          2. Execute the anchoring pipeline on a clean version-controlled code checkout to derive all U-class parameters.
          3. Record the git commit hash, the anchor name and value, the derived parameters, and any PRNG seeds into a structured YAML file.
          4. Commit the manifest to the repository, linking it to the code version that generated it.
        expected_signals: [A valid YAML file compliant with the manifest schema.]
        pitfalls: [Using an uncommitted ("dirty") code state, omitting a required parameter, failing to record a random seed.]
context_windows:
  - module: COSMO-000
    excerpt: |
      Anchor choice (pick exactly one per D3): {Ω_m0, H0, or a_e in QED sector with proven bridge}. Once chosen, derive U-class parameter set {m_Γ, λ_4, …} via symmetry constraints and freeze. Emit a Freeze Manifest (YAML) with commit hash, anchor, U/T values, and seeds.
  - module: COSMO-000
    excerpt: |
      Parameter propagation from Freeze Manifest; no retuning.
      ...
      result_background.json
      {
      "H_z": [[z, H]],
      "commit": "<git>",
      "freeze_manifest": "path/to/manifest.yaml"
      }
poetic_connections:
  motifs: [immutability, anchor, genesis block, seed crystal, reproducibility]
  evocative_lines:
    - "One‑shot anchor used and frozen."
    - "Emit a Freeze Manifest (YAML) with commit hash, anchor, U/T values, and seeds."
  association_matrix:
    - [ "ONE_SHOT_ANCHOR", 0.9 ]
    - [ "PREREGISTERED_PREDICTION", 0.8 ]
    - [ "REPRODUCIBILITY", 1.0 ]
formal_mappings:
  candidates:
    - target: Dependency Lock File (e.g., `poetry.lock`, `package-lock.json`)
      domain: Software Engineering
      mapping_kind: operational
      equation_hint: (none)
      justification: |
        Like a dependency lock file, the Freeze Manifest locks the "dependencies" of a scientific prediction (parameters, code version) to ensure a specific, reproducible result. It extends the concept from software dependencies to include physical and numerical parameters.
      references: []
      confidence: 0.9
    - target: `params.yaml` / `dvc.lock`
      domain: MLOps (DVC)
      mapping_kind: operational
      equation_hint: (none)
      justification: |
        In data-centric pipelines like those managed by DVC (Data Version Control), parameter files and the resulting lock file serve an analogous role: versioning the inputs and configuration to guarantee that a data processing or model training pipeline can be exactly reproduced.
      references:
        - title: Data Version Control Documentation
          where: https://dvc.org/doc/start/data-management/data-and-model-versioning
          date: 2023-01-01
      confidence: 0.9
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "Any computational result (e.g., a JSON artifact) produced using a given Freeze Manifest is bit-for-bit reproducible by any agent who has access to the manifest and the specified software commit."
      domain: phenomenology
      falsifier: "Two separate runs of the same pipeline version, using the same manifest, produce statistically distinguishable results. This would indicate an unrecorded source of stochasticity (e.g., an unseeded RNG) or a hardware-dependent floating point discrepancy not properly controlled for."
      status: proposed
      links: [COSMO-000]
naming_notes:
  collisions: [Software Manifest (e.g., `AndroidManifest.xml`), Cargo Manifest]
  disambiguation: |
    Distinct from a *software package manifest*, which lists code dependencies, the Freeze Manifest lists the *physical and computational* dependencies for a specific scientific prediction. It "freezes" the physics parameters and initial conditions, not just the software library versions.
crosslinks:
  near_synonyms: []
  antonyms: [LIVE_FIT_PARAMETERS]
  prerequisites: [ONE_SHOT_ANCHOR]
  downstream_effects: [PREREGISTERED_PREDICTION]
license: CC-BY-SA-4.0
---

# Freeze Manifest

## Canonical (Pirouette)
A version-controlled, machine-readable data artifact, typically in YAML format, that serves as the single source of truth for a reproducible scientific prediction. It is generated once following a one-shot anchor (D3) procedure. The manifest must contain: the specific software version (e.g., git commit hash), the chosen anchor parameter and its value, all derived U-class and T-class parameters, and all seeds for any stochastic processes. Any subsequent computational artifact (e.g., a power spectrum, a background evolution table) must reference the manifest that generated it.

## EFT-First Summary
In the context of verifiable scientific computing, the Freeze Manifest acts as a "lock file" for a physical theory's parameters and the code used to evaluate it. Analogous to dependency lock files in software engineering (`poetry.lock`) or parameter versioning in MLOps (`dvc.lock`), it guarantees that a specific set of predictions is immutably tied to a single, grounded set of initial assumptions. This enforces methodological rigor by preventing post-hoc parameter tuning and ensuring that preregistered predictions are computationally reproducible by any third party.

## Glossary Links
- See also: [ONE_SHOT_ANCHOR](./one_shot_anchor.md), [PREREGISTERED_PREDICTION](./preregistered_prediction.md)