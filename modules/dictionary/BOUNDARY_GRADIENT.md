---
term: "Boundary Gradient"
canonical_id: "BOUNDARY_GRADIENT"
symbol: "Γ"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-137"]
---

---
term: Boundary Gradient
canonical_id: BOUNDARY_GRADIENT
symbol: Γ
aliases: [Feature Gradient, Mnemonic Slope, Coherence Cliff]
parents: [DOMA-137]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-137
      lines: "§4.3"
      snippet: |
        Boundary Gradient (Γ): The steepness of its slopes. A sharp, high-gradient boundary suggests an encapsulated, taboo memory. A diffuse, chaotic boundary indicates a memory that is actively "bleeding" into the surrounding culture, generating turbulence.
  editors: [Weaver-Agent 7]
  review_log: []
triad:
  art: |
    The sharpness of a memory's edge. A sheer cliff marks a terror too deep to speak of, while a gentle, marshy slope shows a story that has seeped into every part of the land, coloring the soil.
  law: |
    The Boundary Gradient Γ is the magnitude of the spatial gradient of the coherence anomaly field at the perimeter of a Mnemonic Landscape feature. A high Γ (>1 standard deviation above baseline noise) indicates a sharply defined, encapsulated memory; a low Γ indicates a diffuse, integrated memory.
  philosophy: |
    Γ distinguishes between unprocessed trauma and integrated history. A high-Γ "taboo" acts as a singular point of failure, while a low-Γ "bleeding" memory creates systemic, low-grade turbulence. Healing is not erasing the feature, but reshaping its boundary from a cliff into a livable landscape.
pirouette_definition: |
  The Boundary Gradient (Γ) is a scalar field quantity that measures the rate of change of coherence at the boundary of a feature (e.g., a Coherence Well or Plateau) within a Mnemonic Landscape. It quantifies the "steepness" of the transition from the feature's anomalous coherence back to the cultural baseline. High values indicate a sharp, encapsulated boundary, characteristic of taboo or suppressed memories, while low, diffuse values indicate a memory that is actively and often turbulently integrated with the surrounding culture.
operational_definition:
  units: m⁻¹ (inverse meters), assuming dimensionless Coherence.
  symbol_table:
    - name: Γ
      meaning: Boundary Gradient magnitude
      dimensions: L⁻¹
      default_range: contextual, typically 10⁻³ to 10⁻⁶ m⁻¹ for cultural features
  measurement:
    procedures:
      - name: Mnemonic Cartography Gradient Analysis
        outline: |
          1. Construct a spatiotemporal cultural field from diverse data streams (socio-economic, linguistic, historical).
          2. Calculate the deviation from a Baseline Coherence Model, yielding a coherence anomaly map `δC(x, y)`.
          3. Identify the perimeter of a significant Mnemonic Feature (Well or Plateau).
          4. Compute the spatial gradient `∇(δC)` at points along this perimeter.
          5. The Boundary Gradient Γ is the magnitude of this vector, `|∇(δC)|`.
        expected_signals: [Sharp peaks in Γ at the boundaries of suppressed massacre sites or unacknowledged traumas. Broad, low-amplitude Γ distributions for foundational myths or assimilated historical events.]
        pitfalls: [Data sparsity creating artificial gradients. Conflating unrelated adjacent features. Misspecification of the Baseline Coherence Model.]
context_windows:
  - module: DOMA-137
    excerpt: |
      For each significant feature, analyze its geometric and dynamic properties... Boundary Gradient (Γ): The steepness of its slopes. A sharp, high-gradient boundary suggests an encapsulated, taboo memory. A diffuse, chaotic boundary indicates a memory that is actively "bleeding" into the surrounding culture, generating turbulence.
  - module: DOMA-137
    excerpt: |
      A "Coherence Dam" where a significant Wound Channel is actively suppressed... corresponds to a deep Coherence Well that the culture refuses to acknowledge... This structure is characterized by an extremely high Boundary Gradient, representing the immense cultural energy expended to maintain the separation between the traumatic memory and the present.
