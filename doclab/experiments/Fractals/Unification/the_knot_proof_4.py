import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# --- Configuration ---
STEPS = 500
DT = 0.05
G_BASE = 1.0           # Base gravitational constant
G_PHASE = 5.0          # Strength of the "Phase Gravity" boost
RESONANCE_WIDTH = 0.2  # How strict the harmonic matching is
DAMPING = 0.01         # Energy loss (optional)

# --- The Physics Engine ---
def compute_phase_gravity(pos1, pos2, w1, w2, phase1, phase2):
    """
    Calculates the force between two twisting travelers.
    The force is amplified by 'Phase Resonance'.
    """
    r_vec = pos2 - pos1
    r = np.linalg.norm(r_vec)
    r_safe = max(r, 0.5) # Prevent singularity
    
    # 1. Base Spatial Attraction (Standard Gravity / Vacuum Tension)
    f_base_mag = G_BASE / (r_safe**2)
    
    # 2. Harmonic Resonance Factor (The "Boost")
    # We look for simple integer ratios: 1:1, 2:1, 3:2 etc.
    # But specifically, the user mentioned "opposite direction" (w1 = -w2).
    # So we check if w1 + w2 is close to 0 (Fundamental resonance)
    # Or if n*w1 + m*w2 ~ 0 for harmonics.
    
    # Let's assume the "Fundamental" opposite match is the strongest.
    # Deviation from perfect anti-parallel twist
    twist_sum = w1 + w2 
    
    # Gaussian resonance curve: Peaks when w1 == -w2
    resonance = np.exp(-(twist_sum**2) / (2 * RESONANCE_WIDTH**2))
    
    # 3. Instantaneous Phase Alignment (The "Phase Locking")
    # Do phases line up constructively? cos(phi1 - phi2)
    # If they are counter-rotating, phase diff changes rapidly, 
    # but the *interaction* might be rectified (always attractive).
    # Let's model "Phase Gravity" as an efficiency multiplier that relies on Resonance.
    
    # Efficiency is high when Resonance is high.
    efficiency = 1.0 + (G_PHASE * resonance)
    
    # Total Phase Gravity Force
    f_total_mag = f_base_mag * efficiency
    
    force_vec = (r_vec / r_safe) * f_total_mag
    
    return force_vec, efficiency

# --- Simulation State ---
# Two Travelers
# Traveler 1: Twist +3.0
p1 = np.array([-4.0, 1.0, 0.0])
v1 = np.array([0.5, 0.5, 0.0])
w1 = 3.0
phi1 = 0.0

# Traveler 2: Twist -3.0 (Perfect Resonance start)
p2 = np.array([4.0, -1.0, 0.0])
v2 = np.array([-0.5, -0.5, 0.0])
w2 = -3.0  # Try changing this to see resonance break (e.g. -2.5)
phi2 = np.pi # Start out of phase

history = []
efficiency_history = []

# --- Run Loop ---
for i in range(STEPS):
    # 1. Calculate Force
    force, eff = compute_phase_gravity(p1, p2, w1, w2, phi1, phi2)
    efficiency_history.append(eff)
    
    # 2. Apply Acceleration
    # Mass = 1 for simplicity
    v1 += force * DT
    v2 -= force * DT # Newton's 3rd
    
    # Damping (Energy Transfer Loss)
    v1 *= (1 - DAMPING)
    v2 *= (1 - DAMPING)
    
    # 3. Update Position
    p1 += v1 * DT
    p2 += v2 * DT
    
    # 4. Update Phase
    phi1 += w1 * DT
    phi2 += w2 * DT
    
    # 5. Drift w2 slightly to show resonance sensitivity (Optional simulation of instability)
    # Un-comment to see them "lose lock"
    # w2 += np.sin(i * 0.05) * 0.01 
    
    history.append((p1.copy(), p2.copy()))

# --- Visualization ---
fig = plt.figure(figsize=(12, 6))

# Plot 1: Trajectories in Phase Space (X-Y Plane)
ax1 = fig.add_subplot(1, 2, 1)
hist_p1 = np.array([h[0] for h in history])
hist_p2 = np.array([h[1] for h in history])

ax1.plot(hist_p1[:,0], hist_p1[:,1], 'b-', label='Traveler (+w)')
ax1.plot(hist_p2[:,0], hist_p2[:,1], 'r-', label='Traveler (-w)')
ax1.scatter([p1[0]], [p1[1]], c='b', s=100)
ax1.scatter([p2[0]], [p2[1]], c='r', s=100)

# Draw "Manifold Tension" lines between them at intervals
for j in range(0, STEPS, 50):
    p1_j = hist_p1[j]
    p2_j = hist_p2[j]
    # Color depends on efficiency at that moment
    eff_j = efficiency_history[j]
    # Normalize color
    alpha = min((eff_j - 1.0) / G_PHASE, 1.0) 
    ax1.plot([p1_j[0], p2_j[0]], [p1_j[1], p2_j[1]], 'g--', alpha=0.3 + 0.7*alpha)

ax1.set_title("Phase Gravity Trajectories\n(Green intensity = Resonance Efficiency)")
ax1.set_xlabel("X Position")
ax1.set_ylabel("Y Position")
ax1.legend()
ax1.grid(True)

# Plot 2: Efficiency (The "Boost") vs Time
ax2 = fig.add_subplot(1, 2, 2)
ax2.plot(efficiency_history, 'g-', lw=2)
ax2.set_title("Energy Transfer Efficiency (Phase Resonance)")
ax2.set_xlabel("Time Step")
ax2.set_ylabel("Gravitational Multiplier")
ax2.grid(True)

plt.tight_layout()
plt.savefig('phase_gravity_model.png')
plt.show()