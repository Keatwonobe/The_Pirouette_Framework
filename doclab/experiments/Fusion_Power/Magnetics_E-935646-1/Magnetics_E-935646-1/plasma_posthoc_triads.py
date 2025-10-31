#!/usr/bin/env python
"""
plasma_posthoc_triads.py

Posthoc over finished *_kappa.csv (and matching *_meta.json and raw .dat/.prm if provided):
- Classify each window into archetypes using a calibration YAML.
- Detect triadic resonance (f3 ≈ f1+f2) via TPCI-style detuning scan with phase-shuffle nulls.

Outputs:
- *_archetypes.csv (if not already present)
- triads_summary.json with per-file results

Inspired by your EEG triad detector (TPCI with detuning & permutation null). See your original code. 
"""
import argparse, json, re, yaml, numpy as np, pandas as pd
from pathlib import Path
from scipy.signal import butter, filtfilt, hilbert, welch
from scipy.optimize import curve_fit

# --- Minimal re-implementation of pieces from your EEG triad tool ---
def bandpass_phase(x, fs, f_lo, f_hi):
    b,a=butter(4, [f_lo/(fs/2), f_hi/(fs/2)], btype='band')
    z=filtfilt(b,a,x,axis=-1)
    return np.angle(hilbert(z, axis=-1))

def tpci(phi1, phi2, phi3):
    z=np.exp(1j*(phi3-phi1-phi2))
    return np.abs(np.mean(z))

def gauss(x, A, mu, sig, B):
    return A*np.exp(-(x-mu)**2/(2*sig**2))+B

def halfwidth_gauss(x,y):
    try:
        mu0 = x[int(np.argmax(y))]; A0=float(np.max(y)-np.median(y)); B0=float(np.median(y)); sig0=0.25
        popt,_ = curve_fit(gauss, x, y, p0=(A0,mu0,sig0,B0), maxfev=5000)
        A,mu,sig,B = popt
        return float(np.sqrt(2*np.log(2))*abs(sig)), dict(A=A,mu=mu,sig=sig,B=B)
    except Exception:
        return np.nan, None

def phase_shuffle(phi, rng):
    T=phi.shape[-1]; shift=rng.integers(0,T); return np.roll(phi, shift, axis=-1)

# --- Raw loader from your plasma ingester (lightweight) ---
def parse_prm(prm_path):
    meta={}
    for line in open(prm_path,"r",encoding="utf-8"):
        parts=line.strip().split(",")
        if len(parts)>=3: meta[parts[1]]=parts[2]
    return meta

def meta_float(meta, key, default=None):
    try: return float(meta.get(key,""))
    except: return default

def derive_sfreq(meta):
    dt_us = meta_float(meta,"ClockInterval(uSec)") or meta_float(meta,"Ext.ClockInterval(uSec)")
    if dt_us and dt_us>0: return 1_000_000.0/dt_us
    raise ValueError("Missing ClockInterval(uSec)")

def load_volts(dat_path:Path, prm_path:Path):
    import zlib, numpy as np
    prm=parse_prm(prm_path)
    raw=dat_path.read_bytes()
    comp=(prm.get("CompressionMethod","") or "").upper()
    looks = len(raw)>=2 and raw[0]==0x78 and raw[1] in (0x01,0x5E,0x9C,0xDA)
    if comp.startswith("ZLIB") and looks:
        try: raw=zlib.decompress(raw)
        except: pass
    arr=np.frombuffer(raw, dtype="<i2")
    volts=arr.astype(np.float64)*meta_float(prm,"VResolution",1.0)+meta_float(prm,"VOffset",0.0)
    sf=derive_sfreq(prm)
    return volts, sf

def classify_df(df, calib):
    def classify_row(r):
        b=r["band"]; th=calib["bands"].get(b, None)
        if not th: return "Uncalibrated"
        kap=r["kappa_abs"]; dp=r["delta_power"]
        k_lo=th["kappa_lo"]; k_hi=th["kappa_hi"]; dp_pos=th["deltaP_pos"]
        if kap>=k_hi and dp>=dp_pos: return "Gladiator"
        if kap>=k_hi and dp<0: return "Vortex"
        if kap>=k_lo and dp>=dp_pos: return "Weaver"
        return "Drifter"
    def classify_row(r):
        b = r["band"]
        th = calib.get("bands", {}).get(b)
        if not th:
            return "Uncalibrated"

        # ✅ Coerce YAML to floats defensively
        try:
            k_lo   = float(th.get("kappa_lo"))
            k_hi   = float(th.get("kappa_hi"))
            dp_pos = float(th.get("deltaP_pos"))
        except (TypeError, ValueError):
            return "Uncalibrated"

        kap = r["kappa_abs"]
        dp  = r["delta_power"]

        # If either value is NaN, bail out to a neutral class
        if not np.isfinite(kap) or not np.isfinite(dp):
            return "Drifter"

        if kap >= k_hi and dp >= dp_pos: return "Gladiator"
        if kap >= k_hi and dp <  0:      return "Vortex"
        if kap >= k_lo and dp >= dp_pos: return "Weaver"
        return "Drifter"
    out=df.copy()
    # ✅ Force numeric; turn bad parses into NaN (which fail the thresholds gracefully)
    for col in ("kappa_abs", "delta_power"):
        out[col] = pd.to_numeric(out[col], errors="coerce")
    # ✅ Ensure band is a plain string (avoid accidental categories)
    out["band"] = out["band"].astype(str)
    out["archetype"]=out.apply(classify_row, axis=1)
    return out

