
import math, numpy as np
from dataclasses import dataclass
from typing import Callable, Optional, Tuple, Dict

HBARC_MEV_FM = 197.3269804

@dataclass
class ClosureInputs:
    # Solver-side
    phi_star: float                 # plateau center
    Delta_phi_eff: float            # effective plateau width from solver (binding result)
    chi: float = 1.0                # susceptibility factor (can be left 1.0 initially)
    # Optional existing lattice outputs for comparison/calibration
    sqrt_sigma_lattice: Optional[float] = None
    r0_lattice: Optional[float] = None
    a_lattice: Optional[float] = None
    # Physical calibration target
    target_sqrt_sigma_MeV: float = 440.0

def omega_c_from_phi_star(phi_star: float) -> float:
    return 1.0/phi_star

def xi_gamma(omega_c: float, Delta_phi_eff: float, chi: float=1.0) -> float:
    # natural units (ħ=c=1)
    return (chi**-0.5) / (omega_c * Delta_phi_eff)

def kappa3_from_curvature(omega_c: float, phi_star: float, curvature: float) -> float:
    # kappa3 ~ (omega_c/phi_star)^2 * curvature  (ħ=1)
    return (omega_c/phi_star)**2 * curvature

def sigma_from_components(kappa3_val: float, xi_gamma_val: float) -> float:
    return kappa3_val / (xi_gamma_val**2)

# -------- curvature extraction --------
def curvature_from_callable(H_phi: Callable[[float], float], phi_star: float, h: float=1e-3) -> float:
    fph = H_phi(phi_star + h)
    fmh = H_phi(phi_star - h)
    f0  = H_phi(phi_star)
    return (fph - 2.0*f0 + fmh)/(h*h)

def curvature_from_samples(phi_vals: np.ndarray,
                           H_vals: np.ndarray,
                           phi_star: float,
                           window: float=0.02) -> float:
    """
    Fit a local quadratic H ≈ a*(phi-phi*)^2 + b*(phi-phi*) + c
    in a small window around phi_star; curvature is 2*a.
    """
    d = np.abs(phi_vals - phi_star)
    mask = d <= window
    if mask.sum() < 5:
        # if too few points, expand window
        order = np.argsort(d)
        sel = order[:max(5, int(0.1*len(order)))]
        x = phi_vals[sel] - phi_star
        y = H_vals[sel]
    else:
        x = phi_vals[mask] - phi_star
        y = H_vals[mask]
    # quadratic fit
    X = np.vstack([x**2, x, np.ones_like(x)]).T
    a, b, c = np.linalg.lstsq(X, y, rcond=None)[0]
    return 2.0*a

# -------- calibration --------
def calibrate_mass_and_length(sqrt_sigma_lattice: float,
                              target_sqrt_sigma_MeV: float=440.0) -> tuple[float, float]:
    """
    Returns (mass_scale_MeV_per_lattice_unit, length_unit_fm_per_lattice_unit).
    """
    mass_scale = target_sqrt_sigma_MeV / sqrt_sigma_lattice
    length_unit = HBARC_MEV_FM / mass_scale
    return mass_scale, length_unit

# -------- end-to-end pipeline --------
def option_c_closure_end2end(inputs: ClosureInputs,
                             curvature: Optional[float]=None,
                             H_phi: Optional[Callable[[float], float]]=None,
                             sample_data: Optional[tuple[np.ndarray, np.ndarray]]=None
                             ) -> Dict:
    """
    Provide either:
      - curvature directly, OR
      - H_phi callable, OR
      - sample_data = (phi_vals, H_vals)
    to extract curvature. Then compute xi_Gamma, kappa3, sigma, sqrt_sigma.
    If sqrt_sigma_lattice is given, perform physical calibration.
    """
    # 1) omega_c and xi_Gamma
    omega_c = omega_c_from_phi_star(inputs.phi_star)
    xiG = xi_gamma(omega_c, inputs.Delta_phi_eff, inputs.chi)

    # 2) curvature
    if curvature is None:
        if H_phi is not None:
            curvature = curvature_from_callable(H_phi, inputs.phi_star)
        elif sample_data is not None:
            phi_vals, H_vals = sample_data
            curvature = curvature_from_samples(phi_vals, H_vals, inputs.phi_star)
        else:
            raise ValueError("Provide curvature, or H_phi callable, or (phi_vals, H_vals) samples.")

    # 3) kappa3 and sigma
    k3 = kappa3_from_curvature(omega_c, inputs.phi_star, curvature)
    sigma_val = sigma_from_components(k3, xiG)
    sqrt_sigma_lat = math.sqrt(sigma_val)

    out = {
        "inputs": vars(inputs),
        "derived_lattice": {
            "omega_c": omega_c,
            "xi_Gamma": xiG,
            "curvature": curvature,
            "kappa3": k3,
            "sigma": sigma_val,
            "sqrt_sigma": sqrt_sigma_lat,
        },
        "calibration": None,
        "converted": None,
    }

    # 4) calibration (optional)
    if inputs.sqrt_sigma_lattice is not None:
        mass_scale = inputs.target_sqrt_sigma_MeV / inputs.sqrt_sigma_lattice
        length_unit = HBARC_MEV_FM / mass_scale
        converted = {}
        if inputs.r0_lattice is not None:
            converted["r0_fm"] = inputs.r0_lattice * length_unit
        if inputs.a_lattice is not None:
            converted["a_fm"] = inputs.a_lattice * length_unit
        out["calibration"] = {
            "mass_scale_MeV_per_unit": mass_scale,
            "length_unit_fm": length_unit
        }
        out["converted"] = converted

    return out
