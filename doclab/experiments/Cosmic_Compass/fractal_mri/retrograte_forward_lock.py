import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_gradient_magnitude

# Configuration
RESOLUTION = 400
BOUNDS = 1.5
GAMMA = 0.015  # Friction for retro
DT = 0.05
STEPS_RETRO = 1000
STEPS_FORWARD = 100

def get_potential_gradient(m, l):
    # Hénon-Heiles Potential Gradient
    # V = 0.5(m^2 + l^2) + m^2*l - l^3/3
    # dV/dm = m + 2ml
    # dV/dl = l + m^2 - l^2
    dm = m + 2 * m * l
    dl = l + (m**2 - l**2)
    return dm, dl

def generate_retro_map(res, bounds, gamma):
    # Retrograde: Dissipative Structure (Sedimentation)
    m_vals = np.linspace(-bounds, bounds, res)
    l_vals = np.linspace(-bounds, bounds, res)
    M, L = np.meshgrid(m_vals, l_vals)
    
    m, l = M.copy(), L.copy()
    vm = np.zeros_like(m)
    vl = np.zeros_like(l)
    orbit_length = np.zeros_like(m)
    active = np.ones_like(m, dtype=bool)
    
    for _ in range(STEPS_RETRO):
        if not np.any(active): break
        
        grad_m, grad_l = get_potential_gradient(m[active], l[active])
        
        # Damped update
        vm[active] += (-grad_m - gamma * vm[active]) * DT
        vl[active] += (-grad_l - gamma * vl[active]) * DT
        
        m[active] += vm[active] * DT
        l[active] += vl[active] * DT
        
        speed = np.sqrt(vm[active]**2 + vl[active]**2)
        orbit_length[active] += speed
        
        # Stop conditions
        stopped = speed < 0.01
        escaped = (m[active]**2 + l[active]**2) > 10.0
        
        # Update active mask
        # We need to map the subset 'active' back to the full grid
        # Just update the full grid directly for simplicity in this script structure
        # (Optimization: boolean indexing is tricky with state updates in place, 
        #  so we'll just update everyone who is active)
        still_active_indices = np.where(active)[0] 
        # Actually, let's just do full grid update for code clarity in VM, it's fast enough for 400x400
        
    return orbit_length

def generate_forward_map(res, bounds):
    # Forward: Basin Boundaries / Escape Time
    # We essentially want to find the "edges"
    m_vals = np.linspace(-bounds, bounds, res)
    l_vals = np.linspace(-bounds, bounds, res)
    M, L = np.meshgrid(m_vals, l_vals)
    
    m, l = M.copy(), L.copy()
    pm = np.zeros_like(m)
    pl = np.zeros_like(l)
    
    # We map "Exit Basin"
    # 0: Trapped/Long time, 1, 2, 3: The three escapes
    # Escape condition: r > 2.0. Angle determines basin.
    basin_map = np.zeros_like(m)
    
    for _ in range(STEPS_FORWARD):
        grad_m, grad_l = get_potential_gradient(m, l)
        
        pm -= grad_m * DT
        pl -= grad_l * DT
        m += pm * DT
        l += pl * DT
        
        # Check escape
        r2 = m**2 + l**2
        escaped = r2 > 4.0 # r=2
        
        # Determine basin for escaped particles
        # Angles: 
        # Basin 1 (Top): ~90 deg (pi/2)
        # Basin 2 (Bottom Left): ~210 deg (7pi/6)
        # Basin 3 (Bottom Right): ~330 deg (11pi/6)
        
        if np.any(escaped):
            theta = np.arctan2(l, m)
            # Map theta to basin ID [1, 2, 3]
            # Simple angle checks
            # Note: We only mark *newly* escaped points to avoid overwriting
            # But simpler: just process final state.
            pass
            
    # Final state processing for basins
    theta = np.arctan2(l, m)
    r2 = m**2 + l**2
    escaped = r2 > 4.0
    
    # Basin 1: Top (lambda > 0 mainly) - theta around pi/2
    mask1 = escaped & ((theta > np.pi/6) & (theta < 5*np.pi/6))
    
    # Basin 2: Bottom Left - theta around -5pi/6 (-150 deg)
    # theta is in [-pi, pi]
    # -pi to -pi/2 area
    mask2 = escaped & ((theta < -np.pi/2) | (theta > 5*np.pi/6)) 
    # Wait, 5pi/6 is 150deg. -pi/2 is -90. 
    # Let's use simple geometric cuts for the 3-fold symmetry
    # Symmetry axes are at 90, 210, 330.
    
    basin_map[mask1] = 1
    
    # Correct basin mapping based on standard Henon-Heiles exits
    # Exit A: y -> infinity (theta ~ 90)
    # Exit B: theta ~ 210
    # Exit C: theta ~ 330
    
    basin_map[escaped & (theta > np.pi/6) & (theta < 5*np.pi/6)] = 1  # Top
    basin_map[escaped & (theta >= 5*np.pi/6)] = 2 # Left (part 1)
    basin_map[escaped & (theta <= -5*np.pi/6)] = 2 # Left (part 2)
    basin_map[escaped & (theta > -5*np.pi/6) & (theta < -np.pi/6)] = 3 # Right (Wait, need to check geometry)
    
    # Actually, easier proxy for "Boundary" is just "Time to Escape" or Lyapunov
    # But user specifically mentioned Wada basins.
    # Let's stick to Basin Boundaries.
    # A cleaner way to get boundaries is to calculate the gradient of the *Escape Time*
    # because boundaries are where escape time diverges or changes rapidly.
    # Let's use Escape Time gradient as the "Forward Structure".
    
    return basin_map, m, l # returning final m,l for debug if needed

