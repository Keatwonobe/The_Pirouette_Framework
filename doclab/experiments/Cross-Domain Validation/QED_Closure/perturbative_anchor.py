import math

def predict_from_K(K1, K2, K3, mapping="invK", alpha_em_inv_target=127.955, chis=(1.0,1.0,1.0)):
    """
    mapping: "invK" -> alpha_i = c * chi_i / K_i
             "invK2"-> alpha_i = c * chi_i / K_i^2
    Uses GUT normalization: alpha_Y = (3/5)*alpha_1
    Solves for c so that alpha_em matches target, then outputs sin^2(theta_W) and alpha_3 at the same scale.
    """
    p = 1 if mapping=="invK" else 2
    chi1, chi2, chi3 = chis
    alpha_em_target = 1.0/alpha_em_inv_target

    # alpha1 = c*chi1/K1^p; alpha2 = c*chi2/K2^p
    # 1/alpha_em = 1/alpha2 + 1/alphaY,  alphaY=(3/5)alpha1
    denom = ( (K2**p)/(chi2) + (5.0/3.0)*(K1**p)/(chi1) )
    c_norm = alpha_em_target * denom

    alpha1 = c_norm * chi1 / (K1**p)
    alpha2 = c_norm * chi2 / (K2**p)
    alpha3 = c_norm * chi3 / (K3**p)
    alphaY = (3.0/5.0)*alpha1
    sin2  = alphaY/(alphaY + alpha2)

    return {"mapping": mapping, "c_norm": c_norm, "alpha1": alpha1, "alpha2": alpha2, "alpha3": alpha3, "sin2": sin2}

# Your K's from the Casimir step:
K3 = 467.5126
K2 = 262.9758
K1 =  35.0634

print(predict_from_K(K1,K2,K3, mapping="invK"))
print(predict_from_K(K1,K2,K3, mapping="invK2"))
