import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

# =========================================================
#  PROTON ENGINE: "GHOST HUNTER" PROTOCOL (NO NUMBA)
# =========================================================

# --- CONFIGURATION ---
OUTPUT_FILENAME = "proton_ghost_hunter_affine.gif"
FRAMES = 120            # Reduced for runtime
GLOBAL_SCALE = 32.0     

# LAYOUT DIMENSIONS
PILOT_SIZE = 150        
PILOT_COLS = 2          
PILOT_PANEL_W = PILOT_SIZE * PILOT_COLS
MAP_DIM = 450           
SIDE_W = 250            
MAIN_H = 450            
BOTTOM_H = 150          
TOTAL_W = PILOT_PANEL_W + MAP_DIM + SIDE_W

# PHYSICS: 6 SOURCES
SRC_STRONG_M = np.array([-10.0, 10.0, 0.0])
SRC_STRONG_L = np.array([5.0, 5.0, -10.0])
SRC_WEAK_M = np.array([5.0, 5.0, -5.0]) 
SRC_WEAK_L = np.array([-5.0, 2.5, 2.5]) 

# TARGET HINTS
HINTS_STRONG = [(-10.0, 5.0), (10.0, 5.0), (0.0, -10.0)]
HINTS_GHOST = [(0.0, 5.0), (5.0, -2.5), (-5.0, -2.5)]

COLORS_STRONG = [(0, 255, 255), (255, 0, 255), (255, 255, 0)] 
COLORS_GHOST = [(255, 50, 50), (50, 255, 50), (50, 100, 255)]  

# --- MATH KERNEL (VECTORIZED) ---

def render_microscope(center_m, center_l, width, res, pulse):
    half_w = width / 2.0
    m_vals = np.linspace(center_m - half_w, center_m + half_w, res)
    l_vals = np.linspace(center_l - half_w, center_l + half_w, res)
    M, L = np.meshgrid(m_vals, l_vals)
    
    psi_real = np.zeros((res, res), dtype=np.float64)
    psi_imag = np.zeros((res, res), dtype=np.float64)
    
    theta = pulse['theta']
    c, s = np.cos(theta), np.sin(theta)
    
    # 1. STRONG SOURCES
    for i in range(3):
        sm = SRC_STRONG_M[i]*c - SRC_STRONG_L[i]*s
        sl = SRC_STRONG_M[i]*s + SRC_STRONG_L[i]*c
        
        dx = M - sm
        dy = L - sl
        r = np.sqrt(dx**2 + dy**2)
        r[r < 1e-12] = 1e-12
        
        k = (2 * np.pi) / (10.0)
        phase = k * r
        amp = (1.0 / r)
        psi_real += amp * np.cos(phase)
        psi_imag += amp * np.sin(phase)

    # 2. GHOST SOURCES
    for i in range(3):
        sm = SRC_WEAK_M[i]*c - SRC_WEAK_L[i]*s
        sl = SRC_WEAK_M[i]*s + SRC_WEAK_L[i]*c
        
        dx = M - sm
        dy = L - sl
        r = np.sqrt(dx**2 + dy**2)
        r[r < 1e-12] = 1e-12
        
        k = (2 * np.pi) / (5.0) 
        phase = k * r
        amp = (0.4 / r) 
        psi_real += amp * np.cos(phase)
        psi_imag += amp * np.sin(phase)

    return psi_real**2 + psi_imag**2

def find_peak(img, width, center_m, center_l):
    res = img.shape[0]
    idx = np.unravel_index(np.argmax(img), img.shape)
    pixel_l = (center_l - width/2) + idx[0] * (width / (res - 1))
    pixel_m = (center_m - width/2) + idx[1] * (width / (res - 1))
    return np.max(img), pixel_m, pixel_l

# --- AFFINE KERNEL (NEW) ---

def triangle_affine(S, G):
    """
    Given two triangles S = [S0,S1,S2], G = [G0,G1,G2],
    each vertex a 2D point-like iterable, return the
    affine transform (A, b) such that:
        T(x) = A @ x + b
        T(Si) = Gi  for i=0,1,2
    """
    if len(S) != 3 or len(G) != 3:
        raise ValueError("Triangles must have exactly 3 vertices.")
        
    S0, S1, S2 = map(lambda p: np.array(p, dtype=float), S)
    G0, G1, G2 = map(lambda p: np.array(p, dtype=float), G)

    # 2x2 matrices with columns as edge vectors from S0/G0
    MS = np.column_stack((S1 - S0, S2 - S0))
    MG = np.column_stack((G1 - G0, G2 - G0))

    # A = MG @ inv(MS) transforms S-space to G-space
    A = MG @ np.linalg.inv(MS)
    
    # b is the translation vector: b = G0 - A @ S0
    b = G0 - A @ S0
    return A, b

