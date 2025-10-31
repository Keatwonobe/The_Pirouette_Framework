---
term: "Shadow Gauge"
canonical_id: "SHADOW_GAUGE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DYNA-005_coherent_adherence_protocol"]
---

---
term: Shadow Gauge
canonical_id: SHADOW_GAUGE
symbol: \(V_{\text{obs}}\)
aliases: [Observer Cost, Probe Burden, Shadow Overreach]
parents: [DYNA-005_coherent_adherence_protocol]
children: [PPS-015, DOMA-QCOMP-001, DOMA-203]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DYNA-005_coherent_adherence_protocol
      lines: "§1, §4"
      snippet: |
        Pirouette Lagrangian: \(\mathcal L_p=K_\tau - V_\Gamma\) with observation cost \(V_{\text{obs}}\) (Shadow Gauge)...
        3) **Shadow Gauge Limits** — a public cap on probe strength so \(V_{\text{obs}}\) cannot exceed budget.
  editors: [SYS-ARCH-BOT, Dr. Elara Vance]
  review_log: []
triad:
  art: |
    The price of the spotlight; the weight of a gaze. It is the accounting for the choir's hoarse throats, a measure of the observer's intrusion before the song can be heard.
  law: |
    Any action \(\mathcal A\) that probes a system must be accompanied by a disclosed, metered, and capped Observer Cost (\(V_{\text{obs}}\)). Any increase \(\Delta V_{\text{obs}}\) imposed on sentient participants requires their informed consent and cannot exceed a public budget.
  philosophy: |
    To observe is to interact; to measure is to disturb. The Shadow Gauge makes this physical reality an ethical imperative, forcing systems to account for the cost of their own awareness and preventing 'observation' from becoming a covert channel for coercion.
pirouette_definition: |
  A formal accounting mechanism and potential term, \(V_{\text{obs}}\), within the Pirouette Lagrangian that quantifies the total cost of observation. This cost includes measurement back-action, attentional burden, data extraction, and other forms of systemic intrusion required to determine a system's state (e.g., its Adherence, \(T_a\)). The Coherent Adherence Protocol (CAP v2) mandates that \(V_{\text{obs}}\) be explicitly metered, publicly capped, and, for sentient participants, only increased with informed consent.
operational_definition:
  units: Information (bits, nats) or Energy (Joules), context-dependent.
  symbol_table:
    - name: \(V_{\text{obs}}\)
      meaning: Total Observer Cost potential.
      dimensions: Energy (M L^2 T^-2) or Dimensionless (Information).
      default_range: "[0, V_max_budget]"
    - name: \(\Delta V_{\text{obs}}\)
      meaning: Change in Observer Cost from a specific action.
      dimensions: Energy (M L^2 T^-2) or Dimensionless (Information).
      default_range: contextual
  measurement:
    procedures:
      - name: Probe Power Integration
        outline: |
          For physical systems, integrate the power of the measurement probe (e.g., laser power in W) over the interaction time (s). For informational systems (e.g., UX), quantify the cost by bits of data requested/processed, number of notifications, or time-on-task required for user response.
        expected_signals: [Probe power spectral density, API call logs, user interaction logs]
        pitfalls: [Ignoring back-action from passive sensing, under-counting cognitive load in UX measurements]
      - name: Counterfactual A/B Test
        outline: |
          Establish two identical contexts (A and B). In B, apply the measurement protocol. The difference in a target welfare metric (e.g., user-reported focus, system energy use) provides an estimate of \(V_{\text{obs}}\). Must be run against a control with *equal* \(V_{\text{obs}}\) to isolate other effects.
        expected_signals: [Differential welfare metrics, differential system resource usage]
        pitfalls: [Confounding variables, Hawthorne effect (observation changing behavior independently of probe cost)]
