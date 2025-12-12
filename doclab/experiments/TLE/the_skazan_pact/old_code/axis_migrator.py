import json
import os
from pathlib import Path

def migrate_axes(axes_dir):
    axes_dir = Path(axes_dir)

    if not axes_dir.exists():
        raise FileNotFoundError(f"Axis directory not found: {axes_dir}")

    for path in axes_dir.glob("*.json"):
        try:
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"[WARN] Could not load {path}: {e}")
            continue

        # Filename without extension → new axis ID
        new_axis_id = path.stem  # e.g. ax_biotic

        old_axis_id = data.get("axis_id", None)

        # Don’t overwrite if it already matches what we want
        if old_axis_id == new_axis_id:
            print(f"[OK] {path.name}: axis_id already correct → {new_axis_id}")
            continue

        # Move the old axis_id into hilbert_id
        if old_axis_id is not None:
            data["hilbert_id"] = old_axis_id

        # Write new clean axis_id
        data["axis_id"] = new_axis_id

        # Log change
        print(f"[UPDATE] {path.name}: axis_id {old_axis_id} → {new_axis_id}")

        # Save back to file
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    print("\nMigration complete.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Migrate axis JSONs to filename-based axis_id.")
    parser.add_argument(
        "--dir",
        type=str,
        required=True,
        help="Path to axes directory containing *.json axis files."
    )

    args = parser.parse_args()
    migrate_axes(args.dir)