def generate_escape_time_map(res, bounds):
    m_vals = np.linspace(-bounds, bounds, res)
    l_vals = np.linspace(-bounds, bounds, res)
    M, L = np.meshgrid(m_vals, l_vals)
    
    m, l = M.copy(), L.copy()
    pm = np.zeros_like(m)
    pl = np.zeros_like(l)
    escape_time = np.full_like(m, STEPS_FORWARD * DT)
    
    active = np.ones_like(m, dtype=bool)
    
    for t in range(STEPS_FORWARD):
        if not np.any(active): break
        
        # Symplectic Euler / Verlet-ish
        grad_m, grad_l = get_potential_gradient(m[active], l[active])
        pm[active] -= grad_m * DT
        pl[active] -= grad_l * DT
        m[active] += pm[active] * DT
        l[active] += pl[active] * DT
        
        r2 = m[active]**2 + l[active]**2
        escaped_now = r2 > 4.0
        
        # Update escape times for those who just escaped
        # We need to map back to full array. 
        # A bit tedious with boolean masking subsets. 
        # Let's just do full array update, it's vectorised.
        
        # Re-evaluate full array for simplicity
        r2_full = m**2 + l**2
        escaped_full = r2_full > 4.0
        
        # If currently active AND escaped, record time
        just_escaped = active & escaped_full
        escape_time[just_escaped] = t * DT
        active[just_escaped] = False
        
    return escape_time

# 1. Generate Maps
print("Generating Retro Map...")
retro_map = generate_retro_map(RESOLUTION, BOUNDS, GAMMA)

print("Generating Forward Map...")
forward_map = generate_escape_time_map(RESOLUTION, BOUNDS)

# 2. Process for Overlay
# Retro: Normalize log scale
retro_disp = np.log1p(retro_map)
retro_disp = (retro_disp - retro_disp.min()) / (retro_disp.max() - retro_disp.min())

# Forward: Gradient Magnitude to find boundaries
grad = gaussian_gradient_magnitude(forward_map, sigma=1)
forward_boundaries = (grad - grad.min()) / (grad.max() - grad.min())
# Threshold to make it sharp lines
forward_edges = forward_boundaries > 0.1

# 3. Topology Slice Analysis
# We take a circular cut at r = 0.5 (halfway to bounds)
# This cuts through the "arms" and the "basins"
r_cut = 0.5
theta_vals = np.linspace(0, 2*np.pi, 360)
x_cut = r_cut * np.cos(theta_vals)
y_cut = r_cut * np.sin(theta_vals)

