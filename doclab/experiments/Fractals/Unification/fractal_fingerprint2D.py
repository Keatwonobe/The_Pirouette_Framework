# fractal_fingerprint2D.py

import numpy as np
from numpy.fft import fft2, fftshift
from scipy.ndimage import zoom

def gradient_anisotropy(field):
    # simple finite differences
    d_lat = np.diff(field, axis=0, append=field[-1:, :])
    d_lon = np.diff(field, axis=1, append=field[:, -1:])
    rms_lat = np.sqrt(np.mean(d_lat**2))
    rms_lon = np.sqrt(np.mean(d_lon**2))
    anisotropy = rms_lon / (rms_lat + 1e-12)  # >1 = horizontal shear dominance
    return rms_lat, rms_lon, anisotropy

def box_count_dimension(field, n_scales=6, threshold=None):
    # threshold -> binary set of "active" pixels
    if threshold is None:
        threshold = np.percentile(field, 70)
    mask = field > threshold
    n, m = mask.shape
    sizes = []
    counts = []
    for s in range(1, n_scales+1):
        box = 2**s
        if box > min(n, m):
            break
        # how many boxes contain at least one True?
        n_boxes_x = n // box
        n_boxes_y = m // box
        cnt = 0
        for i in range(n_boxes_x):
            for j in range(n_boxes_y):
                if mask[i*box:(i+1)*box, j*box:(j+1)*box].any():
                    cnt += 1
        if cnt > 0:
            sizes.append(box)
            counts.append(cnt)
    if len(counts) < 2:
        return np.nan, np.array(sizes), np.array(counts)

    sizes = np.array(sizes, dtype=float)
    counts = np.array(counts, dtype=float)
    log_inv_s = np.log(1.0 / sizes)
    log_N     = np.log(counts)
    # linear fit
    p = np.polyfit(log_inv_s, log_N, 1)
    D = p[0]
    return D, log_inv_s, log_N

def power_spectrum_lobes(field):
    # optionally downsample for speed
    target = 256
    n, m = field.shape
    scale = min(target/n, target/m, 1.0)
    if scale < 1.0:
        field = zoom(field, scale, order=1)

    F = fftshift(fft2(field - field.mean()))
    P = np.abs(F)**2
    # normalize
    P /= P.max() + 1e-12

    # crude “lobe metrics”: 
    # power in horizontal vs vertical vs diagonal wedges
    h_band = P[P.shape[0]//2-5:P.shape[0]//2+5, :]
    v_band = P[:, P.shape[1]//2-5:P.shape[1]//2+5]
    h_power = h_band.mean()
    v_power = v_band.mean()

    # diagonals: corners
    c = P.shape[0]//2
    d1 = np.diag(P)
    d2 = np.diag(P[:, ::-1])
    d_power = 0.5*(d1.mean() + d2.mean())

    return {
        "h_power": float(h_power),
        "v_power": float(v_power),
        "d_power": float(d_power),
    }, P

def fractal_fingerprint(field):
    """
    field: 2D numpy array
    returns: dict of scalar fingerprints + raw spectra if needed
    """
    field = np.asarray(field, dtype=float)
    rms_lat, rms_lon, anis = gradient_anisotropy(field)
    D, log_inv_s, log_N = box_count_dimension(field)
    ps_metrics, P = power_spectrum_lobes(field)

    return {
        "rms_lat": rms_lat,
        "rms_lon": rms_lon,
        "gradient_anisotropy": anis,
        "box_dim": D,
        "ps_h_power": ps_metrics["h_power"],
        "ps_v_power": ps_metrics["v_power"],
        "ps_d_power": ps_metrics["d_power"],
        # raw extras if you want them:
        "log_inv_s": log_inv_s,
        "log_N": log_N,
        "power_spectrum": P,
    }
