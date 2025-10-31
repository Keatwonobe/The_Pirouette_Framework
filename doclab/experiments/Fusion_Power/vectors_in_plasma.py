#!/usr/bin/env python
"""
vectors_in_plasma.py

Ingest LHD Magnetics_E .dat/.prm pairs and compute helical κ metrics.
(See header in previous message for usage.)
"""
import argparse, json, os, re, sys, zlib, math, warnings
from pathlib import Path
from typing import Dict, Tuple, List

import numpy as np
import pandas as pd
from scipy.signal import butter, sosfiltfilt, hilbert

def parse_prm(prm_path: Path) -> Dict[str, str]:
    meta = {}
    with open(prm_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line: continue
            parts = line.split(",")
            if len(parts) < 3: continue
            key, val = parts[1], parts[2]
            meta[key] = val
    return meta

def meta_float(meta: Dict[str,str], key: str, default=None):
    try:
        return float(meta.get(key, ""))
    except Exception:
        return default

def meta_int(meta: Dict[str,str], key: str, default=None):
    try:
        return int(float(meta.get(key, "")))
    except Exception:
        return default

def derive_sfreq(meta: Dict[str,str]) -> float:
    dt_us = meta_float(meta, "ClockInterval(uSec)") or meta_float(meta, "Ext.ClockInterval(uSec)")
    if dt_us and dt_us > 0:
        return 1_000_000.0 / dt_us
    raise ValueError("Cannot derive sampling frequency from PRM; missing ClockInterval(uSec).")

def load_dat(dat_path: Path, prm_meta: Dict[str,str], force_raw=False, force_zlib=False) -> np.ndarray:
    """
    Load LHD .dat as int16; decompress if needed. Decide using:
      - file size vs CompLength(byte)/DataLength(byte)
      - zlib header sniff (0x78 0x01/5E/9C/DA)
    Then scale to volts via VResolution & VOffset.
    """
    raw_bytes = dat_path.read_bytes()
    fsize = len(raw_bytes)

    comp = (prm_meta.get("CompressionMethod","") or "").upper()
    comp_len = meta_int(prm_meta, "CompLength(byte)")
    data_len = meta_int(prm_meta, "DataLength(byte)")
    n_samp  = meta_int(prm_meta, "Samples/Ch")

    # Heuristics
    looks_like_zlib = fsize >= 2 and raw_bytes[0] == 0x78 and raw_bytes[1] in (0x01, 0x5E, 0x9C, 0xDA)

    # Decide decompress?
    must_decompress = False
    if force_raw and force_zlib:
        raise ValueError("Choose at most one of --force-raw / --force-zlib.")
    if force_zlib:
        must_decompress = True
    elif force_raw:
        must_decompress = False
    else:
        if comp.startswith("ZLIB"):
            if comp_len and fsize == comp_len:
                must_decompress = True
            elif data_len and fsize == data_len:
                must_decompress = False
            elif looks_like_zlib:
                must_decompress = True
            else:
                # ambiguous: try decompress; fall back to raw on failure
                try:
                    _ = zlib.decompress(raw_bytes[:64])
                    must_decompress = True
                except zlib.error:
                    must_decompress = False
        else:
            must_decompress = False

    # Do it (with graceful fallback)
    if must_decompress:
        try:
            raw_bytes = zlib.decompress(raw_bytes)
            print(f"[load_dat] Decompressed zlib: {fsize} → {len(raw_bytes)} bytes")
        except zlib.error as e:
            print(f"[load_dat] WARN: zlib decompress failed ({e}); using raw bytes")
            # fall through to raw

    # Sanity vs DataLength(byte)
    if data_len and len(raw_bytes) != data_len:
        print(f"[load_dat] NOTE: bytes={len(raw_bytes)} vs DataLength(byte)={data_len} (continuing)")

    # Interpret as int16, try LE then BE if count mismatches
    arr = np.frombuffer(raw_bytes, dtype="<i2")
    if n_samp and arr.size != n_samp:
        arr_be = np.frombuffer(raw_bytes, dtype=">i2")
        if arr_be.size == n_samp:
            print("[load_dat] Using big-endian int16")
            arr = arr_be
        else:
            print(f"[load_dat] NOTE: sample count {arr.size} != PRM Samples/Ch {n_samp}; proceeding with little-endian")

    # Scale to volts
    vres = meta_float(prm_meta, "VResolution", 1.0)
    voff = meta_float(prm_meta, "VOffset", 0.0)
    volts = arr.astype(np.float64) * vres + voff
    return volts


def butter_bandpass_iir(low, high, fs, order=4):
    nyq = 0.5 * fs
    wp = [max(1e-9, low/nyq), min(0.999999, high/nyq)]
    return butter(order, wp, btype='bandpass', output='sos')

def analytic_band(x: np.ndarray, sfreq: float, f_lo: float, f_hi: float) -> np.ndarray:
    sos = butter_bandpass_iir(f_lo, f_hi, sfreq, order=4)
    padlen = min(3 * int(sfreq//2), max(0, len(x)//2))
    bp = sosfiltfilt(sos, x, axis=-1, padlen=padlen)
    z = hilbert(bp, axis=-1)
    return z

def kappa_estimator(z: np.ndarray, sfreq: float, f_center: float) -> float:
    dt = 1.0 / sfreq
    zp = np.gradient(z, dt, axis=-1)
    omega = 2.0 * math.pi * f_center
    num = np.imag(np.vdot(zp, z))     
    den = omega * np.real(np.vdot(z, z)) + 1e-12
    return - float(num / den)

def window_iter(n, w, h):
    for start in range(0, max(1, n - w + 1), h):
        yield start, start + w

def parse_bands(bands_list: List[str], sfreq: float):
    out = []
    nyq = 0.5 * sfreq
    for spec in bands_list:
        name, rng = spec.split(":")
        lo, hi = rng.split("-")
        lo, hi = float(lo), float(hi)
        if hi >= nyq:
            hi = nyq - 1.0
        f_c = (lo + hi) / 2.0
        out.append((name, lo, hi, f_c))
    return out

def process_series(name: str, volts: np.ndarray, sfreq: float, bands, win_s: float, hop_s: float, outdir: Path):
    w = int(round(win_s * sfreq))
    h = int(round(hop_s * sfreq))
    if w < 8:
        raise ValueError("Window too short. Increase --win.")
    results = []
    N = volts.size
    for bname, f_lo, f_hi, f_c in bands:
        for s, e in window_iter(N, w, h):
            seg = volts[s:e]
            if len(seg) < w: continue
            z = analytic_band(seg, sfreq, f_lo, f_hi)
            kap = kappa_estimator(z, sfreq, f_c)
            P = float(np.mean(np.abs(z)**2))
            results.append({"series": name, "start": s, "end": e, "start_s": s/sfreq, "end_s": e/sfreq,
                            "band": bname, "f_lo": f_lo, "f_hi": f_hi, "f_c": f_c,
                            "kappa": kap, "kappa_abs": abs(kap), "power": P})
    if not results:
        return None
    df = pd.DataFrame(results).sort_values(["band","start"])
    out = []
    for bname, g in df.groupby("band", sort=False):
        g = g.copy()
        nwin = max(10, min(50, int(0.05 * g.shape[0])))
        base = g.head(nwin)["power"].median()
        g["delta_power"] = (g["power"] - base) / (base + 1e-12)
        out.append(g)
    dff = pd.concat(out, ignore_index=True)
    outdir.mkdir(parents=True, exist_ok=True)
    csv = outdir / f"{sanitize(name)}_kappa.csv"
    dff.to_csv(csv, index=False)
    return csv

def sanitize(x: str) -> str:
    return re.sub(r'[^A-Za-z0-9_\-]+', '_', x)

def main():
    ap = argparse.ArgumentParser(description="LHD Magnetics_E κ-analysis")
    ap.add_argument("--dat", help="Path to a .dat")
    ap.add_argument("--prm", help="Path to matching .prm")
    ap.add_argument("--stem", help="Stem like 'Magnetics_E-935646-1' to process pairs --pairs a b as ...-a.dat..-b.dat")
    ap.add_argument("--pairs", nargs=2, type=int, help="Start end indices for stem pairs (e.g., 1 20)")
    ap.add_argument("--out", default="plasma_out", help="Output directory")
    ap.add_argument("--win", type=float, default=0.050, help="Window seconds (default 0.050 = 50 ms)")
    ap.add_argument("--hop", type=float, default=0.025, help="Hop seconds (default 0.025 = 25 ms)")
    ap.add_argument("--bands", nargs="+", default=["low:50-300","mid:300-1200","high:1200-4000"]),
    ap.add_argument("--force-raw", action="store_true", help="Treat .dat as raw int16 (skip zlib) even if PRM says ZLIB"),
    ap.add_argument("--force-zlib", action="store_true", help="Force zlib decompress even if heuristics say raw")
    help='Bands like name:lo-hi in Hz; auto-clipped to Nyquist'
    ap.add_argument("--resume", action="store_true")
    args = ap.parse_args()

    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)
    ckpt = outdir / "checkpoint.json"
    state = {"done": []}
    if args.resume and ckpt.exists():
        try:
            state = json.loads(ckpt.read_text())
        except Exception:
            pass

    jobs = []
    if args.dat and args.prm:
        jobs.append((Path(args.dat), Path(args.prm)))
    elif args.stem and args.pairs:
        start, end = args.pairs
        for k in range(start, end+1):
            dat = Path(f"{args.stem}-{k}.dat")
            prm = Path(f"{args.stem}-{k}.prm")
            jobs.append((dat, prm))
    else:
        print("Provide either --dat/--prm OR --stem with --pairs start end")
        sys.exit(2)

    for dat_path, prm_path in jobs:
        if not dat_path.exists() or not prm_path.exists():
            print(f"Skipping (missing): {dat_path} / {prm_path}")
            continue
        key = f"{dat_path.name}"
        if args.resume and key in state["done"]:
            continue
        meta = parse_prm(prm_path)
        try:
            sfreq = derive_sfreq(meta)   # e.g., ClockInterval(uSec)=100 → 10 kHz
        except Exception as e:
            print(f"Cannot derive sfreq for {dat_path.name}: {e}")
            continue
        volts = load_dat(dat_path, meta, force_raw=args.force_raw, force_zlib=args.force_zlib)
        bands = parse_bands(args.bands, sfreq)
        series_name = dat_path.stem
        dest = outdir / "waves"
        dest.mkdir(parents=True, exist_ok=True)
        csv = process_series(series_name, volts, sfreq, bands, args.win, args.hop, dest)
        info = {
            "series": series_name,
            "sfreq": sfreq,
            "n_samples": int(volts.size),
            "duration_s": float(volts.size / sfreq),
            "bands": [{"name": b, "lo": lo, "hi": hi, "center": fc} for (b,lo,hi,fc) in bands],
            "win": args.win, "hop": args.hop,
            "prm": {k: meta[k] for k in ["Shot","SubShot","Samples/Ch","VResolution","VOffset","Range(V)","ClockInterval(uSec)"] if k in meta}
        }
        with open(dest / f"{sanitize(series_name)}_meta.json","w") as f:
            json.dump(info, f, indent=2)
        state["done"].append(key)
        ckpt.write_text(json.dumps(state, indent=2))
        print(f"Done: {dat_path.name} → {csv}")

if __name__ == "__main__":
    main()
