
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Song-of-Scale Unified MiniSEED Analyzer
---------------------------------------
A clean, modernized pipeline to process MiniSEED ecosystems (seismic, LIGO-like, or other MSEED sources)
through the "Song of Scale" protocol:

  - Banding (user-defined or auto-log bands)
  - Windowed ΔP (relative power vs. local baseline)
  - Windowed κ* (helical-gauge curvature of the analytic signal)
  - State archetypes (Weaver, Gladiator, Vortex, Drifter) via quantile thresholds
  - Pirouette epochization & cycle detection (W→G→V→D)
  - Optional triadic phase closure index (TPCI) around f3≈f1+f2

Outputs per session:
  *_sos_windows.csv     # per-window ΔP & |κ*| with band and timing
  *_sos_states.csv      # per-window archetype labels
  *_sos_epochs.csv      # merged sustained-state segments
  *_triads_summary.json # optional triad summaries
  *_manifest.csv        # per-file summary stats

Usage examples:
  python sos_unified_mseed_analyzer.py ./data --auto-bands --min-f 0.1 --max-f 50 --bands-per-decade 6
  python sos_unified_mseed_analyzer.py ./data --bands "0.1-1,1-4,4-8,8-14" --win-ms 50 --hop-ms 25
  python sos_unified_mseed_analyzer.py ./data --triads --triad-span 0.5 --triad-detune 2.0

Notes:
  - Designed to be inventory-agnostic (no remove_response), but you can resample/detrend/taper.
  - Works on heterogeneous collections: low-frequency seismic AND higher-frequency LIGO-like MiniSEED.
  - If your LIGO data is not MiniSEED, convert first (outside this script).
