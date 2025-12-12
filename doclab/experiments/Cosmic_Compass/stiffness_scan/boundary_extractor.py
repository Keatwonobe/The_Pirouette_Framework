import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from scipy.ndimage import sobel, generic_filter
import time

def extract_basin_boundaries(resolution=800, zoom_factor=1.0, max_steps=500):
    """
    Extract the fractal boundaries between basins - where trajectories
    are maximally sensitive and interlocking occurs.
    """
    print(f"Mapping Basin Boundaries...")
    print(f"Resolution: {resolution}x{resolution} | Zoom: {zoom_factor}x")
    
    # Setup grid
    m_center, l_center = 0.0, 0.5
    m_span = 3.0 * zoom_factor
    l_span = 3.0 * zoom_factor
    
    m_vals = np.linspace(m_center - m_span/2, m_center + m_span/2, resolution)
    l_vals = np.linspace(l_center - l_span/2, l_center + l_span/2, resolution)
    M, L = np.meshgrid(m_vals, l_vals)
    
    # Initialize
    p_m = np.zeros_like(M)
    p_l = np.zeros_like(L)
    status = np.zeros_like(M, dtype=int)
    active_mask = np.ones_like(M, dtype=bool)
    
    sigma = 1.0
    dt = 0.1
    
    print("Evolving trajectories...")
    t0 = time.time()
    
    # Integration loop
    for step in range(max_steps):
        grad_m = M + 2 * sigma * M * L
        grad_l = L + sigma * (M**2 - L**2)
        
        p_m_half = p_m - (dt / 2) * grad_m
        p_l_half = p_l - (dt / 2) * grad_l
        
        M = M + dt * p_m_half
        L = L + dt * p_l_half
        
        grad_m_new = M + 2 * sigma * M * L
        grad_l_new = L + sigma * (M**2 - L**2)
        
        p_m = p_m_half - (dt / 2) * grad_m_new
        p_l = p_l_half - (dt / 2) * grad_l_new
        
        r2 = M**2 + L**2
        escaped_now = (r2 > 20) & active_mask
        
        if np.any(escaped_now):
            theta = np.arctan2(L[escaped_now], M[escaped_now])
            
            mask_e1 = (theta > 0.5) & (theta < 2.5)
            mask_e3 = np.abs(theta) > 2.5
            mask_e2 = ~(mask_e1 | mask_e3)
            
            current_status = status[escaped_now]
            current_status[mask_e1] = 1
            current_status[mask_e2] = 2
            current_status[mask_e3] = 3
            status[escaped_now] = current_status
            
            active_mask[escaped_now] = False
            
            if not np.any(active_mask):
                break
    
    print(f"Complete in {time.time() - t0:.2f}s")
    
    # Extract boundaries using gradient detection
    print("Extracting boundaries...")
    
    # Sobel edge detection
    edges_m = np.abs(sobel(status, axis=0))
    edges_l = np.abs(sobel(status, axis=1))
    boundary_strength = np.sqrt(edges_m**2 + edges_l**2)
    
    # Normalize
    boundary_strength = boundary_strength / (np.max(boundary_strength) + 1e-10)
    
    # Also detect triple points (where all three basins meet)
    def count_unique_neighbors(window):
        """Count unique basin types in neighborhood"""
        unique = len(np.unique(window[window > 0]))
        return unique
    
    print("Finding triple points...")
    neighbor_diversity = generic_filter(status.astype(float), count_unique_neighbors, size=3)
    triple_points = (neighbor_diversity >= 3)
    
    return status, boundary_strength, triple_points, m_vals, l_vals


def compute_coherence_gradient(resolution=800, zoom_factor=1.0):
    """
    Compute the coherence field σ = ∂²V/∂m∂λ across the space.
    This should be high at boundaries where interlocking occurs.
    """
    print("Computing coherence gradient field...")
    
    m_center, l_center = 0.0, 0.5
    m_span = 3.0 * zoom_factor
    l_span = 3.0 * zoom_factor
    
    m_vals = np.linspace(m_center - m_span/2, m_center + m_span/2, resolution)
    l_vals = np.linspace(l_center - l_span/2, l_center + l_span/2, resolution)
    M, L = np.meshgrid(m_vals, l_vals)
    
    # V = (m² + λ²)/2 + σ·m²·λ - σ·λ³/3
    # ∂V/∂m = m + 2σ·m·λ
    # ∂²V/∂m∂λ = 2σ·m  <- The coherence coupling term!
    
    sigma = 1.0
    coherence_field = 2 * sigma * M
    
    # Also compute the full gradient magnitude
    grad_V_m = M + 2 * sigma * M * L
    grad_V_l = L + sigma * (M**2 - L**2)
    grad_magnitude = np.sqrt(grad_V_m**2 + grad_V_l**2)
    
    return coherence_field, grad_magnitude, m_vals, l_vals


