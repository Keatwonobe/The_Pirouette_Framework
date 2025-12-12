---
term: "Channel Pressure"
canonical_id: "CHANNEL_PRESSURE"
symbol: "Γ"
aliases: [Coherence Dam]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-158"]
---

---
term: Channel Pressure
canonical_id: CHANNEL_PRESSURE
symbol: Γ
aliases: [Coherence Dam, Gamma_edge]
parents: [DOMA-158]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-158
      snippet: |
        *   **Channel Pressure (Γ):** This replaces `Gamma_edge`. It quantifies the dissonance, friction, or resistance to flow between two connected nodes. It is the cost of interaction.
            *   **Inference:** Look for bottlenecks, antagonism, or latency. In a social network, this is the inverse of trust. In an organization, it is bureaucratic friction. In a power grid, it is line impedance.
            *   **Scaling:** `0` (a frictionless, perfectly resonant connection) to `1` (a complete blockage or "Coherence Dam").
  editors: [Weaver-Agent]
  review_log: []
triad:
  art: |
    A channel is a riverbed for coherence. Pressure is the narrowing of the canyon, the grit on the stone, the dam that holds the current back. It is the sound of the water fighting the rock.
  law: |
    The realized Coherence Flow (`J`) across a channel is the potential flow gated by its conductance, `(1 - Γ)`. As Channel Pressure `Γ` approaches 1, flow ceases, regardless of the source's coherence or the phase alignment between nodes.
  philosophy: |
    Channel Pressure localizes the system's "pain" onto its connections. It operationalizes the cost of interaction, revealing that system-wide inefficiency is not a vague miasma but a discrete set of specific, measurable frictions. To heal the system, one must ease the pressure on these specific channels.
pirouette_definition: |
  A dimensionless scalar quantity `Γ ∈ [0, 1]` assigned to a channel (edge) in a network. It quantifies the fraction of potential Coherence Flow that is lost or dissipated due to friction, dissonance, latency, or structural obstruction between the two connected nodes. A value of `Γ = 0` represents a perfectly frictionless, resonant channel, while `Γ = 1` represents a complete blockage, or a "Coherence Dam."
operational_definition:
  units: Dimensionless scalar.
  symbol_table:
    - name: Γ_ij
      meaning: Channel Pressure on the connection from node `i` to node `j`.
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: J_ij
      meaning: Coherence Flow from node `i` to node `j`.
      dimensions: dimensionless
      default_range: "[-1, 1]"
    - name: Kτ_i
      meaning: Coherence of the source node `i`.
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: φ_i, φ_j
      meaning: Temporal Phase of nodes `i` and `j`.
      dimensions: dimensionless (angle)
      default_range: "[0, 2π)"
  measurement:
    procedures:
      - name: Inferential Channel Audit
        outline: |
          Channel Pressure is typically inferred rather than measured directly. It is the inverse of a measured or modeled "channel quality" metric, normalized to the `[0, 1]` range.
          1. Identify a proxy for flow resistance between nodes `i` and `j` (e.g., network latency, packet loss, semantic disagreement, bureaucratic delay, electrical impedance).
          2. Measure this proxy over a representative time window.
          3. Normalize the measurement such that the ideal, frictionless case maps to `0` and a practical maximum blockage maps to `1`.
        expected_signals: [Latency, packet loss, semantic dissonance score, inverse trust metric, impedance]
        pitfalls: [Confusing a lack of connection with `Γ=1` (a channel must exist to have pressure), mistaking low source coherence `Kτ` for high channel pressure `Γ`.]
