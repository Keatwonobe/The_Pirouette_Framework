# wound_interference_demo.py
# Toy 2+1D simulation of two Ki-like defects (spin-1/2 analogs) approaching and interacting.
# Produces frames of an "echo" field and a simple constructive/destructive mask.
#
# This is a conceptual scaffold—replace the field/echo definitions with your CORE-003 formulas.

import numpy as np, os, argparse
import matplotlib.pyplot as plt

def ki_defect_field(x, y, x0, y0, t, vx=0.0, vy=0.0, core=0.2, charge=1.0):
    # Move the center linearly
    cx = x0 + vx * t
    cy = y0 + vy * t
    r2 = (x - cx)**2 + (y - cy)**2
    # Phase winds with azimuth; amplitude decays radially (toy)
    theta = np.arctan2(y - cy, x - cx)
    amp = np.exp(-r2/(2*core**2))
    # Spin-1/2-like phase with sign from "charge"
    phase = 0.5 * theta * charge
    real = amp * np.cos(phase)
    imag = amp * np.sin(phase)
    return real + 1j*imag

def echo_overlap(psi1, psi2, dt=0.05):
    # Simple temporal echo proxy: corr between psi(t) and psi(t-dt)
    # Using product with phase-conjugate as a toy.
    return (psi1 * np.conj(psi2)).real

def simulate(outdir, T=4.0, dt=0.05, N=256, L=4.0):
    os.makedirs(outdir, exist_ok=True)
    xs = np.linspace(-L, L, N)
    ys = np.linspace(-L, L, N)
    X, Y = np.meshgrid(xs, ys)

    # Two defects approach each other
    params = dict(core=0.35)
    x01, y01, vx1, vy1 = -1.3, 0.0, +0.30, 0.00
    x02, y02, vx2, vy2 = +1.3, 0.0, -0.30, 0.00

    t_grid = np.arange(0, T, dt)
    for i, t in enumerate(t_grid):
        psi1 = ki_defect_field(X, Y, x01, y01, t, vx1, vy1, **params)
        psi2 = ki_defect_field(X, Y, x02, y02, t, vx2, vy2, **params)

        # Echo tensor proxy: overlap of present with small past offset
        psi1_past = ki_defect_field(X, Y, x01, y01, t-dt, vx1, vy1, **params)
        psi2_past = ki_defect_field(X, Y, x02, y02, t-dt, vx2, vy2, **params)

        E = echo_overlap(psi1+psi2, psi1_past+psi2_past, dt=dt)

        # Constructive/destructive mask via sign of lagged autocorr
        mask = np.sign(E)  # +1 constructive, -1 destructive, 0 neutral
        constructive = (mask > 0).astype(float)
        destructive = (mask < 0).astype(float)

        # Plot (single chart per figure per policy)
        plt.figure(figsize=(5,4))
        plt.imshow(E, extent=[-L,L,-L,L], origin="lower")
        plt.colorbar()
        plt.title(f"Echo overlap (t={t:.2f})")
        plt.tight_layout()
        plt.savefig(os.path.join(outdir, f"echo_{i:04d}.png"), dpi=120)
        plt.close()

        plt.figure(figsize=(5,4))
        plt.imshow(constructive - destructive, extent=[-L,L,-L,L], origin="lower", vmin=-1, vmax=1)
        plt.colorbar()
        plt.title(f"Constructive(+)/Destructive(-) regions (t={t:.2f})")
        plt.tight_layout()
        plt.savefig(os.path.join(outdir, f"mask_{i:04d}.png"), dpi=120)
        plt.close()

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default="./wound_out")
    ap.add_argument("--T", type=float, default=4.0)
    ap.add_argument("--dt", type=float, default=0.05)
    ap.add_argument("--N", type=int, default=256)
    ap.add_argument("--L", type=float, default=4.0)
    args = ap.parse_args()
    simulate(args.outdir, T=args.T, dt=args.dt, N=args.N, L=args.L)
