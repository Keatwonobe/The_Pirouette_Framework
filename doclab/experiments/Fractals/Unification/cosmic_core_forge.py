import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from astropy.io import fits
from astropy_healpix import HEALPix
from scipy.special import sph_harm
from scipy.ndimage import gaussian_filter
import astropy.units as u
from astropy.coordinates import SkyCoord
import sys

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
LMAX = 50              # Harmonic resolution
N_RES = 256            # Spatial resolution
N_FRAMES = 120         # Temporal evolution frames
CORE_RADIUS_DEG = 30   # Size of the core volume to examine

# Twist range for temporal evolution (k=1 is "now")
K_RANGE = np.linspace(0.9999, 1.0001, N_FRAMES)

# ======================
# 1. FIND THE CENTER
# ======================

def get_alms_and_grid(fits_path, lmax, n_res):
    """Load CMB and compute spherical harmonic coefficients"""
    print(f"[*] Loading CMB Data from {fits_path}...")
    try:
        data = fits.getdata(fits_path)
        if "I" in data.dtype.names: 
            cmb = np.array(data["I"], dtype=np.float64)
        elif "INP_CMB" in data.dtype.names: 
            cmb = np.array(data["INP_CMB"], dtype=np.float64)
        else: 
            cmb = data.astype(np.float64)
        cmb[np.isnan(cmb)] = np.nanmean(cmb)
    except FileNotFoundError:
        print(f"[!] ERROR: {fits_path} not found")
        sys.exit(1)

    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")
    
    # Compute a_lm coefficients
    n_theta_alm = lmax * 3
    n_phi_alm = lmax * 4
    t_alm = np.linspace(0, np.pi, n_theta_alm)
    p_alm = np.linspace(-np.pi, np.pi, n_phi_alm, endpoint=False)
    TH_ALM, PH_ALM = np.meshgrid(t_alm, p_alm, indexing='ij')
    
    lon = np.rad2deg((PH_ALM + 2*np.pi) % (2*np.pi))
    lat = np.rad2deg(0.5*np.pi - TH_ALM)
    coords = SkyCoord(l=lon*u.deg, b=lat*u.deg, frame="galactic")
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    T_sample = cmb[ipix]
    weights = np.sin(TH_ALM) * (t_alm[1] - t_alm[0]) * (p_alm[1] - p_alm[0])

    print(f"[*] Computing spherical harmonic coefficients (lmax={lmax})...")
    alms = {}
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            Y_lm = sph_harm(m, l, PH_ALM, TH_ALM)
            alms[(l, m)] = np.sum(T_sample * np.conjugate(Y_lm) * weights)
    
    # Create evaluation grid
    theta = np.linspace(0, np.pi, n_res)
    phi = np.linspace(-np.pi, np.pi, n_res)
    TH_GRID, PH_GRID = np.meshgrid(theta, phi, indexing='ij')
    
    return alms, TH_GRID, PH_GRID, cmb

def synthesize_field(alms, TH, PH, k_twist=1.0):
    """Synthesize the CMB field with optional topological twist"""
    field = np.zeros_like(TH, dtype=np.complex128)
    delta_phi_multiplier = (k_twist - 1) * PH
    
    for l in range(LMAX + 1):
        for m in range(-l, l + 1):
            if (l, m) not in alms: 
                continue
            Y_lm = sph_harm(m, l, PH, TH)
            phase_correction = np.exp(1j * m * delta_phi_multiplier)
            field += alms[(l, m)] * Y_lm * phase_correction
            
    return field.real

def compute_structure_intensity(field):
    """Compute gradient magnitude (structure intensity)"""
    gy, gx = np.gradient(field)
    return np.sqrt(gx**2 + gy**2)

