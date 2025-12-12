import numpy as np
import matplotlib.pyplot as plt
from scipy.special import sph_harm

# ==========================================
# 1. SYNTHETIC CMB GENERATOR
# ==========================================

def generate_synthetic_cmb(res, l_max=30):
    """
    Generates a random CMB-like field using spherical harmonics.
    """
    x = np.linspace(-1, 1, res)
    y = np.linspace(-1, 1, res)
    X, Y = np.meshgrid(x, y)
    
    # Map square to sphere (approximate for visual patch)
    theta = np.pi * (Y + 1) / 2 # 0 to pi
    phi = np.pi * (X + 1)       # 0 to 2pi
    
    cmb = np.zeros_like(X)
    
    print(f"[-] Synthesizing CMB (l_max={l_max})...")
    
    # Add random harmonics
    for l in range(1, l_max):
        for m in range(-l, l+1):
            # Random complex coefficient
            a_lm = np.random.randn() + 1j * np.random.randn()
            # Scale power (Cl ~ 1/l^2 approx)
            scale = 1.0 / (l**1.5)
            harmonic = sph_harm(m, l, phi, theta).real
            cmb += scale * a_lm.real * harmonic
            
    # Normalize
    cmb = (cmb - cmb.mean()) / cmb.std()
    return cmb

# ==========================================
# 2. WADA GEOMETRY GENERATOR (Deterministic)
# ==========================================

def get_basin_single(m, l):
    # Simplified non-compiled version for compatibility
    # Just checking the geometric structure
    # We use a pre-computed or simple analytic check for speed here
    # Actually, let's use the provided code structure but purely vectorized numpy
    return 0 

def generate_wada_mask(res, zoom=2.0):
    """
    Generates the Wada Basin boundaries.
    """
    x = np.linspace(-zoom, zoom, res)
    y = np.linspace(-zoom, zoom, res)
    X, Y = np.meshgrid(x, y)
    
    # Fast vectorized integration (Euler)
    m = X.copy()
    l = Y.copy()
    pm = np.zeros_like(m)
    pl = np.zeros_like(l)
    
    active = np.ones_like(m, dtype=bool)
    steps = 40
    dt = 0.1
    sigma = 1.0
    
    print(f"[-] Generating Wada Geometry ({res}x{res})...")
    
    for _ in range(steps):
        fm = -(m + 2*sigma*m*l)
        fl = -(l + sigma*(m**2 - l**2))
        pm += 0.5 * dt * fm
        pl += 0.5 * dt * fl
        m += dt * pm
        l += dt * pl
        fm = -(m + 2*sigma*m*l)
        fl = -(l + sigma*(m**2 - l**2))
        pm += 0.5 * dt * fm
        pl += 0.5 * dt * fl
        
    # Determine Basins
    angle = np.arctan2(l, m)
    
    # Create the "Skeleton Mask" (Edges)
    # We use the angle gradient to find boundaries
    grad = np.abs(np.diff(angle, axis=1, append=angle[:, -1:])) + \
           np.abs(np.diff(angle, axis=0, append=angle[-1:, :]))
           
    mask = grad > 0.5 # Threshold for boundary
    return mask.astype(float)

# ==========================================
# 3. THE INTERACTION
# ==========================================

RES = 800

# 1. Get the "Random" Universe
cmb = generate_synthetic_cmb(RES, l_max=40)

# 2. Get the "Fixed" Wada Skeleton
wada = generate_wada_mask(RES, zoom=2.0)

# 3. INTERFERENCE
# We look for correlations.
# Visualizing: CMB intensity * Wada Structure
interference = cmb * wada

# Plot
fig, axes = plt.subplots(1, 3, figsize=(18, 6), facecolor='black')

# Plot 1: The Cosmic Data (CMB)
axes[0].imshow(cmb, cmap='RdBu', extent=[-1, 1, -1, 1])
axes[0].set_title("1. The Data (Synthetic CMB)", color='white')
axes[0].axis('off')

# Plot 2: The Hidden Geometry (Wada)
axes[1].imshow(wada, cmap='gray', extent=[-1, 1, -1, 1], vmin=0, vmax=1)
axes[1].set_title("2. The Geometry (Wada Skeleton)", color='white')
axes[1].axis('off')

# Plot 3: The Pop-Out (Interaction)
# We use a glowing colormap to show where they hit
im = axes[2].imshow(interference, cmap='inferno', extent=[-1, 1, -1, 1])
axes[2].set_title("3. The Pop-Out (Constructive Interference)", color='white')
axes[2].axis('off')

plt.suptitle("Testing the 'Traveler' Hypothesis: Geometric Filtering", color='white', fontsize=16)
plt.tight_layout()
plt.savefig('wada_cmb_interaction.png')
print("[+] Interaction Analysis Complete.")