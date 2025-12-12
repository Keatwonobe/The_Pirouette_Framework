# reverse_orbital_particle_fractal.py

import numpy as np
import matplotlib.pyplot as plt
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


class AnalyticalSpireArchitect:
    def __init__(
        self,
        resolution=1000,
        zoom=1e-5,
        center_real=-1.8,
        center_imag=0.0,
        twist=2.83814,
        max_radius=4.0,
    ):
        """
        Reverse-orbital analytical fractal.

        center_real, center_imag : location of the particle's fixed point
                                   in the (mass, coupling) plane.
        twist                    : angular twist per unit log-radius (your 2.83814).
        """
        self.resolution = resolution
        self.zoom = zoom
        self.center_real = center_real
        self.center_imag = center_imag
        self.twist = twist
        self.max_radius = max_radius

    # --- core analytical maps ----------------------------------------------

    def decoherence_time(self, x, y):
        """
        Analytical 'time-to-escape' / decoherence scale.
        Same functional form as your previous script; just factored out.
        """
        z = x + 1j * y
        # distance from particle core in complex plane
        r = np.abs(z)
        # avoid division by zero
        r = np.maximum(r, 1e-12)

        # toy model: logarithmic + twist-weighted term
        # (this is the same structure you were using, just written explicitly)
        t = np.log1p(self.max_radius / r) / self.twist
        return t

    def asymptotic_phase(self, x, y):
        """
        Asymptotic basin label: angle of the reverse orbit.
        """
        z = x + 1j * y
        theta = np.angle(z)
        # add a twist-dependent logarithmic winding
        r = np.abs(z)
        r = np.maximum(r, 1e-12)
        return theta + self.twist * np.log(r)

    # --- rendering -----------------------------------------------------------

    def render_blueprint(self, save_path=None):
        N = self.resolution
        span = self.zoom

        logger.info(f"[Spire] resolution={N}, zoom={span}, center=({self.center_real}, {self.center_imag}), "
                    f"twist={self.twist}")

        x = np.linspace(self.center_real - span, self.center_real + span, N)
        y = np.linspace(self.center_imag - span, self.center_imag + span, N)
        X, Y = np.meshgrid(x, y)

        # translate to local coordinates around the particle core
        Xloc = X - self.center_real
        Yloc = Y - self.center_imag

        deco = self.decoherence_time(Xloc, Yloc)
        phase = self.asymptotic_phase(Xloc, Yloc)

        fig, axes = plt.subplots(1, 2, figsize=(12, 6))

        # Left: decoherence time (log stretched)
        im0 = axes[0].imshow(np.log10(deco), origin='lower')
        axes[0].set_title("Predicted Decoherence Time (log10 scale)")
        axes[0].axis('off')
        fig.colorbar(im0, ax=axes[0], fraction=0.046, pad=0.04)

        # Right: phase basins (wrapped)
        phase_wrapped = np.mod(phase, 2 * np.pi)
        im1 = axes[1].imshow(phase_wrapped, origin='lower')
        axes[1].set_title("Reverse Orbital Phase Map")
        axes[1].axis('off')
        fig.colorbar(im1, ax=axes[1], fraction=0.046, pad=0.04)

        plt.suptitle(
            f"Reverse-Orbital Fractal\n"
            f"center=({self.center_real:.3f}, {self.center_imag:.3f}), twist={self.twist:.5f}",
            fontsize=14,
        )
        plt.tight_layout()

        if save_path is not None:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"[Spire] Saved fractal to: {save_path}")
        else:
            plt.show()


def electron_fractal():
    """
    Electron: your original parameter choice.
    """
    arch = AnalyticalSpireArchitect(
        resolution=1000,
        zoom=1e-5,
        center_real=-1.8,
        center_imag=0.0,
        twist=2.83814,
    )
    arch.render_blueprint(save_path="electron_fractal.png")


def muon_fractal():
    """
    Muon: same universal twist, but fixed point deeper in the mass well and
    slightly offset in coupling.

    The numbers here are a *model choice*:

    - mass ratio m_mu / m_e ≈ 206.768
    - we map that to a shift along the mass field axis and a slightly
      tighter zoom (shorter coherence length).
    """
    # heuristic mapping from mass ratio to field-space shift
    mass_ratio = 206.768
    delta_m = np.log10(mass_ratio)  # ≈ 2.31

    center_real_mu = -1.8 - 0.5 * delta_m   # push deeper along mass axis
    center_imag_mu = 0.15                   # small off-axis coupling
    twist_mu = 2.83814                      # keep same universal twist

    arch = AnalyticalSpireArchitect(
        resolution=1200,
        zoom=5e-6,          # smaller coherence bubble
        center_real=center_real_mu,
        center_imag=center_imag_mu,
        twist=twist_mu,
    )
    arch.render_blueprint(save_path="muon_fractal.png")


if __name__ == "__main__":
    # electron_fractal()
    muon_fractal()
