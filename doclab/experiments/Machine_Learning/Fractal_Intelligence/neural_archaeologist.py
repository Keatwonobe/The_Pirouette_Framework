# neural_archaeologist_fit.py
import torch
import torch.nn as nn
import numpy as np
import os
import matplotlib.pyplot as plt
import json
from scipy.stats import kurtosis
from scipy.signal import find_peaks

# --- Configuration ---
OBS_DIM = 105  # For Ant-v5
ACTION_DIM = 8 # For Ant-v5
# Adding Ki
KI_MOTION = 4.18879
PI = np.pi
GOLDEN_RATIO = 1.61803
MODEL_PATH = "./pirouette_fit_models/" # Make sure this matches your FIT trainer's output
ANALYSIS_RESULTS_PATH = "./fit_archaeology_results/"
os.makedirs(ANALYSIS_RESULTS_PATH, exist_ok=True)

# --- SOLUTION: The Actor class is now defined directly in this script ---
# This avoids importing from the trainer and triggering the file deletion.
class Actor(nn.Module):
    def __init__(self,s,a,h=256):
        super().__init__()
        self.n=nn.Sequential(nn.Linear(s,h),nn.ReLU(),nn.Linear(h,h),nn.ReLU())
        self.m=nn.Linear(h,a)
        self.ls=nn.Linear(h,a)
    def forward(self,s):
        x=self.n(s)
        return self.m(x),torch.clamp(self.ls(x),-20,2)

# --- Analysis Functions (Unchanged) ---

def analyze_weight_distribution(model):
    """Calculates basic statistics for each layer's weights."""
    stats = {}
    for name, param in model.named_parameters():
        if 'weight' in name:
            weights = param.data.cpu().numpy().flatten()
            stats[name] = {
                'mean': np.mean(weights),
                'std_dev': np.std(weights),
                # --- FIX: Use scipy.stats.kurtosis instead ---
                # We use fisher=False to get the standard kurtosis value (where 3.0 is normal)
                'kurtosis': float(kurtosis(weights, fisher=False))
            }
    return stats

def analyze_svd_coherence(model):
    """
    Performs SVD on weight matrices to get a 'coherence score' (proxy for T_a).
    A higher score (from a lower effective rank) implies higher coherence.
    """
    coherence_scores = {}
    total_effective_rank_ratio = 0
    num_layers = 0

    for name, param in model.named_parameters():
        if 'weight' in name and param.data.dim() == 2:
            num_layers += 1
            U, S, V = torch.svd(param.data)
            normalized_s = S / torch.sum(S)
            effective_rank_ratio = (torch.sum(normalized_s)**2) / torch.sum(normalized_s**2) / S.shape[0]
            coherence_scores[name] = 1.0 - effective_rank_ratio.item()
            total_effective_rank_ratio += effective_rank_ratio.item()
    
    overall_coherence = 1.0 - (total_effective_rank_ratio / num_layers) if num_layers > 0 else 0
    return overall_coherence, coherence_scores

def probe_for_ki_resonance(model, obs_dim, num_steps=1000, max_freq=5.0):
    """
    Probes the network with rhythmic inputs to find its resonant frequency (proxy for Ki-attunement).
    """
    model.eval()
    device = next(model.parameters()).device
    frequencies = np.linspace(0.1, max_freq, 100)
    output_powers = []
    baseline_state = torch.zeros(1, obs_dim, device=device)

    for freq in frequencies:
        actions_over_time = []
        for t in range(num_steps):
            perturbation = torch.sin(torch.tensor(2 * np.pi * freq * (t / num_steps)))
            perturbed_state = baseline_state.clone()
            perturbed_state[0, 0] = perturbation

            with torch.no_grad():
                mean, _ = model(perturbed_state)
                action = torch.tanh(mean)
            actions_over_time.append(action[0, 0].item())
        
        fft_result = np.fft.fft(actions_over_time)
        fft_freq = np.fft.fftfreq(num_steps)
        target_idx = np.argmin(np.abs(fft_freq - freq))
        power = np.abs(fft_result[target_idx])**2
        output_powers.append(power)

    max_power_idx = np.argmax(output_powers)
    resonant_freq = frequencies[max_power_idx]
    attunement_score = np.max(output_powers)

    return resonant_freq, attunement_score, frequencies, output_powers