# Interpolate values along the cut
from scipy.ndimage import map_coordinates

# Coordinate transform to pixel space
# Bounds: [-1.5, 1.5] -> [0, 400]
def world_to_pixel(w):
    return (w + BOUNDS) / (2 * BOUNDS) * (RESOLUTION - 1)

pixel_x = world_to_pixel(x_cut)
pixel_y = world_to_pixel(y_cut)
coords = np.vstack((pixel_y, pixel_x)) # map_coordinates expects (row, col) i.e. (y, x)

retro_profile = map_coordinates(retro_disp, coords, order=1)
forward_profile = map_coordinates(forward_boundaries, coords, order=1)

# Normalize profiles for comparison
retro_norm = (retro_profile - np.min(retro_profile)) / (np.max(retro_profile) - np.min(retro_profile))
forward_norm = (forward_profile - np.min(forward_profile)) / (np.max(forward_profile) - np.min(forward_profile))

# 4. Plotting
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# Overlay Image
ax1.imshow(retro_disp, cmap='bone', origin='lower', extent=[-BOUNDS, BOUNDS, -BOUNDS, BOUNDS])
# Create a masked array for the forward edges to overlay them clearly
# Use a color map that stands out against 'bone' (black/white/blue) -> Red or Bright Orange
ax1.contour(forward_map, levels=15, colors='cyan', linewidths=0.5, alpha=0.5, 
            extent=[-BOUNDS, BOUNDS, -BOUNDS, BOUNDS])
ax1.set_title("Overlay: Retro Structure (Bone) + Forward Boundaries (Cyan)")

# Topology Slice
ax2.plot(np.degrees(theta_vals), retro_norm, color='black', label='Retro Structure (Stability)', linewidth=2)
ax2.plot(np.degrees(theta_vals), forward_norm, color='cyan', label='Forward Tension (Boundary)', linewidth=1.5, alpha=0.8)
ax2.set_xlabel("Angle (degrees)")
ax2.set_ylabel("Normalized Intensity")
ax2.set_title(f"Topology Slice at r={r_cut}")
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('topology_analysis.png')
print("Analysis complete.")

# Re-configure and re-run
STEPS_FORWARD = 500  # Increased from 100
STEPS_RETRO = 1000
RESOLUTION = 300     # Slightly lower for speed given more steps
R_CUT = 1.0          # Further out to hit the arms

print("Regenerating maps with higher steps...")
retro_map = generate_retro_map(RESOLUTION, BOUNDS, GAMMA)
forward_map = generate_escape_time_map(RESOLUTION, BOUNDS) # Using escape time for structure

print(f"Retro Map Range: {retro_map.min()} - {retro_map.max()}")
print(f"Forward Map Range: {forward_map.min()} - {forward_map.max()}")

# Process
retro_disp = np.log1p(retro_map)
# Normalize
if retro_disp.max() > retro_disp.min():
    retro_disp = (retro_disp - retro_disp.min()) / (retro_disp.max() - retro_disp.min())

# Gradient of forward map
grad = gaussian_gradient_magnitude(forward_map, sigma=1)
forward_boundaries = grad
if forward_boundaries.max() > forward_boundaries.min():
    forward_boundaries = (forward_boundaries - forward_boundaries.min()) / (forward_boundaries.max() - forward_boundaries.min())

# Slice
theta_vals = np.linspace(0, 2*np.pi, 360)
x_cut = R_CUT * np.cos(theta_vals)
y_cut = R_CUT * np.sin(theta_vals)

# Pixel coords
pixel_x = world_to_pixel(x_cut)
pixel_y = world_to_pixel(y_cut)
coords = np.vstack((pixel_y, pixel_x))

retro_profile = map_coordinates(retro_disp, coords, order=1)
forward_profile = map_coordinates(forward_boundaries, coords, order=1)

# Norm profiles
r_min, r_max = retro_profile.min(), retro_profile.max()
f_min, f_max = forward_profile.min(), forward_profile.max()

if r_max > r_min:
    retro_norm = (retro_profile - r_min) / (r_max - r_min)
