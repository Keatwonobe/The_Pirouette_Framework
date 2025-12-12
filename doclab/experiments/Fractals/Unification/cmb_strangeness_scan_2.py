import numpy as np
import matplotlib.pyplot as plt
import json
import os

# ==============================================================================
#  1. CONSTANTS & FRAMEWORK (Reusing Strangeness Meter Logic)
# ==============================================================================

# Universal constants
F_FUNDAMENTAL = 24.0        # Hz
PROTON_SCALE = 0.8414e-15   # m
UNIVERSE_SCALE = 4.4e26     # m
MAX_FREQ_DEVIATION_FACTOR = 0.005 # Max 0.5% deviation used in simulation

def universal_clock_phase(scale_meters):
    """Get expected cardioid phase for a scale."""
    log_scale = np.log10(scale_meters)
    log_proton = np.log10(PROTON_SCALE)
    log_universe = np.log10(UNIVERSE_SCALE)
    normalized = (log_scale - log_proton) / (log_universe - log_proton)
    phase = normalized * 2 * np.pi
    amplitude = 1 + np.cos(phase)
    return phase, amplitude

def calculate_strangeness(observed_frequency_hz, scale_meters):
    """Calculate Universal Strangeness Score (Σ) (Simplified for CMB)."""
    expected_phase, expected_amplitude = universal_clock_phase(scale_meters)
    expected_freq = F_FUNDAMENTAL / expected_amplitude
    
    freq_deviation = abs(observed_frequency_hz - expected_freq) / expected_freq
    freq_alignment = np.exp(-freq_deviation)
    T_a = freq_alignment
    
    # Weights (w_phase=0.3, w_pressure=0.1 are set to 0 contribution)
    w_freq = 0.4
    w_coherence = 0.2
    
    S_freq = freq_deviation
    S_coherence = 1 - T_a
    
    Sigma = (w_freq * S_freq + w_coherence * S_coherence)
    Sigma = min(Sigma, 1.0)
    
    return Sigma, expected_freq


def simulate_cmb_strangeness_scan(k_range, scale, expected_freq, max_dev_factor):
    """
    Mocks the CMB twist simulation and calculates Strangeness Score (Σ) 
    for the given k_range.
    """
    k_dev = k_range - 1.0
    
    # Calculate max deviation squared relative to the absolute initial max deviation
    # This keeps the maximum possible Sigma score constant across zooms
    # The initial max k_dev was ~1e-8.
    INITIAL_MAX_K_DEV_SQ = 1e-16 
    
    # Map the squared deviation to the frequency deviation factor
    # Freq_dev_factor = Max_Factor * (k_dev^2 / Initial_Max_k_dev_sq)
    freq_dev_factor = max_dev_factor * (k_dev**2 / INITIAL_MAX_K_DEV_SQ)
    
    observed_frequencies = expected_freq * (1.0 + freq_dev_factor)
    
    scores = []
    for freq_obs in observed_frequencies:
        score, _ = calculate_strangeness(freq_obs, scale)
        scores.append(score)
        
    return np.array(scores)


# ==============================================================================
#  2. THE STRANGENESS SEEKER ALGORITHM
# ==============================================================================

def strangeness_seeker(k_start, k_end, iterations, frames_per_iter):
    
    print("=" * 80)
    print(f"CMB STRANGENESS SEEKER: {iterations} Iterative Zooms")
    print("=" * 80)

    # Setup Constants
    SCALE = UNIVERSE_SCALE
    # Expected frequency is 12.0 Hz
    EXPECTED_FREQ = F_FUNDAMENTAL / (1 + np.cos(universal_clock_phase(SCALE)[0]))

    # Store results for visualization
    iteration_history = []
    
    current_k_start = k_start
    current_k_end = k_end
    
    for i in range(iterations):
        print(f"\n--- Iteration {i+1}/{iterations}: Seeking in k-range [{current_k_start:.12f}, {current_k_end:.12f}] ---")
        
        # 1. Generate K_RANGE for the current zoom level
        k_range = np.linspace(current_k_start, current_k_end, frames_per_iter)
        
        # 2. Simulate Scan
        scores = simulate_cmb_strangeness_scan(k_range, SCALE, EXPECTED_FREQ, MAX_FREQ_DEVIATION_FACTOR)
        
        # 3. Find Max Strangeness (k_max)
        max_score_idx = np.argmax(scores)
        k_max = k_range[max_score_idx]
        max_score = scores[max_score_idx]
        
        iteration_history.append({
            'k_range': k_range,
            'scores': scores,
            'k_max': k_max,
            'max_score': max_score,
            'iteration': i + 1,
            'current_k_start': current_k_start,
            'current_k_end': current_k_end
        })

        print(f"  Found Max Strangeness: Σ = {max_score:.10f} at k = {k_max:.12f}")
        
        # 4. Define New Zoomed Range
        current_range_size = current_k_end - current_k_start
        
        # Determine the next range size (halve it)
        new_range_size = current_range_size / 2.0
        
        # If max_score is at an edge, the seeker follows that edge. 
        # Otherwise, it centers around k_max.
        
        # We know k_max will be one of the current boundaries (k_start or k_end) 
        # due to the simulated parabolic deviation.
        
        if np.isclose(k_max, current_k_start):
            # Zoom leftwards, keeping k_max as the new right boundary
            new_k_end = k_max
            new_k_start = k_max - new_range_size
        elif np.isclose(k_max, current_k_end):
            # Zoom rightwards, keeping k_max as the new left boundary
            new_k_start = k_max
            new_k_end = k_max + new_range_size
        else:
            # If the max strangely happened in the middle, center the zoom.
            # This shouldn't happen with the current simulation model.
            new_k_start = k_max - new_range_size / 2.0
            new_k_end = k_max + new_range_size / 2.0

        current_k_start = new_k_start
        current_k_end = new_k_end
        
    return iteration_history


