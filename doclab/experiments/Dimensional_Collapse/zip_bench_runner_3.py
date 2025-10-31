

from __future__ import annotations
import os, io, math, gzip, glob, argparse, textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Dict, Optional

import numpy as np
import pandas as pd
from PIL import Image

# ------------------------------
# Small utils
# ------------------------------

def ensure_dir(p: str):
    if p and not os.path.exists(p):
        os.makedirs(p, exist_ok=True)

def slugify(s: str) -> str:
    return "".join(ch if ch.isalnum() or ch in "-_." else "_" for ch in s)

# ------------------------------
# Geometry & collapse core
# ------------------------------

def polar_grid(n: int = 192, r_max: float = 1.0):
    lin = np.linspace(-r_max, r_max, n)
    x, y = np.meshgrid(lin, lin)
    r = np.sqrt(x*x + y*y) + 1e-12
    theta = np.arctan2(y, x)
    return x, y, r, theta

def helical_time_evolve(field: np.ndarray, kappa: float, t: float = 6.0, omega: float = 2*math.pi*1.0) -> np.ndarray:
    gx, _ = np.gradient(field)
    return np.cos(kappa*omega*t)*field + np.sin(kappa*omega*t)*gx

def signed_angular_gradient(field: np.ndarray, theta: np.ndarray) -> np.ndarray:
    gx, gy = np.gradient(field)
    tx, ty = -np.sin(theta), np.cos(theta)
    return gx*tx + gy*ty

def dominant_mode_signed(field: np.ndarray, theta: np.ndarray, max_m: int = 8, r_mask_inner: int = 4) -> Tuple[int, np.ndarray]:
    s = signed_angular_gradient(field, theta)
    s = s - s.mean()
    n = s.shape[0]; c = n//2
    rr = np.sqrt((np.indices(s.shape)[0]-c)**2 + (np.indices(s.shape)[1]-c)**2)
    mask = rr > r_mask_inner
    amps = []
    for m in range(1, max_m+1):
        c0 = np.sum(s[mask]*np.cos(m*theta[mask]))
        s0 = np.sum(s[mask]*np.sin(m*theta[mask]))
        amps.append((m, float(np.hypot(c0, s0))))
    amps.sort(key=lambda t: t[1], reverse=True)
    return int(amps[0][0]), s

def proj_mode(field: np.ndarray, theta: np.ndarray, m: int) -> Tuple[float, np.ndarray]:
    b = np.cos(m*theta)
    coef = np.sum(field*b) / (np.sum(b*b) + 1e-12)
    return float(coef), b

def energy_L2(field: np.ndarray) -> float:
    return float(np.sqrt(np.mean(field**2) + 1e-12))

def gate_from_params(Ta: float, Gamma: float) -> float:
    g_lin = np.clip((1.0 - Ta)*Gamma, 0.0, 1.0)
    return float(1.0 - math.exp(-3.0 * g_lin))

def Ta_from_gate(g: float, Gamma: float) -> float:
    if g <= 0.0: return 1.0
    if g >= 1.0: return 0.0
    one_minus_Ta = - math.log(1.0 - g) / (3.0*Gamma + 1e-12)
    return float(np.clip(1.0 - one_minus_Ta, 0.0, 1.0))

# ------------------------------
# Entropy & utilities
# ------------------------------

def entropy_image_field(field: np.ndarray, bins: int = 64) -> float:
    f = np.clip(field, -1.0, 1.0)
    hist, _ = np.histogram(f, bins=bins, range=(-1,1), density=True)
    p = hist / (hist.sum() + 1e-12); p = p[p>0]
    return float(-(p*np.log2(p)).sum())

def entropy_text_bytes(data: bytes, bins: int = 256) -> float:
    if len(data)==0: return 0.0
    arr = np.frombuffer(data, dtype=np.uint8)
    hist, _ = np.histogram(arr, bins=bins, range=(0,256), density=False)
    p = hist / (hist.sum() + 1e-12); p = p[p>0]
    return float(-(p*np.log2(p)).sum())

from PIL import Image

def to_png_bytes_from_field(field: np.ndarray) -> int:
    f = np.clip((field + 1.0) * 127.5, 0, 255).astype(np.uint8)
    im = Image.fromarray(f, mode="L")
    bio = io.BytesIO(); im.save(bio, format="PNG", optimize=True)
    return len(bio.getvalue())

