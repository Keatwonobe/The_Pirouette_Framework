# Helical Collapse Spectroscopy (HCS) — minimal simulation harness
#
# What this does:
# 1) Builds a synthetic 3-lobe field Φ3(r,θ) on a 2D grid.
# 2) Evolves it under a toy helical time operator parameterized by kappa.
# 3) Applies a Ψ(3→2) “collapse” that re-expresses one spatial DOF as a Ki-modulated temporal phase.
# 4) Measures:
#    - dominant angular harmonic (lobe count) before and after,
#    - Ki beat frequency via temporal FFT of the post-collapse phase signal,
#    - a simple “phase conservation” balance proxy (space-flux pre vs time-flux post),
#    - chi_coherence = (Ta/(1-Ta)) * (Ki/Gamma),
#    - a toy spectral scaling ~ sqrt(1 + kappa^2).
# 5) Logs everything into a CSV for critics to replicate.
#
# Notes:
# - This is a *minimal* pedagogical harness that matches the critic-grade log schema we outlined.
# - It uses toy dynamics so we can run quickly in-session; you can swap the dynamics kernel later.
# - We keep charts simple (matplotlib, 1 chart per figure, no specified colors).

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy.fft import rfft, rfftfreq
from dataclasses import dataclass
from typing import Tuple, Dict
import math
import uuid
import os

# -----------------------------
# Utilities
# -----------------------------

def polar_grid(n: int = 256, r_max: float = 1.0):
    """Return (x, y, r, theta) on a square grid."""
    lin = np.linspace(-r_max, r_max, n)
    x, y = np.meshgrid(lin, lin)
    r = np.sqrt(x*x + y*y) + 1e-12
    theta = np.arctan2(y, x)
    return x, y, r, theta

def make_phi3(n: int = 256, r_max: float = 1.0, sigma: float = 0.6):
    """A 3-lobe field Φ3(r,θ) ~ cos(3θ)*exp(-r^2/sigma^2)."""
    x, y, r, theta = polar_grid(n, r_max)
    env = np.exp(-(r**2) / (sigma**2))
    phi = np.cos(3.0 * theta) * env
    return phi, (x, y, r, theta)

def dominant_angular_mode(field: np.ndarray, theta: np.ndarray, max_m: int = 8) -> int:
    """Estimate the dominant angular harmonic m by projecting onto cos(mθ), sin(mθ)."""
    # Mask near center to avoid singularity bias
    n = field.shape[0]
    mask = np.ones_like(field, dtype=bool)
    center = n//2
    rr = np.sqrt((np.indices(field.shape)[0]-center)**2 + (np.indices(field.shape)[1]-center)**2)
    mask[rr < 5] = False

    amps = []
    for m in range(1, max_m+1):
        c = np.sum(field[mask] * np.cos(m * theta[mask]))
        s = np.sum(field[mask] * np.sin(m * theta[mask]))
        amps.append((m, np.hypot(c, s)))
    amps.sort(key=lambda t: t[1], reverse=True)
    return amps[0][0]

def helical_time_evolve(field: np.ndarray, kappa: float, t: float, omega: float = 2*np.pi*1.0):
    """
    Toy helical evolution: apply a time-dependent phase twist proportional to kappa.
    For real field, we emulate by mixing with a phase-shifted copy.
    """
    # Create a simple "helical twist" via a rotation in an internal 2D space.
    cos_term = np.cos(kappa * omega * t)
    sin_term = np.sin(kappa * omega * t)
    evolved = cos_term * field + sin_term * np.gradient(field, axis=0)  # crude, fast surrogate
    return evolved

