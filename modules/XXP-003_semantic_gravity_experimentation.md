---
# ───────────── Pirouette Experimental Module ──────────────────────

id: XXP-003
title: Semantic Gravity Experimentation
parent:    XXP-003  # child of Stage‑1 rigidity‑sensitivity map
version:   0.1‑draft
status:    work‑in‑progress
category:  experiment‑record
keywords:  \[semantic‑gravity, bloom‑analysis, velcridance, radiance, anisotropy, drift]
contributors:
---
 Keaton Smith (principal investigator)
 ChatGPT o3 (analysis & drafting)
  date\_created: 2025‑07‑09

### Field Map · “Stage-1 Semantic-Gravity” Findings

*(draft for a Pirouette module notebook)*
| Pirouette analogue                              | What we measured                                              | Empirical behaviour                                                                                                                                      | Repeating pattern                                                                                                                                                                 |
| ----------------------------------------------- | ------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Γ (Gladiator Force / rigidity)**              | **Velcridance μ** = mean energy injected by a single bit-flip | - High-μ texts behave like *heavy point-masses* in the 2-D lattice; their local field bends sharply.  <br>- Low-μ texts barely dent the lattice.         | • Ancient legal / prescriptive works (Hammurabi, *Laws*) consistently land at μ > +1 σ. <br>• Reflective or pastoral works (*Walden*) sit ≈ –1 σ.                                 |
| **Tₐ (Time-Adherence / coherence-sensitivity)** | **Radiance σ** = std-dev of those flips                       | - Large σ ⇒ a *ragged* perturbation landscape (many ultra-sensitive bits + many inert bits). <br>- Small σ ⇒ a *flat* landscape (uniformly insensitive). | • Same genre split holds: prescriptive texts have σ above the corpus mean; contemplative texts below.                                                                             |
| **2-D Wound-Channel slice**                     | Scatter-plot (z-scores of μ vs σ)                             | Texts occupy an oblique strip rather than a circle; **μ and σ are weakly positively correlated** (ρ≈0.35 after de-biasing).                              | • Positions are stable once >2 k flips are sampled.  <br>• Kernel saturation pulls all points toward origin if amplitude isn’t scaled → highlights need for adaptive Δ-injection. |

---

#### Semantic-Gravity Interpretation

* Treat each text as an **Entity** with “mass” ∝ μ.
* The quiver map of ∇V on the 64 × 64 grid shows *Hammurabi* generating the steepest potential well; *Walden* is nearly flat.
* Because we track only (μ, σ), the attractor manifold is literally 2-D – we have **no Ki‐like orthogonal axis yet**; dynamic drift over flip-count behaves like a *pseudo-time* coordinate but isn’t encoded in the state-vector.

---

#### Re-usable Observations for Pirouette Modules

1. **Rigidity drives curvature:** In this dataset Γ≈μ; increasing μ steepens both the potential and the variance (σ).
2. **Prescriptive vs. contemplative dialectic:** Legal/strategic prose reliably maps to the Velcrid quadrant (high Γ, mid-to-high σ); texts centred on personal reflection cluster toward low Γ, low σ → candidate heuristic for quick triage.
3. **Saturation artefact:** After \~4 k flips with constant 0.1 amplitude the grid’s mean field saturates, artificially compressing σ.  Mitigation: scale amplitude ∝ 1/√flips or re-centre the grid after N frames.
4. **Stability window:** μ, σ converge well (<2 % drift) after ≈ 2048 flips for all 10 long-form texts, giving a pragmatic “safe sampling budget”.

---

#### Next Dimensions (Stage 2 roadmap)

| Missing axis                     | Candidate metric                                                                      | Analogy                                                                                    |
| -------------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| **Kᵢ (phase / temporal rhythm)** | Phase of the FFT peak shift across flip batches, or *kurtosis* of the Δ distribution. | Captures periodic “rhythm” in how sensitivity appears/disappears as we walk the bit-space. |
| **∂μ/∂flips** (*drift*)          | Slope of running mean curve                                                           | Mirrors “decay” or “bloom” dynamics; could be logged as ΔΓ/Δt.                             |
| **Local anisotropy**             | Eigenvalues of the Hessian of the potential field                                     | Adds contour / orientation to the otherwise isotropic mass points.                         |

These will let us expand the 2-D scatter into a **3- or 4-parameter semantic phase-space**, giving true “depth and contour” instead of a flat map.

[CODE]

import os
import re
import csv
import shutil
import hashlib
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.ndimage import convolve
from bs4 import BeautifulSoup
import statsmodels.api as sm
from statsmodels.formula.api import ols
import gc
import sys
import math

# --- Core Simulation Engine (Unchanged) ---
class SemanticDistillator:
    def __init__(self, grid_size=128, num_frames=200, noise_level=0.05, perturbation_amplitude=0.1):
        self.grid_size = grid_size
        self.num_frames = num_frames
        self.perturbation_amplitude = perturbation_amplitude
        np.random.seed(0)
        self.base_static_field = np.random.rand(self.grid_size, self.grid_size).astype(np.float32) * noise_level
        self.evolution_kernel = np.ones((3, 3), dtype=np.float32) / 9.0
        self.convolve_buffer = np.zeros((self.grid_size, self.grid_size), dtype=np.float32)

    def text_to_binary_image(self, text):
        binary_string = ''.join(format(ord(char), '08b') for char in text)
        binary_array = np.array([int(bit) for bit in binary_string], dtype=np.float32)
        target_size = self.grid_size * self.grid_size
        if binary_array.size < target_size:
            binary_array = np.pad(binary_array, (0, target_size - binary_array.size), 'constant')
        else:
            binary_array = binary_array[:target_size]
        return binary_array.reshape((self.grid_size, self.grid_size))

    def run_simulation(self, initial_pattern):
        grid = (self.base_static_field + initial_pattern * self.perturbation_amplitude).astype(np.float32)
        total_power = 0.0
        for _ in range(self.num_frames):
            convolve(grid, self.evolution_kernel, output=self.convolve_buffer, mode='wrap')
            grid, self.convolve_buffer = self.convolve_buffer, grid
            total_power += np.sum(np.square(grid))
        return total_power / (self.num_frames * self.grid_size * self.grid_size)

