import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from mpl_toolkits.mplot3d import Axes3D
from astropy.io import fits
from astropy_healpix import HEALPix
from scipy.special import sph_harm
import astropy.units as u
from PIL import Image
import io
import os
import sys

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
LMAX = 40           # Optimized for speed
CMB_RES = 300       # Resolution for interference map
FRACTAL_RES = 150   # Resolution for fractals
FRAMES = 60         # Total animation frames
DURATION = 150      # ms per frame (Slow motion)

# CMB Twist Range (The "Event Window")
K_START = 0.9999
K_END = 1.0001
K_RANGE = np.linspace(K_START, K_END, FRAMES)

# Fractal Physics
STEPS_PER_FRAME = 10 # Sub-steps for smooth growth
DT = 0.02
GAMMA = 0.015
TWIST_FRACTAL = 3.8 # The "Proton" Twist

# ======================
# 1. CMB INTERFERENCE ENGINE
# ======================
YLM_CACHE = None
ALMS_CACHE = None
TH_GRID = None
PH_GRID = None

def init_cmb_engine(fits_path, lmax, n_res):
    global YLM_CACHE, ALMS_CACHE, TH_GRID, PH_GRID
    if ALMS_CACHE is not None: return

    print(f"[*] [CMB] Loading & Caching Harmonics (LMAX={lmax})...")
    try:
        data = fits.getdata(fits_path)
        if "I" in data.dtype.names: cmb = np.array(data["I"], dtype=np.float64)
        elif "INP_CMB" in data.dtype.names: cmb = np.array(data["INP_CMB"], dtype=np.float64)
        else: cmb = data.astype(np.float64)
        cmb[np.isnan(cmb)] = np.nanmean(cmb)
    except FileNotFoundError:
        print("[!] CMB File not found. Using Mock Data.")
        cmb = np.random.randn(12*32**2) # Mock

    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")
    
    # ALM Grid
    n_t = lmax * 4; n_p = lmax * 8
    t_a = np.linspace(0, np.pi, n_t)
    p_a = np.linspace(-np.pi, np.pi, n_p, endpoint=False)
    TA, PA = np.meshgrid(t_a, p_a, indexing='ij')
    
    # Extract ALMs
    lon = np.rad2deg((PA + 2*np.pi) % (2*np.pi)) * u.deg
    lat = np.rad2deg(0.5*np.pi - TA) * u.deg
    ipix = hpix.lonlat_to_healpix(lon, lat)
    T_samp = cmb[ipix]
    dth = t_a[1]-t_a[0]; dph = p_a[1]-p_a[0]
    w = np.sin(TA) * dth * dph
    
    alms = {}
    for l in range(lmax+1):
        for m in range(-l, l+1):
            try: Y = sph_harm(m, l, PA, TA)
            except: from scipy.special import sph_harm as sh; Y = sh(m, l, PA, TA)
            alms[(l, m)] = np.sum(T_samp * np.conjugate(Y) * w)
    ALMS_CACHE = alms
    
    # Synthesis Grid
    theta = np.linspace(0, np.pi, n_res)
    phi = np.linspace(-np.pi, np.pi, n_res)
    TH_GRID, PH_GRID = np.meshgrid(theta, phi, indexing='ij')
    
    # Cache Untwisted Ylms
    YLM_CACHE = {}
    for l in range(lmax+1):
        for m in range(-l, l+1):
            try: Y = sph_harm(m, l, PH_GRID, TH_GRID)
            except: from scipy.special import sph_harm as sh; Y = sh(m, l, PH_GRID, TH_GRID)
            YLM_CACHE[(l, m)] = Y

def get_interference_frame(k_val, lmax):
    # 1. Synthesize Twisted Map
    map_twist = np.zeros_like(TH_GRID, dtype=np.complex128)
    delta_phi = (k_val - 1.0) * PH_GRID
    
    for l in range(lmax+1):
        for m in range(-l, l+1):
            term = ALMS_CACHE[(l,m)] * YLM_CACHE[(l,m)]
            phase = np.exp(1j * m * delta_phi)
            map_twist += term * phase
            
    map_ref = np.zeros_like(TH_GRID, dtype=np.complex128)
    for l in range(lmax+1):
        for m in range(-l, l+1):
            map_ref += ALMS_CACHE[(l,m)] * YLM_CACHE[(l,m)]
            
    diff = np.abs(map_ref - map_twist)
    return np.power(diff, 0.4) # Gamma correction

