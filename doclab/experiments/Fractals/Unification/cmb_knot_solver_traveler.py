import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import RegularGridInterpolator
import pandas as pd
import sys

# --- CMB Dependencies (Required for the Full Computation) ---
# NOTE: Ensure Astropy and its dependencies (Healpy if needed) are installed in your environment.
from astropy.io import fits
from astropy_healpix import HEALPix
from scipy.special import sph_harm
import astropy.units as u
from astropy.coordinates import SkyCoord

# ==========================================================
# I. GLOBAL CONFIGURATION
# ==========================================================
# --- CMB Data Input ---
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits" # User-specified file
TARGET_L = 40          # The "Skeleton" Harmonic (from helical_scanner_bass.py)
K_VALUE = 1.0          # The true, untwisted geometry (k=1.0)
N_RES = 300            # Resolution of the skeletal map grid

# --- Physics Configuration (Integrated from proof_5 and proof_6) ---
STEPS = 1200
DT = 0.01
RADIUS = 20.0          
G_PHASE = 8.0          
STRESS_COEFF = 3.0     
SPEED_HIGH = 15.0      
CRITICAL_SPIN = 12.0   # Threshold for "Friction Spikes"
SPIKE_INTENSITY = 5.0  # Intensity of the spike / stiffness
CHANNEL_WINDUP = 0.8   # Wind-up rate based on velocity (from proof_6.py)
TWEAK_COEFF = 0.005    # Tuning factor for drag force magnitude (Retrograde Stiffness)

# --- Global Data Storage ---
SKELETAL_INTERPOLATOR = None

# ==========================================================
# II. CMB DATA EXTRACTION & MANIFOLD PREPARATION
# ==========================================================

def get_ylm(m, l, phi, theta):
    """Helper for Spherical Harmonic computation."""
    return sph_harm(m, l, phi, theta)

def extract_and_synthesize_skeletal_map():
    """
    Combines the extraction and synthesis steps from helical_scanner_bass.py
    to create the Skeletal Map Interpolator.
    """
    global SKELETAL_INTERPOLATOR
    
    print(f"[*] Starting CMB data pipeline for L={TARGET_L}, k={K_VALUE}...")

    # --- 1. Extract a_lm for TARGET_L ---
    try:
        data = fits.getdata(FITS_PATH)
    except FileNotFoundError:
        print(f"[!] FATAL ERROR: CMB FITS file '{FITS_PATH}' not found. Cannot proceed.")
        sys.exit(1)

    # Data loading and pre-processing
    if "I" in data.dtype.names: cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names: cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else: cmb = data.astype(np.float64)
    cmb[np.isnan(cmb)] = np.nanmean(cmb)

    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")

    # Integration grid for a_lm computation
    n_theta_alm = TARGET_L * 4
    n_phi_alm = TARGET_L * 8
    theta_alm = np.linspace(0, np.pi, n_theta_alm)
    phi_alm = np.linspace(-np.pi, np.pi, n_phi_alm, endpoint=False)
    TH_ALM, PH_ALM = np.meshgrid(theta_alm, phi_alm, indexing='ij')

    lon_deg = np.rad2deg((PH_ALM + 2*np.pi) % (2*np.pi))
    lat_deg = np.rad2deg(0.5*np.pi - TH_ALM)
    coords = SkyCoord(l=lon_deg*u.deg, b=lat_deg*u.deg, frame="galactic")
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    T_sample = cmb[ipix]

    dtheta = theta_alm[1] - theta_alm[0]
    dphi = phi_alm[1] - phi_alm[0]
    weights = np.sin(TH_ALM) * dtheta * dphi

    alms = {}
    l = TARGET_L
    for m in range(-l, l + 1):
        Y_lm = get_ylm(m, l, PH_ALM, TH_ALM)
        alms[(l, m)] = np.sum(T_sample * np.conjugate(Y_lm) * weights)
    
    print(f"  -> Extracted a_lm for L={TARGET_L}.")

    # --- 2. Synthesize Skeletal Map ---
    theta_res = np.linspace(0, np.pi, N_RES)
    phi_res = np.linspace(-np.pi, np.pi, N_RES)
    TH_RES, PH_RES = np.meshgrid(theta_res, phi_res, indexing='ij')
    
    map_out = np.zeros_like(TH_RES, dtype=np.complex128)
    
    for m in range(-l, l + 1):
        if (l, m) not in alms: continue
        
        Y_lm = get_ylm(m, l, PH_RES, TH_RES)
        twist_phase = np.exp(1j * m * (K_VALUE - 1.0) * PH_RES)
        map_out += alms[(l, m)] * Y_lm * twist_phase
            
    T_skeleton = map_out.real
    
    # --- 3. Create Interpolator ---
    # Convert map coordinates to Latitude (y-axis) and Longitude (x-axis) in degrees
    lon_pts = np.rad2deg(phi_res)
    lat_pts = np.rad2deg(0.5 * np.pi - theta_res)
    
    # The RegularGridInterpolator requires its coordinates to be monotonic.
    # We must match the order: lat_pts should be from min to max. 
    # Since theta runs 0 to pi, lat_pts runs 90 to -90. We reverse it for the interpolator.
    lat_pts_sorted = np.sort(lat_pts)
    T_skeleton_sorted = T_skeleton[np.argsort(lat_pts), :][::-1] 
    
    SKELETAL_INTERPOLATOR = RegularGridInterpolator(
        (lat_pts_sorted, lon_pts), 
        T_skeleton_sorted, 
        bounds_error=False, 
        fill_value=0.0
    )
    print("✅ Full Skeletal Map Interpolator ready for simulation.")


