import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
from PIL import Image, ImageDraw
from scipy.interpolate import interp1d

# =========================================================
#  PROTON MICROSCOPE: PHASE-LOCKED ORBITER (v8.0)
#  "Synchronized Geometric Tracking"
# =========================================================

# --- CONFIGURATION ---
OUTPUT_FILENAME = "proton_phaselock_zoom.gif"
RENDER_RES = 500
RADAR_RES = 64
TOTAL_FRAMES = 140

# --- ZOOM SETTINGS ---
# We zoom from 21.0 down to 0.5 (Very deep dive)
# The Asymptotic curve ensures we don't crash.
ZOOM_START = 21.0
ZOOM_ASYMPTOTE = 11.69 

# --- PHYSICS ENGINE ---
SRC_M_BASE = np.array([-10.0, 10.0, 0.0])
SRC_L_BASE = np.array([5.0, 5.0, -10.0])

@njit(parallel=True)
def render_microscope(center_m, center_l, width, res, src_m, src_l, src_amp):
    half_w = width / 2.0
    m_vals = np.linspace(center_m - half_w, center_m + half_w, res)
    l_vals = np.linspace(center_l - half_w, center_l + half_w, res)
    intensity_map = np.zeros((res, res), dtype=np.float64)
    
    k_vec = np.zeros(3)
    for i in range(3):
        dist = np.sqrt(src_m[i]**2 + src_l[i]**2)
        k_vec[i] = (2 * np.pi) / (dist + 1e-9)

    for i in prange(res):
        y = l_vals[i]
        for j in range(res):
            x = m_vals[j]
            psi_real, psi_imag = 0.0, 0.0
            for q in range(3):
                dx = x - src_m[q]
                dy = y - src_l[q]
                r = np.sqrt(dx*dx + dy*dy)
                if r < 1e-12: r = 1e-12
                phase = k_vec[q] * r
                amp = (src_amp / r)
                psi_real += amp * np.cos(phase)
                psi_imag += amp * np.sin(phase)
            intensity_map[i, j] = psi_real**2 + psi_imag**2
    return intensity_map

def rotate_coords(m, l, theta):
    c, s = np.cos(theta), np.sin(theta)
    return m*c - l*s, m*s + l*c

# --- GEOMETRY ENGINE ---

class OrbitSynchronizer:
    def __init__(self):
        self.center = (0,0)
        self.major = 0
        self.minor = 0
        self.angle = 0
        self.phase_interpolator = None
        
    def fit_and_sync(self, valid_frames, raw_m, raw_l):
        """
        1. Fits ellipse to spatial data.
        2. Maps temporal data (frames) to ellipse angles (phase).
        """
        # --- A. SPATIAL FIT (PCA) ---
        data = np.vstack((raw_m, raw_l)).T
        self.center = np.mean(data, axis=0)
        centered = data - self.center
        cov = np.cov(centered.T)
        evals, evecs = np.linalg.eig(cov)
        
        # Sort eigenvectors
        sort_idx = np.argsort(evals)[::-1]
        evals = evals[sort_idx]
        evecs = evecs[:, sort_idx]
        
        self.major = 2.0 * np.sqrt(evals[0]) # 2 sigma
        self.minor = 2.0 * np.sqrt(evals[1])
        self.angle = np.arctan2(evecs[1, 0], evecs[0, 0])
        
        print(f"  > Geometry Locked: Center={self.center} | Axes=({self.major:.2f}, {self.minor:.2f})")
        
        # --- B. TEMPORAL SYNC (Phase Locking) ---
        # We need to know what angle the particle is at for every frame.
        
        phases = []
        for i in range(len(raw_m)):
            # 1. Translate to local
            dx = raw_m[i] - self.center[0]
            dy = raw_l[i] - self.center[1]
            
            # 2. Rotate back to axis-aligned
            # x_prime = x cos(-theta) - y sin(-theta)
            # y_prime = x sin(-theta) + y cos(-theta)
            neg_theta = -self.angle
            x_aligned = dx * np.cos(neg_theta) - dy * np.sin(neg_theta)
            y_aligned = dx * np.sin(neg_theta) + dy * np.cos(neg_theta)
            
            # 3. Normalize by axes (transform ellipse to unit circle)
            x_norm = x_aligned / self.major
            y_norm = y_aligned / self.minor
            
            # 4. Get angle
            phi = np.arctan2(y_norm, x_norm)
            phases.append(phi)
            
        # Unwrap phases (handle the jump from pi to -pi)
        phases_unwrapped = np.unwrap(phases)
        
        # Create a smooth function: Frame -> Angle
        # We allow extrapolation to complete the ellipse if data is partial
        self.phase_interpolator = interp1d(
            valid_frames, 
            phases_unwrapped, 
            kind='linear', 
            fill_value='extrapolate'
        )
        print("  > Temporal Phase-Locking Complete.")

    def get_camera_pos(self, frame_idx):
        # 1. Get the synchronized phase angle for this frame
        theta = self.phase_interpolator(frame_idx)
        
        # 2. Calculate point on ellipse
        # Unrotated
        x_local = self.major * np.cos(theta)
        y_local = self.minor * np.sin(theta)
        
        # Rotated
        x_rot = x_local * np.cos(self.angle) - y_local * np.sin(self.angle)
        y_rot = x_local * np.sin(self.angle) + y_local * np.cos(self.angle)
        
        return self.center[0] + x_rot, self.center[1] + y_rot

