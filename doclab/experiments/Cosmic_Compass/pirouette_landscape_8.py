import numpy as np
import logging
import sys
import os
import json
import gc

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# --- CONFIGURATION ---
# Vertical Exaggeration. 
# Since we are using Log scaling, higher numbers here preserve the "spire" look.
HEIGHT_SCALE = 15.0 
# ---------------------

def minimal_memory_ply_export(input_file="phase_space_raw.npz", output_file="pirouette_raw_log_3.ply"):
    """
    PURE LOGARITHMIC EXPORT.
    No artificial caps. No "Monolith" flattening.
    Maps Z directly to log(escape_time).
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
    with np.load(input_file) as npz_data:
        M_VALS_ARRAY = np.array(npz_data['m_vals'], dtype=np.float32, copy=True)
        L_VALS_ARRAY = np.array(npz_data['l_vals'], dtype=np.float32, copy=True)
        esc_shape = npz_data['escape_time'].shape
    gc.collect()
    
    ROWS = int(esc_shape[0])
    COLS = int(esc_shape[1])
    TOTAL_VERTS = ROWS * COLS
    TOTAL_FACES = (ROWS - 1) * (COLS - 1) * 2
    
    logger.info(f"      Grid: {ROWS}x{COLS} = {TOTAL_VERTS:,} vertices")

    # --- CALCULATE GLOBAL SCALING ---
    logger.info("[2/4] Calculating Logarithmic Scaling...")
    with np.load(input_file) as npz_data:
        esc_temp = npz_data['escape_time']
        MAX_STEPS = int(np.max(esc_temp))
        
        # PURE LOG SCALE: log(1 + steps)
        # This naturally compresses the huge values but preserves the "spike"
        Z_temp = np.log1p(esc_temp)
        MAX_Z_LOG = np.max(Z_temp)
        
        # Normalization factor to hit our target HEIGHT_SCALE
        Z_MULT = HEIGHT_SCALE / MAX_Z_LOG
        
        del Z_temp, esc_temp
    gc.collect()
    
    logger.info(f"      Max steps in data: {MAX_STEPS}")
    logger.info(f"      Log Scale Multiplier: {Z_MULT:.4f}")
    
    # --- LOAD DATA ---
    logger.info("[3/4] Loading data arrays...")
    with np.load(input_file) as npz_data:
        ESC_FULL = np.array(npz_data['escape_time'], copy=True)
        BID_FULL = np.array(npz_data['basin_id'], copy=True)
    gc.collect()
    
    # Gradient for Rim
    logger.info("      Calculating rim gradients...")
    grads = np.gradient(ESC_FULL)
    slope = np.sqrt(grads[0]**2 + grads[1]**2)
    RIM_MASK = (slope > 5.0) & (slope < 100.0)
    del grads, slope
    gc.collect()
    
    # === VERTICES SECTION ===
    if not vertices_complete:
        logger.info(f"[4/4] Writing vertices to {output_file}...")
        write_mode = 'a' if start_row > 0 else 'w'
        try:
            OUTPUT_FILE_HANDLE = open(output_file, write_mode, buffering=8192*16)
        except Exception as e:
            logger.error(f"Failed to open file: {e}")
            return
        
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
        
        CHUNK_ROWS = 50
        CHECKPOINT_INTERVAL = 2
        chunk_start_idx = start_row // CHUNK_ROWS
        total_chunks = (ROWS + CHUNK_ROWS - 1) // CHUNK_ROWS
        
        try:
            for chunk_idx in range(chunk_start_idx, total_chunks):
                start_row_chunk = chunk_idx * CHUNK_ROWS
                end_row_chunk = min(start_row_chunk + CHUNK_ROWS, ROWS)
                actual_start = max(start_row_chunk, start_row)
                
                pct = (start_row_chunk / ROWS) * 100
                sys.stdout.write(f"\r      Vertices: {pct:.1f}% (chunk {chunk_idx+1}/{total_chunks}) ")
                sys.stdout.flush()
                
                esc_chunk = ESC_FULL[start_row_chunk:end_row_chunk, :]
                bid_chunk = BID_FULL[start_row_chunk:end_row_chunk, :]
                rim_chunk = RIM_MASK[start_row_chunk:end_row_chunk, :]
                
                # --- Z CALCULATION ---
                # Pure log mapping. No clamping.
                Z_chunk = np.log1p(esc_chunk) * Z_MULT
                
                rows_to_process = list(range(actual_start, end_row_chunk))
                
                for GLOBAL_ROW in rows_to_process:
                    LOCAL_ROW = GLOBAL_ROW - start_row_chunk
                    Y_VALUE = float(L_VALS_ARRAY[GLOBAL_ROW])
                    cols_to_process = list(range(COLS))
                    
                    for COL_INDEX in cols_to_process:
                        X_VALUE = float(M_VALS_ARRAY[COL_INDEX])
                        Z_VALUE = float(Z_chunk[LOCAL_ROW, COL_INDEX])
                        
                        BASIN = int(bid_chunk[LOCAL_ROW, COL_INDEX])
                        IS_RIM = bool(rim_chunk[LOCAL_ROW, COL_INDEX])
                        STEPS = int(esc_chunk[LOCAL_ROW, COL_INDEX])
                        
                        # --- COLORING STRATEGY ---
                        if STEPS >= MAX_STEPS * 0.99:
                            # THE VOID: Points that hit the simulation limit
                            R, G, B = 10, 10, 10 
                        elif IS_RIM and BASIN != 0:
                            R, G, B = 255, 255, 255
                        elif BASIN == 0:
                            R, G, B = 220, 220, 230
                        elif BASIN == 1:
                            R, G, B = 20, 180, 180
                        elif BASIN == 3:
                            R, G, B = 200, 50, 40
                        else:
                            R, G, B = 210, 160, 40
                        
                        OUTPUT_FILE_HANDLE.write(f"{X_VALUE:.4f} {Y_VALUE:.4f} {Z_VALUE:.4f} {R} {G} {B}\n")
                
                if (chunk_idx + 1) % CHECKPOINT_INTERVAL == 0:
                    OUTPUT_FILE_HANDLE.flush()
                    with open(checkpoint_file, 'w') as cf:
                        json.dump({
                            'last_completed_row': end_row_chunk,
                            'vertices_complete': False,
                            'last_completed_face_row': 0
                        }, cf)
            
            print()
            OUTPUT_FILE_HANDLE.flush()
            with open(checkpoint_file, 'w') as cf:
                json.dump({
                    'last_completed_row': ROWS,
                    'vertices_complete': True,
                    'last_completed_face_row': 0
                }, cf)
            
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
            raise
    
    else:
        logger.info(f"[4/4] Vertices already complete, opening file for faces...")
        try:
            OUTPUT_FILE_HANDLE = open(output_file, 'a', buffering=8192*16)
        except Exception as e:
            logger.error(f"Failed to open file: {e}")
            return

    # === FACES SECTION (Standard) ===
    logger.info(f"      Writing faces from row {start_face_row}/{ROWS-1}...")
    FACE_CHECKPOINT_INTERVAL = 100
    try:
        face_rows_to_process = list(range(start_face_row, ROWS - 1))
        for FACE_ROW in face_rows_to_process:
            if FACE_ROW % 50 == 0:
                pct = (FACE_ROW / (ROWS - 1)) * 100
                sys.stdout.write(f"\r      Faces: {pct:.1f}% ")
                sys.stdout.flush()
            face_cols_to_process = list(range(COLS - 1))
            for FACE_COL in face_cols_to_process:
                TL = FACE_ROW * COLS + FACE_COL
                TR = TL + 1
                BL = TL + COLS
                BR = BL + 1
                OUTPUT_FILE_HANDLE.write(f"3 {TL} {BL} {TR}\n")
                OUTPUT_FILE_HANDLE.write(f"3 {TR} {BL} {BR}\n")
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
        if os.path.exists(checkpoint_file):
            os.remove(checkpoint_file)
        logger.info("✓ DONE.")
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
        raise

if __name__ == "__main__":
    minimal_memory_ply_export()