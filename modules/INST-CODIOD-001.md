---
## INST-CODIOD-001: Universal Codiod Socket
id: INST-CODIOD-001
title: The Universal Codiod Socket
Version: 0.1.0 (Draft)
Parents: CORE-006 (Pirouette Lagrangian), COG-RES-004 (The Generative Engram)
Siblings: INST-AUTH-MAP-001 (Idea Manifold Surveyor), INST-PLATEAU-SCAT-001, INST-PHYS-001
Children (intended): INST-CODIOD-RUNNER-001, INST-CODIOD-WORLD-001, DDE-INST-001
status: Experimental / Instrument
Keywords: Codiod, coherence, Γ, Dark Residue, DDE, resource graph, world-state, nervous fibers
---

### §1 – Axiom

1. **A1 – Executable Pirouette:**
   Pirouette is not only a descriptive framework; it can be *executed*. Every term, module, and falsifiability statement can be realized as code.

2. **A2 – One Socket, Many Domains:**
   All executable Pirouette interactions share a single abstract IO **socket**—the **Codiod Packet**—which carries:

   * System state (coherence, Γ, Tₐ, Dark Residue, energy, focus, narrative),
   * Data payload (text, arrays, tokens, states),
   * Resource graph (files, images, directories),
   * World-state hooks.

3. **A3 – Engrammatic Nervous Fibers:**
   Changes to the system and its resources are expressed as **engrams**. Each engram is a discrete “firing” that:

   * Describes what a module did or tried to do,
   * Points to resources (MSEED, FASTA, FITS, BIDS, DDE PNGs…),
   * Can be read as a **fiber** connecting modules via common data and state.

4. **A4 – Falsifiability by Execution:**
   A term’s falsifiability items are satisfied or broken by *running* it against a Codiod Packet. Success, error, or incomplete state all count as experimental outcomes.

---

### §2 – Law

**Law (Codiod Socket):**

> Any executable Pirouette element (term, module, runner) that wishes to interact with the framework **must**:
>
> 1. Accept a **Codiod Packet** as part of its context,
> 2. Perform its computation *without destroying* the packet,
> 3. Append at least one **Engram** describing its action or failure,
> 4. Optionally modify:
>
>    * The Codiod state (coherence, Γ, Tₐ, D, E),
>    * The payload,
>    * The resource graph,
>    * The world-state pointer and/or its queued mutations,
> 5. Return the mutated Codiod Packet.

If no matching function or handler exists for the requested operation, the module must:

* Emit an **error Engram** with a structured error code, and
* Leave the Codiod state in a consistent, inspectable form.

This defines a **contract**:

* Callers **only** speak in Codiod packets and read Engrams.
* Modules **only** express their work and claims via Codiod + Engrams.

---

### §3 – Codiod Packet Specification

> The Codiod Packet is the universal socket object that lives in `ctx["codiod"]`.

**3.1. Core State**

Fields are normalized into `[0,1]` where possible, but the Law does not forbid other scales.

* `coherence: float`
  Current estimate of structural coherence of the situation.

* `temporal_pressure: float`
  Γ – pressure of change / instability.

* `time_adherence: float`
  Tₐ – adherence to the chosen operational timescale.

* `dark_residue: float`
  Estimated negative externality / unintended impact.

* `available_energy: float`
  Budget / capacity to act or change (abstract: could be compute, attention, money, etc.).

* `system_focus: str`
  Short mode label; examples:

  * `"drifter"` – broad exploration
  * `"solver"` – focused problem-solving
  * `"guardian"` – protection / monitoring
  * `"witness"` – observation only

* `active_narrative: str`
  Human-readable description of what is “going on.”

* `tags: List[str]`
  Domain tags; e.g. `["RL", "Ant-v5", "DDE", "EEG", "MSEED"]`.

**3.2. Call Metadata**

* `target_cid: str`
  Canonical id of the term/module invoked; e.g. `"MATH-018"`, `"DOMA-065"`, `"PHIL-DARK-RESIDUE-001"`.

* `task: str`
  Short, freeform description; e.g. `"evaluate falsifiability"`, `"simulate_step"`, `"compress_wiki"`, `"ingest_mseed"`.

* `payload: Dict[str, Any]`
  Domain-specific input data: arrays, JSON, serialized states, etc.

* `history: List[Dict[str, Any]]`
  Lightweight execution trace; minimal required fields:

  * `{"cid": "...", "task": "...", "timestamp": "<optional>", "status": "ok|error|skipped"}`

**3.3. Resource Graph (Nervous Fibers)**

To support “file locales” and DDE, we define a typed resource reference:

