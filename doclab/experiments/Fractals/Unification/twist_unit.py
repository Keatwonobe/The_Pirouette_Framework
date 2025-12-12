import numpy as np

C = 299_792_458.0        # m/s
HBAR = 1.054_571_817e-34 # J*s

# ============================================================
# 1. Time-averaged sector weights
# ============================================================

def sector_weights(tau,
                   ring_radius=2.2,
                   n_angles=360,
                   t_max=5000,
                   dt=0.01,
                   omega0=1.0):
    """
    Evolve a test particle on the electron-shell ring at twist=tau
    and return time-averaged sector weights (G, T, R).

    New: include a baseline angular frequency omega0 so that the
    particle actually orbits the ring instead of sitting at a
    fixed point. The twist tau modulates the speed via sin(theta),
    creating tau-dependent dwell fractions.
    """
    n_steps = int(t_max / dt)

    # initial angle can now be arbitrary; we'll use 0
    theta = 0.0

    wG = wT = wR = 0.0
    sector_count = 0

    for _ in range(n_steps):
        # baseline rotation + twist modulation
        dtheta = (omega0 + tau * np.sin(theta)) * dt
        theta += dtheta

        # wrap to [-pi, pi]
        theta = (theta + np.pi) % (2*np.pi) - np.pi

        # sector accumulation
        if -np.pi/3 <= theta <= np.pi/3:
            wG += 1
        elif theta > np.pi/3:
            wT += 1
        else:
            wR += 1

        sector_count += 1

    return wG/sector_count, wT/sector_count, wR/sector_count

def sector_weights_continuum(tau,
                             omega0=6.0,
                             n_theta=4096):
    """
    Winding-compensated sector weights.

    Instead of running a time-step simulation and counting integer
    sector hits, we compute the infinite-time angular density

        rho(θ; τ) ∝ 1 / (omega0 + τ sin θ)

    and integrate it over the three sector wedges.

    This is the W→∞ limit: the "unwound" manifold where the
    stair-steps from discrete winding disappear.
    """
    # Sample θ uniformly around the ring
    thetas = np.linspace(-np.pi, np.pi, n_theta, endpoint=False)

    # Instantaneous angular speed
    omega = omega0 + tau * np.sin(thetas)

    # To avoid singularities if |tau| ≳ omega0, clip small speeds
    eps = 1e-9
    omega = np.sign(omega) * np.maximum(np.abs(omega), eps)

    # Density ∝ 1 / |omega|
    rho = 1.0 / np.abs(omega)
    rho /= rho.sum()  # normalize to 1

    # Sector masks
    mask_G = (thetas >= -np.pi/3) & (thetas <= np.pi/3)
    mask_T = (thetas >  np.pi/3)
    mask_R = (thetas < -np.pi/3)

    wG = rho[mask_G].sum()
    wT = rho[mask_T].sum()
    wR = rho[mask_R].sum()

    return wG, wT, wR



# ============================================================
# 2. 1:2:8 error functional
# ============================================================

def error_128(tau, **kwargs):
    target = np.array([1/11, 2/11, 8/11])
    w = np.array(sector_weights(tau, **kwargs))
    E = np.sum((w - target)**2)
    return E, w[0], w[1], w[2]


# ============================================================
# 3. Potential and derivatives
# ============================================================

def twist_potential(tau, Lambda0=1.0, **kwargs):
    E, _, _, _ = error_128(tau, **kwargs)
    return Lambda0 * E


def finite_difference_derivatives(tau, h=1e-3, **kwargs):
    Vp = (twist_potential(tau + h, **kwargs)
        - twist_potential(tau - h, **kwargs)) / (2*h)

    Vpp = (twist_potential(tau + h, **kwargs)
         - 2*twist_potential(tau, **kwargs)
         + twist_potential(tau - h, **kwargs)) / (h*h)

    return Vp, Vpp


# ============================================================
# 4. Twist scan with extrema + inflection detection
# ============================================================

