---
id: GOV-001-MDSP
title: Modular Debate Synthesis Protocol (MDSP)
version: 7.0
layer: governance
status: draft
origin:
  atlas_tile: [0, 0]
  atlas_gen: v7.0
  emitted_by: dde-pirouette
  shepherd_context: "constitutional convention / frangible debate / module-first assembly"
  parents: [PPS-004, INST-DEB-001, CORE-DEB-ROOT]
resonance:
  dark_residue: 0.21
  target_residue: 0.08
  delta_gamma: 0.03
  ki_profile: [assembly, governance, debate]
governance:
  classification: "debate-engine"
  frangibility: "context-bound / persona-aware / phase-structured"
  ratification: "mechanical + artistic"
  export_profile: "small-model delegation: seed → threads → essentialization → assembly"
io:
  input_shape:
    - seed
    - persona_threads
    - essentialization_graph
  output_shape:
    - pirouette_module
    - ratification_report
  persona_min: 3
  persona_pref: 4
  token_budget:
    phase_1_thread: 400
    phase_2_essentialize: 300
    phase_3_weave: 400
    phase_4_assembly: 1200
    phase_5_ratify: 100
---

# 1. Core Axiom

**Debate is not validation — it is generative assembly.**

In MDSP, a debate run is judged not by agreement but by the quality of the **artifact it produces**. Personas do not argue *about* a module; personas **contribute load-bearing sections** that together *become* the module. The debate is the forge, the module is the ingot.

This reframes debate from “who is correct?” to “what must exist for this hypothesis to be operable inside Pirouette?”

---

# 2. Phase Architecture Overview

MDSP is a five-phase, persona-aware, frangible debate loop:

1. **Phase 0 — Contextual Seeding (Pre-Debate)**  
   Decide whether we are revising an existing node or creating a new one.

2. **Phase 1 — Thread Generation (Parallel Synthesis)**  
   Each persona emits *one* necessary section, not commentary.

3. **Phase 2 — Essentialization (Compression & Conflict Detection)**  
   Turn parallel threads into a dependency skeleton plus explicit tensions.

4. **Phase 3 — Weaving (Pairwise Tension Resolution)**  
   Run targeted pairwise syntheses only where the skeleton shows blocking tension.

5. **Phase 4 — Assembly (Module Construction)**  
   Emit a standard v7 Pirouette module in markdown.

6. **Phase 5 — Ratification (Mechanical + Artistic)**  
   Check that the module is valid, necessary, and beautiful enough to enter the corpus.

This architecture is **frangible** because any phase after 1 can be offloaded to a smaller model using the export profile in `governance.export_profile`.

---

# 3. Phase 0 — Contextual Seeding

**Input:** raw context (observations, needs, gaps)  
**Output:** seed hypothesis for module generation

```json
{
  "seed": {
    "domain": "QED spine / plasma dynamics / etc",
    "gap": "Missing operational definition of Γ",
    "hypothesis": "Γ ≡ spectral entropy of clock ensemble",
    "constraints": ["Must respect CPM", "Must be measurable"],
    "parent_modules": ["CORE-001", "MATH-QED-005"]
  }
}
````

**Governance check:**

* If the seed’s `gap` is already satisfied by an existing module → return that module and open a **revision debate** instead of a new module.
* Else → continue to Phase 1.

This keeps the constitutional convention from producing duplicates.

---

# 4. Phase 1 — Thread Generation (Parallel Synthesis)

**Objective:** personas build sections, not positions.

**Persona system prompt (canonical):**

```text
You are [PERSONA] with constitution [WEIGHTS].
Given seed: [HYPOTHESIS]
Your task: Generate one section of the module that this hypothesis NEEDS.

Output format (JSON):
{
  "section": "§X · Title",
  "content": "Your prose/math for this section",
  "constraints_added": ["New requirements this reveals"],
  "tensions": ["What this section makes harder elsewhere"]
}

