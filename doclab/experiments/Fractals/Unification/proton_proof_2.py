"""
Raw twist-mode scan: sample all outputs of error_128(τ) and
plot them individually so we can see which mode actually
has structure near the suspected proton region.

Usage:
    python twist_raw_scan.py
"""

import numpy as np
import matplotlib.pyplot as plt
from twist_unit import error_128   # assumed signature: (E, G, T, R)

# --- scan range (same window as before for continuity) ---
TAU_GUESS = 3.8
WINDOW    = 2.0
N_SAMPLES = 2400

def sample_raw_modes(t_min, t_max, n_samples):
    taus = np.linspace(t_min, t_max, n_samples)
    E = np.empty_like(taus)
    G = np.empty_like(taus)
    T = np.empty_like(taus)
    R = np.empty_like(taus)

    for i, t in enumerate(taus):
        e, g, tt, rr = error_128(float(t))
        E[i] = float(e)
        G[i] = float(g)
        T[i] = float(tt)
        R[i] = float(rr)

    return taus, E, G, T, R

def main():
    t_min = TAU_GUESS - WINDOW
    t_max = TAU_GUESS + WINDOW

    print(f"[#] Sampling raw modes on τ ∈ [{t_min}, {t_max}]")
    taus, E, G, T, R = sample_raw_modes(t_min, t_max, N_SAMPLES)

    # --- plot each mode separately ---
    fig, axs = plt.subplots(4, 1, figsize=(9, 10), sharex=True)
    modes = [E, G, T, R]
    labels = [r"$E_{1:2:8}$ (combo)",
              r"$G$ (mode 1)",
              r"$T$ (mode 2)",
              r"$R$ (mode 3)"]

    for ax, arr, lab in zip(axs, modes, labels):
        ax.plot(taus, arr, alpha=0.9)
        ax.set_ylabel(lab)
        ax.grid(True, alpha=0.3)

    axs[-1].set_xlabel(r"Twist $\tau$")
    fig.suptitle("Raw twist-unit modes vs τ", y=0.95)
    plt.tight_layout()
    plt.savefig("twist_raw_modes.png", dpi=200)
    print("[+] Saved plot: twist_raw_modes.png")

    # --- quick min / span report for each mode ---
    for name, arr in zip(["E", "G", "T", "R"], modes):
        amin = float(arr.min())
        amax = float(arr.max())
        print(f"[Δ] {name}: min={amin:.6e}, max={amax:.6e}, span={amax-amin:.6e}")

if __name__ == "__main__":
    main()
