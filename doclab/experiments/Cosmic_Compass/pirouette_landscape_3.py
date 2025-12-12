import numpy as np
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def generate_deep_field(resolution=3000, max_steps=1200, zoom=5.0, filename="phase_space_raw.npz"):
    """
    Generates the raw phase space data and saves to disk.
    Resolution=3000 will create a ~9 million vertex model.
    """
    logger.info(f"{'='*60}")
    logger.info(f"PHASE SPACE GENERATOR: {resolution}x{resolution}")
    logger.info(f"{'='*60}")
    
    # 1. Setup Grid
    # Shift L slightly (+0.2) to center the asymmetric 'Up' channel
    offset_l = 0.2 
    m_span = 1.2 * zoom
    l_span = 1.2 * zoom
    
    logger.info("Initializing Coordinate Grid...")
    m_vals = np.linspace(-m_span, m_span, resolution)
    l_vals = np.linspace(-l_span + offset_l, l_span + offset_l, resolution)
    
    # We use float32 to save RAM during calculation (precision is sufficient)
    M, L = np.meshgrid(m_vals.astype(np.float32), l_vals.astype(np.float32))
    
    # 2. Physics Constants
    sigma = 1.0 
    dt = 0.1
    
    p_m = np.zeros_like(M)
    p_l = np.zeros_like(L)
    active = np.ones_like(M, dtype=bool)
    
    # We store steps as uint16 to save space (max 65535 steps)
    escape_time = np.zeros_like(M, dtype=np.uint16) + max_steps
    basin_id = np.zeros_like(M, dtype=np.uint8) 

    logger.info("Integrating Hamiltonian Dynamics...")
    t0 = time.time()
    
    # 3. Integration Loop
    for step in range(1, max_steps + 1):
        if not np.any(active): break
        
        # --- Leapfrog Step ---
        # Gradient 1
        grad_m = M + 2 * sigma * M * L
        grad_l = L + sigma * (M**2 - L**2)
        p_m[active] -= 0.5 * dt * grad_m[active]
        p_l[active] -= 0.5 * dt * grad_l[active]
        
        # Drift
        M[active] += dt * p_m[active]
        L[active] += dt * p_l[active]
        
        # Gradient 2 (at new pos)
        grad_m = M + 2 * sigma * M * L
        grad_l = L + sigma * (M**2 - L**2)
        p_m[active] -= 0.5 * dt * grad_m[active]
        p_l[active] -= 0.5 * dt * grad_l[active]
        
        # --- Escape Logic ---
        # "Deep Field" bounds: check further out (r^2 > 25) to see the shelf clearly
        r2 = M**2 + L**2
        escaped_now = (r2 > 25.0) & active
        
        if np.any(escaped_now):
            theta = np.arctan2(L[escaped_now], M[escaped_now])
            
            # Basin Classification
            # 1=Teal (Up), 3=Red (Wings), 2=Gold (Down/Center)
            b_now = np.full(np.sum(escaped_now), 2, dtype=np.uint8) # Default Gold
            
            mask_teal = (theta > 0.5) & (theta < 2.5)
            mask_red  = (np.abs(theta) > 2.6)
            
            b_now[mask_teal] = 1
            b_now[mask_red] = 3
            
            basin_id[escaped_now] = b_now
            escape_time[escaped_now] = step
            active[escaped_now] = False
            
        if step % 100 == 0:
            logger.info(f"Step {step}/{max_steps} | Active: {np.sum(active)/active.size:.1%}")

    duration = time.time() - t0
    logger.info(f"Simulation Complete in {duration:.2f}s")
    
    # 4. Save Compressed Data
    logger.info(f"Saving to {filename}...")
    np.savez_compressed(filename, 
                        m_vals=m_vals, 
                        l_vals=l_vals, 
                        escape_time=escape_time, 
                        basin_id=basin_id,
                        meta=np.array([resolution, max_steps]))
    logger.info("Done.")

if __name__ == "__main__":
    # You can crank this resolution up now. 
    # 2000 is safe, 4000 is "Paper Quality" (but ~1GB file)
    generate_deep_field(resolution=4000, max_steps=1200, zoom=5.0)