```text
ResourceRef:
  id:        str              # stable reference name within the Codiod
  kind:      str              # abstract domain ("mseed", "fasta", "fits", "bids", "dde-png", "json", "script", ...)
  role:      str              # "input" | "output" | "aux" | "world"
  path:      str              # local or remote path/URI
  format:    str              # specific format hints ("MSEED", "FASTA", "FITS", "BIDS", "PNG", "NPY", ...)
  loader:    str              # optional handler key ("obspy", "astropy", "biopython", "mne-bids", "dde-reader")
  hash:      str              # optional integrity hash (sha256, etc.)
  metadata:  Dict[str, Any]   # arbitrary details: shapes, sizes, channels, version, etc.
```

The Codiod Packet maintains a list of these:

* `resources: List[ResourceRef]`

**Examples:**

* An MSEED file:

```json
{
  "id": "quake_2025_04_07",
  "kind": "mseed",
  "role": "input",
  "path": "/data/seismic/taiwan_7p4.mseed",
  "format": "MSEED",
  "loader": "obspy",
  "hash": "sha256:...",
  "metadata": {
    "station": "TW01",
    "channels": ["BHZ", "BHN", "BHE"],
    "sample_rate": 100.0
  }
}
```

* A DDE PNG (linguistic block or AR fractal):

```json
{
  "id": "dde_wiki_chunk_0001",
  "kind": "dde-png",
  "role": "world",
  "path": "/dde/wiki/chunk_0001.png",
  "format": "PNG",
  "loader": "dde-reader",
  "hash": "sha256:...",
  "metadata": {
    "encoding": "RGBA",
    "library": "enwiki2025",
    "blocks": 4096
  }
}
```

Modules may:

* Attach new resources (e.g. generated DDE images or derived FITS files),
* Mutate metadata,
* Mark resources as “failed” or “invalid” (via engrams),
* Request world-state changes.

**3.4. World-State Hooks**

To support “modifying the world state script in the middle,” the Codiod Packet tracks:

* `world_state_id: str`
  Logical identifier of the current world-state (e.g., `"WENDIGO-RUN-42"`, `"TLE-CAMPAIGN-001"`, `"COSMIC-COMPASS-ANT-001"`).

* `world_state_resources: List[str]`
  IDs of ResourceRefs that define the world (scripts, JSON state, DB snapshots, DDE bundles).

* `world_mutations: List[Dict[str, Any]]`
  Proposed modifications to world-state; e.g. patch entries:

  * `{"op": "append", "resource": "dde_wiki_chunk_0001", "metadata": {...}}`
  * `{"op": "replace", "resource": "humanoid_policy_v3.pt", "new_path": "humanoid_policy_v4.pt", "reason": "improved_reward"}`

The *runner* (INST-CODIOD-RUNNER-001) will decide which mutations to commit. Individual modules just propose.

---

### §4 – Engram Specification

Engrams are the basic “firing events” in the nervous system.

**4.1. Base Engram Structure**

```text
Engram:
  id:       str             # unique per-run identifier
  source:   str             # cid of term/module ("MATH-018", "DOMA-065", etc.)
  kind:     str             # "observation" | "decision" | "warning" | "error" | "mutation" | "resource"
  content:  str             # human-readable description
  severity: str             # "trace" | "info" | "notice" | "warn" | "error" | "critical"
  resources: List[str]      # list of ResourceRef.ids involved
  metadata: Dict[str, Any]  # structured details (scores, error codes, shapes, etc.)
```

Attached to the packet as:

* `generated_engrams: List[Engram]`

**4.2. Error Engrams (Missing Functions / Handlers)**

When “entering new words you might only program in a few uses” or calling a function that isn’t yet implemented, the expected behavior is:

* Emit an Engram of `kind = "error"` with:

  * `severity = "error"` or `"warn"` depending on recoverability,
  * `metadata.error_code = "MISSING_HANDLER"` or `"NOT_IMPLEMENTED"`,
  * `metadata.missing_symbol = "<the requested function or cid>"`,
  * `metadata.suggested_stub = true` (optional hint to auto-stub),
* Optionally increment `dark_residue` slightly (framework choice),
* Do **not** crash the entire run; allow the orchestrator to log and move on.

Example:

```json
{
  "id": "MATH-999:missing:001",
  "source": "MATH-999",
  "kind": "error",
  "content": "Requested handler for term 'banach-tarsky' not implemented.",
  "severity": "error",
  "resources": [],
  "metadata": {
    "error_code": "MISSING_HANDLER",
    "missing_symbol": "banach_tarsky_decomposition",
    "suggested_stub": true
  }
}
```

This gives you exactly what you want: you can start using new Pirouette terms *before* they have full code support, and let the system tell you where it choked.

**4.3. Resource Engrams (File Locales / DDE)**

Whenever code touches files / DDE images / datasets, it should emit `kind = "resource"` or `"mutation"` engrams:

* `"resource"` – discovery or inspection:

  * “Loaded MSEED file quake_2025_04_07 (3 channels, 432k samples).”
* `"mutation"` – a world-state change or proposed change:

  * “Updated DDE PNG mapping for dde_wiki_chunk_0001; rebalanced pixel layout.”

