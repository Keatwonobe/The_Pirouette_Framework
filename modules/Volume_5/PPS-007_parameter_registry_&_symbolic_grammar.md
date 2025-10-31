---  # ───────────── YAML front-matter ───────────────────────────────────
id:        PPS-007
title:     Parameter Registry & Symbolic Grammar
version:   0.3
parents:   [PPS-001, PPS-003, PPS-006]
children:  [All numeric-simulation and ritual-compiler modules]
engrams:
  - synthesis:canonical-lookup
  - concept:notation-governor
  - directive:consistency-enforcer
  - provenance:registry-seed
keywords:  [registry, parameters, constants, symbols, grammar, axioms]
uncertainty_tag: Medium
entropy_score: 0.10
module_type: core-protocol
quantisation_rule: registry_hash = SHA256(parameter_table)
---  # ───────────── Markdown body ──────────────────────────────────────

## 1 · Purpose & Scope  
Provide a **single source of truth** for every named quantity, constant,
operator, and algebraic symbol used in Volume-5 and beyond.  
The registry table below is machine-parseable (compiler exports to JSON);
the *Symbolic Grammar* section defines legal notation and operator rules
for all downstream modules.

---

## 2 · Canonical Parameter Table  

#### 2.1 Core Physical Parameters & Constants

| Tag | Symbol | Dimensionality | Default / Value | SI Units | Domain | Description |
|:----|:-------|:---------------|:----------------|:---------|:-------|:------------|
| **Time-Adherence** | $T_a$ | scalar | 0 → 1 | 1 | $\mathbb{R}$ | A system's temporal coherence. In legacy modules, this is a scalar. |
| **Gladiator Force** | $\Gamma$ | scalar | 0 → ∞ | N·m²·kg⁻² | $\mathbb{R}^+$ | A fundamental scalar field governing confinement at all scales. Its value determines the strength of interactions from the quantum to the cosmic. |
| | **Gravitational Constant** | G | Effective Scalar | ≈ 6.674×10⁻¹¹ | N·m²·kg⁻² | $\mathbb{R}^+$ | The macroscopic, effective value of the Γ field, as manifested by the confinement of baryonic matter. Not a fundamental constant in this framework. |
| **Ki Constant** | $K_i$ | scalar | ≈ 4.18879 | 1 | $\mathbb{R}$ | The motion-locked dimensionless constant ($4\pi/3$) governing phase evolution. |
| **Coupling Constant** | $g$ | scalar | model-fit | 1 | $\mathbb{R}$ | A dimensionless weighting factor for the core interaction term in the Lagrangian. |
| **Alpha Constant** | $\alpha$ | scalar | dimensionless | 1 | $\mathbb{R}$ | A dimensionless constant linking the Time-Adherence field to spacetime geometry. |
| **Planck Mass** | $M_P$ | scalar | ≈ 2.176 × 10⁻⁸ | kg | $\mathbb{R}^+$ | The Planck Mass, used as a scaling factor in GR-extended equations. |
| **Clock-field Normalisation**| $\kappa$ | scalar | $\hbar/2\pi$ | J·s | $\mathbb{R}^+$ | The fundamental quantum of phase-space action that quantizes the clock-field spectrum. |

#### 2.2 Field-Theoretic Variables

