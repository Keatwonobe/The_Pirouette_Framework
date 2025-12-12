import numpy as np
from astropy_healpix import HEALPix
from astropy.coordinates import SkyCoord
import astropy.units as u
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb 
from scipy.special import sph_harm
from scipy.ndimage import gaussian_filter

# ======================
# CONFIG
# ======================
# Replicating original scan parameters exactly
TWIST_MODE = "untwist" 
LMAX = 40
N_THETA = 320 
N_PHI = 640
NSIDE = 2048 # Matches the real CMB file resolution

# Scanning Parameters
K_RANGE_COARSE = np.linspace(0, 2, 600) 
SPIKE_THRESHOLD = 0.005 
SPIKE_WINDOW = 5        

# ======================
# 1. THE FAKE UNIVERSE GENERATOR
# ======================
def generate_mock_cmb(nside):
    """Generates a HEALPix map of Smoothed Red Noise (The Control)."""
    print("[*] Generating Mock Universe (Red Noise on Sphere)...")
    
    # 1. Generate noise on a temporary high-res grid
    temp_theta = np.linspace(0, np.pi, 1000)
    temp_phi = np.linspace(-np.pi, np.pi, 2000)
    TH_gen, PH_gen = np.meshgrid(temp_theta, temp_phi, indexing='ij')
    
    # 2. Gaussian Smooth it (Simulating acoustic peaks/blobs)
    print("    -> creating and smoothing noise...")
    np.random.seed(42) # Fixed seed for reproducibility
    noise = np.random.normal(0, 1, size=TH_gen.shape)
    smooth_noise = gaussian_filter(noise, sigma=5.0) 
    
    # 3. Project to HEALPix
    print(f"    -> projecting to HEALPix (NSIDE={nside})...")
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")
    
    lon_deg = np.rad2deg((PH_gen + 2*np.pi) % (2*np.pi))
    lat_deg = np.rad2deg(0.5*np.pi - TH_gen)
    coords = SkyCoord(l=lon_deg*u.deg, b=lat_deg*u.deg, frame="galactic")
    ipix_gen = hpix.lonlat_to_healpix(coords.l, coords.b)
    
    mock_cmb = np.zeros(hpix.npix)
    mock_cmb[ipix_gen.ravel()] = smooth_noise.ravel()
    
    # Fill gaps
    zero_mask = mock_cmb == 0
    mock_cmb[zero_mask] = np.mean(mock_cmb[~zero_mask])
    
    return mock_cmb, hpix

# ======================
# 2. HELPER FUNCTIONS
# ======================
def twist_phi(phi, k, mode="untwist"):
    if mode == "twist":
        src = phi * k
    else:
        src = phi / k
    return (src + np.pi) % (2.0 * np.pi) - np.pi

def build_equatorial_grid(n_theta, n_phi):
    theta = np.linspace(0.0, np.pi, n_theta)
    phi   = np.linspace(-np.pi, np.pi, n_phi, endpoint=False)
    TH, PH = np.meshgrid(theta, phi, indexing="ij")
    return TH, PH

def healpix_sample(cmb, hpix, TH, PH):
    lon_deg = np.rad2deg((PH + 2*np.pi) % (2*np.pi))
    lat_deg = np.rad2deg(0.5*np.pi - TH) 
    coords = SkyCoord(l=lon_deg*u.deg, b=lat_deg*u.deg, frame="galactic")
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    return cmb[ipix]

# ======================
# 3. ANALYSIS MATH (Spherical Harmonics)
# ======================
Y_LM_CONJ_WEIGHTED = None

def compute_alm_final(T, TH, PH, lmax):
    global Y_LM_CONJ_WEIGHTED
    if Y_LM_CONJ_WEIGHTED is None:
        theta_1d = TH[:, 0]
        phi_1d   = PH[0, :]
        dtheta = theta_1d[1] - theta_1d[0]
        dphi   = phi_1d[1] - phi_1d[0]
        sinTH = np.sin(TH)
        weight = (sinTH * dtheta * dphi).ravel()
        PH_flat  = PH.ravel()
        TH_flat  = TH.ravel()
        N_GRID   = TH_flat.size
        Y_lms = np.zeros((lmax+1, 2*lmax+1, N_GRID), dtype=np.complex128)
        print(f"    -> Pre-computing Spherical Harmonics (One-time)...")
        for l in range(lmax+1):
            for m in range(-l, l+1):
                Y_lms[l, m + lmax] = sph_harm(m, l, PH_flat, TH_flat)
        Y_LM_CONJ_WEIGHTED = np.conjugate(Y_lms).reshape(-1, N_GRID) * weight

    T_flat = T.ravel()
    alms_flat = np.dot(T_flat, Y_LM_CONJ_WEIGHTED.T) 
    return alms_flat.reshape(lmax+1, 2*lmax+1)

