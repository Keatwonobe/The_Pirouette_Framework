import numpy as np
import logging
import sys
import os
import gc

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def vectorized_ply_export(input_file="phase_space_raw.npz", output_file="pirouette_deep_field.ply"):
    
    # --- STEP 1: LOAD DATA ---
    if not os.path.exists(input_file):
        logger.error(f"FATAL: {input_file} not found.")
        return

    logger.info(f"[1/4] Loading Data into RAM...")
    with np.load(input_file) as data:
        # Load and cast to ensure we own the memory
        m_vals = data['m_vals'].astype(np.float32)
        l_vals = data['l_vals'].astype(np.float32)
        esc = data['escape_time']
        bid = data['basin_id']

    rows, cols = esc.shape
    total_verts = rows * cols
    total_faces = (rows - 1) * (cols - 1) * 2
    
    logger.info(f"      Grid: {rows}x{cols}")
    logger.info(f"      Vertices: {total_verts:,}")

    # --- STEP 2: VECTORIZED CALCULATION (No Loops) ---
    logger.info("[2/4] Vectorizing Geometry & Colors (This may take RAM)...")
    
    # A. Geometry (Meshgrid + Flatten)
    # This creates the full coordinate arrays instantly
    M_grid, L_grid = np.meshgrid(m_vals, l_vals)
    M_flat = M_grid.ravel()
    L_flat = L_grid.ravel()
    
    # Free grid memory immediately
    del M_grid, L_grid
    gc.collect()

    # B. Height (Z)
    esc_flat = esc.ravel()
    bid_flat = bid.ravel()
    
    max_steps = np.max(esc_flat)
    Z_flat = np.log1p(esc_flat)
    
    # Monolith Logic
    trapped_mask = (esc_flat >= max_steps * 0.99)
    natural_max = np.max(Z_flat[~trapped_mask]) if np.any(~trapped_mask) else 1.0
    Z_flat[trapped_mask] = natural_max * 1.2
    
    # Normalize Z
    Z_flat = Z_flat / np.max(Z_flat) * 3.0
    
    # C. Colors (Vectorized Masking)
    # Initialize all to Gold (2)
    # We use a structured array or just a flat (N, 3) uint8 array
    Colors = np.zeros((total_verts, 3), dtype=np.uint8)
    Colors[:] = [210, 160, 40] # Default Gold
    
    # Masks
    mask_tower = (bid_flat == 0) | trapped_mask
    mask_teal  = (bid_flat == 1) & ~trapped_mask
    mask_red   = (bid_flat == 3) & ~trapped_mask
    
    # Apply Colors
    Colors[mask_tower] = [220, 220, 230] # Silver
    Colors[mask_teal]  = [20, 180, 180]  # Teal
    Colors[mask_red]   = [200, 50, 40]   # Red
    
    # Rim Highlighting (Gradient)
    # We calculate gradient on the 2D array before flattening for correctness
    grads = np.gradient(esc)
    slope = np.sqrt(grads[0]**2 + grads[1]**2)
    mask_rim = ((slope > 5.0) & (slope < 100.0)).ravel()
    
    # Apply Rim White (Overwrites previous colors)
    # Don't paint the tower white, only the edges leading to it
    mask_rim_valid = mask_rim & (bid_flat != 0)
    Colors[mask_rim_valid] = [255, 255, 255]

    # Clean up source arrays
    del esc, bid, grads, slope, mask_tower, mask_teal, mask_red, mask_rim, mask_rim_valid
    gc.collect()

    # --- STEP 3: WRITE VERTICES (Chunked) ---
    logger.info(f"[3/4] Streaming Vertices to {output_file}...")
    
    try:
        with open(output_file, 'w') as f:
            # Header
            f.write("ply\n")
            f.write("format ascii 1.0\n")
            f.write(f"element vertex {total_verts}\n")
            f.write("property float x\n")
            f.write("property float y\n")
            f.write("property float z\n")
            f.write("property uchar red\n")
            f.write("property uchar green\n")
            f.write("property uchar blue\n")
            f.write(f"element face {total_faces}\n")
            f.write("property list uchar int vertex_index\n")
            f.write("end_header\n")
            
            # Write Vertices in Chunks using numpy savetxt logic
            chunk_size = 100000
            total_chunks = (total_verts // chunk_size) + 1
            
            for i in range(total_chunks):
                start = i * chunk_size
                end = min((i + 1) * chunk_size, total_verts)
                if start >= end: break
                
                if i % 5 == 0:
                    sys.stdout.write(f"\r      Vertex Chunk {i+1}/{total_chunks}")
                    sys.stdout.flush()
                
                # Combine into one array for savetxt: [X, Y, Z, R, G, B]
                # Note: This creates a temporary copy, but only for the chunk size.
                chunk_data = np.column_stack((
                    M_flat[start:end], 
                    L_flat[start:end], 
                    Z_flat[start:end], 
                    Colors[start:end]
                ))
                
                # Write chunk
                # Format: float float float int int int
                np.savetxt(f, chunk_data, fmt='%.4f %.4f %.4f %d %d %d')
            
            print() # Newline

            # --- STEP 4: WRITE FACES (Calculated & Chunked) ---
            logger.info("[4/4] Generating & Writing Faces...")
            
            # We generate face indices mathematically to avoid storing them
            # Grid logic:
            # TL(i,j) -- TR(i,j+1)
            # |          |
            # BL(i+1,j)- BR(i+1,j+1)
            
            # Indices for the top-left corners of all quads
            # We exclude the last row and last col
            r_idx = np.arange(rows - 1)
            c_idx = np.arange(cols - 1)
            R, C = np.meshgrid(r_idx, c_idx, indexing='ij')
            
            # Flatten to list of "Top-Left" indices
            tl = (R * cols + C).ravel()
            tr = tl + 1
            bl = tl + cols
            br = bl + 1
            
            # Free meshgrid memory
            del R, C
            gc.collect()
            
            num_quads = len(tl)
            face_chunk_size = 100000
            total_face_chunks = (num_quads // face_chunk_size) + 1
            
            for i in range(total_face_chunks):
                start = i * face_chunk_size
                end = min((i + 1) * face_chunk_size, num_quads)
                if start >= end: break

                if i % 5 == 0:
                    sys.stdout.write(f"\r      Face Chunk {i+1}/{total_face_chunks}")
                    sys.stdout.flush()

                # Get indices for this chunk
                tl_c = tl[start:end]
                tr_c = tr[start:end]
                bl_c = bl[start:end]
                br_c = br[start:end]
                
                # Interleave triangles: (tl, bl, tr) and (tr, bl, br)
                # We construct a (N, 4) array for savetxt where col 0 is '3' (tri count)
                
                # Tri 1
                ones = np.ones_like(tl_c) * 3
                tri1 = np.column_stack((ones, tl_c, bl_c, tr_c))
                
                # Tri 2
                tri2 = np.column_stack((ones, tr_c, bl_c, br_c))
                
                # Interleave or just write sequentially
                # Sequential writing is fine for PLY, order doesn't matter for topology usually,
                # but let's just dump tri1 then tri2 to keep it simple and fast.
                
                np.savetxt(f, tri1, fmt='%d %d %d %d')
                np.savetxt(f, tri2, fmt='%d %d %d %d')

            print()

    except Exception as e:
        logger.error(f"Write failed: {e}")
        return

    logger.info("DONE. File saved successfully.")

if __name__ == "__main__":
    vectorized_ply_export()