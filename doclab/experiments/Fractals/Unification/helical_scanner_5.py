import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy_healpix import HEALPix
from astropy.coordinates import SkyCoord
import astropy.units as u
from scipy.special import sph_harm, sph_harm_y
from PIL import Image
import warnings
import os
import sys

warnings.filterwarnings("ignore", category=RuntimeWarning)

# ============================================================
# CONFIGURATION
# ============================================================
FITS_PATH   = "COM_CompMap_CMB-smica_2048_R1.20.fits"
LMAX        = 40
REMOVE_BAND = (10, 40)   # (L1, L2) Substrate = everything EXCEPT this band

# Synthesis grid (Visualization Resolution)
N_TH_SYN = 180
N_PH_SYN = 360

# Twist scan parameters
K_MIN, K_MAX = -1.5, 4.0
N_K          = 121
K_VALUES     = np.linspace(K_MIN, K_MAX, N_K)

# Cache / Output
ALM_CACHE = f"cmb_alms_lmax{LMAX}.npz"
GIF_NAME  = "cmb_substrate_helical_scanner5.gif"

# ============================================================
# HELPER: Spherical Harmonics
# ============================================================
def get_ylm(m, l, phi, theta):
    """
    Wrapper that prefers sph_harm_y (scipy 1.15+) if present,
    otherwise falls back to sph_harm.
    """
    try:
        return sph_harm_y(l, m, phi, theta)
    except (TypeError, AttributeError):
        return sph_harm(m, l, phi, theta)

# ============================================================
# STEP 1: Load CMB and compute a_lm (Integration Grid)
# ============================================================
def load_cmb_and_alms(fits_path, lmax):
    """
    Compute a_lm up to lmax from the SMICA CMB map using quadrature
    on a HEALPix grid. Caches result to disk.
    """
    if os.path.exists(ALM_CACHE):
        print(f"[*] Loading cached a_lm from {ALM_CACHE}...")
        data = np.load(ALM_CACHE)
        alms = {}
        Ls, Ms = data["L"], data["M"]
        Re, Im = data["Re"], data["Im"]
        for L, M, r, im in zip(Ls, Ms, Re, Im):
            alms[(int(L), int(M))] = r + 1j * im
        return alms

    print(f"[*] Computing a_lm up to L={lmax} from {fits_path}...")
    try:
        data = fits.getdata(fits_path)
    except FileNotFoundError:
        print(f"[!] ERROR: {fits_path} not found.")
        sys.exit(1)

    # Handle SMICA column structure
    if isinstance(data, np.ndarray) and data.dtype.fields:
        if "I" in data.dtype.names:
            cmb = np.array(data["I"], dtype=np.float64)
        elif "INP_CMB" in data.dtype.names:
            cmb = np.array(data["INP_CMB"], dtype=np.float64)
        else:
            cmb = np.array(data[data.dtype.names[0]], dtype=np.float64)
    else:
        cmb = data.astype(np.float64)

    cmb[np.isnan(cmb)] = np.nanmean(cmb)

    nside = int(np.sqrt(cmb.size / 12))
    hpix  = HEALPix(nside=nside, order="ring", frame="galactic")

    # Integration grid (Higher res than synthesis to capture details)
    n_theta = lmax * 4
    n_phi   = lmax * 8
    theta   = np.linspace(0, np.pi, n_theta)
    phi     = np.linspace(-np.pi, np.pi, n_phi, endpoint=False)
    TH, PH  = np.meshgrid(theta, phi, indexing="ij")

    lon = np.rad2deg((PH + 2*np.pi) % (2*np.pi))
    lat = np.rad2deg(0.5*np.pi - TH)
    coords = SkyCoord(l=lon*u.deg, b=lat*u.deg, frame="galactic")
    ipix   = hpix.lonlat_to_healpix(coords.l, coords.b)
    T_s    = cmb[ipix]

    dtheta = theta[1] - theta[0]
    dphi   = phi[1]   - phi[0]
    weights = np.sin(TH) * dtheta * dphi

    alms = {}
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            Y = get_ylm(m, l, PH, TH)
            val = np.sum(T_s * np.conjugate(Y) * weights)
            alms[(l, m)] = val

    # Cache to disk
    Ls, Ms, Re, Im = [], [], [], []
    for (l, m), v in alms.items():
        Ls.append(l); Ms.append(m)
        Re.append(v.real); Im.append(v.imag)
    np.savez(ALM_CACHE, L=np.array(Ls), M=np.array(Ms),
             Re=np.array(Re), Im=np.array(Im))
    print(f"[*] Saved a_lm cache to {ALM_CACHE}")

    return alms

