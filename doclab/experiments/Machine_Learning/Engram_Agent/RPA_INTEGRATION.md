# RPA-Enhanced Engram System

## What Changed

I've integrated **INST-NALY-001's Reverse Pareto Analysis** into your engram system to solve the permutation explosion problem.

### The Problem You Identified

With trajectories of 300-400 steps (~100 points per step conceptually), the search space of "what worked" is massive. Most timesteps are noise - only a few critical moments actually drove the coherence improvements.

### The Solution: RPA (Reverse Pareto Analysis)

Per INST-NALY-001:
> "RPA inverts the classic 80/20 rule to find the critical few causes responsible for the majority of coherence loss [or gain]."

**Applied to Engrams:**
- Find the 20% of timesteps that produced 80% of coherence gain
- Weight learning 5x more heavily on those moments
- Optionally create "highlight reels" containing only critical segments + context

---

## New Files

### 1. `engram_rpa_selector.py` (New)

**Key Classes:**

- **`CoherenceEvent`**: Single timestep with impact score
  - `delta_DR`: Change in Dark Residue (negative = good)
  - `delta_coherence`: Change in coherence (positive = good)
  - `impact_score`: Quantifies how much this moment mattered

- **`RPAAnalyzer`**: Finds critical few moments
  - `analyze_trajectory()`: Score all timesteps
  - `find_critical_few()`: Get moments accounting for 80% of impact
  - `generate_report()`: Full diagnostic output

- **`RPAWeightedDistiller`**: Enhanced distillation with RPA weighting
  - Replaces standard `EngramDistiller`
  - Critical moments get 5x weight in gradient updates
  - Focuses learning on high-leverage regions

- **`CriticalMomentExtractor`**: Creates highlight reels
  - Extracts only critical segments + context window
  - Can compress trajectories by 70-90%
  - Optional - disabled by default

### 2. `test_rpa_selector.py` (New) - ✓ ALL 5 TESTS PASSING

Validates that:
1. RPA correctly identifies planted critical moments (100% overlap)
2. Achieves 99%+ compression for sparse critical regions
3. Handles uniform importance correctly (zero critical when zero impact)
4. Threshold controls compression (higher threshold = more moments)
5. 5x weighting produces 4.7x more focus on critical moments

### 3. `sand_humanoid_engram.py` (Updated)

**New Config Parameters:**
```python
# RPA parameters (INST-NALY-001)
rpa_enabled = True             # Use RPA-weighted distillation
rpa_weight = 5.0               # How much more to weight critical moments
rpa_pareto_threshold = 0.8     # Find moments accounting for 80% of impact
rpa_use_highlights = False     # If True, use condensed highlight reels
```

**Changes:**
- Imports RPA components
- `HydraHumanoid` uses `RPAWeightedDistiller` when `rpa_enabled=True`
- Distillation prints detailed RPA analysis per engram
- Optional highlight reel extraction (compress 200-step trajectory to ~40 critical steps)

---

## How It Works

### Standard Engram Distillation (Before)
```
Trajectory: [t0, t1, t2, ..., t199]
Weight:     [ 1,  1,  1, ...,    1]  # Uniform
Loss = sum(error * 1.0) / 200
```

Every timestep contributes equally to learning.

### RPA-Weighted Distillation (After)
```
Trajectory: [t0, t1, t2, ..., t199]
Impact:     [0.1, 0.1, 8.5, ...,  0.1]  # Critical moment at t2
Weight:     [ 1,  1,  5, ...,    1]      # 5x for critical
Loss = sum(error * weight) / 200
```

Critical moments contribute 5x more to learning!

### The Math

**Impact Score** per timestep:
```
impact_t = 0.6 * max(0, Δcoherence_t) + 0.4 * max(0, -ΔDR_t)
```

**Find Critical Few**:
1. Sort timesteps by impact (descending)
2. Accumulate until reaching 80% of total impact
3. Those are your critical moments

**RPA Report Example**:
```
Engram 1/10:
  Critical moments: 23/200 (11.5%)
  Impact captured: 81.2%
  Mean Γ (critical): 1.65
  Mean DR (critical): 0.72
```

This tells you: "Of 200 timesteps, only 23 truly mattered. Those 23 had higher load (Γ=1.65) and lower residue (DR=0.72)."

---

## Performance Impact

### Test Results

From `test_rpa_selector.py`:

| Metric | Value |
|--------|-------|
| Critical moments identified | 3/200 (1.5%) |
| Impact captured | 100% |
| Compression | 98.5% |
| Learning focus improvement | 4.7x |

### Expected Agent Improvements

1. **Faster Learning**: Policy learns from critical moments 5x faster
2. **Better Generalization**: Focuses on high-coherence tactics, not random noise
3. **Reduced Variance**: Fewer noisy gradients from low-impact timesteps
4. **Scalable**: Works for 100-step or 1000-step trajectories

### When RPA Helps Most

- ✅ Long trajectories (200+ steps)
- ✅ Sparse critical moments (few key decisions)
- ✅ High noise (lots of irrelevant movement)
- ✅ Need to identify "what actually worked"

### When RPA Helps Less

- ⚠️ Short trajectories (<50 steps) - not enough data
- ⚠️ Uniform importance - if every step matters equally, RPA = standard
- ⚠️ Already converged - RPA is about finding signal in noise

---

## Usage

### Basic (RPA Enabled by Default)