"""
import argparse
import json
import math
import warnings
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional

import numpy as np
import pandas as pd
from scipy import signal

from obspy import read as obspy_read

# -----------------------------
# Utils
# -----------------------------

def find_mseed_files(root: Path, recursive: bool = True) -> List[Path]:
    exts = ('.mseed', '.miniseed', '.msd', '.MSD', '.MSEED')
    if root.is_file() and root.suffix.lower() in exts:
        return [root]
    files = []
    if recursive:
        for p in root.rglob('*'):
            if p.is_file() and p.suffix.lower() in ('.mseed', '.miniseed', '.msd'):
                files.append(p)
    else:
        for p in root.glob('*'):
            if p.is_file() and p.suffix.lower() in ('.mseed', '.miniseed', '.msd'):
                files.append(p)
    return sorted(files)

def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)

# -----------------------------
# Config
# -----------------------------

@dataclass
class SoSConfig:
    # Bands: either explicit list or auto-log generation
    bands: List[Tuple[float, float]]
    win_s: float = 0.050
    hop_s: float = 0.025
    dwell: int = 3
    hysteresis: int = 1
    max_gap: int = 2
    do_triads: bool = False
    triad_span: float = 0.5    # Hz around center for f1/f2
    triad_detune: float = 2.0  # Hz around f3 ≈ f1+f2
    triad_pts_per_hz: int = 10

@dataclass
class PreConfig:
    detrend: bool = True
    taper: float = 0.02  # proportion for cosine taper
    resample_hz: Optional[float] = None  # e.g., 200.0 (None keeps native)

@dataclass
class IOConfig:
    outdir: Path
    session: str = "session"

# -----------------------------
# Song-of-Scale Analyzer
# -----------------------------

class SoSAnalyzer:
    def __init__(self, sos_cfg: SoSConfig, pre_cfg: PreConfig, io_cfg: IOConfig):
        self.sos = sos_cfg
        self.pre = pre_cfg
        self.io = io_cfg

        self.rows_windows: List[Dict[str, Any]] = []
        self.rows_states:  List[Dict[str, Any]] = []
        self.rows_epochs:  List[Dict[str, Any]] = []
        self.triads_out:   List[Dict[str, Any]] = []
        self.manifest:     List[Dict[str, Any]] = []

    # ---------- preprocessing ----------
    def _preprocess_trace(self, tr):
        x = tr.data.astype(np.float64, copy=False)
        fs = float(tr.stats.sampling_rate)

        # detrend/taper
        if self.pre.detrend:
            x = signal.detrend(x, type='linear')
        if self.pre.taper and self.pre.taper > 0:
            n = len(x)
            m = max(1, int(self.pre.taper * n))
            w = np.hanning(2*m)
            win = np.ones(n)
            win[:m] = w[:m]
            win[-m:] = w[-m:]
            x = x * win

        # resample if requested
        if self.pre.resample_hz and abs(self.pre.resample_hz - fs) > 1e-6:
            # rational resample
            g = math.gcd(int(round(self.pre.resample_hz)), int(round(fs)))
            up = int(round(self.pre.resample_hz / g))
            down = int(round(fs / g))
            x = signal.resample_poly(x, up, down)
            fs = float(self.pre.resample_hz)

        return x, fs

    # ---------- core math ----------
    def _bandpass(self, x, fs, f_lo, f_hi, order=4):
        ny = 0.5 * fs
        if f_hi >= ny * 0.999:
            f_hi = ny * 0.999
        if f_lo <= 0:
            f_lo = 0.001
        b, a = signal.butter(order, [f_lo/ny, f_hi/ny], btype='band')
        return signal.filtfilt(b, a, x)

    def _windows(self, N, fs, win_s, hop_s):
        w = max(1, int(round(win_s * fs)))
        h = max(1, int(round(hop_s * fs)))
        idx = []
        for start in range(0, max(1, N - w + 1), h):
            idx.append((start, start + w))
        return idx

    def _kappa_deltaP_rows(self, x_band, fs, win_s, hop_s, f_center):
        # analytic signal and derivatives
        z = signal.hilbert(x_band)
        dz = np.gradient(z) * fs
        P = np.abs(z) ** 2

        wins = self._windows(len(x_band), fs, win_s, hop_s)
        if not wins:
            return []

        # baseline P0 = median of first 5% windows
        k0 = max(1, int(0.05 * len(wins)))
        P0 = np.median([np.mean(P[s:e]) for (s, e) in wins[:k0]]) + 1e-12

        rows = []
        denom_eps = 1e-12
        for (s, e) in wins:
            re = np.real(np.vdot(z[s:e], z[s:e]))
            im = np.imag(np.vdot(dz[s:e], z[s:e]))
            kappa_star = - im / (2 * np.pi * f_center * (re + denom_eps) + denom_eps)
            P_win = float(np.mean(P[s:e]))
            dP = (P_win - P0) / (P0)
            t0 = s / fs
            t1 = e / fs
            rows.append((t0, t1, float(abs(kappa_star)), float(dP)))
        return rows

    def _label_states(self, rows):
        if not rows:
            return []
        kappa_mag = np.array([r[2] for r in rows])
        dP = np.array([r[3] for r in rows])
        th_l = np.quantile(kappa_mag, 0.65)
        th_h = np.quantile(kappa_mag, 0.85)
        th_P = np.quantile(dP, 0.60)

        out = []
        for (t0, t1, kmag, dp) in rows:
            if dp >= th_P and th_l <= kmag < th_h:
                lab = "Weaver"
            elif dp >= th_P and kmag >= th_h:
                lab = "Gladiator"
            elif dp < 0 and kmag >= th_h:
                lab = "Vortex"
            else:
                lab = "Drifter"
            out.append((t0, t1, lab))
        return out

    def _epochize(self, labels, dwell=3, hysteresis=1):
        if not labels:
            return [], []
        segs = []
        cur_lab, cur_start = labels[0][2], labels[0][0]
        run = 1
        for i in range(1, len(labels)):
            _, _, lab = labels[i]
            if lab == cur_lab or run < hysteresis:
                run += 1
                continue
            if run >= dwell:
                segs.append((cur_start, labels[i-1][1], cur_lab))
            cur_lab, cur_start, run = lab, labels[i][0], 1
        segs.append((cur_start, labels[-1][1], cur_lab))

        # cycles = sequences of three forward states in W→G→V→D order
        order = ["Weaver","Gladiator","Vortex","Drifter"]
        def next_ok(a,b): return (order.index(b) - order.index(a)) % 4 == 1
        cycles = []
        i = 0
        while i < len(segs)-2:
            s1, s2, s3 = segs[i], segs[i+1], segs[i+2]
            if next_ok(s1[2], s2[2]) and next_ok(s2[2], s3[2]):
                cycles.append((s1[0], s3[1], {s1[2], s2[2], s3[2]}))
                i += 3
            else:
                i += 1
        return segs, cycles

    def _tpci(self, x_band, fs, f_pairs, detune_hz=2.0, pts_per_hz=10):
        out = []
        def phaser(f):
            bw = max(0.5, min(5.0, f * 0.2))  # simple adaptive bandwidth
            flo = max(0.1, f - bw/2)
            fhi = f + bw/2
            y = self._bandpass(x_band, fs, flo, fhi)
            z = signal.hilbert(y)
            return np.unwrap(np.angle(z))

        for (f1, f2) in f_pairs:
            f3_0 = f1 + f2
            grid = np.linspace(f3_0 - detune_hz, f3_0 + detune_hz, int(2 * detune_hz * pts_per_hz) + 1)
            vals = []
            for f3 in grid:
                phi1, phi2, phi3 = phaser(f1), phaser(f2), phaser(f3)
                L = min(len(phi1), len(phi2), len(phi3))
                val = np.abs(np.mean(np.exp(1j * (phi3[:L] - phi1[:L] - phi2[:L]))))
                vals.append(val)
            vals = np.array(vals)
            peak = float(np.max(vals))
            half = peak / 2.0
            idx_peak = int(np.argmax(vals))
            # estimate half bandwidth
            # left
            left = idx_peak
            while left > 0 and vals[left] >= half:
                left -= 1
            # right
            right = idx_peak
            n = len(vals) - 1
            while right < n and vals[right] >= half:
                right += 1
            half_bw_hz = (right - left) / pts_per_hz
            out.append({"f1": f1, "f2": f2, "peak": peak, "half_bw_hz": float(half_bw_hz)})
        return out

    # ---------- main processing ----------
    def process_file(self, path: Path):
        try:
            st = obspy_read(str(path), format="MSEED")
        except Exception as e:
            warnings.warn(f"Failed to read {path}: {e}")
            return

        file_rows = 0
        for tr in st:
            try:
                x, fs = self._preprocess_trace(tr)
            except Exception as e:
                warnings.warn(f"Preprocess fail {path} {tr.id}: {e}")
                continue

            # For each band
            for (blo, bhi) in self.sos.bands:
                if blo >= bhi:
                    continue
                if bhi >= 0.5 * fs * 0.999:
                    # skip bands beyond Nyquist
                    continue

                try:
                    xb = self._bandpass(x, fs, blo, bhi)
                    f_center = 0.5 * (blo + bhi)
                    rows = self._kappa_deltaP_rows(xb, fs, self.sos.win_s, self.sos.hop_s, f_center)
                except Exception as e:
                    warnings.warn(f"Bandpass/κΔP fail {path} {tr.id} [{blo}-{bhi}Hz]: {e}")
                    continue

                # store windows
                for (t0, t1, kmag, dP) in rows:
                    self.rows_windows.append({
                        "file": str(path), "trace": tr.id, "network": tr.stats.network,
                        "station": tr.stats.station, "location": tr.stats.location,
                        "channel": tr.stats.channel, "fs": fs,
                        "band_lo": blo, "band_hi": bhi, "t0": t0, "t1": t1,
                        "kappa_mag": kmag, "deltaP": dP
                    })
                file_rows += len(rows)

                # labels
                try:
                    labels = self._label_states(rows)
                except Exception as e:
                    warnings.warn(f"Label fail {path} {tr.id} [{blo}-{bhi}Hz]: {e}")
                    labels = []

                for (t0, t1, lab) in labels:
                    self.rows_states.append({
                        "file": str(path), "trace": tr.id, "network": tr.stats.network,
                        "station": tr.stats.station, "location": tr.stats.location,
                        "channel": tr.stats.channel, "fs": fs,
                        "band_lo": blo, "band_hi": bhi, "t0": t0, "t1": t1,
                        "state": lab
                    })

                # epochization
                try:
                    segs, cycles = self._epochize(labels, dwell=self.sos.dwell, hysteresis=self.sos.hysteresis)
                except Exception as e:
                    warnings.warn(f"Epochize fail {path} {tr.id} [{blo}-{bhi}Hz]: {e}")
                    segs, cycles = [], []

                for (t0, t1, lab) in segs:
                    self.rows_epochs.append({
                        "file": str(path), "trace": tr.id, "network": tr.stats.network,
                        "station": tr.stats.station, "location": tr.stats.location,
                        "channel": tr.stats.channel, "fs": fs,
                        "band_lo": blo, "band_hi": bhi, "t0": t0, "t1": t1,
                        "state": lab
                    })

                # triads (optional): use a simple pair near band center
                if self.sos.do_triads:
                    span = max(0.25, min((bhi - blo) / 3.0, self.sos.triad_span))
                    f_pairs = [(max(blo+1e-3, f_center - span), min(bhi-1e-3, f_center + span/2))]
                    try:
                        triads = self._tpci(xb, fs, f_pairs,
                                            detune_hz=self.sos.triad_detune,
                                            pts_per_hz=self.sos.triad_pts_per_hz)
                        for td in triads:
                            td.update({
                                "file": str(path), "trace": tr.id,
                                "network": tr.stats.network, "station": tr.stats.station,
                                "location": tr.stats.location, "channel": tr.stats.channel,
                                "fs": fs, "band_lo": blo, "band_hi": bhi
                            })
                            self.triads_out.append(td)
                    except Exception as e:
                        warnings.warn(f"TPCI fail {path} {tr.id} [{blo}-{bhi}Hz]: {e}")
                        continue

        # manifest record
        self.manifest.append({
            "file": str(path), "rows": file_rows, "traces": len(st)
        })

    # ---------- saving ----------
    def save(self):
        ensure_dir(self.io.outdir)
        base = self.io.outdir / self.io.session

        if self.rows_windows:
            pd.DataFrame(self.rows_windows).to_csv(str(base) + "_sos_windows.csv", index=False)
        if self.rows_states:
            pd.DataFrame(self.rows_states).to_csv(str(base) + "_sos_states.csv", index=False)
        if self.rows_epochs:
            pd.DataFrame(self.rows_epochs).to_csv(str(base) + "_sos_epochs.csv", index=False)
        if self.triads_out:
            with open(str(base) + "_triads_summary.json", "w") as f:
                json.dump(self.triads_out, f, indent=2)
        if self.manifest:
            pd.DataFrame(self.manifest).to_csv(str(base) + "_manifest.csv", index=False)

# -----------------------------
# Bands helpers
# -----------------------------

def parse_bands(bands_str: str) -> List[Tuple[float, float]]:
    out = []
    for chunk in bands_str.split(","):
        lo, hi = chunk.strip().split("-")
        out.append((float(lo), float(hi)))
    return out

def auto_log_bands(fmin: float, fmax: float, per_decade: int) -> List[Tuple[float, float]]:
    if fmin <= 0 or fmax <= fmin:
        raise ValueError("Auto bands require 0 < fmin < fmax")
    # compute logarithmic edges
    decades = math.log10(fmax) - math.log10(fmin)
    n_bins = max(1, int(math.ceil(decades * per_decade)))
    edges = np.logspace(math.log10(fmin), math.log10(fmax), n_bins + 1)
    bands = [(float(edges[i]), float(edges[i+1])) for i in range(n_bins)]
    # merge tiny last band if almost zero-width
    merged = []
    for lo, hi in bands:
        if merged and (hi - lo) < 1e-6:
            mlo, mhi = merged.pop()
            merged.append((mlo, hi))
        else:
            merged.append((lo, hi))
    return merged

# -----------------------------
# CLI
# -----------------------------

def build_argparser():
    p = argparse.ArgumentParser(
        description="Song-of-Scale unified MiniSEED analyzer (seismic & LIGO-like)"
    )
    p.add_argument("path", type=str, help="Path to MiniSEED file or directory")
    p.add_argument("--recursive", action="store_true", help="Recurse into subdirectories")
    p.add_argument("--outdir", type=str, default="./sos_out", help="Output directory")
    p.add_argument("--session", type=str, default="session", help="Session name for outputs")

    # Bands
    g = p.add_argument_group("Bands")
    g.add_argument("--bands", type=str, default=None,
                   help="Explicit bands 'lo1-hi1,lo2-hi2,...' in Hz")
    g.add_argument("--auto-bands", action="store_true", help="Use logarithmic auto-bands")
    g.add_argument("--min-f", type=float, default=0.1, help="Auto-bands minimum frequency (Hz)")
    g.add_argument("--max-f", type=float, default=50.0, help="Auto-bands maximum frequency (Hz)")
    g.add_argument("--bands-per-decade", type=int, default=6,
                   help="Number of bands per decade for auto-bands")

    # Windows
    w = p.add_argument_group("Windows")
    w.add_argument("--win-ms", type=float, default=50.0, help="Window length in milliseconds")
    w.add_argument("--hop-ms", type=float, default=25.0, help="Hop length in milliseconds")

    # Epochization
    e = p.add_argument_group("Epochization")
    e.add_argument("--dwell", type=int, default=3, help="Dwell windows")
    e.add_argument("--hysteresis", type=int, default=1, help="Hysteresis windows")
    e.add_argument("--max-gap", type=int, default=2, help="(reserved) max gap windows")

    # Triads
    t = p.add_argument_group("Triads (optional)")
    t.add_argument("--triads", action="store_true", help="Compute TPCI triads")
    t.add_argument("--triad-span", type=float, default=0.5, help="Hz span around band center")
    t.add_argument("--triad-detune", type=float, default=2.0, help="Hz detune around f3≈f1+f2")
    t.add_argument("--triad-pph", type=int, default=10, help="TPCl samples per Hz")

    # Preprocessing
    pr = p.add_argument_group("Preprocessing")
    pr.add_argument("--no-detrend", action="store_true", help="Disable linear detrend")
    pr.add_argument("--taper", type=float, default=0.02, help="Cosine taper proportion (0-0.25)")
    pr.add_argument("--resample", type=float, default=None, help="Resample to Hz (None keeps native)")

    return p

def main():
    args = build_argparser().parse_args()
    root = Path(args.path)
    outdir = Path(args.outdir)
    ensure_dir(outdir)

    # Bands resolution
    if args.auto_bands:
        bands = auto_log_bands(args.min_f, args.max_f, args.bands_per_decade)
    elif args.bands:
        bands = parse_bands(args.bands)
    else:
        # sensible cross-domain defaults (log mix covering ~0.1–64 Hz)
        bands = [(0.1, 0.3),(0.3, 1.0),(1.0, 3.0),(3.0, 8.0),
                 (8.0, 14.0),(14.0, 24.0),(24.0, 44.0),(44.0, 64.0)]

    sos_cfg = SoSConfig(
        bands=bands,
        win_s=float(args.win_ms)/1000.0,
        hop_s=float(args.hop_ms)/1000.0,
        dwell=int(args.dwell),
        hysteresis=int(args.hysteresis),
        max_gap=int(args.max_gap),
        do_triads=bool(args.triads),
        triad_span=float(args.triad_span),
        triad_detune=float(args.triad_detune),
        triad_pts_per_hz=int(args.triad_pph),
    )
    pre_cfg = PreConfig(
        detrend=not args.no_detrend,
        taper=max(0.0, min(0.25, float(args.taper))),
        resample_hz=float(args.resample) if args.resample else None
    )
    io_cfg = IOConfig(outdir=outdir, session=args.session)

    analyzer = SoSAnalyzer(sos_cfg=sos_cfg, pre_cfg=pre_cfg, io_cfg=io_cfg)

    files = find_mseed_files(root, recursive=args.recursive)
    if not files:
        print(f"No MiniSEED files found in {root}")
        return

    print(f"Found {len(files)} file(s). Processing...")
    for f in files:
        print(f" - {f}")
        analyzer.process_file(f)

    analyzer.save()
    print(f"Done. Outputs in: {outdir}")

if __name__ == "__main__":
    main()
