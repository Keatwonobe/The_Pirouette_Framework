import numpy as np
from numba import njit, prange

@njit(parallel=True, fastmath=True)
def integrate_henon_heiles_optimized(m_flat, l_flat, t_max=50.0, dt=0.05, sigma=1.0):
    """
    Optimized integrator using Numba.
    1. Parallel execution across CPU cores.
    2. Lower escape threshold (r > 4.0 is usually sufficient past saddle points).
    3. Compiled machine code loops.
    """
    n = len(m_flat)
    out_m = np.empty(n, dtype=np.float64)
    out_l = np.empty(n, dtype=np.float64)
    
    # Escape threshold: Saddle points are at r=1/sigma. 
    # Once r > 3 or 4, the particle is ballistically escaping.
    escape_r2 = 16.0  
    steps = int(t_max / dt)

    for i in prange(n):
        m = m_flat[i]
        l = l_flat[i]
        pm = 0.0
        pl = 0.0
        
        active = True
        
        for _ in range(steps):
            # Symplectic Velocity Verlet (slightly more stable than the original custom one)
            # 1. Half-step momentum
            fm = -(m + 2*sigma*m*l)
            fl = -(l + sigma*(m**2 - l**2))
            
            pm += 0.5 * dt * fm
            pl += 0.5 * dt * fl
            
            # 2. Full-step position
            m += dt * pm
            l += dt * pl
            
            # 3. New Forces
            fm_new = -(m + 2*sigma*m*l)
            fl_new = -(l + sigma*(m**2 - l**2))
            
            # 4. Half-step momentum
            pm += 0.5 * dt * fm_new
            pl += 0.5 * dt * fl_new
            
            # Check escape
            if m*m + l*l > escape_r2:
                # Optional: Project slightly forward to stabilize angle? 
                # Not strictly necessary if r is large enough.
                active = False
                break
        
        out_m[i] = m
        out_l[i] = l
        
    return out_m, out_l

# --- HELPER TO PLUG INTO YOUR EXISTING CODE ---
def integrate_henon_heiles_batch(m_grid, l_grid, t_max=50.0, dt=0.1, sigma=1.0):
    # Flatten inputs for the Numba function
    shape = m_grid.shape
    m_flat = m_grid.flatten()
    l_flat = l_grid.flatten()
    
    # Run optimized kernel
    # Note: First run will include compilation time (~1-2s), subsequent runs are instant
    m_out, l_out = integrate_henon_heiles_optimized(m_flat, l_flat, t_max, dt, sigma)
    
    return m_out.reshape(shape), l_out.reshape(shape)