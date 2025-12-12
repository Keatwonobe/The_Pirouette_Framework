import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# PIROUETTE PRESSURE TEST 4: QUANTUM ENTANGLEMENT
# --------------------------------------------------
# We test for "Hidden Connections" (Pilot Waves).
# Two particles are simulated in isolation (no direct
# force), but they share the same dynamic vacuum.
#
# If they stay phase-locked despite the chaos,
# it proves that the Vacuum itself acts as the
# "Entanglement Bridge."
# --------------------------------------------------

# Constants
BASE_TWIST = 2.83814 
GAMMA = 0.02
DT = 0.005
STEPS = 5000

# The "Hidden Variable" (A background tremor in the vacuum)
# Frequency and Amplitude of the cosmic background noise
NOISE_FREQ = 0.05
NOISE_AMP = 0.002

def get_vacuum_force(m, lam, t, twist_current):
    # --- Physics with Dynamic Twist ---
    F_teal_m = -(m + 0.866) 
    F_teal_lam = -(lam - 0.5)

    F_red_m = -(m - 0.0)
    # The Twist is varying with time (Global Hidden Variable)
    p_violation = twist_current * np.sin(m * 2.5) 
    F_red_lam = -(lam + 1.0) + p_violation

    sum_m = (F_teal_m + F_red_m)
    sum_lam = (F_teal_lam + F_red_lam)
    mag = np.sqrt(sum_m**2 + sum_lam**2)
    scale = np.sqrt(mag)
    F_gold_m = sum_m * scale
    F_gold_lam = sum_lam * scale
    
    # Weights
    angle = np.degrees(np.arctan2(lam, m)) % 360
    diff_g = np.minimum(np.abs(angle - 30), 360-np.abs(angle - 30))
    w_gold = np.exp(-(diff_g/80)**2)
    diff_t = np.minimum(np.abs(angle - 150), 360-np.abs(angle - 150))
    w_teal = np.exp(-(diff_t/80)**2)
    diff_r = np.minimum(np.abs(angle - 270), 360-np.abs(angle - 270))
    w_red = np.exp(-(diff_r/80)**2)
    
    tot = w_gold + w_teal + w_red + 1e-6
    nw_red = w_red / tot
    nw_teal = w_teal / tot
    nw_gold = w_gold / tot
    
    Fm = (nw_teal * F_teal_m + nw_red * F_red_m + nw_gold * F_gold_m)
    Flam = (nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam)
    
    return Fm, Flam, nw_red

def run_entanglement_test():
    print("Running Entanglement Test (Shared Vacuum Dynamics)...")
    
    # Initialize Two Particles (Identical Start)
    # Alice
    m1, l1 = -1.8, 0.0
    pm1, pl1 = 0.0, 2.0 
    
    # Bob (Slightly perturbed initial condition to test robustness)
    m2, l2 = -1.8, 0.0001
    pm2, pl2 = 0.0, 2.0
    
    phase_diff = []
    
    print("Simulating isolated particles in shared vacuum...")
    
    for t_step in range(STEPS):
        t_time = t_step * DT
        
        # Calculate the Global Hidden Variable (The "Pulse" of the Universe)
        # Both particles "feel" this same twist value
        current_twist = BASE_TWIST + NOISE_AMP * np.sin(NOISE_FREQ * t_step)
        
        # --- Update Alice ---
        Fm1, Fl1, w1 = get_vacuum_force(m1, l1, t_time, current_twist)
        drag1 = 1.0 / (1.0 + 0.5 * DT * GAMMA * w1)
        pm1 = (pm1 + 0.5 * DT * Fm1) * drag1
        pl1 = (pl1 + 0.5 * DT * Fl1) * drag1
        m1 += DT * pm1
        l1 += DT * pl1
        
        # --- Update Bob ---
        Fm2, Fl2, w2 = get_vacuum_force(m2, l2, t_time, current_twist)
        drag2 = 1.0 / (1.0 + 0.5 * DT * GAMMA * w2)
        pm2 = (pm2 + 0.5 * DT * Fm2) * drag2
        pl2 = (pl2 + 0.5 * DT * Fl2) * drag2
        m2 += DT * pm2
        l2 += DT * pl2
        
        # Measure Phase Difference
        # Phase = Angle of velocity vector (The Spin Direction)
        phi1 = np.arctan2(pl1, pm1)
        phi2 = np.arctan2(pl2, pm2)
        diff = abs(phi1 - phi2)
        phase_diff.append(diff)

    # ----------------------------------------
    # PLOTTING
    # ----------------------------------------
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), facecolor='black')
    
    # Plot 1: The Hidden Variable
    time_axis = np.arange(STEPS) * DT
    noise_signal = BASE_TWIST + NOISE_AMP * np.sin(NOISE_FREQ * np.arange(STEPS))
    
    ax1.set_facecolor('black')
    ax1.plot(time_axis, noise_signal, color='grey', linestyle='--', label='Global Vacuum Tremor (Hidden Variable)')
    ax1.set_title("The Connected Universe", color='white', fontsize=14)
    ax1.set_ylabel("Vacuum Twist", color='white')
    ax1.legend(facecolor='black', labelcolor='white')
    ax1.grid(color='#333333', alpha=0.5)
    ax1.tick_params(colors='white')
    
    # Plot 2: Synchronization Error
    ax2.set_facecolor('black')
    ax2.plot(time_axis, phase_diff, color='cyan', linewidth=1.5)
    
    # If the line stays flat near zero, they are entangled.
    # If it diverges, chaos has broken the link.
    ax2.set_title("Entanglement Check: Phase Divergence", color='white', fontsize=14)
    ax2.set_xlabel("Time", color='white')
    ax2.set_ylabel("Phase Difference (Radians)", color='white')
    ax2.set_ylim(0, 0.1) # Zoom in on zero
    ax2.grid(color='#333333', alpha=0.5)
    ax2.tick_params(colors='white')
    
    final_err = phase_diff[-1]
    status = "LOCKED (ENTANGLED)" if final_err < 0.05 else "DECOHERENCE (CHAOS)"
    col = "lime" if final_err < 0.05 else "red"
    
    plt.figtext(0.5, 0.02, f"SYSTEM STATUS: {status}", ha="center", color=col, fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('entanglement_test.png')
    plt.show()

if __name__ == "__main__":
    run_entanglement_test()