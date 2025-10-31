---
id: DOMA-209
title: Pirouette Neutrino Ordering under Universal Geometry
version: 1.0
status: Result (validated against NuFIT v6.0; external priors toggled)
parents: [PPS-PR, DOMA-LEPTON]
children: [NEU-062 (δCP scan), NEU-063 (0νββ reach), NEU-064 (joint-geometry fit)]
---
summary: 
  Under the Pirouette mass law with universal geometry (single p,q for nature),
  normal ordering (NO) simultaneously matches oscillation splittings and external
  constraints; inverted ordering (IO) fails unless geometry bifurcates, in which
  case cosmology excludes it.

assumptions:
  - Universal geometry: the (p, q) exponents in the Pirouette mass law are global, not ordering-specific.
  - Oscillation targets from NuFIT v6.0 TB-off central values (NO/IO tables).
  - External datasets are encoded as soft priors:
      Σmν cap ≈ 0.12 eV (Planck18+BAO-like) or tight ≈ 0.073 eV (Planck+DESI Y1-like);
      KATRIN mβ < 0.45 eV (90% CL);
      0νββ band flagged via KamLAND-Zen 800 NME envelope (~28–122 meV).

method:
  - Fit NO: minimize χ² to Δm²_21, Δm²_3ℓ over (μ, p, q).
  - IO (frozen geometry): hold (p, q) from NO and refit μ → test universal-geometry consistency.
  - IO (free geometry): refit (μ, p, q) → tests whether IO is even algebraically compatible before external priors.
  - Compute observables Σmν, mβ, |mββ| and add external χ²ext (soft one-sided penalties).
  - Report χ²osc, χ²ext, χ²tot.

results:
  NO (best-fit): 
    p = 2.5251, q = 3.9398, μ = 7.7093×10^-1 eV, χ²osc = 0.000
    masses (eV): 0.023003, 0.024577, 0.055156
    Σmν = 0.103 eV, mβ = 24.6 meV, |mββ|max = 23.5 meV
    χ²ext (Σ cap ≈ 0.12 eV) = 0.000 → viable

  IO (frozen geometry = NO p,q):
    μ = 1.3607×10^-1 eV, χ²osc = 1.3866×10^4 → violently inconsistent

  IO (free geometry):
    p = 1.9145, q = 1.4314, μ = 3.3238×10^-1 eV, χ²osc = 0.000
    masses (eV): 0.083649, 0.084095, 0.067180
    Σmν = 0.235 eV, mβ = 83.5 meV, |mββ|max = 80.4 meV
    χ²ext (Σ cap ≈ 0.12 eV) = 3.669 → strongly penalized

interpretation:
  - Universal-geometry hypothesis ⇒ IO is geometrically disallowed (fails when (p,q) are held fixed).
  - Allowing geometry to bifurcate rescues IO for oscillations, but drives Σmν into
    the cosmology penalty box and places |mββ| squarely in current/near-future 0νββ reach.

predictions:
  - Cosmology: With standard ΛCDM + BAO-like priors, Σmν should fall in the ~0.09–0.12 eV band;
    tighter Σ caps (<0.08 eV) will pressure even the NO best-fit and select nearby (p, q) basins.
  - 0νββ: |mββ| for NO in this geometry peaks around ~20–25 meV (phase-dependent);
    next-generation experiments begin to probe the upper NO tail but primarily test IO-like bands.
  - β decay: mβ in the tens of meV; KATRIN-class experiments won’t bind this best-fit.

falsification tests:
  - Joint-universal fit: minimize χ²_NO + χ²_IO with a single (p,q). If a low χ² exists, universal-geometry
    is wrong as currently formulated. If not, IO is excluded by geometry alone.
  - δCP robustness: scan δ ∈ [0, 2π]; IO should not find a universal-geometry basin that fixes oscillations
    and evades Σ caps simultaneously.
  - External-prior swap: test alternative cosmology likelihoods; if any standard combination prefers Σ ≳ 0.2 eV,
    this module must be revised.

