#!/usr/bin/env python
"""
prototron_orbit_carver.py

Third view of the Pirouette manifold:
- Instead of scanning initial conditions once (basins) or probing shoreline tension
  (Lyapunov), we inject three "prototrons" and let their orbits carve a density web.
- The resulting trail density can be compared directly to:
    * The entropy anchor / retro spiderweb (stability skeleton)
    * The forward Lyapunov tension map (shock cones / jets)

This is deliberately lightweight and self-contained.
"""

import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------
# 1. Hénon-Heiles potential and dynamics
# ----------------------------------------

def henon_heiles_potential(x, y):
    """
    Standard Hénon–Heiles potential (same form as your other scripts):
        V(x,y) = 0.5*(x^2 + y^2) + x^2*y - (1/3)*y^3
    Escape energy is E_escape = 1/6 ≈ 0.1667.
    """
    return 0.5 * (x**2 + y**2) + x**2 * y - (y**3) / 3.0

def henon_heiles_force(x, y):
    """
    Force = -∇V.
    """
    dVdx = x + 2.0 * x * y          # ∂V/∂x
    dVdy = y + x**2 - y**2          # ∂V/∂y
    return -dVdx, -dVdy

def leapfrog_step(x, y, px, py, dt):
    """
    Simple symplectic (leapfrog / velocity Verlet) integrator step.

    State variables:
        x, y   : positions
        px, py : conjugate momenta (velocities, since m = 1)
        dt     : timestep
    """
    # Half-kick (update momenta by half-step)
    fx, fy = henon_heiles_force(x, y)
    px_half = px + 0.5 * dt * fx
    py_half = py + 0.5 * dt * fy

    # Drift (update positions by full step with half-step momenta)
    x_new = x + dt * px_half
    y_new = y + dt * py_half

    # Second half-kick
    fx_new, fy_new = henon_heiles_force(x_new, y_new)
    px_new = px_half + 0.5 * dt * fx_new
    py_new = py_half + 0.5 * dt * fy_new

    return x_new, y_new, px_new, py_new

# ----------------------------------------
# 2. Prototron initialization
# ----------------------------------------

def init_prototrons(E_target=0.14):
    """
    Initialize three "prototrons" inside the well.
    
    FIX: We scale the positions inward (x0.6) to ensure the local 
    Potential Energy is lower than the Target Energy (E_target).
    This gives them positive velocity to start carving the web.
    """
    # Normalized directions toward the 3 corners
    # Top, Bottom-Right, Bottom-Left
    base_positions = np.array([
        [ 0.0,  1.0],   
        [ 0.866, -0.5],   
        [-0.866, -0.5],   
    ], dtype=float)

    # Scale inward so they start safely inside the potential well
    # At 0.6 scale, Potential is low enough for E=0.14 to work.
    scale_factor = 0.6 
    positions = base_positions * scale_factor

    momenta = []

    for (x0, y0) in positions:
        V0 = henon_heiles_potential(x0, y0)
        kinetic = E_target - V0
        
        # Safety check to prevent the crash you saw
        if kinetic <= 0:
            # Fallback: if specific spot is too high, push closer to center
            print(f"Warning: Adjusting position for {x0},{y0} to gain energy.")
            x0 *= 0.8
            y0 *= 0.8
            V0 = henon_heiles_potential(x0, y0)
            kinetic = E_target - V0

        p_mag = np.sqrt(2.0 * kinetic)

        # Calculate tangential direction for stable orbit injection
        r = np.sqrt(x0**2 + y0**2)
        if r == 0:
            ux, uy = 0.0, 1.0
        else:
            ux = x0 / r
            uy = y0 / r

        # Tangential vector (rotate 90 degrees)
        tx = -uy
        ty =  ux

        px0 = p_mag * tx
        py0 = p_mag * ty
        momenta.append([px0, py0])

    # Update positions array in case we did a fallback adjustment
    # (Though with scale_factor=0.6, fallback shouldn't trigger)
    return positions, np.array(momenta)


# ----------------------------------------
# 3. Orbit carving
# ----------------------------------------

