import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

# --- 1. Physics Engine Constants ---
NUM_NODES = 80           # More nodes for smoother "scraping"
DT = 0.01                # Smaller time step for stability
STEPS = 200              # Longer simulation
CORE_RADIUS = 0.1        # The "thickness" of the travelers
CONTRACTION_STRENGTH = 4.0 # Much faster head speed
CIRCULATION = 8.0        # Stronger interaction (Twist)
ANCHOR_DIST = 10.0       # The "Infinite" distance

# --- 2. Biot-Savart Law (The Twist) ---
def get_biot_savart_velocity(target_points, filaments, gammas):
    total_vel = np.zeros_like(target_points)
    for fil, gamma in zip(filaments, gammas):
        for i in range(len(fil) - 1):
            p1, p2 = fil[i], fil[i+1]
            dl = p2 - p1
            midpoint = (p1 + p2) / 2.0
            r_vec = target_points - midpoint
            r_mag = np.linalg.norm(r_vec, axis=1)
            
            # Singularities create the "noise" in your previous graph.
            # We add a safety check here.
            cross_prod = np.cross(dl, r_vec)
            denominator = (r_mag**2 + CORE_RADIUS**2)**1.5
            factor = (gamma / (4 * np.pi)) / denominator
            total_vel += cross_prod * factor[:, np.newaxis]
    return total_vel

# --- 3. Topology: Gauss Linking Integral (Damped) ---
def calculate_linking_number(loop1, loop2):
    linking_sum = 0.0
    for i in range(len(loop1) - 1):
        r1, dr1 = loop1[i], loop1[i+1] - loop1[i]
        for j in range(len(loop2) - 1):
            r2, dr2 = loop2[j], loop2[j+1] - loop2[j]
            r12 = r1 - r2
            dist = np.linalg.norm(r12)
            
            # Damping to prevent division by zero during the "scrape"
            if dist < 0.05: continue 
            
            num = np.dot(r12, np.cross(dr1, dr2))
            den = dist**3
            linking_sum += num / den
            
    return linking_sum / (4 * np.pi)

# --- 4. Initialization: Long Tapered Tails ---
# We create filaments that stretch from near-center out to "infinity"
s = np.linspace(0, 1, NUM_NODES) 
# s=0 is the Head (center), s=1 is the Tail (infinity)

# Traveler 1: Top-Left to Center
f1_x = -2 + s * (2 + ANCHOR_DIST)  # Starts at -2, goes to +Anchor
f1_y = 0.5 * np.ones_like(s)       # Offset Y
f1_z = 0.5 - s * 0.5               # Slight slope

# Traveler 2: Top-Right to Center (Skewed)
f2_x = 2 - s * (2 + ANCHOR_DIST)   # Starts at 2, goes to -Anchor
f2_y = -0.5 * np.ones_like(s)      # Offset Y (opposite)
f2_z = -0.5 + s * 0.5              # Slight slope

# Pack them up. Note: We reverse the arrays so index 0 is the HEAD (center)
filament1 = np.column_stack((f1_x, f1_y, f1_z))
filament2 = np.column_stack((f2_x, f2_y, f2_z))

filaments = [filament1, filament2]
gammas = [CIRCULATION, CIRCULATION] 

history = []
lk_history = []

# --- 5. Simulation Loop ---
print("Simulating the Scrape...")

for step in range(STEPS):
    history.append([f.copy() for f in filaments])
    
    # Calculate Topology
    lk = calculate_linking_number(filaments[0], filaments[1])
    lk_history.append(lk)
    
    new_filaments = []
    for f_idx, fil in enumerate(filaments):
        # 1. Interaction (Twist)
        v_twist = get_biot_savart_velocity(fil, filaments, gammas)
        
        # 2. Contraction (The "Fast Head")
        # We apply contraction based on distance from center.
        # Closer to center = Faster contraction (Zooming in)
        # Far from center = Pinned (Infinite tail)
        
        r_mag = np.linalg.norm(fil, axis=1)
        
        # Velocity profile: fast at small r, zero at large r
        # This keeps the tail anchored at "infinity"
        contraction_factor = np.exp(-r_mag / 4.0) 
        v_contract = -fil * contraction_factor[:, np.newaxis] * CONTRACTION_STRENGTH
        
        v_total = v_twist + v_contract
        
        # Update Position
        new_fil = fil + v_total * DT
        
        # HARD CONSTRAINT: Pin the last few nodes to simulate infinity
        # This prevents the tail from flopping around and ruining the linking number
        new_fil[-5:] = fil[-5:] 
        
        new_filaments.append(new_fil)
        
    filaments = new_filaments

# --- 6. Visualization ---
print("Rendering...")
fig = plt.figure(figsize=(12, 6))

# Plot 1: 3D View
ax = fig.add_subplot(1, 2, 1, projection='3d')
ax.set_title("The Dichotomy Scrape")

# Plot 2: Linking Number
ax2 = fig.add_subplot(1, 2, 2)
ax2.set_title("Topological Charge Stabilization")
ax2.set_ylim(-2, 2) # We expect it to stabilize around 1 or -1
ax2.grid(True)
line_lk, = ax2.plot([], [], 'b-')

def update(frame):
    ax.clear()
    f1 = history[frame][0]
    f2 = history[frame][1]
    
    # Draw the travelers
    # We use a scatter for the HEAD to show the speed
    ax.plot(f1[:,0], f1[:,1], f1[:,2], color='crimson', alpha=0.6, label='Traveler 1')
    ax.scatter(f1[0,0], f1[0,1], f1[0,2], color='red', s=50) # The "Head"
    
    ax.plot(f2[:,0], f2[:,1], f2[:,2], color='teal', alpha=0.6, label='Traveler 2')
    ax.scatter(f2[0,0], f2[0,1], f2[0,2], color='cyan', s=50) # The "Head"
    
    # Focus the camera on the "Scrape" point (Center)
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_zlim(-2, 2)
    ax.legend()
    
    # Update Graph
    line_lk.set_data(range(frame), lk_history[:frame])
    ax2.set_xlim(0, STEPS)
    
    return line_lk,

ani = animation.FuncAnimation(fig, update, frames=len(history), interval=30)
plt.show()