# ======================
# 2. FRACTAL PHYSICS ENGINE
# ======================
def get_force_unified(m, lam):
    F_teal_m = -(m + 0.866) 
    F_teal_lam = -(lam - 0.5)

    F_red_m = -(m - 0.0)
    p_violation = TWIST_FRACTAL * np.sin(m * 2.5) 
    F_red_lam = -(lam + 1.0) + p_violation

    sum_m = (F_teal_m + F_red_m)
    sum_lam = (F_teal_lam + F_red_lam)
    mag = np.sqrt(sum_m**2 + sum_lam**2)
    scale = np.sqrt(mag)
    
    F_gold_m = sum_m * scale
    F_gold_lam = sum_lam * scale
    
    angle = np.degrees(np.arctan2(lam, m)) % 360
    
    d_g = np.minimum(np.abs(angle - 30), 360-np.abs(angle - 30)); w_g = np.exp(-(d_g/80)**2)
    d_t = np.minimum(np.abs(angle - 150), 360-np.abs(angle - 150)); w_t = np.exp(-(d_t/80)**2)
    d_r = np.minimum(np.abs(angle - 270), 360-np.abs(angle - 270)); w_r = np.exp(-(d_r/80)**2)
    
    tot = w_g + w_t + w_r + 1e-6
    Fm = (w_t*F_teal_m + w_r*F_red_m + w_g*F_gold_m) / tot
    Flam = (w_t*F_teal_lam + w_r*F_red_lam + w_g*F_gold_lam) / tot
    
    return Fm, Flam

