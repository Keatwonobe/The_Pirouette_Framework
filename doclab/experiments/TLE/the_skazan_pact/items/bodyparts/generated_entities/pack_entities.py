import os, json, argparse, datetime

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[WARN] Skipped {path}: {e}")
        return None

def pack_codex(input_dir, output_file):
    bundle = {
        "TLE_VERSION": "1.0",
        "compiled_at": datetime.datetime.utcnow().isoformat() + "Z",
        "directories": {}
    }

    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if not file.endswith(".json"):
                continue
            category = os.path.basename(root)
            data = load_json(os.path.join(root, file))
            if not data:
                continue
            bundle.setdefault("directories", {}).setdefault(category, {})[file] = data

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=2)
    print(f"[OK] Codex bundle written to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pack The Lost Eternal JSON Codex.")
    parser.add_argument("--input", required=False, default=".")
    parser.add_argument("--output", default="tle_entity_bundle.json", help="Output bundle path")
    args = parser.parse_args()
    pack_codex(args.input, args.output)
