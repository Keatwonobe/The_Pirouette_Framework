"""
closure_unified.py
One-file runner for:
  - Two-loop SM RGE with top threshold (piecewise)
  - Calibration of c_norm from plateau K_i to match α_em(M_Z)
  - Predictions: sin^2 θ_W(M_Z), α_s(M_Z)
  - Upward run for (near-)unification and proton lifetime band
  - One-shot figure (α_i^{-1} vs log μ) + JSON summary

Usage (defaults use KU1=2.625, KSU2=1.878, KSU3=1.047, ΛB=200 GeV):

  python closure_unified.py \
      --KU1 2.625 --KSU2 1.878 --KSU3 1.047 --LB 200 \
      --mapping inverse --mu_max 1e17 \
      --out_prefix ./closure_unified

Author: Keaton + ChatGPT
"""

import math, json, argparse, textwrap
from dataclasses import dataclass
import numpy as np
import matplotlib.pyplot as plt

pi = math.pi
MZ   = 91.1876
mW   = 80.379
mH   = 125.10
mt   = 172.69

# SM 1-loop b's with g1 in GUT normalization
b_full = (41/10, -19/6, -7)

# 2-loop gauge matrix (SM, n_g=3)
B_full = (
    (199/50, 27/10, 44/5),
    (9/10,   35/6,  12),
    (11/10,  9/2,  -26),
)

# Yukawa coefficients entering gauge 2-loop
cY_full = (17/10, 3/2, 2)

@dataclass
class RGState:
    mu: float
    a1: float
    a2: float
    a3: float
    yt: float

def beta_alphas(a1, a2, a3, yt, nf):
    b1, b2, b3 = b_full
    b3_eff = -11 + 2.0*nf/3.0
    vec_b = (b1, b2, b3_eff)
    B = B_full
    vec_a = (a1, a2, a3)
    d_inv = []
    for i,(bi,ci) in enumerate(zip(vec_b, cY_full)):
        s = 0.0
        for j in range(3):
            s += B[i][j]*vec_a[j]
        d_inv_i = -(bi)/(2*pi) - s/(8*pi**2) + ci*yt*yt/(8*pi**2)
        d_inv.append(d_inv_i)
    return tuple(d_inv)

def beta_yt(a1, a2, a3, yt):
    g1sq = 4*pi*a1*3/5
    g2sq = 4*pi*a2
    g3sq = 4*pi*a3
    dyt = yt/(16*pi**2) * ( 4.5*yt*yt - (17/20)*g1sq - (9/4)*g2sq - 8*g3sq )
    return dyt

def rk4_step(st: RGState, dlnmu, nf):
    def deriv(s):
        di = beta_alphas(s.a1, s.a2, s.a3, s.yt, nf)
        dyt = beta_yt(s.a1, s.a2, s.a3, s.yt) if s.mu >= mt else 0.0
        return di, dyt

    def advance(s, fac, k):
        a1 = 1.0 / (1.0/s.a1 + fac*k[0][0])
        a2 = 1.0 / (1.0/s.a2 + fac*k[0][1])
        a3 = 1.0 / (1.0/s.a3 + fac*k[0][2])
        yt = s.yt + fac*k[1]
        return RGState(mu=s.mu*math.exp(fac*dlnmu), a1=a1, a2=a2, a3=a3, yt=yt)

    k1 = deriv(st)
    s2 = advance(st, 0.5, k1);          k2 = deriv(s2)
    s3 = advance(st, 0.5, k2);          k3 = deriv(s3)
    s4 = advance(st, 1.0, k3);          k4 = deriv(s4)

    inv1 = 1/st.a1 + dlnmu*(k1[0][0] + 2*k2[0][0] + 2*k3[0][0] + k4[0][0])/6
    inv2 = 1/st.a2 + dlnmu*(k1[0][1] + 2*k2[0][1] + 2*k3[0][1] + k4[0][1])/6
    inv3 = 1/st.a3 + dlnmu*(k1[0][2] + 2*k2[0][2] + 2*k3[0][2] + k4[0][2])/6
    yt   = st.yt + dlnmu*(k1[1]       + 2*k2[1]       + 2*k3[1]       + k4[1]      )/6

    return RGState(mu=st.mu*math.exp(dlnmu),
                   a1=1/inv1, a2=1/inv2, a3=1/inv3, yt=yt)

