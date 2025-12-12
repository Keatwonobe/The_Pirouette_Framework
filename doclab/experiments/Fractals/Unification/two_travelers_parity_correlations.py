# two_travelers_parity_scan.py

import numpy as np
import matplotlib.pyplot as plt

from fractal_fingerprint2D import fractal_fingerprint

DATACUBE_PATH = "substrate_helical_datacube.npz"

def load_cube(path=DATACUBE_PATH):
    data = np.load(path)
    # Same keys as scan_k_for_matches_2.py
    T_sub = data["T_sub"]        # shape: (nk, nlat, nlon)
    k_values = data["k_values"]  # shape: (nk,)
    return T_sub, k_values

def normalize(field):
    f = field.astype(float)
    f = f - np.mean(f)
    s = np.std(f)
    if s > 0:
        f /= s
    return f

def corr(a, b):
    a = normalize(a).ravel()
    b = normalize(b).ravel()
    return float(np.dot(a, b) / (len(a) + 1e-12))

def find_index_for_k(k_values, k_target):
    return int(np.argmin(np.abs(k_values - k_target)))

def main():
    T_sub, k_values = load_cube()
    nk = len(k_values)

    # Build a mapping from k to index for quick lookup
    k_arr = np.array(k_values)
    k_to_idx = dict(zip(k_arr, range(len(k_arr)))) # A standard way to map array elements to their indices

    # For each k <= 0, find nearest +k partner and compute symmetry metrics
    pair_ks = []
    corr_raw = []
    corr_flip_lon = []
    corr_rot180 = []
    D_neg = []
    A_neg = []
    D_pos = []
    A_pos = []

    for i, k_neg in enumerate(k_arr):
        if k_neg > 0:
            continue
        k_pos_target = -k_neg
        j = int(np.argmin(np.abs(k_arr - k_pos_target)))
        k_pos = float(k_arr[j])

        slice_neg = T_sub[i]
        slice_pos = T_sub[j]

        # raw correlation
        r_raw = corr(slice_neg, slice_pos)

        # longitude flip of pos
        slice_pos_flip_lon = slice_pos[:, ::-1]
        r_flip = corr(slice_neg, slice_pos_flip_lon)

        # 180° rotation (lon+lat flip)
        slice_pos_rot = slice_pos[::-1, ::-1]
        r_rot = corr(slice_neg, slice_pos_rot)

        # fractal fingerprints
        metrics_neg = fractal_fingerprint(slice_neg)
        Dn = metrics_neg["box_dim"]
        An = metrics_neg["gradient_anisotropy"]

        metrics_pos = fractal_fingerprint(slice_pos)
        Dp = metrics_pos["box_dim"]
        Ap = metrics_pos["gradient_anisotropy"]

        pair_ks.append((k_neg, k_pos))
        corr_raw.append(r_raw)
        corr_flip_lon.append(r_flip)
        corr_rot180.append(r_rot)
        D_neg.append(Dn)
        A_neg.append(An)
        D_pos.append(Dp)
        A_pos.append(Ap)

    pair_ks = np.array(pair_ks)
    k_neg_list = pair_ks[:, 0]
    k_pos_list = pair_ks[:, 1]
    corr_raw = np.array(corr_raw)
    corr_flip_lon = np.array(corr_flip_lon)
    corr_rot180 = np.array(corr_rot180)
    D_neg = np.array(D_neg)
    A_neg = np.array(A_neg)
    D_pos = np.array(D_pos)
    A_pos = np.array(A_pos)

    # === 1) Plot correlation vs k (negative branch) ===
    plt.figure(figsize=(10, 5))
    plt.plot(k_neg_list, corr_raw, label="raw corr(k-, k+)")
    plt.plot(k_neg_list, corr_flip_lon, label="corr(k-, flip_lon(k+))")
    plt.plot(k_neg_list, corr_rot180, label="corr(k-, rot180(k+))")
    plt.axvline(-0.492, color="k", linestyle="--", alpha=0.4,
                label="candidate -0.492")
    plt.xlabel("k (negative branch)")
    plt.ylabel("Correlation")
    plt.title("Two-Traveler Parity Scan: CMB substrate")
    plt.legend()
    plt.tight_layout()
    plt.savefig("two_travelers_parity_correlations.png", dpi=200)

    # === 2) Fingerprint differences (how 'complementary' are they?) ===
    # We'll look at |D_neg - D_pos| and |A_neg - A_pos|
    dD = np.abs(D_neg - D_pos)
    dA = np.abs(A_neg - A_pos)

    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(k_neg_list, dD, label="|D(-k) - D(+k)|", color="C0")
    ax1.set_xlabel("k (negative branch)")
    ax1.set_ylabel("Δ fractal dimension", color="C0")
    ax1.tick_params(axis="y", labelcolor="C0")

    ax2 = ax1.twinx()
    ax2.plot(k_neg_list, dA, label="|A(-k) - A(+k)|", color="C1")
    ax2.set_ylabel("Δ anisotropy", color="C1")
    ax2.tick_params(axis="y", labelcolor="C1")

    ax1.axvline(-0.492, color="k", linestyle="--", alpha=0.4)

    plt.title("Two-Traveler Fractal Complementarity")
    fig.tight_layout()
    plt.savefig("two_travelers_parity_fingerprints.png", dpi=200)

    # === 3) Explicit metrics for the (-0.492, +0.517) candidate pair ===

    k_neg_star = -0.492
    k_pos_star = 0.517

    i_star = find_index_for_k(k_arr, k_neg_star)
    j_star = find_index_for_k(k_arr, k_pos_star)

    s_neg = T_sub[i_star]
    s_pos = T_sub[j_star]

    r_raw_star = corr(s_neg, s_pos)
    r_flip_star = corr(s_neg, s_pos[:, ::-1])
    r_rot_star = corr(s_neg, s_pos[::-1, ::-1])

    metrics_neg_star = fractal_fingerprint(s_neg)
    Dn_star = metrics_neg_star["box_dim"]
    An_star = metrics_neg_star["gradient_anisotropy"]

    metrics_pos_star = fractal_fingerprint(s_pos)
    Dp_star = metrics_pos_star["box_dim"]
    Ap_star = metrics_pos_star["gradient_anisotropy"]

    print("=== Two-Travelers Candidate Pair ===")
    print(f"k_neg ≈ {k_arr[i_star]:.3f}, k_pos ≈ {k_arr[j_star]:.3f}")
    print(f"Raw correlation:          {r_raw_star:.4f}")
    print(f"Lon-flip correlation:     {r_flip_star:.4f}")
    print(f"Rot-180 correlation:      {r_rot_star:.4f}")
    print()
    print(f"Slice -k: D={Dn_star:.3f}, anis={An_star:.3f}")
    print(f"Slice +k: D={Dp_star:.3f}, anis={Ap_star:.3f}")
    print(f"ΔD={abs(Dn_star-Dp_star):.3f}, Δanis={abs(An_star-Ap_star):.3f}")

    # Optional: save a side-by-side comparison image
    fig2, axes = plt.subplots(1, 2, figsize=(12, 4), sharex=True, sharey=True)
    im0 = axes[0].imshow(s_neg, origin="lower", cmap="inferno")
    axes[0].set_title(f"Slice k={k_arr[i_star]:.3f}")
    im1 = axes[1].imshow(s_pos, origin="lower", cmap="inferno")
    axes[1].set_title(f"Slice k={k_arr[j_star]:.3f}")
    fig2.colorbar(im1, ax=axes.ravel().tolist())
    fig2.subplots_adjust()
    plt.savefig("two_travelers_candidate_slices.png", dpi=200)

if __name__ == "__main__":
    main()
