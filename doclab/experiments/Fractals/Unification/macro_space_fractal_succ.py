import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------
# We simulate a "Cloud" of test particles to measure the geometry's contraction.
PARTICLE_COUNT = 5000
INIT_RADIUS = 3.0
DT = 0.05 
STEPS = 1000  # Enough time to settle
GAMMA = 0.02  # The friction/drain rate from the Ripple script

def get_force_batch(m, lam, twist):
    # Vectorized Physics
    F_teal_m = -(m + 0.866) 
    F_teal_lam = -(lam - 0.5)

    F_red_m = -m 
    p_violation = twist * np.sin(m * 2.5) 
    F_red_lam = -(lam + 1.0) + p_violation

    sum_m = (F_teal_m + F_red_m)
    sum_lam = (F_teal_lam + F_red_lam)
    mag_sq = sum_m**2 + sum_lam**2
    mag = np.sqrt(mag_sq)
    scale = np.sqrt(mag) 
    
    F_gold_m = sum_m * scale
    F_gold_lam = sum_lam * scale
    
    # Weights (Simplified Gaussian for speed)
    angle = np.degrees(np.arctan2(lam, m)) % 360
    
    # Vectorized weight calc
    def w_calc(a, t):
        d = np.abs(a - t)
        d = np.minimum(d, 360.0 - d)
        return np.exp(-(d/80.0)**2)
    
    w_gold = w_calc(angle, 30.0)
    w_teal = w_calc(angle, 150.0)
    w_red = w_calc(angle, 270.0)
    
    tot = w_gold + w_teal + w_red + 1e-6
    nw_red = w_red / tot
    nw_teal = w_teal / tot
    nw_gold = w_gold / tot
    
    Fm = (nw_teal * F_teal_m + nw_red * F_red_m + nw_gold * F_gold_m)
    Flam = (nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam)
    
    return Fm, Flam, nw_red

def measure_contraction_rate(target_twist):
    """
    Experiment 1: The 'Inhale' Speed
    Tracks the Average Radius of the universe over time.
    """
    # Initialize random cloud
    theta = np.random.uniform(0, 2*np.pi, PARTICLE_COUNT)
    r = np.sqrt(np.random.uniform(0, INIT_RADIUS**2, PARTICLE_COUNT))
    m = r * np.cos(theta)
    lam = r * np.sin(theta)
    
    pm = np.zeros_like(m)
    plam = np.zeros_like(lam)
    
    history_radius = []
    
    for t in range(STEPS):
        # Measure current size
        avg_r = np.mean(np.sqrt(m**2 + lam**2))
        history_radius.append(avg_r)
        
        # Physics
        Fm, Flam, w_red = get_force_batch(m, lam, target_twist)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag
        m += DT * pm
        lam += DT * plam
        
    return history_radius

def find_the_click():
    """
    Experiment 2: The Parameter Sweep
    Looks for a sharp discontinuity in final compactness vs Twist.
    """
    twist_values = np.linspace(0.0, 5.0, 50) # Scan from 0 to 5
    final_sizes = []
    
    print("Scanning for the 'Click'...")
    for tw in twist_values:
        # Mini-sim for each twist
        # Same init every time for fairness
        np.random.seed(42) 
        theta = np.random.uniform(0, 2*np.pi, 500) # Fewer particles for sweep speed
        r = np.sqrt(np.random.uniform(0, INIT_RADIUS**2, 500))
        m = r * np.cos(theta)
        lam = r * np.sin(theta)
        pm = np.zeros_like(m)
        plam = np.zeros_like(lam)
        
        # Run to equilibrium
        for _ in range(800):
            Fm, Flam, w_red = get_force_batch(m, lam, tw)
            drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
            pm = (pm + 0.5 * DT * Fm) * drag
            plam = (plam + 0.5 * DT * Flam) * drag
            m += DT * pm
            lam += DT * plam
            
        final_avg_r = np.mean(np.sqrt(m**2 + lam**2))
        final_sizes.append(final_avg_r)
        
    return twist_values, final_sizes

# Run Experiments
print("Measuring the Inhale...")
inhale_curve = measure_contraction_rate(2.83814) # The Ripple Twist

print("Scanning for the Click...")
twist_axis, size_axis = find_the_click()

# Plot
fig, axes = plt.subplots(1, 2, figsize=(16, 6), facecolor='#050510')

# Plot 1: The Inhale (Time)
axes[0].set_facecolor('#050510')
axes[0].plot(inhale_curve, color='#00ffff', linewidth=2)
axes[0].set_title(f"The Inhale: Universe Contraction Rate\n(Twist=2.83, Gamma={GAMMA})", color='white', fontsize=14)
axes[0].set_ylabel("Average Radius (Compactness)", color='white')
axes[0].set_xlabel("Time Steps", color='white')
axes[0].grid(color='#333333')
axes[0].tick_params(colors='white')

# Calculate % shrinkage
start_size = inhale_curve[0]
end_size = inhale_curve[-1]
shrink_pct = (1 - end_size/start_size) * 100
axes[0].text(STEPS/2, (start_size+end_size)/2, f"Volume Loss: {shrink_pct:.1f}%", 
             color='yellow', fontsize=16, ha='center')

# Plot 2: The Click (Twist Sweep)
axes[1].set_facecolor('#050510')
axes[1].plot(twist_axis, size_axis, color='#ff00ff', linewidth=2, marker='o', markersize=4)
axes[1].set_title("Searching for the 'Click':\nFinal Compactness vs. Twist Strength", color='white', fontsize=14)
axes[1].set_ylabel("Equilibrium Radius", color='white')
axes[1].set_xlabel("Twist Parameter", color='white')
axes[1].grid(color='#333333')
axes[1].tick_params(colors='white')

# Highlight the sharp drops
# Find the steepest drop
diffs = np.diff(size_axis)
min_idx = np.argmin(diffs)
click_twist = twist_axis[min_idx]
axes[1].axvline(click_twist, color='white', linestyle='--', alpha=0.5)
axes[1].text(click_twist + 0.1, size_axis[min_idx], f"Possible SNAP\n@ {click_twist:.2f}", color='white')

plt.tight_layout()
plt.savefig('succ_analysis.png')
plt.show()