def decompose_zoom(A):
    """
    Decomposes the 2x2 affine matrix A into scale, angle, and shear.
    """
    det = np.linalg.det(A)
    scale = np.sqrt(abs(det))

    # Normalize A to look at pure rotation + shear
    A_ns = A / (scale + 1e-12)

    # SVD: A_ns = U @ Σ @ V^T -> R = U @ V^T is the closest rotation
    U, s, Vt = np.linalg.svd(A_ns)
    R = U @ Vt

    # Rotation angle (from R[1,0] = sin(angle), R[0,0] = cos(angle))
    angle = np.arctan2(R[1,0], R[0,0])

    # s are the singular values, representing anisotropic stretch (shear)
    return scale, angle, s, R

# --- NEW GEOMETRY HELPER FUNCTION ---

def calculate_triangle_area(p0, p1, p2):
    """
    Calculates the area of a triangle given three 2D vertices.
    Area = 0.5 * |(x1-x0)(y2-y0) - (x2-x0)(y1-y0)|
    """
    x0, y0 = p0
    x1, y1 = p1
    x2, y2 = p2
    
    # Determinant part of the cross product for the area formula
    return 0.5 * np.abs((x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0))

# -----------------------------

# --- TRACKER ---

class ParticleTracker:
    def __init__(self, hint, pid, ptype):
        self.id = pid
        self.type = ptype 
        self.cam_m, self.cam_l = hint
        self.width = 6.0 if ptype == 'GHOST' else 8.0
        self.color = COLORS_GHOST[pid] if ptype == 'GHOST' else COLORS_STRONG[pid]
        self.history = []
        self.intensity_log = []
        
    def update(self, pulse):
        # 1. Scan
        scan = render_microscope(self.cam_m, self.cam_l, self.width, 80, pulse)
        
        # 2. Lock
        peak, pm, pl = find_peak(scan, self.width, self.cam_m, self.cam_l)
        
        # 3. Move (Damped)
        damp = 0.5 if self.type == 'STRONG' else 0.2
        self.cam_m += (pm - self.cam_m) * damp
        self.cam_l += (pl - self.cam_l) * damp
        
        self.history.append((self.cam_m, self.cam_l))
        self.intensity_log.append(peak)

    def render_pilot(self, pulse):
        # Context
        ctx_w = self.width * 5.0
        raw_ctx = render_microscope(self.cam_m, self.cam_l, ctx_w, PILOT_SIZE, pulse)
        norm_ctx = (raw_ctx - raw_ctx.min()) / (raw_ctx.max() - raw_ctx.min() + 1e-9)
        
        # Core
        raw_core = render_microscope(self.cam_m, self.cam_l, self.width, PILOT_SIZE, pulse)
        norm_core = (raw_core - raw_core.min()) / (raw_core.max() - raw_core.min() + 1e-9)
        
        # Blend
        boost = 0.6 if self.type == 'GHOST' else 0.3
        final = (norm_core * 0.7) + (norm_ctx * boost)
        final = np.clip(final, 0, 1)
        
        # Colorize
        c_vec = np.array(self.color) / 255.0
        rgb = np.dstack((final * c_vec[0], final * c_vec[1], final * c_vec[2]))
        
        # Hotspot
        mask = norm_core > 0.9
        rgb[mask] = rgb[mask] * 0.5 + 0.5
        
        img = Image.fromarray((rgb * 255).astype(np.uint8))
        d = ImageDraw.Draw(img)
        label = f"M-{self.id+1}" if self.type == 'STRONG' else f"G-{self.id+1}"
        d.text((5, 5), label, fill=self.color)
        return img

# --- DASHBOARD RENDERER ---

