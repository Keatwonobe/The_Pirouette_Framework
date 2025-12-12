---
id: DYNA-WITNESS-002
title: Witness-Centered Run Ecology (Script-Independent Form)
version: 1.0
depends_on:
  - DYNA-WITNESS-001
intent: >
  Generalize the "save the good runs" insight into a reusable, domain-agnostic
  ecology that can be dropped into any Pirouette-style experiment, even where the
  runner is unknown or external.
status: canonical
---

## 1. Motivation

DYNA-WITNESS-001 said: **the act of witnessing is the real collapse.**  
This module says: **once you witness, you must *govern* what you witnessed.**

In practice, every domain (RL, simulation bursts, plateau scans, data-cleaning passes,
semantic crawls, physics kernel sweeps) produces *episodes*: finite, scoreable
encounters with a manifold.

These episodes are **not all equal**. Some are:

- *strangely good* (high score, low jank → "bright coherence"),
- *strangely bad* (low score, high jank → "dark residue attractors"),
- and a big middle where *change lives*.

This module formalizes the idea you just landed on:  
> *Pirouette is a curated pile of coherent dives.*  
So we’ll treat **curation** itself as a dynamic.

---

## 2. Objects

We define four script-agnostic objects.

1. **Run**  
   A single attempt at something.  
   ```text
   Run = {
     id:          UUID or (task, episode, timestamp),
     task:        string,              # domain / environment / dataset
     score:       float,               # "present" success
     dr:          float,               # dark residue, "how jank"
     span:        float in [0,1],      # how far we got into the manifold
     meta:        dict                 # arbitrary (seed, model, params, notes...)
   }
````

2. **Witness**
   A passive logger that receives every `Run` and never lies about history.

3. **Gallery**
   A *view* over witnessed runs, filtered and ordered by a coherence function.

4. **Ecology**
   A *policy* for how often we look at each part of the gallery (best, worst, mid).

This module gives you 2–4 in generic form.

---

## 3. Core Principle

> **Do not throw runs away.**
> **Do not sample only the peaks.**
> **Do not obsess over the failures.**
> **Live in the Pareto band.**

Why?

* The **best** runs tell you *what’s already coherent* → good for publishing, not for learning.
* The **worst** runs tell you *what the manifold rejects* → good for guardrails.
* The **middle** runs tell you *what can still be bent* → good for optimization.

So the ecology is:

1. Always **record** (witness-first).
2. Always **separate** (top / mid / worst).
3. **Bias sampling** toward mid.
4. Occasionally **revisit** worst for reverse-Pareto analysis (what *caused* dark residue).
5. Always **export galleries** so humans/agents can see the manifold.

---

## 4. Generic Coherence Function

We want to rank runs *without* assuming a specific script.

Define a **coherence score**:

[
C(\text{run}) = w_s \cdot \text{norm(score)} ;+; w_{sp} \cdot \text{span} ;-; w_{dr} \cdot \text{dr}
]

Where:

* `score` → “present success”
* `span` → “environmental perception / coverage”
* `dr` → “jank / residue / incoherence”
* `w_s, w_sp, w_dr` → tunable, but default to (1.0, 0.5, 1.0)

This lets you plug in *anything* that emits `(score, span, dr)`.

If your runner doesn’t emit those yet, you can **fake** them:

* `score = metric_you_already_log`
* `span = steps / max_steps` or `processed_items / total_items`
* `dr = abs(diff between current and previous params)` or `#exceptions / #ops`

---

## 5. Data Structures (Minimal)

```python
class Run:
    def __init__(self, task, score, dr, span, meta=None):
        self.task  = task
        self.score = float(score)
        self.dr    = float(dr)
        self.span  = float(span)
        self.meta  = meta or {}
```

```python
class Witness:
    def __init__(self):
        self.all_runs = []              # complete history
        self.by_task  = {}              # task -> [runs]

    def observe(self, run: Run):
        # 1. store globally
        self.all_runs.append(run)
        # 2. store per task
        bucket = self.by_task.setdefault(run.task, [])
        bucket.append(run)
```

This is *all* you need to start.
No runner dependency yet.

---

## 6. Gallery Construction

Now, for any task, build three galleries.

