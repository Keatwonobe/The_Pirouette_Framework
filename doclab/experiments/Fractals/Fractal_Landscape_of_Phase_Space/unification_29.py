import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# PIROUETTE FRAMEWORK: THE QUANTIZATION CHECK
# --------------------------------------------------
# We analyze the "Fractal Torus" to see if it obeys
# Quantum mechanics. We measure:
# 1. Toroidal Winding (Big Loop)
# 2. Poloidal Winding (Little Loop/Twist)
# 3. The Ratio (The Spin)
# --------------------------------------------------

TWIST = 3.8
GAMMA = 0.05
DT = 0.005
STEPS = 50000
STABILIZE = 10000

def get_force_vectorized(m, lam):
    # --- Standard Pirouette Physics ---
    F_teal_m = -(m + 0.866) 
    F_teal_lam = -(lam - 0.5)
    F_red_m = -(m - 0.0)
    p_violation = TWIST * np.sin(m * 2.5) 
    F_red_lam = -(lam + 1.0) + p_violation
    sum_m = (F_teal_m + F_red_m)
    sum_lam = (F_teal_lam + F_red_lam)
    magnitude = np.sqrt(sum_m**2 + sum_lam**2)
    scaling_factor = np.sqrt(magnitude)
    F_gold_m = sum_m * scaling_factor
    F_gold_lam = sum_lam * scaling_factor
    
    # Weights
    angle = np.degrees(np.arctan2(lam, m)) % 360
    diff_g = np.abs(angle - 30); diff_g = np.minimum(diff_g, 360-diff_g)
    w_gold = np.exp(-(diff_g/80)**2)
    diff_t = np.abs(angle - 150); diff_t = np.minimum(diff_t, 360-diff_t)
    w_teal = np.exp(-(diff_t/80)**2)
    diff_r = np.abs(angle - 270); diff_r = np.minimum(diff_r, 360-diff_r)
    w_red = np.exp(-(diff_r/80)**2)
    
    tot = w_gold + w_teal + w_red + 1e-6
    nw_red, nw_teal, nw_gold = w_red/tot, w_teal/tot, w_gold/tot
    
    Fm = (nw_teal * F_teal_m + nw_red * F_red_m + nw_gold * F_gold_m)
    Flam = (nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam)
    
    return Fm, Flam, nw_red

def run_winding_check():
    print("Measuring Particle Topology (Spin)...")
    
    # Coordinate from your stable particle
    m, lam = -1.8, 0.0
    pm, plam = 0.0, 2.0 
    
    # Stabilization
    for _ in range(STABILIZE):
        Fm, Flam, w_red = get_force_vectorized(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag
        m += DT * pm
        lam += DT * plam
        
        Fm, Flam, w_red = get_force_vectorized(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag

    # Measurement Phase
    print("Counting Loops...")
    
    phi_history = []   # Angle in the plane (Big Loop)
    theta_history = [] # Twist angle (Momentum twist)
    
    total_phi = 0.0
    total_theta = 0.0
    
    prev_phi = np.arctan2(lam, m)
    # We define theta as the angle of the velocity vector (Spin)
    prev_theta = np.arctan2(plam, pm) 
    
    for i in range(STEPS):
        Fm, Flam, w_red = get_force_vectorized(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag
        m += DT * pm
        lam += DT * plam
        
        # Second half step
        Fm, Flam, w_red = get_force_vectorized(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag
        
        # --- TOPOLOGY MATH ---
        # 1. Toroidal Angle (Space)
        curr_phi = np.arctan2(lam, m)
        dphi = curr_phi - prev_phi
        # Unwrap
        if dphi > np.pi: dphi -= 2*np.pi
        if dphi < -np.pi: dphi += 2*np.pi
        total_phi += dphi
        prev_phi = curr_phi
        
        # 2. Poloidal Angle (Momentum/Spin)
        curr_theta = np.arctan2(plam, pm)
        dtheta = curr_theta - prev_theta
        if dtheta > np.pi: dtheta -= 2*np.pi
        if dtheta < -np.pi: dtheta += 2*np.pi
        total_theta += dtheta
        prev_theta = curr_theta
        
        if i % 100 == 0:
            phi_history.append(total_phi / (2*np.pi))
            theta_history.append(total_theta / (2*np.pi))

    # Calculate Ratios
    # Spin = Twist / Orbit
    # A spin 1/2 particle twists 720 degrees (2 turns) to do 1 orbit.
    
    orbits = abs(total_phi) / (2*np.pi)
    twists = abs(total_theta) / (2*np.pi)
    ratio = twists / orbits
    
    print("-" * 40)
    print("QUANTIZATION RESULTS")
    print("-" * 40)
    print(f"Total Spatial Orbits: {orbits:.2f}")
    print(f"Total Momentum Twists: {twists:.2f}")
    print(f"Winding Ratio (Spin): {ratio:.4f}")
    
    # Interpretation
    if 0.9 < ratio < 1.1:
        print(">> IDENTIFICATION: BOSON (Integer Spin 1)")
    elif 1.9 < ratio < 2.1:
        print(">> IDENTIFICATION: FERMION (Half-Integer Spin 1/2 equiv)")
        print("   (Note: In this geometric projection, Ratio 2:1 often maps to Spin 1/2)")
    elif 0.45 < ratio < 0.55:
        print(">> IDENTIFICATION: EXOTIC (Spin 2?)")
    else:
        print(">> IDENTIFICATION: FRACTIONAL/ANYON")
        
    print("-" * 40)
    
    # Plotting the Winding
    plt.figure(figsize=(10, 6), facecolor='black')
    plt.plot(phi_history, theta_history, color='lime', linewidth=2)
    plt.plot(phi_history, [x * ratio for x in phi_history], color='white', linestyle='--', alpha=0.5, label=f'Linear Fit (Slope={ratio:.2f})')
    
    plt.title(f"The Winding Number: Topology of the Particle\nSlope = {ratio:.4f}", color='white', fontsize=14)
    plt.xlabel("Spatial Turns (Orbits)", color='white')
    plt.ylabel("Internal Twists (Spin)", color='white')
    plt.grid(color='#333333', alpha=0.5)
    plt.tick_params(colors='white')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('particle_winding_number.png')
    plt.show()

if __name__ == "__main__":
    run_winding_check()