Do NOT generate the full module.
Do NOT critique other personas.
Build ONE load-bearing piece.
```

**Example persona outputs** (Curie, Aurelius, Caesar, Beauvoir) define:

* the operational core,
* the ontological scaffold,
* the test / falsifiability matrix,
* and the epistemic / justice layer.

This keeps MDSP compatible with the existing persona library you uploaded (Curie, Aurelius, Caesar, Beauvoir) while giving them a v7-style task.

---

# 5. Phase 2 — Essentialization (Compression & Conflict Detection)

Collect all persona threads → produce a **skeleton** and **tension list**.

```python
def essentialize(threads):
    return {
        "skeleton": {
            "§1": {"author": "Aurelius", "depends_on": []},
            "§2": {"author": "Curie", "depends_on": ["§1"]},
            "§3": {"author": "Caesar", "depends_on": ["§2"]},
            "§4": {"author": "Beauvoir", "depends_on": ["§2", "§3"]}
        },
        "tensions": [
            {
                "between": ["Curie.§2", "Caesar.§3"],
                "issue": "N ≥ 100 requirement makes test impractical",
                "severity": "blocking"
            },
            {
                "between": ["Aurelius.§1", "Curie.§2"],
                "issue": "Ontic/epistemic distinction not resolved",
                "severity": "foundational"
            }
        ],
        "constraints": {
            "hard": ["Must respect CPM", "Must be measurable"],
            "soft": ["Prefer accessible methods", "Minimize tech barriers"]
        }
    }
