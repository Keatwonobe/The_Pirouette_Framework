---
term: "Shadow Profile"
canonical_id: "SHADOW_PROFILE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-159"]
---

---
term: Shadow Profile
canonical_id: SHADOW_PROFILE
symbol: Π_s
aliases: [Observation Profile, Measurement Audit]
parents: [DOMA-159]
children: [INST-DIAG-002_placeholder]
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-159
      lines: "§5"
      snippet: |
        Synthesize the metrics into a "Shadow Profile." This profile provides a clear, quantitative summary of the observation's nature—whether it was a gentle glance or a formative intervention.
  editors: [Weaver-Agent]
  review_log: []
triad:
  art: |
    A Shadow Profile is the fingerprint left by a gaze. It is the geometric signature of a single act of knowing, revealing whether the observer's touch was a question or a command.
  law: |
    A Shadow Profile is a standardized four-component vector (V_obs, ΔKτ_sys, Φ_Kτ, τ_echo) that quantifies the total impact of an observation. Any measurement interaction can be losslessly compressed into this profile.
  philosophy: |
    The profile enforces cognitive responsibility. By making the cost and character of observation explicit, it transforms measurement from a passive act of data extraction into a conscious, accountable dialogue with reality.
pirouette_definition: |
  A synthesized, quantitative summary of an observation's nature, derived from the four core Shadow Gauge metrics: Shadow Weight (V_obs), Coherence Cost (ΔKτ_sys), Information Transfer (Φ_Kτ), and Echo Persistence (τ_echo). The profile serves as a formal audit of an observer's geometric and energetic impact on a system's coherence manifold.
operational_definition:
  units: Component-dependent vector. See symbol table.
  symbol_table:
    - name: V_obs
      meaning: Shadow Weight; magnitude of the observer's potential field.
      dimensions: M L^2 T^-2 (Energy)
      default_range: 10^-34 to 10^3 J
    - name: ΔKτ_sys
      meaning: Coherence Cost; net change in the system's internal temporal coherence.
      dimensions: M L^2 T^-2 (Energy)
      default_range: -contextual to +contextual
    - name: Φ_Kτ
      meaning: Information Transfer; net flow of coherence between observer and system.
      dimensions: M L^2 T^-2 (Energy)
      default_range: -contextual to +contextual
    - name: τ_echo
      meaning: Echo Persistence; decay time of the measurement's imprint on the system.
      dimensions: T (Time)
      default_range: 10^-24 to 10^12 s
  measurement:
    procedures:
      - name: Shadow Gauge Audit Protocol
        outline: |
          1.  **Baseline:** Characterize the unperturbed system's Pirouette Lagrangian (𝓛_sys).
          2.  **Coupling:** Model the observer's potential field (V_obs) as an additional term.
          3.  **Calculation:** Evolve the system under the perturbed Lagrangian (𝓛'_sys = 𝓛_sys - V_obs).
          4.  **Reporting:** Compute the four core metrics from the system's trajectory to generate the Shadow Profile (Π_s).
        expected_signals: [V_obs, ΔKτ_sys, Φ_Kτ, τ_echo]
        pitfalls: [Inaccurate baseline characterization (𝓛_sys), incorrect modeling of the observer's potential (V_obs), contamination from unmodeled environmental potentials (VΓ_env).]
context_windows:
  - module: DOMA-159
    excerpt: |
      The Audit Protocol... Synthesize the metrics into a "Shadow Profile." This profile provides a clear, quantitative summary of the observation's nature—whether it was a gentle glance or a formative intervention.
  - module: DOMA-159
    excerpt: |
      **Quantum Physics:** Frames the measurement problem as a resonant coupling that forges a new, definite reality from a field of potential, with the Shadow Profile quantifying the nature of the "collapse."
      **Social Sciences:** Quantifies the Hawthorne effect by modeling how a researcher's presence (V_obs) alters the coherence manifold of a group...
poetic_connections:
  motifs: [fingerprint of observation, signature of a gaze, the cost of knowing, measurement as dialogue]
  evocative_lines:
    - "To know a thing is to change it."
    - "To measure the world is to take responsibility for the echo you leave behind."
  association_matrix:
    - [ "Observer's Shadow", 0.9 ]
    - [ "Measurement Echo", 0.9 ]
    - [ "Coherence Cost", 0.8 ]
    - [ "Coherence Trade-off", 0.7 ]
formal_mappings:
  candidates:
    - target: Quantum Measurement Back-Action / Information-Disturbance Tradeoff
      domain: AMO|Quantum
      mapping_kind: conceptual
      equation_hint: |
        Π_s ~ (coupling, decoherence, info_gain, relaxation_time)
      justification: |
        The Shadow Profile provides a structured vector of quantities that formalize the concepts of measurement back-action (ΔKτ_sys), probe coupling (V_obs), and information gain (Φ_Kτ) inherent in quantum measurement theory. It aims to unify these typically distinct considerations into a single, comprehensive descriptor of the interaction.
      references:
        - title: "Quantum Measurement and Control"
          where: "Wiseman & Milburn, Cambridge University Press"
          date: 2009-01-01
      confidence: 0.75
  adopted:
    - target:
      rationale:
      confidence: 0.0
constraints_and_falsifiers:
  claims:
    - statement: "A truly 'innocent' observation is impossible; any non-null measurement will yield a non-zero Shadow Profile."
      domain: theory|experiment
      falsifier: "Demonstration of a measurement that verifiably extracts information from a system (non-zero Φ_Kτ) while producing a null result for the other three profile components (V_obs=0, ΔKτ_sys=0, τ_echo=0)."
      status: proposed
      links: [DOMA-159]
naming_notes:
  collisions: [The term "profile" is generic. The symbol Π is used for projection operators in QM and for osmotic pressure in chemistry.]
  disambiguation: |
    Distinguish from psychological or user profiles. A Shadow Profile is a physical characterization of a specific *act of measurement*, not of the observer or the system itself in isolation.
crosslinks:
  near_synonyms: [MEASUREMENT_AUDIT]
  antonyms: [INNOCENT_OBSERVATION]
  prerequisites: [OBSERVERS_SHADOW, MEASUREMENT_ECHO, SHADOW_WEIGHT, COHERENCE_COST]
  downstream_effects: [COHERENCE_TRADEOFF, INST-DIAG-002_placeholder]
license: CC-BY-SA-4.0
---