def find_mathematical_center(alms, TH, PH):
    """
    Find the center using multiple signatures:
    1. Maximum structure intensity (wound channel curvature)
    2. Maximum gradient variance (interference knot)
    3. Cold spot location (holonomy deficit)
    """
    print("[*] Searching for the Mathematical Center...")
    
    # Synthesize the reference field
    field_ref = synthesize_field(alms, TH, PH, k_twist=1.0)
    
    # Compute structure intensity
    structure = compute_structure_intensity(field_ref)
    
    # Find cold spot (minimum temperature)
    cold_idx = np.unravel_index(np.argmin(field_ref), field_ref.shape)
    cold_theta, cold_phi = TH[cold_idx], PH[cold_idx]
    
    # Find max structure (wound channel curvature)
    structure_smooth = gaussian_filter(structure, sigma=3)
    max_struct_idx = np.unravel_index(np.argmax(structure_smooth), structure_smooth.shape)
    struct_theta, struct_phi = TH[max_struct_idx], PH[max_struct_idx]
    
    # Find interference knot (max gradient variance in local region)
    # This is where forward/retrograde travelers interfere most strongly
    grad_variance = np.zeros_like(field_ref)
    window = 5
    for i in range(window, TH.shape[0] - window):
        for j in range(window, TH.shape[1] - window):
            local_patch = structure[i-window:i+window, j-window:j+window]
            grad_variance[i, j] = np.var(local_patch)
    
    knot_idx = np.unravel_index(np.argmax(grad_variance), grad_variance.shape)
    knot_theta, knot_phi = TH[knot_idx], PH[knot_idx]
    
    # Convert to galactic coordinates
    def theta_phi_to_galactic(theta, phi):
        l = np.rad2deg(phi)
        b = np.rad2deg(0.5*np.pi - theta)
        return l, b
    
    cold_l, cold_b = theta_phi_to_galactic(cold_theta, cold_phi)
    struct_l, struct_b = theta_phi_to_galactic(struct_theta, struct_phi)
    knot_l, knot_b = theta_phi_to_galactic(knot_theta, knot_phi)
    
    print(f"    Cold Spot:           l={cold_l:6.2f}°, b={cold_b:6.2f}°")
    print(f"    Max Structure:       l={struct_l:6.2f}°, b={struct_b:6.2f}°")
    print(f"    Interference Knot:   l={knot_l:6.2f}°, b={knot_b:6.2f}°")
    
    # Average the signatures (they should cluster near the true center)
    center_theta = np.mean([cold_theta, struct_theta, knot_theta])
    center_phi = np.mean([cold_phi, struct_phi, knot_phi])
    center_l, center_b = theta_phi_to_galactic(center_theta, center_phi)
    
    print(f"\n[✓] Mathematical Center: l={center_l:.2f}°, b={center_b:.2f}°")
    
    return center_theta, center_phi, (cold_theta, cold_phi), (struct_theta, struct_phi), (knot_theta, knot_phi)

# ======================
# 2. EXTRACT CORE VOLUME
# ======================

def extract_core_volume(TH, PH, center_theta, center_phi, radius_deg):
    """Extract indices for the core volume around the center"""
    radius_rad = np.deg2rad(radius_deg)
    
    # Angular distance from center
    angular_dist = np.arccos(
        np.sin(center_theta) * np.sin(TH) * np.cos(PH - center_phi) +
        np.cos(center_theta) * np.cos(TH)
    )
    
    core_mask = angular_dist <= radius_rad
    return core_mask

# ======================
# 3. TEMPORAL DYNAMICS
# ======================

def compute_core_dynamics(alms, TH, PH, center_theta, center_phi, k_range):
    """
    Compute temporal evolution of the core through topological twist.
    Returns time series of core properties.
    """
    print(f"[*] Computing Core Dynamics over {len(k_range)} time steps...")
    
    core_mask = extract_core_volume(TH, PH, center_theta, center_phi, CORE_RADIUS_DEG)
    
    # Time series data
    core_intensity = np.zeros(len(k_range))
    core_coherence = np.zeros(len(k_range))
    core_curvature = np.zeros(len(k_range))
    
    for i, k in enumerate(k_range):
        if (i + 1) % 20 == 0:
            print(f"    Step {i+1}/{len(k_range)}")
        
        # Synthesize field at this time step
        field = synthesize_field(alms, TH, PH, k_twist=k)
        structure = compute_structure_intensity(field)
        
        # Extract core statistics
        core_field = field[core_mask]
        core_struct = structure[core_mask]
        
        # Intensity: Mean absolute temperature fluctuation
        core_intensity[i] = np.mean(np.abs(core_field))
        
        # Coherence: Inverse of standard deviation (higher = more coherent)
        core_coherence[i] = 1.0 / (np.std(core_field) + 1e-10)
        
        # Curvature: Mean structure intensity (gradient magnitude)
        core_curvature[i] = np.mean(core_struct)
    
    return core_intensity, core_coherence, core_curvature, core_mask

