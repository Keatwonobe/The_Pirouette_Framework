#!/usr/bin/env python
"""
vectors_in_plasma_calib.py

Wrapper around your earlier vectors_in_plasma: adds --calib YAML that classifies windows into
Weaver/Gladiator/Drifter/Vortex, and writes an *_archetypes.csv alongside *_kappa.csv.

Usage
-----
python vectors_in_plasma_calib.py --dat ...dat --prm ...prm --calib calib.yaml --out plasma_out
python vectors_in_plasma_calib.py --stem Magnetics_E-935646-1 --pairs 1 20 --calib calib.yaml --out plasma_out --resume
"""
import argparse, json, os, re, sys, zlib, math, warnings, yaml
from pathlib import Path
from typing import Dict, List
import numpy as np, pandas as pd
from scipy.signal import butter, sosfiltfilt, hilbert

# --- helpers copied from your ingestion script ---
def parse_prm(prm_path: Path):
    meta = {}
    for line in open(prm_path, "r", encoding="utf-8"):
        line=line.strip()
        if not line: continue
        parts=line.split(",")
        if len(parts) < 3: continue
        meta[parts[1]] = parts[2]
    return meta

def meta_float(meta, key, default=None):
    try: return float(meta.get(key, ""))
    except: return default
def meta_int(meta, key, default=None):
    try: return int(float(meta.get(key, "")))
    except: return default

def derive_sfreq(meta):
    dt_us = meta_float(meta, "ClockInterval(uSec)") or meta_float(meta, "Ext.ClockInterval(uSec)")
    if dt_us and dt_us > 0:
        return 1_000_000.0 / dt_us
    raise ValueError("Cannot derive sampling frequency from PRM")

def load_dat(dat_path: Path, prm_meta: Dict[str,str], force_raw=False, force_zlib=False):
    raw = dat_path.read_bytes()
    fsize = len(raw)
    comp = (prm_meta.get("CompressionMethod","") or "").upper()
    comp_len = meta_int(prm_meta, "CompLength(byte)")
    data_len = meta_int(prm_meta, "DataLength(byte)")
    looks_like_zlib = fsize>=2 and raw[0]==0x78 and raw[1] in (0x01,0x5E,0x9C,0xDA)
    if force_raw and force_zlib:
        raise ValueError("Choose at most one of --force-raw / --force-zlib")
    must_decomp = False
    if force_zlib: must_decomp=True
    elif force_raw: must_decomp=False
    else:
        if comp.startswith("ZLIB"):
            if comp_len and fsize==comp_len: must_decomp=True
            elif data_len and fsize==data_len: must_decomp=False
            elif looks_like_zlib: must_decomp=True
            else:
                try:
                    import zlib as _z; _z.decompress(raw[:64]); must_decomp=True
                except Exception: must_decomp=False
        else:
            must_decomp=False
    if must_decomp:
        try:
            raw = zlib.decompress(raw)
        except Exception as e:
            print(f"[WARN] zlib decompress failed ({e}); using raw")
    # int16 decode (endian check)
    n_samp = meta_int(prm_meta, "Samples/Ch")
    arr = np.frombuffer(raw, dtype="<i2")
    if n_samp and arr.size!=n_samp:
        arr_be = np.frombuffer(raw, dtype=">i2")
        if arr_be.size==n_samp: arr=arr_be
    volts = arr.astype(np.float64)*meta_float(prm_meta,"VResolution",1.0)+meta_float(prm_meta,"VOffset",0.0)
    return volts

def butter_bandpass_iir(low, high, fs, order=4):
    nyq = 0.5*fs; wp=[max(1e-9, low/nyq), min(0.999999, high/nyq)]
    return butter(order, wp, btype='bandpass', output='sos')