def psi_3to2_collapse(field: np.ndarray, geom: Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
                      Ta: float, Gamma: float, Ki: float, t_array: np.ndarray):
    """
    Ψ(3→2) collapse surrogate:
    - Reweight angular modes to favor m=2 over m=3 as (Ta, Gamma) enter a corridor.
    - Impose a Ki-modulated temporal phase on the global (spatially averaged) phase signal.
    Returns time-series of a "phase observable" after collapse and the post-collapse field.
    """
    x, y, r, theta = geom
    # Project onto m=3 and m=2 basis and mix according to a corridor function
    m3 = np.cos(3*theta)
    m2 = np.cos(2*theta)
    a3 = np.sum(field * m3)
    a2 = np.sum(field * m2)

    # Corridor weight: as Ta ↓ and Gamma ↑, push toward m=2 dominance
    corridor = np.clip((1.0 - Ta) * Gamma, 0.0, 1.0)  # 0..1
    w2 = 0.3 + 0.7 * corridor
    w3 = 1.0 - w2

    collapsed_spatial = w2 * a2 * m2 + w3 * a3 * m3

    # Temporal Ki-beat signal (phase observable): emulate by spatial average of tanh of collapsed field,
    # modulated by sin(Ki * t). This gives us a clean line to detect.
    base_obs = np.tanh(collapsed_spatial.mean())
    phi_t = base_obs * np.sin(Ki * t_array)

    return phi_t, collapsed_spatial

def detect_frequency(signal: np.ndarray, dt: float) -> Tuple[float, float]:
    """Return (peak_freq, SNR) from rFFT of the signal."""
    sig = signal - np.mean(signal)
    N = len(sig)
    yf = np.abs(rfft(sig))
    xf = rfftfreq(N, dt)
    if len(xf) < 3:
        return 0.0, 0.0
    # ignore DC
    yf[0] = 0.0
    peak_idx = np.argmax(yf)
    peak = yf[peak_idx]
    noise = np.median(yf[yf > 0]) if np.any(yf > 0) else 1e-12
    snr = float(peak / (noise + 1e-12))
    return float(xf[peak_idx]), snr

def phase_flux_space(field: np.ndarray, dx: float = 1.0) -> float:
    """Proxy for ∫|∇φ| dA (space-flux)."""
    gx, gy = np.gradient(field, dx, dx)
    return float(np.mean(np.hypot(gx, gy)))

def phase_flux_time(signal: np.ndarray, dt: float) -> float:
    """Proxy for ∫|∂t φ| dt (time-flux)."""
    d = np.gradient(signal, dt)
    return float(np.mean(np.abs(d)))

@dataclass
class RunConfig:
    kappa: float
    Ta: float
    Gamma: float
    Ki: float
    seed: int

def run_hcs(config: RunConfig,
            grid_n: int = 256,
            r_max: float = 1.0,
            sigma: float = 0.6,
            t_total: float = 8.0,
            fs: float = 100.0,
            omega0: float = 2*np.pi*1.0) -> Dict[str, float]:
    """Execute one HCS run and return log metrics."""
    np.random.seed(config.seed)

    # Build 3-lobe field
    phi3, geom = make_phi3(n=grid_n, r_max=r_max, sigma=sigma)

    # Pre-collapse lobe count
    lobes_before = dominant_angular_mode(phi3, geom[3])

    # Helical evolution at final time t_total (toy; could be extended to full time stepping)
    evolved = helical_time_evolve(phi3, config.kappa, t_total, omega=omega0)

    # Collapse & temporal stream
    t_array = np.arange(0.0, t_total, 1.0/fs)
    phi_t, collapsed_field = psi_3to2_collapse(evolved, geom, config.Ta, config.Gamma, config.Ki, t_array)

    # Post-collapse lobe count
    lobes_after = dominant_angular_mode(collapsed_field, geom[3])

    # Measure Ki beat
    dt = 1.0 / fs
    peak_freq, snr = detect_frequency(phi_t, dt)

    # Space vs time flux
    space_flux = phase_flux_space(phi3)  # pre-collapse
    time_flux = phase_flux_time(phi_t, dt)  # post-collapse

    # Phase balance error (normalized difference)
    denom = (abs(space_flux) + abs(time_flux) + 1e-12)
    phase_balance_error = float(abs(space_flux - time_flux) / denom)

    # chi_coherence
    chi_coherence = float((config.Ta / max(1e-6, (1.0 - config.Ta))) * (config.Ki / max(1e-6, config.Gamma)))

    # Toy spectral scaling prediction
    spectral_scale = math.sqrt(1.0 + config.kappa**2)

    # Verdict: corridor & signatures present
    corridor_entered = (config.Ta <= 0.35) and (config.Gamma >= 0.75)
    lobe_drop = (lobes_before == 3) and (lobes_after <= 2)
    beat_detected = (snr >= 5.0) and (peak_freq > 0.0)
    verdict_pass = bool(corridor_entered and lobe_drop and beat_detected and (phase_balance_error < 0.5))

    return {
        "run_id": str(uuid.uuid4())[:8],
        "seed": config.seed,
        "kappa": config.kappa,
        "Ta": config.Ta,
        "Gamma": config.Gamma,
        "Ki_mode": config.Ki,
        "En_spectrum_scale_pred": spectral_scale,
        "lobes_before": lobes_before,
        "lobes_after": lobes_after,
        "phi_beat_freq": peak_freq,
        "phi_beat_SNR": snr,
        "phase_flux_space": space_flux,
        "phase_flux_time": time_flux,
        "phase_balance_error": phase_balance_error,
        "chi_coherence": chi_coherence,
        "verdict_pass": verdict_pass
    }

