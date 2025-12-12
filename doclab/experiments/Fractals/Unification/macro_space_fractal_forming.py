import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LightSource, Normalize
import io
from PIL import Image

# --------------------------------------------------
# CONFIGURATION (Matching the Ripple Script)
# --------------------------------------------------
RES = 150            # Reduced from 400 for GIF generation speed
RANGE = 1800.0
DT = 0.015
GAMMA = 0.02         # Low friction = lots of ripples
TWIST = 2.83814      # The "Ripple" Twist
FRAMES = 30
STEPS_PER_FRAME = 20 # Total steps = 600 (approx similar to original 500)

def get_force_vectorized(m, lam):
    # Vectorized Physics Engine (Numpy version)
    
    # 1. Teal (EM)
    F_teal_m = -(m + 0.866) 
    F_teal_lam = -(lam - 0.5)

    # 2. Red (Weak)
    F_red_m = -m # Note: Ripple script used -m, Space Fractal used -(m-0.0). Same.
    p_violation = TWIST * np.sin(m * 2.5) 
    F_red_lam = -(lam + 1.0) + p_violation

    # 3. Gold (Strong)
    sum_m = (F_teal_m + F_red_m)
    sum_lam = (F_teal_lam + F_red_lam)
    mag_sq = sum_m**2 + sum_lam**2
    mag = np.sqrt(mag_sq)
    
    scale = np.sqrt(mag) # F^1.5 scaling
    F_gold_m = sum_m * scale
    F_gold_lam = sum_lam * scale
    
    # Weights
    # Calculate angle in degrees
    angle = np.degrees(np.arctan2(lam, m)) % 360
    
    def w_calc(a, t):
        d = np.abs(a - t)
        # Vectorized wrap-around 360 handling
        d = np.minimum(d, 360.0 - d)
        return np.exp(-(d/80.0)**2)
    
    w_gold = w_calc(angle, 30.0)
    w_teal = w_calc(angle, 150.0)
    w_red = w_calc(angle, 270.0)
    
    tot = w_gold + w_teal + w_red + 1e-6
    nw_red = w_red / tot
    nw_teal = w_teal / tot
    nw_gold = w_gold / tot
    
    Fm = (nw_teal * F_teal_m + nw_red * F_red_m + nw_gold * F_gold_m)
    Flam = (nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam)
    
    return Fm, Flam, nw_red

def generate_gif():
    print("Initializing Grid...")
    # Setup Grid
    x = np.linspace(-RANGE, RANGE, RES)
    y = np.linspace(-RANGE, RANGE, RES)
    X, Y = np.meshgrid(x, y)
    
    # State Variables
    m = X.copy()
    lam = Y.copy()
    pm = np.zeros_like(m)
    plam = np.zeros_like(lam)
    
    # Tracking
    m_start = m.copy()
    lam_start = lam.copy()
    
    # Winding Tracking
    prev_ang = np.arctan2(lam, m)
    total_ang = np.zeros_like(m)
    
    frames_buffer = []
    
    print(f"Rendering {FRAMES} frames...")
    
    fig = plt.figure(figsize=(8, 8), facecolor='black') # Smaller figure for speed
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('black')
    
    # Lighting
    ls = LightSource(azdeg=315, altdeg=45)
    
    for frame in range(FRAMES):
        # Physics Integration Loop
        for _ in range(STEPS_PER_FRAME):
            Fm, Flam, w_red = get_force_vectorized(m, lam)
            drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
            pm = (pm + 0.5 * DT * Fm) * drag
            plam = (plam + 0.5 * DT * Flam) * drag
            m += DT * pm
            lam += DT * plam
            
            # Winding Math
            curr_ang = np.arctan2(lam, m)
            delta = curr_ang - prev_ang
            # Unwrap
            delta = np.where(delta > np.pi, delta - 2*np.pi, delta)
            delta = np.where(delta < -np.pi, delta + 2*np.pi, delta)
            total_ang += delta
            prev_ang = curr_ang

        # --- Render Frame ---
        ax.clear()
        ax.axis('off')
        ax.grid(False)
        ax.set_facecolor('black')
        
        # 1. Height (Log Displacement)
        dist = np.sqrt((m - m_start)**2 + (lam - lam_start)**2)
        Z = np.log1p(dist)
        
        # 2. Color (Winding Number)
        # Normalize winding to something visible
        winding = np.abs(total_ang) / (2*np.pi)
        
        # We overlay the Space Fractal Colors onto the 3D surface
        # Using 'twilight' or 'hsv' to show phase, or 'inferno' mixed with phase?
        # Let's use the 'nipy_spectral' from the Space Fractal script for consistency
        # But applied to the 3D surface lighting
        
        # Normalize winding for colormap (e.g., 0 to 4 spins)
        norm = Normalize(vmin=0, vmax=4)
        colors = cm.nipy_spectral(norm(winding))
        
        # Apply lighting to the colors
        rgb = ls.shade_rgb(colors, Z, vert_exag=0.1, blend_mode='soft')
        
        # Plot
        surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, facecolors=rgb,
                               linewidth=0, antialiased=False, shade=False)
        
        # View
        ax.view_init(elev=55, azim=-45)
        ax.set_title(f"Ridges forming: Step {(frame+1)*STEPS_PER_FRAME}", color='white')
        
        # Capture
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=80)
        buf.seek(0)
        img = Image.open(buf)
        frames_buffer.append(img)
        
        if frame % 5 == 0:
            print(f"Processed frame {frame}/{FRAMES}")

    # Save GIF
    print("Saving GIF...")
    frames_buffer[0].save('pirouette_ridges_forming.gif',
                          save_all=True,
                          append_images=frames_buffer[1:],
                          optimize=True,
                          duration=100, # ms per frame
                          loop=0)
    print("Done.")

generate_gif()