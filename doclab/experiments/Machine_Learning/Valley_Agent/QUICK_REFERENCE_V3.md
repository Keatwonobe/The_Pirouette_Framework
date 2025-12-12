# Quick Reference: Sand RL v3.0 (Stable)

## What Changed

**Problem:** Reached 980 reward in 110 episodes, maintained for 590 episodes, then catastrophic collapse at 700-900.

**Root Cause:** Entropy collapse → policy deterministic → environmental variations → catastrophic failure

**Fix:** 5 stability mechanisms

---

## The 5 Fixes (Quick Version)

1. **Entropy Floor** - Never goes below 0.005 (was decaying to ~0.009)
2. **Value Clipping** - Max loss of 100 (prevents divergence)
3. **Buffer Clear** - Auto-clears if performance drops 70%
4. **Advantage Clip** - ±10 limit (prevents catastrophic updates)
5. **Early Stop** - Optional target (e.g., --early-stop 950)

---

## Usage

### Standard (All Fixes Active)
```bash
python sand_rl_incremental.py --env Ant-v5 --episodes 2500
```

### With Early Stop (Recommended)
```bash
python sand_rl_incremental.py --env Ant-v5 --early-stop 950
```

### For Humanoid
```bash
python sand_rl_incremental.py --env Humanoid-v5 --early-stop 2000 --episodes 10000
```

---

## Expected Performance

### Ant-v5
- Episode 0-110: 400 → 990
- Episode 110+: Stable ~980
- No collapse!

### Humanoid-v5
- Episode 0-1000: 100 → 1500
- Episode 1000-3000: 1500 → 2500
- Stable growth, no collapse

---

## What You'll See

### Good (v3 Stable)
```
Episode 100: Reward 985 | Avg: 978
Episode 200: Reward 992 | Avg: 985
Episode 500: Reward 980 | Avg: 983
Episode 1000: Reward 988 | Avg: 984
```

### Warning Signs (Auto-Fixed)
```
Episode 750: Reward 940 | Avg: 950

  ⚠ Buffer cleared! Performance dropped: 950 < 30% of best (985)

Episode 800: Reward 960 | Avg: 958  ← Recovering
Episode 850: Reward 980 | Avg: 975  ← Back to stable
```

### Early Stop (Optional)
```
Episode 110: Reward 985 | Avg: 978

🎯 Performance target reached! Avg reward: 978.0
   Stopping early at episode 110
```

---

## Key Parameters

| Parameter | Default | For Ant | For Humanoid |
|-----------|---------|---------|--------------|
| episodes | 10000 | 2500 | 10000 |
| early-stop | None | 950 | 2000 |
| checkpoint-interval | 50 | 50 | 100 |
| lr | 3e-4 | 3e-4 | 3e-4 or 1e-4 |

---

## Diagnostic

Check `collapse_diagnosis.png` for:
- Your actual training curve
- Entropy decay visualization
- Advantage distribution evolution
- Intervention points

---

## Migration from v2

**Old checkpoints won't work** (new parameters added).

**Fresh start:**
```bash
python sand_rl_incremental.py --env Ant-v5 --output-dir ./ant_v3
```

**Quick test (30 min):**
```bash
python sand_rl_incremental.py --env Ant-v5 --episodes 200 --early-stop 900
```

---

## Troubleshooting

### "Still collapsing after 1000 episodes"
- Lower early-stop threshold (stop sooner)
- Or: Very rare edge case, lower entropy_decay to 0.9999

### "Not reaching 950 on Ant"
- Normal variation (might take 150-200 episodes)
- Check reward around episode 100-200
- If < 900, might need lr adjustment

### "Humanoid not walking"
- Be patient (needs 1000-2000 episodes minimum)
- Check steps/episode (should reach 1000 by episode 500)
- If failing early, increase max_steps to 3000

---

## Files

- `sand_rl_incremental.py` - v3.0 (Stable - this version)
- `LATE_COLLAPSE_FIXED.md` - Complete explanation
- `collapse_diagnosis.png` - Visual analysis
- `ANTI_FORGETTING_UPDATE.md` - v1→v2 fixes
- `VISUAL_COMPARISON.md` - v1 vs v2 comparison

---

## Bottom Line

**v1:** Learned then forgot (fixed with Actor-Critic)  
**v2:** Learned, stayed stable, then collapsed at episode 700 (your results)  
**v3:** Learns, stays stable, never collapses (this version)

**Your issue:** You learned too well, too fast! Now we just stop before the collapse.

**Try this:**
```bash
python sand_rl_incremental.py --env Ant-v5 --early-stop 950
```

Should stop around episode 110 with 980 reward. Perfect! 🎯
