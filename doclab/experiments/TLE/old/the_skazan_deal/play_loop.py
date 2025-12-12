# story_runner_v2_map.py: adds a visual renderer that produces per-round PNGs and an animated GIF.
from pathlib import Path
import json, random, datetime, argparse, math, os
from PIL import Image, ImageDraw, ImageFont, ImageOps

BASE = Path(".")
LOGS = BASE / "logs"
INIT = BASE / "initiative"
ROSTER = BASE / "roster"
IMAGES = BASE / "images"
VIS = BASE / "vis"
for d in (LOGS, INIT, ROSTER, IMAGES, VIS):
    d.mkdir(exist_ok=True)

WORLD_PATH = BASE / "world.json"
WORLD = json.loads(WORLD_PATH.read_text()) if WORLD_PATH.exists() else {
    "name": "Unnamed World",
    "grid_scale_ft": 5,
    "rules": {"tn_base": 8, "range_per_ep_ft": 5, "ante": {"enabled": True}, "environment": {"corruption_per_2_ep": True}},
}

# -------------- Core mechanics (copied + minimal augment from v2) --------------
def load_char(fp):
    j = json.loads(Path(fp).read_text())
    j.setdefault("position", {"x": 0, "y": 0})
    j["_alive"] = j["pools"]["HP"] > 0
    j["_err"] = j["stats"]["ERR"]
    j["_spoken"] = False
    j["_max_hp"] = j["pools"]["HP"]
    return j

def roll_d20():
    return random.randint(1, 20)

