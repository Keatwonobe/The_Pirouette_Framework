# analyze_traveler_candidates.py
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import map_coordinates
from fractal_fingerprint2D import fractal_fingerprint
import os

# CONFIG
DATACUBE = "substrate_helical_datacube.npz"
CANDIDATE_K = [-0.492, 0.517]  # From your match scan
PATH_AMPLITUDE = 20.0          # Amplitude of sine wave path in degrees

def get_path_coordinates(n_points=100, amplitude=20.0, phase_shift=0.0):
    """
    Defines a 'Traveler' path: a great-circle-ish sine wave on the map.
    Adjust phase_shift to align with the feature you see in the map.
    """
    lon = np.linspace(-180, 180, n_points)
    # Simple traveler model: Sinusoidal path across the sky
    lat = amplitude * np.sin(np.deg2rad(lon + phase_shift))
    return lon, lat

def extract_patch(field, lon0, lat0, patch_deg=15):
    """Extracts a local square patch centered on (lon0, lat0)."""
    ny, nx = field.shape
    # Map (lon, lat) to (x, y) indices
    # lon: -180..180 -> 0..nx
    # lat: -90..90   -> 0..ny
    
    x0 = (lon0 + 180) * (nx / 360)
    y0 = (90 - lat0) * (ny / 180)
    
    # Define patch bounds in pixels
    r_px = int(patch_deg * (nx / 360))
    
    # We use map_coordinates for safe sub-pixel extraction / wrapping
    y_grid, x_grid = np.mgrid[-r_px:r_px, -r_px:r_px]
    
    # Shift grid to center
    x_sample = (x_grid + x0) % nx  # Wrap longitude
    y_sample = np.clip(y_grid + y0, 0, ny-1) # Clamp latitude
    
    patch = map_coordinates(field, [y_sample, x_sample], order=1, mode='wrap')
    return patch

def main():
    if not os.path.exists(DATACUBE):
        print(f"[!] Error: {DATACUBE} not found.")
        return

    print(f"[*] Loading {DATACUBE}...")
    data = np.load(DATACUBE)
    cube = data["T_sub"]
    k_vals = data["k_values"]

    for k_target in CANDIDATE_K:
        # 1. Find and Extract Slice
        idx = np.argmin(np.abs(k_vals - k_target))
        actual_k = k_vals[idx]
        field = cube[idx]
        
        print(f"\n=== Analyzing Candidate k = {actual_k:.3f} ===")

        # 2. Visualize the Slice (Upgrade A)
        plt.figure(figsize=(10, 5))
        plt.imshow(field, origin="lower", extent=[-180, 180, -90, 90], cmap="magma", aspect="auto")
        
        # Overlay the hypothesis path
        path_lon, path_lat = get_path_coordinates(amplitude=PATH_AMPLITUDE)
        plt.plot(path_lon, path_lat, 'w--', alpha=0.5, label="Traveler Path Hypothesis")
        
        plt.colorbar(label="Substrate Temperature")
        plt.title(f"Substrate Slice @ k={actual_k:.3f}")
        plt.legend()
        plt.tight_layout()
        outfile = f"analysis_slice_k{actual_k:.3f}.png"
        plt.savefig(outfile)
        print(f"    Saved visual inspection to {outfile}")
        plt.close()

        # 3. Sliding Window Fingerprint (Upgrade B)
        print("    Running sliding-window fractal scan along path...")
        stats = []
        for l, b in zip(path_lon, path_lat):
            patch = extract_patch(field, l, b)
            if patch.std() < 1e-6:
                stats.append((np.nan, np.nan))
                continue
                
            fp = fractal_fingerprint(patch)
            stats.append((fp['box_dim'], fp['gradient_anisotropy']))
        
        # Unpack
        Ds, Anis = zip(*stats)
        
        # Plot Fingerprint Stability
        fig, ax1 = plt.subplots(figsize=(10, 4))
        
        ax1.set_xlabel('Longitude along Path (deg)')
        ax1.set_ylabel('Fractal Dimension (D)', color='tab:blue')
        ax1.plot(path_lon, Ds, color='tab:blue', lw=2)
        ax1.tick_params(axis='y', labelcolor='tab:blue')
        ax1.axhline(1.8, color='k', ls=':', alpha=0.3, label="Wada Target")

        ax2 = ax1.twinx() 
        ax2.set_ylabel('Anisotropy', color='tab:red')
        ax2.plot(path_lon, Anis, color='tab:red', lw=2, ls='--')
        ax2.tick_params(axis='y', labelcolor='tab:red')
        
        plt.title(f"Fractal Consistency along Path (k={actual_k:.3f})")
        plt.tight_layout()
        plt.savefig(f"analysis_path_metrics_k{actual_k:.3f}.png")
        print(f"    Saved path metrics to analysis_path_metrics_k{actual_k:.3f}.png")

if __name__ == "__main__":
    main()