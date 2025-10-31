# Retry execution with diagnostic prints to ensure output is produced.
import numpy as np, math, pandas as pd, matplotlib.pyplot as plt

I = np.array([[1,0],[0,1]], dtype=complex)
Z = np.array([[1,0],[0,-1]], dtype=complex)

def kron_n(ops):
    out = np.array([[1]], dtype=complex)
    for op in ops:
        out = np.kron(out, op)
    return out

def Zk(N, k):
    ops = [Z if i==k else I for i in range(N)]
    return kron_n(ops)

def ZkZl(N, k, l):
    ops = [Z if (i==k or i==l) else I for i in range(N)]
    return kron_n(ops)

def build_H_parts(N, h, J):
    HV = np.zeros((2**N, 2**N), dtype=complex)
    HK = np.zeros((2**N, 2**N), dtype=complex)
    for i in range(N):
        HV += h[i] * Zk(N, i)
    for i in range(N):
        for j in range(i+1, N):
            if J[i,j] != 0:
                HK += J[i,j] * ZkZl(N, i, j)
    H_total = HV - HK
    return H_total, HV, HK

def exact_ground_state(H):
    vals, vecs = np.linalg.eigh((H + H.conj().T)/2)
    idx = np.argmin(vals.real)
    return vals[idx].real, vecs[:, idx]

def most_likely_bitstring(psi):
    probs = np.abs(psi)**2
    idx = int(np.argmax(probs))
    N = int(np.log2(len(psi)))
    return format(idx, f"0{N}b"), float(probs[idx].real)

def expectation(state, H):
    return float(np.vdot(state, H @ state).real)

def normalize(v):
    n = np.linalg.norm(v)
    return v if n==0 else v/n

def ry(theta):
    c = math.cos(theta/2.0); s = math.sin(theta/2.0)
    return np.array([[c, -s],[s, c]], dtype=complex)

def rz(phi):
    return np.array([[np.exp(-1j*phi/2), 0],[0, np.exp(1j*phi/2)]], dtype=complex)

def init_state_plus(N):
    plus = (1/np.sqrt(2))*np.array([1,1], dtype=complex)
    state = plus
    for _ in range(N-1):
        state = np.kron(state, plus)
    return state

def apply_single(state, N, k, U):
    U_full = kron_n([U if i==k else I for i in range(N)])
    return U_full @ state

def apply_cz(state, N, ctrl, targ):
    new = state.copy()
    dim = 2**N
    for idx in range(dim):
        b_ctrl = (idx >> (N-1-ctrl)) & 1
        b_targ = (idx >> (N-1-targ)) & 1
        if b_ctrl==1 and b_targ==1:
            new[idx] *= -1
    return new

def ansatz_apply(N, L, thetas):
    state = init_state_plus(N)
    t = 0
    for layer in range(L):
        for q in range(N):
            theta = thetas[t]; t+=1
            phi   = thetas[t]; t+=1
            U = rz(phi) @ ry(theta)
            state = apply_single(state, N, q, U)
        for q in range(N):
            qn = (q+1) % N
            state = apply_cz(state, N, q, qn)
    return normalize(state)

def spsa_minimize(func, x0, iters=140, a0=0.3, c0=0.2, alpha=0.602, gamma=0.101, seed=0):
    rng = np.random.default_rng(seed)
    x = x0.copy()
    hist = []
    for k in range(1, iters+1):
        ak = a0/(k**alpha)
        ck = c0/(k**gamma)
        delta = rng.choice([-1,1], size=x.shape)
        yp = func(x + ck*delta)
        ym = func(x - ck*delta)
        ghat = (yp - ym)/(2*ck) * delta
        x = x - ak*ghat
        hist.append(float(func(x)))
    return x, hist

def random_instance(N, rng, h_scale=0.35, J_scale=0.7, edge_prob=0.65):
    h = rng.uniform(-h_scale, h_scale, size=N)
    J = np.zeros((N,N))
    for i in range(N):
        for j in range(i+1, N):
            if rng.random() < edge_prob:
                J[i,j] = rng.uniform(0.0, J_scale)
    J = J + J.T
    return h, J

# Settings
N = 4; L = 3; ITER = 120; NUM_INSTANCES = 10
rng = np.random.default_rng(42)

rows = []; energy_trajs = []

for idx in range(NUM_INSTANCES):
    h, J = random_instance(N, rng)
    H, HV, HK = build_H_parts(N, h, J)
    E_exact, psi_exact = exact_ground_state(H)
    bit_exact, p_exact = most_likely_bitstring(psi_exact)

    theta0 = np.zeros(L*N*2)
    def E_of_theta(th):
        psi = ansatz_apply(N, L, th)
        return expectation(psi, H)

    theta_opt, hist = spsa_minimize(E_of_theta, theta0, iters=ITER, a0=0.32, c0=0.22, seed=idx)
    psi_var = ansatz_apply(N, L, theta_opt)
    E_var = expectation(psi_var, H)
    bit_var, p_var = most_likely_bitstring(psi_var)

    gap = E_var - E_exact
    C_exact = expectation(psi_exact, HK) / max(1e-9, abs(expectation(psi_exact, HV)))
    C_var   = expectation(psi_var,   HK) / max(1e-9, abs(expectation(psi_var,   HV)))

    rows.append({"instance": idx, "E_exact": E_exact, "E_var": E_var, "gap": gap,
                 "bit_exact": bit_exact, "p_exact": p_exact, "bit_var": bit_var, "p_var": p_var,
                 "C_exact": C_exact, "C_var": C_var})
    energy_trajs.append(hist)

df = pd.DataFrame(rows)
csv_path = "pqs_bench_results_small_retry.csv"
df.to_csv(csv_path, index=False)

print("Wrote CSV:", csv_path)
print(df.head())

plt.figure(figsize=(6,4))
plt.hist(df["gap"], bins=10)
plt.title("Variational Gap Distribution (E_var - E_exact)")
plt.xlabel("Energy gap"); plt.ylabel("Count"); plt.tight_layout(); plt.show()

plt.figure(figsize=(6,4))
plt.scatter(df["C_var"], df["gap"])
plt.title("Coherence Metric (C_var) vs Gap")
plt.xlabel("C_var"); plt.ylabel("Energy gap"); plt.tight_layout(); plt.show()

plt.figure(figsize=(6,4))
for hist in energy_trajs[:5]:
    plt.plot(hist)
plt.title("Energy vs Iterations (first 5 instances)")
plt.xlabel("Iteration"); plt.ylabel("Energy"); plt.tight_layout(); plt.show()

csv_path
