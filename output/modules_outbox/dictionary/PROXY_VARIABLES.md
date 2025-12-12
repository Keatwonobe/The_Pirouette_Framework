---
term: "Proxy Variables"
canonical_id: "PROXY_VARIABLES"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-069"]
---

---
term: Proxy Variables
canonical_id: PROXY_VARIABLES
symbol:
aliases: [Indicators, Observables]
parents: [DOMA-069]
children: [INST-SFA-001, DOMA-SYCH-001]
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-069
      lines: "L22-L28"
      snippet: |
        | Channel | Lagrangian Term | ... | Domain-Specific Proxies (Examples) |
        | :--- | :--- | :--- | :--- |
        | **Coherence** | `Kτ` | ... | **Physics:** Clock stability. **Biology:** Homeostasis. **Society:** Social trust. **Psychology:** A focused state of Flow. |
        | **Pressure** | `VΓ` | ... | **Physics:** Temperature. **Biology:** Pathogen load. **Economics:** Market volatility. **Software:** Rate of incoming critical support tickets. |
  editors: [System Weaver AI]
  review_log: []
triad:
  art: |
    A clock's stability, the trust in a society, a cell's homeostasis—these are not the thing itself, but the local dialect through which the universal grammar of Coherence is spoken. A proxy is the shadow on the cave wall, a measurable echo of an ideal form.
  law: |
    Every measurement of `Kτ` or `VΓ` must be preceded by an explicit declaration of the observable, domain-specific proxy variables being used. The quality of a prediction is formally limited by the verified correlation between the chosen proxies and the universal terms they represent.
  philosophy: |
    Proxy variables bridge the abstract, universal mathematics of the Pirouette Lagrangian to the tangible, messy reality of a specific system. They are the necessary act of translation that makes the framework empirically solvable, grounding its predictive power in verifiable data.
pirouette_definition: |
  A set of observable, domain-specific measurements selected to serve as empirical representatives for the universal Lagrangian terms of Coherence (`Kτ`) and Pressure (`VΓ`). The selection and calibration of proxy variables is the foundational act of the Weaver's Lens protocol (DOMA-069), translating the abstract dynamics of a system into a verifiable, quantitative time-series suitable for solving its geodesic.
operational_definition:
  units: Domain-specific (e.g., Hz, K, currency volatility index, ticket/hour). Must be normalized into the dimensionless units of `Kτ` and `VΓ` via the specified calibration protocol.
  symbol_table:
    - name: Kτ
      meaning: Coherence (target term)
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: VΓ
      meaning: Pressure (target term)
      dimensions: dimensionless
      default_range: "[0, ∞)"
  measurement:
    procedures:
      - name: The Weaver's Lens Calibration Ritual
        outline: |
          1.  **Define the Lens:** Explicitly declare the proxy variables for `Kτ` and `VΓ`.
          2.  **Vow of Silence (Zeroing):** Isolate the instrument to measure its baseline internal noise.
          3.  **Harmonious Duet (Cross-Calibration):** Compare readings against a trusted standard to ensure consensus reality.
          4.  **Notary's Seal (Commit):** Cryptographically sign and commit the calibration state and all subsequent `{Kτ, VΓ}` measurements to an immutable ledger.
        expected_signals: [Time-series data for each proxy, Spectral density plots]
        pitfalls: [Poor proxy selection (low correlation to the universal term), Calibration drift, Mistaking instrument noise for system signal]
context_windows:
  - module: DOMA-069
    excerpt: |
      Measurement is not about detecting a pre-defined field; it is an act of translation, of identifying the observable, domain-specific proxies for the universal terms of the Lagrangian (`𝓛_p = Kτ - VΓ`). To measure any system is to first define its lens.
  - module: DOMA-069
    excerpt: |
      An instrument that lies is worse than no instrument at all. A measurement without provenance is an opinion. This ritual ensures that every observation is rigorous, transparent, and reproducible... The Weaver must explicitly declare the proxy variables chosen for `Kτ` and `VΓ` for the system under analysis. This declaration is the "calibration certificate" and the foundational act of honest observation.
poetic_connections:
  motifs: [translation, correspondence, shadow, echo, representation, instrumentation]
  evocative_lines:
    - "The first measures the purity of a single note—the song of a thing being itself."
    - "The second measures the encompassing noise of the foundry in which that note must be sung."
  association_matrix:
    - [ "WEAVERS_LENS", 0.9 ]
    - [ "COHERENCE", 0.8 ]
    - [ "PRESSURE", 0.8 ]
    - [ "CALIBRATION", 0.7 ]
formal_mappings:
  candidates:
    - target: Order Parameter
      domain: CM
      mapping_kind: conceptual
      justification: |
        Proxy variables for Coherence (`Kτ`) function as order parameters in condensed matter physics. They are macroscopic observables (e.g., magnetization) whose non-zero value indicates an ordered, coherent phase. The choice of proxy is similarly domain-specific.
      references:
        - title: Principles of Condensed Matter Physics
          where: Chapter 1
          date: 2000-09-14
      confidence: 0.8
    - target: Effective Temperature (T_eff)
      domain: EFT
      mapping_kind: operational
      justification: |
        Proxy variables for Pressure (`VΓ`) often map to measures of environmental noise or stochastic forcing. In many physical systems, this is quantified as an effective temperature, which determines the magnitude of fluctuations via the fluctuation-dissipation theorem.
      references: []
      confidence: 0.7
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "A well-chosen pair of proxy variables will produce `(Kτ, VΓ)` tuples that, when integrated via the Pirouette Lagrangian, predict the system's near-future trajectory with a mean squared error significantly below that of a naive (e.g., random walk) model."
      domain: phenomenology
      falsifier: "For a given system, if no set of physically plausible proxy variables can be found that yields predictions better than a random walk, then either the framework is inapplicable to that system or the core principle of correspondence is false."
      status: proposed
      links: [DOMA-069]
naming_notes:
  collisions: []
  disambiguation: |
    The term is used analogously to "proxy variable" in statistics: a measurable variable used in place of one that cannot be directly measured. Crucially, a proxy variable is *not* the universal term itself (`Kτ` or `VΓ`), but a carefully chosen and calibrated representative. The validity of any analysis rests on the strength of this representation.
crosslinks:
  near_synonyms: [INDICATOR, OBSERVABLE]
  antonyms: [UNIVERSAL_TERM, ABSTRACT_VARIABLE]
  prerequisites: [LAGRANGIAN_PIR-CORE-006, FRACTAL_BRIDGE-CORE-014]
  downstream_effects: [GEODESIC, SYSTEM_DIAGNOSIS]
license: CC-BY-SA-4.0
---