def render_spectrograph(trackers, width, height):
    img = Image.new('RGB', (width, height), (5, 5, 10))
    d = ImageDraw.Draw(img)
    
    d.text((20, 10), "RESONANCE SPECTROGRAPH [GHOST INTENSITY]", fill=(200, 200, 200))
    
    plot_h = height - 40
    plot_w = width - 40
    ox, oy = 20, 30
    
    ghosts = [t for t in trackers if t.type == 'GHOST']
    
    for g in ghosts:
        data = g.intensity_log[-100:]
        if not data: continue
        
        d_min, d_max = min(data), max(data)
        if d_max == d_min: d_max += 1e-9
        
        pts = []
        step_x = plot_w / 100
        
        for i, val in enumerate(data):
            x = ox + i * step_x
            norm_y = (val - d_min) / (d_max - d_min)
            y = (oy + plot_h) - (norm_y * plot_h)
            pts.append((x, y))
            
        if len(pts) > 1:
            d.line(pts, fill=g.color, width=2)
            
    d.line([ox, oy+plot_h/2, ox+plot_w, oy+plot_h/2], fill=(50, 50, 50))
    return img

# --- MISSION ---

def run_ghost_hunt():
    print("--- 👻 INITIATING GHOST PROTOCOL ---")
    
    trackers = []
    # 3 Strong
    for i, h in enumerate(HINTS_STRONG):
        trackers.append(ParticleTracker(h, i, 'STRONG'))
    # 3 Ghosts
    for i, h in enumerate(HINTS_GHOST):
        trackers.append(ParticleTracker(h, i, 'GHOST'))
        
    frames_buffer = []
    affine_log = [] # <<< NEW: Log for affine map analysis
    
    for f in range(FRAMES):
        pulse = {
            'theta': 2 * np.pi * (f / 100),
            'amp_boost': 1.0 + 0.2 * np.sin(f * 0.1)
        }
        
        # 1. Update Trackers
        for t in trackers: t.update(pulse)
        
        # 2. Render Pilots
        pilots = [t.render_pilot(pulse) for t in trackers]
        panel_a = Image.new('RGB', (PILOT_PANEL_W, MAIN_H))
        for i in range(3):
            panel_a.paste(pilots[i], (0, i * PILOT_SIZE))
            panel_a.paste(pilots[i+3], (PILOT_SIZE, i * PILOT_SIZE))
            
        # 3. Render Map
        raw_map = render_microscope(0, 0, GLOBAL_SCALE, MAP_DIM, pulse)
        norm_map = (raw_map - raw_map.min()) / (raw_map.max() - raw_map.min() + 1e-9)
        norm_map = np.power(norm_map, 0.4)
        map_rgb = (plt.get_cmap('inferno')(norm_map)[:, :, :3] * 255).astype(np.uint8)
        panel_b = Image.fromarray(np.flipud(map_rgb))
        d_map = ImageDraw.Draw(panel_b)
        
        # Get latest points
        strong_pts = [t.history[-1] for t in trackers if t.type=='STRONG']
        ghost_pts = [t.history[-1] for t in trackers if t.type=='GHOST']
        
        # --- 4. COMPUTE AFFINE MAP (NEW INTEGRATION) ---
        A, b = None, None
        scale, angle, shear_s = 0.0, 0.0, [1.0, 1.0] # default values
        
        if len(strong_pts) == 3 and len(ghost_pts) == 3:
            try:
                A, b = triangle_affine(strong_pts, ghost_pts)
                scale, angle, s, R = decompose_zoom(A)
                shear_s = s
                
                # NEW: Calculate triangle areas
                area_S = calculate_triangle_area(*strong_pts)
                area_G = calculate_triangle_area(*ghost_pts)
                
                # Avoid division by zero if area_S is too small
                area_ratio = area_G / (area_S + 1e-9) 
                
                affine_log.append({
                    'A': A, 'b': b, 'scale': scale, 'angle': angle, 
                    'shear_s': shear_s, 'area_ratio': area_ratio
                })
                
            except np.linalg.LinAlgError:
                print(f"Warning: Frame {f} - Collinear vertices, skipping affine compute.")
        # -----------------------------------------------

        def to_px(m, l):
            x = (m - (-GLOBAL_SCALE/2)) / GLOBAL_SCALE * (MAP_DIM-1)
            y = (MAP_DIM-1) - ((l - (-GLOBAL_SCALE/2)) / GLOBAL_SCALE * (MAP_DIM-1))
            return x, y
            
        s_px = [to_px(*p) for p in strong_pts]
        g_px = [to_px(*p) for p in ghost_pts]
        
        if len(s_px) == 3: d_map.polygon(s_px, outline=(200, 200, 200), width=1)
        if len(g_px) == 3: d_map.polygon(g_px, outline=(100, 100, 100), width=1)
            
        for i, p in enumerate(s_px):
            d_map.ellipse([p[0]-4, p[1]-4, p[0]+4, p[1]+4], fill=COLORS_STRONG[i], outline=(255,255,255))
        for i, p in enumerate(g_px):
            d_map.ellipse([p[0]-3, p[1]-3, p[0]+3, p[1]+3], fill=COLORS_GHOST[i], outline=(255,255,255))
            
        # 5. Render Helix
        panel_c = Image.new('RGB', (SIDE_W, MAIN_H), (10, 5, 20))
        d_side = ImageDraw.Draw(panel_c)
        d_side.text((10, 10), "HELIX [ALL TRACKS]", fill=(150, 150, 150))
        
        hist_len = 50
        y_step = (MAIN_H - 20) / hist_len
        start_y = 20
        
        for ti, t in enumerate(trackers):
            hist = t.history[-hist_len:]
            pts = []
            for i, (m, l) in enumerate(hist):
                # Normalize M-L to SIDE_W width
                px = (m - (-GLOBAL_SCALE/2)) / GLOBAL_SCALE * (SIDE_W - 1) 
                py = start_y + i * y_step
                pts.append((px, py))
            if len(pts) > 1: d_side.line(pts, fill=t.color, width=2)

        # 6. Bottom Panel
        panel_d = render_spectrograph(trackers, TOTAL_W, BOTTOM_H)
        
        # 7. Composite
        final = Image.new('RGB', (TOTAL_W, MAIN_H + BOTTOM_H))
        final.paste(panel_a, (0, 0))
        final.paste(panel_b, (PILOT_PANEL_W, 0))
        final.paste(panel_c, (PILOT_PANEL_W + MAP_DIM, 0))
        final.paste(panel_d, (0, MAIN_H))
        
        frames_buffer.append(final)
        if f % 20 == 0: print(f"Frame {f} | Tracking 6 Targets...")


    print(f"Saving {OUTPUT_FILENAME}...")
    frames_buffer[0].save(OUTPUT_FILENAME, save_all=True, append_images=frames_buffer[1:], duration=50, loop=0)

    # --- 8. CRITICAL STEP: SAVE INTENSITY LOGS ---
    log_data = {}
    for i, t in enumerate(trackers):
        name = f"M{i+1}" if t.type == 'STRONG' else f"G{i-2}"
        log_data[name] = np.array(t.intensity_log)

    log_filename = 'intensity_logs.npy'
    np.save(log_filename, log_data)
    print(f"Saved intensity logs to {log_filename}")

    # --- 9. REFLEXIVE ANALYSIS REPORT (ENHANCED with FFT) ---

    # FFT Helper Function
    def analyze_frequency(log_array):
        # We assume the time step d=1 (frame number)
        N = len(log_array)
        if N < 2: return 0.0
        
        # FFT and Frequencies
        fft_result = np.abs(np.fft.fft(log_array))
        freqs = np.fft.fftfreq(N, d=1)
        
        # Find peak frequency, excluding DC component (index 0)
        # We need to look up to N/2 (Nyquist)
        # +1 is needed because argmax returns the index relative to the sliced array
        idx = np.argmax(fft_result[1:N//2]) + 1 
        
        return freqs[idx]
    
    if affine_log:
        all_scales = np.array([log['scale'] for log in affine_log])
        all_angles = np.array([log['angle'] for log in affine_log])
        all_shear_s0 = np.array([log['shear_s'][0] for log in affine_log])
        all_shear_s1 = np.array([log['shear_s'][1] for log in affine_log])
        all_area_ratios = np.array([log['area_ratio'] for log in affine_log])
        
        # New: Translation Vector Analysis
        all_b = np.array([log['b'] for log in affine_log])
        mean_b = np.mean(all_b, axis=0)
        
        # New: Shear Anisotropy Fluctuation
        # Ratio of singular values s0/s1 (anisotropy)
        shear_anisotropy = all_shear_s0 / all_shear_s1
        # Calculate fluctuation (Standard Deviation)
        # Using log to stabilize the variance calculation
        log_shear_anisotropy_std = np.std(np.log(shear_anisotropy + 1e-9))
        
        # Unwrap and find total twist (change in angle)
        unwrapped_angles = np.unwrap(all_angles)
        total_twist = unwrapped_angles[-1] - unwrapped_angles[0]

        # --- NEW: DYNAMIC ANALYSIS (FFT) ---
        
        strong_freqs = []
        ghost_freqs = []
        
        for name, log in log_data.items():
            freq = analyze_frequency(log)
            if name.startswith('M'):
                strong_freqs.append(freq)
            else:
                ghost_freqs.append(freq)

        mean_f_strong = np.mean(strong_freqs)
        mean_f_ghost = np.mean(ghost_freqs)
        
        # Calculate the fundamental dynamic ratio
        frequency_ratio = mean_f_ghost / (mean_f_strong + 1e-9)

        # CODE SNIPPET FOR VISUALIZATION (Next user action)


        # Load the saved data
        log_data = np.load('intensity_logs.npy', allow_pickle=True).item()

        # Get data
        M1_log = log_data['M1']
        G1_log = log_data['G1']
        N = len(M1_log)

        # FFT for M1
        fft_M1 = np.abs(np.fft.fft(M1_log))[1:N//2]
        freqs = np.fft.fftfreq(N, d=1)[1:N//2]

        # FFT for G1
        fft_G1 = np.abs(np.fft.fft(G1_log))[1:N//2]

        plt.figure(figsize=(10, 5))
        plt.plot(freqs, fft_M1, label='Strong (M1)', marker='o', linestyle='--')
        plt.plot(freqs, fft_G1, label='Ghost (G1)', marker='x', linestyle='-')
        plt.title('Intensity Log FFT Comparison')
        plt.xlabel('Frequency (cycles/frame)')
        plt.ylabel('Amplitude')
        plt.legend()
        plt.grid(True)
        plt.show()

        # Print peak indices for confirmation
        print(f"M1 Peak Index: {np.argmax(fft_M1) + 1} at frequency {freqs[np.argmax(fft_M1)]:.5f}")
        print(f"G1 Peak Index: {np.argmax(fft_G1) + 1} at frequency {freqs[np.argmax(fft_G1)]:.5f}")
        
        print("\n--- 🔬 REFLEXIVE GEOMETRY REPORT (ENHANCED) ---")
        
        # --- BASE METRICS ---
        print("\n## 🌌 Base Kinematics (A Matrix)")
        print(f"Mean Fractal Scale (Zoom Factor): {np.mean(all_scales):.4f}")
        print(f"Total Twist (Radian): {total_twist:.4f} rad")
        
        # --- 1. AFFINE INVARIANT (AREA RATIO) ---
        print("\n## 📐 Affine Invariant (Area Ratio)")
        print(f"Mean Area Ratio (Ghost/Strong): {np.mean(all_area_ratios):.4f}")
        
        # --- 2. ISOTROPIC CONFORMALITY FLUCTUATIONS ---
        print("\n## 🌪️ Conformal Stress (Shear)")
        print(f"Mean Anisotropic Shear (s0/s1): {np.mean(shear_anisotropy):.4f}")
        print(f"Anisotropic Shear Fluctuation (σ(log(s0/s1))): {log_shear_anisotropy_std:.4f}")
        
        # --- 3. TOTAL DISPLACEMENT VECTOR ---
        print("\n## 🛰️ Total Displacement (Translation Vector)")
        print(f"Mean Translation Vector ⟨b⟩: M={mean_b[0]:.4f}, L={mean_b[1]:.4f}")
        print(f"Mean Displacement Magnitude |⟨b⟩|: {np.linalg.norm(mean_b):.4f}")
        print("----------------------------------")

        # --- 4. DYNAMIC FREQUENCY ANALYSIS (NEW) ---
        print("\n## 🎶 Dynamic Frequency Analysis")
        print(f"Mean Strong Source Freq ⟨f_M⟩: {mean_f_strong:.5f} cycles/frame")
        print(f"Mean Ghost Source Freq ⟨f_G⟩: {mean_f_ghost:.5f} cycles/frame")
        print(f"Dynamic Frequency Ratio ⟨f_G⟩/⟨f_M⟩: {frequency_ratio:.4f}")
        
        # --- 5. MASS HIERARCHY TEST ---
        # Test against the two proposed scaling constants
        phi_sq_ratio = 2.61803**2 # phi^4 scaling (for mu/e and tau/mu)
        
        print("\n## 🧬 Mass Hierarchy Test")
        print(f"Test 1: Dynamic Ratio vs. Predicted Geometric Ratio (2π/3) = 2.0944")
        print(f"Error: {100 * np.abs(frequency_ratio - 2.0944) / 2.0944:.2f}%")
        
        print(f"Test 2: Dynamic Ratio vs. Predicted Golden Ratio Scaling (φ²) = 2.618")
        print(f"Error: {100 * np.abs(frequency_ratio - 2.618) / 2.618:.2f}%")
        print("----------------------------------")
    
    print("✅ GHOSTS CAPTURED.")


if __name__ == "__main__":
    run_ghost_hunt()