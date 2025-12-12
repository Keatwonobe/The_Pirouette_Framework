import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from matplotlib.patches import ConnectionPatch

class PirouetteHamiltonian:
    def __init__(self):
        self.coupling = 0.5
        self.mass_m = 1.0
        self.mass_l = 1.0

    def potential(self, m, l):
        V_harmonic = 0.5 * (m**2 + l**2)
        V_wound = self.coupling * (m**2 * l - (l**3) / 3.0)
        return V_harmonic + V_wound

    def gradient(self, m, l):
        dV_dm = m + 2 * self.coupling * m * l
        dV_dl = l + self.coupling * (m**2 - l**2)
        return np.array([dV_dm, dV_dl])

class SymplecticIntegrator:
    def __init__(self, physics_engine, dt=0.05):
        self.engine = physics_engine
        self.dt = dt

    def step(self, state):
        m, l, pm, pl = state
        grad = self.engine.gradient(m, l)
        pm_half = pm - 0.5 * self.dt * grad[0]
        pl_half = pl - 0.5 * self.dt * grad[1]
        m_new = m + self.dt * pm_half / self.engine.mass_m
        l_new = l + self.dt * pl_half / self.engine.mass_l
        grad_new = self.engine.gradient(m_new, l_new)
        pm_new = pm_half - 0.5 * self.dt * grad_new[0]
        pl_new = pl_half - 0.5 * self.dt * grad_new[1]
        return np.array([m_new, l_new, pm_new, pl_new])

