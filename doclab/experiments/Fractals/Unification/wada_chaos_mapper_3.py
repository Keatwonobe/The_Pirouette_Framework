import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
import time
from PIL import Image

# ==========================================
# CONFIGURATION
# ==========================================
RES = 300            # Resolution (Keep low for fast execution)
ZOOM = 2.0           # Initial Viewport radius
ESCAPE_R2 = 25.0     # Escape horizon
DT = 0.05            # Time step
T_MAX = 100.0        # Max simulation time
SIGMA = 1.0          # Potential Parameter
NUM_FRAMES = 10      # Number of frames for the GIF

# ==========================================
# 1. PHYSICS KERNEL (JIT COMPILED)
# ==========================================
@njit(fastmath=True)
def get_pixel_data(m, l):
    """Simulates a single particle and returns Basin, Stress, and Steps."""
    pm, pl = 0.0, 0.0; steps = 0; stress = 0.0
    max_steps = int(T_MAX / DT)

    for _ in range(max_steps):
        fm = -(m + 2*SIGMA*m*l); fl = -(l + SIGMA*(m**2 - l**2))
        force_mag = np.sqrt(fm*fm + fl*fl); stress += force_mag * DT
        pm += 0.5 * DT * fm; pl += 0.5 * DT * fl
        m += DT * pm; l += DT * pl
        fm = -(m + 2*SIGMA*m*l); fl = -(l + SIGMA*(m**2 - l**2))
        pm += 0.5 * DT * fm; pl += 0.5 * DT * fl
        steps += 1

        if m*m + l*l > ESCAPE_R2:
            angle = np.arctan2(l, m)
            if angle > 0.5 and angle < 2.6: return 1, stress, steps
            elif angle <= -2.6 or angle >= 2.6: return 2, stress, steps
            else: return 3, stress, steps
    return 0, stress, steps

@njit(parallel=True, fastmath=True)
def render_manifold(res, zoom, center_m, center_l):
    """Renders the manifold with a specific center and zoom."""
    basin_map = np.zeros((res, res), dtype=np.int8)
    stress_map = np.zeros((res, res), dtype=np.float32)
    time_map = np.zeros((res, res), dtype=np.float32)

    cx = (res - 1) / 2.0; cy = (res - 1) / 2.0; scale = (2.0 * zoom) / res

    for y in prange(res):
        for x in range(res):
            # Map Pixel -> Physics Coordinate (Modified for arbitrary center)
            px = center_m + (x - cx) * scale
            py = center_l + (y - cy) * scale

            basin, stress, steps = get_pixel_data(px, py)

            basin_map[y, x] = basin
            stress_map[y, x] = stress
            time_map[y, x] = steps

    return basin_map, stress_map, time_map

# ==========================================
# 2. ITERATIVE ZOOM LOGIC
# ==========================================

def get_new_viewport(stress_map, old_zoom, old_res, current_m, current_l, zoom_factor=0.5):
    """Calculates the new center (m, l) and the new zoom factor for the next iteration."""

    # Find the average location of the highest 0.5% of frustration (the 'burn')
    threshold = np.percentile(stress_map, 99.5)
    high_stress_pixels = np.argwhere(stress_map >= threshold)

    if len(high_stress_pixels) == 0:
        y_max, x_max = np.unravel_index(np.argmax(stress_map), stress_map.shape)
    else:
        center_index = np.mean(high_stress_pixels, axis=0).astype(int)
        y_max, x_max = center_index

    H, W = stress_map.shape
    scale = (2.0 * old_zoom) / old_res

    # Map the peak pixel back to physics coordinates relative to the current center
    m_offset = (x_max - W / 2.0) * scale
    l_offset = (y_max - H / 2.0) * scale

    new_m = current_m + m_offset
    new_l = current_l + l_offset
    new_zoom = old_zoom * zoom_factor

    return new_m, new_l, new_zoom

# ==========================================
# 3. MAIN EXECUTION LOOP
# ==========================================

if __name__ == "__main__":
    
    current_m, current_l, current_zoom = 0.0, 0.0, ZOOM # Initial setup: center (0,0), zoom 2.0
    frame_files = [] 
    
    fig, ax = plt.subplots(figsize=(8, 8), facecolor='black')
    ax.axis('off')
    
    print(f"[*] Starting Fractal Mapper: {NUM_FRAMES} frames @ {RES}x{RES}")
    
    for i in range(NUM_FRAMES):
        start_time = time.time()
        
        # 1. RENDER
        basin, stress, steps = render_manifold(RES, current_zoom, current_m, current_l)
        
        elapsed = time.time() - start_time
        print(f"  Frame {i+1}/{NUM_FRAMES} rendered in {elapsed:.2f}s | Zoom: {current_zoom:.6f}")
        
        # 2. PLOT AND SAVE FRAME
        ax.cla()
        ax.set_title(f"Frustration Manifold (Zoom Factor: {ZOOM/current_zoom:.1f})", color='white')
        ax.axis('off')
        
        # Use the current center and zoom for the plot extent
        ax.imshow(stress, origin='lower', cmap='inferno', 
                  vmin=0, vmax=np.percentile(stress, 98), 
                  extent=[-current_zoom+current_m, current_zoom+current_m, -current_zoom+current_l, current_zoom+current_l])

        filename = f'fractal_frame_{i:02d}.png'
        plt.savefig(filename, dpi=100)
        frame_files.append(filename)

        # 3. CALCULATE NEXT VIEWPORT
        if i < NUM_FRAMES - 1:
            current_m, current_l, current_zoom = get_new_viewport(
                stress, current_zoom, RES, current_m, current_l, zoom_factor=0.5
            )

    plt.close(fig)

    # 4. STITCH FRAMES INTO GIF
    print("[*] Stitching frames into GIF...")
    if frame_files:
        imgs = [Image.open(f) for f in frame_files]
        imgs[0].save('fractal_mapper_zoom.gif', save_all=True, append_images=imgs[1:], duration=200, loop=0)
        print("[+] Fractal Mapper GIF saved to 'fractal_mapper_zoom.gif'")