def scan_twist_range(t_min, t_max, n_samples, **kwargs):
    taus = np.linspace(t_min, t_max, n_samples)
    Vvals = []
    Evals = []
    min_flags = np.zeros(n_samples, dtype=bool)
    max_flags = np.zeros(n_samples, dtype=bool)
    inflection = np.zeros(n_samples, dtype=bool)

    for i, tau in enumerate(taus):
        Vvals.append(twist_potential(tau, **kwargs))
        Evals.append(error_128(tau, **kwargs)[0])

    Vvals = np.array(Vvals)
    Evals = np.array(Evals)

    for i in range(1, n_samples-1):
        left, mid, right = Vvals[i-1], Vvals[i], Vvals[i+1]
        if mid < left and mid < right:
            min_flags[i] = True
        if mid > left and mid > right:
            max_flags[i] = True

        # detect inflection via discrete curvature
        slope_left = mid - left
        slope_right = right - mid
        if np.sign(slope_left) != np.sign(slope_right):
            inflection[i] = True

    return taus, Vvals, Evals, min_flags, max_flags, inflection

def lorentz_factor(p, m):
    # p: 3-momentum vector
    p2 = np.dot(p, p)
    return np.sqrt(1.0 + p2 / (m**2 * C**2))


def step_relativistic_particle(x, p, species, E_field, B_field, dt):
    """
    Single time step for a relativistic charged particle.

    x: position (3,)
    p: 3-momentum (3,)
    species: TwistSpecies
    E_field, B_field: callables E(x), B(x) returning 3-vectors
    dt: external coordinate time step
    """
    m = species.mass
    q = species.charge  # this is in "twist-charge" units; you can map to e later

    gamma = lorentz_factor(p, m)
    v = p / (gamma * m)

    # fields at current location
    E = np.asarray(E_field(x))
    B = np.asarray(B_field(x))

    # Lorentz force
    dpdt = q * (E + np.cross(v, B))

    # update p, x
    p_new = p + dpdt * dt
    gamma_new = lorentz_factor(p_new, m)
    v_new = p_new / (gamma_new * m)
    x_new = x + v_new * dt

    return x_new, p_new

class TwistSpecies:
    def __init__(self, name, tau, tau_e, m_e, T0=None, ring_radius=2.2):
        self.name = name
        self.tau = tau
        self.ring_radius = ring_radius

        # static sector fractions
        self.G, self.T, self.R = sector_weights(tau, ring_radius=ring_radius)

        # calibrate T0 from electron if not given
        if T0 is None:
            # tau_e, m_e given in same run so we can set T0
            self.T0 = HBAR * tau_e / (m_e * C**2)
        else:
            self.T0 = T0

        # mass from twist clock
        self.mass = HBAR * tau / (self.T0 * C**2)

        # simple charge & weak-ness ansatz (you can refine later)
        # e.g. EM charge from Teal, weak "isospin" from Red
        self.charge = (self.T - self.G)  # arbitrary linear map for now
        self.weakness = self.R

def winding_eigenmode_scan(tau_min, tau_max,
                           n_tau=2000,
                           omega0=6.0,
                           n_theta=4096,
                           eps=1e-4):
    """
    Scan twist space for 'winding eigenmodes' where the continuum
    angular speed omega(θ; τ) = omega0 + τ sin θ nearly vanishes.

    Returns:
        taus          – sampled τ values
        min_speeds    – min_θ |omega(θ; τ)| at each τ
        eigen_flags   – boolean array: True where min_speed < eps
    """
    taus = np.linspace(tau_min, tau_max, n_tau)
    thetas = np.linspace(-np.pi, np.pi, n_theta, endpoint=False)

    min_speeds = np.empty_like(taus)
    eigen_flags = np.zeros_like(taus, dtype=bool)

    for i, tau in enumerate(taus):
        omega = omega0 + tau * np.sin(thetas)
        speeds = np.abs(omega)
        m = speeds.min()
        min_speeds[i] = m
        if m < eps:
            eigen_flags[i] = True

    return taus, min_speeds, eigen_flags
