import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# PIROUETTE PRESSURE TEST 3: THE HIERARCHY PROBLEM
# --------------------------------------------------
# We compare the strength of the "Electric" Force
# (Geometric Flux Repulsion) vs. the "Gravitational"
# Force (Vacuum Viscosity/Inertia).
#
# In the Standard Model, EM is 10^36 times stronger.
# In Pirouette, we check if the geometric mechanisms
# produce a natural hierarchy of scales.
# --------------------------------------------------

# Constants
TWIST = 2.83814 
GAMMA = 0.02     # The Higgs/Gravity Coupling
G_COUPLE = 0.8   # The Electric Coupling
DT = 0.005

def get_vacuum_weights(m, lam):
    """Calculates the local basin weights (The Higgs Field Texture)."""
    angle = np.degrees(np.arctan2(lam, m)) % 360
    
    diff_g = np.minimum(np.abs(angle - 30), 360-np.abs(angle - 30))
    w_gold = np.exp(-(diff_g/80)**2)
    
    diff_t = np.minimum(np.abs(angle - 150), 360-np.abs(angle - 150))
    w_teal = np.exp(-(diff_t/80)**2)
    
    diff_r = np.minimum(np.abs(angle - 270), 360-np.abs(angle - 270))
    w_red = np.exp(-(diff_r/80)**2)
    
    tot = w_gold + w_teal + w_red + 1e-6
    return w_red / tot, w_teal / tot, w_gold / tot # Return normalized weights

def run_hierarchy_test():
    print("Running Hierarchy Test (Force Strength Comparison)...")
    
    # 1. MEASURE GRAVITY (Inertial Drag)
    # Gravity in Pirouette is the resistance to motion through the Higgs field.
    # F_drag = Velocity * Gamma * Weight
    print("  Measuring Vacuum Drag (Mass/Gravity)...")
    
    velocities = np.linspace(0.1, 2.0, 50)
    drag_forces = []
    
    # We test at the stable particle location
    m_loc, l_loc = -1.8, 0.0 
    nw_red, _, _ = get_vacuum_weights(m_loc, l_loc)
    
    for v in velocities:
        # F_drag = v * (0.5 * Gamma * Weight) roughly from the integration step
        # Actually, drag reduces velocity: v_new = v_old * (1 / (1 + k))
        # The "Force" is approx v * k
        k = 0.5 * DT * GAMMA * nw_red
        f_drag_effective = v * k / DT # Convert back to Force units
        drag_forces.append(f_drag_effective)

    # 2. MEASURE ELECTROMAGNETISM (Flux Repulsion)
    # F_elec = G / r^2
    print("  Measuring Geometric Repulsion (Electric Force)...")
    
    distances = np.linspace(0.2, 2.0, 50) # Same range as "Velocity" conceptually
    elec_forces = []
    
    for r in distances:
        f_elec = G_COUPLE / (r**2)
        elec_forces.append(f_elec)
        
    # 3. COMPARE
    # We pick a "Typical" interaction
    typ_drag = np.mean(drag_forces)
    typ_elec = np.mean(elec_forces)
    ratio = typ_elec / typ_drag
    
    print("-" * 40)
    print("HIERARCHY RESULTS")
    print("-" * 40)
    print(f"Mean Vacuum Drag (Gravity/Mass): {typ_drag:.6f}")
    print(f"Mean Flux Repulsion (Electric):  {typ_elec:.6f}")
    print(f"Calculated Hierarchy Ratio:      {ratio:.2f}")
    print("-" * 40)
    
    # ----------------------------------------
    # PLOTTING
    # ----------------------------------------
    plt.figure(figsize=(10, 6), facecolor='black')
    ax = plt.gca()
    ax.set_facecolor('black')
    
    # We plot on Log Scale to see orders of magnitude
    ax.semilogy(distances, elec_forces, color='cyan', linewidth=3, label='Electric Force (Repulsion)')
    ax.semilogy(velocities, drag_forces, color='grey', linestyle='--', linewidth=2, label='Gravitational Drag (Inertia)')
    
    # Annotate the Gap
    mid_idx = len(distances)//2
    gap_top = elec_forces[mid_idx]
    gap_bot = drag_forces[mid_idx]
    ax.annotate(f'Gap ~ {gap_top/gap_bot:.1f}x', 
                xy=(distances[mid_idx], gap_bot), 
                xytext=(distances[mid_idx]+0.5, gap_bot*10),
                arrowprops=dict(facecolor='white', shrink=0.05),
                color='white', fontsize=12)

    ax.set_title("The Hierarchy Problem: Force Strength Comparison", color='white', fontsize=14)
    ax.set_xlabel("Distance (r) / Velocity (v)", color='white')
    ax.set_ylabel("Force Magnitude (Log Scale)", color='white')
    
    ax.legend(facecolor='black', labelcolor='white')
    ax.grid(color='#333333', alpha=0.5, which="both")
    ax.tick_params(colors='white', which="both")
    
    plt.tight_layout()
    plt.savefig('hierarchy_test.png')
    plt.show()

if __name__ == "__main__":
    run_hierarchy_test()