import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# PIROUETTE FRAMEWORK: THE QUANTUM HALL SCAN
# --------------------------------------------------
# We suspect that the "Spin" (Winding Ratio) is
# quantized. We will scan the "Twist" parameter
# (The Fundamental Constant) to see if the Spin
# "locks" onto specific rational numbers (Plateaus).
# --------------------------------------------------

START_TWIST = 3.0
END_TWIST = 5.0
SAMPLES = 40  # Resolution of the scan
GAMMA = 0.05
DT = 0.01     # Faster integration for scanning
STEPS = 8000  # Short burst measurements

def get_winding_ratio(twist_val):
    # Local Physics Function with variable Twist
    def get_force_local(m, lam):
        F_teal_m = -(m + 0.866) 
        F_teal_lam = -(lam - 0.5)
        F_red_m = -(m - 0.0)
        p_violation = twist_val * np.sin(m * 2.5) # <--- VARIABLE TWIST
        F_red_lam = -(lam + 1.0) + p_violation
        
        sum_m = (F_teal_m + F_red_m)
        sum_lam = (F_teal_lam + F_red_lam)
        mag = np.sqrt(sum_m**2 + sum_lam**2)
        scale = np.sqrt(mag)
        F_gold_m = sum_m * scale
        F_gold_lam = sum_lam * scale
        
        angle = np.degrees(np.arctan2(lam, m)) % 360
        diff_g = np.minimum(np.abs(angle - 30), 360-np.abs(angle - 30))
        w_gold = np.exp(-(diff_g/80)**2)
        diff_t = np.minimum(np.abs(angle - 150), 360-np.abs(angle - 150))
        w_teal = np.exp(-(diff_t/80)**2)
        diff_r = np.minimum(np.abs(angle - 270), 360-np.abs(angle - 270))
        w_red = np.exp(-(diff_r/80)**2)
        
        tot = w_gold + w_teal + w_red + 1e-6
        nw_red, nw_teal, nw_gold = w_red/tot, w_teal/tot, w_gold/tot
        
        Fm = (nw_teal * F_teal_m + nw_red * F_red_m + nw_gold * F_gold_m)
        Flam = (nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam)
        return Fm, Flam, nw_red

    # Run Simulation
    m, lam = -1.8, 0.0
    pm, plam = 0.0, 2.0
    
    # Burn-in
    for _ in range(2000):
        Fm, Flam, w_red = get_force_local(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag
        m += DT * pm
        lam += DT * plam
        Fm, Flam, w_red = get_force_local(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag

    # Measure
    total_phi = 0.0
    total_theta = 0.0
    prev_phi = np.arctan2(lam, m)
    prev_theta = np.arctan2(plam, pm)
    
    for _ in range(STEPS):
        Fm, Flam, w_red = get_force_local(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag
        m += DT * pm
        lam += DT * plam
        
        Fm, Flam, w_red = get_force_local(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag
        
        curr_phi = np.arctan2(lam, m)
        dphi = curr_phi - prev_phi
        if dphi > np.pi: dphi -= 2*np.pi
        if dphi < -np.pi: dphi += 2*np.pi
        total_phi += dphi
        prev_phi = curr_phi
        
        curr_theta = np.arctan2(plam, pm)
        dtheta = curr_theta - prev_theta
        if dtheta > np.pi: dtheta -= 2*np.pi
        if dtheta < -np.pi: dtheta += 2*np.pi
        total_theta += dtheta
        prev_theta = curr_theta
        
    if abs(total_phi) < 1e-3: return 0 # Avoid divide by zero if particle dies
    return abs(total_theta) / abs(total_phi)

def run_quantum_hall_scan():
    print(f"Scanning Fundamental Constants (Twist {START_TWIST} -> {END_TWIST})...")
    
    twists = np.linspace(START_TWIST, END_TWIST, SAMPLES)
    ratios = []
    
    for i, t in enumerate(twists):
        r = get_winding_ratio(t)
        ratios.append(r)
        print(f"Twist: {t:.2f} | Spin Ratio: {r:.4f}")
        
    # ----------------------------------------
    # PLOTTING
    # ----------------------------------------
    plt.figure(figsize=(12, 6), facecolor='black')
    ax = plt.gca()
    ax.set_facecolor('black')
    
    # The Main Data Line
    ax.plot(twists, ratios, 'o-', color='cyan', linewidth=2, markersize=5)
    
    # Horizontal Reference Lines (The Plateaus we hope for)
    ax.axhline(y=1.0, color='white', linestyle='--', alpha=0.3, label='Spin 1 (Boson)')
    ax.axhline(y=0.5, color='lime', linestyle='--', alpha=0.3, label='Spin 1/2 (Fermion)')
    ax.axhline(y=0.85, color='gold', linestyle=':', alpha=0.3, label='Your Anyon')
    
    ax.set_title("The Quantization of Spin: Searching for Integer Plateaus", color='white', fontsize=14)
    ax.set_xlabel("Vacuum Twist Parameter (Interaction Strength)", color='white')
    ax.set_ylabel("Emergent Spin (Winding Ratio)", color='white')
    
    ax.legend(facecolor='black', labelcolor='white')
    ax.grid(color='#333333', alpha=0.5)
    ax.tick_params(colors='white')
    
    plt.tight_layout()
    plt.savefig('quantum_hall_scan.png')
    plt.show()

if __name__ == "__main__":
    run_quantum_hall_scan()