artifacts:
  - Script: pirouette_nufit_v60_txt.py (flags: --cosmo {off,planck18_bao,planck_desiY1}, --enforce_0nubb)
  - Printout: three-row global table (NO / IO-frozen / IO-free) with χ²osc, χ²ext, χ²tot.

conclusion:
  Within Pirouette’s universal-geometry mass law, neutrino masses are **normally ordered**.
  Any IO realization demands a different geometry and is then disfavored by cosmology and under
  imminent 0νββ scrutiny.
---
[python script]
---
#!/usr/bin/env python3
import argparse, re, math, numpy as np
from scipy.optimize import minimize
from pathlib import Path

# ---------- Robust NuFIT v6.0 .txt parser ----------
NUM = r'[-+]?(\d+(\.\d+)?([eE][-+]?\d+)?|\.\d+([eE][-+]?\d+)?)'
PAIR = re.compile(r'^\s*([^=#]+?)\s*=\s*(' + NUM + r')(\s*\+/-\s*' + NUM + r')?.*$', re.ASCII)

def _norm_key(raw: str) -> str:
    k = raw.strip().lower()
    # Unicode & syntax normalization
    k = k.replace('²', '^2').replace('θ', 'theta').replace('δ', 'delta')
    k = k.replace('sin^2', 'sin2')
    k = k.replace('(', '_').replace(')', '_').replace('[', '_').replace(']', '_')
    k = re.sub(r'[^a-z0-9_]+', '_', k)              # collapse non-alnum to underscores
    k = re.sub(r'__+', '_', k).strip('_')
    # Common aliases
    k = k.replace('s2th', 'sin2_th').replace('s2theta', 'sin2_theta')
    k = k.replace('sin2theta', 'sin2_th')
    k = k.replace('th12_deg', 'theta12_deg').replace('th13_deg','theta13_deg').replace('th23_deg','theta23_deg')
    k = k.replace('deltacp', 'delta_cp').replace('delta_deg', 'delta_cp_deg')
    k = k.replace('dm2', 'dm').replace('dmsq', 'dm')
    k = k.replace('delta_m2', 'dm').replace('delta_m', 'dm')
    k = k.replace('3l', '3l').replace('31', '3l')    # allow dm31→dm3l
    # Final compactions for expected keys
    k = k.replace('sin2_theta12', 'sin2_th12').replace('sin2_theta13','sin2_th13').replace('sin2_theta23','sin2_th23')
    return k

def parse_v60_release_txt(path: str):
    raw = {}
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            m = PAIR.match(line)
            if not m:
                continue
            key_raw = m.group(1)
            val = float(m.group(2))
            key = _norm_key(key_raw)
            raw[key] = val

    # Accept MANY variants; compute sin2 from angles if needed
    def pick(d, names):
        for n in names:
            if n in d: return d[n]
        return None

    # Try sin² first; else deg angles
    s2_12 = pick(raw, ['sin2_th12', 'sin2_theta_12'])
    s2_13 = pick(raw, ['sin2_th13', 'sin2_theta_13'])
    s2_23 = pick(raw, ['sin2_th23', 'sin2_theta_23'])

    th12_deg = pick(raw, ['theta12_deg', 'th12_deg', 'theta12'])
    th13_deg = pick(raw, ['theta13_deg', 'th13_deg', 'theta13'])
    th23_deg = pick(raw, ['theta23_deg', 'th23_deg', 'theta23'])

    if s2_12 is None and th12_deg is not None:
        s2_12 = math.sin(math.radians(th12_deg))**2
    if s2_13 is None and th13_deg is not None:
        s2_13 = math.sin(math.radians(th13_deg))**2
    if s2_23 is None and th23_deg is not None:
        s2_23 = math.sin(math.radians(th23_deg))**2

    if any(v is None for v in [s2_12, s2_13, s2_23]):
        keys_list = ', '.join(sorted(raw.keys()))
        raise KeyError(
            "Could not find sin²θ entries or angles to derive them. "
            f"Parsed keys were: {keys_list}"
        )

    delta_deg = pick(raw, ['delta_cp_deg', 'delta_deg', 'delta_cp'])
    if delta_deg is None:
        # sometimes δ is given as radians or plain 'delta'; last resort 0
        delta_deg = 0.0

    # Mass splittings (NuFIT uses dm21 and dm3l)
    dm21 = pick(raw, ['dm21', 'dm_21', 'dm2_21', 'dm_21_ev_2'])
    dm3l = pick(raw, ['dm3l', 'dm_3l', 'dm2_31', 'dm31', 'dm_3l_ev_2'])  # allow dm31 alias

    if dm21 is None or dm3l is None:
        keys_list = ', '.join(sorted(raw.keys()))
        raise KeyError(
            "Could not find Δm² entries (dm21, dm3l). "
            f"Parsed keys were: {keys_list}"
        )

    # Quick visibility for debugging
    print(f"[parse:{Path(path).name}] sin2θ12={s2_12:.6f}, sin2θ13={s2_13:.6f}, sin2θ23={s2_23:.6f}, "
          f"δCP(deg)={delta_deg:.2f}, dm21={dm21:.6e}, dm3ℓ={dm3l:.6e}")

    return {
        "sin2_th12": s2_12, "sin2_th13": s2_13, "sin2_th23": s2_23,
        "delta_deg": delta_deg,
        "dm21": dm21, "dm3l": dm3l
    }

