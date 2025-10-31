# Triaxial Resonance Probe search for the sine-family parameter map
# Author: ChatGPT (for Keaton) — standalone, reproducible
# Model: f_c(z) = alpha * sin(z) + c, scanned over c-plane; "potential" is chosen scalar per parameter
#
# How it works:
# 1) We explore the parameter plane (c = Γ + i Ta) by iterating the critical orbit z0 = π/2 for each c.
# 2) For each c we compute a scalar field S(c): either smoothed escape-time or Lyapunov exponent.
# 3) We then sweep a small equilateral triangle ("Triaxial Resonance Probe") across the lattice and
#    score each center by the standard deviation of S at the three vertices. Lower stddev = higher resonance.
# 4) We report the most resonant coordinate (argmin stddev), plus quick PNGs of the fields.
#
# Notes:
# - The sine map is entire; escape typically happens via exponential growth in Im(z).
# - For a Mandelbrot-like parameter scan, we iterate from a critical point (z0 = π/2) not z0 = 0.
# - You can switch S(c) between 'escape' (smoothed) and 'lyap' below.
#
# This script is designed to run in ~tens of seconds at the default resolution.
# You can safely increase resolution and iterations once you're happy with the behavior.

import numpy as np
import matplotlib.pyplot as plt
from math import pi
from dataclasses import dataclass
import cmath
import time

# ----------------------------- Config ---------------------------------

@dataclass
class Config:
    alpha: float = 4.0 * np.pi / 3.0  # K_motion
    # Parameter plane bounds (c = Γ + i Ta)
    re_min: float = -3.0
    re_max: float =  3.0
    im_min: float = -3.0
    im_max: float =  3.0
    # Resolution
    width: int  = 640
    height: int = 480
    # Iteration and escape
    max_iter: int = 350
    escape_radius: float = 50.0
    # Potential choice: 'escape' or 'lyap'
    potential: str = 'lyap'
    # Probe parameters
    probe_side: float = 0.01  # side length of equilateral triangle in complex-plane units
    # random small epsilon to avoid coincident sampling
    eps: float = 1e-12
    # smoothing constant for escape potential (works reasonably for entire maps)
    smooth_log_base: float = 2.0
    # Visualization
    cmap_main: str = 'viridis'
    cmap_probe: str = 'magma'


CFG = Config()

# --------------------------- Core Dynamics -----------------------------

def iterate_map(c: complex, cfg: Config):
    """
    Iterate the critical orbit z0 = pi/2 for parameter c under f_c(z) = alpha*sin(z) + c.
    Returns:
      escaped (bool), iters (int),
      smooth_escape (float), lyap_exp (float)
    """
    alpha = cfg.alpha
    z = complex(np.pi/2, 0.0)  # one of the critical points (cos z = 0)
    # For Lyapunov exponent: track average log|f'(z)| = log|alpha*cos(z)|
    # We'll compute along the actual orbit; if escape happens early, use partial average.
    sum_log_deriv = 0.0
    escaped = False
    smooth = None

    R = cfg.escape_radius
    for n in range(1, cfg.max_iter + 1):
        # derivative magnitude at current point
        deriv = alpha * cmath.cos(z)
        sum_log_deriv += np.log(abs(deriv) + 1e-16)

        # iterate
        z = alpha * cmath.sin(z) + c

        # check escape
        if abs(z) > R:
            escaped = True
            # smooth escape time (Douady-like): n + 1 - log log |z| / log 2
            try:
                smooth = n + 1 - np.log(np.log(abs(z))) / np.log(cfg.smooth_log_base)
            except Exception:
                smooth = float(n)
            break

    iters = n if escaped else cfg.max_iter
    lyap = sum_log_deriv / iters

    # For bounded points, define smooth as max_iter (a big value) to distinguish from quick escape
    if smooth is None:
        smooth = float(cfg.max_iter)

    return escaped, iters, smooth, lyap