def generate_composite_fractal():
    physics = PirouetteHamiltonian()
    integrator = SymplecticIntegrator(physics, dt=0.05)

    # Find vacuum
    res = minimize(lambda x: physics.potential(x[0], x[1]), [0.1, 0.1], method='Nelder-Mead')
    vacuum = res.x

    # Setup High Energy State (Kick 0.65 - Fractal Regime)
    kick = 0.65
    state = np.array([vacuum[0], vacuum[1] + kick, 0.0, 0.0])

    points_m = []
    points_pm = []
    prev_l = state[1]

    # Run Simulation (Long run for density)
    steps = 150000 
    for t in range(steps):
        next_state = integrator.step(state)
        curr_l = next_state[1]

        if prev_l < 0 and curr_l >= 0:
            fraction = (0 - prev_l) / (curr_l - prev_l + 1e-9)
            cross_m = state[0] + fraction * (next_state[0] - state[0])
            cross_pm = state[2] + fraction * (next_state[2] - state[2])
            points_m.append(cross_m)
            points_pm.append(cross_pm)
        
        state = next_state
        prev_l = curr_l

    points_m = np.array(points_m)
    points_pm = np.array(points_pm)

    # Define Zoom Regions
    # Level 1: Macro (Full View)
    xlim_1 = (np.min(points_m), np.max(points_m))
    ylim_1 = (np.min(points_pm), np.max(points_pm))

    # Level 2: Mid Zoom (Focus on the thickest part of the arc)
    # Finding a dense region
    center_idx = len(points_m) // 2
    # We'll pick a region based on data density, let's look at the top arc
    mask_mid = (points_pm > 0.5 * np.max(points_pm))
    mid_m = points_m[mask_mid]
    mid_pm = points_pm[mask_mid]
    
    # Let's take a slice around the mean m of this upper arc
    center_m_mid = np.mean(mid_m)
    span_mid = (np.max(points_m) - np.min(points_m)) * 0.15 # 15% width
    xlim_2 = (center_m_mid - span_mid/2, center_m_mid + span_mid/2)
    # Find pm range in this slice
    mask_slice = (points_m > xlim_2[0]) & (points_m < xlim_2[1])
    slice_pm = points_pm[mask_slice]
    center_pm_mid = np.mean(slice_pm)
    span_pm_mid = (np.max(slice_pm) - np.min(slice_pm)) * 1.2 # slightly larger than data
    ylim_2 = (np.min(slice_pm), np.max(slice_pm))

    # Level 3: Micro Zoom (Focus on a filament inside Level 2)
    # We filter points for Level 2 first
    l2_m = points_m[(points_m > xlim_2[0]) & (points_m < xlim_2[1]) & (points_pm > ylim_2[0]) & (points_pm < ylim_2[1])]
    l2_pm = points_pm[(points_m > xlim_2[0]) & (points_m < xlim_2[1]) & (points_pm > ylim_2[0]) & (points_pm < ylim_2[1])]
    
    # Pick a tiny slice in the middle of L2
    center_m_micro = np.mean(l2_m)
    span_micro = (xlim_2[1] - xlim_2[0]) * 0.1 # 10% of Level 2
    xlim_3 = (center_m_micro - span_micro/2, center_m_micro + span_micro/2)
    
    # Get pm range for L3
    mask_micro = (l2_m > xlim_3[0]) & (l2_m < xlim_3[1])
    micro_pm = l2_pm[mask_micro]
    if len(micro_pm) == 0: # Fallback if empty
         xlim_3 = (l2_m[0] - span_micro/2, l2_m[0] + span_micro/2)
         ylim_3 = (l2_pm[0] - span_micro/2, l2_pm[0] + span_micro/2)
    else:
        ylim_3 = (np.min(micro_pm), np.max(micro_pm))

    # Plotting
    fig = plt.figure(figsize=(18, 6))
    
    # Axes 1: Macro
    ax1 = fig.add_subplot(131)
    ax1.scatter(points_m, points_pm, s=0.1, c='black', alpha=0.5)
    ax1.set_title("I. The Macro-State (Torus)")
    ax1.set_xlabel("m field")
    ax1.set_ylabel("momentum")
    
    # Draw box 1 on ax1
    rect1 = plt.Rectangle((xlim_2[0], ylim_2[0]), xlim_2[1]-xlim_2[0], ylim_2[1]-ylim_2[0], ec='red', fc='none', lw=1.5)
    ax1.add_patch(rect1)

    # Axes 2: Mid
    ax2 = fig.add_subplot(132)
    ax2.scatter(points_m, points_pm, s=1.0, c='darkred', alpha=0.6)
    ax2.set_xlim(xlim_2)
    ax2.set_ylim(ylim_2)
    ax2.set_title("II. The Strain Layers (Resonance)")
    ax2.set_xlabel("m field")
    
    # Draw box 2 on ax2
    rect2 = plt.Rectangle((xlim_3[0], ylim_3[0]), xlim_3[1]-xlim_3[0], ylim_3[1]-ylim_3[0], ec='blue', fc='none', lw=1.5)
    ax2.add_patch(rect2)
    
    # Connect box 1 to ax2
    con1 = ConnectionPatch(xyA=(xlim_2[1], ylim_2[1]), xyB=(xlim_2[0], ylim_2[1]), coordsA="data", coordsB="data", 
                           axesA=ax1, axesB=ax2, color="red", alpha=0.3)
    con2 = ConnectionPatch(xyA=(xlim_2[1], ylim_2[0]), xyB=(xlim_2[0], ylim_2[0]), coordsA="data", coordsB="data", 
                           axesA=ax1, axesB=ax2, color="red", alpha=0.3)
    fig.add_artist(con1)
    fig.add_artist(con2)


    # Axes 3: Micro
    ax3 = fig.add_subplot(133)
    ax3.scatter(points_m, points_pm, s=3.0, c='royalblue', alpha=0.8)
    ax3.set_xlim(xlim_3)
    ax3.set_ylim(ylim_3)
    ax3.set_title("III. The Infinite Braid (Fractal)")
    ax3.set_xlabel("m field")

    # Connect box 2 to ax3
    con3 = ConnectionPatch(xyA=(xlim_3[1], ylim_3[1]), xyB=(xlim_3[0], ylim_3[1]), coordsA="data", coordsB="data", 
                           axesA=ax2, axesB=ax3, color="blue", alpha=0.3)
    con4 = ConnectionPatch(xyA=(xlim_3[1], ylim_3[0]), xyB=(xlim_3[0], ylim_3[0]), coordsA="data", coordsB="data", 
                           axesA=ax2, axesB=ax3, color="blue", alpha=0.3)
    fig.add_artist(con3)
    fig.add_artist(con4)

    plt.suptitle("The Topology of Infinite Strain: Recursive Structure in the Pirouette Field", fontsize=16)
    plt.tight_layout()
    plt.savefig('reality_fractal_composite.png', dpi=300)

generate_composite_fractal()