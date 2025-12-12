---
term: "Signal"
canonical_id: "SIGNAL"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-015"]
---

---
term: Signal
canonical_id: SIGNAL
symbol: 
aliases: [living echo, machine-readable pattern, JSON Output]
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
        **The Signal (JSON Output):** This is the module's dynamic, living echo. The forge parses the YAML Blueprint to create a clean, structured JSON object—the machine-readable pattern that propagates through the framework's digital nervous system. The Signal is not for reading; it is for interacting, allowing other instruments and analytical engines to connect with the module's core logic.
  editors: [system_agent]
  review_log: []
triad:
  art: |
    A module's living echo, a structured ghost that haunts the framework's digital nervous system. It is the pure pattern, stripped of its narrative flesh, ready to speak with other machines.
  law: |
    A Signal is a valid JSON object derived exclusively from a module's YAML Blueprint. Any information present in the Signal that cannot be traced to the Blueprint, or any Blueprint key-value pair not represented in the Signal, constitutes a Forge malfunction.
  philosophy: |
    The Signal embodies the principle that an idea's formal structure is as vital as its narrative content. It ensures that every act of human expression is simultaneously an act of machine instrumentation, allowing insight to propagate and interact at the speed of logic.
pirouette_definition: |
  The dynamic, machine-readable JSON object generated from a module's YAML Blueprint. The Signal represents the module's formal structure, stripped of its narrative content, and serves as the primary interface for interaction with other digital instruments, analytical engines, and automated processes within the framework's ecosystem. It is the coherent, actionable pattern of an idea, designed for propagation and synthesis.
operational_definition:
  units: structured data (JSON)
  symbol_table:
    - name: N/A
      meaning: The Signal is a data structure, not a physical quantity, and has no associated symbol.
      dimensions: dimensionless
      default_range: N/A
  measurement:
    procedures:
      - name: Signal Integrity Verification
        outline: |
          1. Parse the YAML Blueprint of a source `.pmd` file.
          2. Generate the Signal JSON using the standard Forge process.
          3. For each key in the Blueprint, verify its corresponding key-value pair exists and is correctly typed in the Signal.
          4. Validate the Signal is well-formed JSON.
          5. Verify the Signal contains no data sourced from the Markdown Narrative.
        expected_signals: [A valid JSON object containing keys like `id`, `version`, `parents`, `dependencies`, `keywords`]
        pitfalls: [Forge process errors (e.g., YAML parsing failures), Inclusion of narrative-only content in the Signal ('data leakage'), Type mismatches between YAML and JSON (e.g., string vs. integer)]
context_windows:
  - module: DOMA-015
    excerpt: |
      The forge parses the YAML Blueprint to create a clean, structured JSON object—the machine-readable pattern that propagates through the framework's digital nervous system. The Signal is not for reading; it is for interacting, allowing other instruments and analytical engines to connect with the module's core logic.
  - module: DOMA-015
    excerpt: |
      **The Blueprint (YAML Front-matter):** This is not metadata. It is the act of mapping a new idea onto the existing coherence manifold of the framework. By defining the module's `id`, `parents`, `dependencies`, and `keywords`, the Weaver performs a precise act of placement... This structured YAML is the riverbed, the stable geometry that grounds the module and gives it a place within the whole.
poetic_connections:
  motifs: [living echo, digital nervous system, machine-readable pattern, data ghost]
  evocative_lines:
    - "...the machine-readable pattern that propagates through the framework's digital nervous system."
    - "...an artifact with the highest possible integrity."
  association_matrix:
    - [ "BLUEPRINT", 1.0 ]
    - [ "CODEX", 0.9 ]
    - [ "FORGE", 0.9 ]
    - [ "NARRATIVE", 0.1 ]
formal_mappings:
  candidates:
    - target: Data Transfer Object (DTO)
      domain: Computer Science
      mapping_kind: conceptual
      equation_hint:
      justification: |
        Like a DTO, a Signal is a simple object whose purpose is to transfer structured data between processes or systems. It contains no business logic itself but represents the serialized state and identity of an entity (the module) for consumption by other services (instruments).
      references:
        - title: Patterns of Enterprise Application Architecture
          where: Martin Fowler
          date: 2002-11-15
      confidence: 0.9
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "A Signal is a complete and lossless representation of its source module's Blueprint."
      domain: phenomenology
      falsifier: "Discovering a key in a module's YAML Blueprint that is consistently omitted from its generated Signal, or a key in the Signal that has no origin in the Blueprint."
      status: supported
      links: [DOMA-015]
naming_notes:
  collisions: [Signal (Digital Signal Processing), Signal (Reactive Programming), Signal (Electronics)]
  disambiguation: |
    In Pirouette, 'Signal' refers specifically to the static, structured data packet representing a module's identity, not to a time-varying quantity (as in DSP) or a reactive programming primitive (a stream of events). It is an atomic representation, not a continuous flow.
crosslinks:
  near_synonyms: [BLUEPRINT]
  antonyms: [NARRATIVE, CODEX]
  prerequisites: [MODULE, BLUEPRINT]
  downstream_effects: [INSTRUMENT_INTERACTION, FRAMEWORK_ANALYSIS]
license: CC-BY-SA-4.0
---

# Signal

## Canonical (Pirouette)
The dynamic, machine-readable JSON object generated from a module's YAML Blueprint. The Signal represents the module's formal structure, stripped of its narrative content, and serves as the primary interface for interaction with other digital instruments, analytical engines, and automated processes within the framework's ecosystem. It is the coherent, actionable pattern of an idea, designed for propagation and synthesis.

## EFT-First Summary
The Signal acts as a standardized data packet, analogous to a Data Transfer Object (DTO) in software architecture. It serializes the formal, structural properties of a Pirouette module (defined in its Blueprint) into a machine-readable JSON format. This allows any component within the framework's digital ecosystem to query, route, and interact with the module's core identity without needing to parse its human-readable narrative content.

## Glossary Links
- See also: [Blueprint](<glossary_link_placeholder>), [Codex](<glossary_link_placeholder>), [Forge](<glossary_link_placeholder>)