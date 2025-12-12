# scan_k_for_matches.py  (v2 – uses Wada prism as target)

import os
import numpy as np
from fractal_fingerprint2D import fractal_fingerprint
from PIL import Image

# NEW: pull in the fast C3-symmetry Wada solver
from wada_prism_solver import solve_folded_universe


# ---------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------
DATACUBE_FILE = "substrate_helical_datacube.npz"

# if you still want the old behaviour, set this False
USE_WADA_TARGET = True

# if USE_WADA_TARGET == False, this filename will be used / generated
FALLBACK_TARGET_FILE = "proton_triport.png"


# ---------------------------------------------------------------------
# Target generators
# ---------------------------------------------------------------------
def generate_synthetic_target(filename):
    """
    Old fallback: simple XOR-style fractal pattern written to disk
    so you can still run without the Wada solver if you want.
    """
    print(f"[!] Target '{filename}' not found. Generating synthetic test pattern...")

    n = 512
    y, x = np.ogrid[:n, :n]
    pattern = (x ^ y) % 17 < 5

    img = Image.fromarray((pattern * 255).astype(np.uint8))
    img.save(filename)
    print(f"    Saved synthetic target to {filename}")
    return np.array(pattern, dtype=float)


def generate_wada_target(res=2048, zoom=2.0, save_png=None):
    """
    Uses the prism-optimized Wada solver as the comparison target.

    Returns:
        field : 2D float array with basin IDs turned into a scalar field.
    """
    print(f"[*] Generating Wada prism target (res={res}, zoom={zoom})...")
    # this calls the numba-accelerated kernel; first call will JIT-compile
    basin_map = solve_folded_universe(res, zoom)

    # basin_map is int8 in {0,1,2,3}.  Turn into a float field.
    # You can change this encoding if you want to emphasize boundaries instead.
    field = basin_map.astype(float)

    # Optional debug image
    if save_png is not None:
        from matplotlib import pyplot as plt
        from matplotlib.colors import ListedColormap

        cmap = ListedColormap(['black', '#00cccc', '#8800ff', '#ffaa00'])
        plt.figure(figsize=(6, 6), facecolor='black')
        plt.imshow(field, origin='lower', cmap=cmap, interpolation='nearest')
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(save_png, dpi=150)
        plt.close()
        print(f"    Saved Wada preview to {save_png}")

    return field


# ---------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------
def main():
    # 1. Load the datacube
    if not os.path.exists(DATACUBE_FILE):
        print(f"Error: {DATACUBE_FILE} missing. Run helical_scanner_5B_datacube.py first.")
        return

    print(f"[*] Loading {DATACUBE_FILE}...")
    DATA = np.load(DATACUBE_FILE)
    cube = DATA["T_sub"]          # shape: (n_k, n_lat, n_lon)
    k_values = DATA["k_values"]

    # 2. Fingerprints for each k-slice
    print(f"[*] Scanning {len(k_values)} k-slices for fractal signatures...")
    fp_k = []

    for i, k in enumerate(k_values):
        field = cube[i]
        fp = fractal_fingerprint(field)
        fp["k"] = float(k)
        fp_k.append(fp)
        print(f"[k={k:6.3f}] D={fp['box_dim']:.3f}, ani={fp['gradient_anisotropy']:.3f}")

    # 3. Build target fingerprint
    if USE_WADA_TARGET:
        # New: Wada prism as target
        target_field = generate_wada_target(
            res=2048,     # bump up/down as your patience / GPU allows
            zoom=2.0,
            save_png="wada_target_preview.png"
        )
        proton_fp = fractal_fingerprint(target_field)
        print(
            f"[*] Wada Target Fingerprint: "
            f"D={proton_fp['box_dim']:.3f}, "
            f"Anisotropy={proton_fp['gradient_anisotropy']:.3f}"
        )
    else:
        # Old behaviour: load an image from disk (or synthesize)
        if os.path.exists(FALLBACK_TARGET_FILE):
            print(f"[*] Loading target image: {FALLBACK_TARGET_FILE}")
            img_data = np.array(Image.open(FALLBACK_TARGET_FILE).convert("L"), dtype=float)
        else:
            img_data = generate_synthetic_target(FALLBACK_TARGET_FILE)

        proton_fp = fractal_fingerprint(img_data)
        print(
            f"[*] Image Target Fingerprint: "
            f"D={proton_fp['box_dim']:.3f}, "
            f"Anisotropy={proton_fp['gradient_anisotropy']:.3f}"
        )

    # 4. Distance metric between fingerprints
    def fp_distance(a, b,
                    keys=("box_dim", "gradient_anisotropy",
                          "ps_h_power", "ps_v_power", "ps_d_power")):
        s = 0.0
        # Weight box dimension strongly; tweak as needed
        weights = {
            "box_dim": 10.0,
            "gradient_anisotropy": 1.0,
            "ps_h_power": 5.0,
        }
        for key in keys:
            va = a[key]
            vb = b[key]
            if np.isnan(va) or np.isnan(vb):
                continue
            w = weights.get(key, 1.0)
            s += w * (va - vb) ** 2
        return np.sqrt(s)

    # 5. Compare all k-slices to the target
    distances = []
    for fp in fp_k:
        distances.append((fp["k"], fp_distance(fp, proton_fp)))

    distances.sort(key=lambda x: x[1])

    # 6. Report best matches
    print("\n=== TOP 10 MATCHES TO TARGET ===")
    print(f"{'Twist (k)':<10} | {'Distance':<10} | {'Dim (D)':<10} | {'Anisotropy'}")
    print("-" * 60)
    for k_val, dist in distances[:10]:
        original = next(f for f in fp_k if f["k"] == k_val)
        print(
            f"{k_val:<10.3f} | {dist:<10.4f} | "
            f"{original['box_dim']:<10.3f} | {original['gradient_anisotropy']:.3f}"
        )


if __name__ == "__main__":
    main()
