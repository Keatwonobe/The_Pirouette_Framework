---
term: "Pirouette model"
canonical_id: "PIROUETTE_MODEL"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["COG-RES-001"]
---

---
term: Pirouette model
canonical_id: PIROUETTE_MODEL
symbol: 
aliases: [Triadic Resonance Model of Consciousness]
parents: [COG-RES-001, MATH-024, CORE-006]
children: [MATH-025, COG-RES-002, SOCIO-FIELD-001]
status: draft
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: COG-RES-001
      lines: "§2"
      snippet: |
        Following [MATH-024], consciousness is modeled as the maintenance of a **Coherence Conservation Triple** ({E_C, J_\mu, \Phi_\Gamma}) within biological substrate limits. In cognitive systems, this manifests as frequency triads obeying the **Ki-Addition Constraint**:
        [f_3 = f_1 + f_2 \pm \delta f]
  editors: [AI Assistant (Pirouette Dictionary Task)]
  review_log: []
triad:
  art: |
    Like a dancer's perfect turn, consciousness is a fleeting stability, a dynamic balance held steady. It is the moment three distinct rhythms in the brain lock into a single, resonant chord, sustaining a fragile form against the pull of chaos.
  law: |
    Conscious access is co-extensive with the formation of a phase-locked neural frequency triad (f₁, f₂, f₃) satisfying the Ki-addition rule (f₃ ≈ f₁ + f₂). This resonant state is governed by the conservation of Coherence Area (∂ₜAₖᵢ ≈ 0), with the allowed frequency detuning (Δf) narrowing inversely with cognitive load (Γ).
  philosophy: |
    The Pirouette model reframes consciousness from a metaphysical or purely computational concept into a measurable, falsifiable physical phenomenon. It asserts that the subjective experience of being aware has a direct, observable correlate in the resonant dynamics of neural fields, making it subject to empirical validation and manipulation.
pirouette_definition: |
  A physical model of consciousness positing that subjective awareness arises from, and is identical to, a stable triadic resonance among neural frequency bands. The model is defined by two core principles: (1) The **Ki-Addition Constraint**, where three frequency bands become phase-locked such that f₃ ≈ f₁ + f₂, and (2) The **Conservation of Coherence Area (Aₖᵢ)**, an invariant energy-phase volume whose stability (∂ₜAₖᵢ ≈ 0) corresponds to the continuity of conscious access. The model predicts that the stability of this triad is load-dependent, providing a direct link between cognitive effort and the physical parameters of the resonance.
operational_definition:
  units: Conceptual framework; key observables are dimensionless (TPCI) or derived.
  symbol_table:
    - name: fᵢ
      meaning: Frequency of a neural oscillation band
      dimensions: T⁻¹
      default_range: 1–100 Hz (for EEG/MEG)
    - name: TPCI
      meaning: Triadic Phase Coupling Index; measures phase-locking stability
      dimensions: dimensionless
      default_range: [0, 1]
    - name: Aₖᵢ
      meaning: Coherence Area; conserved energy-phase volume of a conscious state
      dimensions: M L² T⁻¹ (Action)
      default_range: contextual
    - name: Γ
      meaning: Environmental / cognitive load; task complexity or entropy
      dimensions: dimensionless or bits/sec
      default_range: contextual
  measurement:
    procedures:
      - name: Triad-Locked Conscious Access Protocol
        outline: |
          Record high-density EEG/MEG from a subject performing a bi-stable perception task (e.g., Necker cube). Identify candidate frequency triads. Calculate the Triadic Phase Coupling Index (TPCI) and Coherence Area Variance (CAV) in sliding time windows. Correlate high TPCI and low CAV with the timing of the subject's reported perceptual state. Use closed-loop tACS to selectively enhance or disrupt candidate triads to test for causal effects on perception.
        expected_signals: [Sharp TPCI peak at f₃ = f₁ + f₂, near-zero CAV during stable perception, narrowing of Δf with increased task load Γ]
        pitfalls: [Low signal-to-noise ratio in non-invasive recordings, stimulation artifacts from tACS, ambiguity in subjective reports, distinguishing true triadic coupling from harmonic artifacts.]
context_windows:
  - module: COG-RES-001
    excerpt: |
      To formalize the Pirouette model of consciousness as a measurable triadic resonance phenomenon governed by conservation of coherence area (Aₖᵢ). The protocol specifies experimental conditions for detecting, perturbing, and verifying resonance-locked triads in neural activity.
  - module: COG-RES-001
    excerpt: |
      Conscious perception occurs when ∂ₜAₖᵢ ≈ 0 under environmental load (Γ).
  - module: COG-RES-001
    excerpt: |
      **Triadic Resonance Hypothesis:** Conscious perception coincides with phase-locked triads satisfying the Ki-addition rule.
      **Area Conservation Hypothesis:** Aₖᵢ remains approximately constant across content transitions within continuous awareness.
