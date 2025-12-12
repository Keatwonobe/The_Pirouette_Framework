# synthetic_traveler_test.py
import numpy as np
import matplotlib.pyplot as plt
from helical_scanner_5 import (
    get_ylm, build_mode_maps, synthesize_helical, 
    N_TH_SYN, N_PH_SYN, REMOVE_BAND, LMAX
)

def generate_needle_universe(lmax):
    """
    Creates Alms for a universe with a single 'Traveler' needle.
    Replaces load_cmb_and_alms for the synthetic test.
    """
    # 1. Define High-Res Integration Grid
    n_theta = lmax * 4
    n_phi   = lmax * 8
    theta   = np.linspace(0, np.pi, n_theta)
    phi     = np.linspace(-np.pi, np.pi, n_phi, endpoint=False)
    TH, PH  = np.meshgrid(theta, phi, indexing="ij")
    
    # 2. Build Map: Noise + Needle
    print("    Generating map with injected needle...")
    # Background Noise
    map_data = np.random.randn(*TH.shape) * 0.2
    
    # Needle: A gaussian ridge satisfying phi = 2*theta - pi (Diagonal)
    # Distance approximation
    dist = np.abs(2*TH - PH - np.pi) / np.sqrt(5)
    width = np.deg2rad(4.0)
    needle = np.exp(-0.5 * (dist/width)**2) * 5.0  # High amplitude
    
    map_data += needle
    
    # 3. Compute Alms via Quadrature
    dtheta = theta[1] - theta[0]
    dphi   = phi[1]   - phi[0]
    weights = np.sin(TH) * dtheta * dphi
    
    alms = {}
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            Y = get_ylm(m, l, PH, TH)
            val = np.sum(map_data * np.conjugate(Y) * weights)
            alms[(l, m)] = val
            
    return alms

def main():
    print("=== SYNTHETIC TRAVELER TEST (Upgrade C) ===")
    
    # 1. Generate Synthetic Alms
    alms = generate_needle_universe(LMAX)
    
    # 2. Build Mode Maps (apply same band removal as real data)
    print("    Building helical mode maps...")
    modes, TH, PH = build_mode_maps(alms, LMAX, remove_band=REMOVE_BAND)
    
    # 3. Scan K to find the "Focusing" point
    # If the hypothesis holds, the needle should re-appear sharply at a specific k
    k_scan = np.linspace(-1.0, 3.0, 50)
    max_intensity = []
    
    print(f"    Scanning {len(k_scan)} twist values...")
    for k in k_scan:
        T_k = synthesize_helical(modes, PH, k_twist=k)
        max_intensity.append(np.max(np.abs(T_k)))
        
    # 4. Plot Results
    plt.figure(figsize=(8, 4))
    plt.plot(k_scan, max_intensity, 'r-o', lw=1)
    plt.title("Synthetic Needle: Peak Intensity vs Twist")
    plt.xlabel("Twist (k)")
    plt.ylabel("Max Field Intensity")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("synthetic_traveler_result.png")
    print("✅ Test complete. Saved 'synthetic_traveler_result.png'")
    print("    Look for a sharp peak in the plot. If it exists, the math confirms")
    print("    that a diagonal needle looks like a helical resonance.")

if __name__ == "__main__":
    main()