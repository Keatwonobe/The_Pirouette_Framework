# helical_scanner_5B_datacube.py

import numpy as np
import os
from helical_scanner_5 import (
    FITS_PATH, LMAX, REMOVE_BAND,
    load_cmb_and_alms, build_mode_maps, synthesize_helical,
    K_MIN, K_MAX, N_K, K_VALUES,
    N_TH_SYN, N_PH_SYN
)

OUT_NPZ = "substrate_helical_datacube.npz"



def main():
    print("=== Scanner 5B : Building T_sub(k, lat, lon) datacube ===")

    alms = load_cmb_and_alms(FITS_PATH, LMAX)
    modes, TH, PH = build_mode_maps(alms, LMAX, remove_band=REMOVE_BAND)

    n_k   = len(K_VALUES)
    n_lat = N_TH_SYN
    n_lon = N_PH_SYN

    cube = np.zeros((n_k, n_lat, n_lon), dtype=np.float32)

    for i, k in enumerate(K_VALUES):
        print(f"[>] k = {k:.3f}  ({i+1}/{n_k})")
        T_k = synthesize_helical(modes, PH, k_twist=k)
        T_k -= T_k.mean()
        cube[i] = T_k.astype(np.float32)

    np.savez_compressed(
        OUT_NPZ,
        T_sub=cube,
        k_values=K_VALUES,
        theta=np.linspace(0, np.pi, n_lat),
        phi=np.linspace(-np.pi, np.pi, n_lon, endpoint=False)
    )
    print(f"✅ Saved datacube to {OUT_NPZ}")

if __name__ == "__main__":
    main()
