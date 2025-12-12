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
import sys

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
LMAX = 60
CMB_RES = 512       # High Res for Macro View
FRACTAL_RES = 150   # Medium Res for smooth GIF generation (3D is heavy)
TWIST = 1.0         # The Moment of Impact
FRAMES = 60         # Animation Frames
STEPS_PER_FRAME = 15 # Physics steps per frame
DT = 0.05
GAMMA = 0.015

# ======================
# 1. CMB ENGINE (Macro Static)
# ======================
def get_cmb_field(fits_path, lmax, n_res, k_twist):
    print(f"[*] [CMB] Synthesizing Impact Geometry...")
    try:
        data = fits.getdata(fits_path)
        if "I" in data.dtype.names: cmb = np.array(data["I"], dtype=np.float64)
        elif "INP_CMB" in data.dtype.names: cmb = np.array(data["INP_CMB"], dtype=np.float64)
        else: cmb = data.astype(np.float64)
        cmb[np.isnan(cmb)] = np.nanmean(cmb)
    except FileNotFoundError:
        print("[!] CMB File not found. Using Mock Field.")
        theta = np.linspace(0, np.pi, n_res)
        phi = np.linspace(-np.pi, np.pi, n_res)
        M, L = np.meshgrid(theta, phi, indexing='ij')
        return np.sin(3*M)*np.cos(3*L)

    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")
    
    n_theta = lmax * 3; n_phi = lmax * 4
    t_alm = np.linspace(0, np.pi, n_theta)
    p_alm = np.linspace(-np.pi, np.pi, n_phi, endpoint=False)
    TH_ALM, PH_ALM = np.meshgrid(t_alm, p_alm, indexing='ij')
    
    lon = np.rad2deg((PH_ALM + 2*np.pi) % (2*np.pi)) * u.deg
    lat = np.rad2deg(0.5*np.pi - TH_ALM) * u.deg
    ipix = hpix.lonlat_to_healpix(lon, lat)
    T_sample = cmb[ipix]
    weights = np.sin(TH_ALM) * (t_alm[1] - t_alm[0]) * (p_alm[1] - p_alm[0])

    alms = {}
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            Y_lm = sph_harm(m, l, PH_ALM, TH_ALM)
            alms[(l, m)] = np.sum(T_sample * np.conjugate(Y_lm) * weights)
            
    theta = np.linspace(0, np.pi, n_res)
    phi = np.linspace(-np.pi, np.pi, n_res)
    
    m_range = np.arange(-lmax, lmax + 1)
    n_theta = len(theta)
    zeros_phi = np.zeros_like(theta)
    
    profiles = np.zeros((len(m_range), n_theta), dtype=np.complex128)
    for i, m in enumerate(m_range):
        for l in range(max(1, abs(m)), lmax + 1): 
            if (l, m) not in alms: continue
            profiles[i, :] += alms[(l, m)] * sph_harm(m, l, zeros_phi, theta)
            
    phase_matrix = np.exp(1j * m_range[:, None] * k_twist * phi[None, :])
    field = (profiles.T @ phase_matrix).real
    return field

