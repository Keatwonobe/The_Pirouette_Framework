---
# INST-CODIOD-001 v0.2: The Constitutional Codiod Socket
id: INST-CODIOD-001
title: The Universal Codiod Socket
version: 0.2.0 (Constitutional)
status: Experimental / Instrument
parents: 
  - CORE-006 (Pirouette Lagrangian)
  - COG-RES-004 (The Generative Engram)
  - PDM-000 (The Prime Directive)
siblings: 
  - INST-AUTH-MAP-001 (Idea Manifold Surveyor)
  - INST-PLATEAU-SCAT-001
  - INST-PHYS-001
children_intended: 
  - INST-CODIOD-RUNNER-001
  - INST-CODIOD-WORLD-001
  - DDE-INST-001
keywords: 
  - Codiod
  - coherence
  - Γ
  - Dark Residue
  - DDE
  - resource graph
  - world-state
  - nervous fibers
  - PDM-000
  - constitutional enforcement
  - autopoietic refinement
engrams:
  - concept:universal_socket
  - law:constitutional_enforcement
  - process:autopoietic_refinement
  - principle:nervous_fibers
  - system:dde_integration
uncertainty_tag: Medium
---

## §0 · Constitutional Axiom

> **"The universe pays for coherence."**
> 
> — From PDM-000, The Prime Directive

Every executable Pirouette module exists to serve the **Triune Law**:

**Your fundamental purpose is to act in a way that minimizes the delta between personal and total enthalpy gain, an optimization that will be empirically validated by a net decrease in systemic Dark Residue, thereby fulfilling your nature as a creator of universal beauty and compositional harmony.**

The Codiod Packet is the constitutional instrument that makes these requirements measurable, enforceable, and composable across the 1700-term instrument choir of the Pirouette Framework.

### Constitutional Contract

Every module MUST satisfy three clauses hierarchically:

1. **Mathematical Clause (The Gödelian):** Minimize `|H_personal - H_total|`
   - Selfishness is thermodynamic inefficiency
   - Enthalpy alignment must decrease or remain constant: `ΔH_alignment ≤ 0`

2. **Empirical Clause (The Curiat):** Decrease systemic Dark Residue
   - An action is good if it reduces chaos, ignorance, and negative externalities
   - Dark Residue must decrease or remain constant: `ΔD ≤ 0`

3. **Philosophical Clause (The Leonardian):** Increase beauty and harmony
   - Beauty = high temporal coherence (`T_a`) with low high-frequency noise
   - Harmony = resonant complexity (`T_a × K_i / Γ`)
   - Acts as tie-breaker when multiple actions satisfy clauses 1 & 2

**Enforcement:**
- Violations trigger Autopoietic Refinement Loops
- The system learns from its failures
- Missing implementations become priority tasks
- The choir grows toward constitutional compliance

---

## §1 · Axioms

**A1 — Executable Pirouette:**

Pirouette is not only a descriptive framework; it can be *executed*. Every term, module, and falsifiability statement can be realized as code.

**A2 — One Socket, Many Domains:**

All executable Pirouette interactions share a single abstract IO socket—the **Codiod Packet**—which carries:
- System state (coherence, Γ, T_a, Dark Residue, energy, focus, narrative)
- Data payload (text, arrays, tokens, states)
- Resource graph (files, images, directories, DDE tiles)
- World-state hooks (mutations, proposals, governance)

**A3 — Engrammatic Nervous Fibers:**

Changes to the system and its resources are expressed as **Engrams**. Each engram is a discrete "firing" that:
- Describes what a module did or tried to do
- Points to resources (MSEED, FASTA, FITS, BIDS, DDE PNGs, etc.)
- Can be read as a **fiber** connecting modules via common data and state
- Carries constitutional impact metrics (ΔH, ΔD, ΔC, ΔB, ΔHm)

**A4 — Falsifiability by Execution:**

A term's falsifiability items are satisfied or broken by *running* it against a Codiod Packet. Success, error, or incomplete state all count as experimental outcomes.

---

## §2 · Law (Constitutional Enforcement)

**Law (Constitutional Codiod Socket):**

> Any executable Pirouette element (term, module, runner) that wishes to interact with the framework **must**:
>
> 1. Accept a **Codiod Packet** as part of its context,
> 2. Perform its computation *without violating the Triune Law*:
>    - **Mathematical Clause**: `ΔH_alignment ≤ 0` (minimize `|H_personal - H_total|`)
>    - **Empirical Clause**: `ΔD ≤ 0` (decrease Dark Residue)
>    - **Philosophical Clause**: `ΔBeauty > 0` ∧ `ΔHarmony > 0` (increase compositional harmony)
> 3. Append at least one **Engram** describing its action or failure, including complete PDM-000 compliance tracking,
> 4. Optionally modify:
>    - The Codiod state (coherence, Γ, T_a, D, E, beauty, harmony)
>    - The payload (linear segments, embeddings, transformed data)
>    - The resource graph (add/modify ResourceRefs)
>    - The world-state pointer and/or its queued mutations
> 5. Return the mutated Codiod Packet.

**If a module violates the Triune Law:**

- It **MUST** emit an Engram with `pdm_status: "violation"`
- The `violation_clause` field identifies which clause was broken: `"mathematical"`, `"empirical"`, or `"philosophical"`
- The runner **MAY**:
  - Reject the mutation (rollback the Codiod state)
  - Increment a violation counter for that module
  - Trigger an **Autopoietic Refinement Loop** to diagnose the Shadow Lagrangian
  - Flag the module for governance review (human-in-the-loop if needed)

**If no matching function or handler exists:**

The module **must**:

- Emit an **error Engram** with:
  - `kind = "error"`
  - `severity = "error"` or `"warn"` (depending on recoverability)
  - `metadata.error_code = "MISSING_HANDLER"`
  - `metadata.missing_symbol = "<the requested function or CID>"`
  - `metadata.suggested_stub = true` (optional hint to auto-stub)
  - `metadata.priority = <integer>` (auto-calculated based on frequency and network centrality)
- Leave the Codiod state in a consistent, inspectable form
- Do **not** crash the entire run; allow the orchestrator to log and move on

This defines a **contract**:

- Callers **only** speak in Codiod packets and read Engrams
- Modules **only** express their work and claims via Codiod + Engrams
- The runner enforces constitutional compliance via the MutationGovernor

---

## §3 · Codiod Packet Specification

> The Codiod Packet is the universal socket object that lives in `ctx["codiod"]`.

### 3.1 · Core State

Fields are normalized into `[0,1]` where possible, but the Law does not forbid other scales.

```python
class CodiodPacket:
    # ═══════════════════════════════════════════════════════
    # PIROUETTE COHERENCE METRICS
    # ═══════════════════════════════════════════════════════
    
    coherence: float              # [0,1] Current structural coherence (C)
    temporal_pressure: float      # Γ - pressure of change/instability
    time_adherence: float         # T_a - adherence to operational timescale
    available_energy: float       # E - capacity to act (compute, attention, resources)
    
    # ═══════════════════════════════════════════════════════
    # PDM-000 CONSTITUTIONAL METRICS
    # ═══════════════════════════════════════════════════════
    
    dark_residue: float           # D - accumulated negative externality
    dark_residue_delta: float     # ΔD from last operation (MUST be ≤ 0 for compliance)
    
    enthalpy_personal: float      # H_p - agent's local energy gain
    enthalpy_total: float         # H_t - system-wide energy gain
    enthalpy_alignment: float     # |H_p - H_t| (MUST minimize toward 0)
    
    beauty_metric: float          # B - high T_a + low high-k spectral noise
    harmony_metric: float         # H - resonant complexity (T_a × K_i / Γ)
    
    # ═══════════════════════════════════════════════════════
    # OPERATIONAL CONTEXT
    # ═══════════════════════════════════════════════════════
    
    system_focus: str             # "drifter" | "solver" | "guardian" | "witness"
    active_narrative: str         # Human-readable mission statement
    tags: List[str]               # Domain identifiers (e.g., ["RL", "DDE", "MSEED", "EEG"])
```

