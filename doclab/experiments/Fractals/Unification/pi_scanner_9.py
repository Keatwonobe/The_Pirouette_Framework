import numpy as np
import matplotlib.pyplot as plt
from numba import njit
import time
from scipy.ndimage import binary_erosion, maximum_filter 

# =========================================================
#  UNIFIED PROTON SCANNER (Single-View Multi-Analysis)
#  V9: Added Maximal Lyapunov Exponent (Analysis 4)
# =========================================================

# --- GLOBAL CONFIGURATION ---
M_MIN, M_MAX = -240000000000, 240000000000
L_MIN, L_MAX = -240000000000, 240000000000
RES_BASE = 1000      # Grid resolution for all analyses
MAX_STEPS = 500      
R_ESCAPE = 1000.0    
EPSILON = 1e-8       # Perturbation for Helicity and Lyapunov calculations

# --- PHYSICS PARAMETERS ---
TWIST = 3.8
GAMMA = 0.5
DT    = 0.015
HELICITY_STOP = np.pi * 0.95
RESYNCH_STEPS = 10   # Resynchronization steps for Lyapunov Exponent

# --- CORE DYNAMICS (Unified) ---
@njit
def normalize_angle_diff(delta):
    return np.arctan2(np.sin(delta), np.cos(delta))

@njit
def get_force_weights(m, lam):
    """Returns the weights of the three forces (R, T, G) and all 3 forces for trajectory."""
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

# --- ANALYSIS 1 CORE: HELICITY AND GEOMETRY ---
@njit
def measure_helicity(m0, l0):
    """Run real + shadow trajectory and return log(max angular decorrelation)."""
    # ... (Implementation omitted for brevity, identical to the provided code)
    m1, l1 = m0, l0
    pm1, pl1 = 0.0, 0.0
    m2, l2 = m0 + EPSILON, l0 + EPSILON
    pm2, pl2 = 0.0, 0.0
    max_diff_angle = 0.0

    for _ in range(MAX_STEPS):
        nw_red1, nw_teal1, nw_gold1, Frm1, Frl1, Ftm1, Ftl1, Fgm1, Fgl1 = get_force_weights(m1, l1)
        Fm1 = nw_teal1 * Ftm1 + nw_red1 * Frm1 + nw_gold1 * Fgm1
        Flam1 = nw_teal1 * Ftl1 + nw_red1 * Frl1 + nw_gold1 * Fgl1
        drag1 = 1.0 / (1.0 + 0.5 * DT * GAMMA * nw_red1)
        pm1 = (pm1 + 0.5 * DT * Fm1) * drag1
        pl1 = (pl1 + 0.5 * DT * Flam1) * drag1
        m1 += DT * pm1
        l1 += DT * pl1
        
        nw_red2, nw_teal2, nw_gold2, Frm2, Frl2, Ftm2, Ftl2, Fgm2, Fgl2 = get_force_weights(m2, l2)
        Fm2 = nw_teal2 * Ftm2 + nw_red2 * Frm2 + nw_gold2 * Fgm2
        Flam2 = nw_teal2 * Ftl2 + nw_red2 * Frl2 + nw_gold2 * Fgl2
        drag2 = 1.0 / (1.0 + 0.5 * DT * GAMMA * nw_red2)
        pm2 = (pm2 + 0.5 * DT * Fm2) * drag2
        pl2 = (pl2 + 0.5 * DT * Flam2) * drag2
        m2 += DT * pm2
        l2 += DT * pl2
        
        diff = normalize_angle_diff(np.arctan2(l1, m1) - np.arctan2(l2, m2))
        max_diff_angle = max(max_diff_angle, np.abs(diff))
        
        if max_diff_angle > HELICITY_STOP or (m1**2 + l1**2) > R_ESCAPE**2:
            break
            
    return np.log(max_diff_angle + EPSILON)

def compute_helicity_grid(m_vals, l_vals):
    # ... (Wrapper implementation omitted for brevity)
    res = len(m_vals)
    H = np.zeros((res, res), dtype=float)
    # This takes time, but must be run
    for i, lam in enumerate(l_vals):
        for j, m in enumerate(m_vals):
            H[i, j] = measure_helicity(m, lam)
    return H

