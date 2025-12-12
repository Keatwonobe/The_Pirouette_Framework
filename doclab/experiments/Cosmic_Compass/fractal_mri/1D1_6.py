import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import Normalize

# =============================================================================
# 1. Physics Engine: Forces and Jacobian
# =============================================================================

def get_force_tension_mode(m, lam, twist=1.5):
    """
    Net tension-mode force in (m, lam) space.
    Combines Teal (harmonic), Red (parity-violating), and Gold (sum) anchors.
    """
    # Teal anchor: harmonic toward (-0.866, 0.5)
    F_teal_m = -(m + 0.866)
    F_teal_lam = -(lam - 0.5)

    # Red anchor: toward (0, -1) with parity-violating twist
    F_red_m = -(m - 0.0)
    p_violation = twist * np.sin(m * 2.5)
    F_red_lam = -(lam + 1.0) + p_violation

    # Gold = tension = vector sum
    F_gold_m = F_teal_m + F_red_m
    F_gold_lam = F_teal_lam + F_red_lam

    # Basin weights by angle
    angle = np.degrees(np.arctan2(lam, m)) % 360.0

    def gaussian(x, mu, sig):
        diff = np.minimum(np.abs(x - mu), 360.0 - np.abs(x - mu))
        return np.exp(-(diff / sig) ** 2)

    w_gold = gaussian(angle, 30.0, 80.0)
    w_teal = gaussian(angle, 150.0, 80.0)
    w_red  = gaussian(angle, 270.0, 80.0)

    tot = w_gold + w_teal + w_red + 1e-6

    Fm = (w_teal * F_teal_m + w_red * F_red_m + w_gold * F_gold_m) / tot
    Flam = (w_teal * F_teal_lam + w_red * F_red_lam + w_gold * F_gold_lam) / tot
    return Fm, Flam


def jacobian_tension_mode(m, lam, twist=1.5, eps=1e-3):
    """
    Finite-difference Jacobian of F at (m, lam).
    """
    m = float(m)
    lam = float(lam)

    Fm0, Flam0 = get_force_tension_mode(m, lam, twist)

    # Perturb m
    Fm_p, Flam_p = get_force_tension_mode(m + eps, lam, twist)
    Fm_m, Flam_m = get_force_tension_mode(m - eps, lam, twist)

    # Perturb lam
    Fm_l, Flam_l = get_force_tension_mode(m, lam + eps, twist)
    Fm_lp, Flam_lp = get_force_tension_mode(m, lam - eps, twist)

    dFm_dm     = (Fm_p    - Fm_m)    / (2 * eps)
    dFlam_dm   = (Flam_p  - Flam_m)  / (2 * eps)
    dFm_dlam   = (Fm_l    - Fm_lp)   / (2 * eps)
    dFlam_dlam = (Flam_l  - Flam_lp) / (2 * eps)

    J = np.array([[dFm_dm, dFm_dlam],
                  [dFlam_dm, dFlam_dlam]], dtype=float)
    return J


def get_eigenframe(m, lam, twist=1.5):
    """
    Returns the Soft (U1) and Hard (Perp) unit eigenvectors.
    Corrected for 2D system (m, lam).
    """
    J = jacobian_tension_mode(m, lam, twist=twist)
    vals, vecs = np.linalg.eig(J)

    # Sort by magnitude of eigenvalue (smallest abs value = softest mode)
    idx = np.argsort(np.abs(vals))
    
    # Extract soft and hard vectors
    e_soft = vecs[:, idx[0]].real
    e_hard = vecs[:, idx[1]].real

    # Normalization and consistent orientation
    def fix_orientation(v):
        n = np.linalg.norm(v)
        if n == 0: return np.array([1.0, 0.0])
        v = v / n
        # Force first component positive to avoid sign flipping artifacts
        if v[0] < 0: v = -v
        return v

    return fix_orientation(e_soft), fix_orientation(e_hard)


# =============================================================================
# 2. Analysis Tools: Velocity Decomposition & Gauge Connections
# =============================================================================

