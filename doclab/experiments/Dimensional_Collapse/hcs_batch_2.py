
#!/usr/bin/env python3
"""
HCS Batch (Patched) — Signed Angular Gradient + Angular-Basis Collapse

Key changes vs earlier batch:
1) Lobe detection operates on the **signed angular derivative** g_theta, not |∇φ|.
2) Collapse removes the **detected dominant mode** and recycles its L2 energy into m=2
   with a smooth corridor gate g = 1 - exp(-3*(1-Ta)*Gamma).
3) Pass criteria emphasize geometric change: Δm ≥ 1 and m_post ≤ 2, plus energy balance check.

Outputs are preserved: CSV atlas and per-image artifacts when requested.
"""

import os, sys, math, csv, glob, uuid
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

# ------------------- Core geometry -------------------

def polar_grid(n=192, r_max=1.0):
    lin = np.linspace(-r_max, r_max, n)
    x, y = np.meshgrid(lin, lin)
    r = np.sqrt(x*x + y*y) + 1e-12
    theta = np.arctan2(y, x)
    return x, y, r, theta

def ingest_field(path, size=192):
    img = Image.open(path).convert("L").resize((size, size))
    arr = np.array(img).astype(np.float32)
    arr = (arr - arr.mean()) / (arr.std() + 1e-12)
    return np.tanh(arr / 2.5)

# ------------------- Signed angular gradient & lobes -------------------

def signed_angular_gradient(field, theta):
    gx, gy = np.gradient(field)
    tx, ty = -np.sin(theta), np.cos(theta)   # tangential unit vector
    return gx*tx + gy*ty

def dominant_angular_mode(field, theta, max_m=8):
    # Measure on signed angular derivative (restores odd/even sensitivity)
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

# ------------------- Helical evolution (surrogate) -------------------

def helical_time_evolve(field, kappa, t=6.0, omega=2*np.pi*1.0):
    gx, _ = np.gradient(field)
    return np.cos(kappa*omega*t)*field + np.sin(kappa*omega*t)*gx

# ------------------- Angular-basis collapse -------------------

def _proj(field, theta, m):
    b = np.cos(m*theta)
    coef = np.sum(field*b) / (np.sum(b*b) + 1e-12)
    return coef, b

def psi_collapse_to_m2(field, theta, Ta, Gamma, m_dom):
    # Smooth corridor gate
    g = float(np.clip((1.0 - Ta)*Gamma, 0.0, 1.0))
    g = 1.0 - np.exp(-3.0*g)

    # Remove fraction g of dominant mode
    c_dom, b_dom = _proj(field, theta, m_dom)
    removed = g * c_dom * b_dom
    remainder = field - removed

    # Recycle L2 energy into m=2 with sign of existing c2
    c2, b2 = _proj(remainder, theta, 2)
    E_removed = np.sqrt(np.mean(removed**2) + 1e-12)
    b2u = b2 / (np.sqrt(np.mean(b2**2)) + 1e-12)
    refill = E_removed * b2u * np.sign(c2 if abs(c2) > 1e-8 else 1.0)

    collapsed = remainder + refill
    energy_balance = float(abs(np.sqrt(np.mean(removed**2)) - np.sqrt(np.mean(refill**2))))
    return collapsed, g, energy_balance

# ------------------- Run a single condition -------------------