def analyze_weight_spectrum_ratios(model):
    """
    Analyzes the ratios between dominant singular values of weight matrices
    to find signatures of Ki-like harmonic resonance.
    """
    all_ratios = {}
    for name, param in model.named_parameters():
        if 'weight' in name and param.data.dim() == 2:
            U, S, V = torch.svd(param.data)
            
            # Find peaks in the singular value spectrum (the most dominant values)
            singular_values = S.cpu().numpy()
            peaks, _ = find_peaks(singular_values, height=np.mean(singular_values), distance=2)
            
            if len(peaks) < 2:
                continue

            top_singular_values = singular_values[peaks]
            layer_ratios = []

            # Check ratios between the top singular values
            for i in range(len(top_singular_values)):
                for j in range(i + 1, len(top_singular_values)):
                    ratio = top_singular_values[i] / top_singular_values[j]
                    targets = {
                        'ki_motion_div_pi': KI_MOTION / PI, # ~1.33
                        'golden_ratio': GOLDEN_RATIO
                    }
                    for t_name, t_val in targets.items():
                        if abs(ratio - t_val) < 0.05 or abs(1/ratio - t_val) < 0.05:
                            layer_ratios.append({
                                'type': t_name,
                                'ratio': ratio,
                                'values': (float(top_singular_values[i]), float(top_singular_values[j]))
                            })
            if layer_ratios:
                all_ratios[name] = layer_ratios
    return all_ratios

# --- Main Execution ---

def run_archaeology(model_rank):
    print(f"\n--- Running Archaeology on Model Rank {model_rank} ---")
    actor_path = os.path.join(MODEL_PATH, f"rank_{model_rank}", "actor.pth")

    if not os.path.exists(actor_path):
        print(f"Model file not found for rank {model_rank}. Skipping.")
        return None

    device = torch.device("cpu")
    model = Actor(OBS_DIM, ACTION_DIM).to(device)
    model.load_state_dict(torch.load(actor_path, map_location=device))

    # 1. Static Analysis: T_a Proxy
    dist_stats = analyze_weight_distribution(model)
    ta_coherence_score, layer_scores = analyze_svd_coherence(model)
    print(f"  [T_a] Overall Coherence Score (from SVD): {ta_coherence_score:.4f}")

    # 2. Dynamic Analysis: Ki Proxy
    res_freq, attunement, freqs, powers = probe_for_ki_resonance(model, OBS_DIM)
    print(f"  [Ki] Resonant Frequency: {res_freq:.2f} Hz")
    print(f"  [Ki] Attunement Score (Power at Resonance): {attunement:.4f}")

    # Plotting code (remains the same)...
    plt.figure(figsize=(10, 5))
    plt.plot(freqs, powers, marker='.', linestyle='-')
    plt.title(f'Ki Resonance Probe for FIT Model Rank {model_rank}')
    plt.xlabel("Input Frequency (Hz)")
    plt.ylabel("Output Power at Frequency")
    plt.axvline(res_freq, color='r', linestyle='--', label=f'Peak Resonance: {res_freq:.2f} Hz')
    plt.legend(); plt.grid(True)
    plot_path = os.path.join(ANALYSIS_RESULTS_PATH, f"rank_{model_rank}_resonance_probe.png")
    plt.savefig(plot_path)
    plt.close()
    print(f"  > Resonance plot saved to {plot_path}")
    
    # --- FIX: Cast all metrics to standard Python floats before saving ---
    results = {
        'rank': int(model_rank),
        'ta_coherence_score': float(ta_coherence_score),
        'ki_resonant_frequency': float(res_freq),
        'ki_attunement_score': float(attunement),
        'weight_stats': {k: {sk: float(sv) for sk, sv in v.items()} for k, v in dist_stats.items()},
        'svd_layer_scores': {k: float(v) for k, v in layer_scores.items()}
    }
    ki_ratios = analyze_weight_spectrum_ratios(model)
    if ki_ratios:
        print(f"  [Ki] Found {len(ki_ratios)} layer(s) with Ki-resonant spectral ratios.")
        results['ki_structural_ratios'] = ki_ratios
    return results

if __name__ == '__main__':
    all_results = []
    # Assuming GENETIC_POOL_SIZE is 10 as per the fit trainer script
    for rank_id in range(1, 11): 
        result = run_archaeology(rank_id)
        if result:
            all_results.append(result)
            
    results_file = os.path.join(ANALYSIS_RESULTS_PATH, "fit_archaeology_summary.json")
    with open(results_file, 'w') as f:
        json.dump(all_results, f, indent=4)
        
    print(f"\n✅ FIT Archaeology complete. Summary saved to {results_file}")