"""
SUSTAINED OPERATION STRESS TEST
================================
Your Python is healthy in isolation, but crashes under sustained load.
This test mimics the EXACT runtime conditions of your PLY writer.

We're testing:
- Long-running loops (90+ minutes)
- Sustained file writes
- Large array access patterns
- Memory pressure over time
"""

import numpy as np
import time
import gc
import sys
import psutil
import traceback

print("="*70)
print("SUSTAINED OPERATION STRESS TEST")
print("="*70)
print()

# Simulate your actual workload
print("[SETUP] Creating test data matching your actual grid...")
ROWS = 4000
COLS = 4000
CHUNK_SIZE = 50

# Create test npz file
print("  Creating 16M vertex test dataset...")
test_m = np.linspace(-6, 6, COLS).astype(np.float32)
test_l = np.linspace(-5.8, 6.2, ROWS).astype(np.float32)
test_esc = np.random.randint(0, 1200, size=(ROWS, COLS), dtype=np.uint16)
test_bid = np.random.randint(0, 4, size=(ROWS, COLS), dtype=np.uint8)

np.savez_compressed('stress_test_data.npz',
                    m_vals=test_m, l_vals=test_l,
                    escape_time=test_esc, basin_id=test_bid)

print("  ✓ Test data created")
print()

# Track crashes
crash_log = []

def log_state(msg, chunk_idx):
    mem = psutil.virtual_memory()
    proc = psutil.Process()
    print(f"[{chunk_idx:3d}] {msg} | RAM: {mem.percent:.1f}% | Process: {proc.memory_info().rss / (1024**3):.2f} GB")

print("[TEST] Starting sustained write operation...")
print(f"  Total chunks to process: {ROWS // CHUNK_SIZE}")
print(f"  This will take ~5-10 minutes to complete")
print()

start_time = time.time()

try:
    # EXACTLY MIMIC YOUR FORTRESS CODE STRUCTURE
    
    # Load coordinates FIRST
    with np.load('stress_test_data.npz') as data:
        M_VALS_ARRAY = np.array(data['m_vals'], dtype=np.float32, copy=True)
        L_VALS_ARRAY = np.array(data['l_vals'], dtype=np.float32, copy=True)
    
    gc.collect()
    
    # Load full arrays
    with np.load('stress_test_data.npz') as data:
        ESC_FULL = np.array(data['escape_time'], copy=True)
        BID_FULL = np.array(data['basin_id'], copy=True)
    
    gc.collect()
    
    # Calculate gradient
    grads = np.gradient(ESC_FULL)
    slope = np.sqrt(grads[0]**2 + grads[1]**2)
    RIM_MASK = (slope > 5.0) & (slope < 100.0)
    del grads, slope
    gc.collect()
    
    # Constants
    MAX_STEPS = 1200
    NATURAL_MAX = 7.08
    MONOLITH_HEIGHT = 8.496
    Z_SCALE = 0.353106
    
    # Open output file
    OUTPUT_FILE = open('stress_test_output.ply', 'w', buffering=8192*16)
    
    # Write header
    OUTPUT_FILE.write("ply\n")
    OUTPUT_FILE.write("format ascii 1.0\n")
    OUTPUT_FILE.write(f"element vertex {ROWS*COLS}\n")
    OUTPUT_FILE.write("property float x\n")
    OUTPUT_FILE.write("property float y\n")
    OUTPUT_FILE.write("property float z\n")
    OUTPUT_FILE.write("property uchar red\n")
    OUTPUT_FILE.write("property uchar green\n")
    OUTPUT_FILE.write("property uchar blue\n")
    OUTPUT_FILE.write("end_header\n")
    
    total_chunks = ROWS // CHUNK_SIZE
    
    # Main loop - EXACTLY like your code
    for chunk_idx in range(total_chunks):
        start_row = chunk_idx * CHUNK_SIZE
        end_row = min(start_row + CHUNK_SIZE, ROWS)
        
        # Progress every 10 chunks
        if chunk_idx % 10 == 0:
            log_state("Processing chunk", chunk_idx)
        
        # TYPE CHECK - detect corruption early
        if chunk_idx % 20 == 0:
            assert isinstance(M_VALS_ARRAY, np.ndarray), f"CORRUPTION at chunk {chunk_idx}: M_VALS = {type(M_VALS_ARRAY)}"
            assert isinstance(L_VALS_ARRAY, np.ndarray), f"CORRUPTION at chunk {chunk_idx}: L_VALS = {type(L_VALS_ARRAY)}"
            assert isinstance(ESC_FULL, np.ndarray), f"CORRUPTION at chunk {chunk_idx}: ESC_FULL = {type(ESC_FULL)}"
        
        # Extract chunk
        try:
            esc_chunk = ESC_FULL[start_row:end_row, :]
            bid_chunk = BID_FULL[start_row:end_row, :]
            rim_chunk = RIM_MASK[start_row:end_row, :]
        except Exception as e:
            crash_log.append({
                'chunk': chunk_idx,
                'phase': 'chunk_extraction',
                'error': str(e),
                'types': {
                    'ESC_FULL': str(type(ESC_FULL)),
                    'BID_FULL': str(type(BID_FULL)),
                    'RIM_MASK': str(type(RIM_MASK))
                }
            })
            raise
        
        # Calculate Z
        Z_chunk = np.log1p(esc_chunk)
        trapped_chunk = (esc_chunk >= MAX_STEPS * 0.99)
        Z_chunk[trapped_chunk] = MONOLITH_HEIGHT
        Z_chunk = Z_chunk * Z_SCALE
        
        # Write vertices
        for GLOBAL_ROW in range(start_row, end_row):
            LOCAL_ROW = GLOBAL_ROW - start_row
            
            try:
                Y_VALUE = float(L_VALS_ARRAY[GLOBAL_ROW])
            except Exception as e:
                crash_log.append({
                    'chunk': chunk_idx,
                    'row': GLOBAL_ROW,
                    'phase': 'L_VALS_access',
                    'error': str(e),
                    'L_VALS_type': str(type(L_VALS_ARRAY))
                })
                raise
            
            for COL_INDEX in range(COLS):
                try:
                    X_VALUE = float(M_VALS_ARRAY[COL_INDEX])
                    Z_VALUE = float(Z_chunk[LOCAL_ROW, COL_INDEX])
                    BASIN = int(bid_chunk[LOCAL_ROW, COL_INDEX])
                    IS_RIM = bool(rim_chunk[LOCAL_ROW, COL_INDEX])
                    IS_TRAPPED = bool(trapped_chunk[LOCAL_ROW, COL_INDEX])
                except Exception as e:
                    crash_log.append({
                        'chunk': chunk_idx,
                        'row': GLOBAL_ROW,
                        'col': COL_INDEX,
                        'phase': 'variable_access',
                        'error': str(e),
                        'types': {
                            'M_VALS_ARRAY': str(type(M_VALS_ARRAY)),
                            'Z_chunk': str(type(Z_chunk)),
                            'trapped_chunk': str(type(trapped_chunk))
                        }
                    })
                    raise
                
                # Color
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
                
                # Write
                try:
                    OUTPUT_FILE.write(f"{X_VALUE:.4f} {Y_VALUE:.4f} {Z_VALUE:.4f} {R} {G} {B}\n")
                except Exception as e:
                    crash_log.append({
                        'chunk': chunk_idx,
                        'phase': 'file_write',
                        'error': str(e)
                    })
                    raise
        
        # Periodic flush
        if chunk_idx % 5 == 0:
            OUTPUT_FILE.flush()
        
        # Periodic GC
        if chunk_idx % 10 == 0:
            gc.collect()
    
    OUTPUT_FILE.close()
    
    elapsed = time.time() - start_time
    print()
    print("="*70)
    print("✓ STRESS TEST PASSED!")
    print(f"  Time: {elapsed/60:.1f} minutes")
    print(f"  Vertices written: {ROWS * COLS:,}")
    print("="*70)
    
