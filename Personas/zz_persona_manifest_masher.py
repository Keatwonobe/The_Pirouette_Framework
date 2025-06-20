import os
import json
from pathlib import Path
import datetime

def gather_module_entries(modules_dir):
    """
    Scans `modules_dir` for JSON files and extracts
    the manifest fields from each one.

    Handles JSON files containing a single object or a list of objects.
    """
    entries = []
    print(f"Scanning for module files in: {modules_dir}")
    if not os.path.isdir(modules_dir):
        print(f"Error: Directory not found at {modules_dir}")
        return []

    for fname in os.listdir(modules_dir):
        # Skip this script and the output manifest itself
        if not fname.lower().endswith('.json') or "tendu_manifest" in fname:
            continue
        
        path = os.path.join(modules_dir, fname)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # FIX: Check if the loaded data is a list or a single dictionary
            if isinstance(data, list):
                # If it's a list, process each item in the list
                for item in data:
                    entry = {
                        "tenduModuleID": item.get("tenduModuleID"),
                        "moduleName": item.get("moduleName"),
                        "version": item.get("version"),
                        "pirouetteFrameworkOrigin": item.get("pirouetteFrameworkOrigin"),
                        "primaryPurposeConciseStatement": item.get("primaryPurposeConciseStatement"),
                        "filePath": os.path.relpath(path, modules_dir) # Store relative path
                    }
                    entries.append(entry)
            elif isinstance(data, dict):
                # If it's a dict, process it directly as before
                entry = {
                    "tenduModuleID": data.get("tenduModuleID"),
                    "moduleName": data.get("moduleName"),
                    "version": data.get("version"),
                    "pirouetteFrameworkOrigin": data.get("pirouetteFrameworkOrigin"),
                    "primaryPurposeConciseStatement": data.get("primaryPurposeConciseStatement"),
                    "filePath": os.path.relpath(path, modules_dir) # Store relative path
                }
                entries.append(entry)

        except json.JSONDecodeError:
            print(f"Warning: Skipping malformed JSON file: {fname}")
        except Exception as e:
            print(f"An unexpected error occurred with file {fname}: {e}")
            
    return entries

def build_master_manifest(output_path, compendium_info, module_entries):
    """
    Builds the full manifest structure and writes it to `output_path`.
    This will create the file or replace it if it already exists.
    """
    manifest = {
        "tenduCompendiumInfo": compendium_info,
        "modules": module_entries
    }
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"\nSuccessfully wrote master manifest to {output_path}")
    print(f"Found and processed {len(module_entries)} module entries.")


if __name__ == "__main__":
    # --- Configuration ---
    # UPGRADE: Use Pathlib for robust, cross-platform path management.
    # This assumes your 'tendu_modules' directory is in the same folder as this script.
    # If not, adjust the path accordingly, e.g., Path(__file__).parent.parent / 'data' / 'tendu_modules'
    
    script_dir = Path(__file__).parent
    modules_dir = script_dir 
    output_manifest = script_dir / "AA_tendu_manifest.json"

    # The manifest compendium information.
    # UPGRADE: The date is now set automatically to the current date.
    compendium_info = {
        "compendiumName": "Tendu: A Procedural Guide for Pirouette Analytical Modes",
        "version": "1.0.1", # Incremented version
        "dateLastUpdated": datetime.date.today().isoformat(),
        "description": "This manifest lists all available Tendu Modules for AI integration."
    }

    # --- Execution ---
    entries = gather_module_entries(modules_dir)
    if entries:
        build_master_manifest(output_manifest, compendium_info, entries)
    else:
        print("No module entries found. Manifest not generated.")