---
term: "Effective cross-section"
canonical_id: "EFFECTIVE_CROSS_SECTION"
symbol: "(σ/m)_eff"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["SECT-001"]
---

---
term: Effective cross-section
canonical_id: EFFECTIVE_CROSS_SECTION
symbol: (σ/m)_eff
aliases: ['Macroscopic Drag Proxy', 'SIDM Proxy']
parents: ['SECT-001']
children: []
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: SECT-001
      lines: "Section 4"
      snippet: |
        Two superfluid halos interpenetrate with negligible microscopic scattering; **macroscopic drag** arises from phonon radiation & interface work:
        • Effective cross‑section proxy: (σ/m)_eff ≈ C_sf (σ, ξ, c_s, v_rel) with C_sf computed from interface perturbations.
        • Prediction (Bullet‑like): (σ/m)_eff ≲ 0.2 cm² g⁻¹ with frozen parameters; redshift scaling fixed by n_0(a).
  editors: ['Agent: Pirouette Definer']
  review_log: []
triad:
  art: |
    Galaxies glide through one another like ghosts, yet their passage ripples the cosmic superfluid, creating a drag that mimics a physical collision.
  law: |
    (σ/m)_eff is the effective area-to-mass ratio inferred from the observed deceleration and spatial offset of dark matter halos during a merger, caused by macroscopic drag forces (phonon radiation, interface work) rather than microscopic particle collisions.
  philosophy: |
    This decouples the phenomenology of self-interacting dark matter from the requirement of a new fundamental interaction, attributing galaxy-scale friction to the collective, emergent properties of a cosmic superfluid.
pirouette_definition: |
  The effective cross-section, (σ/m)_eff, is a phenomenological parameter quantifying the strength of macroscopic drag on a dark matter halo moving through the cosmic superfluid. It is not a fundamental particle scattering cross-section. Instead, it arises from the collective dynamics of the superfluid during halo interpenetration, specifically from energy loss to phonon radiation and work done against surface tension at the halo-background interface. Its value is a function of superfluid parameters (surface tension σ, healing length ξ, sound speed c_s) and the kinematic state (relative velocity v_rel) of the merger.
operational_definition:
  units: cm² g⁻¹
  symbol_table:
    - name: (σ/m)_eff
      meaning: Effective cross-section per unit mass
      dimensions: L² M⁻¹
      default_range: 0–0.2 cm² g⁻¹
    - name: C_sf
      meaning: Functional form for the drag calculation
      dimensions: L² M⁻¹
      default_range: contextual
    - name: σ
      meaning: Superfluid surface tension
      dimensions: M T⁻²
      default_range: contextual
    - name: v_rel
      meaning: Relative velocity between merging halos
      dimensions: L T⁻¹
      default_range: 100–3000 km s⁻¹
  measurement:
    procedures:
      - name: Merger Offset Inference
        outline: |
          1. Observe a merging galaxy cluster using multi-wavelength astronomy.
          2. Identify the spatial distribution of the baryonic gas component (typically via X-ray emission from hot gas).
          3. Identify the spatial distribution of the total mass, dominated by the dark matter halo (typically via gravitational lensing).
          4. Measure the projected spatial offset (Δx) between the centroids of the gas and the dark matter.
          5. Run N-body/hydrodynamic simulations of the merger, incorporating the superfluid drag model.
          6. Vary the input (σ/m)_eff until the simulated offset Δx matches the observed offset.
        expected_signals: [A non-zero spatial offset between lensing and X-ray centroids, A characteristic dependence of the offset magnitude on the estimated impact parameter and relative velocity]
        pitfalls: [Projection effects obscuring the true 3D geometry of the collision, Uncertainty in the merger's age and initial conditions, Contamination from baryonic feedback or magnetic fields affecting gas dynamics]
context_windows:
  - module: SECT-001
    excerpt: |
      Section 4 — Mergers & Offsets (Effective σ/m proxy)
      Two superfluid halos interpenetrate with negligible microscopic scattering; **macroscopic drag** arises from phonon radiation & interface work:
      • Effective cross‑section proxy: (σ/m)_eff ≈ C_sf (σ, ξ, c_s, v_rel) with C_sf computed from interface perturbations.
      • Prediction (Bullet‑like): (σ/m)_eff ≲ 0.2 cm² g⁻¹ with frozen parameters; redshift scaling fixed by n_0(a).
  - module: SECT-001
    excerpt: |
      Section 6 — Distinctive, Falsifiable Signatures
      ...
      B) **Merger offset scaling** without invoking particulate self‑interaction; predicts specific v_rel dependence through interface work.
      ...
      Section 8 — Preregistered Targets (OOS)
      ...
      • Merger Δx scaling vs. v_rel with predicted (σ/m)_eff ceiling.
