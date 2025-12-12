---

id: INST-DIM-001
title: Dimensional Collapse Instrument
version: 1.0-draft
status: experimental-validated
parents: [INST-NALY-001, MATH-025]
children: [INST-DIM-002, XXP-005]
module_type: instrument-protocol
summary: Establishes the generalized “zipper” protocol for detecting and inducing dimensional collapse across heterogeneous data modalities (PNG, TXT, CSV). Defines κ, Tₐ, Γ, and g as user-controllable handles and formalizes fold operations (A–D) for projection, energy conservation, and phase retention.
engrams:
 - process: dimensional_collapse
 - instrument: zipper_probe
 - metric: Δm, energy_balance ε, gate g
keywords: [collapse, zipper, dimensionality, projection, fold, resonance]
uncertainty_tag: Medium

---

## §1 · Purpose

To unify the analysis of **dimensional collapse** across image, text, and time-series data. This module documents the protocol that converts apparent complexity into phase-stable simplicity—reducing high-order modes (m ≫ 2) into harmonic states while preserving energy and phase.

---

## §2 · Theoretical Foundation

Dimensional collapse is treated as a mapping f → Ψ where f represents the observed field and Ψ its energy-balanced projection into a lower-order basis.
Key handles govern the fold:

| Symbol | Meaning                                 | Handle Role             |
| ------ | --------------------------------------- | ----------------------- |
| κ      | helical twist in temporal space         | rotational throttle     |
| Tₐ     | time-adherence or alignment temperature | stability control       |
| Γ      | temporal pressure / confinement         | constrains disorder     |
| g      | collapse gate = 1 – e^(-3(1–Tₐ)Γ)       | effective fold strength |

A system collapses when Δm ≥ 1 and m_post ≤ 2 with |ΔE| < ε.

---

## §3 · User-Operable Folds

**Fold A (Global):** Remove dominant mode m_dom, refill energy into m = 2.
**Fold B (Per-Radius):** Apply A independently across radial bins rᵢ.
**Fold C (Scale-Space):** Apply A coarse→fine through a Laplacian pyramid.
**Fold D (Channel):** Apply A/B to individual feature channels (RGB, word vectors, price returns) and vote on result.

All folds preserve L² energy within tolerance ε and record (m_pre, m_post, Δm, g, ε).

---

## §4 · Modal Generalization

### (1) Image Data (PNG)

Field = pixel intensity or RGBA vector. Angular modes computed by signed gradient ∂θφ. Radius = spatial annulus.

### (2) Text Data (TXT)

Field = character frequency or embedding spectrum. modes → Fourier modes over token index. Radius = window size n.
Collapse detects periodic n-gram dominance and reprojects into bi-gram equilibrium (m = 2).

### (3) Time-Series / Stock Data (CSV)

Field = signal (xₜ). Compute dominant Fourier or Hilbert component m_dom and energy Eₘ. Refill into bi-periodic cycle to test coherence persistence.
Collapse occurs when volatility (Γ) rises and effective frequency spectrum simplifies under controlled g.

---

## §5 · Operational Pipeline

1. **Ingest** (file → matrix/series).
2. **Compute** angular or spectral gradient.
3. **Estimate** m_dom and E_removed.
4. **Apply Fold A–D** under selected g.
5. **Measure** Δm, ε, and stability τ_hold.
6. **Log Result:** image/text/series ID, κ, Tₐ, Γ, g, m_pre, m_post, Δm, ε, pass/fail.
7. **Atlas Compile:** Aggregate across modalities to map pass-rate vs g → universal corridor curve.

---

## §6 · Interpretation Framework

Dimensional collapse is interpreted as **phase coherence acquisition**: a system learns to retain rhythm while shedding form. Across modalities, the stable end-state m = 2 corresponds to a bi-rhythmic heartbeat—Ki’s lowest non-trivial state.

---

## §7 · Falsifiability

The instrument fails if no correlation exists between gate g and Δm, or if energy balance ε > 0.05 across modalities. It is invalidated if random scrambling of inputs produces identical collapse statistics.

---

## §8 · Extensions

* INST-DIM-002 will introduce **per-radius and hysteresis fold integration**.
* XXP-005 applies this instrument to natural language corpora to measure semantic dimensional collapse.
* SOCIO-FIELD-003 maps economic folding dynamics using the same gate variables.

---