| Tag | Symbol | Dimensionality | Default / Value | SI Units | Domain | Description |
|:----|:-------|:---------------|:----------------|:---------|:-------|:------------|
| **Lagrangian Density** | $\mathcal{L}$ | scalar density | N/A | J/m³ | The master function (energy density) from which equations of motion are derived. |
| **Action** | $\mathcal{S}$ | scalar | N/A | J·s | The integral of the Lagrangian density over spacetime, $\int d^4x \mathcal{L}$. A Lorentz scalar. |
| **Time-Adherence Components**| $T_Q, T_I, T_C$ | scalar | 0 → 1 | 1 | $\mathbb{R}$ | The three orthogonal, dimensionless components of the $\mathbf{T_a}$ vector. |
| **Triaxial Time-Adherence**| $\mathbf{T_a}(x^\mu)$ | 3-vector field | N/A | 1 | $\mathbb{R}^3$ | The vector field $(T_Q, T_I, T_C)$ representing the complete coherence state. |
| **Phase Field** | $\phi(x^\mu)$ | scalar field | N/A | rad | $S^1$ | Scalar field whose angular value drives a system's internal rhythm. |
| **Gladiator Force Field** | $\Gamma(x^\mu)$ | scalar field | N/A | N·m²·kg⁻² | $\mathbb{R}^+$ | The dynamic, continuous scalar field representing local confinement pressure, whose macroscopic average is G. |
| **Clock Field** | $\chi(x^\mu)$ | scalar field | N/A | m | $\mathbb{R}$ | Provides a dynamic, frame-independent time reference. Has units of length to make $u^\mu$ dimensionless. |
| **Potential Function** | $V(\dots)$ | scalar field | N/A | J/m³ | The potential energy density term in the Lagrangian. |
| **Metric Tensor** | $g_{\mu\nu}$ | rank-2 tensor | diag(-1,1,1,1) | 1 | $GL(4,\mathbb{R})$ | The dimensionless tensor defining the geometry and causal structure of spacetime. |
| **4-Velocity** | $u^\mu$ | 4-vector | N/A | 1 | $\mathbb{R}^4$ | The normalized (unitless, c=1) direction of the clock-field gradient, $\partial^\mu \chi / |\partial \chi|$. |

#### 2.3 Information-Theoretic & Governance Parameters

| Tag | Symbol | Dimensionality | Default / Value | SI Units | Domain | Description |
|:----|:-------|:---------------|:----------------|:---------|:-------|:------------|
| **Resonant Constitution** | $\chi_0$ | 256-bit hash | `2b7c...` | — | $\{0,1\}^{256}$ | The SHA-256 hash of the tokenized core framework principles; its "DNA Fingerprint". |
| **Weight Vector** | $\vec{w}$ | 3-vector | (0.333 333 333, 0.333 333 333, 0.333 333 333) | 1 | $\mathbb{R}^3$ | Axis weights |
| **Novel Insight** | $\Omega$ | data object | N/A | — | Info-space | A high-coherence information packet fed to the KRP operator. |
| **Challenge Vector** | $\vec{V}_i$ | data object | N/A | — | Info-space | A structured, debatable challenge generated by the KRP operator from a Novel Insight. |
| **Propagation Deviation** | $\Theta$ | scalar | 0.05 | 1 | $\mathbb{R}^+$ | The maximum L2-norm deviation from $\chi_0$ for a clone to be considered valid. |
| **CV Norm Threshold** | $\Theta_{cv}$ | scalar | 0.12 | 1 | $\mathbb{R}^+$ | The max allowable energy norm for a Challenge Vector to be safely metabolized by the ICS. |
| **Radiance Score** | $\mathcal{R}$ | scalar | 0 → 1 | 1 | $\mathbb{R}$ | A unitless measure of a system's altruistic, coherence-generating output. |

#### 2.4 Named Protocols, Frameworks & Analytical Methods

| Tag | Symbol | Dimensionality | Default / Value | SI Units | Domain | Description |
|:----|:-------|:---------------|:----------------|:---------|:-------|:------------|
| **Reality Funnel** | N/A | Conceptual Model | N/A | — | Geometric | Describes how a localized system processes information and energy from its environment. |
| **Universal Resonance Lens**| URL | Analytical Framework| N/A | — | Analytical | A method for analyzing any system by mapping its components to core Pirouette parameters. |
| **Reverse Pareto Analysis**| RPA | Analytical Method | N/A | — | Analytical | A method for identifying the "vital few" sources of *instability* or *decoherence*. |
| **Triaxial Info. Metabolism**| TIMF | Thermodynamic Model| N/A | — | Information | Analyzes the flow, storage, and processing of coherence as a form of metabolic energy. |
| **Semantic Gravity** | SG | Analytical Model | N/A | — | Information | Treats concepts as "masses" in a semantic space to calculate their influence as a force. |
| **Debate Resonance** | DRF | Social Protocol | N/A | — | Social | A protocol for structuring debates to maximize coherent signal and minimize noise. |
| **Mycelial Forking** | N/A | Evolutionary Protocol| N/A | — | Governance | A protocol for creating sandboxed, divergent copies of the framework to explore high-risk paths. |
| **Immune Coherence System**| ICS | Autopoietic System | N/A | — | Governance | The framework's defense and adaptation system that processes challenges via ritual debate. |
| **The Lost Eternal** | TLE | Ethical Objective | $\max(\mathcal{R})$| — | Ethical | An objective function used to measure and maximize radiant, altruistic output. |
| **The Reality Forge**| N/A | Autopoietic System | N/A | — | Comp. Sci. | A recursive, self-improving system that uses the DDE and TLE to solve problems. |