def tn_from_ep(ep): 
    return WORLD["rules"]["tn_base"] + (ep // 2)

def atk_total(j, die): 
    return die + (j["stats"]["DEX"] // 4) + (j["stats"]["INT"] // 4)

def choose_target(ch, others):
    enemies = [o for o in others if o["side"] != ch["side"] and o["_alive"]]
    if not enemies: return None
    enemies.sort(key=lambda o: (o["pools"]["HP"], o["pools"]["AEP"]))
    return enemies[0]

def distance(a, b):
    dx = b["position"]["x"] - a["position"]["x"]
    dy = b["position"]["y"] - a["position"]["y"]
    return math.sqrt(dx*dx + dy*dy)

def step_toward(a, b, squares=1):
    if not b: return a["position"]
    ax, ay = a["position"]["x"], a["position"]["y"]
    bx, by = b["position"]["x"], b["position"]["y"]
    dx, dy = bx - ax, by - ay
    if dx == 0 and dy == 0:
        return {"x": ax, "y": ay}
    mag = math.sqrt(dx*dx + dy*dy)
    ux, uy = dx / mag, dy / mag
    nx = ax + int(round(ux * squares))
    ny = ay + int(round(uy * squares))
    return {"x": nx, "y": ny}

# -------------- Timeline capture --------------
def snapshot(order, round_i, action_note):
    # capture lightweight positions and HP for visualization
    return {
        "round": round_i,
        "note": action_note,
        "actors": [
            {
                "id": ch["id"],
                "name": ch["name"],
                "side": ch["side"],
                "hp": ch["pools"]["HP"],
                "aep": ch["pools"]["AEP"],
                "alive": ch["_alive"],
                "x": ch["position"]["x"],
                "y": ch["position"]["y"],
            }
            for ch in order
        ],
    }

def run_and_capture(seed=42, max_rounds=10):
    random.seed(seed)
    files = sorted(INIT.glob("*.json"))
    if not files:
        # bootstrap sample if present
        for fname in ["pilgrim-001.json", "wolf-001.json"]:
            src = BASE / fname
            if src.exists():
                (INIT / fname).write_text(src.read_text())
        files = sorted(INIT.glob("*.json"))
    order = [load_char(fp) for fp in files]
    # initiative
    order = sorted(order, key=lambda c: -(random.randint(1,20) + c["stats"].get("init_bonus",0) + (c["stats"]["DEX"]//4)))
    timeline = []
    timeline.append(snapshot(order, 0, "Setup / Initiative"))

    rnd = 1
    while rnd <= max_rounds:
        for ch in order:
            if ch["_alive"]:
                ch["_err"] = ch["stats"]["ERR"]
                ch["_spoken"] = False
        timeline.append(snapshot(order, rnd, f"Round {rnd} begins"))

        for ch in order:
            if not ch["_alive"]:
                continue
            others = [o for o in order if o["id"] != ch["id"]]
            if ch["_err"] <= 0:
                timeline.append(snapshot(order, rnd, f"{ch['name']} pauses (no ERR)"))
                continue

            # talk chance
            tactics = ch.get("persona", {}).get("tactics", [])
            arche = ch.get("persona", {}).get("archetype", "")
            will_talk = ("talk_first" in tactics or arche == "parleyist") and not ch["_spoken"] and random.random() < 0.5
            if will_talk:
                ch["_spoken"] = True
                timeline.append(snapshot(order, rnd, f"{ch['name']} speaks"))
                continue

            tgt = choose_target(ch, others)
            aggressive = (arche == "intrepid")
            ep_spend = max(1, min(ch["_err"], ch["_err"] if aggressive else 3))

            # 25% reposition
            if random.random() < 0.25 and tgt:
                old = (ch["position"]["x"], ch["position"]["y"])
                squares = min(ep_spend, 4)
                newpos = step_toward(ch, tgt, squares=squares)
                ch["position"] = {"x": newpos["x"], "y": newpos["y"]}
                ch["_err"] -= squares
                timeline.append(snapshot(order, rnd, f"{ch['name']} moves {squares} sq toward {tgt['name']}"))
                continue

            # attack
            ch["_err"] -= ep_spend
            tn = tn_from_ep(ep_spend)
            d20 = roll_d20()
            total = atk_total(ch, d20)

            if not tgt or not tgt["_alive"]:
                timeline.append(snapshot(order, rnd, f"{ch['name']} attacks but no target"))
                continue

            defend = min(ep_spend, max(0, tgt["_err"] // 2))
            tgt["_err"] -= defend
            dmg = max(0, ep_spend - defend)
            soak = min(dmg, tgt["pools"]["AEP"])
            tgt["pools"]["AEP"] -= soak
            dmg -= soak
            if total >= tn:
                tgt["pools"]["HP"] -= dmg
                if tgt["pools"]["HP"] <= 0:
                    tgt["_alive"] = False

            timeline.append(snapshot(order, rnd, f"{ch['name']} attacks {tgt['name']} (d20 {d20} vs TN {tn})"))
        # end condition
        alive_sides = set([ch["side"] for ch in order if ch["_alive"]])
        if len(alive_sides) <= 1:
            timeline.append(snapshot(order, rnd, "Encounter ends"))
            break
        rnd += 1

    return order, timeline

# -------------- Visual compositor --------------
def find_token_image(ch):
    # try images/{id}.png then images/{name}.png (slug-ish)
    cand = [
        IMAGES / f"{ch['id']}.png",
        IMAGES / f"{ch['name'].lower().replace(' ','_')}.png",
    ]
    for c in cand:
        if c.exists():
            return Image.open(c).convert("RGBA")
    return None

def initials(name):
    parts = [p for p in name.split() if p]
    if not parts: return "??"
    if len(parts) == 1: return parts[0][:2].upper()
    return (parts[0][0] + parts[-1][0]).upper()

def compute_bounds(timeline):
    xs, ys = [], []
    for snap in timeline:
        for a in snap["actors"]:
            xs.append(a["x"]); ys.append(a["y"])
    if not xs:
        return (-5, 5, -5, 5)
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    # pad
    return (xmin-2, xmax+2, ymin-2, ymax+2)

def render_timeline(timeline, outdir: Path, cell_px=64):
    outdir.mkdir(parents=True, exist_ok=True)
    # background
    bg_path = IMAGES / "background.png"
    bounds = compute_bounds(timeline)
    width_cells = max(8, bounds[1]-bounds[0]+1)
    height_cells = max(6, bounds[3]-bounds[2]+1)
    W, H = width_cells*cell_px, height_cells*cell_px

    if bg_path.exists():
        bg = Image.open(bg_path).convert("RGBA").resize((W, H))
    else:
        # draw a neutral grid
        bg = Image.new("RGBA", (W, H), (245, 245, 245, 255))
        draw = ImageDraw.Draw(bg)
        for x in range(0, W, cell_px):
            draw.line([(x,0),(x,H)], fill=(200,200,200,255), width=1)
        for y in range(0, H, cell_px):
            draw.line([(0,y),(W,y)], fill=(200,200,200,255), width=1)

    # load fonts (fallback if none)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 20)
    except:
        font = ImageFont.load_default()

    # pre-cache token images
    token_cache = {}

    frames = []
    for idx, snap in enumerate(timeline):
        frame = bg.copy()
        draw = ImageDraw.Draw(frame)

        # title
        title = f"{WORLD.get('name','World')} — {snap['note']}"
        draw.rectangle([(0,0),(W,30)], fill=(0,0,0,160))
        draw.text((8,6), title, font=font, fill=(255,255,255,255))

        for a in snap["actors"]:
            # convert grid to pixel
            gx = a["x"] - bounds[0]
            gy = a["y"] - bounds[2]
            px = gx*cell_px + cell_px//2
            py = gy*cell_px + cell_px//2

            # token image or fallback
            key = a["id"]
            if key not in token_cache:
                token_cache[key] = find_token_image(a)  # returns PIL or None
            token = token_cache[key]
            if token is not None:
                token_r = token.resize((int(cell_px*0.9), int(cell_px*0.9)))
            else:
                # simple disc with initials
                token_r = Image.new("RGBA", (int(cell_px*0.9), int(cell_px*0.9)), (0,0,0,0))
                dd = ImageDraw.Draw(token_r)
                r = token_r.size[0]//2
                fill = (60,60,60,230) if a["side"] == "foe" else (20,20,20,230)
                dd.ellipse([(0,0),(2*r,2*r)], fill=fill)
                txt = initials(a["name"])
                tw, th = dd.textlength(txt, font=font), font.size
                dd.text((r - tw/2, r - th/2), txt, font=font, fill=(255,255,255,255))

            # health ring
            ring = Image.new("RGBA", token_r.size, (0,0,0,0))
            rr = ImageDraw.Draw(ring)
            hp = max(0, a["hp"])
            max_hp = 1 if a["hp"]<=0 else max(a["hp"], 1)  # without max in data, scale by current
            # if alive we show a thin ring; if dead, cross out
            if a["alive"]:
                rr.ellipse([(0,0),(token_r.size[0]-1, token_r.size[1]-1)], outline=(255,255,255,180), width=2)
            else:
                rr.line([(0,0),(token_r.size[0], token_r.size[1])], fill=(255,0,0,200), width=3)
                rr.line([(0,token_r.size[1]),(token_r.size[0],0)], fill=(255,0,0,200), width=3)

            # paste token centered
            x0 = int(px - token_r.size[0]/2)
            y0 = int(py - token_r.size[1]/2)
            frame.alpha_composite(token_r, (x0,y0))
            frame.alpha_composite(ring, (x0,y0))

            # label
            label = f"{a['name']} ({a['hp']} HP)"
            draw.text((x0, y0 + token_r.size[1] + 2), label, font=font, fill=(0,0,0,255))

        frames.append(frame)

    # save frames and animated GIF
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    frame_dir = outdir / f"frames_{stamp}"
    frame_dir.mkdir(parents=True, exist_ok=True)
    out_gif = outdir / f"encounter_{stamp}.gif"

    for i, fr in enumerate(frames):
        fp = frame_dir / f"frame_{i:03d}.png"
        fr.save(fp)

    # animated GIF (optimize size)
    if frames:
        frames[0].save(out_gif, save_all=True, append_images=frames[1:], duration=700, loop=0, optimize=False, disposal=2)

    return str(frame_dir), (str(out_gif) if frames else None)

# -------------- Runner --------------
if __name__ == "__main__":
    order, timeline = run_and_capture(seed=42, max_rounds=10)
    fdir, gif = render_timeline(timeline, VIS)
    print("Frames directory:", fdir)
    print("Animated GIF:", gif)