def pearson_corr(a: np.ndarray, b: np.ndarray) -> float:
    a = a.astype(np.float64); b = b.astype(np.float64)
    a = (a - a.mean())/(a.std()+1e-12)
    b = (b - b.mean())/(b.std()+1e-12)
    return float(np.clip(np.mean(a*b), -1.0, 1.0))

def gzip_size(b: bytes, level: int = 6) -> int:
    bio = io.BytesIO()
    with gzip.GzipFile(fileobj=bio, mode="wb", compresslevel=level) as gz:
        gz.write(b)
    return len(bio.getvalue())

def unigram_kl(p_counts: np.ndarray, q_counts: np.ndarray) -> float:
    p = p_counts / (p_counts.sum() + 1e-12)
    q = q_counts / (q_counts.sum() + 1e-12)
    eps = 1e-12
    return float(np.sum(p * np.log((p + eps)/(q + eps))))

# ------------------------------
# Feature mappers
# ------------------------------

def image_to_field(path: str, size: int = 192) -> np.ndarray:
    img = Image.open(path).convert("L").resize((size, size))
    arr = np.array(img).astype(np.float32)
    arr = (arr - arr.mean())/(arr.std()+1e-12)
    return np.tanh(arr/2.5)

def text_to_field_and_bytes(path: str, size: int = 192) -> Tuple[np.ndarray, bytes]:
    data = Path(path).read_bytes()
    N = size*size
    buf = data[:N].ljust(N, b" ")
    arr = np.frombuffer(buf, dtype=np.uint8).astype(np.float32).reshape(size, size)
    arr = (arr - arr.mean())/(arr.std()+1e-12)
    return np.tanh(arr/3.0), data

# --- replace csv_to_series(...) with this tougher version ---
def csv_to_series(path: str, value_col: Optional[str] = None) -> np.ndarray:
    import csv
    import io
    import pandas as pd
    import numpy as np

    # Try pandas with delimiter sniffing
    try:
        with open(path, "r", newline="") as f:
            sample = f.read(65536)
        import csv as _csv
        dialect = _csv.Sniffer().sniff(sample, delimiters=",;\t| ")
        sep = dialect.delimiter
        df = pd.read_csv(path, sep=sep, engine="python", on_bad_lines="skip")  # pandas >=1.3
        # Choose value column: explicit > last numeric > first numeric
        if value_col and value_col in df.columns:
            s = pd.to_numeric(df[value_col], errors="coerce")
        else:
            numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
            if not numeric_cols:
                # force-coerce all, then take the last col
                df2 = df.apply(pd.to_numeric, errors="coerce")
                numeric_cols = [c for c in df2.columns if pd.api.types.is_numeric_dtype(df2[c])]
                if numeric_cols:
                    s = df2[numeric_cols[-1]]
                else:
                    raise ValueError("No numeric columns after coercion.")
            else:
                s = df[numeric_cols[-1]]
        arr = s.dropna().to_numpy(dtype=np.float32)
        if arr.size == 0:
            raise ValueError("Empty numeric series after cleaning.")
        # standardize
        arr = (arr - arr.mean())/(arr.std()+1e-12)
        return arr.astype(np.float32)
    except Exception:
        # Fallback: DictReader (headered), pick explicit or last field, coerce floats
        vals = []
        with open(path, "r", newline="") as f:
            reader = csv.DictReader(f)
            cols = reader.fieldnames or []
            pick = value_col or (cols[-1] if cols else None)
            for row in reader:
                try:
                    vals.append(float(row[pick]))
                except Exception:
                    continue
        s = np.array(vals, dtype=np.float32)
        if s.size == 0:
            # final fallback: raw lines, split on common delimiters, take last token
            raw = Path(path).read_text(errors="ignore").splitlines()
            out = []
            for line in raw:
                for d in (",",";","\t","|"," "):
                    if d in line:
                        tok = line.strip().split(d)[-1]
                        try:
                            out.append(float(tok))
                        except Exception:
                            pass
                        break
            s = np.array(out, dtype=np.float32)
        s = (s - s.mean())/(s.std()+1e-12) if s.size else s
        return s


