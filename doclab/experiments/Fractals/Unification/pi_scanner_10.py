import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from numba import njit
from scipy.ndimage import binary_erosion
import time

# =========================================================
#  UNIFIED PROTON SCANNER V10: THE MULTI-LENS SYSTEM
#  Features: Dashboard View + 4 Discrete High-Res Channels
# =========================================================

# --- GLOBAL CONFIGURATION ---
M_MIN, M_MAX = -24000000000, 24000000000
L_MIN, L_MAX = -24000000000, 24000000000
RES_BASE = 1000      # High resolution for crisp individual maps
MAX_STEPS = 200      
R_ESCAPE = 1000.0    
EPSILON = 1e-8       
TWIST = 3.8
GAMMA = 0.5
DT    = 0.015
HELICITY_STOP = np.pi * 0.95
RESYNCH_STEPS = 10   

# --- CORE DYNAMICS (JIT Compiled Physics) ---
@njit
def normalize_angle_diff(delta):
    return np.arctan2(np.sin(delta), np.cos(delta))

@njit
def get_force_weights(m, lam):
    """Calculates force weights (Gold, Teal, Red) based on geometry."""
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

# --- UNIFIED PIXEL TRACER ---
# This function calculates EVERYTHING for a single pixel in one go to save compute time.
@njit
def trace_pixel_unified(m0, l0):
    # 1. Setup State
    m, l = m0, l0
    pm, pl = 0.0, 0.0
    
    # 2. Setup Lyapunov Shadows
    dm, dl = EPSILON, EPSILON
    d_norm = np.sqrt(dm**2 + dl**2)
    dm, dl = dm/d_norm * EPSILON, dl/d_norm * EPSILON
    sum_log_expansion = 0.0
    
    # 3. Setup Helicity Shadows
    m_h, l_h = m0 + EPSILON, l0 + EPSILON
    pm_h, pl_h = 0.0, 0.0
    max_diff_angle = 0.0
    
    # 4. Setup Chromatic Accumulators
    tot_r, tot_t, tot_g = 0.0, 0.0, 0.0
    
    steps_taken = 0
    escaped = False
    
    # --- TIME LOOP ---
    for step in range(MAX_STEPS):
        # A. Main Trajectory Dynamics
        nw_r, nw_t, nw_g, Frm, Frl, Ftm, Ftl, Fgm, Fgl = get_force_weights(m, l)
        
        # Color Accumulation
        tot_r += nw_r; tot_t += nw_t; tot_g += nw_g
        
        # Forces
        Fm = nw_t * Ftm + nw_r * Frm + nw_g * Fgm
        Flam = nw_t * Ftl + nw_r * Frl + nw_g * Fgl
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * nw_r)
        
        # Update Main
        pm = (pm + 0.5 * DT * Fm) * drag
        pl = (pl + 0.5 * DT * Flam) * drag
        m += DT * pm
        l += DT * pl
        
        # B. Helicity Shadow Update
        nw_rh, nw_th, nw_gh, Frmh, Frlh, Ftmh, Ftlh, Fgmh, Fglh = get_force_weights(m_h, l_h)
        Fmh = nw_th * Ftmh + nw_rh * Frmh + nw_gh * Fgmh
        Flamh = nw_th * Ftlh + nw_rh * Frlh + nw_gh * Fglh
        drag_h = 1.0 / (1.0 + 0.5 * DT * GAMMA * nw_rh)
        pm_h = (pm_h + 0.5 * DT * Fmh) * drag_h
        pl_h = (pl_h + 0.5 * DT * Flamh) * drag_h
        m_h += DT * pm_h
        l_h += DT * pl_h
        
        # Measure Helicity
        diff = normalize_angle_diff(np.arctan2(l, m) - np.arctan2(l_h, m_h))
        max_diff_angle = max(max_diff_angle, np.abs(diff))
        
        # C. Lyapunov Resynchronization
        # (Simplified perturbation update using force gradients approximation)
        # To save massive compute, we use the fact that dF ~ F(shadow) - F(main)
        # Note: A full Jacobian is more accurate but 10x slower.
        m_s, l_s = m + dm, l + dl
        nw_rs, nw_ts, nw_gs, Frms, Frls, Ftms, Ftls, Fgms, Fgls = get_force_weights(m_s, l_s)
        Fm_s = nw_ts * Ftms + nw_rs * Frms + nw_gs * Fgms
        Flam_s = nw_ts * Ftls + nw_rs * Frls + nw_gs * Fgls
        drag_s = 1.0 / (1.0 + 0.5 * DT * GAMMA * nw_rs)
        
        dFm = Fm_s - Fm
        dFlam = Flam_s - Flam
        dpm = (dm + 0.5 * DT * dFm) * drag_s
        dpl = (dl + 0.5 * DT * dFlam) * drag_s
        dm += DT * dpm
        dl += DT * dpl
        
        # Resynch Logic
        if step % RESYNCH_STEPS == 0 and step > 0:
            d_curr = np.sqrt(dm**2 + dl**2)
            if d_curr < 1e-15: d_curr = 1e-15
            sum_log_expansion += np.log(d_curr / EPSILON)
            dm = dm * (EPSILON / d_curr)
            dl = dl * (EPSILON / d_curr)

        steps_taken = step
        if (m**2 + l**2) > R_ESCAPE**2:
            escaped = True
            break
            
    # --- POST PROCESS ---
    # 1. Chromatic
    norm = tot_r + tot_t + tot_g + 1e-9
    r_val, g_val, b_val = tot_r/norm, tot_t/norm, tot_g/norm
    
    # 2. Helicity
    helicity_val = np.log(max_diff_angle + EPSILON)
    
    # 3. Lyapunov
    total_time = steps_taken * DT
    if total_time < 1e-9: total_time = 1e-9
    lyap_val = sum_log_expansion / total_time
    if escaped: lyap_val = 5.0 # Max saturation for escapees
    
    # 4. Mask/Steps (Normalized 0-1)
    step_val = steps_taken / MAX_STEPS
    
    return r_val, g_val, b_val, helicity_val, lyap_val, step_val, escaped