poetic_connections:
  motifs: [superfluid drag, phantom friction, emergent collision, interface ripple]
  evocative_lines:
    - "Two superfluid halos interpenetrate with negligible microscopic scattering..."
    - "macroscopic drag arises from phonon radiation & interface work"
  association_matrix:
    - [ "SURFACE_TENSION", 0.9 ]
    - [ "HALO_MERGER", 0.8 ]
    - [ "HEALING_LENGTH", 0.6 ]
    - [ "SOUND_SPEED", 0.5 ]
formal_mappings:
  candidates:
    - target: Self-Interacting Dark Matter (SIDM) cross section, σ_SI/m
      domain: Astro/Cosmo
      mapping_kind: operational
      equation_hint: |
        F_drag ∝ ρ_halo · v_rel² · (σ/m)_eff
      justification: |
        Both (σ/m)_eff and the SIDM cross-section are parameters used in simulations to model the drag force experienced by dark matter halos during mergers. They are operationally equivalent in that they are both constrained by the same observable (e.g., the Bullet Cluster offset). However, the underlying physical mechanism is fundamentally different: particulate scattering (SIDM) versus collective fluid dynamics (Pirouette).
      references:
        - title: Dark matter self-interactions and small-scale structure
          where: Phys.Rept. 830 (2019) 1-60
          date: 2019-10-01
      confidence: 0.9
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The value of (σ/m)_eff is not constant but depends on the relative merger velocity (v_rel) and scales with cosmological redshift via the background superfluid density n_0(a)."
      domain: phenomenology
      falsifier: "Observing a sample of mergers that show (σ/m)_eff is constant across a wide range of velocities, or that its redshift scaling is inconsistent with the predicted C_sf(v_rel, n_0(a)) function."
      status: proposed
      links: ['SECT-001']
    - statement: "The superfluid model, with parameters fixed by CMB and halo core data, predicts a ceiling for the effective cross-section of (σ/m)_eff ≲ 0.2 cm² g⁻¹."
      domain: theory
      falsifier: "A robust measurement of (σ/m)_eff significantly exceeding this value (e.g., > 0.5 cm² g⁻¹) in a system where the model is expected to apply."
      status: proposed
      links: ['SECT-001']
naming_notes:
  collisions: ['The symbol σ is used for superfluid surface tension in SECT-001.']
  disambiguation: |
    (σ/m)_eff is a single, composite symbol representing a macroscopic, emergent property. It must not be confused with a microscopic particle cross-section. The 'σ' in this term is a proxy for an area and is distinct from the symbol 'σ' used alone to denote the superfluid's surface tension, which is one of the physical inputs used to calculate (σ/m)_eff.
crosslinks:
  near_synonyms: []
  antonyms: ['MICROSCOPIC_CROSS_SECTION']
  prerequisites: ['SURFACE_TENSION', 'HEALING_LENGTH', 'SOUND_SPEED']
  downstream_effects: ['HALO_MERGER_OFFSET']
license: CC-BY-SA-4.0
---