# ======================
# 3. ANIMATION LOOP
# ======================
def run_unification_v2():
    # --- INIT CMB ---
    init_cmb_engine(FITS_PATH, LMAX, CMB_RES)
    
    # --- INIT FRACTALS ---
    # Sim A: Zoom 2.5 (Vacuum Buckle)
    bA = 2.5
    mA = np.linspace(-bA, bA, FRACTAL_RES); lA = np.linspace(-bA, bA, FRACTAL_RES)
    MA, LA = np.meshgrid(mA, lA)
    vmA = np.zeros_like(MA); vlA = np.zeros_like(LA)
    actA = np.ones_like(MA, dtype=bool)
    spinA = np.zeros_like(MA)
    prevA = np.arctan2(LA, MA)
    
    # Sim B: Zoom 1.5 (The Spike) - Angled
    bB = 1.25
    mB = np.linspace(-bB, bB, FRACTAL_RES); lB = np.linspace(-bB, bB, FRACTAL_RES)
    MB, LB = np.meshgrid(mB, lB)
    vmB = np.zeros_like(MB); vlB = np.zeros_like(LB)
    actB = np.ones_like(MB, dtype=bool)
    spinB = np.zeros_like(MB)
    prevB = np.arctan2(LB, MB)
    
    # Sim C: Proton Basin (Tracking Life on Grid A)
    lifeC = np.zeros_like(MA, dtype=float)

    frames_buf = []
    print(f"[*] Rendering {FRAMES} frames (Slow Motion)...")

    for i, k_val in enumerate(K_RANGE):
        if i % 5 == 0: print(f"    Processing Frame {i+1}/{FRAMES}...")
        
        # --- 1. CMB FRAME ---
        cmb_frame = get_interference_frame(k_val, LMAX)
        
        # --- 2. FRACTAL PHYSICS SUB-STEPS ---
        for _ in range(STEPS_PER_FRAME):
            # Sim A (Buckle & Proton)
            if np.any(actA):
                Fm, Flam = get_force_unified(MA, LA)
                vmA[actA] += (Fm[actA] - GAMMA*vmA[actA]) * DT
                vlA[actA] += (Flam[actA] - GAMMA*vlA[actA]) * DT
                MA[actA] += vmA[actA] * DT
                LA[actA] += vlA[actA] * DT
                
                currA = np.arctan2(LA, MA)
                dA = currA - prevA
                dA = np.where(dA>np.pi, dA-2*np.pi, dA); dA = np.where(dA<-np.pi, dA+2*np.pi, dA)
                
                spinA[actA] += np.abs(dA[actA])
                prevA = currA
                
                # FIXED TYPO HERE: actA instead of activeA
                spd = np.sqrt(vmA[actA]**2 + vlA[actA]**2) 
                lifeC[actA] += spd
                actA[actA] &= (spd > 0.01)

            # Sim B (The Spike)
            if np.any(actB):
                Fm, Flam = get_force_unified(MB, LB)
                vmB[actB] += (Fm[actB] - GAMMA*vmB[actB]) * DT
                vlB[actB] += (Flam[actB] - GAMMA*vlB[actB]) * DT
                MB[actB] += vmB[actB] * DT
                LB[actB] += vlB[actB] * DT
                
                currB = np.arctan2(LB, MB)
                dB = currB - prevB
                dB = np.where(dB>np.pi, dB-2*np.pi, dB); dB = np.where(dB<-np.pi, dB+2*np.pi, dB)
                spinB[actB] += np.abs(dB[actB])
                prevB = currB
                
                spdB = np.sqrt(vmB[actB]**2 + vlB[actB]**2)
                actB[actB] &= (spdB > 0.01)

        # --- 3. COMPOSITE PLOT ---
        fig = plt.figure(figsize=(14, 10), facecolor='#050505')
        gs = gridspec.GridSpec(2, 3, height_ratios=[1.2, 1])
        
        # TOP: CMB Interference
        ax1 = plt.subplot(gs[0, :])
        im1 = ax1.imshow(cmb_frame, origin='lower', cmap='inferno', aspect='auto',
                         extent=[-180, 180, -90, 90])
        ax1.set_title(f"THE EVENT HORIZON | Interference K = {k_val:.8f}", color='cyan', fontsize=14)
        ax1.axis('off')
        
        # BOT LEFT: Vacuum Buckle (2.5x)
        ax2 = plt.subplot(gs[1, 0])
        ax2.imshow(np.log1p(spinA), origin='lower', cmap='magma', extent=[-2.5,2.5,-2.5,2.5])
        ax2.set_title("VACUUM MANIFOLD\n(Buckling)", color='gold', fontsize=10)
        ax2.axis('off')
        
        # BOT CENTER: The Spike (1.25x Angled)
        ax3 = plt.subplot(gs[1, 1], projection='3d')
        ax3.set_facecolor('#050505')
        skip = 2
        Xp = np.linspace(-1.25, 1.25, FRACTAL_RES)[::skip]
        Yp = np.linspace(-1.25, 1.25, FRACTAL_RES)[::skip]
        XX, YY = np.meshgrid(Xp, Yp)
        ZZ = np.log1p(spinB)[::skip, ::skip]
        
        ax3.plot_surface(XX, YY, ZZ, cmap='magma', rcount=50, ccount=50, shade=True)
        ax3.view_init(elev=35, azim=-45 + (i*0.5))
        ax3.set_title("THE REENTRY SPIKE\n(Topological Verticality)", color='orange', fontsize=10)
        ax3.axis('off')
        
        # BOT RIGHT: Proton Scar (2.5x)
        ax4 = plt.subplot(gs[1, 2])
        ax4.imshow(np.log1p(lifeC), origin='lower', cmap='viridis', extent=[-2.5,2.5,-2.5,2.5])
        ax4.set_title("PROTON BASIN\n(The Scar)", color='white', fontsize=10)
        ax4.axis('off')
        
        plt.tight_layout()
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', facecolor='#050505')
        buf.seek(0)
        frames_buf.append(Image.open(buf).copy())
        plt.close(fig)
        buf.close()

    print(f"[*] Saving GIF (Duration: {DURATION}ms)...")
    frames_buf[0].save('unification_genesis_v2.gif', save_all=True, 
                       append_images=frames_buf[1:], optimize=True, 
                       duration=DURATION, loop=0)
    print("✅ DONE: unification_genesis_v2.gif")

if __name__ == "__main__":
    run_unification_v2()