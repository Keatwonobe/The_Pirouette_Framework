import argparse, json, math, numpy as np, pandas as pd
from pathlib import Path
from scipy.optimize import minimize
from scipy.interpolate import interp1d, griddata

# ---------- Utilities
def pmns_from_angles(s12, s13, s23, delta_deg):
    # sines of angles are given as sin^2 in NuFIT tables; caller passes s12=sin^2(theta12), etc.
    th12 = math.asin(math.sqrt(s12))
    th13 = math.asin(math.sqrt(s13))
    th23 = math.asin(math.sqrt(s23))
    d = math.radians(delta_deg)
    c12, s12r = math.cos(th12), math.sin(th12)
    c13, s13r = math.cos(th13), math.sin(th13)
    c23, s23r = math.cos(th23), math.sin(th23)
    e_id = complex(math.cos(d), math.sin(d))  # e^{iδ}
    # PDG-like parameterization
    U = np.zeros((3,3), dtype=complex)
    U[0,0] = c12*c13
    U[0,1] = s12r*c13
    U[0,2] = s13r*np.conjugate(e_id)
    U[1,0] = -s12r*c23 - c12*s23r*s13r*e_id
    U[1,1] =  c12*c23 - s12r*s23r*s13r*e_id
    U[1,2] =  s23r*c13
    U[2,0] =  s12r*s23r - c12*c23*s13r*e_id
    U[2,1] = -c12*s23r - s12r*c23*s13r*e_id
    U[2,2] =  c23*c13
    return U

def purity_and_pr(U):
    # Columns are mass eigenstates i=1..3; rows are flavors e,mu,tau
    Purity = []
    PR = []
    for i in range(3):
        col = U[:, i]
        w = np.abs(col)**2
        Purity.append(np.max(w))
        PR.append(1.0/np.sum(w**2))
    return np.array(Purity), np.array(PR)

def pirouette_masses(mu_nu, p, q, PR, Purity):
    return mu_nu * (PR/3.0)**p * (Purity**q)  # m1,m2,m3 (unordered)

def order_and_splittings(masses, ordering):
    # Sort to match NO or IO conventions (m1<m2<m3 for NO; m3<m1<m2 for IO)
    m = np.sort(masses)
    if ordering.lower() == "no":
        m1, m2, m3 = m[0], m[1], m[2]
        dm21 = m2**2 - m1**2
        dm3l = m3**2 - m1**2
    else:
        # IO: m3 is the lightest
        m3, m1, m2 = m[0], m[1], m[2]
        dm21 = m2**2 - m1**2
        dm3l = m3**2 - m1**2  # negative by convention; compare by absolute value if needed
    return (m1, m2, m3), dm21, dm3l

def read_params_table(path):
    # Expect columns: sin2_th12, sin2_th13, sin2_th23, dm21, dm3l, delta_deg
    df = pd.read_csv(path)
    row = df.iloc[0].to_dict()
    return (row["sin2_th12"], row["sin2_th13"], row["sin2_th23"],
            row["dm21"], row["dm3l"], row["delta_deg"])

def chi2_from_cov(vec_diff, cov=None, sigma=None):
    if cov is not None:
        C = np.array(pd.read_csv(cov, header=None))
        return float(vec_diff.T @ np.linalg.inv(C) @ vec_diff)
    elif sigma is not None:
        return float(np.sum((vec_diff/np.array(sigma))**2))
    else:
        return float(vec_diff @ vec_diff)

def load_profile_curve(path_csv):
    df = pd.read_csv(path_csv)
    x = df.iloc[:,0].values
    y = df.iloc[:,1].values
    return interp1d(x, y, kind='linear', bounds_error=False, fill_value=np.nan)

# ---------- Fit pipeline
def fit_no_then_io(files, approx_sigmas=None):
    # 1) NO seed angles/targets
    s12, s13, s23, dm21_NO, dm3l_NO, delta_NO = read_params_table(files["params_NO"])
    U_NO = pmns_from_angles(s12, s13, s23, delta_NO)
    Purity, PR = purity_and_pr(U_NO)

    target_NO = np.array([dm21_NO, dm3l_NO])

    def objective_no(x):
        mu, p, q = x
        m, d21, d3l = order_and_splittings(pirouette_masses(mu, p, q, PR, Purity), "no")
        pred = np.array([d21, d3l])
        diff = pred - target_NO
        return chi2_from_cov(diff, cov=files.get("cov_NO"), sigma=approx_sigmas)

    x0 = np.array([1e-2, 0.0, 0.0])  # mu in eV-ish, flat p,q prior
    bounds = [(1e-6, 1.0), (-3, 3), (-3, 3)]
    res_NO = minimize(objective_no, x0, bounds=bounds, method="L-BFGS-B")

    mu_star, p_star, q_star = res_NO.x

    # 2) IO refit mu only (freeze p,q)
    s12I, s13I, s23I, dm21_IO, dm3l_IO, delta_IO = read_params_table(files["params_IO"])
    U_IO = pmns_from_angles(s12I, s13I, s23I, delta_IO)
    PurityI, PRI = purity_and_pr(U_IO)
    target_IO = np.array([dm21_IO, dm3l_IO])

    def objective_io(mu_only):
        mu = mu_only[0]
        m, d21, d3l = order_and_splittings(pirouette_masses(mu, p_star, q_star, PRI, PurityI), "io")
        pred = np.array([d21, d3l])
        diff = pred - target_IO
        return chi2_from_cov(diff, cov=files.get("cov_IO"), sigma=approx_sigmas)

    res_IO = minimize(objective_io, np.array([mu_star]), bounds=[(1e-6, 1.0)], method="L-BFGS-B")
    mu_io = res_IO.x[0]
    return (res_NO, mu_star, p_star, q_star), (res_IO, mu_io), (Purity, PR, PurityI, PRI)

