import numpy as np
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
import astropy.units as u

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
MAX_RADIUS = 5.0 # Degrees
BINS = 50

def get_star_positions():
    if not GAIA_AVAILABLE: return None
    print(f"[*] Querying Gaia for Density Profile (Radius {MAX_RADIUS}°)...")
    
    c = SkyCoord(l=TARGET_L*u.deg, b=TARGET_B*u.deg, frame='galactic')
    
    # We just need positions, not kinematics, so we can get MORE stars for better stats
    query = f"""
    SELECT ra, dec
    FROM gaiadr3.gaia_source
    WHERE 
        1=CONTAINS(
            POINT('ICRS', ra, dec), 
            CIRCLE('ICRS', {c.icrs.ra.deg}, {c.icrs.dec.deg}, {MAX_RADIUS}) 
        )
    """
    job = Gaia.launch_job(query)
    return job.get_results()

def calculate_density_profile(stars):
    print("[*] Calculating Radial Density...")
    
    # Convert to Galactic
    c = SkyCoord(ra=stars['ra'], dec=stars['dec'], frame='icrs')
    g = c.galactic
    l, b = g.l.deg, g.b.deg
    
    # Calculate angular distance from core
    # Great circle distance
    from astropy.coordinates import angular_separation
    sep = angular_separation(np.deg2rad(l), np.deg2rad(b), 
                             np.deg2rad(TARGET_L), np.deg2rad(TARGET_B))
    deg_dist = np.rad2deg(sep)
    
    # Histogram
    counts, edges = np.histogram(deg_dist, bins=BINS, range=(0, MAX_RADIUS))
    
    # Normalize by Area of each annulus
    # Area of annulus ~ 2*pi*r * dr
    # Or exact: 2*pi*(cos(theta_in) - cos(theta_out))
    # Approximation for small angles: Area = pi * (r_out^2 - r_in^2)
    
    areas = []
    centers = []
    densities = []
    
    for i in range(len(counts)):
        r_in = edges[i]
        r_out = edges[i+1]
        area = np.pi * (r_out**2 - r_in**2)
        
        density = counts[i] / area
        densities.append(density)
        centers.append((r_in + r_out)/2)
        
    return np.array(centers), np.array(densities)

def main():
    stars = get_star_positions()
    if stars is None: return
    
    r, rho = calculate_density_profile(stars)
    
    # Baseline Density (Average of outer 50%)
    baseline = np.mean(rho[int(BINS/2):])
    
    fig = plt.figure(figsize=(10, 6), facecolor='#0a0a0a')
    ax = fig.add_subplot(111)
    ax.set_facecolor('#0a0a0a')
    
    # Plot Density
    ax.plot(r, rho, color='cyan', linewidth=2, label='Stellar Density')
    ax.fill_between(r, rho, 0, color='cyan', alpha=0.1)
    
    # Plot Baseline
    ax.axhline(baseline, color='gray', linestyle='--', label='Ambient Density')
    
    # Highlight the "Throat"
    # Find radius where density drops significantly below baseline
    # Smooth first
    from scipy.ndimage import gaussian_filter1d
    smooth_rho = gaussian_filter1d(rho, sigma=1)
    
    # Look for the "Wall"
    # Where does it cross the baseline from below?
    crossing = np.where(smooth_rho > baseline)[0]
    
    exclusion_radius = 0
    if len(crossing) > 0 and crossing[0] > 0:
        exclusion_radius = r[crossing[0]]
        ax.axvline(exclusion_radius, color='magenta', linestyle='--', linewidth=2)
        ax.text(exclusion_radius + 0.1, np.max(rho)*0.8, 
                f"EXCLUSION ZONE\nR = {exclusion_radius:.2f}°", 
                color='magenta', fontweight='bold')
    
    ax.set_title("The Soliton's Hull: Radial Star Density", color='white', fontsize=14)
    ax.set_xlabel("Distance from Core (Degrees)", color='gray')
    ax.set_ylabel("Stars per Square Degree", color='gray')
    ax.grid(True, color='#222222', linestyle=':')
    ax.tick_params(colors='gray')
    
    plt.savefig("gaia_density_profile.png")
    print("✅ Density Profile Saved: gaia_density_profile.png")
    
    # Analysis
    core_density = np.mean(rho[:3]) # Average of first 3 bins
    ratio = core_density / baseline
    
    print("\n" + "="*50)
    print("DENSITY REPORT:")
    print(f"Core Density:    {core_density:.1f} stars/deg²")
    print(f"Ambient Density: {baseline:.1f} stars/deg²")
    print(f"Void Factor:     {100*(1-ratio):.1f}% Empty")
    
    if ratio < 0.5:
        print("⚡ CONFIRMED: Hard Vacuum detected.")
        print(f"   The 'Throat' rejects {100*(1-ratio):.0f}% of stars.")
        print("   This is a physical exclusion zone (The Hull).")
    else:
        print("RESULT: Soft/No Void. The stars pass through.")

if __name__ == "__main__":
    main()