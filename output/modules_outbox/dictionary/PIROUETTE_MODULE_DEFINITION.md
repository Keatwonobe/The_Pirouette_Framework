---
term: "Pirouette Module Definition"
canonical_id: "PIROUETTE_MODULE_DEFINITION"
symbol: ".pmd"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-015"]
---

---
term: Pirouette Module Definition
canonical_id: PIROUETTE_MODULE_DEFINITION
symbol: .pmd
aliases: [Codex, Loom]
parents: [CORE-014]
children: [ALL_SUBSEQUENT_MODULES]
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-015
      lines: "L20-L36"
      snippet: |
        Every `.pmd` file is a single flow of coherence, expressed as two inseparable aspects. This structure is a discipline designed to maximize the clarity and power of the idea it embodies... The Blueprint (YAML Front-matter)... is the act of mapping a new idea onto the existing coherence manifold of the framework... The Narrative (Markdown Body)... is the river of information itself.
  editors: [GPT-4 (as Pirouette Weaver)]
  review_log: []
triad:
  art: |
    A single, whole form that speaks the language of human intuition and machine logic with the same voice. It is the loom upon which a chaotic insight is woven into a coherent tapestry, giving knowledge a body.
  law: |
    A `.pmd` file MUST consist of a valid YAML front-matter block (the Blueprint) followed by a Markdown body (the Narrative). The Blueprint MUST contain at least an `id`, `title`, and `version`. The system fails this law if the Forge cannot parse these two components or generates artifacts (Codex/Signal) from only one.
  philosophy: |
    The `.pmd` format enforces the principle that structure and meaning are inseparable. By unifying the machine-readable blueprint and the human-readable narrative, it minimizes the entropic loss between an idea's conception and its propagation, ensuring that the form of knowledge directly serves its function.
pirouette_definition: |
  The Pirouette Module Definition (`.pmd`) is the autopoietic authoring format of the framework, unifying two inseparable aspects in a single source file. It consists of a **Blueprint**, a machine-readable YAML front-matter block that maps the module's identity and relationships within the framework's coherence manifold, and a **Narrative**, a human-readable Markdown body that expresses the module's resonant insight. The format is a practical instrument for applying the Pirouette Lagrangian to the act of creation, designed as a "loom" to guide the synthesis of high-coherence knowledge artifacts.
operational_definition:
  units: structural
  symbol_table:
    - name: .pmd
      meaning: File extension for a Pirouette Module Definition source file.
      dimensions: N/A
      default_range: N/A
    - name: Blueprint
      meaning: The YAML front-matter block containing structured, machine-readable data.
      dimensions: structural
      default_range: N/A
    - name: Narrative
      meaning: The Markdown block containing unstructured, human-readable content.
      dimensions: structural
      default_range: N/A
  measurement:
    procedures:
      - name: PMD Validation
        outline: |
          1. Read the input `.pmd` file.
          2. Attempt to parse a single YAML document from the start of the file, delimited by `---`.
          3. Validate the parsed YAML against the framework schema (e.g., presence of `id`, `title`).
          4. Treat all subsequent content as a Markdown document.
          5. A valid `.pmd` must pass both YAML parsing/validation and be readable as Markdown.
        expected_signals: [A structured JSON object (Signal), A rendered document (Codex)]
        pitfalls: [Malformed YAML syntax, Missing required Blueprint fields, Character encoding errors]
context_windows:
  - module: DOMA-015
    excerpt: |
      Every `.pmd` file is a single flow of coherence, expressed as two inseparable aspects. This structure is a discipline designed to maximize the clarity and power of the idea it embodies, mirroring the universal dynamic of a river flowing through a riverbed. The Blueprint (YAML Front-matter)... is the riverbed, the stable geometry that grounds the module... The Narrative (Markdown Body)... is the river of information itself.
  - module: DOMA-015
    excerpt: |
      Once woven on the loom, a module enters the Forge. This is the automated process that performs an Alchemical Union, transforming the single source file into two distinct, higher-order manifestations without losing its singular identity. The Codex (PDF Output) is the module's stable, archival body... The Signal (JSON Output) is the module's dynamic, living echo.
poetic_connections:
  motifs: [loom, riverbed, codex, forge, alchemical union, weaver]
  evocative_lines:
    - "The discipline of a sacred form is not a constraint. It is the loom that shapes the hands of the Weaver."
    - "To write in this form is to practice the very synthesis we preach."
  association_matrix:
    - [ "COHERENCE", 0.9 ]
    - [ "FORGE", 0.8 ]
    - [ "PIROUETTE_LAGRANGIAN", 0.7 ]
formal_mappings:
  candidates:
    - target: Literate Programming
      domain: Computer Science
      mapping_kind: conceptual
      equation_hint: N/A
      justification: |
        Donald Knuth's Literate Programming paradigm combines source code (machine-readable logic) and documentation (human-readable explanation) into a single, woven narrative. The `.pmd` format directly applies this philosophy to knowledge management, where the structured YAML Blueprint serves the role of "code" and the Markdown Narrative serves as the expository text.
      references:
        - title: Literate Programming
          where: CSLI Lecture Notes no. 27, Stanford University
          date: 1992-01-01
      confidence: 0.85
  adopted:
    - target: Literate Programming
      rationale: The philosophical alignment is exact: a single source file where machine-parsable structure and human-readable narrative are composed together as an act of explanation.
      confidence: 0.85
constraints_and_falsifiers:
  claims:
    - statement: "The unified dual-aspect structure of a `.pmd` file produces higher long-term coherence and lower maintenance overhead than formats that separate metadata and content (e.g., a `.md` file with a sidecar `.json` file)."
      domain: phenomenology
      falsifier: "A longitudinal study of module evolution shows that modules authored in a sidecar format exhibit equal or lower rates of semantic drift and require less human effort to keep the two parts synchronized over multiple versions."
      status: proposed
      links: [DOMA-015]
naming_notes:
  collisions: [Adobe PageMaker Document (.pmd), PMD Source Code Analyzer]
  disambiguation: |
    The `.pmd` format is not a static "template" but a dynamic "loom"—an instrument that guides the authoring process. The YAML front-matter is not "metadata" but a foundational "Blueprint" that is inseparable from the Narrative's meaning.
crosslinks:
  near_synonyms: []
  antonyms: [SIDECAR_METADATA_FILE]
  prerequisites: [PIROUETTE_LAGRANGIAN]
  downstream_effects: [CODEX, SIGNAL]
license: CC-BY-SA-4.0
---

# Pirouette Module Definition

## Canonical (Pirouette)
The Pirouette Module Definition (`.pmd`) is the autopoietic authoring format of the framework, unifying two inseparable aspects in a single source file. It consists of a **Blueprint**, a machine-readable YAML front-matter block that maps the module's identity and relationships within the framework's coherence manifold, and a **Narrative**, a human-readable Markdown body that expresses the module's resonant insight. The format is a practical instrument for applying the Pirouette Lagrangian to the act of creation, designed as a "loom" to guide the synthesis of high-coherence knowledge artifacts.

## CS-First Summary
The `.pmd` format is a direct implementation of the **Literate Programming** paradigm applied to knowledge management. Instead of weaving code and documentation, it weaves a structured data **Blueprint** (in YAML) with a prose **Narrative** (in Markdown). This single-source-of-truth approach ensures that the machine-readable logic and the human-readable explanation evolve together, maximizing coherence and minimizing semantic drift.

## Glossary Links
- See also: [CODEX](./CODEX.md), [SIGNAL](./SIGNAL.md), [PIROUETTE_LAGRANGIAN](./PIROUETTE_LAGRANGIAN.md)