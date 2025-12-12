"""
MINIMAL REPRODUCTION TEST
=========================
This strips away everything to find the exact trigger.
"""

import numpy as np

print("Test 1: Simple tuple unpacking")
try:
    R, G, B = 220, 220, 230
    print(f"  ✓ Success: R={R}, G={G}, B={B}")
except Exception as e:
    print(f"  ✗ FAILED: {e}")
    import traceback
    traceback.print_exc()

print("\nTest 2: Tuple unpacking in loop")
try:
    for i in range(10):
        R, G, B = 220, 220, 230
        x = R + G + B
    print(f"  ✓ Success: last sum = {x}")
except Exception as e:
    print(f"  ✗ FAILED: {e}")
    import traceback
    traceback.print_exc()

print("\nTest 3: With numpy arrays present")
try:
    arr = np.zeros((100, 100))
    for i in range(10):
        R, G, B = 220, 220, 230
        val = arr[0, 0]
    print(f"  ✓ Success")
except Exception as e:
    print(f"  ✗ FAILED: {e}")
    import traceback
    traceback.print_exc()

print("\nTest 4: With file open")
try:
    with open('test_minimal.txt', 'w') as f:
        for i in range(10):
            R, G, B = 220, 220, 230
            f.write(f"{R} {G} {B}\n")
    print(f"  ✓ Success")
except Exception as e:
    print(f"  ✗ FAILED: {e}")
    import traceback
    traceback.print_exc()

print("\nTest 5: Complex nested structure")
try:
    arr = np.random.rand(1000, 1000)
    with open('test_minimal2.txt', 'w') as OUTPUT_FILE:
        for chunk in range(10):
            chunk_data = arr[chunk*100:(chunk+1)*100, :]
            
            for row in range(100):
                for col in range(1000):
                    val = float(chunk_data[row, col])
                    
                    # The problematic line
                    R, G, B = 220, 220, 230
                    
                    OUTPUT_FILE.write(f"{val:.4f} {R} {G} {B}\n")
    
    print(f"  ✓ Success")
except Exception as e:
    print(f"  ✗ FAILED: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("If any test failed, your Python interpreter has a serious bug.")
print("="*70)

# Cleanup
import os
try:
    os.remove('test_minimal.txt')
    os.remove('test_minimal2.txt')
except:
    pass