def timeseries_to_field(series: np.ndarray, size: int = 192) -> np.ndarray:
    x,y,r,theta = polar_grid(size, 1.0)
    env = np.exp(-(r**2)/(0.6**2))
    steps = max(1, series.shape[0])
    idx = ((theta + math.pi)/(2*math.pi) * steps).astype(int) % steps
    arr = series[idx] * env
    return np.tanh(arr)

# ------------------------------
# Collapse variants
# ------------------------------

def collapse_global(field: np.ndarray, theta: np.ndarray, g: float) -> Tuple[np.ndarray, int, float]:
    m_pre, _ = dominant_mode_signed(field, theta)
    c_dom, b_dom = proj_mode(field, theta, m_pre)
    removed = g * c_dom * b_dom
    remainder = field - removed
    c2, b2 = proj_mode(remainder, theta, 2)
    E_removed = energy_L2(removed)
    b2u = b2 / (energy_L2(b2)+1e-12)
    refill = E_removed * b2u * np.sign(c2 if abs(c2)>1e-8 else 1.0)
    out = remainder + refill
    m_post, _ = dominant_mode_signed(out, theta)
    Eb = abs(energy_L2(field) - energy_L2(out))
    return out, m_post, Eb

def collapse_per_radius(field: np.ndarray, theta: np.ndarray, g: float, r_bins: int = 6) -> Tuple[np.ndarray, int, float]:
    n = field.shape[0]; c = n//2
    rr = np.sqrt((np.indices(field.shape)[0]-c)**2 + (np.indices(field.shape)[1]-c)**2)
    r_norm = rr/(rr.max()+1e-12)
    edges = np.linspace(0.0, 1.0, r_bins+1)
    out = field.copy()
    for i in range(r_bins):
        mask = (r_norm >= edges[i]) & (r_norm < edges[i+1])
        if not np.any(mask):
            continue
        m_loc, _ = dominant_mode_signed(out*mask, theta)
        c_dom, b_dom = proj_mode(out, theta, m_loc)
        removed = g * c_dom * b_dom * mask
        remainder = out - removed
        c2, b2 = proj_mode(remainder, theta, 2)
        E_removed = energy_L2(removed)
        b2u = b2 / (energy_L2(b2)+1e-12)
        refill = E_removed * b2u * np.sign(c2 if abs(c2)>1e-8 else 1.0)
        out = remainder + refill*mask
    m_post, _ = dominant_mode_signed(out, theta)
    Eb = abs(energy_L2(field) - energy_L2(out))
    return out, m_post, Eb

# ------------------------------
# Learner with hysteresis & per‑radius default
# ------------------------------

def learn_sequence(field0: np.ndarray, size: int = 192, kappa: float = 0.9, Gamma: float = 0.88, g0: float = 0.45,
                   alpha: float = 0.15, iters: int = 8, g_star: float = 0.6, per_radius: bool = True, r_bins: int = 6,
                   entropy_kind: str = "image") -> Tuple[pd.DataFrame, np.ndarray]:
    x,y,r,theta = polar_grid(size, 1.0)
    field = field0.copy()
    g = float(np.clip(g0, 0.0, 1.0))
    hold = 0; t_to_corr = -1
    logs: List[Dict[str, float]] = []

    for t in range(iters):
        Ta = Ta_from_gate(g, Gamma)
        evolved = helical_time_evolve(field, kappa, t=6.0)
        H_pre = entropy_image_field(evolved) if entropy_kind != "text_bytes" else entropy_image_field(evolved)
        g_eff = gate_from_params(Ta, Gamma)
        if per_radius:
            collapsed, m_post, Eb = collapse_per_radius(evolved, theta, g_eff, r_bins=r_bins)
        else:
            collapsed, m_post, Eb = collapse_global(evolved, theta, g_eff)
        H_post = entropy_image_field(collapsed)
        dI = H_pre - H_post
        Psi_o = (dI / (g_eff + 1e-12))
        C = (dI / (Eb + 1e-3)) * g_eff
        if (g_eff >= g_star) and (m_post <= 2):
            hold += 1
            if hold == 2 and t_to_corr < 0:
                t_to_corr = t
        else:
            hold = 0
        g = float(np.clip(g + alpha * Psi_o, 0.0, 1.0))
        field = collapsed
        logs.append({
            "iter": t, "g": g_eff, "Ta": Ta, "Gamma": Gamma, "kappa": kappa,
            "H_pre": H_pre, "H_post": H_post, "dI": dI,
            "m_post": int(m_post), "Eb": Eb, "Psi_o": Psi_o, "C": C,
            "t_to_corr": int(t_to_corr)
        })
    return pd.DataFrame(logs), field

