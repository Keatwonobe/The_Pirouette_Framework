import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# 1. The Algebraic Skeleton: SU(3) in T/R/G Basis
# =============================================================================

def gell_mann_matrices():
    """
    Return the 8 Gell-Mann-like matrices in the {T, R, G} basis.
    T=(1,0,0), R=(0,1,0), G=(0,0,1).
    """
    # 1: Mix T<->R (Real)
    lam1 = np.array([[0, 1, 0],
                     [1, 0, 0],
                     [0, 0, 0]], dtype=complex)
    
    # 2: Mix T<->R (Imaginary)
    lam2 = np.array([[0, -1j, 0],
                     [1j,  0, 0],
                     [0,   0, 0]], dtype=complex)
    
    # 3: Isospin (T vs R)
    lam3 = np.array([[1,  0, 0],
                     [0, -1, 0],
                     [0,  0, 0]], dtype=complex)
    
    # 4: Mix T<->G (Real)
    lam4 = np.array([[0, 0, 1],
                     [0, 0, 0],
                     [1, 0, 0]], dtype=complex)
    
    # 5: Mix T<->G (Imaginary)
    lam5 = np.array([[0, 0, -1j],
                     [0, 0,  0],
                     [1j, 0,  0]], dtype=complex)
    
    # 6: Mix R<->G (Real)
    lam6 = np.array([[0, 0, 0],
                     [0, 0, 1],
                     [0, 1, 0]], dtype=complex)
    
    # 7: Mix R<->G (Imaginary)
    lam7 = np.array([[0, 0, 0],
                     [0, 0, -1j],
                     [0, 1j, 0]], dtype=complex)
    
    # 8: Hypercharge (T+R vs G)
    lam8 = (1/np.sqrt(3)) * np.array([[1, 0, 0],
                                      [0, 1, 0],
                                      [0, 0,-2]], dtype=complex)
    
    return [lam1, lam2, lam3, lam4, lam5, lam6, lam7, lam8]

def verify_algebra(lams):
    """
    Checks orthonormality and computes structure constants.
    """
    print("--- Verifying SU(3) Octet Orthonormality ---")
    ortho_matrix = np.zeros((8,8))
    for a in range(8):
        for b in range(8):
            # Trace(La Lb) = 2 delta_ab
            tr = np.trace(np.dot(lams[a], lams[b]))
            ortho_matrix[a,b] = tr.real
    
    # Check diagonal
    diag = np.diag(ortho_matrix)
    print(f"Diagonals (should be ~2.0): {np.round(diag, 2)}")
    off_diag_sum = np.sum(np.abs(ortho_matrix)) - np.sum(np.abs(diag))
    print(f"Sum of off-diagonals (should be ~0): {off_diag_sum:.2e}")
    
    return ortho_matrix

# =============================================================================
# 2. The Geometric Shadow: Basin Jacobians
# =============================================================================