def derived_observables(m, U):
    # Sigma m, m_beta, m_bb ranges (no Majorana phases here; |m_bb| lower bound 0.. upper via |sum U_ei^2 m_i|)
    m = np.array(m)
    Sigma = float(np.sum(m))
    Ue = np.abs(U[0,:])**2
    m_beta = float(np.sqrt(np.sum(Ue * (m**2))))
    # crude max for m_bb assuming aligned phases:
    mee_max = float(np.abs(np.sum((U[0,:]**2) * m)))
    return Sigma, m_beta, mee_max

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--params_NO", required=True)
    ap.add_argument("--params_IO", required=True)
    ap.add_argument("--cov_NO", default=None)
    ap.add_argument("--cov_IO", default=None)
    ap.add_argument("--profiles_dir", default=None)
    ap.add_argument("--grid_theta23_delta", default=None)
    ap.add_argument("--approx_sigma_dm21", type=float, default=None)
    ap.add_argument("--approx_sigma_dm3l", type=float, default=None)
    args = ap.parse_args()

    files = {"params_NO": args.params_NO, "params_IO": args.params_IO,
             "cov_NO": args.cov_NO, "cov_IO": args.cov_IO}

    sigmas = None
    if args.approx_sigma_dm21 and args.approx_sigma_dm3l:
        sigmas = [args.approx_sigma_dm21, args.approx_sigma_dm3l]

    (res_NO, mu, p, q), (res_IO, mu_io), (Purity, PR, PurityI, PRI) = fit_no_then_io(files, approx_sigmas=sigmas)
    # Reconstruct masses & derived quantities
    s12, s13, s23, dm21_NO, dm3l_NO, delta_NO = read_params_table(args.params_NO)
    U_NO = pmns_from_angles(s12, s13, s23, delta_NO)
    m_NO, d21_NO, d3l_NO = order_and_splittings(pirouette_masses(mu, p, q, PR, Purity), "no")
    Sig_NO, mb_NO, mee_NO = derived_observables(m_NO, U_NO)

    s12I, s13I, s23I, dm21_IO, dm3l_IO, delta_IO = read_params_table(args.params_IO)
    U_IO = pmns_from_angles(s12I, s13I, s23I, delta_IO)
    m_IO, d21_IO, d3l_IO = order_and_splittings(pirouette_masses(mu_io, p, q, PRI, PurityI), "io")
    Sig_IO, mb_IO, mee_IO = derived_observables(m_IO, U_IO)

    print("\n=== Pirouette vs NuFIT v6.0 ===")
    print(f"NO fit:  mu={mu:.6e} eV,  p={p:.4f},  q={q:.4f},  χ²={res_NO.fun:.3f}")
    print(f" -> m_NO = {m_NO} eV;  Σm={Sig_NO:.4e} eV;  m_beta={mb_NO:.4e} eV;  |m_bb|_max={mee_NO:.4e} eV")
    print(f" -> Δm^2_21={d21_NO:.4e} eV^2  (NuFIT target {dm21_NO:.4e})")
    print(f" -> Δm^2_3l={d3l_NO:.4e} eV^2  (NuFIT target {dm3l_NO:.4e})")

    print(f"\nIO refit: mu={mu_io:.6e} eV (p,q frozen),  χ²={res_IO.fun:.3f}")
    print(f" -> m_IO = {m_IO} eV;  Σm={Sig_IO:.4e} eV;  m_beta={mb_IO:.4e} eV;  |m_bb|_max={mee_IO:.4e} eV")
    print(f" -> Δm^2_21={d21_IO:.4e} eV^2  (NuFIT target {dm21_IO:.4e})")
    print(f" -> Δm^2_3l={d3l_IO:.4e} eV^2  (NuFIT target {dm3l_IO:.4e})")

    # Optional likelihood evaluation from 1D profiles
    if args.profiles_dir:
        profs = {}
        for name in ["delta_cp", "theta23"]:  # extend if you have more
            f = Path(args.profiles_dir) / f"{name}_profile.csv"
            if f.exists():
                profs[name] = load_profile_curve(str(f))
        if "delta_cp" in profs:
            dc_NO = delta_NO
            dc_pen = profs["delta_cp"](dc_NO)
            print(f"\nProfile likelihood check: Δχ²(δ_CP={dc_NO:.1f}°) ≈ {dc_pen:.3f} (NO)")
        if "theta23" in profs:
            th23_deg = math.degrees(math.asin(math.sqrt(s23)))
            print(f"Profile likelihood check: evaluating θ23 ≈ {th23_deg:.2f}°")
            print(f" -> Δχ²(θ23) ≈ {profs['theta23'](th23_deg):.3f}")

    # Optional 2D grid glance
    if args.grid_theta23_delta and Path(args.grid_theta23_delta).exists():
        df = pd.read_csv(args.grid_theta23_delta)
        pts = df[["theta23_deg","delta_deg"]].values
        z = df["dchi2"].values
        th23_deg = math.degrees(math.asin(math.sqrt(s23)))
        dchi2_here = griddata(pts, z, (th23_deg, delta_NO), method='linear')
        print(f"\n2D grid check Δχ²(θ23={th23_deg:.2f}°, δ={delta_NO:.1f}°) ≈ {float(dchi2_here):.3f}")

if __name__ == "__main__":
    main()
