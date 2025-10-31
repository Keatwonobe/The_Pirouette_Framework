---
term: "RG Coarse-Graining"
canonical_id: "RG_COARSE_GRAINING"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-020"]
---

---
term: RG Coarse-Graining
canonical_id: RG_COARSE_GRAINING
symbol: 
aliases: [Numerical Renormalization Group, RG Flow]
parents: [MATH-020]
children: [MATH-018]
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-020
      lines: "L80-L130"
      snippet: |
        B1 — Flow Definition
        Let couplings g ≡ {λ_Γ, c_K, …}. Define coarse-graining at scale b>1 by averaging Γ over blocks and recomputing effective action S_eff[Γ,K]. Extract β_i ≡ d g_i/d ln μ via matching of 2-point and 4-point vertices.
  editors: [Agent/LLM]
  review_log: []
triad:
  art: |
    As a lens zooms out, the intricate filigree of the world resolves into broad strokes of color and form, revealing the dominant laws that govern the landscape.
  law: |
    The flow of the model's coupling constants (g_i) under a change of scale (μ) is governed by a set of beta functions, β_i ≡ d g_i/d ln μ. Fixed points of this flow, where β(g*)=0, define the stable and unstable macroscopic phases of the theory.
  philosophy: |
    To chart the model's identity across scales, revealing its high-energy origins (UV fixed points) and its low-energy destiny (IR fixed points). This procedure tests the model's consistency and exposes emergent phenomena like confinement or gravitational limits without relying on perturbation theory.
pirouette_definition: |
  A numerical, non-perturbative procedure for determining the scale-dependence of the Pirouette model's coupling constants (g). The model is discretized on a lattice (Ω_L) and, through a block-spin transformation, high-energy modes are integrated out. By measuring n-point vertices (e.g., 2-point and 4-point) on the coarse-grained lattice, an effective action is computed and its couplings (g') are extracted. The differential change in couplings defines the beta function, β(g) = dg/dlnμ, whose flow is integrated to find fixed points (UV, IR), map phases, and compute running observables like α(q²).
