import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.gridspec import GridSpec

# ======================
# SIMULATION CONFIGURATION
# ======================
RES = 600
FRAMES = 300       # Longer simulation to capture the full spiral
FPS = 30
DT = 0.05          # Time step

# PHYSICS PARAMETERS
G_CONST = 2.0      # Strength of mutual gravity
K_SUBSTRATE = 1.0  # Strength of the Hénon-Heiles potential
FRICTION = 0.005   # "Wound Channel" drag (energy loss)

print("=" * 60)
print("P H Y S I C S   S I M U L A T O R   -   C R I T I C A L   C A P T U R E")
print("=" * 60)

# ======================
# 1. THE SUBSTRATE (Potential Map)
# ======================
def generate_potential_map(res):
    print(f"[*] Calculating Potential Landscape ({res}x{res})...")
    m = np.linspace(-2.2, 2.2, res)
    l = np.linspace(-2.2, 2.2, res)
    M, L = np.meshgrid(m, l)
    
    # Hénon-Heiles Potential Energy Surface
    # V(x, y) = 1/2(x^2 + y^2) + (x^2y - y^3/3)
    V = 0.5 * (M**2 + L**2) + (M**2 * L - L**3/3.0)
    
    # We clip it for visual clarity (The "Triangle" is V < 1/6)
    V_vis = np.clip(V, 0, 0.5)
    
    print("[✓] Landscape generated.")
    return V_vis, M, L

# ======================
# 2. THE PHYSICS ENGINE (RK4 Integrator)
# ======================
class SystemState:
    def __init__(self):
        # Initial Conditions: "Travelers" entering from bottom corners
        # Pos: x1, y1, x2, y2
        self.pos = np.array([-1.5, -1.8,  1.5, -1.8]) 
        
        # Vel: vx1, vy1, vx2, vy2
        # They aim for the center, but with a slight upward bias
        self.vel = np.array([ 0.8,  0.9, -0.8,  0.9]) 
        
        self.history = []
        self.energy = []

    def get_forces(self, p, v):
        x1, y1, x2, y2 = p
        vx1, vy1, vx2, vy2 = v
        
        # 1. SUBSTRATE FORCES (Gradient of Hénon-Heiles)
        # Fx = -dV/dx = -(x + 2xy)
        # Fy = -dV/dy = -(y + x^2 - y^2)
        
        fx1_env = -K_SUBSTRATE * (x1 + 2*x1*y1)
        fy1_env = -K_SUBSTRATE * (y1 + x1**2 - y1**2)
        
        fx2_env = -K_SUBSTRATE * (x2 + 2*x2*y2)
        fy2_env = -K_SUBSTRATE * (y2 + x2**2 - y2**2)
        
        # 2. MUTUAL GRAVITY (Interaction)
        # Vector r12 = p2 - p1
        dx = x2 - x1
        dy = y2 - y1
        dist_sq = dx**2 + dy**2 + 0.01 # Softening to prevent infinity
        dist = np.sqrt(dist_sq)
        
        f_grav_mag = G_CONST / dist_sq
        fx_grav = f_grav_mag * (dx / dist)
        fy_grav = f_grav_mag * (dy / dist)
        
        # 3. FRICTION (Energy Loss)
        fx1_drag = -FRICTION * vx1
        fy1_drag = -FRICTION * vy1
        fx2_drag = -FRICTION * vx2
        fy2_drag = -FRICTION * vy2
        
        # Sum Forces
        ax1 = fx1_env + fx_grav + fx1_drag
        ay1 = fy1_env + fy_grav + fy1_drag
        
        ax2 = fx2_env - fx_grav + fx2_drag # Newton's 3rd law (Equal/Opposite)
        ay2 = fy2_env - fy_grav + fy2_drag
        
        return np.array([ax1, ay1, ax2, ay2])

    def step(self, dt):
        # RK4 Integration
        k1_v = self.get_forces(self.pos, self.vel)
        k1_p = self.vel
        
        k2_v = self.get_forces(self.pos + k1_p * dt*0.5, self.vel + k1_v * dt*0.5)
        k2_p = self.vel + k1_v * dt*0.5
        
        k3_v = self.get_forces(self.pos + k2_p * dt*0.5, self.vel + k2_v * dt*0.5)
        k3_p = self.vel + k2_v * dt*0.5
        
        k4_v = self.get_forces(self.pos + k3_p * dt, self.vel + k3_v * dt)
        k4_p = self.vel + k3_v * dt
        
        self.vel += (dt/6.0) * (k1_v + 2*k2_v + 2*k3_v + k4_v)
        self.pos += (dt/6.0) * (k1_p + 2*k2_p + 2*k3_p + k4_p)
        
        self.history.append(self.pos.copy())
        
        # Calc Energy (Kinetic + Potential) for HUD
        ke = 0.5 * np.sum(self.vel**2)
        # Just use dist for simplistic potential metric
        pe = -G_CONST / np.sqrt((self.pos[2]-self.pos[0])**2 + (self.pos[3]-self.pos[1])**2 + 0.01)
        self.energy.append(ke + pe)

