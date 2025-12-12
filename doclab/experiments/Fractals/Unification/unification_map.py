import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ----------------------------------------
# PARAMETERS
# ----------------------------------------
TWIST = 3.8
DT = 0.015
STEPS = 10000  # Run for a good duration to see the surface

# ----------------------------------------
# PHYSICS ENGINE (Tension Mode)
# ----------------------------------------
def get_force_unification(m, lam):
    # Teal Anchor
    F_teal_m = -(m + 0.866)
    F_teal_lam = -(lam - 0.5)

    # Red Anchor (Twisted)
    F_red_m = -(m - 0.0)
    p_violation = TWIST * np.sin(m * 2.5)
    F_red_lam = -(lam + 1.0) + p_violation

    # Gold = Vector Sum (Tension)
    F_gold_m = (F_teal_m + F_red_m)
    F_gold_lam = (F_teal_lam + F_red_lam)

    # Weights
    angle = np.degrees(np.arctan2(lam, m)) % 360
    
    # Fast Gaussian
    def gaussian(x, mu, sig):
        diff = np.minimum(np.abs(x - mu), 360 - np.abs(x - mu))
        return np.exp(-(diff/sig)**2)

    w_gold = gaussian(angle, 30, 80)
    w_teal = gaussian(angle, 150, 80)
    w_red = gaussian(angle, 270, 80)
    
    tot = w_gold + w_teal + w_red + 1e-6
    
    Fm = (w_teal * F_teal_m + w_red * F_red_m + w_gold * F_gold_m) / tot
    Flam = (w_teal * F_teal_lam + w_red * F_red_lam + w_gold * F_gold_lam) / tot
    
    return Fm, Flam

def jacobian_unification(m, lam, eps=1e-3):
    """Numerical Jacobian for U1 extraction"""
    Fm0, Flam0 = get_force_unification(m, lam)
    
    Fm_m, Flam_m = get_force_unification(m + eps, lam)
    Fm_p, Flam_p = get_force_unification(m - eps, lam)
    
    Fm_l, Flam_l = get_force_unification(m, lam + eps)
    Fm_lp, Flam_lp = get_force_unification(m, lam - eps)
    
    dFm_dm = (Fm_m - Fm_p) / (2*eps)
    dFlam_dm = (Flam_m - Flam_p) / (2*eps)
    dFm_dlam = (Fm_l - Fm_lp) / (2*eps)
    dFlam_dlam = (Flam_l - Flam_lp) / (2*eps)
    
    return np.array([[dFm_dm, dFm_dlam], [dFlam_dm, dFlam_dlam]])

def get_u1_basis(m, lam):
    """Find the 'Soft Mode' direction (eigenvector with smallest eigenvalue)"""
    J = jacobian_unification(m, lam)
    vals, vecs = np.linalg.eig(J)
    idx = np.argmin(np.abs(vals))
    e = vecs[:, idx].real
    n = np.linalg.norm(e)
    if n == 0: return np.array([1.0, 0.0])
    return e / n

def leapfrog_unification(m, lam, pm, plam, dt):
    Fm, Flam = get_force_unification(m, lam)
    pm_h = pm + 0.5 * dt * Fm
    plam_h = plam + 0.5 * dt * Flam
    m_n = m + dt * pm_h
    lam_n = lam + dt * plam_h
    Fm_n, Flam_n = get_force_unification(m_n, lam_n)
    pm_n = pm_h + 0.5 * dt * Fm_n
    plam_n = plam_h + 0.5 * dt * Flam_n
    return m_n, lam_n, pm_n, plam_n

def run_unification_map():
    # Initial Condition (The Stable Knot)
    m, lam = -0.5, 0.5
    pm, plam = 0.9, 0.4
    
    # Data Storage
    u1_component = []   # X: Electromagnetism (Soft Mode Projection)
    weak_component = [] # Y: Weak Force (Local Twist Magnitude)
    strong_component = [] # Z: Strong Force (Confining Energy/Perpendicular Motion)
    
    print("Mapping the Unification Surface...")
    
    # Warmup to settle into attractor
    for _ in range(2000):
        m, lam, pm, plam = leapfrog_unification(m, lam, pm, plam, DT)
        
    # Recording Loop
    for i in range(STEPS):
        # 1. Integrate
        m, lam, pm, plam = leapfrog_unification(m, lam, pm, plam, DT)
        
        # 2. Extract Components
        v_vec = np.array([pm, plam])
        
        # X: U1 Projection
        e_soft = get_u1_basis(m, lam)
        u1_val = np.dot(v_vec, e_soft)
        
        # Y: Weak Twist (Local Asymmetry)
        # This is the 'p_violation' term
        weak_val = TWIST * np.sin(m * 2.5)
        
        # Z: Strong Confinement (Perpendicular Velocity)
        # Energy NOT in the soft mode
        v_par = u1_val * e_soft
        v_perp = v_vec - v_par
        strong_val = np.linalg.norm(v_perp)
        
        u1_component.append(u1_val)
        weak_component.append(weak_val)
        strong_component.append(strong_val)

    # ----------------------------------------
    # PLOTTING
    # ----------------------------------------
    fig = plt.figure(figsize=(12, 10), facecolor='black')
    ax = fig.add_subplot(111, projection='3d', facecolor='black')
    
    # Scatter plot with color based on Strong Force intensity
    sc = ax.scatter(u1_component, weak_component, strong_component, 
                    c=strong_component, cmap='inferno', s=1, alpha=0.6)
    
    ax.set_xlabel('U(1) Soft Mode (Photon)', color='cyan')
    ax.set_ylabel('Weak Twist (Asymmetry)', color='red')
    ax.set_zlabel('Strong Tension (Confinement)', color='gold')
    
    ax.set_title(f"The Unification Map: Hopf Fibration of Forces\n(Twist={TWIST})", color='white', fontsize=16)
    
    # Hide grid panes for cleaner look
    ax.grid(False)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('#333333')
    ax.yaxis.pane.set_edgecolor('#333333')
    ax.zaxis.pane.set_edgecolor('#333333')
    ax.tick_params(colors='white')
    
    # Set view angle to see the structure best
    ax.view_init(elev=30, azim=45)
    
    plt.tight_layout()
    plt.savefig('unification_map.png')
    plt.show()

if __name__ == "__main__":
    run_unification_map()