operational_definition:
  units: Dimensionless. The procedure maps a set of dimensionless couplings to another set. The scale parameter μ has dimensions of energy.
  symbol_table:
    - name: g_i
      meaning: A vector of coupling constants for the theory (e.g., λ_Γ, c_K).
      dimensions: dimensionless
      default_range: contextual
    - name: μ
      meaning: Renormalization energy scale.
      dimensions: M L^2 T^-2
      default_range: contextual, from lattice cutoff to IR limit
    - name: b
      meaning: Real-space block factor for coarse-graining.
      dimensions: dimensionless
      default_range: b > 1, typically b=2
    - name: β_i(g)
      meaning: Beta function for the coupling g_i.
      dimensions: dimensionless
      default_range: contextual
    - name: g*
      meaning: Vector of coupling constants at a fixed point of the RG flow.
      dimensions: dimensionless
      default_range: contextual
  measurement:
    procedures:
      - name: Lattice Monte-Carlo Block-Spin RG
        outline: |
          1. Discretize the model's action on a lattice Ω_L with spacing `a`.
          2. Use Monte-Carlo methods to generate equilibrium field configurations for a given set of input couplings `g`.
          3. Partition the lattice into blocks of size `b` and compute averaged block fields.
          4. From the statistics of the block fields, compute the 2-point and 4-point correlation functions.
          5. Fit these correlation functions to extract the effective couplings `g'` of the coarse-grained theory.
          6. Compute the beta function β ≈ (g' - g) / ln(b).
          7. Integrate the flow dg/dlnμ = β(g) using numerical solvers (e.g., RK45) to trace the coupling trajectory between the UV and IR.
        expected_signals: [A trajectory of couplings `g(μ)`, identification of fixed points `g*` where `β(g*)=0`, and derived running quantities like Δα_Pir(q²).]
        pitfalls: [Finite size effects from the lattice, critical slowing down near fixed points, statistical errors from Monte-Carlo estimators, systematic errors from the choice of blocking transformation.]
context_windows:
  - module: MATH-020
    excerpt: |
      ...running a coarse-graining renormalization group (RG) flow on (Γ,K) to expose UV/IR structure, confinement‑like behavior, and gravity‑limit phenomenology... Define coarse‑graining at scale b>1 by averaging Γ over blocks and recomputing effective action S_eff[Γ,K]. Extract β_i ≡ d g_i/d ln μ via matching of 2‑point and 4‑point vertices... Integrate flows with adaptive RK45 in ln μ.
poetic_connections:
  motifs: [scale, emergence, universality, fixed points, flow, resolution]
  evocative_lines:
    - "...expose UV/IR structure, confinement-like behavior, and gravity-limit phenomenology."
  association_matrix:
    - [ "UV_COMPLETION", 0.9 ]
    - [ "IR_LIMIT", 0.9 ]
    - [ "PHASE_TRANSITION", 0.8 ]
    - [ "CONFINEMENT", 0.6 ]
formal_mappings:
  candidates:
    - target: Wilson-Kadanoff Renormalization Group
      domain: QFT
      mapping_kind: operational
      equation_hint: |
        S_eff[φ'] = -ln ∫ Dφ_fast exp(-S[φ', φ_fast])
      justification: |
        The procedure in MATH-020 B is a direct numerical implementation of the Wilson-Kadanoff block-spin renormalization group. It involves integrating out high-momentum (short-distance) degrees of freedom by averaging fields on a lattice and observing how the effective couplings of the theory change, which defines the RG flow.
      references:
        - title: "The renormalization group: Critical phenomena and the Kondo problem"
          where: "Rev. Mod. Phys. 47, 773"
          date: 1975-10-01
      confidence: 1.0
  adopted:
    - target: Wilson-Kadanoff Renormalization Group
      rationale: The procedure is a textbook, numerical application of this foundational concept in quantum and statistical field theory.
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "The Pirouette model possesses a non-trivial UV fixed point and flows to an IR fixed point corresponding to a phase with confinement-like behavior."
      domain: theory
      falsifier: "Numerical RG flow diverges or fails to find stable fixed points, indicating the model is not a consistent QFT. Alternatively, the IR fixed point corresponds to a trivial (free) theory, contradicting phenomenological requirements."
      status: under-test
      links: [MATH-020]
naming_notes:
  collisions: [The term "RG" is ubiquitous in physics and requires context.]
  disambiguation: |
    Distinguish from perturbative RG, which uses Feynman diagrams and dimensional regularization to compute beta functions as a power series in the couplings. This is a non-perturbative, numerical method based on real-space blocking on a lattice, valid for both weak and strong coupling.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [COUPLING_CONSTANT]
  downstream_effects: [ALPHA_RUNNING, EDM_SUPPRESSION, CONFINEMENT, IR_LIMIT]
license: CC-BY-SA-4.0
---

# RG Coarse-Graining

## Canonical (Pirouette)
A numerical, non-perturbative procedure for determining the scale-dependence of the Pirouette model's coupling constants (g). The model is discretized on a lattice (Ω_L) and, through a block-spin transformation, high-energy modes are integrated out. By measuring n-point vertices (e.g., 2-point and 4-point) on the coarse-grained lattice, an effective action is computed and its couplings (g') are extracted. The differential change in couplings defines the beta function, β(g) = dg/dlnμ, whose flow is integrated to find fixed points (UV, IR), map phases, and compute running observables like α(q²).

## EFT-First Summary
The Pirouette RG Coarse-Graining is a direct numerical implementation of the Wilson-Kadanoff block-spin renormalization group, a standard non-perturbative tool in Quantum Field Theory. It systematically integrates out high-energy degrees of freedom to determine how the theory's fundamental couplings evolve with energy scale. This reveals the theory's ultimate high-energy (UV) and low-energy (IR) behavior, identifying its stable phases and emergent phenomena.

## Glossary Links
- See also: [ALPHA_RUNNING](./ALPHA_RUNNING.md), [IR_LIMIT](./IR_LIMIT.md)