# ==========================================================
# III. TRAVELLER PHYSICS V3 (CMB & RETROGRADE STIFFNESS)
# ==========================================================

def get_manifold_influence(pos):
    """Samples the Skeletal Map for influence magnitude and direction."""
    x, y, z = pos
    r = np.linalg.norm(pos)
    
    if SKELETAL_INTERPOLATOR is not None and r > 1.0:
        # 1. Convert Cartesian to Spherical (Longitude/Latitude in degrees)
        lon_deg = np.rad2deg(np.arctan2(y, x))
        lat_deg = np.rad2deg(np.arccos(z / r))
        
        # 2. Sample the Skeletal Map Amplitude
        # The absolute value |T_skeleton| is the stiffness/friction magnitude
        amplitude = np.abs(SKELETAL_INTERPOLATOR([(lat_deg, lon_deg)]))[0]
        
        # 3. Define Influence Vector Direction (Tangential perturbation)
        # Use a vector orthogonal to position (tangent to sphere) with slight randomization
        # This models noise/stiffness along the manifold's surface
        np.random.seed(int(abs(x*10 + y*5 + z))) 
        random_perturbation = np.random.uniform(-1, 1, 3)
        tangent_vec = np.cross(pos, [0, 0, 1])
        if np.linalg.norm(tangent_vec) < 0.1: tangent_vec = np.cross(pos, [1, 0, 0])
        tangent_vec /= np.linalg.norm(tangent_vec)
        
        influence_direction = tangent_vec + random_perturbation * 0.1
        influence_direction /= np.linalg.norm(influence_direction)
        
        # Manifold Force = Amplitude * Scaling
        influence_vec = influence_direction * amplitude * 0.05
        
        return influence_vec, amplitude
    else:
        # Fallback to deterministic noise
        np.random.seed(int(abs(x*10 + y*5 + z))) 
        noise = np.random.uniform(-1, 1, 3)
        return noise * 0.5, 0.5

def compute_physics_v3(pos1, pos2, vel1, vel2, w1, w2):
    
    # --- 1. Phase Gravity & Kinematic Resonance (Intrinsic Pairing) ---
    r_vec = pos2 - pos1
    r = np.linalg.norm(r_vec)
    r_safe = max(r, 0.1)
    
    twist_sum = w1 + w2 
    # Resonance requires anti-parallel spin alignment (from proof_5.py)
    resonance = np.exp(-(twist_sum**2) / 0.1)
    
    speed = (np.linalg.norm(vel1) + np.linalg.norm(vel2)) / 2.0
    stress_factor = 1.0 + STRESS_COEFF * (speed**2)
    
    f_mag = (G_PHASE * resonance * stress_factor) / (r_safe**2)
    force_bond = (r_vec / r_safe) * f_mag
    
    # --- 2. Skeletal Manifold Influence ---
    influence1, amp1 = get_manifold_influence(pos1)
    influence2, amp2 = get_manifold_influence(pos2)
    
    # --- 3. Retrograde Stiffness Spike (Reflexive Action) ---
    # Spin exceeds critical limit -> Spike magnitude (from proof_6.py)
    spike1 = max(0, abs(w1) - CRITICAL_SPIN) * SPIKE_INTENSITY
    spike2 = max(0, abs(w2) - CRITICAL_SPIN) * SPIKE_INTENSITY
    total_spike = spike1 + spike2
    
    # Retrograde Stiffness Force F_stiff (Elasticity Interference Mode)
    # Applied as drag: opposes velocity, scaled by spike magnitude
    f_stiff1 = -vel1 * total_spike * TWEAK_COEFF 
    f_stiff2 = -vel2 * total_spike * TWEAK_COEFF
    
    # --- 4. Net External Force Calculation ---
    F1 = force_bond + influence1 + f_stiff1
    F2 = -force_bond + influence2 + f_stiff2
    
    return F1, F2, f_mag, total_spike

# ==========================================================
# IV. SIMULATION RUNNER & PLOTTING
# ==========================================================

