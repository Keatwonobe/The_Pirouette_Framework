import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------
PARTICLE_COUNT = 5000
INIT_RADIUS = 3.0
DT = 0.05
STEPS = 1000
GAMMA = 0.02
TWIST = 2.83814 # The Ripple Twist

def get_force_batch(m, lam, twist):
    # Vectorized Physics
    F_teal_m = -(m + 0.866)
    F_teal_lam = -(lam - 0.5)

    F_red_m = -m
    p_violation = twist * np.sin(m * 2.5)
    F_red_lam = -(lam + 1.0) + p_violation

    sum_m = (F_teal_m + F_red_m)
    sum_lam = (F_teal_lam + F_red_lam)
    mag_sq = sum_m**2 + sum_lam**2
    mag = np.sqrt(mag_sq)
    scale = np.sqrt(mag)

    F_gold_m = sum_m * scale
    F_gold_lam = sum_lam * scale

    # Weights
    angle = np.degrees(np.arctan2(lam, m)) % 360

    def w_calc(a, t):
        d = np.abs(a - t)
        d = np.minimum(d, 360.0 - d)
        return np.exp(-(d/80.0)**2)

    w_gold = w_calc(angle, 30.0)
    w_teal = w_calc(angle, 150.0)
    w_red = w_calc(angle, 270.0)

    tot = w_gold + w_teal + w_red + 1e-6
    nw_red = w_red / tot
    nw_teal = w_teal / tot
    nw_gold = w_gold / tot

    Fm = (nw_teal * F_teal_m + nw_red * F_red_m + nw_gold * F_gold_m)
    Flam = (nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam)

    return Fm, Flam, nw_red

def measure_half_life():
    print("Simulating Decay...")
    # Initialize random cloud
    np.random.seed(42)
    theta = np.random.uniform(0, 2*np.pi, PARTICLE_COUNT)
    r = np.sqrt(np.random.uniform(0, INIT_RADIUS**2, PARTICLE_COUNT))
    m = r * np.cos(theta)
    lam = r * np.sin(theta)

    pm = np.zeros_like(m)
    plam = np.zeros_like(lam)

    volume_history = []
    time_history = []

    for t in range(STEPS):
        # Measure Volume (Mean Squared Radius is proportional to Phase Space Area)
        # V ~ <R^2>
        current_vol = np.mean(m**2 + lam**2)
        volume_history.append(current_vol)
        time_history.append(t * DT)

        # Physics
        Fm, Flam, w_red = get_force_batch(m, lam, TWIST)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag
        m += DT * pm
        lam += DT * plam

    volume_history = np.array(volume_history)
    time_history = np.array(time_history)

    # Normalize Volume to 100% at start
    V0 = volume_history[0]
    V_norm = (volume_history / V0) * 100

    # Find Half-Life (Time to cross 50%)
    # Find index where V_norm < 50
    indices_below = np.where(V_norm < 50)[0]
    if len(indices_below) > 0:
        idx = indices_below[0]
        # Linear interpolation for precision
        v_after = V_norm[idx]
        v_before = V_norm[idx-1]
        t_after = time_history[idx]
        t_before = time_history[idx-1]
        
        fraction = (50 - v_before) / (v_after - v_before)
        half_life_time = t_before + fraction * (t_after - t_before)
    else:
        half_life_time = None

    # Curve Fit (Exponential Decay)
    def decay_func(t, lambda_val, offset):
        return 100 * np.exp(-lambda_val * t) + offset

    # Fit only the first part of the curve before it settles
    try:
        popt, pcov = curve_fit(decay_func, time_history, V_norm, p0=[0.1, 0])
        lambda_fit = popt[0]
        offset_fit = popt[1]
        fitted_curve = decay_func(time_history, *popt)
        fit_half_life = np.log(2) / lambda_fit
    except:
        lambda_fit = 0
        fitted_curve = np.zeros_like(time_history)
        fit_half_life = 0

    return time_history, V_norm, half_life_time, fitted_curve, fit_half_life

def plot_half_life():
    t_axis, vol_axis, t_half, fit_curve, fit_t_half = measure_half_life()

    fig, ax = plt.subplots(figsize=(10, 7), facecolor='#050510')
    ax.set_facecolor('#050510')

    # Plot Data
    ax.plot(t_axis, vol_axis, color='#00ffff', linewidth=2.5, label='Measured Volume')

    # Plot Fit (Optional, ghosted)
    # ax.plot(t_axis, fit_curve, color='white', linestyle='--', alpha=0.3, label=f'Exp Fit (HL={fit_t_half:.2f})')

    # Mark Half-Life
    if t_half is not None:
        ax.axhline(50, color='#ff00ff', linestyle='--', alpha=0.8)
        ax.axvline(t_half, color='#ff00ff', linestyle='--', alpha=0.8)
        
        # Dot
        ax.plot([t_half], [50], marker='o', color='white', markersize=8, zorder=10)
        
        # Annotation
        ax.annotate(f"HALF-LIFE\nT = {t_half:.3f} (sim units)", 
                    xy=(t_half, 50), xytext=(t_half + 5, 60),
                    arrowprops=dict(facecolor='white', shrink=0.05),
                    color='white', fontsize=12, fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.5", fc="#ff00ff", ec="white", alpha=0.8))

    # Styling
    ax.set_title(f"Vacuum Decay Rate: The 'Inhale' Speed\n(Twist={TWIST}, Gamma={GAMMA})", color='white', fontsize=16)
    ax.set_ylabel("Phase Space Volume (%)", color='white', fontsize=12)
    ax.set_xlabel("Time (Simulation Units)", color='white', fontsize=12)
    ax.grid(color='#333333', linestyle=':')
    ax.tick_params(colors='white', labelsize=10)
    
    # Add Stats Box
    stats = (
        f"Initial Volume: 100%\n"
        f"Final Volume: {vol_axis[-1]:.1f}%\n"
        f"Half-Life: {t_half:.3f}"
    )
    ax.text(0.75, 0.85, stats, transform=ax.transAxes, 
            color='cyan', fontsize=12, family='monospace',
            bbox=dict(boxstyle="round,pad=0.5", fc="black", ec="cyan", alpha=0.5))

    # Spines
    for spine in ax.spines.values():
        spine.set_edgecolor('white')

    plt.tight_layout()
    plt.savefig('vacuum_half_life.png', dpi=150)
    plt.show()

plot_half_life()