context_windows:
  - module: DYNA-005_coherent_adherence_protocol
    excerpt: |
      **Protocol goal (non-manipulative form):**
      \[
      \max_{\mathcal A}\;\;\underbrace{\mathbf E[\,K_\tau(T_a)\,]}_{\text{usable coherence}}
      -\underbrace{V_\Gamma}_{\text{pressure}}
      -\underbrace{V_{\text{obs}}}_{\text{observer cost}}
      -\lambda\,\underbrace{\mathcal D}_{\text{Dark Residue}}
      \quad \text{s.t.}\;\;\mathcal C_{\mathrm{consent}},\;\mathcal C_{\mathrm{transparency}}.
      \]
  - module: DYNA-005_coherent_adherence_protocol
    excerpt: |
      **Ethical Covenant (hard constraints)**
      3) **Shadow Gauge Limits** — a public cap on probe strength so \(V_{\text{obs}}\) cannot exceed budget.
      **Dark Residue Functional**
      - **Attention debt**: cumulative increases in \(V_{\text{obs}}\) imposed on users (probe burden).
poetic_connections:
  motifs: [observation cost, measurement problem, consent, transparency, attention economy]
  evocative_lines:
    - "it changes the *room*, not the throat."
    - "any influence that raises \(V_{\text{obs}}\) on people without consent (Shadow overreach)"
  association_matrix:
    - [ "Adherence", 0.7 ]
    - [ "Dark Residue", 0.8 ]
    - [ "Consent", 0.9 ]
formal_mappings:
  candidates:
    - target: Quantum measurement back-action
      domain: AMO
      mapping_kind: conceptual
      equation_hint: |
        \([\hat{X}, \hat{P}] = i\hbar \implies \Delta x \Delta p \ge \hbar/2\)
      justification: |
        In quantum mechanics, any measurement necessarily disturbs the system. \(V_{\text{obs}}\) generalizes this principle, accounting for the energy or information exchanged during a probe, analogous to the disturbance required to gain information and reduce uncertainty about a conjugate variable.
      references:
        - title: The Quantum Theory of Measurement
          where: P. Busch, P.J. Lahti, P. Mittelstaedt
          date: 1991-01-01
      confidence: 0.8
    - target: Mutual Information / Channel Capacity
      domain: Math
      mapping_kind: mathematical
      equation_hint: |
        \(V_{\text{obs}} \propto I(S; M)\)
      justification: |
        \(V_{\text{obs}}\) can be modeled as the cost to acquire a certain amount of mutual information \(I(S; M)\) between the system state \(S\) and the measurement \(M\). The more information gained (lower uncertainty), the higher the necessary cost, formalizing the trade-off between knowledge and intrusiveness.
      references:
        - title: A Mathematical Theory of Communication
          where: Bell System Technical Journal, Vol. 27
          date: 1948-07-01
      confidence: 0.7
  adopted:
    []
constraints_and_falsifiers:
  claims:
    - statement: "Increasing \(V_{\text{obs}}\) on a sentient system without consent measurably increases its Dark Residue (\(\mathcal D\)), specifically the `Loss(autonomy)` and `Debt(attention)` terms."
      domain: phenomenology
      falsifier: "An experiment shows a system where \(V_{\text{obs}}\) is raised covertly, yet user-reported autonomy and attention metrics remain unchanged or improve, and no other negative externalities are detected."
      status: proposed
      links: [DYNA-005_coherent_adherence_protocol]
    - statement: "A non-zero increase in Adherence (\(\Delta T_a > 0\)) can be achieved via environmental shaping with \(\Delta V_{\text{obs}} = 0\)."
      domain: phenomenology
      falsifier: "A system is found where \(T_a\) can *only* be increased by actions with a non-zero, positive \(V_{\text{obs}}\), proving environmental shaping is insufficient and direct probing is always necessary."
      status: proposed
      links: [DYNA-005_coherent_adherence_protocol]
naming_notes:
  collisions: [The symbol 'V' is overloaded for potential energy. The subscript 'obs' is critical.]
  disambiguation: |
    Distinguish from \(V_\Gamma\) (Temporal Pressure), which is a potential related to intrinsic system dynamics, not measurement. The Shadow Gauge (\(V_{\text{obs}}\)) is the cost *to see* the system's state, while Temporal Pressure is a force *within* the system's state evolution.
crosslinks:
  near_synonyms: [OBSERVER_COST]
  antonyms: [COVERT_INFLUENCE]
  prerequisites: [COHERENT_ADHERENCE_PROTOCOL, ADHERENCE, DARK_RESIDUE]
  downstream_effects: [ADHERENCE_MEASUREMENT, DARK_RESIDUE_ACCOUNTING]
license: CC-BY-SA-4.0
---