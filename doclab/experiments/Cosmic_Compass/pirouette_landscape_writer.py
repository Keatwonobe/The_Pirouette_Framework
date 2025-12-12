import numpy as np
import logging
import sys
import os
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def debug_ply_export(input_file="phase_space_raw.npz", output_file="pirouette_deep_field.ply"):
    
    # --- STEP 1: LOAD DATA ---
    if not os.path.exists(input_file):
        logger.error(f"FATAL: {input_file} not found. Please run the generator first.")
        return

    logger.info(f"[1/3] Loading Data from {input_file}...")
    
    try:
        with np.load(input_file) as data_archive:
            # COPY data to local variables with unambiguous names
            # We explicitly cast to np.array to ensure they are not file views
            ARRAY_M = np.array(data_archive['m_vals'])
            ARRAY_L = np.array(data_archive['l_vals'])
            ARRAY_ESC = np.array(data_archive['escape_time'])
            ARRAY_BID = np.array(data_archive['basin_id'])
            
            # Print types immediately
            logger.info(f"      ARRAY_M type: {type(ARRAY_M)}")
            logger.info(f"      ARRAY_L type: {type(ARRAY_L)}")
            logger.info(f"      ARRAY_ESC type: {type(ARRAY_ESC)}")
            
    except Exception as e:
        logger.error(f"Error loading numpy file: {e}")
        return

    rows, cols = ARRAY_ESC.shape
    total_verts = rows * cols
    
    # --- STEP 2: PRE-PROCESS ARRAYS ---
    logger.info("[2/3] Pre-calculating Height and Masks...")
    
    # Height Calculation
    max_steps = np.max(ARRAY_ESC)
    Z_LOG = np.log1p(ARRAY_ESC)
    
    # Trapped Mask (Boolean Array)
    ARRAY_TRAPPED = (ARRAY_ESC >= max_steps * 0.99)
    
    # Monolith Height Adjustment
    natural_max = np.max(Z_LOG[~ARRAY_TRAPPED]) if np.any(~ARRAY_TRAPPED) else 1.0
    Z_LOG[ARRAY_TRAPPED] = natural_max * 1.2
    
    # Normalize Z
    ARRAY_Z = Z_LOG / np.max(Z_LOG) * 3.0
    
    # Rim Mask (Boolean Array)
    grads = np.gradient(ARRAY_ESC)
    slope = np.sqrt(grads[0]**2 + grads[1]**2)
    ARRAY_RIM = (slope > 5.0) & (slope < 100.0)
    
    # Final Type Check before Loop
    if not isinstance(ARRAY_M, np.ndarray): raise TypeError(f"ARRAY_M is {type(ARRAY_M)}, expected ndarray")
    if not isinstance(ARRAY_RIM, np.ndarray): raise TypeError(f"ARRAY_RIM is {type(ARRAY_RIM)}, expected ndarray")
    if not isinstance(ARRAY_TRAPPED, np.ndarray): raise TypeError(f"ARRAY_TRAPPED is {type(ARRAY_TRAPPED)}, expected ndarray")

    # --- STEP 3: WRITE TO FILE ---
    logger.info(f"[3/3] Streaming {total_verts:,} vertices to {output_file}...")
    
    # Defined Colors (Tuples)
    RGB_TOWER = (220, 220, 230)
    RGB_TEAL  = (20, 180, 180)
    RGB_GOLD  = (210, 160, 40)
    RGB_RED   = (200, 50, 40)
    RGB_RIM   = (255, 255, 255)
    
    try:
        with open(output_file, 'w') as FILE_HANDLE:
            # Header
            FILE_HANDLE.write("ply\n")
            FILE_HANDLE.write("format ascii 1.0\n")
            FILE_HANDLE.write(f"element vertex {total_verts}\n")
            FILE_HANDLE.write("property float x\n")
            FILE_HANDLE.write("property float y\n")
            FILE_HANDLE.write("property float z\n")
            FILE_HANDLE.write("property uchar red\n")
            FILE_HANDLE.write("property uchar green\n")
            FILE_HANDLE.write("property uchar blue\n")
            FILE_HANDLE.write(f"element face {(rows-1) * (cols-1) * 2}\n")
            FILE_HANDLE.write("property list uchar int vertex_index\n")
            FILE_HANDLE.write("end_header\n")
            
            logger.info("      Writing Vertices...")
            
            # Using specific indices to avoid 'range' confusion
            for row_idx in range(rows):
                
                # Progress Log
                if row_idx % 50 == 0:
                    pct = (row_idx / rows) * 100
                    sys.stdout.write(f"\r      {pct:.1f}% ")
                    sys.stdout.flush()
                
                # Cache Y value
                y_val = ARRAY_L[row_idx]
                
                for col_idx in range(cols):
                    # SAFETY CHECK: If this crashes, the traceback will point here
                    x_val = ARRAY_M[col_idx]
                    z_val = ARRAY_Z[row_idx, col_idx]
                    
                    # Lookups
                    basin_val = ARRAY_BID[row_idx, col_idx]
                    is_rim_val = ARRAY_RIM[row_idx, col_idx]
                    is_trapped_val = ARRAY_TRAPPED[row_idx, col_idx]
                    
                    # Color Logic
                    if is_rim_val and basin_val != 0:
                        r, g, b = RGB_RIM
                    elif basin_val == 0 or is_trapped_val:
                        r, g, b = RGB_TOWER
                    elif basin_val == 1:
                        r, g, b = RGB_TEAL
                    elif basin_val == 2:
                        r, g, b = RGB_GOLD
                    elif basin_val == 3:
                        r, g, b = RGB_RED
                    else:
                        r, g, b = RGB_GOLD
                        
                    # Write Line
                    FILE_HANDLE.write(f"{x_val:.4f} {y_val:.4f} {z_val:.4f} {r} {g} {b}\n")
            
            print() # Newline
            logger.info("      Writing Faces...")
            
            total_rows = rows - 1
            for r in range(total_rows):
                if r % 50 == 0:
                    pct = (r / total_rows) * 100
                    sys.stdout.write(f"\r      {pct:.1f}% ")
                    sys.stdout.flush()
                    
                for c in range(cols - 1):
                    tl = r * cols + c
                    tr = tl + 1
                    bl = (r + 1) * cols + c
                    br = bl + 1
                    
                    FILE_HANDLE.write(f"3 {tl} {bl} {tr}\n")
                    FILE_HANDLE.write(f"3 {tr} {bl} {br}\n")
            
            print()

    except Exception:
        # Full Crash Report
        print("\n\n!!! CRASH DETECTED !!!")
        traceback.print_exc()
        print("-" * 30)
        print("DIAGNOSTIC DUMP:")
        try:
            print(f"Current row_idx: {row_idx}")
            print(f"Current col_idx: {col_idx}")
            print(f"Type of ARRAY_M: {type(ARRAY_M)}")
            print(f"Type of ARRAY_M[0]: {type(ARRAY_M[0])}")
            print(f"Type of FILE_HANDLE: {type(FILE_HANDLE)}")
        except:
            print("Could not print diagnostics.")
        return

    logger.info("DONE. File saved successfully.")

if __name__ == "__main__":
    debug_ply_export()