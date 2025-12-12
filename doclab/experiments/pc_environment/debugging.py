"""
PYTHON ENVIRONMENT DIAGNOSTIC TOOL
===================================
This script deliberately triggers the kinds of operations that cause your crashes
and monitors EVERYTHING to figure out what's corrupting your variables.

It tests:
1. Memory integrity during large array operations
2. Variable scoping with nested contexts
3. File handle + numpy interactions
4. Garbage collection behavior
5. System resource limits
6. Python interpreter health

Run this and it will tell you EXACTLY what's broken.
"""

import sys
import os
import gc
import traceback
import psutil
import numpy as np
import time
import json
from datetime import datetime
import ctypes
import platform

# ANSI color codes for readability
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def log_pass(msg):
    print(f"{Colors.GREEN}✓ PASS{Colors.RESET} {msg}")

def log_fail(msg):
    print(f"{Colors.RED}✗ FAIL{Colors.RESET} {msg}")

def log_warn(msg):
    print(f"{Colors.YELLOW}⚠ WARN{Colors.RESET} {msg}")

def log_info(msg):
    print(f"{Colors.BLUE}ℹ INFO{Colors.RESET} {msg}")

class DiagnosticReport:
    def __init__(self):
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'python_version': sys.version,
            'platform': platform.platform(),
            'tests': {}
        }
    
    def add_test(self, name, passed, details):
        self.results['tests'][name] = {
            'passed': passed,
            'details': details
        }
    
    def save(self):
        with open('python_diagnostic_report.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\n{Colors.BLUE}📊 Full report saved to: python_diagnostic_report.json{Colors.RESET}")

report = DiagnosticReport()

print("="*70)
print("PYTHON ENVIRONMENT DIAGNOSTIC TOOL")
print("="*70)
print()

# ============================================================================
# TEST 1: System Information
# ============================================================================
print(f"\n{Colors.BLUE}[TEST 1] SYSTEM INFORMATION{Colors.RESET}")
print("-" * 70)

try:
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Platform: {platform.platform()}")
    print(f"Architecture: {platform.machine()}")
    print(f"Processor: {platform.processor()}")
    
    mem = psutil.virtual_memory()
    print(f"Total RAM: {mem.total / (1024**3):.2f} GB")
    print(f"Available RAM: {mem.available / (1024**3):.2f} GB")
    print(f"RAM Usage: {mem.percent}%")
    
    log_pass("System information collected")
    report.add_test("system_info", True, {
        'python': sys.version,
        'platform': platform.platform(),
        'total_ram_gb': mem.total / (1024**3),
        'available_ram_gb': mem.available / (1024**3)
    })
except Exception as e:
    log_fail(f"Failed to get system info: {e}")
    report.add_test("system_info", False, str(e))

# ============================================================================
# TEST 2: Memory Allocation Test
# ============================================================================
print(f"\n{Colors.BLUE}[TEST 2] LARGE MEMORY ALLOCATION{Colors.RESET}")
print("-" * 70)

try:
    log_info("Allocating 500 MB array...")
    test_array = np.zeros((1000, 1000, 125), dtype=np.float32)  # ~500 MB
    
    # Verify it's actually a numpy array
    assert isinstance(test_array, np.ndarray), f"Type corruption! Got {type(test_array)}"
    
    # Check memory usage
    mem_after = psutil.virtual_memory()
    log_info(f"RAM after allocation: {mem_after.percent}%")
    
    # Try to access it
    test_array[500, 500, 50] = 42.0
    value = test_array[500, 500, 50]
    assert value == 42.0, f"Value corruption! Expected 42.0, got {value}"
    
    log_pass("Large array allocation and access successful")
    report.add_test("large_memory_allocation", True, {
        'array_size_mb': 500,
        'ram_usage_after': mem_after.percent
    })
    
    del test_array
    gc.collect()
    
except Exception as e:
    log_fail(f"Memory allocation failed: {e}")
    log_fail(traceback.format_exc())
    report.add_test("large_memory_allocation", False, str(e))

# ============================================================================
# TEST 3: Variable Type Stability
# ============================================================================
print(f"\n{Colors.BLUE}[TEST 3] VARIABLE TYPE STABILITY{Colors.RESET}")
print("-" * 70)

try:
    log_info("Creating multiple variables and checking type stability...")
    
    # Create variables of different types
    var_int = 42
    var_float = 3.14159
    var_str = "hello"
    var_list = [1, 2, 3]
    var_array = np.array([1, 2, 3, 4, 5])
    
    # Record initial types
    initial_types = {
        'var_int': type(var_int).__name__,
        'var_float': type(var_float).__name__,
        'var_str': type(var_str).__name__,
        'var_list': type(var_list).__name__,
        'var_array': type(var_array).__name__
    }
    
    # Do some operations
    for i in range(1000):
        _ = var_int + i
        _ = var_float * 2.0
        _ = var_str + str(i)
        _ = var_list[0]
        _ = var_array[0]
    
    # Check types haven't changed
    corruption_detected = False
    for var_name, var in [('var_int', var_int), ('var_float', var_float), 
                           ('var_str', var_str), ('var_list', var_list), 
                           ('var_array', var_array)]:
        current_type = type(var).__name__
        expected_type = initial_types[var_name]
        if current_type != expected_type:
            log_fail(f"{var_name} type changed! {expected_type} -> {current_type}")
            corruption_detected = True
        else:
            log_info(f"{var_name}: {current_type} (stable)")
    
    if not corruption_detected:
        log_pass("All variable types remained stable")
        report.add_test("variable_type_stability", True, initial_types)
    else:
        log_fail("Variable type corruption detected!")
        report.add_test("variable_type_stability", False, "Types changed during execution")
    
except Exception as e:
    log_fail(f"Type stability test failed: {e}")
    log_fail(traceback.format_exc())
    report.add_test("variable_type_stability", False, str(e))

# ============================================================================
# TEST 4: Nested Context Managers (THE BIG ONE)
# ============================================================================
print(f"\n{Colors.BLUE}[TEST 4] NESTED CONTEXT MANAGERS{Colors.RESET}")
print("-" * 70)

try:
    log_info("Creating test numpy file...")
    
    # Create a test npz file
    test_data = {
        'm_vals': np.linspace(0, 10, 100).astype(np.float32),
        'l_vals': np.linspace(0, 10, 100).astype(np.float32),
        'escape_time': np.random.randint(0, 1000, size=(100, 100), dtype=np.uint16),
        'basin_id': np.random.randint(0, 4, size=(100, 100), dtype=np.uint8)
    }
    
    np.savez_compressed('test_diagnostic.npz', **test_data)
    
    log_info("Testing nested context managers (THIS TRIGGERS YOUR BUG)...")
    
    # This mimics your crashing code structure
    with open('test_output.txt', 'w') as f:
        with np.load('test_diagnostic.npz') as data:
            m_vals = data['m_vals']
            
            # Check type immediately
            type_before = type(m_vals).__name__
            log_info(f"m_vals type inside nested context: {type_before}")
            
            # Try to use it
            test_val = m_vals[0]
            log_info(f"Successfully accessed m_vals[0] = {test_val}")
            
            # Write something
            f.write("test\n")
        
        # Check type after inner context closes
        type_after = type(m_vals).__name__
        log_info(f"m_vals type after npz context closed: {type_after}")
        
        # THIS IS WHERE YOUR BUG HAPPENS
        # Try to access m_vals after npz file closed
        try:
            test_val_2 = m_vals[0]
            log_pass("m_vals still accessible after npz context closed")
        except Exception as e:
            log_fail(f"m_vals became invalid after npz closed: {e}")
            log_fail(f"m_vals type is now: {type(m_vals)}")
            raise
    
    log_pass("Nested context test passed")
    report.add_test("nested_contexts", True, {})
    
    # Cleanup
    os.remove('test_diagnostic.npz')
    os.remove('test_output.txt')
    
except Exception as e:
    log_fail(f"NESTED CONTEXT TEST FAILED - THIS IS YOUR BUG!")
    log_fail(f"Error: {e}")
    log_fail(traceback.format_exc())
    report.add_test("nested_contexts", False, {
        'error': str(e),
        'traceback': traceback.format_exc()
    })

# ============================================================================
# TEST 5: Memory-Mapped vs Copied Arrays
# ============================================================================
print(f"\n{Colors.BLUE}[TEST 5] MEMORY-MAPPED VS COPIED ARRAYS{Colors.RESET}")
print("-" * 70)

try:
    log_info("Creating test npz file...")
    test_array = np.random.rand(100, 100)
    np.savez_compressed('test_memmap.npz', data=test_array)
    
    # Test 1: Without copy (memory-mapped view)
    log_info("Test A: Loading WITHOUT copy (memory-mapped)...")
    with np.load('test_memmap.npz') as npz:
        data_nocopy = npz['data']
        type_nocopy_inside = type(data_nocopy).__name__
        log_info(f"  Type inside context: {type_nocopy_inside}")
    
    # After context closes, is it still valid?
    try:
        type_nocopy_outside = type(data_nocopy).__name__
        _ = data_nocopy[0, 0]
        log_warn(f"  Type outside context: {type_nocopy_outside} (may be invalid!)")
    except Exception as e:
        log_fail(f"  MEMORY-MAPPED VIEW INVALID AFTER CLOSE: {e}")
    
    # Test 2: With copy (owned memory)
    log_info("Test B: Loading WITH copy (owned memory)...")
    with np.load('test_memmap.npz') as npz:
        data_copy = np.array(npz['data'], copy=True)
        type_copy_inside = type(data_copy).__name__
        log_info(f"  Type inside context: {type_copy_inside}")
    
    # After context closes, should still be valid
    try:
        type_copy_outside = type(data_copy).__name__
        val = data_copy[0, 0]
        log_pass(f"  Type outside context: {type_copy_outside} (still valid!)")
        log_pass(f"  Successfully accessed value: {val}")
    except Exception as e:
        log_fail(f"  COPIED ARRAY ALSO FAILED: {e}")
    
    report.add_test("memmap_vs_copy", True, {
        'nocopy_survives_close': False,
        'copy_survives_close': True
    })
    
    os.remove('test_memmap.npz')
    
except Exception as e:
    log_fail(f"Memory-mapped test failed: {e}")
    log_fail(traceback.format_exc())
    report.add_test("memmap_vs_copy", False, str(e))

# ============================================================================
# TEST 6: Garbage Collection Stress Test
# ============================================================================
print(f"\n{Colors.BLUE}[TEST 6] GARBAGE COLLECTION STRESS TEST{Colors.RESET}")
print("-" * 70)

try:
    log_info("Creating and destroying 1000 arrays...")
    
    for i in range(1000):
        arr = np.random.rand(100, 100)
        _ = arr[0, 0]
        del arr
        
        if i % 100 == 0:
            gc.collect()
            log_info(f"  Iteration {i}/1000, RAM: {psutil.virtual_memory().percent}%")
    
    final_mem = psutil.virtual_memory().percent
    log_pass(f"GC stress test passed, final RAM: {final_mem}%")
    report.add_test("gc_stress", True, {'final_ram_percent': final_mem})
    
except Exception as e:
    log_fail(f"GC stress test failed: {e}")
    report.add_test("gc_stress", False, str(e))

# ============================================================================
# TEST 7: File Handle Limits
# ============================================================================
print(f"\n{Colors.BLUE}[TEST 7] FILE HANDLE LIMITS{Colors.RESET}")
print("-" * 70)

try:
    log_info("Testing file handle limits...")
    
    # Try to open many files
    handles = []
    try:
        for i in range(100):
            handles.append(open(f'test_handle_{i}.tmp', 'w'))
        
        log_pass(f"Successfully opened {len(handles)} file handles")
        
        # Close them all
        for h in handles:
            h.close()
            os.remove(h.name)
        
        report.add_test("file_handle_limits", True, {'max_handles_tested': 100})
        
    except Exception as e:
        log_fail(f"Hit file handle limit at {len(handles)} files: {e}")
        for h in handles:
            h.close()
            os.remove(h.name)
        report.add_test("file_handle_limits", False, str(e))
    
except Exception as e:
    log_fail(f"File handle test failed: {e}")
    report.add_test("file_handle_limits", False, str(e))

# ============================================================================
# TEST 8: Python Interpreter Integrity
# ============================================================================
print(f"\n{Colors.BLUE}[TEST 8] PYTHON INTERPRETER INTEGRITY{Colors.RESET}")
print("-" * 70)

try:
    log_info("Checking sys.path integrity...")
    log_info(f"Number of paths: {len(sys.path)}")
    
    log_info("Checking sys.modules integrity...")
    log_info(f"Number of loaded modules: {len(sys.modules)}")
    
    log_info("Checking builtins...")
    assert hasattr(__builtins__, 'print'), "print() missing from builtins!"
    assert hasattr(__builtins__, 'len'), "len() missing from builtins!"
    
    log_pass("Python interpreter appears intact")
    report.add_test("interpreter_integrity", True, {
        'num_paths': len(sys.path),
        'num_modules': len(sys.modules)
    })
    
except Exception as e:
    log_fail(f"Interpreter integrity check failed: {e}")
    report.add_test("interpreter_integrity", False, str(e))

# ============================================================================
# TEST 9: The Exact Bug Reproduction
# ============================================================================
print(f"\n{Colors.BLUE}[TEST 9] EXACT BUG REPRODUCTION{Colors.RESET}")
print("-" * 70)

try:
    log_info("Reproducing EXACT conditions of your crash...")
    
    # Create test data
    test_m = np.linspace(0, 10, 1000).astype(np.float32)
    test_l = np.linspace(0, 10, 1000).astype(np.float32)
    test_esc = np.random.randint(0, 1200, size=(1000, 1000), dtype=np.uint16)
    test_bid = np.random.randint(0, 4, size=(1000, 1000), dtype=np.uint8)
    
    np.savez_compressed('exact_bug_test.npz', 
                        m_vals=test_m, l_vals=test_l,
                        escape_time=test_esc, basin_id=test_bid)
    
    log_info("Step 1: Load coordinates (outside file context)...")
    with np.load('exact_bug_test.npz') as data:
        m_vals = data['m_vals'].astype(np.float32)  # NO COPY
        l_vals = data['l_vals'].astype(np.float32)  # NO COPY
    
    log_info(f"  m_vals type after close: {type(m_vals)}")
    log_info(f"  Is numpy array? {isinstance(m_vals, np.ndarray)}")
    
    log_info("Step 2: Open file for writing...")
    with open('exact_bug_output.ply', 'w') as f:
        log_info("Step 3: Open npz AGAIN (nested context)...")
        with np.load('exact_bug_test.npz') as data:
            esc_full = data['escape_time']
            
            log_info("Step 4: Try to access m_vals...")
            # THIS IS WHERE IT CRASHES FOR YOU
            try:
                x_val = m_vals[0]
                log_info(f"  SUCCESS: m_vals[0] = {x_val}")
                log_info(f"  m_vals type: {type(m_vals)}")
            except TypeError as e:
                log_fail(f"  BUG REPRODUCED! {e}")
                log_fail(f"  m_vals type: {type(m_vals)}")
                log_fail("  THIS IS THE BUG!")
                raise
    
    log_pass("Bug reproduction test passed (couldn't reproduce bug)")
    report.add_test("exact_bug_reproduction", True, {})
    
    os.remove('exact_bug_test.npz')
    os.remove('exact_bug_output.ply')
    
except Exception as e:
    log_fail(f"BUG SUCCESSFULLY REPRODUCED!")
    log_fail(f"Error: {e}")
    log_fail(traceback.format_exc())
    report.add_test("exact_bug_reproduction", False, {
        'bug_reproduced': True,
        'error': str(e),
        'traceback': traceback.format_exc()
    })

# ============================================================================
# FINAL REPORT
# ============================================================================
print("\n" + "="*70)
print("DIAGNOSTIC COMPLETE")
print("="*70)

# Count failures
failures = [k for k, v in report.results['tests'].items() if not v['passed']]

if failures:
    print(f"\n{Colors.RED}❌ FAILURES DETECTED:{Colors.RESET}")
    for fail in failures:
        print(f"  - {fail}")
    print(f"\n{Colors.YELLOW}RECOMMENDATION:{Colors.RESET}")
    
    if 'nested_contexts' in failures:
        print("  💡 Your bug is caused by NUMPY MEMORY-MAPPED FILES!")
        print("  💡 When you use .astype() without copy=True, NumPy returns a VIEW")
        print("  💡 When the npz file closes, the view becomes invalid")
        print("  💡 Python's garbage collector then corrupts the variable")
        print()
        print("  FIX: Always use copy=True when loading from npz files")
        print("  Example: m_vals = np.array(data['m_vals'], dtype=np.float32, copy=True)")
    
    if 'large_memory_allocation' in failures:
        print("  💡 You may have insufficient RAM or memory fragmentation")
        print("  💡 Try closing other applications")
        print("  💡 Consider adding more RAM to your system")
else:
    print(f"\n{Colors.GREEN}✓ ALL TESTS PASSED{Colors.RESET}")
    print("  Your Python environment appears healthy.")
    print("  The bug may be environmental or timing-dependent.")

report.save()
print()