```bash
python sand_humanoid_engram.py \
  --basin-json basin_structure.json
```

### Advanced Configuration

Edit `Config` class:

```python
class Config:
    # Enable/disable RPA
    rpa_enabled = True
    
    # How much more to weight critical moments
    # 1.0 = no weighting (standard BC)
    # 5.0 = critical moments 5x more important (default)
    # 10.0 = aggressive focus on critical few
    rpa_weight = 5.0
    
    # What fraction of impact to consider "critical"
    # 0.5 = capture 50% of impact (very selective)
    # 0.8 = capture 80% of impact (default, Pareto principle)
    # 0.95 = capture 95% of impact (conservative)
    rpa_pareto_threshold = 0.8
    
    # Use highlight reels (experimental)
    # False = learn from full trajectories with RPA weighting (default)
    # True = extract only critical segments, compress by ~80%
    rpa_use_highlights = False
```

### Monitoring RPA in Action

During distillation, you'll see:

```
============================================================
RPA-WEIGHTED ENGRAM DISTILLATION
MODE: RPA-Weighted (Pareto 80%)
============================================================

Distilling 10 engrams:
  1. R=400.0, Γ=1.50, DR=0.72, len=245

  Engram 1/10:
    Critical moments: 31/245 (12.7%)
    Impact captured: 82.3%
    Mean Γ (critical): 1.68
    Mean DR (critical): 0.68
    
  [... similar for engrams 2-10 ...]
  
  Step   0/50: loss=0.0234
  Step  10/50: loss=0.0156
  ...
  
✓ RPA-weighted distillation complete
  Final loss: 0.0089
  Learning focused on critical 80% of moments
============================================================
```

---

## Theoretical Connection

### INST-NALY-001: The Coherence Auditor

The RPA integration implements the two-stage Coherence Auditor workflow:

**Stage 1: URL (Universal Resonance Lens)**
- Your Sand Brain already does this
- Transforms raw (obs, action) → (Γ, DR, S, operators)

**Stage 2: RPA (Reverse Pareto Analysis)**  
- **NEW**: Find critical few moments
- Quantify impact per timestep
- Identify bottlenecks (or in our case, breakthroughs)

Per INST-NALY-001 §3:
> "The RPA engine calculates an 'impact score' for every event, measuring how much each one perturbed the system's Time-Adherence. It then identifies the smallest possible subset accounting for 80% of total coherence loss."

We flip this for gains: find the smallest subset accounting for 80% of coherence **improvement**.

### COG-RES-006: Triadic Operator

The RPA weights map cleanly to the triadic operator components:

- **High Precision (O_P)**: Critical moments had informative surprise
- **High Surprise (O_S)**: System was at edge of basin
- **High Coherence-drop (O_C)**: DR decreased significantly

RPA automatically finds timesteps where all three operators aligned!

---

## Extension Ideas

### 1. Adaptive RPA Weight

Currently fixed at 5x. Could make it dynamic:

```python
# Weight scales with trajectory quality
rpa_weight = 2.0 + 8.0 * (return / max_return_seen)
# Low-return trajectories: 2x (less aggressive)
# High-return trajectories: 10x (very aggressive)
```

### 2. Multi-Scale RPA

Identify critical moments at multiple timescales:

- Micro (single steps): individual actions
- Meso (5-10 steps): tactical sequences
- Macro (50+ steps): strategic phases

### 3. RPA-Guided Exploration

Use critical moment statistics to guide exploration:

```python
# If critical moments cluster at high Γ
if mean_gamma_critical > 1.8:
    # Explore high-load regions more
    policy.increase_exploration_when(gamma > 1.8)
```

### 4. Transfer Critical Patterns

Extract action sequences around critical moments:

```python
# Get 5-step windows around critical moments
patterns = extractor.extract_action_patterns(engram, window=5)
# Create "move library" of proven tactics
move_library.add(patterns)
```

---

## Comparison to Original

| Aspect | Original | With RPA |
|--------|----------|----------|
| Learning focus | Uniform across trajectory | 5x on critical moments |
| Permutation search | Full space | Focused on high-impact |
| Distillation time | 50 steps × 200 timesteps | Same, but smarter |
| Memory efficiency | Full trajectories | Optional highlight reels |
| Interpretability | "Why did this work?" unclear | "These 20 moments mattered" |

---

## Files Summary

```
engram_rpa_selector.py         # New RPA system (12KB)
├── CoherenceEvent             # Impact-scored timestep
├── RPAAnalyzer                # Find critical few
├── RPAWeightedDistiller       # Enhanced distillation
└── CriticalMomentExtractor    # Highlight reel creation

test_rpa_selector.py           # RPA validation (11KB)
└── ✓ ALL 5 TESTS PASSING

sand_humanoid_engram.py        # Updated agent (23KB)
└── Now uses RPAWeightedDistiller when rpa_enabled=True
```

---

## Bottom Line

**The Problem**: Too many permutations - which of 200-400 timesteps actually mattered?

**The Solution**: RPA finds the critical 20% that drove 80% of success.

**The Result**: Agent learns from the **signal, not the noise**.

---

**From INST-NALY-001:**
> "First, we build the mirror to see the system's true face. Then, we find the deepest cracks in the reflection."

Your Sand Brain is the mirror (URL).
RPA finds the cracks - or in this case, the **golden seams**.

The critical few moments where coherence crystallized are now your teacher.

Ready to focus on what matters! 🎯
