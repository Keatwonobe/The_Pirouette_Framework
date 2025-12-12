# proton_potentials_scan.py
import numpy as np
import matplotlib.pyplot as plt
from twist_unit import sector_weights_continuum

def sample(min_tau=1.8, max_tau=6.0, N=1200):
    taus = np.linspace(min_tau, max_tau, N)
    Gs, Ts, Rs = [], [], []
    for t in taus:
        G, T, R = sector_weights_continuum(t)
        Gs.append(G)
        Ts.append(T)
        Rs.append(R)
    return taus, np.array(Gs), np.array(Ts), np.array(Rs)

def main():
    taus, G, T, R = sample()

    eps = 1e-16

    # 1) Shannon entropy: mixing of sectors
    W = np.vstack([G, T, R])  # 3×N
    H = -np.sum(W * np.log(W + eps), axis=0)

    # 2) Imbalance: R vs average of G,T
    I = R - 0.5*(G + T)

    # 3) Ratio: how dominant is R over (G+T)
    Q = R / (G + T + eps)

    fig, axs = plt.subplots(3, 1, figsize=(9, 9), sharex=True)

    axs[0].plot(taus, H)
    axs[0].set_ylabel("Entropy H(τ)")

    axs[1].plot(taus, I)
    axs[1].set_ylabel("Imbalance I(τ)")

    axs[2].plot(taus, Q)
    axs[2].set_ylabel("Ratio Q(τ) = R/(G+T)")
    axs[2].set_xlabel("Twist τ")

    fig.suptitle("Composite 'Proton Potentials' from Sector Weights")
    plt.tight_layout()
    plt.savefig("proton_potentials_2.png", dpi=200)
    print("[+] Saved proton_potentials_2.png")

if __name__ == "__main__":
    main()