# ------------------------------
# Utilities per domain (A1/B1/C1)
# ------------------------------

def util_image_A1(pre_field: np.ndarray, post_field: np.ndarray, corr_thresh: float = 0.90) -> Tuple[float, float, bool]:
    corr = pearson_corr(pre_field, post_field)
    pre_sz = to_png_bytes_from_field(pre_field)
    post_sz = to_png_bytes_from_field(post_field)
    bpp_red = (pre_sz - post_sz) / max(pre_sz, 1)
    ok = (corr >= corr_thresh)
    return float(bpp_red), float(corr), bool(ok)

def util_text_B1(orig_bytes: bytes, post_field: np.ndarray, kl_thresh: float = 0.05) -> Tuple[float, float, bool]:
    fb = np.clip((post_field + 1.0) * 127.5, 0, 255).astype(np.uint8).tobytes()
    gz_orig = gzip_size(orig_bytes)
    gz_post = gzip_size(fb)
    delta_gz = (gz_orig - gz_post) / max(gz_orig, 1)
    arr_o = np.frombuffer(orig_bytes, dtype=np.uint8)
    arr_p = np.frombuffer(fb, dtype=np.uint8)
    hist_o, _ = np.histogram(arr_o, bins=256, range=(0,256), density=False)
    hist_p, _ = np.histogram(arr_p, bins=256, range=(0,256), density=False)
    kl = unigram_kl(hist_o, hist_p)
    ok = (kl <= kl_thresh)
    return float(delta_gz), float(kl), bool(ok)

# Timeseries: spectral entropy & naive forecast MSE delta

def spectral_entropy(series: np.ndarray) -> float:
    s = series - series.mean()
    yf = np.abs(np.fft.rfft(s))
    if yf.size>0: yf[0] = 0.0
    p = yf / (yf.sum() + 1e-12)
    p = p[p>0]
    return float(-(p*np.log2(p)).sum())


def util_timeseries_C1(series: np.ndarray, post_field: np.ndarray) -> Tuple[float, float]:
    n = post_field.shape[0]; c = n//2
    ring = post_field[c, :]
    ring = (ring - ring.mean())/(ring.std()+1e-12)
    H_spec_pre = spectral_entropy(series)
    H_spec_post = spectral_entropy(ring)
    d_specH = H_spec_pre - H_spec_post
    def ar1_mse(x: np.ndarray) -> float:
        x = x.astype(np.float64)
        if x.size < 3: return np.inf
        X = x[:-1]; Y = x[1:]
        a = (X@Y) / (X@X + 1e-12)
        pred = a*X
        return float(np.mean((Y - pred)**2))
    mse_pre = ar1_mse(series)
    mse_post = ar1_mse(ring)
    d_mse = mse_pre - mse_post
    return float(d_specH), float(d_mse)

# ------------------------------
# Probes A2 (linear) & B2 (ring perplexity)
# ------------------------------

def _flatten_feature(field: np.ndarray, down: int = 6) -> np.ndarray:
    # downsample by average pooling to (down x down)
    n = field.shape[0]
    k = n // down
    small = field[:k*down, :k*down].reshape(down, k, down, k).mean(axis=(1,3))
    return small.flatten()

def _one_hot(y: np.ndarray, K: int) -> np.ndarray:
    M = np.zeros((y.size, K), dtype=np.float64)
    M[np.arange(y.size), y] = 1.0
    return M

def linear_probe_A2(items: List[Tuple[str, np.ndarray, int]], lam: float = 1e-2, train_frac: float = 0.7) -> Dict[str, float]:
    # items: (name, field_post, mode_bin)
    X = np.vstack([_flatten_feature(f) for _,f,_ in items])
    y = np.array([b for *_, b in items], dtype=int)
    K = int(y.max()) + 1
    N = X.shape[0]
    idx = np.arange(N)
    rng = np.random.RandomState(42)
    rng.shuffle(idx)
    ntr = max(1, int(train_frac*N))
    tr, te = idx[:ntr], idx[ntr:]
    Xtr, ytr = X[tr], y[tr]
    Xte, yte = X[te], y[te]
    # ridge one-vs-rest: W = (X^T X + lam I)^-1 X^T Y
    Ytr = _one_hot(ytr, K)
    XtX = Xtr.T @ Xtr
    W = np.linalg.solve(XtX + lam*np.eye(XtX.shape[0]), Xtr.T @ Ytr)
    logits = Xte @ W
    pred = logits.argmax(axis=1)
    acc = float((pred == yte).mean()) if yte.size>0 else float('nan')
    return {"acc": acc, "n_train": int(ntr), "n_test": int(yte.size)}

