# su3_cannon.py
import importlib
import numpy as np
import matplotlib.pyplot as plt

import mass_hierarchy_apex_2 as mha  # apex / centreline machinery

# --------------------------------------------------
# 1) Map experiment names -> (module, run_function)
# --------------------------------------------------
EXPERIMENTS = {
    "corr_scan":      ("unification_10", "run_correlation_scan"),
    "topology_mesh":  ("unification_11", "run_topological_mesh"),
    "spectrometer":   ("unification_12", "run_spectrometer"),
    "cosmic_ray":     ("unification_13", "run_cosmic_raytrace"),
    "double_slit":    ("unification_14", "run_double_slit"),
    "emergent_grav":  ("unification_15", "run_emergent_gravity"),
    "unify_scan_1":   ("unification_16", "run_unification_scan"),
    "unify_scan_2":   ("unification_17", "run_unification_scan"),
    "mass_spectrum":  ("unification_18", "run_mass_spectrum"),
}

# Default physics core: the one mass_hierarchy_apex_2 already uses
DEFAULT_FIELD_MODULE = "unification_24"


# --------------------------------------------------
# 2) Retarget the mass machinery to any field module
# --------------------------------------------------
def retarget_field(field_module_name: str = DEFAULT_FIELD_MODULE):
    """
    Patch mass_hierarchy_apex_2 so that local_mass / find_apex /
    trace_centerline use the vacuum definitions from `field_module_name`.

    The target module must define:
        get_force_vectorized(m, lam)
        compute_tensor_flow()
        EPS
        M_MIN, M_MAX, L_MIN, L_MAX
    """
    field_mod = importlib.import_module(field_module_name)

    for attr in ["get_force_vectorized",
                 "compute_tensor_flow",
                 "EPS",
                 "M_MIN", "M_MAX",
                 "L_MIN", "L_MAX"]:
        if not hasattr(field_mod, attr):
            raise AttributeError(
                f"Field module {field_module_name} is missing {attr}"
            )
        setattr(mha, attr, getattr(field_mod, attr))

    print(f"[SU3] Retargeted mass machinery to {field_module_name}")


# --------------------------------------------------
# 3) Minimal SU(3) needle decoder
# --------------------------------------------------

def hessian_at_point(m0, l0, h_m, h_l):
    """2×2 Hessian of f=√λ1(m,λ) using mha.local_mass."""
    def f(m, lam):
        return mha.local_mass(m, lam)

    f0 = f(m0, l0)

    f_mm_p = f(m0 + h_m, l0)
    f_mm_m = f(m0 - h_m, l0)
    f_ll_p = f(m0, l0 + h_l)
    f_ll_m = f(m0, l0 - h_l)

    f_ml_pp = f(m0 + h_m, l0 + h_l)
    f_ml_pm = f(m0 + h_m, l0 - h_l)
    f_ml_mp = f(m0 - h_m, l0 + h_l)
    f_ml_mm = f(m0 - h_m, l0 - h_l)

    f_mm = (f_mm_p - 2.0 * f0 + f_mm_m) / (h_m**2)
    f_ll = (f_ll_p - 2.0 * f0 + f_ll_m) / (h_l**2)
    f_ml = (f_ml_pp - f_ml_pm - f_ml_mp + f_ml_mm) / (4.0 * h_m * h_l)

    H = np.array([[f_mm, f_ml],
                  [f_ml, f_ll]], dtype=float)
    vals, vecs = np.linalg.eigh(H)
    return H, vals, vecs


def compute_frenet(cm, cl):
    """Frenet-like tangent/normal + arc length."""
    n = len(cm)
    ds = np.sqrt(np.diff(cm)**2 + np.diff(cl)**2)
    s = np.concatenate([[0.0], np.cumsum(ds)])
    tangents = np.zeros((n, 2))
    for i in range(1, n - 1):
        v = np.array([cm[i+1] - cm[i-1], cl[i+1] - cl[i-1]], float)
        norm = np.linalg.norm(v)
        tangents[i] = v / norm if norm > 1e-14 else tangents[i-1]
    tangents[0] = tangents[1]
    tangents[-1] = tangents[-2]
    normals = np.column_stack([-tangents[:,1], tangents[:,0]])
    mean_ds = float(np.mean(ds))
    return s, tangents, normals, mean_ds


# tripod angles in (m, λ) plane – adjust once you’ve matched to JT/JR/JG
TRIPOD_ANGLES = {
    "T": 0.0,                 # placeholder
    "R": 2.0 * np.pi / 3.0,   # placeholder
    "G": 4.0 * np.pi / 3.0,   # placeholder
}
TRIPOD_VECS = {k: np.array([np.cos(a), np.sin(a)]) for k, a in TRIPOD_ANGLES.items()}


