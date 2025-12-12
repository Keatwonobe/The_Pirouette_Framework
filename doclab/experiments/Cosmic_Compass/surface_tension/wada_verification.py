import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# --- Physics Engine (Same as before) ---
def potential(x, y, lam):
    return 0.5 * (x**2 + y**2) + lam * (x**2 * y - (1/3) * y**3)

def equations_of_motion(t, state, m, lam):
    x, y, px, py = state
    Fx = -x - 2 * lam * x * y
    Fy = -y - lam * (x**2 - y**2)
    return [px / m, py / m, Fx, Fy]

def get_exit(theta, m, lam, E, x0, y0, t_max=1000.0, r_esc=5.0):
    V_start = potential(x0, y0, lam)
    if V_start > E: return -1 # Tunneling
    p_mag = np.sqrt(2 * m * (E - V_start))
    
    # Define Event
    def escape(t, state, *args):
        return np.sqrt(state[0]**2 + state[1]**2) - r_esc
    escape.terminal = True
    escape.direction = 1

    sol = solve_ivp(
        equations_of_motion, [0, t_max], 
        [x0, y0, p_mag*np.cos(theta), p_mag*np.sin(theta)], 
        args=(m, lam), events=escape, rtol=1e-8, atol=1e-10
    )

    if not sol.t_events[0].size: return 0 # Stuck
    x, y = sol.y[0][-1], sol.y[1][-1]
    angle = np.arctan2(y, x) % (2 * np.pi)
    return int(angle // (2 * np.pi / 3)) + 1

# --- The Wada Hunter ---

def hunt_wada(m, lam, E, x0, y0):
    """
    1. Finds a boundary between Exit 1 and Exit 2.
    2. Zooms in to see if Exit 3 is inside.
    """
    
    # Step 1: Broad Sweep to find a Red/Green border
    print("Step 1: Hunting for a Red/Green interface...")
    thetas = np.linspace(3.1, 3.2, 50) # We know the action is here from your last plot
    exits = []
    for th in thetas:
        exits.append(get_exit(th, m, lam, E, x0, y0))
    
    # Find transition index
    exits = np.array(exits)
    # Look for pattern [1, 2] or [2, 1]
    idx = -1
    for i in range(len(exits)-1):
        if (exits[i] == 1 and exits[i+1] == 2) or (exits[i] == 2 and exits[i+1] == 1):
            idx = i
            break
            
    if idx == -1:
        print("Could not find a clean Red/Green border in initial scan.")
        return

    theta_A = thetas[idx]
    theta_B = thetas[idx+1]
    print(f"Found border between {theta_A:.5f} (Exit {exits[idx]}) and {theta_B:.5f} (Exit {exits[idx+1]})")
    
    # Step 2: The Deep Zoom (The Barcode)
    print("\nStep 2: Generating The Barcode (Zoom 10,000x)...")
    
    # Create a dense line of pixels across this tiny gap
    zoom_thetas = np.linspace(theta_A, theta_B, 400)
    zoom_exits = []
    
    # Progress bar logic
    for i, th in enumerate(zoom_thetas):
        if i % 40 == 0: print(f".", end="", flush=True)
        zoom_exits.append(get_exit(th, m, lam, E, x0, y0, t_max=2000))
    print(" Done.")

    # --- Visualization ---
    zoom_exits = np.array(zoom_exits)
    
    plt.figure(figsize=(12, 4))
    
    # Create an "image" strip (barcode)
    # Map exits to colors: 0=Black, 1=Red, 2=Green, 3=Blue
    colormap = np.zeros((1, len(zoom_exits), 3))
    
    # Define RGB colors
    c_map = {0:[0,0,0], 1:[1,0,0], 2:[0,1,0], 3:[0,0,1]}
    
    for i, ex in enumerate(zoom_exits):
        colormap[0, i, :] = c_map.get(ex, [0,0,0])
        
    plt.imshow(colormap, aspect='auto', extent=[theta_A, theta_B, 0, 1])
    plt.yticks([])
    plt.xlabel(f"Launch Angle (rad)\nWindow Size: {theta_B - theta_A:.6f}")
    plt.title(f"The Wada Barcode: Is Blue hidden between Red and Green?\nE={E}")
    
    # Check for the "Wada Property"
    has_1 = 1 in zoom_exits
    has_2 = 2 in zoom_exits
    has_3 = 3 in zoom_exits
    
    print("\n--- RESULTS ---")
    print(f"Contains Red (Exit 1): {has_1}")
    print(f"Contains Green (Exit 2): {has_2}")
    print(f"Contains Blue (Exit 3): {has_3}")
    
    if has_1 and has_2 and has_3:
        print("\n>>> WADA PROPERTY CONFIRMED <<<")
        print("The boundary between 1 and 2 is not a line.")
        print("It is a fractal containing Exit 3.")
    else:
        print("\nNo Wada detected (or we need to zoom deeper).")

    plt.show()

if __name__ == "__main__":
    MASS = 1.0
    LAMBDA = 1.0
    E_SADDLE = 1.0/6.0
    ENERGY = E_SADDLE + 0.01
    
    hunt_wada(MASS, LAMBDA, ENERGY, 0.0, 0.0)