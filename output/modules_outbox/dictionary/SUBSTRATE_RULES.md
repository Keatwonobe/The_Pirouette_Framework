---
term: "Substrate Rules"
canonical_id: "SUBSTRATE_RULES"
symbol: ""
aliases: [SR-0…6]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DYNA-SUBST-001_pirouette_substrate_rules"]
---

---
term: Substrate Rules
canonical_id: SUBSTRATE_RULES
symbol: SR-0…6
aliases: [SR-0, SR-1, SR-2, SR-3, SR-4, SR-5, SR-6, The Constitution of the Temporal Medium]
parents: [DYNA-SUBST-001]
children: [MATH-GR-001, DYNA-GR-002, GRW-003, COSMO-GR-004, MATH-YM-001, MATH-YM-002, DYNA-WEAK-001, DYNA-COLOR-001, XXP-GR-EXP]
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DYNA-SUBST-001_pirouette_substrate_rules
      snippet: |
        These axioms form the **constitution of the temporal medium**.
        All downstream modules must explicitly reference which SR-k they consume.
  editors: [auto-agent]
  review_log: []
triad:
  art: |
    If particles are knots in time and forces are how those knots keep clocks in step, then spacetime is the loom—the elastic weave of coherence they all move through. GR is the loom’s equation of state. At human scales it looks perfect; at the coherence barrier you can hear the faint creak of the wood—Γ—setting the timbre of the universe.
  law: |
    The six Substrate Rules are the immutable, axiomatic constitution of the temporal medium. They dictate that spacetime is an emergent elastic response, gauge forces are frame-relabeling symmetries, and UV sensitivity is physically capped at the coherence barrier ω_c, collectively determining all effective constants and ensuring GR and the Standard Model emerge as the low-energy effective field theory.
  philosophy: |
    The Substrate Rules provide a unified, causal foundation for both general relativity and quantum field theory by positing a single underlying medium. Their purpose is to replace fine-tuned postulates with a minimal set of physical axioms from which the observed universe, its symmetries, and its constants are emergent and interconnected consequences.
pirouette_definition: |
  The Substrate Rules are the set of six immutable axioms (SR-0 to SR-6) that define the Pirouette temporal medium. They establish:
  - **SR-0 (Existence):** Reality is a temporal medium described by an order parameter Φ and pressure Γ.
  - **SR-1 (Gauge):** Symmetries of the Standard Model arise from local relabeling of internal temporal frames.
  - **SR-2 (Coherence):** A conservation law on the substrate ensures the emergence of a Lorentz-invariant manifold.
  - **SR-3 (Finiteness):** A physical UV cutoff, the coherence barrier ω_c, saturates quantum corrections and removes fine-tuning.
  - **SR-4 (Elasticity):** The spacetime metric g_μν and cosmological constant Λ_Pirouette are defined by the medium's elastic response to gradients.
  - **SR-5 (Universality):** All matter couples minimally to this single emergent metric.
  - **SR-6 (Closure):** Cross-scale relations bind microphysical constants (like ω_c) to macrophysical ones (like G_eff), ensuring the system's self-consistency.
operational_definition:
  units: Axiomatic / Dimensionless
  symbol_table:
    - name: SR-k
      meaning: An individual rule from the set {0, ..., 6}.
      dimensions: Dimensionless
      default_range: k ∈ {0, 1, 2, 3, 4, 5, 6}
    - name: g_μν
      meaning: Effective metric tensor, an emergent property defined by SR-4.
      dimensions: Dimensionless
      default_range: Spacetime metric
    - name: ω_c
      meaning: Coherence barrier, the physical UV cutoff defined by SR-3.
      dimensions: T⁻¹
      default_range: ~ Planck frequency
  measurement:
    procedures:
      - name: Indirect Verification via Consequence Testing
        outline: |
          The Substrate Rules are axioms and not directly measured. Their validity is tested by verifying their physical consequences. This involves precision experiments designed to detect deviations from the predictions of General Relativity and the Standard Model that are forbidden by the Rules.
        expected_signals: [Null results in tests for Lorentz violation (validates SR-2), Luminal and transverse-tensor-only gravitational waves (validates SR-4), Composition-independent free fall (validates SR-5)]
        pitfalls: [Misattributing systemic experimental error to a violation of the Rules, Tests lacking the required precision to probe predicted barrier-scale effects]
context_windows:
  - module: DYNA-SUBST-001
    excerpt: |
      To define the **substrate of Pirouette**—the temporal medium from which spacetime, gauge interactions, and matter arise as excitations and frame-connections. This module establishes immutable axioms (SR-0…6), links them to emergent General Relativity and the SU(3)×SU(2)×U(1) gauge structure, and centralizes all falsifiable predictions involving \(G_{\rm eff}\), \(\Lambda_{\rm Pirouette}\), and the coherence barrier \(\omega_c\).
  - module: DYNA-SUBST-001
    excerpt: |
      **SR-6 — Autopoietic Closure**
      Cross-scale invariants from the Bridge bind micro ↔ macro:
      \[ G_{\rm eff}^{-1}\sim \frac{\omega_c^2}{8\pi\Lambda_{\rm Pirouette}}, \qquad \{\alpha,\alpha_2,\alpha_3\}\leftrightarrow\text{stiffness ratios.} \]
      These axioms form the **constitution of the temporal medium**. All downstream modules must explicitly reference which SR-k they consume.