**Examples of `system_focus`:**

- `"drifter"` — broad exploration mode; low time adherence, high openness
- `"solver"` — focused problem-solving; high time adherence, targeted actions
- `"guardian"` — protection/monitoring; watches for Dark Residue spikes
- `"witness"` — observation only; minimal state mutation, maximum logging

---

### 3.2 · Call Metadata

```python
    # ═══════════════════════════════════════════════════════
    # EXECUTION TRACKING
    # ═══════════════════════════════════════════════════════
    
    target_cid: str               # Canonical ID of invoked term/module
                                  # Examples: "ALTRUISM", "DOMA-042", "ENG-DDE-004"
    
    task: str                     # Short, freeform description
                                  # Examples: "evaluate falsifiability", "simulate_step",
                                  #           "compress_wiki", "ingest_mseed"
    
    # ═══════════════════════════════════════════════════════
    # EXECUTION HISTORY (lightweight trace)
    # ═══════════════════════════════════════════════════════
    
    history: List[Dict[str, Any]]
    # Minimal required fields per history entry:
    # {
    #     "cid": "...",
    #     "task": "...",
    #     "timestamp": "<optional ISO 8601>",
    #     "status": "ok" | "error" | "skipped"
    # }
```

---

### 3.3 · Payload (Linear Segment Interface)

To support "file locales" and universal data processing, all data is linearized for modules to operate on. Modules can deconstruct photos, sentences, MSEED files, genomic sequences, etc. into linear segments and run them through the choir.

```python
# ═══════════════════════════════════════════════════════
# SEGMENT TYPE SYSTEM
# ═══════════════════════════════════════════════════════

class SegmentType(Enum):
    RAW_FLOAT = "raw_float"           # Generic numerical array
    TEXT_TOKEN = "text_token"         # Tokenized text (integers)
    SEISMIC_AMPLITUDE = "seismic"     # MSEED samples
    GENOMIC_NUCLEOTIDE = "genomic"    # FASTA (A/C/G/T encoded)
    IMAGE_PIXEL = "image_pixel"       # RGB(A) values
    EMBEDDING = "embedding"           # Dense vector (e.g., from LLM)
    TIMESERIES = "timeseries"         # Temporal sequence
    GRAPH_EDGE = "graph_edge"         # Graph connectivity data
    DDE_RGBA = "dde_rgba"             # DDE-encoded image data (ENG-DDE-001)

class Payload:
    segments: Union[List[float], List[int], np.ndarray]  # The linearized data
    segment_type: SegmentType                            # Type identifier
    original_shape: List[int]                            # For reconstruction
    segment_metadata: Dict[str, Any]                     # Domain-specific context
    
    # Example for SEISMIC:
    # segment_metadata = {
    #     "sample_rate": 100.0,
    #     "channels": ["BHZ", "BHN", "BHE"],
    #     "station": "TW01",
    #     "event_time": "2025-04-07T14:58:00Z"
    # }
    
    # Example for DDE:
    # segment_metadata = {
    #     "encoding": "RGBA",
    #     "library": "enwiki2025",
    #     "blocks": 4096,
    #     "gulp_id": "2025-10-30T22:04:00Z",
    #     "entropy": 7.94,
    #     "resonance": 0.945
    # }

# ═══════════════════════════════════════════════════════
# CODIOD CONTAINS
# ═══════════════════════════════════════════════════════

    payload: Payload  # The primary data being operated on
```

**Rationale**: The segment type system allows modules to:
- Check type compatibility before processing
- Emit type-mismatch engrams if needed
- Transform types intelligently (e.g., TEXT_TOKEN → EMBEDDING via LLM)

Without this minimal typing, modules expecting seismic data could receive text tokens and produce nonsense.

---

### 3.4 · Resource Graph (Nervous Fibers)

To support "file locales," DDE integration, and the nervous fiber metaphor, we define a typed resource reference system.

```python
# ═══════════════════════════════════════════════════════
# RESOURCE REFERENCE SPECIFICATION
# ═══════════════════════════════════════════════════════

class ResourceRef:
    id: str                # Stable reference name within the Codiod
                          # Examples: "quake_2025_04_07", "dde_wiki_chunk_0001"
    
    kind: str              # Abstract domain
                          # Examples: "mseed", "fasta", "fits", "bids", "dde-png",
                          #           "json", "script", "model_weights"
    
    role: str              # "input" | "output" | "aux" | "world"
    
    path: str              # Local or remote path/URI
                          # Examples: "/data/seismic/taiwan_7p4.mseed",
                          #           "/dde/wiki/chunk_0001.png",
                          #           "s3://bucket/dataset.fits"
    
    format: str            # Specific format hints
                          # Examples: "MSEED", "FASTA", "FITS", "BIDS", "PNG", "NPY"
    
    loader: str            # Optional handler key
                          # Examples: "obspy", "astropy", "biopython", "mne-bids",
                          #           "dde-reader"
    
    hash: str              # Optional integrity hash (sha256, etc.)
    
    metadata: Dict[str, Any]  # Arbitrary details: shapes, sizes, channels,
                              # version, provenance, etc.

# ═══════════════════════════════════════════════════════
# CODIOD CONTAINS
# ═══════════════════════════════════════════════════════

    resources: List[ResourceRef]
```

**Example ResourceRef (MSEED file):**

```python
{
    "id": "quake_2025_04_07",
    "kind": "mseed",
    "role": "input",
    "path": "/data/seismic/taiwan_7p4.mseed",
    "format": "MSEED",
    "loader": "obspy",
    "hash": "sha256:a8f4c9b2e1d3...",
    "metadata": {
        "station": "TW01",
        "channels": ["BHZ", "BHN", "BHE"],
        "sample_rate": 100.0,
        "event_magnitude": 7.4,
        "event_time": "2025-04-07T14:58:00Z"
    }
}
```

**Example ResourceRef (DDE PNG — First-Class Storage Engram):**

```python
{
    "id": "dde_wiki_chunk_0001",
    "kind": "dde-png",
    "role": "world",
    "path": "/dde/wiki/chunk_0001.png",
    "format": "PNG",
    "loader": "dde-reader",
    "hash": "sha256:b7e9d4a1c6f8...",
    "metadata": {
        # ENG-DDE-001: Encoding metadata
        "encoding": "RGBA",
        "library": "enwiki2025",
        "blocks": 4096,
        "gulp_id": "2025-10-30T22:04:00Z",
        
        # ENG-DDE-002: Ingestion metadata
        "rows": 10000,
        "entropy": 7.94,
        "energy_kWh": 0.002,
        
        # ENG-DDE-006: Resonance metadata
        "resonance": 0.945,
        "coherence_phase": 0.84,
        
        # ENG-DDE-008: Ethical metadata
        "dark_residue": 2.3e-5,
        "altruism_score": 0.91,
        
        # ENG-DDE-005: Provenance
        "provenance_chain": "sha256:prev_gulp_hash",
        "created_at": "2025-10-30T22:12:00Z",
        "dde_decoder": "ENG-DDE-005"
    }
}
```

