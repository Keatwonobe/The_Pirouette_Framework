---
term: <Human-readable term>              # e.g., Temporal Pressure
canonical_id: <UPPER_UNDERSCORE_NAME>    # e.g., TEMPORAL_PRESSURE
symbol: <primary symbol(s)>              # e.g., Γ
aliases: [<alias1>, <alias2>]            # other names in Pirouette or literature
parents: [<module-ids>]                  # modules where the term is defined/refined
children: [<module-ids>]                 # downstream modules depending on this term
status: draft|candidate|ratified
version: 0.1
last_updated: YYYY-MM-DD
provenance:
  sources:
    - module: <MODULE-ID>
      lines: "<L#-L#>"                   # optional pointer to lines in source
      snippet: |
        <short copied snippet showing native usage>
  editors: [<name-or-agent>, ...]        # who touched this entry
  review_log: []                         # list of {date, reviewer, notes}
triad:
  art: |
    <1-3 sentence poetic essence. imagery & metaphor permitted.>
  law: |
    <crisp operational rule or law-like statement; measurable; falsifiable hooks.>
  philosophy: |
    <why this matters; conceptual role across the framework; intended telos.>
pirouette_definition: |
  <canonical pirouette definition in house style; concise but complete.>
operational_definition:
  units: <SI or dimensionless etc.>
  symbol_table:
    - name: <symbol>    # e.g., Γ
      meaning: <meaning>
      dimensions: <L^a M^b T^c ... or "dimensionless">
      default_range: <typical numeric range or "contextual">
  measurement:
    procedures:
      - name: <procedure name>
        outline: |
          <sketch of how this would be measured or inferred>
        expected_signals: [<signal1>, <signal2>]
        pitfalls: [<pitfall1>, <pitfall2>]
context_windows:
  # Short, trimmed context quotes harvested from modules (3–6 sentences each).
  - module: <MODULE-ID>
    excerpt: |
      <trimmed excerpt>
  - module: <MODULE-ID>
    excerpt: |
      <trimmed excerpt>
poetic_connections:
  # Lightweight "word-association graph" and sticky lines.
  motifs: [<motif1>, <motif2>, <motif3>]
  evocative_lines:
    - "<short line from modules that 'rings'>"
    - "<another>"
  association_matrix:
    # symmetric or directed; weights in [0,1]
    - [ "term_a", 0.6 ]
    - [ "term_b", 0.4 ]
formal_mappings:
  # Candidate alignments to EFT/SM/CM/GR terms, each with justification and refs.
  candidates:
    - target: <community-term-or-symbol>  # e.g., P(X) kinetic term, sound speed c_s^2
      domain: EFT|SM|GR|CM|AMO|Math
      mapping_kind: conceptual|mathematical|operational
      equation_hint: |
        <optional short equation showing the mapping>
      justification: |
        <2–4 sentences>
      references:
        - title: <paper/book>
          where: <arXiv/journal/section>
          date: <YYYY-MM-DD>
      confidence: 0.0
  adopted:
    - target: <chosen mapping, if any>
      rationale: <why chosen>
      confidence: 0.0
constraints_and_falsifiers:
  claims:
    - statement: "<testable statement>"
      domain: theory|phenomenology|experiment
      falsifier: "<how this could be false>"
      status: proposed|under-test|supported|refuted
      links: [<module-ids or external refs>]
naming_notes:
  collisions: [<symbol collisions>]
  disambiguation: |
    <tips for readers where confusion is likely>
crosslinks:
  near_synonyms: [<term-id>]
  antonyms: [<term-id>]
  prerequisites: [<term-id>]
  downstream_effects: [<term-id>]
license: CC-BY-SA-4.0
---

# {term}

## Canonical (Pirouette)
{pirouette_definition}

## EFT-First Summary
<crisp paragraph using adopted mappings; link to references>

## Glossary Links
- See also: <links to related entries>

