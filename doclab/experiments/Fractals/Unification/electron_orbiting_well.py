"""
electron_orbit_on_manifold.py

Simulate an electron-like test particle moving on/over a Pirouette manifold.

- Input: regular grid X, Y, Z (e.g. from pirouette_macro_scan_6)
- Dynamics:   m d^2 r / dt^2 = - grad V(r) - gamma * v
  where V(x,y) is taken to be proportional to the manifold height Z(x,y).

Units are arbitrary; we're just probing geometry, not absolute scales.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 (needed for 3D)


class ManifoldPotential:
    """
    Wrap a regular grid (X, Y, Z) and provide:
      - V(x, y)
      - gradV(x, y) = (dV/dx, dV/dy)
    using bilinear interpolation on the grid and precomputed gradients.
    """

    def __init__(self, X, Y, Z, scale=1.0):
        """
        Parameters
        ----------
        X, Y : 2D ndarrays or 1D monotonic arrays
            Grid coordinates. If 2D (as from np.meshgrid), we infer the 1D axes.
        Z : 2D ndarray
            Height / potential values on the grid.
        scale : float
            Overall scaling for the potential V = scale * Z.
            Use this to tune how "deep" the wells feel.
        """
        X = np.asarray(X)
        Y = np.asarray(Y)
        Z = np.asarray(Z)

        # Allow both meshgrid-style and 1D axes
        if X.ndim == 2:
            self.x_axis = X[0, :]
        else:
            self.x_axis = X
        if Y.ndim == 2:
            self.y_axis = Y[:, 0]
        else:
            self.y_axis = Y

        self.Z = Z * scale

        # Precompute gradients on the grid for fast lookup
        # np.gradient expects (rows, cols) order = (y, x)
        dZ_dy, dZ_dx = np.gradient(self.Z, self.y_axis, self.x_axis, edge_order=2)
        self.dZ_dx = dZ_dx
        self.dZ_dy = dZ_dy

        # Cache ranges
        self.x_min, self.x_max = self.x_axis[0], self.x_axis[-1]
        self.y_min, self.y_max = self.y_axis[0], self.y_axis[-1]

    # ---------- low-level helpers ---------------------------------

    def _index_and_weights(self, x, y):
        """
        Map (x,y) in continuous coordinates to bilinear weights on the grid.

        Returns
        -------
        i0, i1, j0, j1 : int
            Indices in x (columns) and y (rows).
        wx, wy : float
            Interpolation weights in [0, 1].
        """
        # Clamp to domain (soft boundary)
        x = np.clip(x, self.x_min, self.x_max)
        y = np.clip(y, self.y_min, self.y_max)

        # Map to fractional indices along each axis
        # np.interp gives position in axis-space; we convert to index-space
        def frac_index(val, axis):
            # normalized coordinate along axis
            t = (val - axis[0]) / (axis[-1] - axis[0])
            t = np.clip(t, 0.0, 0.999999)  # stay inside last cell
            f = t * (len(axis) - 1)
            return f

        fx = frac_index(x, self.x_axis)
        fy = frac_index(y, self.y_axis)

        i0 = int(np.floor(fx))
        j0 = int(np.floor(fy))
        i1 = min(i0 + 1, len(self.x_axis) - 1)
        j1 = min(j0 + 1, len(self.y_axis) - 1)

        wx = fx - i0
        wy = fy - j0
        return i0, i1, j0, j1, wx, wy

    def _bilinear(self, grid, x, y):
        i0, i1, j0, j1, wx, wy = self._index_and_weights(x, y)

        # Note: grid indexed as [j, i] = [row, col] = [y, x]
        v00 = grid[j0, i0]
        v10 = grid[j0, i1]
        v01 = grid[j1, i0]
        v11 = grid[j1, i1]

        v0 = v00 * (1 - wx) + v10 * wx
        v1 = v01 * (1 - wx) + v11 * wx
        return v0 * (1 - wy) + v1 * wy

    # ---------- public API ----------------------------------------

    def V(self, x, y):
        """Potential V(x, y) via bilinear interpolation."""
        return self._bilinear(self.Z, x, y)

    def gradV(self, x, y):
        """Gradient (dV/dx, dV/dy) via bilinear interpolation."""
        gx = self._bilinear(self.dZ_dx, x, y)
        gy = self._bilinear(self.dZ_dy, x, y)
        return gx, gy

    def in_domain(self, x, y):
        """Check if (x,y) lies inside the grid bounds."""
        return (self.x_min <= x <= self.x_max) and (self.y_min <= y <= self.y_max)


class OrbitIntegrator:
    """
    Symplectic integrator for a test particle on the potential manifold.

    State = (x, y, vx, vy)
    """

    def __init__(self, potential: ManifoldPotential, mass=1.0, damping=0.0):
        """
        Parameters
        ----------
        potential : ManifoldPotential
            Geometry / potential provider.
        mass : float
            Test particle mass.
        damping : float
            Linear drag coefficient gamma. 0 = Hamiltonian motion.
        """
        self.pot = potential
        self.m = mass
        self.gamma = damping

    def accel(self, x, y, vx, vy):
        """
        Compute acceleration at (x,y) with velocity (vx,vy).

        a = - gradV / m - gamma * v
        """
        dVdx, dVdy = self.pot.gradV(x, y)
        ax = -dVdx / self.m - self.gamma * vx
        ay = -dVdy / self.m - self.gamma * vy
        return ax, ay

    def step(self, state, dt):
        """
        One velocity-Verlet step.

        Parameters
        ----------
        state : array-like (4,)
            [x, y, vx, vy]
        dt : float
            Timestep.

        Returns
        -------
        new_state : ndarray (4,)
        """
        x, y, vx, vy = state
        ax0, ay0 = self.accel(x, y, vx, vy)

        # Position update
        x_new = x + vx * dt + 0.5 * ax0 * dt * dt
        y_new = y + vy * dt + 0.5 * ay0 * dt * dt

        # Velocity half-step
        vx_half = vx + 0.5 * ax0 * dt
        vy_half = vy + 0.5 * ay0 * dt

        # New acceleration at updated position
        ax1, ay1 = self.accel(x_new, y_new, vx_half, vy_half)

        # Velocity full-step
        vx_new = vx_half + 0.5 * ax1 * dt
        vy_new = vy_half + 0.5 * ay1 * dt

        return np.array([x_new, y_new, vx_new, vy_new], dtype=float)

    def integrate(self, state0, dt, n_steps, stop_at_boundary=True):
        """
        Integrate an orbit.

        Parameters
        ----------
        state0 : array-like (4,)
            Initial state [x0, y0, vx0, vy0].
        dt : float
            Timestep.
        n_steps : int
            Number of steps.
        stop_at_boundary : bool
            If True, stop when trajectory leaves domain.

        Returns
        -------
        traj : ndarray (T,4)
            Array of states over time. May be shorter than n_steps if
            stop_at_boundary=True and particle escapes.
        """
        state = np.array(state0, dtype=float)
        traj = np.empty((n_steps, 4), dtype=float)

        for k in range(n_steps):
            x, y, vx, vy = state
            if stop_at_boundary and not self.pot.in_domain(x, y):
                return traj[:k]
            traj[k] = state
            state = self.step(state, dt)

        return traj


# ---------- convenience / example wiring --------------------------

def example_from_npz(npz_path,
                     state0=None,
                     dt=0.01,
                     n_steps=20000,
                     pot_scale=1.0,
                     mass=1.0,
                     damping=0.0,
                     show_plot=True):
    """
    Example entry point:

    Load a manifold from an .npz file with X, Y, Z arrays and shoot
    an "electron" across it.

    Parameters
    ----------
    npz_path : str
        Path to npz file containing X, Y, Z.
    state0 : [x0, y0, vx0, vy0] or None
        Initial state. If None, a default is chosen near the center.
    dt, n_steps, pot_scale, mass, damping : see above.
    show_plot : bool
        If True, show a 3D plot with the orbit overlay.
    """

    data = np.load(npz_path)
    X = data["X"]
    Y = data["Y"]
    Z = data["Z"]

    pot = ManifoldPotential(X, Y, Z, scale=pot_scale)
    integrator = OrbitIntegrator(pot, mass=mass, damping=damping)

    # Default initial conditions: near center with a tangential kick
    if state0 is None:
        x0 = 0.5 * (pot.x_min + pot.x_max)
        y0 = 0.5 * (pot.y_min + pot.y_max)
        vx0 = 0.0
        vy0 = 1.0   # adjust to taste
        state0 = [x0, y0, vx0, vy0]

    traj = integrator.integrate(state0, dt=dt, n_steps=n_steps)

    if show_plot:
        plot_orbit_on_surface(X, Y, Z, traj)

    return traj


def plot_orbit_on_surface(X, Y, Z, traj, elev=35, azim=-60):
    """
    3D visualization helper: plot manifold and overlay orbit.

    Parameters
    ----------
    X, Y, Z : 2D grid arrays for the surface.
    traj : ndarray (T,4)
        Trajectory states.
    elev, azim : floats
        Viewing angles for the 3D axes.
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Surface
    ax.plot_surface(
        X, Y, Z,
        rstride=2, cstride=2,
        cmap="plasma",
        linewidth=0, antialiased=True,
        alpha=0.6
    )

    # Orbit projected onto surface
    x = traj[:, 0]
    y = traj[:, 1]

    # Bilinear interpolate Z for orbit points (reuse quick version)
    # We create a temporary ManifoldPotential with scale=1 for this.
    pot_tmp = ManifoldPotential(X, Y, Z, scale=1.0)
    z = np.array([pot_tmp.V(xi, yi) for xi, yi in zip(x, y)])

    ax.plot(x, y, z, color="cyan", linewidth=1.5)

    ax.set_xlabel("Mass field (m)")
    ax.set_ylabel("Coupling field (λ)")
    ax.set_zlabel("Potential / manifold height")

    ax.view_init(elev=elev, azim=azim)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Example usage:
    # Place an .npz with X, Y, Z in the same directory and uncomment:
    
     example_from_npz(
         "pirouette_manifold_3D.npz",
         dt=0.005,
         n_steps=50000,
         pot_scale=1.0,
         mass=1.0,
         damping=0.01,
         show_plot=True,
     )
