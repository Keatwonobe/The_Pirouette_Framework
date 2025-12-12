
#!/usr/bin/env python3
# (see previous cell for full docstring)
import argparse
from dataclasses import dataclass
from typing import Sequence
import numpy as np


@dataclass
class CompassParams:
    gamma_scale: float = 6.0
    ta_scale: float = 6.0
    sigma_r: float = 7.0
    a_wind: float = 0.35
    a_tpci: float = 0.25
    k_wave: float = 0.45
    theta0: float = 0.0
    kappa0: float = 0.06
    kappa_decay: float = 0.08
    xi: float = 0.8

def mesh_grid(extent: float = 14.0, steps: int = 240):
    g = np.linspace(-extent, extent, steps)
    G, T = np.meshgrid(g, g)
    return G, T

def polarize(G, T, ps: CompassParams):
    R = np.sqrt((G/ps.gamma_scale)**2 + (T/ps.ta_scale)**2)
    Theta = np.arctan2(T/ps.ta_scale, G/ps.gamma_scale)
    return R, Theta

def kappa_field(R, ps: CompassParams):
    return ps.kappa0 * np.exp(-ps.kappa_decay * R)

def G_env(R, ps: CompassParams):
    return np.exp(-(R**2) / (2.0 * ps.sigma_r**2))

def winding(Theta_prime, n: float):
    return np.cos(2.0 * np.pi * n * Theta_prime / np.pi)

def tpci_hint(R, Theta, ps: CompassParams):
    kr = ps.k_wave * R
    radial = np.sinc(kr/np.pi)
    ang = np.cos(Theta - ps.theta0)
    return radial * ang

def compass_potential(G, T, n: float, ps: CompassParams):
    R, Theta = polarize(G, T, ps)
    kap = kappa_field(R, ps)
    Theta_prime = Theta + kap * ps.xi
    U = G_env(R, ps) * (1.0 + ps.a_wind * winding(Theta_prime, n) + ps.a_tpci * tpci_hint(R, Theta, ps))
    return U, R, Theta, kap

def make_plot(G, T, U, kap, title: str, out_path: str = None, elev: float = 30, azim: float = -45):
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(G, T, U, linewidth=0, antialiased=True)
    ax.set_xlabel("Γ (drive)")
    ax.set_ylabel("Ta (time-adherence)")
    ax.set_zlabel("Coherence density U")
    ax.set_title(title)
    ax.view_init(elev=elev, azim=azim)
    if out_path:
        plt.tight_layout()
        plt.savefig(out_path, dpi=180)
    return fig

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--extent", type=float, default=14.0)
    ap.add_argument("--steps", type=int, default=240)
    ap.add_argument("--n", type=float, nargs="+", default=[0.5])
    ap.add_argument("--kappa", type=float, default=None)
    ap.add_argument("--out", type=str, default="compass_demo.png")
    ap.add_argument("--azim", type=float, default=-45.0)
    ap.add_argument("--elev", type=float, default=30.0)
    args = ap.parse_args()

    ps = CompassParams()
    if args.kappa is not None:
        ps.kappa0 = float(args.kappa)

    G, T = mesh_grid(args.extent, args.steps)

    if len(args.n) == 1:
        n = float(args.n[0])
        U, R, Theta, kap = compass_potential(G, T, n, ps)
        title = f"Cosmic Compass (n={n}, κ0={ps.kappa0})"
        make_plot(G, T, U, kap, title, args.out, elev=args.elev, azim=args.azim)
    else:
        U_total = np.zeros_like(G, dtype=float)
        for n in args.n:
            U_n, R, Theta, kap = compass_potential(G, T, float(n), ps)
            U_total += U_n
        U_total /= float(len(args.n))
        title = f"Cosmic Compass (n={','.join(map(str,args.n))}, κ0={ps.kappa0})"
        make_plot(G, T, U_total, kap, title, args.out, elev=args.elev, azim=args.azim)

if __name__ == "__main__":
    main()