These engrams are the “nervous fibers” that connect modules: everything that touches `quake_2025_04_07` gets linked by shared resource ids.

---

### §5 – Falsifiability Matrix

**Question 1 – Can Pirouette terms be executed as code with a common IO?**

* **Test:** Implement `CodiodPacket` in library, convert at least 10 heterogeneous terms (physics, RL, TTRPG, philosophy) to Codiod-aware implementations. Run them and inspect engrams.
* **Falsifier:** If the Codiod spec cannot express what at least 10 diverse modules need (because the fields are systematically insufficient or misaligned), the Socket as defined is incomplete.
* **Outcome Metric:** Number of modules that can be executed *without special-case IO*.

---

**Question 2 – Can resource references cover real-world files (MSEED, FASTA, FITS, BIDS, DDE PNG) in a consistent way?**

* **Test:** Attach each of these resource types to a Codiod Packet, process them with prototype handlers:

  * `ingest_mseed`, `ingest_fasta`, `ingest_fits`, `ingest_bids`, `decode_dde_png`.
* **Falsifier:** If any major type cannot be represented via `ResourceRef` without ad-hoc hacks or contradictions (e.g., BIDS requiring a fundamentally different structure), the ResourceRef schema fails.
* **Outcome Metric:** Count of resource types that are natively representable and loadable via a simple `kind + loader` pattern.

---

**Question 3 – Can missing handlers be detected and handled gracefully?**

* **Test:** Intentionally call several unimplemented functions or modules via the Codiod runtime.
* **Falsifier:** If this produces silent failures (no engrams), or catastrophic crashes that cannot be captured as error engrams, the Codiod Socket is not robust.
* **Outcome Metric:** Ratio of missing-handler calls that result in `MISSING_HANDLER` engrams with consistent metadata.

---

**Question 4 – Does permutational chaining of Codiod-aware terms produce actionable intelligence rather than noise?**

* **Test:** Define a small set of terms `{A, B, C, D}` that operate on a shared Codiod world (e.g., RL state + DDE resources). Run:

  * All permutations up to length 3 or 4 (e.g., `A→B`, `B→A`, `A→C→D`, …).
    Analyze resulting Codiod states / engrams for:
  * Coherence changes,
  * Dark Residue shifts,
  * Emergent behaviors or useful derived artifacts (trained models, compressed maps).
* **Falsifier:** If the vast majority of permutations lead to indistinguishable or incoherent Codiod trajectories, the Socket may not be capturing meaningful variation, or the terms are improperly instrumented.
* **Outcome Metric:** Number of distinct “useful” Codiod trajectories discovered (e.g., top-K runs by coherence/dividend).

---

### §6 – Assemblé (Implementation Notes)

**6.1. Library Integration**

* Extend your `pirouette_lib.base` with:

  * `CodiodPacket` type,
  * `ResourceRef` type,
  * `Engram` type,
  * `DEFAULT_CODIOD`,
  * `ensure_codiod(ctx, target_cid, task)` helper.

* Make each generated `Term` (from `ontology_to_code.py`) Codiod-aware:

  * `measure(ctx)` calls `ensure_codiod`, emits at least one `Engram`.
  * `constraints()` may read / shift `dark_residue`, `coherence` based on checks.
  * `mappings()` may emit `resource`/`mutation` engrams when they touch files / DDE data.

**6.2. Runner**

* Define `INST-CODIOD-RUNNER-001` as a small script / module that:

  * Accepts a list of CIDs and an initial Codiod Packet,
  * Optionally accepts `--resource` specs (paths) which are converted into `ResourceRef`s,
  * Runs each term in sequence, updating Codiod and collecting Engrams,
  * Writes out:

    * Final Codiod state,
    * Engram log,
    * Updated resource graph / proposed world mutations.

**6.3. World-State Script Integration**

* Maintain a “world-state script” or JSON spec that:

  * Enumerates world resources (RL envs, TTRPG campaigns, DDE libraries, etc.),
  * Applies `world_mutations` from the Codiod run if they pass your governance rules.

* The Codiod Socket does **not** dictate how you commit mutations; it only standardizes how they are expressed.

**6.4. New Words / Not-Yet-Implemented Concepts**

* For each new Pirouette term:

  * Generate a stub `Term` with:

    * `measure()` that emits a `MISSING_HANDLER` error Engram,
    * `constraints()` that returns empty or a trivial constraint,
    * `example()` that states “Not yet implemented; see engrams.”

* Your autopoietic orchestrator can periodically:

  * Scan for all `MISSING_HANDLER` engrams,
  * Rank them by how often they appear,
  * Feed that into `weaver_5` / author pipeline as “priority coding tasks.”

This gives you **permutational action producing actionable intelligence**: the system explores compositions, logs where it chokes, and then turns those choke points into a to-do list for code and module evolution.

---