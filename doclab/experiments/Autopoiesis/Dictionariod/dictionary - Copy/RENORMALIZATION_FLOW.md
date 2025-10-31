---
term: "Renormalization Flow"
canonical_id: "RENORMALIZATION_FLOW"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["COG-RES-003"]
---

---
term: Renormalization Flow
canonical_id: RENORMALIZATION_FLOW
symbol: β_κ
aliases: [RG Flow, Curvature Flow]
parents: [COG-RES-003, MATH-026]
children: [DOMA-096]
status: draft
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: COG-RES-003
      lines: "§7"
      snippet: |
        As Γ increases, manifold curvature evolves under renormalization:
        [dκ/dlnℓ = β_κ = (2−d)κ − c₁ bκ + c₂ g²]
        * Below critical Γ_c: curvature flows to fixed point κ* (stable awareness).
        * At Γ_c: κ diverges, producing manifold tearing (awareness collapse).
  editors: [system-ai-alpha]
  review_log: []
triad:
  art: |
    The map of the mind is not static; under the pressure of thought, its landscape warps. Mountains rise and valleys deepen, flowing toward either serene plains or catastrophic fractures, all dictated by the scale of observation.
  law: |
    The change in the Triadic Manifold's local curvature (κ) with respect to changes in observational scale (ℓ, proxied by cognitive load Γ) is governed by a beta function (β_κ). This flow dictates whether the manifold approaches a stable, flat geometry (coherent awareness) or a divergent, singular geometry (awareness collapse).
  philosophy: |
    This concept establishes that the very structure of conscious experience is not a fixed stage but a dynamic medium whose complexity is self-organizing. It provides a formal mechanism for both the stability of awareness under low load and its catastrophic failure and reconfiguration under high load, linking cognitive phenomena to the universal principles of scale-invariance found in physical systems.
pirouette_definition: |
  The process by which the effective local curvature (κ) of the Triadic Manifold (𝓜₃) evolves under a change of scale (ℓ). This scale is contextually interpreted as the inverse of cognitive load (Γ). The flow is described by the beta function β_κ, which determines the trajectory of κ in the space of possible manifold geometries. The fixed points of this flow correspond to stable states of awareness, while divergences signal critical transitions, such as awareness collapse or the nucleation of new coherent states.
operational_definition:
  units: dimensionless
  symbol_table:
    - name: β_κ
      meaning: Beta function for manifold curvature.
      dimensions: dimensionless
      default_range: contextual
    - name: κ
      meaning: Local curvature of the Triadic Manifold 𝓜₃.
      dimensions: dimensionless
      default_range: "[0, ∞)"
    - name: ℓ
      meaning: Observational scale parameter, inversely related to cognitive load.
      dimensions: dimensionless
      default_range: contextual
    - name: Γ
      meaning: Cognitive Load.
      dimensions: dimensionless
      default_range: contextual
    - name: d
      meaning: Effective dimensionality of the manifold.
      dimensions: dimensionless
      default_range: "[2, 3]"
    - name: g, b, c₁, c₂
      meaning: Coupling constants from the Triadic Potential Field V.
      dimensions: dimensionless
      default_range: contextual
  measurement:
    procedures:
      - name: Dynamic Curvature Tracking under Load
        outline: |
          1. Record neural phase data (e.g., via high-density EEG) from a subject performing a task with variable, quantifiable cognitive load (Γ).
          2. For short time windows, identify resonant triads and construct the local Triadic Manifold 𝓜₃.
          3. Calculate the local curvature κ(t) from the manifold's metric tensor.
          4. Bin the calculated κ values by the corresponding Γ value at that time.
          5. Plot the average change in κ as a function of increasing Γ to approximate the flow β_κ.
        expected_signals: [EEG/MEG phase angles (Φ₁, Φ₂, Φ₃), Task-evoked cognitive load Γ(t)]
        pitfalls: [Phase unwrapping errors, insufficient triad density for stable manifold construction, difficulty in isolating Γ from other cognitive variables.]
context_windows:
  - module: COG-RES-003
    excerpt: |
      As Γ increases, manifold curvature evolves under renormalization: [dκ/dlnℓ = β_κ]. Below the critical load Γ_c, curvature flows to a stable fixed point κ*, corresponding to stable awareness. At Γ_c, κ diverges, producing manifold tearing, which represents awareness collapse.
  - module: COG-RES-003
    excerpt: |
      This module... formalizes consciousness as motion along coherence geodesics constrained by Pirouette’s renormalization flow. The path of awareness corresponds to a geodesic on 𝓜₃, but the geometry of the manifold itself is not static; it deforms under cognitive load according to the RG flow derived from [MATH-026].
