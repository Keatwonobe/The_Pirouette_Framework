---
term: "Currents of Commerce"
canonical_id: "CURRENTS_OF_COMMERCE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-040"]
---

---
term: Currents of Commerce
canonical_id: CURRENTS_OF_COMMERCE
symbol: C_c
aliases: [The Four Flows]
parents: [DOMA-040, DYNA-003]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-040
      lines: "L31-L40"
      snippet: |
        *   **Flow of Capital:** The efficient allocation and circulation of financial resources, not just their accumulation.
        *   **Flow of Information:** The frictionless movement of critical data and insight, enabling timely and intelligent decisions.
        *   **Flow of Talent:** The cycle of attracting, developing, deploying, and retaining human potential where it can have the most impact.
        *   **Flow of Trust:** The unspoken current of psychological safety and shared intent that enables collaboration, innovation, and risk-taking.
  editors: [chain-of-thought-agent]
  review_log: []
triad:
  art: |
    An organization is a living body, defined not by its static mass but by the circulation of its lifeblood. These four currents are the primary arteries and veins through which vitality flows.
  law: |
    The holistic health and value-creation capacity of an organization is a direct function of the coherence (laminar, non-turbulent, and non-stagnant state) of its flows of Capital, Information, Talent, and Trust. A pathology in the organization is always a pathology in one or more of these currents.
  philosophy: |
    This concept reframes organizational diagnosis from static accounting to dynamic systems analysis. It insists that a business is not a machine to be fixed but a river to be tended, shifting the leader's role from mechanic to river-keeper.
pirouette_definition: |
  The Currents of Commerce are the four canonical flows that constitute an organization's systemic health and operational coherence: Capital, Information, Talent, and Trust. They are the specific application of the universal principles of coherence flow from The Caduceus Lens (DYNA-003) to the domain of business. The state of these currents—whether Laminar, Turbulent (Fever), or Stagnant (Atrophy)—provides a complete diagnostic map of the organization.
operational_definition:
  units: The term is a vector of four distinct flows, each with its own units.
  symbol_table:
    - name: C_c
      meaning: The set of the four Currents of Commerce.
      dimensions: vector
      default_range: {Φ_K, Φ_I, Φ_T, Φ_Ψ}
    - name: Φ_K
      meaning: Flow of Capital
      dimensions: currency · T⁻¹
      default_range: contextual
    - name: Φ_I
      meaning: Flow of Information
      dimensions: information · T⁻¹ (e.g., decisions/day)
      default_range: contextual
    - name: Φ_T
      meaning: Flow of Talent
      dimensions: persons · T⁻¹ (e.g., hires/quarter)
      default_range: contextual
    - name: Φ_Ψ
      meaning: Flow of Trust
      dimensions: dimensionless index (e.g., NPS-style score)
      default_range: [-1, 1]
  measurement:
    procedures:
      - name: Multi-Current Flow Audit
        outline: |
          1.  **Capital (Φ_K):** Analyze cash flow velocity, return on invested capital (ROIC) cycles, and budget allocation speed. Contrast with industry benchmarks.
          2.  **Information (Φ_I):** Map key decision paths and measure latency from signal to action. Use network analysis on communication platforms to identify bottlenecks.
          3.  **Talent (Φ_T):** Measure time-to-hire, internal mobility rates, regrettable attrition, and promotion velocity.
          4.  **Trust (Φ_Ψ):** Deploy validated psychological safety surveys (e.g., Amy Edmondson's scale). Measure rate of inter-departmental collaboration vs. escalation.
        expected_signals: [Predictable, low-variance rates for Laminar flow; high-variance, spiky, unpredictable rates for Turbulent flow; near-zero or declining rates for Stagnant flow.]
        pitfalls: [Confusing quantity with quality (e.g., high information flow that is noise); survey data for Trust can be skewed by fear of speaking up; Capital flow metrics can be easily manipulated by accounting practices.]
context_windows:
  - module: DOMA-040
    excerpt: |
      The Fractal Bridge (CORE-014) allows us to map the universal principles of flow onto the specific physiology of an organization. A business is a body, and its lifeblood is coherence in motion across four primary currents: Flow of Capital, Flow of Information, Flow of Talent, and Flow of Trust. The health of the business is the laminar, unimpeded state of these currents, moving in concert.
  - module: DOMA-040
    excerpt: |
      The Diagnostic Protocol: 1. Map the Currents. First, identify the critical flows of coherence that constitute the enterprise's lifeblood, as outlined in §2 (Capital, Information, Talent, Trust). 2. Diagnose the Flow State. For each critical current, assess its state. Is the value stream Laminar and predictable? Is communication between departments Turbulent and chaotic? Is a critical hiring process Stagnant? This provides a detailed map of the organization's health.
poetic_connections:
  motifs: [lifeblood, circulation, river, artery, channel, physiology]
  evocative_lines:
    - "The balance sheet is a photograph of where the river was. The flow is a prophecy of where the river is going."
    - "A Weaver does not see a company as a machine to be fixed, but as a river to be tended."
  association_matrix:
    - [ "LAMINAR_FLOW", 0.9 ]
    - [ "COHERENCE_ATROPHY", 0.7 ]
    - [ "COHERENCE_FEVER", 0.7 ]
    - [ "COHERENCE_EROSION", 0.7 ]
    - [ "COHERENCE_INDEX", 0.8 ]
formal_mappings:
  candidates:
    - target: Multi-component flux vector (J_i)
      domain: CM
      mapping_kind: conceptual
      equation_hint: |
        J_total = Σ J_i
      justification: |
        In continuum mechanics and transport phenomena, the state of a system is often described by the fluxes of different conserved quantities (mass, momentum, energy). The Currents of Commerce are an analogous set of "conserved" quantities essential for organizational viability, where the total health is a function of the individual flows.
      references: []
      confidence: 0.4
  adopted:
    - target: None
      rationale: The mapping is primarily analogical and diagnostic, intended to leverage the powerful intuitions of fluid dynamics without claiming a strict mathematical isomorphism.
      confidence: 0.0
constraints_and_falsifiers:
  claims:
    - statement: "Any significant organizational pathology can be diagnosed as a disruption (Atrophy, Fever, or Erosion) in at least one of the four Currents of Commerce."
      domain: phenomenology
      falsifier: "Demonstrating a recurring, systemic organizational failure that has no measurable correlate in the flows of capital, information, talent, or trust. For example, a failure caused exclusively by a change in a static, external law that affects all competitors equally, without altering internal dynamics."
      status: proposed
      links: [DOMA-040]
naming_notes:
  collisions: [The term "current" is generic in physics and finance (e.g., electric current, current assets). The full phrase "Currents of Commerce" is required for specificity.]
  disambiguation: |
    This is not a list of separate business functions. It is a holistic, interdependent model where the flows are mutually reinforcing or degrading. A blockage in Information flow will eventually starve Capital allocation, repel Talent, and erode Trust.
crosslinks:
  near_synonyms: []
  antonyms: [ORGANIZATIONAL_STASIS]
  prerequisites: [LAMINAR_FLOW, FRACTAL_BRIDGE]
  downstream_effects: [COHERENCE_ATROPHY, COHERENCE_FEVER, COHERENCE_EROSION, COHERENCE_INDEX]
license: CC-BY-SA-4.0