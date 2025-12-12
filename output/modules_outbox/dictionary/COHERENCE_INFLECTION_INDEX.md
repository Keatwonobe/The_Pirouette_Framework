---
term: "Coherence Inflection Index"
canonical_id: "COHERENCE_INFLECTION_INDEX"
symbol: "CII"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-112"]
---

---
term: Coherence Inflection Index
canonical_id: COHERENCE_INFLECTION_INDEX
symbol: CII
aliases: []
parents: [DOMA-112]
children: []
status: ratified
version: 2.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-112
      lines: "L63-L69"
      snippet: |
        The final step translates this drift into a simple, context-aware metric of risk. The Coherence Inflection Index (CII) is the normalized magnitude of the drift vector, scaled against the ambient Temporal Pressure (`Γ`).
        `CII = ||V_drift|| / (1 + kΓ)`
        Where `k` is a domain-specific scaling constant. This formulation measures *unforced* instability...
  editors: [system/writer-agent]
  review_log: []
triad:
  art: |
    A system's song begins to falter long before its structure breaks. The CII is an instrument for hearing that first, subtle dissonance—the tremor in the hum that precedes the snap. It is the art of hearing the future in the changing song of the present.
  law: |
    A Coherence Inflection Index rising above a baseline threshold (>0.3) signals an imminent systemic state transition. The magnitude of the CII quantifies the system's unforced instability, and its rate of change correlates to the transition's proximity.
  philosophy: |
    The CII moves the Weaver from a reactive posture to a predictive one, transforming diagnosis into the science of foresight. It quantifies the tension building up before a system is forced to snap into a new configuration, providing a crucial lead time to intervene, mitigate, or adapt.
pirouette_definition: |
  The Coherence Inflection Index is the final, predictive metric of systemic risk, quantifying the degree of a system's *unforced* instability. It is a dimensionless scalar calculated as the magnitude of the Manifold Drift Vector (`V_drift`) normalized by the ambient Temporal Pressure (`Γ`), providing an early warning of an impending state transition or *Ki Morphogenesis* event. A rising CII indicates that a system is actively deviating from its geodesic path of maximal coherence.
operational_definition:
  units: Dimensionless
  symbol_table:
    - name: CII
      meaning: Coherence Inflection Index
      dimensions: dimensionless
      default_range: "[0, 1+]; Critical threshold typically > 0.6"
    - name: V_drift
      meaning: Manifold Drift Vector; the rate of change of a system's resonant signature (`Ki`)
      dimensions: "[Pattern] [T]⁻¹"
      default_range: contextual
    - name: Γ
      meaning: Ambient Temporal Pressure
      dimensions: "[Pressure]"
      default_range: contextual
    - name: k
      meaning: Domain-specific scaling constant
      dimensions: "[Pressure]⁻¹"
      default_range: contextual
  measurement:
    procedures:
      - name: Sentinel Protocol
        outline: |
          1.  **Resonance Mapping:** Ingest time-series data (e.g., vibration, network traffic) to extract the system's dominant resonant signature (`Ki`) over time.
          2.  **Drift Calculation:** Compute the time-derivative of the `Ki` pattern to determine the Manifold Drift Vector (`V_drift`).
          3.  **Normalization:** Calculate the magnitude of `V_drift` and normalize it by the measured ambient Temporal Pressure (`Γ`) and a domain-specific constant (`k`) using the formula `CII = ||V_drift|| / (1 + kΓ)`.
        expected_signals: [Time-series data from system sensors, Environmental pressure data]
        pitfalls: [Low signal-to-noise ratio preventing clear `Ki` extraction, Incorrect choice of scaling constant `k` masking or exaggerating instability, Systems with inherently chaotic or multi-modal `Ki` patterns yielding a misleading `V_drift`]
