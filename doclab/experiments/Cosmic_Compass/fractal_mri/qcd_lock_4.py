import numpy as np
import matplotlib.pyplot as plt

def run_oscillation_of_necessity():
    # Simulation Parameters
    steps = 1000
    dt = 0.05
    t = np.linspace(0, steps*dt, steps)
    
    # --- 1. The Twist (Red / Weak Force) ---
    # A driving oscillation with Parity Violation (Asymmetry)
    # It pushes +1.2 but only pulls -0.8 (Chiral bias)
    frequency = 1.5
    parity_bias = 0.3
    twist = np.sin(frequency * t) + parity_bias
    
    # --- 2. The Reaction (Yellow / Strong Force) ---
    # Modeled as the vacuum response.
    # We solve for position x(t) dynamically.
    
    x = 0.0
    v = 0.0
    
    # Arrays to store history
    tension_history = []
    twist_history = []
    delta_history = []  # This is the EM field (Net Force / Motion)
    position_history = []
    
    # Vacuum parameters
    mass = 1.0       # Inertia of the field
    stiffness = 2.0  # Coupling constant for Strong Force
    damping = 0.1    # Slight energy loss (radiation)
    
    print("Simulating the Struggle between Twist and Tension...")
    
    for i in range(steps):
        # Current Drive (The Twist)
        F_twist = twist[i]
        
        # Current Reaction (The Tension)
        # CONFINEMENT LOGIC:
        # Near 0, force is small (Asymptotic Freedom).
        # As x grows, force grows cubically (Confinement).
        F_tension = -stiffness * (x**3) 
        
        # The Delta (Teal / Electromagnetism)
        # This is the "Force Gap" that creates motion
        F_net = F_twist + F_tension - (damping * v)
        
        # Integrate (Newton's Second Law)
        a = F_net / mass
        v += a * dt
        x += v * dt
        
        # Store Data
        # We store -F_tension to plot it as "Opposing" the twist visually
        twist_history.append(F_twist)
        tension_history.append(-F_tension) 
        delta_history.append(v) # Velocity represents the magnetic/electric wave propagation
        position_history.append(x)

    # --- Visualization ---
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True, facecolor='black')
    
    # Plot 1: The Struggle (Stress vs Twist)
    ax1.set_facecolor('black')
    ax1.plot(t, twist_history, color='#ff4444', linewidth=2, label='The Twist (Weak Force / Asymmetry)')
    ax1.plot(t, tension_history, color='#ffd700', linewidth=2, linestyle='--', label='The Tension (Strong Force / Confinement)')
    
    # Fill the "Delta" area
    ax1.fill_between(t, twist_history, tension_history, color='#00cccc', alpha=0.3, label='The Delta (EM Potential)')
    
    ax1.set_title("The Geometry of Necessity: Stress vs Twist", color='white', fontsize=14)
    ax1.legend(loc='upper right', facecolor='black', edgecolor='white', labelcolor='white')
    ax1.grid(False)
    ax1.tick_params(colors='white')
    
    # Plot 2: The Emergence (Electromagnetism)
    # Does the chaotic struggle produce a clean wave?
    ax2.set_facecolor('black')
    ax2.plot(t, delta_history, color='#00ffff', linewidth=2.5, label='Resulting Motion (Electromagnetism)')
    
    # Add a perfect sine wave for comparison to show "regularity from chaos"
    perfect_wave = np.sin(frequency * t) * np.max(np.abs(delta_history))
    ax2.plot(t, perfect_wave, color='white', alpha=0.2, linestyle=':', label='Ideal Wave (Reference)')

    ax2.set_title("Emergent Phenomenon: The EM Wave", color='white', fontsize=14)
    ax2.set_xlabel("Time", color='white')
    ax2.legend(loc='upper right', facecolor='black', edgecolor='white', labelcolor='white')
    ax2.grid(False)
    ax2.tick_params(colors='white')
    
    # Remove spines
    for ax in [ax1, ax2]:
        for spine in ax.spines.values():
            spine.set_edgecolor('#444444')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_oscillation_of_necessity()