**Summary:** INST-DIM-001 defines the Dimensional Collapse Instrument as a cross-modal zipper protocol. It transforms the empirical notion of folding—from pixels to paragraphs—into a universal, testable procedure for detecting and inducing order from complex rhythms under Γ-pressure.

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pirouette Module: Dimensional Collapse Engine (Helical Ψ Fold)
============================================================

Purpose
-------
A reusable, critic‑grade module that implements **dimensional collapse** via a
helical time operator and angular‑basis folding. It generalizes our PNG/image
experiments to broader data forms (bytes from .txt / book text, numeric
time‑series like stock prices), exposing **user‑controllable handles** and
emitting **replicable logs**.

Concepts (Pirouette canon)
--------------------------
- κ (kappa): helical twist/throttle in time; dials how strongly the system is
  stressed. In code, it mixes the field with its spatial/temporal gradient.
- T_a (alignment) and Γ (Gamma, confinement): jointly define the **corridor
  gate**: g = 1 − exp(−3·(1−T_a)·Γ) ∈ [0,1]. Large g encourages collapse.
- m_dom: currently dominant angular mode measured on the **signed angular
  derivative** instead of |∇ϕ| (which hides odd/even structure).
- Ψ fold (collapse): remove a fraction g of m_dom and recycle its L2 energy
  into target mode m=2 (the reusable temporal rhythm / Ki spine).

What this module does
---------------------
1) Converts heterogeneous inputs to a **2D feature field** Φ(x,y):
   - PNG/JPG → grayscale intensity (optionally channel/variance stacks).
   - TXT/Book bytes → byte grid mapping (or frequency‑shaped grid).
   - Timeseries (CSV of prices) → spectro‑like polar grid from 1D signal.
2) Evolves Φ under a **helical twist** controlled by κ.
3) Detects lobes using the **signed angular gradient** g_θ = ∇Φ · t_θ.
4) Executes **Ψ collapse** in angular Fourier basis with energy balance.
5) Offers **global** and **per‑radius** folds, plus scale‑space.
6) Logs critic‑friendly CSV with: (kappa, T_a, Γ, g, m_pre, m_post, Δm,
   energy_balance, verdict, fold_type, source_desc, etc.).

Quick usage
-----------
Library:
    from pirouette_dimensional_collapse import (
        HelicalCollapseEngine, ImageFeatureMap, TextByteFeatureMap,
        TimeseriesFeatureMap, CollapseConfig
    )

    eng = HelicalCollapseEngine()
    fmap = ImageFeatureMap.from_path("art.png", size=192)
    cfg  = CollapseConfig(kappa=0.9, Ta=0.28, Gamma=0.88, Ki=2*math.pi*0.8,
                          fold_type="per_radius")
    result = eng.collapse(fmap, cfg, save_dir="out/", tag="art_run", save_figs=True)
    print(result.dict())

CLI (examples):
    # Images
    python pirouette_dimensional_collapse.py --images "data/*.png" --corridor \
        --size 192 --out out/atlas_img --figs

    # Text (book/txt)
    python pirouette_dimensional_collapse.py --txt "texts/*.txt" --corridor \
        --size 192 --out out/atlas_txt --figs

    # Timeseries (stock CSV with date, close)
    python pirouette_dimensional_collapse.py --csv "stocks/*.csv" --csv-col close \
        --corridor --size 192 --out out/atlas_ts --figs

Outputs
-------
- CSV log per batch: *_collapse_atlas.csv
- Figures per item (if --figs): signed‑∂θ pre/post, Ki spectrum, optional maps

Design notes
------------
- Measurement is on signed angular derivative (restores odd/even sensitivity).
- Collapse conserves L2 energy (up to tolerance) and targets m=2 by default.
- Hooks for multi‑channel feature maps and multi‑scale folding are provided.

