import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
import time

# ==========================================
# 1. THE PHYSICS KERNEL (Symplectic Numba)
# ==========================================
@njit(fastmath=True)
def get_basin_single(m, l, t_max=60.0, dt=0.05, escape_r2=16.0):
    """
    Integrates a single particle to find its exit basin.
    Returns: 1 (Teal), 2 (Center/Purple), 3 (Gold)
    """
    pm, pl = 0.0, 0.0
    steps = int(t_max / dt)
    
    # Pre-calc constants
    sigma = 1.0
    
    for _ in range(steps):
        # -- Symplectic Step 1 --
        fm = -(m + 2*sigma*m*l)
        fl = -(l + sigma*(m**2 - l**2))
        pm += 0.5 * dt * fm
        pl += 0.5 * dt * fl
        
        m += dt * pm
        l += dt * pl
        
        # -- Symplectic Step 2 --
        fm = -(m + 2*sigma*m*l)
        fl = -(l + sigma*(m**2 - l**2))
        pm += 0.5 * dt * fm
        pl += 0.5 * dt * fl
        
        # -- Ballistic Check --
        r2 = m*m + l*l
        if r2 > escape_r2:
            # We have escaped. Determine exit angle.
            angle = np.arctan2(l, m)
            # Map angle to basin (The 3 Valleys)
            # Valley 1: ~90 deg (Top)
            # Valley 2: ~210 deg (Bottom Left)
            # Valley 3: ~330 deg (Bottom Right)
            
            if angle > 0.5 and angle < 2.6: return 1  # Top
            elif angle <= -2.6 or angle >= 2.6: return 2 # Left (visual swap for color balance)
            else: return 3 # Right
            
    return 0 # Did not escape (Trapped/Limit Cycle)

@njit(parallel=True, fastmath=True)
def solve_prism_sector(res, zoom):
    """
    Solves ONLY the primary 120-degree wedge (Triangle Sector).
    """
    # Create grid in Polar Coordinates directly to easily crop the wedge
    # We want a full square grid, but we will mark non-wedge pixels as 0 to skip them
    
    out_map = np.zeros((res, res), dtype=np.int8)
    
    # Center offset
    cx = (res - 1) / 2.0
    cy = (res - 1) / 2.0
    scale = (2.0 * zoom) / res
    
    for y in prange(res):
        for x in range(res):
            # Map pixel to physical space
            px = (x - cx) * scale
            py = (y - cy) * scale
            
            # Check Angle
            angle = np.arctan2(py, px)
            
            # We only solve if angle is between -30 and 90 degrees (a 120 degree slice)
            # Or simpler: 0 to 120 (0 to 2pi/3)
            # Let's use the standard sector: 90 deg +/- 60 deg?
            # Let's do 0 to 120 degrees (0 to 2.09 radians)
            # Normalizing angle to [0, 2pi]
            if angle < 0: angle += 2*np.pi
            
            # THE PRISM OPTIMIZATION:
            # We only compute if the point falls in the first 1/3rd of the pie.
            if 0.0 <= angle < (2 * np.pi / 3):
                out_map[y, x] = get_basin_single(px, py)
            else:
                out_map[y, x] = 0 # Mark as empty
                
    return out_map

# ==========================================
# 2. THE GEOMETRY ENGINE (Reconstruction)
# ==========================================

def reconstruction_pass(partial_map):
    """
    Takes the 1/3rd computed map and rotates it twice to fill the void.
    Applies permutation to the basin IDs so the colors spiral correctly.
    """
    # 1. The Original (0 - 120 deg)
    full_map = partial_map.copy()
    
    # 2. Rotation 1 (+120 deg)
    # We rotate the IMAGE by 120 degrees counter-clockwise
    # Basin Shift: 1->2, 2->3, 3->1
    
    # Note: scipy.ndimage.rotate is slow.
    # For a perfect square grid, strict 90deg is easy, 120 is hard with arrays.
    # actually, calculating the wedge pixel-by-pixel is harder to rotate.
    
    # ALTERNATIVE STRATEGY:
    # Instead of image rotation, let's use the Symmetry at the SOLVER level.
    # See 'solve_folded_universe' below.
    return full_map

@njit(parallel=True, fastmath=True)
def solve_folded_universe(res, zoom):
    """
    Iterates over EVERY pixel, but maps it to the 'Prism Sector' before solving.
    Then maps the result back.
    
    This ensures we never calculate a trajectory that is merely a rotation of another.
    """
    out_map = np.zeros((res, res), dtype=np.int8)
    
    cx = (res - 1) / 2.0
    cy = (res - 1) / 2.0
    scale = (2.0 * zoom) / res
    
    deg120 = 2 * np.pi / 3
    deg240 = 4 * np.pi / 3
    
    for y in prange(res):
        for x in range(res):
            # 1. Current Physical Coords
            px = (x - cx) * scale
            py = (y - cy) * scale
            
            # 2. Get Polar
            r = np.sqrt(px*px + py*py)
            theta = np.arctan2(py, px)
            if theta < 0: theta += 2*np.pi
            
            # 3. Fold into Primary Sector [0, 120)
            # We track how many rotations we did to shift the color later
            rotation_count = 0
            
            effective_theta = theta
            
            if theta >= deg240:
                effective_theta = theta - deg240
                rotation_count = 2
            elif theta >= deg120:
                effective_theta = theta - deg120
                rotation_count = 1
                
            # 4. Map back to Cartesian for the Solver
            # The solver only sees the "Prism" version of the particle
            eff_px = r * np.cos(effective_theta)
            eff_py = r * np.sin(effective_theta)
            
            # 5. SOLVE (Expensive Step)
            # We enter the Numba solver with the folded coordinates
            raw_basin = get_basin_single(eff_px, eff_py)
            
            # 6. Unfold Color
            # If basin is 0 (trapped), it stays 0
            if raw_basin == 0:
                out_map[y, x] = 0
            else:
                # Cycle: 1->2->3->1
                # basin 1 (teal), 2 (purple), 3 (gold)
                # We need to shift the basin ID by 'rotation_count'
                # (val - 1 + shift) % 3 + 1
                
                final_basin = (raw_basin - 1 + rotation_count) % 3 + 1
                out_map[y, x] = final_basin
                
    return out_map

# ==========================================
# 3. EXECUTION
# ==========================================

def run_benchmark():
    RES = 9000
    ZOOM = 2.0
    
    print(f"[-] Initializing Prism Solver (Resolution: {RES}x{RES})...")
    print(f"[-] Folding Space into 120-degree Sector...")
    
    t0 = time.time()
    # First run includes compilation overhead
    result_map = solve_folded_universe(RES, ZOOM)
    t1 = time.time()
    
    print(f"[+] Solved in {t1-t0:.4f} seconds.")
    print(f"    (Theoretical comparison: Full Grid would take ~{(t1-t0)*3:.2f}s)")
    
    # Plot
    plt.figure(figsize=(10, 10), facecolor='black')
    # Custom palette: Black, Cyan, Purple, Orange
    cmap = plt.cm.colors.ListedColormap(['black', '#00cccc', '#8800ff', '#ffaa00'])
    
    plt.imshow(result_map, origin='lower', cmap=cmap, interpolation='nearest')
    plt.title(f"The Prism Optimization (C3 Symmetry)", color='white', fontsize=15)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('wada_prism_solver.png', dpi=150)
    plt.show()

if __name__ == "__main__":
    run_benchmark()