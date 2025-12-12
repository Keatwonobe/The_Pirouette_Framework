import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter
from numba import njit, prange
import time

# ==========================================
# 1. CONFIGURATION
# ==========================================
# Reduced for faster execution in the VM
RES = 800            # Resolution
ZOOM = 2.0           # Viewport radius
ESCAPE_R2 = 25.0     # Escape horizon
DT = 0.05            # Time step
T_MAX = 50.0         # Max simulation time (reduced from 100.0)
SIGMA = 1.0          # Potential Parameter
FRAMES = 80          # Number of frames for the GIF

# ==========================================
# 2. PHYSICS KERNEL (JIT COMPILED) - Same as wada_chaos_mapper.py
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
# 3. MAIN EXECUTION & ANIMATION
# ==========================================
if __name__ == "__main__":
    print(f"[*] Starting Manifold Scan ({RES}x{RES})...")
    start_time = time.time()

    # --- 3a. Initial Static Scan ---
    basin, stress, steps = render_manifold(RES, ZOOM)
    elapsed = time.time() - start_time
    print(f"[+] Scan Complete in {elapsed:.2f}s")

    # --- 3b. Data Pre-processing for Animation ---

    # Chaos Frequency Map F_c = 1/T, where T = steps * DT
    time_map_s = steps * DT
    # Avoid division by zero/near-zero for points that didn't escape
    MIN_TIME = 1.0 / (2.0 * T_MAX) # Use a very low frequency for non-escaped points
    frequency_map = np.where(time_map_s > 0, 1.0 / time_map_s, MIN_TIME)

    # Normalization (The 'voids' will be low-frequency, 'crackles' high-frequency)
    FREQ_MAX = np.percentile(frequency_map[frequency_map > MIN_TIME], 99.9)
    frequency_map_norm = np.clip(frequency_map, MIN_TIME, FREQ_MAX)
    
    # Frustration Map Normalization
    STRESS_MAX = np.percentile(stress, 99.5)
    stress_norm = np.clip(stress, 0, STRESS_MAX)

    # Time thresholds for the reveal animation
    step_max = steps.max()
    time_thresholds = np.linspace(1, step_max, FRAMES, dtype=int)


    # --- 3c. Setup Animation ---
    
    fig = plt.figure(figsize=(10, 10), facecolor='black')
    gs = fig.add_gridspec(2, 2, hspace=0.1, wspace=0.1) 

    ax_stress = fig.add_subplot(gs[0, 0])
    ax_freq = fig.add_subplot(gs[0, 1])
    ax_mask = fig.add_subplot(gs[1, 0])
    ax_hist = fig.add_subplot(gs[1, 1])

    for ax in [ax_stress, ax_freq, ax_mask]:
        ax.set_facecolor('black'); ax.axis('off')
    
    # Hist setup (The Heartbeat/Profile)
    ax_hist.set_facecolor('#111111'); ax_hist.grid(axis='y', color='#333333', linewidth=0.5)
    ax_hist.set_xlabel("Frustration/Stress Magnitude", color='white', fontsize=8)
    ax_hist.set_ylabel("Instantaneous Density", color='white', fontsize=8)
    ax_hist.set_title("Instantaneous Chaos Profile", color='orange', fontsize=10)
    ax_hist.tick_params(colors='white', labelsize=7)
    ax_hist.set_xlim(0, STRESS_MAX)
    ax_hist.set_ylim(0, 0.25)
    
    # Initial Images
    zero_map = np.zeros_like(stress_norm)
    
    im_stress = ax_stress.imshow(zero_map, origin='lower', cmap='inferno', vmin=0, vmax=STRESS_MAX)
    ax_stress.set_title("Frustration Manifold (Chaos)", color='white')

    im_freq = ax_freq.imshow(zero_map, origin='lower', cmap='viridis', vmin=MIN_TIME, vmax=FREQ_MAX)
    ax_freq.set_title("Chaos Frequency Map ($F_c$)", color='white')
    
    # Mask Image
    im_mask = ax_mask.imshow(zero_map, origin='lower', cmap='cividis', vmin=0, vmax=1)
    ax_mask.set_title("Instantaneous Reveal Mask", color='white')
    
    # Histogram Setup (The bars will be updated dynamically)
    hist_data, bin_edges = np.histogram([], bins=20, range=(0, STRESS_MAX), density=True)
    bars = ax_hist.bar(bin_edges[:-1], hist_data, width=np.diff(bin_edges), color='purple', alpha=0.7)
    
    title_text = fig.suptitle("Wada Chaos Mapper 4: Time-Lapse Reveal", color='white', fontsize=14, fontfamily='monospace', y=0.95)

    def animate(i):
        current_steps = time_thresholds[i]
        
        # Calculate the cumulative mask (all points revealed up to this time)
        cumulative_mask = steps <= current_steps
        
        # Calculate the instantaneous mask (points revealed ONLY in this frame)
        # We need the previous threshold to calculate the difference
        prev_steps = time_thresholds[i-1] if i > 0 else 0
        instantaneous_mask = (steps <= current_steps) & (steps > prev_steps)
        
        # 1. Update Frustration Map (Burning In)
        revealed_stress = np.where(cumulative_mask, stress_norm, 0)
        im_stress.set_data(revealed_stress)
        
        # 2. Update Chaos Frequency Map (Burning In)
        revealed_freq = np.where(cumulative_mask, frequency_map_norm, 0)
        im_freq.set_data(revealed_freq)
        
        # 3. Update Instantaneous Reveal Mask (Burning Out)
        im_mask.set_data(instantaneous_mask.astype(float)) # Mask for current frame

        # 4. Update Instantaneous Chaos Profile (Histogram)
        # Data for the histogram is the stress of ONLY the instantaneously revealed points
        instant_stress_data = stress[instantaneous_mask]
        
        if len(instant_stress_data) > 10:
            hist_data, _ = np.histogram(instant_stress_data, bins=20, range=(0, STRESS_MAX), density=True)
            for bar, h in zip(bars, hist_data):
                bar.set_height(h)
        else:
             # Set all bars to zero if not enough data to form a meaningful profile
            for bar in bars: bar.set_height(0)

        # Update Title
        T_current = current_steps * DT
        title_text.set_text(f"Wada Chaos Mapper 4: Time-Lapse Reveal | Escape Time $T \\leq {T_current:.2f}$s | Frame {i+1}/{FRAMES}")
        
        if i % 10 == 0: print(f"Rendering frame {i+1}...")
        
        return im_stress, im_freq, im_mask, *bars, title_text

    print(f"[-] Igniting Animation Engine...")
    anim = animation.FuncAnimation(fig, animate, frames=FRAMES, interval=100, blit=False)
    
    # Save the animation
    writer = PillowWriter(fps=10)
    anim.save('wada_chaos_mapper_4.gif', writer=writer)
    plt.close(fig)
    print("[+] Experiment Complete. Saved to 'wada_chaos_mapper_4.gif'")