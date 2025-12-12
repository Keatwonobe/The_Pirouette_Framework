"""
needle_impact_on_particles.py

Study how the needle apex in the vacuum stiffness surface
affects the previously-identified particle candidates.

Requirements:
- Must live in the same directory as unification_24.py
- That file must define: compute_tensor_flow, RES, M_MIN, M_MAX, L_MIN, L_MAX
"""

import numpy as np
import matplotlib.pyplot as plt

# Import your existing field / tensor machinery
import unification_24 as base

# ------------------------------------------------------------
# 1. Particle candidates (copied from your spectrometry report)
# ------------------------------------------------------------
candidates = [
    # id, species, m, λ, action_mass
    (0,  "Red",  -2.40, -3.00,  2.72406),
    (1,  "Red",  -1.74, -3.00, 11.00568),
    (2,  "Red",  -0.12, -3.00,  4.48516),
    (3,  "Red",   1.35, -3.00,  1.80143),
    (4,  "Red",   2.97, -3.00,  7.38332),
    (5,  "Red",   0.12, -1.86, 10.09232),
    (6,  "Red",   0.15, -1.08,  2.23260),
    (7,  "Red",  -0.21, -0.60,  3.85218),
    (9,  "Teal", -0.90,  0.81,  4.81893),
    (10, "Gold",  2.46,  1.74, 13.34630),
    (13, "Gold",  1.77,  2.76,  3.91280),
    (14, "Teal", -3.00,  2.97,  2.60456),
    (15, "Gold",  2.85,  2.97, 10.12158),
]

species_color = {
    "Red":  "red",
    "Teal": "cyan",
    "Gold": "gold",
}

# ------------------------------------------------------------
# 2. Helper: bilinear interpolation on the tensor grid
# ------------------------------------------------------------
def bilinear_interp(x, y, x_grid, y_grid, field):
    """
    Bilinear interpolation of 'field' defined on (x_grid, y_grid) mesh.
    x_grid, y_grid are 1D arrays; field has shape (len(y_grid), len(x_grid)).
    """
    # find indices
    if not (x_grid[0] <= x <= x_grid[-1] and y_grid[0] <= y <= y_grid[-1]):
        return np.nan

    ix = np.searchsorted(x_grid, x) - 1
    iy = np.searchsorted(y_grid, y) - 1
    ix = np.clip(ix, 0, len(x_grid) - 2)
    iy = np.clip(iy, 0, len(y_grid) - 2)

    x0, x1 = x_grid[ix], x_grid[ix+1]
    y0, y1 = y_grid[iy], y_grid[iy+1]

    tx = (x - x0) / (x1 - x0 + 1e-12)
    ty = (y - y0) / (y1 - y0 + 1e-12)

    f00 = field[iy,   ix  ]
    f10 = field[iy,   ix+1]
    f01 = field[iy+1, ix  ]
    f11 = field[iy+1, ix+1]

    f0 = f00*(1-tx) + f10*tx
    f1 = f01*(1-tx) + f11*tx
    return f0*(1-ty) + f1*ty

# ------------------------------------------------------------
# 3. Build the tensor field and locate the needle apex
# ------------------------------------------------------------
def build_mass_field():
    M, L, vx, vy, mass_map = base.compute_tensor_flow()  # mass_map = sqrt(L1)
    # 1D grids corresponding to axes
    m_range = np.linspace(base.M_MIN, base.M_MAX, base.RES)
    l_range = np.linspace(base.L_MIN, base.L_MAX, base.RES)

    # Find global maximum of mass_map (needle apex)
    idx_max = np.unravel_index(np.argmax(mass_map), mass_map.shape)
    l0 = l_range[idx_max[0]]
    m0 = m_range[idx_max[1]]
    apex_mass = mass_map[idx_max]

    print("\n===== Needle Apex (from mass_map) =====")
    print(f"Apex at m0 = {m0:.6f}, λ0 = {l0:.6f}")
    print(f"Mass eigenvalue √λ1 at apex ≈ {apex_mass:.6f}")

    # Gradient of mass field (for "pressure" directions)
    dMass_dL, dMass_dM = np.gradient(mass_map, l_range, m_range)

    return m_range, l_range, mass_map, dMass_dM, dMass_dL, (m0, l0, apex_mass)

