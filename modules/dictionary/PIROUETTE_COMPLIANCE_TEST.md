---
term: "Pirouette-Compliance Test"
canonical_id: "PIROUETTE_COMPLIANCE_TEST"
symbol: "PCT"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-PHI-001"]
---

---
term: Pirouette-Compliance Test
canonical_id: PIROUETTE_COMPLIANCE_TEST
symbol: PCT
aliases: []
parents: [MATH-PHI-001]
children: [MATH-YM-001, MATH-GR-001, INFO-COH-001]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-PHI-001
      lines: "§2"
      snippet: |
        A domain is **Pirouette** iff it passes all three gates:
        - **PCT-1 (SR Gate):** There exists an embedding of \( \mathcal{D} \) whose invariants are stable under **SR-0…6** *and* preserve CPM...
        - **PCT-2 (Σ Gate):** Under Σ pushforward, the images of \( \mathcal{D} \) support **U(1)/SU(2)/SU(3)** frame relabelings or the GR constitutive law **without** inflating the constant ledger...
        - **PCT-3 (Falsifiability Gate):** The graft produces at least one **testable** prediction...
  editors: [system-generator]
  review_log: []
triad:
  art: |
    A filter that reveals if a beautiful mathematical key can turn a real, physical lock. It tests not just the key's shape, but whether its metal is strong enough to bear the load of turning.
  law: |
    A mathematical domain is designated "Pirouette" if and only if it passes three sequential gates: its invariants must be stable under SR-0…6 (SR Gate), its structures must be compatible with U(1)/SU(2)/SU(3)/GR without new free parameters (Σ Gate), and it must generate at least one new, falsifiable prediction (Falsifiability Gate). Failure at any gate results in a "non-pirouette" classification.
  philosophy: |
    The PCT operationalizes the 'stickiness' diagnostic, selecting invented formalisms that can become physically load-bearing. It distinguishes between math as a mere descriptive language and math as an integral part of the system's stabilizer grammar, enforcing a discipline that prevents the accumulation of elegant but physically inert structures.
pirouette_definition: |
  The Pirouette-Compliance Test (PCT) is a three-stage validation protocol applied to a mathematical domain \( \mathcal{D} \) to determine if it is "pirouette" (physically load-bearing). The three gates are:
  1.  **PCT-1 (SR Gate):** Stability of the domain's invariants under the transformations of SR-0 through SR-6, while preserving Causal Partitioning Maps (CPM).
  2.  **PCT-2 (Σ Gate):** Compatibility of the domain's structures, under the Σ spatialization map, with established gauge symmetries (U(1), SU(2), SU(3)) and the GR constitutive law, without introducing new ad-hoc constants.
  3.  **PCT-3 (Falsifiability Gate):** The domain's integration into the framework must yield at least one new, testable prediction with a clear experimental null hypothesis.
operational_definition:
  units: Dimensionless (Binary Pass/Fail per gate).
  symbol_table:
    - name: PCT-1
      meaning: SR Gate; tests for stability of invariants under SR-0…6.
      dimensions: dimensionless
      default_range: Pass/Fail
    - name: PCT-2
      meaning: Σ Gate; tests for structural compatibility with gauge/gravity formalism without new parameters.
      dimensions: dimensionless
      default_range: Pass/Fail
    - name: PCT-3
      meaning: Falsifiability Gate; tests for the generation of a new, testable prediction.
      dimensions: dimensionless
      default_range: Pass/Fail
  measurement:
    procedures:
      - name: PCT Domain Analysis
        outline: |
          A theoretical assessment of a candidate mathematical domain \( \mathcal{D} \).
          1.  **SR Gate:** Construct an embedding of \( \mathcal{D} \) into the framework. Apply SR-0...6 transformations and verify that the core invariants of \( \mathcal{D} \) are preserved. Check for forbidden polarizations or Lorentz violations in the IR limit.
          2.  **Σ Gate:** Apply the Σ map to the embedded structures of \( \mathcal{D} \). Verify that the resulting geometric/field structures support standard model gauge groups and GR dynamics natively. Confirm no new tunable parameters were required for this mapping.
          3.  **Falsifiability Gate:** Graft \( \mathcal{D} \) into an active XXP analysis (e.g., GR hydrolimit, YM emergence). Derive a new quantitative bound, scaling law, or spectral feature at \(\mathcal{O}((\omega/\omega_c)^2)\) or better, and specify the experimental signature that would falsify it.
        expected_signals: [A formal proof of compliance for all three gates, documented in a domain 'card'.]
        pitfalls: [Confusing mathematical elegance for Σ-compatibility, introducing hidden free parameters ("inflating the constant ledger"), generating predictions that are experimentally inaccessible or tautological.]