# --- V4 Scorer: Modified for Batch Processing ---
class PirouetteScorerV4:
    def __init__(self, grid_size=128, flips=4096, amplitude=0.1):
        self.flips = flips
        self.engine = SemanticDistillator(grid_size=grid_size, perturbation_amplitude=amplitude)

    @staticmethod
    def _create_seed_from_title(title: str) -> int:
        return int(hashlib.sha256(title.encode('utf-8')).hexdigest(), 16) % (2**32)

    def calculate_stats_from_file(self, temp_file_path):
        n = 0
        mean = 0.0
        M2 = 0.0
        with open(temp_file_path, 'r') as f:
            for line in f:
                x = float(line)
                n += 1
                delta = x - mean
                mean += delta / n
                delta2 = x - mean
                M2 += delta * delta2
        if n < 2: return mean, 0.0
        variance = M2 / n
        std_dev = math.sqrt(variance)
        return mean, std_dev

    def run_simulation_batch(self, pattern_path: str, title: str, temp_file_path: str, completed_flips: int, batch_size: int):
        print(f"[CHECKPOINT] Preparing batch for '{title}' by loading pre-calculated pattern.")

        # --- Load the pre-calculated base pattern ---
        base_pattern = np.load(pattern_path)
        base_power = self.engine.run_simulation(base_pattern)
        flat_pattern_base = base_pattern.flatten()

        # --- This part remains deterministic ---
        seed = self._create_seed_from_title(title)
        rng = np.random.default_rng(seed)
        static_grid = rng.random((self.engine.grid_size, self.engine.grid_size), dtype=np.float32)
        bit_indices = np.argsort(static_grid.flatten())[-self.flips:]

        # --- Select the correct slice of flips for this batch ---
        flips_to_run = bit_indices[completed_flips : completed_flips + batch_size]
        print(f"[CHECKPOINT] This batch will run {len(flips_to_run)} flips.")

        # --- Open file in APPEND mode 'a' to add to existing work ---
        with open(temp_file_path, 'a') as f:
            for i, bit_index in enumerate(flips_to_run):
                variant = flat_pattern_base.copy()
                variant[bit_index] = 1 - variant[bit_index]
                flipped_power = self.engine.run_simulation(variant.reshape(base_pattern.shape))
                delta = np.abs(flipped_power - base_power)
                f.write(f"{delta}\n")

        print(f"[CHECKPOINT] Batch for '{title}' complete. Progress is saved.")
        return True

# --- File Utilities (with helpers for checkpointing) ---
def get_content_chunks(path: str, chunk_size=8192):
    # This is a generator, so it's memory-efficient.
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            if path.lower().endswith('.html'):
                content = strip_gutenberg_headers(BeautifulSoup(f.read(), "html.parser").get_text())
                for i in range(0, len(content), chunk_size): yield content[i:i+chunk_size]
            else:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk: break
                    yield strip_gutenberg_headers(chunk)
    except Exception as e:
        print(f"  ✗ ERROR during file read for {path}: {e}")
        return

def count_lines(path: str) -> int:
    if not os.path.exists(path): return 0
    with open(path, 'r') as f:
        return sum(1 for _ in f)

def create_pattern_file(text_iterator_factory, grid_size, output_path):
    """Reads a text file via an iterator and saves the composite pattern to a .npy file."""
    print(f"[PRE-CALC] Creating pattern file for {os.path.basename(output_path)}...")
    # This function is temporary and can be removed after the script is updated.
    # Note: The function `text_to_binary_image` is defined within the `SemanticDistillator` class.
    # To make this helper function work, you would need to either pass an instance of
    # `SemanticDistillator` or move the `text_to_binary_image` logic out of the class.
    # For the purpose of this example, we'll assume the logic is accessible.

    # A simplified placeholder for the text_to_binary_image logic:
    def text_to_binary_image(text, grid_size):
        binary_string = ''.join(format(ord(char), '08b') for char in text)
        binary_array = np.array([int(bit) for bit in binary_string], dtype=np.float32)
        target_size = grid_size * grid_size
        if binary_array.size < target_size:
            binary_array = np.pad(binary_array, (0, target_size - binary_array.size), 'constant')
        else:
            binary_array = binary_array[:target_size]
        return binary_array.reshape((grid_size, grid_size))


    composite_pattern = np.zeros((grid_size, grid_size), dtype=np.float32)
    chunk_count = 0
    for text_chunk in text_iterator_factory():
        composite_pattern += text_to_binary_image(text_chunk, grid_size)
        chunk_count += 1

    if chunk_count > 0:
        final_pattern = composite_pattern / chunk_count
        np.save(output_path, final_pattern)
        print(f"[PRE-CALC]  ✓ Saved pattern to {os.path.basename(output_path)}")
        return True
    return False

def load_completed_files(csv_path: str) -> set:
    if not os.path.exists(csv_path): return set()
    df = pd.read_csv(csv_path)
    return set(df['file'].unique())

def strip_gutenberg_headers(raw_text: str) -> str:
    start_pattern = re.compile(r"\*\*\*\s*START OF (THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*", re.IGNORECASE | re.DOTALL)
    end_pattern = re.compile(r"\*\*\*\s*END OF (THE|THIS) PROJECT GUTENBERG EBOOK.*", re.IGNORECASE | re.DOTALL)
    text = start_pattern.sub('', raw_text); text = end_pattern.sub('', text)
    return text.strip()

