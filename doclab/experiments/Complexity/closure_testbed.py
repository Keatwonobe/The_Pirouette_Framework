# closure_testbed.py
import numpy as np
from scipy import signal

def sos_window(seq, win=128, hop=64, fs=1.0, f_center=1.0):
    seq = np.asarray(seq, float)
    z = signal.hilbert(seq - seq.mean())
    dz = np.gradient(z) * fs
    P = np.abs(z)**2

    # windows
    wins = [(s, s+win) for s in range(0, len(seq)-win+1, hop)]
    k0 = max(1, int(0.05*len(wins)))
    P0 = np.median([P[s:e].mean() for (s, e) in wins[:k0]]) + 1e-12

    rows = []
    for (s, e) in wins:
        z_w, dz_w = z[s:e], dz[s:e]
        re = np.real(np.vdot(z_w, z_w))
        im = np.imag(np.vdot(dz_w, z_w))
        kappa = abs(-im / (2*np.pi*f_center*(re+1e-12) + 1e-12))
        dP = (P[s:e].mean() - P0) / P0
        rows.append((kappa, dP))
    return rows

def sos_label(rows, q_k_low=0.65, q_k_high=0.85, q_dp=0.60):
    km = np.array([r[0] for r in rows])
    dp = np.array([r[1] for r in rows])
    th_l = np.quantile(km, q_k_low)
    th_h = np.quantile(km, q_k_high)
    th_P = np.quantile(dp, q_dp)
    labels = []
    for k, d in rows:
        if d >= th_P and th_l <= k < th_h:  lab = "Weaver"
        elif d >= th_P and k >= th_h:       lab = "Gladiator"
        elif d < 0 and k >= th_h:           lab = "Vortex"
        else:                               lab = "Drifter"
        labels.append((k, d, lab))
    return labels, dict(th_k_low=th_l, th_k_high=th_h, th_dP=th_P)

def crunch_sequence(seq):
    rows = sos_window(seq)
    labeled, th = sos_label(rows)
    return labeled, th

def count_wgvd_cycles(states, order=("Weaver", "Gladiator", "Vortex", "Drifter")):
    """Count how many times we see W→G→V→D in order (not necessarily contiguous)."""
    idx = 0
    cycles = 0
    for s in states:
        if s == order[idx]:
            idx += 1
            if idx == len(order):
                cycles += 1
                idx = 0
    return cycles
