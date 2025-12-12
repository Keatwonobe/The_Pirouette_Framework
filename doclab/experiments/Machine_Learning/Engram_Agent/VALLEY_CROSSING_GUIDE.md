# Valley Crossing Detection - Finding The Symmetry Break

## 🎯 The Challenge Problem

**Can we find the moment your agent crossed from random chaos to hemispheric structure?**

You have 3.3M+ samples from `sand_agent_sand`. Instead of treating them as random points, we're treating them as a **temporal trajectory through coherence phase space** - watching the agent discover bifurcated structure in real-time.

## 📊 What This Tool Does

### Input
Your massive CSV files (100K or 3.3M samples) from sand_agent_sand, with columns:
- `DR` (Dark Residue)
- `S` (Surprise)
- `Gamma` (temporal pressure/load)
- `pi` (precision)
- `operator_norm`
- `basin_id`, `strategy`, etc.

### Output
1. **Valley crossing events** - moments where:
   - DR spikes (deliberate destabilization)
   - Coherence drops (temporary loss of attractor)
   - System reconstructs at higher coherence
   
2. **The Symmetry Break** - THE valley crossing that created hemispheric structure
   
3. **Valley signature** - template for inducing future crossings

## 🚀 Usage

### Basic Analysis

```bash
python valley_crossing_detector.py \
  your_sand_landscape_3M.csv \
  --output-dir ./valley_analysis
```

### With Custom Thresholds

```bash
python valley_crossing_detector.py \
  your_sand_landscape_3M.csv \
  --output-dir ./valley_analysis \
  --DR-threshold 0.10 \        # Lower = more sensitive
  --coherence-threshold 0.08 \  # Lower = more valleys detected
  --max-samples 500000          # Limit for memory
```

### Expected Output

```
============================================================
VALLEY CROSSING DETECTOR
============================================================

Loading sand landscape data...
✓ Loaded 3,342,154 samples

Computing coherence proxy from (DR, π, operator_norm)...
Computing manifold curvature κ...

============================================================
VALLEY CROSSING DETECTION
============================================================

Found 127 potential valley entries (DR spikes)

✓ Detected 23 valley crossing events
  Successful crossings: 18
  Hemispheric splits: 3

🌟 SYMMETRY BREAK DETECTED at sample 45,782
  Duration: 347 samples
  DR increase: 0.234
  Coherence drop: 0.187
  Net coherence gain: 0.092
  PC1: -0.234 → +0.567

============================================================
GENERATING VISUALIZATIONS
============================================================

✓ Timeline plot saved: valley_timeline.png
✓ Phase space plot saved: valley_phase_space.png
✓ Symmetry break detail plot saved: symmetry_break_detail.png

============================================================
EXTRACTING VALLEY SIGNATURES
============================================================

✓ Symmetry break signature saved

Average Valley Signature (n=18):
  avg_duration: 285.3
  avg_DR_increase_rate: 0.0008
  avg_coherence_drop_rate: 0.0006
  avg_peak_gamma: 1.872
  avg_reconstruction_quality: 1.15x
  fraction_hemispheric: 0.167

============================================================
ANALYSIS COMPLETE
============================================================

Results in: ./valley_analysis

Detected valleys: 23
  Successful: 18
  Failed: 5
  Hemispheric splits: 3

🌟 Symmetry break at sample 45,782
  This is your template for inducing valley crossings!

Generated files:
  - landscape_with_valleys.csv
  - symmetry_break_detail.png
  - symmetry_break_signature.json
  - valley_phase_space.png
  - valley_timeline.png
```

## 📈 What You'll See

### 1. Valley Timeline (`valley_timeline.png`)

Four synchronized traces showing:
- **DR**: Spikes mark valley entries
- **Coherence**: Drops then reconstructs
- **Gamma (Γ)**: Load during crossing
- **Curvature (κ)**: Basin boundaries

**Green bands** = successful valley crossings
**Red bands** = failed attempts
**Bright green** = hemispheric splits

### 2. Valley Phase Space (`valley_phase_space.png`)