# ============================================================
# STEP 2: Build Mode Maps (Synthesis Grid)
# ============================================================
def build_mode_maps(alms, LMAX, remove_band=None):
    """
    Build the per-ℓ,m mode contribution maps on the SYNTHESIS grid.
    Returns: (mode_maps, TH, PH)
    """
    # Create the synthesis grid based on Global Config
    theta = np.linspace(0, np.pi, N_TH_SYN)
    phi   = np.linspace(-np.pi, np.pi, N_PH_SYN, endpoint=False)
    TH, PH = np.meshgrid(theta, phi, indexing="ij")

    mode_maps = {} # Changed to dict for sparse access if needed, or list
    # Use list for indexed access to match L
    mode_maps_list = []

    for L in range(LMAX + 1):
        shape = (N_TH_SYN, N_PH_SYN)
        layer = np.zeros(shape, dtype=np.complex128)

        for M in range(-L, L+1):
            alm = alms.get((L, M), 0)
            if alm == 0:
                continue
            # Project onto grid
            contrib = alm * np.exp(1j * M * PH) * (np.cos(TH) ** L)
            layer += contrib
        
        mode_maps_list.append(layer)

    # BAND REMOVAL
    if remove_band is not None:
        lmin, lmax_band = remove_band
        for L in range(lmin, min(lmax_band+1, LMAX+1)):
            mode_maps_list[L][:] = 0.0

    # Convert to dict for compatibility with synthesize_helical if it expects dict
    # But synthesize_helical below expects dict {m: map} ??? 
    # WAIT: The previous code had a specific logic for helical synthesis. 
    # Let's align with the "twist" logic: T = Sum( M_m * exp(i*m*(k-1)*phi) )
    # So we need to aggregate by M, not L.
    
    # RE-AGGREGATION BY M for Helical Twist efficiency
    maps_by_m = {}
    
    for L in range(LMAX + 1):
        # Skip if in removed band
        if remove_band and (remove_band[0] <= L <= remove_band[1]):
            continue
            
        for M in range(-L, L+1):
            alm = alms.get((L, M), 0)
            if alm == 0: continue
            
            # The mode shape excluding the phi-phase part that depends on twist
            # We separate the exp(im phi) part? 
            # Original math: Y_lm ~ P_lm(theta) * exp(i m phi)
            # Helical twist: phi -> k * phi
            # So effectively we modify the M-frequency. 
            
            # To optimize: We sum up all P_lm(theta) for a given M first.
            # But the user's previous code was: contrib = alm * exp(1j*M*PH) * cos(TH)**L
            # That `cos(TH)**L` is a proxy for P_lm (approx). 
            
            # We stick to the user's logic exactly to preserve the physics model:
            base_contrib = alm * (np.cos(TH) ** L) 
            
            if M not in maps_by_m:
                maps_by_m[M] = np.zeros((N_TH_SYN, N_PH_SYN), dtype=np.complex128)
            
            # We store the part that DOES NOT have the twist yet.
            # Normal reconstruction: base * exp(i M phi)
            # Twisted reconstruction: base * exp(i M k phi)
            # So we store 'base' which is alm * P_lm(theta)
            
            # WAIT: The previous code stored `mode_maps[L]`. 
            # Let's look at `synthesize_helical` in the original snippet.
            # It iterated `for m, M in mode_maps.items():`
            # This implies the input `mode_maps` was DICT OF M, not L.
            
            maps_by_m[M] += base_contrib

    return maps_by_m, TH, PH