# ======================
# 4. VISUALIZATION
# ======================

def create_core_forge_visualization(alms, TH, PH, center_theta, center_phi, 
                                   core_mask, k_range, 
                                   core_intensity, core_coherence, core_curvature):
    """
    Create the animated visualization of the Cosmic Core Forge.
    Shows the heart of reality being forged through time.
    """
    print("[*] Forging the Visualization...")
    
    fig = plt.figure(figsize=(16, 10), facecolor='#000000')
    gs = fig.add_gridspec(3, 2, height_ratios=[2, 1, 1], hspace=0.3, wspace=0.3)
    
    # Main core view (top spanning both columns)
    ax_core = fig.add_subplot(gs[0, :])
    ax_core.set_facecolor('#000000')
    
    # Time series plots
    ax_intensity = fig.add_subplot(gs[1, 0])
    ax_intensity.set_facecolor('#0a0a0a')
    ax_coherence = fig.add_subplot(gs[1, 1])
    ax_coherence.set_facecolor('#0a0a0a')
    ax_curvature = fig.add_subplot(gs[2, 0])
    ax_curvature.set_facecolor('#0a0a0a')
    ax_phase = fig.add_subplot(gs[2, 1], projection='polar')
    ax_phase.set_facecolor('#000000')
    
    # Initialize plots
    lon_grid = np.rad2deg(PH)
    lat_grid = np.rad2deg(0.5*np.pi - TH)
    extent = [lon_grid.min(), lon_grid.max(), lat_grid.min(), lat_grid.max()]
    
    # Initial frame
    field_0 = synthesize_field(alms, TH, PH, k_twist=k_range[0])
    structure_0 = compute_structure_intensity(field_0)
    
    # Create composite view: structure intensity with core highlighted
    composite = np.zeros((*structure_0.shape, 3))
    composite[:, :, 0] = structure_0 / structure_0.max()  # Red channel
    composite[:, :, 1] = structure_0 / structure_0.max() * 0.5  # Green channel
    composite[:, :, 2] = structure_0 / structure_0.max() * 0.2  # Blue channel
    composite[core_mask] = [1, 1, 0.3]  # Highlight core in yellow
    
    im_core = ax_core.imshow(composite, extent=extent, origin='lower', aspect='auto')
    
    # Mark center
    center_l = np.rad2deg(center_phi)
    center_b = np.rad2deg(0.5*np.pi - center_theta)
    ax_core.plot(center_l, center_b, 'r+', markersize=20, markeredgewidth=3)
    ax_core.set_title("THE COSMIC CORE | Heart of the Fire", 
                     color='white', fontsize=16, pad=20)
    ax_core.set_xlabel("Galactic Longitude", color='gray')
    ax_core.set_ylabel("Galactic Latitude", color='gray')
    ax_core.tick_params(colors='gray')
    
    # Time series
    time_steps = np.arange(len(k_range))
    line_int, = ax_intensity.plot([], [], color='#ff4444', linewidth=2)
    ax_intensity.set_xlim(0, len(k_range))
    ax_intensity.set_ylim(core_intensity.min()*0.9, core_intensity.max()*1.1)
    ax_intensity.set_title("Core Intensity", color='white', fontsize=10)
    ax_intensity.set_xlabel("Time Step", color='gray', fontsize=8)
    ax_intensity.tick_params(colors='gray', labelsize=8)
    ax_intensity.grid(color='#222', linestyle=':', alpha=0.3)
    
    line_coh, = ax_coherence.plot([], [], color='#44ff44', linewidth=2)
    ax_coherence.set_xlim(0, len(k_range))
    ax_coherence.set_ylim(core_coherence.min()*0.9, core_coherence.max()*1.1)
    ax_coherence.set_title("Core Coherence", color='white', fontsize=10)
    ax_coherence.set_xlabel("Time Step", color='gray', fontsize=8)
    ax_coherence.tick_params(colors='gray', labelsize=8)
    ax_coherence.grid(color='#222', linestyle=':', alpha=0.3)
    
    line_curv, = ax_curvature.plot([], [], color='#4444ff', linewidth=2)
    ax_curvature.set_xlim(0, len(k_range))
    ax_curvature.set_ylim(core_curvature.min()*0.9, core_curvature.max()*1.1)
    ax_curvature.set_title("Core Curvature", color='white', fontsize=10)
    ax_curvature.set_xlabel("Time Step", color='gray', fontsize=8)
    ax_curvature.tick_params(colors='gray', labelsize=8)
    ax_curvature.grid(color='#222', linestyle=':', alpha=0.3)
    
    # Phase space (polar)
    ax_phase.set_title("Phase Evolution", color='white', fontsize=10, pad=20)
    ax_phase.tick_params(colors='gray', labelsize=8)
    line_phase, = ax_phase.plot([], [], color='cyan', linewidth=1, alpha=0.6)
    
    def init():
        line_int.set_data([], [])
        line_coh.set_data([], [])
        line_curv.set_data([], [])
        line_phase.set_data([], [])
        return line_int, line_coh, line_curv, line_phase, im_core
    
    def animate(frame):
        # Update core view
        k = k_range[frame]
        field = synthesize_field(alms, TH, PH, k_twist=k)
        structure = compute_structure_intensity(field)
        
        composite = np.zeros((*structure.shape, 3))
        composite[:, :, 0] = structure / structure.max()
        composite[:, :, 1] = structure / structure.max() * 0.5
        composite[:, :, 2] = structure / structure.max() * 0.2
        
        # Pulse the core highlighting
        pulse = 0.5 + 0.5 * np.sin(frame * 0.2)
        composite[core_mask] = [1, pulse, 0.3]
        
        im_core.set_data(composite)
        ax_core.set_title(f"THE COSMIC CORE | k={k:.6f} | Frame {frame+1}/{N_FRAMES}", 
                         color='white', fontsize=16, pad=20)
        
        # Update time series
        line_int.set_data(time_steps[:frame+1], core_intensity[:frame+1])
        line_coh.set_data(time_steps[:frame+1], core_coherence[:frame+1])
        line_curv.set_data(time_steps[:frame+1], core_curvature[:frame+1])
        
        # Update phase space (intensity vs coherence)
        theta_phase = np.linspace(0, 2*np.pi, frame+1)
        r_phase = core_intensity[:frame+1] / core_intensity.max()
        line_phase.set_data(theta_phase, r_phase)
        
        return line_int, line_coh, line_curv, line_phase, im_core
    
    anim = FuncAnimation(fig, animate, init_func=init, frames=N_FRAMES,
                        interval=50, blit=True, repeat=True)
    
    return fig, anim