# --- GENERATOR WRAPPER ---
def generate_data_cubes(res=RES_BASE):
    m_vals = np.linspace(M_MIN, M_MAX, res)
    l_vals = np.linspace(L_MIN, L_MAX, res)
    
    # Buffers
    C_grid = np.zeros((res, res, 3)) # Color
    H_grid = np.zeros((res, res))    # Helicity
    L_grid = np.zeros((res, res))    # Lyapunov
    S_grid = np.zeros((res, res))    # Steps/Mask
    
    print(f"Starting High-Res Scan ({res}x{res})...")
    start = time.time()
    
    for i in range(res):
        if i % 100 == 0: print(f"  Row {i}/{res}")
        lam = l_vals[i]
        for j in range(res):
            m = m_vals[j]
            r, g, b, h, ly, st, esc = trace_pixel_unified(m, lam)
            
            # Composite Color with Escape Alpha
            if esc:
                intensity = 0.2 + 0.8 * st # Brighter if it survived longer
                C_grid[i,j,:] = [r*intensity, g*intensity, b*intensity]
            else:
                C_grid[i,j,:] = [r, g, b]
                
            H_grid[i,j] = h
            L_grid[i,j] = ly
            S_grid[i,j] = st
            
    print(f"Scan Complete. Time: {time.time() - start:.2f}s")
    return m_vals, l_vals, C_grid, H_grid, L_grid, S_grid

# --- VISUALIZATION ENGINE ---
def render_views():
    import time
    
    # 1. Compile JIT (Run dummy)
    trace_pixel_unified(0.1, 0.1)
    
    # 2. Generate Data
    m, l, C, H, L, S = generate_data_cubes()
    extent = [M_MIN, M_MAX, L_MIN, L_MAX]
    
    print("Rendering Views...")
    
    # --- VIEW 1: THE DASHBOARD (Combined) ---
    fig, axs = plt.subplots(2, 2, figsize=(16, 16))
    
    # Top Left: Helicity
    im1 = axs[0,0].imshow(H, origin='lower', extent=extent, cmap='magma', aspect='auto')
    axs[0,0].set_title("Helicity (Rotational Sensitivity)")
    plt.colorbar(im1, ax=axs[0,0], fraction=0.046, pad=0.04)
    
    # Top Right: Lyapunov
    # Center colormap around 0
    divnorm = colors.TwoSlopeNorm(vmin=np.min(L), vcenter=(np.max(L)-np.min(L))/2, vmax=np.max(L))
    im2 = axs[0,1].imshow(L, origin='lower', extent=extent, cmap='seismic', norm=divnorm, aspect='auto')
    axs[0,1].set_title("Lyapunov Exponent (Stability vs Chaos)")
    plt.colorbar(im2, ax=axs[0,1], fraction=0.046, pad=0.04)
    
    # Bottom Left: Chromatic
    axs[1,0].imshow(C, origin='lower', extent=extent, aspect='auto')
    axs[1,0].set_title("Chromatic Field (Force Dominance)")
    
    # Bottom Right: The Mask (Escape Time)
    im4 = axs[1,1].imshow(S, origin='lower', extent=extent, cmap='gist_earth', aspect='auto')
    axs[1,1].set_title("The Mask (Escape Time Basin)")
    plt.colorbar(im4, ax=axs[1,1], fraction=0.046, pad=0.04)
    
    plt.tight_layout()
    plt.savefig("V10_Dashboard.png", dpi=200)
    plt.close()
    
    # --- VIEW 2: SINGULAR HELICITY ---
    plt.figure(figsize=(12, 12))
    plt.imshow(H, origin='lower', extent=extent, cmap='magma')
    plt.title("Detailed Helicity Map")
    plt.axis('off') # Pure data
    plt.savefig("V10_Helicity_Singular.png", dpi=300, bbox_inches='tight', pad_inches=0)
    plt.close()
    
    # --- VIEW 3: SINGULAR LYAPUNOV ---
    plt.figure(figsize=(12, 12))
    plt.imshow(L, origin='lower', extent=extent, cmap='RdBu_r', norm=divnorm)
    plt.title("Detailed Lyapunov Map")
    plt.axis('off')
    plt.savefig("V10_Lyapunov_Singular.png", dpi=300, bbox_inches='tight', pad_inches=0)
    plt.close()
    
    # --- VIEW 4: SINGULAR MASK (Escape Fractal) ---
    plt.figure(figsize=(12, 12))
    # Using 'hot' reversed or 'bone' creates a very structural look for masks
    plt.imshow(S, origin='lower', extent=extent, cmap='gnuplot2') 
    plt.title("Detailed Basin Mask")
    plt.axis('off')
    plt.savefig("V10_Mask_Singular.png", dpi=300, bbox_inches='tight', pad_inches=0)
    plt.close()

    print("All views rendered successfully.")

if __name__ == "__main__":
    render_views()