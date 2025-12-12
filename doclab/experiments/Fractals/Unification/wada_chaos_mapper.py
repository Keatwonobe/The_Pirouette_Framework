import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
import time

# ==========================================
# CONFIGURATION
# ==========================================
RES = 2000           # Resolution (2000x2000 = 4 Million Probes)
ZOOM = 2.0           # Viewport radius
ESCAPE_R2 = 25.0     # Escape horizon
DT = 0.05            # Time step
T_MAX = 100.0        # Max simulation time
SIGMA = 1.0          # Potential Parameter

# ==========================================
# PHYSICS KERNEL (JIT COMPILED)
# ==========================================
@njit(fastmath=True)
def get_pixel_data(m, l):
    """
    Simulates a single particle and returns:
    1. Basin (0=Trapped, 1,2,3=Escaped)
    2. Frustration (Accumulated Force Stress)
    3. Escape Time (Steps taken)
    """
    pm, pl = 0.0, 0.0 # Start from rest
    steps = 0
    stress = 0.0
    max_steps = int(T_MAX / DT)
    
    for _ in range(max_steps):
        # 1. Force Calculation
        fm = -(m + 2*SIGMA*m*l)
        fl = -(l + SIGMA*(m**2 - l**2))
        
        # Frustration Accumulation (The "Burn")
        # We sum the magnitude of the force felt at every step
        force_mag = np.sqrt(fm*fm + fl*fl)
        stress += force_mag * DT
        
        # 2. Symplectic Integration
        pm += 0.5 * DT * fm
        pl += 0.5 * DT * fl
        m += DT * pm
        l += DT * pl
        
        # Recalc for second half-step
        fm = -(m + 2*SIGMA*m*l)
        fl = -(l + SIGMA*(m**2 - l**2))
        pm += 0.5 * DT * fm
        pl += 0.5 * DT * fl
        
        steps += 1
        
        # 3. Escape Condition
        if m*m + l*l > ESCAPE_R2:
            angle = np.arctan2(l, m)
            # Map angle to 3 basins
            if angle > 0.5 and angle < 2.6: return 1, stress, steps
            elif angle <= -2.6 or angle >= 2.6: return 2, stress, steps
            else: return 3, stress, steps
            
    return 0, stress, steps # Trapped

@njit(parallel=True, fastmath=True)
def render_manifold(res, zoom):
    # Output buffers
    basin_map = np.zeros((res, res), dtype=np.int8)
    stress_map = np.zeros((res, res), dtype=np.float32)
    time_map = np.zeros((res, res), dtype=np.float32)
    
    cx = (res - 1) / 2.0
    cy = (res - 1) / 2.0
    scale = (2.0 * zoom) / res
    
    # Parallel Loop over pixels
    for y in prange(res):
        for x in range(res):
            # Map Pixel -> Physics Coordinate
            px = (x - cx) * scale
            py = (y - cy) * scale
            
            basin, stress, steps = get_pixel_data(px, py)
            
            basin_map[y, x] = basin
            stress_map[y, x] = stress
            time_map[y, x] = steps
            
    return basin_map, stress_map, time_map

# ==========================================
# MAIN EXECUTION
# ==========================================
if __name__ == "__main__":
    print(f"[*] Starting Manifold Scan ({RES}x{RES})...")
    start_time = time.time()
    
    basin, stress, steps = render_manifold(RES, ZOOM)
    
    elapsed = time.time() - start_time
    print(f"[+] Scan Complete in {elapsed:.2f}s")
    
    # --- PLOTTING ---
    fig, axes = plt.subplots(1, 3, figsize=(24, 8), facecolor='#111111')
    
    # 1. THE BASIN MAP (Wada Property)
    # 0=Black, 1=Red, 2=Blue, 3=Green
    cmap_basin = plt.matplotlib.colors.ListedColormap(['black', '#ff4444', '#4488ff', '#44ff88'])
    axes[0].imshow(basin, origin='lower', cmap=cmap_basin)
    axes[0].set_title("The Wada Basins (Destinations)", color='white')
    axes[0].axis('off')
    
    # 2. THE FRUSTRATION MAP (The Chaos)
    # Brightness = Accumulated Stress
    axes[1].imshow(stress, origin='lower', cmap='inferno', vmin=0, vmax=np.percentile(stress, 98))
    axes[1].set_title("The Frustration Manifold (Chaos)", color='white')
    axes[1].axis('off')
    
    # 3. THE STABILITY MAP (The Opposite)
    # Dark = Fast Escape (Stable), Bright = Slow Escape (Unstable)
    axes[2].imshow(steps, origin='lower', cmap='magma', vmin=0, vmax=np.percentile(steps, 95))
    axes[2].set_title("The Time Crystal (Stability)", color='white')
    axes[2].axis('off')
    
    plt.tight_layout()
    plt.savefig('wada_manifold_scan.png', dpi=150)
    print(f"[+] Maps saved to 'wada_manifold_scan.png'")
    plt.show()