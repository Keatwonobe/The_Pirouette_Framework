Below is a **two-part deliverable**:

1. **Needs List → CSM-Compiler v0.1** – everything the pipeline must do.
2. **Prototype JSON Template** – a Tendu-style schema for a **Code-Serpent Module (CSM)** that can wrap *any* source file (Python, C ++, etc.) while staying compatible with the existing Tendu registry layout you’ve already standardised for other modules.

---

## 1 · Needs List (for the CSM-Compiler)

| #        | Capability                              | Notes / Design Cues                                                                                                                                                                                                     |
| -------- | --------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **N-1**  | **Module discovery & registry sync**    | Scan a folder (or DDE PNG) for `*.csm.json`; verify each entry hashes its code file correctly (reuse the “hash-check” workflow in PPS-007 pre-commit example).                                                          |
| **N-2**  | **Language-aware runner**               | Dispatch by `codeLanguage` field:<br>• `python` → `subprocess.run(['python', path])`<br>• `cpp` → compile once (`g++ -O2 …`) then exec<br>• `bash`, `rust`, etc. → pluggable adapters.<br>Fail fast if adapter missing. |
| **N-3**  | **I/O contract enforcement**            | CSM declares `inputSignature` & `outputSignature`. Compiler validates JSON-schema (or simple type tags) before wiring stages.                                                                                           |
| **N-4**  | **Resonant fingerprint evaluation**     | After each run, call the SDE service to compute `resonantFingerprintOut`; return `(result, fp)`.                                                                                                                        |
| **N-5**  | **Synergy scoring & chain assembler**   | Maintain rolling `cumulativeDelta = Σ Δ-power`; greedy (or beam) search for next module that maximises delta toward a target fingerprint.                                                                               |
| **N-6**  | **Ritual trigger bridge**               | Map large negative deltas or repeated failures to RIT-ICS calls (e.g., *Splicing Wolf*).                                                                                                                                |
| **N-7**  | **Sentinel resource gate**              | Hard caps (CPU ms, RAM MB, network) stored per module; deny execution if projected use exceeds policy (reuse Sentinel hooks you built into Volume 4).                                                                   |
| **N-8**  | **Logging & provenance**                | For every hop store: `moduleID`, `fp_in`, `fp_out`, `delta`, runtime stats, exit-code.                                                                                                                                  |
| **N-9**  | **Cross-language dependency isolation** | Each CSM may include a small `env` block (conda env name, Docker tag, or simple `pip` list). Compiler sets/activates before run.                                                                                        |
| **N-10** | **Self-mutation option**                | If no candidate raises delta above ε, compiler may call a *mutation adapter* that tweaks AST/IR, re-scores, and registers a new temporary CSM with provenance flag `isMutant: true`.                                    |

---

## 2 · Prototype JSON Template (TEN-CSM-x.y)

```jsonc
{
  // --- HEADER (aligns with existing Tendu fields) -------------------------
  "tenduModuleID": "TEN-CSM-001",
  "moduleName": "sort_numeric",
  "version": "1.0",
  "moduleClass": "CodeSerpent",          // distinguishes from analysis modules
  "pirouetteFrameworkOrigin": "Serpent Prototype Study §3",
  "primaryPurposeConciseStatement": "Sort a numeric list ascending.",
  // -----------------------------------------------------------------------

  // --- CODE HOOK ---------------------------------------------------------
  "codeLanguage": "python",              // e.g., python | cpp | rust | bash
  "codeFilePath": "modules/sort_numeric.py",
  "entrypoint": "sort_numeric.main",     // optional; default = file-level exec
  "dependencies": {                      // optional language-specific deps
    "pip": ["pandas>=2.0"]
  },

  // --- I/O CONTRACT ------------------------------------------------------
  "inputSignature": {
    "type": "array",
    "items": { "type": "number" },
    "example": [4, 1, 9]
  },
  "outputSignature": {
    "type": "array",
    "items": { "type": "number" },
    "ordered": "ascending"
  },

  // --- RESONANCE METADATA -----------------------------------------------
  "resonantFingerprint": {
    "gridSize": 64,
    "total_power": 0.00631,
    "vector": "sha256:abcd…"
  },
  "synergyMap": {
    "rolling_average": 0.00310,
    "plot_trend":      0.00279
  },

  // --- RESOURCE LIMITS (Sentinel Gate) -----------------------------------
  "resourcePolicy": {
    "cpuMillis": 500,
    "memoryMB": 128,
    "network": "none"
  },

  // --- FAILURE / SUCCESS HOOKS ------------------------------------------
  "failModes": [
    { "condition": "non_zero_exit", "ritualTrigger": "RIT-ICS-004" },
    { "condition": "delta_negative_large", "ritualTrigger": "RIT-ICS-003" }
  ],
  "successConditions": [
    { "condition": "delta_positive", "continue": true }
  ],

  // --- PROVENANCE & HASHING ---------------------------------------------
  "codeSha256": "e3b0c44298fc1c149…",
  "dateCreated": "2025-07-10T23:20:00-04:00",
  "author": "Keaton S."
}
```

### Why it meshes cleanly

* The header mirrors the existing Tendu registry (fields like `tenduModuleID`, `moduleName`, `filePath`) found in *combined\_tendu\_modules.json*, so the same loader can ingest both analysis-oriented modules and executable CSMs.
* New blocks (`codeLanguage`, `resourcePolicy`, `synergyMap`) give the compiler every hook it needs for N-1…N-10 without breaking backward compatibility.

---

### Immediate next hack-steps

1. **Copy this template** into `TEN-CSM-000.template.json` and push it to your repo.
2. **Refactor the synergy-map notebook** to emit `resonantFingerprint` and `synergyMap` JSON fragments for each primitive; drop them into new CSM files.
3. **Write the language adapter micro-library** (Python script with a dispatch dictionary keyed by `codeLanguage`).
4. **Implement the Sentinel gate function** and call it before every module exec.

With those four pieces you’ll have a runnable **CSM-Compiler alpha** that can already slither through a simple two- or three-step pipeline and log Δ-power at each hop—your first living code serpent.