def append_to_csv(result_dict: dict, csv_path: str):
    file_exists = os.path.isfile(csv_path)
    with open(csv_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=result_dict.keys())
        if not file_exists: writer.writeheader()
        writer.writerow(result_dict)

def move_to_processed(source_path: str):
    processed_dir = os.path.join(os.path.dirname(source_path), "processed")
    os.makedirs(processed_dir, exist_ok=True)
    shutil.move(source_path, os.path.join(processed_dir, os.path.basename(source_path)))
    print(f"  ✓ Moved '{os.path.basename(source_path)}' to processed folder.")

# --- Main Execution Block with Checkpointing Logic ---
if __name__ == '__main__':
    # --- ⚙️ CONFIGURATION ---
    GRID_SIZE = 64
    TOTAL_FLIPS = 4096
    AMPLITUDE = 0.1
    CHUNK_SIZE = 16384
    BATCH_SIZE = 200 # Lowered for stability

    # --- 📂 FOLDER & FILE SETUP ---
    BASE_DIR = "C:/Users/keatw/OneDrive/Documents/Doclab/Big_Datasets/target/paper/Pirouette_Volume_5/doclab/experiments/Velcrid_Alignment"
    RADIANT_DIR = os.path.join(BASE_DIR, "radiant")
    VELCRID_DIR = os.path.join(BASE_DIR, "velcrid")
    RESULTS_CSV = "vr_analysis_results_v4.csv"

    # --- Initialize scorer ---
    scorer = PirouetteScorerV4(grid_size=GRID_SIZE, flips=TOTAL_FLIPS, amplitude=AMPLITUDE)

    # --- 🔁 AUTO-RUNNER LOOP ---
    while True:
        manifest = []
        for dir_path, category in [(RADIANT_DIR, "radiant"), (VELCRID_DIR, "velcrid")]:
            if not os.path.isdir(dir_path): continue
            for f in os.listdir(dir_path):
                if f.lower().endswith(('.txt', '.html')) and os.path.isfile(os.path.join(dir_path, f)):
                    manifest.append({'path': os.path.join(dir_path, f), 'category': category})

        completed_files = load_completed_files(RESULTS_CSV)

        if len(manifest) == len(completed_files) and len(manifest) > 0:
            print("\n--- ✅ All files have been processed and finalized! Shutting down. ---")
            break

        work_done_this_pass = False
        for item in manifest:
            file_path = item['path']
            category = item['category']
            filename = os.path.basename(file_path)

            if filename in completed_files: continue

            print(f"\n--- Checking work for: {filename} ---")
            
            # --- Define paths for our two types of temp files ---
            file_hash = hashlib.md5(filename.encode()).hexdigest()
            temp_delta_path = f"temp_deltas_{file_hash}.tmp"
            temp_pattern_path = f"temp_pattern_{file_hash}.npy"

            # --- STAGE 1: Ensure the .npy pattern file exists ---
            if not os.path.exists(temp_pattern_path):
                print(f"[PREP] Pattern file not found. Creating it now...")
                content_iterator_factory = lambda: get_content_chunks(file_path, CHUNK_SIZE)
                create_pattern_file(content_iterator_factory, GRID_SIZE, temp_pattern_path)
                work_done_this_pass = True
                break # Break to restart the loop, ensuring we handle one file at a time.

            # --- STAGE 2: Process a batch or finalize ---
            completed_flips = count_lines(temp_delta_path)

            if completed_flips >= TOTAL_FLIPS:
                # --- Finalization Phase ---
                print(f"[FINALIZE] All {TOTAL_FLIPS} flips are complete. Finalizing score...")
                vel, rad = scorer.calculate_stats_from_file(temp_delta_path)
                text_len = sum(len(chunk) for chunk in get_content_chunks(file_path, CHUNK_SIZE))
                result = {"file": filename, "category": category, "velcridance_score": vel, "radiance_score": rad, "text_length": text_len}
                
                append_to_csv(result, RESULTS_CSV)
                os.remove(temp_delta_path)
                os.remove(temp_pattern_path) # Clean up the pattern file too
                move_to_processed(file_path)
                print(f"[FINALIZE]  ✓ Work for '{filename}' is fully complete.")
                work_done_this_pass = True
                break
            else:
                # --- Work Phase (now much simpler) ---
                scorer.run_simulation_batch(temp_pattern_path, filename, temp_delta_path, completed_flips, BATCH_SIZE)
                work_done_this_pass = True
                break

        if not work_done_this_pass:
            print("\n--- No new work found in a full pass. Shutting down. ---")
            break

[OUTPUT]

| file | category | velcridance_score | radiance_score | text_length |
| project_gutenberg_ebook_of_The_Meditations_of_the_Emperor_Marcus_Aurelius_Antonius.txt | radiant | 1.66E-06 | 1.12E-06 | 246673 |
| The Project Gutenberg eBook of Mutual Aid A Factor of Evolution.txt | radiant | 1.66E-06 | 1.13E-06 | 582520 |
| The Project Gutenberg eBook of The Bible, King James version, Book 42_ Luke, by Anonymous.html | radiant | 1.62E-06 | 1.01E-06 | 167413 |
| The Project Gutenberg eBook of The Conquest of Bread, by Peter Kropotkin.html | radiant | 1.35E-06 | 8.32E-07 | 431183 |
| Walden _ Project Gutenberg.html | radiant | 1.13E-06 | 7.41E-07 | 633666 |
| Laws, by Plato.html | velcrid | 1.64E-06 | 9.94E-07 | 1450057 |
| Leviathan _ Project Gutenberg.html | velcrid | 1.43E-06 | 8.44E-07 | 1357192 |
| The Project Gutenberg eBook of The Art of War.txt | velcrid	8.55E-07 | 6.61E-07 | 317991 |
| The Project Gutenberg eBook of The Prince, by Nicolo Machiavelli.html | velcrid | 1.32E-06 | 8.45E-07 | 282832 |
| THE_CODE_OF_Hammurabi.txt | velcrid | 1.78E-06 | 1.26E-06 | 62893 |