# ======================
# 5. MAIN EXECUTION
# ======================

def main():
    print("=" * 70)
    print("COSMIC CORE FORGE | Finding the Heart of Reality")
    print("=" * 70)
    
    # Load data and compute harmonics
    alms, TH, PH, cmb = get_alms_and_grid(FITS_PATH, LMAX, N_RES)
    
    # Find the mathematical center
    center_theta, center_phi, cold, struct, knot = find_mathematical_center(alms, TH, PH)
    
    # Compute temporal dynamics
    core_int, core_coh, core_curv, core_mask = compute_core_dynamics(
        alms, TH, PH, center_theta, center_phi, K_RANGE
    )
    
    # Create visualization
    fig, anim = create_core_forge_visualization(
        alms, TH, PH, center_theta, center_phi, core_mask, K_RANGE,
        core_int, core_coh, core_curv
    )
    
    # Save
    output_file = "cosmic_core_forge.gif"
    print(f"\n[*] Saving animation to {output_file}...")
    writer = PillowWriter(fps=20)
    anim.save(output_file, writer=writer)
    
    print(f"\n[✓] Core Forge Complete!")
    print(f"[✓] Saved: {output_file}")
    print("\nThe heart of the fire has been revealed.")
    print("=" * 70)

if __name__ == "__main__":
    main()