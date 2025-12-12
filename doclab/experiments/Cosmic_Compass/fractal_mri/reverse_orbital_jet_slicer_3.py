import numpy as np
import matplotlib.pyplot as plt
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

def henon_heiles_grad(m, l):
    """Gradient of the Hénon–Heiles potential."""
    dV_dm = m + 2*m*l
    dV_dl = l + (m**2 - l**2)
    return dV_dm, dV_dl

class JetElasticityBiopsy:
    def __init__(self, resolution=600, dt=0.05, max_steps=400, kick=1e-5):
        """
        Merges the 'Triple Jet' viewports with the 'Reality/Shadow' physics.
        
        Args:
            kick (float): The epsilon distance between Reality and Shadow.
        """
        self.res = resolution
        self.dt = dt
        self.max_steps = max_steps
        self.kick = kick

        # The 3 Exhaust Ports (Saddles)
        self.saddles = [
            (0.0, 1.0),                           # Top
            (np.sqrt(3)/2.0, -0.5),               # Bottom-Right
            (-np.sqrt(3)/2.0, -0.5)               # Bottom-Left
        ]
        
        # Viewport size (match the Slicer's zoom level)
        self.m_halfspan = 0.5
        self.l_halfspan = 0.5

    def _measure_local_tension(self, m0, l0):
        """
        Vectorized calculation of divergence (Lyapunov proxy) 
        for a grid centered at (m0, l0).
        """
        # 1. Setup Grid
        m_range = np.linspace(m0 - self.m_halfspan, m0 + self.m_halfspan, self.res)
        l_range = np.linspace(l0 - self.l_halfspan, l0 + self.l_halfspan, self.res)
        M, L = np.meshgrid(m_range, l_range)

        # 2. Initialize Reality (Particle A)
        ma = M.copy()
        la = L.copy()
        pma, pla = np.zeros_like(ma), np.zeros_like(la)

        # 3. Initialize Shadow (Particle B) - The "Kick"
        mb = ma + self.kick
        lb = la + self.kick
        pmb, plb = np.zeros_like(mb), np.zeros_like(lb)

        # Trackers
        max_divergence = np.zeros_like(M)
        active = np.ones_like(M, dtype=bool)

        logger.info(f"...simulating {self.res}x{self.res} particles...")

        for step in range(self.max_steps):
            if not np.any(active):
                break

            # --- LEAPFROG INTEGRATION (Synchronized) ---
            
            # 1. First half-kick (Momentum)
            dVa_dm, dVa_dl = henon_heiles_grad(ma, la)
            dVb_dm, dVb_dl = henon_heiles_grad(mb, lb)
            
            pma[active] -= 0.5 * self.dt * dVa_dm[active]
            pla[active] -= 0.5 * self.dt * dVa_dl[active]
            pmb[active] -= 0.5 * self.dt * dVb_dm[active]
            plb[active] -= 0.5 * self.dt * dVb_dl[active]

            # 2. Drift (Position)
            ma[active] += self.dt * pma[active]
            la[active] += self.dt * pla[active]
            mb[active] += self.dt * pmb[active]
            lb[active] += self.dt * plb[active]

            # 3. Second half-kick (Momentum)
            dVa_dm, dVa_dl = henon_heiles_grad(ma, la)
            dVb_dm, dVb_dl = henon_heiles_grad(mb, lb)
            
            pma[active] -= 0.5 * self.dt * dVa_dm[active]
            pla[active] -= 0.5 * self.dt * dVa_dl[active]
            pmb[active] -= 0.5 * self.dt * dVb_dm[active]
            plb[active] -= 0.5 * self.dt * dVb_dl[active]

            # --- MEASURE TENSION ---
            # Euclidean distance between Reality and Shadow
            dist_sq = (ma - mb)**2 + (la - lb)**2
            current_dist = np.sqrt(dist_sq)
            
            # Update max recorded separation for active particles
            # We use numpy maximum to keep the highest value seen so far
            max_divergence[active] = np.maximum(max_divergence[active], current_dist[active])

            # Optimization: If divergence is huge, we can stop tracking specific pixels
            # (They are already chaotic/escaped)
            escaped_or_diverged = (dist_sq > 4.0) & active
            active[escaped_or_diverged] = False

        return m_range, l_range, max_divergence

    def render(self, filename="triple_jet_tension.png"):
        fig, axes = plt.subplots(1, 3, figsize=(18, 6), facecolor="#000510")
        
        labels = ["Top Port", "Bottom-Right Port", "Bottom-Left Port"]

        for ax, (m0, l0), label in zip(axes, self.saddles, labels):
            logger.info(f"[*] Scanning Tension at {label} ({m0:.3f}, {l0:.3f})")
            
            m_range, l_range, div = self._measure_local_tension(m0, l0)

            # Log scale for visualization (Matches the 'Shadow' aesthetic)
            # Add epsilon to avoid log(0) if they stayed perfectly sync (unlikely)
            plot_data = np.log(div + self.kick)

            # Use 'magma' or 'inferno' to represent heat/stress
            im = ax.imshow(
                plot_data, 
                origin="lower", 
                cmap="magma",
                extent=[m_range[0], m_range[-1], l_range[0], l_range[-1]],
                interpolation='bilinear'
            )

            ax.set_title(f"{label}\n(Lyapunov Instability)", color="#ffcc00")
            ax.set_xlabel("M (lateral)", color="#aaaaaa")
            ax.set_ylabel("L (axial)", color="#aaaaaa")
            ax.tick_params(colors="#aaaaaa")

            # Mark the exact saddle point
            ax.plot([m0], [l0], "wo", markersize=3, alpha=0.6)

        plt.suptitle(f"Manifold Elasticity: The Three Jets (Kick={self.kick})", color="white", fontsize=16)
        plt.tight_layout()
        plt.savefig(filename, dpi=150, facecolor="#000510")
        logger.info(f"[+] Tension biopsy saved to: {filename}")
        plt.show()

if __name__ == "__main__":
    # A slightly lower Max Step is needed for tension maps compared to escape maps
    # because the divergence happens exponentially fast.
    scanner = JetElasticityBiopsy(resolution=600, max_steps=300)
    scanner.render()