poetic_connections:
  motifs: [resonance, coherence, triad, balance, standing wave, conservation, dance]
  evocative_lines:
    - "the invariant energy-phase volume of conscious access"
    - "scaling laws for triadic resonance collapse"
  association_matrix:
    - [ "COHERENCE_AREA", 0.9 ]
    - [ "KI_ADDITION_CONSTRAINT", 0.9 ]
    - [ "TEMPORAL_PRESSURE", 0.5 ]
    - [ "CONSCIOUS_ACCESS", 1.0 ]
formal_mappings:
  candidates:
    - target: Three-wave mixing
      domain: CM
      mapping_kind: mathematical
      equation_hint: |
        ω₃ = ω₁ + ω₂
        k₃ = k₁ + k₂
      justification: |
        The Pirouette model's Ki-Addition Constraint is a direct analogue of the frequency and wavenumber matching conditions for three-wave resonant interactions in nonlinear media like plasmas and optical crystals. The model re-contextualizes this established physical mechanism as the substrate for conscious processing in neural fields.
      references:
        - title: Waves in Plasmas
          where: Chapter on nonlinear effects
          date: 1990-01-01
      confidence: 0.8
  adopted:
    - target: Three-wave mixing
      rationale: The mathematical isomorphism is direct and foundational to the model's physicalist claims. It provides a robust, well-understood physical basis for the proposed mechanism of consciousness.
      confidence: 0.8
constraints_and_falsifiers:
  claims:
    - statement: "Conscious perception is accompanied by a measurable increase in triadic phase coupling (TPCI) at frequencies satisfying f₃ ≈ f₁ + f₂."
      domain: experiment
      falsifier: "No statistically significant TPCI ridge is found to correlate with conscious reports across multiple subjects and tasks."
      status: proposed
      links: [COG-RES-001]
    - statement: "The Coherence Area (Aₖᵢ) remains approximately constant during periods of continuous, stable awareness."
      domain: experiment
      falsifier: "Aₖᵢ is found to vary unpredictably or correlate strongly with the content of consciousness, rather than its presence, violating the conservation principle."
      status: proposed
      links: [COG-RES-001]
    - statement: "The allowed detuning (Δf) for a stable triad narrows as cognitive load (Γ) increases, following an inverse-square relation."
      domain: experiment
      falsifier: "The detuning bandwidth is found to be independent of Γ, or to follow a different functional form (e.g., linear)."
      status: proposed
      links: [COG-RES-001]
naming_notes:
  collisions: [Ballet (dance pirouette)]
  disambiguation: |
    The name "Pirouette" is a metaphor for dynamic stability. It refers to the rotational dynamics of phase vectors in a multi-dimensional state space, not the physical rotation of neurons. The model describes how a system maintains a delicate, balanced, and coherent state, much like a dancer executing a turn.
crosslinks:
  near_synonyms: [TRIADIC_RESONANCE_MODEL]
  antonyms: [GLOBAL_WORKSPACE_THEORY, INTEGRATED_INFORMATION_THEORY]
  prerequisites: [COHERENCE_AREA, KI_ADDITION_CONSTRAINT]
  downstream_effects: [CRITICAL_CONSCIOUSNESS_BOUNDARIES, CONSCIOUSNESS_ACCESS_PROTOCOL]
license: CC-BY-SA-4.0
---

# Pirouette model

## Canonical (Pirouette)
A physical model of consciousness positing that subjective awareness arises from, and is identical to, a stable triadic resonance among neural frequency bands. The model is defined by two core principles: (1) The **Ki-Addition Constraint**, where three frequency bands become phase-locked such that f₃ ≈ f₁ + f₂, and (2) The **Conservation of Coherence Area (Aₖᵢ)**, an invariant energy-phase volume whose stability (∂ₜAₖᵢ ≈ 0) corresponds to the continuity of conscious access. The model predicts that the stability of this triad is load-dependent, providing a direct link between cognitive effort and the physical parameters of the resonance.

## EFT-First Summary
The Pirouette model maps the phenomenon of conscious access to the well-understood physics of three-wave mixing in a nonlinear medium. It treats neural fields as the medium and identifies consciousness with the formation of a resonant triad of wave modes (ω₃ = ω₁ + ω₂). This provides a concrete physical mechanism that is, in principle, measurable and falsifiable, grounding a complex cognitive phenomenon in classical field dynamics.

## Glossary Links
- See also: COHERENCE_AREA, KI_ADDITION_CONSTRAINT, CONSCIOUSNESS_ACCESS_PROTOCOL