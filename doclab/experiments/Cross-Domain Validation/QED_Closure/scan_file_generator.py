import json
import numpy as np
import pathlib
from typing import List, Dict, Any

def generate_param_grid(
    g_range: tuple[float, float] = (0.5, 2.5),
    beta_range: tuple[float, float] = (0.5, 3.5),
    num_steps: int = 36
) -> List[tuple[float, float]]:
    """Creates a grid of (g, beta) value pairs."""
    g_vals = np.linspace(g_range[0], g_range[1], num_steps)
    beta_vals = np.linspace(beta_range[0], beta_range[1], num_steps)
    
    grid = []
    for g in g_vals:
        for beta in beta_vals:
            # Round to avoid excessive floating point digits in JSON
            grid.append((round(g, 4), round(beta, 4)))
    return grid

def create_scan_file(
    output_path: str = "qed_option_c_scan_results.json",
    num_steps: int = 36
):
    """
    Generates the scan file by creating a parameter grid and
    formatting it into the JSON structure expected by the notebook.
    """
    print(f"Generating {num_steps}x{num_steps} = {num_steps*num_steps} parameter sets...")
    
    param_grid = generate_param_grid(num_steps=num_steps)
    scan_rows: List[Dict[str, Any]] = []

    for g, beta in param_grid:
        # Create the full parameter block for this row.
        # The analysis notebook will pick the g/beta from the
        # group it is analyzing (e.g., "SU3"), so we can
        # just use the same g/beta for all three.
        params = {
            # Default lattice specs
            "N": 16,
            "Nt": 32,
            "a": 1.0,
            
            # Gauge Blocks
            "U1": {
                "type": "abelian",
                "Nc": 1,
                "g": g,
                "beta": beta
            },
            "SU2": {
                "type": "nonabelian",
                "Nc": 2,
                "g": g,
                "beta": beta
            },
            "SU3": {
                "type": "nonabelian",
                "Nc": 3,
                "g": g,
                "beta": beta
            }
        }
        
        # The notebook's coerce function accepts this format
        scan_rows.append({"params": params})

    # --- Save to file ---
    out_file = pathlib.Path(output_path)
    out_file.write_text(json.dumps(scan_rows, indent=2))
    
    print(f"\\nSuccessfully generated scan file at:")
    print(f"{out_file.resolve()}")

if __name__ == "__main__":
    # This will create a 36x36 grid for 1296 total points.
    create_scan_file(
        output_path="qed_option_c_scan_results.json",
        num_steps=36
    )
