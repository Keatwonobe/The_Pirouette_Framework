# hcs_gradient_analyzer.py
# VERSION 2 - "Better Eyes"
# - Implements lobe detection on the phase-gradient field, as per DOMA-164.md.
# - This allows for the detection of more subtle, higher-order structures.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from PIL import Image
import argparse

# --- Helper Functions (dominant_angular_mode is the only one modified) ---

def polar_grid(n: int = 192, r_max: float = 1.0):
    lin = np.linspace(-r_max, r_max, n)
    x, y = np.meshgrid(lin, lin)
    r = np.sqrt(x*x + y*y) + 1e-12
    theta = np.arctan2(y, x)
    return x, y, r, theta

# added
def signed_angular_gradient(field, theta):
    gx, gy = np.gradient(field)
    tx, ty = -np.sin(theta), np.cos(theta)   # tangential unit vector
    return gx*tx + gy*ty
# added
def dominant_angular_mode(field, theta, max_m=8):
    # Measure on the signed angular derivative, not |∇φ|
    s = signed_angular_gradient(field, theta)
    s = s - s.mean()
    n = s.shape[0]; c = n//2
    rr = np.sqrt((np.indices(s.shape)[0]-c)**2 + (np.indices(s.shape)[1]-c)**2)
    mask = rr > 4
    amps = []
    for m in range(1, max_m+1):
        c0 = np.sum(s[mask]*np.cos(m*theta[mask]))
        s0 = np.sum(s[mask]*np.sin(m*theta[mask]))
        amps.append((m, float(np.hypot(c0, s0))))
    amps.sort(key=lambda t: t[1], reverse=True)
    return int(amps[0][0]), s


def helical_time_evolve(field, kappa, t, omega=2*np.pi*1.0):
    # Corrected gradient usage for helical evolution
    grad_field_y, grad_field_x = np.gradient(field)
    return np.cos(kappa * omega * t) * field + np.sin(kappa * omega * t) * grad_field_y
# added
def _proj_mode(field, theta, m):
    basis = np.cos(m*theta)
    coef = np.sum(field*basis) / (np.sum(basis*basis) + 1e-12)
    return coef, basis
# added
def psi_collapse_to_m2(field, theta, Ta, Gamma, m_dom):
    # smooth gate (annealed corridor)
    g = float(np.clip((1.0 - Ta)*Gamma, 0.0, 1.0))
    g = 1.0 - np.exp(-3.0*g)

    # remove fraction g of dominant mode
    c_dom, b_dom = _proj_mode(field, theta, m_dom)
    removed = g * c_dom * b_dom
    remainder = field - removed

    # recycle removed energy into m=2 with existing phase/sign
    c2, b2 = _proj_mode(remainder, theta, 2)
    E_removed = np.sqrt(np.mean(removed**2) + 1e-12)
    b2_unit = b2 / (np.sqrt(np.mean(b2**2)) + 1e-12)
    refill = E_removed * b2_unit * np.sign(c2 if abs(c2) > 1e-8 else 1.0)

    collapsed = remainder + refill
    collapse_map = np.abs(collapsed - field)
    return collapsed, g, collapse_map


def detect_frequency(signal, dt):
    from numpy.fft import rfft, rfftfreq
    sig = signal - np.mean(signal)
    yf = np.abs(rfft(sig))
    xf = rfftfreq(len(sig), dt)
    if len(xf) < 3: return 0.0, 0.0, xf, yf
    yf[0] = 0.0
    i = int(np.argmax(yf))
    peak = float(yf[i])
    noise = float(np.median(yf[yf > 0])) if np.any(yf > 0) else 1e-12
    return float(xf[i]), float(peak / (noise + 1e-12)), xf, yf

def phase_flux_space(field, dx=1.0):
    gx, gy = np.gradient(field, dx, dx)
    return float(np.mean(np.hypot(gx, gy)))

def phase_flux_time(signal, dt):
    d = np.gradient(signal, dt)
    return float(np.mean(np.abs(d)))

def ingest_field(path, size=192):
    img = Image.open(path).convert("L").resize((size, size))
    arr = np.array(img).astype(np.float32)
    arr = (arr - arr.mean()) / (arr.std() + 1e-12)
    return np.tanh(arr / 2.5)

# --- Main Simulation and Visualization Function ---

