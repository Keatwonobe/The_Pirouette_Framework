# -*- coding: utf-8 -*-
"""
Compass Criticality Scanner
---------------------------
Purpose: Detect geometric/spectral criticality in the Compass by sweeping a control
parameter (e.g., Δκ) and tracking non-analytic changes in order parameters.

How to integrate with your real explorer:
- Replace `toy_compass_fields()` with a function that returns (X, Y, zeta, E0, E1)
  for a given parameter dict. Shape: all arrays must be (Ny, Nx).
- Set `USE_TOY_MODEL=False` and implement `real_compass_fields(params)`.
- Choose `PARAM_NAME`, `PARAM_VALUES`, and `ZETA_LEVEL` to match your study.
- Run this script; it will write a CSV of metrics and produce a few plots.

Outputs:
- /mnt/data/criticality_scan.csv
- /mnt/data/criticality_derivative.png
- /mnt/data/criticality_topology.png
- /mnt/data/criticality_gap.png
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from typing import Dict, Tuple, List

# -------------------------
# 1) MODEL INTERFACE
# -------------------------

def toy_compass_fields(params: Dict[str, float],
                       Nx: int = 256,
                       Ny: int = 256) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    A small synthetic model that *mimics* a topology change and gap softening.
    This is just to demonstrate the pipeline end-to-end.

    Returns:
        X, Y: meshgrids (Ny, Nx)
        zeta: scalar field (Ny, Nx)
        E0, E1: pseudo "patch solver" eigenlevels (Ny, Nx)
    """
    # Domain
    x = np.linspace(-2.0, 2.0, Nx)
    y = np.linspace(-2.0, 2.0, Ny)
    X, Y = np.meshgrid(x, y)

    # Control knob ~ Δκ
    dk = params.get("d_kappa", 0.3)

    # A radial "bubble" whose radius changes with dk;
    # near dk ~ 0.5 the loop appears/disappears (topology change).
    r2 = X**2 + Y**2

    # Radius controlled by dk; critical around dk_c
    dk_c = 0.5
    radius2 = 0.75 + 2.0*(dk - dk_c)

    # Smooth wall thickness
    eps = 0.05

    # zeta level set is a smoothed indicator for r2 ~ radius2
    # This creates a ring-like contour whose existence depends on dk.
    zeta = np.tanh((radius2 - r2)/eps)

    # Fake spectral levels: soften near the ring when it exists, and soften more as dk approaches dk_c
    soften = np.exp(-((r2 - radius2)**2)/(2*(3*eps)**2))
    base0 = 0.4 + 0.1*np.sin(3*X)*np.cos(2*Y)
    base1 = 0.9 + 0.1*np.cos(4*X)*np.sin(2*Y)
    # Stronger softening when close to critical dk
    crit_weight = np.exp(-((dk - dk_c)**2)/(2*0.06**2))
    E0 = base0 - 0.35 * soften * crit_weight
    E1 = base1 - 0.10 * soften * crit_weight

    return X, Y, zeta, E0, E1


