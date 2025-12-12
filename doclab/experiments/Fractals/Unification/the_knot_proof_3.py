import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

# --- 1. Physics Constants ---
NUM_NODES = 120          # Higher resolution strings
BASE_DT = 0.01           # Base time step
MAX_MOVE_PER_STEP = 0.05 # Constraint: Nodes cannot move more than this per physics tick
STEPS = 350

# Physics Parameters
BASE_STIFFNESS = 0.5
MAX_STIFFNESS = 800.0    # The Planck Tension
VELOCITY_SCALING = 0.6   # How fast stiffness ramps up
CIRCULATION = 15.0       # Stronger Twist to ensure the "Hook"
CORE_RADIUS = 0.25       # Interaction radius

# --- 2. Biot-Savart (The Twist) ---
def get_biot_savart_velocity(target_points, filaments, gammas):
    total_vel = np.zeros_like(target_points)
    for fil, gamma in zip(filaments, gammas):
        for i in range(len(fil) - 1):
            p1, p2 = fil[i], fil[i+1]
            dl = p2 - p1
            midpoint = (p1 + p2) / 2.0
            r_vec = target_points - midpoint
            r_mag = np.linalg.norm(r_vec, axis=1)
            
            # Softened core to prevent division by zero, but allow strong interaction
            r_mag = np.maximum(r_mag, 0.05)
            
            cross_prod = np.cross(dl, r_vec)
            denominator = (r_mag**2 + CORE_RADIUS**2)**1.5
            factor = (gamma / (4 * np.pi)) / denominator
            total_vel += cross_prod * factor[:, np.newaxis]
    return total_vel

# --- 3. Topology Tracker ---
def calculate_linking_number(loop1, loop2):
    linking_sum = 0.0
    l1, l2 = loop1[::4], loop2[::4] 
    for i in range(len(l1) - 1):
        r1, dr1 = l1[i], l1[i+1] - l1[i]
        for j in range(len(l2) - 1):
            r2, dr2 = l2[j], l2[j+1] - l2[j]
            r12 = r1 - r2
            dist = np.linalg.norm(r12)
            if dist < 0.05: continue
            num = np.dot(r12, np.cross(dr1, dr2))
            den = dist**3
            linking_sum += num / den
    return linking_sum / (4 * np.pi)

# --- 4. Initialization ---
s = np.linspace(0, 1, NUM_NODES) 

# Start further out to allow speed to build
ANCHOR_DIST = 12.0
f1_x = -6 + s * (6 + ANCHOR_DIST)
f1_y = 2.0 * np.ones_like(s)
f1_z = 0.8 - s * 0.8
filament1 = np.column_stack((f1_x, f1_y, f1_z))

f2_x = 6 - s * (6 + ANCHOR_DIST)
f2_y = -2.0 * np.ones_like(s)
f2_z = -0.8 + s * 0.8
filament2 = np.column_stack((f2_x, f2_y, f2_z))

filaments = [filament1, filament2]
velocities = [np.zeros_like(filament1), np.zeros_like(filament2)]
gammas = [CIRCULATION, -CIRCULATION] # Retrograde Chirality

history = []
lk_history = []
stiffness_history = []

print("Simulating Causal Entanglement (Adaptive Sub-stepping)...")

