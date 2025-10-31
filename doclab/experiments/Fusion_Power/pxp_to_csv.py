# pxp_to_csv.py
import sys, re, json
from pathlib import Path
import numpy as np
import pandas as pd

# robust import
try:
    from igor import packed as igor_packed
except ImportError:
    from igor2 import packed as igor_packed

def sanitize(name): return re.sub(r'[^A-Za-z0-9_\-]+', '_', name)

def infer_sfreq(meta):
    for k in ('sfB','hsB','xScaleDelta'):  # Igor dx fields
        if k in meta:
            try:
                dx = float(meta[k])
                if dx > 0: return 1.0/dx
            except: pass
    return None

def extract_waves(pxp_path: Path):
    with open(pxp_path, 'rb') as f:
        obj = igor_packed.load(f)

    waves = {}
    def visit(node, prefix="root"):
        if isinstance(node, dict):
            # If this dictionary itself contains the data, extract it.
            # This is a more robust way to find waves.
            if 'wData' in node:
                data = np.array(node['wData']).astype(float).squeeze()
                meta = node.get('wave_header', {})
                # Try to get a name, fall back to the structural path
                name = node.get('name', prefix)
                waves[str(name)] = (data, meta)
                # We found the data, no need to look further inside this dictionary
                return

            # If not a wave, continue searching its children
            for k, v in node.items():
                visit(v, f"{prefix}/{k}")

        elif isinstance(node, list):
            for i, v in enumerate(node):
                visit(v, f"{prefix}[{i}]")

    visit(obj)
    return waves

if __name__ == "__main__":
    pxp = Path("DS2018-4.pxp")
    out = Path(sys.argv[2] if len(sys.argv)>2 else pxp.with_suffix('').name + "_csv")
    out.mkdir(exist_ok=True, parents=True)

    waves = extract_waves(pxp)
    if not waves:
        print("No waves found—this PXP may reference external IBW files. If so, export IBW or point this at the IBW folder.")
        sys.exit(1)

    manifest = []
    for nm, (data, meta) in waves.items():
        base = sanitize(nm)
        csv = out / f"{base}.csv"
        pd.DataFrame({"value": data}).to_csv(csv, index=False)
        sf = infer_sfreq(meta)
        with open(out / f"{base}.json","w") as f:
            json.dump({"name": nm, "sfreq": sf, "meta": meta}, f, indent=2)
        manifest.append({"name": nm, "file": csv.name, "sfreq": sf})
    pd.DataFrame(manifest).to_csv(out / "_manifest.csv", index=False)
    print(f"Wrote {len(manifest)} waves to {out}")
