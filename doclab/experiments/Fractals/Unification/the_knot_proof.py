import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

# --- 1. Physics Constants ---
NUM_NODES = 100
DT = 0.01
STEPS = 300
BASE_STIFFNESS = 2.0     # Resting tension of the vacuum
VELOCITY_SCALING = 0.5   # How much speed increases stiffness (The "Scream" factor)
CIRCULATION = 12.0       # Strong Vorticity
CORE_RADIUS = 0.2
ANCHOR_DIST = 15.0       # Infinite Tails

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
            
            # Desingularized Biot-Savart
            cross_prod = np.cross(dl, r_vec)
            denominator = (r_mag**2 + CORE_RADIUS**2)**1.5
            factor = (gamma / (4 * np.pi)) / denominator
            total_vel += cross_prod * factor[:, np.newaxis]
    return total_vel

# --- 3. Topology Tracker ---
def calculate_linking_number(loop1, loop2):
    linking_sum = 0.0
    l1, l2 = loop1[::3], loop2[::3] # Optimization
    for i in range(len(l1) - 1):
        r1, dr1 = l1[i], l1[i+1] - l1[i]
        for j in range(len(l2) - 1):
            r2, dr2 = l2[j], l2[j+1] - l2[j]
            r12 = r1 - r2
            dist = np.linalg.norm(r12)
            if dist < 0.1: continue
            num = np.dot(r12, np.cross(dr1, dr2))
            den = dist**3
            linking_sum += num / den
    return linking_sum / (4 * np.pi)

# --- 4. Initialization ---
s = np.linspace(0, 1, NUM_NODES) 

# Initial Setup: Parallel but offset tracks
# They are flying past each other, like in your "Traveler Zoom"
f1_x = -5 + s * (5 + ANCHOR_DIST)
f1_y = 1.5 * np.ones_like(s)
f1_z = 0.5 - s * 0.5
filament1 = np.column_stack((f1_x, f1_y, f1_z))

f2_x = 5 - s * (5 + ANCHOR_DIST)
f2_y = -1.5 * np.ones_like(s)
f2_z = -0.5 + s * 0.5
filament2 = np.column_stack((f2_x, f2_y, f2_z))

filaments = [filament1, filament2]
velocities = [np.zeros_like(filament1), np.zeros_like(filament2)]
# OPPOSITE SIGNS for Chirality/Retrograde Time
gammas = [CIRCULATION, -CIRCULATION] 

history = []
lk_history = []
tension_history = []

print("Simulating Vacuum Stiffness (Elastic Entanglement)...")

# --- 5. Simulation Loop ---
for step in range(STEPS):
    history.append([f.copy() for f in filaments])
    
    # Topology
    if step % 2 == 0:
        lk = calculate_linking_number(filaments[0], filaments[1])
        lk_history.append(lk)
    else:
        lk_history.append(lk_history[-1])

    new_filaments = []
    new_velocities = []
    
    # --- VACUUM DYNAMICS ---
    head1, head2 = filaments[0][0], filaments[1][0]
    vel1, vel2 = velocities[0][0], velocities[1][0]
    
    # 1. Calculate Relative Velocity
    v_rel = np.linalg.norm(vel1 - vel2)
    
    # 2. Stiffness rises Exponentially with Speed
    # This is your "Black Flash" condition
    current_k = BASE_STIFFNESS * np.exp(VELOCITY_SCALING * v_rel)
    tension_history.append(current_k)
    
    # 3. Calculate Tension Force (Hooke's Law)
    r_12 = head2 - head1
    dist = np.linalg.norm(r_12)
    force_mag = current_k * dist
    force_vec = (r_12 / (dist + 1e-6)) * force_mag
    
    forces = [force_vec, -force_vec]
    
    for f_idx, fil in enumerate(filaments):
        vel = velocities[f_idx]
        
        # Apply tension to HEAD only
        accel = np.zeros_like(vel)
        accel[0] = forces[f_idx]
        
        # Drag/Damping (Vacuum Viscosity)
        vel *= 0.96 
        
        # Propagate tension down the string (The "Whip" effect)
        # Nodes follow their parents
        for i in range(1, 10):
            accel[i] = accel[0] * (0.7 ** i)

        vel += accel * DT
        
        # Add Biot-Savart Twist
        v_twist = get_biot_savart_velocity(fil, filaments, gammas)
        
        # Update
        new_fil = fil + (vel + v_twist) * DT
        
        # Anchor Tails
        new_fil[-5:] = fil[-5:]
        vel[-5:] = 0
        
        new_filaments.append(new_fil)
        new_velocities.append(vel)
        
    filaments = new_filaments
    velocities = new_velocities

# --- 6. Visualization ---
print("Rendering the Knot...")
fig = plt.figure(figsize=(14, 6))

ax = fig.add_subplot(1, 2, 1, projection='3d')
ax2 = fig.add_subplot(1, 2, 2)

def update(frame):
    ax.clear()
    ax2.clear()
    
    f1 = history[frame][0]
    f2 = history[frame][1]
    
    # Draw Travelers
    # Retrograde Traveler is Cyan, Normal is Red
    ax.plot(f1[:,0], f1[:,1], f1[:,2], color='crimson', lw=2, label='Traveler (+)')
    ax.scatter(f1[0,0], f1[0,1], f1[0,2], color='red', s=100, edgecolors='white')
    
    ax.plot(f2[:,0], f2[:,1], f2[:,2], color='cyan', lw=2, label='Traveler (-)')
    ax.scatter(f2[0,0], f2[0,1], f2[0,2], color='blue', s=100, edgecolors='white')
    
    # Draw the GOLD LINE (Vacuum Tension)
    # Thickness scales with Stiffness
    stiff = tension_history[frame]
    lw_stiff = min(stiff / 5.0, 5.0)
    ax.plot([f1[0,0], f2[0,0]], [f1[0,1], f2[0,1]], [f1[0,2], f2[0,2]], 
            color='gold', linestyle='--', linewidth=lw_stiff, alpha=0.8, label='Vacuum Bond')
    
    mid = (f1[0] + f2[0]) / 2
    zoom = 3.0
    ax.set_xlim(mid[0]-zoom, mid[0]+zoom)
    ax.set_ylim(mid[1]-zoom, mid[1]+zoom)
    ax.set_zlim(mid[2]-zoom, mid[2]+zoom)
    ax.set_title(f"Elastic Entanglement | Stiffness: {stiff:.1f}")
    ax.legend(loc='lower right')
    
    # Plot Topology
    ax2.set_title("Topological Locking")
    ax2.plot(lk_history[:frame], color='purple', lw=2)
    ax2.set_ylabel("Linking Number")
    ax2.set_xlabel("Time")
    ax2.set_ylim(-2, 2)
    ax2.grid(True)
    
ani = animation.FuncAnimation(fig, update, frames=len(history), interval=30)
plt.show()