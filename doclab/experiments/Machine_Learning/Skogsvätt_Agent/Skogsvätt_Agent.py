import numpy as np

class Skogsvatt:
    """
    Minimal Triadic Operator Agent (no RL backend).
    State x ∈ ℝ^n evolves purely by operator dynamics.
    """
    def __init__(self, dim=8):
        self.x = np.random.randn(dim) * 0.1
        self.x_prev = self.x.copy()

        # phase
        self.phi = 0.0
        self.omega = 0.25 * np.pi  # theta-like
        self.update_window = (0.0, np.pi/2)

        # thresholds
        self.DR_shadow = 1.5

        # parameters
        self.eta_P = 0.05
        self.eta_S = 0.02
        self.eta_Q = 0.08
        self.eta_C = 0.03
        self.eta_B = 0.10

        # precision coefficients
        self.a0 = -1.0
        self.aS =  1.2
        self.aDR = 0.8
        self.aG =  0.3

    # ----- metrics -----

    def DR(self, x):
        # dark residue = norm of curvature (proxy)
        return np.linalg.norm(x)**2

    def contrast_grad(self, x):
        # arbitrary potential: pushes toward edges
        return np.tanh(x)

    def shadow_grad(self, x):
        # pulls back toward safe region
        return -x

    # ----- main step -----

    def step(self, Gamma=0.1):
        # compute metrics
        DR_t = self.DR(self.x)
        DR_prev = self.DR(self.x_prev)

        S_t = np.linalg.norm(self.x - self.x_prev)
        Q_t = max(0.0, DR_prev - DR_t)
        C_t = abs(DR_t - DR_prev)
        B_t = 1.0 if DR_t > self.DR_shadow else 0.0

        # phase gate
        self.phi = (self.phi + self.omega + 0.1*np.random.randn()) % (2*np.pi)
        g = 1.0 if self.update_window[0] <= self.phi <= self.update_window[1] else 0.0

        # precision
        Pi_t = 1/(1 + np.exp(
            -(self.a0 + self.aS*S_t - self.aDR*DR_t - self.aG*Gamma)
        ))

        # gradients
        grad_DR = 2*self.x

        # operator components
        O_P = -g * self.eta_P * Pi_t * grad_DR
        O_S =  g * self.eta_S * S_t * np.random.randn(*self.x.shape)
        O_C =  g * ( self.eta_Q * Q_t * (self.x - self.x_prev)
                    + self.eta_C * C_t * self.contrast_grad(self.x)
                    - self.eta_B * B_t * self.shadow_grad(self.x) )

        # update
        delta_x = O_P + O_S + O_C
        x_new = self.x + delta_x

        # rotate state
        self.x_prev = self.x
        self.x = x_new
        return self.x, dict(DR=DR_t, S=S_t, Q=Q_t, C=C_t, B=B_t, Pi=Pi_t, g=g)