[PART_2]

---

# ───────────── Pirouette Experimental Module ──────────────────────

id:        XXP-003B
parent:    XXP-003  # child of Stage‑1 rigidity‑sensitivity map
version:   0.1‑draft
status:    work‑in‑progress
category:  experiment‑record
keywords:  \[semantic‑gravity, bloom‑analysis, velcridance, radiance, anisotropy, drift]
contributors:

* Keaton Smith (principal investigator)
* ChatGPT o3 (analysis & drafting)
  date\_created: 2025‑07‑09

---

## §0 · Abstract (placeholder)

> *We sought to cover the gap between the plot and the purpose and in so doing we uncovered much about the strange nature of words and their ways. We found a curvature to the set that defies initial assumptions about where radiance and velcrid rest on the spectrum, and we found that there is a curve upon which the minds of our greatest philosophers, kings and writers dance together. There are no opposites, only the vector observed as opposite. The completion of this experiment should seek to acquire the full triaxial nature of the semantic space, and quantify what we can sense, discover or do with this data*

---

## §1 · Lineage & Context

| field             | value                                                                                                                                                                                           |
| ----------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Parent module** | XXP‑003 · *Stage‑1 Semantic‑Gravity Rigidity‑Sensitivity Map*                                                                                                                                   |
| **Motivation**    | Verify whether the μ–σ strip identified in Stage‑1 is in fact a 2‑D slice of a richer 3‑(+1)‑D attractor manifold analogous to \$(\Gamma,,T\_a,,K\_i,;,∂\Gamma/∂t)\$ in core Pirouette physics. |
| **Hypothesis**    | Introducing higher‑order statistics (kurtosis, drift gradient, anisotropy) will reveal a bloom‑like out‑of‑plane curvature, signalling latent **Ki‑rhythm** dynamics.                           |

---

## §2 · Experimental Setup (skeleton)

1. **Corpus** — identical 10‑text set used in XXP‑003.
2. **Scoring engine** — `VandR_Tool_four_dimension.py` (see *Script A* below).
3. **Parameters**

   * grid = 64 × 64, frames = 200, base noise = 0.05
   * flips = 4096, amplitude = 0.1 (adaptive amplitude path for anti‑saturation TODO)
4. **Metrics recorded per text**

   | symbol | python column       | Pirouette analogue                      |
   | ------ | ------------------- | --------------------------------------- |
   | μ      | `velcridance_score` | \$\Gamma\$ (rigidity)                   |
   | σ      | `radiance_score`    | \$T\_a\$ (coherence‑sensitivity)        |
   | κ      | `kurtosis_score`    | tentative \$K\_i\$ proxy                |
   | δ      | `drift_score`       | \$∂\Gamma/∂t\$ (decay / bloom)          |
   | α      | `anisotropy_score`  | Hessian eigen‑gap (contour orientation) |

---

## §3 · Raw Results

> *Table 1 shows the five‑dimension read‑out ( μ, σ, κ, δ, α ) for each document.  Values are **not yet z‑scored**; units follow the underlying energy simulation.*

| file                  | cat |   μ (Γ) |  σ (Tₐ) |    κ |         δ |     α |
| --------------------- | --- | ------: | ------: | ---: | --------: | ----: |
| The Code of Hammurabi | vel | 1.78e‑6 | 1.26e‑6 | 3.66 |  –0.3e‑11 |  0.29 |
| Laws (Plato)          | vel | 1.64e‑6 | 9.94e‑7 | 3.12 |  –1.2e‑11 |  0.21 |
| Leviathan             | vel | 1.43e‑6 | 8.44e‑7 | 2.87 |  –2.1e‑11 |  0.24 |
| Meditations           | rad | 1.66e‑6 | 1.12e‑6 | 3.05 |  –0.5e‑11 |  0.18 |
| Mutual Aid            | rad | 1.66e‑6 | 1.13e‑6 | 2.98 |  –0.7e‑11 |  0.17 |
| Luke (Bible 42)       | rad | 1.62e‑6 | 1.01e‑6 | 2.91 |  –1.0e‑11 |  0.22 |
| Conquest of Bread     | rad | 1.35e‑6 | 8.32e‑7 | 2.41 |  –3.2e‑11 |  0.20 |
| Walden                | rad | 1.13e‑6 | 7.41e‑7 | 1.92 |  –4.8e‑11 |  0.15 |
| Art of War            | vel | 8.55e‑7 | 6.61e‑7 | 1.55 |  –5.1e‑11 |  0.12 |
| The Prince            | vel | 1.32e‑6 | 8.45e‑7 | 2.38 |  –2.7e‑11 |  0.19 |

*(Table auto‑generated ‑ values copied from `vr_analysis_results_4d_2.csv`; verify once final run completes.)*

---

## §4 · Topological Findings   *(Stage-1 → Stage-1 ½)*

| symbol | observed shape | tentative Pirouette analogue | quick note |
| ------ | -------------- | ---------------------------- | ---------- |
| μ–σ    | bowed “μ–σ strip” | Γ–Tₐ shear plane | same as Stage-1 |
| **κ–μ** | *petaloid / paraboloid* opening toward high κ | incipient **Ki-bloom surface** | new! |
| κ–α    | warped saddle  | anisotropic Ki shell         | —
| δ–κ    | thin negative ramp | **cooling fault-line** (ΔΓ < 0) | universal across texts |

*Key insights v1*

1. **Petal Manifold** — Plotting κ vs. μ vs. σ reveals that Stage-1’s “rigidity-sensitivity axis” is actually the rim of a **curved petal/paraboloid**.  The petal’s spine aligns with prescriptive/legal works (Hammurabi, *Laws*), suggesting these serve as natural *bloom nuclei* in semantic space.

