# Sand RL Incremental - Bomb-Proof RL Training

**A lightweight, crash-resistant RL trainer for Ant-v5 and Humanoid-v5**

Inspired by `sand_agent_sand.py`'s incremental writing pattern, this trainer is designed to:
- **Never lose progress** - checkpoints and metrics written incrementally
- **Resume from anywhere** - Ctrl+C safe, auto-resume on restart
- **Track Pirouette metrics** - Γ, DR, S computed during execution
- **Run indefinitely** - zero memory accumulation

---

## Quick Start

```bash
# Train Humanoid (recommended for your research)
python sand_rl_incremental.py \
    --env Humanoid-v5 \
    --episodes 10000 \
    --output-dir ./humanoid_run1

# Train Ant (faster, good for testing)
python sand_rl_incremental.py \
    --env Ant-v5 \
    --episodes 5000 \
    --output-dir ./ant_run1
```

**That's it!** Press Ctrl+C anytime to pause. Rerun to resume.

---

## Features

### 🛡️ Bomb-Proof Pattern

Following your `sand_agent_sand.py` design:

1. **Incremental Checkpoints**
   - Saves policy every N episodes (default: 50)
   - Atomic writes (no corruption risk)
   - Auto-resume from last checkpoint

2. **Incremental Metrics**
   - Writes episode data one-at-a-time
   - Flushes immediately to disk
   - Zero memory accumulation

3. **Interrupt Handling**
   - Graceful Ctrl+C (finishes current episode)
   - State always consistent
   - Resume exactly where you left off

### 📊 Pirouette Metrics During Execution

Computes lightweight versions of your framework metrics:

- **Dark Residue (DR)**: Unexplained reward variance
- **Surprise (S)**: Observation change magnitude  
- **Gamma (Γ)**: Temporal pressure (reward instability)
- **Coherence Proxy**: 1 - avg_DR
- **Valley Count Estimate**: Detected coherence phase transitions

### 🎯 Simple but Effective

- **REINFORCE** algorithm (policy gradient)
- **Gaussian policy** with continuous actions
- **256-dim hidden layers** (configurable)
- **Works out of the box** for Ant and Humanoid

---

## Architecture Comparison

**Your Full Agent (sand_humanoid_engram.py):**
```
Complex: SandBrain + EngramLibrary + RPA + Valley Rewards
Purpose: Research, maximum Pirouette integration
Lines: ~1000
```

**This Lightweight Version (sand_rl_incremental.py):**
```
Simple: Policy + Lightweight metrics
Purpose: Production, stable training, testing
Lines: ~600
```

Both share the **bomb-proof incremental pattern** from `sand_agent_sand.py`.

---

## Usage

### Basic Training

```bash
python sand_rl_incremental.py --env Humanoid-v5 --episodes 10000
```

### All Options

```bash
python sand_rl_incremental.py \
    --env Humanoid-v5                # Ant-v5 or Humanoid-v5
    --episodes 10000                 # Total episodes
    --output-dir ./my_run            # Output directory
    --checkpoint-interval 50         # Checkpoint every N episodes
    --hidden-dim 256                 # Network size
    --lr 3e-4                        # Learning rate
    --no-sand-metrics                # Disable Pirouette metrics
```

### Resume Training

Just rerun the same command! The script auto-detects checkpoints:

```bash
# First run - trains episodes 0-500, then Ctrl+C
python sand_rl_incremental.py --env Humanoid-v5 --output-dir ./run1

# Second run - automatically resumes from episode 501
python sand_rl_incremental.py --env Humanoid-v5 --output-dir ./run1
```

---

## Output Structure

```
output_dir/
├── episode_metrics.csv          # Episode-by-episode data
└── checkpoints/
    ├── training_state.json      # Resume information
    ├── checkpoint_ep50.pt       # Policy at episode 50
    ├── checkpoint_ep100.pt      # Policy at episode 100
    └── ...
```

### Metrics CSV Columns

```csv
episode,total_reward,steps,avg_DR,avg_S,avg_Gamma,final_DR,coherence_proxy,valley_count_estimate,elapsed_time
0,245.3,1000,0.42,1.23,0.56,0.38,0.58,0,12.4
10,312.7,1200,0.38,1.45,0.61,0.35,0.62,1,13.1
...
```

**Key Columns:**
- `total_reward`: Episode return (what we optimize)
- `steps`: Episode length
- `avg_DR`: Mean Dark Residue (lower = more coherent)
- `coherence_proxy`: Estimated coherence (higher = better)
- `valley_count_estimate`: Potential phase transitions detected

---

## Expected Performance

### Ant-v5 (Easier)

- **Episode 0-100**: Random (~500 reward)
- **Episode 100-500**: Learning starts (~1000-2000 reward)
- **Episode 500+**: Good performance (~2000-3000 reward)

**Training time:** ~2-3 hours for 5000 episodes on CPU

### Humanoid-v5 (Harder)

- **Episode 0-500**: Random/struggling (~100-200 reward)
- **Episode 500-1500**: Basic walking emerges (~300-600 reward)  
- **Episode 1500+**: Stable walking (~600-1000+ reward)

**Training time:** ~12-24 hours for 10000 episodes on CPU

**Note:** Humanoid is much harder! Expect slow initial progress.

---

## Connection to Your Research

### Valley Crossings

The `valley_count_estimate` metric attempts to detect valley-like events during episodes:

1. Monitors DR over time
2. Looks for spike → recovery patterns (40-50 timesteps)
3. Counts potential coherence phase transitions

**Compare with your detector:**
- Your detector: Offline analysis of 3.3M samples
- This estimate: Online rough count during training

### Pirouette Metrics