def real_compass_fields(params: Dict[str, float],
                        Nx: int = 256,
                        Ny: int = 256) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Computes the Compass potential, Zeta field, and energy levels based on the
    Pirouette framework implemented in the user's HTML explorer.
    """
    # --- Physical and Model Constants from your explorer ---
    HBAR = 1.054571817e-34  # J*s
    M_E = 9.1093837e-31      # kg
    LAMBDA_E_BAR = 3.8615926796e-13 # m (reduced Compton wavelength)
    E_S = params.get("E_s", 13.6) # Energy scale in eV, default to 13.6
    E_S_JOULES = E_S * 1.60218e-19 # Convert eV to Joules

    # --- Grid Setup ---
    extent = 14.0
    g_coords = np.linspace(-extent, extent, Nx)
    t_coords = np.linspace(-extent, extent, Ny)
    G, T = np.meshgrid(g_coords, t_coords) # G and T are the 2D arrays we need
    dx = (extent * 2) / (Nx - 1)
    dy = (extent * 2) / (Ny - 1)

    # --- Compass Potential (U) Calculation (translated from explorer_qho_zeta.html) ---
    R = np.hypot(G / params['gamma_scale'], T / params['ta_scale'])
    Theta = np.arctan2(T / params['ta_scale'], G / params['gamma_scale'])
    kap = params['kappa0'] * np.exp(-params['kappa_decay'] * R)
    G_env = np.exp(-(R**2) / (2.0 * params['sigma_r']**2))
    Theta_prime = Theta + kap * params['xi']
    winding_val = np.cos(2.0 * np.pi * params['n'] * Theta_prime / np.pi)
    kr = params['k_wave'] * R
    radial = np.sinc(kr / np.pi)
    ang = np.cos(Theta - params['theta0'])
    tpci_hint_val = radial * ang
    U = G_env * (1.0 + params['a_wind'] * winding_val + params['a_tpci'] * tpci_hint_val)

    # --- Calculate Derivatives for Zeta Components ---
    grad_T, grad_G = np.gradient(U, dy, dx)
    grad_U_mag = np.hypot(grad_G, grad_T)
    U_tt, U_gt = np.gradient(grad_T, dy, dx)
    U_tg, U_gg = np.gradient(grad_G, dy, dx)
    tr = -(U_gg + U_tt)
    det = U_gg * U_tt - U_gt * U_tg
    discriminant = np.sqrt(np.maximum(0, tr**2 - 4 * det))
    k1 = 0.5 * (tr - discriminant)
    k2 = 0.5 * (tr + discriminant)

    # --- Calculate Zeta Components (as per DYNA-008 (rev)) ---
    k_soft = np.maximum(k1, 1e-9)
    omega_c = np.sqrt((E_S_JOULES * k_soft) / (M_E * LAMBDA_E_BAR**2))
    density = 1.0 / (grad_U_mag + 1e-9)
    curvature = np.abs(U_gg) + np.abs(U_tt)
    kg_field = density * curvature
    kg_field = (kg_field - np.min(kg_field)) / (np.max(kg_field) - np.min(kg_field))
    Gamma = E_S_JOULES * (1.0 * grad_U_mag + 0.5 * LAMBDA_E_BAR * curvature + 1.0 * kg_field)
    delta_kappa = params['delta_kappa']
    zeta = (delta_kappa * Gamma) / (HBAR * omega_c)

    # --- Energy Level Proxy (as per QHO approximation) ---
    E0 = -U
    E1 = E0 + HBAR * omega_c

    # This is the corrected line: return the 2D meshgrids G and T
    return G, T, zeta, E0, E1

def compute_fields(params: Dict[str, float],
        Nx: int = 256,
        Ny: int = 256) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    return real_compass_fields(params, Nx=Nx, Ny=Ny)


# -------------------------
# 2) GEOMETRY / TOPOLOGY HELPERS
# -------------------------

def contour_paths(X: np.ndarray, Y: np.ndarray, F: np.ndarray, level: float) -> List[np.ndarray]:
    """
    Extract level-set polygons using matplotlib's contour machinery.
    Returns a list of (N_i, 2) arrays of vertices.
    """
    # Use a throwaway figure in headless mode
    fig = plt.figure()
    try:
        cs = plt.contour(X, Y, F, levels=[level])
        paths = []
        for c in cs.collections:
            for p in c.get_paths():
                v = p.vertices  # (N,2)
                paths.append(v.copy())
    finally:
        plt.close(fig)
    return paths


def total_length(paths: List[np.ndarray]) -> float:
    length = 0.0
    for P in paths:
        diffs = np.diff(P, axis=0)
        length += np.sum(np.sqrt((diffs**2).sum(axis=1)))
    return float(length)


# -------------------------
# 3) CRITICALITY METRICS
# -------------------------

# -------------------------
# 3) ANALYSIS & SCANNING
# -------------------------

# -------------------------
# 3) ANALYSIS & SCANNING
# -------------------------

def scan_parameter(
    field_generator: callable,
    base_params: Dict[str, float],
    param_name: str,
    param_values: np.ndarray,
    zeta_level: float = 1.0,
    Nx: int = 256,
    Ny: int = 256
) -> pd.DataFrame:
    """
    Sweeps a parameter, computes fields, and extracts metrics for each value.
    This version is upgraded with physically correct gap, loop length, and sigma_tau.
    """
    results = []
    # Find contours using scikit-image
    from skimage.measure import find_contours

    for i, value in enumerate(param_values):
        print(f"  -> Scanning {param_name} = {value:.4f} ({i+1}/{len(param_values)})")
        current_params = base_params.copy()
        current_params[param_name] = value

        G, T, zeta, E0, E1 = field_generator(current_params, Nx, Ny)
        
        # --- FIX 1: Correct Energy Gap Calculation ---
        gap = E1 - E0 # The gap is the difference E1 - E0
        stay_mask = zeta < zeta_level
        
        min_gap = np.nan
        mean_gap = np.nan
        if np.any(stay_mask):
            gvals = gap[stay_mask]
            min_gap = float(np.nanmin(gvals))
            mean_gap = float(np.nanmean(gvals))

        # --- FIX 2 & 3: World-Unit Loop Length and Robust Sigma_Tau ---
        dG = G[0,1] - G[0,0]
        dT = T[1,0] - T[0,0]
        
        # Gradient of Zeta for the new sigma_tau calculation
        dz_dT, dz_dG = np.gradient(zeta, dT, dG)
        gradmag = np.sqrt(dz_dG**2 + dz_dT**2)

        # Find contours in pixel coordinates
        contours_pix = find_contours(zeta, zeta_level)
        
        sigma_tau = 0.0
        loop_length = 0.0
        
        for contour_pix in contours_pix:
            # Convert pixel coordinates to world coordinates (G, T)
            contour_world = contour_pix * np.array([dT, dG]) + np.array([T[0,0], G[0,0]])
            
            # Calculate arc length in world units
            dP = np.diff(contour_world, axis=0)
            seglen = np.sqrt((dP**2).sum(axis=1))
            loop_length += float(seglen.sum())

            # Sample |∇ζ| at each point on the contour
            # Convert world coords back to nearest grid index to sample gradmag
            Ti = np.clip(np.round(contour_pix[:, 0]).astype(int), 0, Ny - 1)
            Gi = np.clip(np.round(contour_pix[:, 1]).astype(int), 0, Nx - 1)
            g_samples = gradmag[Ti, Gi]
            
            # Integrate using the trapezoidal rule for better accuracy
            if len(seglen) > 0:
                sigma_tau += float(np.sum(0.5 * (g_samples[:-1] + g_samples[1:]) * seglen))

        results.append({
            "value": value,
            "components": len(contours_pix),
            "loop_length": loop_length,
            "sigma_tau": sigma_tau,
            "min_gap": min_gap,
            "mean_gap": mean_gap, # Add mean_gap to results
        })

    df = pd.DataFrame(results)
    # Calculate finite-difference derivatives
    df = df.sort_values(by="value").reset_index(drop=True)
    # Add mean_gap to the list of columns to differentiate
    for col in ["loop_length", "sigma_tau", "min_gap", "mean_gap"]:
        df[f"d_{col}"] = df[col].diff() / df["value"].diff()

    return df


# -------------------------
# 4) SCRIPT EXECUTION
# -------------------------
if __name__ == "__main__":

    
    # Define the full set of parameters for your real model
    # These values are taken as defaults from your explorer HTML files
    MODEL_PARAMS = {
        'n': 0.5, 'gamma_scale': 47.5, 'ta_scale': 47.5,
        'sigma_r': 7.0, 'a_wind': 0.35, 'a_tpci': 0.25,
        'k_wave': 0.45, 'theta0': 0.0, 'kappa0': 0.06,
        'kappa_decay': 0.08, 'xi': 0.8, 'E_s': 13.6,
        'delta_kappa': 0.3 # This will be swept
    }
        # Specify which function to use
    field_generator = real_compass_fields

    # --- Scan Configuration ---
    # We are scanning the Chiral Differential (delta_kappa) as you did manually
    PARAM_NAME = "delta_kappa"
    # Scan from 0.2 to 0.4 to capture the critical point around 0.3
    PARAM_VALUES = np.linspace(0.275, 0.3, 201)
    # Define the critical zeta level for contour analysis
    ZETA_LEVEL = 1.0

    print(f"Scanning parameter '{PARAM_NAME}' from {PARAM_VALUES[0]:.2f} to {PARAM_VALUES[-1]:.2f}")
    df = scan_parameter(
        field_generator,
        MODEL_PARAMS,
        PARAM_NAME,
        PARAM_VALUES,
        zeta_level=ZETA_LEVEL,
        Nx=256,
        Ny=256
    )
    csv_path = "pirouette_criticality_scan_tiny.csv"
    df.to_csv(csv_path, index=False)
    print(f"Scan complete. Results saved to {csv_path}")
    # -------------------------
    # 5) PLOTS
    # -------------------------

    # Derivative-based alerts
    # --- Plotting ---
    print("Generating plots...")

    # Derivative-based alerts
    plt.figure(figsize=(10, 6))
    plt.plot(df["value"], df["d_loop_length"], label="d(loop_length)/dκ", marker='.')
    plt.plot(df["value"], df["d_sigma_tau"], label="d(σ_τ)/dκ", marker='.')
    # Plot the derivative of the MEAN gap
    plt.plot(df["value"], df["d_mean_gap"], label="d(mean_gap)/dκ", marker='.')
    plt.axvline(x=df.loc[df['d_sigma_tau'].abs().idxmax(), 'value'], color='r', linestyle='--', label=f'Max Criticality at κ={df.loc[df["d_sigma_tau"].abs().idxmax(), "value"]:.4f}')
    plt.xlabel(f"Parameter: {PARAM_NAME}")
    plt.ylabel("Derivative of Metric")
    plt.title("Criticality Indicators (Derivatives)")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    deriv_plot = "criticality_derivative_tiny.png"
    plt.savefig(deriv_plot, dpi=160, bbox_inches="tight")
    plt.close()
    print(f"Saved derivative plot to {deriv_plot}")

    # Topology (components & loop length)
    plt.figure(figsize=(10, 6))
    plt.plot(df["value"], df["components"], marker="o", linestyle='--', label="Connected Components")
    plt.xlabel(f"Parameter: {PARAM_NAME}")
    plt.ylabel("Count of ζ=1 Contours")
    plt.title("Topological Transition vs. Parameter")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    topo_plot = "criticality_topology_tiny.png"
    plt.savefig(topo_plot, dpi=160, bbox_inches="tight")
    plt.close()
    print(f"Saved topology plot to {topo_plot}")

    # Energetics (gap)
    plt.figure(figsize=(10, 6))
    # Corrected this line to plot the MEAN gap
    plt.plot(df["value"], df["mean_gap"], marker=".", label="Mean Energy Gap in 'Stay' region")
    plt.xlabel(f"Parameter: {PARAM_NAME}")
    plt.ylabel("Mean Energy Gap (proxy, Joules)")
    plt.title("Energetics vs. Parameter")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    gap_plot = "criticality_gap_tiny.png"
    plt.savefig(gap_plot, dpi=160, bbox_inches="tight")
    plt.close()
    print(f"Saved energetics plot to {gap_plot}")
    print("\nAll plots saved.")

