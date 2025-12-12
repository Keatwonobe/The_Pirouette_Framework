# phase_coherence_scan.py
import os
import numpy as np
import matplotlib.pyplot as plt
from helical_scanner_5 import (
    get_ylm, N_TH_SYN, N_PH_SYN, LMAX
)

DATACUBE = "substrate_helical_datacube.npz"

def compute_alms_from_grid(field, lmax):
    """
    Inverse transform: Takes a k-slice T(theta, phi) and finds its Alms.
    Used to check phase relationships in the twisted frame.
    """
    n_th, n_ph = field.shape
    theta = np.linspace(0, np.pi, n_th)
    phi   = np.linspace(-np.pi, np.pi, n_ph, endpoint=False)
    TH, PH = np.meshgrid(theta, phi, indexing="ij")
    
    dtheta = theta[1] - theta[0]
    dphi   = phi[1]   - phi[0]
    weights = np.sin(TH) * dtheta * dphi
    
    alms = {}
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            Y = get_ylm(m, l, PH, TH)
            # Integration
            val = np.sum(field * np.conjugate(Y) * weights)
            alms[(l, m)] = val
    return alms

def phase_coherence_metric(alms, lmax):
    """
    Returns a score 0..1 indicating how 'locked' the phases are.
    A localized traveler implies linear phase shift in m.
    We look for consistency in the phase difference between adjacent m's.
    """
    coherence_sum = 0.0
    count = 0
    
    for l in range(2, lmax+1):
        # Extract phases for this l across all m
        # We look at m -> m+1 phase jumps
        phases = []
        for m in range(-l, l): # up to l-1
            a1 = alms.get((l, m), 0)
            a2 = alms.get((l, m+1), 0)
            if abs(a1) < 1e-6 or abs(a2) < 1e-6:
                continue
            
            # Phase difference
            dphi = np.angle(a2) - np.angle(a1)
            phases.append(np.exp(1j * dphi))
            
        if len(phases) > 2:
            # The magnitude of the mean vector of phase differences
            # If dphi is constant (linear phase), this is 1.0.
            # If dphi is random, this is ~0.
            R = np.abs(np.mean(phases))
            coherence_sum += R
            count += 1
            
    return coherence_sum / max(count, 1)

def main():
    if not os.path.exists(DATACUBE):
        print("Datacube missing.")
        return

    print(f"[*] Loading {DATACUBE}...")
    data = np.load(DATACUBE)
    cube = data["T_sub"]
    k_vals = data["k_values"]
    
    coherence_scores = []
    
    # We scan a subset of k to save time, or all if fast enough
    # Using stride of 2 for speed
    print(f"[*] Computing phase coherence for {len(k_vals)} slices...")
    
    for i, k in enumerate(k_vals):
        field = cube[i]
        
        # Decompose back to Alms (in the twisted frame)
        # Using a lower LMAX for speed in this metric check
        alms_k = compute_alms_from_grid(field, lmax=15)
        
        score = phase_coherence_metric(alms_k, lmax=15)
        coherence_scores.append(score)
        
        if i % 10 == 0:
            print(f"    k={k:.3f} | Phase Coherence={score:.4f}")
            
    # Plot
    plt.figure(figsize=(10, 5))
    plt.plot(k_vals, coherence_scores, 'g-')
    plt.title("Helical Phase Locking vs Twist")
    plt.xlabel("Twist k")
    plt.ylabel("Phase Coherence Order Parameter")
    plt.axvline(-0.492, color='k', ls='--', alpha=0.3, label="Candidate -0.492")
    plt.legend()
    plt.tight_layout()
    plt.savefig("phase_coherence_scan.png")
    print("✅ Saved phase_coherence_scan.png")

if __name__ == "__main__":
    main()