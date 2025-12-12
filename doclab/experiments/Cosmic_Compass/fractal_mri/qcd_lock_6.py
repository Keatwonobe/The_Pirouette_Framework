import numpy as np
import matplotlib.pyplot as plt

def get_neutrality_force_spin(m, lam, sigma=1.0):
    # --- Re-implementing the "Free Rule" Physics ---
    
    # 1. Teal (EM): Harmonic Attraction
    F_teal_m = -(m + 0.866) 
    F_teal_lam = -(lam - 0.5)

    # 2. Red (Weak): Parity Violated Attraction
    # The asymmetry is key here. It creates the "limp" that might induce Spin 1/2.
    F_red_m = -(m - 0.0)
    # Stronger parity kick to test the "Double Cover" hypothesis
    p_violation = 0.8 * np.sin(m * 3) 
    F_red_lam = -(lam + 1.0) + p_violation

    # 3. Gold (Strong): The Neutrality Constraint
    # F_gold = -(F_teal + F_red)
    F_gold_m = -(F_teal_m + F_red_m)
    F_gold_lam = -(F_teal_lam + F_red_lam)
    
    # Basin Weighting
    angle = np.degrees(np.arctan2(lam, m)) % 360
    
    def gaussian(x, mu, sig):
        diff = np.minimum(np.abs(x - mu), 360 - np.abs(x - mu))
        return np.exp(-(diff/sig)**2)

    w_gold = gaussian(angle, 30, 60)
    w_teal = gaussian(angle, 150, 60)
    w_red = gaussian(angle, 270, 60)
    
    tot = w_gold + w_teal + w_red + 1e-6
    
    # Total Force
    Fm = (w_teal * F_teal_m + w_red * F_red_m + w_gold * F_gold_m) / tot
    Flam = (w_teal * F_teal_lam + w_red * F_red_lam + w_gold * F_gold_lam) / tot
    
    return Fm, Flam

def leapfrog_spin(m, lam, pm, plam, dt):
    Fm, Flam = get_neutrality_force_spin(m, lam)
    
    pm_h = pm + 0.5 * dt * Fm
    plam_h = plam + 0.5 * dt * Flam
    
    m_n = m + dt * pm_h
    lam_n = lam + dt * plam_h
    
    Fm_n, Flam_n = get_neutrality_force_spin(m_n, lam_n)
    
    pm_n = pm_h + 0.5 * dt * Fm_n
    plam_n = plam_h + 0.5 * dt * Flam_n
    
    return m_n, lam_n, pm_n, plam_n

def measure_winding_number():
    # Setup
    dt = 0.02
    steps = 4000
    
    # Initial Condition (Start near the Teal basin)
    m, lam = -0.5, 0.5
    pm, plam = 0.4, -0.2 # Give it some orbital energy
    
    # Tracking
    phases = []
    times = []
    states = [] # To check recurrence
    
    prev_angle = np.arctan2(lam, m)
    total_angle = 0.0
    lap_counter = 0
    
    print("Running 'Spinometer' Analysis...")
    print(f"{'Event':<15} | {'Time':<8} | {'Total Angle':<12} | {'State Match (Metric)':<20}")
    print("-" * 65)
    
    for i in range(steps):
        t = i * dt
        
        # Save state for comparison
        # State vector S = [m, lam, pm, plam]
        current_state = np.array([m, lam, pm, plam])
        
        # Integrate
        m, lam, pm, plam = leapfrog_spin(m, lam, pm, plam, dt)
        
        # Calculate Phase Accumulation
        curr_angle = np.arctan2(lam, m)
        delta = curr_angle - prev_angle
        
        # Unwrap phase (handle the -pi to pi jump)
        if delta > np.pi: delta -= 2*np.pi
        if delta < -np.pi: delta += 2*np.pi
        
        total_angle += delta
        prev_angle = curr_angle
        
        # Check for Laps (Crossings of 360 degrees)
        # We detect when total_angle passes a multiple of 2*pi
        current_laps = int(abs(total_angle) / (2*np.pi))
        
        if current_laps > lap_counter:
            lap_counter = current_laps
            
            # ANALYZE THE RETURN STATE
            # Compare current state to Initial State (Index 0)
            # Metric: Euclidean distance in Phase Space
            # If distance is small, it's a full recurrence.
            # If distance is large, it hasn't truly reset.
            
            initial_state = np.array([-0.5, 0.5, 0.4, -0.2])
            dist = np.linalg.norm(current_state - initial_state)
            
            match_quality = "PERFECT RESET" if dist < 0.2 else "MISMATCH (Twisted)"
            
            print(f"Lap {lap_counter:<11} | {t:<8.2f} | {np.degrees(total_angle):<12.1f} | {dist:<8.4f} ({match_quality})")

    return total_angle

if __name__ == "__main__":
    final_phase = measure_winding_number()
    n = abs(final_phase) / (2*np.pi)
    print("-" * 65)
    print(f"Total Winding: {n:.4f}")
    print(f"Estimated Spin S = {n / 2:.2f} ?? (If 1 orbit is a 'cycle')")