def ring_perplexity_B2(pre_fields: List[np.ndarray], post_fields: List[np.ndarray], qbins: int = 64, train_frac: float = 0.7) -> Dict[str, float]:
    # Extract ring token sequences from fields, quantize, build bigram on train(pre), eval ppl on test(pre/post)
    def ring_tokens(F: np.ndarray) -> np.ndarray:
        n = F.shape[0]; c = n//2
        ring = F[c, :]
        q = np.clip(((ring + 1.0)*0.5*qbins).astype(int), 0, qbins-1)
        return q
    seq_pre = [ ring_tokens(f) for f in pre_fields ]
    seq_post= [ ring_tokens(f) for f in post_fields ]
    N = len(seq_pre)
    idx = np.arange(N)
    rng = np.random.RandomState(123)
    rng.shuffle(idx)
    ntr = max(1, int(train_frac*N))
    tr, te = idx[:ntr], idx[ntr:]
    def bigram_fit(seqs: List[np.ndarray]) -> np.ndarray:
        M = np.ones((qbins, qbins), dtype=np.float64)  # Laplace smoothing
        for s in seqs:
            for i in range(len(s)-1):
                M[s[i], s[i+1]] += 1.0
        # row-normalize
        M = M / M.sum(axis=1, keepdims=True)
        return M
    def perplexity(M: np.ndarray, seqs: List[np.ndarray]) -> float:
        lsum = 0.0; count = 0
        for s in seqs:
            for i in range(len(s)-1):
                p = M[s[i], s[i+1]]
                lsum += -math.log2(p + 1e-12)
                count += 1
        return float(2**(lsum/max(1,count)))
    M = bigram_fit([seq_pre[i] for i in tr])
    ppl_pre = perplexity(M, [seq_pre[i] for i in te])
    ppl_post= perplexity(M, [seq_post[i] for i in te])
    return {"ppl_pre": ppl_pre, "ppl_post": ppl_post, "delta": ppl_pre - ppl_post, "n_train": int(ntr), "n_test": int(len(te))}

# ------------------------------
# Dataset discovery
# ------------------------------

def discover_files(root: Optional[str], patterns: List[str]) -> List[str]:
    if not root: return []
    found: List[str] = []
    for pat in patterns:
        found += glob.glob(str(Path(root)/"**"/pat), recursive=True)
    seen = set(); uniq = []
    for p in found:
        if p not in seen:
            uniq.append(p); seen.add(p)
    return uniq

# ------------------------------
# Runner
# ------------------------------

