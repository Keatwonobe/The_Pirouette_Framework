---
term: "Curl Component"
canonical_id: "CURL_COMPONENT"
symbol: "∇ × **A**"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["SOCIO-FIELD-002"]
---

---
term: Curl Component
canonical_id: CURL_COMPONENT
symbol: ∇ × **A**
aliases: [antagonistic circulation, solenoidal dissonance]
parents: [SOCIO-FIELD-001, MATH-024]
children: [DOMA-096, SOCIO-POLICY-001]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: SOCIO-FIELD-002
      lines: "§2"
      snippet: |
        In social contexts, deviations from this balance manifest as curl-dominant distortions of the dissonance field (**D**):
        [**D** = ∇φ + ∇ × **A**]
  editors: [auto-generator]
  review_log: []
triad:
  art: |
    A hidden whirlpool in the river of social intent. It is the tangled current that pulls systems apart, turning shared motion into a self-consuming vortex.
  law: |
    A system undergoes irreversible coherence collapse when the mean-squared curl component (Θ = ⟨|∇ × **A**|²⟩) exceeds a domain-specific critical threshold (Θc), indicating that antagonistic circulation has overwhelmed cooperative potential flow.
  philosophy: |
    To isolate and quantify the non-cooperative, rotational dynamics within a system. It represents systemic friction and wasted energy, providing a direct target for interventions designed to restore laminar, potential-driven coherence.
pirouette_definition: |
  The rotational, non-conservative component (∇ × **A**) of the dissonance field (**D**). It represents localized, circulating patterns of antagonistic social interaction that are mathematically orthogonal to cooperative, potential-driven flows (∇φ). Its squared magnitude, averaged over a coherence-critical region (Ωc), defines the Curl Threshold (Θ), a primary indicator of imminent systemic instability and cascade failure.
operational_definition:
  units: Dimensionless after normalization by network density.
  symbol_table:
    - name: ∇ × **A**
      meaning: The Curl Component; the rotational part of the dissonance field.
      dimensions: Contextual; typically [Interaction] / [Area]
      default_range: contextual
    - name: **A**
      meaning: The antagonistic vector potential.
      dimensions: Contextual; typically [Interaction] / [Length]
      default_range: contextual
    - name: **D**
      meaning: The total dissonance field.
      dimensions: Same as ∇ × **A**
      default_range: contextual
    - name: Θ
      meaning: The Curl Threshold parameter; mean-squared curl magnitude.
      dimensions: dimensionless
      default_range: "[0, ∞); critical transitions often occur near Θc ≈ 1"
  measurement:
    procedures:
      - name: Local Curl Estimation from Interaction Graphs
        outline: |
          Compute the antagonistic vector potential **A** from residual flow in social interaction graphs (mobility, communication, economic). Apply a finite-difference curl operator over the graph lattice. Normalize the result by local network density to yield a dimensionless measure of Θ.
        expected_signals: [Rising low-frequency variance in Θ(t) pre-shock, Cross-scale locking of Θ during state transition, Sharp peak in information entropy of transactions as Θ approaches Θc]
        pitfalls: [High signal noise obscuring precursor oscillations, Misidentification of the coherence-critical region (Ωc), Aliasing from insufficient temporal sampling of the interaction graph]
context_windows:
  - module: SOCIO-FIELD-002
    excerpt: |
      In social contexts, deviations from this balance manifest as curl-dominant distortions of the dissonance field (**D**): [**D** = ∇φ + ∇ × **A**]. When the curl component exceeds a critical magnitude, local coherence collapse propagates nonlinearly---analogous to vortex shedding in fluid dynamics.
  - module: SOCIO-FIELD-002
    excerpt: |
      The system enters cascade mode when: [Θ > Θc = k_Γ (⟨|∇φ|²⟩ / ⟨|**A**|²⟩)]. This expresses that instability occurs when antagonistic circulation overpowers cooperative potential by a factor exceeding k_Γ.
