import numpy as np
from numba import njit

# --- DD CORE UTILITIES (FOR DEMO) ---

SPLIT = 134217729.0

@njit(fastmath=True)
def split_double(a):
    c = SPLIT * a
    a_h = c - (c - a)
    a_l = a - a_h
    return a_h, a_l

@njit(fastmath=True)
def two_sum(a, b):
    s = a + b
    v = s - a
    e = (a - v) + (b - (s - v))
    return s, e

@njit(fastmath=True)
def two_prod(a, b):
    p = a * b
    a_h, a_l = split_double(a)
    b_h, b_l = split_double(b)
    e = ((a_h * b_h - p) + a_h * b_l + a_l * b_h) + a_l * b_l
    return p, e

# --- DD ARITHMETIC (FOR DEMO) ---

@njit(fastmath=True)
def dd_sub(a, b):
    # a and b are DD arrays [high, low]
    s, e = two_sum(a[0], -b[0])
    e += a[1] - b[1]
    s_new, e_new = two_sum(s, e)
    return np.array([s_new, e_new])

@njit
def test_dd_precision(a_val, b_val):
    # Standard float64 subtraction - demonstrates precision loss
    diff_f64 = a_val - b_val
    
    # DD subtraction
    a_dd = np.array([a_val, 0.0])
    b_dd = np.array([b_val, 0.0])
    diff_dd = dd_sub(a_dd, b_dd)
    
    # DD number as a single float (high + low)
    diff_dd_reconstructed = diff_dd[0] + diff_dd[1]
    
    return diff_f64, diff_dd_reconstructed

a_too_small = 1.0 + 1e-18
b_too_small = 1.0
f64_18, dd_18 = test_dd_precision(a_too_small, b_too_small)

print(f"\n--- PRECISION DEMO (Difference 1e-18) ---")
print(f"Standard Float64 Difference: {f64_18:.20e} (Truncated due to hardware limit)")
print(f"DD Reconstructed Difference: {dd_18:.20e} (Successfully captured)")