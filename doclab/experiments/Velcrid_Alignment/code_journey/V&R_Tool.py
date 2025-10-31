import os
import re
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ---- Paths ----
BASE_DIR = "C:/Users/keatw/OneDrive/Documents/Doclab/Big_Datasets/target/paper/Pirouette_Volume_5/doclab/experiments/Velcrid_Alignment"
RADIANT_DIR = os.path.join(BASE_DIR, "radiant")
VELCRID_DIR = os.path.join(BASE_DIR, "velcrid")

# ---- Simple HTML → text stripper ----
TAG_RE = re.compile(r"<[^>]+>")

def strip_html(raw: str) -> str:
    return TAG_RE.sub("", raw)

# ---- Load Semantic Engine & Velcrid scorer ----
from semantic_test_engine_2 import SemanticDistillator as _Engine
from velcridance_score_module import VelcridanceScorer

engine = _Engine()
v_scorer = VelcridanceScorer()

def radiance_score(text: str, flips: int = 10, grid_size: int = 64) -> float:
    """
    Mirror of Velcrid scorer but returns avg_delta (higher = more flexible).
    """
    base_pattern = engine.text_to_binary_image(text, grid_size, grid_size)
    base_power = engine.run_simulation(base_pattern)
    pattern_flat = base_pattern.flatten()

    deltas = []
    rng = np.random.default_rng(seed=42)
    for _ in range(flips):
        idx = rng.choice(len(pattern_flat))
        variant = pattern_flat.copy()
        variant[idx] = 1 - variant[idx]
        fp = engine.run_simulation(variant.reshape(grid_size, grid_size))
        deltas.append(abs(base_power - fp["total_power"]))
    return float(np.mean(deltas))

# ---- Harvest files ----
records = []
for label, folder in [("radiant", RADIANT_DIR), ("velcrid", VELCRID_DIR)]:
    if not os.path.isdir(folder):
        print(f"Missing directory: {folder}")
        continue
    for fname in os.listdir(folder):
        path = os.path.join(folder, fname)
        if not os.path.isfile(path):
            continue
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                raw = f.read()
        except Exception as e:
            print(f"Could not read {path}: {e}")
            continue
        # crude HTML detection
        content = strip_html(raw) if "<html" in raw[:500].lower() or "</" in raw[:1000] else raw
        text = re.sub(r"\s+", " ", content).strip()
        if len(text) < 500:  # skip too-short files
            continue

        # compute scores
        try:
            v_val = v_scorer.compute_v_score(text)
            r_val = radiance_score(text)
        except Exception as e:
            print(f"Scoring error for {fname}: {e}")
            continue

        records.append({
            "file": fname,
            "label": label,
            "R_score": r_val,
            "V_score": v_val,
            "chars": len(text)
        })

df = pd.DataFrame(records)

# ---- Simple scatter plot ----
plt.figure(figsize=(8,6))
for lbl in df["label"].unique():
    subset = df[df["label"] == lbl]
    plt.scatter(subset["R_score"], subset["V_score"], label=lbl)
plt.xlabel("Radiance (flexibility) score")
plt.ylabel("Velcridance (rigidity) score")
plt.title("R vs V across pilot corpus")
plt.legend()
plot_path = "/mnt/data/rv_scatter.png"
plt.tight_layout()
plt.savefig(plot_path, dpi=150)
print(f"Plot saved to {plot_path}")
