import argparse
import json
import numpy as np
from astropy.io import fits
from pathlib import Path

EPS = 1e-12  # to prevent div-by-zero

def load_fits_image(path, hdu=0):
    with fits.open(path) as hdul:
        data = hdul[hdu].data.astype(np.float64)
    # squeeze in case it's 1xNxM
    return np.squeeze(data)

def central_grads(arr, pixscale=1.0):
    # simple centered diffs
    gy, gx = np.gradient(arr, pixscale)
    return gx, gy

def curl_z_from_scalar(arr, pixscale=1.0):
    # In 2D we can treat the scalar as a potential-like quantity
    # and define a pseudo-vector A = (0, 0, arr)
    # curl A = (d/dy arr, -d/dx arr, 0)
    gy, gx = np.gradient(arr, pixscale)
    curl_abs = np.sqrt(gy**2 + gx**2)  # magnitude in plane
    return curl_abs

def compute_shell_mask(grad_abs, curl_abs, frac=0.2):
    ratio = curl_abs / (grad_abs + EPS)
    flat_idx = np.argsort(ratio.ravel())[::-1]
    k = int(len(flat_idx) * frac)
    shell = np.zeros_like(ratio, dtype=bool)
    shell.ravel()[flat_idx[:k]] = True
    return shell, ratio

def analyze_image(img, frac=0.2, pixscale=1.0):
    gx, gy = central_grads(img, pixscale)
    grad_abs = np.sqrt(gx**2 + gy**2)
    curl_abs = curl_z_from_scalar(img, pixscale)

    shell_mask, ratio = compute_shell_mask(grad_abs, curl_abs, frac=frac)

    theta_shell = np.mean((curl_abs**2)[shell_mask])
    grad_shell = np.mean((grad_abs**2)[shell_mask])

    k_gamma = theta_shell / (grad_shell + EPS)

    return {
        "theta_shell": float(theta_shell),
        "grad_shell": float(grad_shell),
        "k_gamma": float(k_gamma),
        "frac": float(frac),
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fits", required=True, help="input FITS cutout (HI or optical)")
    ap.add_argument("--hdu", type=int, default=0)
    ap.add_argument("--meta", help="JSON with galaxy metadata (distance, vrot, rd_kpc, name)")
    ap.add_argument("--frac", type=float, default=0.2)
    ap.add_argument("--pixscale", type=float, default=1.0, help="arcsec/pixel or km/s/pixel; for ratios only, value not critical")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    img = load_fits_image(args.fits, hdu=args.hdu)
    res = analyze_image(img, frac=args.frac, pixscale=args.pixscale)

    meta = {}
    if args.meta:
        with open(args.meta, "r") as f:
            meta = json.load(f)

    # if we have disk scale + rotation we can make dimensionless ktilde
    if "rd_kpc" in meta and "vrot_kms" in meta:
        # rough orbital period in seconds
        R_m = meta["rd_kpc"] * 3.086e19  # kpc → m
        v_ms = meta["vrot_kms"] * 1e3
        Ta_sec = 2.0 * np.pi * R_m / (v_ms + EPS)
        # normalize k_gamma by this timescale
        res["k_gamma_tilde"] = res["k_gamma"] * Ta_sec
    res.update(meta)

    outpath = args.out or (Path(args.fits).stem + f"_gamma_frac{args.frac:.2f}.json")
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2)
    print(f"[ok] wrote {outpath}")

if __name__ == "__main__":
    main()