def run_su3_needle_analysis(step_size=0.15, n_steps=220, h_factor=0.5):
    """
    Aim the SU(3) cannon at the current field (whatever we retargeted
    mass_hierarchy_apex_2 to) and decode the traveler needle.
    """
    # 1) apex & mass field
    m0, l0, m_peak, M, L, Mass, apex_ij = mha.find_apex()
    print(f"[SU3] Apex at m0={m0:.6f}, λ0={l0:.6f}, peak √λ1≈{m_peak:.3f}")

    # 2) trace centreline (downhill wake)
    cm, cl, cf = mha.trace_centerline(
        M, L, Mass,
        start_ij=apex_ij,
        step_size=step_size,
        n_steps=n_steps,
        mode="downhill",
    )

    n = len(cm)
    dm = float(M[0,1] - M[0,0])
    dl = float(L[1,0] - L[0,0])
    h_m = dm * h_factor
    h_l = dl * h_factor

    s, t_vecs, n_vecs, mean_ds = compute_frenet(cm, cl)

    # 3) Hessians & eigen-directions along needle
    k_t = np.zeros(n)
    k_n = np.zeros(n)
    theta_dom = np.zeros(n)
    weights = {k: np.zeros(n) for k in TRIPOD_ANGLES.keys()}

    for i in range(n):
        H, evals, evecs = hessian_at_point(cm[i], cl[i], h_m, h_l)

        t = t_vecs[i]
        nrm = n_vecs[i]
        k_t[i] = float(t @ (H @ t))
        k_n[i] = float(nrm @ (H @ nrm))

        idx_dom = 0 if abs(evals[0]) > abs(evals[1]) else 1
        v_dom = evecs[:, idx_dom]  # unit vector
        theta_dom[i] = np.arctan2(v_dom[1], v_dom[0])

        # tripod mixture
        raw_w = []
        for name, u in TRIPOD_VECS.items():
            c = float(np.dot(v_dom, u))  # signed
            w = c * c
            weights[name][i] = w
            raw_w.append(w)
        total = sum(raw_w)
        if total > 1e-14:
            for name in TRIPOD_ANGLES.keys():
                weights[name][i] /= total

    interior = slice(3, max(3, n-3))

    # 4) mean mixture → SU(3) state
    mean_w = {k: float(np.mean(weights[k][interior]))
              for k in ["T", "R", "G"]}
    amps = np.array([np.sqrt(mean_w[k]) for k in ["T", "R", "G"]])
    amps /= np.linalg.norm(amps)

    print("\n[SU3] Mean mixture over interior:")
    for k in ["T", "R", "G"]:
        print(f"  <w_{k}> ≈ {mean_w[k]:.3f}")
    print(f"\n[SU3] Approximate color state |ψ> ≈ "
          f"({amps[0]:.3f}, {amps[1]:.3f}, {amps[2]:.3f}) in {{T,R,G}} basis")

    # 5) quick mixture plot
    plt.figure(figsize=(9,5))
    for k, col in zip(["T", "R", "G"], ["tab:blue", "tab:orange", "tab:green"]):
        plt.plot(s, weights[k], label=f"w_{k}", color=col)
    plt.xlabel("Arc length s along needle")
    plt.ylabel("Mixture weight")
    plt.ylim(-0.05, 1.05)
    plt.legend()
    plt.title("Tripod mixture along needle")
    plt.tight_layout()
    plt.savefig("su3_needle_weights.png", dpi=170)
    print("[SU3] saved su3_needle_weights.png")

    return {
        "s": s,
        "cm": cm,
        "cl": cl,
        "k_t": k_t,
        "k_n": k_n,
        "weights": weights,
        "amps": amps,
        "mean_w": mean_w,
        "mean_ds": mean_ds,
    }


# --------------------------------------------------
# 4) Top-level driver
# --------------------------------------------------

def fire_su3_cannon(field_module: str = DEFAULT_FIELD_MODULE,
                    experiment: str | None = None):
    """
    field_module : which unification_N provides the vacuum (defaults to 24).
    experiment   : optional key in EXPERIMENTS to also run a big global plot.
    """
    # 1) retarget physics core
    retarget_field(field_module)

    # 2) optionally run a big experiment for context
    if experiment is not None:
        mod_name, fn_name = EXPERIMENTS[experiment]
        exp_mod = importlib.import_module(mod_name)
        print(f"[EXP] Running {mod_name}.{fn_name}()...")
        getattr(exp_mod, fn_name)()

    # 3) run the SU(3) needle decoder
    return run_su3_needle_analysis()


if __name__ == "__main__":
    # Example: use unification_24 as core, and also show the topology mesh
    fire_su3_cannon(field_module="unification_24",
                    experiment="topology_mesh")