else:
    retro_norm = retro_profile

if f_max > f_min:
    forward_norm = (forward_profile - f_min) / (f_max - f_min)
else:
    forward_norm = forward_profile

# Correlation
import numpy as np
if r_max > r_min and f_max > f_min:
    correlation = np.corrcoef(retro_norm, forward_norm)[0, 1]
    print(f"Correlation: {correlation:.4f}")
else:
    print("Cannot compute correlation (flat profile)")

# Plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# Overlay
ax1.imshow(retro_disp, cmap='bone', origin='lower', extent=[-BOUNDS, BOUNDS, -BOUNDS, BOUNDS])
ax1.contour(forward_boundaries, levels=[0.2, 0.4, 0.6], colors='cyan', linewidths=0.5, alpha=0.7, 
            extent=[-BOUNDS, BOUNDS, -BOUNDS, BOUNDS])
ax1.set_title("Overlay: Retro (Bone) + Forward Boundaries (Cyan)")

# Slice
ax2.plot(np.degrees(theta_vals), retro_norm, 'w-', label='Retro Stability', linewidth=2)
ax2.plot(np.degrees(theta_vals), forward_norm, 'c-', label='Forward Boundary', linewidth=1.5, alpha=0.8)
# Add filled area to show overlap
ax2.fill_between(np.degrees(theta_vals), 0, np.minimum(retro_norm, forward_norm), color='gray', alpha=0.3, label='Overlap')

ax2.set_facecolor('black')
ax2.grid(color='white', alpha=0.1)
ax2.legend(facecolor='black', labelcolor='white')
ax2.set_title(f"Topology Slice at r={R_CUT}")

plt.tight_layout()
plt.savefig('topology_overlay_final.png')

def generate_retro_map_robust(res, bounds, gamma):
    m_vals = np.linspace(-bounds, bounds, res)
    l_vals = np.linspace(-bounds, bounds, res)
    M, L = np.meshgrid(m_vals, l_vals)
    
    m, l = M.copy(), L.copy()
    vm = np.zeros_like(m)
    vl = np.zeros_like(l)
    orbit_length = np.zeros_like(m)
    active = np.ones_like(m, dtype=bool)
    
    dt = 0.05
    
    for _ in range(1000): # Steps
        if not np.any(active): break
        
        # Only process active points to save time?
        # To avoid indexing hell, we can process full arrays but mask the delta
        # Or use simple flattening.
        
        # Flatten for easy indexing
        m_flat = m.ravel()
        l_flat = l.ravel()
        vm_flat = vm.ravel()
        vl_flat = vl.ravel()
        active_flat = active.ravel()
        orbit_flat = orbit_length.ravel()
        
        # Indices of active particles
        idx = np.where(active_flat)[0]
        
        if len(idx) == 0: break
        
        # Subset
        m_sub = m_flat[idx]
        l_sub = l_flat[idx]
        vm_sub = vm_flat[idx]
        vl_sub = vl_flat[idx]
        
        # Physics
        dm_sub = m_sub + 2 * m_sub * l_sub
        dl_sub = l_sub + (m_sub**2 - l_sub**2)
        
        vm_sub += (-dm_sub - gamma * vm_sub) * dt
        vl_sub += (-dl_sub - gamma * vl_sub) * dt
        
        m_sub += vm_sub * dt
        l_sub += vl_sub * dt
        
        speed_sub = np.sqrt(vm_sub**2 + vl_sub**2)
        orbit_flat[idx] += speed_sub
        
        # Check stop/escape
        stopped = speed_sub < 0.01
        escaped = (m_sub**2 + l_sub**2) > 10.0
        
        # Deactivate
        # indices in 'sub' that are done
        done_sub_mask = stopped | escaped
        
        # Map back to global 'active'
        # The indices in 'idx' corresponding to 'done_sub_mask' need to be set False in active_flat
        done_global_indices = idx[done_sub_mask]
        active_flat[done_global_indices] = False
        
        # Update state arrays
        m_flat[idx] = m_sub
        l_flat[idx] = l_sub
        vm_flat[idx] = vm_sub
        vl_flat[idx] = vl_sub
        
        # Reshape back (optional, but needed if we accessed m again as 2D, but we use flat next iter)
        # Actually we just keep flat pointers? No, we need to return 2D.
        # Just update the flat views, they point to the same memory?
        # Numpy flatten() returns a copy usually. ravel() returns a view if possible.
        # To be safe, let's just write back.
        pass 
        # Actually ravel() is a view, so writing to m_flat modifies m?
        # m_flat[idx] = m_sub works? 
        # Let's verifying:
        # m.ravel()[0] = 99 -> m[0,0] is 99? Yes.
        # But `m_flat = m.ravel()` ... `m_flat[idx] = ...`
        # Safe.
    
    return orbit_length

