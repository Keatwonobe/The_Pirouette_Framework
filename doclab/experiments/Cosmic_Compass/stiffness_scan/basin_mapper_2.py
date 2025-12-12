import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import time

def run_pirouette_expanded(resolution=1000, zoom_factor=2.0, damping=0.0):
    """
    Simulates the Pirouette Framework's Delta-substrate dynamics 
    with a wider Field of View and optional "Wound Channel" damping.
    
    Parameters:
    - resolution: Grid density (higher = more detail for the 'fleck')
    - zoom_factor: Multiplier for the field of view (1.0 = Paper standard)
    - damping: Friction coefficient (mimics Wound Channel memory/drag)
    """
    print(f"Initializing Expanded Pirouette Scan (Res: {resolution}x{resolution})...")
    print(f"Zoom Level: {zoom_factor}x | Wound Channel Damping: {damping}")
    
    # 1. Setup Expanded Grid
    # Standard paper bounds: m[-1.5, 1.5], l[-1.0, 2.0]
    # We expand these by zoom_factor, centered roughly on the Genesect (0, 0.5)
    
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
    max_steps = 200 # Paper standard [cite: 156]
    
    print("Evolving trajectories...")
    t0 = time.time()

    # 3. Integration with Optional Damping (The Wound Channel?)
    for step in range(max_steps):
        # Gradients
        grad_m = M + 2 * sigma * M * L
        grad_l = L + sigma * (M**2 - L**2)
        
        # Half-step momentum
        # Damping applies to momentum: F = -gradV - damping*v
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
            # Calculate angle theta for escaped particles
            # Paper definition: theta in radians
            theta = np.arctan2(L[escaped_now], M[escaped_now])
            
            # --- The "Proper" Region Layout  ---
            # Escape 1 (Teal/Weak): theta in (0.5, 2.5) -> Approx Top Left
            # Escape 3 (Red/Hypercharge): |theta| > 2.5 -> Bottom Wedge
            # Escape 2 (Gold/Strong): Remainder -> Approx Top Right
            
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
    colors = ['black', '#00CED1', '#DAA520', '#FF4500'] # Black, Teal, Gold, Red
    cmap = ListedColormap(colors)
    
    plt.figure(figsize=(12, 12))
    
    # Extent needs to match the new zoomed bounds
    extent = [m_vals[0], m_vals[-1], l_vals[0], l_vals[-1]]
    
    plt.imshow(status, origin='lower', extent=extent, cmap=cmap)
    plt.title(f"Pirouette v9 Extended Field\nZoom: {zoom_factor}x | Damping: {damping}")
    plt.xlabel(r"$m$ (Mass Field)")
    plt.ylabel(r"$\lambda$ (Coupling Field)")
    
    # Overlay the 'Standard' Paper Box to show where we were before
    # Paper bounds: m[-1.5, 1.5], l[-1.0, 2.0]
    box_x = [-1.5, 1.5, 1.5, -1.5, -1.5]
    box_y = [-1.0, -1.0, 2.0, 2.0, -1.0]
    plt.plot(box_x, box_y, 'w--', linewidth=1, alpha=0.7, label="Original Paper Bounds")
    plt.legend(loc='upper right')
    
    plt.show()

if __name__ == "__main__":
    # Run 1: Zoom out to look for elephants
    run_pirouette_expanded(resolution=1000, zoom_factor=2.5, damping=0.0)
    
    # Run 2: (Optional) Test the 'Wound Channel' Asymmetry
    # Uncomment below to see if drag creates the structural asymmetry
    # run_pirouette_expanded(resolution=1000, zoom_factor=1.0, damping=0.05)