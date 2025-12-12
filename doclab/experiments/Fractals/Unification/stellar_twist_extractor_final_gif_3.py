import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from astropy.coordinates import SkyCoord
import astropy.units as u
from PIL import Image
import os

# Try to import astroquery
try:
    from astroquery.gaia import Gaia
    GAIA_AVAILABLE = True
except ImportError:
    GAIA_AVAILABLE = False
    print(" [!] WARNING: 'astroquery' library not found.")

# ======================
# CONFIGURATION
# ======================
TARGET_L = 204.1 
TARGET_B = -63.9
SEARCH_RADIUS = 5.0   # Tighter radius to see the core interaction
LIMIT = 1000          # Number of stars
TIME_RANGE_YEARS = 200000 # +/- Years to simulate
STEPS = 60            # Frames in animation

def get_gaia_data():
    if not GAIA_AVAILABLE: return None
    print(f"[*] Querying Gaia DR3 for {LIMIT} stars around l={TARGET_L}, b={TARGET_B}...")
    
    # Center coords
    c_center = SkyCoord(l=TARGET_L*u.deg, b=TARGET_B*u.deg, frame='galactic')
    c_icrs = c_center.icrs
    
    query = f"""
    SELECT TOP {LIMIT}
        ra, dec, parallax, pmra, pmdec, radial_velocity, phot_g_mean_mag
    FROM gaiadr3.gaia_source
    WHERE 
        1=CONTAINS(
            POINT('ICRS', ra, dec), 
            CIRCLE('ICRS', {c_icrs.ra.deg}, {c_icrs.dec.deg}, {SEARCH_RADIUS}) 
        )
        AND parallax > 1.0
        AND pmra IS NOT NULL
    """
    job = Gaia.launch_job(query)
    return job.get_results()

def propagate_stars(stars):
    print("[*] Calculating Trajectories (Past & Future)...")
    
    # Helper to safely extract values
    def get_val(col):
        if hasattr(col, 'unit') and col.unit is not None:
            return col.value
        return col

    # Extract raw values
    ra = get_val(stars['ra'])
    dec = get_val(stars['dec'])
    pmra = get_val(stars['pmra'])
    pmdec = get_val(stars['pmdec'])
    plx = get_val(stars['parallax'])
    rv = get_val(stars['radial_velocity'])
    
    # Handle NaNs
    rv = np.nan_to_num(rv, nan=0.0)
    # Avoid div by zero for distance (though query restricts plx > 1.0)
    dist_pc = 1000.0 / plx
    
    # Create Full 6D SkyCoord (Position + Velocity)
    # This is required for Astropy to transform velocities to Galactic frame
    c = SkyCoord(ra=ra*u.deg, 
                 dec=dec*u.deg, 
                 distance=dist_pc*u.pc,
                 pm_ra_cosdec=pmra*u.mas/u.yr, 
                 pm_dec=pmdec*u.mas/u.yr,
                 radial_velocity=rv*u.km/u.s,
                 frame='icrs')
    
    # Transform to Galactic
    g = c.galactic
    l0 = g.l.deg
    b0 = g.b.deg
    
    # Extract Galactic Proper Motions
    # pm_l_cosb is the proper motion in longitude (corrected for latitude)
    pm_l = g.pm_l_cosb.value / 3600000.0 # Convert mas/yr -> deg/yr
    pm_b = g.pm_b.value / 3600000.0      # Convert mas/yr -> deg/yr
    
    # Calculate positions for all frames
    # From -TIME to +TIME
    times = np.linspace(-TIME_RANGE_YEARS, TIME_RANGE_YEARS, STEPS)
    
    # Storage: [Frame, Star]
    trajectories_l = np.zeros((STEPS, len(stars)))
    trajectories_b = np.zeros((STEPS, len(stars)))
    
    for t_idx, t in enumerate(times):
        # Linear motion: pos = pos0 + velocity * time
        # This linear approximation works well for the "visual flow" over 200k years locally
        trajectories_l[t_idx] = l0 + (pm_l * t)
        trajectories_b[t_idx] = b0 + (pm_b * t)
        
    return trajectories_l, trajectories_b, times, get_val(stars['phot_g_mean_mag'])

