
import numpy as np
from scipy import signal
from pathlib import Path

def windows(n, win=128, hop=64):
    i = 0
    while i + win <= n:
        yield i, i + win
        i += hop

def generate_closure_rng(
    n_samples=10_000,
    max_val=69,
    target_dP=0.06,
    target_kappa=0.09,
    win=128,
    hop=64,
    inject_cycles=True,
    cycle_every=3,
    rng=None,
):
    if rng is None:
        rng = np.random.default_rng()
    base = rng.integers(1, max_val + 1, size=n_samples)

    t = np.arange(n_samples)
    carrier = 0.12 * np.sin(2 * np.pi * (1.0 / 256.0) * t)

    widx = 0
    for s, e in windows(n_samples, win=win, hop=hop):
        seg = carrier[s:e]

        # power shaping
        if np.mean(seg * seg) < target_dP:
            seg = seg + 0.15 * np.hanning(len(seg))

        # curvature shaping
        if np.var(seg) < target_kappa ** 2:
            seg = seg + 0.05 * np.sin(2 * np.pi * (1.0 / 32.0) * np.arange(len(seg)))

        if inject_cycles:
            mod = widx % cycle_every
            if mod == 0:  # Weaver
                seg = seg + 0.20 * np.hanning(len(seg))
            elif mod == 1:  # Gladiator
                seg = seg + 0.25 * np.hanning(len(seg))
                seg = seg + 0.08 * np.sin(2 * np.pi * (1.0 / 20.0) * np.arange(len(seg)))
            elif mod == 2:  # Vortex
                seg = seg - 0.18 * np.hanning(len(seg))
            # Drifter: do nothing
        carrier[s:e] = seg
        widx += 1

    x_float = base.astype(float) + carrier
    ranks = np.argsort(x_float)
    base_sorted = np.sort(base)
    shaped = np.empty_like(base)
    shaped[ranks] = base_sorted
    return shaped, carrier

def main():
    seq, carrier = generate_closure_rng()
    out = Path("closure_rng_10000.txt")
    np.savetxt(out, seq, fmt="%d")
    print(f"wrote {len(seq)} ints to {out}")

if __name__ == "__main__":
    main()
