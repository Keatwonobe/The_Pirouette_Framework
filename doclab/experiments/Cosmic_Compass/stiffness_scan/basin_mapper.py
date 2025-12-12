import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import time

def run_pirouette_simulation(resolution=800, max_steps=200, dt=0.1):
    """
    Simulates the Pirouette Framework's Delta-substrate dynamics 
    to visualize the Wada basins and test for asymmetry.
    """
    print(f"Initializing Field Pirouette Simulation ({resolution}x{resolution})...")
    
    # 1. Setup the Grid (m, lambda) parameter space
    # Matches boundaries from Section 2.4.2 [cite: 148]
    m_vals = np.linspace(-1.5, 1.5, resolution)
    l_vals = np.linspace(-1.0, 2.0, resolution)
    M, L = np.meshgrid(m_vals, l_vals)
    
    # 2. Initialize State
    # p_m and p_l start at 0
    p_m = np.zeros_like(M)
    p_l = np.zeros_like(L)
    
    # Arrays to track particle status
    # 0 = Trapped (Black), 1,2,3 = Escaped (Colors)
    status = np.zeros_like(M, dtype=int)
    active_mask = np.ones_like(M, dtype=bool)
    
    # Sigma (surface tension parameter)
    # The paper implies sigma=1 for standard Hénon-Heiles, though not explicitly set to a number.
    # We assume sigma=1.0 for the cubic term m^2*lambda - lambda^3/3
    sigma = 1.0 
    
    print("Evolving trajectories via Leapfrog integration...")
    t0 = time.time()

    # 3. Leapfrog Integration Loop 
    for step in range(max_steps):
        # -- Gradient Calculation (dH/dm, dH/dlambda) --
        # H = 0.5(p^2) + 0.5(m^2 + l^2) + sigma(m^2*l - l^3/3)
        # dH/dm = m + 2*sigma*m*l
        # dH/dl = l + sigma*(m^2 - l^2)
        
        # Current gradients
        grad_m = M + 2 * sigma * M * L
        grad_l = L + sigma * (M**2 - L**2)
        
        # Half-step momentum update [cite: 149]
        p_m_half = p_m - (dt / 2) * grad_m
        p_l_half = p_l - (dt / 2) * grad_l
        
        # Full-step position update [cite: 151]
        M = M + dt * p_m_half
        L = L + dt * p_l_half
        
        # Re-evaluate gradients at new position
        grad_m_new = M + 2 * sigma * M * L
        grad_l_new = L + sigma * (M**2 - L**2)
        
        # Full-step momentum update [cite: 152]
        p_m = p_m_half - (dt / 2) * grad_m_new
        p_l = p_l_half - (dt / 2) * grad_l_new
        
        # -- Check Escape Conditions [cite: 157-161] --
        r2 = M**2 + L**2
        escaped_now = (r2 > 20) & active_mask
        
        if np.any(escaped_now):
            # Calculate angle theta for escaped particles
            # theta = arctan2(lambda, m)
            theta = np.arctan2(L[escaped_now], M[escaped_now])
            
            # Classify Basins based on paper definitions:
            # Note: Paper uses theta thresholds. 
            # Escape 1 (Teal/Weak): theta in (0.5, 2.5)
            # Escape 2 (Gold/Strong): theta not in (0.5, 2.5) but |theta| < 2.5
            # Escape 3 (Red/Hypercharge): |theta| > 2.5
            
            # Using masks for vectorized classification
            mask_e1 = (theta > 0.5) & (theta < 2.5)
            mask_e3 = np.abs(theta) > 2.5
            mask_e2 = ~(mask_e1 | mask_e3) # The remainder
            
            # Assign codes: 0=Trapped, 1=Teal, 2=Gold, 3=Red
            # We need to map these to the indices in 'escaped_now'
            current_status = status[escaped_now]
            current_status[mask_e1] = 1
            current_status[mask_e2] = 2
            current_status[mask_e3] = 3
            status[escaped_now] = current_status
            
            # Mark as inactive so we don't simulate them into infinity
            active_mask[escaped_now] = False
            
            # Stop if everything has escaped (unlikely with trapped region)
            if not np.any(active_mask):
                break

    dt_sim = time.time() - t0
    print(f"Simulation complete in {dt_sim:.2f} seconds.")

    # 4. Asymmetry Analysis
    # Count pixels in each basin
    count_trapped = np.sum(status == 0)
    count_teal = np.sum(status == 1) # Eq to SU(2)
    count_gold = np.sum(status == 2) # Eq to SU(3)
    count_red = np.sum(status == 3)  # Eq to U(1)
    
    total = resolution * resolution
    print("-" * 30)
    print("BASIN MEASURES (Statistical Invariants):")
    print(f"Trapped (Particles): {count_trapped / total:.4f}")
    print(f"Basin 1 (Teal): {count_teal / total:.4f}")
    print(f"Basin 2 (Gold): {count_gold / total:.4f}")
    print(f"Basin 3 (Red):  {count_red / total:.4f}")
    
    # Check Asymmetry (Left vs Right Lobe)
    # Right Lobe: m > 0, lambda > 0 (approx)
    # Left Lobe: m < 0, lambda > 0 (approx)
    # We can check simple pixel counts in quadrants
    
    print("-" * 30)
    print("ASYMMETRY CHECK:")
    # Defined roughly by the geometry in Figure 3
    right_lobe_mask = (status != 0) & (M > 0.5) & (L > 0.5)
    left_lobe_mask = (status != 0) & (M < -0.5) & (L > 0.5)
    
    r_count = np.sum(right_lobe_mask)
    l_count = np.sum(left_lobe_mask)
    
    print(f"Right Lobe Pixel Count: {r_count}")
    print(f"Left Lobe Pixel Count:  {l_count}")
    print(f"Ratio (R/L): {r_count/l_count:.3f} (Expect ~1.9 based on paper)")

    # 5. Visualization
    # Custom colormap: Black, Teal, Gold, Red
    colors = ['black', '#00CED1', '#DAA520', '#FF4500']
    cmap = ListedColormap(colors)
    
    plt.figure(figsize=(10, 10))
    plt.imshow(status, origin='lower', extent=[-1.5, 1.5, -1.0, 2.0], cmap=cmap)
    plt.title(f"The Field Pirouette (v9)\nHénon-Heiles Wada Basins")
    plt.xlabel(r"$m$ (Mass Field)")
    plt.ylabel(r"$\lambda$ (Coupling Field)")
    plt.colorbar(ticks=[0, 1, 2, 3], label="Basin Fate")
    plt.show()

if __name__ == "__main__":
    run_pirouette_simulation()