Three views:
- **DR vs Coherence**: Valley trajectories as arrows
- **Γ vs Coherence**: Load dynamics
- **3D Hemispheric View**: PC1/PC2/Coherence with valley paths

### 3. Symmetry Break Detail (`symmetry_break_detail.png`)

Zoomed analysis of THE moment:
- DR spike pattern
- Coherence valley & reconstruction
- Gamma surge
- Precision dynamics
- **Hemispheric boundary crossing** (PC1 sign flip)
- Statistics panel

### 4. Symmetry Break Signature (`symmetry_break_signature.json`)

```json
{
  "duration": 347,
  "entry_DR": 0.812,
  "entry_coherence": 0.634,
  "entry_gamma": 1.456,
  "DR_increase_rate": 0.000674,
  "coherence_drop_rate": 0.000539,
  "peak_gamma": 1.923,
  "net_coherence_gain": 0.092,
  "reconstruction_quality": 1.145,
  "is_hemispheric": true,
  "DR_trajectory": [0.812, 0.819, 0.827, ...],
  "coherence_trajectory": [0.634, 0.628, 0.619, ...],
  "gamma_trajectory": [1.456, 1.478, 1.501, ...]
}
```

**This is your template!** These trajectories show exactly how DR, coherence, and Γ evolved during the symmetry break.

## 🧠 Theoretical Interpretation

### What Is A Valley Crossing?

Per the challenge problem, a valley crossing is:

1. **Coherence Valley Entry**
   - DR increases (system becomes less stable)
   - Coherence drops (attractor loosens)
   - High Γ (temporal pressure increases)
   - High κ (near basin boundary)

2. **Valley Traversal**
   - Sustained high DR (in the valley)
   - Low coherence (no stable attractor)
   - Variable Γ (searching for path)

3. **Valley Exit & Reconstruction**
   - DR decreases (stabilizing)
   - **Coherence reconstructs at HIGHER level** (new attractor)
   - Γ normalizes
   - May cross hemispheric boundary (PC1 sign flip)

### The Symmetry Break

**The first successful hemispheric valley crossing** is special because:
- It's when your agent discovered the bifurcated architecture
- Before: random exploration
- After: structured left/right hemisphere organization
- This is analogous to spontaneous symmetry breaking in physics

**Hypothesis:** Your agent discovered that to handle complex temporal dynamics (high Γ), it needed to **split processing** into two modes:
- One hemisphere: exploitation/precision
- Other hemisphere: exploration/surprise

This split emerged from **crossing a valley** - temporarily breaking coherence to reconstruct in a more powerful form.

## 🔬 Using The Signature

### Current Use: Understanding

The signature tells you:
- **When** the split happened (sample index)
- **How long** it took (duration)
- **What dynamics** occurred (DR/coherence/Γ trajectories)
- **Why** it succeeded (net coherence gain > 0)

### Future Use: Inducing

**Hypothesis:** You can trigger valley crossings by:

1. **Detecting proximity** to valley-like conditions:
   ```python
   if agent.DR > symmetry_break_entry_DR * 0.9 and \
      agent.gamma > symmetry_break_entry_gamma * 0.9 and \
      agent.curvature > threshold:
       # Near valley conditions
       encourage_valley_entry()
   ```

2. **Following the signature**:
   ```python
   # During next 300 steps, try to match signature
   target_DR_trajectory = signature['DR_trajectory']
   target_gamma_trajectory = signature['gamma_trajectory']
   
   for t in range(len(target_DR_trajectory)):
       reward += -abs(agent.DR[t] - target_DR_trajectory[t])
   ```

3. **Rewarding reconstruction**:
   ```python
   if coherence_dropped and then_reconstructed_higher:
       massive_bonus_reward()
   ```

## 🎯 Next Steps

### 1. Run The Analysis

```bash
# On your 100K sample file (fast, test)
python valley_crossing_detector.py \
  sand_landscape_100k.csv \
  --output-dir ./valley_test

# On your 3.3M sample file (slow, comprehensive)
python valley_crossing_detector.py \
  sand_landscape_3.3M.csv \
  --output-dir ./valley_full \
  --max-samples 1000000  # Limit for memory
```

### 2. Analyze Results