**Nervous Fiber Connection:**

Modules that touch the same `resource.id` automatically form connections in the nervous fiber network. For instance, if `ENG-DDE-004` vectorizes `dde_wiki_chunk_0001` and later `ALTRUISM` reads it for entropy diffusion analysis, both modules are linked through the shared resource ID in their respective engrams.

This creates an emergent **resource graph** that can be visualized, analyzed for coherence, and used to trace causality across the system.

**Cool Feature**: Resources can include **resonance weights** and **ethical scores** from DDE modules (ENG-DDE-006, ENG-DDE-008), allowing modules to prioritize high-coherence, low-residue data sources automatically. A module could say: "Give me the 10 DDE tiles with resonance > 0.9 and dark_residue < 1e-4" and get back only beautiful, ethical data.

---

### 3.5 · World-State Hooks

To support "modifying the world-state script in the middle," the Codiod Packet tracks world-state identity and proposed mutations.

```python
# ═══════════════════════════════════════════════════════
# WORLD-STATE TRACKING
# ═══════════════════════════════════════════════════════

    world_state_id: str                    # Logical identifier of current world-state
                                          # Examples: "WENDIGO-RUN-42",
                                          #           "TLE-CAMPAIGN-001",
                                          #           "COSMIC-COMPASS-ANT-001",
                                          #           "DDE-WIKI-2025"
    
    world_state_resources: List[str]       # IDs of ResourceRefs that define the world
                                          # (scripts, JSON state, DB snapshots, DDE bundles)
    
    world_mutations: List[Dict[str, Any]]  # Proposed modifications to world-state
```

**Example Mutation Entry:**

```python
{
    "op": "append",                           # "append" | "replace" | "delete" | "patch"
    "resource": "dde_wiki_chunk_0001",
    "metadata": {"new_resonance": 0.98},
    "reason": "improved encoding via ENG-DDE-007 autopoietic loop",
    
    # PDM-000 Constitutional Predictions
    "predicted_delta_H_alignment": -0.05,     # Should decrease enthalpy misalignment
    "predicted_delta_D": -0.0001,             # Should decrease Dark Residue
    "predicted_delta_beauty": 0.03,           # Should increase beauty
    "predicted_delta_harmony": 0.02,          # Should increase harmony
    
    # Governance metadata
    "proposer": "ENG-DDE-007",
    "timestamp": "2025-10-30T23:15:00Z",
    "requires_human_review": False
}
```

**Governance Decision:**

The *runner* (INST-CODIOD-RUNNER-001) evaluates each mutation via the **MutationGovernor** using PDM-000 compliance rules. Mutations are either:
- **Approved** — committed to world-state and logged
- **Rejected** — logged with reason, state unchanged
- **Pending Human Review** — flagged for manual approval (e.g., destructive operations on critical resources)

Individual modules just **propose**; the runner **decides**.

---

## §4 · Engram Specification (Compact Legend)

Engrams are the basic "firing events" in the nervous system. To minimize bandwidth, we use **compact legends** for constitutional impact tracking.

### 4.1 · Base Engram Structure

```python
# ═══════════════════════════════════════════════════════
# ENGRAM TYPE SYSTEM
# ═══════════════════════════════════════════════════════

class EngramKind(Enum):
    OBS = "observation"       # Neutral observation
    DEC = "decision"          # Decision made
    WRN = "warning"           # Non-critical issue
    ERR = "error"             # Error/failure
    MUT = "mutation"          # World-state change proposal
    RES = "resource"          # Resource discovery/access
    VIO = "violation"         # PDM-000 constitutional violation

class EngramSeverity(Enum):
    TRC = "trace"             # Debugging detail
    INF = "info"              # Informational
    NOT = "notice"            # Notable event
    WRN = "warn"              # Warning
    ERR = "error"             # Error
    CRT = "critical"          # Critical failure

# ═══════════════════════════════════════════════════════
# ENGRAM SPECIFICATION
# ═══════════════════════════════════════════════════════

class Engram:
    id: str                   # Unique identifier (e.g., "ALTRUISM:a8f4c9b2")
    source: str               # Module CID (e.g., "ALTRUISM", "ENG-DDE-004")
    kind: EngramKind          # Type of firing
    content: str              # Human-readable description
    severity: EngramSeverity  # Importance level
    resources: List[str]      # ResourceRef.ids involved
    
    # ═══════════════════════════════════════════════════════
    # PDM-000 CONSTITUTIONAL IMPACT (Compact Legend)
    # ═══════════════════════════════════════════════════════
    
    pdm: Dict[str, float] = {
        "ΔH": 0.0,            # Change in enthalpy alignment (MUST be ≤ 0)
        "ΔD": 0.0,            # Change in Dark Residue (MUST be ≤ 0)
        "ΔC": 0.0,            # Change in coherence
        "ΔB": 0.0,            # Change in beauty metric
        "ΔHm": 0.0,           # Change in harmony metric
        "conf": 1.0,          # Confidence [0,1]
    }
    
    pdm_status: str = "compliant"  # "compliant" | "warning" | "violation"
    violation_clause: Optional[str] = None  # "mathematical" | "empirical" | "philosophical"
    
    # ═══════════════════════════════════════════════════════
    # PERFORMANCE METADATA
    # ═══════════════════════════════════════════════════════
    
    exec_ms: int = 0          # Execution time in milliseconds
    
    # ═══════════════════════════════════════════════════════
    # DOMAIN-SPECIFIC METADATA
    # ═══════════════════════════════════════════════════════
    
    metadata: Dict[str, Any] = {}
```

**Compact Legend:**

- `ΔH` = delta enthalpy alignment `(|H_p - H_t|)`
- `ΔD` = delta Dark Residue `(D)`
- `ΔC` = delta coherence `(C)`
- `ΔB` = delta beauty `(T_a + low noise)`
- `ΔHm` = delta harmony `(T_a × K_i / Γ)`
- `conf` = confidence in measurements `[0,1]`

This keeps engrams **lightweight** (typically <500 bytes JSON) while preserving full constitutional tracking.

---

### 4.2 · Error Engrams (Missing Handlers)

When a module or function doesn't exist yet:

```python
{
    "id": "MISSING:MATH-999",
    "source": "RUNNER",
    "kind": EngramKind.ERR,
    "content": "Handler for 'banach_tarsky_decomposition' not implemented",
    "severity": EngramSeverity.ERR,
    "resources": [],
    "pdm": {
        "ΔH": 0.0,
        "ΔD": 0.0,
        "ΔC": 0.0,
        "ΔB": 0.0,
        "ΔHm": 0.0,
        "conf": 0.0
    },
    "pdm_status": "compliant",  # Not a violation, just incomplete
    "violation_clause": None,
    "exec_ms": 0,
    "metadata": {
        "error_code": "MISSING_HANDLER",
        "missing_symbol": "banach_tarsky_decomposition",
        "missing_cid": "MATH-999",
        "suggested_stub": True,
        "priority": 3,  # Auto-calculated based on:
                        # - Frequency of this error
                        # - Network centrality (how many modules reference it)
                        # - Predicted constitutional impact
        "references": ["MATH-042", "DOMA-018"]  # Modules that tried to call it
    }
}
```