# ... (box_counting_dimension omitted for brevity)
def box_counting_dimension(boundary_mask):
    scales = 2**np.arange(1, 8)  
    counts = []
    
    for box_size in scales:
        ny, nx = boundary_mask.shape
        if box_size > min(ny, nx): break

        n_boxes_y = (ny + box_size - 1) // box_size
        n_boxes_x = (nx + box_size - 1) // box_size
        
        count = 0
        for i in range(n_boxes_y):
            for j in range(n_boxes_x):
                y_start, y_end = i*box_size, min((i+1)*box_size, ny)
                x_start, x_end = j*box_size, min((j+1)*box_size, nx)
                
                box = boundary_mask[y_start:y_end, x_start:x_end]
                if np.any(box):
                    count += 1
        counts.append(count)
    
    log_r = np.log(scales[:len(counts)])
    log_N = np.log(counts)
    
    if len(log_r) < 2: return np.nan
        
    coeffs = np.polyfit(log_r, log_N, 1)
    D_f = -coeffs[0]
    return D_f

# --- ANALYSIS 2 CORE: CHROMATIC FIELD ---
@njit
def trace_chromatic_pixel(m0, l0):
    """Traces a particle to get final Color Charge and Escape Info (from pi_scanner_6.py)"""
    # ... (Implementation omitted for brevity, identical to the provided code)
    m, l = m0, l0
    pm, pl = 0.0, 0.0
    total_red, total_teal, total_gold = 0.0, 0.0, 0.0
    total_winding = 0.0
    prev_angle = np.arctan2(l, m)
    steps_taken = 0
    escaped = False
    
    for i in range(MAX_STEPS):
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
            
    norm = total_red + total_teal + total_gold + 1e-9
    r_val = total_red / norm
    g_val = total_teal / norm 
    b_val = total_gold / norm 
    
    return steps_taken, escaped, r_val, g_val, b_val, total_winding

def render_chromatic_scan(m_vals, l_vals):
    # ... (Wrapper implementation omitted for brevity)
    h, w = len(l_vals), len(m_vals)
    image = np.zeros((h, w, 4)) 
    escape_mask = np.zeros((h, w), dtype=np.bool_) 
    
    # This takes time, but must be run
    for i in range(h):
        for j in range(w):
            steps, escaped, r, g, b, winding = trace_chromatic_pixel(m_vals[j], l_vals[i])
            
            if not escaped:
                intensity = 1.0
                if abs(winding) > 6*np.pi: intensity = 0.6 
            else:
                nu = np.log(np.log(m_vals[j]**2 + l_vals[i]**2)) / np.log(2)
                smooth_steps = steps + 1 - nu
                intensity = 0.1 + 0.9 * (smooth_steps / MAX_STEPS) 

            image[i, j, 0] = r 
            image[i, j, 1] = g
            image[i, j, 2] = b
            image[i, j, 3] = intensity 
            
            escape_mask[i, j] = not escaped 
            
    return image, escape_mask 


# --- ANALYSIS 4 CORE: LYAPUNOV EXPONENT (NEW) ---