def run_simulation_and_plot():
    
    # Prepare the CMB Skeletal Manifold
    extract_and_synthesize_skeletal_map()
    
    # Initial Conditions (based on proof_5.py)
    theta = np.pi / 4 
    
    p1 = np.array([-RADIUS * np.cos(theta), -RADIUS * np.sin(theta), 0.0])
    v1 = np.array([SPEED_HIGH, SPEED_HIGH * 0.2, 0.0]) 
    w1 = 5.0 
    
    p2 = np.array([RADIUS * np.cos(theta), RADIUS * np.sin(theta), 0.0])
    v2 = np.array([-SPEED_HIGH, -SPEED_HIGH * 0.2, 0.0])
    w2 = -5.0
    
    path1, path2 = [], []
    strengths = []
    spikes = []
    w_history = []
    
    for _ in range(STEPS):
        path1.append(p1.copy())
        path2.append(p2.copy())
        w_history.append(abs(w1))
        
        # Update Rotational Velocity (w) - Channel Wind-up
        speed1 = np.linalg.norm(v1)
        speed2 = np.linalg.norm(v2)
        dw1 = CHANNEL_WINDUP * speed1 * np.sign(w1) * DT
        dw2 = CHANNEL_WINDUP * speed2 * np.sign(w2) * DT
        w1 += dw1
        w2 += dw2
        
        # Physics
        F1, F2, bond_strength, spike_mag = compute_physics_v3(p1, p2, v1, v2, w1, w2)
        strengths.append(bond_strength)
        spikes.append(spike_mag)
        
        # Update Kinematics
        v1 += F1 * DT
        v2 += F2 * DT
        
        p1 += v1 * DT
        p2 += v2 * DT
        
        # Check merge condition
        if np.linalg.norm(p1 - p2) < 0.5: break
        
    p1_hist, p2_hist = np.array(path1), np.array(path2)
    bond_str, spike_mag, w_hist = np.array(strengths), np.array(spikes), np.array(w_history)


    # --- Plotting ---
    fig = plt.figure(figsize=(18, 6))

    # 1. Trajectories with Spike Locations (Top Down)
    ax1 = fig.add_subplot(1, 3, 1)
    circle = plt.Circle((0, 0), RADIUS, color='gray', fill=False, linestyle='--', alpha=0.5, label='Universe Boundary')
    ax1.add_artist(circle)

    ax1.plot(p1_hist[:,0], p1_hist[:,1], 'r-', linewidth=1.5, label='Traveler 1 (Forward)')
    ax1.plot(p2_hist[:,0], p2_hist[:,1], 'b-', linewidth=1.5, label='Traveler 2 (Retrograde)')

    spike_mask = spike_mag > 0.1
    ax1.scatter(p1_hist[spike_mask, 0], p1_hist[spike_mask, 1], c=spike_mag[spike_mask], cmap='hot', s=20, label='Retrograde Stiffness Activation')
    ax1.set_title("CMB Skeletal Resonance Trajectory (L=40)")
    ax1.set_xlim(-RADIUS-5, RADIUS+5)
    ax1.set_ylim(-RADIUS-5, RADIUS+5)
    ax1.legend()
    ax1.grid(True)

    # 2. Spin Up Process (Proof of Activation)
    ax2 = fig.add_subplot(1, 3, 2)
    ax2.plot(w_hist, 'b-', label='Rotational Velocity (|w|)')
    ax2.axhline(CRITICAL_SPIN, color='r', linestyle='--', label='Critical Threshold')
    ax2.set_title("Channel Wind-Up: Velocity $\\to$ Rotation")
    ax2.set_ylabel("Angular Velocity")
    ax2.set_xlabel("Time Step")
    ax2.legend()
    ax2.grid(True)

    # 3. Bond Strength vs Retrograde Stiffness Spike
    ax3 = fig.add_subplot(1, 3, 3)
    ax3.plot(bond_str, 'purple', label='Bond Strength (Phase Gravity + Stress)')
    ax3.plot(spike_mag, 'gold', alpha=0.7, label='Retrograde Stiffness Spike')
    ax3.set_title("Bond Dynamics vs Reflexive Action")
    ax3.set_xlabel("Time Step")
    ax3.set_yscale('log')
    ax3.legend()
    ax3.grid(True)

    plt.tight_layout()
    plt.savefig('cmb_skeletal_resonance_trajectory_publication.png')
    print("\n✅ Simulation Complete. Results saved to 'cmb_skeletal_resonance_trajectory_publication.png'")


if __name__ == "__main__":
    # Suppress Astropy FITS warnings for cleaner publication-ready run
    import warnings
    from astropy.wcs import FITSFixedWarning
    warnings.filterwarnings('ignore', category=FITSFixedWarning)
    
    run_simulation_and_plot()