# --- MATH MODULE: ASYMPTOTIC ZOOM ---

def get_zoom_level(frame, total_frames, start, asymptote):
    # s = ((w_N - w_inf) / (w_0 - w_inf)) ^ (1/N)
    target_end = asymptote + 0.1 # End slightly above asymptote
    
    num = target_end - asymptote
    den = start - asymptote
    s = np.power(num / den, 1.0 / total_frames)
    
    w = asymptote + (start - asymptote) * (s ** frame)
    return w

# --- MAIN EXECUTION ---

def run_phaselock_mission():
    frames_buffer = []
    
    # --- PHASE 1: SURVEY (Collect Data) ---
    print("--- PHASE 1: SURVEYING TRAJECTORY ---")
    valid_frames = []
    raw_m = []
    raw_l = []
    
    curr_m, curr_l = 0.0, -2.5 # Initial guess
    survey_width = ZOOM_ASYMPTOTE * 8.0 # Look fairly wide to find the track
    
    # Survey for 60% of the total animation time to get a good arc
    survey_duration = int(TOTAL_FRAMES * 0.6) 
    
    for f in range(survey_duration):
        sys_theta = 2 * np.pi * (f / 100)
        curr_src_m, curr_src_l = rotate_coords(SRC_M_BASE, SRC_L_BASE, sys_theta)
        pulse = 1.0 + 0.1 * np.sin(f * 0.1)
        
        radar = render_microscope(curr_m, curr_l, survey_width, RADAR_RES, curr_src_m, curr_src_l, pulse)
        
        if np.max(radar) > 0.02: # If we see a signal
            idx = np.unravel_index(np.argmax(radar), radar.shape)
            scale = survey_width / RADAR_RES
            offset_m = (idx[1] - RADAR_RES/2) * scale
            offset_l = (RADAR_RES/2 - idx[0]) * scale
            
            found_m = curr_m + offset_m
            found_l = curr_l + offset_l
            
            # Record
            valid_frames.append(f)
            raw_m.append(found_m)
            raw_l.append(found_l)
            
            # Update tracker
            curr_m, curr_l = found_m, found_l
    
    # --- PHASE 2: SYNC (The Math) ---
    print("--- PHASE 2: CALCULATING PHASE MAP ---")
    orbiter = OrbitSynchronizer()
    orbiter.fit_and_sync(valid_frames, raw_m, raw_l)
    
    # --- PHASE 3: RENDER (The Output) ---
    print("--- PHASE 3: RENDERING SYNCHRONIZED DIVE ---")
    
    for f in range(TOTAL_FRAMES):
        # 1. Physics Time
        sys_theta = 2 * np.pi * (f / 100)
        curr_src_m, curr_src_l = rotate_coords(SRC_M_BASE, SRC_L_BASE, sys_theta)
        pulse = 1.0 + 0.1 * np.sin(f * 0.1)
        
        # 2. Get Camera Position (Phase Locked)
        cam_m, cam_l = orbiter.get_camera_pos(f)
        
        # 3. Get Zoom Level
        w = get_zoom_level(f, TOTAL_FRAMES, ZOOM_START, ZOOM_ASYMPTOTE)
        
        # 4. Render
        raw = render_microscope(cam_m, cam_l, w, RENDER_RES, curr_src_m, curr_src_l, pulse)
        
        # Post-Process
        norm = (raw - raw.min()) / (raw.max() - raw.min() + 1e-9)
        norm = np.power(norm, 0.5)
        img = (plt.get_cmap('magma')(norm)[:, :, :3] * 255).astype(np.uint8)
        img = np.flipud(img)
        pil_img = Image.fromarray(img)
        
        # HUD
        draw = ImageDraw.Draw(pil_img)
        draw.text((10, 10), f"MODE: PHASE LOCKED", fill="cyan")
        draw.text((10, 25), f"ZOOM: {w:.4f}", fill="yellow")
        
        # Crosshair to prove we are locked
        cx, cy = RENDER_RES // 2, RENDER_RES // 2
        draw.line((cx-5, cy, cx+5, cy), fill="cyan")
        draw.line((cx, cy-5, cx, cy+5), fill="cyan")
        
        frames_buffer.append(pil_img)
        
        if f % 10 == 0:
            print(f"Frame {f}/{TOTAL_FRAMES} | Zoom: {w:.2f}")

    frames_buffer[0].save(OUTPUT_FILENAME, save_all=True, append_images=frames_buffer[1:], duration=50, loop=0)
    print("✅ DONE.")

if __name__ == "__main__":
    run_phaselock_mission()