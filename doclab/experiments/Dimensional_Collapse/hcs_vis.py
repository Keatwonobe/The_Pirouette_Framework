# hcs_visualizer.py
# MODIFIED from hcs_zipper.py
# - Now accepts any image via command line.
# - Enhanced visualizations:
#   - Adds a "Collapse Locus" plot to show where the change occurs.
#   - Adds colorbars to all image plots for scale.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from PIL import Image
import argparse  # NEW: For handling command-line arguments

# --- Helper Functions (largely unchanged) ---

def polar_grid(n: int = 192, r_max: float = 1.0):
    lin = np.linspace(-r_max, r_max, n)
    x, y = np.meshgrid(lin, lin)
    r = np.sqrt(x*x + y*y) + 1e-12
    theta = np.arctan2(y, x)
    return x, y, r, theta

def dominant_angular_mode(field, theta, max_m=8):
    n = field.shape[0]
    mask = np.ones_like(field, dtype=bool)
    c = n // 2
    rr = np.sqrt((np.indices(field.shape)[0] - c)**2 + (np.indices(field.shape)[1] - c)**2)
    mask[rr < 4] = False
    amps = []
    for m in range(1, max_m + 1):
        c0 = np.sum(field[mask] * np.cos(m * theta[mask]))
        s0 = np.sum(field[mask] * np.sin(m * theta[mask]))
        amps.append((m, float(np.hypot(c0, s0))))
    amps.sort(key=lambda t: t[1], reverse=True)
    return int(amps[0][0])

def helical_time_evolve(field, kappa, t, omega=2*np.pi*1.0):
    return np.cos(kappa * omega * t) * field + np.sin(kappa * omega * t) * np.gradient(field, axis=0)[0]

def psi_3to2_collapse_strong(field, theta, Ta, Gamma):
    # NEW: This function now also returns a map of where the collapse occurred.
    m3 = np.cos(3 * theta)
    m2 = np.cos(2 * theta)
    a3 = np.sum(field * m3)
    field_no_m3 = field - (a3 / (np.sum(m3 * m3) + 1e-12)) * m3
    E = np.sqrt(np.mean(field_no_m3**2) + 1e-12)
    m2u = m2 / np.sqrt(np.mean(m2**2) + 1e-12)
    refill = E * m2u
    g = float(np.clip((1.0 - Ta) * Gamma, 0.0, 1.0))
    
    collapsed_field = (1.0 - g) * field + g * refill
    # NEW: Calculate the absolute difference to see the magnitude of change at each pixel.
    collapse_map = np.abs(collapsed_field - field)
    
    return collapsed_field, g, collapse_map

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
    
    lobes_before = dominant_angular_mode(field, theta)
    space_flux = phase_flux_space(field)
    
    evolved = helical_time_evolve(field, kappa, t=6.0)
    # NEW: Capture the collapse_map from the modified function.
    collapsed, gate, collapse_map = psi_3to2_collapse_strong(evolved, theta, Ta, Gamma)
    
    lobes_after = dominant_angular_mode(collapsed, theta)
    t = np.arange(0, 6.0, 1/160.0)
    base = float(np.tanh(collapsed.mean()))
    phi = base * np.sin(Ki * t)
    dt = 1/160.0
    f, snr, xf, yf = detect_frequency(phi, dt)
    time_flux = phase_flux_time(phi, dt)
    bal = abs(space_flux - time_flux) / (abs(space_flux) + abs(time_flux) + 1e-12)
    verdict = bool((Ta <= 0.35) and (Gamma >= 0.75) and (lobes_after <= 2) and (snr >= 5.0) and (bal < 0.9))
    
    fp = sp = cp = None  # NEW: Initialize path for collapse plot
    if save_figs and outdir and tag:
        os.makedirs(outdir, exist_ok=True)
        
        # NEW: Enhanced Pre/Post figure with colorbars for scale.
        plt.figure(figsize=(10, 4))
        plt.subplot(1, 2, 1)
        im1 = plt.imshow(field, cmap="gray")
        plt.colorbar(im1, fraction=0.046, pad=0.04)
        plt.axis("off")
        plt.title(f"Pre (lobes≈{lobes_before})")
        
        plt.subplot(1, 2, 2)
        im2 = plt.imshow(collapsed, cmap="gray")
        plt.colorbar(im2, fraction=0.046, pad=0.04)
        plt.axis("off")
        plt.title(f"Post (lobes≈{lobes_after})")
        
        plt.tight_layout()
        fp = os.path.join(outdir, f"{tag}_pre_post.png")
        plt.savefig(fp)
        plt.close()
        
        # Spectrum plot (unchanged)
        plt.figure(figsize=(6, 4))
        plt.plot(xf, yf)
        plt.xlabel("Frequency")
        plt.ylabel("Amplitude")
        plt.title(f"Ki spectrum (SNR={snr:.1f}, peak={f:.2f})")
        plt.tight_layout()
        sp = os.path.join(outdir, f"{tag}_spectrum.png")
        plt.savefig(sp)
        plt.close()

        # NEW: Plot showing the location and magnitude of the collapse.
        plt.figure(figsize=(5.5, 4))
        im_collapse = plt.imshow(collapse_map, cmap="inferno")
        plt.colorbar(im_collapse, label="Magnitude of Change")
        plt.title("Collapse Locus")
        plt.axis("off")
        plt.tight_layout()
        cp = os.path.join(outdir, f"{tag}_collapse_map.png")
        plt.savefig(cp)
        plt.close()

    return {
        "lobes_before": int(lobes_before), "lobes_after": int(lobes_after), 
        "gate": float(gate), "beat_peak": float(f), "beat_SNR": float(snr),
        "phase_balance_error": float(bal), "verdict_pass": verdict, 
        "field_png": fp or "", "spectrum_png": sp or "", "collapse_png": cp or "" # NEW: Return collapse plot path
    }