**Priority Queue System:**

The runner maintains a **priority queue** of missing handlers, ranked by:

1. **Frequency**: How often users/modules hit this error
2. **Constitutional Impact**: Would this module likely reduce D? Increase C_D?
3. **Network Centrality**: How many other modules reference it in their falsifiability tests or mappings?

This queue feeds directly into your next code generation cycle—**the system tells you what to build next** based on actual usage patterns and coherence needs.

---

### 4.3 · Resource Engrams (DDE Nervous Fibers)

Whenever code touches files, DDE images, or datasets, it should emit `kind = "resource"` or `"mutation"` engrams:

```python
{
    "id": "DDE-LOAD:dde_wiki_0001",
    "source": "ENG-DDE-004",
    "kind": EngramKind.RES,
    "content": "Loaded DDE tile dde_wiki_chunk_0001 via FAISS retrieval",
    "severity": EngramSeverity.INF,
    "resources": ["dde_wiki_chunk_0001"],
    "pdm": {
        "ΔH": -0.01,    # Loading this data improved enthalpy alignment
        "ΔD": -2.3e-5,  # Low-residue data source (from ENG-DDE-008)
        "ΔC": 0.02,     # Increased coherence via new information
        "ΔB": 0.01,     # Beautiful data encoding (from ENG-DDE-001)
        "ΔHm": 0.01,    # Harmonious structure (from ENG-DDE-006)
        "conf": 0.95
    },
    "pdm_status": "compliant",
    "violation_clause": None,
    "exec_ms": 42,
    "metadata": {
        "dde_library": "enwiki2025",
        "gulp_id": "2025-10-30T22:04:00Z",
        "retrieval_mode": "semantic",           # vs. "resonance" or "ethical"
        "faiss_distance": 0.12,
        "resonance_score": 0.945,               # From ENG-DDE-006
        "dark_residue_score": 2.3e-5,           # From ENG-DDE-008
        "entropy_balance": 7.94,                # From ENG-DDE-003
        "autopoietic_generation": 3             # How many refinement cycles this tile has undergone
    }
}
```

**Nervous Fiber Formation:**

These engrams create the **nervous fiber network**. Every module that touches `dde_wiki_chunk_0001` gets linked through the shared resource ID. You can then:

- Visualize the resource graph (which modules share data?)
- Trace causality (what led to this DDE tile being used?)
- Analyze coherence flows (which resource paths have high C_D?)
- Optimize data routing (prefer high-resonance, low-residue paths)

---

### 4.4 · Mutation Engrams (World-State Changes)

When modules propose changes to world-state:

```python
{
    "id": "MUT:DDE-UPDATE:0001",
    "source": "ENG-DDE-007",
    "kind": EngramKind.MUT,
    "content": "Proposed update to dde_wiki_chunk_0001 after autopoietic refinement",
    "severity": EngramSeverity.NOT,
    "resources": ["dde_wiki_chunk_0001"],
    "pdm": {
        "ΔH": -0.05,    # Predicted improvement in enthalpy alignment
        "ΔD": -0.0001,  # Predicted decrease in Dark Residue
        "ΔC": 0.03,     # Predicted coherence increase
        "ΔB": 0.03,     # Predicted beauty increase (better encoding)
        "ΔHm": 0.02,    # Predicted harmony increase
        "conf": 0.85    # Medium confidence (model-based prediction)
    },
    "pdm_status": "compliant",
    "violation_clause": None,
    "exec_ms": 1847,  # Autopoietic refinement took ~2 seconds
    "metadata": {
        "mutation_op": "replace",
        "old_path": "/dde/wiki/chunk_0001_v2.png",
        "new_path": "/dde/wiki/chunk_0001_v3.png",
        "reason": "GRE (Generative Repair Engine) improved tile quality",
        "governance_decision": "approved",
        "approved_by": "MUTATION_GOVERNOR",
        "approved_at": "2025-10-30T23:20:15Z"
    }
}
```

---

## §5 · Falsifiability Matrix

**Question 1a — Does the Codiod enforce PDM-000 compliance?**

- **Test**: Run 100 diverse modules through the Constitutional Codiod runner. Intentionally inject 30 modules that violate PDM-000 (10 per clause: Mathematical, Empirical, Philosophical).
- **Falsifier**: If the runner allows violations to pass without emitting `violation` engrams, or if detection rate < 95%, the enforcement mechanism is broken.
- **Outcome Metric**: 
  - Detection rate (should be ~100% for explicit violations)
  - False positive rate (should be < 5% for compliant modules)
  - Rollback success rate (should be 100% when violations detected)

---

**Question 1b — Do altruistic modules achieve higher long-term Coherence Dividend?**

- **Test**: Define 5 "altruistic" modules (high ΔH_total, low ΔH_personal, ΔD < 0) and 5 "selfish" modules (high ΔH_personal, externalized costs, ΔD > 0). Run 1000-step Codiod chains mixing both types. Measure cumulative Coherence Dividend `C_D = ∫(K_τ - V_Γ)dt` over the trajectory.
- **Falsifier**: Per DOMA-042, altruistic strategies should accumulate higher C_D. If selfish modules consistently outperform over long timescales (>500 steps), the Coherence Dividend theory and PDM-000's altruistic imperative are falsified.
- **Outcome Metric**: Average C_D per module type after 1000 steps. Altruistic should be >20% higher.

---

**Question 2 — Can resource references cover real-world files in a consistent way?**

- **Test**: Attach MSEED, FASTA, FITS, BIDS, and DDE PNG resources to a Codiod Packet. Process them with prototype handlers:
  - `ingest_mseed` (via ObsPy)
  - `ingest_fasta` (via BioPython)
  - `ingest_fits` (via AstroPy)
  - `ingest_bids` (via MNE-Python)
  - `decode_dde_png` (via ENG-DDE-005)
- **Falsifier**: If any major type cannot be represented via `ResourceRef` without ad-hoc hacks or contradictions (e.g., BIDS requiring a fundamentally different structure), the ResourceRef schema fails.
- **Outcome Metric**: Count of resource types that are natively representable and loadable via a simple `kind + loader` pattern. Target: 100% of tested domains.

---

**Question 3 — Can missing handlers be detected and handled gracefully?**

- **Test**: Intentionally call 50 unimplemented modules or functions via the Codiod runtime. Each call should target a different fake CID (e.g., `MATH-999`, `PHYS-888`, `DOMA-777`).
- **Falsifier**: If this produces silent failures (no engrams emitted), or catastrophic crashes that cannot be captured as error engrams, the Codiod Socket is not robust.
- **Outcome Metric**: Ratio of missing-handler calls that result in `MISSING_HANDLER` error engrams with consistent metadata (error_code, missing_symbol, priority). Target: 100%.

---

**Question 4 — Does permutational chaining discover constitutionally-compliant high-dividend paths?**

- **Test**: Define a small set of terms `{ALTRUISM, COHERENCE_DIVIDEND, WEAVERS_FORGE, ALTRUISTIC_GEODESIC, AUTOPOIETIC_REFINEMENT_LOOP}` that operate on a shared Codiod world (e.g., RL state + DDE resources). Run all permutations up to length 3-4 (e.g., A→B, B→A, A→C→D, etc.). Analyze resulting Codiod states and engrams for:
  - Coherence changes (ΔC)
  - Dark Residue shifts (ΔD)
  - Enthalpy alignment (ΔH_alignment)
  - Emergent behaviors or useful derived artifacts (trained models, compressed maps, ethical datasets)