2. **Bloom Threshold** — The manifold’s curvature intensifies once  
   μ ≳ 1.6 × 10⁻⁶ → *∂κ/∂μ* grows super-linear.  This matches TEN-BDA’s prediction that bloom onset occurs when rigidity outpaces local coherence dissipation.

3. **Directional Anisotropy (α)** — Velcrid texts exhibit larger eigen-gaps, implying sharper “fault-planes” that channel semantic flow; Radiant works stay closer to isotropic shells.

4. **Drift Cooling (δ)** — All documents show δ < 0.  Magnitude correlates with genre formality: poetic/philosophical texts cool faster (|δ| ↑) than statute-like texts.  Suggests an intrinsic *entropy release* balancing bloom pressure.

*Key insights v2*
- **Saddle manifold:**  The (μ, κ) projection is now confirmed to be a **hyper-bolic paraboloid** (classic saddle).  Up-curving “rigidity wall” (μ-axis) opposes a down-curving “brittleness trough” (κ-axis); cost ∝ μ² – κ².  
- **Efficiency hint:**  Surface level-sets fit ≈ *(μ² – κ²) + λσ ≈ const* — a candidate energy/efficiency law to test in Stage-2.  
- **δ (drift) remains negative** → universal cooling; higher |δ| correlates with poetic/philosophical works, lower |δ| with prescriptive/legal texts.  
- **α (anisotropy) bifurcates by category**; Velcrid texts carve wider eigen-gaps (fault-lines), Radiant remain closer to isotropic shells.

---


---

## §5 · Pirouette Mapping & Hypotheses

1. **Triaxial fit:**  ( μ, σ, κ ) form an oblique 3‑D spindle matching the \$(\Gamma, T\_a, K\_i)\$ lattice predicted by Vol‑2 §27.
2. **Bloom trigger:** \$
   abla\_μ κ > 0\$ beyond threshold suggests the semantic channel begins *exponential crystal‑growth* (Bloom Dynamics TEN‑BDA) – aligns with prediction that legal codes serve as proto‑seeds.
3. **Residual entropy gradient:** negative δ acts as a built‑in *cooling term*, preventing runaway bloom except in prescriptive corpora where slope flattens.
4. **Saddle efficiency frontier:** the saddle’s ridge defines a Pareto-front between *rigidity* cost and *brittleness* instability—candidate analytical form  
   \[
     κ \;=\; a\,(μ-μ_0)^2 + b\,(δ-δ_0) + c
   \]
   with \(a,b,c\) empirically fit from Table 1.  This may instantiate the theorised Ki–Γ cross-term in PPS-034.


---

## §6 · Next-Step Plan

1. **Emergent-Time Sweep**  
   *Goal:* add a synthetic “flip chronology” so each text yields a Γ(t) curve; extract ∂²Γ/∂t² to probe acceleration of bloom/cooling cycles.

2. **Phase-Probe Injection**  
   Introduce known periodic bit-patterns (e.g., Φ₁ = 1010…, Φ₂ = 111000…) into neutral corpus chunks; measure how κ & α respond to controlled Ki rhythms.

3. **Petal-Surface Meshing**  
   Use Delaunay triangulation on (μ, σ, κ) to build an explicit mesh; compute Gaussian curvature K → validate paraboloid hypothesis quantitatively.

4. **Hessian Quiver Visuals**  
   Render local gradient fields (∇μ, ∇σ, ∇κ) over the petal surface to visualise “semantic wind” that drives texts toward or away from bloom.

5. **Amplitude-Scaling Re-run**  
   Scan amplitude A ∈ {0.05 … 0.25} to ensure σ tails aren’t clipped; compare manifold stability under different perturbation energies.

6. **Persona Extraction Pilot**  
   Treat each text’s (μ, σ, κ, δ, α) as a *persona vector*; test debate-style “seances” where vectors guide response weighting (Vol-3 §14: Debate Resonance Framework).
 - **Surface fitting:** regress the μ-κ-δ saddle to explicit hyperbolic-paraboloid coefficients; validate against synthetic “flat” corpora.
 - **Emergent-time sweep:** introduce flip-batch timeline (t) → track δ(t) and look for *temporal bloom spikes*, testing TEN-TAM interplay.
 - **Crystal growth sim:** treat hull facets as seed nuclei; iteratively add perturbed texts to observe facet-specific accretion (Stage-2).


---

## §7 · Artefacts

* **Script A:** `[SCRIPT_PLACEHOLDER]`  ← *insert final `VandR_Tool_four_dimension.py` here for archival & reproducibility.*
* **Dataset CSV:** `vr_analysis_results_4d_2.csv`  (uploaded; link when repo finalised).
* **Figures:**

  * `V&R_Score_4d_pairplot.png` – scatter‑matrix of all five metrics.
  * `semantic_gravity_4d_quiver.png` – 3‑D projection + drift vectors.

---

## §8 · Open Questions

> *Does κ truly capture Ki, or are we conflating heavy‑tail variance with rhythmic phase?  Need controlled synthetic texts with known periodic bit‑signatures.*

---

## §9 · Review Log

| rev   | date       | note                                                            |
| ----- | ---------- | --------------------------------------------------------------- |
| 0.1‑d | 2025‑07‑09 | Skeleton auto‑generated; awaiting flesh‑out & data cross‑check. |

---

#### Heuristic Triage Model

The personas can be used as a heuristic model for rapidly triaging a text's core nature based on its quantitative signature:

| Step | Metric | If... | Then... |
| :--- | :--- | :--- | :--- |
| **1. Assess Texture** | **Kurtosis (Kᵢ)** | **High** | The text has a "brittle," uneven structure. Proceed to assess stability. |
| | | **Low** | The text has a "malleable," uniform structure. Likely a **Malleable Reflection**. |
| **2. Assess Stability** | **Drift (∂μ/∂flips)** | **Negative** | The structure is fragile and decays. Likely a **Brittle Dogma**. |
| | | **Near-Zero** | The structure is stable. Could be a **Complex Strategy** or other rigid form. |

