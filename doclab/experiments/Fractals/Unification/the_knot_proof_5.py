import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# --- Configuration ---
STEPS = 1000
DT = 0.01
RADIUS = 20.0          # Size of the "Universe" Sphere
G_PHASE = 8.0          # Strong Phase Gravity
STRESS_COEFF = 3.0     # Speed increases bond
MANIFOLD_NOISE = 0.5   # The "Cracks" and "Seams" (Potentials)
SPEED_HIGH = 15.0
SPEED_LOW = 2.0

# --- Physics Engine ---
def get_manifold_noise(pos):
    """
    Simulates the 'Potentials' and 'Knots' already in the manifold.
    Returns a random force vector based on position (deterministic noise).
    """
    # Simple deterministic hash-like noise
    np.random.seed(int(abs(pos[0]*10 + pos[1]*5 + pos[2]))) 
    noise = np.random.uniform(-1, 1, 3)
    return noise * MANIFOLD_NOISE

def compute_physics(pos1, pos2, vel1, vel2, w1, w2):
    # 1. Phase Gravity (The Attraction)
    r_vec = pos2 - pos1
    r = np.linalg.norm(r_vec)
    r_safe = max(r, 0.1)
    
    # Resonance (Anti-parallel twist match)
    twist_sum = w1 + w2 
    resonance = np.exp(-(twist_sum**2) / 0.1)
    
    # Relativistic Stress
    speed = (np.linalg.norm(vel1) + np.linalg.norm(vel2)) / 2.0
    stress_factor = 1.0 + STRESS_COEFF * (speed**2)
    
    # Force Magnitude
    f_mag = (G_PHASE * resonance * stress_factor) / (r_safe**2)
    force_vec = (r_vec / r_safe) * f_mag
    
    # 2. Manifold Resistance (The "Cracks")
    # High speed should cut through this (Momentum vs Force)
    noise1 = get_manifold_noise(pos1)
    noise2 = get_manifold_noise(pos2)
    
    return force_vec, f_mag, noise1, noise2

# --- Simulation Runner ---
def run_simulation(speed_mode):
    # Initialize at Sphere Surface (Opposite sides)
    theta = np.pi / 4 # Slightly offset launch angle (The "Crooked" factor)
    
    # Traveler 1 (Forward Time, +w)
    p1 = np.array([-RADIUS * np.cos(theta), -RADIUS * np.sin(theta), 0.0])
    # Aimed mostly inward but with some skew
    v1 = np.array([speed_mode, speed_mode * 0.2, 0.0]) 
    w1 = 5.0
    
    # Traveler 2 (Retrograde Time, -w)
    p2 = np.array([RADIUS * np.cos(theta), RADIUS * np.sin(theta), 0.0])
    v2 = np.array([-speed_mode, -speed_mode * 0.2, 0.0])
    w2 = -5.0
    
    path1, path2 = [], []
    strengths = []
    
    for _ in range(STEPS):
        path1.append(p1.copy())
        path2.append(p2.copy())
        
        # Physics
        force_bond, bond_strength, n1, n2 = compute_physics(p1, p2, v1, v2, w1, w2)
        strengths.append(bond_strength)
        
        # Update (Force = Mass * Accel, Mass=1)
        # Apply Bond Force
        v1 += force_bond * DT
        v2 -= force_bond * DT
        
        # Apply Manifold Noise (Perturbation)
        # Note: Noise force is constant, but effect on trajectory depends on momentum
        v1 += n1 * DT
        v2 += n2 * DT
        
        # Move
        p1 += v1 * DT
        p2 += v2 * DT
        
        # Check boundary (Stop if they exit sphere or merge)
        if np.linalg.norm(p1) > RADIUS * 1.5: break
        if np.linalg.norm(p1 - p2) < 0.5: break # Merged
        
    return np.array(path1), np.array(path2), np.array(strengths)

# --- Execute ---
print("Simulating Low Speed Run...")
p1_low, p2_low, str_low = run_simulation(SPEED_LOW)

print("Simulating High Speed Run...")
p1_high, p2_high, str_high = run_simulation(SPEED_HIGH)

# --- Plotting ---
fig = plt.figure(figsize=(14, 6))

# 1. Trajectories (Top Down)
ax1 = fig.add_subplot(1, 2, 1)
# Draw Sphere Boundary
circle = plt.Circle((0, 0), RADIUS, color='gray', fill=False, linestyle='--', alpha=0.5, label='Universe Boundary')
ax1.add_artist(circle)

# Low Speed
ax1.plot(p1_low[:,0], p1_low[:,1], 'r--', alpha=0.5, label=f'Low Speed ({SPEED_LOW})')
ax1.plot(p2_low[:,0], p2_low[:,1], 'b--', alpha=0.5)

# High Speed
ax1.plot(p1_high[:,0], p1_high[:,1], 'r-', linewidth=2, label=f'High Speed ({SPEED_HIGH})')
ax1.plot(p2_high[:,0], p2_high[:,1], 'b-', linewidth=2)

ax1.set_title("Trajectory Straightness: Inertia vs Manifold Noise")
ax1.set_xlim(-RADIUS-2, RADIUS+2)
ax1.set_ylim(-RADIUS-2, RADIUS+2)
ax1.legend()
ax1.grid(True)

# 2. Pairing Strength
ax2 = fig.add_subplot(1, 2, 2)
ax2.plot(str_high, 'gold', label='High Speed Bond')
ax2.plot(str_low, 'purple', label='Low Speed Bond')
ax2.set_title("Pairing Strength (Phase Gravity + Stress)")
ax2.set_xlabel("Time Step")
ax2.set_ylabel("Bond Force (Log Scale)")
ax2.set_yscale('log')
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.savefig('spherical_pairing_proof.png')