def compute_field(cfg: Config):
    """
    Compute scalar field S(c) over the parameter grid.
    Returns:
      xs, ys (1D arrays of coordinates),
      S (2D array), escaped_mask (2D bool), lyap (2D array), smooth (2D array)
    """
    xs = np.linspace(cfg.re_min, cfg.re_max, cfg.width, dtype=np.float64)
    ys = np.linspace(cfg.im_min, cfg.im_max, cfg.height, dtype=np.float64)

    S = np.zeros((cfg.height, cfg.width), dtype=np.float64)
    lyap_field = np.zeros_like(S)
    smooth_field = np.zeros_like(S)
    escaped_mask = np.zeros_like(S, dtype=bool)

    t0 = time.time()
    for j, im in enumerate(ys):
        for i, re in enumerate(xs):
            c = complex(re, im)
            escaped, iters, smooth, lyap = iterate_map(c, cfg)
            lyap_field[j, i] = lyap
            smooth_field[j, i] = smooth
            escaped_mask[j, i] = escaped

            if cfg.potential == 'lyap':
                S[j, i] = lyap
            elif cfg.potential == 'escape':
                S[j, i] = smooth
            else:
                raise ValueError("Unknown potential type")

        # basic progress
        if (j+1) % max(1, cfg.height // 10) == 0:
            print(f"Row {j+1}/{cfg.height} computed...")

    print(f"Field computed in {time.time() - t0:.2f} s")
    return xs, ys, S, escaped_mask, lyap_field, smooth_field


# ------------------------ Triaxial Probe Metric ------------------------

def triangle_offsets(side: float):
    """
    Equilateral triangle centered at 0 with side length 'side' in complex plane.
    Returns three complex offsets at 0°, 120°, 240° (rotated about centroid).
    """
    # Build triangle in 2D, centroid at origin.
    # Side s => distance from centroid to vertex r = s / sqrt(3)
    r = side / np.sqrt(3.0)
    angles = np.deg2rad([0.0, 120.0, 240.0])
    return [r * np.exp(1j * ang) for ang in angles]


def sample_S_at_point(c_center: complex, xs, ys, S):
    """
    Bilinear sample of S at arbitrary complex coordinate c_center.
    Returns NaN if outside bounds.
    """
    re_min, re_max = xs[0], xs[-1]
    im_min, im_max = ys[0], ys[-1]
    x, y = c_center.real, c_center.imag

    if not (re_min <= x <= re_max and im_min <= y <= im_max):
        return np.nan

    # map to grid indices
    fx = (x - re_min) / (re_max - re_min) * (len(xs) - 1)
    fy = (y - im_min) / (im_max - im_min) * (len(ys) - 1)

    i0 = int(np.floor(fx))
    j0 = int(np.floor(fy))
    i1 = min(i0 + 1, len(xs) - 1)
    j1 = min(j0 + 1, len(ys) - 1)

    dx = fx - i0
    dy = fy - j0

    # bilinear interpolation
    v00 = S[j0, i0]
    v10 = S[j0, i1]
    v01 = S[j1, i0]
    v11 = S[j1, i1]
    v0 = v00 * (1 - dx) + v10 * dx
    v1 = v01 * (1 - dx) + v11 * dx
    v = v0 * (1 - dy) + v1 * dy
    return v


def resonance_sweep(xs, ys, S, cfg: Config):
    """
    Slide the triaxial probe over the grid; at each center compute stddev of S at vertices.
    Returns map of stddev and the argmin.
    """
    offs = triangle_offsets(cfg.probe_side)
    H, W = S.shape
    std_map = np.full_like(S, np.nan, dtype=np.float64)

    t0 = time.time()
    for j, im in enumerate(ys):
        for i, re in enumerate(xs):
            c0 = complex(re, im)
            vals = []
            ok = True
            for d in offs:
                sv = sample_S_at_point(c0 + d, xs, ys, S)
                if np.isnan(sv):
                    ok = False
                    break
                vals.append(sv)
            if ok:
                std_map[j, i] = np.std(vals)

        if (j+1) % max(1, len(ys)//10) == 0:
            print(f"Probe row {j+1}/{len(ys)}...")

    ij = np.unravel_index(np.nanargmin(std_map), std_map.shape)
    jmin, imin = ij
    c_best = complex(xs[imin], ys[jmin])
    best_std = std_map[jmin, imin]
    print(f"Resonance sweep in {time.time() - t0:.2f} s")
    return std_map, c_best, best_std


# ------------------------- Run & Visualize -----------------------------

def main(cfg: Config = CFG):
    xs, ys, S, escaped_mask, lyap_field, smooth_field = compute_field(cfg)
    std_map, c_best, best_std = resonance_sweep(xs, ys, S, cfg)

    print("\n=== RESULTS ===")
    print(f"alpha = {cfg.alpha:.10f}")
    print(f"Potential = {cfg.potential}")
    print(f"Best resonance (min std) at c = Γ + i Ta = {c_best.real:.9f} + i*{c_best.imag:.9f}")
    print(f"Min std = {best_std:.6e}")
    print(f"Grid: {cfg.width}x{cfg.height}, max_iter={cfg.max_iter}, probe_side={cfg.probe_side}")

    # Save images
    def save_fig(data, title, fname, cmap='viridis', vmin=None, vmax=None):
        plt.figure(figsize=(7,5), dpi=140)
        extent = [cfg.re_min, cfg.re_max, cfg.im_min, cfg.im_max]
        plt.imshow(data, origin='lower', extent=extent, aspect='auto', cmap=cmap, vmin=vmin, vmax=vmax)
        plt.colorbar(label=title)
        # mark best point
        plt.scatter([c_best.real], [c_best.imag], s=30, marker='x', linewidths=1.5, edgecolor='white', facecolor='white', label='Best resonance')
        plt.legend(loc='upper right', frameon=True)
        plt.xlabel('Γ (Re c)')
        plt.ylabel('Tₐ (Im c)')
        plt.title(title)
        plt.tight_layout()
        plt.savefig(f"/mnt/data/{fname}", bbox_inches='tight')
        plt.close()

    # Normalize std_map for visualization
    finite_std = std_map[np.isfinite(std_map)]
    vmin = np.percentile(finite_std, 1) if finite_std.size else None
    vmax = np.percentile(finite_std, 99) if finite_std.size else None

    # Visuals
    save_fig(S, f"S(c) field ({cfg.potential})", "S_field.png", cmap=cfg.cmap_main)
    save_fig(std_map, "Triaxial resonance metric (std dev ↓ = resonance ↑)", "resonance_std.png", cmap=cfg.cmap_probe, vmin=vmin, vmax=vmax)
    save_fig(lyap_field, "Lyapunov exponent field", "lyapunov_field.png", cmap='plasma')
    save_fig(smooth_field, "Smoothed escape-time field", "escape_field.png", cmap='cividis')

    print("\nSaved:")
    print("- /mnt/data/S_field.png")
    print("- /mnt/data/resonance_std.png")
    print("- /mnt/data/lyapunov_field.png")
    print("- /mnt/data/escape_field.png")

    return {
        "c_best_real": c_best.real,
        "c_best_imag": c_best.imag,
        "min_std": best_std
    }


res = main(CFG)
res