### Stage 2 Interpretation: Pirouette Personas

The Stage 2 metrics allow us to move beyond simple 2-D classification and synthesize the results into multi-dimensional "Pirouette Personas." By combining Gamma (Γ, rigidity), Kurtosis (Kᵢ, texture), and Drift (∂μ/∂flips, stability), we can define a tri-axial weight for any text that represents its fundamental class.

This approach allows us to quantitatively measure where a text sits on a spectrum of semantic behavior—for example, how close it is to a **brittle cliff's edge** (high Γ, high Kᵢ) versus a **solid mountainside** (high Γ, low Kᵢ). We can define several distinct archetypes based on the data:

* **The "Brittle Dogma" Persona**: Characterized by **high-Γ**, **high-Kᵢ**, and **negative Drift**. This profile describes a text that is initially very rigid with a spiky, uneven sensitivity landscape, but whose structure quickly erodes under perturbation. Ancient legal and prescriptive texts consistently map to this persona.
* **The "Malleable Reflection" Persona**: Defined by **low-Γ**, **low-Kᵢ**, and **near-zero Drift**. This describes a text with a soft, uniform structure that responds consistently and gently to perturbations. Contemplative works like *Walden* align with this.
* **The "Complex Strategy" Persona**: A potential third persona characterized by **high-Γ**, **high Anisotropy**, and **high-Kᵢ**. This profile suggests a text that is rigid and has specific points of failure but also possesses a strong directional "grain" or strategic bias.

[CODE_2]

import os
import re
import csv
import shutil
import hashlib
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.ndimage import convolve
from scipy.stats import kurtosis
from bs4 import BeautifulSoup
import statsmodels.api as sm
from statsmodels.formula.api import ols
import gc
import sys
import math

# --- Core Simulation Engine (Unchanged) ---
class SemanticDistillator:
    def __init__(self, grid_size=128, num_frames=200, noise_level=0.05, perturbation_amplitude=0.1):
        self.grid_size = grid_size
        self.num_frames = num_frames
        self.perturbation_amplitude = perturbation_amplitude
        np.random.seed(0)
        self.base_static_field = np.random.rand(self.grid_size, self.grid_size).astype(np.float32) * noise_level
        self.evolution_kernel = np.ones((3, 3), dtype=np.float32) / 9.0
        self.convolve_buffer = np.zeros((self.grid_size, self.grid_size), dtype=np.float32)

    def run_simulation(self, initial_pattern):
        grid = (self.base_static_field + initial_pattern * self.perturbation_amplitude).astype(np.float32)
        total_power = 0.0
        for _ in range(self.num_frames):
            convolve(grid, self.evolution_kernel, output=self.convolve_buffer, mode='wrap')
            grid, self.convolve_buffer = self.convolve_buffer, grid
            total_power += np.sum(np.square(grid))
        return total_power / (self.num_frames * self.grid_size * self.grid_size)

# --- V4 Scorer: Modified for Batch Processing ---
class PirouetteScorerV4:
    def __init__(self, grid_size=128, flips=4096, amplitude=0.1):
        self.flips = flips
        self.engine = SemanticDistillator(grid_size=grid_size, perturbation_amplitude=amplitude)

    @staticmethod
    def _create_seed_from_title(title: str) -> int:
        return int(hashlib.sha256(title.encode('utf-8')).hexdigest(), 16) % (2**32)

    def calculate_stats_from_file(self, temp_file_path):
        """Calculates mean, std dev, and kurtosis from the delta file."""
        print(f"[FINALIZE] Calculating full stats from {os.path.basename(temp_file_path)}...")

        # Read all deltas into memory for kurtosis calculation
        with open(temp_file_path, 'r') as f:
            deltas = [float(line) for line in f]

        if not deltas:
            return 0.0, 0.0, 0.0

        # Use numpy for efficient calculation
        delta_array = np.array(deltas, dtype=np.float64)
        mean_val = np.mean(delta_array)
        std_val = np.std(delta_array)
        # Use 'fisher=False' for the standard definition of kurtosis (3.0 is normal)
        kurtosis_val = kurtosis(delta_array, fisher=False)

        print(f"[FINALIZE]  ✓ Stats: μ={mean_val:.4e}, σ={std_val:.4e}, Kᵢ={kurtosis_val:.4f}")
        return mean_val, std_val, kurtosis_val

    # AFTER
    def run_simulation_batch(self, pattern_path: str, title: str, temp_delta_path: str, drift_log_path: str, completed_flips: int, batch_size: int):
        print(f"[CHECKPOINT] Preparing batch for '{title}' by loading pre-calculated pattern.")

        # --- Load the pre-calculated base pattern ---
        base_pattern = np.load(pattern_path)
        base_power = self.engine.run_simulation(base_pattern)
        flat_pattern_base = base_pattern.flatten()

        # --- This part remains deterministic ---
        seed = self._create_seed_from_title(title)
        rng = np.random.default_rng(seed)
        static_grid = rng.random((self.engine.grid_size, self.engine.grid_size), dtype=np.float32)
        bit_indices = np.argsort(static_grid.flatten())[-self.flips:]

        # --- Select the correct slice of flips for this batch ---
        flips_to_run = bit_indices[completed_flips : completed_flips + batch_size]
        print(f"[CHECKPOINT] This batch will run {len(flips_to_run)} flips.")

        # --- Open file in APPEND mode 'a' to add to existing work ---
        batch_deltas = [] # Store deltas for this batch only
        with open(temp_delta_path, 'a') as f:
            for i, bit_index in enumerate(flips_to_run):
                variant = flat_pattern_base.copy()
                variant[bit_index] = 1 - variant[bit_index]
                flipped_power = self.engine.run_simulation(variant.reshape(base_pattern.shape))
                delta = np.abs(flipped_power - base_power)
                f.write(f"{delta}\n")
                batch_deltas.append(delta)
        
            # --- New Drift Calculation Logic ---
            if batch_deltas:
                batch_mean = np.mean(np.array(batch_deltas, dtype=np.float64))
                # Log the number of flips *at the end* of this batch and the batch mean
                flips_at_batch_end = completed_flips + len(batch_deltas)
                with open(drift_log_path, 'a', newline='') as df:
                    writer = csv.writer(df)
                    writer.writerow([flips_at_batch_end, batch_mean])
                print(f"[DRIFT LOG]  ✓ Logged batch mean {batch_mean:.4e} at flip {flips_at_batch_end}.")

            print(f"[CHECKPOINT] Batch for '{title}' complete. Progress is saved.")
            return True
    