poetic_connections:
  motifs: [vortex, turbulence, friction, cascade, antagonism, eddy]
  evocative_lines:
    - "antagonistic circulation overpowers cooperative potential"
    - "local coherence collapse propagates nonlinearly"
  association_matrix:
    - [ "DISSONANCE_FIELD", 0.9 ]
    - [ "CURL_THRESHOLD", 0.8 ]
    - [ "COHERENCE", -0.7 ]
    - [ "TEMPORAL_PRESSURE", 0.5 ]
formal_mappings:
  candidates:
    - target: Vorticity (**ω** = ∇ × **v**)
      domain: CM (Fluid Dynamics)
      mapping_kind: conceptual
      equation_hint: |
        **D** → **v** ; ∇ × **A** → **ω**
      justification: |
        The Curl Component represents local, rotational flow within a field, directly analogous to vorticity in a fluid. The source module uses fluid dynamics metaphors ("vortex shedding", "circulation") to describe its behavior, particularly its role in driving transitions to instability (turbulence).
      references: []
      confidence: 0.8
    - target: Magnetic Field (**B** = ∇ × **A**)
      domain: EM (Electromagnetism)
      mapping_kind: mathematical
      equation_hint: |
        **D** → **E** + **B** ; ∇ × **A** → **B**
      justification: |
        The mathematical structure is identical to the definition of the magnetic field **B** from the magnetic vector potential **A**. This mapping highlights the "field" nature of the component and its origin from a potential, but the physical analogy is less direct than vorticity.
      references: []
      confidence: 0.6
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The mean-squared curl component (Θ) possesses a predictable, domain-invariant critical threshold (Θc) that signals the onset of systemic coherence collapse."
      domain: phenomenology
      falsifier: "If Θc cannot be consistently determined across different social systems or if it fails to predict instability, the model's universality claim is invalid."
      status: proposed
      links: [SOCIO-FIELD-002]
    - statement: "The Curl Component is a non-stochastic feature of the dissonance field, exhibiting precursor oscillations before critical transitions."
      domain: theory
      falsifier: "If time-series analysis shows Θ(t) behaves as uncorrelated noise without predictive power, the underlying model of coherence flow conservation is incorrect."
      status: proposed
      links: [SOCIO-FIELD-002]
naming_notes:
  collisions: [The symbol ∇ × **A** is formally identical to the definition of the magnetic field in electromagnetism. The symbol **A** is commonly used for the magnetic vector potential.]
  disambiguation: |
    While mathematically analogous to terms in other fields, in Pirouette, **A** is the vector potential for *antagonistic* social flow. The Curl Component is therefore not a physical force but a measure of organized, non-cooperative, and ultimately destabilizing social dynamics.
crosslinks:
  near_synonyms: [ANTAGONISTIC_CIRCULATION]
  antonyms: [POTENTIAL_COMPONENT]
  prerequisites: [DISSONANCE_FIELD]
  downstream_effects: [CURL_THRESHOLD, COHERENCE_COLLAPSE]
license: CC-BY-SA-4.0
---

# Curl Component

## Canonical (Pirouette)
The rotational, non-conservative component (∇ × **A**) of the dissonance field (**D**). It represents localized, circulating patterns of antagonistic social interaction that are mathematically orthogonal to cooperative, potential-driven flows (∇φ). Its squared magnitude, averaged over a coherence-critical region (Ωc), defines the Curl Threshold (Θ), a primary indicator of imminent systemic instability and cascade failure.

## EFT-First Summary
In the language of fluid dynamics, the Curl Component is the social vorticity field (**ω**_soc). It is the solenoidal part of the dissonance velocity field (**v**_D) and quantifies local rotational energy that does not contribute to bulk potential flow. Systemic instability arises via a phase transition when the mean-squared vorticity (⟨**ω**_soc²⟩) exceeds a critical value, analogous to the onset of turbulence.

## Glossary Links
- See also: Dissonance Field, Curl Threshold, Coherence Collapse, Potential Component