@njit
def measure_lyapunov_exponent(m0, l0):
    """Calculates the Maximal Lyapunov Exponent (LE) using the resynchronization method."""
    m, l = m0, l0
    pm, pl = 0.0, 0.0
    
    dm, dl = EPSILON, EPSILON 
    d = np.sqrt(dm**2 + dl**2)
    dm, dl = dm * (EPSILON / d), dl * (EPSILON / d)
    
    sum_log_expansion = 0.0
    resynch_count = MAX_STEPS // RESYNCH_STEPS
    
    if resynch_count == 0: return 0.0 

    for k in range(resynch_count):
        
        for _ in range(RESYNCH_STEPS):
            # Trajectory (m, l)
            nw_red, nw_teal, nw_gold, Frm, Frl, Ftm, Ftl, Fgm, Fgl = get_force_weights(m, l)
            Fm = nw_teal * Ftm + nw_red * Frm + nw_gold * Fgm
            Flam = nw_teal * Ftl + nw_red * Frl + nw_gold * Fgl
            drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * nw_red)
            pm = (pm + 0.5 * DT * Fm) * drag
            pl = (pl + 0.5 * DT * Flam) * drag
            m += DT * pm
            l += DT * pl

            # Shadow Trajectory (m_s, l_s) for simplified perturbation (dm, dl) update
            m_s, l_s = m + dm, l + dl
            
            # Shadow Force/Dynamics (using force at shadow point)
            nw_red_s, nw_teal_s, nw_gold_s, Frm_s, Frl_s, Ftm_s, Ftl_s, Fgm_s, Fgl_s = get_force_weights(m_s, l_s)
            Fm_s = nw_teal_s * Ftm_s + nw_red_s * Frm_s + nw_gold_s * Fgm_s
            Flam_s = nw_teal_s * Ftl_s + nw_red_s * Frl_s + nw_gold_s * Fgl_s
            drag_s = 1.0 / (1.0 + 0.5 * DT * GAMMA * nw_red_s)
            
            # Simplified update of the perturbation vector (dm, dl) using difference in forces
            dFm = Fm_s - Fm
            dFlam = Flam_s - Flam
            
            dpm = (dm + 0.5 * DT * dFm) * drag_s 
            dpl = (dl + 0.5 * DT * dFlam) * drag_s
            dm += DT * dpm
            dl += DT * dpl
            
            if (m*m + l*l) > R_ESCAPE**2:
                return 10.0 

        d_new = np.sqrt(dm**2 + dl**2)
        
        if d_new < 1e-15: 
            total_time = (k + 1) * RESYNCH_STEPS * DT
            return sum_log_expansion / (total_time + 1e-9)

        sum_log_expansion += np.log(d_new / EPSILON)
        
        dm = dm * (EPSILON / d_new)
        dl = dl * (EPSILON / d_new)
        

    total_time = resynch_count * RESYNCH_STEPS * DT
    lyapunov_exponent = sum_log_expansion / (total_time + 1e-9)
    return lyapunov_exponent

def compute_lyapunov_grid(m_vals, l_vals):
    # ... (Wrapper implementation omitted for brevity)
    res = len(m_vals)
    Lambda = np.zeros((res, res), dtype=float)
    # This takes time, but must be run
    for i, lam in enumerate(l_vals):
        for j, m in enumerate(m_vals):
            Lambda[i, j] = measure_lyapunov_exponent(m, lam)
    return Lambda

# --- ANALYSIS 3 CORE: MICROSCOPE ZOOM ---
def run_microscope_zoom(m_knot, l_knot, zoom_radius=12):
    # ... (Implementation omitted for brevity)
    RES = 500 
    m_min, m_max = m_knot - zoom_radius, m_knot + zoom_radius
    l_min, l_max = l_knot - zoom_radius, l_knot + zoom_radius
    m_vals = np.linspace(m_min, m_max, RES)
    l_vals = np.linspace(l_min, l_max, RES)
    
    # We re-use the chromatic render function for this
    img_core_raw, _ = render_chromatic_scan(m_vals, l_vals) 
    
    # Post-process for display
    final_core = np.zeros((RES, RES, 3))
    bg = np.array([0.05, 0.0, 0.0]) 
    alpha = img_core_raw[:,:,3]
    rgb = img_core_raw[:,:,0:3]
    for c in range(3):
        final_core[:,:,c] = rgb[:,:,c] * alpha + bg[c] * (1 - alpha)
        
    plt.figure(figsize=(8, 8))
    plt.imshow(final_core, origin='lower', extent=[m_min, m_max, l_min, l_max])
    plt.plot(m_knot, l_knot, 'w+', markersize=15, label="Knot Singularity")
    plt.title(f"Analysis 3: Microscope - The Knot Event Horizon\n(Zoom Radius: {zoom_radius})")
    plt.xlabel("Mass Field (m)")
    plt.ylabel("Coupling Field (λ)")
    plt.legend()
    plt.tight_layout()
    plt.savefig("analysis_3_quark_singularity_core.png", dpi=300)
    plt.close()