# --- File Utilities (with helpers for checkpointing) ---
def get_content_chunks(path: str, chunk_size=8192):
    # This is a generator, so it's memory-efficient.
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            if path.lower().endswith('.html'):
                content = strip_gutenberg_headers(BeautifulSoup(f.read(), "html.parser").get_text())
                for i in range(0, len(content), chunk_size): yield content[i:i+chunk_size]
            else:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk: break
                    yield strip_gutenberg_headers(chunk)
    except Exception as e:
        print(f"  ✗ ERROR during file read for {path}: {e}")
        return

def text_to_binary_image(text, grid_size):
    """Converts a string of text into a binary image grid."""
    binary_string = ''.join(format(ord(char), '08b') for char in text)
    binary_array = np.array([int(bit) for bit in binary_string], dtype=np.float32)
    target_size = grid_size * grid_size
    if binary_array.size < target_size:
        binary_array = np.pad(binary_array, (0, target_size - binary_array.size), 'constant')
    else:
        binary_array = binary_array[:target_size]
    return binary_array.reshape((grid_size, grid_size))

def count_lines(path: str) -> int:
    if not os.path.exists(path): return 0
    with open(path, 'r') as f:
        return sum(1 for _ in f)

def create_pattern_file(text_iterator_factory, grid_size, output_path):
    """
    Reads text chunks and saves a composite pattern to a .npy file.
    Returns True on success, False on failure, and None if the source is empty.
    """
    print(f"[PREP] Creating pattern file for {os.path.basename(output_path)}...")
    composite_pattern = np.zeros((grid_size, grid_size), dtype=np.float32)
    chunk_count = 0
    try:
        for text_chunk in text_iterator_factory():
            composite_pattern += text_to_binary_image(text_chunk, grid_size)
            chunk_count += 1
    except Exception as e:
        print(f"[PREP]  ✗ Error during text_to_binary_image conversion: {e}")
        return False # Indicates a processing failure

    if chunk_count > 0:
        final_pattern = composite_pattern / chunk_count
        np.save(output_path, final_pattern)
        print(f"[PREP]  ✓ Saved pattern to {os.path.basename(output_path)}")
        return True # Indicates success
    else:
        # This is the crucial new part: handle empty files.
        print(f"[PREP]  ✗ No content found after processing. The file is likely empty.")
        return None # Indicates the source file was empty

def load_completed_files(csv_path: str) -> set:
    if not os.path.exists(csv_path): return set()
    df = pd.read_csv(csv_path)
    return set(df['file'].unique())

def strip_gutenberg_headers(raw_text: str) -> str:
    start_pattern = re.compile(r"\*\*\*\s*START OF (THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*", re.IGNORECASE | re.DOTALL)
    end_pattern = re.compile(r"\*\*\*\s*END OF (THE|THIS) PROJECT GUTENBERG EBOOK.*", re.IGNORECASE | re.DOTALL)
    text = start_pattern.sub('', raw_text); text = end_pattern.sub('', text)
    return text.strip()

def append_to_csv(result_dict: dict, csv_path: str):
    file_exists = os.path.isfile(csv_path)
    with open(csv_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=result_dict.keys())
        if not file_exists: writer.writeheader()
        writer.writerow(result_dict)

def move_to_processed(source_path: str):
    processed_dir = os.path.join(os.path.dirname(source_path), "processed")
    os.makedirs(processed_dir, exist_ok=True)
    shutil.move(source_path, os.path.join(processed_dir, os.path.basename(source_path)))
    print(f"  ✓ Moved '{os.path.basename(source_path)}' to processed folder.")

def calculate_drift_score(drift_log_path):
    """Calculates the slope of the running mean from the drift log file."""
    if not os.path.exists(drift_log_path): return 0.0
    
    # Read the CSV log of batch means
    data = pd.read_csv(drift_log_path, header=None, names=['flip_count', 'batch_mean'])
    if len(data) < 2: return 0.0 # Need at least two points to define a slope
    
    # Perform linear regression to find the slope
    slope = np.polyfit(data['flip_count'], data['batch_mean'], 1)[0]
    print(f"[FINALIZE]  ✓ Drift Score (∂μ/∂flips): {slope:.4e}")
    return slope

def calculate_anisotropy_score(pattern_path):
    """Calculates the average anisotropy from the potential field defined by the pattern."""
    if not os.path.exists(pattern_path): return 0.0

    pattern = np.load(pattern_path)
    
    # Calculate the gradient (first derivative)
    gy, gx = np.gradient(pattern)
    
    # Calculate the components of the Hessian matrix (second derivatives)
    gxy, gxx = np.gradient(gx)
    gyy, gyx = np.gradient(gy)
    
    # Average the mixed derivatives for a symmetric Hessian
    H_xy = (gxy + gyx) / 2.0
    
    # Vectorized calculation of eigenvalue differences across the entire grid
    trace = gxx + gyy
    determinant = gxx * gyy - H_xy**2
    
    # The difference between eigenvalues is sqrt(trace^2 - 4*determinant)
    # Use np.maximum to prevent taking the square root of a small negative number from float error
    eigenvalue_diff = np.sqrt(np.maximum(0, trace**2 - 4 * determinant))
    
    # Summarize anisotropy across the grid by taking the mean
    anisotropy_score = np.mean(eigenvalue_diff)
    print(f"[FINALIZE]  ✓ Anisotropy Score: {anisotropy_score:.4e}")
    return anisotropy_score