def triad_scan(volts, sf, f1, f2, band=5.0, detune=2.0, pph=10, perms=200, seed=42):
    import numpy as np
    # phases
    phi1=bandpass_phase(volts, sf, f1-band, f1+band)
    phi2=bandpass_phase(volts, sf, f2-band, f2+band)
    det = np.linspace(-detune, detune, 2*int(detune*pph)+1)
    curve=[]
    for df in det:
        f3=f1+f2+df
        phi3=bandpass_phase(volts, sf, f3-band, f3+band)
        curve.append(tpci(phi1,phi2,phi3))
    curve=np.array(curve)
    bw_half, fitpars = halfwidth_gauss(det, curve) if np.ptp(curve)>0.02 else (np.nan, None)

    # null via phase-shuffle
    rng=np.random.default_rng(seed); null=[]
    for i in range(perms):
        phi2n=phase_shuffle(phi2, rng)
        cn=[]
        for df in det:
            f3=f1+f2+df
            phi3=bandpass_phase(volts, sf, f3-band, f3+band)
            cn.append(tpci(phi1,phi2n,phi3))
        bw,_=halfwidth_gauss(det, cn)
        if np.isfinite(bw): null.append(bw)
    pval = float(np.mean(np.array(null) >= bw_half)) if (np.isfinite(bw_half) and len(null)>9) else None
    return dict(detune=det.tolist(), curve=curve.tolist(), bandwidth_half=None if not np.isfinite(bw_half) else float(bw_half), p_bw_ge_null=pval)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--waves-dir", required=True, help="Folder containing *_kappa.csv and *_meta.json")
    ap.add_argument("--calib", required=True, help="Calibration YAML")
    ap.add_argument("--triads", nargs="+", default=["80,120","150,300"], help='Pairs "f1,f2" (Hz); f3=f1+f2')
    ap.add_argument("--band", type=float, default=5.0, help="+/- Hz for bandpass around f1,f2,f3")
    ap.add_argument("--detune", type=float, default=2.0)
    ap.add_argument("--pph", type=int, default=10)
    ap.add_argument("--perms", type=int, default=200)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--dat-root", help="Root folder where .dat/.prm live; if provided, triad scan runs on raw volts")
    ap.add_argument("--out", default="plasma_posthoc_out")
    args = ap.parse_args()

    waves = Path(args.waves_dir)
    outdir = Path(args.out); outdir.mkdir(parents=True, exist_ok=True)

    with open(args.calib,"r") as f:
        calib=yaml.safe_load(f)

    # 1) Classify all CSVs
    arche_summ=[]
    for csv in sorted(waves.glob("*_kappa.csv")):
        df=pd.read_csv(csv)
        df=classify_df(df, calib)
        out_csv=outdir/(csv.stem.replace("_kappa","_archetypes")+".csv")
        df.to_csv(out_csv, index=False)

        # small summary
        counts=df.groupby(["band","archetype"]).size().reset_index(name="n")
        counts["file"]=csv.name
        arche_summ.append(counts)
    if arche_summ:
        pd.concat(arche_summ, ignore_index=True).to_csv(outdir/"archetype_counts.csv", index=False)

    # 2) Triad scans on raw volts (optional)
    triad_results=[]
    if args.dat_root:
        dat_root=Path(args.dat_root)
        for meta_json in sorted(waves.glob("*_meta.json")):
            stem=meta_json.stem.replace("_meta","")
            # try to find .dat/.prm by stem
            dat = dat_root/(stem+".dat")
            prm = dat_root/(stem+".prm")
            if not (dat.exists() and prm.exists()):
                # also try splitting series naming like Magnetics_E-... already matches
                continue
            volts, sf = load_volts(dat, prm)
            for pair in args.triads:
                f1,f2=map(float, pair.split(","))
                res = triad_scan(volts, sf, f1, f2, band=args.band, detune=args.detune, pph=args.pph, perms=args.perms, seed=args.seed)
                res.update({"file": stem, "f1": f1, "f2": f2, "f3_nom": f1+f2, "sfreq": sf})
                triad_results.append(res)
        if triad_results:
            with open(outdir/"triads_summary.json","w") as f:
                json.dump(triad_results, f, indent=2)
    print(f"Done. Outputs in {outdir}")

if __name__=="__main__":
    main()
