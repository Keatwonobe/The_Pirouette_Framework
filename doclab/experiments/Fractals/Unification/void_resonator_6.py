import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
import matplotlib.colors as colors

# ============================================================
# 1. HIGH-SPEED PHYSICS KERNEL
# ============================================================

@njit(fastmath=True)
def physics_step_batch(m_in, l_in, pm_in, pl_in, sigmas, dt=0.1):
    """
    Runs the physics step for MANY different sigmas simultaneously
    on the SAME set of sensor particles.
    
    m_in: (N_Sensors,)
    sigmas: (N_Scans,)
    Returns: m_out, l_out (N_Scans, N_Sensors)
    """
    n_sensors = m_in.shape[0]
    n_scans = sigmas.shape[0]
    
    m_out = np.zeros((n_scans, n_sensors), dtype=np.float32)
    l_out = np.zeros((n_scans, n_sensors), dtype=np.float32)
    
    # We broadcast manually for Numba speed
    for s in range(n_scans):
        sigma = sigmas[s]
        for i in range(n_sensors):
            m = m_in[i]
            l = l_in[i]
            pm = pm_in[i]
            pl = pl_in[i]
            
            # 1st Kick
            fm = -(m + 2 * sigma * m * l)
            fl = -(l + sigma * (m**2 - l**2))
            pm += 0.5 * dt * fm
            pl += 0.5 * dt * fl
            
            # Drift
            m += dt * pm
            l += dt * pl
            
            # 2nd Kick
            fm = -(m + 2 * sigma * m * l)
            fl = -(l + sigma * (m**2 - l**2))
            pm += 0.5 * dt * fm
            pl += 0.5 * dt * fl
            
            m_out[s, i] = m
            l_out[s, i] = l
            
    return m_out, l_out

@njit(fastmath=True)
def reality_step_single(m, l, pm, pl, sigma, dt=0.1):
    """
    Evolves the True Reality (Single Sigma)
    """
    # 1st Kick
    fm = -(m + 2 * sigma * m * l)
    fl = -(l + sigma * (m**2 - l**2))
    pm += 0.5 * dt * fm
    pl += 0.5 * dt * fl
    
    # Drift
    m += dt * pm
    l += dt * pl
    
    # 2nd Kick
    fm = -(m + 2 * sigma * m * l)
    fl = -(l + sigma * (m**2 - l**2))
    pm += 0.5 * dt * fm
    pl += 0.5 * dt * fl
    
    # Soft Boundary
    mask = (m*m + l*l) > 9.0
    # Manual masking for Numba
    for i in range(len(m)):
        if mask[i]:
            m[i] *= 0.5
            l[i] *= 0.5
            pm[i] *= -0.5
            pl[i] *= -0.5
            
    return m, l, pm, pl

# ============================================================
# 2. THE CARTOGRAPHER
# ============================================================