def alm_correlation(alm0, alm1, lmax):
    num = 0 + 0j
    den0 = 0.0
    den1 = 0.0
    for l in range(lmax+1):
        for m in range(-l, l+1):
            a0 = alm0[l, m + LMAX]
            a1 = alm1[l, m + LMAX]
            num  += a0 * np.conjugate(a1)
            den0 += np.abs(a0)**2
            den1 += np.abs(a1)**2
    if den0 == 0 or den1 == 0: return 0.0
    return num / np.sqrt(den0 * den1)

def find_troughs(k_values, C_abs_values, threshold, window):
    trough_k = []
    for i in range(window, len(C_abs_values) - window):
        C_i = C_abs_values[i]
        C_before = C_abs_values[i - window : i]
        C_after  = C_abs_values[i + 1 : i + window + 1]
        C_avg_surrounding = np.mean(np.concatenate((C_before, C_after)))
        if (C_avg_surrounding - C_i) > threshold:
            trough_k.append(k_values[i])
    trough_k.sort()
    final_troughs = []
    if trough_k:
        final_troughs.append(trough_k[0])
        for k in trough_k[1:]:
            if np.abs(k - final_troughs[-1]) > (k_values[1] - k_values[0]) * 3:
                final_troughs.append(k)
    return final_troughs

def plot_correlation_spectrum(k_values, C_abs_values, special_k_list, suffix=""):
    fig, ax = plt.subplots(figsize=(10, 5), constrained_layout=True)
    ax.plot(k_values, C_abs_values, label="|C(k)| Mock Universe")
    ax.axvline(1.0, color="k", linestyle="--", label="k = 1")
    for k_special in special_k_list:
        ax.axvline(k_special, color="r", linestyle=":", alpha=0.5)
        
    ax.set_ylabel("|C(k)|")
    ax.set_xlabel("Twist constant k")
    ax.set_title(f"Mock Scan: Multipole correlation (Red Noise + HEALPix)")
    ax.legend()
    plt.savefig(f"mock_spectrum_{suffix}.png")
    plt.close(fig)

# ======================
# MAIN EXECUTION
# ======================
def main_mock_scan():
    # 1. Generate the Fake Data
    mock_cmb, hpix = generate_mock_cmb(NSIDE)
    
    # 2. Setup Grid
    print("[*] Building analysis grid...")
    TH, PH = build_equatorial_grid(N_THETA, N_PHI)
    
    # 3. Base Reference
    print("[*] Sampling Base Mock Map...")
    cmb_orig = healpix_sample(mock_cmb, hpix, TH, PH)
    alm_orig = compute_alm_final(cmb_orig, TH, PH, LMAX)
    
    # 4. The Scan
    C_values = []
    print(f"[*] Starting MOCK SCAN over {len(K_RANGE_COARSE)} k values...")
    
    for i, k in enumerate(K_RANGE_COARSE):
        if i % 50 == 0: print(f"    [-] k = {k:.4f}")
        
        # Twist
        PH_src = twist_phi(PH, k, mode=TWIST_MODE)
        
        # Sample from the Mock HEALPix array
        cmb_tw = healpix_sample(mock_cmb, hpix, TH, PH_src)
        
        # Correlate
        alm_tw = compute_alm_final(cmb_tw, TH, PH, LMAX)
        Ck = np.abs(alm_correlation(alm_orig, alm_tw, LMAX))
        C_values.append(Ck)
        
    C_values = np.array(C_values)
    
    # 5. Analysis
    print("[*] Analyzing Spectrum...")
    troughs = find_troughs(K_RANGE_COARSE, C_values, SPIKE_THRESHOLD, SPIKE_WINDOW)
    
    print(f"[+] Found {len(troughs)} spikes in the MOCK data.")
    plot_correlation_spectrum(K_RANGE_COARSE, C_values, troughs, "full_scan")

if __name__ == "__main__":
    main_mock_scan()