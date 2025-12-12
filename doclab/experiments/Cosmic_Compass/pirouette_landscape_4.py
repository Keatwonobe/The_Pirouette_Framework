import numpy as np
import logging
import sys
import os

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def minimal_memory_ply_export(input_file="phase_space_raw.npz", output_file="pirouette_deep_field.ply"):
    """
    Ultra-lean PLY writer that processes row-by-row to minimize RAM.
    Key insight: We never load the full vertex array into memory.
    """
    
    if not os.path.exists(input_file):
        logger.error(f"FATAL: {input_file} not found.")
        return

    logger.info(f"[1/4] Loading coordinate arrays only...")
    with np.load(input_file) as data:
        # Force copy to owned memory before context closes
        m_vals = np.array(data['m_vals'], dtype=np.float32, copy=True)
        l_vals = np.array(data['l_vals'], dtype=np.float32, copy=True)
        esc_shape = data['escape_time'].shape
    
    rows, cols = esc_shape
    
    # Sanity check
    assert isinstance(m_vals, np.ndarray), f"m_vals corrupted: {type(m_vals)}"
    assert isinstance(l_vals, np.ndarray), f"l_vals corrupted: {type(l_vals)}"
    total_verts = rows * cols
    total_faces = (rows - 1) * (cols - 1) * 2
    
    logger.info(f"      Grid: {rows}x{cols} = {total_verts:,} vertices")
    logger.info(f"      Faces: {total_faces:,}")
    
    # Pre-calculate global normalization parameters
    logger.info("[2/4] Calculating normalization parameters...")
    with np.load(input_file) as data:
        esc_full = data['escape_time']
        max_steps = np.max(esc_full)
        
        # Find natural max for monolith scaling
        Z_temp = np.log1p(esc_full)
        trapped_mask = (esc_full >= max_steps * 0.99)
        natural_max = np.max(Z_temp[~trapped_mask]) if np.any(~trapped_mask) else 1.0
        monolith_height = natural_max * 1.2
        
        # Global Z normalization factor
        Z_temp[trapped_mask] = monolith_height
        z_scale = 3.0 / np.max(Z_temp)
        
        del Z_temp, trapped_mask
    
    logger.info(f"      Max steps: {max_steps}")
    logger.info(f"      Natural max Z: {natural_max:.3f}")
    logger.info(f"      Z scale factor: {z_scale:.6f}")
    
    # --- LOAD ALL NECESSARY DATA FIRST ---
    logger.info("[3/4] Loading data arrays...")
    with np.load(input_file) as data:
        esc_full = np.array(data['escape_time'], copy=True)
        bid_full = np.array(data['basin_id'], copy=True)
    
    # Pre-calculate gradient for rim detection
    logger.info("      Calculating rim gradients...")
    grads = np.gradient(esc_full)
    slope = np.sqrt(grads[0]**2 + grads[1]**2)
    rim_mask = (slope > 5.0) & (slope < 100.0)
    del grads, slope
    
    # --- NOW WRITE FILE ---
    logger.info(f"[4/4] Writing to {output_file}...")
    
    ply_file = open(output_file, 'w', buffering=8192*16)
    
    # Header
    ply_file.write("ply\n")
    ply_file.write("format ascii 1.0\n")
    ply_file.write(f"element vertex {total_verts}\n")
    ply_file.write("property float x\n")
    ply_file.write("property float y\n")
    ply_file.write("property float z\n")
    ply_file.write("property uchar red\n")
    ply_file.write("property uchar green\n")
    ply_file.write("property uchar blue\n")
    ply_file.write(f"element face {total_faces}\n")
    ply_file.write("property list uchar int vertex_index\n")
    ply_file.write("end_header\n")
    
    logger.info("      Streaming vertices row-by-row...")
    
    # Process in row chunks to balance speed vs memory
    chunk_rows = 50  # Process 50 rows at a time
    total_chunks = (rows + chunk_rows - 1) // chunk_rows
    
    for chunk_idx in range(total_chunks):
        start_row = chunk_idx * chunk_rows
        end_row = min(start_row + chunk_rows, rows)
        
        # Progress
        pct = (start_row / rows) * 100
        sys.stdout.write(f"\r      Vertices: {pct:.1f}% ")
        sys.stdout.flush()
        
        # Extract chunk data
        esc_chunk = esc_full[start_row:end_row, :]
        bid_chunk = bid_full[start_row:end_row, :]
        rim_chunk = rim_mask[start_row:end_row, :]
        
        # Calculate Z for chunk
        Z_chunk = np.log1p(esc_chunk)
        trapped_chunk = (esc_chunk >= max_steps * 0.99)
        Z_chunk[trapped_chunk] = monolith_height
        Z_chunk = Z_chunk * z_scale
        
        # Write vertices for this chunk
        for local_row in range(end_row - start_row):
            global_row = start_row + local_row
            y_val = l_vals[global_row]
            
            for col_idx in range(cols):
                x_val = m_vals[col_idx]
                z_val = Z_chunk[local_row, col_idx]
                
                basin = bid_chunk[local_row, col_idx]
                is_rim = rim_chunk[local_row, col_idx]
                is_trapped = trapped_chunk[local_row, col_idx]
                
                # Color selection (optimized with early exits)
                if is_rim and basin != 0:
                    r, g, b = 255, 255, 255  # Rim
                elif basin == 0 or is_trapped:
                    r, g, b = 220, 220, 230  # Tower
                elif basin == 1:
                    r, g, b = 20, 180, 180   # Teal
                elif basin == 3:
                    r, g, b = 200, 50, 40    # Red
                else:
                    r, g, b = 210, 160, 40   # Gold
                
                # Direct write (fastest way)
                ply_file.write(f"{x_val:.4f} {y_val:.4f} {z_val:.4f} {r} {g} {b}\n")
    
    print()  # Newline after progress
    
    # --- WRITE FACES ---
    logger.info("      Writing faces...")
    
    # Write faces in chunks (purely mathematical, no array storage)
    for r in range(rows - 1):
        if r % 100 == 0:
            pct = (r / (rows - 1)) * 100
            sys.stdout.write(f"\r      Faces: {pct:.1f}% ")
            sys.stdout.flush()
        
        for c in range(cols - 1):
            tl = r * cols + c
            tr = tl + 1
            bl = tl + cols
            br = bl + 1
            
            # Write two triangles per quad
            ply_file.write(f"3 {tl} {bl} {tr}\n")
            ply_file.write(f"3 {tr} {bl} {br}\n")
    
    print()
    ply_file.close()
    
    logger.info("✓ DONE. File written successfully.")
    logger.info(f"  Output: {output_file}")
    
    # Report file size
    file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
    logger.info(f"  Size: {file_size_mb:.1f} MB")

if __name__ == "__main__":
    minimal_memory_ply_export()