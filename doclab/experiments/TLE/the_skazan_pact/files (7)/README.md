# TLE Combat Runner v3.1 - Web Edition

## 🚀 Quick Start

### Option 1: Auto-Load from Codex (Recommended for 35+ characters)

1. **Generate your codex bundle:**
   ```bash
   python generate_codex.py
   ```
   This scans your directories and creates `codex.json`.

2. **Place files together:**
   ```
   your-session/
   ├── codex.json              ← Generated bundle
   └── tle_combat_runner.html  ← Combat runner
   ```

3. **Open `tle_combat_runner.html`** in your browser
   - It will auto-detect and load codex.json
   - All 35 characters will load instantly
   - Positions auto-assigned by side

### Option 2: Drag & Drop

Simply drag `codex.json` onto the combat runner interface.

---

## 📦 Codex Structure

The `codex.json` file has this structure:
```json
{
  "directories": {
    "initiative": {
      "player_001.json": { /* character data */ },
      "guard_01.json": { /* character data */ },
      ...
    },
    "spells": {
      "fireball.json": { /* spell data */ }
    },
    "items": {
      "health_potion.json": { /* item data */ }
    }
  }
}
```

---

## 🎮 Combat Commands

### Setup Phase
```bash
init              # Start combat (rolls initiative)
reload            # Clear and reload from codex
look              # View battlefield state
side <idx> <team> # Assign character to side
ai on/off <idx>   # Toggle AI control
```

### Combat Actions
```bash
attack 2 spend 8 buy 3        # Attack target 2 (8 base EP, 3 dice EP)
cast fireball 3 power 10      # Cast spell at target 3 (auto-range)
check 2.mask_identity         # Skill check on target 2
move 500 400 50               # Move to (x, y, z)
talk 2 wis                    # Conversation check vs target 2
use potion on 1               # Use item on target
pass / end                    # End turn
```

---

## 🗺️ Auto-Positioning

Characters without x/y coordinates get **automatic battlefield placement by side**:

| Side       | Zone                  | Color  |
|------------|-----------------------|--------|
| `players`  | Left side (0-30%)     | Cyan   |
| `raiders`  | Right side (70-100%)  | Red    |
| `guards`   | Right side (70-100%)  | Orange |
| `neutral`  | Center (40-60%)       | Gray   |

All characters start at **z=0** (ground level). Use `move` to adjust.

---

## 🎯 Features Integrated

✅ **Spellcasting** - Range cost (1 EP = 5 ft), TLE-001 accuracy  
✅ **Dice Buy** - Entropy gambling with fizzle (roll ≤1 = fail)  
✅ **Check System** - DC-based field revelation  
✅ **AI Targeting** - Weakest/strongest/closest strategies  
✅ **Social System** - Conversation, hostility shifts  
✅ **Damage Channels** - Wound routing (cut, pierce, thermal, etc.)  
✅ **3D Positioning** - Full X, Y, Z coordinate tracking  
✅ **HP/EP Bars** - Live health/energy display  
✅ **Initiative Tracker** - Real-time turn queue  

---

## 🔧 Character JSON Requirements

Minimum required fields for auto-loading:
```json
{
  "id": "guard_01",
  "name": "Temple Guard",
  "side": "guards",
  "player": false,
  "pools": {
    "HP": 20,
    "max_HP": 20,
    "EP": 15,
    "max_EP": 15
  },
  "stats": {
    "str": 14,
    "dex": 12,
    "con": 16,
    "int": 8,
    "wis": 10,
    "TEP": 12
  }
}
```

Optional fields:
- `position`: `{x: 300, y: 400, z: 0}` - Manual placement
- `color`: `"#ff0000"` - Custom display color
- `size`: `20` - Character size on map
- `spells`: `["fireball", "shield"]` - Available spells
- `inventory`: `["sword", "potion"]` - Items
- `hostility`: `"hostile"/"neutral"/"friendly"`
- `ai_enabled`: `true/false` - AI control

---

## 🐛 Troubleshooting

**Codex won't load?**
- Ensure `codex.json` is in same folder as HTML
- Check browser console (F12) for errors
- Try drag-and-drop method instead

**Characters appear as dots?**
- Check `size` field exists
- Verify `color` is set (or will use side default)

**AI not acting?**
- Verify `ai_enabled: true` in character JSON
- Check character is on different side than targets
- Ensure character has EP > 0

**HP/EP bars wrong?**
- Check `max_HP` and `max_EP` fields exist
- `generate_codex.py` sanitizes data automatically

---

## 📝 Example Session Workflow

```bash
# 1. Generate codex from your initiative folder
python generate_codex.py

# 2. Open tle_combat_runner.html
# → Auto-loads all 35 characters
# → Shows battlefield roster by side

# 3. Start combat
>> init

# 4. Play turns
>> attack 5 spend 10 buy 2
>> cast lightning_bolt 3 power 8
>> move 600 400
>> pass

# 5. End session
# → Character states auto-saved in memory
# → Can reload with: reload
```

---

## 🔄 Python Fallback

Keep `combat_runner.py` as backup:
- More detailed logging
- File persistence
- Advanced debugging

Web runner is optimized for:
- Fast visual feedback
- Real-time battlefield view
- Quick playtesting

---

## 📊 Performance

- ✅ Tested with 35+ characters
- ✅ Smooth rendering at 60fps
- ✅ Instant initiative calculation
- ✅ Sub-second codex loading

---

## 🎨 Customization

Edit CSS variables in HTML `<style>` section:
```css
:root {
    --bg: #050505;      /* Background */
    --term: #33ff33;    /* Terminal green */
    --cyan: #00ffff;    /* Highlights */
    --alert: #ff3333;   /* Errors/damage */
    --gold: #ffcc00;    /* Crits/special */
}
```

---

Made with ⚡ for the Pirouette Framework  
Compatible with TLE combat system modules
