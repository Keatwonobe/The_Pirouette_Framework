import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class PirouetteHamiltonian:
    """
    PHYSICS ENGINE: The 'Real' Simulator
    ====================================
    Models the Pirouette as a dynamical system with a Hamiltonian:
    H = Kinetic_Energy + Potential_Energy
    
    Potential V(m, l) is defined by the 'Wound Channel' geometry:
    - A resonant valley (the channel)
    - Non-linear coupling terms (the 'winding')
    """
    
    def __init__(self):
        # Physical constants for the "Wound Channel"
        self.coupling = 0.5  # Strength of interaction between m^2 and lambda
        self.mass_m = 1.0    # Effective mass of m-field
        self.mass_l = 1.0    # Effective mass of lambda-field
        
    def potential(self, m, l):
        """
        The 'Stiffness' Landscape V(m, l).
        We model this as a coupled non-linear oscillator (Hénon-Heiles type),
        which is famous for producing chaotic/fractal behavior.
        """
        # 1. Harmonic Well (The Base Resonance)
        # Keeps the system bound near the origin (vacuum)
        V_harmonic = 0.5 * (m**2 + l**2)
        
        # 2. The "Wound" (Non-linear perturbation)
        # This term creates the triangular symmetry of the channel
        # and induces chaos at higher energies.
        V_wound = self.coupling * (m**2 * l - (l**3) / 3.0)
        
        # Total Potential (Inverted for stiffness: High Stiffness = Low Potential)
        return V_harmonic + V_wound

    def gradient(self, m, l):
        """Force field: -Gradient of Potential"""
        # dV/dm = m + 2*coupling*m*l
        dV_dm = m + 2 * self.coupling * m * l
        
        # dV/dl = l + coupling*(m^2 - l^2)
        dV_dl = l + self.coupling * (m**2 - l**2)
        
        return np.array([dV_dm, dV_dl])

class SymplecticIntegrator:
    """
    TIME EVOLUTION: Preserves the 'Soul' of the system.
    Uses Leapfrog integration to conserve energy, ensuring that
    any chaos we see is real physics, not numerical error.
    """
    
    def __init__(self, physics_engine, dt=0.01):
        self.engine = physics_engine
        self.dt = dt
        
    def step(self, state):
        """
        Evolves state [m, l, p_m, p_l] forward by dt.
        """
        m, l, pm, pl = state
        
        # 1. Kick (Update Momenta half-step)
        grad = self.engine.gradient(m, l)
        pm_half = pm - 0.5 * self.dt * grad[0]
        pl_half = pl - 0.5 * self.dt * grad[1]
        
        # 2. Drift (Update Positions full-step)
        m_new = m + self.dt * pm_half / self.engine.mass_m
        l_new = l + self.dt * pl_half / self.engine.mass_l
        
        # 3. Kick (Update Momenta second half-step)
        grad_new = self.engine.gradient(m_new, l_new)
        pm_new = pm_half - 0.5 * self.dt * grad_new[0]
        pl_new = pl_half - 0.5 * self.dt * grad_new[1]
        
        return np.array([m_new, l_new, pm_new, pl_new])