poetic_connections:
  motifs: [scar tissue, cliff edge, shoreline, levee, containment, diffusion, membrane tension]
  evocative_lines:
    - "A sharp, high-gradient boundary suggests an encapsulated, taboo memory."
    - "...a memory that is actively 'bleeding' into the surrounding culture, generating turbulence."
    - "To heal a place, we must first learn to listen to its ghosts."
  association_matrix:
    - [ "COHERENCE_WELL", 0.9 ]
    - [ "TURBULENT_FLOW", 0.7 ]
    - [ "WOUND_CHANNEL", 0.6 ]
    - [ "COHERENCE_DAM", 0.8 ]
formal_mappings:
  candidates:
    - target: Gradient of order parameter (∇φ) at a domain wall
      domain: Condensed Matter
      mapping_kind: conceptual
      equation_hint: |
        Energy density ≈ c₁ (∇φ)² + c₂ (φ² - φ₀²)²
      justification: |
        Mnemonic features act as domains of a different cultural "phase" (e.g., a low-coherence "trauma phase"). Γ measures the sharpness of the "domain wall" separating this phase from the baseline. A high Γ (thin wall) stores significant tension, while a low Γ (thick wall) represents a region of active phase mixing and turbulence.
      references:
        - title: "Principles of Condensed Matter Physics"
          where: "Ch. 7: Defects and Topology"
          date: 2000-09-07
      confidence: 0.7
  adopted:
    - target: Gradient of order parameter (∇φ) at a domain wall
      rationale: The analogy provides a robust physical intuition for the relationship between boundary sharpness, energy storage (cultural tension), and dynamics (turbulence).
      confidence: 0.7
constraints_and_falsifiers:
  claims:
    - statement: "Cultures with Mnemonic Features exhibiting high Boundary Gradients (Γ > Γ_crit) will show a higher incidence of 'flashpoint' conflicts—sudden eruptions triggered by minor provocations at the memory's boundary."
      domain: phenomenology
      falsifier: "Observational data shows no correlation between the measured sharpness (Γ) of a cultural memory's boundary and the nature of social conflicts related to it. Alternatively, low-Γ (diffuse) features are found to be more explosive."
      status: proposed
      links: [DOMA-137]
naming_notes:
  collisions: ["Γ is the standard symbol for the Gamma function, Christoffel symbols (GR), and particle decay rates (QFT)."]
  disambiguation: |
    In the Pirouette Framework, Γ exclusively refers to the spatial gradient of a *coherence anomaly* field, a diagnostic property of the Mnemonic Landscape. It is not a fundamental geometric property of the manifold (like Christoffel symbols) nor a temporal decay rate.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [COHERENCE_MANIFOLD, MNEMONIC_LANDSCAPE, COHERENCE_WELL]
  downstream_effects: [TURBULENT_FLOW, COHERENCE_DAM]
license: CC-BY-SA-4.0
---

# Boundary Gradient

## Canonical (Pirouette)
The Boundary Gradient (Γ) is a scalar field quantity that measures the rate of change of coherence at the boundary of a feature (e.g., a Coherence Well or Plateau) within a Mnemonic Landscape. It quantifies the "steepness" of the transition from the feature's anomalous coherence back to the cultural baseline. High values indicate a sharp, encapsulated boundary, characteristic of taboo or suppressed memories, while low, diffuse values indicate a memory that is actively and often turbulently integrated with the surrounding culture.

## EFT-First Summary
In analogy with condensed matter physics, the Boundary Gradient Γ can be understood as the gradient of a cultural order parameter (Coherence) at the edge of a phase domain (a Mnemonic Feature). It measures the spatial sharpness of the transition between a region of anomalous coherence (e.g., a "trauma phase") and the cultural baseline. A high Γ corresponds to a thin, high-tension "domain wall," while a low Γ corresponds to a thick, diffuse interface where the two phases mix turbulently.

## Glossary Links
- See also: [Mnemonic Landscape](<#>), [Coherence Well](<#>), [Turbulent Flow](<#>)