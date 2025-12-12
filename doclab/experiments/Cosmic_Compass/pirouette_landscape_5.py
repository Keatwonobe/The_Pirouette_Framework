import numpy as np
import logging
import sys
import os
import json

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def minimal_memory_ply_export(input_file="phase_space_raw.npz", output_file="pirouette_deep_field.ply"):
    """
    Ultra-lean PLY writer with CHECKPOINT/RESUME capability.
    
    CHECKPOINT SYSTEM:
    - Saves progress every 5 chunks to .checkpoint.json
    - On crash/restart, resumes from last saved row
    - Auto-deletes checkpoint on successful completion
    - If you get 1% per run, you'll finish in ~100 runs max
    """
    
    checkpoint_file = output_file + ".checkpoint.json"
    start_row = 0
    
    # Check for existing checkpoint
    if os.path.exists(checkpoint_file):
        try:
            with open(checkpoint_file, 'r') as cf:
                checkpoint_data = json.load(cf)
                start_row = checkpoint_data.get('last_completed_row', 0)
                logger.info(f"🔄 RESUMING from row {start_row} (checkpoint found)")
        except:
            logger.warning("Checkpoint file corrupted, starting fresh")
            start_row = 0
    
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
    
    # Open mode: 'w' if starting fresh, 'a' if resuming
    write_mode = 'a' if start_row > 0 else 'w'
    ply_file = open(output_file, write_mode, buffering=8192*16)
    
    # Write header only if starting fresh
    if start_row == 0:
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
    
    logger.info(f"      Streaming vertices from row {start_row}/{rows}...")
    
    # Process in row chunks to balance speed vs memory
    chunk_rows = 50  # Process 50 rows at a time
    checkpoint_interval = 2  # Save checkpoint every 5 chunks
    
    chunk_start_idx = start_row // chunk_rows
    total_chunks = (rows + chunk_rows - 1) // chunk_rows
    
    try:
        for chunk_idx in range(chunk_start_idx, total_chunks):
            start_row_chunk = chunk_idx * chunk_rows
            end_row_chunk = min(start_row_chunk + chunk_rows, rows)
            
            # Skip to exact resume point if mid-chunk
            actual_start = max(start_row_chunk, start_row)
            
            # Progress
            pct = (start_row_chunk / rows) * 100
            sys.stdout.write(f"\r      Vertices: {pct:.1f}% (chunk {chunk_idx+1}/{total_chunks}) ")
            sys.stdout.flush()
            
            # Extract chunk data
            esc_chunk = esc_full[start_row_chunk:end_row_chunk, :]
            bid_chunk = bid_full[start_row_chunk:end_row_chunk, :]
            rim_chunk = rim_mask[start_row_chunk:end_row_chunk, :]
            
            # Calculate Z for chunk
            Z_chunk = np.log1p(esc_chunk)
            trapped_chunk = (esc_chunk >= max_steps * 0.99)
            Z_chunk[trapped_chunk] = monolith_height
            Z_chunk = Z_chunk * z_scale
            
            # Write vertices for this chunk
            for global_row in range(actual_start, end_row_chunk):
                local_row = global_row - start_row_chunk
                y_val = l_vals[global_row]
                
                for col_idx in range(cols):
                    x_val = m_vals[col_idx]
                    z_val = Z_chunk[local_row, col_idx]
                    
                    basin = bid_chunk[local_row, col_idx]
                    is_rim = rim_chunk[local_row, col_idx]
                    is_trapped = trapped_chunk[local_row, col_idx]
                    
                    # Color selection
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
                    
                    # Direct write
                    ply_file.write(f"{x_val:.4f} {y_val:.4f} {z_val:.4f} {r} {g} {b}\n")
            
            # CHECKPOINT: Save progress every N chunks
            if (chunk_idx + 1) % checkpoint_interval == 0:
                ply_file.flush()  # Force write to disk
                with open(checkpoint_file, 'w') as cf:
                    json.dump({'last_completed_row': end_row_chunk}, cf)
                logger.info(f"\n      💾 Checkpoint saved at row {end_row_chunk}")
        
        print()  # Newline after progress
        
        # --- WRITE FACES ---
        logger.info("      Writing faces...")
        
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
        
        # SUCCESS: Delete checkpoint
        if os.path.exists(checkpoint_file):
            os.remove(checkpoint_file)
            logger.info("      ✓ Checkpoint deleted (completed successfully)")
        
        logger.info("✓ DONE. File written successfully.")
        logger.info(f"  Output: {output_file}")
        
        # Report file size
        file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
        logger.info(f"  Size: {file_size_mb:.1f} MB")
        
    except Exception as e:
        # CRASH: Ensure checkpoint is saved
        logger.error(f"\n\n💥 CRASH DETECTED: {e}")
        ply_file.flush()
        ply_file.close()
        
        # Save emergency checkpoint
        with open(checkpoint_file, 'w') as cf:
            json.dump({'last_completed_row': start_row_chunk}, cf)
        
        logger.error(f"Emergency checkpoint saved at row {start_row_chunk}")
        logger.error("Run script again to resume from this point")
        raise

if __name__ == "__main__":
    minimal_memory_ply_export()