except Exception as e:
    elapsed = time.time() - start_time
    print()
    print("="*70)
    print("✗ CRASH DETECTED!")
    print(f"  Time: {elapsed/60:.1f} minutes")
    print(f"  Chunk: {chunk_idx}/{total_chunks}")
    print(f"  Error: {e}")
    print("="*70)
    print()
    print("CRASH DETAILS:")
    if crash_log:
        for entry in crash_log:
            print(f"  {entry}")
    print()
    traceback.print_exc()
    print()
    print("="*70)
    print("DIAGNOSIS:")
    print("="*70)
    
    error_str = str(e).lower()
    
    if 'not subscriptable' in error_str:
        print("💡 VARIABLE CORRUPTION DETECTED")
        print("   This happens when Python's internals get confused")
        print("   under sustained memory pressure.")
        print()
        print("   LIKELY CAUSES:")
        print("   1. Windows memory management issues")
        print("   2. Python GC bugs under sustained load")
        print("   3. NumPy/Python interaction edge cases")
        print()
        print("   RECOMMENDATIONS:")
        print("   A. Reduce CHUNK_SIZE to 25 or 10")
        print("   B. Force gc.collect() every chunk")
        print("   C. Use smaller grid (2000x2000) if possible")
        print("   D. Run on Linux if available (better memory management)")
    
    elif 'out of bounds' in error_str or 'index' in error_str:
        print("💡 INDEX CORRUPTION DETECTED")
        print("   Loop variables got corrupted during execution")
        print()
        print("   RECOMMENDATIONS:")
        print("   A. This is a Python interpreter bug under load")
        print("   B. Try Python 3.12 or 3.10 (different versions)")
        print("   C. Reduce chunk size")
    
    else:
        print(f"💡 UNKNOWN ERROR: {e}")
        print("   Check crash log above for details")

finally:
    # Cleanup
    try:
        OUTPUT_FILE.close()
    except:
        pass
    
    import os
    if os.path.exists('stress_test_data.npz'):
        os.remove('stress_test_data.npz')
    if os.path.exists('stress_test_output.ply'):
        os.remove('stress_test_output.ply')