# Re-run with robust function
print("Regenerating Retro Map Robustly...")
retro_map = generate_retro_map_robust(300, 1.5, 0.015)

# Forward map was fine?
print("Regenerating Forward Map...")
forward_map = generate_escape_time_map(300, 1.5)

# Range check
print(f"Retro Range: {np.nanmin(retro_map)} - {np.nanmax(retro_map)}")
print(f"Forward Range: {forward_map.min()} - {forward_map.max()}")

# ... Proceed with Overlay (Copy paste processing logic)
# Process
retro_disp = np.log1p(retro_map)
if retro_disp.max() > retro_disp.min():
    retro_disp = (retro_disp - retro_disp.min()) / (retro_disp.max() - retro_disp.min())

# Gradient of forward map
grad = gaussian_gradient_magnitude(forward_map, sigma=1)
forward_boundaries = grad
if forward_boundaries.max() > forward_boundaries.min():
    forward_boundaries = (forward_boundaries - forward_boundaries.min()) / (forward_boundaries.max() - forward_boundaries.min())

# Slice
R_CUT = 1.0 # Radius
theta_vals = np.linspace(0, 2*np.pi, 360)
x_cut = R_CUT * np.cos(theta_vals)
y_cut = R_CUT * np.sin(theta_vals)

# Pixel coords
pixel_x = world_to_pixel(x_cut)
pixel_y = world_to_pixel(y_cut)
coords = np.vstack((pixel_y, pixel_x))

retro_profile = map_coordinates(retro_disp, coords, order=1)
forward_profile = map_coordinates(forward_boundaries, coords, order=1)

# Norm profiles
r_min, r_max = retro_profile.min(), retro_profile.max()
f_min, f_max = forward_profile.min(), forward_profile.max()

retro_norm = (retro_profile - r_min) / (r_max - r_min + 1e-9)
forward_norm = (forward_profile - f_min) / (f_max - f_min + 1e-9)

# Correlation
correlation = np.corrcoef(retro_norm, forward_norm)[0, 1]
print(f"Correlation: {correlation:.4f}")

# Plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# Overlay
ax1.imshow(retro_disp, cmap='bone', origin='lower', extent=[-BOUNDS, BOUNDS, -BOUNDS, BOUNDS])
ax1.contour(forward_boundaries, levels=[0.3], colors='cyan', linewidths=0.8, alpha=0.8, 
            extent=[-BOUNDS, BOUNDS, -BOUNDS, BOUNDS])
ax1.set_title("Overlay: Retro (Bone) + Forward Boundaries (Cyan)")

# Slice
ax2.plot(np.degrees(theta_vals), retro_norm, 'w-', label='Retro Stability', linewidth=2)
ax2.plot(np.degrees(theta_vals), forward_norm, 'c-', label='Forward Boundary', linewidth=1.5, alpha=0.8)
ax2.fill_between(np.degrees(theta_vals), 0, np.minimum(retro_norm, forward_norm), color='gray', alpha=0.3, label='Overlap')

ax2.set_facecolor('black')
ax2.grid(color='white', alpha=0.1)
ax2.legend(facecolor='black', labelcolor='white')
ax2.set_title(f"Topology Slice at r={R_CUT} | Corr: {correlation:.2f}")

plt.tight_layout()
plt.savefig('topology_overlay_final.png')