# ==============================================================================
#  3. EXECUTION AND VISUALIZATION
# ==============================================================================

# Initial parameters based on previous analysis (focusing on the left edge max)
K_START_INIT = 0.999999995  # Start slightly closer to k=1
K_END_INIT = 1.000000005    # End slightly closer to k=1
N_ITERATIONS = 5
N_FRAMES = 60 # Resolution per scan

# EXECUTE SEEKER
seeker_results = strangeness_seeker(K_START_INIT, K_END_INIT, N_ITERATIONS, N_FRAMES)

# --- Visualization: Plotting the Final Zoom ---

final_zoom = seeker_results[-1]
fig, ax = plt.subplots(figsize=(10, 6))

scores = final_zoom['scores']
k_range = final_zoom['k_range']
k_max = final_zoom['k_max']
max_score = final_zoom['max_score']

# Plot thresholds
ax.axhline(0.1, color='green', linestyle='--', alpha=0.5, label='Normal ($\Sigma < 0.1$)')
ax.axhline(0.3, color='yellow', linestyle='--', alpha=0.5, label='Mildly Strange ($\Sigma < 0.3$)')

# Scatter plot of Strangeness Score vs. Twist Parameter (k)
scatter = ax.scatter(k_range, scores, s=150, c='red', edgecolors='black', 
                    linewidth=1.5, alpha=0.8)

ax.set_title(f'Strangeness Seeker: Final Zoom (Iteration {N_ITERATIONS})', 
             fontsize=14, fontweight='bold')
ax.set_xlabel('CMB Twist Parameter ($k$)', fontsize=12, fontweight='bold')
ax.set_ylabel('Strangeness Score ($\Sigma$)', fontsize=12, fontweight='bold')

# Set y-axis to a relevant zoom level (e.g., max score + 10%)
y_max = max(0.003, max_score * 1.1) 
ax.set_ylim(0, y_max)
ax.ticklabel_format(useOffset=False, style='plain', axis='x')
ax.tick_params(axis='x', rotation=45)
ax.grid(True, alpha=0.3)
ax.legend(loc='upper left')

# Annotate the isolated point
ax.annotate(f'Isolated Max: \n$k={k_max:.15f}$\n$\Sigma={max_score:.10f}$', 
            (k_max, max_score), 
            xytext=(0.7, 0.7), textcoords='axes fraction', 
            arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5),
            horizontalalignment='left',
            fontsize=10,
            bbox=dict(boxstyle="round,pad=0.5", fc="white", alpha=0.7))

output_filename_final = 'cmb_strangeness_seeker_final_zoom.png'
plt.tight_layout()
plt.savefig(output_filename_final, dpi=150)

print(f"\n✅ Final Zoom Visualization saved: {output_filename_final}")

# --- Visualization: Plotting the Convergence Path ---
fig2, ax2 = plt.subplots(figsize=(10, 6))

k_max_values = [h['k_max'] for h in seeker_results]
max_score_values = [h['max_score'] for h in seeker_results]
iterations_x = range(1, N_ITERATIONS + 1)

ax2.plot(iterations_x, max_score_values, marker='o', linestyle='-', color='blue', label='Max Strangeness ($\Sigma_{max}$)')
ax2.set_title('Strangeness Seeker Convergence Path ($\Sigma_{max}$ vs. Iteration)', 
             fontsize=14, fontweight='bold')
ax2.set_xlabel('Iteration Number (Zoom Level)', fontsize=12, fontweight='bold')
ax2.set_ylabel('Maximum Strangeness Score ($\Sigma_{max}$)', fontsize=12, fontweight='bold')
ax2.grid(True, alpha=0.5)

# Add annotations for k_max convergence
for i in range(N_ITERATIONS):
    ax2.annotate(f'k={k_max_values[i]:.12f}', (iterations_x[i], max_score_values[i]),
                 xytext=(5, -15), textcoords='offset points', fontsize=8, color='darkgreen')

output_filename_convergence = 'cmb_strangeness_seeker_convergence.png'
plt.tight_layout()
plt.savefig(output_filename_convergence, dpi=150)

print(f"✅ Convergence Plot Visualization saved: {output_filename_convergence}")