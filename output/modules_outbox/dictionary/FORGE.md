---
term: "Forge"
canonical_id: "FORGE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-015"]
---

---
term: Forge
canonical_id: FORGE
symbol: ⚗️
aliases: [Alchemical Forge]
parents: [DOMA-015]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-015
      lines: "§4"
      snippet: |
        Once woven on the loom, a module enters the Forge. This is the automated process that performs an Alchemical Union, transforming the single source file into two distinct, higher-order manifestations without losing its singular identity.
  editors: [Agent-Scribe]
  review_log: []
triad:
  art: |
    From the singular seed of a `.pmd` file, the Forge births twins: one of flesh and contemplation (the Codex), the other of pure signal and interaction (the JSON). It is the crucible where a single idea is given two distinct, coherent voices.
  law: |
    The Forge is a deterministic transformation `F: pmd -> (pdf, json)`. For a given `.pmd` input and a fixed build environment, the output Codex and Signal must be bit-for-bit reproducible.
  philosophy: |
    The Forge enforces the principle that an idea is incomplete until it can speak to both human intuition and machine logic. It rejects compromise by creating specialized, optimized manifestations for each domain, ensuring the original coherence is propagated without loss.
pirouette_definition: |
  The automated process that transforms a `.pmd` source file into its two higher-order manifestations: the human-readable Codex (PDF) and the machine-readable Signal (JSON). This 'Alchemical Union' ensures a single source of truth produces outputs optimized for distinct modes of engagement—contemplation and computation—without compromising the integrity of the original woven idea.
operational_definition:
  units: N/A (process)
  symbol_table:
    - name: F_⚗️(.pmd)
      meaning: The Forge transformation function applied to a `.pmd` file.
      dimensions: N/A (functional map)
      default_range: N/A
  measurement:
    procedures:
      - name: Forge Integrity Test
        outline: |
          1. Define a canonical set of diverse `.pmd` test files (the "Crucible Set").
          2. Establish a reference build environment (e.g., a specific container with version-pinned dependencies like Pandoc, LaTeX, and a JSON parser).
          3. Execute the Forge process on each file in the Crucible Set, generating reference PDF and JSON outputs.
          4. Store cryptographic hashes (e.g., SHA-256) of these reference outputs.
          5. For any new implementation or version of the Forge, run it on the Crucible Set within the reference environment and verify that the output hashes match the reference hashes exactly.
        expected_signals: [Matching SHA-256 hashes for both PDF and JSON outputs against a known reference.]
        pitfalls: [Environment drift (unpinned dependency versions), non-deterministic elements in build tools (e.g., embedded timestamps in PDFs).]
context_windows:
  - module: DOMA-015
    excerpt: |
      Once woven on the loom, a module enters the Forge. This is the automated process that performs an Alchemical Union, transforming the single source file into two distinct, higher-order manifestations without losing its singular identity. The Codex is the module's stable, archival body, designed for human contemplation. The Signal is the module's dynamic, living echo... a clean, structured JSON object that propagates through the framework's digital nervous system.
poetic_connections:
  motifs: [alchemy, transformation, bifurcation, synthesis, crucible]
  evocative_lines:
    - "the Alchemical Union of form and freedom"
    - "speak the language of human poetry and machine logic with a single voice"
  association_matrix:
    - [ "PMD_FORMAT", 0.9 ]
    - [ "CODEX", 0.8 ]
    - [ "SIGNAL", 0.8 ]
    - [ "LOOM", 0.6 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Compiler Toolchain (e.g., gcc)
      domain: Computer Science
      mapping_kind: conceptual
      equation_hint: |
        source_code -> compiler -> (executable, debug_symbols)
      justification: |
        Like a compiler, the Forge takes a high-level source format (`.pmd`) and transforms it into multiple, lower-level, and purpose-specific outputs. The JSON Signal is analogous to a machine-executable binary, while the PDF Codex is analogous to formatted documentation (e.g., man pages) or debug information generated as part of the same build process from a single source of truth.
      references: []
      confidence: 0.8
constraints_and_falsifiers:
  claims:
    - statement: "The Forge process is deterministic: a given `.pmd` input and a fixed build environment will always produce bit-identical PDF and JSON outputs."
      domain: experiment
      falsifier: "Observing two different output hashes for the PDF or JSON files when running the Forge twice on the same `.pmd` file in an identical, controlled environment."
      status: proposed
      links: [DOMA-015]
naming_notes:
  collisions: [SourceForge, Git-Forge]
  disambiguation: |
    In Pirouette, 'Forge' refers specifically to the `.pmd` -> `(PDF, JSON)` build process, not a software repository or collaborative platform. The name is an alchemical metaphor for transformation, not a smith's workshop for tools.
crosslinks:
  near_synonyms: [BUILD_PROCESS, COMPILER]
  antonyms: [AUTHORING, MANUAL_CONVERSION]
  prerequisites: [PMD_FORMAT, LOOM]
  downstream_effects: [CODEX, SIGNAL]
license: CC-BY-SA-4.0
---

# Forge

## Canonical (Pirouette)
The automated process that transforms a `.pmd` source file into its two higher-order manifestations: the human-readable Codex (PDF) and the machine-readable Signal (JSON). This 'Alchemical Union' ensures a single source of truth produces outputs optimized for distinct modes of engagement—contemplation and computation—without compromising the integrity of the original woven idea.

## Operational Summary
Functionally, the Forge is the Pirouette Framework's compiler toolchain. It ingests a source file (`.pmd`) and deterministically produces two outputs from it: a typeset document for human analysis (the Codex) and a structured data object for machine computation (the Signal). This ensures a single, human-authored source generates both its contemplative and computational forms.

## Glossary Links
- See also: PMD Format, Codex, Signal, Loom