# ------------------------------------------------------------
# 4. Follow steepest-descent flow from each candidate
# ------------------------------------------------------------
def trace_flow_from_point(m_start, l_start,
                          m_range, l_range,
                          dMass_dM, dMass_dL,
                          step=0.02, n_steps=200):
    """
    Follow downhill flow in the mass eigenvalue landscape:
        d(m,λ)/dτ = -∇(mass)
    Returns arrays of (m_path, l_path).
    """
    m = m_start
    l = l_start
    m_path = [m]
    l_path = [l]

    for _ in range(n_steps):
        g_m = bilinear_interp(m, l, m_range, l_range, dMass_dM)
        g_l = bilinear_interp(m, l, m_range, l_range, dMass_dL)
        if np.isnan(g_m) or np.isnan(g_l):
            break

        # Downhill direction
        v_m, v_l = -g_m, -g_l
        norm = np.hypot(v_m, v_l)
        if norm < 1e-12:
            break
        v_m /= norm
        v_l /= norm

        m_new = m + step * v_m
        l_new = l + step * v_l

        # Stop if we leave the domain
        if not (m_range[0] <= m_new <= m_range[-1] and
                l_range[0] <= l_new <= l_range[-1]):
            break

        m, l = m_new, l_new
        m_path.append(m)
        l_path.append(l)

    return np.array(m_path), np.array(l_path)

# ------------------------------------------------------------
# 5. Main analysis + plotting
# ------------------------------------------------------------
def main():
    m_range, l_range, mass_map, dMass_dM, dMass_dL, apex = build_mass_field()
    m0, l0, apex_mass = apex

    # Precompute convenience for background plot
    M_grid, L_grid = np.meshgrid(m_range, l_range)

    # For reporting
    report_rows = []

    # Prepare figure
    plt.figure(figsize=(11, 8))
    plt.style.use("default")

    # Background: mass field
    im = plt.pcolormesh(M_grid, L_grid, np.log1p(mass_map),
                        shading="auto", cmap="magma")
    cbar = plt.colorbar(im, label="log(1 + √λ1)  (vacuum stiffness)")

    # Mark apex
    plt.scatter([m0], [l0], marker="*", s=150, c="white", edgecolors="black",
                zorder=5)
    plt.text(m0+0.05, l0+0.05, "Needle apex", color="white")

    # For each candidate: compute local gradient & flow line
    for cid, species, m, l, a_mass in candidates:
        # Local mass and gradient
        local_mass = bilinear_interp(m, l, m_range, l_range, mass_map)
        g_m = bilinear_interp(m, l, m_range, l_range, dMass_dM)
        g_l = bilinear_interp(m, l, m_range, l_range, dMass_dL)

        # Direction toward apex
        vec_to_apex = np.array([m0 - m, l0 - l])
        r = np.hypot(*vec_to_apex)
        if r > 0:
            u_to_apex = vec_to_apex / r
            grad_vec = np.array([g_m, g_l])
            radial_component = np.dot(grad_vec, u_to_apex)
        else:
            radial_component = np.nan

        # Delta in mass between candidate and apex
        delta_mass = apex_mass - local_mass

        # Trace downhill flow
        m_path, l_path = trace_flow_from_point(
            m, l,
            m_range, l_range,
            dMass_dM, dMass_dL,
            step=0.02, n_steps=250
        )

        color = species_color[species]
        # Path
        plt.plot(m_path, l_path, color=color, alpha=0.9, linewidth=1.5)
        # Start point
        plt.scatter([m], [l], color=color, edgecolors="black",
                    s=60, zorder=6)
        plt.text(m+0.05, l+0.05,
                 f"{cid}",
                 color="white", fontsize=8, weight="bold")

        report_rows.append({
            "id": cid,
            "species": species,
            "m": m,
            "lam": l,
            "action_mass": a_mass,
            "local_mass": local_mass,
            "delta_to_apex": delta_mass,
            "radial_grad": radial_component,
            "distance_to_apex": r,
        })

    plt.xlabel("Mass field m")
    plt.ylabel("Coupling field λ")
    plt.title("Needle Impact on Particle Candidates\n"
              "(background = vacuum mass eigenvalue, curves = downhill flow)")

    plt.tight_layout()
    plt.savefig("needle_impact_map.png", dpi=200)
    print("\nSaved figure: needle_impact_map.png")

    # Text report
    print("\n===== Needle Impact Report =====")
    print("ID | Sp | (m, λ)        | dist_to_apex | local_mass | Δmass(apex-local) | radial_grad")
    print("-------------------------------------------------------------------------------")
    for row in report_rows:
        print(f"{row['id']:2d} | {row['species'][:1]:2s} | "
              f"({row['m']:6.2f},{row['lam']:6.2f}) | "
              f"{row['distance_to_apex']:11.3f} | "
              f"{row['local_mass']:10.3f} | "
              f"{row['delta_to_apex']:15.3f} | "
              f"{row['radial_grad']:11.3f}")

if __name__ == "__main__":
    main()