# ======================
# 2. FRACTAL PHYSICS ENGINE
# ======================
def get_force_unified(m, lam, twist):
    # Unified Field Laws
    F_teal_m = -(m + 0.866) 
    F_teal_lam = -(lam - 0.5)

    F_red_m = -(m - 0.0)
    p_violation = twist * np.sin(m * 2.5) 
    F_red_lam = -(lam + 1.0) + p_violation

    sum_m = (F_teal_m + F_red_m)
    sum_lam = (F_teal_lam + F_red_lam)
    magnitude = np.sqrt(sum_m**2 + sum_lam**2)
    scaling = np.sqrt(magnitude)
    
    F_gold_m = sum_m * scaling
    F_gold_lam = sum_lam * scaling
    
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
def run_unification_gif():
    # --- PREPARE DATA ---
    # 1. CMB Map (Static Background)
    cmb_map = get_cmb_field(FITS_PATH, 60, CMB_RES, TWIST)
    
    # 2. Fractal State Initialization
    # We need two separate grids for the two zoom levels, or just one large one?
    # Let's do two separate simulations to match the exact zooms requested.
    
    # Simulation A: Zoom 2.5 (Vacuum Buckle)
    bounds_A = 2.5
    res_A = FRACTAL_RES
    mA = np.linspace(-bounds_A, bounds_A, res_A)
    lA = np.linspace(-bounds_A, bounds_A, res_A)
    MA, LA = np.meshgrid(mA, lA)
    vmA = np.zeros_like(MA); vlA = np.zeros_like(LA)
    activeA = np.ones_like(MA, dtype=bool)
    # We track "Stiffness" (Spin accumulation) for this one
    spinA = np.zeros_like(MA)
    prev_angA = np.arctan2(LA, MA)

    # Simulation B: Zoom 1.5 (The Spike) - Using same logic but closer view
    bounds_B = 1.5
    res_B = FRACTAL_RES
    mB = np.linspace(-bounds_B, bounds_B, res_B)
    lB = np.linspace(-bounds_B, bounds_B, res_B)
    MB, LB = np.meshgrid(mB, lB)
    vmB = np.zeros_like(MB); vlB = np.zeros_like(LB)
    activeB = np.ones_like(MB, dtype=bool)
    spinB = np.zeros_like(MB)
    prev_angB = np.arctan2(LB, MB)
    
    # Simulation C: Proton Basin (Using Sim A grid but tracking lifetime)
    lifetimeC = np.zeros_like(MA, dtype=float)

    frames = []
    print(f"[*] Rendering {FRAMES} frames of Genesis...")

    # --- RENDER LOOP ---
    for frame in range(FRAMES):
        # --- PHYSICS STEP ---
        # Run N steps of physics per frame to speed up "growth"
        for _ in range(STEPS_PER_FRAME):
            # Sim A (Zoom 2.5)
            FmA, FlamA = get_force_unified(MA, LA, TWIST)
            vmA[activeA] += (FmA[activeA] - GAMMA*vmA[activeA]) * DT
            vlA[activeA] += (FlamA[activeA] - GAMMA*vlA[activeA]) * DT
            MA[activeA] += vmA[activeA] * DT
            LA[activeA] += vlA[activeA] * DT
            
            # Spin Calc A
            curr_angA = np.arctan2(LA, MA)
            dA = curr_angA - prev_angA
            dA = np.where(dA>np.pi, dA-2*np.pi, dA); dA = np.where(dA<-np.pi, dA+2*np.pi, dA)
            spinA[activeA] += np.abs(dA)
            prev_angA = curr_angA
            
            # Lifetime Calc C (Proton)
            speedA = np.sqrt(vmA[activeA]**2 + vlA[activeA]**2)
            lifetimeC[activeA] += speedA # Accumulate distance
            activeA[activeA] &= (speedA > 0.01)

            # Sim B (Zoom 1.5)
            FmB, FlamB = get_force_unified(MB, LB, TWIST)
            vmB[activeB] += (FmB[activeB] - GAMMA*vmB[activeB]) * DT
            vlB[activeB] += (FlamB[activeB] - GAMMA*vlB[activeB]) * DT
            MB[activeB] += vmB[activeB] * DT
            LB[activeB] += vlB[activeB] * DT
            
            # Spin Calc B
            curr_angB = np.arctan2(LB, MB)
            dB = curr_angB - prev_angB
            dB = np.where(dB>np.pi, dB-2*np.pi, dB); dB = np.where(dB<-np.pi, dB+2*np.pi, dB)
            spinB[activeB] += np.abs(dB)
            prev_angB = curr_angB
            activeB[activeB] &= ((vmB[activeB]**2 + vlB[activeB]**2) > 0.01)

        # --- PLOTTING ---
        fig = plt.figure(figsize=(16, 12), facecolor='#050505')
        gs = gridspec.GridSpec(2, 3, height_ratios=[1.5, 1])
        
        # PANEL 1: CMB MACRO (Static, Whole Spectrum)
        ax_cmb = plt.subplot(gs[0, :])
        # Use 'nipy_spectral' for the "Whole Spectrum" effect requested
        ax_cmb.imshow(cmb_map, origin='lower', cmap='nipy_spectral', extent=[-180, 180, -90, 90])
        ax_cmb.set_title(f"THE MOMENT OF IMPACT | CMB Geometry (Twist K={TWIST})", color='cyan', fontsize=16)
        ax_cmb.axis('off')
        
        # PANEL 2: VACUUM MAP (Zoom 2.5)
        ax_vac = plt.subplot(gs[1, 0])
        # Log scale for fractal detail
        ax_vac.imshow(np.log1p(spinA.reshape(res_A, res_A)), origin='lower', cmap='magma', 
                      extent=[-2.5, 2.5, -2.5, 2.5])
        ax_vac.set_title("VACUUM MANIFOLD (2.5x)\n(The Buckle)", color='white', fontsize=12)
        ax_vac.axis('off')
        
        # PANEL 3: THE SPIKE (Zoom 1.5, 3D Angled)
        ax_spike = plt.subplot(gs[1, 1], projection='3d')
        ax_spike.set_facecolor('#050505')
        
        # Create grid for plotting (needs to match reshaped data)
        X_plot, Y_plot = np.meshgrid(np.linspace(-1.5, 1.5, res_B), np.linspace(-1.5, 1.5, res_B))
        Z_plot = np.log1p(spinB.reshape(res_B, res_B))
        
        ax_spike.plot_surface(X_plot, Y_plot, Z_plot, cmap='magma', rcount=res_B, ccount=res_B, shade=True)
        ax_spike.view_init(elev=30, azim=-45) # Angled view as requested
        ax_spike.set_title("THE REENTRY FLAME (1.5x)\n(The Spike)", color='gold', fontsize=12)
        ax_spike.axis('off')
        
        # PANEL 4: PROTON BASIN (Zoom 2.5)
        ax_prot = plt.subplot(gs[1, 2])
        ax_prot.imshow(np.log1p(lifetimeC.reshape(res_A, res_A)), origin='lower', cmap='bone', 
                       extent=[-2.5, 2.5, -2.5, 2.5])
        ax_prot.set_title("PROTON BASIN GENESIS\n(The Scar)", color='white', fontsize=12)
        ax_prot.axis('off')
        
        plt.tight_layout()
        
        # Capture Frame
        buf = io.BytesIO()
        plt.savefig(buf, format='png', facecolor='#050505')
        buf.seek(0)
        frames.append(Image.open(buf).copy())
        plt.close(fig)
        buf.close()
        
        # sys.stdout.write(f"\r[>] Frame {frame+1}/{FRAMES}")
        # sys.stdout.flush()

    print(f"\n[*] Compiling GIF...")
    frames[0].save('unification_genesis.gif', save_all=True, append_images=frames[1:], 
                   optimize=True, duration=100, loop=0)
    print("✅ Unification GIF Saved: unification_genesis.gif")

if __name__ == "__main__":
    run_unification_gif()