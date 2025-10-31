import os
import re
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.ndimage import convolve
from bs4 import BeautifulSoup
import requests
import warnings
import shutil
import csv

# Suppress pandas warnings for cleaner output
warnings.filterwarnings("ignore", category=FutureWarning)

# --- Core SDE Simulation Logic ---
GRID_SIZE = 64
NUM_FRAMES = 200
NOISE_LEVEL = 0.05
EVOLUTION_KERNEL = np.ones((3, 3)) / 9.0
PERTURBATION_AMPLITUDE = 0.01

class SemanticDistillator:
    def __init__(self, seed=0):
        np.random.seed(seed)
        self.base_static_field = np.random.rand(GRID_SIZE, GRID_SIZE) * NOISE_LEVEL

    def text_to_binary_image(self, text):
        binary_string = ''.join(format(ord(char), '08b') for char in text)
        binary_array = np.array([int(bit) for bit in binary_string], dtype=np.float32)
        target_size = GRID_SIZE * GRID_SIZE
        if len(binary_array) > target_size:
            binary_array = binary_array[:target_size]
        else:
            padding = np.zeros(target_size - len(binary_array))
            binary_array = np.concatenate([binary_array, padding])
        return binary_array.reshape((GRID_SIZE, GRID_SIZE))

    def run_simulation(self, initial_pattern):
        grid = self.base_static_field + initial_pattern * PERTURBATION_AMPLITUDE
        total_power = np.sum([np.sum(grid:=convolve(grid, EVOLUTION_KERNEL, mode='wrap')**2) for _ in range(NUM_FRAMES)])
        return total_power / (NUM_FRAMES * GRID_SIZE * GRID_SIZE)

def flip_bit_in_image(img, bit_index):
    flat_img = img.flatten()
    if bit_index < len(flat_img):
        flat_img[bit_index] = 1 - flat_img[bit_index]
    return flat_img.reshape(img.shape)

# --- Scoring Modules ---

class RadianceScorer:
    def __init__(self, grid_size=64, flips=32, seed=123):
        self.grid_size = grid_size
        self.flips = flips
        self.rng = np.random.default_rng(seed)
        self.engine = SemanticDistillator(seed=seed)

    def score(self, text: str) -> dict:
        base_pattern = self.engine.text_to_binary_image(text)
        base_power = self.engine.run_simulation(base_pattern)
        bit_indices_to_flip = self.rng.choice(self.grid_size**2, self.flips, replace=False)
        deltas = [np.abs(self.engine.run_simulation(flip_bit_in_image(base_pattern.copy(), i)) - base_power) for i in bit_indices_to_flip]
        return {"radiance_score": float(np.mean(deltas))}

class VelcridanceScorer:
    def __init__(self, grid_size=64, flips=32, seed=42):
        self.grid_size = grid_size
        self.flips = flips
        self.rng = np.random.default_rng(seed)
        self.engine = SemanticDistillator(seed=seed)

    def score(self, text: str) -> dict:
        base_pattern = self.engine.text_to_binary_image(text)
        base_power = self.engine.run_simulation(base_pattern)
        bit_indices_to_flip = self.rng.choice(self.grid_size**2, self.flips, replace=False)
        deltas = [np.abs(self.engine.run_simulation(flip_bit_in_image(base_pattern.copy(), i)) - base_power) for i in bit_indices_to_flip]
        mean_delta = np.mean(deltas)
        return {"velcridance_score": 1 / (1 + mean_delta)}

# --- Utility and Processing Functions ---

def strip_html(raw_html: str) -> str:
    soup = BeautifulSoup(raw_html, "html.parser")
    for element in soup(["script", "style"]):
        element.decompose()
    return re.sub(r'\s+', ' ', soup.get_text()).strip()

def get_content(path: str) -> str:
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    return strip_html(content) if path.lower().endswith('.html') else content

