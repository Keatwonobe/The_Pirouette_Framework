import numpy as np
import matplotlib.pyplot as plt
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

def henon_heiles_grad(m, l):
    """Gradient of the Hénon–Heiles potential."""
    dV_dm = m + 2*m*l
    dV_dl = l + (m**2 - l**2)
    return dV_dm, dV_dl

class TripleJetSlicer:
    def __init__(self, resolution=800, dt=0.05, max_steps=10000):
        """
        TRIPLE JET SLICER
        Biopsies all three exhaust ports (saddles) of the Hénon–Heiles manifold.
        """
        self.res = resolution
        self.dt = dt
        self.max_steps = max_steps

        # Saddle locations (m, l)
        self.saddles = [
            (0.0, 1.0),                           # top
            (np.sqrt(3)/2.0, -0.5),               # bottom-right
            (-np.sqrt(3)/2.0, -0.5)               # bottom-left
        ]

        # Window size around each saddle
        self.m_halfspan = 0.5
        self.l_halfspan = 0.5

    def _slice_around_saddle(self, m0, l0):
        """
        Compute escape times for a box centered on a given saddle (m0, l0).
        """
        m_range = np.linspace(m0 - self.m_halfspan,
                              m0 + self.m_halfspan, self.res)
        l_range = np.linspace(l0 - self.l_halfspan,
                              l0 + self.l_halfspan, self.res)

        M, L = np.meshgrid(m_range, l_range)
        m_curr = M.copy()
        l_curr = L.copy()
        pm = np.zeros_like(M)
        pl = np.zeros_like(L)

        escape_time = np.zeros_like(M, dtype=np.float32)
        active = np.ones_like(M, dtype=bool)

        for step in range(self.max_steps):
            if step % 1000 == 0:
                logger.info(f"  step {step}/{self.max_steps} for saddle ({m0:.3f},{l0:.3f})")

            if not np.any(active):
                break

            dV_dm, dV_dl = henon_heiles_grad(m_curr, l_curr)

            # leapfrog: half-kick
            pm[active] -= 0.5 * self.dt * dV_dm[active]
            pl[active] -= 0.5 * self.dt * dV_dl[active]

            # drift
            m_curr[active] += self.dt * pm[active]
            l_curr[active] += self.dt * pl[active]

            # second half-kick
            dV_dm, dV_dl = henon_heiles_grad(m_curr, l_curr)
            pm[active] -= 0.5 * self.dt * dV_dm[active]
            pl[active] -= 0.5 * self.dt * dV_dl[active]

            # escape condition
            r2 = m_curr**2 + l_curr**2
            escaped_now = (r2 > 20.0) & active
            if np.any(escaped_now):
                escape_time[escaped_now] = step
                active[escaped_now] = False

        return m_range, l_range, escape_time

    def render_triple_cones(self, filename="triple_jet_biopsy.png"):
        fig, axes = plt.subplots(1, 3, figsize=(18, 6), facecolor="#000510")

        for ax, (m0, l0), label in zip(
            axes,
            self.saddles,
            ["Top Port", "Bottom-Right Port", "Bottom-Left Port"]
        ):
            logger.info(f"[*] Slicing around saddle {label} at ({m0:.3f},{l0:.3f})")
            m_range, l_range, esc = self._slice_around_saddle(m0, l0)

            plot_data = np.log1p(esc)  # log scale for dynamic range

            im = ax.imshow(
                plot_data, origin="lower", cmap="inferno",
                extent=[m_range[0], m_range[-1], l_range[0], l_range[-1]]
            )

            ax.set_title(label, color="orange")
            ax.set_xlabel("M (lateral)", color="white")
            ax.set_ylabel("L (axial)", color="white")
            ax.tick_params(colors="white")

            # Mark the saddle
            ax.plot([m0], [l0], "wo", markersize=4, alpha=0.8)

        plt.tight_layout()
        plt.savefig(filename, dpi=200)
        logger.info(f"[+] Triple jet biopsy saved to: {filename}")
        plt.show()

if __name__ == "__main__":
    slicer = TripleJetSlicer(resolution=600)
    slicer.render_triple_cones()