def run_one(field, kappa, Ta, Gamma, Ki, outdir=None, tag=None, save_figs=False):
    n = field.shape[0]
    x, y, r, theta = polar_grid(n, 1.0)
    
    # MODIFIED: Capture lobes and gradient field from the new function.
    lobes_before, pre_gradient_field = dominant_angular_mode(field, theta)
    space_flux = phase_flux_space(field)
    
    evolved = helical_time_evolve(field, kappa, t=6.0)
    # added
    m_pre, pre_sig = dominant_angular_mode(evolved, theta)
    collapsed, gate, collapse_map = psi_collapse_to_m2(evolved, theta, Ta, Gamma, m_dom=m_pre)
    m_post, post_sig = dominant_angular_mode(collapsed, theta)

    
    # MODIFIED: Capture lobes and gradient field for the 'after' state.
    lobes_after, post_gradient_field = dominant_angular_mode(collapsed, theta)
    
    t = np.arange(0, 6.0, 1/160.0)
    base = float(np.tanh(collapsed.mean()))
    phi = base * np.sin(Ki * t)
    dt = 1/160.0
    f, snr, xf, yf = detect_frequency(phi, dt)
    time_flux = phase_flux_time(phi, dt)
    bal = abs(space_flux - time_flux) / (abs(space_flux) + abs(time_flux) + 1e-12)
    verdict = bool((Ta <= 0.35) and (Gamma >= 0.75) and (lobes_after <= 2) and (snr >= 5.0) and (bal < 0.9))
    
    fp = sp = cp = None
    if save_figs and outdir and tag:
        os.makedirs(outdir, exist_ok=True)
        
        # MODIFIED: Visualization now shows the gradient field where lobes are detected.
        plt.figure(figsize=(10, 4))
        plt.suptitle("Phase-Gradient Fields", fontsize=16)

        plt.subplot(1, 2, 1)
        im1 = plt.imshow(pre_gradient_field, cmap="viridis")
        plt.colorbar(im1, fraction=0.046, pad=0.04)
        plt.axis("off")
        # MODIFIED: Title now reflects the new measurement method.
        plt.title(f"Pre-Collapse (Gradient Lobes ≈ {lobes_before})")
        
        plt.subplot(1, 2, 2)
        im2 = plt.imshow(post_gradient_field, cmap="viridis")
        plt.colorbar(im2, fraction=0.046, pad=0.04)
        plt.axis("off")
        plt.title(f"Post-Collapse (Gradient Lobes ≈ {lobes_after})")
        
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        fp = os.path.join(outdir, f"{tag}_gradient_fields.png")
        plt.savefig(fp)
        plt.close()
        
        # Spectrum plot (unchanged)
        plt.figure(figsize=(6, 4))
        plt.plot(xf, yf); plt.xlabel("Frequency"); plt.ylabel("Amplitude")
        plt.title(f"Ki spectrum (SNR={snr:.1f}, peak={f:.2f})")
        plt.tight_layout(); sp = os.path.join(outdir, f"{tag}_spectrum.png")
        plt.savefig(sp); plt.close()

        # Collapse Locus plot (unchanged)
        plt.figure(figsize=(5.5, 4))
        im_collapse = plt.imshow(collapse_map, cmap="inferno")
        plt.colorbar(im_collapse, label="Magnitude of Change")
        plt.title("Collapse Locus"); plt.axis("off"); plt.tight_layout()
        cp = os.path.join(outdir, f"{tag}_collapse_map.png")
        plt.savefig(cp); plt.close()

    return {
        "lobes_before": int(lobes_before), "lobes_after": int(lobes_after), 
        "gate": float(gate), "beat_peak": float(f), "beat_SNR": float(snr),
        "phase_balance_error": float(bal), "verdict_pass": verdict, 
        "gradient_png": fp or "", "spectrum_png": sp or "", "collapse_png": cp or ""
    }

# --- Main Execution Block (Unchanged) ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the HCS dimensional collapse simulation on a single image.")
    parser.add_argument("image_path", type=str, help="Path to the input image file.")
    args = parser.parse_args()

    kappas = [0.2, 0.9]
    params = [(0.90, 0.40, 2 * np.pi * 0.6), (0.28, 0.88, 2 * np.pi * 0.8)]
    rows = []; base_dir = "simulation_gallery_gradient"
    os.makedirs(base_dir, exist_ok=True)

    pth = args.image_path
    if not os.path.exists(pth):
        print(f"❌ Error: Image path not found at '{pth}'"); exit()
    
    print(f"Processing image with GRADIENT analysis: {pth}")
    slug = os.path.splitext(os.path.basename(pth))[0]
    field = ingest_field(pth, size=192)
    out_dir = os.path.join(base_dir, slug)
    os.makedirs(out_dir, exist_ok=True)

    for i, k in enumerate(kappas):
        for j, (Ta, Gamma, Ki) in enumerate(params):
            param_type = 'ctrl' if j == 0 else 'corr'
            tag = f"{slug}_k{k:.2f}_{param_type}"
            res = run_one(field, k, Ta, Gamma, Ki, outdir=out_dir, tag=tag, save_figs=(j == 1))
            
            row_data = {"image": slug, "kappa": k, "param_type": param_type, **res}
            rows.append(row_data)

    atlas = pd.DataFrame(rows)
    csv_path = f"atlas_{slug}_gradient.csv"
    atlas.to_csv(csv_path, index=False)
    
    print(f"\n✅ Gradient analysis complete! Your files are in '{base_dir}' and the current directory.")