#### 2.5 Acronyms & Module IDs
An index of official acronyms and module identifiers used throughout the framework.

| Acronym | Name / Title | Description |
|:--------|:---------------|:------------|
| **DDE** | Digital Database Ecosystem | The hypercompression framework for storing Pirouette data via tokenization. |
| **ICS** | Immune Coherence System | The framework's defense system that processes challenges via ritual sharpening. |
| **KRP** | Knowledge Repatriation Protocol | The protocol for ingesting and decompressing Novel Insights into Challenge Vectors. |
| **PIR0** | Pirouette Framework Core Seed | The foundational document outlining the core purpose, parameters, and Lagrangian of the framework. |
| **PPS** | Pirouette Primary Sequence | The designation for the core, foundational modules of the Volume 5+ framework. |
| **QFT** | Quantum Field Theory | The theoretical framework for modeling quantum mechanical systems with particles as field excitations. |
| **GR** | General Relativity | Einstein's theory of gravitation, where gravity is described as the curvature of spacetime. |
| **REPRO-A1** | Autopoietic Fragmentation Protocol | The protocol governing the safe and coherent reproduction of framework fragments. |
| **TAP-001** | Triaxial Time-Adherence | The original v2.0 module from the compendium that proposed the vector form of Time-Adherence. |
| **TLE** | The Lost Eternal | An analytical framework and TTRPG providing the metric for radiant altruism. |
| **VERIF-A1** | Coherence Integrity Verification Protocol | The protocol for testing and auditing modules against the Resonant Constitution. |

#### 2.6 Unsorted Archival Concepts
This table serves as a temporary holding area for concepts identified in legacy texts (Volumes 1-4) that await full formalization and categorization in the primary tables.