# ============================================================
# STEP 3: Helical Synthesis
# ============================================================
def synthesize_helical(mode_maps_by_m, PH, k_twist):
    """
    Helical twist synthesis:
    T_k(θ,φ) = Re Σ_m [ (Σ_l a_lm P_lm) * e^{i m k φ} ]
    
    mode_maps_by_m contains the (Σ_l a_lm P_lm) part for each m.
    """
    out = np.zeros_like(PH, dtype=np.complex128)

    for m, M_field in mode_maps_by_m.items():
        # Apply the twisted phase: exp(i * m * k * phi)
        # Note: Standard reconstruction is k=1
        phase = np.exp(1j * m * k_twist * PH)
        out  += M_field * phase

    return out.real

# ============================================================
# STEP 4: Normalization
# ============================================================
def normalize_frame(arr):
    lo, hi = np.percentile(arr, [2, 98])
    arr = np.clip(arr, lo, hi)
    if hi > lo:
        arr = (arr - lo) / (hi - lo)
    else:
        arr[:] = 0.0
    return arr

# ============================================================
# MAIN: GIF Generator
# ============================================================
def main():
    print("=== Helical Scanner 5 : Substrate Twist Evolution ===")
    print(f"LMAX = {LMAX}, removing L={REMOVE_BAND[0]}–{REMOVE_BAND[1]} band.")

    # 1. Load a_lm
    alms = load_cmb_and_alms(FITS_PATH, LMAX)

    # 2. Build aggregated maps by M (for efficient twisting)
    print("[*] Building substrate helical mode maps (Aggregated by M)...")
    # Note: build_mode_maps handles the band removal internally
    maps_by_m, TH, PH = build_mode_maps(alms, LMAX, remove_band=REMOVE_BAND)

    # 3. Reference map (k=1)
    print("[*] Synthesizing reference substrate (k=1)...")
    T_ref = synthesize_helical(maps_by_m, PH, k_twist=1.0)
    T_ref -= T_ref.mean()

    # 4. Generate frames
    frames = []
    lon = np.linspace(-180, 180, N_PH_SYN)
    lat = np.linspace(-90,  90, N_TH_SYN)
    extent = [lon.min(), lon.max(), lat.min(), lat.max()]

    print(f"[*] Scanning k from {K_MIN} to {K_MAX} ({N_K} steps)...")
    for i, k in enumerate(K_VALUES):
        sys.stdout.write(f"\r[>] k = {k:.3f}  ({i+1}/{N_K})")
        sys.stdout.flush()

        T_k = synthesize_helical(maps_by_m, PH, k_twist=k)
        T_k -= T_k.mean()

        # Visualizing the Difference from Normality (Strain)
        diff = np.abs(T_ref - T_k)
        diff_norm = normalize_frame(diff)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(diff_norm.T, origin="lower", extent=extent, cmap="inferno", aspect="auto")
        ax.set_title(f"Substrate Strain | k = {k:.3f}")
        plt.tight_layout()
        
        fname = f"scanner5_temp_{i:03d}.png"
        plt.savefig(fname, dpi=100)
        plt.close(fig)

        with Image.open(fname) as pim:
            frames.append(pim.convert("P", palette=Image.ADAPTIVE))
        os.remove(fname)

    print(f"\n[*] Saving GIF to {GIF_NAME}...")
    frames[0].save(GIF_NAME, save_all=True, append_images=frames[1:], duration=80, loop=0)
    print("✅ Done.")

if __name__ == "__main__":
    main()