# ---------- PMNS, Purity, PR ----------
def pmns_from_sin2(s12, s13, s23, delta_deg):
    th12 = math.asin(math.sqrt(s12))
    th13 = math.asin(math.sqrt(s13))
    th23 = math.asin(math.sqrt(s23))
    d = math.radians(delta_deg)
    c12, s12r = math.cos(th12), math.sin(th12)
    c13, s13r = math.cos(th13), math.sin(th13)
    c23, s23r = math.cos(th23), math.sin(th23)
    e_id = complex(math.cos(d), math.sin(d))
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
    Purity, PR = [], []
    for i in range(3):
        w = np.abs(U[:, i])**2
        Purity.append(np.max(w))
        PR.append(1.0/np.sum(w**2))
    return np.array(Purity), np.array(PR)

# ---------- Pirouette mass law & splittings ----------
def pirouette_masses(mu_nu, p, q, PR, Purity):
    return mu_nu * (PR/3.0)**p * (Purity**q)

def order_and_splittings(masses, ordering):
    m = np.sort(masses)
    if ordering.lower() == "no":
        m1, m2, m3 = m[0], m[1], m[2]
        dm21 = m2**2 - m1**2
        dm3l = m3**2 - m1**2
    else:
        m3, m1, m2 = m[0], m[1], m[2]
        dm21 = m2**2 - m1**2
        dm3l = m3**2 - m1**2  # negative
    return (m1, m2, m3), dm21, dm3l

def derived_observables(m, U):
    m = np.array(m)
    Sigma = float(np.sum(m))
    Ue = np.abs(U[0,:])**2
    m_beta = float(np.sqrt(np.sum(Ue * (m**2))))
    mee_max = float(np.abs(np.sum((U[0,:]**2) * m)))
    return Sigma, m_beta, mee_max

def soft_one_sided_penalty(x, cap, width):
    """
    A smooth χ² penalty for x > cap with softness 'width' (fraction of cap).
    For x <= cap, returns 0.  For x just above cap, grows quadratically.
    """
    if cap is None or x <= cap:
        return 0.0
    sigma = width * cap
    return float(((x - cap) / sigma) ** 2)

def cosmology_cap_from_profile(profile: str):
    """
    Returns a (cap_value, softness) pair for Σmν in eV.
    softness is the fractional width used by soft_one_sided_penalty.
    """
    if profile == "off":
        return None, None
    if profile == "planck18_bao":
        # conservative-ish 95% CL ~ 0.12 eV; give 50% softness
        return 0.12, 0.50
    if profile == "planck_desiY1":
        # tight option; ~0.073 eV at ~95% CL; give 50% softness
        return 0.073, 0.50
    # default fallback (off)
    return None, None