# --- 5. Simulation Loop ---
for frame in range(STEPS):
    # Snapshot for animation
    history.append([f.copy() for f in filaments])
    
    # Topology Check
    if frame % 5 == 0:
        lk = calculate_linking_number(filaments[0], filaments[1])
        lk_history.append(lk)
    else:
        lk_history.append(lk_history[-1] if lk_history else 0)

    # --- PHYSICS SUB-STEPPING ---
    # We estimate the required time steps to prevent tunneling
    
    # 1. Get current max velocity estimate
    v1_max = np.max(np.linalg.norm(velocities[0], axis=1))
    v2_max = np.max(np.linalg.norm(velocities[1], axis=1))
    max_v = max(v1_max, v2_max, 1.0) # Avoid zero division
    
    # 2. Calculate sub-steps needed
    # We want max_v * dt < MAX_MOVE_PER_STEP
    # dt = MAX_MOVE / max_v
    # num_substeps = BASE_DT / dt
    needed_dt = MAX_MOVE_PER_STEP / max_v
    num_substeps = int(np.ceil(BASE_DT / needed_dt))
    
    # Cap sub-steps for performance (but keep it high)
    num_substeps = max(1, min(num_substeps, 100))
    sub_dt = BASE_DT / num_substeps
    
    # Log stiffness for the frame
    # (We calculate it based on the state at start of frame)
    head1, head2 = filaments[0][0], filaments[1][0]
    vel1, vel2 = velocities[0][0], velocities[1][0]
    v_rel = np.linalg.norm(vel1 - vel2)
    raw_k = BASE_STIFFNESS * np.exp(VELOCITY_SCALING * v_rel)
    frame_stiffness = np.clip(raw_k, 0, MAX_STIFFNESS)
    stiffness_history.append(frame_stiffness)

    # Execute Sub-steps
    for _ in range(num_substeps):
        new_filaments = []
        new_velocities = []
        
        # Re-calculate Dynamic Stiffness per sub-step for accuracy
        head1, head2 = filaments[0][0], filaments[1][0]
        vel1, vel2 = velocities[0][0], velocities[1][0]
        v_rel = np.linalg.norm(vel1 - vel2)
        
        current_k = np.clip(BASE_STIFFNESS * np.exp(VELOCITY_SCALING * v_rel), 0, MAX_STIFFNESS)
        
        # Calculate Tension Force
        r_12 = head2 - head1
        dist = np.linalg.norm(r_12)
        force_mag = current_k * dist
        
        # Safety for very close encounters
        safe_dist = max(dist, 0.01)
        force_vec = (r_12 / safe_dist) * force_mag
        
        forces = [force_vec, -force_vec]
        
        for f_idx, fil in enumerate(filaments):
            vel = velocities[f_idx]
            
            # Apply Tension to Head
            accel = np.zeros_like(vel)
            accel[0] = forces[f_idx]
            
            # Propagate (Chain physics)
            for i in range(1, 15):
                accel[i] = accel[0] * (0.85 ** i)
                
            # Update Velocity
            vel += accel * sub_dt
            
            # Damping (Energy loss to vacuum)
            vel *= 0.99 
            
            # Twist Flow (The Hook)
            v_twist = get_biot_savart_velocity(fil, filaments, gammas)
            
            # Update Position
            new_fil = fil + (vel + v_twist) * sub_dt
            
            # Anchor Tails
            new_fil[-5:] = fil[-5:]
            vel[-5:] = 0
            
            new_filaments.append(new_fil)
            new_velocities.append(vel)
            
        filaments = new_filaments
        velocities = new_velocities

# --- 6. Visualization ---
print("Rendering Proof...")
fig = plt.figure(figsize=(14, 6))

ax = fig.add_subplot(1, 2, 1, projection='3d')
ax2 = fig.add_subplot(1, 2, 2)

def update(frame):
    ax.clear()
    ax2.clear()
    
    try:
        f1 = history[frame][0]
        f2 = history[frame][1]
        
        if np.isnan(f1).any() or np.isnan(f2).any(): return

        # Draw Travelers
        ax.plot(f1[:,0], f1[:,1], f1[:,2], color='crimson', lw=2, label='Traveler (+)')
        ax.scatter(f1[0,0], f1[0,1], f1[0,2], color='red', s=100)
        
        ax.plot(f2[:,0], f2[:,1], f2[:,2], color='cyan', lw=2, label='Traveler (-)')
        ax.scatter(f2[0,0], f2[0,1], f2[0,2], color='blue', s=100)
        
        # Draw Vacuum Bond
        stiff = stiffness_history[frame]
        lw_stiff = min(stiff / 20.0, 6.0)
        color_stiff = 'gold'
        if stiff > MAX_STIFFNESS * 0.9: color_stiff = 'white'
            
        ax.plot([f1[0,0], f2[0,0]], [f1[0,1], f2[0,1]], [f1[0,2], f2[0,2]], 
                color=color_stiff, linestyle='--', linewidth=lw_stiff, alpha=0.7)
        
        # Dynamic Camera
        mid = (f1[0] + f2[0]) / 2
        dist = np.linalg.norm(f1[0] - f2[0])
        zoom = max(dist * 0.6, 1.5) # Zoom in close when they knot
        
        ax.set_xlim(mid[0]-zoom, mid[0]+zoom)
        ax.set_ylim(mid[1]-zoom, mid[1]+zoom)
        ax.set_zlim(mid[2]-zoom, mid[2]+zoom)
        ax.set_title(f"Stiffness: {stiff:.0f} | Substeps: {int(stiff/10)+1}")
        ax.legend(loc='lower left')
        
        # Plot Topology
        ax2.set_title(f"Linking Number (Current: {lk_history[frame]:.2f})")
        ax2.plot(lk_history[:frame], color='purple', lw=2)
        ax2.axhline(1.0, color='gray', linestyle=':', alpha=0.5)
        ax2.axhline(-1.0, color='gray', linestyle=':', alpha=0.5)
        ax2.set_ylim(-2, 2)
        ax2.grid(True)
    except:
        pass

ani = animation.FuncAnimation(fig, update, frames=len(history), interval=30)
plt.show()