import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LightSource, Normalize
import io
from PIL import Image

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------
RES = 150            # Reduced from 400 for GIF generation speed
RANGE = 1800.0
DT = 0.015
GAMMA = 0.02         # Low friction = lots of ripples
TWIST = 2.83814      # The "Ripple" Twist

# --- NEW CONFIGURATION ---
STEPS_PER_DIRECTION = 120 # 60 steps backward, 60 steps forward
TOTAL_STEPS = STEPS_PER_DIRECTION * 2 # Total physics steps to simulate
FRAMES = 30 # Total frames in the GIF
STEPS_PER_FRAME = TOTAL_STEPS // FRAMES # 120 steps / 30 frames = 4 steps/frame
# -------------------------


def get_force_vectorized(m, lam):
    # Vectorized Physics Engine (Numpy version)
    
    # 1. Teal (EM)
    F_teal_m = -(m + 0.866) 
    F_teal_lam = -(lam - 0.5)

    # 2. Red (Weak)
    F_red_m = -m
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
    
    # State Variables (Initial State for all simulations)
    m = X.copy()
    lam = Y.copy()
    pm = np.zeros_like(m)
    plam = np.zeros_like(lam)
    
    # State storage for rendering
    # We store 121 states: 60 backward, initial state (at index 60), 60 forward
    m_states = [None] * (TOTAL_STEPS + 1)
    lam_states = [None] * (TOTAL_STEPS + 1)
    total_ang_states = [None] * (TOTAL_STEPS + 1)

    # --------------------------------------------------
    # 1. Simulate Backward from the initial state
    # --------------------------------------------------
    print(f"Simulating {STEPS_PER_DIRECTION} steps backward...")
    # The 'initial' state is stored at the midpoint (index STEPS_PER_DIRECTION)
    m_states[STEPS_PER_DIRECTION] = m.copy()
    lam_states[STEPS_PER_DIRECTION] = lam.copy()
    total_ang = np.zeros_like(m)
    total_ang_states[STEPS_PER_DIRECTION] = total_ang.copy()
    prev_ang = np.arctan2(lam, m)

    # Note: We use -DT to reverse the direction of integration (time-reversal)
    for step in range(STEPS_PER_DIRECTION - 1, -1, -1):
        Fm, Flam, w_red = get_force_vectorized(m, lam)
        # Time-reversal of the semi-implicit Euler (Symplectic Integrator)
        drag_inv = 1.0 / (1.0 + 0.5 * (-DT) * GAMMA * w_red) # -DT in drag
        pm = (pm + 0.5 * (-DT) * Fm) * drag_inv
        plam = (plam + 0.5 * (-DT) * Flam) * drag_inv
        m += (-DT) * pm
        lam += (-DT) * plam
        
        # Winding Math (same direction for winding calculation, just reversed coordinates)
        curr_ang = np.arctan2(lam, m)
        delta = curr_ang - prev_ang
        delta = np.where(delta > np.pi, delta - 2*np.pi, delta)
        delta = np.where(delta < -np.pi, delta + 2*np.pi, delta)
        total_ang += delta
        prev_ang = curr_ang

        m_states[step] = m.copy()
        lam_states[step] = lam.copy()
        total_ang_states[step] = total_ang.copy()

        if (STEPS_PER_DIRECTION - step) % 10 == 0:
            print(f"Processed backward step {STEPS_PER_DIRECTION - step}/{STEPS_PER_DIRECTION}")


    # --------------------------------------------------
    # 2. Simulate Forward from the initial state (m_start, lam_start)
    # --------------------------------------------------
    print(f"\nSimulating {STEPS_PER_DIRECTION} steps forward...")
    
    # Reset to initial state for forward pass
    m = m_states[STEPS_PER_DIRECTION].copy()
    lam = lam_states[STEPS_PER_DIRECTION].copy()
    pm = np.zeros_like(m)
    plam = np.zeros_like(lam)
    total_ang = np.zeros_like(m)
    prev_ang = np.arctan2(lam, m)

    # Track start for displacement calculation
    m_start = m.copy()
    lam_start = lam.copy()

    # Note: DT is positive for forward simulation
    for step in range(STEPS_PER_DIRECTION + 1, TOTAL_STEPS + 1):
        Fm, Flam, w_red = get_force_vectorized(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag
        m += DT * pm
        lam += DT * plam
        
        # Winding Math
        curr_ang = np.arctan2(lam, m)
        delta = curr_ang - prev_ang
        delta = np.where(delta > np.pi, delta - 2*np.pi, delta)
        delta = np.where(delta < -np.pi, delta + 2*np.pi, delta)
        total_ang += delta
        prev_ang = curr_ang

        m_states[step] = m.copy()
        lam_states[step] = lam.copy()
        total_ang_states[step] = total_ang.copy()

        if (step - STEPS_PER_DIRECTION) % 10 == 0:
            print(f"Processed forward step {step - STEPS_PER_DIRECTION}/{STEPS_PER_DIRECTION}")


    # --------------------------------------------------
    # 3. Render Frames from Stored States
    # --------------------------------------------------
    print(f"\nRendering {FRAMES} frames...")
    
    fig = plt.figure(figsize=(8, 8), facecolor='black')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('black')
    
    # Lighting
    ls = LightSource(azdeg=315, altdeg=45)
    
    frames_buffer = []
    
    # Iterate through the 121 states to select the 30 frames
    for frame in range(FRAMES):
        # Index in the stored states
        # The first frame corresponds to the earliest state (index 0)
        idx = frame * STEPS_PER_FRAME
        
        m_frame = m_states[idx]
        lam_frame = lam_states[idx]
        total_ang_frame = total_ang_states[idx]

        # --- Render Frame ---
        ax.clear()
        ax.axis('off')
        ax.grid(False)
        ax.set_facecolor('black')
        
        # 1. Height (Log Displacement)
        # Always relative to the true initial state (index STEPS_PER_DIRECTION)
        dist = np.sqrt((m_frame - m_start)**2 + (lam_frame - lam_start)**2)
        Z = np.log1p(dist)
        
        # 2. Color (Winding Number)
        # Normalize winding
        winding = np.abs(total_ang_frame) / (2*np.pi)
        
        # Normalize winding for colormap (e.g., 0 to 4 spins)
        norm = Normalize(vmin=0, vmax=4)
        colors = cm.nipy_spectral(norm(winding))
        
        # Apply lighting to the colors
        rgb = ls.shade_rgb(colors, Z, vert_exag=0.1, blend_mode='soft')
        
        # Plot
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1, facecolors=rgb,
                               linewidth=0, antialiased=False, shade=False)
        
        # View
        ax.view_init(elev=55, azim=-45)
        
        # Step label calculation: 
        # -60 (start) to +60 (end)
        display_step = idx - STEPS_PER_DIRECTION
        
        ax.set_title(f"Ridges forming: Step {display_step}", color='white')
        
        # Capture
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=80)
        buf.seek(0)
        img = Image.open(buf)
        frames_buffer.append(img)
        
        print(f"Rendered frame {frame+1}/{FRAMES} (State Index: {idx}, Display Step: {display_step})")

    # Save GIF
    print("\nSaving GIF...")
    frames_buffer[0].save('pirouette_ridges_forming_bidirectional.gif',
                          save_all=True,
                          append_images=frames_buffer[1:],
                          optimize=True,
                          duration=100, # ms per frame
                          loop=0)
    print("Done. File saved as pirouette_ridges_forming_bidirectional.gif")

if __name__ == "__main__":
    generate_gif()