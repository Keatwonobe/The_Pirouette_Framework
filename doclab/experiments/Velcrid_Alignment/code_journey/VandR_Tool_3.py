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

# Suppress pandas warnings for cleaner output
warnings.filterwarnings("ignore", category=FutureWarning)


# --- Core SDE Simulation Logic ---
GRID_SIZE = 64
NUM_FRAMES = 200
NOISE_LEVEL = 0.05
EVOLUTION_KERNEL = np.ones((3, 3)) / 9.0
PERTURBATION_AMPLITUDE = 0.01

class SemanticDistillator:
    """A streamlined version of the SDE for this specific test."""
    def __init__(self, seed=0):
        np.random.seed(seed)
        self.base_static_field = np.random.rand(GRID_SIZE, GRID_SIZE) * NOISE_LEVEL

    def text_to_binary_image(self, text, width=64, height=64):
        """Converts a string to a binary image based on its ASCII representation."""
        binary_string = ''.join(format(ord(char), '08b') for char in text)
        binary_array = np.array([int(bit) for bit in binary_string], dtype=np.float32)
        if len(binary_array) > GRID_SIZE * GRID_SIZE:
            binary_array = binary_array[:GRID_SIZE * GRID_SIZE]
        else:
            padding = np.zeros(GRID_SIZE * GRID_SIZE - len(binary_array))
            binary_array = np.concatenate([binary_array, padding])
        return binary_array.reshape((GRID_SIZE, GRID_SIZE))

    def run_simulation(self, initial_pattern):
        """Runs the core cellular automata simulation."""
        grid = self.base_static_field + initial_pattern * PERTURBATION_AMPLITUDE
        total_power = 0
        for _ in range(NUM_FRAMES):
            grid = convolve(grid, EVOLUTION_KERNEL, mode='wrap')
            total_power += np.sum(grid**2)
        return total_power / (NUM_FRAMES * GRID_SIZE * GRID_SIZE)

    def get_energy_signature(self, text, seed=0):
        """Gets the final 'total power' for a given text input."""
        self.__init__(seed)
        binary_image = self.text_to_binary_image(text)
        return self.run_simulation(binary_image)

def flip_bit_in_image(img, bit_index):
    """Flips a single bit in a flattened binary image."""
    flat_img = img.flatten()
    if bit_index < len(flat_img):
        flat_img[bit_index] = 1 - flat_img[bit_index]
    return flat_img.reshape(img.shape)

# --- Scoring Modules ---

class RadianceScorer:
    """
    Radiance ≈ mean |Δenergy| produced by single-bit flips.
    Higher score ➜ more *sensitive* / more 'radiant'.
    """
    def __init__(self, grid_size=64, flips=32, seed=123):
        self.grid_size = grid_size
        self.flips = flips
        self.rng = np.random.default_rng(seed)
        self.engine = SemanticDistillator(seed=seed)

    def score(self, text: str) -> dict:
        base_pattern = self.engine.text_to_binary_image(text, self.grid_size, self.grid_size)
        base_power = self.engine.run_simulation(base_pattern)
        total_bits = self.grid_size * self.grid_size
        bit_indices_to_flip = self.rng.choice(total_bits, self.flips, replace=False)
        deltas = []
        for bit_index in bit_indices_to_flip:
            flipped_pattern = flip_bit_in_image(base_pattern.copy(), bit_index)
            flipped_power = self.engine.run_simulation(flipped_pattern)
            deltas.append(np.abs(flipped_power - base_power))
        mean_delta = np.mean(deltas) if deltas else 0
        return {"radiance_score": float(mean_delta)}

class VelcridanceScorer:
    """
    Velcridance is a measure of semantic rigidity.
    Higher score ➜ more resistant to perturbation ➜ more Velcrid-like.
    """
    def __init__(self, grid_size=64, flips=32, seed=42):
        self.grid_size = grid_size
        self.flips = flips
        self.rng = np.random.default_rng(seed)
        self.engine = SemanticDistillator(seed=seed)

    def score(self, text: str) -> dict:
        base_pattern = self.engine.text_to_binary_image(text, self.grid_size, self.grid_size)
        base_power = self.engine.run_simulation(base_pattern)
        total_bits = self.grid_size * self.grid_size
        bit_indices_to_flip = self.rng.choice(total_bits, self.flips, replace=False)
        deltas = []
        for bit_index in bit_indices_to_flip:
            flipped_pattern = flip_bit_in_image(base_pattern.copy(), bit_index)
            flipped_power = self.engine.run_simulation(flipped_pattern)
            deltas.append(np.abs(flipped_power - base_power))
        mean_delta = np.mean(deltas) if deltas else 0
        velcridance_score = 1 / (1 + mean_delta) if mean_delta is not None else 0
        return {"velcridance_score": float(velcridance_score)}

