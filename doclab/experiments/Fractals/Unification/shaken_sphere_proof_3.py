import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

# --- 1. Physics Engine Constants ---
NUM_NODES = 100          # High resolution
DT = 0.005               # Tiny time step to handle high speed
STEPS = 300              # Longer run
GRAVITY_STRENGTH = 15.0  # The "m/s/s" acceleration constant
CIRCULATION = 10.0       # The twist strength
CORE_RADIUS = 0.15       # Thickness of the string
ANCHOR_DIST = 15.0       # Where the tails are pinned

# --- 2. Biot-Savart Law (The Twist Field) ---
def get_biot_savart_velocity(target_points, filaments, gammas):
    total_vel = np.zeros_like(target_points)
    for fil, gamma in zip(filaments, gammas):
        for i in range(len(fil) - 1):
            p1, p2 = fil[i], fil[i+1]
            dl = p2 - p1
            midpoint = (p1 + p2) / 2.0
            r_vec = target_points - midpoint
            r_mag = np.linalg.norm(r_vec, axis=1)
            
            # Vectorized Cross Product
            cross_prod = np.cross(dl, r_vec)
            denominator = (r_mag**2 + CORE_RADIUS**2)**1.5
            factor = (gamma / (4 * np.pi)) / denominator
            total_vel += cross_prod * factor[:, np.newaxis]
    return total_vel

# --- 3. Topology: Gauss Linking Integral ---
def calculate_linking_number(loop1, loop2):
    linking_sum = 0.0
    # Downsample for speed (calculate topology on every 2nd node)
    l1 = loop1[::2]
    l2 = loop2[::2]
    
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

# Initial Positions (Travelers starting far apart)
# Head at index 0, Tail at index -1
f1_x = -3 + s * (3 + ANCHOR_DIST)
f1_y = 1.0 * np.ones_like(s) # Offset Y
f1_z = 1.0 - s * 1.0
filament1 = np.column_stack((f1_x, f1_y, f1_z))

f2_x = 3 - s * (3 + ANCHOR_DIST)
f2_y = -1.0 * np.ones_like(s) # Negative Offset Y
f2_z = -1.0 + s * 1.0
filament2 = np.column_stack((f2_x, f2_y, f2_z))

filaments = [filament1, filament2]
gammas = [CIRCULATION, CIRCULATION]

# NEW: Velocity State (Momentum)
# Initialize with slight inward velocity
velocities = [np.zeros_like(filament1), np.zeros_like(filament2)] 

history = []
lk_history = []

# --- 5. Simulation Loop ---
print("Engaging Gravity Drive...")

for step in range(STEPS):
    history.append([f.copy() for f in filaments])
    
    # Check Topology
    if step % 2 == 0: # Check every other frame to save time
        lk = calculate_linking_number(filaments[0], filaments[1])
        lk_history.append(lk)
    else:
        lk_history.append(lk_history[-1])

    new_filaments = []
    new_velocities = []
    
    for f_idx, fil in enumerate(filaments):
        vel = velocities[f_idx]
        
        # A. Calculate Acceleration (Gravity)
        # Vector pointing to center
        r_vec = -fil 
        r_mag = np.linalg.norm(r_vec, axis=1) + 0.1 # avoid div/0
        
        # Gravity = G * M / r^2 (Stronger as they get closer)
        # We mask the tail so only the "snake" part falls in
        gravity_accel = r_vec * (GRAVITY_STRENGTH / (r_mag**2))[:, np.newaxis]
        
        # Damp the tail acceleration to zero to keep it pinned
        # Apply full gravity to head (index 0), zero to tail (index -1)
        tail_damping = np.linspace(1, 0, NUM_NODES)**2
        gravity_accel *= tail_damping[:, np.newaxis]

        # B. Update Velocity (v = v + a*t)
        vel += gravity_accel * DT
        
        # C. Calculate Interaction Velocity (The Twist)
        # This is not an acceleration, but the flow of the medium itself
        v_twist = get_biot_savart_velocity(fil, filaments, gammas)
        
        # Total movement vector
        total_vel = vel + v_twist
        
        # D. Update Position
        new_fil = fil + total_vel * DT
        
        # HARD CONSTRAINT: Pin the tails
        new_fil[-5:] = fil[-5:] 
        vel[-5:] = 0 # Kill momentum at the anchor
        
        new_filaments.append(new_fil)
        new_velocities.append(vel)
        
    filaments = new_filaments
    velocities = new_velocities

# --- 6. Visualization ---
print("Rendering Chaos...")
fig = plt.figure(figsize=(12, 6))

ax = fig.add_subplot(1, 2, 1, projection='3d')
ax2 = fig.add_subplot(1, 2, 2)
ax2.set_title("Linking Number (Topological Charge)")
ax2.set_ylim(-3, 3) 
ax2.grid(True)
line_lk, = ax2.plot([], [], 'r-', lw=1.5)

def update(frame):
    ax.clear()
    f1 = history[frame][0]
    f2 = history[frame][1]
    
    # Visualizing speed with head color
    head_color = 'yellow' if frame < 50 else 'orange'
    if frame > 100: head_color = 'red'

    ax.plot(f1[:,0], f1[:,1], f1[:,2], color='blue', alpha=0.5)
    ax.scatter(f1[0,0], f1[0,1], f1[0,2], color=head_color, s=80, marker='o') # Heavy Head
    
    ax.plot(f2[:,0], f2[:,1], f2[:,2], color='green', alpha=0.5)
    ax.scatter(f2[0,0], f2[0,1], f2[0,2], color=head_color, s=80, marker='o') # Heavy Head
    
    # Zoom based on where the action is (tracking the heads)
    center_focus = (f1[0] + f2[0]) / 2
    r_zoom = 4.0
    ax.set_xlim(center_focus[0]-r_zoom, center_focus[0]+r_zoom)
    ax.set_ylim(center_focus[1]-r_zoom, center_focus[1]+r_zoom)
    ax.set_zlim(center_focus[2]-r_zoom, center_focus[2]+r_zoom)
    
    ax.set_title(f"Frame {frame} | Gravity Assist Mode")
    
    # Update Graph
    line_lk.set_data(range(frame), lk_history[:frame])
    ax2.set_xlim(0, STEPS)
    
    return line_lk,

ani = animation.FuncAnimation(fig, update, frames=len(history), interval=20)
plt.show()