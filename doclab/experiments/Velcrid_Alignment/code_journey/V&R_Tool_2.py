import os
import re
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.ndimage import convolve
from bs4 import BeautifulSoup
import requests

# --- Core SDE Simulation Logic (from semantic_test_engine_2.py) ---
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

# --- Scoring Modules (from radiance_score_module.py and velcridance_score_module.py) ---

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
        """
        Calculates the radiance score for a given text.
        """
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
        return {
            "radiance_score": float(mean_delta),
            "base_power": float(base_power),
            "num_flips": self.flips
        }

class VelcridanceScorer:
    """
    Velcridance is a measure of semantic rigidity.
    It is estimated by measuring how *little* a text’s energy signature changes under random 1-bit flips.
    Higher score ➜ more resistant to perturbation ➜ more Velcrid-like.
    """
    def __init__(self, grid_size=64, flips=32, seed=42):
        self.grid_size = grid_size
        self.flips = flips
        self.rng = np.random.default_rng(seed)
        self.engine = SemanticDistillator(seed=seed)

    def score(self, text: str) -> dict:
        """
        Calculates the velcridance score for a given text.
        """
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
        
        # Velcridance is inversely related to the mean delta
        velcridance_score = 1 / (1 + mean_delta) if mean_delta is not None else 0
        
        return {
            "velcridance_score": float(velcridance_score),
            "mean_delta": float(mean_delta),
            "base_power": float(base_power),
            "num_flips": self.flips
        }

# --- Utility Functions (from V&R_Tool.py) ---

def strip_html(raw_html: str) -> str:
    """Simple HTML -> text stripper."""
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text()

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
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        if path.endswith('.html'):
            return strip_html(content)
        return content
    else:
        print(f"Error: File not found at {path}")
        return None

# --- Main Analysis Function ---

def analyze_document(file_path: str):
    """
    Analyzes a document for Radiance and Velcridance scores.
    """
    content = get_content(file_path)
    if not content:
        return

    print(f"--- Analyzing: {file_path} ---")

    # Initialize scorers
    radiance_scorer = RadianceScorer()
    velcridance_scorer = VelcridanceScorer()

    # Get scores
    radiance_results = radiance_scorer.score(content)
    velcridance_results = velcridance_scorer.score(content)

    # Print results
    print("\n--- Radiance Score ---")
    print(json.dumps(radiance_results, indent=2))

    print("\n--- Velcridance Score ---")
    print(json.dumps(velcridance_results, indent=2))

if __name__ == '__main__':
    # Example usage:
    # Replace 'path/to/your/document.txt' with the actual file path.
    # You can use a local file path or a URL.
    file_to_analyze = 'C:/Users/keatw/OneDrive/Documents/Doclab/Big_Datasets/target/paper/Pirouette_Volume_5/doclab/experiments/Velcrid_Alignment/radiant/project_gutenberg_ebook_of_The_Meditations_of_the_Emperor_Marcus_Aurelius_Antonius.txt'
    if not os.path.exists(file_to_analyze):
        print(f"Example file '{file_to_analyze}' not found.")
        print("Please provide a valid file path or URL to analyze.")
    else:
        analyze_document(file_to_analyze)