def main():
    data = get_gaia_data()
    if data is None: return
    
    l_trace, b_trace, times, mags = propagate_stars(data)
    
    # Normalize Mags for size
    sizes = (20 - np.nan_to_num(mags, nan=15)) * 2
    sizes[sizes < 0.5] = 0.5
    
    print(f"[*] Rendering {STEPS} frames...")
    frames = []
    
    # Pre-calculate bounds
    xlims = (TARGET_L + SEARCH_RADIUS, TARGET_L - SEARCH_RADIUS) # Invert L
    ylims = (TARGET_B - SEARCH_RADIUS, TARGET_B + SEARCH_RADIUS)
    
    for i in range(STEPS):
        if i % 10 == 0: print(f"    Frame {i}/{STEPS}...")
        
        fig = plt.figure(figsize=(10, 10), facecolor='black')
        ax = fig.add_subplot(111)
        ax.set_facecolor('black')
        
        # Current Positions
        curr_l = l_trace[i]
        curr_b = b_trace[i]
        
        # 1. Draw Trails (Dynamic)
        # Draw tail from (i-10) to i
        tail_len = 15
        if i > 0:
            start = max(0, i - tail_len)
            
            # Vectorized plotting for speed is tricky with varying colors per segment
            # We loop over stars but plot segments
            # Optimization: Plot all previous positions as one faint scatter or LineCollection
            # Simple approach: Plot lines for significant movers
            
            # Filter distinct lines to keep plot fast/clean
            for s in range(len(curr_l)):
                # Only draw if visible in frame
                if (curr_l[s] < max(xlims) + 1 and curr_l[s] > min(xlims) - 1):
                    # Color Logic: Magenta = Past (<0), Cyan = Future (>0)
                    color = 'magenta' if times[i] < 0 else 'cyan'
                    
                    ax.plot(l_trace[start:i+1, s], b_trace[start:i+1, s], 
                            color=color, alpha=0.6, lw=1.0)

        # 2. Draw Stars (Heads)
        ax.scatter(curr_l, curr_b, s=sizes, c='white', edgecolors='none', alpha=0.9, zorder=10)
        
        # 3. Draw The Maw (Fixed Anchor)
        maw = plt.Circle((TARGET_L, TARGET_B), 1.0, color='lime', alpha=0.2)
        ax.add_patch(maw)
        ax.scatter(TARGET_L, TARGET_B, marker='+', s=100, color='lime', zorder=20)
        
        # Formatting
        ax.set_xlim(xlims)
        ax.set_ylim(ylims)
        
        year_val = times[i]
        year_label = f"T = {year_val/1000:.1f}k Years"
        
        if year_val < -1000: color = 'magenta' 
        elif year_val > 1000: color = 'cyan'
        else: color = 'white'
            
        ax.text(TARGET_L, TARGET_B + SEARCH_RADIUS - 1, year_label, 
                color=color, fontsize=16, fontweight='bold', ha='center')
        
        ax.text(TARGET_L, TARGET_B - SEARCH_RADIUS + 0.5, "GAIA DR3 KINEMATICS", 
                color='gray', fontsize=10, ha='center')
        
        ax.set_xlabel("Galactic Longitude", color='gray')
        ax.set_ylabel("Galactic Latitude", color='gray')
        ax.grid(True, color='#222222', linestyle=':')
        
        # Save frame
        fname = f"temp_traj_{i:03d}.png"
        plt.savefig(fname, dpi=80, facecolor='black')
        plt.close(fig)
        
        with Image.open(fname) as img:
            frames.append(img.copy())
        os.remove(fname)
        
    # Save GIF
    print("[*] Assembling GIF...")
    if frames:
        frames[0].save('gaia_trajectory_history.gif', save_all=True, append_images=frames[1:], duration=100, loop=0)
        print("✅ GIF Saved: gaia_trajectory_history.gif")

if __name__ == "__main__":
    main()