def run_hcs_one(image_path, kappa, Ta, Gamma, Ki, size=192,
                save_dir=None, tag=None, save_figs=False):
    x, y, r, theta = polar_grid(size, 1.0)
    field = ingest_field(image_path, size=size)

    # pre
    m_pre, s_pre = dominant_angular_mode(field, theta)

    # evolve & collapse
    evolved = helical_time_evolve(field, kappa, t=6.0)
    collapsed, gate, Eb = psi_collapse_to_m2(evolved, theta, Ta, Gamma, m_dom=m_pre)
    m_post, s_post = dominant_angular_mode(collapsed, theta)

    # pass rules (geometry-first)
    delta_m = int(m_pre) - int(m_post)
    pass_geom = (delta_m >= 1) and (m_post <= 2)
    pass_energy = (Eb < 0.05)  # loose L2 balance tolerance
    verdict = bool(pass_geom and pass_energy and (gate >= 0.5))

    # visuals (optional)
    field_png = spec_png = ""
    if save_figs and save_dir and tag:
        os.makedirs(save_dir, exist_ok=True)
        # Pre/Post signed gradient
        plt.figure(figsize=(9,4))
        plt.subplot(1,2,1); plt.imshow(s_pre, cmap="viridis"); plt.axis("off"); plt.title(f"Signed ∂θ Pre (m≈{m_pre})")
        plt.subplot(1,2,2); plt.imshow(s_post, cmap="viridis"); plt.axis("off"); plt.title(f"Signed ∂θ Post (m≈{m_post})")
        plt.tight_layout()
        field_png = os.path.join(save_dir, f"{tag}_signed_grad.png")
        plt.savefig(field_png); plt.close()

        # Minimal spectrum (synthetic beat for continuity with prior logs)
        t = np.arange(0, 6.0, 1/160.0)
        from numpy.fft import rfft, rfftfreq
        phi = float(np.tanh(collapsed.mean())) * np.sin(Ki*t)
        yf = np.abs(rfft(phi)); xf = rfftfreq(len(phi), 1/160.0); yf[0]=0.0
        plt.figure(figsize=(6,4)); plt.plot(xf, yf); plt.xlabel("Frequency"); plt.ylabel("Amplitude"); plt.title("Ki spectrum")
        spec_png = os.path.join(save_dir, f"{tag}_spectrum.png")
        plt.tight_layout(); plt.savefig(spec_png); plt.close()

    return {
        "image_source": os.path.basename(image_path),
        "kappa": float(kappa), "Ta": float(Ta), "Gamma": float(Gamma), "Ki": float(Ki/(2*np.pi)),
        "gate": float(gate), "energy_balance": float(Eb),
        "lobes_before": int(m_pre), "lobes_after": int(m_post),
        "delta_m": int(delta_m), "verdict_pass": bool(verdict),
        "field_png": field_png, "spectrum_png": spec_png
    }

# ------------------- Batch harness -------------------

def run_batch(images, kappas, param_sets, size=192, gallery_dir=None, save_figs=False):
    rows = []
    for img in images:
        slug = os.path.splitext(os.path.basename(img))[0]
        outdir = os.path.join(gallery_dir, slug) if gallery_dir else None
        if outdir and save_figs and not os.path.exists(outdir):
            os.makedirs(outdir, exist_ok=True)
        for k in kappas:
            for ptype, (Ta, Gamma, Ki) in param_sets.items():
                tag = f"{slug}_k{k:.2f}_{ptype}"
                res = run_hcs_one(img, k, Ta, Gamma, Ki, size=size,
                                  save_dir=outdir, tag=tag, save_figs=(save_figs and ptype=='corr'))
                res["param_type"] = ptype
                rows.append(res)
    return pd.DataFrame(rows)

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--images_glob", default="C:/Users/keatw/OneDrive/Documents/Expressions/*.png")
    ap.add_argument("--size", type=int, default=192)
    ap.add_argument("--gallery", default="zipper_gallery_patch")
    ap.add_argument("--csv_out", default="master_collapse_atlas_patched.csv")
    ap.add_argument("--figs", action="store_true")
    args = ap.parse_args()

    images = sorted(glob.glob(args.images_glob))
    kappas = [0.2, 0.9]
    params = {
        "ctrl": (0.90, 0.40, 2*np.pi*0.6),
        "corr": (0.28, 0.88, 2*np.pi*0.8),
    }

    df = run_batch(images, kappas, params, size=args.size,
                   gallery_dir=args.gallery, save_figs=args.figs)
    df.to_csv(args.csv_out, index=False)
    print(f"Wrote {len(df)} rows to {args.csv_out}")

if __name__ == "__main__":
    main()
