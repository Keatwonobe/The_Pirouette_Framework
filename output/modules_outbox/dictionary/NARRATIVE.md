---
term: "Narrative"
canonical_id: "NARRATIVE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-015"]
---

---
term: Narrative
canonical_id: NARRATIVE
symbol: 
aliases: [Markdown Body, The River]
parents: [DOMA-015]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-015
      lines: "§2"
      snippet: |
        This is the river of information itself. Following the YAML, the module's narrative unfolds in flexible and expressive Markdown. It is the structured, linear expression of the resonant insight, where complex ideas are communicated with both rigor and elegance.
  editors: [System Weaver]
  review_log: []
triad:
  art: |
    The river of information that flows through the channel carved by the Blueprint. It is the song of the module, carrying the current of metaphor, logic, and poetry that brings an idea to life.
  law: |
    Every module must contain a Narrative as a Markdown-formatted body immediately following the YAML Blueprint. The Narrative must contain the complete, human-readable expression of the module's core concepts.
  philosophy: |
    The Narrative embodies the principle of Temporal Coherence (Kτ). Its purpose is to ensure that knowledge is not merely structured but also communicated with elegance and clarity, making the framework's wisdom accessible to human intuition.
pirouette_definition: |
  The expressive, human-readable body of a module, written in Markdown, which follows the structured YAML Blueprint. The Narrative is the primary medium for conveying the module's core ideas, arguments, and metaphors in a linear, coherent flow. It is the dynamic and semantic component that is rendered into the archival Codex.
operational_definition:
  units: N/A (qualitative)
  symbol_table: []
  measurement:
    procedures:
      - name: Coherence Alignment Test
        outline: |
          Using NLP topic modeling and vector embeddings, analyze the semantic content of the Narrative. Measure the cosine similarity between the Narrative's dominant topic vectors and the vector representations of keywords and concepts defined in the module's Blueprint. A high similarity score indicates a well-aligned Narrative.
        expected_signals: [High cosine similarity (>0.8) between Narrative and Blueprint vectors, Low perplexity score from a framework-tuned language model.]
        pitfalls: [Fails to capture poetic or novel metaphorical connections, may penalize stylistically dense or abstract prose.]
context_windows:
  - module: DOMA-015
    excerpt: |
      **The Narrative (Markdown Body):** This is the river of information itself. Following the YAML, the module's narrative unfolds in flexible and expressive Markdown. It is the structured, linear expression of the resonant insight, where complex ideas are communicated with both rigor and elegance. This is the current of metaphor, logic, and poetry that moves through the channel carved by the Blueprint—dynamic, adaptive, and alive with meaning.
  - module: DOMA-015
    excerpt: |
      **Temporal Coherence (Kτ):** This is the quality and integrity of the human-readable narrative. It is its clarity, its elegance, its poetic force, and its semantic richness. It is the "song" of the module.
poetic_connections:
  motifs: [river, flow, song, current, fabric, poetry]
  evocative_lines:
    - "This is the river of information itself."
    - "It is the 'song' of the module."
    - "The current of metaphor, logic, and poetry that moves through the channel..."
  association_matrix:
    - [ "BLUEPRINT", 0.9 ]
    - [ "TEMPORAL_COHERENCE", 0.8 ]
    - [ "CODEX", 0.7 ]
    - [ "WEAVER", 0.6 ]
formal_mappings:
  candidates:
    - target: Prose Component in Literate Programming
      domain: Computer Science
      mapping_kind: conceptual
      equation_hint:
      justification: |
        In Donald Knuth's Literate Programming, explanatory prose (`weave`) is integrated with code (`tangle`). The Narrative is directly analogous to the `weave` component, providing the human-centric explanation that gives context and meaning to the structured, machine-readable Blueprint.
      references:
        - title: "Literate Programming"
          where: "The Computer Journal, Vol. 27, No. 2"
          date: 1984-05-01
      confidence: 0.9
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "A module's Narrative is the primary carrier of its Temporal Coherence (Kτ)."
      domain: phenomenology
      falsifier: "Demonstrate that a module's Kτ score, measured via framework tools, is not significantly degraded when its Narrative is replaced with semantically null but grammatically correct placeholder text, implying Kτ is derived almost entirely from the Blueprint."
      status: proposed
      links: [DOMA-015, CORE-006]
    - statement: "The Narrative must be compliant with the CommonMark specification."
      domain: theory
      falsifier: "A ratified module whose Narrative section fails to be correctly parsed and rendered into a Codex by a standard CommonMark parser."
      status: supported
      links: [DOMA-015]
naming_notes:
  collisions: []
  disambiguation: |
    The Narrative is not simply "the text" of a module; it is specifically the flowing, human-readable prose that follows the structured Blueprint. The Blueprint is the riverbed (structure, machine-readable), while the Narrative is the river (flow, human-readable).
crosslinks:
  near_synonyms: []
  antonyms: [BLUEPRINT]
  prerequisites: [BLUEPRINT]
  downstream_effects: [TEMPORAL_COHERENCE, CODEX, SIGNAL]
license: CC-BY-SA-4.0
---

# Narrative

## Canonical (Pirouette)
The expressive, human-readable body of a module, written in Markdown, which follows the structured YAML Blueprint. The Narrative is the primary medium for conveying the module's core ideas, arguments, and metaphors in a linear, coherent flow. It is the dynamic and semantic component that is rendered into the archival Codex.

## Computer Science Analogy
The Narrative functions as the human-readable "prose" component in a literate programming paradigm, conveying the logical flow and meaning that complements the structured, machine-readable data of the Blueprint. It is analogous to the output of a `weave` process, intended for human comprehension.

## Glossary Links
- See also: Blueprint, Temporal Coherence, Codex