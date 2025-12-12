import numpy as np
import matplotlib.pyplot as plt

# --- Configuration ---
STEPS = 1200
DT = 0.01
RADIUS = 20.0
G_PHASE = 8.0
STRESS_COEFF = 3.0
CHANNEL_WINDUP = 0.8   # New Term: Channel pulls rotation
CRITICAL_SPIN = 12.0   # Threshold for "Friction Spikes"
SPIKE_INTENSITY = 5.0
SPEED_HIGH = 15.0

# --- Physics Engine ---
def compute_physics_with_channel(pos1, pos2, vel1, vel2, w1, w2):
    # 1. Spatial Dynamics (Same as before)
    r_vec = pos2 - pos1
    r = np.linalg.norm(r_vec)
    r_safe = max(r, 0.1)
    
    twist_sum = w1 + w2 
    resonance = np.exp(-(twist_sum**2) / 0.1)
    
    speed1 = np.linalg.norm(vel1)
    speed2 = np.linalg.norm(vel2)
    avg_speed = (speed1 + speed2) / 2.0
    
    stress_factor = 1.0 + STRESS_COEFF * (avg_speed**2)
    f_mag = (G_PHASE * resonance * stress_factor) / (r_safe**2)
    force_vec = (r_vec / r_safe) * f_mag
    
    # 2. NEW: Channel Wind-Up (Rotational Acceleration)
    # The channel "pulls" them, spinning them faster than they want to go.
    # d_omega / dt is proportional to linear speed (moving through the medium winds you up)
    # We add this to the EXISTING spin direction
    dw1 = CHANNEL_WINDUP * speed1 * np.sign(w1) * DT
    dw2 = CHANNEL_WINDUP * speed2 * np.sign(w2) * DT
    
    w1_new = w1 + dw1
    w2_new = w2 + dw2
    
    # 3. NEW: Interference Friction Spikes
    # If spin exceeds critical limit, the medium fights back -> Energy Spike
    spike1 = max(0, abs(w1_new) - CRITICAL_SPIN) * SPIKE_INTENSITY
    spike2 = max(0, abs(w2_new) - CRITICAL_SPIN) * SPIKE_INTENSITY
    total_spike = spike1 + spike2
    
    # Friction Drag (Energy loss due to spikes)
    drag_factor = 1.0 - (total_spike * 0.01) # Small drag per spike
    
    return force_vec, f_mag, w1_new, w2_new, total_spike, drag_factor

# --- Simulation ---
theta = np.pi / 4
p1 = np.array([-RADIUS * np.cos(theta), -RADIUS * np.sin(theta), 0.0])
v1 = np.array([SPEED_HIGH, SPEED_HIGH * 0.2, 0.0]) 
w1 = 5.0 # Start below critical

p2 = np.array([RADIUS * np.cos(theta), RADIUS * np.sin(theta), 0.0])
v2 = np.array([-SPEED_HIGH, -SPEED_HIGH * 0.2, 0.0])
w2 = -5.0

history_p1 = []
history_p2 = []
history_w = []
history_spikes = []

for _ in range(STEPS):
    history_p1.append(p1.copy())
    history_p2.append(p2.copy())
    
    force, bond, w1, w2, spike, drag = compute_physics_with_channel(p1, p2, v1, v2, w1, w2)
    
    history_w.append(abs(w1)) # Track spin magnitude
    history_spikes.append(spike)
    
    # Update Kinematics
    v1 += force * DT
    v2 -= force * DT
    
    # Apply Drag from Interference Spikes
    v1 *= drag
    v2 *= drag
    
    p1 += v1 * DT
    p2 += v2 * DT
    
    if np.linalg.norm(p1 - p2) < 0.5: break

# --- Visualization ---
fig = plt.figure(figsize=(14, 10))

# 1. Trajectory with Spikes
ax1 = fig.add_subplot(2, 2, 1)
hp1 = np.array(history_p1)
hp2 = np.array(history_p2)
# Plot background path
ax1.plot(hp1[:,0], hp1[:,1], 'k-', alpha=0.3)
ax1.plot(hp2[:,0], hp2[:,1], 'k-', alpha=0.3)

# Scatter plot "Spike Events"
spikes = np.array(history_spikes)
spike_mask = spikes > 0.1
ax1.scatter(hp1[spike_mask, 0], hp1[spike_mask, 1], c=spikes[spike_mask], cmap='hot', s=20, label='Interference Spikes')
ax1.scatter(hp2[spike_mask, 0], hp2[spike_mask, 1], c=spikes[spike_mask], cmap='hot', s=20)

ax1.set_title("Trajectory with Friction Interference Spikes")
ax1.legend()
ax1.grid(True)

# 2. Spin Up Process
ax2 = fig.add_subplot(2, 2, 2)
ax2.plot(history_w, 'b-', label='Rotational Velocity (w)')
ax2.axhline(CRITICAL_SPIN, color='r', linestyle='--', label='Critical Threshold')
ax2.set_title("Channel Wind-Up: Velocity -> Rotation")
ax2.set_ylabel("Angular Velocity")
ax2.legend()
ax2.grid(True)

# 3. Energy Release (Spikes)
ax3 = fig.add_subplot(2, 1, 2)
ax3.plot(history_spikes, 'r-', linewidth=1)
ax3.set_title("Interference Pattern Energy Release (Friction Spikes)")
ax3.set_xlabel("Time Step")
ax3.set_ylabel("Interference Magnitude")
ax3.fill_between(range(len(history_spikes)), history_spikes, color='red', alpha=0.3)
ax3.grid(True)

plt.tight_layout()
plt.savefig('channel_windup_interference.png')