class FractalRealityScanner:
    
    def __init__(self):
        self.physics = PirouetteHamiltonian()
        self.integrator = SymplecticIntegrator(self.physics, dt=0.05)
        
    def find_attractor(self):
        """Phase 1: Relaxation Scan (Find the bottom of the well)"""
        logger.info("\nPHASE 1: RELAXATION SCAN")
        logger.info("Dropping probe to find the vacuum state...")
        
        # Minimize the potential
        res = minimize(
            lambda x: self.physics.potential(x[0], x[1]),
            [0.1, 0.1], # Start slightly off-center
            method='Nelder-Mead'
        )
        
        center = res.x
        depth = res.fun
        logger.info(f"Vacuum found at: m={center[0]:.4f}, l={center[1]:.4f}")
        logger.info(f"Potential Depth: {depth:.4f}")
        return center

    def measure_chaos(self, start_state, steps=2000):
        """Phase 2: Lyapunov Exponent (The Butterfly Effect)"""
        logger.info("\nPHASE 2: LYAPUNOV ANALYSIS")
        logger.info("Measuring sensitivity to initial conditions...")
        
        # Trajectory A (Reference)
        state_A = start_state.copy()
        
        # Trajectory B (Shadow) - Perturbed by 1 nanometer
        state_B = start_state.copy()
        state_B[0] += 1e-9 
        
        divergence = []
        
        for t in range(steps):
            state_A = self.integrator.step(state_A)
            state_B = self.integrator.step(state_B)
            
            # Distance in Phase Space (4D Euclidean)
            dist = np.linalg.norm(state_A - state_B)
            
            # Avoid log(0)
            if dist < 1e-15: dist = 1e-15
            divergence.append(np.log(dist))
            
        # Analyze Divergence
        # If slope > 0: Chaos. If slope ~ 0: Criticality.
        time = np.arange(len(divergence))
        slope, intercept = np.polyfit(time[200:], divergence[200:], 1) # Skip transient
        
        logger.info(f"Lyapunov Exponent (λ): {slope:.6f}")
        if abs(slope) < 0.0005:
            logger.info(">> CRITICALITY CONFIRMED (λ ≈ 0)")
        elif slope > 0:
            logger.info(">> CHAOS DETECTED (λ > 0)")
        else:
            logger.info(">> STABILITY DETECTED (λ < 0)")
            
        # Plot
        plt.figure(figsize=(10, 5))
        plt.plot(divergence, 'b-', alpha=0.6, label='Log Separation')
        plt.plot(time, slope*time + intercept, 'r--', label=f'Fit λ={slope:.5f}')
        plt.title(f"Butterfly Effect Analysis (λ={slope:.5f})")
        plt.xlabel("Time Step")
        plt.ylabel("ln(|δ|)")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.savefig('fractal_lyapunov.png')
        
        return slope

    def image_fractal(self, start_state, steps=10000):
        """Phase 3: Poincaré Section (Seeing the Geometry)"""
        logger.info("\nPHASE 3: POINCARÉ FRACTAL IMAGING")
        logger.info("Slicing the 4D torus to reveal internal geometry...")
        
        state = start_state.copy()
        
        # We record points (m, p_m) every time the lambda-field crosses 0
        # This is the "Slice"
        
        points_m = []
        points_pm = []
        
        prev_l = state[1]
        
        for t in range(steps):
            next_state = self.integrator.step(state)
            curr_l = next_state[1]
            
            # Check for crossing of l=0 plane
            if prev_l < 0 and curr_l >= 0:
                # Interpolate to find exact crossing point
                fraction = (0 - prev_l) / (curr_l - prev_l)
                
                cross_m = state[0] + fraction * (next_state[0] - state[0])
                cross_pm = state[2] + fraction * (next_state[2] - state[2])
                
                points_m.append(cross_m)
                points_pm.append(cross_pm)
            
            state = next_state
            prev_l = curr_l
            
            if t % 1000 == 0:
                print(f"  > Step {t}/{steps}...")
                
        logger.info(f"Captured {len(points_m)} intersections.")
        
        # Plot
        plt.figure(figsize=(8, 8))
        plt.scatter(points_m, points_pm, s=1.0, c='black', alpha=0.6)
        plt.title("Poincaré Section: The Fractal 'Brain'")
        plt.xlabel("m field")
        plt.ylabel("m momentum")
        plt.grid(True, alpha=0.2)
        plt.savefig('fractal_geometry.png')

if __name__ == "__main__":
    scanner = FractalRealityScanner()
    
    # 1. Find the Vacuum
    vacuum = scanner.find_attractor()
    
    # 2. Inject Energy to orbit the vacuum
    # We give it a "kick" to start the Pirouette spinning
    # [m, l, p_m, p_l]
    # We start slightly displaced from vacuum with some momentum
    # This energy level determines if we are in the chaotic regime
    probe_state = np.array([vacuum[0], vacuum[1] + 0.1, 0.05, 0.05])
    
    # 3. Run Analysis
    scanner.measure_chaos(probe_state)
    scanner.image_fractal(probe_state, steps=20000)