def analytic_band(x, fs, f_lo, f_hi):
    sos = butter_bandpass_iir(f_lo, f_hi, fs, order=4)
    import numpy as _np
    from scipy.signal import sosfiltfilt, hilbert
    padlen = min(3*int(fs//2), max(0, len(x)//2))
    bp = sosfiltfilt(sos, x, axis=-1, padlen=padlen)
    z = hilbert(bp, axis=-1)
    return z
def kappa_estimator(z, fs, f_center):
    dt=1.0/fs; zp=np.gradient(z, dt, axis=-1); omega=2.0*np.pi*f_center
    num=np.imag(np.vdot(zp,z)); den=omega*np.real(np.vdot(z,z))+1e-12
    return -float(num/den)

def parse_bands(bands_list, sfreq):
    out=[]; nyq=0.5*sfreq
    for spec in bands_list:
        name,rng = spec.split(":")
        lo,hi = map(float, rng.split("-"))
        hi = min(hi, nyq-1.0); f_c=(lo+hi)/2.0
        out.append((name,lo,hi,f_c))
    return out

def classify_row(row, calib):
    b = row["band"]
    th = calib["bands"].get(b, None)
    if not th: return "Uncalibrated"
    kap = row["kappa_abs"]; dp = row["delta_power"]
    k_lo = th["kappa_lo"]; k_hi = th["kappa_hi"]; dp_pos = th["deltaP_pos"]
    if kap >= k_hi and dp >= dp_pos: return "Gladiator"
    if kap >= k_hi and dp < 0:        return "Vortex"
    if kap >= k_lo and dp >= dp_pos:  return "Weaver"
    return "Drifter"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dat")
    ap.add_argument("--prm")
    ap.add_argument("--stem")
    ap.add_argument("--pairs", nargs=2, type=int)
    ap.add_argument("--out", default="plasma_out")
    ap.add_argument("--win", type=float, default=0.050)
    ap.add_argument("--hop", type=float, default=0.025)
    ap.add_argument("--bands", nargs="+", default=["low:50-300","mid:300-1200","high:1200-4000"])
    ap.add_argument("--calib", required=True, help="Calibration YAML from plasma_calibrate.py")
    ap.add_argument("--force-raw", action="store_true")
    ap.add_argument("--force-zlib", action="store_true")
    ap.add_argument("--resume", action="store_true")
    args = ap.parse_args()

    with open(args.calib,"r") as f:
        calib = yaml.safe_load(f)

    outdir = Path(args.out); outdir.mkdir(parents=True, exist_ok=True)
    ckpt = outdir/"checkpoint.json"; state={"done":[]}
    if args.resume and ckpt.exists():
        import json
        try: state=json.loads(ckpt.read_text())
        except: pass

    jobs=[]
    if args.dat and args.prm:
        jobs.append((Path(args.dat), Path(args.prm)))
    elif args.stem and args.pairs:
        a,b=args.pairs
        for k in range(a,b+1):
            jobs.append((Path(f"{args.stem}-{k}.dat"), Path(f"{args.stem}-{k}.prm")))
    else:
        print("Provide --dat/--prm OR --stem --pairs"); return

    for dat, prm in jobs:
        if not dat.exists() or not prm.exists():
            print(f"Missing: {dat} / {prm}"); continue
        key=dat.name
        if args.resume and key in state["done"]: continue

        meta=parse_prm(prm); sf=derive_sfreq(meta)
        x=load_dat(dat, meta, force_raw=args.force_raw, force_zlib=args.force_zlib)
        bands=parse_bands(args.bands, sf)

        # Compute kappa dataframe
        import pandas as pd, numpy as np
        w=int(round(args.win*sf)); h=int(round(args.hop*sf))
        rows=[]
        N=x.size
        for (b,lo,hi,fc) in bands:
            # baseline on first chunk of windows
            pw=[]; segs=[]
            for s in range(0, max(1,N-w+1), h):
                seg=x[s:s+w]
                if len(seg)<w: break
                z=analytic_band(seg, sf, lo, hi)
                kap=kappa_estimator(z, sf, fc)
                P=float(np.mean(np.abs(z)**2))
                rows.append(dict(series=dat.stem, start=s, end=s+w, start_s=s/sf, end_s=(s+w)/sf,
                                 band=b, f_lo=lo, f_hi=hi, f_c=fc, kappa=kap, kappa_abs=abs(kap), power=P))
        df=pd.DataFrame(rows).sort_values(["band","start"])
        out=[]
        for b,g in df.groupby("band", sort=False):
            g=g.copy()
            nwin=max(10, min(50, int(0.05*g.shape[0])))
            base=g.head(nwin)["power"].median()
            g["delta_power"]=(g["power"]-base)/(base+1e-12)
            out.append(g)
        df=pd.concat(out, ignore_index=True)

        # Classify
        df["archetype"]=df.apply(lambda r: classify_row(r, calib), axis=1)

        dest=outdir/"waves"; dest.mkdir(parents=True, exist_ok=True)
        df.to_csv(dest/f"{dat.stem}_kappa.csv", index=False)
        df[["series","start_s","end_s","band","kappa_abs","delta_power","archetype"]].to_csv(
            dest/f"{dat.stem}_archetypes.csv", index=False
        )
        with open(dest/f"{dat.stem}_meta.json","w") as f:
            json.dump({"sfreq":sf, "duration_s": float(N/sf), "bands": calib.get("bands", {})}, f, indent=2)

        state["done"].append(key)
        ckpt.write_text(json.dumps(state, indent=2))
        print(f"Done {dat.name}")

if __name__=="__main__":
    main()
