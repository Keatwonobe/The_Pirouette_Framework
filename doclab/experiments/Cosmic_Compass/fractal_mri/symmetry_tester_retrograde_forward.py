# symmetry_tester.py
from PIL import Image
import numpy as np
import sys

def symmetry_stats(arr, label="image"):
    # optional crop to avoid borders/titles
    pad = 100
    a = arr[pad:-pad, pad:-pad]

    def stats(diff):
        d = np.abs(diff).astype(np.float32)
        mean = d.mean()
        p999 = np.percentile(d, 99.9)
        return mean, p999

    v = a - a[:, ::-1, :]        # left–right mirror
    h = a - a[::-1, :, :]        # top–bottom mirror
    r = a - a[::-1, ::-1, :]     # 180° rotation

    print(f"\n=== {label} ===")
    for name, diff in [("Vertical", v), ("Horizontal", h), ("Rot180", r)]:
        mean, p999 = stats(diff)
        print(f"{name:10s}: mean Δ = {mean:6.3f}, 99.9% Δ ≤ {p999:6.3f}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python symmetry_tester.py path/to/image.png")
        sys.exit(1)

    path = sys.argv[1]
    img = Image.open(path).convert("RGB")
    arr = np.asarray(img, dtype=np.int16)
    symmetry_stats(arr, label=path)