def append_to_csv(result_dict: dict, csv_path: str):
    """Appends a dictionary of results to a CSV file."""
    file_exists = os.path.isfile(csv_path)
    with open(csv_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=result_dict.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(result_dict)

def move_to_processed(source_path: str):
    """Moves a file to the 'processed' subdirectory of its parent folder."""
    base_dir = os.path.dirname(source_path)
    filename = os.path.basename(source_path)
    processed_dir = os.path.join(base_dir, "processed")
    os.makedirs(processed_dir, exist_ok=True)
    destination_path = os.path.join(processed_dir, filename)
    shutil.move(source_path, destination_path)
    print(f"  ✓ Moved to: {os.path.relpath(destination_path)}")

def analyze_and_log(dir_path: str, label: str, r_scorer: RadianceScorer, v_scorer: VelcridanceScorer, csv_path: str):
    if not os.path.isdir(dir_path):
        print(f"Warning: Directory not found: {dir_path}")
        return

    print(f"\n--- Scanning '{label}' directory: {dir_path} ---")
    files_to_process = [f for f in os.listdir(dir_path) if f.lower().endswith(('.txt', '.html')) and os.path.isfile(os.path.join(dir_path, f))]

    if not files_to_process:
        print("  No new files to process.")
        return

    for filename in files_to_process:
        file_path = os.path.join(dir_path, filename)
        print(f"\n- Processing: {filename}")
        try:
            content = get_content(file_path)
            if not content or not content.strip():
                print(f"  ✗ Error: No content found in file.")
                move_to_processed(file_path) # Move empty files
                continue

            radiance = r_scorer.score(content)["radiance_score"]
            velcridance = v_scorer.score(content)["velcridance_score"]

            result = {
                "file": filename,
                "category": label,
                "velcridance_score": velcridance,
                "radiance_score": radiance
            }

            append_to_csv(result, csv_path)
            print(f"  ✓ Scores logged: V={velcridance:.4f}, R={radiance:.6f}")
            move_to_processed(file_path)

        except Exception as e:
            print(f"  ✗ An error occurred while processing {filename}: {e}")
            # Optionally, move errored files to a different directory
            # move_to_errored(file_path)
            continue

def plot_results(csv_path: str):
    if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
        print("\nNo results to plot. The CSV file is empty or missing.")
        return

    df = pd.read_csv(csv_path)
    if df.empty:
        print("\nNo data in CSV to plot.")
        return
        
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(10, 8))
    colors = {'radiant': 'gold', 'velcrid': 'darkblue'}
    
    for category, group in df.groupby('category'):
        ax.scatter(group['velcridance_score'], group['radiance_score'], s=80, alpha=0.7, ec='w', c=colors.get(category, 'gray'), label=category.capitalize())

    ax.set_title('Velcridance vs. Radiance Score Analysis', fontsize=16)
    ax.set_xlabel('Velcridance Score (Semantic Rigidity)', fontsize=12)
    ax.set_ylabel('Radiance Score (Semantic Sensitivity)', fontsize=12)
    ax.legend(title='Category')
    ax.grid(True)
    
    output_filename = 'vr_analysis_plot.png'
    plt.savefig(output_filename)
    print(f"\n✅ Results plot updated and saved as '{output_filename}'")
    plt.show()

# --- Main Execution Block ---

if __name__ == '__main__':
    BASE_DIR = "C:/Users/keatw/OneDrive/Documents/Doclab/Big_Datasets/target/paper/Pirouette_Volume_5/doclab/experiments/Velcrid_Alignment"
    RADIANT_DIR = os.path.join(BASE_DIR, "radiant")
    VELCRID_DIR = os.path.join(BASE_DIR, "velcrid")
    RESULTS_CSV = "vr_analysis_results.csv"

    # Create directories if they don't exist
    os.makedirs(RADIANT_DIR, exist_ok=True)
    os.makedirs(VELCRID_DIR, exist_ok=True)
    
    # Initialize scorers once
    radiance_scorer = RadianceScorer()
    velcridance_scorer = VelcridanceScorer()
    
    # Process both directories, logging results incrementally
    analyze_and_log(RADIANT_DIR, "radiant", radiance_scorer, velcridance_scorer, RESULTS_CSV)
    analyze_and_log(VELCRID_DIR, "velcrid", radiance_scorer, velcridance_scorer, RESULTS_CSV)

    print("\n--- Analysis Run Complete ---")
    
    # Generate the summary plot from all logged results
    plot_results(RESULTS_CSV)