def run_cartography():
    print("[-] Initializing Landscape Cartographer...")
    
    # Config
    RES = 1000
    N_SENSORS = 500
    FRAMES = 200
    
    # The Scan Range (The "Map" Width)
    SIGMA_MIN = 0.1
    SIGMA_MAX = 2.5
    SIGMA_RES = 300 # How many hypotheses to test per frame
    scan_sigmas = np.linspace(SIGMA_MIN, SIGMA_MAX, SIGMA_RES).astype(np.float32)
    
    # Initialize Reality
    y, x = np.mgrid[-2:2:complex(0, RES), -2:2:complex(0, RES)]
    real_m = x.astype(np.float32).ravel()
    real_l = y.astype(np.float32).ravel()
    real_pm = np.zeros_like(real_m)
    real_pl = np.zeros_like(real_l)
    
    # Pick Sensors
    sensor_idx = np.random.choice(RES*RES, N_SENSORS, replace=False)
    
    # True Physics Drift
    true_sigma = 1.0
    true_sigma_hist = []
    
    # The Map Data: [Time, Sigma_Index] -> Loss
    loss_landscape = np.zeros((FRAMES, SIGMA_RES))
    
    print(f"[-] Scanning {FRAMES} timesteps x {SIGMA_RES} hypotheses...")
    
    # Internal Memory for Sensors (to do prediction)
    # We need to know where sensors were at T-1 to predict T
    # Initial state:
    s_m = real_m[sensor_idx]
    s_l = real_l[sensor_idx]
    s_pm = real_pm[sensor_idx]
    s_pl = real_pl[sensor_idx]
    
    for t in range(FRAMES):
        # 1. Snapshot T-1 (The basis for prediction)
        prev_m = s_m.copy()
        prev_l = s_l.copy()
        prev_pm = s_pm.copy()
        prev_pl = s_pl.copy()
        
        # 2. Evolve Reality to T
        # (Full grid update is too slow for CPU demo, so we simulate reality ONLY on sensors for the map)
        # This is valid because the sensors are just a subset of reality.
        # Ideally we'd sim the whole grid to get neighbor interactions if using spatial coupling,
        # but Wada is currently strictly local + global gravity.
        s_m, s_l, s_pm, s_pl = reality_step_single(s_m, s_l, s_pm, s_pl, true_sigma)
        
        # 3. THE SCAN (Parallel Universe Testing)
        # We ask: "If we started at T-1, where would Sigma=X land us?"
        pred_m, pred_l = physics_step_batch(prev_m, prev_l, prev_pm, prev_pl, scan_sigmas)
        
        # 4. Compute Loss Surface
        # Loss = MSE between Prediction and Reality (T)
        # Broadcasting: (N_Scans, N_Sensors) - (N_Sensors,)
        diff_m = pred_m - s_m
        diff_l = pred_l - s_l
        dist_sq = diff_m**2 + diff_l**2
        
        # Mean over sensors -> (N_Scans,)
        losses = np.mean(dist_sq, axis=1)
        
        # Store Log Loss for better visibility
        loss_landscape[t, :] = np.log1p(losses)
        
        true_sigma_hist.append(true_sigma)
        
        # Drift Reality
        # Drift pattern: Sine wave into Chaos
        true_sigma = 1.1 + 0.4 * np.sin(t * 0.05)
        
        if t % 20 == 0:
            print(f"    Scanning Frame {t}/{FRAMES}...")

    # ==========================================
    # VISUALIZATION
    # ==========================================
    print("[-] Rendering Map...")
    
    fig, ax = plt.subplots(figsize=(12, 8), facecolor='#0f0f0f')
    ax.set_facecolor('#0f0f0f')
    
    # Plot Heatmap
    # X: Sigma, Y: Time
    # We transpose to get Time on Y
    extent = [SIGMA_MIN, SIGMA_MAX, FRAMES, 0] # Flip Y to put T=0 at top? No, T=0 at bottom usually better.
    extent = [SIGMA_MIN, SIGMA_MAX, 0, FRAMES]
    
    im = ax.imshow(loss_landscape, aspect='auto', extent=extent, origin='lower',
                   cmap='magma', vmin=0, vmax=np.percentile(loss_landscape, 95))
    
    # Overlay Truth
    t_axis = np.arange(FRAMES)
    ax.plot(true_sigma_hist, t_axis, color='cyan', linewidth=2, linestyle='--', label='Hidden Truth')
    
    # Annotate
    ax.set_title("The Loss Landscape of Chaos", color='white', fontsize=16)
    ax.set_xlabel("Hypothesis (Sigma)", color='gray', fontsize=12)
    ax.set_ylabel("Time (Evolution)", color='gray', fontsize=12)
    ax.tick_params(axis='both', colors='gray')
    ax.grid(color='white', alpha=0.1, linestyle=':')
    
    # Add Colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label("Log Prediction Error (Surprisal)", color='gray')
    cbar.ax.tick_params(colors='gray')
    
    ax.legend(facecolor='#222', labelcolor='white', loc='upper right')
    
    plt.tight_layout()
    plt.savefig('wada_loss_landscape.png')
    print("[+] Map Complete. Saved to 'wada_loss_landscape.png'")

if __name__ == "__main__":
    run_cartography()