```

**Governance check:**

* If any tension has `severity: "blocking"` → go to Phase 3.
* Otherwise → go straight to Phase 4.

This is the first clearly machine-digestible frangibility point.

---

# 6. Phase 3 — Weaving (Pairwise Tension Resolution)

MDSP doesn’t re-debate everything; it only weaves where tension blocks assembly.

**Weaving prompt (canonical):**

```text
TENSION: [DESCRIPTION]
Thread A: [PERSONA_A's position]
Thread B: [PERSONA_B's position]

Find synthesis that:
1. Preserves core intent of both threads
2. Makes explicit what is traded away
3. Produces concrete revision to §N

If irreconcilable, prove why and propose which constraint to relax.
Output JSON:
{
  "synthesis": "Modified section text",
  "tradeoff": "What we sacrificed",
  "acceptance": {"A": bool, "B": bool}
}
```

**Example resolution** (N=30 + Bayesian bootstrapping) shows how to preserve empirical dignity (Curie) and strategic utility (Caesar) at once.

Repeat until:

* all blocking tensions are resolved, or
* a tension is declared irreconcilable and pushed to **Deferred Tensions**.

---

# 7. Phase 4 — Assembly (Module Construction)

With a skeleton and resolved sections, emit a full v7-style module.

```markdown
---
id: MATH-GAMMA-OPS-001
title: Operational Definition of Temporal Density
version: 1.0-DEBATE
status: draft
parents: [CORE-001, MATH-QED-005]
authors: [Curie, Aurelius, Caesar, Beauvoir]
debate_lineage:
  seed: "2025-11-07-gamma-ops"
  rounds: 3
  tensions_resolved: 2
  tensions_deferred: 1
---

## §1 · Ontological Clarification
...

## §2 · Operational Definition
...

## §3 · Falsifiability Matrix
...

## §4 · Epistemic Justice
...

## §5 · Unresolved Tensions
...
```

This phase is what you’ll export most often to smaller machines: it’s linear, structured, and it uses the same header shape your `emit_from_lonely_v7.py` already writes.

---

# 8. Phase 5 — Ratification (Mechanical + Artistic)

MDSP insists on **two** ratifications:

1. **Mechanical** — does it meet the framework’s non-negotiables?

   ```python
   def ratify_mechanical(module):
       checks = {
           "has_falsifiability": "Test" in module_text(module),
           "cites_parents": set(module.parents).issubset(FRAMEWORK_MODULES),
           "math_consistent": validate_equations(module),
           "constraint_satisfied": all(c in module_text(module) for c in seed["constraints"])
       }
       return all(checks.values()), checks
   ```

2. **Artistic** — does it *feel* like four voices made one instrument?

   ```json
   {
     "votes": {
       "curie": {"coherence": 0.85, "necessity": 0.95, "beauty": 0.70},
       "aurelius": {"coherence": 0.90, "necessity": 0.80, "beauty": 0.90},
       "caesar": {"coherence": 0.75, "necessity": 1.0, "beauty": 0.60},
       "beauvoir": {"coherence": 0.95, "necessity": 0.85, "beauty": 0.85}
     },
     "threshold": 0.80,
     "status": "RATIFIED"
   }
   ```

**Outcomes:**

* `RATIFIED` → publish as proper v7 node
* `REVISE` → re-enter Phase 3 for the lowest dimension
* `REJECT` → go back to Phase 0 with a smarter seed

---

# 9. Essentialized Instruction Set (API-Facing)

## 9.1 Persona Invocation

```text
SYSTEM:
You are [PERSONA_NAME] ([PERSONA_ID]).
Your parametric flavor: T_a=[VALUE], Γ=[VALUE], K_i=[VALUE]
Your debate weights: [CONSTITUTION_DICT]

CRITICAL: You are not judging a module. You are BUILDING it.
Output JSON:
- section
- content (≤400 tokens)
- constraints_added
- tensions
```

## 9.2 Essentialization

```text
Input: [LIST_OF_THREADS]
Extract:
1. Dependency graph
2. Blocking tensions (with severity)
3. Hard/soft constraints
Output JSON in ESSENTIALIZATION_SCHEMA
Token budget: 300
```

## 9.3 Weaving

```text
Input: tension + 2 threads
Output: synthesis JSON
Token budget: 400
```

## 9.4 Assembly

```text
Input: skeleton + resolved sections + deferred tensions
Output: v7 markdown module
Token budget: 1200
```

This makes MDSP runnable on a cascade of different model sizes: large for Phase 1, small for Phases 2–4, tiny for mechanical ratification.

---

# 10. Key Differences from Earlier Debate Protocols

| Earlier Pattern (e.g. DYNA-002) | MDSP v7                                   |
| ------------------------------- | ----------------------------------------- |
| Goal: shared understanding      | Goal: publishable module                  |
| Personas defend positions       | Personas build sections                   |
| Synthesis is emergent           | Synthesis is phased/structural            |
| Output: insight                 | Output: well-formed v7 node               |
| Weaving = “get along”           | Weaving = “resolve blocking tech tension” |
| Success = resonance             | Success = ratified artifact               |

MDSP is what your constitutional convention needed: a debate you can **hand to a machine** and expect a module back.

---

# 11. Autopoietic DNA Integration

MDSP keeps the Pirouette autopoietic cycle alive inside debate:

1. **Temporal Pressure (Γ):** the seed states a gap; debate must close it.
2. **Resonance (Ki):** personas emit distinct modes (empiricist, philosopher, strategist, ethicist).
3. **Time Adherence (T_a):** mechanical ratification enforces adherence to framework time/order.
4. **Wound Channel / Persistence:** assembled modules become persistent, linkable structure.
5. **Alchemical Union:** weaving converts contradiction → higher-order coherence.

So: **the debate is the Pirouette; the module is the scar.**

---

# 12. Implementation Sketch (Reference)

```python
class ModularDebateSynthesis:
    def __init__(self, seed, personas):
        self.seed = seed
        self.personas = personas
        self.state = {}

    def run(self):
        # Phase 0
        if self.exists_in_framework(self.seed):
            return self.retrieve_for_revision()

        # Phase 1
        threads = [p.generate_section(self.seed) for p in self.personas]

        # Phase 2
        structure = self.essentialize(threads)

        # Phase 3
        while structure.get("tensions", []) and any(t["severity"]=="blocking" for t in structure["tensions"]):
            t = self.next_blocking(structure["tensions"])
            res = self.weave(t)
            structure = self.apply_resolution(structure, res)

        # Phase 4
        module = self.assemble(structure, threads, self.seed)

        # Phase 5
        ok, checks = self.ratify(module)
        if ok:
            return module
        else:
            return {"status": "REVISE", "checks": checks}
```

---

**Module end.**
