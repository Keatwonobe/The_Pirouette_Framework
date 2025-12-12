import numpy as np
import matplotlib.pyplot as plt
from astropy_healpix import HEALPix
from astropy.coordinates import SkyCoord
import astropy.units as u

# ======================
# CONFIGURATION
# ======================
N_DOTS = 30000          # The "Army of Travelers"
K_TRAVELER = 0.9        # The "Traveler" Resonance
L_DOMINANT = 10         # The "Carrier Wave" (Skeleton) that moves them

def main():
    print(f"[*] Initializing {N_DOTS} Holographic Travelers...")
    
    # 1. Generate Random Antipodal Pairs
    # We create N/2 points, then add their antipodes
    n_pairs = N_DOTS // 2
    
    # Random distribution on sphere
    phi_1 = np.random.uniform(-np.pi, np.pi, n_pairs)
    # Inverse cosine for uniform sphere distribution
    theta_1 = np.arccos(np.random.uniform(-1, 1, n_pairs))
    
    # Calculate Antipodes (Opposite side of sphere)
    phi_2 = (phi_1 + np.pi) % (2*np.pi) - np.pi
    theta_2 = np.pi - theta_1
    
    # Combine
    phi_start = np.concatenate([phi_1, phi_2])
    theta_start = np.concatenate([theta_1, theta_2])
    
    print("[*] Applying 'Traveler' Twist (k=0.9)...")
    
    # 2. The Physics of the Transfer
    # The Twist isn't just a rotation; it's a PHASE SHEAR dependent on L.
    # Effective shift: d_phi = (k - 1) * phi
    # But strictly, this happens per harmonic. 
    # In real space, this manifests as a coordinate stretch.
    
    # We model the "Traveler" effect as a Longitudinal Shear
    # New Angle = Old Angle * k
    phi_end = (phi_start * K_TRAVELER)
    
    # Normalize back to [-pi, pi]
    phi_end = (phi_end + np.pi) % (2*np.pi) - np.pi
    
    # 3. Calculate "Drift" (Geodesic Distance)
    # Using Haversine formula approximation for speed
    # (Since theta doesn't change in this simple shear model, 
    # drift is purely longitudinal arc length)
    
    # Arc length = R * delta_phi * sin(theta)
    # We just want relative drift intensity
    drift = np.abs(phi_end - phi_start) * np.sin(theta_start)
    
    # 4. Visualization: The Holographic Plate
    print("[*] Developing Holographic Plate...")
    
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection="mollweide")
    
    # Plot the "End" positions, colored by how far they drifted
    # If they preserve origin, they should cluster or show structure.
    # If they scatter, it will look like noise.
    
    sc = ax.scatter(phi_end, np.pi/2 - theta_start, 
                    c=drift, cmap='turbo', s=1.5, alpha=0.6)
    
    ax.set_title(f"Holographic Phase Tracking: {N_DOTS} Travelers\nTwist k={K_TRAVELER} (The Traveler)", fontsize=14)
    cbar = plt.colorbar(sc, orientation='horizontal', pad=0.05, aspect=40)
    cbar.set_label("Phase Drift Magnitude (Shear Stress)")
    
    # Add Grid to see deformation
    ax.grid(True, alpha=0.3)
    
    plt.savefig("cmb_holographic_tracker.png", dpi=150)
    print("✅ Tracker Result saved to 'cmb_holographic_tracker.png'")

if __name__ == "__main__":
    main()