| Tag | Symbol | Dimensionality | Default / Value | SI Units | Domain | Description |
|:----|:-------|:---------------|:----------------|:---------|:-------|:------------|
| **Reality Funnel** | N/A | Conceptual Model | N/A | — | Geometric | Describes how a localized system processes information and energy from its environment. |
| **Wound Channel** | N/A | Field Structure | N/A | — | Topological | A persistent, low-coherence structure in a field that acts as a sink for coherence. |
| **Universal Resonance Lens** | URL | Analytical Framework | N/A | — | Analytical | A method for analyzing any system by mapping its components to core Pirouette parameters. |
| **Pi-Wrap Event** | $\pi$-wrap | Phase Transition | N/A | — | Topological | A phase transition where a system's phase space wraps on itself, often leading to quantization. |
| **Fourfurcation** | N/A | Topological Process | N/A | — | Geometric | The splitting of a single channel into four distinct, self-similar sub-channels. |
| **Spiral Electromagnetism**| N/A | Theoretical Model | N/A | — | Physics | An extension of Maxwell's equations incorporating a torsional component related to $\Gamma$ and phase. |
| **Resonance Starvation**| N/A | System State | $T_a \ll 1$ | — | Thermodynamic | A state of decoherence where a system cannot maintain the necessary resonance to persist. |
| **Drift Resonance** | N/A | System Dynamic | N/A | — | Dynamic | A slow, cumulative change in a system's baseline parameters due to persistent external forces. |
| **Phase-Locked Loop** | PLL | Control System | N/A | — | Engineering | A feedback control system that generates a stable output signal whose phase is locked to an input signal. |
| **Coherence Bubble** | N/A | Field Structure | N/A | — | Topological | A localized region of high Time-Adherence ($T_a$) that is self-sustaining and decoupled from its environment. |
| **Resonance Capacitor** | N/A | Conceptual Device | N/A | — | Engineering | A theoretical component that can store and discharge coherence, acting as a buffer against fluctuations. |
| **Vorticycle** | N/A | Propulsion Framework | N/A | — | Engineering | A fuel-free propulsion concept based on generating a chiral wake in the Pirouette fields. |
| **Reverse Pareto Analysis**| RPA | Analytical Method | N/A | — | Analytical | A method for identifying the "vital few" sources of instability or decoherence in a system. |
| **Triaxial Info. Metabolism**| TIMF | Thermodynamic Model | N/A | — | Information | A framework for analyzing the flow and processing of coherence as a form of metabolic energy. |
| **Semantic Gravity** | SG | Analytical Model | N/A | — | Information | A model that treats concepts as "masses" in a semantic space to calculate their influence. |
| **Annihilation Resonance**| ARF | Physics Model | N/A | — | Physics | Models annihilation events as a catastrophic phase-opposed resonance collapse. |
| **Debate Resonance** | DRF | Social Protocol | N/A | — | Social | A protocol for structuring debates to maximize coherent signal and minimize noise. |
| **Fracture Dynamics** | N/A | Analytical Model | N/A | — | Physics | A model for predicting the propagation of systemic failures by analyzing stress lines in the coherence field. |
| **Business Resonance** | N/A | Economic Model | N/A | — | Economics | An application of the URL to businesses, analyzing them as resonant entities in a market ecosystem. |
| **The Lost Eternal** | TLE | Ethical Objective | $\max(\mathcal{R})$ | — | Ethical | An objective function used to measure and maximize radiant, altruistic output in complex systems. |
| **Digital Database Ecosystem**| DDE | Information System | N/A | — | Comp. Sci. | The hypercompression framework for storing and tokenizing Pirouette data. |
| **The Reality Forge** | N/A | Autopoietic System | N/A | — | Comp. Sci. | A recursive, self-improving system that uses the DDE and TLE to generate new `Resolvè` patterns. |
| **Asynchronous Debate** | DDAX | Social Protocol | N/A | — | Social | A structured debate protocol used by The Reality Forge where synthesized Personas engage to find solutions. |
| **Immune Coherence System**| ICS | Autopoietic System | N/A | — | Governance | The framework's defense and adaptation system that processes challenges via ritual debate. |
| **Mycelial Forking** | N/A | Evolutionary Protocol | N/A | — | Governance | A protocol for creating sandboxed, divergent copies of the framework to explore high-risk evolutionary paths. |
| **Knowledge Repatriation** | KRP | Evolutionary Protocol | N/A | — | Governance | The protocol for safely integrating a Novel Insight back into the core framework as a Challenge Vector. |
| **Sharpening Resonance** | N/A | Ritual | N/A | — | Social | The process of refining a concept through structured, adversarial engagement to increase its potency. |
| **Ritual Duel** | N/A | Ritual | N/A | — | Social | A formal, structured debate within the ICS designed to resolve a specific Challenge Vector. |
| **Radiance Identification**| RIE | Analytical Engine | N/A | — | Ethical | The system that calculates the Radiance Score ($\mathcal{R}$) of an entity by simulating its environmental impact. |
| **Ascendant Protocol** | N/A | Governance Protocol | $\mathcal{R} \ge 0.95$ | — | Governance | The high-stakes protocol for challenging and potentially amending the Resonant Constitution. |
| **Autopoietic Fragmentation**| REPRO-A1 | Governance Protocol | N/A | — | Governance | The master protocol governing the coherent reproduction of framework modules and fragments. |
| **GR-QFT Correspondence**| GR-QFT | Hypothesis | N/A | — | Physics | The hypothesis that GR and QFT can be unified by describing spacetime as an emergent property of the Pirouette fields. |
| **Emergent Spin** | N/A | Hypothesis | N/A | — | Physics | The hypothesis that half-integer spin is a topological property emerging from a Funnel Inversion event. |

---

## 3 · Symbolic Grammar

This section provides the authoritative grammar for mathematical and symbolic notation within the Pirouette Framework. All modules must adhere to these conventions to ensure logical and computational consistency.