poetic_connections:
  motifs: [manifold tearing, scale invariance, cognitive landscape, phase transition]
  evocative_lines:
    - "At Γ_c: κ diverges, producing manifold tearing (awareness collapse)."
    - "curvature flows to fixed point κ* (stable awareness)."
  association_matrix:
    - [ "TRIADIC_MANIFOLD", 0.9 ]
    - [ "COGNITIVE_LOAD", 0.8 ]
    - [ "AWARENESS_COLLAPSE", 0.7 ]
    - [ "CADUCEUS_FLOW", 0.5 ]
formal_mappings:
  candidates:
    - target: Renormalization Group (RG) Flow / Beta Function β(g)
      domain: EFT|Math
      mapping_kind: mathematical
      equation_hint: |
        dκ/d(ln ℓ) = β_κ  <-->  d(g)/d(ln μ) = β(g)
      justification: |
        The Pirouette framework's Renormalization Flow is a direct mathematical analogue of RG flow in quantum and statistical field theory. It maps a system parameter (manifold curvature κ) to a physical coupling constant (g), and maps the observational scale (ℓ) or cognitive load (Γ) to the energy/momentum scale (μ). The beta function β_κ governs the evolution of the system's "effective theory" of consciousness as the scale of analysis changes.
      references:
        - title: The theory of critical phenomena
          where: Rev. Mod. Phys. 46, 597
          date: 1974-10-01
      confidence: 0.95
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The local curvature κ of the Triadic Manifold exhibits scale-dependent behavior consistent with a beta function, flowing toward a stable fixed point κ* under low cognitive load (Γ < Γ_c)."
      domain: phenomenology
      falsifier: "Experimental measurements show κ is either independent of Γ or changes in a manner inconsistent with a flow-to-fixed-point dynamic (e.g., random fluctuations, linear increase without saturation)."
      status: proposed
      links: [COG-RES-003]
    - statement: "There exists a critical cognitive load Γ_c at which the manifold curvature κ diverges, corresponding to a measurable awareness transition or collapse."
      domain: experiment
      falsifier: "Under maximal cognitive load, subjects report awareness collapse, but concurrent neuro-geometric analysis shows that κ remains bounded and the manifold topology remains intact."
      status: proposed
      links: [COG-RES-003]
naming_notes:
  collisions: [Caduceus Flow (describes motion *on* the manifold, not evolution *of* the manifold)]
  disambiguation: |
    Renormalization Flow describes how the *geometry of the manifold itself* changes with scale (cognitive load). This is distinct from Geodesic Motion or Caduceus Flow, which describe the path of awareness *across* a given, static manifold geometry. The Renormalization Flow is a "meta-dynamic" that governs the space in which other dynamics unfold.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [TRIADIC_MANIFOLD, COGNITIVE_LOAD]
  downstream_effects: [AWARENESS_COLLAPSE, CADUCEUS_FLOW]
license: CC-BY-SA-4.0
---

# Renormalization Flow

## Canonical (Pirouette)
The Renormalization Flow is the process governing how the effective local curvature (κ) of the Triadic Manifold (𝓜₃) evolves under a change of observational scale (ℓ), which is inversely related to cognitive load (Γ). This evolution is described by a beta function, β_κ, which dictates whether the manifold's geometry flows towards a stable, low-curvature state (indicative of coherent awareness) or diverges towards a singularity (indicative of awareness collapse). The flow's fixed points define the stable geometric configurations available to consciousness.

## EFT-First Summary
Analogous to the Renormalization Group (RG) flow in Effective Field Theory, this process describes how a fundamental parameter of the "theory of consciousness"—the manifold's curvature κ—changes as the energy scale (cognitive load Γ) is varied. The beta function, `dκ/d(ln ℓ) = β_κ`, determines the system's behavior. At low energies (low load), the curvature flows to an infrared (IR) fixed point, representing a stable, large-scale conscious state. At a critical energy (Γ_c), the flow diverges, signaling a phase transition where the geometric description breaks down, corresponding to awareness collapse.

## Glossary Links
- See also: [TRIADIC_MANIFOLD](<link>), [COGNITIVE_LOAD](<link>), [AWARENESS_COLLAPSE](<link>)