context_windows:
  - module: DOMA-158
    excerpt: |
      **Channel Pressure (Γ):** This replaces `Gamma_edge`. It quantifies the dissonance, friction, or resistance to flow between two connected nodes. It is the cost of interaction... Scaling: `0` (a frictionless, perfectly resonant connection) to `1` (a complete blockage or "Coherence Dam").
  - module: DOMA-158
    excerpt: |
      The flow from node `i` to node `j` is given by: `J_ij = Kτ_i * cos(φ_i - φ_j) * (1 - Γ_ij)`. This formula elegantly captures the core dynamics... **Conductance (`1 - Γ_ij`):** This represents the fraction of potential flow not lost to friction. A frictionless channel (`Γ = 0`) has a conductance of `1`.
  - module: DOMA-158
    excerpt: |
      This entire analysis is a practical application of the Principle of Maximal Coherence (CORE-006)... **Pressure (`f(Γ)`):** The "potential" term is the sum of all losses due to turbulence and stagnation. It is the "cost" of the network fighting itself, revealed by the high-frequency modes.
poetic_connections:
  motifs: [friction, dam, bottleneck, dissonance, impedance, static, resistance]
  evocative_lines:
    - "The high, sharp notes cry out from its points of pain."
    - "It is the cost of interaction."
  association_matrix:
    - [ "COHERENCE_FLOW", -0.9 ]
    - [ "TURBULENT_FLOW", 0.8 ]
    - [ "CONDUCTANCE", -1.0 ]
    - [ "NODE_COHERENCE", 0.1 ]
formal_mappings:
  candidates:
    - target: Electrical Resistance (R) / Impedance (Z)
      domain: CM
      mapping_kind: mathematical
      equation_hint: |
        Pirouette Conductance, C_p = 1 - Γ
        Electrical Conductance, G = 1 / R
      justification: |
        The module explicitly cites "line impedance" as an example. The mathematical form `(1 - Γ)` is labeled "Conductance" and acts as a multiplicative gate on flow, directly analogous to how electrical conductance (`G`) gates current (`I = G * V`). Γ is a normalized form of resistance.
      references:
        - title: The Network as a Coherence Manifold
          where: DOMA-158, §2
          date: 2025-10-18
      confidence: 0.9
    - target: Dissipation/Friction Term
      domain: CM
      mapping_kind: conceptual
      equation_hint: |
        L = T - V - D(γ)
      justification: |
        In Lagrangian mechanics, non-conservative forces like friction are sometimes included via a dissipation function. The Pirouette Lagrangian `𝓛_p = Kτ - f(Γ)` explicitly casts `f(Γ)` as the potential/cost term representing losses, analogous to a dissipation function.
      references: []
      confidence: 0.7
  adopted:
    - target: Normalized Resistance
      rationale: The mapping to electrical resistance/conductance is explicit in the source module, mathematically direct, and operationally intuitive. `Γ` is best understood as a dimensionless, normalized measure of resistance to flow.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "In a network analyzed via the Coherence Laplacian, interventions that lower `Γ` on channels identified by high-frequency eigenvectors will lead to a measurable increase in total system-wide Coherence Flow."
      domain: phenomenology
      falsifier: "A series of targeted interventions to reduce measured friction (e.g., simplifying a protocol, mediating a dispute) on high-`Γ` channels fails to increase network-wide flow, or shows that `Γ` was not the primary constraint. This would falsify the diagnostic power of the Coherence Laplacian or the flow model itself."
      status: proposed
      links: [DOMA-158]
naming_notes:
  collisions: [Γ (Gamma function), Γ (Christoffel symbol in GR), γ (damping coefficient)]
  disambiguation: |
    In the Pirouette Framework, `Γ` is always a dimensionless scalar on a channel (edge), normalized to the range `[0, 1]`. It represents a *loss factor* or normalized resistance, not a geometric connection or a mathematical function. Context is key: Pirouette's `Γ` always appears in the context of network channels and Coherence Flow.
crosslinks:
  near_synonyms: [Resistance, Dissonance, Friction, Impedance]
  antonyms: [Conductance, Resonance]
  prerequisites: [NODE_COHERENCE, TEMPORAL_PHASE]
  downstream_effects: [COHERENCE_FLOW, TURBULENT_FLOW, COHERENCE_LAPLACIAN]
license: CC-BY-SA-4.0