context_windows:
  - module: DOMA-112
    excerpt: |
      A system does not break all at once; it first whispers its distress. Before every crash, every bifurcation, every sudden shift, there are subtle precursors of instability. This module provides the instrumentation to hear those whispers. The Coherence Inflection Sentinel is a universal early-warning system designed to detect the subtle decay in a system's internal rhythm that precedes a major systemic state change...
  - module: DOMA-112
    excerpt: |
      The Coherence Inflection Index (CII) is the normalized magnitude of the drift vector, scaled against the ambient Temporal Pressure (`Γ`). This formulation measures *unforced* instability; a high CII indicates significant internal degradation that is not merely a reaction to external pressure. A low CII signifies a healthy system firmly anchored to its geodesic, while a rising CII signals that a state transition is imminent.
  - module: DOMA-112
    excerpt: |
      The CII provides a clear, color-coded diagnostic for any system's health... A value > 0.6 indicates a **Critical** state where the system is highly unstable and a major state transition is imminent. This numerical warning can be further refined... High CII + Rising Dissonance warns of an impending descent into **Turbulent Flow**.
poetic_connections:
  motifs: [precursor_hum, faltering_song, tremor_before_quake, unforced_instability]
  evocative_lines:
    - "A system does not break all at once; it first whispers its distress."
    - "It is the art of hearing the future in the changing song of the present."
  association_matrix:
    - [ "MANIFOLD_DRIFT_VECTOR", 0.9 ]
    - [ "KI_MORPHOGENESIS", 0.8 ]
    - [ "TEMPORAL_PRESSURE", 0.6 ]
    - [ "TURBULENT_FLOW", 0.5 ]
formal_mappings:
  candidates:
    - target: Maximal Lyapunov exponent (λ_max)
      domain: Math
      mapping_kind: conceptual
      equation_hint: |
        CII ∝ d/dt |δx(t)| where δx is state-space deviation
      justification: |
        CII measures the rate of divergence from a stable trajectory (geodesic), analogous to how a positive maximal Lyapunov exponent quantifies the exponential rate of separation of nearby trajectories in phase space. A rising CII signals a move toward a chaotic or unstable regime where stability is lost, conceptually similar to λ_max transitioning from negative to positive.
      references:
        - title: "Coping with chaos"
          where: "Wiley, 1990"
          date: 1990-01-01
      confidence: 0.7
    - target: Critical slowing down
      domain: Math
      mapping_kind: conceptual
      justification: |
        Near a critical point or bifurcation, systems exhibit critical slowing down, where their recovery time from perturbations diverges. A high CII, indicating a struggle to maintain coherence, is a symptom of this underlying loss of resilience. The drift measured by CII is an active manifestation of the instability that causes the system to slow its return to equilibrium.
      references:
        - title: "Critical slowing down as a personalized early warning signal for depression"
          where: "PNAS, 110(28)"
          date: 2013-07-09
      confidence: 0.6
  adopted:
    - target:
      rationale:
      confidence: 0.0
constraints_and_falsifiers:
  claims:
    - statement: "A statistically significant increase in the CII (e.g., crossing the 0.3 threshold) in a monitored system will precede a major state transition with a lead time greater than the system's characteristic timescale."
      domain: phenomenology
      falsifier: "Observing multiple systems where major state transitions (e.g., market crashes, equipment failures) occur without a preceding rise in CII, or where high CII values persist indefinitely without a transition, would falsify its predictive power."
      status: proposed
      links: [DOMA-112]
naming_notes:
  collisions: [Inflection point (calculus)]
  disambiguation: |
    "Inflection" in this context refers to a critical "bending" or change in the system's state trajectory on the coherence manifold, signaling an imminent change of state. It is not the mathematical inflection point of a 1D function (where the second derivative is zero), but rather the point where stability is lost.
crosslinks:
  near_synonyms: []
  antonyms: [GEODESIC_STABILITY_INDEX]
  prerequisites: [MANIFOLD_DRIFT_VECTOR, TEMPORAL_PRESSURE]
  downstream_effects: [KI_MORPHOGENESIS, TURBULENT_FLOW, STAGNANT_FLOW]
license: CC-BY-SA-4.0
---