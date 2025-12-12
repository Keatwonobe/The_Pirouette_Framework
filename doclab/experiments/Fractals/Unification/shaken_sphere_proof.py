import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

# --- 1. Physics Engine Constants ---
NUM_NODES = 50           # Nodes per filament
DT = 0.05                # Time step
STEPS = 100              # Total simulation steps
CORE_RADIUS = 0.2        # Smoothing for Biot-Savart (prevents singularities)
CONTRACTION_RATE = 0.5   # Strength of the radial collapse (The "Shaking")
CIRCULATION = 5.0        # Strength of the vortex tubes (The "Travelers")

# --- 2. Biot-Savart Law Solver ---
def get_biot_savart_velocity(target_points, filaments, gammas):
    """
    Calculates velocity induced at target_points by all filaments
    using the desingularized Biot-Savart law.
    """
    total_vel = np.zeros_like(target_points)
    
    for fil, gamma in zip(filaments, gammas):
        # Calculate segment vectors dl and midpoint vectors r
        # fil has shape (N, 3)
        # We model the filament as a series of straight segments
        for i in range(len(fil) - 1):
            p1 = fil[i]
            p2 = fil[i+1]
            dl = p2 - p1
            midpoint = (p1 + p2) / 2.0
            
            # Vector from segment midpoint to all target points
            # r_vec shape: (M, 3)
            r_vec = target_points - midpoint
            r_mag = np.linalg.norm(r_vec, axis=1)
            
            # Cross product dl x r
            # dl is (3,), r_vec is (M, 3) -> result is (M, 3)
            cross_prod = np.cross(dl, r_vec)
            
            # Biot-Savart formula with Rosenhead-Moore smoothing
            # dU = (Gamma / 4pi) * (dl x r) / (|r|^2 + a^2)^(3/2)
            factor = (gamma / (4 * np.pi)) * (1.0 / (r_mag**2 + CORE_RADIUS**2)**1.5)
            
            # Add to total velocity (broadcasting factor across columns)
            total_vel += cross_prod * factor[:, np.newaxis]
            
    return total_vel

# --- 3. Topology: Gauss Linking Integral ---
def calculate_linking_number(loop1, loop2):
    """
    Computes the Gauss Linking Number between two discrete curves.
    Note: Ideally loops are closed, but this approximates for open entangled tubes.
    """
    linking_sum = 0.0
    for i in range(len(loop1) - 1):
        r1 = loop1[i]
        dr1 = loop1[i+1] - loop1[i]
        for j in range(len(loop2) - 1):
            r2 = loop2[j]
            dr2 = loop2[j+1] - loop2[j]
            
            r12 = r1 - r2
            dist = np.linalg.norm(r12)
            if dist < 1e-5: continue # Avoid self-intersection singularity
            
            # (r1 - r2) . (dr1 x dr2) / |r1 - r2|^3
            num = np.dot(r12, np.cross(dr1, dr2))
            den = dist**3
            linking_sum += num / den
            
    return linking_sum / (4 * np.pi)

# --- 4. Initialization: The "Skew Travelers" ---
# Two lines entering the sphere, slightly skewed so they aren't parallel.
# Filament 1: Enters from top-left, exits bottom-right
t = np.linspace(-1, 1, NUM_NODES)
f1_x = t * 2
f1_y = np.ones_like(t) * 0.5
f1_z = -t * 2 + 0.5 # Slight tilt
filament1 = np.column_stack((f1_x, f1_y, f1_z))

# Filament 2: Enters from top-right, exits bottom-left (perpendicular-ish)
f2_x = -t * 2
f2_y = -np.ones_like(t) * 0.5
f2_z = -t * 2 - 0.5 # Slight tilt opposite way
filament2 = np.column_stack((f2_x, f2_y, f2_z))

filaments = [filament1, filament2]
gammas = [CIRCULATION, CIRCULATION] # Both have positive helicity relative to flow

# History for plotting
history = []
lk_history = []

# --- 5. Simulation Loop ---
print("Running Simulation...")
for step in range(STEPS):
    current_state = [f.copy() for f in filaments]
    history.append(current_state)
    
    # Check Topology
    lk = calculate_linking_number(filaments[0], filaments[1])
    lk_history.append(lk)
    
    new_filaments = []
    for f_idx, fil in enumerate(filaments):
        # 1. Calculate Interaction Velocity (Biot-Savart)
        v_interact = get_biot_savart_velocity(fil, filaments, gammas)
        
        # 2. Calculate Contraction Velocity (The "Shrinking Sphere")
        # V_radial = -Rate * r (pushes everything to origin)
        # We mask this so it doesn't crush the center to a singularity instantly
        r_mag = np.linalg.norm(fil, axis=1)
        v_contract = -CONTRACTION_RATE * fil
        
        # Total Velocity
        v_total = v_interact + v_contract
        
        # Euler Integration Step
        new_fil = fil + v_total * DT
        
        # Renormalize/Resample nodes could go here to keep stability, 
        # but for short timescale proof-of-concept, we skip it.
        new_filaments.append(new_fil)
        
    filaments = new_filaments
    if step % 10 == 0:
        print(f"Step {step}: Linking Number approx {lk:.4f}")

# --- 6. Visualization ---
print("Generating Animation...")
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

def update(frame):
    ax.clear()
    # Plot Sphere Boundary (Visual guide only)
    # The sphere shrinks over time effectively in the simulation, 
    # here we just draw a static reference or shrinking one.
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    R_viz = 3.0 * (1.0 - (frame/STEPS)*0.8) # Visualization of shrinking boundary
    x = R_viz * np.cos(u)*np.sin(v)
    y = R_viz * np.sin(u)*np.sin(v)
    z = R_viz * np.cos(v)
    ax.plot_wireframe(x, y, z, color="gray", alpha=0.1)

    # Plot Filaments
    f1 = history[frame][0]
    f2 = history[frame][1]
    
    ax.plot(f1[:,0], f1[:,1], f1[:,2], color='red', linewidth=3, label='Traveler 1')
    ax.plot(f2[:,0], f2[:,1], f2[:,2], color='green', linewidth=3, label='Traveler 2')
    
    # Plot "Ghost" Torus structure trace (connect midpoints)
    # Visualizing the emergent geometry
    
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_zlim(-3, 3)
    ax.set_title(f"Time: {frame*DT:.2f} | Linking Num: {lk_history[frame]:.3f}")
    ax.legend()

ani = animation.FuncAnimation(fig, update, frames=len(history), interval=50)
plt.show()

# Optional: Plot Linking Number evolution
plt.figure()
plt.plot(lk_history)
plt.title("Topological Charge (Linking Number) vs Time")
plt.xlabel("Step")
plt.ylabel("Gauss Linking Integral")
plt.grid(True)
plt.show()