def carve_orbits(
    n_steps=200_000,
    dt=0.01,
    bounds=1.5,
    res=1200,
    E_target=0.14,
    blur_sigma=1.0,
):
    """
    Run three prototrons through the Hénon–Heiles potential, accumulate trail density
    on an (M,L) grid.

    Parameters
    ----------
    n_steps : int
        Number of integration steps.
    dt : float
        Timestep.
    bounds : float
        Grid half-extent in both x and y: [-bounds, bounds]^2.
    res : int
        Grid resolution in each dimension.
    E_target : float
        Total energy for each prototron (must be below escape threshold 1/6).
    blur_sigma : float
        Optional Gaussian blur applied to the density (in pixels).
        Set <= 0 to skip.

    Returns
    -------
    density : 2D array
        Normalized trail density (sum over all prototrons).
    """

    # Initialize prototrons
    positions, momenta = init_prototrons(E_target=E_target)
    x = positions[:, 0].copy()
    y = positions[:, 1].copy()
    px = momenta[:, 0].copy()
    py = momenta[:, 1].copy()

    # Histogram grid
    density = np.zeros((res, res), dtype=np.float64)

    # Precompute mapping factors
    scale = (res - 1) / (2.0 * bounds)

    for step in range(n_steps):
        # Integrate each prototron one leapfrog step
        for i in range(3):
            x[i], y[i], px[i], py[i] = leapfrog_step(x[i], y[i], px[i], py[i], dt)

        # Deposit into histogram
        for i in range(3):
            xi, yi = x[i], y[i]
            if abs(xi) <= bounds and abs(yi) <= bounds:
                ix = int((xi + bounds) * scale)
                iy = int((yi + bounds) * scale)
                density[iy, ix] += 1.0

        # Optional: occasionally print progress
        if (step + 1) % 50000 == 0:
            print(f"[{step+1}/{n_steps}] max density = {density.max():.1f}")

    # Normalize
    if density.max() > 0:
        density /= density.max()

    # Optional blur
    if blur_sigma > 0:
        try:
            from scipy.ndimage import gaussian_filter
            density = gaussian_filter(density, blur_sigma)
            density /= density.max()
        except ImportError:
            print("SciPy not available, skipping blur.")

    return density


# ----------------------------------------
# 4. Visualization
# ----------------------------------------

def plot_density(density, bounds=1.5, cmap="magma"):
    res = density.shape[0]
    extent = (-bounds, bounds, -bounds, bounds)

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    # Linear density
    ax = axes[0]
    im0 = ax.imshow(
        density,
        origin="lower",
        extent=extent,
        cmap=cmap,
        interpolation="bilinear",
    )
    ax.set_title("Prototron Trail Density (linear)")
    ax.set_xlabel("M (lateral)")
    ax.set_ylabel("L (axial)")
    fig.colorbar(im0, ax=ax, fraction=0.046, pad=0.04)

    # Log density
    ax = axes[1]
    logd = np.log10(density + 1e-6)
    im1 = ax.imshow(
        logd,
        origin="lower",
        extent=extent,
        cmap=cmap,
        interpolation="bilinear",
    )
    ax.set_title("Prototron Trail Density (log10)")
    ax.set_xlabel("M (lateral)")
    ax.set_ylabel("L (axial)")
    fig.colorbar(im1, ax=ax, fraction=0.046, pad=0.04)

    plt.suptitle("Orbit-Carved Web from Three Prototrons", fontsize=14)
    plt.tight_layout()
    plt.show()


def main():
    # Parameters tuned to give nicely tangled orbits but stay bounded.
    bounds = 1.5
    res = 1200
    n_steps = 200_000
    dt = 0.01
    E_target = 0.14    # just below 1/6 escape

    density = carve_orbits(
        n_steps=n_steps,
        dt=dt,
        bounds=bounds,
        res=res,
        E_target=E_target,
        blur_sigma=1.0,
    )
    plot_density(density, bounds=bounds, cmap="viridis")


if __name__ == "__main__":
    main()
