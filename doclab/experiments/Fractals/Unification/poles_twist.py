import numpy as np
from twist_unit import winding_eigenmode_scan

if __name__ == "__main__":
    taus, mins, eigen = winding_eigenmode_scan(0.0, 10.0, omega0=6.0)
    print("Eigenmode τs (near poles):")
    for t, m, flag in zip(taus, mins, eigen):
        if flag:
            print(f"  τ ≈ {t:.5f}, min|ω| ≈ {m:.3e}")
