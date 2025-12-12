import numpy as np
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
import astropy.units as u

# ======================
# CONFIGURATION
# ======================
N_STARS = 5000           # Number of stars to map
W_RESONANCE = 1.0047     # Your "Squaring the Circle" Resonance Factor
HELIX_TURNS = 50         # How tight the coil is for the scan
RESOLUTION = 2000        # Pixel resolution for the "Hubble" look

# ======================
# 1. GENERATE (OR LOAD) STAR CATALOG
# ======================
def get_star_catalog(n_stars):
    """
    Simulates a realistic star field (Galactic Disk + Isotropic Halo).
    In a real app, we would load the Hipparcos or Gaia catalog here.
    """
    print(f"[*] Generating catalog of {n_stars} stars...")
    
    # 1. The Galactic Disk (Concentrated at b=0)
    n_disk = int(n_stars * 0.7)
    l_disk = np.random.uniform(0, 360, n_disk)
    # Gaussian distribution around galactic equator
    b_disk = np.random.normal(0, 5, n_disk) 
    
    # 2. The Isotropic Background (Random sphere)
    n_halo = n_stars - n_disk
    l_halo = np.random.uniform(0, 360, n_halo)
    # Inverse sine for uniform sphere distribution
    v = np.random.uniform(-1, 1, n_halo)
    b_halo = np.rad2deg(np.arcsin(v))
    
    # Combine
    l = np.concatenate([l_disk, l_halo])
    b = np.concatenate([b_disk, b_halo])
    
    # Magnitudes (Brightness) - Power law distribution
    mags = np.random.pareto(1.5, n_stars) + 1
    mags = 10 / mags # Invert so bigger number = brighter for plotting size
    
    return l, b, mags

# ======================
# 2. THE HELICAL TRANSFORM
# ======================
def spherical_to_helical_index(l, b, w, turns):
    """
    Maps (l, b) coordinates to Helical Index (t, phase).
    This is the core of your "Indexing" theory.
    """
    # Convert to Radians
    phi = np.deg2rad(l)
    theta = np.deg2rad(90 - b) # 0 at North Pole
    
    # Standard z projection (-1 to 1)
    z = np.cos(theta)
    
    # Helical Phase Mapping
    # We unwrap the sphere into a long helical strip
    # t_index represents "how far along the wire" the star is
    
    # The "Ideal" helix satisfies: phi = w * t
    # We want to find the closest point on the helix to the star
    
    # Normalized height index (0 to 1)
    h_idx = (z + 1) / 2.0
    
    # Helical Phase Offset
    # How far is the star "off" the perfect resonant line?
    ideal_phi = (h_idx * turns * 2 * np.pi * w) % (2 * np.pi)
    phase_error = np.abs(phi - ideal_phi)
    phase_error = np.minimum(phase_error, 2*np.pi - phase_error)
    
    return h_idx, phase_error

# ======================
# 3. MAIN
# ======================
def main():
    l, b, brightness = get_star_catalog(N_STARS)
    
    print("[*] Indexing Stars via Helical Math...")
    # We map stars not by (x,y), but by (Height, Resonance Error)
    h_index, phase_error = spherical_to_helical_index(l, b, W_RESONANCE, HELIX_TURNS)
    
    # ======================
    # VISUALIZATION 1: The Helical Unwrapping
    # ======================
    plt.figure(figsize=(12, 10), facecolor='black')
    ax = plt.gca()
    ax.set_facecolor('black')
    
    # Plot stars
    # X-axis: The Helical "Time" (Height z)
    # Y-axis: The "Resonance Error" (How far off the wire)
    # This effectively "scans" the sky into a 2D strip
    
    plt.scatter(h_index, b, s=brightness*2, c='white', alpha=0.8, edgecolors='none')
    
    # Add a "Scan Line" visual
    # If the theory is right, stars should cluster? 
    # Or this just gives us a unique sorting algorithm.
    
    plt.title(f"The Helical Index: {N_STARS} Stars Sorted by Phase\n(W={W_RESONANCE}, Turns={HELIX_TURNS})", color='white')
    plt.xlabel("Helical Height Index (z)", color='gray')
    plt.ylabel("Galactic Latitude (b)", color='gray')
    
    # Stylize for "Hubble" look
    ax.tick_params(colors='gray')
    plt.grid(True, color='#222222', linestyle='--')
    
    plt.savefig("helical_star_index.png", dpi=300, bbox_inches='tight')
    print("✅ Index saved to helical_star_index.png")

    # ======================
    # VISUALIZATION 2: The Point Scan Starfield (The "Blush" Map)
    # ======================
    # Let's project this back onto a flat map but keep the "Scan" aesthetic
    plt.figure(figsize=(15, 8), facecolor='black')
    ax = plt.subplot(111, projection="aitoff")
    ax.set_facecolor('black')
    
    # Convert degrees to radians for Aitoff
    l_rad = np.deg2rad(l - 180)
    b_rad = np.deg2rad(b)
    
    # Color stars by their "Helical Resonance" (Phase Error)
    # Blue = Perfectly on the Helix
    # Red = Far from the Helix
    
    sc = plt.scatter(l_rad, b_rad, s=brightness, c=phase_error, cmap='twilight', alpha=0.9)
    
    plt.title("The Helical Starfield Scan", color='white', y=1.05)
    plt.grid(True, color='#333333')
    ax.tick_params(colors='gray')
    
    # Create a custom colorbar that looks sci-fi
    cbar = plt.colorbar(sc, orientation='horizontal', pad=0.05, aspect=50)
    cbar.set_label("Helical Phase Drift", color='gray')
    cbar.ax.xaxis.set_tick_params(color='gray')
    plt.setp(plt.getp(cbar.ax.axes, 'xticklabels'), color='gray')
    
    plt.savefig("helical_starfield_scan.png", dpi=300, bbox_inches='tight')
    print("✅ Starfield saved to helical_starfield_scan.png")

if __name__ == "__main__":
    main()