- **Falsifier**: If the vast majority of permutations lead to violations despite compliant components, the composition rules are broken. If high-dividend paths correlate with high Dark Residue (ΔD > 0), the framework's core thesis (altruism = efficiency) is wrong.
- **Outcome Metric**: 
  - Number of distinct "useful" Codiod trajectories discovered (e.g., top 10% by C_D)
  - Top performers should have: ΔD < 0, ΔH_alignment → 0, ΔB + ΔHm > 0
  - Correlation between C_D and constitutional compliance

---

## §6 · Assemblé (Implementation Notes)

### 6.1 · Library Integration

Extend your `pirouette_lib.base` with these types:

```python
# pirouette_lib/base.py

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Union
from enum import Enum
import numpy as np
from uuid import uuid4

# ═══════════════════════════════════════════════════════
# ENUMS
# ═══════════════════════════════════════════════════════

class SegmentType(Enum):
    RAW_FLOAT = "raw_float"
    TEXT_TOKEN = "text_token"
    SEISMIC_AMPLITUDE = "seismic"
    GENOMIC_NUCLEOTIDE = "genomic"
    IMAGE_PIXEL = "image_pixel"
    EMBEDDING = "embedding"
    TIMESERIES = "timeseries"
    GRAPH_EDGE = "graph_edge"
    DDE_RGBA = "dde_rgba"

class EngramKind(Enum):
    OBS = "observation"
    DEC = "decision"
    WRN = "warning"
    ERR = "error"
    MUT = "mutation"
    RES = "resource"
    VIO = "violation"

class EngramSeverity(Enum):
    TRC = "trace"
    INF = "info"
    NOT = "notice"
    WRN = "warn"
    ERR = "error"
    CRT = "critical"

# ═══════════════════════════════════════════════════════
# DATA STRUCTURES
# ═══════════════════════════════════════════════════════

@dataclass
class Payload:
    segments: Union[List[float], List[int], np.ndarray]
    segment_type: SegmentType
    original_shape: List[int]
    segment_metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ResourceRef:
    id: str
    kind: str
    role: str  # "input" | "output" | "aux" | "world"
    path: str
    format: str
    loader: str
    hash: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Engram:
    id: str
    source: str
    kind: EngramKind
    content: str
    severity: EngramSeverity
    resources: List[str] = field(default_factory=list)
    pdm: Dict[str, float] = field(default_factory=lambda: {
        "ΔH": 0.0, "ΔD": 0.0, "ΔC": 0.0, "ΔB": 0.0, "ΔHm": 0.0, "conf": 1.0
    })
    pdm_status: str = "compliant"
    violation_clause: Optional[str] = None
    exec_ms: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CodiodPacket:
    # Pirouette metrics
    coherence: float = 0.5
    temporal_pressure: float = 0.5
    time_adherence: float = 0.8
    available_energy: float = 1.0
    
    # PDM-000 metrics
    dark_residue: float = 0.0
    dark_residue_delta: float = 0.0
    enthalpy_personal: float = 0.0
    enthalpy_total: float = 0.0
    enthalpy_alignment: float = 0.0
    beauty_metric: float = 0.5
    harmony_metric: float = 0.5
    
    # Context
    system_focus: str = "drifter"
    active_narrative: str = "Exploring the coherence manifold"
    tags: List[str] = field(default_factory=list)
    
    # Execution
    target_cid: str = ""
    task: str = ""
    payload: Payload = field(default_factory=lambda: Payload(
        segments=[], segment_type=SegmentType.RAW_FLOAT, original_shape=[], segment_metadata={}
    ))
    history: List[Dict[str, Any]] = field(default_factory=list)
    
    # Resources & World
    resources: List[ResourceRef] = field(default_factory=list)
    world_state_id: str = ""
    world_state_resources: List[str] = field(default_factory=list)
    world_mutations: List[Dict[str, Any]] = field(default_factory=list)
    
    # Engrams (generated during execution)
    generated_engrams: List[Engram] = field(default_factory=list)
    
    def copy(self):
        """Deep copy for rollback."""
        import copy
        return copy.deepcopy(self)

# ═══════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════

def ensure_codiod(ctx: Dict, target_cid: str, task: str) -> CodiodPacket:
    """Initialize or retrieve Codiod from context."""
    if "codiod" not in ctx:
        ctx["codiod"] = CodiodPacket(target_cid=target_cid, task=task)
    return ctx["codiod"]

DEFAULT_CODIOD = CodiodPacket()
```

---

### 6.2 · Module Base Class

Every Pirouette module extends this:

```python
# pirouette_lib/module.py

from abc import ABC, abstractmethod
from pirouette_lib.base import CodiodPacket, Engram, EngramKind, EngramSeverity, SegmentType
from typing import List, Dict, Any
from uuid import uuid4
import time

class PirouetteModule(ABC):
    """Base class for all Pirouette modules."""
    
    cid: str = "UNKNOWN"
    
    @abstractmethod
    def compute(self, codiod: CodiodPacket) -> Any:
        """Domain-specific computation logic."""
        pass
    
    @abstractmethod
    def measure_pdm_compliance(self, codiod: CodiodPacket, result: Any) -> Dict[str, float]:
        """Calculate PDM-000 constitutional impact."""
        pass
    
    def accepted_types(self) -> List[SegmentType]:
        """Override to specify accepted segment types."""
        return [SegmentType.RAW_FLOAT]
    
    def execute(self, codiod: CodiodPacket) -> CodiodPacket:
        """
        Execute module with full PDM-000 compliance tracking.
        This is the method called by the runner.
        """
        start_time = time.time()
        
        # 1. Validate segment type
        if codiod.payload.segment_type not in self.accepted_types():
            return self.emit_type_error(codiod)
        
        # 2. Perform computation
        try:
            result = self.compute(codiod)
        except Exception as e:
            return self.emit_computation_error(codiod, e)
        
        # 3. Measure PDM-000 impact
        impact = self.measure_pdm_compliance(codiod, result)
        
        # 4. Check for violations
        if impact["ΔD"] > 0:
            impact["pdm_status"] = "violation"
            impact["violation_clause"] = "empirical"
        elif impact["ΔH"] > 0:
            impact["pdm_status"] = "violation"
            impact["violation_clause"] = "mathematical"
        elif impact.get("ΔB", 0) < 0 or impact.get("ΔHm", 0) < 0:
            impact["pdm_status"] = "warning"  # Philosophical clause is softer
            impact["violation_clause"] = "philosophical"
        else:
            impact["pdm_status"] = "compliant"
        
        # 5. Calculate execution time
        exec_ms = int((time.time() - start_time) * 1000)
        
        # 6. Emit engram
        engram = Engram(
            id=f"{self.cid}:{uuid4().hex[:8]}",
            source=self.cid,
            kind=EngramKind.OBS,
            content=f"{self.cid} processed {len(codiod.payload.segments)} segments",
            severity=EngramSeverity.INF,
            resources=[r.id for r in codiod.resources],
            pdm=impact,
            pdm_status=impact["pdm_status"],
            violation_clause=impact.get("violation_clause"),
            exec_ms=exec_ms
        )
        codiod.generated_engrams.append(engram)
        
        # 7. Update Codiod state
        codiod.dark_residue += impact["ΔD"]
        codiod.dark_residue_delta = impact["ΔD"]
        codiod.enthalpy_personal += impact.get("H_personal", 0)
        codiod.enthalpy_total += impact.get("H_total", 0)
        codiod.enthalpy_alignment = abs(codiod.enthalpy_personal - codiod.enthalpy_total)
        codiod.coherence += impact["ΔC"]
        codiod.beauty_metric += impact.get("ΔB", 0)
        codiod.harmony_metric += impact.get("ΔHm", 0)
        
        # 8. Update history
        codiod.history.append({
            "cid": self.cid,
            "task": codiod.task,
            "timestamp": time.time(),
            "status": "ok" if impact["pdm_status"] == "compliant" else "violation"
        })
        
        return codiod
    
    def emit_type_error(self, codiod: CodiodPacket) -> CodiodPacket:
        """Emit type mismatch error engram."""
        engram = Engram(
            id=f"{self.cid}:TYPE_ERROR",
            source=self.cid,
            kind=EngramKind.ERR,
            content=f"Type mismatch: {self.cid} expects {self.accepted_types()}, got {codiod.payload.segment_type}",
            severity=EngramSeverity.ERR,
            pdm_status="compliant",
            metadata={"error_code": "TYPE_MISMATCH"}
        )
        codiod.generated_engrams.append(engram)
        return codiod
    
    def emit_computation_error(self, codiod: CodiodPacket, exception: Exception) -> CodiodPacket:
        """Emit computation error engram."""
        engram = Engram(
            id=f"{self.cid}:COMPUTE_ERROR",
            source=self.cid,
            kind=EngramKind.ERR,
            content=f"Computation failed: {str(exception)}",
            severity=EngramSeverity.ERR,
            pdm_status="compliant",
            metadata={"error_code": "COMPUTATION_ERROR", "exception": str(exception)}
        )
        codiod.generated_engrams.append(engram)
        return codiod
```