# --- Utility and Processing Functions ---

def strip_html(raw_html: str) -> str:
    """Simple HTML -> text stripper."""
    soup = BeautifulSoup(raw_html, "html.parser")
    for script_or_style in soup(["script", "style"]):
        script_or_style.decompose()
    return re.sub(r'\s+', ' ', soup.get_text()).strip()

def get_content(path: str) -> str:
    """Reads content from a file path or URL."""
    if path.startswith('http://') or path.startswith('https://'):
        try:
            response = requests.get(path)
            response.raise_for_status()
            if 'text/html' in response.headers.get('Content-Type', ''):
                return strip_html(response.text)
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL: {e}")
            return None
    elif os.path.exists(path):
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        if path.lower().endswith('.html'):
            return strip_html(content)
        return content
    else:
        print(f"Error: File not found at {path}")
        return None

def analyze_document(file_path: str, radiance_scorer: RadianceScorer, velcridance_scorer: VelcridanceScorer) -> dict:
    """Analyzes a single document and returns its scores."""
    print(f"  - Processing: {os.path.basename(file_path)}")
    content = get_content(file_path)
    if not content or not content.strip():
        print(f"    - Warning: No content found in {os.path.basename(file_path)}")
        return None

    radiance_results = radiance_scorer.score(content)
    velcridance_results = velcridance_scorer.score(content)

    return {
        "radiance_score": radiance_results["radiance_score"],
        "velcridance_score": velcridance_results["velcridance_score"]
    }

def process_directory(dir_path: str, label: str, r_scorer: RadianceScorer, v_scorer: VelcridanceScorer) -> list:
    """Processes all valid files in a directory."""
    results = []
    if not os.path.isdir(dir_path):
        print(f"Warning: Directory not found: {dir_path}")
        return results

    print(f"\n--- Scanning '{label}' directory: {dir_path} ---\n")
    for filename in os.listdir(dir_path):
        if filename.lower().endswith(('.txt', '.html')):
            file_path = os.path.join(dir_path, filename)
            scores = analyze_document(file_path, r_scorer, v_scorer)
            if scores:
                scores['file'] = filename
                scores['category'] = label
                results.append(scores)
    return results

def plot_results(df: pd.DataFrame):
    """Generates and saves a scatter plot of the results."""
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(10, 8))
    
    colors = {'radiant': 'gold', 'velcrid': 'darkblue'}
    
    for category, group in df.groupby('category'):
        ax.scatter(group['velcridance_score'], group['radiance_score'],
                   s=80, alpha=0.8,
                   c=colors[category],
                   label=category.capitalize())

    ax.set_title('Velcridance vs. Radiance Score Analysis', fontsize=16)
    ax.set_xlabel('Velcridance Score (Semantic Rigidity)', fontsize=12)
    ax.set_ylabel('Radiance Score (Semantic Sensitivity)', fontsize=12)
    ax.legend(title='Category')
    ax.grid(True)
    
    # Save the plot
    output_filename = 'vr_analysis_plot.png'
    plt.savefig(output_filename)
    print(f"\n✅ Results plot saved as '{output_filename}'")
    plt.show()


# --- Main Execution Block ---

if __name__ == '__main__':
    # --- IMPORTANT: UPDATE THIS PATH ---
    # Set the base directory where your 'radiant' and 'velcrid' folders are located.
    BASE_DIR = "C:/Users/keatw/OneDrive/Documents/Doclab/Big_Datasets/target/paper/Pirouette_Volume_5/doclab/experiments/Velcrid_Alignment" # Use "." for the current directory, or a full path like "C:/Users/..."

    RADIANT_DIR = os.path.join(BASE_DIR, "radiant")
    VELCRID_DIR = os.path.join(BASE_DIR, "velcrid")

    # Initialize scorers once to maintain state and efficiency
    radiance_scorer = RadianceScorer()
    velcridance_scorer = VelcridanceScorer()
    
    # Process both directories
    all_results = []
    all_results.extend(process_directory(RADIANT_DIR, "radiant", radiance_scorer, velcridance_scorer))
    all_results.extend(process_directory(VELCRID_DIR, "velcrid", velcridance_scorer, velcridance_scorer))

    if not all_results:
        print("\nNo files were processed. Please check your directory paths and file types.")
    else:
        # Create and display the results table
        results_df = pd.DataFrame(all_results)
        results_df = results_df[['file', 'category', 'velcridance_score', 'radiance_score']] # Reorder columns
        
        print("\n--- Analysis Complete ---")
        print("\n📊 Results Summary:")
        print(results_df.to_string(index=False))

        # Generate the plot
        plot_results(results_df)