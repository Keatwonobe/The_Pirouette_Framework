#!/usr/bin/env python3
"""
helical_kappa_demo.py

A small "how this works" tool for the Helical Calculus and κ-Hamiltonian
defined in MATH-028.

What this script illustrates:

1. Helical derivative:
      d_h/dt = d/dt + i κ ω
   We apply it to a simple oscillatory signal and contrast it with the
   classical derivative.

2. κ-Hamiltonian energy levels:
      E_n(κ) = ℏ ω (n + 1/2) sqrt(1 + κ^2)
   We show how κ>0 changes the spectrum relative to κ=0.

3. Rotational memory intuition:
   We evolve a complex amplitude under classical vs helical dynamics
   and print out how the phase drifts when κ ≠ 0.

This is NOT a full operator algebra implementation; it's an
explanatory toy you can show in a README or notebook to convey
what you were thinking when you introduced κ.
"""

import argparse
import numpy as np

try:
    import matplotlib.pyplot as plt
    HAS_MPL = True
except Exception:
    HAS_MPL = False


# -----------------------------
# Core helical calculus pieces
# -----------------------------

def helical_derivative(P: np.ndarray,
                       t: np.ndarray,
                       kappa: float,
                       omega: float) -> np.ndarray:
    """
    Numerical helical derivative of a complex signal P(t):

        d_h P / dt = dP/dt + i κ ω P

    P:      complex or real array, shape (N,)
    t:      real array of times, same shape as P
    kappa:  helical coupling κ
    omega:  base angular frequency ω

    Returns: complex array d_h P / dt
    """
    dPdt = np.gradient(P, t)
    return dPdt + 1j * kappa * omega * P


def energy_levels(n_max: int,
                  kappa: float,
                  omega: float,
                  hbar: float = 1.0) -> np.ndarray:
    """
    κ-Hamiltonian energy spectrum for a helical harmonic oscillator:

        E_n(κ) = ℏ ω (n + 1/2) sqrt(1 + κ^2)

    n_max:  largest level index to compute (0..n_max)
    kappa:  helical coupling κ
    omega:  base angular frequency
    hbar:   Planck's constant (set to 1 for convenience)

    Returns: array of shape (n_max+1,)
    """
    n = np.arange(n_max + 1, dtype=float)
    return hbar * omega * (n + 0.5) * np.sqrt(1.0 + kappa ** 2)


# --------------------------------
# Demo 1: Derivatives side-by-side
# --------------------------------

def demo_derivatives(kappa: float,
                     omega: float,
                     t_end: float = 10.0,
                     n_points: int = 2000) -> None:
    """
    Show classical vs helical derivative on a simple oscillation:

        P(t) = exp(-i ω t)

    Prints some sample values and, if matplotlib is available,
    plots the magnitude of both derivatives.
    """
    print("\n=== DEMO 1: Helical derivative vs classical derivative ===")
    print(f"Using κ = {kappa:.3f}, ω = {omega:.3f}")

    t = np.linspace(0.0, t_end, n_points)
    P = np.exp(-1j * omega * t)  # simple phase-rotating complex amplitude

    dPdt_classical = np.gradient(P, t)
    dPdt_helical = helical_derivative(P, t, kappa=kappa, omega=omega)

    # Take a few sample points for the console
    sample_indices = np.linspace(0, n_points - 1, 5, dtype=int)
    print("\nSample comparison at selected times:")
    for idx in sample_indices:
        tt = t[idx]
        c_val = dPdt_classical[idx]
        h_val = dPdt_helical[idx]
        print(f" t = {tt:6.3f} | classical dP/dt = {c_val.real: .4f} + {c_val.imag: .4f} i"
              f" | helical d_hP/dt = {h_val.real: .4f} + {h_val.imag: .4f} i")

    if HAS_MPL:
        plt.figure()
        plt.title(f"Derivative magnitude, κ={kappa}")
        plt.plot(t, np.abs(dPdt_classical), label="|dP/dt| (classical)")
        plt.plot(t, np.abs(dPdt_helical), linestyle="--", label="|d_hP/dt| (helical)")
        plt.xlabel("t")
        plt.ylabel("magnitude")
        plt.legend()
        plt.tight_layout()
        plt.show()
    else:
        print("\n(matplotlib not available; skipping plots)")


# ---------------------------------------
# Demo 2: Energy levels vs κ and n
# ---------------------------------------

def demo_spectrum(kappa_values,
                  omega: float,
                  n_max: int = 5,
                  hbar: float = 1.0) -> None:
    """
    Print and optionally plot the κ-Hamiltonian spectrum
    for several κ values.
    """
    print("\n=== DEMO 2: κ-Hamiltonian spectrum ===")
    print(f"ω = {omega:.3f}, n = 0..{n_max}")

    for kappa in kappa_values:
        E = energy_levels(n_max=n_max, kappa=kappa, omega=omega, hbar=hbar)
        print(f"\nκ = {kappa:.3f}")
        for n, En in enumerate(E):
            print(f"  E_{n}(κ={kappa:.3f}) = {En:.6f}")

    if HAS_MPL:
        plt.figure()
        n = np.arange(n_max + 1)
        for kappa in kappa_values:
            E = energy_levels(n_max=n_max, kappa=kappa, omega=omega, hbar=hbar)
            plt.plot(n, E, marker="o", label=f"κ={kappa}")
        plt.xlabel("level n")
        plt.ylabel("E_n(κ)")
        plt.title("κ-Hamiltonian energy levels")
        plt.legend()
        plt.tight_layout()
        plt.show()
    else:
        print("\n(matplotlib not available; skipping spectrum plot)")


