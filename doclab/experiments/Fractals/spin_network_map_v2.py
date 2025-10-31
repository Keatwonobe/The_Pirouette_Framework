
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import argparse

def update_spins(theta, J, lam, beta):
    mean_vector = np.mean(np.exp(1j * theta))
    psi = np.angle(mean_vector)
    Ta = np.abs(mean_vector)**2
    J_eff = J * (1 + beta * (1 - Ta))
    theta = theta + J_eff * np.sin(psi - theta) - lam * np.sin(theta)
    return np.mod(theta, 2*np.pi), Ta

def simulate_point(J, lam, n_spins, n_iters, beta, n_runs, seed):
    rng = np.random.default_rng(seed)
    M_runs = []
    Ta_last = 0.0
    for r in range(n_runs):
        theta = 2*np.pi*rng.random(n_spins)
        for _ in range(n_iters):
            theta, Ta = update_spins(theta, J, lam, beta)
        M = np.abs(np.mean(np.exp(1j*theta)))
        M_runs.append(M)
        Ta_last = Ta
    M_runs = np.array(M_runs)
    M_mean = float(M_runs.mean())
    M_std  = float(M_runs.std(ddof=1)) if n_runs > 1 else 0.0
    m2 = float(np.mean(M_runs**2))
    m4 = float(np.mean(M_runs**4))
    U = 1.0 - (m4 / (3.0*m2*m2)) if m2 > 0 else 0.0
    return M_mean, Ta_last, M_std, U

def build_maps(j_min, j_max, l_min, l_max, j_steps, l_steps,
               n_spins, n_iters, beta, n_runs, seed):
    J_vals = np.linspace(j_min, j_max, j_steps)
    L_vals = np.linspace(l_min, l_max, l_steps)
    M_map  = np.zeros((l_steps, j_steps))
    Ta_map = np.zeros_like(M_map)
    Std_map = np.zeros_like(M_map)
    U_map = np.zeros_like(M_map)
    base_rng = np.random.default_rng(seed)
    seeds = base_rng.integers(0, 2**31-1, size=(l_steps, j_steps))
    for i, lam in enumerate(L_vals):
        for j, J in enumerate(J_vals):
            M, Ta, Mstd, U = simulate_point(J, lam, n_spins, n_iters, beta, n_runs, int(seeds[i, j]))
            M_map[i, j]  = M
            Ta_map[i, j] = Ta
            Std_map[i, j]= Mstd
            U_map[i, j]  = U
    return J_vals, L_vals, M_map, Ta_map, Std_map, U_map

def gradient_ridge(map2d, J_vals, L_vals):
    dL, dJ = np.gradient(map2d, L_vals, J_vals, edge_order=2)
    G = np.sqrt(dL**2 + dJ**2)
    if G.max() > 0:
        G = (G - G.min()) / (G.max() - G.min())
    return G

def plot_all(J_vals, L_vals, M_map, Ta_map, Std_map, U_map, out_prefix):
    extent = [J_vals[0], J_vals[-1], L_vals[0], L_vals[-1]]
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    Ridge_M  = gradient_ridge(M_map,  J_vals, L_vals)
    Ridge_Ta = gradient_ridge(Ta_map, J_vals, L_vals)
    fig, axs = plt.subplots(2, 3, figsize=(16, 9), constrained_layout=True)
    im0 = axs[0,0].imshow(M_map,  origin='lower', extent=extent, aspect='auto', cmap='inferno'); axs[0,0].set_title("Coherence M")
    im1 = axs[0,1].imshow(Ta_map, origin='lower', extent=extent, aspect='auto', cmap='inferno'); axs[0,1].set_title("Time-Adherence T(a)")
    im2 = axs[0,2].imshow(Std_map,origin='lower', extent=extent, aspect='auto', cmap='inferno'); axs[0,2].set_title("Std(M) across runs")
    im3 = axs[1,0].imshow(U_map,  origin='lower', extent=extent, aspect='auto', cmap='inferno'); axs[1,0].set_title("Binder cumulant U")
    im4 = axs[1,1].imshow(Ridge_M, origin='lower', extent=extent, aspect='auto', cmap='inferno'); axs[1,1].set_title("Ridge strength of M")
    im5 = axs[1,2].imshow(Ridge_Ta,origin='lower', extent=extent, aspect='auto', cmap='inferno'); axs[1,2].set_title("Ridge strength of T(a)")
    for ax in axs.flat:
        ax.set_xlabel("Coupling J")
        ax.set_ylabel("Frustration λ")
        ax.text(0.02, 0.02, f"Generated: {ts}", transform=ax.transAxes, fontsize=7, color='white', alpha=0.7)
    for im in [im0, im1, im2, im3, im4, im5]:
        cbar = plt.colorbar(im, ax=axs.flat, shrink=0.85)
        cbar.ax.tick_params(labelsize=8)
    plt.suptitle("Spin–T(a) Phase Diagnostics", fontsize=14)
    fname = f"{out_prefix}_diagnostics.png"
    plt.savefig(fname, dpi=220)
    print(f"Saved figure: {fname}")
    plt.close(fig)

def main():
    ap = argparse.ArgumentParser(description="Map M, T(a), and diagnostics for the spin–T(a) model")
    ap.add_argument("--j-min", type=float, default=-5.0)
    ap.add_argument("--j-max", type=float, default=5.0)
    ap.add_argument("--l-min", type=float, default=-5.0)
    ap.add_argument("--l-max", type=float, default=5.0)
    ap.add_argument("--j-steps", type=int, default=200)
    ap.add_argument("--l-steps", type=int, default=200)
    ap.add_argument("--spins", type=int, default=256)
    ap.add_argument("--iters", type=int, default=400)
    ap.add_argument("--beta", type=float, default=1.0)
    ap.add_argument("--runs", type=int, default=3, help="independent runs per cell (>=2 for Std/Binder)")
    ap.add_argument("--seed", type=int, default=1337)
    ap.add_argument("--out", type=str, default="spin_ta_map_v2")
    args = ap.parse_args()
    J_vals, L_vals, M_map, Ta_map, Std_map, U_map = build_maps(
        args.j_min, args.j_max, args.l_min, args.l_max,
        args.j_steps, args.l_steps,
        args.spins, args.iters, args.beta, args.runs, args.seed
    )
    plot_all(J_vals, L_vals, M_map, Ta_map, Std_map, U_map, args.out)

if __name__ == "__main__":
    main()
