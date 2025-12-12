# HP/EP Calculation Fix - Quick Guide

## 🔧 The Issue

Characters were showing **per-level HP/EP values** (e.g., 10 HP) instead of **total values** (e.g., 160 HP for level 16 character).

Example:
- **Before:** City Guard shows 10/10 HP (per-level value)
- **After:** City Guard shows 160/160 HP (10 HP × level 16)

---

## ✅ The Fix

### Updated Files:
1. **tle_combat_runner.html** - Now calculates totals from `pools_profile` + `level`
2. **generate_codex.py** - Pre-calculates values when generating codex
3. **validate_codex.py** - Checks calculation accuracy

---

## 🚀 How to Apply

### Option 1: Regenerate Codex (Recommended)
```bash
# Regenerate with fixed calculation
python generate_codex.py

# Validate calculations
python validate_codex.py

# Reload in browser
>> reload
```

The codex generator now **pre-calculates** HP/EP totals, so the web runner loads correct values immediately.

### Option 2: Just Reload
If you already have `codex.json`, the web runner will now calculate correctly on load:
```bash
# In browser
>> reload
```

---

## 📊 How It Works

### Character JSON Structure:
```json
{
  "id": "city_guard_01",
  "name": "City Guard (Rookie)",
  "level": 16,
  "pools_profile": {
    "HP_per_level": [10],
    "ENT_per_level": [10]
  }
}
```

### Calculation:
```
Total HP = Average(HP_per_level) × level
         = 10 × 16
         = 160 HP

Total EP = Average(ENT_per_level) × level
         = 10 × 16
         = 160 EP
```

### After Processing:
```json
{
  "pools": {
    "HP": 160,
    "max_HP": 160,
    "EP": 160,
    "max_EP": 160
  }
}
```

---

## 🔍 Validation

Run the validator to check calculations:
```bash
python validate_codex.py
```

**Expected Output:**
```
✓ Loaded: codex.json

Checking initiative/...
  ℹ city_guard_01: No pools.max_HP - will calculate as 160
  ✓ 35 entries

✓ No issues found - codex is clean!
```

If you see **"HP mismatch"** warnings, regenerate the codex.

---

## 🎮 Verifying in Browser

After reloading, check the battlefield:

```bash
>> look

[1] City Guard (Rookie) | guards | HP 160/160 | EP 160/160
[2] Raider Grunt | raiders | HP 176/176 | EP 176/176
...
```

HP/EP bars on the battlefield should now show accurate percentages!

---

## 🧮 Examples

| Character | Level | HP/Level | Total HP |
|-----------|-------|----------|----------|
| City Guard (Rookie) | 16 | 10 | **160** |
| Raider Grunt | 16 | 11 | **176** |
| City Guard (Veteran) | 18 | 10 | **180** |
| Player Drifter | 12 | 12 | **144** |

---

## 🐛 Troubleshooting

### Still Seeing 10/10 HP?

**Check 1:** Does character have `level` field?
```bash
python validate_codex.py
# Look for "Missing 'level'" warnings
```

**Check 2:** Does character have `pools_profile`?
```json
{
  "pools_profile": {
    "HP_per_level": [10],
    "ENT_per_level": [10]
  }
}
```

**Check 3:** Regenerated codex?
```bash
python generate_codex.py
>> reload
```

### Characters with Direct HP Values

Some NPCs might have direct values instead:
```json
{
  "combat": {
    "hp": 160
  },
  "ep": {
    "max": 160
  }
}
```

These work correctly without calculation.

---

## 📝 Character Format Support

The system now supports **three formats**:

### Format 1: Level-Based (Players)
```json
{
  "level": 16,
  "pools_profile": {
    "HP_per_level": [10, 12],  // Range or single value
    "ENT_per_level": [10]
  }
}
```
**Calculation:** Average × Level

### Format 2: Direct Pools
```json
{
  "pools": {
    "HP": 160,
    "max_HP": 160,
    "EP": 160,
    "max_EP": 160
  }
}
```
**No calculation needed**

### Format 3: Combat/EP Structure (NPCs)
```json
{
  "combat": { "hp": 160 },
  "ep": { "max": 160 }
}
```
**Converted to pools format**

---

## ✨ Benefits

✅ **Accurate HP/EP display** on battlefield  
✅ **Correct HP bars** (visual percentage)  
✅ **Proper damage calculations**  
✅ **Initiative tracker** shows real HP  
✅ **Pre-calculated** in codex (faster loading)  

---

## 🎯 Quick Checklist

- [ ] Updated HTML file
- [ ] Updated generate_codex.py
- [ ] Regenerated codex: `python generate_codex.py`
- [ ] Validated: `python validate_codex.py`
- [ ] Reloaded in browser: `>> reload`
- [ ] Checked with `>> look`
- [ ] Verified HP bars on battlefield

---

**Done! Your characters should now show their full HP/EP values!** 🎉