def run_zip_bench(images_root: Optional[str], txt_root: Optional[str], csv_root: Optional[str], value_col: Optional[str],
                  out_dir: str, size: int = 192, iters: int = 8, per_radius: bool = True, r_bins: int = 6,
                  kappa: float = 0.9, Gamma: float = 0.88, g0: float = 0.45, alpha: float = 0.15, g_star: float = 0.6,
                  eval_probes: bool = True) -> Dict[str, str]:
    ensure_dir(out_dir)
    # --- START: New code for checkpointing ---
    results_csv = str(Path(out_dir) / "zip_bench_results.csv")
    processed_items = set()
    try:
        if os.path.exists(results_csv):
            # Load the 'item' column to see which files have been processed
            df_existing = pd.read_csv(results_csv)
            if 'item' in df_existing.columns:
                processed_items = set(df_existing['item'])
            print(f"Found {len(processed_items)} already processed items. Resuming...")
    except Exception as e:
        print(f"Could not read existing results file, starting fresh. Error: {e}")
    # --- END: New code for checkpointing ---
    images = discover_files(images_root, ["*.png", "*.jpg", "*.jpeg"])
    texts  = discover_files(txt_root,    ["*.txt", "*.md"])    
    csvs   = discover_files(csv_root,    ["*.txt"])            

    # Logs/Results
    all_logs: List[pd.DataFrame] = []
    results_rows: List[Dict[str, object]] = []

    # For probes
    probe_items_img: List[Tuple[str,np.ndarray,int]] = []
    probe_pre_fields_txt: List[np.ndarray] = []
    probe_post_fields_txt: List[np.ndarray] = []

    # IMAGES
    for p in images:
        try:
            pre_field = image_to_field(p, size=size)
            df, post_field = learn_sequence(pre_field, size=size, kappa=kappa, Gamma=Gamma, g0=g0, alpha=alpha,
                                            iters=iters, g_star=g_star, per_radius=per_radius, r_bins=r_bins,
                                            entropy_kind="image")
            bpp_red, corr, ok = util_image_A1(pre_field, post_field)
            C_sum, Eb_sum = float(df["C"].sum()), float(df["Eb"].sum())
            t_to_corr = int(df.loc[df["t_to_corr"]>=0, "t_to_corr"].min()) if (df["t_to_corr"]>=0).any() else iters+1
            # Coarse mode bin from final m_post
            m_bin = 0 if df["m_post"].iloc[-1] <= 1 else (1 if df["m_post"].iloc[-1] == 2 else 2)
            if eval_probes:
                probe_items_img.append((os.path.basename(p), post_field, m_bin))
            # J
            lambda_U, lambda_E, lambda_S = 1.0, 0.1, 0.05
            U = bpp_red if ok else 0.0
            J = C_sum + lambda_U*U - lambda_E*Eb_sum - lambda_S*t_to_corr
            results_rows.append({"item": os.path.basename(p), "kind":"image", "bpp_red": bpp_red, "corr": corr, "ok": ok,
                                 "C_sum": C_sum, "Eb_sum": Eb_sum, "t_to_corr": t_to_corr, "J": J, "path": p})
            df = df.copy(); df["item"] = os.path.basename(p); df["kind"] = "image"; df["path"] = p
            all_logs.append(df)
        except Exception as e:
            print("[image fail]", p, e)

    # TEXTS
    for p in texts:
        try:
            pre_field, bytes_data = text_to_field_and_bytes(p, size=size)
            df, post_field = learn_sequence(pre_field, size=size, kappa=kappa, Gamma=Gamma, g0=g0, alpha=alpha,
                                            iters=iters, g_star=g_star, per_radius=per_radius, r_bins=r_bins,
                                            entropy_kind="text_bytes")
            delta_gz, kl, ok = util_text_B1(bytes_data, post_field)
            C_sum, Eb_sum = float(df["C"].sum()), float(df["Eb"].sum())
            t_to_corr = int(df.loc[df["t_to_corr"]>=0, "t_to_corr"].min()) if (df["t_to_corr"]>=0).any() else iters+1
            if eval_probes:
                probe_pre_fields_txt.append(pre_field)
                probe_post_fields_txt.append(post_field)
            lambda_U, lambda_E, lambda_S = 1.0, 0.1, 0.05
            U = delta_gz if ok else 0.0
            J = C_sum + lambda_U*U - lambda_E*Eb_sum - lambda_S*t_to_corr
            results_rows.append({"item": os.path.basename(p), "kind":"text", "delta_gz": delta_gz, "kl": kl, "ok": ok,
                                 "C_sum": C_sum, "Eb_sum": Eb_sum, "t_to_corr": t_to_corr, "J": J, "path": p})
            df = df.copy(); df["item"] = os.path.basename(p); df["kind"] = "text"; df["path"] = p
            all_logs.append(df)
        except Exception as e:
            print("[text fail]", p, e)

    # TIMESERIES
    for i, p in enumerate(csvs):
        try:
            item_name = os.path.basename(p)
            
            # Check if we should skip this file
            if item_name in processed_items:
                continue # Skip to the next file

            # Print progress
            print(f"Processing timeseries [{i+1}/{len(csvs)}]: {item_name}")

            series = csv_to_series(p, value_col=value_col)
            pre_field = timeseries_to_field(series, size=size)
            df, post_field = learn_sequence(pre_field, size=size, kappa=kappa, Gamma=Gamma, g0=g0, alpha=alpha,
                                            iters=iters, g_star=g_star, per_radius=per_radius, r_bins=r_bins,
                                            entropy_kind="image")
            d_specH, d_mse = util_timeseries_C1(series, post_field)
            C_sum, Eb_sum = float(df["C"].sum()), float(df["Eb"].sum())
            t_to_corr = int(df.loc[df["t_to_corr"]>=0, "t_to_corr"].min()) if (df["t_to_corr"]>=0).any() else iters+1
            lambda_U, lambda_E, lambda_S = 1.0, 0.1, 0.05
            U = max(0.0, d_specH) + 0.1*max(0.0, d_mse)
            J = C_sum + lambda_U*U - lambda_E*Eb_sum - lambda_S*t_to_corr
            
            # --- START: New saving logic ---
            # Create a one-row DataFrame for the current result
            new_result_df = pd.DataFrame([{
                "item": item_name, "kind":"timeseries", "d_specH": d_specH, "d_mse": d_mse,
                "C_sum": C_sum, "Eb_sum": Eb_sum, "t_to_corr": t_to_corr, "J": J, "path": p
            }])
            
            # Append to the CSV immediately
            # The header is only written if the file doesn't exist yet
            header = not os.path.exists(results_csv)
            new_result_df.to_csv(results_csv, mode='a', header=header, index=False)
            # --- END: New saving logic ---

            df = df.copy(); df["item"] = item_name; df["kind"] = "timeseries"; df["path"] = p
            all_logs.append(df)
        except Exception as e:
            print(f"[csv fail on {os.path.basename(p)}] {e}")

    # Write logs/results
    logs_df = pd.concat(all_logs, ignore_index=True) if all_logs else pd.DataFrame()
    results_df = pd.DataFrame(results_rows)
    logs_csv = str(Path(out_dir)/"zip_bench_logs.csv")
    results_csv = str(Path(out_dir)/"zip_bench_results.csv")
    logs_df.to_csv(logs_csv, index=False)
    results_df.to_csv(results_csv, index=False)

    # --- Probes ---
    a2_csv = b2_csv = None
    a2_acc = None
    b2_delta = None
    if eval_probes:
        # A2: linear probe on images
        if len(probe_items_img) >= 6:  # need a few samples
            a2 = linear_probe_A2(probe_items_img, lam=1e-2, train_frac=0.7)
            a2_acc = a2["acc"]
            a2_csv = str(Path(out_dir)/"probe_A2_linear.csv")
            pd.DataFrame([a2]).to_csv(a2_csv, index=False)
        # B2: ring perplexity on text
        if len(probe_pre_fields_txt) >= 6:
            b2 = ring_perplexity_B2(probe_pre_fields_txt, probe_post_fields_txt, qbins=64, train_frac=0.7)
            b2_delta = b2["delta"]
            b2_csv = str(Path(out_dir)/"probe_B2_perplexity.csv")
            pd.DataFrame([b2]).to_csv(b2_csv, index=False)

    # --- Transfer correlations ---
    xfer_rows = []
    def corr_pair(dfA, xcol, dfB, ycol, label):
        try:
            xa = dfA[xcol].to_numpy().astype(np.float64)
            yb = dfB[ycol].to_numpy().astype(np.float64)
            n = min(xa.size, yb.size)
            if n < 3: return None
            xa, yb = xa[:n], yb[:n]
            x = (xa - xa.mean())/(xa.std()+1e-12)
            y = (yb - yb.mean())/(yb.std()+1e-12)
            r = float(np.mean(x*y))
            xfer_rows.append({"from": xcol+"@images", "to": ycol+f"@{label}", "pearson_r": r, "n": n})
        except Exception:
            return None
    try:
        img = results_df[results_df["kind"]=="image"]
        txt = results_df[results_df["kind"]=="text"]
        ts  = results_df[results_df["kind"]=="timeseries"]
        if not img.empty and not txt.empty:
            corr_pair(img, "C_sum", txt, "delta_gz", "text")
            corr_pair(img, "J",     txt, "delta_gz", "text")
        if not img.empty and not ts.empty:
            corr_pair(img, "C_sum", ts,  "d_specH",  "timeseries")
            corr_pair(img, "J",     ts,  "d_specH",  "timeseries")
        if not txt.empty and not ts.empty:
            corr_pair(txt, "C_sum", ts,  "d_specH",  "timeseries")
            corr_pair(txt, "J",     ts,  "d_specH",  "timeseries")
    except Exception:
        pass
    xfer_df = pd.DataFrame(xfer_rows)
    xfer_csv = str(Path(out_dir)/"zip_bench_transfer.csv")
    xfer_df.to_csv(xfer_csv, index=False)

    # --- Report ---
    report = Path(out_dir)/"report.md"
    by_kind = results_df.groupby("kind").agg(n=("item","count"), mean_C=("C_sum","mean"), mean_J=("J","mean")).reset_index()
    sect_probes = []
    if a2_acc is not None:
        sect_probes.append(f"A2 (images) linear‑probe accuracy: **{a2_acc:.3f}**")
    else:
        sect_probes.append("A2 (images) linear‑probe: not enough items to evaluate (need ≥6 collapsed images).")
    if b2_delta is not None:
        sign = "↓" if b2_delta>0 else "↑"
        sect_probes.append(f"B2 (text) ring perplexity change: **Δ={b2_delta:.3f} ({sign} is better)**")
    else:
        sect_probes.append("B2 (text) ring perplexity: not enough items to evaluate (need ≥6 texts).")
    sect_xfer = (xfer_df.to_markdown(index=False) if not xfer_df.empty else "(no cross‑dataset pairs to correlate)")
    md = f"""
# ZIP‑Bench v0.3 Report

**Items:** images={len(images)}, text={len(texts)}, timeseries={len(csvs)}  
**Per‑radius folding:** {'ON' if per_radius else 'OFF'}  
**Iterations per item:** {iters}

## Domain Summary
{by_kind.to_markdown(index=False)}

## Probes
{os.linesep.join(sect_probes)}

## Transfer correlations
{xfer_df.to_markdown(index=False) if not xfer_df.empty else '(none)'}

## Notes
- J = ΣC + U − 0.1Σε − 0.05·T_corr; higher is better.  
- A2 uses closed‑form ridge one‑vs‑rest on pooled features (no sklearn).  
- B2 bigram perplexity is computed on ring quantization; Δ>0 means post‑collapse is **more predictable**.
"""
    report.write_text(textwrap.dedent(md), encoding='utf-8')

    return {"logs_csv": logs_csv, "results_csv": results_csv, "transfer_csv": xfer_csv, "report": str(report),
            "probe_A2": a2_csv or "", "probe_B2": b2_csv or ""}

