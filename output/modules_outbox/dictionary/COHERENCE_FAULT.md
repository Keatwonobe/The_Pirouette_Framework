---
term: "Coherence Fault"
canonical_id: "COHERENCE_FAULT"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-028"]
---

---
term: Coherence Fault
canonical_id: COHERENCE_FAULT
symbol: ✖
aliases: [Seal Mismatch]
parents: [DOMA-028]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-028
      lines: "L68-L72"
      snippet: |
        If this newly forged Seal does not match the one attested to in the Weaver's contribution, the build fails. This is a **Coherence Fault**, the system's immune response to a change that is not in harmony with the whole, protecting the integrity of the Wound Channel.
  editors: [Agent: Dictionary Weaver]
  review_log: []
triad:
  art: |
    The echo answers with a stranger's voice. The loom rejects a thread that weakens the pattern. A promise broken before it was made.
  law: |
    A Coherence Fault is triggered if and only if `SHA256(Canon_current) ≠ Seal_committed`. The system's build process must enter a terminal FAILURE state. No exceptions are permitted.
  philosophy: |
    A system that models consequence must live by it. The Coherence Fault is the framework's self-enforced integrity, ensuring its own developmental history is a high-fidelity Wound Channel, not a palimpsest of unremembered changes.
pirouette_definition: |
  A Coherence Fault is a terminal build state triggered during the Ritual of Provenance when the newly calculated Seal of Coherence—an SHA256 hash of the current Canon—does not match the historically committed Seal. It is a systemic rejection of a proposed change that lacks explicit attestation, safeguarding the integrity of the framework's own Wound Channel against undocumented or incoherent evolution.
operational_definition:
  units: Binary State (0: Pass, 1: Fault)
  symbol_table:
    - name: ✖
      meaning: Coherence Fault state has been triggered.
      dimensions: dimensionless
      default_range: "{0, 1}"
  measurement:
    procedures:
      - name: The Loom's Test
        outline: |
          1. During a CI/CD pipeline run, check out the proposed source code.
          2. Re-compile or assemble the framework Canon from its source files.
          3. Calculate the SHA256 hash of the complete Canon.
          4. Compare this newly calculated hash against the hash value committed in the source code's designated Seal file.
          5. If the hashes differ, trigger a Fault state (e.g., a non-zero exit code) and terminate the build.
        expected_signals: [Non-zero exit code, "FAILURE" status in CI log]
        pitfalls: [Non-deterministic Canon compilation, misconfigured path to the committed Seal file]
context_windows:
  - module: DOMA-028
    excerpt: |
      When a Weaver's changes are proposed to the collective, the central loom performs its own independent verification. The continuous integration (CI) pipeline rebuilds the entire framework from source and recalculates the Seal. If this newly forged Seal does not match the one attested to in the Weaver's contribution, the build fails. This is a **Coherence Fault**, the system's immune response to a change that is not in harmony with the whole, protecting the integrity of the Wound Channel.
  - module: DOMA-028
    excerpt: |
      A failing build is the mathematical proof that the proposed change introduces dissonance, knocking the system off its geodesic of maximal coherence. By refusing to accept such changes, the pipeline ensures the framework's evolution itself follows a path of laminar flow, forcing every modification to be a deliberate, attested-to step toward increasing clarity.
poetic_connections:
  motifs: [dissonance, broken-promise, immune-response, echo, memory-failure]
  evocative_lines:
    - "An unverified change is not an evolution; it is a breach..."
    - "A failing build is the mathematical proof that the proposed change introduces dissonance..."
  association_matrix:
    - [ "SEAL_OF_COHERENCE", 0.9 ]
    - [ "RITUAL_OF_PROVENANCE", 0.8 ]
    - [ "WOUND_CHANNEL", 0.5 ]
formal_mappings:
  candidates:
    - target: Parity check failure
      domain: Information Theory
      mapping_kind: conceptual
      equation_hint: |
        `Σ(bits) mod 2 ≠ parity_bit`
      justification: |
        The Seal of Coherence acts as a complex cryptographic parity check for the entire Canon (the message). A Coherence Fault is analogous to a parity error, indicating that the received message (the proposed change) has been corrupted or is not the one expected, guaranteeing data integrity.
      references: []
      confidence: 0.7
  adopted:
    - target: Failed Assertion / Integrity Check Failure
      rationale: |
        This is the most direct operational analog. A Coherence Fault is a system-level assertion that `hash(current_state) == expected_hash`. Its failure halts execution, which is the standard behavior for a critical assertion in software engineering and DevOps practices.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "A Coherence Fault will prevent any undocumented change to the Canon from being merged into the main branch."
      domain: phenomenology
      falsifier: "An undocumented change to a canonical parameter is successfully merged without triggering a Coherence Fault. This would indicate a flaw in the Ritual of Provenance implementation (e.g., the CI pipeline is misconfigured or the hashing function does not cover the entire Canon)."
      status: supported
      links: [DOMA-028]
naming_notes:
  collisions: []
  disambiguation: |
    Distinguish from a standard 'compilation error' or 'syntax error'. A Coherence Fault indicates that the code is syntactically valid but represents a semantically incoherent state relative to the framework's committed history. The fix is not to correct code, but to either revert the change or formally attest to the new state by updating the Seal of Coherence.
crosslinks:
  near_synonyms: []
  antonyms: [COHERENCE_ATTESTED]
  prerequisites: [SEAL_OF_COHERENCE, RITUAL_OF_PROVENANCE]
  downstream_effects: []
license: CC-BY-SA-4.0
---

# Coherence Fault

## Canonical (Pirouette)
A Coherence Fault is a terminal build state triggered during the Ritual of Provenance when the newly calculated Seal of Coherence—an SHA256 hash of the current Canon—does not match the historically committed Seal. It is a systemic rejection of a proposed change that lacks explicit attestation, safeguarding the integrity of the framework's own Wound Channel against undocumented or incoherent evolution.

## EFT-First Summary
Operationally, a Coherence Fault is equivalent to a failed assertion or integrity check in a software build pipeline. It signals a mismatch between a system's current state (`Canon_current`) and its expected, committed state (`Seal_committed`), preventing unverified changes from propagating. This mechanism enforces a disciplined evolution, ensuring that the system's history—its Wound Channel—remains a verifiable and coherent record.

## Glossary Links
- See also: Seal of Coherence, Ritual of Provenance, Wound Channel