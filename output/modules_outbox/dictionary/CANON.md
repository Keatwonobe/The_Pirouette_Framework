---
term: "Canon"
canonical_id: "CANON"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-028"]
---

---
term: Canon
canonical_id: CANON
symbol: 
aliases: []
parents: [DOMA-028, CORE-011]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-028
      snippet: |
        The framework's core parameters—its fundamental constants, its defined relationships, its symbolic grammar—form the Canon. This Canon is the framework's DNA.
  editors: [Archivist-Agent]
  review_log: []
triad:
  art: |
    The framework’s DNA, the immutable song of its core logic. To change the Canon is to rewrite the very music of its being, a performance whose integrity is recorded for all time.
  law: |
    The integrity of the Canon is operationally defined by the Seal of Coherence, a SHA256 hash of its complete, serialized state. Any modification to the Canon requires the Seal to be re-calculated and attested to, a process enforced by the Ritual of Provenance.
  philosophy: |
    The Canon enforces the principle that the framework must embody the very laws it describes. Its own history, recorded through changes to the Canon, must be an indelible and coherent Wound Channel, making the act of development a philosophical practice of integrity.
pirouette_definition: |
  The collection of the framework's core parameters, fundamental constants, symbolic grammar, and defined relationships. The Canon represents the immutable state-of-truth for the framework's logic at a given point in its evolution. Its integrity is cryptographically guaranteed by the Seal of Coherence.
operational_definition:
  units: Data Structure (Dimensionless)
  symbol_table: []
  measurement:
    procedures:
      - name: Seal of Coherence Calculation
        outline: |
          1. Serialize the complete canonical data set (all core parameters, constants, and grammar files) into a single, ordered byte stream.
          2. Apply the SHA256 hashing algorithm to this byte stream.
          3. The resulting 256-bit hexadecimal string is the Seal of Coherence, which represents the measured state of the Canon.
        expected_signals: [SHA256 Hash (Hexadecimal String), Coherence Fault (Boolean Mismatch)]
        pitfalls: [Serialization instability (e.g., changes in file order or non-significant whitespace altering the hash), Toolchain dependency errors]
context_windows:
  - module: DOMA-028
    excerpt: |
      The framework's core parameters—its fundamental constants, its defined relationships, its symbolic grammar—form the **Canon**. This Canon is the framework's DNA. To alter the Canon is to alter the framework's very nature. The Ritual of Provenance is the epigenetic process that ensures this DNA mutates with intention and perfect fidelity...
  - module: DOMA-028
    excerpt: |
      To attest to the integrity of the Canon at any point in time, we employ a cryptographic hash (SHA256). This is the **Seal of Coherence**. The Seal is not merely a checksum. It is the **Canonical Echo** of the framework's complete state. The hashing function acts as a resonance chamber, taking the complex pattern of the Canon and collapsing it into a single, high-fidelity, and unique signature.
poetic_connections:
  motifs: [DNA, Song/Echo, Loom/Weaving, Indelible Ink, Foundational Law]
  evocative_lines:
    - "A framework that preaches a universe of memory and consequence cannot be written in disappearing ink."
    - "Every hash is a knot in the thread of our reasoning, a promise that the story we tell about ourselves is the story we are actually living."
  association_matrix:
    - [ "SEAL_OF_COHERENCE", 0.9 ]
    - [ "RITUAL_OF_PROVENANCE", 0.8 ]
    - [ "WOUND_CHANNEL", 0.7 ]
formal_mappings:
  candidates:
    - target: Source of Truth (SoT)
      domain: Systems Architecture
      mapping_kind: operational
      justification: |
        The Canon serves as the declarative Source of Truth for the framework's core configuration. The Ritual of Provenance is a GitOps-style reconciliation loop that ensures the system's state never deviates from this declared truth, with the Seal of Coherence acting as the proof of reconciliation.
      references: []
      confidence: 0.8
  adopted:
    - target: Merkle Root
      domain: Cryptography
      mapping_kind: conceptual
      equation_hint: |
        Seal ≈ H(Canon_part1 || H(Canon_part2 || ...))
      rationale: |
        The mapping to a Merkle Root is adopted for its precision. It captures the essence of a single hash verifying a large, structured body of data, where tampering with any part invalidates the whole. This cryptographic dependency is the core mechanism of the Canon's integrity.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "Any unattested change to the Canon will be detected and rejected by the Ritual of Provenance."
      domain: experiment
      falsifier: "A change is made to a canonical file, but the pre-commit hook or the CI pipeline fails to detect the resulting Seal of Coherence mismatch and allows the change to be merged."
      status: supported
      links: [DOMA-028]
naming_notes:
  collisions: ["Canonical form (mathematics)", "Literary canon"]
  disambiguation: |
    In Pirouette, 'Canon' specifically refers to the cryptographically-versioned set of core framework definitions, not to a general set of accepted texts or a mathematical 'canonical form'. It is closer in meaning to religious or legal canon—a body of foundational law that governs the system.
crosslinks:
  near_synonyms: [SOURCE_OF_TRUTH]
  antonyms: [CONFIGURATION_DRIFT, EPHEMERA]
  prerequisites: [WOUND_CHANNEL]
  downstream_effects: [SEAL_OF_COHERENCE, RITUAL_OF_PROVENANCE]
license: CC-BY-SA-4.0
---

# Canon

## Canonical (Pirouette)
The collection of the framework's core parameters, fundamental constants, symbolic grammar, and defined relationships. The Canon represents the immutable state-of-truth for the framework's logic at a given point in its evolution. Its integrity is cryptographically guaranteed by the Seal of Coherence.

## EFT-First Summary
The Canon functions as a source of truth for the framework's core logic, analogous to a dataset verified by a **Merkle Root** in cryptography. Its state is collapsed into a single cryptographic hash (the Seal of Coherence), ensuring that any change to a single parameter invalidates the entire structure, providing a robust, falsifiable guarantee of integrity. This transforms software development from a series of edits into the deliberate carving of a permanent historical record.

## Glossary Links
- See also: Seal of Coherence, Ritual of Provenance, Wound Channel