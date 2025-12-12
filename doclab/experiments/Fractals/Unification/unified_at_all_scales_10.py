import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numba

# ======================
# CONFIGURATION
# ======================
RES = 800              # Resolution of the scan (Higher = sharper fractal)
MAX_STEPS = 2000       # Simulation duration
DT = 0.02              # Time step
ESCAPE_R = 10.0        # Distance to consider "Escaped"

print("=" * 60)
print("D I P O L E   S C A T T E R I N G   S C A N")
print("Searching for the Wada Set in the Impact Zone...")
print("=" * 60)

# ======================
# PHYSICS KERNEL (Numba for Speed)
# ======================
@numba.jit(nopython=True)
def simulate_collision(impact_param, velocity):
    # Initial Conditions
    # T1 (Matter): Starts Left, moving Right
    x1, y1 = -3.0, impact_param / 2.0
    vx1, vy1 = velocity, 0.0
    
    # T2 (Antimatter): Starts Right, moving Left
    x2, y2 = 3.0, -impact_param / 2.0
    vx2, vy2 = -velocity, 0.0
    
    # Physics Parameters
    # "Equal and Opposite"
    # T1 is +Mass (Attractor), T2 is -Mass (Repulsor/Attractor complex)
    # In this specific "Dipole" setup, Matter falls into Void, Void chases Matter.
    # This is modeled as a runaway pair if isolated, but here we place them in the Substrate.
    
    # Substrate Constants (The Hénon-Heiles Triangle)
    k_sub = 1.0 
    
    for t in range(MAX_STEPS):
        # 1. Substrate Forces (The Background Geometry)
        # The Universe itself pulls them into the Triangle
        # V = 1/2(r^2) + cubic terms
        
        # T1 Forces
        fx1_sub = -k_sub * (x1 + 2*x1*y1)
        fy1_sub = -k_sub * (y1 + x1**2 - y1**2)
        
        # T2 Forces
        fx2_sub = -k_sub * (x2 + 2*x2*y2)
        fy2_sub = -k_sub * (y2 + x2**2 - y2**2)
        
        # 2. Mutual Interaction (The Dipole)
        dx = x2 - x1
        dy = y2 - y1
        dist_sq = dx*dx + dy*dy + 0.01
        dist = np.sqrt(dist_sq)
        
        # Force Magnitude (1/r^2 gravity)
        f_mag = 2.0 / dist_sq
        
        # Direction
        nx = dx / dist
        ny = dy / dist
        
        # The "Runaway" Dynamic:
        # T1 (Positive) is attracted to T2 (Negative) -> Pulled towards it.
        # T2 (Negative) is repelled by T1 (Positive) -> Pushed away from it? 
        # Actually, for "Void chases Matter", T2 must be attracted to T1's positive mass *behaviorally*.
        # Let's assume standard attraction for capture:
        
        fx_int = f_mag * nx
        fy_int = f_mag * ny
        
        # Apply Forces
        # T1 accelerates towards T2
        vx1 += (fx1_sub + fx_int) * DT
        vy1 += (fy1_sub + fy_int) * DT
        
        # T2 accelerates towards T1 (Capture scenario)
        vx2 += (fx2_sub - fx_int) * DT
        vy2 += (fy2_sub - fy_int) * DT
        
        # Update Positions
        x1 += vx1 * DT
        y1 += vy1 * DT
        x2 += vx2 * DT
        y2 += vy2 * DT
        
        # Check Escape (Scattering)
        r1_sq = x1*x1 + y1*y1
        if r1_sq > ESCAPE_R*ESCAPE_R:
            # Determine Exit Channel (Basin)
            angle = np.arctan2(y1, x1)
            if angle > 0.5 and angle < 2.5: return 1   # Top Exit
            if angle > 2.5 or angle < -2.5: return 2   # Left Exit
            return 3                                   # Right Exit
            
    # If we run out of steps, they are Captured (The Knot)
    return 0

@numba.jit(nopython=True, parallel=True)
def run_scan_grid(res, impact_min, impact_max, vel_min, vel_max):
    grid = np.zeros((res, res), dtype=np.int32)
    
    impacts = np.linspace(impact_min, impact_max, res)
    vels = np.linspace(vel_min, vel_max, res)
    
    for i in numba.prange(res): # Velocity Axis (Y)
        v = vels[i]
        for j in range(res):    # Impact Axis (X)
            imp = impacts[j]
            grid[i, j] = simulate_collision(imp, v)
            
    return grid

# ======================
# MAIN EXECUTION
# ======================
def generate_wada_dipole():
    # Scan Parameters
    # We look for the "Sweet Spot" where velocity matches the potential depth
    IMPACT_RANGE = (-0.2, 0.2)
    VELOCITY_RANGE = (0.1, 1.5)
    
    print(f"[*] Simulating {RES*RES} Collisions...")
    fate_map = run_scan_grid(RES, IMPACT_RANGE[0], IMPACT_RANGE[1], VELOCITY_RANGE[0], VELOCITY_RANGE[1])
    print("[✓] Scan Complete.")
    
    # Visualization
    plt.figure(figsize=(12, 10), facecolor='#050505')
    
    # Custom Colormap
    # 0 = Black (Knot/Capture)
    # 1 = Red, 2 = Teal, 3 = Gold (The 3 Escape Basins)
    cmap = ListedColormap(['black', '#ff3333', '#00cccc', '#ffaa00'])
    
    plt.imshow(fate_map, origin='lower', 
               extent=[IMPACT_RANGE[0], IMPACT_RANGE[1], VELOCITY_RANGE[0], VELOCITY_RANGE[1]],
               aspect='auto', cmap=cmap)
    
    plt.xlabel("Impact Parameter (Offset)", color='white', fontsize=12)
    plt.ylabel("Approach Velocity", color='white', fontsize=12)
    plt.title("The Inevitable Knot: Fate Map of Dipole Collision", color='white', fontsize=16, pad=20)
    
    # Annotation
    plt.text(0, 0.2, "CAPTURE ZONE\n(The Knot)", color='white', ha='center', va='center', fontsize=14, fontweight='bold', alpha=0.5)
    plt.text(-1.5, 1.3, "SCATTERING", color='white', ha='center', fontsize=12, alpha=0.5)
    
    plt.tick_params(colors='white')
    plt.tight_layout()
    plt.savefig('dipole_wada_scan.png')
    plt.show()

if __name__ == "__main__":
    generate_wada_dipole()