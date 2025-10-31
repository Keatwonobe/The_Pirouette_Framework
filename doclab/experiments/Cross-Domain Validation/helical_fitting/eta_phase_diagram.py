# eta_phase_diagram.py
# Compute and visualize sign(η) over a (V_Gamma, K_tau) grid using a PRG-style β-flow.
# Replace the formula for η with your MATH-028 flow; this file is a scaffold.

import numpy as np, argparse, os
import matplotlib.pyplot as plt

def eta_local(VG, Ktau, dK=1.0, phi=1.0, psi=0.0, kappa=0.0):
    # Toy formula: η = +1 - φ*VG + ψ*Kτ - κ*VG*Kτ
    # Set coefficients from your fitted PRG; signs matter for regimes.
    return 1.0 - phi*VG + psi*Ktau - kappa*VG*Ktau

def compute_grid(VG_min, VG_max, KT_min, KT_max, n=400, **coeffs):
    VG = np.linspace(VG_min, VG_max, n)
    KT = np.linspace(KT_min, KT_max, n)
    V, K = np.meshgrid(VG, KT)
    E = eta_local(V, K, **coeffs)
    return V, K, E

def plot_phase(V, K, E, out_png):
    # Regions: Blue (η>0), Red (η<0), White ~ 0. We'll encode via thresholds on E.
    plt.figure(figsize=(6,5))
    # Single image per policy; use imshow with E for sign visualization
    plt.imshow(E, extent=[V.min(), V.max(), K.min(), K.max()], origin="lower")
    plt.colorbar()
    plt.xlabel("V_Gamma (noise/pressure)")
    plt.ylabel("K_tau (coherence density)")
    plt.title("η phase diagram (sign and magnitude)")
    plt.tight_layout()
    plt.savefig(out_png, dpi=150)
    plt.close()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--VG_min", type=float, default=0.0)
    ap.add_argument("--VG_max", type=float, default=2.0)
    ap.add_argument("--KT_min", type=float, default=0.0)
    ap.add_argument("--KT_max", type=float, default=2.0)
    ap.add_argument("--n", type=int, default=300)
    ap.add_argument("--phi", type=float, default=0.8)
    ap.add_argument("--psi", type=float, default=0.3)
    ap.add_argument("--kappa", type=float, default=0.2)
    ap.add_argument("--out", default="./eta_phase.png")
    args = ap.parse_args()

    V, K, E = compute_grid(args.VG_min, args.VG_max, args.KT_min, args.KT_max, n=args.n,
                           phi=args.phi, psi=args.psi, kappa=args.kappa)
    plot_phase(V, K, E, args.out)

if __name__ == "__main__":
    main()
