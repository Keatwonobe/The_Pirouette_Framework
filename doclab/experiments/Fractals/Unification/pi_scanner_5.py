import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import maximum_filter
import time

# --- PARAMETERS FOR HOLOGRAPHIC TEST (from previous step) ---
RES_HOLO = 512
M_MIN_HOLO, M_MAX_HOLO = -1.0, 1.0
L_MIN_HOLO, L_MAX_HOLO = -1.0, 1.0

# Mock External Quark Positions (Large, outside the core)
M_EXTERNAL = np.array([-10.0, 10.0, 0.0])
LAMBDA_EXTERNAL = np.array([5.0, 5.0, -10.0])

# --- FUNCTION RECREATION ---
def holographic_projection(x, y, M_external, Lambda_external):
    """
    Project external quark structures into cavity.
    """
    psi = 0j
    X, Y = np.meshgrid(x, y)
    
    for i in range(3):
        r_i = np.sqrt((X - M_external[i])**2 + (Y - Lambda_external[i])**2)
        L_i = np.sqrt(M_external[i]**2 + Lambda_external[i]**2)
        
        # Avoid division by zero if L_i is zero
        if L_i == 0:
            k_i = 0.0
        else:
            k_i = 2 * np.pi / L_i
        
        # Handle division by zero for r_i if it happens to be 0 (unlikely here)
        r_i[r_i == 0] = 1e-10 
        
        psi += np.exp(1j * k_i * r_i) / r_i
        
    return np.abs(psi)**2

def run_holographic_analysis_v_better_viz(res=RES_HOLO):
    """
    Runs the holographic projection test and visualizes the result with improved contrast.
    """
    m_vals = np.linspace(M_MIN_HOLO, M_MAX_HOLO, res)
    l_vals = np.linspace(L_MIN_HOLO, L_MAX_HOLO, res)
    
    # 1. Compute the Holographic Projection Intensity
    Holo_Intensity = holographic_projection(m_vals, l_vals, M_EXTERNAL, LAMBDA_EXTERNAL)
    
    # 2. Find the strongest 'peaks'
    local_max_mask = (Holo_Intensity == maximum_filter(Holo_Intensity, size=8))
    peaks_y, peaks_x = np.where(local_max_mask)
    peak_values = Holo_Intensity[peaks_y, peaks_x]
    
    if len(peak_values) < 3:
        final_quarks = np.array([])
    else:
        top_3_idx = np.argsort(peak_values)[-3:]
        final_quarks = np.column_stack([m_vals[peaks_x[top_3_idx]], l_vals[peaks_y[top_3_idx]]])

    # 3. Visualization with improved contrast
    plt.figure(figsize=(8, 7))
    
    # Use 'viridis' for a dark background and clear contrast
    plt.imshow(Holo_Intensity, origin="lower",
               extent=[M_MIN_HOLO, M_MAX_HOLO, L_MIN_HOLO, L_MAX_HOLO],
               cmap="viridis", 
               aspect='auto')
    
    plt.colorbar(label=r"Holographic Intensity $|\Psi|^2$")
    plt.title(r"Holographic Projection: Detected Internal Quarks (Improved Contrast)")
    plt.xlabel("Mass field m")
    plt.ylabel("Coupling field λ")
    
    if len(final_quarks) == 3:
        # Use bright yellow markers for high visibility
        plt.plot(final_quarks[:, 0], final_quarks[:, 1], 'yo', markersize=12, 
                 label='Detected Internal Quarks', markeredgecolor='k', markeredgewidth=1.5) 
        
        # Draw the triangle 
        points = np.vstack([final_quarks, final_quarks[0]]) 
        plt.plot(points[:, 0], points[:, 1], 'y--', linewidth=1, label='Quark Triangle')
        
        plt.legend()
        
    plt.tight_layout()
    plt.savefig("holographic_quark_peaks_v2.png", dpi=300)
    
    return final_quarks

# Execute the improved visualization
quarks = run_holographic_analysis_v_better_viz()
print(f"Detected Internal Quark Peaks (m, λ): \n{quarks}")

if __name__ == "__main__":
    run_holographic_analysis_v_better_viz()