import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve

def helical_v3_solver(signal, t, params_A, params_B, lambda_reg=1.0):
    """
    Helical v3.0: Variational Mode Decomposition
    Solves for components A and B by minimizing the Helical Action.
    
    Args:
        signal: The mixed time series S(t)
        t: Time vector
        params_A: (omega_A, kappa_A)
        params_B: (omega_B, kappa_B)
        lambda_reg: Balance parameter (usually 1.0 if noise is symmetric)
        
    Returns:
        psi_A, psi_B: The analytically separated components
    """
    dt = t[1] - t[0]
    N = len(signal)
    
    # Unpack parameters
    wA, kA = params_A
    wB, kB = params_B
    
    # 1. Construct the Annihilation Operators (D_A and D_B)
    # D = d/dt - i*omega*(1+kappa)
    # Discrete derivative matrix (forward difference)
    # We use sparse matrices for speed and memory efficiency
    
    # Differential part: (1/dt) * [ -1  1  0 ... ]
    diags_diff = [-np.ones(N), np.ones(N)]
    D_diff = sparse.diags(diags_diff, [0, 1], shape=(N-1, N)) / dt
    
    # Decouple the complex constants
    # Effective frequency (Geometric Phase Velocity)
    # Note: Using the v2.0 effective frequency correction
    Omega_A = wA * np.sqrt(1 + kA**2) 
    Omega_B = wB * np.sqrt(1 + kB**2)
    
    # Alternatively, use the direct helical phase velocity from Lagrangian:
    # Omega_A = wA * (1 + kA) # (Depending on specific ansatz, let's use the v2.0 one for consistency)
    
    # Interaction part: -i * Omega * Identity
    # We drop the last row to match the derivative shape
    I = sparse.eye(N, format='csr')[:N-1, :] 
    
    Op_A = D_diff - 1j * Omega_A * I
    Op_B = D_diff - 1j * Omega_B * I
    
    # 2. Construct the Euler-Lagrange System
    # (D_A^dag D_A + lambda * D_B^dag D_B) psi_A = lambda * D_B^dag D_B S_obs
    
    # Adjoints (Conjugate Transpose)
    Op_A_H = Op_A.getH()
    Op_B_H = Op_B.getH()
    
    # The "Reaction Matrices" (The Physics of the Spiral)
    LHS = Op_A_H @ Op_A + lambda_reg * (Op_B_H @ Op_B)
    
    # The "Driving Force"
    # We apply the B-destroyer to the total signal. 
    # Whatever survives is the "Source term" for A.
    RHS_vector = lambda_reg * (Op_B_H @ Op_B @ signal)
    
    # 3. Solve the linear system
    # This finds the global minimum of the Helical Action
    psi_A = spsolve(LHS, RHS_vector)
    
    # B is whatever is left
    psi_B = signal - psi_A
    
    return psi_A, psi_B

# Example usage context (to replace the filter call in your main loop):
# psi_A_v3, psi_B_v3 = helical_v3_solver(signal, t, (omega_A, kappa_A), (omega_B, kappa_B))