context_windows:
  - module: MATH-PHI-001
    excerpt: |
      A domain is **Pirouette** iff it passes all three gates:
      - **PCT-1 (SR Gate):** There exists an embedding of \( \mathcal{D} \) whose invariants are stable under **SR-0…6** *and* preserve CPM (no forbidden polarizations, no IR Lorentz violation).
      - **PCT-2 (Σ Gate):** Under Σ pushforward, the images of \( \mathcal{D} \) support **U(1)/SU(2)/SU(3)** frame relabelings or the GR constitutive law **without** inflating the constant ledger (no ad-hoc knobs).
      - **PCT-3 (Falsifiability Gate):** The graft produces at least one **testable** prediction at \(\mathcal{O}((\omega/\omega_c)^2)\) or better, with a clear kill-switch condition.
  - module: MATH-PHI-001
    excerpt: |
      **CI gate.** Any domain with \( \mathrm{Stk} \ge 0.6 \) and \( \mathrm{RPA} \ge \tau \) is **promoted** to “pirouette” and may modify children modules; else remains a helper. [...]
      **AC-1**: PCT passes for any domain marked “pirouette”.
      **AC-4**: Any elevated domain yields at least one **XXP** falsifiable bound, wired to tests.
poetic_connections:
  motifs: [stickiness, load-bearing, stabilizer grammar, junkyard vs goldmine, loom and mesh]
  evocative_lines:
    - "Most math is a net. The sticky math is the mesh that the loom itself uses."
    - "We invent nets. The loom keeps only what catches its threads with less and less mesh."
  association_matrix:
    - [ "STICKINESS", 0.9 ]
    - [ "SIGMA_COMPATIBILITY", 0.8 ]
    - [ "FALSIFIABILITY", 0.8 ]
    - [ "REVERSE_PARETO_ANALYSIS", 0.5 ]
formal_mappings:
  candidates:
    - target: Anomaly Cancellation Checks
      domain: QFT
      mapping_kind: conceptual
      justification: |
        Like anomaly cancellation, the PCT is a meta-level consistency check that a theoretical structure (here, a mathematical domain) must pass to be considered a valid component of a physical model. Both act as filters against internally inconsistent or physically pathological constructs.
      confidence: 0.8
    - target: Swampland Conjectures
      domain: String Theory
      mapping_kind: conceptual
      justification: |
        The PCT functions similarly to Swampland criteria, which delineate which effective field theories can be consistently coupled to quantum gravity. The Σ Gate, in particular, acts as a "UV-consistency" check for mathematical structures, ensuring they are compatible with the framework's core physical postulates (gauge theory, GR).
      confidence: 0.7
    - target: Popperian Falsifiability
      domain: Philosophy of Science
      mapping_kind: conceptual
      justification: |
        PCT-3 is a direct operationalization of Karl Popper's criterion of falsifiability. It mandates that any mathematical structure elevated to "pirouette" status must increase the empirical vulnerability of the overall theory, preventing the addition of purely aesthetic or unfalsifiable complexity.
      confidence: 0.9
  adopted:
    - target: none-adopted
      rationale: The PCT is a framework-internal protocol. While conceptually analogous to external concepts, a direct mapping is inappropriate as its specific gates (SR, Σ) are unique to the Pirouette context.
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "A mathematical domain that passes all three PCT gates will have a high Stickiness score (Stk ≥ 0.6)."
      domain: theory
      falsifier: "Finding a domain that passes all gates but yields low compression power (C) and few new falsifiable predictions (P), resulting in a low Stk score. This would indicate the PCT gates are insufficient to guarantee 'stickiness'."
      status: proposed
      links: [MATH-PHI-001]
    - statement: "No mathematical domain currently classified as 'Junkyard' (e.g., p-adic analysis as a primary ontology) can pass the PCT."
      domain: theory
      falsifier: "A novel discovery that provides a Σ-compatible embedding of a 'Junkyard' domain, allowing it to pass PCT-2 and subsequently generate a unique, confirmed prediction, thus passing PCT-3."
      status: under-test
      links: [MATH-PHI-001]
naming_notes:
  collisions: [The symbol "PCT" is famously used for the "Parity, Charge-conjugation, Time-reversal" symmetry theorem in quantum field theory. This is a significant collision.]
  disambiguation: |
    Within the Pirouette Framework, PCT always refers to the Pirouette-Compliance Test for *mathematical domains*. The CPT/PCT theorem of QFT concerns discrete symmetries of a physical Lagrangian. Context (discussion of math vs. physics) is the primary disambiguator.
crosslinks:
  near_synonyms: []
  antonyms: [NON_PIROUETTE_DOMAIN]
  prerequisites: [SR_RULES, SIGMA_MAP]
  downstream_effects: [STICKINESS, REVERSE_PARETO_ANALYSIS]
license: CC-BY-SA-4.0
---