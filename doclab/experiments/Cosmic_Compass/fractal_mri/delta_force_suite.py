import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Tuple, Dict, Optional
from scipy.ndimage import binary_dilation


# =========================
#   HÉNON–HEILES DYNAMICS
# =========================

def henon_heiles_grad(m: np.ndarray, l: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Gradient of the Hénon–Heiles potential:
        V = 1/2 (m^2 + l^2) + m^2 l - (1/3) l^3
    """
    dV_dm = m + 2.0 * m * l
    dV_dl = l + (m ** 2 - l ** 2)
    return dV_dm, dV_dl


def leapfrog_step(m, l, pm, pl, dt):
    """
    Single symplectic leapfrog step.
    """
    dV_dm, dV_dl = henon_heiles_grad(m, l)

    # half-kick
    pm -= 0.5 * dt * dV_dm
    pl -= 0.5 * dt * dV_dl

    # drift
    m += dt * pm
    l += dt * pl

    # second half-kick
    dV_dm, dV_dl = henon_heiles_grad(m, l)
    pm -= 0.5 * dt * dV_dm
    pl -= 0.5 * dt * dV_dl

    return m, l, pm, pl


# =========================
#   CONFIG / STRUCTS
# =========================

@dataclass
class PortConfig:
    name: str
    saddle_m: float
    saddle_l: float
    direction: str       # "up" (top) or "down" (bottom jets)
    halfspan_m: float = 0.5
    halfspan_l: float = 0.5


PORTS = [
    PortConfig("Top Port",          0.0,               1.0,  "up"),
    PortConfig("Bottom-Right Port", np.sqrt(3)/2.0,   -0.5,  "down"),
    PortConfig("Bottom-Left Port", -np.sqrt(3)/2.0,   -0.5,  "down"),
]


# =========================
#   SLICE / MRI ROUTINES
# =========================

def slice_escape_time(port: PortConfig,
                      resolution: int = 400,
                      dt: float = 0.03,
                      max_steps: int = 4000,
                      escape_radius2: float = 20.0):
    """
    Compute escape time for a window around a given port.
    Returns m_range, l_range, escape_time (shape [res, res]).
    """
    m_range = np.linspace(port.saddle_m - port.halfspan_m,
                          port.saddle_m + port.halfspan_m, resolution)
    l_range = np.linspace(port.saddle_l - port.halfspan_l,
                          port.saddle_l + port.halfspan_l, resolution)

    M, L = np.meshgrid(m_range, l_range)
    m = M.copy()
    l = L.copy()
    pm = np.zeros_like(M)
    pl = np.zeros_like(L)

    escape_time = np.zeros_like(M, dtype=np.float32)
    active = np.ones_like(M, dtype=bool)

    for step in range(max_steps):
        if not np.any(active):
            break

        m[active], l[active], pm[active], pl[active] = leapfrog_step(
            m[active], l[active], pm[active], pl[active], dt
        )

        r2 = m**2 + l**2
        escaped_now = (r2 > escape_radius2) & active
        if np.any(escaped_now):
            escape_time[escaped_now] = (step + 1) * dt
            active[escaped_now] = False

    # Anything still active did not escape in time → treat as "bound" with max time
    escape_time[active] = max_steps * dt
    return m_range, l_range, escape_time


def slice_lyapunov(port: PortConfig,
                   resolution: int = 400,
                   dt: float = 0.03,
                   max_steps: int = 4000,
                   escape_radius2: float = 20.0,
                   eps: float = 1e-5):
    """
    Finite-time Lyapunov 'tension' map around the port.
    Uses a single shadow trajectory per grid cell, separated by eps along m.
    Returns m_range, l_range, lyap_exponent[res,res].
    """
    m_range = np.linspace(port.saddle_m - port.halfspan_m,
                          port.saddle_m + port.halfspan_m, resolution)
    l_range = np.linspace(port.saddle_l - port.halfspan_l,
                          port.saddle_l + port.halfspan_l, resolution)

    M, L = np.meshgrid(m_range, l_range)

    # primary and shadow
    m = M.copy()
    l = L.copy()
    pm = np.zeros_like(M)
    pl = np.zeros_like(L)

    m_s = M.copy() + eps
    l_s = L.copy()
    pm_s = np.zeros_like(M)
    pl_s = np.zeros_like(L)

    active = np.ones_like(M, dtype=bool)
    lyap = np.zeros_like(M, dtype=np.float32)

    for step in range(max_steps):
        if not np.any(active):
            break

        # advance both
        m[active], l[active], pm[active], pl[active] = leapfrog_step(
            m[active], l[active], pm[active], pl[active], dt
        )
        m_s[active], l_s[active], pm_s[active], pl_s[active] = leapfrog_step(
            m_s[active], l_s[active], pm_s[active], pl_s[active], dt
        )

        # distance between nearby trajectories
        dm = m_s - m
        dl = l_s - l
        dist = np.sqrt(dm**2 + dl**2)

        # escape condition: once either copy escapes, we stop counting
        r2 = m**2 + l**2
        r2_s = m_s**2 + l_s**2
        escaped_now = ((r2 > escape_radius2) | (r2_s > escape_radius2)) & active

        # finite-time Lyapunov estimate at escape (or end)
        if np.any(escaped_now):
            lyap[escaped_now] = np.log(dist[escaped_now] / eps) / ((step+1) * dt)
            active[escaped_now] = False

    # For any still active, compute FTLE at the end
    remaining = active
    if np.any(remaining):
        dm = m_s - m
        dl = l_s - l
        dist = np.sqrt(dm**2 + dl**2)
        lyap[remaining] = np.log(dist[remaining] / eps) / (max_steps * dt)

    return m_range, l_range, lyap


# =========================
#   GEOMETRIC ANALYSIS
# =========================

def estimate_shock_lines(m_range, l_range, escape_time,
                         port: PortConfig,
                         bound_frac: float = 0.9) -> Dict[str, Optional[Tuple[float, float, float]]]:
    """
    Approximate the 'shock' boundary around the wedge as a straight line
    on each side (left/right) using linear regression.

    Returns a dict:
        side -> (slope_a, intercept_b, angle_deg_from_horizontal)
    where the line is m = a*l + b.
    """
    max_t = escape_time.max()
    bound = escape_time > bound_frac * max_t   # "black wedge" ≈ very long non-escape

    dilated = binary_dilation(bound)
    boundary = dilated & (~bound)

    M, L = np.meshgrid(m_range, l_range)

    if port.direction == "up":
        dir_mask = L > port.saddle_l
    else:
        dir_mask = L < port.saddle_l

    near_mask = (np.abs(L - port.saddle_l) < port.halfspan_l) & \
                (np.abs(M - port.saddle_m) < port.halfspan_m)

    pts_mask = boundary & dir_mask & near_mask
    ys, xs = np.where(pts_mask)

    results = {"left": None, "right": None}
    if len(xs) < 10:
        return results

    m_coords = m_range[xs]
    l_coords = l_range[ys]

    for side, cond in [
        ("left",  m_coords <= port.saddle_m),
        ("right", m_coords >= port.saddle_m),
    ]:
        idx = np.where(cond)[0]
        if len(idx) < 5:
            continue
        ms = m_coords[idx]
        ls = l_coords[idx]

        A = np.vstack([ls, np.ones_like(ls)]).T
        a, b = np.linalg.lstsq(A, ms, rcond=None)[0]

        # slope a = dM/dL; angle from horizontal (M-axis):
        # tan(theta) = dL/dM = 1/a  => theta = arctan(1/|a|)
        angle = np.degrees(np.arctan(1.0 / np.abs(a)))
        results[side] = (a, b, angle)

    return results


def estimate_axis_lyapunov(m_range, l_range, lyap_map, port: PortConfig,
                           n_samples: int = 40) -> float:
    """
    Sample Lyapunov exponent values along the jet axis (through the saddle)
    and return their mean. Axis defined as:
        - top port: line m = saddle_m, l > saddle_l
        - bottom ports: m = saddle_m, l < saddle_l
    """
    M, L = np.meshgrid(m_range, l_range)
    axis_mask = np.abs(M - port.saddle_m) < 0.01

    if port.direction == "up":
        axis_mask &= L > port.saddle_l
    else:
        axis_mask &= L < port.saddle_l

    ys, xs = np.where(axis_mask)
    if len(xs) == 0:
        return np.nan

    # sort along axial direction and pick at most n_samples
    order = np.argsort(l_range[ys])
    ys = ys[order][:n_samples]
    xs = xs[order][:n_samples]

    return float(np.nanmean(lyap_map[ys, xs]))


def escape_stats_near_saddle(m_range, l_range, escape_time,
                             port: PortConfig,
                             radius: float = 0.1):
    """
    Compute mean and std of escape times in a small disk around the saddle
    on the 'jet' side.
    """
    M, L = np.meshgrid(m_range, l_range)

    r2 = (M - port.saddle_m)**2 + (L - port.saddle_l)**2
    mask = r2 < radius**2

    if port.direction == "up":
        mask &= L > port.saddle_l
    else:
        mask &= L < port.saddle_l

    data = escape_time[mask]
    if data.size == 0:
        return np.nan, np.nan
    return float(data.mean()), float(data.std())


# =========================
#   DRIVER / FORCE TABLE
# =========================

def analyze_port(port: PortConfig,
                 resolution: int = 400,
                 dt: float = 0.03,
                 max_steps: int = 4000):
    print(f"\n=== Analyzing {port.name} ===")

    # Escape-time slice
    m_range, l_range, esc = slice_escape_time(
        port, resolution=resolution, dt=dt, max_steps=max_steps
    )

    # Lyapunov slice
    _, _, lyap = slice_lyapunov(
        port, resolution=resolution, dt=dt, max_steps=max_steps
    )

    # Shock angles
    shock = estimate_shock_lines(m_range, l_range, esc, port)

    # Axis Lyapunov exponent
    axis_lyap = estimate_axis_lyapunov(m_range, l_range, lyap, port)

    # Escape stats near saddle
    esc_mean, esc_std = escape_stats_near_saddle(m_range, l_range, esc, port)

    # Report
    print(f"  Axis Lyapunov exponent λ_axis ≈ {axis_lyap:.4g}")
    print(f"  Escape time near saddle: mean ≈ {esc_mean:.3g}, std ≈ {esc_std:.3g}")

    for side in ["left", "right"]:
        val = shock.get(side)
        if val is None:
            print(f"  {side.capitalize()} shock: [not enough data]")
        else:
            a, b, ang = val
            print(f"  {side.capitalize()} shock: m = {a:.3g} * l + {b:.3g}, "
                  f"angle from horizontal ≈ {ang:.2f}°")

    # Optional: return raw data if you want to plot
    return {
        "port": port,
        "m_range": m_range,
        "l_range": l_range,
        "escape": esc,
        "lyap": lyap,
        "shocks": shock,
        "axis_lyap": axis_lyap,
        "esc_mean": esc_mean,
        "esc_std": esc_std,
    }


def main():
    results = []
    for port in PORTS:
        res = analyze_port(port, resolution=400, dt=0.03, max_steps=4000)
        results.append(res)

    print("\n\n=== Δ-Force Table (rough) ===")
    print("Port\t\tλ_axis\t\t<t_escape>\tShockAngles(deg from horiz, L/R)")
    for res in results:
        p = res["port"]
        shock = res["shocks"]
        left_ang = shock["left"][2] if shock["left"] is not None else np.nan
        right_ang = shock["right"][2] if shock["right"] is not None else np.nan
        print(f"{p.name:16s}\t{res['axis_lyap']:.4g}\t"
              f"{res['esc_mean']:.3g}\t"
              f"{left_ang:.1f}, {right_ang:.1f}")

    # You can add plotting here if desired.


if __name__ == "__main__":
    main()
