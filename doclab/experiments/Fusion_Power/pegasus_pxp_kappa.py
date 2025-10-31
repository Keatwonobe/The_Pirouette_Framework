#!/usr/bin/env python
"""
pegasus_pxp_kappa.py

Parse PEGASUS tokamak data saved in Igor Pro formats (.pxp project and/or .ibw waves),
extract time-series waves, and compute helical κ metrics per window.

Usage
-----
# List contents (waves) in a .pxp or a folder of .ibw
python pegasus_pxp_kappa.py --input "DS2018-4.pxp" --list

# Process all waves whose names match a regex (e.g., magnetic probes), write CSVs
python pegasus_pxp_kappa.py --input "DS2018-4.pxp" --select "^(B_|BP_|Mag)" --sfreq 100000 --out outpeg --resume

# Process a folder containing many .ibw files (exported from Igor: Data→Save Waves)
python pegasus_pxp_kappa.py --input "C:\\data\\pegasus_ibw" --select "^(B_|BP_)" --sfreq 100000 --out outpeg --resume

Notes
-----
- For .pxp, this uses `igor2`'s packed file loader. If your .pxp variant is not
  fully supported, export the waves you need from Igor to .ibw and point this
  script at the folder; .ibw is robustly supported.
- Sampling frequency (--sfreq) is required if not encoded in the wave's scale.
  If waves have a time scaling in the Igor header, we try to infer sfreq.
- We compute per-window analytic signal (IIR band-pass + Hilbert) and the helical
  κ estimator: κ* = -Im<z',z> / (ω <z,z>) for user-defined bands.

Dependencies
------------
pip install igor2 numpy scipy pandas

"""
import argparse, re, json, os, sys, math, warnings
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import numpy as np
import pandas as pd
from scipy.signal import butter, sosfiltfilt, hilbert

# Optional import: igor2
# Optional import: igor2 (may be installed as "igor2" instead of "igor")
try:
    from igor import binarywave as igor_bw
    from igor import packed as igor_packed
except ImportError:
    try:
        from igor2 import binarywave as igor_bw
        from igor2 import packed as igor_packed
    except Exception:
        igor_bw = None
        igor_packed = None


# ---------------------------- Helical tools ----------------------------- #
BANDS = {
    "low":  (1e3,  5e3,  3e3),   # example bands for tokamak fast data; edit to taste
    "mid":  (5e3,  20e3, 12e3),
    "high": (20e3, 80e3, 40e3),
}

def butter_bandpass_iir(low, high, fs, order=4):
    nyq = 0.5 * fs
    wp = [low/nyq, high/nyq]
    return butter(order, wp, btype='bandpass', output='sos')