# --- MASTER RUN FUNCTION (The Orchestrator) ---
def run_unified_analysis(m_min=M_MIN, m_max=M_MAX, l_min=L_MIN, l_max=L_MAX, res=RES_BASE):
    m_vals = np.linspace(m_min, m_max, res)
    l_vals = np.linspace(l_min, l_max, res)
    extent_labels = [m_min, m_max, l_min, l_max]

    # JIT Compilation must run here before any timing begins.
    trace_chromatic_pixel(0.1, 0.1) 
    measure_helicity(0.1, 0.1)
    measure_lyapunov_exponent(0.1, 0.1) 
    
    ## 1. Stability and Geometry Analysis (Helicity) ##
    H = compute_helicity_grid(m_vals, l_vals)
    idx_flat = np.argmax(H)
    i, j = np.unravel_index(idx_flat, H.shape)
    m_knot, l_knot = m_vals[j], l_vals[i]
    basin_mask_h = H <= np.quantile(H, 0.25) 
    boundary_mask_h = binary_erosion(basin_mask_h)
    D_f_h = box_counting_dimension(basin_mask_h & ~boundary_mask_h)

    # Visualization A1 (Helicity)
    plt.figure(figsize=(10, 8))
    plt.imshow(np.clip(H, np.quantile(H, 0.01), np.quantile(H, 0.99)), origin="lower", extent=extent_labels, cmap="turbo", aspect='auto')
    plt.colorbar(label=r"Angular Decorrelation (Helicity $H$)")
    plt.title("Analysis 1: Stability Basin (Helicity Map)")
    plt.xlabel("Mass Field (m)")
    plt.ylabel("Coupling Field (λ)")
    plt.ticklabel_format(axis='both', style='sci', scilimits=(0,0))
    plt.tight_layout()
    plt.savefig("analysis_1_helicity_map.png", dpi=300)
    plt.close()

    ## 2. Chromatic Field Analysis ##
    raw_img, escape_mask = render_chromatic_scan(m_vals, l_vals)
    
    # D_f for Escape-Time based mask
    D_f_e = box_counting_dimension(escape_mask & ~binary_erosion(escape_mask))
    
    # Post-process for display
    final_img = np.zeros((res, res, 3))
    alpha = raw_img[:, :, 3]
    rgb = raw_img[:, :, 0:3]
    bg = np.array([0.0, 0.0, 0.05])
    for c in range(3): final_img[:, :, c] = rgb[:, :, c] * alpha + bg[c] * (1 - alpha)
    
    # Visualization A2 (Chromatic)
    plt.figure(figsize=(10, 10))
    plt.imshow(final_img, origin='lower', extent=extent_labels)
    plt.title(f"Analysis 2: Chromatic Structure\n(Red=Twist, Green=Stable, Blue=NonLinear)")
    plt.xlabel("Mass Field (m)")
    plt.ylabel("Coupling Field (λ)")
    plt.ticklabel_format(axis='both', style='sci', scilimits=(0,0))
    plt.tight_layout()
    plt.savefig("analysis_2_chromatic_scan.png", dpi=300)
    plt.close()

    ## 3. Holographic/Microscope Zoom ##
    run_microscope_zoom(m_knot, l_knot, zoom_radius=12.0) 
    
    ## 4. Lyapunov Exponent Scan (New) ##
    Lambda = compute_lyapunov_grid(m_vals, l_vals)
    
    # Visualization A4 (Lyapunov)
    plt.figure(figsize=(10, 8))
    plt.imshow(Lambda, origin="lower", extent=extent_labels, cmap="RdYlBu_r", aspect='auto')
    plt.colorbar(label=r"Maximal Lyapunov Exponent $\Lambda$")
    plt.title("Analysis 4: Maximal Lyapunov Exponent Scan\n(Red/Positive = Chaos, Blue/Negative = Stable)")
    plt.xlabel("Mass Field (m)")
    plt.ylabel("Coupling Field (λ)")
    plt.ticklabel_format(axis='both', style='sci', scilimits=(0,0))
    plt.tight_layout()
    plt.savefig("analysis_4_lyapunov_scan.png", dpi=300)
    plt.close()

if __name__ == "__main__":
    run_unified_analysis()