# --- Main Execution Block ---
if __name__ == "__main__":
    # NEW: Set up command-line argument parsing.
    parser = argparse.ArgumentParser(description="Run the HCS dimensional collapse simulation on a single image.")
    parser.add_argument("image_path", type=str, help="Path to the input image file.")
    args = parser.parse_args()

    # --- Simulation Parameters ---
    kappas = [0.2, 0.9]
    params = [(0.90, 0.40, 2 * np.pi * 0.6), (0.28, 0.88, 2 * np.pi * 0.8)]  # (Ta, Gamma, Ki) for control, corridor
    rows = []
    base_dir = "simulation_gallery"
    os.makedirs(base_dir, exist_ok=True)

    # NEW: Use the single image path provided by the user.
    pth = args.image_path
    if not os.path.exists(pth):
        print(f"❌ Error: Image path not found at '{pth}'")
        exit()
    
    print(f"Processing image: {pth}")
    slug = os.path.splitext(os.path.basename(pth))[0]
    field = ingest_field(pth, size=192)
    out_dir = os.path.join(base_dir, slug)
    os.makedirs(out_dir, exist_ok=True)

    for i, k in enumerate(kappas):
        for j, (Ta, Gamma, Ki) in enumerate(params):
            param_type = 'ctrl' if j == 0 else 'corr'
            tag = f"{slug}_k{k:.2f}_{param_type}"
            # save_figs is only true for the 'corr' case (j==1)
            res = run_one(field, k, Ta, Gamma, Ki, outdir=out_dir, tag=tag, save_figs=(j == 1))
            
            # NEW: Cleanly prepare data for the DataFrame.
            row_data = {
                "image": slug, "kappa": k, "param_type": param_type,
                "Ta": Ta, "Gamma": Gamma, "Ki_freq": Ki / (2 * np.pi),
                **res
            }
            # Rename keys for clarity in the final CSV
            row_data["prepost_png"] = row_data.pop("field_png")
            row_data["spectrum_png"] = row_data.pop("spectrum_png")
            row_data["collapse_locus_png"] = row_data.pop("collapse_png")
            rows.append(row_data)

    atlas = pd.DataFrame(rows)
    # NEW: Make output filenames unique to the input image.
    csv_path = f"atlas_{slug}.csv"
    atlas.to_csv(csv_path, index=False)

    # --- Aggregate Plots (now specific to the input image) ---
    plt.figure(figsize=(6, 4))
    for k in kappas:
        sel = atlas[atlas["kappa"] == k]
        pr = float(np.mean(sel["verdict_pass"])) if len(sel) > 0 else 0.0
        plt.scatter([k], [pr])
    plt.xlabel("κ (kappa)")
    plt.ylabel("Pass-rate")
    plt.title(f"Pass-rate vs κ for '{slug}'")
    plt.tight_layout()
    pass_png = f"passrate_{slug}.png"
    plt.savefig(pass_png)
    plt.close()

    plt.figure(figsize=(6, 4))
    for k in kappas:
        sel = atlas[atlas["kappa"] == k]
        avg_snr = float(np.mean(sel["beat_SNR"])) if len(sel) > 0 else 0.0
        plt.scatter([k], [avg_snr])
    plt.xlabel("κ (kappa)")
    plt.ylabel("Average Signal-to-Noise Ratio (SNR)")
    plt.title(f"Average SNR vs κ for '{slug}'")
    plt.tight_layout()
    snr_png = f"avg_snr_{slug}.png"
    plt.savefig(snr_png)
    plt.close()
    
    print("\n✅ Processing complete! Your files are ready:")
    print(f"  - Results CSV:      {csv_path}")
    print(f"  - Image Gallery:    {out_dir}")
    print(f"  - Pass-rate Plot:   {pass_png}")
    print(f"  - SNR Plot:         {snr_png}")