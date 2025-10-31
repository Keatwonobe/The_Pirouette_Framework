---
term: "Effective Drag"
canonical_id: "EFFECTIVE_DRAG"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["COSMO-006"]
---

---
term: Effective Drag
canonical_id: EFFECTIVE_DRAG
symbol: (σ/m)ₑff
aliases: ["superfluid drag", "merger drag"]
parents: ["COSMO-006", "COSMO‑Γ‑MERGE"]
children: []
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: COSMO-006
      lines: "Section 4"
      snippet: |
        Hydro‑Poisson + interface tracking (level set). Effective drag from interface work and phonon radiation → (σ/m)_eff prediction as a function of (v_rel, n, σ, ξ).
  editors: ["Pirouette Agent"]
  review_log: []
triad:
  art: |
    Like two oil drops in water, merging halos ripple the cosmic superfluid, shedding energy not as heat but as quantum whispers and stretched surfaces. This friction, born of quantum texture, slows their final embrace.
  law: |
    Effective Drag is a dissipative force on merging superfluid halos, parameterized by (σ/m)ₑff, which is a computable function of relative velocity, background density, intrinsic surface tension, and healing length. Its magnitude is directly proportional to the observable offset between the halo's core and its associated stellar component.
  philosophy: |
    Effective Drag provides a mechanism to generate observable offsets in mergers without invoking standard baryonic or dynamical friction. It transforms abstract superfluid parameters (surface tension σ, healing length ξ) into a concrete, potentially observable astrophysical signature, thus testing the core tenets of the superfluid model on galactic scales.
pirouette_definition: |
  Effective Drag is a velocity-dependent dissipative force that opposes the motion of superfluid halos during mergers. It arises from two primary physical mechanisms within the superfluid hydrodynamics model (SECT‑Γ‑A‑HALO): (1) energy loss due to the work done in deforming and merging the halo-background interface (surface tension), and (2) energy radiated away as phonons (sound waves) into the surrounding medium. The strength of this force is encapsulated by the (σ/m)ₑff parameter, which is a key prediction of merger simulations.
operational_definition:
  units: cm²/g or other units of area/mass
  symbol_table:
    - name: (σ/m)ₑff
      meaning: Effective self-interaction cross-section per unit mass, derived from drag effects.
      dimensions: L² M⁻¹
      default_range: "0.1–10 cm²/g"
    - name: Δ_x
      meaning: Spatial offset between a dark matter halo core and its baryonic counterpart post-merger.
      dimensions: L
      default_range: "1–100 kpc"
    - name: v_rel
      meaning: Relative velocity of the two merging halos.
      dimensions: L T⁻¹
      default_range: "100–3000 km/s"
    - name: σ
      meaning: Intrinsic surface tension of the superfluid interface.
      dimensions: M T⁻²
      default_range: contextual
    - name: ξ
      meaning: Healing length of the superfluid.
      dimensions: L
      default_range: contextual
  measurement:
    procedures:
      - name: Merger Offset Inference
        outline: |
          1. Identify a galaxy cluster with evidence of a recent merger (e.g., Bullet Cluster-like systems).
          2. Independently map the total mass distribution (via gravitational lensing) and the stellar/gas distribution (via optical/X-ray imaging).
          3. Measure the spatial offset Δ_x between the centroid of the total mass and the centroid of the baryonic component.
          4. Run a suite of Pirouette superfluid merger simulations (COSMO-006) varying input parameters (σ, ξ, P(X)) to match the observed merger kinematics.
          5. The value of (σ/m)ₑff from the simulation that reproduces the observed offset Δ_x is the inferred measurement.
        expected_signals: ["Non-zero spatial offset Δ_x between lensing mass peak and galaxy peak", "Wake-like structures or density ripples in the lensing map"]
        pitfalls: ["Projection effects misrepresenting the true 3D offset", "Baryonic feedback or ram pressure stripping mimicking a drag-induced offset", "Insufficient resolution in lensing or baryonic maps"]
context_windows:
  - module: COSMO-006
    excerpt: |
      Hydro‑Poisson + interface tracking (level set). Effective drag from interface work and phonon radiation → (σ/m)_eff prediction as a function of (v_rel, n, σ, ξ). The `merge_sf.json` artifact contains the primary outputs: `{Delta_x, sigma_over_m_eff, shock_Mach, …}`.
poetic_connections:
  motifs: ["friction", "interface", "dissipation", "ripple", "viscosity"]
  evocative_lines:
    - "Effective drag from interface work and phonon radiation"
  association_matrix:
    - [ "SURFACE_TENSION", 0.9 ]
    - [ "MERGER_OFFSET", 0.9 ]
    - [ "HEALING_LENGTH", 0.7 ]
    - [ "PHONON", 0.6 ]
formal_mappings:
  candidates:
    - target: Self-Interacting Dark Matter (SIDM) drag force
      domain: CM
      mapping_kind: operational
      equation_hint: |
        F_drag ∝ ρ_DM (σ/m) v_rel²
      justification: |
        Both Effective Drag in Pirouette and the drag force in SIDM models produce an effective friction between dark matter components, leading to observable offsets in galaxy mergers. The (σ/m)ₑff parameter is operationally analogous to the SIDM cross-section per unit mass, as both are constrained by the magnitude of these offsets.
      references:
        - title: "The self-interacting dark matter paradigm"
          where: "arXiv:1707.05323"
          date: 2017-07-17
      confidence: 0.8
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The magnitude of (σ/m)ₑff is a non-monotonic function of relative velocity v_rel due to the transition between the interface-dominated regime (low v_rel) and the phonon-radiation-dominated regime (high v_rel)."
      domain: theory
      falsifier: "Simulations within the SECT‑Γ‑A‑HALO framework consistently show a monotonic relationship between (σ/m)ₑff and v_rel across all tested parameter spaces."
      status: proposed
      links: ["COSMO-006"]
naming_notes:
  collisions: []
  disambiguation: |
    Distinguish from standard 'dynamical friction' acting on massive bodies in a collisionless medium, which depends on the gravitational wake, not on fluid properties like surface tension. Also distinguish from viscous drag in a classical fluid, as the mechanisms (interface work, phonon radiation) are quantum in origin.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: ["SURFACE_TENSION", "HEALING_LENGTH"]
  downstream_effects: ["MERGER_OFFSET"]
license: CC-BY-SA-4.0
---