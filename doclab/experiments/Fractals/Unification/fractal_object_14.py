import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.decomposition import PCA

# --------------------------------------------------
# PIROUETTE FRAMEWORK: PORTRAIT OF A FERMION
# --------------------------------------------------
# We input the Fundamental Constant we discovered
# (Twist = 2.83814) to visualize the "Perfect"
# Spin 1/2 Particle. We expect a double-loop
# or Mobius-like topology (720 deg symmetry).
# --------------------------------------------------

TWIST = 2.83814 # <--- THE MAGIC NUMBER
GAMMA = 0.05
DT = 0.005
STEPS = 50000
STABILIZE = 15000
# --- NEW PARAMETER for cleaner plot ---
SUBSAMPLE_RATE = 10 

def get_force_vectorized(m, lam):
    # --- Standard Pirouette Physics ---
    F_teal_m = -(m + 0.866) 
    F_teal_lam = -(lam - 0.5)
    F_red_m = -(m - 0.0)
    p_violation = TWIST * np.sin(m * 2.5) 
    F_red_lam = -(lam + 1.0) + p_violation
    sum_m = (F_teal_m + F_red_m)
    sum_lam = (F_teal_lam + F_red_lam)
    mag = np.sqrt(sum_m**2 + sum_lam**2)
    scale = np.sqrt(mag)
    F_gold_m = sum_m * scale
    F_gold_lam = sum_lam * scale
    
    angle = np.degrees(np.arctan2(lam, m)) % 360
    # Weights
    diff_g = np.minimum(np.abs(angle - 30), 360-np.abs(angle - 30))
    w_gold = np.exp(-(diff_g/80)**2)
    diff_t = np.minimum(np.abs(angle - 150), 360-np.abs(angle - 150))
    w_teal = np.exp(-(diff_t/80)**2)
    diff_r = np.minimum(np.abs(angle - 270), 360-np.abs(angle - 270))
    w_red = np.exp(-(diff_r/80)**2)
    
    tot = w_gold + w_teal + w_red + 1e-6
    nw_red, nw_teal, nw_gold = w_red/tot, w_teal/tot, w_gold/tot
    
    Fm = (nw_teal * F_teal_m + nw_red * F_red_m + nw_gold * F_gold_m)
    Flam = (nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam)
    
    return Fm, Flam, nw_red

def run_fermion_vis():
    print(f"Generating 4D Portrait of Spin 1/2 Particle (Twist={TWIST})...")
    
    # Coordinate from Poincare map
    m, lam = -1.8, 0.0
    pm, plam = 0.0, 2.0 # plam is the momentum conjugate to lambda
    
    # Stabilization (Unchanged)
    for _ in range(STABILIZE):
        # ... (stabilization logic using m, lam, pm, plam) ...
        Fm, Flam, w_red = get_force_vectorized(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag
        m += DT * pm
        lam += DT * plam
        
        Fm, Flam, w_red = get_force_vectorized(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag

    # Recording (4D History)
    hist_m = []
    hist_lam = []
    hist_pm = []
    hist_plam = [] # <--- RECORDING PLAM
    colors = []
    
    for i in range(STEPS):
        Fm, Flam, w_red = get_force_vectorized(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag
        m += DT * pm
        lam += DT * plam
        
        Fm, Flam, w_red = get_force_vectorized(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag
        
        hist_m.append(m)
        hist_lam.append(lam)
        hist_pm.append(pm)
        hist_plam.append(plam) # <--- ADDED
        colors.append(i)

    # ----------------------------------------
    # 4D to 3D Dimensionality Reduction (PCA)
    # ----------------------------------------
    print("Performing PCA on 4D phase space (m, lambda, pm, plam)...")
    
    # Create the 4D data matrix
    data_4d = np.vstack([hist_m, hist_lam, hist_pm, hist_plam]).T
    
    # 1. Standardize the data (important for PCA)
    # Standardize only if units are vastly different, otherwise skip this step
    # For now, let's assume they are comparable, but PCA should handle it.
    
    # 2. Run PCA to get the best 3D projection
    pca = PCA(n_components=3)
    data_3d = pca.fit_transform(data_4d)

    # The 3 new coordinates
    PC1 = data_3d[:, 0]
    PC2 = data_3d[:, 1]
    PC3 = data_3d[:, 2]

    # Subsample the data for a cleaner line plot
    SUBSAMPLE_RATE = 10 
    M = PC1[::SUBSAMPLE_RATE]
    L = PC2[::SUBSAMPLE_RATE]
    P = PC3[::SUBSAMPLE_RATE]
    C = np.array(colors[::SUBSAMPLE_RATE]) 
    
    # ----------------------------------------
    # PLOTTING 3D PCA Projection
    # ----------------------------------------
    fig = plt.figure(figsize=(12, 10), facecolor='black')
    ax = fig.add_subplot(111, projection='3d')
    # ... (axis setup remains the same) ...
    
    # Get the colormap
    norm = plt.Normalize(C.min(), C.max())
    cmap = plt.get_cmap('hsv')
    
    # Iterate over segments and plot them individually with their color
    for i in range(len(M) - 1):
        color = cmap(norm(C[i]))
        ax.plot(
            M[i:i+2], 
            L[i:i+2], 
            P[i:i+2], 
            color=color, 
            linewidth=1.0, 
            alpha=0.9
        )
        
    ax.set_xlabel(f'Principal Component 1 ({pca.explained_variance_ratio_[0]*100:.1f}%)', color='white')
    ax.set_ylabel(f'Principal Component 2 ({pca.explained_variance_ratio_[1]*100:.1f}%)', color='white')
    ax.set_zlabel(f'Principal Component 3 ({pca.explained_variance_ratio_[2]*100:.1f}%)', color='white')
    ax.tick_params(colors='white')
    
    # Title reflects the PCA projection
    ax.set_title(f"Fermion Soliton: 4D Phase Space PCA Projection\n(Twist = {TWIST})", color='white', fontsize=16)
    
    # Optimal View for the "Double Loop"
    ax.view_init(elev=20, azim=60)

    plt.tight_layout()
    plt.savefig('fermion_soliton_4d_pca.png')
    plt.show()

if __name__ == "__main__":
    run_fermion_vis()