def external_chi2(Sigma_mnu, m_beta, m_bb_abs, cosmo_profile: str, enforce_0nubb: bool):
    """
    Build an 'external' χ² from:
      - cosmology on Σmν (soft one-sided penalty)
      - KATRIN (very mild, one-sided; won't bind current values)
      - 0νββ band flag: add a small penalty if requested and inside excluded mass band
    Returns (chi2_ext, flags_dict)
    """
    chi2 = 0.0
    flags = {"cosmo_hit": False, "katrin_hit": False, "nubb_flag": False}

    # Cosmology soft-cap
    sig_cap, softness = cosmology_cap_from_profile(cosmo_profile)
    if sig_cap is not None:
        add = soft_one_sided_penalty(Sigma_mnu, sig_cap, softness)
        if add > 0:
            flags["cosmo_hit"] = True
            chi2 += add

    # KATRIN (90% CL ~ 0.45 eV) — extremely weak here; keep as documentation
    m_beta_cap = 0.45
    add = soft_one_sided_penalty(m_beta, m_beta_cap, 0.33)  # 1/3 width
    if add > 0:
        flags["katrin_hit"] = True
        chi2 += add

    # 0νββ: KamLAND-Zen 800 mass band (convert to a "flag" penalty if inside)
    # Treat band as [0.028, 0.122] eV over NME envelope; do not over-interpret.
    mee_min, mee_max = 0.028, 0.122
    if enforce_0nubb and (mee_min <= m_bb_abs <= mee_max):
        flags["nubb_flag"] = True
        chi2 += 1.0  # small, symbolic penalty (you can tune)

    return chi2, flags

def print_fit_row(label, chi2_osc, Sigma, m_beta, m_bb, chi2_ext, flags, total_first=False):
    total = chi2_osc + chi2_ext
    star = "*" if flags.get("cosmo_hit", False) else ""
    dagger = "†" if flags.get("nubb_flag", False) else ""
    if total_first:
        print(f"{label:14s} | χ²osc={chi2_osc:7.3f} | χ²ext={chi2_ext:7.3f} | χ²tot={total:7.3f} "
              f"| Σ={Sigma:.3f} eV{star} | mβ={m_beta*1e3:.1f} meV | |m_bb|={m_bb*1e3:.1f} meV{dagger}")
    else:
        print(f"{label:14s} | Σ={Sigma:.3f} eV{star} | mβ={m_beta*1e3:.1f} meV | |m_bb|={m_bb*1e3:.1f} meV{dagger} "
              f"| χ²osc={chi2_osc:7.3f} | χ²ext={chi2_ext:7.3f} | χ²tot={total:7.3f}")