```python
def build_galleries(runs: list, top_k=15, worst_k=5):
    # order by coherence
    def coherence(r: Run, ws=1.0, wsp=0.5, wdr=1.0):
        return ws*r.score + wsp*r.span - wdr*r.dr

    ordered = sorted(
        runs,
        key=lambda r: coherence(r),
        reverse=True
    )

    top   = ordered[:top_k]
    worst = ordered[-worst_k:] if len(ordered) >= worst_k else ordered[-1:]
    mid   = ordered[top_k:-worst_k] if len(ordered) > (top_k + worst_k) else []

    return top, mid, worst
```

**Notes:**

* `top` → what you show people
* `mid` → what you sample from
* `worst` → what you analyze when DR suddenly spikes

This is now ENTIRELY independent of `wendigo_feather.py`.
Any script that can call `Witness.observe(...)` can use this.

---

## 7. Ecology / Sampling Policy

This is the “try the very best and very worst the least” part.

```python
import random

def sample_for_next_run(task_runs, ratio=(0.1, 0.7, 0.2)):
    """
    ratio = (p_top, p_mid, p_worst)
    """
    top, mid, worst = build_galleries(task_runs)
    p_top, p_mid, p_worst = ratio

    r = random.random()
    if r < p_top and top:
        return random.choice(top)
    elif r < (p_top + p_mid) and mid:
        return random.choice(mid)
    elif worst:
        return random.choice(worst)
    else:
        # fallback if very small dataset
        return random.choice(task_runs)
```

Interpretation:

* **Top (10%)** → “stability anchors” (what good looks like)
* **Mid (70%)** → “where to push”
* **Worst (20%)** → “what to avoid / what produced dark residue”

You can **flip** the ratio for exploration-heavy phases.

---

## 8. Export / Gallery Per Game

Your original instinct — “give me a gallery per game of what ‘good’ looks like” — is the right affordance. Make this boringly simple:

```python
import json, os, time

def export_task_gallery(task: str, runs: list, outdir="gallery_witness"):
    os.makedirs(outdir, exist_ok=True)
    top, mid, worst = build_galleries(runs)
    stamp = time.strftime("%Y%m%d-%H%M%S")

    payload = {
        "task": task,
        "timestamp": stamp,
        "counts": {
            "total": len(runs),
            "top": len(top),
            "mid": len(mid),
            "worst": len(worst),
        },
        "top": [run.__dict__ for run in top],
        "worst": [run.__dict__ for run in worst],
        # mid can be large, so we skip or truncate
        "mid_sample": [run.__dict__ for run in mid[:25]],
    }

    with open(os.path.join(outdir, f"{task}_{stamp}.json"), "w") as f:
        json.dump(payload, f, indent=2)
```

No dependency on the actual runner.
If tomorrow you run your *plateau-scatterer* or *fractal-mirror learner*, just call:

```python
witness.observe(Run(task="fractal_mirror", score=..., dr=..., span=...))
export_task_gallery("fractal_mirror", witness.by_task["fractal_mirror"])
```

---

## 9. Pirouette Reading

**Claim**: *a Pirouette volume is a temporal stack of “top” galleries across domains.*

This module makes that explicit:

* DYNA-WITNESS-001: “Observation is the pinch.”
* **DYNA-WITNESS-002**: “Curate what the pinch caught.”
* DYNA-WITNESS-003 (next): “Let galleries talk to each other.”

So yes, the thing you suspected is basically true:

> *Pirouette is a collection of best (i.e. most coherent) dives across domains,
> stitched together by a witness that never stopped writing things down.*

This module is how we make that legible.

---

## 10. Minimal Usage Pattern

```python
w = Witness()

# somewhere in your runner loop (whatever it is)
w.observe(Run(task="cartpole", score=23, dr=0.01, span=0.2))
w.observe(Run(task="cartpole", score=86, dr=0.03, span=0.4))
w.observe(Run(task="pendulum", score=-1350, dr=0.15, span=0.9))

# later...
for task, runs in w.by_task.items():
    export_task_gallery(task, runs)
```

No tight coupling. No required file layout.
Just: **witness → group → gallery → sample.**

---

## 11. Notes for Canon

1. This is a **DYNA** module because it governs *flow of episodes*, not formulae.
2. This can sit under a higher **GOV-** or **ARCH-** module that decides *retention*.
3. This solves the “my script was flat” problem by **making flatness visible**: if
   the gallery shows only mid-runs, the issue is in the runner, not the ecology.
4. This is the missing half of “I saved good experiments and it got better.”
   Now it’s repeatable.

---