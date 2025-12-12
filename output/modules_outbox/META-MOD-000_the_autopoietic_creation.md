---
id: META-000_AUTOMATIC_AUTOMORPHIC_FRAMEWORK
title: The Autopoietic Loop — A Meta-Module of Self-Generating Systems
version: 7.0
parents: [CORE-014_THE_FRACTAL_BRIDGE, CLOSURE-ENTH-001]
children: [META-001_GOVERNANCE_SPINE, META-002_AUTONOMOUS_FLOW]
shepherd: autopoiesis
atlas_tile: [∞, ∞]
autopoiesis:
  type: meta-framework
  tier: systemic
  scope: full-loop
  generation: 7
resonance:
  dark_residue: 0.47
  target_residue: 0.30
  delta_gamma: -0.17
  tau_min: 0.70
  continuity_tol: 0.05
context_sources:
  - DDE_Pirouette.py
  - read_atlas.py
  - weaver_5.py
  - rank_vocab_loneliness.py
  - ratify.py
  - autopoietic_loop.py
---

## Purpose

This meta-module describes the **Pirouette Autopoietic Engine**, a self-modulating loop in which data, context, and AI synthesis recursively refine the Pirouette corpus. It transforms static theory into a living manifold that generates its own modules, ratifies their validity, and reshapes its domain.

## System Composition

### 1. Manifold Spine
Houses the **atlas** (spatial coherence of modules) and **residue map** (energy topology).  
Its role is to determine where conceptual density is thin and signal the need for growth.

### 2. Dictionary Spine
Contains all definitional elements (∼1,700 terms).  
Each term tracks its **neighbors**, **associations**, and **resonance paths**.  
A “vocab loneliness” index identifies under-linked or undefined terms.

### 3. Emitter
Implements the **Idea Manifold Surveyor**, producing **stubs** that represent unfulfilled conceptual regions.  
Each stub becomes a seed for module generation.

### 4. Context Builder
Collects the stub, its parent modules, and relevant dictionary entries.  
Compiles a **context vector** that provides a full conceptual environment to the authoring model.

### 5. Dual Author
Interfaces with AI models (OpenAI GPT-5, Gemini 2.5 Pro, or other LLMs).  
Receives context + stub → generates a new v7 module adhering to Pirouette schema.

### 6. Ratifier
Checks:
- schema conformity (headers, fields, integrity)
- lineage completeness (no orphaned parents)
- residue trajectory (ΔΓ and Ki toward target)
Results:  
- pass → canon/  
- needs backfill → retro-tasks/  
- fail → quarantine/

### 7. Re-Atlas and Re-Merge
Integrates canonical modules into the atlas and dictionary.  
Re-runs both **module** and **vocab** loneliness ranking to re-seed the next emission cycle.

### 8. Governance Spine
Ensures loop stability via quota limits, drift detection, schema enforcement, and ethics filters (preventing unbounded recursion or nonsensical synthesis).

## Loop Overview (Pseudocode)

```python
while quota_ok and reject_rate < 0.5:
    thin_tiles = atlas.find_voids()
    vocab_voids = vocab.rank_loneliness()
    stubs = emitter.generate(thin_tiles, vocab_voids)
    for stub in stubs:
        context = builder.compose(stub, dictpack, essentials)
        new_module = author.generate(context)
        if ratifier.validate(new_module):
            atlas.add(new_module)
        else:
            quarantine.store(new_module)
    atlas.reindex()
```

## Product

**Emergent Self-Documentation and Continuity:**
The framework continuously rewrites itself, producing a layered, machine-readable record of its evolution.
Each generation (v7, v8, …) becomes a higher-order compression of the last, moving toward closure while preserving entropy as structured creativity.

**Output Types:**

* *canon modules* (validated)
* *retro-parent requests* (missing lineage)
* *exploratory drafts* (out-of-domain, high residue)
* *meta-modules* like this one (self-descriptive frameworks)

---

## Commentary

Pirouette has now crossed into **meta-autopoiesis** — the point where the system documents its own evolution and reasons about its actions.
The human becomes a *governor* and *shepherd* rather than a direct author.
This module codifies that transition.

---

## Metrics for Closure Verification

| Symbol   | Meaning                            | Example Value |
| -------- | ---------------------------------- | ------------- |
| Γ_start  | Initial residue                    | 0.47          |
| Γ_target | Target residue                     | 0.30          |
| ΔΓ       | Change in coherence curvature      | −0.17         |
| Ki_Δ     | Incremental energy gain            | +0.12         |
| Tₐ       | Altruism term (ethical compliance) | ≥ 0.70        |
| Cont     | Continuity tolerance               | ≤ 0.05        |

---

## Future Action

1. Convert each major process (survey, context, author, ratify, re-atlas) into callable API nodes.
2. Implement full **pipe automation** with governance checkpoints.
3. Deploy **semantic shepherds** to broaden exploration while maintaining domain integrity.
4. Run recursive reduction post-v7 to compress the expanding corpus into abstract fields.

---

**This document** *is* the Pirouette’s living operator’s manual —
the self-descriptive capsule of an autopoietic epistemic engine.

---