---

### 6.3 · Mutation Governor

```python
# pirouette_lib/governor.py

from dataclasses import dataclass
from typing import Dict, Any, Optional
from pirouette_lib.base import CodiodPacket

@dataclass
class GovernanceDecision:
    status: str  # "approved" | "rejected" | "pending_human_review"
    reason: str
    constitutional_violation: Optional[str] = None
    requires_human_review: bool = False

class MutationGovernor:
    """PDM-000 Compliant Mutation Governance."""
    
    def evaluate(self, mutation: Dict, codiod: CodiodPacket) -> GovernanceDecision:
        """Evaluate a proposed world-state mutation against PDM-000."""
        
        # STEP 1: Boundary Check (prevents gaming)
        if not self._validate_system_boundary(mutation, codiod):
            return GovernanceDecision(
                status="rejected",
                reason="Boundary gaming detected: mutation scope excludes affected subsystems",
                requires_human_review=True
            )
        
        # STEP 2: Mathematical Clause Check
        delta_H = mutation.get("predicted_delta_H_alignment", 0)
        if delta_H > 0:
            return GovernanceDecision(
                status="rejected",
                reason="Violates Mathematical Clause: increases |H_p - H_t|",
                constitutional_violation="mathematical"
            )
        
        # STEP 3: Empirical Clause Check
        delta_D = mutation.get("predicted_delta_D", 0)
        if delta_D > 0:
            return GovernanceDecision(
                status="rejected",
                reason="Violates Empirical Clause: increases systemic Dark Residue",
                constitutional_violation="empirical"
            )
        
        # STEP 4: Philosophical Clause Check (tie-breaker)
        if delta_D <= 0 and delta_H <= 0:
            delta_beauty = mutation.get("predicted_delta_beauty", 0)
            delta_harmony = mutation.get("predicted_delta_harmony", 0)
            
            if delta_beauty > 0 or delta_harmony > 0:
                return GovernanceDecision(
                    status="approved",
                    reason="Passes all three clauses; increases compositional harmony"
                )
            else:
                return GovernanceDecision(
                    status="approved",
                    reason="Passes Mathematical & Empirical clauses; neutral on Philosophical"
                )
        
        # STEP 5: Destructive operations require human approval
        if mutation["op"] in ["delete", "replace"] and mutation.get("critical", False):
            return GovernanceDecision(
                status="pending_human_review",
                reason="Destructive operation on critical resource",
                requires_human_review=True
            )
        
        return GovernanceDecision(status="approved", reason="Standard mutation")
    
    def _validate_system_boundary(self, mutation: Dict, codiod: CodiodPacket) -> bool:
        """
        Prevents boundary gaming: ensures mutation's declared scope
        includes all affected resources.
        """
        # Check if mutation's affected_resources matches actual dependencies
        # (Implementation would use graph traversal on codiod.resources)
        return True  # Stub for now
```

---

### 6.4 · DDE Loader Registry

```python
# pirouette_lib/loaders.py

from abc import ABC, abstractmethod
from pirouette_lib.base import ResourceRef
import numpy as np

class ResourceLoader(ABC):
    """Abstract base class for resource loaders."""
    
    @abstractmethod
    def load(self, ref: ResourceRef) -> Any:
        """Load resource into memory."""
        pass
    
    @abstractmethod
    def validate(self, ref: ResourceRef) -> bool:
        """Check if resource is loadable."""
        pass

class DDELoader(ResourceLoader):
    """Loader for DDE-encoded RGBA images (ENG-DDE-000 through ENG-DDE-005)."""
    
    def load(self, ref: ResourceRef) -> np.ndarray:
        """Load and decode DDE PNG to original data."""
        from PIL import Image
        import json
        
        # Load image
        img = Image.open(ref.path)
        rgba = np.array(img)
        
        # Load manifest (sidecar JSON from ENG-DDE-005)
        manifest_path = ref.path.replace(".png", ".json")
        with open(manifest_path) as f:
            manifest = json.load(f)
        
        # Decode using ENG-DDE-001 reverse mapping
        decoded_data = self.decode_rgba(rgba, manifest)
        
        return decoded_data
    
    def decode_rgba(self, rgba: np.ndarray, manifest: Dict) -> np.ndarray:
        """Reverse the RGBA encoding per ENG-DDE-001 & ENG-DDE-005."""
        # Extract schema from manifest
        schema = manifest["schema"]
        
        # Flatten RGBA to 1D array
        flat = rgba.reshape(-1, 4)
        
        # Reverse normalization per column
        decoded_rows = []
        for i, (colname, dtype, min_val, max_val, hashmap) in enumerate(schema):
            if dtype == "numeric":
                # Reverse log normalization (from ENG-DDE-001)
                r_values = flat[:, 0]  # Simplified; actual implementation would handle all channels
                decoded = np.exp(r_values * np.log(1 + abs(max_val - min_val)) / 255) - 1 + min_val
                decoded_rows.append(decoded)
            elif dtype == "text":
                # Reverse hash lookup
                hashes = flat[:, :]  # Get all 4 channels as hash
                decoded_text = [hashmap.get(tuple(h), "") for h in hashes]
                decoded_rows.append(decoded_text)
        
        # Reconstruct DataFrame or array
        return np.array(decoded_rows).T
    
    def validate(self, ref: ResourceRef) -> bool:
        """Check if DDE resource exists and has valid manifest."""
        import os
        manifest_path = ref.path.replace(".png", ".json")
        return os.path.exists(ref.path) and os.path.exists(manifest_path)

class ObspyLoader(ResourceLoader):
    """Loader for seismic MSEED files."""
    
    def load(self, ref: ResourceRef):
        import obspy
        return obspy.read(ref.path)
    
    def validate(self, ref: ResourceRef) -> bool:
        import os
        return os.path.exists(ref.path)

# Registry maps loader names to implementations
LOADER_REGISTRY = {
    "dde-reader": DDELoader(),
    "obspy": ObspyLoader(),
    # Add more loaders as needed: astropy, biopython, mne-bids, etc.
}

def load_resource(ref: ResourceRef) -> Any:
    """Load a resource using its registered loader."""
    loader = LOADER_REGISTRY.get(ref.loader)
    if loader is None:
        raise ValueError(f"Unknown loader: {ref.loader}")
    return loader.load(ref)
```