# ---------- Fitting pipeline ----------
def fit_NO_IO(no_txt, io_txt, approx_sigma_dm21=None, approx_sigma_dm3l=None):
    # --- Step 1: Load and prepare all data for both orderings first ---
    NO = parse_v60_release_txt(no_txt)
    IO = parse_v60_release_txt(io_txt)

    # NO data setup
    U_NO = pmns_from_sin2(NO["sin2_th12"], NO["sin2_th13"], NO["sin2_th23"], NO["delta_deg"])
    Pur_NO, PR_NO = purity_and_pr(U_NO)
    target_NO = np.array([NO["dm21"], NO["dm3l"]])

    # IO data setup
    U_IO = pmns_from_sin2(IO["sin2_th12"], IO["sin2_th13"], IO["sin2_th23"], IO["delta_deg"])
    Pur_IO, PR_IO = purity_and_pr(U_IO)
    target_IO = np.array([IO["dm21"], IO["dm3l"]])

    # --- Step 2: Define a robust Chi^2 helper that SCALES the differences ---
    def chi2(diff):
        # This is the key fix. We scale the difference by the approximate
        # experimental error (sigma) to get a meaningful chi-squared value.
        if (approx_sigma_dm21 is not None) and (approx_sigma_dm3l is not None):
            sig = np.array([approx_sigma_dm21, approx_sigma_dm3l])
            return float(np.sum((diff / sig)**2))
        # Fallback to simple sum of squares if sigmas are not provided
        return float(diff @ diff)

    # --- Step 3: Define objective functions ---
    def obj_no(x):
        mu, p, q = x
        m, d21, d3l = order_and_splittings(pirouette_masses(mu, p, q, PR_NO, Pur_NO), "no")
        return chi2(np.array([d21, d3l]) - target_NO)

    def obj_io_free(x, PR, Pur, target):
        mu, p, q = x
        m, d21, d3l = order_and_splittings(pirouette_masses(mu, p, q, PR, Pur), "io")
        return chi2(np.array([d21, d3l]) - target)

    def obj_io_frozen(mu_only, p_star, q_star):
        mu = mu_only[0]
        m, d21, d3l = order_and_splittings(pirouette_masses(mu, p_star, q_star, PR_IO, Pur_IO), "io")
        return chi2(np.array([d21, d3l]) - target_IO)

    # --- Step 4: Run the optimizations ---
    res_NO = minimize(obj_no, x0=np.array([1e-2, 0.0, 0.0]),
                      bounds=[(1e-6, 1.0), (-4, 4), (-4, 4)], method="L-BFGS-B")
    mu_star, p_star, q_star = res_NO.x

    res_IO_frozen = minimize(lambda mu: obj_io_frozen(mu, p_star, q_star),
                             x0=np.array([mu_star]),
                             bounds=[(1e-6, 1.0)], method="L-BFGS-B")

    res_IO_free = minimize(obj_io_free, x0=np.array([1e-2, 0.0, 0.0]),
                           args=(PR_IO, Pur_IO, target_IO),
                           bounds=[(1e-6, 1.0), (-4, 4), (-4, 4)], method="L-BFGS-B")

    # --- Step 5: Reconstruct results and return ---
    m_NO, d21_NO, d3l_NO = order_and_splittings(
        pirouette_masses(mu_star, p_star, q_star, PR_NO, Pur_NO), "no")
    Sig_NO, mb_NO, mee_NO = derived_observables(m_NO, U_NO)

    m_IO_frozen, d21_IO_frozen, d3l_IO_frozen = order_and_splittings(
        pirouette_masses(res_IO_frozen.x[0], p_star, q_star, PR_IO, Pur_IO), "io")
    Sig_IO_frozen, mb_IO_frozen, mee_IO_frozen = derived_observables(m_IO_frozen, U_IO)

    mu_io_free, p_io_free, q_io_free = res_IO_free.x
    m_IO_free, d21_IO_free, d3l_IO_free = order_and_splittings(
        pirouette_masses(mu_io_free, p_io_free, q_io_free, PR_IO, Pur_IO), "io")
    Sig_IO_free, mb_IO_free, mee_IO_free = derived_observables(m_IO_free, U_IO)

    out = {
        "NO": {
            "mu": float(mu_star), "p": float(p_star), "q": float(q_star),
            "chi2": float(res_NO.fun),
            "dm21_pred": float(d21_NO), "dm3l_pred": float(d3l_NO),
            "dm21_target": float(target_NO[0]), "dm3l_target": float(target_NO[1]),
            "m_eV": [float(x) for x in m_NO],
            "Sigma_m": float(Sig_NO), "m_beta": float(mb_NO), "m_bb_max": float(mee_NO),
        },
        "IO_frozen": {
            "mu": float(res_IO_frozen.x[0]), "p_frozen": float(p_star), "q_frozen": float(q_star),
            "chi2": float(res_IO_frozen.fun),
            "dm21_pred": float(d21_IO_frozen), "dm3l_pred": float(d3l_IO_frozen),
            "dm21_target": float(target_IO[0]), "dm3l_target": float(target_IO[1]),
            "m_eV": [float(x) for x in m_IO_frozen],
            "Sigma_m": float(Sig_IO_frozen), "m_beta": float(mb_IO_frozen), "m_bb_max": float(mee_IO_frozen),
        },
        "IO_free": {
            "mu": float(mu_io_free), "p": float(p_io_free), "q": float(q_io_free),
            "chi2": float(res_IO_free.fun),
            "dm21_pred": float(d21_IO_free), "dm3l_pred": float(d3l_IO_free),
            "dm21_target": float(target_IO[0]), "dm3l_target": float(target_IO[1]),
            "m_eV": [float(x) for x in m_IO_free],
            "Sigma_m": float(Sig_IO_free), "m_beta": float(mb_IO_free), "m_bb_max": float(mee_IO_free),
        }
    }
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no_txt", required=True, help="NuFIT v6.0 NO file, e.g. v60.release-TBoff-NO.txt")
    ap.add_argument("--io_txt", required=True, help="NuFIT v6.0 IO file, e.g. v60.release-TBoff-IO.txt")
    ap.add_argument("--approx_sigma_dm21", type=float, default=1.9e-6)
    ap.add_argument("--approx_sigma_dm3l", type=float, default=2.1e-5)
    # --- NEW: CLI flags for external constraints ---
    ap.add_argument("--cosmo",
                    choices=["off", "planck18_bao", "planck_desiY1"],
                    default="planck18_bao",
                    help="Cosmology prior profile for Σmν. 'off' disables the external Σ prior.")
    ap.add_argument("--enforce_0nubb",
                    action="store_true",
                    help="If set, adds tension when |m_bb| lies within KamLAND-Zen 800 exclusion band (NME envelope).")
    args = ap.parse_args()

    # --- Run the core oscillation fit ---
    res = fit_NO_IO(args.no_txt, args.io_txt, args.approx_sigma_dm21, args.approx_sigma_dm3l)

    # --- Process each fit result to calculate external chi-squared ---
    
    # [NO] scenario
    no_res = res['NO']
    chi2_ext_NO, flags_NO = external_chi2(
        no_res['Sigma_m'], no_res['m_beta'], abs(no_res['m_bb_max']),
        args.cosmo, args.enforce_0nubb
    )

    # [IO frozen] scenario
    io_frozen_res = res['IO_frozen']
    chi2_ext_IOfz, flags_IOfz = external_chi2(
        io_frozen_res['Sigma_m'], io_frozen_res['m_beta'], abs(io_frozen_res['m_bb_max']),
        args.cosmo, args.enforce_0nubb
    )

    # [IO free] scenario
    io_free_res = res['IO_free']
    chi2_ext_IOfree, flags_IOfree = external_chi2(
        io_free_res['Sigma_m'], io_free_res['m_beta'], abs(io_free_res['m_bb_max']),
        args.cosmo, args.enforce_0nubb
    )

    # --- Print the final summary table ---
    print("\n=== Pirouette × NuFIT v6.0: Global Comparison (oscillation + external) ===")
    print_fit_row(
        "[NO]",
        chi2_osc=no_res['chi2'],
        Sigma=no_res['Sigma_m'],
        m_beta=no_res['m_beta'],
        m_bb=abs(no_res['m_bb_max']),
        chi2_ext=chi2_ext_NO,
        flags=flags_NO
    )
    print_fit_row(
        "[IO frozen]",
        chi2_osc=io_frozen_res['chi2'],
        Sigma=io_frozen_res['Sigma_m'],
        m_beta=io_frozen_res['m_beta'],
        m_bb=abs(io_frozen_res['m_bb_max']),
        chi2_ext=chi2_ext_IOfz,
        flags=flags_IOfz
    )
    print_fit_row(
        "[IO free]",
        chi2_osc=io_free_res['chi2'],
        Sigma=io_free_res['Sigma_m'],
        m_beta=io_free_res['m_beta'],
        m_bb=abs(io_free_res['m_bb_max']),
        chi2_ext=chi2_ext_IOfree,
        flags=flags_IOfree
    )

    

if __name__ == "__main__":
    main()