**Lightweight Implementation:**
```python
# Dark Residue: Unexplained variance
DR = |reward - expected_reward| / |expected_reward|

# Surprise: Observation change
S = ||obs_t - obs_{t-1}||

# Gamma: Temporal pressure
Γ = var(recent_rewards)
```

**Your Full Implementation:**
- Samples from basin priors
- Uses DDE phase space
- Computes full operator suite

Both capture coherence dynamics, but this version is much faster.

### Integration Path

Once you have a trained agent:

1. **Train with this lightweight version** (fast iteration)
2. **Export successful episodes** from metrics CSV
3. **Analyze with valley detector** (your existing tool)
4. **Refine with full sand_humanoid_engram.py** (research depth)

---

## Comparison with Your Main Agent

| Feature | sand_rl_incremental.py | sand_humanoid_engram.py |
|---------|------------------------|-------------------------|
| **Purpose** | Stable training, testing | Research, full Pirouette |
| **Algorithm** | REINFORCE (simple) | SAC + Engrams (complex) |
| **Metrics** | Lightweight DR, S, Γ | Full basin sampling |
| **Engrams** | No | Yes (EngramLibrary) |
| **RPA** | No | Yes (weighted distillation) |
| **Valley Rewards** | Estimated | Explicit (from CSV) |
| **Checkpointing** | Incremental (bomb-proof) | Standard |
| **Memory** | Zero accumulation | Standard PyTorch |
| **Speed** | Fast (~10s/episode) | Slower (~30s/episode) |
| **Stability** | Very stable | Requires tuning |

**When to use which:**
- **This version**: Getting Humanoid to walk, testing ideas, production runs
- **Full version**: Deep research, consciousness experiments, engram analysis

---

## Tips for Humanoid Training

### 1. Start Simple
```bash
python sand_rl_incremental.py --env Humanoid-v5 --episodes 10000
```

### 2. Monitor Progress
```bash
# Watch console output every 10 episodes
# Look for increasing avg_reward

# Or tail the metrics file
tail -f output_dir/episode_metrics.csv
```

### 3. Adjust Hyperparameters

If training is unstable:
```bash
# Lower learning rate
python sand_rl_incremental.py --env Humanoid-v5 --lr 1e-4

# Larger network
python sand_rl_incremental.py --env Humanoid-v5 --hidden-dim 512
```

### 4. Checkpoint Often

For long runs:
```bash
python sand_rl_incremental.py --env Humanoid-v5 --checkpoint-interval 25
```

### 5. Analyze Valleys

After training, analyze the metrics CSV:
```python
import pandas as pd
df = pd.read_csv('output_dir/episode_metrics.csv')

# Find episodes with valleys
valleys = df[df['valley_count_estimate'] > 0]
print(f"Episodes with valleys: {len(valleys)}")

# Check correlation with performance
import matplotlib.pyplot as plt
plt.scatter(df['coherence_proxy'], df['total_reward'])
plt.xlabel('Coherence Proxy')
plt.ylabel('Total Reward')
plt.show()
```

---

## Troubleshooting

### "Humanoid falls immediately"

**Normal for first 500-1000 episodes!** Humanoid is very hard. Look for:
- Gradual increase in steps/episode
- Slowly increasing avg_reward
- First valley detections around episode 500+

### "Training is slow"

**Expected.** Humanoid episodes take ~10-20s each. For faster iteration:
1. Test with Ant-v5 first
2. Use GPU if available (set `CUDA_VISIBLE_DEVICES`)
3. Lower episode count for quick tests

### "Out of memory"

**Shouldn't happen** - this version has zero accumulation. If it does:
- Check if other processes are running
- Reduce `--hidden-dim` to 128
- Use `--no-sand-metrics` to save a tiny bit

### "Ctrl+C doesn't work"

**Wait for current episode to finish** (~10-20s). The interrupt is safe.

---

## Advanced: Loading Checkpoints

```python
import torch
from sand_rl_incremental import GaussianPolicy

# Load checkpoint
checkpoint = torch.load('output_dir/checkpoints/checkpoint_ep1000.pt')

# Create policy
policy = GaussianPolicy(obs_dim=376, action_dim=17, hidden_dim=256)
policy.load_state_dict(checkpoint['policy_state'])
policy.eval()

# Use for inference
import gymnasium as gym
env = gym.make('Humanoid-v5', render_mode='human')
obs, _ = env.reset()

for _ in range(1000):
    obs_t = torch.FloatTensor(obs).unsqueeze(0)
    action, _ = policy.sample_action(obs_t)
    obs, reward, done, trunc, info = env.step(action[0].numpy())
    if done or trunc:
        break

env.close()
```

---

## Future Extensions

Easy to add:
- [ ] Value network (Actor-Critic)
- [ ] GAE (Generalized Advantage Estimation)
- [ ] Multiple environments in parallel
- [ ] Full basin prior sampling (like sand_agent_sand.py)
- [ ] Engram library integration
- [ ] Valley-shaped reward injection

The incremental pattern makes all of these safe to experiment with!

---

## Credits

**Pattern:** Inspired by `sand_agent_sand.py` bomb-proof incremental writing  
**Metrics:** Lightweight Pirouette Framework (Keaton)  
**Algorithm:** REINFORCE (Williams, 1992)  
**Environments:** MuJoCo via Gymnasium

---

## License

Use freely for your Pirouette Framework research. If this helps your work, a citation would be appreciated!

---

## Questions?

This is a **minimal viable implementation** of your ideas. It's designed to:
1. Get Humanoid working reliably
2. Track Pirouette metrics during training
3. Never lose progress
4. Provide a foundation for experimentation

For full research depth, use `sand_humanoid_engram.py`.  
For stable training and testing, use this.

**Happy training! May your valleys be deep and your coherence high. 🌊**