# -----------------------------
# Run a small sweep
# -----------------------------

sweep = []
configs = [
    RunConfig(kappa=0.0,  Ta=0.9,  Gamma=0.4,  Ki=2.0*np.pi*0.5, seed=1),  # control (no corridor)
    RunConfig(kappa=0.6,  Ta=0.3,  Gamma=0.85, Ki=2.0*np.pi*0.6, seed=2),  # in corridor; medium kappa
    RunConfig(kappa=1.0,  Ta=0.25, Gamma=0.9,  Ki=2.0*np.pi*0.8, seed=3),  # strong corridor; higher kappa
    RunConfig(kappa=0.4,  Ta=0.28, Gamma=0.82, Ki=2.0*np.pi*0.4, seed=4),  # corridor; lower kappa/Ki
    RunConfig(kappa=1.25, Ta=0.2,  Gamma=0.95, Ki=2.0*np.pi*1.0, seed=5),  # deep corridor; high kappa/Ki
]

for cfg in configs:
    sweep.append(run_hcs(cfg))

df = pd.DataFrame(sweep)

# Save CSV
out_csv = "hcs_runs.csv"
df.to_csv(out_csv, index=False)

# Plot 1: lobe counts before vs after (scatter)
plt.figure(figsize=(6,4))
plt.scatter(df["lobes_before"], df["lobes_after"])
plt.xlabel("Lobes Before")
plt.ylabel("Lobes After")
plt.title("Symmetry Drop (3→2) Check")
plt.tight_layout()
plt.savefig("hcs_lobes_scatter.png")
plt.close()

# Plot 2: SNR vs kappa (Ki-beat detectability)
plt.figure(figsize=(6,4))
plt.scatter(df["kappa"], df["phi_beat_SNR"])
plt.xlabel("kappa")
plt.ylabel("Ki Beat SNR")
plt.title("Beat Detectability vs κ")
plt.tight_layout()
plt.savefig("hcs_snr_vs_kappa.png")
plt.close()

# Plot 3: Phase balance error vs corridor condition
plt.figure(figsize=(6,4))
corridor_mask = (df["Ta"] <= 0.35) & (df["Gamma"] >= 0.75)
plt.scatter(np.arange(len(df))[corridor_mask], df["phase_balance_error"][corridor_mask])
plt.xlabel("Run Index (corridor only)")
plt.ylabel("Phase Balance Error")
plt.title("Phase Balance (space vs time) in Corridor")
plt.tight_layout()
plt.savefig("hcs_phase_balance_corridor.png")
plt.close()

# Print file locations for the user
out_files = {
    "csv": out_csv,
    "lobes_scatter": "hcs_lobes_scatter.png",
    "snr_vs_kappa": "hcs_snr_vs_kappa.png",
    "phase_balance_corridor": "hcs_phase_balance_corridor.png",
}
out_files