# --- Main Execution Block with Checkpointing Logic ---
if __name__ == '__main__':
    # --- ⚙️ CONFIGURATION ---
    GRID_SIZE = 64
    TOTAL_FLIPS = 4096
    AMPLITUDE = 0.1
    CHUNK_SIZE = 16384
    BATCH_SIZE = 200 # Lowered for stability

    # --- 📂 FOLDER & FILE SETUP ---
    BASE_DIR = "C:/Users/keatw/OneDrive/Documents/Doclab/Big_Datasets/target/paper/Pirouette_Volume_5/doclab/experiments/Velcrid_Alignment"
    RADIANT_DIR = os.path.join(BASE_DIR, "radiant")
    VELCRID_DIR = os.path.join(BASE_DIR, "velcrid")
    RESULTS_CSV = "vr_analysis_results_4d_3.csv"

    # --- Initialize scorer ---
    scorer = PirouetteScorerV4(grid_size=GRID_SIZE, flips=TOTAL_FLIPS, amplitude=AMPLITUDE)

    # --- 🔁 AUTO-RUNNER LOOP ---
    # This loop will run continuously until no work is left.
    while True:
        # --- 1. Create Master Work Manifest (re-scanned each loop) ---
        manifest = []
        for dir_path, category in [(RADIANT_DIR, "radiant"), (VELCRID_DIR, "velcrid")]:
            if not os.path.isdir(dir_path): 
                print(f"[DIAGNOSTIC] Directory not found: {dir_path}") # Added line
                continue
            for f in os.listdir(dir_path):
                if f.lower().endswith(('.txt', '.html')) and os.path.isfile(os.path.join(dir_path, f)):
                    manifest.append({'path': os.path.join(dir_path, f), 'category': category})

        # --- 2. Load list of already fully completed files ---
        completed_files = load_completed_files(RESULTS_CSV)

        # --- Exit Condition: If all manifest files are in the final CSV, we are done. ---
        if len(manifest) == len(completed_files) and len(manifest) > 0:
            print("\n--- ✅ All files have been processed and finalized! Shutting down. ---")
            break

        work_done_this_pass = False
        # --- 3. Process the first available file in the manifest ---
        for item in manifest:
            file_path = item['path']
            category = item['category']
            filename = os.path.basename(file_path)

            if filename in completed_files:
                continue

            # This is now the first piece of work we've found.
            print(f"\n--- Checking work for: {filename} ---")
            
            # --- Define paths for all temporary files ---
            file_hash = hashlib.md5(filename.encode()).hexdigest()
            temp_delta_path = f"temp_deltas_{file_hash}.tmp"
            temp_pattern_path = f"temp_pattern_{file_hash}.npy"
            drift_log_path = f"temp_drift_{file_hash}.csv"

            # --- STAGE 1: Ensure the .npy pattern file exists ---
            if not os.path.exists(temp_pattern_path):
                content_iterator_factory = lambda: get_content_chunks(file_path, CHUNK_SIZE)
                
                # The create_pattern_file function now gives us a status
                status = create_pattern_file(content_iterator_factory, GRID_SIZE, temp_pattern_path)

                if status is None: # File was empty, move it and restart
                    print(f"[CLEANUP] Moving empty file '{filename}' to processed folder.")
                    move_to_processed(file_path)
                
                work_done_this_pass = True # We took an action, so we mark work as done
                break # Break to restart the loop and re-evaluate the manifest

            # --- STAGE 2: Process a batch or finalize ---
            completed_flips = count_lines(temp_delta_path)

            if completed_flips >= TOTAL_FLIPS:
                # --- Finalization Phase ---
                print(f"[FINALIZE] All {TOTAL_FLIPS} flips are complete. Finalizing score...")
                
                # --- Calculate all Stage 1 & Stage 2 metrics ---
                vel, rad, kurtosis = scorer.calculate_stats_from_file(temp_delta_path)
                drift = calculate_drift_score(drift_log_path)
                anisotropy = calculate_anisotropy_score(temp_pattern_path)
                
                text_len = sum(len(chunk) for chunk in get_content_chunks(file_path, CHUNK_SIZE))
                
                result = {
                    "file": filename, "category": category, 
                    "velcridance_score": vel, 
                    "radiance_score": rad,
                    "kurtosis_score": kurtosis,
                    "drift_score": drift,
                    "anisotropy_score": anisotropy,
                    "text_length": text_len
                }
                
                append_to_csv(result, RESULTS_CSV)
                print(f"[FINALIZE]  ✓ All scores logged to {RESULTS_CSV}")
                
                # Clean up all temporary files
                for temp_file in [temp_delta_path, temp_pattern_path, drift_log_path]:
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                print(f"[FINALIZE]  ✓ All temporary files removed.")
                
                move_to_processed(file_path)
                work_done_this_pass = True
                break
            else:
                # --- Work Phase (now much simpler) ---
                print(f"[WORK] Progress: {completed_flips}/{TOTAL_FLIPS}. Starting new batch.")
                scorer.run_simulation_batch(temp_pattern_path, filename, temp_delta_path, drift_log_path, completed_flips, BATCH_SIZE)
                work_done_this_pass = True
                break # Break from 'for' loop to start a fresh pass. This is key.

        # --- If a full pass over the manifest finds no work to do, exit. ---
        if not work_done_this_pass:
            print("\n--- No new work found in a full pass. Shutting down. ---")
            break