def analyze_state(m, lam, vm, vlam, twist=1.5):
    """
    Computes energy components and gauge connections for a full spatial slice.
    """
    n = m.shape[0]
    
    # Velocity Decomposition Arrays
    U1 = np.zeros(n)
    Delta_perp = np.zeros(n)
    E_tot = np.zeros(n)
    E_u1 = np.zeros(n)
    E_perp = np.zeros(n)
    
    # Gauge Potential Arrays
    A_soft = np.zeros(n)
    A_hard = np.zeros(n)
    
    # Pre-compute frames for the whole string
    frames = []
    for i in range(n):
        e_s, e_h = get_eigenframe(m[i], lam[i], twist)
        frames.append((e_s, e_h))
        
        # 1. Velocity Projection
        v = np.array([vm[i], vlam[i]])
        u1_val = np.dot(v, e_s)
        
        v_par = u1_val * e_s
        v_perp = v - v_par
        
        U1[i] = u1_val
        Delta_perp[i] = np.linalg.norm(v_perp)
        E_tot[i] = np.dot(v, v)
        E_u1[i] = u1_val**2
        E_perp[i] = E_tot[i] - E_u1[i]

    # 2. Gauge Connection (Berry Phase-like spatial connection)
    # A_mu = <e | d/dx | e>
    for i in range(n):
        ip = (i + 1) % n
        e_s_curr, e_h_curr = frames[i]
        e_s_next, e_h_next = frames[ip]
        
        # Discrete derivative of the basis vector
        d_es = e_s_next - e_s_curr
        d_eh = e_h_next - e_h_curr
        
        # Project derivative onto basis (A ~ e * de)
        A_soft[i] = np.dot(d_es, e_s_curr)
        A_hard[i] = np.dot(d_eh, e_h_curr)

    # Numerical cleanup
    E_perp = np.maximum(E_perp, 0.0)
    
    return U1, Delta_perp, E_tot, E_u1, E_perp, A_soft, A_hard


# =============================================================================
# 3. Simulation Loop
# =============================================================================

