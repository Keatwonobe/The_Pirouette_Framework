import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.ndimage import convolve

# --- Core SDE Simulation Logic (Unchanged) ---
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

def flip_bit_in_string(s, bit_index):
    """Flips a single bit in the binary representation of a string."""
    binary_string = ''.join(format(ord(char), '08b') for char in s)
    if bit_index >= len(binary_string):
        raise ValueError("bit_index is out of bounds")
    bit_list = list(binary_string)
    bit_list[bit_index] = '1' if bit_list[bit_index] == '0' else '0'
    flipped_binary_string = "".join(bit_list)
    byte_chunks = [flipped_binary_string[i:i+8] for i in range(0, len(flipped_binary_string), 8)]
    new_s = "".join(chr(int(byte, 2)) for byte in byte_chunks if len(byte) == 8)
    return new_s

# --- Updated Batch Analysis and Consistency Test ---

def run_gradient_test_for_word(distillator, base_word, trial_seed):
    """
    Runs a single gradient test for one word with a specific seed.
    Returns the mean delta for this single trial.
    """
    base_energy = distillator.get_energy_signature(base_word, seed=trial_seed)
    num_bits = len(base_word) * 8
    deltas = []

    for i in range(num_bits):
        try:
            flipped_word = flip_bit_in_string(base_word, i)
            if len(flipped_word) == len(base_word):
                energy = distillator.get_energy_signature(flipped_word, seed=trial_seed)
                deltas.append(np.abs(energy - base_energy))
        except (ValueError, UnicodeDecodeError):
            continue
            
    return np.mean(deltas) if deltas else 0

def run_batch_consistency_analysis(words_to_test, num_trials=20):
    """
    Performs a batch analysis on a list of words, running multiple trials
    for each to test consistency.
    """
    print("--- Starting Batch Semantic Gradient & Consistency Analysis ---")
    distillator = SemanticDistillator()
    results = []

    for word in words_to_test:
        print(f"\nProcessing '{word}'...")
        trial_deltas = []
        for i in range(num_trials):
            # Use a different seed for each trial to test consistency against random static
            trial_seed = i 
            mean_delta = run_gradient_test_for_word(distillator, word, trial_seed)
            trial_deltas.append(mean_delta)
            results.append({'word': word, 'trial': i, 'mean_delta': mean_delta})
            print(f"  Trial {i+1}/{num_trials} | Mean Delta: {mean_delta:.6e}")
        
        # --- Statistical Summary for the Word ---
        avg_of_deltas = np.mean(trial_deltas)
        std_of_deltas = np.std(trial_deltas)
        print(f"\nSummary for '{word}':")
        print(f"  Average of Mean Deltas over {num_trials} trials: {avg_of_deltas:.6e}")
        print(f"  Standard Deviation of Mean Deltas: {std_of_deltas:.6e}")
        if std_of_deltas / avg_of_deltas < 0.1: # Heuristic for high consistency
             print("  [CONCLUSION] Results are HIGHLY CONSISTENT across trials.")
        else:
             print("  [CONCLUSION] Results show significant VARIANCE across trials.")


    return pd.DataFrame(results)

# --- Main Execution ---

if __name__ == "__main__":
    # A list of concepts to test. Includes pairs of related and contrasting words.
    concepts = [
        "love", "hate", "courage", "fear", "truth", "deceit", 
        "order", "chaos", "justice", "injustice"
    ]
    
    results_df = run_batch_consistency_analysis(concepts, num_trials=10)
    
    # --- Visualization ---
    plt.figure(figsize=(16, 9))
    sns.boxplot(x='word', y='mean_delta', data=results_df, palette='viridis')
    sns.stripplot(x='word', y='mean_delta', data=results_df, color='black', size=4, jitter=True, alpha=0.6)

    plt.title("Consistency of Semantic Perturbation Deltas Across 10 Trials", fontsize=18, pad=20)
    plt.xlabel("Concept Word", fontsize=14)
    plt.ylabel("Mean Energy Delta from 1-Bit Flips", fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.yscale('log') # Use a log scale to better visualize small differences
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Save the plot for review
    plot_filename = "batch_gradient_consistency_assessment.png"
    plt.savefig(plot_filename)
    print(f"\n--- Analysis complete. Plot saved to {plot_filename} ---")
    
    plt.show()