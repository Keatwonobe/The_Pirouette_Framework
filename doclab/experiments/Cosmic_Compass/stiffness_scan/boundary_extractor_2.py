import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LightSource
from mpl_toolkits.mplot3d import Axes3D
import time

def generate_wada_photo(resolution=500, zoom=4.0, max_steps=1000, filename="wada_summit.png"):
    print(f"[1/4] Initializing Physics Grid ({resolution}x{resolution})...")
    
    # 1. Setup Grid
    # M (Mass) corresponds to x, L (Lambda) corresponds to y
    m_span = 3.0 * zoom
    l_span = 3.0 * zoom
    m_vals = np.linspace(-m_span/2, m_span/2, resolution)
    l_vals = np.linspace(-l_span/2 + 0.5, l_span/2 + 0.5, resolution) # Centered on interaction region
    M, L = np.meshgrid(m_vals, l_vals)

    # 2. Physics Integration (Leapfrog Hénon-Heiles)
    # Constants
    sigma = 1.0
    dt = 0.1
    p_m = np.zeros_like(M)
    p_l = np.zeros_like(L)
    
    # Tracking arrays
    active_mask = np.ones_like(M, dtype=bool)
    escape_steps = np.zeros_like(M, dtype=float) + max_steps
    status = np.zeros_like(M, dtype=int) # 0=Trapped
    
    print(f"[2/4] Integrating Trajectories (Max Steps: {max_steps})...")
    t0 = time.time()
    
    # Vectorized integration loop
    for step in range(1, max_steps + 1):
        if not np.any(active_mask): break
            
        # Half-step momentum
        grad_m = M + 2 * sigma * M * L
        grad_l = L + sigma * (M**2 - L**2)
        p_m[active_mask] -= 0.5 * dt * grad_m[active_mask]
        p_l[active_mask] -= 0.5 * dt * grad_l[active_mask]
        
        # Full-step position
        M[active_mask] += dt * p_m[active_mask]
        L[active_mask] += dt * p_l[active_mask]
        
        # Half-step momentum (new position)
        grad_m = M + 2 * sigma * M * L
        grad_l = L + sigma * (M**2 - L**2)
        p_m[active_mask] -= 0.5 * dt * grad_m[active_mask]
        p_l[active_mask] -= 0.5 * dt * grad_l[active_mask]
        
        # Check escapes (r^2 > 20)
        r2 = M**2 + L**2
        escaped_now = (r2 > 20.0) & active_mask
        
        if np.any(escaped_now):
            # Calculate exit angle for color classification
            theta = np.arctan2(L[escaped_now], M[escaped_now])
            
            # Map angles to basins (Teal/Gold/Red)
            # Basin 1 (Teal): 0.5 < theta < 2.5
            # Basin 3 (Red): |theta| > 2.5
            # Basin 2 (Gold): Remaining
            s_now = np.zeros(np.sum(escaped_now), dtype=int)
            mask_1 = (theta > 0.5) & (theta < 2.5)
            mask_3 = np.abs(theta) > 2.5
            mask_2 = ~(mask_1 | mask_3)
            
            s_now[mask_1] = 1 # Teal
            s_now[mask_2] = 2 # Gold
            s_now[mask_3] = 3 # Red
            
            status[escaped_now] = s_now
            escape_steps[escaped_now] = step
            active_mask[escaped_now] = False

    print(f"      Integration done in {time.time()-t0:.2f}s")

    # 3. Prepare Visualization Data
    print("[3/4] Baking Textures and Heightmaps...")
    
    # Height Z is log of stability (trapped = high, quick escape = low)
    Z = np.log1p(escape_steps)
    # Normalize Z for visual height
    Z_norm = Z / np.max(Z)
    
    # Create the RGB color texture map based on status
    # Colors: 0=Black, 1=Teal, 2=Gold, 3=Red
    colors = np.zeros((resolution, resolution, 3))
    
    # Define Palette (Normalized RGB)
    c_black = np.array([0.05, 0.05, 0.05]) # Dark Grey for stability
    c_teal  = np.array([0.0, 0.8, 0.8])
    c_gold  = np.array([0.9, 0.7, 0.1])
    c_red   = np.array([0.9, 0.3, 0.1])
    
    colors[status == 0] = c_black
    colors[status == 1] = c_teal
    colors[status == 2] = c_gold
    colors[status == 3] = c_red

    # 4. Render 3D Surface
    print("[4/4] Raytracing Surface (Matplotlib)...")
    
    fig = plt.figure(figsize=(12, 10), dpi=150) # High DPI for "Photo" quality
    ax = fig.add_subplot(111, projection='3d')
    
    # Lighting: This adds the 3D depth perception
    ls = LightSource(azdeg=315, altdeg=45)
    
    # Shade the color map based on the Z-height gradients
    shaded_rgb = ls.shade_rgb(colors, Z_norm, vert_exag=0.5, blend_mode='soft')
    
    # Plot Surface
    # rstride/cstride=1 gives full resolution (might be slow, increase to 2 for speed)
    surf = ax.plot_surface(
        np.linspace(-m_span/2, m_span/2, resolution), 
        np.linspace(-l_span/2, l_span/2, resolution), 
        Z_norm, 
        facecolors=shaded_rgb,
        rstride=1, cstride=1, # Optimization: Render mesh at half-res, but colors are full-res
        linewidth=0, 
        antialiased=False, 
        shade=False # We already shaded it manually
    )
    
    # Aesthetics
    ax.set_zlim(0, 1.2)
    ax.axis('off') # Turn off ugly grid box for a clean "object" look
    ax.view_init(elev=55, azim=-45) # "Isometric-like" view looking into the triangle
    
    plt.title("The Pirouette Manifold: Stability as Height", color='white', fontsize=14)
    fig.patch.set_facecolor('#111111') # Dark background
    ax.set_facecolor('#111111')
    
    print(f"      Saving to {filename}...")
    plt.savefig(filename, facecolor=fig.get_facecolor(), bbox_inches='tight', pad_inches=0)
    print("      Done.")

if __name__ == "__main__":
    generate_wada_photo()