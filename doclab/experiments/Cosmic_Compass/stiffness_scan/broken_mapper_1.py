import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import time

def run_pirouette_wound_channel(resolution=1000, zoom_factor=2.5, damping=0.05):
    """
    Simulates the 'Wound Channel' activation.
    Introduces Damping (Vacuum Memory) to break Parity Symmetry.
    
    Target: Reproduce the Teal(Weak) vs Gold(Strong) asymmetry.
    """
    print(f"Initializing WOUND CHANNEL Simulation...")
    print(f"Symmetry Breaking Condition: Damping = {damping}")
    
    # 1. Setup Grid (Zoomed to see the Lobes clearly)
    m_center, l_center = 0.0, 0.5
    m_span = 3.0 * zoom_factor
    l_span = 3.0 * zoom_factor
    
    m_vals = np.linspace(m_center - m_span/2, m_center + m_span/2, resolution)
    l_vals = np.linspace(l_center - l_span/2, l_center + l_span/2, resolution)
    M, L = np.meshgrid(m_vals, l_vals)
    
    # 2. Initialize State
    p_m = np.zeros_like(M)
    p_l = np.zeros_like(L)
    status = np.zeros_like(M, dtype=int)
    active_mask = np.ones_like(M, dtype=bool)
    
    # Parameters
    sigma = 1.0 
    dt = 0.1
    max_steps = 250 # Slightly longer to let the friction take effect
    
    print("Injecting Temporal Stress (Evolving)...")
    t0 = time.time()

    # 3. Integration with Vacuum Drag
    for step in range(max_steps):
        # Gradients
        grad_m = M + 2 * sigma * M * L
        grad_l = L + sigma * (M**2 - L**2)
        
        # Half-step momentum with DAMPING (The Wound Channel)
        # The damping term (-damping * p) represents energy lost to the substrate geometry
        p_m_half = p_m - (dt / 2) * grad_m - (damping * p_m * dt / 2)
        p_l_half = p_l - (dt / 2) * grad_l - (damping * p_l * dt / 2)
        
        # Full-step position
        M = M + dt * p_m_half
        L = L + dt * p_l_half
        
        # New Gradients
        grad_m_new = M + 2 * sigma * M * L
        grad_l_new = L + sigma * (M**2 - L**2)
        
        # Full-step momentum
        p_m = p_m_half - (dt / 2) * grad_m_new - (damping * p_m_half * dt / 2)
        p_l = p_l_half - (dt / 2) * grad_l_new - (damping * p_l_half * dt / 2)
        
        # -- Check Escape Conditions --
        r2 = M**2 + L**2
        escaped_now = (r2 > 20) & active_mask
        
        if np.any(escaped_now):
            theta = np.arctan2(L[escaped_now], M[escaped_now])
            
            # Escape 1 (Teal/Weak): (0.5, 2.5)
            # Escape 3 (Red/Hypercharge): |theta| > 2.5
            # Escape 2 (Gold/Strong): Remainder
            
            mask_e1 = (theta > 0.5) & (theta < 2.5)
            mask_e3 = np.abs(theta) > 2.5
            mask_e2 = ~(mask_e1 | mask_e3)
            
            current_status = status[escaped_now]
            current_status[mask_e1] = 1 # Teal
            current_status[mask_e2] = 2 # Gold
            current_status[mask_e3] = 3 # Red
            status[escaped_now] = current_status
            
            active_mask[escaped_now] = False
            
            if not np.any(active_mask):
                break

    dt_sim = time.time() - t0
    print(f"Complete in {dt_sim:.2f}s.")

    # 4. Calculate Asymmetry Stats
    count_teal = np.sum(status == 1)
    count_gold = np.sum(status == 2)
    
    # Avoid div by zero
    if count_teal == 0: count_teal = 1 
    ratio = count_gold / count_teal
    
    print("-" * 30)
    print(f"ASYMMETRY RESULT (Damping {damping}):")
    print(f"Teal Pixels (Weak):   {count_teal}")
    print(f"Gold Pixels (Strong): {count_gold}")
    print(f"Gold/Teal Ratio:      {ratio:.4f}")
    print("-" * 30)

    # 5. Visualization
    colors = ['black', '#00CED1', '#DAA520', '#FF4500'] 
    cmap = ListedColormap(colors)
    
    plt.figure(figsize=(12, 12))
    extent = [m_vals[0], m_vals[-1], l_vals[0], l_vals[-1]]
    
    plt.imshow(status, origin='lower', extent=extent, cmap=cmap)
    plt.title(f"The Broken Mirror\nWound Channel Active (Damping={damping}) | Ratio: {ratio:.2f}")
    plt.xlabel(r"$m$ (Mass Field)")
    plt.ylabel(r"$\lambda$ (Coupling Field)")
    
    plt.show()

if __name__ == "__main__":
    run_pirouette_wound_channel()