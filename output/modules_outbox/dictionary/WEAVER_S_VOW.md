---
term: "Weaver's Vow"
canonical_id: "WEAVER_S_VOW"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-028"]
---

---
term: Weaver's Vow
canonical_id: WEAVERS_VOW
symbol: ✓commit
aliases: ["Pre-commit Vow", "Local Vow"]
parents: [DOMA-028]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-028
      lines: "§4, part I"
      snippet: |
        Before a Weaver can contribute their thread to the loom, they must make a local vow of integrity. A pre-commit script automatically calculates the Seal of Coherence from their proposed changes. If it does not match the documented Seal, the contribution is halted.
  editors: ["system-agent"]
  review_log: []
triad:
  art: |
    A personal, silent promise made to the loom before the shuttle is thrown. It is the moment of reflection where the weaver ensures their own thread is true before joining it to the collective tapestry.
  law: |
    A contribution SHALL NOT be committed to the local repository if the calculated Seal of Coherence for the proposed state does not exactly match the previously committed Seal. This check MUST execute automatically as a pre-commit hook.
  philosophy: |
    The Vow transforms individual action into a conscious act of system-wide responsibility. It asserts that coherence is not a retroactive cleanup task but a prerequisite for participation, ensuring that the Wound Channel is carved with intention from its very inception.
pirouette_definition: |
  The Weaver's Vow is the mandatory, automated pre-commit hook that enforces the first stage of the Ritual of Provenance. It acts as a local gatekeeper, calculating the Seal of Coherence from a Weaver's proposed changes and blocking the commit if it deviates from the Canon's last attested state, thereby preventing local dissonance from contaminating the shared developmental history.
operational_definition:
  units: Boolean
  symbol_table:
    - name: ✓commit
      meaning: The successful execution state of the Weaver's Vow, signifying local coherence.
      dimensions: dimensionless
      default_range: "{0 (Fail), 1 (Pass)}"
  measurement:
    procedures:
      - name: Local Coherence Verification
        outline: |
          1. Stage changes for a Git commit.
          2. Attempt to commit the changes, automatically triggering the pre-commit hook.
          3. The hook script calculates a new SHA256 hash (the Seal) from the canonical source files.
          4. This new hash is compared against the hash stored in the repository's Seal file.
          5. If they match, the procedure returns 'Pass' (1) and the commit succeeds. If they differ, it returns 'Fail' (0) and the commit is aborted with an error.
        expected_signals: ["CommitSuccess", "CommitAborted (Coherence Fault)"]
        pitfalls: ["Improperly configured Git hooks environment.", "Canonical files are not correctly identified by the hashing script.", "Bypassing the hook with `--no-verify` flag."]
context_windows:
  # Short, trimmed context quotes harvested from modules (3–6 sentences each).
  - module: DOMA-028
    excerpt: |
      Before a Weaver can contribute their thread to the loom, they must make a local vow of integrity. A pre-commit script automatically calculates the Seal of Coherence from their proposed changes. If it does not match the documented Seal, the contribution is halted. This prevents accidental dissonance from ever entering the shared channel.
  - module: DOMA-028
    excerpt: |
      The ritual is enforced through an unyielding automated workflow, transforming the act of coding from a private activity into a public, accountable act of weaving. A failing build is the mathematical proof that the proposed change introduces dissonance, knocking the system off its geodesic of maximal coherence.
poetic_connections:
  # Lightweight "word-association graph" and sticky lines.
  motifs: ["integrity", "vow", "gatekeeping", "local responsibility", "weaving", "promise"]
  evocative_lines:
    - "An unverified change is not an evolution; it is a breach..."
    - "...the act of coding from a private activity into a public, accountable act of weaving."
  association_matrix:
    # symmetric or directed; weights in [0,1]
    - [ "SEAL_OF_COHERENCE", 0.9 ]
    - [ "RITUAL_OF_PROVENANCE", 0.8 ]
    - [ "LOOMS_TEST", 0.7 ]
    - [ "WOUND_CHANNEL", 0.5 ]
formal_mappings:
  # Candidate alignments to EFT/SM/CM/GR terms, each with justification and refs.
  candidates: []
  adopted:
    - target: Pre-commit hook / Linter
      domain: DevOps|Computer Science
      mapping_kind: operational
      rationale: "Operationally, the Weaver's Vow is a specific type of pre-commit hook used for cryptographic integrity verification. Like a linter, it is an automated local check that enforces a rule before code is accepted, but instead of checking style, it verifies the global cryptographic integrity of a defined 'canon' of core parameters."
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The Weaver's Vow prevents any non-attested changes to the Canon from being committed to a local repository via a standard `git commit` command."
      domain: phenomenology
      falsifier: "A developer successfully commits a change that alters a canonical file without first running the attestation command to update the Seal of Coherence. This could be achieved by bypassing the hook (e.g., `git commit --no-verify`) or if the hook is not installed correctly."
      status: supported
      links: [DOMA-028]
naming_notes:
  collisions: []
  disambiguation: |
    The Weaver's Vow is distinct from the **Loom's Test**. The Vow is a *local, pre-commit* check performed on the developer's machine. The Loom's Test is a *remote, post-push* verification that happens in the shared Continuous Integration (CI) environment.
crosslinks:
  near_synonyms: []
  antonyms: [LOOMS_TEST]
  prerequisites: [SEAL_OF_COHERENCE]
  downstream_effects: [LOOMS_TEST]
license: CC-BY-SA-4.0
---

# Weaver's Vow

## Canonical (Pirouette)
The Weaver's Vow is the mandatory, automated pre-commit hook that enforces the first stage of the Ritual of Provenance. It acts as a local gatekeeper, calculating the Seal of Coherence from a Weaver's proposed changes and blocking the commit if it deviates from the Canon's last attested state, thereby preventing local dissonance from contaminating the shared developmental history.

## EFT-First Summary
The Weaver's Vow is an operational integrity check, analogous to a cryptographic linter or static analysis gate. It ensures that any proposed change to the system's core parameters ('The Canon') is locally verified against a committed hash ('The Seal') before being accepted into the version history, enforcing a state of maximal coherence at the individual contributor level. This is a practical, local implementation of the framework's core principle of developmental integrity.

## Glossary Links
- See also: SEAL_OF_COHERENCE, RITUAL_OF_PROVENANCE, LOOMS_TEST