def run_simulation(
    n_points=200,
    length=50.0,
    total_time=250.0,
    c=1.0,
    gamma=0.05,
    twist=1.5,
    drive_amp=0.8,
    drive_omega=1.2,
    drive_width=7,
    parity_bias=0.25,
    snapshot_interval=5,
):
    # Setup Grid
    z = np.linspace(0.0, length, n_points, endpoint=False)
    dz = z[1] - z[0]
    dt = 0.35 * dz / max(c, 1e-8)
    n_steps = int(total_time / dt)

    # Initialize Fields (small random seed)
    m = 0.01 * (np.random.rand(n_points) - 0.5)
    lam = 0.01 * (np.random.rand(n_points) - 0.5)
    vm = np.zeros_like(m)
    vlam = np.zeros_like(lam)

    # Drive Mask
    center = n_points // 2
    drive_mask = np.zeros(n_points)
    half_w = max(1, drive_width // 2)
    drive_mask[center - half_w : center + half_w + 1] = 1.0

    # Neighbor indices for Laplacian
    idx = np.arange(n_points)
    ip = (idx + 1) % n_points
    im = (idx - 1) % n_points

    # Data Storage
    history = {
        'time': [],
        'Delta_tot': [],
        'U1': [],
        'Delta_perp': [],
        'E_tot': [],
        'E_u1': [],
        'E_perp': [],
        'A_soft': [],
        'A_hard': [],
        'orbit_m': [],
        'orbit_l': []
    }

    print(f"--- Simulation Start: {n_steps} steps ---")

    for step in range(n_steps):
        t = step * dt

        # Physics: Internal Forces
        Fm_int, Flam_int = get_force_tension_mode(m, lam, twist=twist)

        # Physics: External Drive
        drive_phase = np.sin(drive_omega * t) + parity_bias
        Fm_drive = 0.0
        Flam_drive = drive_amp * drive_phase * drive_mask

        # Physics: Wave Equation (Laplacian)
        lap_m = (m[ip] - 2.0 * m + m[im]) / dz**2
        lap_lam = (lam[ip] - 2.0 * lam + lam[im]) / dz**2
        
        # Update Accelerations
        am = Fm_int + (c**2 * lap_m) + Fm_drive - gamma * vm
        alam = Flam_int + (c**2 * lap_lam) + Flam_drive - gamma * vlam

        # Euler Integration
        vm += am * dt
        vlam += alam * dt
        m += vm * dt
        lam += vlam * dt

        # Snapshots
        if step % snapshot_interval == 0:
            history['time'].append(t)
            history['orbit_m'].append(m[center])
            history['orbit_l'].append(lam[center])
            
            # Analyze frame logic
            U1, D_perp, Et, Eu1, Ep, As, Ah = analyze_state(m, lam, vm, vlam, twist)
            
            history['Delta_tot'].append(np.sqrt(vm**2 + vlam**2))
            history['U1'].append(U1)
            history['Delta_perp'].append(D_perp)
            history['E_tot'].append(Et)
            history['E_u1'].append(Eu1)
            history['E_perp'].append(Ep)
            history['A_soft'].append(As)
            history['A_hard'].append(Ah)

    print("--- Simulation Complete ---")
    
    # Convert lists to arrays
    for k in history:
        history[k] = np.array(history[k])
        
    return z, history


# =============================================================================
# 4. Publication-Quality Visualization
# =============================================================================

def plot_publication_results(z, hist):
    """
    Generates a high-quality composite figure.
    """
    # Set style params manually for consistent "Science/Paper" look
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.size': 10,
        'axes.titlesize': 11,
        'axes.labelsize': 10,
        'figure.dpi': 120
    })

    times = hist['time']
    # Calculate Spacetime bounds
    extent = [z[0], z[-1], times[0], times[-1]]
    
    # Create Figure with GridSpec
    fig = plt.figure(figsize=(12, 10))
    gs = gridspec.GridSpec(3, 2, height_ratios=[1, 1, 0.6], width_ratios=[1, 1])
    
    # --- Plot 1: Total Excitation (Velocity Magnitude) ---
    ax0 = fig.add_subplot(gs[0, 0])
    im0 = ax0.imshow(hist['Delta_tot'], aspect='auto', origin='lower', extent=extent, cmap='magma')
    ax0.set_title(r"Total Excitation $\Delta_{tot} = ||v||$")
    ax0.set_ylabel("Time (t)")
    plt.colorbar(im0, ax=ax0, label="Magnitude")

    # --- Plot 2: Soft Mode Projection (U1) ---
    # Diverging colormap because U1 velocity can be negative
    ax1 = fig.add_subplot(gs[0, 1])
    max_u1 = np.max(np.abs(hist['U1']))
    im1 = ax1.imshow(hist['U1'], aspect='auto', origin='lower', extent=extent, 
                     cmap='RdBu_r', vmin=-max_u1, vmax=max_u1)
    ax1.set_title(r"Soft Mode Projection $U_1 = \vec{v} \cdot \hat{e}_{soft}$")
    ax1.set_ylabel("Time (t)")
    plt.colorbar(im1, ax=ax1, label="Amplitude")

    # --- Plot 3: Geometric Gauge Potential (A_soft) ---
    # This visualizes the rotation of the eigenframe across space
    ax2 = fig.add_subplot(gs[1, 0])
    max_a = np.max(np.abs(hist['A_soft']))
    im2 = ax2.imshow(hist['A_soft'], aspect='auto', origin='lower', extent=extent, 
                     cmap='PuOr', vmin=-max_a, vmax=max_a)
    ax2.set_title(r"Gauge Potential $\mathcal{A}_z^{soft}$ (Frame Twist)")
    ax2.set_xlabel("Position (z)")
    ax2.set_ylabel("Time (t)")
    plt.colorbar(im2, ax=ax2, label=r"$\langle e | \partial_z e \rangle$")

    # --- Plot 4: Confining/Perpendicular Energy Density ---
    ax3 = fig.add_subplot(gs[1, 1])
    im3 = ax3.imshow(hist['E_perp'], aspect='auto', origin='lower', extent=extent, cmap='inferno')
    ax3.set_title(r"Confining Energy $E_{\perp} = E_{tot} - E_{U1}$")
    ax3.set_xlabel("Position (z)")
    plt.colorbar(im3, ax=ax3, label="Energy")

    # --- Plot 5: Global Energy Partitioning (Time Series) ---
    ax4 = fig.add_subplot(gs[2, :]) # Spans both columns
    
    # Spatial averages
    mean_Et = hist['E_tot'].mean(axis=1)
    mean_Eu1 = hist['E_u1'].mean(axis=1)
    mean_Ep = hist['E_perp'].mean(axis=1)
    
    ax4.plot(times, mean_Et, color='k', lw=1.5, alpha=0.8, label=r'Total Energy $\langle E_{tot} \rangle$')
    ax4.plot(times, mean_Eu1, color='#1f77b4', lw=1.2, ls='--', label=r'Soft Mode $\langle E_{U1} \rangle$')
    ax4.plot(times, mean_Ep, color='#d62728', lw=1.2, ls=':', label=r'Hard Mode $\langle E_{\perp} \rangle$')
    
    ax4.set_xlim(times[0], times[-1])
    ax4.set_title("Global Energy Partitioning")
    ax4.set_xlabel("Time")
    ax4.set_ylabel("Mean Energy Density")
    ax4.grid(True, alpha=0.3)
    ax4.legend(loc='upper right', frameon=True)

    plt.tight_layout()
    plt.show()

# =============================================================================
# Main Execution
# =============================================================================

if __name__ == "__main__":
    # Run the physics
    z, history = run_simulation(
        n_points=200, 
        length=50.0, 
        total_time=250.0
    )
    
    # Render the plots
    plot_publication_results(z, history)