# --------------------------------------------------
# Demo 3: “Rotational memory” phase drift comparison
# --------------------------------------------------

def demo_rotational_memory(kappa: float,
                           omega: float,
                           t_end: float = 20.0,
                           n_points: int = 2000) -> None:
    """
    Evolve a complex amplitude under simple "classical" vs "helical"
    dynamics to show how κ induces extra phase drift.

    We integrate:
        dP_classical/dt = -i ω P_classical
        dP_helical/dt   = -i ω P_helical + i κ ω P_helical
                        = -i ω (1 - κ) P_helical     (toy picture)

    This is a simplified classical analog of the cross-term in the
    κ-Hamiltonian, just to show what "rotational memory" FEELS like
    in time series form.
    """
    print("\n=== DEMO 3: Rotational memory phase drift ===")
    print(f"Using κ = {kappa:.3f}, ω = {omega:.3f}")

    t = np.linspace(0.0, t_end, n_points)
    dt = t[1] - t[0]

    P_class = np.zeros_like(t, dtype=complex)
    P_helix = np.zeros_like(t, dtype=complex)

    # initial condition: P(0) = 1
    P_class[0] = 1.0 + 0.0j
    P_helix[0] = 1.0 + 0.0j

    for i in range(1, n_points):
        P_class[i] = P_class[i - 1] + dt * (-1j * omega * P_class[i - 1])
        P_helix[i] = P_helix[i - 1] + dt * (-1j * omega * (1.0 - kappa) * P_helix[i - 1])

    # Print phase at a few checkpoints
    sample_indices = np.linspace(0, n_points - 1, 6, dtype=int)
    print("\nTime    phase(classical)   phase(helical)")
    print("-----  -----------------   --------------")
    for idx in sample_indices:
        tt = t[idx]
        phase_c = np.angle(P_class[idx])
        phase_h = np.angle(P_helix[idx])
        print(f"{tt:5.2f}   {phase_c: .4f} rad       {phase_h: .4f} rad")

    if HAS_MPL:
        plt.figure()
        plt.title(f"Phase vs time, κ={kappa}")
        plt.plot(t, np.unwrap(np.angle(P_class)), label="classical phase")
        plt.plot(t, np.unwrap(np.angle(P_helix)), linestyle="--", label="helical phase")
        plt.xlabel("t")
        plt.ylabel("phase (unwrapped)")
        plt.legend()
        plt.tight_layout()
        plt.show()
    else:
        print("\n(matplotlib not available; skipping phase plots)")


# ----------------
# CLI / Entrypoint
# ----------------

def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Explanatory demo tool for the Helical Calculus and κ-Hamiltonian.\n"
            "Use this to show what κ does to derivatives, spectra, and phase."
        )
    )
    parser.add_argument(
        "--mode",
        choices=["derivative", "spectrum", "memory", "all"],
        default="all",
        help="Which demo to run."
    )
    parser.add_argument(
        "--kappa",
        type=float,
        default=0.3,
        help="Helical coupling κ for derivative/memory demos (default: 0.3)."
    )
    parser.add_argument(
        "--omega",
        type=float,
        default=1.0,
        help="Base angular frequency ω (default: 1.0)."
    )
    parser.add_argument(
        "--n-max",
        type=int,
        default=5,
        help="Maximum energy level index for the spectrum demo."
    )
    parser.add_argument(
        "--kappa-grid",
        type=float,
        nargs="*",
        default=[0.0, 0.2, 0.5, 1.0],
        help=(
            "List of κ values for the spectrum demo. "
            "Default: 0.0 0.2 0.5 1.0"
        )
    )
    return parser


def main():
    parser = build_arg_parser()
    args = parser.parse_args()

    print("\n[ Helical κ-Hamiltonian: 'how this works' demo tool ]")
    print("  - derivative: compare d/dt vs d_h/dt")
    print("  - spectrum:   compare E_n(κ) across κ values")
    print("  - memory:     show κ-driven phase drift over time\n")

    if args.mode in ("derivative", "all"):
        demo_derivatives(kappa=args.kappa, omega=args.omega)

    if args.mode in ("spectrum", "all"):
        demo_spectrum(kappa_values=args.kappa_grid,
                      omega=args.omega,
                      n_max=args.n_max)

    if args.mode in ("memory", "all"):
        demo_rotational_memory(kappa=args.kappa, omega=args.omega)

    print("\nDone.\n")


if __name__ == "__main__":
    main()
