# scan_k_for_matches.py

import numpy as np
import os
from fractal_fingerprint2D import fractal_fingerprint
from PIL import Image

# Config
DATACUBE_FILE = "substrate_helical_datacube.npz"
TARGET_FILE   = "proton_triport.png"

def generate_synthetic_target(filename):
    """Generates a dummy fractal (Sierpinski-like) if the file is missing."""
    print(f"[!] Target '{filename}' not found. Generating synthetic test pattern...")
    
    n = 512
    y, x = np.ogrid[:n, :n]
    # A simple fractal logic: XOR pattern
    pattern = (x ^ y) % 17 < 5
    
    # Save it so we have it for next time
    img = Image.fromarray((pattern * 255).astype(np.uint8))
    img.save(filename)
    print(f"    Saved synthetic target to {filename}")
    return np.array(pattern, dtype=float)

def main():
    # 1. Load the datacube
    if not os.path.exists(DATACUBE_FILE):
        print(f"Error: {DATACUBE_FILE} missing. Run helical_scanner_5B_datacube.py first.")
        return

    print(f"[*] Loading {DATACUBE_FILE}...")
    DATA = np.load(DATACUBE_FILE)
    cube      = DATA["T_sub"]      # (n_k, n_lat, n_lon)
    k_values  = DATA["k_values"]

    # 2. Compute fingerprints for the substrate volume (Scan k)
    print(f"[*] Scanning {len(k_values)} k-slices for fractal signatures...")
    fp_k = []
    
    for i, k in enumerate(k_values):
        field = cube[i]
        fp = fractal_fingerprint(field)
        fp["k"] = float(k)
        fp_k.append(fp)
        # Print every 10th or so to keep log clean, or all if short
        # Printing abbreviated log to save console space
        # print(f"[k={k:.3f}] D={fp['box_dim']:.3f}, ani={fp['gradient_anisotropy']:.3f}")

    # 3. Load or Generate Target Fingerprint
    if os.path.exists(TARGET_FILE):
        print(f"[*] Loading target image: {TARGET_FILE}")
        img_data = np.array(Image.open(TARGET_FILE).convert("L"), dtype=float)
    else:
        img_data = generate_synthetic_target(TARGET_FILE)

    proton_fp = fractal_fingerprint(img_data)
    print(f"[*] Target Fingerprint: D={proton_fp['box_dim']:.3f}, Anisotropy={proton_fp['gradient_anisotropy']:.3f}")

    # 4. Define Distance Metric
    def fp_distance(a, b, keys=("box_dim","gradient_anisotropy","ps_h_power","ps_v_power","ps_d_power")):
        s = 0.0
        weights = {"box_dim": 10.0, "gradient_anisotropy": 1.0, "ps_h_power": 5.0} # Weighting D higher
        for key in keys:
            va = a[key]; vb = b[key]
            if np.isnan(va) or np.isnan(vb):
                continue
            w = weights.get(key, 1.0)
            s += w * (va - vb)**2
        return np.sqrt(s)

    # 5. Find Matches
    distances = []
    for fp in fp_k:
        distances.append((fp["k"], fp_distance(fp, proton_fp)))

    distances = sorted(distances, key=lambda x: x[1])
    
    print("\n=== TOP 10 MATCHES TO TARGET ===")
    print(f"{'Twist (k)':<10} | {'Distance':<10} | {'Dim (D)':<10} | {'Anisotropy'}")
    print("-" * 50)
    for k_val, dist in distances[:10]:
        # retrieve original stats for display
        original = next(f for f in fp_k if f["k"] == k_val)
        print(f"{k_val:<10.3f} | {dist:<10.4f} | {original['box_dim']:<10.3f} | {original['gradient_anisotropy']:.3f}")

if __name__ == "__main__":
    main()