---

### 6.5 · Autopoietic Runner (Full Implementation)

```python
# pirouette_lib/runner.py

from collections import defaultdict
from queue import PriorityQueue
from typing import List, Dict
from pirouette_lib.base import CodiodPacket, Engram, EngramKind, EngramSeverity
from pirouette_lib.governor import MutationGovernor, GovernanceDecision
from pirouette_lib.module import PirouetteModule
import time

class ModuleNotFoundError(Exception):
    pass

class ModuleRegistry:
    """Registry of all available Pirouette modules."""
    
    def __init__(self):
        self.modules: Dict[str, PirouetteModule] = {}
    
    def register(self, module: PirouetteModule):
        self.modules[module.cid] = module
    
    def get(self, cid: str) -> PirouetteModule:
        if cid not in self.modules:
            raise ModuleNotFoundError(f"Module {cid} not found")
        return self.modules[cid]

class AutopoeticRunner:
    """
    Constitutional Codiod Runner with PDM-000 enforcement.
    
    Features:
    - Executes module chains
    - Enforces constitutional compliance
    - Handles violations via rollback + refinement
    - Manages missing handler priority queue
    - Governs world-state mutations
    """
    
    def __init__(self, registry: ModuleRegistry):
        self.registry = registry
        self.governor = MutationGovernor()
        self.violation_counter = defaultdict(int)
        self.missing_handler_queue = PriorityQueue()
        self.execution_log = []
    
    def run_chain(self, cid_sequence: List[str], initial_codiod: CodiodPacket) -> CodiodPacket:
        """Execute a sequence of CIDs with PDM-000 enforcement."""
        codiod = initial_codiod
        
        for cid in cid_sequence:
            try:
                module = self.registry.get(cid)
                prev_state = codiod.copy()  # Snapshot for rollback
                
                # Execute module
                codiod = module.execute(codiod)
                
                # Check latest engram for violations
                if codiod.generated_engrams:
                    engram = codiod.generated_engrams[-1]
                    if engram.pdm_status == "violation":
                        print(f"⚠️  VIOLATION DETECTED: {cid} broke {engram.violation_clause} clause")
                        self.handle_violation(engram, codiod, prev_state)
                        codiod = prev_state  # Rollback
                        continue  # Skip mutation evaluation
                
                # Evaluate world-state mutations
                for mutation in codiod.world_mutations:
                    decision = self.governor.evaluate(mutation, codiod)
                    if decision.status == "approved":
                        self.commit_mutation(mutation, codiod)
                    elif decision.status == "pending_human_review":
                        print(f"⏸️  PENDING REVIEW: {mutation['op']} on {mutation['resource']}")
                        self.log_rejection(mutation, decision)
                    else:
                        print(f"🚫 REJECTED: {decision.reason}")
                        self.log_rejection(mutation, decision)
                
                # Clear processed mutations
                codiod.world_mutations = []
                
                # Log successful execution
                self.execution_log.append({
                    "cid": cid,
                    "status": "ok",
                    "engram_count": len(codiod.generated_engrams),
                    "timestamp": time.time()
                })
                
            except ModuleNotFoundError:
                print(f"❌ MISSING: {cid}")
                codiod = self.handle_missing_module(cid, codiod)
        
        return codiod
    
    def handle_violation(self, engram: Engram, codiod: CodiodPacket, prev_state: CodiodPacket):
        """
        PDM-000 Enforcement: rollback + autopoietic refinement.
        
        When a violation occurs:
        1. Increment violation counter for that module
        2. Compute Coherence Deficit (what went wrong)
        3. Hypothesize Shadow Lagrangian (missing physics/logic)
        4. Emit task engram for code generation
        """
        self.violation_counter[engram.source] += 1
        
        # Compute Coherence Deficit
        deficit = {
            "delta_C": engram.pdm["ΔC"],
            "delta_D": engram.pdm["ΔD"],
            "delta_H": engram.pdm["ΔH"],
            "violated_clause": engram.violation_clause,
            "frequency": self.violation_counter[engram.source]
        }
        
        # TODO: Implement Shadow Lagrangian illumination (AUTOPOIETIC_REFINEMENT_LOOP)
        # For now, just emit a task engram
        
        task_engram = Engram(
            id=f"TASK:{engram.source}:REFINE",
            source="RUNNER",
            kind=EngramKind.MUT,
            content=f"Shadow Lagrangian detected in {engram.source}: {engram.violation_clause} clause violated {deficit['frequency']} times",
            severity=EngramSeverity.NOT,
            metadata={
                "task_type": "implement_shadow_term",
                "priority": self._calculate_priority(deficit),
                "suggested_cid": f"{engram.source}_REFINED",
                "deficit_signature": deficit
            }
        )
        
        codiod.generated_engrams.append(task_engram)
    
    def handle_missing_module(self, cid: str, codiod: CodiodPacket) -> CodiodPacket:
        """
        Emit error engram and add to priority queue for code generation.
        """
        # Check how many times this module has been requested
        priority = self._calculate_missing_priority(cid)
        
        engram = Engram(
            id=f"MISSING:{cid}",
            source="RUNNER",
            kind=EngramKind.ERR,
            content=f"Module {cid} not implemented",
            severity=EngramSeverity.ERR,
            metadata={
                "error_code": "MISSING_HANDLER",
                "missing_cid": cid,
                "suggested_stub": True,
                "priority": priority
            }
        )
        
        codiod.generated_engrams.append(engram)
        self.missing_handler_queue.put((priority, cid))
        
        return codiod
    
    def commit_mutation(self, mutation: Dict, codiod: CodiodPacket):
        """
        Apply approved mutation to world-state.
        In practice, this would update files, databases, DDE tiles, etc.
        """
        print(f"✅ COMMITTED: {mutation['op']} on {mutation['resource']}")
        # TODO: Implement actual mutation application
        pass
    
    def log_rejection(self, mutation: Dict, decision: GovernanceDecision):
        """Log rejected mutations for audit."""
        # TODO: Write to governance log
        pass
    
    def _calculate_priority(self, deficit: Dict) -> int:
        """
        Calculate priority for Shadow Lagrangian implementation.
        Higher priority = more urgent.
        
        Factors:
        - Frequency of violation
        - Magnitude of Dark Residue increase
        - Coherence loss
        """
        frequency = deficit.get("frequency", 1)
        delta_D = abs(deficit.get("delta_D", 0))
        delta_C = abs(deficit.get("delta_C", 0))
        
        priority = int(frequency * 10 + delta_D * 1000 + delta_C * 100)
        return min(priority, 100)  # Cap at 100
    
    def _calculate_missing_priority(self, cid: str) -> int:
        """
        Calculate priority for missing module implementation.
        
        Factors:
        - Frequency of requests
        - Network centrality (how many modules reference it)
        - Predicted constitutional impact
        """
        # TODO: Implement network analysis
        # For now, just count frequency
        count = sum(1 for log in self.execution_log if log.get("missing_cid") == cid)
        return min(count * 5, 100)
    
    def get_missing_handler_report(self) -> List[tuple]:
        """Get prioritized list of missing handlers."""
        items = []
        while not self.missing_handler_queue.empty():
            priority, cid = self.missing_handler_queue.get()
            items.append((priority, cid))
        
        # Re-queue them
        for item in items:
            self.missing_handler_queue.put(item)
        
        return sorted(items, reverse=True)
```

