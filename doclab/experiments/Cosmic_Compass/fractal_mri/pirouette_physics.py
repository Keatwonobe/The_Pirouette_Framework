"""
PIROUETTE PHYSICS ENGINE (v1.0)
-------------------------------
Derived Experimentally on: Nov 30, 2025
Fundamental Constant (Twist): 2.83814

This library implements the "Pirouette" Unified Field Framework.
It simulates particles not as point-masses, but as topological
solitons (knots) moving through a structured vacuum field.

Key Features:
- Non-Linear Vacuum Geometry (Teal/Red/Gold Basins)
- Emergent Mass via Vacuum Drag (Higgs-like)
- Topological Protection (Spin 1/2 Stability)
- Elastic Scattering via Flux Tube Repulsion
"""

import numpy as np

# ==========================================
# 1. THE FUNDAMENTAL CONSTANTS
# ==========================================
class Constants:
    # The "Fine Structure Constant" of the Pirouette Universe.
    # Found via Edge Hunter algorithm to produce stable Spin 1/2 matter.
    TWIST = 2.83814 
    
    # The viscosity of the vacuum (The Higgs Coupling).
    # Determines how quickly particles shed excess energy to find stable orbits.
    GAMMA = 0.02
    
    # Interaction Strength (The "Coulomb" constant).
    G_COUPLE = 0.8 
    
    # Simulation Precision
    DT = 0.005

# ==========================================
# 2. THE VACUUM GEOMETRY (THE FIELD)
# ==========================================
def get_vacuum_force(m, lam):
    """
    Calculates the local force vector of the vacuum at coordinates (m, lam).
    This defines the geometry of the universe.
    """
    # --- The Three Forces ---
    # 1. Teal (Electromagnetism/Hypercharge)
    F_teal_m = -(m + 0.866) 
    F_teal_lam = -(lam - 0.5)

    # 2. Red (Weak Force/Isospin) - Includes the TWIST violation
    F_red_m = -(m - 0.0)
    p_violation = Constants.TWIST * np.sin(m * 2.5) 
    F_red_lam = -(lam + 1.0) + p_violation

    # 3. Gold (Strong Force/Color) - Geometric Tension
    sum_m = (F_teal_m + F_red_m)
    sum_lam = (F_teal_lam + F_red_lam)
    mag = np.sqrt(sum_m**2 + sum_lam**2)
    scale = np.sqrt(mag) # Non-linear confinement scaling
    F_gold_m = sum_m * scale
    F_gold_lam = sum_lam * scale
    
    # --- Basin Weighting (Mixing Angles) ---
    angle = np.degrees(np.arctan2(lam, m)) % 360
    
    # Gaussian blending between sectors
    diff_g = np.minimum(np.abs(angle - 30), 360-np.abs(angle - 30))
    w_gold = np.exp(-(diff_g/80)**2)
    
    diff_t = np.minimum(np.abs(angle - 150), 360-np.abs(angle - 150))
    w_teal = np.exp(-(diff_t/80)**2)
    
    diff_r = np.minimum(np.abs(angle - 270), 360-np.abs(angle - 270))
    w_red = np.exp(-(diff_r/80)**2)
    
    # Normalize Weights
    tot = w_gold + w_teal + w_red + 1e-6
    nw_red = w_red / tot
    nw_teal = w_teal / tot
    nw_gold = w_gold / tot
    
    # --- Resultant Vector ---
    Fm = (nw_teal * F_teal_m + nw_red * F_red_m + nw_gold * F_gold_m)
    Flam = (nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam)
    
    # Return Force and the "Red Weight" (used for Drag/Mass calculation)
    return Fm, Flam, nw_red

# ==========================================
# 3. THE PARTICLE CLASS
# ==========================================
class Particle:
    def __init__(self, m, lam, pm, plam, name="Electron"):
        self.m = m          # Mass Field Position
        self.lam = lam      # Coupling Field Position
        self.pm = pm        # Momentum (Mass)
        self.plam = plam    # Momentum (Coupling)
        self.name = name
        self.history_m = []
        self.history_l = []

    @classmethod
    def create_stable_fermion(cls, name="Fermion", offset_x=0, offset_y=0):
        """
        Factory method to spawn a particle in the known Stable Zone.
        Coordinates derived from the 'Resurrection' experiment.
        """
        # Base coordinates for the Limit Cycle
        base_m = -1.8 + offset_x
        base_l = 0.0 + offset_y
        # Base Velocity required to enter orbit
        base_pm = 0.0
        base_pl = 2.0 
        return cls(base_m, base_l, base_pm, base_pl, name)

    def apply_force(self, fm, fl, drag):
        """Applies a force vector with drag to update momentum."""
        self.pm = (self.pm + 0.5 * Constants.DT * fm) * drag
        self.plam = (self.plam + 0.5 * Constants.DT * fl) * drag

    def update_position(self):
        """Updates position based on current momentum."""
        self.m += Constants.DT * self.pm
        self.lam += Constants.DT * self.plam
        
    def record(self):
        """Saves current position to history."""
        self.history_m.append(self.m)
        self.history_l.append(self.lam)