# ------------------------------
# CLI
# ------------------------------

def main():
    ap = argparse.ArgumentParser(description="ZIP‑Bench v0.3 Runner — Pirouette collapse‑as‑learning (probes+report)")
    ap.add_argument("--images-root", type=str, default=None, help="root folder of images (PNG/JPG)")
    ap.add_argument("--txt-root",    type=str, default=None, help="root folder of text files (.txt, .md)")
    ap.add_argument("--csv-root",    type=str, default=None, help="root folder of CSV time series")
    ap.add_argument("--csv-col",     type=str, default=None, help="value column for CSV (e.g., Close)")
    ap.add_argument("--out",         type=str, default="zip_bench_out")
    ap.add_argument("--size",        type=int, default=192)
    ap.add_argument("--iters",       type=int, default=8)
    ap.add_argument("--global-fold", action="store_true", help="use global (not per‑radius) folding")
    ap.add_argument("--r-bins",      type=int, default=6)
    ap.add_argument("--kappa",       type=float, default=0.9)
    ap.add_argument("--Gamma",       type=float, default=0.88)
    ap.add_argument("--g0",          type=float, default=0.45)
    ap.add_argument("--alpha",       type=float, default=0.15)
    ap.add_argument("--g-star",      type=float, default=0.6)
    ap.add_argument("--no-probes",   action="store_true", help="disable A2/B2 probes and report")
    args = ap.parse_args()

    outs = run_zip_bench(images_root=args.images_root, txt_root=args.txt_root, csv_root=args.csv_root,
                         value_col=args.csv_col, out_dir=args.out, size=args.size, iters=args.iters,
                         per_radius=(not args.global_fold), r_bins=args.r_bins, kappa=args.kappa, Gamma=args.Gamma,
                         g0=args.g0, alpha=args.alpha, g_star=args.g_star, eval_probes=(not args.no_probes))
    print("Wrote:")
    for k,v in outs.items():
        print(f"  {k}: {v}")

if __name__ == "__main__":
    main()