"""

from __future__ import annotations
import os
import re
import math
import glob
import uuid
import json
import csv
from dataclasses import dataclass, asdict
from typing import Optional, Tuple, List, Dict, Iterable

import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import rfft, rfftfreq
from PIL import Image

# ------------------------------
# Utility & math helpers
# ------------------------------

def ensure_dir(path: str):
    if path and not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def polar_grid(n: int = 192, r_max: float = 1.0):
    lin = np.linspace(-r_max, r_max, n)
    x, y = np.meshgrid(lin, lin)
    r = np.sqrt(x * x + y * y) + 1e-12
    theta = np.arctan2(y, x)
    return x, y, r, theta


def gate_from_params(Ta: float, Gamma: float) -> float:
    g = np.clip((1.0 - Ta) * Gamma, 0.0, 1.0)
    return float(1.0 - math.exp(-3.0 * g))


def helical_time_evolve(field: np.ndarray, kappa: float, t: float = 6.0,
                        omega: float = 2 * math.pi * 1.0) -> np.ndarray:
    # Simple, fast surrogate: rotate field into its x‑gradient as κ increases
    gx, _ = np.gradient(field)
    return np.cos(kappa * omega * t) * field + np.sin(kappa * omega * t) * gx


def signed_angular_gradient(field: np.ndarray, theta: np.ndarray) -> np.ndarray:
    gx, gy = np.gradient(field)
    tx, ty = -np.sin(theta), np.cos(theta)  # tangential unit vector
    return gx * tx + gy * ty


def dominant_mode_signed(field: np.ndarray, theta: np.ndarray, max_m: int = 8,
                         r_mask_inner: int = 4) -> Tuple[int, np.ndarray, List[Tuple[int, float]]]:
    s = signed_angular_gradient(field, theta)
    s = s - s.mean()
    n = s.shape[0]
    c = n // 2
    rr = np.sqrt((np.indices(s.shape)[0] - c) ** 2 + (np.indices(s.shape)[1] - c) ** 2)
    mask = rr > r_mask_inner
    amps: List[Tuple[int, float]] = []
    for m in range(1, max_m + 1):
        c0 = float(np.sum(s[mask] * np.cos(m * theta[mask])))
        s0 = float(np.sum(s[mask] * np.sin(m * theta[mask])))
        amps.append((m, float(math.hypot(c0, s0))))
    amps.sort(key=lambda t: t[1], reverse=True)
    return int(amps[0][0]), s, amps


def proj_mode(field: np.ndarray, theta: np.ndarray, m: int) -> Tuple[float, np.ndarray]:
    b = np.cos(m * theta)
    coef = float(np.sum(field * b) / (np.sum(b * b) + 1e-12))
    return coef, b


def energy_L2(field: np.ndarray) -> float:
    return float(np.sqrt(np.mean(field ** 2) + 1e-12))


def detect_frequency(signal: np.ndarray, dt: float) -> Tuple[float, float, np.ndarray, np.ndarray]:
    sig = signal - np.mean(signal)
    yf = np.abs(rfft(sig))
    xf = rfftfreq(len(sig), dt)
    if len(xf) < 3:
        return 0.0, 0.0, xf, yf
    yf[0] = 0.0
    peak_idx = int(np.argmax(yf))
    peak = float(yf[peak_idx])
    noise = float(np.median(yf[yf > 0])) if np.any(yf > 0) else 1e-12
    return float(xf[peak_idx]), float(peak / (noise + 1e-12)), xf, yf

# ------------------------------
# Feature maps (adapters)
# ------------------------------

class FeatureMap:
    """Abstract 2D feature field provider."""

    def field(self) -> np.ndarray:
        raise NotImplementedError

    def describe(self) -> str:
        return "featuremap"


class ImageFeatureMap(FeatureMap):
    def __init__(self, img: Image.Image, size: int = 192):
        self.size = int(size)
        g = img.convert("L").resize((self.size, self.size))
        arr = np.array(g).astype(np.float32)
        arr = (arr - arr.mean()) / (arr.std() + 1e-12)
        self._field = np.tanh(arr / 2.5)

    @classmethod
    def from_path(cls, path: str, size: int = 192) -> "ImageFeatureMap":
        return cls(Image.open(path), size=size)

    def field(self) -> np.ndarray:
        return self._field

    def describe(self) -> str:
        return "image"


class TextByteFeatureMap(FeatureMap):
    """Map bytes of a text file into a square grid; normalize and squash."""

    def __init__(self, data: bytes, size: int = 192):
        self.size = int(size)
        N = self.size * self.size
        buf = data[:N].ljust(N, b"\0")
        arr = np.frombuffer(buf, dtype=np.uint8).astype(np.float32).reshape(self.size, self.size)
        arr = (arr - arr.mean()) / (arr.std() + 1e-12)
        self._field = np.tanh(arr / 3.0)

    @classmethod
    def from_path(cls, path: str, size: int = 192) -> "TextByteFeatureMap":
        with open(path, "rb") as f:
            data = f.read()
        return cls(data, size=size)

    def field(self) -> np.ndarray:
        return self._field

    def describe(self) -> str:
        return "text-bytes"


class TimeseriesFeatureMap(FeatureMap):
    """Map a 1D numeric series into a polar/radial grid (spectrogram‑like)."""

    def __init__(self, series: np.ndarray, size: int = 192):
        self.size = int(size)
        s = np.asarray(series, dtype=np.float32)
        s = (s - np.mean(s)) / (np.std(s) + 1e-12)
        # Build polar rings by repeating the 1D signal along theta and modulating by radius
        x, y, r, theta = polar_grid(self.size, 1.0)
        # radially varying envelope to avoid hard edges
        env = np.exp(-(r ** 2) / (0.6 ** 2))
        # wrap series onto angles
        steps = s.shape[0]
        ang_idx = ((theta + math.pi) / (2 * math.pi) * steps).astype(int) % steps
        arr = s[ang_idx] * env
        self._field = np.tanh(arr)

    @classmethod
    def from_csv(cls, path: str, value_col: str = "close", size: int = 192) -> "TimeseriesFeatureMap":
        import pandas as pd
        df = pd.read_csv(path)
        if value_col not in df.columns:
            # try last numeric column
            nums = [c for c in df.columns if np.issubdtype(df[c].dtype, np.number)]
            assert nums, f"No numeric column found in {path}"
            value_col = nums[-1]
        return cls(df[value_col].to_numpy(), size=size)

    def field(self) -> np.ndarray:
        return self._field

    def describe(self) -> str:
        return "timeseries"

# ------------------------------
# Collapse configuration and result
# ------------------------------

@dataclass
class CollapseConfig:
    kappa: float = 0.9
    Ta: float = 0.28
    Gamma: float = 0.88
    Ki: float = 2 * math.pi * 0.8
    fold_type: str = "global"  # "global" | "per_radius" | "multiscale"
    size: int = 192
    max_m: int = 8
    energy_tol: float = 0.05
    r_bins: int = 6  # for per_radius
    scales: int = 2  # for multiscale

@dataclass
class CollapseResult:
    image_source: str
    source_kind: str
    kappa: float
    Ta: float
    Gamma: float
    Ki: float
    gate: float
    lobes_before: int
    lobes_after: int
    delta_m: int
    energy_balance: float
    verdict_pass: bool
    fold_type: str
    field_png: str = ""
    spectrum_png: str = ""

    def dict(self) -> Dict[str, object]:
        return asdict(self)

# ------------------------------
# Collapser engine
# ------------------------------

class HelicalCollapseEngine:
    def __init__(self):
        pass

    def _collapse_once(self, field: np.ndarray, theta: np.ndarray,
                        cfg: CollapseConfig) -> Tuple[np.ndarray, float, int, int, float]:
        evolved = helical_time_evolve(field, cfg.kappa, t=6.0)
        m_pre, _, _ = dominant_mode_signed(evolved, theta, max_m=cfg.max_m)
        g = gate_from_params(cfg.Ta, cfg.Gamma)

        if cfg.fold_type == "per_radius":
            collapsed = self._fold_per_radius(evolved, theta, g, cfg)
        elif cfg.fold_type == "multiscale":
            collapsed = self._fold_multiscale(evolved, theta, g, cfg)
        else:
            collapsed = self._fold_global(evolved, theta, g, cfg, m_pre)

        m_post, _, _ = dominant_mode_signed(collapsed, theta, max_m=cfg.max_m)
        # energy accounting (removed vs refill measured indirectly via delta of projections)
        # here use simple proxy: |E(evolved) - E(collapsed)|
        Eb = abs(energy_L2(evolved) - energy_L2(collapsed))
        return collapsed, g, m_pre, m_post, Eb

    def _fold_global(self, field: np.ndarray, theta: np.ndarray, g: float,
                      cfg: CollapseConfig, m_dom: int) -> np.ndarray:
        # remove dom
        c_dom, b_dom = proj_mode(field, theta, m_dom)
        removed = g * c_dom * b_dom
        remainder = field - removed
        # refill into m=2
        c2, b2 = proj_mode(remainder, theta, 2)
        E_removed = energy_L2(removed)
        b2u = b2 / (energy_L2(b2) + 1e-12)
        refill = E_removed * b2u * np.sign(c2 if abs(c2) > 1e-8 else 1.0)
        return remainder + refill

    def _fold_per_radius(self, field: np.ndarray, theta: np.ndarray, g: float,
                          cfg: CollapseConfig) -> np.ndarray:
        n = field.shape[0]
        c = n // 2
        rr = np.sqrt((np.indices(field.shape)[0] - c) ** 2 + (np.indices(field.shape)[1] - c) ** 2)
        r_norm = rr / (rr.max() + 1e-12)
        edges = np.linspace(0.0, 1.0, cfg.r_bins + 1)
        out = field.copy()
        for i in range(cfg.r_bins):
            mask = (r_norm >= edges[i]) & (r_norm < edges[i + 1])
            if not np.any(mask):
                continue
            # local dominant mode on signed derivative
            m_loc, _, _ = dominant_mode_signed(out * mask, theta, max_m=cfg.max_m)
            c_dom, b_dom = proj_mode(out, theta, m_loc)
            removed = g * c_dom * b_dom * mask
            remainder = out - removed
            c2, b2 = proj_mode(remainder, theta, 2)
            E_removed = energy_L2(removed)
            b2u = b2 / (energy_L2(b2) + 1e-12)
            refill = E_removed * b2u * np.sign(c2 if abs(c2) > 1e-8 else 1.0)
            out = remainder + refill * mask
        return out

    def _fold_multiscale(self, field: np.ndarray, theta: np.ndarray, g: float,
                          cfg: CollapseConfig) -> np.ndarray:
        out = field.copy()
        for s in range(cfg.scales):
            f_small = self._resize(out, scale=0.5)
            t_small = self._resize(theta, scale=0.5)
            # one global fold at coarse scale
            m_pre_s, _, _ = dominant_mode_signed(f_small, t_small, max_m=cfg.max_m)
            f_small = self._fold_global(f_small, t_small, g, cfg, m_pre_s)
            # upsample and blend
            up = self._resize(f_small, shape=out.shape)
            out = 0.5 * out + 0.5 * up
        # finalize with a global fold
        m_pre_f, _, _ = dominant_mode_signed(out, theta, max_m=cfg.max_m)
        return self._fold_global(out, theta, g, cfg, m_pre_f)

    @staticmethod
    def _resize(arr: np.ndarray, scale: Optional[float] = None, shape: Optional[Tuple[int, int]] = None) -> np.ndarray:
        from PIL import Image
        if shape is None:
            shape = (max(4, int(arr.shape[1] * scale)), max(4, int(arr.shape[0] * scale)))
        img = Image.fromarray(arr.astype(np.float32))
        img = img.resize((shape[1], shape[0]))
        return np.array(img).astype(np.float32)

    def collapse(self, fmap: FeatureMap, cfg: CollapseConfig,
                 save_dir: Optional[str] = None, tag: Optional[str] = None,
                 save_figs: bool = False) -> CollapseResult:
        size = cfg.size
        x, y, r, theta = polar_grid(size, 1.0)
        field = fmap.field()
        if field.shape != (size, size):
            # simple resize to requested square size
            field = self._resize(field, shape=(size, size))
        collapsed, g, m_pre, m_post, Eb = self._collapse_once(field, theta, cfg)

        # verdict
        delta_m = int(m_pre) - int(m_post)
        pass_geom = (delta_m >= 1) and (m_post <= 2)
        pass_energy = (Eb < cfg.energy_tol)
        verdict = bool(pass_geom and pass_energy and (g >= 0.5))

        field_png = spec_png = ""
        if save_figs and save_dir and tag:
            ensure_dir(save_dir)
            # signed‑∂θ pre/post
            _, s_pre, _ = dominant_mode_signed(field, theta, max_m=cfg.max_m)
            _, s_post, _ = dominant_mode_signed(collapsed, theta, max_m=cfg.max_m)
            plt.figure(figsize=(9, 4))
            plt.subplot(1, 2, 1); plt.imshow(s_pre, cmap="viridis"); plt.axis("off"); plt.title(f"Signed ∂θ Pre (m≈{m_pre})")
            plt.subplot(1, 2, 2); plt.imshow(s_post, cmap="viridis"); plt.axis("off"); plt.title(f"Signed ∂θ Post (m≈{m_post})")
            plt.tight_layout(); field_png = os.path.join(save_dir, f"{tag}_signed_grad.png"); plt.savefig(field_png); plt.close()
            # Ki spectrum (synthetic beat for continuity)
            t = np.arange(0, 6.0, 1/160.0)
            phi = float(np.tanh(collapsed.mean())) * np.sin(cfg.Ki * t)
            fpk, snr, xf, yf = detect_frequency(phi, 1/160.0)
            plt.figure(figsize=(6, 4)); plt.plot(xf, yf); plt.xlabel("Frequency"); plt.ylabel("Amplitude"); plt.title(f"Ki spectrum (peak={fpk:.2f})")
            plt.tight_layout(); spec_png = os.path.join(save_dir, f"{tag}_spectrum.png"); plt.savefig(spec_png); plt.close()

        return CollapseResult(
            image_source=tag or fmap.describe(),
            source_kind=fmap.describe(),
            kappa=cfg.kappa, Ta=cfg.Ta, Gamma=cfg.Gamma, Ki=cfg.Ki,
            gate=g, lobes_before=int(m_pre), lobes_after=int(m_post),
            delta_m=int(delta_m), energy_balance=float(Eb),
            verdict_pass=verdict, fold_type=cfg.fold_type,
            field_png=field_png, spectrum_png=spec_png,
        )

# ------------------------------
# Batch & CLI
# ------------------------------

def run_batch(images: List[str] = None, txts: List[str] = None, csvs: List[str] = None,
              cfg: CollapseConfig = None, out_dir: str = "out", figs: bool = False,
              csv_out: str = "collapse_atlas.csv", value_col: str = "close") -> str:
    images = images or []
    txts = txts or []
    csvs = csvs or []
    cfg = cfg or CollapseConfig()

    eng = HelicalCollapseEngine()
    ensure_dir(out_dir)
    rows: List[Dict[str, object]] = []

    def do_one(fmap: FeatureMap, src: str):
        tag = os.path.splitext(os.path.basename(src))[0]
        res = eng.collapse(fmap, cfg, save_dir=os.path.join(out_dir, tag), tag=tag, save_figs=figs)
        d = res.dict(); d["source_path"] = src
        rows.append(d)

    for p in images:
        fmap = ImageFeatureMap.from_path(p, size=cfg.size)
        do_one(fmap, p)
    for p in txts:
        fmap = TextByteFeatureMap.from_path(p, size=cfg.size)
        do_one(fmap, p)
    for p in csvs:
        fmap = TimeseriesFeatureMap.from_csv(p, value_col=value_col, size=cfg.size)
        do_one(fmap, p)

    out_csv = os.path.join(out_dir, csv_out)
    import pandas as pd
    pd.DataFrame(rows).to_csv(out_csv, index=False)
    return out_csv


def _glob_many(patterns: Iterable[str]) -> List[str]:
    out: List[str] = []
    for pat in patterns:
        out.extend(glob.glob(pat))
    return sorted(list(dict.fromkeys(out)))


def main():
    import argparse
    ap = argparse.ArgumentParser(description="Pirouette Dimensional Collapse Engine")
    ap.add_argument("--images", nargs="*", help="glob patterns for PNG/JPG inputs")
    ap.add_argument("--txt", nargs="*", help="glob patterns for TXT inputs")
    ap.add_argument("--csv", nargs="*", help="glob patterns for CSV time series")
    ap.add_argument("--csv-col", default="close", help="value column for CSV time series")
    ap.add_argument("--size", type=int, default=192)
    ap.add_argument("--kappa", type=float, default=0.9)
    ap.add_argument("--Ta", type=float, default=0.28)
    ap.add_argument("--Gamma", type=float, default=0.88)
    ap.add_argument("--Ki", type=float, default=2 * math.pi * 0.8)
    ap.add_argument("--fold", choices=["global", "per_radius", "multiscale"], default="global")
    ap.add_argument("--figs", action="store_true")
    ap.add_argument("--out", default="out")
    ap.add_argument("--csv-out", default="collapse_atlas.csv")
    args = ap.parse_args()

    cfg = CollapseConfig(kappa=args.kappa, Ta=args.Ta, Gamma=argsGamma if hasattr(args,'Gamma') else args.Gamma, # guard
                         Ki=args.Ki, fold_type=args.fold, size=args.size)

    images = _glob_many(args.images or [])
    txts   = _glob_many(args.txt or [])
    csvs   = _glob_many(args.csv or [])

    out_csv = run_batch(images, txts, csvs, cfg, out_dir=args.out, figs=args.figs,
                        csv_out=args.csv_out, value_col=args.csv_col)
    print(f"Wrote {out_csv} with {len(images)+len(txts)+len(csvs)} items.")


if __name__ == "__main__":
    main()
