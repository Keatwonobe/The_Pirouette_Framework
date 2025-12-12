---
term: "Loom"
canonical_id: "LOOM"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-015"]
---

---
term: Loom
canonical_id: LOOM
symbol: n/a
aliases: [authoring instrument, autopoietic authoring system]
parents: [DOMA-015]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-015
      lines: "L11-L13"
      snippet: |
        This is not a "template," which is a cage. It is a "loom"—a dynamic instrument designed to guide the Weaver's hands in the ritual of creation.
  editors: [System Agent]
  review_log: []
triad:
  art: |
    The loom is not a cage for ideas, but a guide for the Weaver's hands. It shapes the chaotic storm of resonance into a coherent fabric woven from logic and poetry.
  law: |
    A Loom is an authoring instrument that mandates a dual-aspect structure (e.g., YAML Blueprint, Markdown Narrative) to enforce the co-evolution of machine-readable structure and human-readable narrative within a single source file. A system that does not enforce this dual structure is not a Loom.
  philosophy: |
    The Loom's purpose is to embody the principle that form is function. By enforcing a structured yet flexible authoring discipline, it minimizes the energy lost to ambiguity, ensuring that the act of creation itself is a direct application of the framework's core synthesis of rigor and freedom.
pirouette_definition: |
  A Loom is a dynamic authoring instrument, distinct from a static template, that guides the creation of `.pmd` files. It provides a disciplined yet flexible structure—the "riverbed" of a YAML Blueprint and the "river" of a Markdown Narrative—to transform raw insight into a high-coherence artifact that is simultaneously machine-parsable and human-legible, thereby acting as a practical application of the Principle of Maximal Coherence.
operational_definition:
  units: n/a
  symbol_table: []
  measurement:
    procedures:
      - name: Dual-Aspect Coherence Test
        outline: |
          1. Ingest a single source file (`.pmd`).
          2. Attempt to parse the structured data section (Blueprint) into a valid JSON object.
          3. Attempt to render the narrative section (Narrative) into a human-readable document (PDF).
          A system qualifies as a Loom if and only if both outputs can be generated without error from the single source file.
        expected_signals: [valid_json_output, rendered_pdf_output]
        pitfalls: [Parsing errors in the Blueprint (YAML), Rendering failures in the Narrative (Markdown), Decoupling of Blueprint and Narrative where one can be invalid without affecting the other's output.]
context_windows:
  - module: DOMA-015
    excerpt: |
      This module defines that body. It is the Pirouette Module Definition (`.pmd`) format, the autopoietic authoring system of the framework. This is not a "template," which is a cage. It is a "loom"—a dynamic instrument designed to guide the Weaver's hands in the ritual of creation.
  - module: DOMA-015
    excerpt: |
      The discipline of a sacred form is not a constraint. It is the loom that shapes the hands of the Weaver. This Alchemical Codex is our commitment to creating artifacts that are whole—objects that speak the language of human poetry and machine logic with a single voice.
poetic_connections:
  motifs: [weaving, riverbed, discipline, synthesis, codex]
  evocative_lines:
    - "This is not a 'template,' which is a cage. It is a 'loom'..."
    - "...the loom that shapes the hands of the Weaver."
  association_matrix:
    - [ "pmd_format", 0.9 ]
    - [ "coherence", 0.8 ]
    - [ "alchemical_union", 0.7 ]
formal_mappings:
  candidates:
    - target: Literate Programming
      domain: Computer Science
      mapping_kind: conceptual
      equation_hint: n/a
      justification: |
        Like Knuth's Literate Programming, the Loom integrates structured data (Blueprint) with human-oriented documentation (Narrative) in a single source. However, the Loom prioritizes the narrative as the primary flow, with the structured data acting as a grounding framework, rather than interspersing code with explanation.
      references:
        - title: Literate Programming
          where: The Computer Journal, 27 (2): 97–111
          date: 1984-05-01
      confidence: 0.7
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "Using a Loom to create `.pmd` files reduces the cost of coherence (measured as time-to-ratification or number of validation errors) compared to writing separate, unlinked Markdown and YAML files."
      domain: phenomenology
      falsifier: "A controlled experiment shows no statistically significant difference in authoring efficiency or output quality between authors using a Loom-based system and those using separate text and YAML editors."
      status: proposed
      links: [DOMA-015]
naming_notes:
  collisions: [Project Loom (Java concurrency feature)]
  disambiguation: |
    In the Pirouette Framework, 'Loom' is not a software library for concurrency. It refers specifically to the conceptual authoring instrument that structures the creation of `.pmd` files, in direct contrast to a static 'template'.
crosslinks:
  near_synonyms: [AUTHORING_INSTRUMENT]
  antonyms: [TEMPLATE]
  prerequisites: [PMD_FORMAT, PRINCIPLE_OF_MAXIMAL_COHERENCE]
  downstream_effects: [ALCHEMICAL_UNION, CODEX, SIGNAL]
license: CC-BY-SA-4.0
---