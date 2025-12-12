import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from helical_scanner_5 import get_ylm, N_TH_SYN, N_PH_SYN
from phase_coherence_scan import compute_alms_from_grid, phase_coherence_metric

DATACUBE = "substrate_helical_datacube.npz"

def inject_impulse(field, strength=5.0, sigma=0.02):
    n_th, n_ph = field.shape
    th = np.linspace(0, np.pi, n_th)
    ph = np.linspace(-np.pi, np.pi, n_ph)
    TH, PH = np.meshgrid(th, ph, indexing="ij")

    # Put the “supernova” at theta≈π/2, phi≈0
    d = np.sqrt((TH - np.pi/2)**2 + PH**2)
    impulse = strength * np.exp(-0.5*(d/sigma)**2)
    return field + impulse

def compute_reaction_time(field0, field1, lmax=10):
    """How long does vacuum take to re-cohere?"""
    a0 = compute_alms_from_grid(field0, lmax)
    a1 = compute_alms_from_grid(field1, lmax)
    c0 = phase_coherence_metric(a0, lmax)
    c1 = phase_coherence_metric(a1, lmax)
    return c1 - c0  # larger = slower reaction

def main():
    data = np.load(DATACUBE)
    cube = data["T_sub"]
    k_vals = data["k_values"]

    reaction = []

    print("\n[*] Running Vacuum Reaction Time Simulation...\n")

    for i, k in enumerate(k_vals):
        base = cube[i]
        shocked = inject_impulse(base, strength=8.0, sigma=0.015)
        r = compute_reaction_time(base, shocked, lmax=12)
        reaction.append(r)

        if i % 10 == 0:
            print(f"k={k:.3f} | Reaction Time Δ={r:.4e}")

    plt.figure(figsize=(10,5))
    plt.plot(k_vals, reaction, 'm-')
    plt.axvline(-0.492, ls='--', alpha=0.4)
    plt.title("Vacuum Reaction Time vs Twist k (Supernova Tuning Fork)")
    plt.xlabel("Twist k")
    plt.ylabel("Reaction Delay (phase coherence drop)")
    plt.tight_layout()
    plt.savefig("vacuum_reaction_time_scan.png")
    print("✅ Saved vacuum_reaction_time_scan.png")

if __name__ == "__main__":
    main()
