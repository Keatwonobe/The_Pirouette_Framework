import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter
from numba import njit, prange

# ==========================================
# 1. THE ORACLE (Destiny Lookup)
# ==========================================
# We use this ONLY to color the particles based on where they WILL go.
# This allows us to see the "Ribbons" inside the chaos before they separate.

@njit(fastmath=True)
def get_basin_single(m, l, t_max=60.0, dt=0.05, escape_r2=16.0):
    pm, pl = 0.0, 0.0
    steps = int(t_max / dt)
    sigma = 1.0
    for _ in range(steps):
        fm = -(m + 2*sigma*m*l); fl = -(l + sigma*(m**2 - l**2))
        pm += 0.5 * dt * fm; pl += 0.5 * dt * fl
        m += dt * pm; l += dt * pl
        fm = -(m + 2*sigma*m*l); fl = -(l + sigma*(m**2 - l**2))
        pm += 0.5 * dt * fm; pl += 0.5 * dt * fl
        if m*m + l*l > escape_r2:
            angle = np.arctan2(l, m)
            if angle > 0.5 and angle < 2.6: return 1
            elif angle <= -2.6 or angle >= 2.6: return 2
            else: return 3
    return 0 # Trapped

@njit(parallel=True, fastmath=True)
def assign_destinies(m_vals, l_vals):
    n = len(m_vals)
    destinies = np.zeros(n, dtype=np.int8)
    for i in prange(n):
        destinies[i] = get_basin_single(m_vals[i], l_vals[i])
    return destinies

# ==========================================
# 2. THE PHYSICS ENGINE (Batch Integrator)
# ==========================================

@njit(parallel=True, fastmath=True)
def step_physics_batch(m, l, pm, pl, dt=0.02, steps=1):
    n = len(m)
    sigma = 1.0
    for i in prange(n):
        for _ in range(steps):
            # Symplectic Velocity Verlet
            fm = -(m[i] + 2*sigma*m[i]*l[i])
            fl = -(l[i] + sigma*(m[i]**2 - l[i]**2))
            
            pm[i] += 0.5 * dt * fm
            pl[i] += 0.5 * dt * fl
            
            m[i] += dt * pm[i]
            l[i] += dt * pl[i]
            
            fm_new = -(m[i] + 2*sigma*m[i]*l[i])
            fl_new = -(l[i] + sigma*(m[i]**2 - l[i]**2))
            
            pm[i] += 0.5 * dt * fm_new
            pl[i] += 0.5 * dt * fl_new
            
    return m, l, pm, pl

# ==========================================
# 3. THE DIRECTOR (Animation Setup)
# ==========================================

class ManifoldCinema:
    def __init__(self, n_particles=20000):
        # Initialize particles in a tiny Gaussian cloud at the center
        # This represents "Information" entering the chaotic scattering region
        self.n = n_particles
        self.m = np.random.normal(0, 0.1, self.n)
        self.l = np.random.normal(0, 0.1, self.n)
        self.pm = np.random.normal(0, 0.1, self.n)
        self.pl = np.random.normal(0, 0.1, self.n)
        
        # Determine their fate immediately (The "Ribbon" Color)
        print("[-] Consulting the Oracle for particle destinies...")
        self.destiny = assign_destinies(self.m, self.l)
        
        # Color Map:
        # 1 (Teal): #00ffff
        # 2 (Purple): #ff00ff
        # 3 (Gold): #ffaa00
        # 0 (Trapped/Black): #222222
        self.colors = np.zeros((self.n, 4))
        for i in range(self.n):
            d = self.destiny[i]
            if d == 1: self.colors[i] = [0, 1, 1, 0.6]      # Cyan
            elif d == 2: self.colors[i] = [1, 0, 1, 0.6]    # Magenta
            elif d == 3: self.colors[i] = [1, 0.6, 0, 0.6]  # Gold
            else: self.colors[i] = [0.2, 0.2, 0.2, 0.3]     # Trapped
            
    def update(self):
        # Run physics
        # We use small steps for smooth "Ribbon" flow
        self.m, self.l, self.pm, self.pl = step_physics_batch(
            self.m, self.l, self.pm, self.pl, dt=0.02, steps=4
        )
        return np.column_stack((self.m, self.l))

# ==========================================
# 4. ACTION!
# ==========================================

cinema = ManifoldCinema(n_particles=25000)

fig, ax = plt.subplots(figsize=(10, 10), facecolor='black')
ax.set_facecolor('black')
ax.axis('off')
ax.set_xlim(-2.0, 2.0)
ax.set_ylim(-2.0, 2.0)

# We use a Scatter plot with very small markers to simulate a "fluid"
scatter = ax.scatter(cinema.m, cinema.l, s=1, c=cinema.colors)

title_text = ax.text(0.02, 0.95, "The Loom of Chaos (Stable Manifolds)", transform=ax.transAxes, color='white', fontsize=14, fontfamily='monospace')

def animate(i):
    data = cinema.update()
    scatter.set_offsets(data)
    
    # Dynamic Zoom?
    # No, keep fixed to show them escaping
    
    if i % 10 == 0: print(f"Rendering frame {i}...")
    return scatter, title_text

print("[-] Filming the Ribbons...")
anim = animation.FuncAnimation(fig, animate, frames=180, interval=30, blit=True)
anim.save('manifold_ribbon_flow.gif', writer=PillowWriter(fps=24))
print("[+] Scene Complete. Saved to 'manifold_ribbon_flow.gif'")