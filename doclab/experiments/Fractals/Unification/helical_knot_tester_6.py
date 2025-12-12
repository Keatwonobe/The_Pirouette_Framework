import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger("GENESIS_REACTOR")

class GenesisReactor:
    def __init__(self):
        self.dt = 0.001       # High precision time
        self.steps = 100000    # Deep time simulation
        
        # --- COSMIC PARAMETERS ---
        self.G = 150.0        # The Strength of the "Travelers" attraction
        self.manifold_drag = 0.05 # The resistance of space (creates the spiral)
        self.twist_factor = 2.5   # The "Holonomy" winding rate
        
    def run_genesis(self):
        logger.info("[-] INITIATING COSMIC IMPACT SEQUENCE...")
        
        # --- INITIAL CONDITIONS: THE ENTRY ---
        # "They enter at the smushed part of the ellipse... path of least resistance."
        # We start them far out, on the Y-axis (the cusp of a cardioid-like shape)
        # separated slightly to induce the couple.
        
        # Traveler 1 (Positive/Red)
        r_start = 18.0
        angle_offset = 0.2 # Slight offset from vertical to start the spin
        
        t1_pos = np.array([r_start * np.sin(angle_offset), r_start * np.cos(angle_offset)])
        t1_vel = np.array([0.0, -2.5]) # Plunging INWARD fast
        
        # Traveler 2 (Negative/Blue) - Mirror entry
        t2_pos = np.array([-r_start * np.sin(angle_offset), r_start * np.cos(angle_offset)])
        t2_vel = np.array([0.0, -2.5]) # Plunging INWARD fast
        
        # History
        traj1 = []
        traj2 = []
        energy_hist = []
        
        t = 0
        impact_triggered = False
        
        for i in range(self.steps):
            # 1. RECORD
            if i % 10 == 0:
                traj1.append(t1_pos.copy())
                traj2.append(t2_pos.copy())
            
            # 2. VECTOR MATH
            # Vector between travelers
            r_vec = t2_pos - t1_pos
            r_dist = np.linalg.norm(r_vec)
            
            # Safety for the singularity (The "Black Hole Triad")
            if r_dist < 0.05:
                # They have crossed. The simulation technically "breaks" here into the next fractal layer.
                # We soften it to let them wind the core.
                r_dist = 0.05 
                if not impact_triggered:
                    logger.info("    [!] EVENT HORIZON BREACHED. INITIATING FRACTAL DESCENT.")
                    impact_triggered = True
            
            # 3. GRAVITY / ATTRACTION
            # F = G * m1 * m2 / r^2
            force_mag = self.G / (r_dist**2)
            force_vec = (r_vec / r_dist) * force_mag
            
            # 4. MANIFOLD PRESSURE (The "Cardioid Channel")
            # This is the "groove" that forces them to spiral instead of collide head-on.
            # It acts perpendicular to velocity (Holonomic Constraint).
            # We add a "Twist" force that scales with 1/r (stronger near core).
            
            # Torque 1
            v1_mag = np.linalg.norm(t1_vel)
            twist_1 = np.array([-t1_vel[1], t1_vel[0]]) # Perpendicular
            if v1_mag > 0: twist_1 /= v1_mag
            
            # Torque 2
            v2_mag = np.linalg.norm(t2_vel)
            twist_2 = np.array([-t2_vel[1], t2_vel[0]])
            if v2_mag > 0: twist_2 /= v2_mag
            
            # The "Scream" Factor: Twist increases as they get closer
            twist_force = self.twist_factor / (r_dist * 0.5)
            
            # 5. INTEGRATION
            # Apply Forces
            # T1 is pulled to T2, plus Twist
            acc1 = force_vec + (twist_1 * twist_force) - (t1_vel * self.manifold_drag)
            
            # T2 is pulled to T1, plus Twist (Opposite winding? No, same chirality for the universe)
            # Actually, to make them "lock", they usually counter-rotate or co-rotate?
            # User said "angles spiral naturally towards one another".
            # Let's apply symmetric twist.
            acc2 = -force_vec + (twist_2 * twist_force) - (t2_vel * self.manifold_drag)
            
            # Update Velocity
            t1_vel += acc1 * self.dt
            t2_vel += acc2 * self.dt
            
            # Update Position
            t1_pos += t1_vel * self.dt
            t2_pos += t2_vel * self.dt
            
            # Calculate "Song" Energy (Kinetic + interaction)
            total_ke = 0.5 * (np.linalg.norm(t1_vel)**2 + np.linalg.norm(t2_vel)**2)
            energy_hist.append(total_ke)
            
            t += self.dt
            
        return np.array(traj1), np.array(traj2), np.array(energy_hist)

    def render(self):
        t1, t2, energy = self.run_genesis()
        
        logger.info("[-] Visualizing The Event...")
        
        fig, ax = plt.subplots(figsize=(12, 12), facecolor='#000000')
        
        # 1. PLOT THE TRAVELERS (The Descent)
        # Gradient: Fade in from darkness -> Bright White at Impact -> Cool down?
        # No, "It's sobering." It ends in a hum.
        # Let's map Color to Velocity/Energy.
        
        # Normalize Energy for coloring
        e_norm = energy[::10] # Downsample to match trajectory
        e_norm = (e_norm - e_norm.min()) / (e_norm.max() - e_norm.min())
        
        # Traveler 1 (The Red Giant / Matter?)
        points1 = t1.reshape(-1, 1, 2)
        segments1 = np.concatenate([points1[:-1], points1[1:]], axis=1)
        cmap1 = LinearSegmentedColormap.from_list("t1", ["#440000", "#ff0000", "#ffaa00", "#ffffff"])
        lc1 = LineCollection(segments1, cmap=cmap1, norm=plt.Normalize(0, 1))
        lc1.set_array(e_norm) # Color by energy spike
        lc1.set_linewidth(1.5)
        lc1.set_alpha(0.9)
        ax.add_collection(lc1)
        
        # Traveler 2 (The Blue Giant / Antimatter?)
        points2 = t2.reshape(-1, 1, 2)
        segments2 = np.concatenate([points2[:-1], points2[1:]], axis=1)
        cmap2 = LinearSegmentedColormap.from_list("t2", ["#000044", "#0000ff", "#00aaff", "#ffffff"])
        lc2 = LineCollection(segments2, cmap=cmap2, norm=plt.Normalize(0, 1))
        lc2.set_array(e_norm)
        lc2.set_linewidth(1.5)
        lc2.set_alpha(0.9)
        ax.add_collection(lc2)
        
        # 2. THE CORE (The "Writhing Heart")
        # Zoom in on the center where the density is highest
        # We can simulate the "Glow" of the recursive creation
        circle = plt.Circle((0, 0), 0.5, color='white', alpha=0.1)
        ax.add_artist(circle)
        circle2 = plt.Circle((0, 0), 0.2, color='white', alpha=0.3)
        ax.add_artist(circle2)
        
        # 3. ANNOTATIONS
        ax.set_xlim(-10, 10)
        ax.set_ylim(-5, 15) # Shifted to show the entry from "Top"
        ax.set_aspect('equal')
        ax.axis('off')
        
        title_text = "THE GENESIS IMPACT: FRACTAL DESCENT\n" 
        title_text += "Entry -> Compression -> Convergence (The Scream) -> Recursive Core"
        ax.set_title(title_text, color='white', fontsize=14, alpha=0.8)
        
        # Text annotation for the stages
        ax.text(0, 14, "ENTRY (The Cusp)", color='gray', ha='center', fontsize=10)
        ax.text(6, 6, "COMPRESSION\n(Manifold Pressure)", color='gray', ha='center', fontsize=8)
        ax.text(0, -2, "THE RECURSIVE CORE\n(Infinite Descent)", color='white', ha='center', fontsize=10)
        
        plt.tight_layout()
        plt.savefig("genesis_impact_event.png", dpi=150)
        logger.info("[+] Cosmology Rendered: 'genesis_impact_event.png'")
        plt.show()

if __name__ == "__main__":
    reactor = GenesisReactor()
    reactor.render()