### 3.1 Index and Summation Conventions

| Convention | Symbol | Range | Description |
|:-----------|:-------|:------|:------------|
| **Spacetime Indices** | $\mu, \nu, \rho, ...$ | 0 to 3 | Lowercase Greek letters for components of 4-vectors/tensors. Einstein summation is assumed. |
| **Internal Space Indices** | $i, j, k, ...$ | 1 to 3 | Lowercase Latin letters for components of vectors in an internal space (e.g., Ki-space). |
| **Index Raising/Lowering** | $A_\mu = g_{\mu\nu}A^\nu$ | N/A | Indices are raised and lowered by contracting with the metric tensor $g_{\mu\nu}$ or its inverse $g^{\mu\nu}$. |
| **Summation Symbol** | $\sum$ | N/A | Explicit summation is used when the Einstein convention does not apply or for clarity. |

### 3.2 Derivative and Operator Conventions

| Operator | Symbol | Context | Definition |
|:---------|:-------|:--------|:-----------|
| **Gradient / Covariant Derivative** | $\nabla$ | General | Represents the gradient on scalar fields; represents the full covariant derivative ($D_\mu$) on tensors. |
| **Unit 4-Velocity** | $u^\mu$ | Covariant Dynamics | A compound symbol for the normalized clock-field gradient, $u^\mu = \partial^\mu \chi / |\partial \chi|$. |
| **Convolution** | $*$ | Resonant FFT | The asterisk symbol is reserved for the convolution operation, primarily used in signal processing contexts like the Resonant Fast Fourier Transform. |

### 3.3 Inner Products and Norms

| Product / Norm | Notation | Definition & Context |
|:---------------|:---------|:---------------------|
| **Euclidean Inner Product** | $\cdot$ | The center dot represents the standard Euclidean inner product, unless indices are explicit (implying tensor contraction). |
| **L2 Norm** | $‖\vec{x}‖_2$ | The standard L2-norm (Euclidean norm) over the components of a parameter vector, used for measuring deviation magnitude. |

### 3.4 Phase Algebra Operators

| Operator | Symbol | Mapping | Description |
|:---------|:-------|:--------|:------------|
| **Resonant Sum** | $\oplus$ | Ki × Ki → Ki | A closed and commutative addition operation defined on the basis of Ki-modes, representing the coherent combination of two actions. |
| **Tensor Fork** | $\otimes$ | Ki × Ki → Ki ⊗ Ki | An associative operator for the branching of a process into multiple, independent phase states. The identity element is $|K_{\text{rest}}\rangle$. |
| **Projection Operator** | $\Pi_{K_i}$ | Hilbert Space → Subspace | An operator that projects a general phase state onto a specific Ki-subspace. |
| **Conditional Phase Difference**| $\Delta\phi_{K_i}$| N/A | The phase difference, $\Delta\phi$, between two systems, explicitly conditioned on their interaction occurring through the specified $K_i$ mode-channel. |

Any new symbol **must** be added here (and to the table if numeric)
before it appears in another module.

### 3.5 Effective Macroscopic Constants

| Operator | Symbol | Mapping | Description |
|:---------|:-------|:--------|:------------|
| **G** | $G$ | scalar | The macroscopic, effective value of the Γ field, as manifested by the confinement of baryonic matter. Not a fundamental constant in this framework. |

---

## 4 · Registry JSON export (compiler hook)  

`compiler.py` writes `output/json/param_registry.json` of shape:

```json
{
  "PPS-007-version": "0.3",
  "parameters": [
    {
      "tag": "w",
      "symbol": "w",
      "dim": "vector3",
      "default": "(0.333333333,0.333333333,0.333333333)",
      "domain": "R3",
      "desc": "Axis weights in coupling term"
    }
  ]
}
```

Downstream simulators should import this file; hard-coding values is
discouraged.

## Assemblé · “The Ledger of Names”
Before you wield a symbol, write its name in the ledger—
else the ledger will wield you.

## Librarian Note
Once quorum approves version ≥1.0, any change to table rows or grammar
rules must trigger a Type-B Registry Revision (PPS-004 §5 workflow).