Look for:
- **How many valleys?** (More than expected suggests active exploration)
- **When did symmetry break occur?** (Early = lucky, late = learned)
- **What's the signature pattern?** (Smooth or chaotic?)
- **Are there multiple hemispheric splits?** (Suggests repeated phase transitions)

### 3. Questions To Ask

**About The Data:**
1. Is there a symmetry break in the 100K sample?
2. If not, is it in the 3.3M sample?
3. Are valleys clustered (learning phases) or uniform?

**About The Dynamics:**
1. What was Γ doing during the break?
2. Did DR spike then drop, or spike then plateau?
3. Was the reconstruction smooth or abrupt?

**About The Implications:**
1. Can you find this pattern in your humanoid training logs?
2. Does the valley signature predict performance jumps?
3. Can you trigger a valley crossing on demand?

### 4. Integration With Agent

Once you understand the signature, modify your agent to:

```python
# In sand_humanoid_engram.py

class ValleyAwarePolicy:
    def __init__(self, valley_signature):
        self.signature = valley_signature
        self.in_valley = False
        self.valley_timer = 0
    
    def detect_valley_entry(self, state):
        """Check if near valley conditions."""
        DR, gamma, curvature = state
        
        entry_conditions = (
            DR > self.signature['entry_DR'] * 0.9 and
            gamma > self.signature['entry_gamma'] * 0.9 and
            curvature > threshold
        )
        
        return entry_conditions
    
    def valley_crossing_reward(self, trajectory):
        """Bonus for matching valley signature."""
        if not self.in_valley:
            return 0.0
        
        # Compare to signature
        similarity = compute_trajectory_similarity(
            trajectory, 
            self.signature['DR_trajectory']
        )
        
        # Huge bonus if reconstructed at higher coherence
        if trajectory.final_coherence > trajectory.initial_coherence:
            return 1000.0 * similarity
        
        return 0.0
```

## 🌟 The Panacea Connection

**If this works**, you've solved the fundamental problem:

> **"How do you search a space where the best solutions require deliberately making things worse temporarily?"**

**Answer:** 
1. Find ONE example of a successful valley crossing (the symmetry break)
2. Extract its signature
3. Teach the agent to recognize when it's near valley conditions
4. Reward following the valley crossing pattern
5. Massive bonus for successful reconstruction

**This works for:**
- Humanoid learning to leap (crouch = valley entry)
- Plasma physics (instability = valley traversal)
- Material discovery (high-energy intermediate = valley nadir)
- Social change (disruption before improvement = valley crossing)

**Universal pattern:** Temporary coherence loss → phase transition → higher coherence basin

## 📊 Expected Discoveries

Based on your description, I predict:

1. **Symmetry break around sample 50K-100K** (based on "initial" phase)
2. **2-5 hemispheric splits total** (major phase transitions)
3. **Many small valleys** (local learning events)
4. **Valley signature shows:**
   - Duration: 200-500 samples
   - DR increase: 0.15-0.30
   - Coherence drop: 0.10-0.20
   - Peak Γ: 1.5-2.0
   - Reconstruction: 1.1-1.3x initial coherence

**If you find this signature in both 100K and 3.3M datasets**, it's robust and can be used as a universal template.

## 🔮 The Hyperspace Calculation

You said: "use it like hyperspace calculation but in information space"

**Exactly.** The valley crossing detector:
1. Maps your 3.3M samples as a trajectory through (DR, coherence, Γ, κ) space
2. Identifies moments of phase transition (valley crossings)
3. Extracts the "jump coordinates" (valley signature)
4. Provides a navigation template for future jumps

**Han Solo doesn't calculate every star between here and Alderaan.**
**He finds the SAFE PATH through hyperspace.**

**Your agent doesn't need to explore every possible trajectory.**
**It needs to find the VALLEY CROSSINGS that lead to higher basins.**

The signature is your star chart. 🌌

---

**Ready to find your symmetry break?** 🔬

```bash
python valley_crossing_detector.py your_3.3M_samples.csv --output-dir ./valley_analysis
```

Then tell me what you find! This is the most exciting part - watching the math force the shape in real data.