def get_basin_jacobians(twist=1.5):
    """
    Computes the 2x2 Jacobian J at the center of the three basins.
    Using the logic from the force definition in 1D1_6.py
    """
    # Centers based on angles 150 (T), 270 (R), 30 (G)
    # Radius approx 1.0 for the unit circle layout, 
    # but the anchors in code were T:(-0.866, 0.5), R:(0,-1).
    # Gold was vector sum, but basin is at 30 deg. Let's use 30 deg unit vector.
    
    centers = {
        'T': np.array([-0.866, 0.5]),
        'R': np.array([0.0, -1.0]),
        'G': np.array([0.866, 0.5])
    }
    
    # Re-implementing the core force/jacobian logic briefly here to be self-contained
    def local_force(m, lam, t=twist):
        F_teal_m = -(m + 0.866)
        F_teal_lam = -(lam - 0.5)
        
        F_red_m = -(m - 0.0)
        p_violation = t * np.sin(m * 2.5)
        F_red_lam = -(lam + 1.0) + p_violation
        
        F_gold_m = F_teal_m + F_red_m
        F_gold_lam = F_teal_lam + F_red_lam
        
        # We assume we are DEEP in the basin, so weights are roughly 1 for that color, 0 for others
        # This gives us the "pure" Jacobian of that basin's attractor
        return {
            'T': (F_teal_m, F_teal_lam),
            'R': (F_red_m, F_red_lam),
            'G': (F_gold_m, F_gold_lam)
        }

    # Numerical Jacobian
    eps = 1e-4
    Jacobians = {}
    
    for name, pos in centers.items():
        m, l = pos
        
        # To get the Jacobian of the "Teal Dynamics", we just look at F_teal derivatives
        # (Since in the center of Teal basin, w_teal=1)
        
        # Central difference
        # We need the force specific to that basin (assuming w=1 dominance)
        def get_f_comp(mm, ll):
            f_dict = local_force(mm, ll)
            return f_dict[name] # Extract only the force component for this basin
            
        fm_p, fl_p = get_f_comp(m + eps, l)
        fm_m, fl_m = get_f_comp(m - eps, l)
        
        fl_lp, fll_lp = get_f_comp(m, l + eps)
        fl_lm, fll_lm = get_f_comp(m, l - eps)
        
        dFm_dm = (fm_p - fm_m) / (2*eps)
        dFl_dm = (fl_p - fl_m) / (2*eps)
        dFm_dl = (fl_lp - fl_lm) / (2*eps)
        dFl_dl = (fll_lp - fll_lm) / (2*eps)
        
        J = np.array([[dFm_dm, dFm_dl], [dFl_dm, dFl_dl]])
        Jacobians[name] = J

    return Jacobians

def analyze_tripod_commutators(Jacs):
    """
    Computes [Ja, Jb] for the geometric Jacobians.
    """
    print("\n--- Geometric Tripod Commutators (The Shadow) ---")
    keys = ['T', 'R', 'G']
    
    results = {}
    
    for i in range(3):
        for j in range(i+1, 3):
            k1, k2 = keys[i], keys[j]
            J1, J2 = Jacs[k1], Jacs[k2]
            
            # Commutator
            Comm = np.dot(J1, J2) - np.dot(J2, J1)
            norm = np.linalg.norm(Comm)
            results[f"[{k1},{k2}]"] = (Comm, norm)
            
            print(f"[{k1}, {k2}] Norm: {norm:.4f}")
            # print(Comm) # Optional: print the actual 2x2 matrix
            
    return results

# =============================================================================
# Run
# =============================================================================

if __name__ == "__main__":
    # 1. Verify SU(3)
    lams = gell_mann_matrices()
    verify_algebra(lams)
    
    # 2. Analyze the Tripod
    jacobians = get_basin_jacobians(twist=1.5)
    analyze_tripod_commutators(jacobians)
    
    # 3. Explicit check of user's hypothesis:
    # "J_G, J_T] ≈ -0.199 J_T + ..."
    # We can perform a least-squares fit of the Commutator matrix against the basis {JT, JR, JG}
    
    print("\n--- Projecting Commutators onto Basin Basis ---")
    # Vectorize matrices for linear regression
    # Basis = [flat(JT), flat(JR), flat(JG)]
    basis_vectors = np.array([jacobians[k].flatten() for k in ['T', 'R', 'G']]).T
    
    for key in ["[R,G]", "[G,T]", "[T,R]"]:
        # Reconstruct commutator from map
        k1, k2 = key[1], key[3]
        comm = np.dot(jacobians[k1], jacobians[k2]) - np.dot(jacobians[k2], jacobians[k1])
        y = comm.flatten()
        
        # Solve: basis_vectors * coeffs = y
        # coeffs will be [c_T, c_R, c_G]
        coeffs, resid, rank, s = np.linalg.lstsq(basis_vectors, y, rcond=None)
        
        print(f"{key} ≈ {coeffs[0]:.3f} J_T + {coeffs[1]:.3f} J_R + {coeffs[2]:.3f} J_G")