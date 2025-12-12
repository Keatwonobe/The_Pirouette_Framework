import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class PirouetteHamiltonian:
    """
    PHYSICS ENGINE (Unchanged)
    Hénon-Heiles type potential for the Wound Channel.
    """
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
    """
    TIME EVOLUTION (Unchanged)
    """
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

class SurfaceTensionScanner:
    
    def __init__(self):
        self.physics = PirouetteHamiltonian()
        self.integrator = SymplecticIntegrator(self.physics, dt=0.05)
        
    def find_vacuum(self):
        res = minimize(lambda x: self.physics.potential(x[0], x[1]), [0.1, 0.1], method='Nelder-Mead')
        return res.x

    def scan_energies(self, vacuum, steps_per_scan=8000):
        logger.info(f"\n{'='*60}")
        logger.info("SURFACE TENSION SCAN (Fractal Breakdown)")
        logger.info(f"{'='*60}")
        
        # We progressively kick the system harder away from the vacuum
        # This increases the Total Hamiltonian Energy (H)
        kicks = [0.1, 0.35, 0.55, 0.65] 
        
        # Setup Plot Grid
        fig, axes = plt.subplots(2, 2, figsize=(12, 12))
        axes = axes.flatten()
        
        for i, kick in enumerate(kicks):
            logger.info(f"\n>> RUN {i+1}: Kick Strength = {kick:.2f}")
            
            # 1. Setup Initial State (Displaced from vacuum)
            # We kick 'l' (lambda) to drive it up the potential wall
            state = np.array([vacuum[0], vacuum[1] + kick, 0.0, 0.0])
            
            # Calculate Total Energy
            V = self.physics.potential(state[0], state[1])
            K = 0.5 * (state[2]**2 + state[3]**2)
            E_total = V + K
            logger.info(f"   System Energy: {E_total:.4f}")
            
            # 2. Poincaré Slice Run
            points_m = []
            points_pm = []
            prev_l = state[1]
            
            # Fast loop
            for t in range(steps_per_scan):
                next_state = self.integrator.step(state)
                curr_l = next_state[1]
                
                # Crossing Condition: l crosses 0 going up
                if prev_l < 0 and curr_l >= 0:
                    fraction = (0 - prev_l) / (curr_l - prev_l + 1e-9)
                    cross_m = state[0] + fraction * (next_state[0] - state[0])
                    cross_pm = state[2] + fraction * (next_state[2] - state[2])
                    points_m.append(cross_m)
                    points_pm.append(cross_pm)
                
                state = next_state
                prev_l = curr_l
            
            # 3. Plotting
            ax = axes[i]
            if len(points_m) > 0:
                ax.scatter(points_m, points_pm, s=0.5, c='black', alpha=0.7)
            
            ax.set_title(f"Energy E = {E_total:.3f} (Kick {kick})")
            ax.set_xlabel("m field")
            ax.set_ylabel("momentum p_m")
            ax.grid(True, alpha=0.2)
            
            # Interpretation Label
            if i == 0: ax.text(0.05, 0.95, "STABLE TORUS", transform=ax.transAxes, color='green', fontweight='bold')
            elif i == 3: ax.text(0.05, 0.95, "FRACTAL CHAOS", transform=ax.transAxes, color='red', fontweight='bold')

        plt.suptitle("The Breakdown of Reality: Poincaré Sections at Rising Energy", fontsize=16)
        plt.tight_layout()
        plt.savefig('surface_tension_breakdown.png')
        logger.info("\n[Saved composite scan to 'surface_tension_breakdown.png']")

if __name__ == "__main__":
    scanner = SurfaceTensionScanner()
    vac = scanner.find_vacuum()
    scanner.scan_energies(vac)