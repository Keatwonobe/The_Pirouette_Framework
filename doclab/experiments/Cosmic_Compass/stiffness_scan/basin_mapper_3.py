import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import time

def run_pirouette_deep_field(resolution=1200, zoom_factor=10.0, max_steps=1000, damping=0.0):
    """
    Simulates the Pirouette Framework's Delta-substrate dynamics 
    at MACROSCOPIC scales (Deep Field).
    
    Parameters:
    - resolution: High res needed to see filaments in the deep field.
    - zoom_factor: Multiplier for the field of view (10x, 20x).
    - max_steps: Increased to allow far-away particles time to interact.
    """
    print(f"Initializing DEEP FIELD Pirouette Scan...")
    print(f"Resolution: {resolution}x{resolution}")
    print(f"Zoom: {zoom_factor}x | Steps: {max_steps} | Damping: {damping}")
    
    # 1. Setup Deep Field Grid
    # Center roughly on the Genesect (0, 0.5)
    m_center, l_center = 0.0, 0.5
    # Standard span is 3.0, so we multiply
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
    
    print("Evolving trajectories (this may take a moment due to step count)...")
    t0 = time.time()

    # 3. Integration Loop
    for step in range(max_steps):
        # Gradients
        grad_m = M + 2 * sigma * M * L
        grad_l = L + sigma * (M**2 - L**2)
        
        # Half-step momentum (with optional damping)
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
        
        # In Deep Field, we only mark escape if they go WAY out past the zoom
        # Or we can keep the standard '20' threshold to see the "Valleys" clearly.
        # Let's keep the standard threshold to visualize the "Drainpipes".
        escaped_now = (r2 > 20) & active_mask
        
        if np.any(escaped_now):
            theta = np.arctan2(L[escaped_now], M[escaped_now])
            
            # Escape 1 (Teal): (0.5, 2.5)
            # Escape 3 (Red): |theta| > 2.5
            # Escape 2 (Gold): Remainder
            
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

    # 4. Visualization
    colors = ['black', '#00CED1', '#DAA520', '#FF4500'] 
    cmap = ListedColormap(colors)
    
    plt.figure(figsize=(12, 12))
    extent = [m_vals[0], m_vals[-1], l_vals[0], l_vals[-1]]
    
    plt.imshow(status, origin='lower', extent=extent, cmap=cmap)
    plt.title(f"Pirouette Deep Field\nZoom: {zoom_factor}x | Damping: {damping}")
    plt.xlabel(r"$m$ (Mass Field)")
    plt.ylabel(r"$\lambda$ (Coupling Field)")
    
    # Draw a box showing the "v9 Paper" scale for context
    # Paper bounds: m[-1.5, 1.5], l[-1.0, 2.0]
    box_x = [-1.5, 1.5, 1.5, -1.5, -1.5]
    box_y = [-1.0, -1.0, 2.0, 2.0, -1.0]
    plt.plot(box_x, box_y, 'w--', linewidth=0.8, alpha=0.5, label="Paper v9 Scale")
    plt.legend(loc='upper right')
    
    plt.show()

if __name__ == "__main__":
    # The "Gravity" Run - Zooming way out
    run_pirouette_deep_field(resolution=1000, zoom_factor=10.0, max_steps=1000, damping=0.0)
    
    # If you want to see if the "sheet hogging" breaks the deep structure:
    # run_pirouette_deep_field(resolution=1000, zoom_factor=10.0, max_steps=1000, damping=0.05)