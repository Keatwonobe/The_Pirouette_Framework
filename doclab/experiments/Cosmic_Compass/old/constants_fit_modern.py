# constants_fit_modern.py
import json, math, numpy as np
from dataclasses import dataclass

# ---- 1) Geometry from the modern compass ------------------------------------
@dataclass
class CompassGeom:
    gamma_scale: float = 6.0
    ta_scale: float    = 6.0
    kappa0: float      = 0.06
    kappa_decay: float = 0.08
    xi: float          = 0.8
    Ki: float          = 4.0*math.pi/3.0   # Ki_motion

    def polar(self, Gamma, Ta):
        r = np.sqrt((Gamma/self.gamma_scale)**2 + (Ta/self.ta_scale)**2)
        th = np.arctan2(Ta/self.ta_scale, Gamma/self.gamma_scale)
        return r, th

    def kappa(self, r):
        return self.kappa0 * np.exp(-self.kappa_decay * r)

    def theta_twisted(self, th, r, use_kappa=True):
        return th + (self.kappa(r) * self.xi if use_kappa else 0.0)

# ---- 2) Constants (you can pull from your mapper) ----------------------------
def load_constants():
    return {
        "alpha": 1/137.035999084,
        "mp_me": 1.67262192369e-27/9.1093837015e-31,
        "alpha_s": 0.1181,
        "alpha_w": 1/29.5,
        "sin2_thetaW": 0.23121,
        # add a few more dimensionless if you wish
    }

# Example positions (replace with ridge-picked points if you prefer):
# Each entry: name -> (Gamma, Ta)
def load_positions():
    return {
        "alpha": (1.5, 1.0),
        "mp_me": (0.0, 2.53),
        "alpha_s": (5.51, 0.0),
        "alpha_w": (-5.13, 0.0),
        "sin2_thetaW": (0.0, -2.53),
    }

# ---- 3) Shared small model class ---------------------------------------------
def design_matrix(rs, thetas_twisted, Ki, with_interact=False):
    # y = b0 + b1 r + b2 cos(Ki*th') + b3 sin(Ki*th') + [b4 r*cos(Ki th')]
    X = []
    for r, thp in zip(rs, thetas_twisted):
        row = [1.0, r, math.cos(Ki*thp), math.sin(Ki*thp)]
        if with_interact:
            row.append(r*math.cos(Ki*thp))
        X.append(row)
    return np.array(X, dtype=float)

def fit_linear(X, y):
    # ridge-free LSQ; add tiny Tikhonov if needed
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    yhat = X @ beta
    resid = y - yhat
    return beta, yhat, resid

def aic(y, yhat, k_params):
    n = len(y)
    rss = np.sum((y - yhat)**2)
    sigma2 = rss/n
    return n*np.log(sigma2 + 1e-30) + 2*k_params

# ---- 4) Run both models: kappa OFF vs ON -------------------------------------
def run_fit(use_interact=False):
    geom = CompassGeom()
    consts = load_constants()
    pos    = load_positions()

    names = []
    rs, ths, ys = [], [], []

    for name, (G, T) in pos.items():
        if name not in consts: continue
        r, th = geom.polar(G, T)
        names.append(name)
        rs.append(float(r))
        ths.append(float(th))
        ys.append(math.log(consts[name]))  # dimensionless log
    rs = np.array(rs); ths = np.array(ths); ys = np.array(ys)

    # κ OFF
    thp0 = ths  # no twist
    X0 = design_matrix(rs, thp0, geom.Ki, with_interact=use_interact)
    b0, yhat0, resid0 = fit_linear(X0, ys)
    aic0 = aic(ys, yhat0, X0.shape[1])

    # κ ON
    thp1 = np.array([geom.theta_twisted(th, r, use_kappa=True) for th, r in zip(ths, rs)])
    X1 = design_matrix(rs, thp1, geom.Ki, with_interact=use_interact)
    b1, yhat1, resid1 = fit_linear(X1, ys)
    aic1 = aic(ys, yhat1, X1.shape[1])

    out = {
        "names": names,
        "params_kOFF": b0.tolist(),
        "AIC_kOFF": float(aic0),
        "params_kON": b1.tolist(),
        "AIC_kON": float(aic1),
        "delta_AIC": float(aic1 - aic0),
        "predictions_kOFF": np.exp(yhat0).tolist(),
        "predictions_kON": np.exp(yhat1).tolist(),
        "observed": np.exp(ys).tolist(),
    }
    return out

if __name__ == "__main__":
    res = run_fit(use_interact=False)   # start simple
    print(json.dumps(res, indent=2))
