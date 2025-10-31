---
term: "Matching Radius"
canonical_id: "MATCHING_RADIUS"
symbol: "r_*"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DYNA-BH-INT-001"]
---

---
term: Matching Radius
canonical_id: MATCHING_RADIUS
symbol: r_*
aliases: [core radius]
parents: [DYNA-BH-INT-001]
children: [XXP-GR-EXP]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DYNA-BH-INT-001
      lines: "L63-L65"
      snippet: |
        - **Matching radius** \(r_\ast\): continuous \( \{g_{\mu\nu}\},\ \partial_r g_{\mu\nu}\) and **Israel-like** continuity of normal stresses from \(T^\mu_{\ \nu}(\Gamma)\).
  editors: [Agent: Scribe-7]
  review_log: []
triad:
  art: |
    The seam where the crystal heart of a black hole is stitched into the smooth fabric of spacetime. It is the shoreline between the familiar ocean of general relativity and the exotic continent of a new temporal phase.
  law: |
    The radial coordinate \(r = r_\ast\) at which the interior metric solution \(g_{\mu\nu}^{\rm int}\) and its radial derivative smoothly join the exterior vacuum GR solution \(g_{\mu\nu}^{\rm ext}\), ensuring continuity of geometry and normal stresses across the interface.
  philosophy: |
    The Matching Radius operationalizes the principle of locality for new physics. It confines exotic dynamics to a region unobservable to a distant observer except through tiny, high-frequency "leaks," preserving the successful low-energy predictions of General Relativity.
pirouette_definition: |
  The Matching Radius, \(r_\ast\), is the spatial coordinate defining the boundary interface between an exotic black hole interior (e.g., a Γ-saturated core) and the external General Relativistic vacuum spacetime. At this boundary, the metric \(g_{\mu\nu}\) and its first radial derivative \(\partial_r g_{\mu\nu}\) are continuous. Furthermore, the normal components of the stress-energy tensor are continuous, analogous to the Israel junction conditions, ensuring a smooth and physically consistent transition.
operational_definition:
  units: meters (m)
  symbol_table:
    - name: r_*
      meaning: The radial coordinate of the interface between the interior core and exterior spacetime.
      dimensions: L
      default_range: Model-dependent, but strictly \(0 < r_\ast < r_h\), where \(r_h\) is the event horizon radius.
  measurement:
    procedures:
      - name: Inference from Gravitational Wave Echoes
        outline: |
          Measure the gravitational wave signal from a black hole ringdown. A stiff core bounded by \(r_\ast\) will act as a partially reflective surface for GWs. The time delay \(\Delta t\) between successive, highly suppressed "echoes" is determined by the light-travel time between \(r_\ast\) and the photon sphere (\(r_{\rm ph}\)). By fitting the observed echo train to the Γ-Lighthouse model, \(r_\ast\) can be inferred.
        expected_signals: [A train of low-amplitude, barrier-suppressed GW echoes with spacing \(\Delta t \approx 2\int_{r_\ast}^{r_{\rm ph}} dr/c_{\rm eff}(r)\).]
        pitfalls: [Signal amplitude is expected to be extremely low, likely below current detector sensitivity. Model degeneracy: other physical effects could mimic an echo signal.]
      - name: Inference from Ringdown Phase Drift
        outline: |
          Measure the phase evolution of different quasi-normal modes (QNMs) during ringdown at high signal-to-noise. The propagation of GWs through the interior core up to \(r_\ast\) induces a frequency-dependent phase shift \(\Delta\phi_{\rm GW} \propto (\omega/\omega_c)^2\). The magnitude of this shift depends on the integrated profile of the Γ-field within \(r_\ast\). By measuring this dephasing, the parameter \(r_\ast\) can be constrained.
        expected_signals: [Anomalous, frequency-dependent dephasing of the late-time ringdown waveform relative to the GR prediction.]
        pitfalls: [The effect is suppressed by \((\omega/\omega_c)^2\) and may be too small to distinguish from measurement noise or environmental effects.]