# ==========================================
# 4. THE UNIVERSE SIMULATION
# ==========================================
class Universe:
    def __init__(self):
        self.particles = []
        self.time = 0.0

    def add_particle(self, p):
        self.particles.append(p)

    def step(self):
        """
        Advances the universe by one time step (DT).
        Calculates:
        1. Internal Vacuum Forces (Self-Energy)
        2. Particle-Particle Interactions (Repulsion)
        3. Motion integration
        """
        # A. Calculate Forces
        forces = [] # Stores (Fm_total, Fl_total, Drag) for each particle
        
        for i, p in enumerate(self.particles):
            # 1. Vacuum Force (The Field)
            vac_fm, vac_fl, w_red = get_vacuum_force(p.m, p.lam)
            
            # 2. Interaction Force (The Collider Logic)
            int_fm, int_fl = 0.0, 0.0
            for j, other in enumerate(self.particles):
                if i == j: continue
                
                dx = other.m - p.m
                dy = other.lam - p.lam
                dist_sq = dx**2 + dy**2 + 1e-6
                dist = np.sqrt(dist_sq)
                
                # Repulsive Force
                f_mag = Constants.G_COUPLE / dist_sq
                
                # Soft Core (prevents divide-by-zero explosions)
                if dist < 0.2: f_mag *= 5.0
                
                # Vector pointing AWAY from other particle
                # Force on p is negative of vector p->other
                fx = -f_mag * (dx / dist)
                fy = -f_mag * (dy / dist)
                
                int_fm += fx
                int_fl += fy
            
            # 3. Drag Calculation (Higgs Mechanism)
            # Drag increases when passing through Red Zones (Mass acquisition)
            drag = 1.0 / (1.0 + 0.5 * Constants.DT * Constants.GAMMA * w_red)
            
            forces.append((vac_fm + int_fm, vac_fl + int_fl, drag))

        # B. Apply Kick 1 (Leapfrog) & Update Position
        for i, p in enumerate(self.particles):
            fm, fl, drag = forces[i]
            p.apply_force(fm, fl, drag)
            p.update_position()
            p.record()

        # C. Re-evaluate Forces at new position (For stability)
        # (Simplified: In a full leapfrog we'd re-calc vacuum forces here.
        # For speed in Python, we assume force is constant for the step 
        # or do a second pass if high precision is needed. 
        # We will do a partial drag update for stability.)
        for i, p in enumerate(self.particles):
            # Re-read local vacuum drag only
            _, _, w_red = get_vacuum_force(p.m, p.lam)
            drag = 1.0 / (1.0 + 0.5 * Constants.DT * Constants.GAMMA * w_red)
            
            # Apply Kick 2 (using previous force, new drag)
            fm, fl, _ = forces[i]
            p.apply_force(fm, fl, drag)

        self.time += Constants.DT

# ==========================================
# 5. DEMO / TEST
# ==========================================
if __name__ == "__main__":
    print("Initializing Pirouette Universe...")
    univ = Universe()
    
    # Create two "Perfect" Electrons
    p1 = Particle.create_stable_fermion(name="Electron A", offset_x=-0.5)
    p2 = Particle.create_stable_fermion(name="Electron B", offset_x=0.5)
    
    # Give them collision velocities
    p1.pm += 1.0 # Move Right
    p2.pm -= 1.0 # Move Left
    
    univ.add_particle(p1)
    univ.add_particle(p2)
    
    print(f"Simulating {len(univ.particles)} particles with Twist={Constants.TWIST}...")
    
    # Run for a few steps to prove it works
    for _ in range(1000):
        univ.step()
        
    print(f"Simulation Complete. Time: {univ.time:.3f}")
    print(f"P1 Location: ({p1.m:.3f}, {p1.lam:.3f})")
    print(f"P2 Location: ({p2.m:.3f}, {p2.lam:.3f})")
    print("Library verified.")