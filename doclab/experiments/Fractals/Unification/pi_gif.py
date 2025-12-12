import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
import time
from PIL import Image
import os

# =========================================================
#  PROTON FRACTAL GIF GENERATOR (The "Crystallization" Effect)
# =========================================================

# --- CONFIGURATION ---
OUTPUT_FILENAME = "proton_genesis.gif"
FRAMES = 80              # Total number of frames
START_STEPS = 15          # Starting iteration depth (blurry)
END_STEPS = 500          # Final iteration depth (sharp)
RES = 1500                # Resolution (lower than 1000 for speed, higher for quality)
DURATION = 100           # ms per frame

# --- PHYSICS PARAMETERS (Matching pi_scanner_8.py) ---
M_MIN, M_MAX = -0.0002, 0.0002
L_MIN, L_MAX = -0.0002, 0.0002
R_ESCAPE = 1000.0
TWIST = 3.8
GAMMA = 0.5
DT    = 0.015

# --- CORE DYNAMICS ---

@njit
def get_force_weights(m, lam):
    # (Identical physics to V8)
    F_teal_m   = -(m + 0.866)
    F_teal_lam = -(lam - 0.5)
    F_red_m   = -(m - 0.0)
    p_violation = TWIST * np.sin(m * 2.5)
    F_red_lam = -(lam + 1.0) + p_violation
    sum_m, sum_lam = F_teal_m + F_red_m, F_teal_lam + F_red_lam
    mag = np.sqrt(sum_m**2 + sum_lam**2)
    scale = np.sqrt(mag)
    F_gold_m, F_gold_lam = sum_m * scale, sum_lam * scale
    
    angle_deg = np.degrees(np.arctan2(lam, m)) % 360.0
    w_gold = np.exp(-(min(abs(angle_deg - 30.0), 360.0 - abs(angle_deg - 30.0)) / 80.0)**2)
    w_teal = np.exp(-(min(abs(angle_deg - 150.0), 360.0 - abs(angle_deg - 150.0)) / 80.0)**2)
    w_red  = np.exp(-(min(abs(angle_deg - 270.0), 360.0 - abs(angle_deg - 270.0)) / 80.0)**2)

    tot = w_gold + w_teal + w_red + 1e-6
    return w_red/tot, w_teal/tot, w_gold/tot, F_red_m, F_red_lam, F_teal_m, F_teal_lam, F_gold_m, F_gold_lam

# --- DYNAMIC RENDER KERNEL ---

@njit(parallel=True)
def render_frame_data(m_vals, l_vals, current_max_steps):
    """
    Renders a single frame with a specific iteration limit (current_max_steps).
    """
    h, w = len(l_vals), len(m_vals)
    image = np.zeros((h, w, 4)) # R, G, B, Alpha
    
    # Parallel loop for speed
    for i in prange(h):
        for j in range(w):
            m, l = m_vals[j], l_vals[i]
            pm, pl = 0.0, 0.0
            total_red, total_teal, total_gold = 0.0, 0.0, 0.0
            total_winding = 0.0
            prev_angle = np.arctan2(l, m)
            steps_taken = 0
            escaped = False
            
            # --- TRAJECTORY LOOP ---
            for s in range(current_max_steps):
                nw_red, nw_teal, nw_gold, Frm, Frl, Ftm, Ftl, Fgm, Fgl = get_force_weights(m, l)
                
                total_red += nw_red
                total_teal += nw_teal
                total_gold += nw_gold
                
                Fm = nw_teal * Ftm + nw_red * Frm + nw_gold * Fgm
                Flam = nw_teal * Ftl + nw_red * Frl + nw_gold * Fgl
                
                drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * nw_red)
                pm = (pm + 0.5 * DT * Fm) * drag
                pl = (pl + 0.5 * DT * Flam) * drag
                m += DT * pm
                l += DT * pl
                
                curr_angle = np.arctan2(l, m)
                d_angle = curr_angle - prev_angle
                if d_angle > np.pi: d_angle -= 2*np.pi
                if d_angle < -np.pi: d_angle += 2*np.pi
                total_winding += d_angle
                prev_angle = curr_angle
                
                steps_taken += 1
                
                if (m**2 + l**2) > R_ESCAPE**2:
                    escaped = True
                    break
            
            # --- COLORING ---
            norm = total_red + total_teal + total_gold + 1e-9
            r_val = total_red / norm
            g_val = total_teal / norm
            b_val = total_gold / norm
            
            if not escaped:
                intensity = 1.0
                # FIXED: Changed 'winding' to 'total_winding'
                if abs(total_winding) > 6*np.pi: intensity = 0.6
            else:
                # Use current_max_steps for normalization to keep brightness consistent during animation
                nu = np.log(np.log(m**2 + l**2)) / np.log(2)
                smooth_steps = steps_taken + 1 - nu
                # We normalize against current_max_steps to show the "front" moving
                intensity = 0.1 + 0.9 * (smooth_steps / current_max_steps)

            image[i, j, 0] = r_val
            image[i, j, 1] = g_val
            image[i, j, 2] = b_val
            image[i, j, 3] = intensity

    return image

# --- MAIN GENERATOR ---

def generate_gif():
    print(f"--- 🎬 PROTON GENESIS: GIF GENERATION ---")
    print(f"Resolution: {RES}x{RES}")
    print(f"Frames: {FRAMES} (Steps {START_STEPS} -> {END_STEPS})")
    
    m_vals = np.linspace(M_MIN, M_MAX, RES)
    l_vals = np.linspace(L_MIN, L_MAX, RES)
    
    # Pre-compile JIT
    print("Compiling Physics Engine...")
    render_frame_data(m_vals[0:2], l_vals[0:2], 10)
    
    # Create Step Sequence (Logarithmic looks better for fractal zooms, Linear for formation)
    # We use a power curve to spend more time on the complex details at the end
    step_sequence = np.linspace(START_STEPS**(0.5), END_STEPS**(0.5), FRAMES)**2
    step_sequence = [int(s) for s in step_sequence]
    
    frames_buffer = []
    
    start_time = time.time()
    
    for idx, steps in enumerate(step_sequence):
        print(f"Rendering Frame {idx+1}/{FRAMES} (Max Steps: {steps})...")
        
        raw_img = render_frame_data(m_vals, l_vals, steps)
        
        # Composite against background
        final_img = np.zeros((RES, RES, 3), dtype=np.uint8)
        bg = np.array([0.0, 0.0, 0.05]) # Dark Blue Deep Space
        
        alpha = raw_img[:, :, 3]
        rgb = raw_img[:, :, 0:3]
        
        for c in range(3):
            # Mix and scale to 0-255
            channel = rgb[:, :, c] * alpha + bg[c] * (1 - alpha)
            final_img[:, :, c] = (np.clip(channel, 0, 1) * 255).astype(np.uint8)
            
        # Flip vertically for correct orientation (origin lower)
        final_img = np.flipud(final_img)
        
        # Convert to Pillow Image
        pil_img = Image.fromarray(final_img)
        frames_buffer.append(pil_img)

    print(f"Rendering complete. Saving GIF to {OUTPUT_FILENAME}...")
    
    # Save GIF
    frames_buffer[0].save(
        OUTPUT_FILENAME,
        save_all=True,
        append_images=frames_buffer[1:],
        optimize=True,
        duration=DURATION,
        loop=0
    )
    
    print(f"✅ DONE! Total time: {time.time() - start_time:.2f}s")
    print(f"File saved: {OUTPUT_FILENAME}")

if __name__ == "__main__":
    generate_gif()