# ======================
# 3. VISUALIZATION
# ======================
def run_simulation():
    # Setup
    V_map, M, L = generate_potential_map(RES)
    sim = SystemState()
    
    # Pre-simulate for speed (we render the history)
    print(f"[*] Computing Physics ({FRAMES} steps)...")
    for _ in range(FRAMES):
        sim.step(DT)
    history = np.array(sim.history)
    print("[✓] Physics Complete.")
    
    # Setup Plot
    fig = plt.figure(figsize=(10, 10), facecolor='#050505')
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    
    # Text
    hud = ax.text(0.5, 0.95, "INITIALIZING...", color='lime', fontfamily='monospace', ha='center', fontsize=12)
    
    def update(frame):
        ax.clear()
        ax.axis('off')
        
        # 1. Draw Substrate (The Potential)
        # We define the "Wada" shape by contouring the Potential
        ax.contourf(M, L, V_map, levels=20, cmap='magma', alpha=0.3)
        ax.contour(M, L, V_map, levels=[1.0/6.0], colors='white', linewidths=1, linestyles='--', alpha=0.3)
        
        # 2. Draw Trails (History)
        # T1 (Cyan)
        current_idx = frame
        if current_idx > 0:
            ax.plot(history[:current_idx, 0], history[:current_idx, 1], color='cyan', lw=2, alpha=0.8)
            ax.plot(history[:current_idx, 2], history[:current_idx, 3], color='magenta', lw=2, alpha=0.8)
            
            # 3. Draw Heads
            head = history[current_idx-1]
            ax.scatter(head[0], head[1], color='cyan', s=100, edgecolors='white', zorder=10)
            ax.scatter(head[2], head[3], color='magenta', s=100, edgecolors='white', zorder=10)
            
            # 4. Interaction Line
            ax.plot([head[0], head[2]], [head[1], head[3]], color='white', linestyle=':', alpha=0.5)
            
            # HUD Logic
            # Detect "Phases" based on the simulation data
            separation = np.sqrt((head[2]-head[0])**2 + (head[3]-head[1])**2)
            
            if frame < 50:
                phase = "GRAVITATIONAL APPROACH"
                color = 'white'
            elif separation > 1.5:
                phase = "SCATTERING / TURN"
                color = 'yellow'
            elif separation < 0.5:
                phase = "CRITICAL CAPTURE (WADA RESONANCE)"
                color = 'red'
            else:
                phase = "ORBITAL DECAY"
                color = 'orange'
                
            hud_text = f"PHASE: {phase}\nSEPARATION: {separation:.3f}\nENERGY: {sim.energy[current_idx-1]:.3f}"
            ax.text(0.5, 0.9, hud_text, color=color, fontfamily='monospace', ha='center', transform=ax.transAxes)

        ax.set_xlim(-2.2, 2.2)
        ax.set_ylim(-2.2, 2.2)
        
    anim = FuncAnimation(fig, update, frames=FRAMES, interval=30)
    anim.save('simulation_capture.gif', writer=PillowWriter(fps=FPS))
    print("[✓] Simulation Rendered.")

if __name__ == "__main__":
    run_simulation()