def analyze_boundary_coherence():
    """
    Main analysis: overlay boundary structure with coherence field
    to find the 'learning secret' - where interlocking happens.
    """
    resolution = 600
    zoom = 1.0
    
    # Get basin boundaries
    status, boundaries, triple_pts, m_vals, l_vals = extract_basin_boundaries(
        resolution=resolution, zoom_factor=zoom
    )
    
    # Get coherence field
    coherence, grad_mag, _, _ = compute_coherence_gradient(
        resolution=resolution, zoom_factor=zoom
    )
    
    extent = [m_vals[0], m_vals[-1], l_vals[0], l_vals[-1]]
    
    # Create comprehensive visualization
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    
    # 1. Basin structure
    colors = ['black', '#00CED1', '#DAA520', '#FF4500']
    cmap = ListedColormap(colors)
    ax1 = axes[0, 0]
    ax1.imshow(status, origin='lower', extent=extent, cmap=cmap)
    ax1.set_title("Basin Structure")
    ax1.set_xlabel("m (Mass Field)")
    ax1.set_ylabel("λ (Coupling Field)")
    
    # 2. Boundary strength
    ax2 = axes[0, 1]
    im2 = ax2.imshow(boundaries, origin='lower', extent=extent, cmap='hot')
    ax2.set_title("Boundary Strength\n(Where Decision Happens)")
    ax2.set_xlabel("m")
    plt.colorbar(im2, ax=ax2, label="∇(Basin)")
    
    # 3. Triple points
    ax3 = axes[0, 2]
    ax3.imshow(status, origin='lower', extent=extent, cmap=cmap, alpha=0.3)
    ax3.imshow(triple_pts, origin='lower', extent=extent, cmap='Reds', alpha=0.7)
    ax3.set_title("Triple Points\n(Maximum Undecidability)")
    ax3.set_xlabel("m")
    
    # 4. Coherence field
    ax4 = axes[1, 0]
    im4 = ax4.imshow(coherence, origin='lower', extent=extent, cmap='RdBu_r')
    ax4.set_title("Coherence Field σ\n(∂²V/∂m∂λ)")
    ax4.set_ylabel("λ (Coupling Field)")
    ax4.set_xlabel("m")
    plt.colorbar(im4, ax=ax4, label="2σm")
    
    # 5. Gradient magnitude
    ax5 = axes[1, 1]
    im5 = ax5.imshow(grad_mag, origin='lower', extent=extent, cmap='viridis')
    ax5.set_title("Potential Gradient |∇V|")
    ax5.set_xlabel("m")
    plt.colorbar(im5, ax=ax5, label="|∇V|")
    
    # 6. THE KEY PLOT: Boundaries overlaid on coherence
    ax6 = axes[1, 2]
    ax6.imshow(coherence, origin='lower', extent=extent, cmap='RdBu_r', alpha=0.6)
    boundary_overlay = ax6.contour(m_vals, l_vals, boundaries, 
                                    levels=[0.3, 0.5, 0.7], 
                                    colors='yellow', linewidths=2)
    ax6.clabel(boundary_overlay, inline=True, fontsize=8)
    ax6.set_title("THE LEARNING SECRET:\nBoundaries on Coherence Field")
    ax6.set_xlabel("m")
    
    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/boundary_coherence_analysis.png', dpi=150, bbox_inches='tight')
    print("\nSaved: boundary_coherence_analysis.png")
    
    # Statistical analysis
    print("\n" + "="*60)
    print("BOUNDARY-COHERENCE STATISTICS")
    print("="*60)
    
    # Where are the strongest boundaries?
    strong_boundary = boundaries > 0.5
    boundary_coords = np.where(strong_boundary)
    
    if len(boundary_coords[0]) > 0:
        # Get m, λ coordinates of boundaries
        m_boundary = m_vals[boundary_coords[1]]
        l_boundary = l_vals[boundary_coords[0]]
        
        # Coherence at boundaries
        coherence_at_boundary = coherence[strong_boundary]
        
        print(f"\nBoundary points: {len(m_boundary)}")
        print(f"Mean coherence at boundaries: {np.mean(coherence_at_boundary):.4f}")
        print(f"Std coherence at boundaries: {np.std(coherence_at_boundary):.4f}")
        print(f"Max boundary coherence: {np.max(coherence_at_boundary):.4f}")
        print(f"Min boundary coherence: {np.min(coherence_at_boundary):.4f}")
        
        # Are boundaries aligned with coherence contours?
        print(f"\nm-coordinate range at boundaries: [{np.min(m_boundary):.3f}, {np.max(m_boundary):.3f}]")
        print(f"λ-coordinate range at boundaries: [{np.min(l_boundary):.3f}, {np.max(l_boundary):.3f}]")
        
        # Triple points analysis
        triple_coords = np.where(triple_pts)
        if len(triple_coords[0]) > 0:
            m_triple = m_vals[triple_coords[1]]
            l_triple = l_vals[triple_coords[0]]
            coherence_at_triple = coherence[triple_pts]
            
            print(f"\nTriple points: {len(m_triple)}")
            print(f"Mean coherence at triple points: {np.mean(coherence_at_triple):.4f}")
            print(f"These are the HIGH INFORMATION regions!")
    
    plt.show()
    
    return status, boundaries, coherence, triple_pts


if __name__ == "__main__":
    status, boundaries, coherence, triple_pts = analyze_boundary_coherence()