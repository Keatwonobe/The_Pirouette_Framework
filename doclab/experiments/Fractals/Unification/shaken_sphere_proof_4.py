import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

# --- 1. Physics Constants ---
NUM_NODES = 80
DT = 0.005
STEPS = 400              # Long run to watch the "hunting" phase
STIFFNESS = 15.0         # The "Vacuum Stiffness" (Spring Constant)
CIRCULATION = 8.0        # The Twist/Vorticity
CORE_RADIUS = 0.1
ANCHOR_DIST = 12.0       # Distance to "Universe Wall"
DRAG = 0.05              # Slight viscosity to damp infinite oscillation

# --- 2. Biot-Savart (The Fluid/Twist Layer) ---
def get_biot_savart_velocity(target_points, filaments, gammas):
    total_vel = np.zeros_like(target_points)
    for fil, gamma in zip(filaments, gammas):
        for i in range(len(fil) - 1):
            p1, p2 = fil[i], fil[i+1]
            dl = p2 - p1
            midpoint = (p1 + p2) / 2.0
            r_vec = target_points - midpoint
            r_mag = np.linalg.norm(r_vec, axis=1)
            
            cross_prod = np.cross(dl, r_vec)
            denominator = (r_mag**2 + CORE_RADIUS**2)**1.5
            factor = (gamma / (4 * np.pi)) / denominator
            total_vel += cross_prod * factor[:, np.newaxis]
    return total_vel

# --- 3. Topology Tracker ---
def calculate_linking_number(loop1, loop2):
    linking_sum = 0.0
    # Downsample for speed
    l1, l2 = loop1[::2], loop2[::2]
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

# Start them OFFSET and FAR APART
# They are not aimed at the center anymore. 
# They are aimed "past" each other to prove they can FIND each other.
f1_x = -4 + s * (4 + ANCHOR_DIST)
f1_y = 2.0 * np.ones_like(s) 
f1_z = 1.0 - s * 1.0
filament1 = np.column_stack((f1_x, f1_y, f1_z))

f2_x = 4 - s * (4 + ANCHOR_DIST)
f2_y = -2.0 * np.ones_like(s)
f2_z = -1.0 + s * 1.0
filament2 = np.column_stack((f2_x, f2_y, f2_z))

filaments = [filament1, filament2]
velocities = [np.zeros_like(filament1), np.zeros_like(filament2)]
gammas = [CIRCULATION, CIRCULATION]

history = []
lk_history = []
dist_history = [] # To track how close they get

print("Vacuum Stiffness Activated. Travelers are seeking linkage...")

# --- 5. Simulation Loop ---
for step in range(STEPS):
    history.append([f.copy() for f in filaments])
    
    # Topology Check
    if step % 2 == 0:
        lk = calculate_linking_number(filaments[0], filaments[1])
        lk_history.append(lk)
    else:
        lk_history.append(lk_history[-1])

    # Physics Update
    new_filaments = []
    new_velocities = []
    
    # Calculate Mutual Vector (The "Tension")
    head1 = filaments[0][0]
    head2 = filaments[1][0]
    
    # Vector from 1 to 2
    r_12 = head2 - head1
    dist = np.linalg.norm(r_12)
    dist_history.append(dist)
    
    # Force Magnitude (Hooke's Law: F = k * x)
    # The "Vacuum Stiffness" pulls them together
    force_mag = STIFFNESS * dist
    force_vec = (r_12 / (dist + 1e-6)) * force_mag
    
    forces = [force_vec, -force_vec] # Equal and Opposite (Newton's 3rd)
    
    for f_idx, fil in enumerate(filaments):
        vel = velocities[f_idx]
        
        # A. Apply Vacuum Tension (Only to the HEAD node)
        # The head drags the rest of the string
        accel = np.zeros_like(vel)
        accel[0] = forces[f_idx] 
        
        # Propagate tension down the string (simplified elastic chain)
        # This makes the "snake" follow the head
        for i in range(1, 5): # First 5 nodes feel the tug immediately
             accel[i] = accel[0] * (0.8 ** i)

        # B. Update Velocity
        vel += accel * DT
        vel *= (1.0 - DRAG) # Damping stabilizes the orbit
        
        # C. Twist Flow (Biot-Savart)
        v_twist = get_biot_savart_velocity(fil, filaments, gammas)
        
        # D. Update Position
        new_fil = fil + (vel + v_twist) * DT
        
        # Anchor the tails
        new_fil[-5:] = fil[-5:] 
        vel[-5:] = 0
        
        new_filaments.append(new_fil)
        new_velocities.append(vel)
        
    filaments = new_filaments
    velocities = new_velocities

# --- 6. Visualization ---
print("Rendering the Linkage...")
fig = plt.figure(figsize=(14, 6))

ax = fig.add_subplot(1, 2, 1, projection='3d')
ax2 = fig.add_subplot(1, 2, 2)

def update(frame):
    ax.clear()
    ax2.clear()
    
    f1 = history[frame][0]
    f2 = history[frame][1]
    
    # Draw Travelers
    ax.plot(f1[:,0], f1[:,1], f1[:,2], color='crimson', alpha=0.6, label='Traveler A')
    ax.scatter(f1[0,0], f1[0,1], f1[0,2], color='red', s=60)
    
    ax.plot(f2[:,0], f2[:,1], f2[:,2], color='royalblue', alpha=0.6, label='Traveler B')
    ax.scatter(f2[0,0], f2[0,1], f2[0,2], color='blue', s=60)
    
    # Draw the "Vacuum Link" (The Invisible Tether)
    ax.plot([f1[0,0], f2[0,0]], 
            [f1[0,1], f2[0,1]], 
            [f1[0,2], f2[0,2]], 
            color='gold', linestyle='--', linewidth=1.5, alpha=0.8, label='Vacuum Tension')
    
    # Dynamic Camera
    mid = (f1[0] + f2[0]) / 2
    ax.set_xlim(mid[0]-3, mid[0]+3)
    ax.set_ylim(mid[1]-3, mid[1]+3)
    ax.set_zlim(mid[2]-3, mid[2]+3)
    ax.set_title(f"Frame {frame} | Manifold Stiffness: {STIFFNESS}")
    ax.legend(loc='lower left')
    
    # Plot Metrics
    ax2.set_title("Topological Convergence")
    ax2.plot(lk_history[:frame], color='purple', label='Linking Number')
    ax2.set_ylabel("Linking Number")
    
    # Overlay Distance on secondary axis
    ax3 = ax2.twinx()
    ax3.plot(dist_history[:frame], color='gold', linestyle=':', label='Separation Dist')
    ax3.set_ylabel("Head Separation", color='gold')
    
    ax2.grid(True)
    
ani = animation.FuncAnimation(fig, update, frames=len(history), interval=20)
plt.show()