poetic_connections:
  motifs: [constitution, axiom, emergence, elasticity, coherence, autopoiesis]
  evocative_lines:
    - "spacetime is the loom—the elastic weave of coherence"
    - "These axioms form the constitution of the temporal medium."
  association_matrix:
    - [ "TEMPORAL_MEDIUM", 0.9 ]
    - [ "EMERGENT_METRIC", 0.8 ]
    - [ "GAUGE_EMERGENCE", 0.8 ]
    - [ "COHERENCE_BARRIER", 0.7 ]
    - [ "AUTOPOIETIC_CLOSURE", 0.6 ]
formal_mappings:
  candidates:
    - target: Analogue Gravity Models
      domain: GR
      mapping_kind: conceptual
      equation_hint: |
        g_eff^μν ∝ c_s⁻² v^μ v^ν + (g_background^μν - v^μ v^ν)
      justification: |
        SR-4 posits that the spacetime metric is an effective description of the substrate's elastic response, analogous to how sound waves in a fluid experience an effective acoustic metric determined by the fluid's properties.
      references:
        - title: Living Rev. Relativ. 14, 3 (2011)
          where: "Analogue Gravity"
          date: 2011-01-01
      confidence: 0.8
    - target: Gauge Principle
      domain: QFT
      mapping_kind: conceptual
      equation_hint: |
        D_μ = ∂_μ - i g A_μ
      justification: |
        SR-1 provides a physical origin for gauge symmetries as redundancies in the description of the underlying temporal frames, moving them from a purely mathematical postulate to an emergent physical property.
      references: []
      confidence: 0.9
    - target: UV/IR Mixing & Swampland Conjectures
      domain: EFT
      mapping_kind: conceptual
      justification: |
        SR-6 (Autopoietic Closure) functions like a swampland conjecture by imposing non-trivial relationships between low-energy (IR) constants like G_eff and high-energy (UV) scales like ω_c, constraining the allowed parameter space of the low-energy effective theory.
      references: []
      confidence: 0.7
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "Gravitational waves have exactly two tensor polarizations and travel at the luminal speed c, with any dispersion suppressed by (ω/ω_c)²."
      domain: experiment
      falsifier: "Detection of extra GW polarizations (scalar, vector) or a measurable, frequency-dependent speed of gravity."
      status: under-test
      links: [XXP-GR-EXP]
    - statement: "The Weak Equivalence Principle is exact; free fall is composition-independent."
      domain: experiment
      falsifier: "Any observation of differential acceleration between objects of different composition in the same gravitational field."
      status: supported
      links: [XXP-GR-EXP]
    - statement: "Fundamental constants like G_eff and α exhibit at most an ultra-slow, correlated drift, with |Ġ/G| < 10⁻¹³ yr⁻¹."
      domain: phenomenology
      falsifier: "Measurement of a larger drift, a drift with the opposite sign predicted by the Bridge, or uncorrelated drifts."
      status: under-test
      links: [XXP-GR-EXP]
    - statement: "Gauge Ward identities are exact below the coherence barrier ω_c."
      domain: theory
      falsifier: "Discovery of species-dependent gauge couplings or non-conserved gauge currents in the low-energy regime."
      status: supported
      links: []
naming_notes:
  collisions: []
  disambiguation: |
    "Substrate Rules" refers specifically to the foundational, immutable set of axioms {SR-0, ..., SR-6}. It should not be confused with dynamical laws or equations of motion derived in downstream modules, which are consequences of these rules rather than the rules themselves.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [TEMPORAL_MEDIUM, TEMPORAL_PRESSURE]
  downstream_effects: [EMERGENT_METRIC, GAUGE_EMERGENCE, COHERENCE_BARRIER, AUTOPOIETIC_CLOSURE]
license: CC-BY-SA-4.0
---

# Substrate Rules

## Canonical (Pirouette)
The Substrate Rules are the set of six immutable axioms (SR-0 to SR-6) that define the Pirouette temporal medium. They establish:
- **SR-0 (Existence):** Reality is a temporal medium described by an order parameter Φ and pressure Γ.
- **SR-1 (Gauge):** Symmetries of the Standard Model arise from local relabeling of internal temporal frames.
- **SR-2 (Coherence):** A conservation law on the substrate ensures the emergence of a Lorentz-invariant manifold.
- **SR-3 (Finiteness):** A physical UV cutoff, the coherence barrier ω_c, saturates quantum corrections and removes fine-tuning.
- **SR-4 (Elasticity):** The spacetime metric g_μν and cosmological constant Λ_Pirouette are defined by the medium's elastic response to gradients.
- **SR-5 (Universality):** All matter couples minimally to this single emergent metric.
- **SR-6 (Closure):** Cross-scale relations bind microphysical constants (like ω_c) to macrophysical ones (like G_eff), ensuring the system's self-consistency.

## EFT-First Summary
In the language of effective field theory, the Substrate Rules provide a physical UV completion for General Relativity and the Standard Model. They posit that the observed spacetime and gauge symmetries are not fundamental but emergent properties of an underlying 'temporal medium,' akin to an analogue gravity system (SR-4). The gauge principle arises from descriptive redundancies in this medium (SR-1), while a finite physical cutoff, the coherence barrier ω_c, regularizes quantum loops and forbids fine-tuning (SR-3). The rules impose self-consistency conditions, similar to swampland conjectures, that link UV and IR scales (SR-6), yielding testable predictions for gravitational wave properties and the (non)variation of fundamental constants.

## Glossary Links
- See also: Temporal Medium, Coherence Barrier, Emergent Metric, Autopoietic Closure