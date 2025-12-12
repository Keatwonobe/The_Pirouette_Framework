import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------
# GRAVITY EXPERIMENT PARAMETERS
# ----------------------------------------
TWIST = 3.8
DT = 0.005
STEPS_PER_MEASUREMENT = 8000
MASS_SOURCE = 2.0  # Strength of the central "Mass" (Gamma Cloud)
GAMMA_VACUUM = 0.11 # Base vacuum viscosity

# Spatial Scan
R_MIN = 1.5
R_MAX = 10.0
SAMPLES = 20

def get_local_gamma(r):
    # Model the Mass as a source of Viscosity
    # Gamma(r) = Gamma_0 + M / r
    # This represents the "Density of Knots" falling off with distance
    return GAMMA_VACUUM + (MASS_SOURCE / r)

def get_force_gravity(m, lam):
    # Standard Soliton Physics
    F_teal_m = -(m + 0.866) 
    F_teal_lam = -(lam - 0.5)

    F_red_m = -(m - 0.0)
    p_violation = TWIST * np.sin(m * 2.5) 
    F_red_lam = -(lam + 1.0) + p_violation

    sum_m = (F_teal_m + F_red_m)
    sum_lam = (F_teal_lam + F_red_lam)
    magnitude = np.sqrt(sum_m**2 + sum_lam**2)
    scaling_factor = np.sqrt(magnitude) if magnitude > 1e-6 else 0
    
    F_gold_m = sum_m * scaling_factor
    F_gold_lam = sum_lam * scaling_factor
    
    angle = np.degrees(np.arctan2(lam, m)) % 360
    
    def gaussian(x, mu, sig):
        diff = np.minimum(np.abs(x - mu), 360 - np.abs(x - mu))
        return np.exp(-(diff/sig)**2)

    w_gold = gaussian(angle, 30, 80)
    w_teal = gaussian(angle, 150, 80)
    w_red = gaussian(angle, 270, 80)
    
    tot = w_gold + w_teal + w_red + 1e-6
    nw_red = w_red / tot
    nw_teal = w_teal / tot
    nw_gold = w_gold / tot
    
    Fm = (nw_teal * F_teal_m + nw_red * F_red_m + nw_gold * F_gold_m)
    Flam = (nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam)
    
    return Fm, Flam, nw_red

def measure_clock_rate(distance):
    """
    Simulate a clock at a given radius.

    Returns
    -------
    rate_internal : float
        Internal spin clock – radians of phase per integration step.
    factor_external : float
        External / gravitational clock factor ~ 1 / <drag>,
        which we will later normalize to get dt/dtau_ext.
    """
    # 1. Local viscosity ("gravity")
    local_gamma = get_local_gamma(distance)

    # 2. Initialize "clock" (same as before)
    m, lam = -0.5, 0.5
    pm, plam = 0.9, 0.4

    prev_ang = np.arctan2(lam, m)
    total_ang = 0.0

    # For the external clock we accumulate all drag factors
    drag_samples = []

    for _ in range(STEPS_PER_MEASUREMENT):
        # --- half-step 1 ---
        Fm, Flam, w_red = get_force_gravity(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * local_gamma * w_red)
        drag_samples.append(drag)

        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag
        m += DT * pm
        lam += DT * plam

        # --- half-step 2 ---
        Fm, Flam, w_red = get_force_gravity(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * local_gamma * w_red)
        drag_samples.append(drag)

        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag

        # --- internal spin clock tick ---
        curr_ang = np.arctan2(lam, m)
        delta = curr_ang - prev_ang
        if delta > np.pi:
            delta -= 2 * np.pi
        if delta < -np.pi:
            delta += 2 * np.pi
        total_ang += delta
        prev_ang = curr_ang

    # Internal spin clock: radians per step
    rate_internal = abs(total_ang) / STEPS_PER_MEASUREMENT

    # External / gravitational clock: inverse of mean drag
    mean_drag = np.mean(drag_samples)
    factor_external = 1.0 / mean_drag

    return rate_internal, factor_external


def run_emergent_gravity():
    r_values = np.linspace(R_MIN, R_MAX, SAMPLES)

    internal_rates = []     # spin-based internal clock
    external_factors = []   # drag-based external clock

    print(f"Mapping Spacetime Curvature (R={R_MIN} to {R_MAX})...")

    # 1. Measure both clocks at each radius
    for r in r_values:
        r_int, f_ext = measure_clock_rate(r)
        internal_rates.append(r_int)
        external_factors.append(f_ext)

    # 2. INTERNAL time dilation:
    # compare internal rate to far-away rate
    rate_inf_int = internal_rates[-1]
    td_internal = [rate_inf_int / rloc for rloc in internal_rates]

    # 3. EXTERNAL (gravitational) time dilation from drag:
    # normalize so dt/dtau_ext -> 1 far away
    ext_inf = external_factors[-1]
    td_external = [fext / ext_inf for fext in external_factors]

    # 4. Fit Schwarzschild to the EXTERNAL curve
    from scipy.optimize import curve_fit

    def schwarzschild_model(r, rs):
        # GR: dt/dtau = 1 / sqrt(1 - Rs/r)
        r = np.asarray(r, dtype=float)
        val = 1.0 - rs / r
        val = np.where(val < 1e-3, 1e-3, val)
        return 1.0 / np.sqrt(val)

    popt, pcov = curve_fit(schwarzschild_model, r_values, td_external, p0=[1.0])
    rs_fit = popt[0]

    print("-" * 60)
    print("EMERGENT GRAVITY RESULTS (Dual Clocks)")
    print(f"Effective Schwarzschild Radius from external clock (Rs): {rs_fit:.4f}")
    print("-" * 60)

    # 5. Plotting
    plt.figure(figsize=(10, 8), facecolor='black')
    ax = plt.gca()
    ax.set_facecolor('black')

    # Internal spin clock (what you had before)
    plt.scatter(
        r_values, td_internal,
        color='cyan', edgecolor='black', linewidth=0.5,
        label='Internal Spin Clock  $dt/d\\tau_{int}$'
    )

    # External / coherence-gravity clock
    plt.plot(
        r_values, td_external,
        'm.-', linewidth=2, markersize=6,
        label='External / Coherence Clock  $dt/d\\tau_{ext}$'
    )

    # GR fit
    r_dense = np.linspace(R_MIN, R_MAX, 400)
    td_gr = schwarzschild_model(r_dense, rs_fit)
    plt.plot(
        r_dense, td_gr,
        'r-', linewidth=2,
        label=f'GR Fit  (Rs = {rs_fit:.2f})'
    )

    # Newtonian limit ~ 1 + Rs/(2r)
    td_newton = 1.0 + rs_fit / (2.0 * r_dense)
    plt.plot(
        r_dense, td_newton,
        'g--', linewidth=1.5,
        label='Newtonian Limit  $1 + R_s/(2r)$'
    )

    plt.title("Emergent Gravity: Dual Clocks vs Distance", color='white', fontsize=16)
    plt.xlabel("Distance from Mass Source (r)", color='white')
    plt.ylabel("Time Dilation Factor  $dt/d\\tau$", color='white')

    plt.grid(color='#333333', alpha=0.5)
    plt.legend(facecolor='black', labelcolor='white')
    plt.tick_params(colors='white')

    plt.tight_layout()
    plt.savefig('emergent_gravity_dual_clocks.png', dpi=200)
    plt.show()


if __name__ == "__main__":
    run_emergent_gravity()