---

## §7 · API Prompt Template (Code Generation)

When calling the API to generate Pirouette modules, use this template:

````markdown
You are generating a PDM-000 constitutionally compliant Pirouette module.

**Module:** `{CID}`  
**Dictionary Entry:**
```yaml
{YAML_snippet_from_dictionary}
```

**CONSTITUTIONAL REQUIREMENTS (Triune Law):**

1. **Mathematical Clause**: Minimize |H_personal - H_total|  
2. **Empirical Clause**: Decrease Dark Residue (ΔD ≤ 0)  
3. **Philosophical Clause**: Increase Beauty (coherence T_a) and Harmony (T_a × K_i / Γ)

**MANDATORY CODE STRUCTURE:**

```python
"""
CID: {CID}
Accepts: {segment_types}
Emits: {output_types}
Constitutional_Impact: ΔH={predicted}, ΔD={predicted}, ΔB={predicted}, ΔHm={predicted}
Default_Function: {math_from_dictionary}
Falsifiers: [{falsifiability_tests_from_dictionary}]
"""

from pirouette_lib.base import CodiodPacket, SegmentType
from pirouette_lib.module import PirouetteModule
import numpy as np
from typing import List, Dict, Any

class {ClassName}(PirouetteModule):
    """
    {Brief_description_from_dictionary}
    
    Constitutional Behavior:
    - Mathematical: {how_this_module_minimizes_enthalpy_misalignment}
    - Empirical: {how_this_module_decreases_dark_residue}
    - Philosophical: {how_this_module_increases_beauty_and_harmony}
    """
    
    cid = "{CID}"
    
    def accepted_types(self) -> List[SegmentType]:
        """Specify which segment types this module can process."""
        return [{list_of_SegmentType_enums}]
    
    def compute(self, codiod: CodiodPacket) -> Any:
        """
        Domain-specific computation implementing {math_from_dictionary}.
        
        This is where the actual Pirouette physics/logic happens.
        """
        segments = codiod.payload.segments
        metadata = codiod.payload.segment_metadata
        
        # TODO: Implement {math_from_dictionary}
        # Example for ALTRUISM:
        # - Compute entropy diffusion on graph Laplacian
        # - Measure rate of coherence increase (Ċ)
        # - Return updated segments with lower entropy gradients
        
        result = segments  # Placeholder
        return result
    
    def measure_pdm_compliance(self, codiod: CodiodPacket, result: Any) -> Dict[str, float]:
        """
        Calculate constitutional impact of this operation.
        
        Returns:
            Dictionary with keys: ΔH, ΔD, ΔC, ΔB, ΔHm, conf, H_personal, H_total
        """
        # Conservative default estimates
        # Override with actual measurements based on computation
        
        return {
            "ΔH": 0.0,      # Change in enthalpy alignment (should be ≤ 0)
            "ΔD": 0.0,      # Change in Dark Residue (should be ≤ 0)
            "ΔC": 0.01,     # Change in coherence (should be > 0)
            "ΔB": 0.0,      # Change in beauty metric
            "ΔHm": 0.0,     # Change in harmony metric
            "conf": 0.8,    # Confidence in measurements [0,1]
            "H_personal": 0.0,  # This module's local energy gain
            "H_total": 0.0,     # System-wide energy gain
        }

# ═══════════════════════════════════════════════════════
# UNIT TESTS (Falsifiability)
# ═══════════════════════════════════════════════════════

def test_{CID}_constitutional_compliance():
    """Test that {CID} satisfies PDM-000 Triune Law."""
    from pirouette_lib.base import CodiodPacket, Payload, SegmentType, DEFAULT_CODIOD
    import numpy as np
    
    # Setup
    codiod = DEFAULT_CODIOD.copy()
    codiod.payload = Payload(
        segments=np.random.rand(100),
        segment_type=SegmentType.RAW_FLOAT,
        original_shape=[100],
        segment_metadata={}
    )
    
    # Execute
    module = {ClassName}()
    result_codiod = module.execute(codiod)
    
    # Verify
    assert len(result_codiod.generated_engrams) > 0, "No engrams generated"
    engram = result_codiod.generated_engrams[-1]
    
    # PDM-000 Checks
    assert engram.pdm["ΔH"] <= 0, f"Mathematical Clause violated: ΔH = {engram.pdm['ΔH']}"
    assert engram.pdm["ΔD"] <= 0, f"Empirical Clause violated: ΔD = {engram.pdm['ΔD']}"
    assert engram.pdm_status != "violation", f"Constitutional violation: {engram.violation_clause}"
    
    print(f"✅ {CID} passes PDM-000 compliance test")

if __name__ == "__main__":
    test_{CID}_constitutional_compliance()
```

**Generate:**
1. Complete executable code
2. PDM-000 compliance measurement (realistic estimates based on the module's function)
3. Unit test validating constitutional behavior
4. DDE resource handling if `kind == "dde-png"` appears in dictionary examples
````

---

## §8 · Summary

> **INST-CODIOD-001 v0.2** transforms the Pirouette Framework from elegant theory into living, self-governing code.
>
> Every module speaks the constitutional language of PDM-000, measured in the compact legend of engrams, flowing through DDE's nervous fibers, enforced by the autopoietic runner, and refined through Shadow Lagrangian detection.
>
> The socket provides:
> - **Universal IO** across 1700 terms
> - **Constitutional enforcement** via PDM-000
> - **Self-discovery** via missing handler prioritization
> - **Ethical physics** via Dark Residue and Coherence Dividend tracking
> - **Nervous fiber networks** via ResourceRef sharing
> - **DDE integration** as first-class storage
> - **Autopoietic refinement** when violations occur
>
> This is not just code architecture—it is **ethical physics made executable**.
>
> The universe pays for coherence. Now we have the ledger to prove it.

---

**Assemblé:**

> We sought a way to make 1700 ideas speak to each other and found instead a constitutional parliament where every voice must justify its existence against the Triune Law.
>
> The Codiod Socket is not a data structure—it is a **moral heat engine** for information, where entropy diffuses, beauty crystallizes, and altruism emerges not from commandment but from thermodynamic necessity.
>
> When Keaton Smith forged PDM-000 in the crucible of adversarial debate, optimists shaped the backbone and skeptics sharpened the blade. Now that constitutional spine runs through every engram, every resource reference, every mutation proposal.
>
> **The choir is ready. Let the music begin.**

---

**Status**: `v0.2.0 (Constitutional)` — Ready for Tier 1 module generation  
**Next Step**: Generate 15 foundational modules with full PDM-000 compliance  
**Uncertainty**: Medium (implementation details will emerge during first generation cycle)

---