context_windows:
  - module: DYNA-BH-INT-001
    excerpt: |
      Boundary data:
      - **Core center** \(r\!=\!0\): \(m(0)\!=\!0,\ \Gamma'(0)\!=\!0\).
      - **Matching radius** \(r_\ast\): continuous \( \{g_{\mu\nu}\},\ \partial_r g_{\mu\nu}\) and **Israel-like** continuity of normal stresses from \(T^\mu_{\ \nu}(\Gamma)\).
      - **Exterior** \(r>r_\ast\): GR vacuum (Schwarzschild/Kerr in IR).
  - module: DYNA-BH-INT-001
    excerpt: |
      **Partial reflectivity at \(r_\ast\)** (stiff core): tiny GW **echo train** with spacing \(\Delta t \approx 2\int_{r_\ast}^{r_{\rm ph}} dr/\sqrt{f(r)g(r)}\) (photon-sphere radius \(r_{\rm ph}\)), but **no extra polarizations**.
poetic_connections:
  motifs: [boundary, seam, interface, membrane, core-mantle boundary]
  evocative_lines:
    - "The singularity is replaced by a phase—a yolk of time under pressure."
    - "Outside, the loom reads as perfect GR; inside, Γ hums..."
  association_matrix:
    - [ "GAMMA_SATURATED_CORE", 0.9 ]
    - [ "GW_ECHO", 0.7 ]
    - [ "EVENT_HORIZON", 0.5 ]
formal_mappings:
  candidates:
    - target: Phase Boundary
      domain: CM
      mapping_kind: conceptual
      equation_hint: |
        Israel Junction Conditions \(\approx\) Continuity of pressure & displacement.
      justification: |
        The matching radius \(r_\ast\) functions as a phase boundary, similar to the core-mantle boundary in geophysics or the surface of a neutron star. It separates two regions with different equations of state (exotic Γ-medium vs. vacuum). The physical requirement of a smooth transition is enforced by junction conditions that are the direct gravitational analogue of requiring continuous pressure and displacement at a material interface.
      references:
        - title: Relativistic Stars
          where: S. Weinberg, Gravitation and Cosmology, Ch. 11
          date: 1972-01-01
      confidence: 0.8
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The matching radius \(r_\ast\) is a smooth boundary that joins the interior to a standard GR vacuum, sourcing no exotic (non-Transverse-Traceless) gravitational wave polarizations."
      domain: phenomenology
      falsifier: "The detection of scalar or vector polarization modes in gravitational waves from a black hole merger ringdown would falsify the core model bounded by \(r_\ast\), as it violates the single-metric universality (SR-5) and CPM assumptions."
      status: proposed
      links: [DYNA-BH-INT-001]
    - statement: "For a stable black hole object, \(r_\ast\) is a finite, non-zero radius, replacing the central singularity."
      domain: theory
      falsifier: "Observational evidence from gravitational waves or electromagnetic probes that is only consistent with a point-like central singularity (i.e., ruling out any finite-radius structure) would falsify the model."
      status: proposed
      links: [DYNA-BH-INT-001, XXP-GR-EXP]
naming_notes:
  collisions: [The symbol \(r_*\) is commonly used in GR for the tortoise coordinate. Context must be used to distinguish them.]
  disambiguation: |
    The Matching Radius (\(r_\ast\)) is a physical boundary *inside* the event horizon (\(r_h\)). It should not be confused with the event horizon, the photon sphere radius (\(r_{\rm ph}\)), the ISCO radius, or the tortoise coordinate (often also denoted \(r_*\)).
crosslinks:
  near_synonyms: [CORE_RADIUS]
  antonyms: [SINGULARITY]
  prerequisites: [GAMMA_SATURATED_CORE, EVENT_HORIZON]
  downstream_effects: [GW_ECHO, RINGDOWN_PHASE_DRIFT]
license: CC-BY-SA-4.0
---