def run_piecewise_to_MZ(alpha1_LB, alpha2_LB, alpha3_LB, yt_LB, LB, steps=4000):
    st = RGState(mu=LB, a1=alpha1_LB, a2=alpha2_LB, a3=alpha3_LB, yt=yt_LB)
    n1 = max(4, steps//2)
    d1 = math.log(mt/LB)/n1
    for _ in range(n1):
        st = rk4_step(st, d1, nf=6)
    n2 = steps - n1
    d2 = math.log(MZ/mt)/max(4, n2)
    for _ in range(max(4, n2)):
        st = rk4_step(st, d2, nf=5)
    return st

def alphas_to_em_sin2(a1, a2):
    aY = (3/5)*a1
    sin2 = aY/(aY + a2)
    aem  = aY*a2/(aY + a2)
    return aem, sin2

def upward_run_from_MZ(st_MZ, mu_max=1e17, steps=6000):
    st = RGState(mu=MZ, a1=st_MZ.a1, a2=st_MZ.a2, a3=st_MZ.a3, yt=st_MZ.yt)
    dln = math.log(mu_max/MZ)/steps
    traj = []
    for _ in range(steps):
        nf = 6 if st.mu >= mt else 5
        st = rk4_step(st, dln, nf=nf)
        traj.append((st.mu, st.a1, st.a2, st.a3))
    return traj

def find_alpha12_cross(traj):
    best = None
    for (mu,a1,a2,a3) in traj:
        d = abs(1/a1 - 1/a2)
        if best is None or d < best[0]:
            best = (d, mu, a1, a2, a3)
    _, MU, a1, a2, a3 = best
    return MU, a1, a2, a3

def proton_life_band(MX, alpha_GUT, kappa=(0.5, 2.0)):
    lo = 1e35 * ( (MX/1e16)**4 ) * ( (alpha_GUT/0.04)**-2 ) * kappa[0]
    hi = 1e35 * ( (MX/1e16)**4 ) * ( (alpha_GUT/0.04)**-2 ) * kappa[1]
    return lo, hi

def alphas_at_LB_from_K(KU1, KSU2, KSU3, c_norm, mapping="inverse"):
    """
    Map stiffness triplet (K_U1, K_SU2, K_SU3) to α_i at ΛB.

    Default (recommended):
      mapping="inverse": α_i(ΛB) = c_norm / K_i^2
        (stiffer plateau → smaller coupling; units absorbed by c_norm)

    Optional (for hypothesis testing):
      mapping="direct" : α_i(ΛB) = c_norm * K_i^2
        (symmetric power for clean dimensional bookkeeping)
    """
    if mapping == "inverse":
        a1 = c_norm / (KU1**2)  # α1 (GUT-norm)
        a2 = c_norm / (KSU2**2)
        a3 = c_norm / (KSU3**2)
    elif mapping == "direct":
        a1 = c_norm * (KU1**2)
        a2 = c_norm * (KSU2**2)
        a3 = c_norm * (KSU3**2)
    else:
        raise ValueError("mapping must be 'inverse' or 'direct'")
    return a1, a2, a3

def calibrate_cnorm_to_alpha_em(KU1, KSU2, KSU3, LB, alpha_em_target=1/127.955, 
                                yt_LB=0.9, mapping="inverse", tol=1e-6, maxit=60):
    lo, hi = 1e-5, 10.0
    st_lo = None
    for _ in range(maxit):
        mid = math.sqrt(lo*hi)
        a1, a2, a3 = alphas_at_LB_from_K(KU1, KSU2, KSU3, mid, mapping)
        st_MZ = run_piecewise_to_MZ(a1, a2, a3, yt_LB, LB, steps=4000)
        aem, s2 = alphas_to_em_sin2(st_MZ.a1, st_MZ.a2)
        if abs(aem - alpha_em_target) < tol:
            return mid, st_MZ
        if aem > alpha_em_target:
            hi = mid
        else:
            lo = mid
        st_lo = st_MZ
    return mid, st_lo

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--KU1", type=float, default=2.625)
    p.add_argument("--KSU2", type=float, default=1.878)
    p.add_argument("--KSU3", type=float, default=1.047)
    p.add_argument("--LB", type=float, default=200.0, help="Bridge scale Λ_B [GeV]")
    p.add_argument("--mapping", type=str, default="inverse", choices=["inverse","direct"])
    p.add_argument("--mu_max", type=float, default=1e17)
    p.add_argument("--yt_LB", type=float, default=0.9)
    p.add_argument("--alpha_em_inv_target", type=float, default=127.955)
    p.add_argument("--out_prefix", type=str, default="./closure_unified")
    args = p.parse_args()

    alpha_em_target = 1/args.alpha_em_inv_target

    c_norm, st_MZ = calibrate_cnorm_to_alpha_em(
        args.KU1, args.KSU2, args.KSU3, args.LB, alpha_em_target,
        yt_LB=args.yt_LB, mapping=args.mapping
    )
    aem_MZ, s2_MZ = alphas_to_em_sin2(st_MZ.a1, st_MZ.a2)
    alpha_s_MZ = st_MZ.a3

    traj = upward_run_from_MZ(st_MZ, mu_max=args.mu_max, steps=6000)
    MU12, a1U, a2U, a3U = find_alpha12_cross(traj)
    alpha_GUT_est = 0.5*(a1U + a2U)
    delta13 = abs(1/a1U - 1/a3U)
    delta23 = abs(1/a2U - 1/a3U)
    tau_lo, tau_hi = proton_life_band(MU12, alpha_GUT_est, kappa=(0.5,2.0))

    # figure
    mus = np.array([x[0] for x in traj])
    a1s = np.array([x[1] for x in traj])
    a2s = np.array([x[2] for x in traj])
    a3s = np.array([x[3] for x in traj])

    plt.figure(figsize=(8,5.5))
    plt.plot(np.log10(mus), 1.0/a1s, label=r"$\alpha_1^{-1}$")
    plt.plot(np.log10(mus), 1.0/a2s, label=r"$\alpha_2^{-1}$")
    plt.plot(np.log10(mus), 1.0/a3s, label=r"$\alpha_3^{-1}$")

    def vline_at(mu, lbl):
        x = math.log10(mu)
        plt.axvline(x, linestyle="--", linewidth=1)
        plt.text(x, plt.ylim()[1]*0.92, lbl, rotation=90, va="top", ha="right")

    vline_at(MZ, "M_Z")
    vline_at(args.LB, r"$\Lambda_B$")
    vline_at(MU12, r"$\mu_{12}$")

    plt.xlabel(r"$\log_{10}\,\mu\,[\mathrm{GeV}]$")
    plt.ylabel(r"$\alpha_i^{-1}(\mu)$")
    plt.title("Two-loop SM running with thresholds (top)")
    plt.legend(loc="best")

    box = textwrap.dedent(f"""
    Inputs:
      K_U1={args.KU1}, K_SU2={args.KSU2}, K_SU3={args.KSU3}, Λ_B={args.LB} GeV, mapping={args.mapping}
    Calibration:
      c_norm={c_norm:.6g}
    M_Z predictions:
      α_em^-1={1/aem_MZ:.3f} (target {1/alpha_em_target:.3f})
      sin^2θ_W={s2_MZ:.5f}
      α_s={alpha_s_MZ:.5f}
    Unification probe:
      μ_12={MU12:.3e} GeV
      Δ(1/α1,1/α3)|μ12={delta13:.3f}, Δ(1/α2,1/α3)|μ12={delta23:.3f}
      τ_p ~ [{tau_lo:.2e}, {tau_hi:.2e}] yr
    """).strip()
    plt.gcf().text(0.02, -0.02, box, fontsize=8, va="top", ha="left")

    fig_path = args.out_prefix + "_figure.png"
    plt.tight_layout()
    plt.savefig(fig_path, dpi=160, bbox_inches="tight")

    summary = {
        "inputs": {"K_U1":args.KU1, "K_SU2":args.KSU2, "K_SU3":args.KSU3,
                   "Lambda_B_GeV":args.LB, "mapping":args.mapping},
        "calibration": {"c_norm": c_norm, "alpha_em_target": alpha_em_target},
        "MZ_outputs": {"alpha_em_inv": 1/float(aem_MZ), "sin2_thetaW": float(s2_MZ), "alpha_s": float(alpha_s_MZ)},
        "unification_probe": {
            "mu12_GeV": MU12,
            "alpha1_inv_mu12": 1/float(a1U),
            "alpha2_inv_mu12": 1/float(a2U),
            "alpha3_inv_mu12": 1/float(a3U),
            "delta13_mu12": float(delta13),
            "delta23_mu12": float(delta23)
        },
        "proton_lifetime_years_band": {"lo": tau_lo, "hi": tau_hi},
        "paths": {"figure": fig_path}
    }
    json_path = args.out_prefix + "_summary.json"
    with open(json_path, "w") as f:
        json.dump(summary, f, indent=2)

    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
