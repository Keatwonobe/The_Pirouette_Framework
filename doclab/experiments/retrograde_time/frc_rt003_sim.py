#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RT-003 Retrograde/Advanced Admixture Simulator
----------------------------------------------
Simulates a driven cavity (damped harmonic oscillator) with a small admixture of advanced
(retrograde) response, parameterized by epsilon. Sweeps frequency, computes magnitude, phase,
apparent group delay, and a toy Casimir-like normalized pressure shift estimate.

Effective linear response:
  H_ret(ω) = 1 / (ω0^2 - ω^2 + i γ ω)         # retarded
  H_adv(ω) = 1 / (ω0^2 - ω^2 - i γ ω)         # advanced
  H_eff(ω; ε) = sqrt(1-ε^2) H_ret + ε H_adv   # ε in [0, 1)

Group delay τ_g = dφ/dω where φ = arg(H_eff).

CLI:
  --f0 <Hz>         resonance frequency (default 1e6 Hz)
  --Q <float>       quality factor (default 2e4)
  --eps "a,b,c"     epsilon values (default "0,1e-3,3e-3,1e-2")
  --fmin <Hz>       sweep start (default 0.5 f0)
  --fmax <Hz>       sweep end (default 1.5 f0)
  --npts <int>      number of frequency points (default 2000)
  --csv <path>      optional CSV output
  --png_phase <p>   optional PNG for phase plot
  --png_tau <p>     optional PNG for group-delay plot
  --casimir_L <m>   effective cavity length L for toy Casimir term (default: 0.05 m)
  --verbose         print summary lines
"""

import argparse
import numpy as np
import csv

def transfer_retarded(omega0, gamma, omega):
    return 1.0 / (omega0**2 - omega**2 + 1j*gamma*omega)

def transfer_advanced(omega0, gamma, omega):
    return 1.0 / (omega0**2 - omega**2 - 1j*gamma*omega)

def mix_response(Hr, Ha, eps):
    eps = float(eps)
    if eps < 0 or eps >= 1:
        raise ValueError("epsilon must be in [0,1)")
    return np.sqrt(1.0 - eps**2) * Hr + eps * Ha

def phase_unwrapped(z):
    return np.unwrap(np.angle(z))

def group_delay(phi, omega):
    dphi = np.gradient(phi, omega, edge_order=2)
    return dphi

def casimir_toy_phase_shift(H_eff, L, c=299792458.0):
    phi = np.angle(H_eff)
    return np.cos(2.0*phi)

def run_sweep(f0=1e6, Q=2e4, eps_list=(0.0, 1e-3, 3e-3, 1e-2), fmin=None, fmax=None, npts=2000,
              csv_path=None, L=0.05, verbose=False):
    omega0 = 2*np.pi*f0
    gamma = omega0 / Q
    if fmin is None: fmin = 0.5*f0
    if fmax is None: fmax = 1.5*f0
    f = np.linspace(fmin, fmax, npts)
    omega = 2*np.pi*f

    Hr = transfer_retarded(omega0, gamma, omega)
    Ha = transfer_advanced(omega0, gamma, omega)

    results = []

    for eps in eps_list:
        He = mix_response(Hr, Ha, eps)
        phi = phase_unwrapped(He)
        tau_g = group_delay(phi, omega)
        cas_norm = casimir_toy_phase_shift(He, L)

        if verbose:
            idx = np.argmin(np.abs(f - f0))
            print(f"[eps={eps:0.4g}]  |H|@f0={np.abs(He[idx]):.3e}, "
                  f"phi@f0={phi[idx]:.3f} rad, tau_g@f0={tau_g[idx]:.3e} s, "
                  f"<cos(2phi)>={np.mean(cas_norm):.3e}")

        results.append({
            "eps": eps,
            "f": f.copy(),
            "mag": np.abs(He),
            "phase": phi,
            "tau_g": tau_g,
            "cas_norm": cas_norm
        })

    if csv_path is not None:
        with open(csv_path, "w", newline="") as cf:
            writer = csv.writer(cf)
            header = ["f_Hz"]
            for eps in eps_list:
                header += [f"mag_eps{eps}", f"phase_rad_eps{eps}", f"tau_s_eps{eps}", f"cas_norm_eps{eps}"]
            writer.writerow(header)
            for i in range(npts):
                row = [f[i]]
                for r in results:
                    row += [r["mag"][i], r["phase"][i], r["tau_g"][i], r["cas_norm"][i]]
                writer.writerow(row)

    return results

def main():
    ap = argparse.ArgumentParser(description="RT-003 retrograde/advanced admixture simulator")
    ap.add_argument("--f0", type=float, default=1e6)
    ap.add_argument("--Q", type=float, default=2e4)
    ap.add_argument("--eps", type=str, default="0,1e-3,3e-3,1e-2")
    ap.add_argument("--fmin", type=float, default=None)
    ap.add_argument("--fmax", type=float, default=None)
    ap.add_argument("--npts", type=int, default=2000)
    ap.add_argument("--csv", type=str, default=None)
    ap.add_argument("--png_phase", type=str, default=None)
    ap.add_argument("--png_tau", type=str, default=None)
    ap.add_argument("--casimir_L", type=float, default=0.05)
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    eps_list = tuple(float(x) for x in args.eps.split(","))

    res = run_sweep(f0=args.f0, Q=args.Q, eps_list=eps_list,
                    fmin=args.fmin, fmax=args.fmax, npts=args.npts,
                    csv_path=args.csv, L=args.casimir_L, verbose=args.verbose)

    if (args.png_phase is not None) or (args.png_tau is not None):
        import matplotlib.pyplot as plt

    if args.png_phase is not None:
        plt.figure()
        for r in res:
            plt.plot(r["f"], r["phase"], label=f"eps={r['eps']}")
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Phase (rad)")
        plt.title("Phase vs Frequency (retrograde admixture)")
        plt.legend()
        plt.tight_layout()
        plt.savefig(args.png_phase, dpi=150)

    if args.png_tau is not None:
        plt.figure()
        for r in res:
            plt.plot(r["f"], r["tau_g"], label=f"eps={r['eps']}")
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Group delay τ_g (s)")
        plt.title("Group Delay vs Frequency")
        plt.legend()
        plt.tight_layout()
        plt.savefig(args.png_tau, dpi=150)

if __name__ == "__main__":
    main()
