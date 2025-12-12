import numpy as np
import logging
import sys
import os
import json
import gc

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def minimal_memory_ply_export(input_file="phase_space_raw.npz", output_file="pirouette_deep_field.ply"):
    """
    ULTRA-DEFENSIVE PLY writer with full checkpoint/resume on BOTH vertices AND faces.
    
    This version is designed for hostile Python environments where variables randomly
    get corrupted. We use aggressive variable protection and checkpoint EVERYTHING.
    """
    
    checkpoint_file = output_file + ".checkpoint.json"
    start_row = 0
    start_face_row = 0
    vertices_complete = False
    
    # Check for existing checkpoint
    if os.path.exists(checkpoint_file):
        try:
            with open(checkpoint_file, 'r') as cf:
                checkpoint_data = json.load(cf)
                start_row = checkpoint_data.get('last_completed_row', 0)
                vertices_complete = checkpoint_data.get('vertices_complete', False)
                start_face_row = checkpoint_data.get('last_completed_face_row', 0)
                
                if vertices_complete:
                    logger.info(f"🔄 RESUMING FACES from row {start_face_row}")
                else:
                    logger.info(f"🔄 RESUMING VERTICES from row {start_row}")
        except:
            logger.warning("Checkpoint file corrupted, starting fresh")
            start_row = 0
            vertices_complete = False
            start_face_row = 0
    
    if not os.path.exists(input_file):
        logger.error(f"FATAL: {input_file} not found.")
        return

    logger.info(f"[1/4] Loading coordinate arrays...")
    
    # DEFENSIVE: Load with explicit copy and immediate validation
    with np.load(input_file) as npz_data:
        M_VALS_ARRAY = np.array(npz_data['m_vals'], dtype=np.float32, copy=True)
        L_VALS_ARRAY = np.array(npz_data['l_vals'], dtype=np.float32, copy=True)
        esc_shape = npz_data['escape_time'].shape
    
    # Force garbage collection to free npz file handles
    gc.collect()
    
    ROWS = int(esc_shape[0])
    COLS = int(esc_shape[1])
    
    # DEFENSIVE: Validate types immediately
    assert isinstance(M_VALS_ARRAY, np.ndarray), f"M_VALS corrupted: {type(M_VALS_ARRAY)}"
    assert isinstance(L_VALS_ARRAY, np.ndarray), f"L_VALS corrupted: {type(L_VALS_ARRAY)}"
    assert isinstance(ROWS, int), f"ROWS corrupted: {type(ROWS)}"
    assert isinstance(COLS, int), f"COLS corrupted: {type(COLS)}"
    
    TOTAL_VERTS = ROWS * COLS
    TOTAL_FACES = (ROWS - 1) * (COLS - 1) * 2
    
    logger.info(f"      Grid: {ROWS}x{COLS} = {TOTAL_VERTS:,} vertices")
    logger.info(f"      Faces: {TOTAL_FACES:,}")
    
    # Pre-calculate global normalization parameters
    logger.info("[2/4] Calculating normalization parameters...")
    with np.load(input_file) as npz_data:
        esc_temp = npz_data['escape_time']
        MAX_STEPS = int(np.max(esc_temp))
        
        Z_temp = np.log1p(esc_temp)
        trapped_mask = (esc_temp >= MAX_STEPS * 0.99)
        NATURAL_MAX = float(np.max(Z_temp[~trapped_mask]) if np.any(~trapped_mask) else 1.0)
        MONOLITH_HEIGHT = NATURAL_MAX * 1.2
        
        Z_temp[trapped_mask] = MONOLITH_HEIGHT
        Z_SCALE = 3.0 / float(np.max(Z_temp))
        
        del Z_temp, trapped_mask, esc_temp
    
    gc.collect()
    
    logger.info(f"      Max steps: {MAX_STEPS}")
    logger.info(f"      Natural max Z: {NATURAL_MAX:.3f}")
    logger.info(f"      Z scale factor: {Z_SCALE:.6f}")
    
    # --- LOAD ALL NECESSARY DATA ---
    logger.info("[3/4] Loading data arrays...")
    with np.load(input_file) as npz_data:
        ESC_FULL = np.array(npz_data['escape_time'], copy=True)
        BID_FULL = np.array(npz_data['basin_id'], copy=True)
    
    gc.collect()
    
    # Pre-calculate gradient
    logger.info("      Calculating rim gradients...")
    grads = np.gradient(ESC_FULL)
    slope = np.sqrt(grads[0]**2 + grads[1]**2)
    RIM_MASK = (slope > 5.0) & (slope < 100.0)
    del grads, slope
    
    gc.collect()
    
    # === VERTICES SECTION ===
    if not vertices_complete:
        logger.info(f"[4/4] Writing vertices to {output_file}...")
        
        # Open mode: 'w' if starting fresh, 'a' if resuming
        write_mode = 'a' if start_row > 0 else 'w'
        
        try:
            OUTPUT_FILE_HANDLE = open(output_file, write_mode, buffering=8192*16)
        except Exception as e:
            logger.error(f"Failed to open file: {e}")
            return
        
        # Write header only if starting fresh
        if start_row == 0:
            OUTPUT_FILE_HANDLE.write("ply\n")
            OUTPUT_FILE_HANDLE.write("format ascii 1.0\n")
            OUTPUT_FILE_HANDLE.write(f"element vertex {TOTAL_VERTS}\n")
            OUTPUT_FILE_HANDLE.write("property float x\n")
            OUTPUT_FILE_HANDLE.write("property float y\n")
            OUTPUT_FILE_HANDLE.write("property float z\n")
            OUTPUT_FILE_HANDLE.write("property uchar red\n")
            OUTPUT_FILE_HANDLE.write("property uchar green\n")
            OUTPUT_FILE_HANDLE.write("property uchar blue\n")
            OUTPUT_FILE_HANDLE.write(f"element face {TOTAL_FACES}\n")
            OUTPUT_FILE_HANDLE.write("property list uchar int vertex_index\n")
            OUTPUT_FILE_HANDLE.write("end_header\n")
        
        logger.info(f"      Processing from row {start_row}/{ROWS}...")
        
        CHUNK_ROWS = 50
        CHECKPOINT_INTERVAL = 2  # More frequent checkpoints
        
        chunk_start_idx = start_row // CHUNK_ROWS
        total_chunks = (ROWS + CHUNK_ROWS - 1) // CHUNK_ROWS
        
        try:
            for chunk_idx in range(chunk_start_idx, total_chunks):
                # DEFENSIVE: Re-validate critical variables at loop start
                assert isinstance(M_VALS_ARRAY, np.ndarray), "M_VALS corrupted in loop"
                assert isinstance(L_VALS_ARRAY, np.ndarray), "L_VALS corrupted in loop"
                
                start_row_chunk = chunk_idx * CHUNK_ROWS
                end_row_chunk = min(start_row_chunk + CHUNK_ROWS, ROWS)
                actual_start = max(start_row_chunk, start_row)
                
                pct = (start_row_chunk / ROWS) * 100
                sys.stdout.write(f"\r      Vertices: {pct:.1f}% (chunk {chunk_idx+1}/{total_chunks}) ")
                sys.stdout.flush()
                
                # Extract chunk
                esc_chunk = ESC_FULL[start_row_chunk:end_row_chunk, :]
                bid_chunk = BID_FULL[start_row_chunk:end_row_chunk, :]
                rim_chunk = RIM_MASK[start_row_chunk:end_row_chunk, :]
                
                # Calculate Z
                Z_chunk = np.log1p(esc_chunk)
                trapped_chunk = (esc_chunk >= MAX_STEPS * 0.99)
                Z_chunk[trapped_chunk] = MONOLITH_HEIGHT
                Z_chunk = Z_chunk * Z_SCALE
                
                # DEFENSIVE: Convert to list to avoid numpy weirdness
                rows_to_process = list(range(actual_start, end_row_chunk))
                
                for GLOBAL_ROW in rows_to_process:
                    LOCAL_ROW = GLOBAL_ROW - start_row_chunk
                    Y_VALUE = float(L_VALS_ARRAY[GLOBAL_ROW])
                    
                    # DEFENSIVE: Convert column range to list
                    cols_to_process = list(range(COLS))
                    
                    for COL_INDEX in cols_to_process:
                        # DEFENSIVE: Extract values one at a time with explicit types
                        X_VALUE = float(M_VALS_ARRAY[COL_INDEX])
                        Z_VALUE = float(Z_chunk[LOCAL_ROW, COL_INDEX])
                        
                        BASIN = int(bid_chunk[LOCAL_ROW, COL_INDEX])
                        IS_RIM = bool(rim_chunk[LOCAL_ROW, COL_INDEX])
                        IS_TRAPPED = bool(trapped_chunk[LOCAL_ROW, COL_INDEX])
                        
                        # Color selection
                        if IS_RIM and BASIN != 0:
                            R, G, B = 255, 255, 255
                        elif BASIN == 0 or IS_TRAPPED:
                            R, G, B = 220, 220, 230
                        elif BASIN == 1:
                            R, G, B = 20, 180, 180
                        elif BASIN == 3:
                            R, G, B = 200, 50, 40
                        else:
                            R, G, B = 210, 160, 40
                        
                        # Write with explicit string formatting
                        line = f"{X_VALUE:.4f} {Y_VALUE:.4f} {Z_VALUE:.4f} {R} {G} {B}\n"
                        OUTPUT_FILE_HANDLE.write(line)
                
                # CHECKPOINT
                if (chunk_idx + 1) % CHECKPOINT_INTERVAL == 0:
                    OUTPUT_FILE_HANDLE.flush()
                    with open(checkpoint_file, 'w') as cf:
                        json.dump({
                            'last_completed_row': end_row_chunk,
                            'vertices_complete': False,
                            'last_completed_face_row': 0
                        }, cf)
                    logger.info(f"\n      💾 Checkpoint saved at row {end_row_chunk}")
            
            print()
            OUTPUT_FILE_HANDLE.flush()
            
            # Mark vertices complete
            with open(checkpoint_file, 'w') as cf:
                json.dump({
                    'last_completed_row': ROWS,
                    'vertices_complete': True,
                    'last_completed_face_row': 0
                }, cf)
            
            logger.info("      ✓ All vertices written")
            
        except Exception as e:
            logger.error(f"\n💥 VERTEX CRASH: {e}")
            OUTPUT_FILE_HANDLE.flush()
            OUTPUT_FILE_HANDLE.close()
            
            with open(checkpoint_file, 'w') as cf:
                json.dump({
                    'last_completed_row': start_row_chunk,
                    'vertices_complete': False,
                    'last_completed_face_row': 0
                }, cf)
            
            logger.error(f"Emergency checkpoint at row {start_row_chunk}")
            logger.error("Run script again to resume")
            raise
    
    else:
        logger.info(f"[4/4] Vertices already complete, opening file for faces...")
        try:
            OUTPUT_FILE_HANDLE = open(output_file, 'a', buffering=8192*16)
        except Exception as e:
            logger.error(f"Failed to open file: {e}")
            return
    
    # === FACES SECTION ===
    logger.info(f"      Writing faces from row {start_face_row}/{ROWS-1}...")
    
    FACE_CHECKPOINT_INTERVAL = 100  # Checkpoint every 100 rows
    
    try:
        # DEFENSIVE: Use explicit range list
        face_rows_to_process = list(range(start_face_row, ROWS - 1))
        
        for FACE_ROW in face_rows_to_process:
            if FACE_ROW % 50 == 0:
                pct = (FACE_ROW / (ROWS - 1)) * 100
                sys.stdout.write(f"\r      Faces: {pct:.1f}% ")
                sys.stdout.flush()
            
            # DEFENSIVE: Use explicit range list for columns
            face_cols_to_process = list(range(COLS - 1))
            
            for FACE_COL in face_cols_to_process:
                TL = FACE_ROW * COLS + FACE_COL
                TR = TL + 1
                BL = TL + COLS
                BR = BL + 1
                
                # Write triangles
                OUTPUT_FILE_HANDLE.write(f"3 {TL} {BL} {TR}\n")
                OUTPUT_FILE_HANDLE.write(f"3 {TR} {BL} {BR}\n")
            
            # CHECKPOINT faces
            if (FACE_ROW + 1) % FACE_CHECKPOINT_INTERVAL == 0:
                OUTPUT_FILE_HANDLE.flush()
                with open(checkpoint_file, 'w') as cf:
                    json.dump({
                        'last_completed_row': ROWS,
                        'vertices_complete': True,
                        'last_completed_face_row': FACE_ROW + 1
                    }, cf)
        
        print()
        OUTPUT_FILE_HANDLE.flush()
        OUTPUT_FILE_HANDLE.close()
        
        # SUCCESS - delete checkpoint
        if os.path.exists(checkpoint_file):
            os.remove(checkpoint_file)
            logger.info("      ✓ Checkpoint deleted (completed)")
        
        logger.info("✓ DONE. File written successfully.")
        logger.info(f"  Output: {output_file}")
        
        file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
        logger.info(f"  Size: {file_size_mb:.1f} MB")
        
    except Exception as e:
        logger.error(f"\n💥 FACE CRASH: {e}")
        OUTPUT_FILE_HANDLE.flush()
        OUTPUT_FILE_HANDLE.close()
        
        with open(checkpoint_file, 'w') as cf:
            json.dump({
                'last_completed_row': ROWS,
                'vertices_complete': True,
                'last_completed_face_row': FACE_ROW
            }, cf)
        
        logger.error(f"Emergency checkpoint at face row {FACE_ROW}")
        logger.error("Run script again to resume")
        raise

if __name__ == "__main__":
    minimal_memory_ply_export()