def analytic_band_epoch(x: np.ndarray, sfreq: float, f_lo: float, f_hi: float) -> np.ndarray:
    """IIR (SOS) band-pass + Hilbert, zero-phase via filtfilt"""
    sos = butter_bandpass_iir(f_lo, f_hi, sfreq, order=4)
    padlen = min(3 * int(sfreq // 2), max(0, len(x)//2))
    bp = sosfiltfilt(sos, x, axis=-1, padlen=padlen)
    z = hilbert(bp, axis=-1)
    return z

def kappa_estimator(z: np.ndarray, sfreq: float, f_center: float) -> float:
    """Return scalar κ* on this window (single channel)."""
    dt = 1.0 / sfreq
    zp = np.gradient(z, dt, axis=-1)
    omega = 2.0 * math.pi * f_center
    # <z', z> over time
    num = np.imag(np.vdot(zp, z))          # Im <z', z>
    den = omega * np.real(np.vdot(z, z)) + 1e-12
    return - float(num / den)

def window_iter(x: np.ndarray, sfreq: float, win_s: float, hop_s: float):
    L = len(x)
    w = int(round(win_s * sfreq))
    h = int(round(hop_s * sfreq))
    for start in range(0, max(1, L - w + 1), h):
        yield start, start + w

# ---------------------------- Igor readers ------------------------------ #
def read_ibw(path: Path) -> Dict:
    if igor_bw is None:
        raise RuntimeError("igor2 not installed. pip install igor2")
    d = igor_bw.load(str(path))
    # d['wave']['wData'] is the ndarray, d['wave']['wave_header'] has scaling
    x = np.array(d['wave']['wData']).astype(float).squeeze()
    meta = d.get('wave', {}).get('wave_header', {})
    return {"name": path.stem, "data": x, "meta": meta}

def infer_sfreq_from_header(meta: Dict) -> Optional[float]:
    # Igor wave header often encodes x scaling as sfA + sfB * idx
    # sfA is starting x, sfB is dx; if dx > 0, sfreq = 1/dx
    dx = None
    for key in ('sfB', 'hsB', 'xScaleDelta'):
        if key in meta:
            try:
                dx = float(meta[key])
                break
            except Exception:
                continue
    if dx and dx > 0:
        return 1.0 / dx
    return None

def list_pxp_contents(path: Path) -> List[str]:
    """Return human-readable names of waves we can find in a PXP."""
    if igor_packed is None:
        raise RuntimeError("igor2 not installed. pip install igor2")
    with open(path, 'rb') as f:
        obj = igor_packed.load(f)
    names = []
    def visit(node, prefix="root"):
        if isinstance(node, dict):
            for k, v in node.items():
                visit(v, f"{prefix}/{k}")
        elif isinstance(node, list):
            for i, v in enumerate(node):
                visit(v, f"{prefix}[{i}]")
        else:
            try:
                t = getattr(node, "type", None)
                nm = getattr(node, "name", None)
                if t and "WAVE" in str(t).upper() and nm:
                    names.append(f"{prefix}/{nm}")
            except Exception:
                pass
    visit(obj)
    return sorted(set(names))

def extract_pxp_waves(path: Path):
    """Best-effort extraction of waves from a PXP. If unsupported, advise IBW export."""
    if igor_packed is None:
        raise RuntimeError("igor2 not installed. pip install igor2")
    with open(path, 'rb') as f:
        obj = igor_packed.load(f)

    waves = []
    def visit(node, prefix="root"):
        if isinstance(node, dict):
            if 'wave' in node and isinstance(node['wave'], dict) and 'wData' in node['wave']:
                data = np.array(node['wave']['wData']).astype(float).squeeze()
                meta = node['wave'].get('wave_header', {})
                nm = node.get('name', f"{prefix}/wave")
                waves.append((str(nm), data, meta))
            else:
                for k, v in node.items():
                    visit(v, f"{prefix}/{k}")
        elif isinstance(node, list):
            for i, v in enumerate(node):
                visit(v, f"{prefix}[{i}]")
        else:
            for attr in ('wave', 'data', 'payload'):
                try:
                    maybe = getattr(node, attr, None)
                    if isinstance(maybe, dict) and 'wData' in maybe:
                        data = np.array(maybe['wData']).astype(float).squeeze()
                        meta = maybe.get('wave_header', {})
                        nm = getattr(node, 'name', f"{prefix}/{attr}")
                        waves.append((str(nm), data, meta))
                        break
                except Exception:
                    continue
    visit(obj)
    dedup = {}
    for nm, data, meta in waves:
        if nm not in dedup:
            dedup[nm] = (data, meta)
    for nm, (data, meta) in dedup.items():
        yield nm, data, meta

# -------------------------- Processing core ----------------------------- #
def process_wave(name: str, x: np.ndarray, sfreq: float, outdir: Path,
                 win_s: float=0.020, hop_s: float=0.010):
    """
    Compute κ and Δpower per band over sliding windows of a single time-series wave.
    Save a CSV with per-window metrics and a small JSON with metadata.
    """
    rows = []
    for bname, (f_lo, f_hi, f_c) in BANDS.items():
        for s, e in window_iter(x, sfreq, win_s, hop_s):
            seg = x[s:e]
            if len(seg) < max(16, int(0.5*sfreq)):
                continue
            z = analytic_band_epoch(seg, sfreq, f_lo, f_hi)
            kap = kappa_estimator(z, sfreq, f_c)
            P = float(np.mean(np.abs(z)**2))
            rows.append({"wave": name, "band": bname, "start": s, "end": e,
                         "kappa": kap, "kappa_abs": abs(kap), "power": P})

    if not rows:
        return None

    df = pd.DataFrame(rows).sort_values(["band","start"])
    out = []
    for bname, g in df.groupby("band", sort=False):
        g = g.copy()
        baseline = g.head(50)["power"].median() if len(g) >= 50 else g["power"].median()
        g["delta_power"] = (g["power"] - baseline) / (baseline + 1e-12)
        out.append(g)
    dff = pd.concat(out, ignore_index=True)

    outdir.mkdir(parents=True, exist_ok=True)
    csv_path = outdir / f"{sanitize(name)}_kappa.csv"
    dff.to_csv(csv_path, index=False)

    meta = {"wave": name, "sfreq": sfreq, "win_s": win_s, "hop_s": hop_s, "bands": BANDS}
    with open(outdir / f"{sanitize(name)}_meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    return csv_path

def sanitize(name: str) -> str:
    return re.sub(r'[^A-Za-z0-9_\-]+', '_', name)

# ------------------------------ CLI ------------------------------------ #
def main():
    ap = argparse.ArgumentParser(description="PEGASUS Igor (.pxp/.ibw) → helical κ metrics")
    ap.add_argument("--input", required=True, help="Path to .pxp file or directory with .ibw files")
    ap.add_argument("--select", default=".*", help="Regex to select wave names (default: all)")
    ap.add_argument("--sfreq", type=float, default=None, help="Sampling frequency in Hz (fallback if not inferable)")
    ap.add_argument("--list", action="store_true", help="List waves and exit")
    ap.add_argument("--out", default="pegasus_out", help="Output directory")
    ap.add_argument("--win", type=float, default=0.020, help="Window length seconds (default 20 ms)")
    ap.add_argument("--hop", type=float, default=0.010, help="Hop seconds (default 10 ms)")
    ap.add_argument("--resume", action="store_true", help="Skip waves already processed")
    args = ap.parse_args()

    in_path = Path(args.input)
    outdir = Path(args.out)
    pat = re.compile(args.select)

    if not in_path.exists():
        raise SystemExit(f"Input not found: {in_path}")

    if in_path.is_file():
        if in_path.suffix.lower() == ".pxp":
            if args.list:
                names = list_pxp_contents(in_path)
                if not names:
                    print("No wave names discovered. If this persists, export to .ibw from Igor and retry.")
                else:
                    print("\n".join(names))
                return
            waves = list(extract_pxp_waves(in_path))
            if not waves:
                raise SystemExit("Could not extract waves from PXP. Export to .ibw and point --input to that folder.")
            dest = outdir / "waves"
            dest.mkdir(parents=True, exist_ok=True)
            for nm, data, meta in waves:
                if not pat.search(nm):
                    continue
                # infer sfreq if possible
                sf = infer_sfreq_from_header(meta) or args.sfreq
                if not sf:
                    warnings.warn(f"No sampling frequency for wave {nm}; please pass --sfreq")
                    continue
                csv_path = dest / f"{sanitize(nm)}_kappa.csv"
                if args.resume and csv_path.exists():
                    continue
                print(f"[PXP] Processing wave: {nm} (sfreq={sf})")
                process_wave(nm, data.astype(float), sf, dest, args.win, args.hop)
        else:
            # Single IBW file
            d = read_ibw(in_path)
            nm, x, meta = d["name"], d["data"], d["meta"]
            if args.list:
                print(nm)
                return
            if not pat.search(nm):
                print("No selected wave matched.")
                return
            sf = infer_sfreq_from_header(meta) or args.sfreq
            if not sf:
                raise SystemExit("Sampling frequency unknown; pass --sfreq")
            dest = outdir / "waves"
            dest.mkdir(parents=True, exist_ok=True)
            print(f"[IBW] Processing wave: {nm} (sfreq={sf})")
            process_wave(nm, x.astype(float), sf, dest, args.win, args.hop)

    elif in_path.is_dir():
        # Folder of IBW
        ibws = sorted(in_path.glob("*.ibw"))
        if args.list:
            for p in ibws:
                print(p.name)
            return
        dest = outdir / "waves"
        dest.mkdir(parents=True, exist_ok=True)
        for p in ibws:
            d = read_ibw(p)
            nm, x, meta = d["name"], d["data"], d["meta"]
            if not pat.search(nm):
                continue
            sf = infer_sfreq_from_header(meta) or args.sfreq
            if not sf:
                warnings.warn(f"No sampling frequency for wave {nm}; skipping (pass --sfreq)")
                continue
            csv_path = dest / f"{sanitize(nm)}_kappa.csv"
            if args.resume and csv_path.exists():
                continue
            print(f"[IBW] Processing wave: {nm} (sfreq={sf})")
            process_wave(nm, x.astype(float), sf, dest, args.win, args.hop)
    else:
        raise SystemExit("Unsupported input type")

if __name__ == "__main__":
    main()
