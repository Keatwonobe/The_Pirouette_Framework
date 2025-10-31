# pqs_minisweep_helix.py
import argparse, math, numpy as np, pandas as pd
import matplotlib.pyplot as plt

# ---------- small helpers ----------
I = np.array([[1,0],[0,1]], dtype=complex)
Z = np.array([[1,0],[0,-1]], dtype=complex)

def kron_n(ops):
    out = np.array([[1]], dtype=complex)
    for op in ops: out = np.kron(out, op)
    return out

def Zk(N,k):  return kron_n([Z if i==k else I for i in range(N)])
def ZkZl(N,k,l): return kron_n([Z if (i==k or i==l) else I for i in range(N)])

def build_H_parts(N, h, J):
    HV = np.zeros((2**N,2**N), dtype=complex)
    HK = np.zeros_like(HV)
    for i in range(N): HV += h[i]*Zk(N,i)
    for i in range(N):
        for j in range(i+1,N):
            if J[i,j] != 0: HK += J[i,j]*ZkZl(N,i,j)
    return HV-HK, HV, HK

def exact_ground_state(H):
    vals, vecs = np.linalg.eigh((H+H.conj().T)/2)
    idx = np.argmin(vals.real)
    return float(vals[idx].real), vecs[:,idx]

def normalize(v):
    n = np.linalg.norm(v);  return v if n==0 else v/n

def ry(a):
    c,s = math.cos(a/2), math.sin(a/2)
    return np.array([[c,-s],[s,c]], dtype=complex)

def rz(p):
    return np.array([[np.exp(-1j*p/2),0],[0,np.exp(1j*p/2)]], dtype=complex)

def init_plus(N):
    plus = (1/np.sqrt(2))*np.array([1,1], dtype=complex)
    out = plus
    for _ in range(N-1): out = np.kron(out, plus)
    return out

def apply_single(state, N, q, U):
    return kron_n([U if i==q else I for i in range(N)]) @ state

def apply_cz_inplace(st, N, a, b):
    dim = 2**N
    mask_a = 1 << (N-1-a)
    mask_b = 1 << (N-1-b)
    # vectorized sign flip on |11> of (a,b)
    for idx in range(dim):
        if (idx & mask_a) and (idx & mask_b): st[idx] *= -1
    return st

def phase_ramp_layer(state, N, layer_idx, strength=0.15):
    center = (N-1)/2
    for q in range(N):
        phi = strength*(layer_idx+1)*(q-center)
        state = apply_single(state, N, q, rz(phi))
    return state

def entangle_layer(state, N, which, layer_idx=0, ramp=False):
    # ring
    for q in range(N):
        state = apply_cz_inplace(state, N, q, (q+1)%N)
    if which in ("helical", "helical_ramp"):
        off = layer_idx % 2
        for q in range(off, N, 2):
            state = apply_cz_inplace(state, N, q, (q+2)%N)
    if which=="helical_ramp":
        state = phase_ramp_layer(state, N, layer_idx, strength=0.15)
    return state

def ansatz_apply(N, L, thetas, which):
    st = init_plus(N); t = 0
    for layer in range(L):
        for q in range(N):
            th = thetas[t]; t+=1
            ph = thetas[t]; t+=1
            st = apply_single(st, N, q, rz(ph) @ ry(th))
        st = entangle_layer(st, N, which, layer_idx=layer, ramp=(which=="helical_ramp"))
    return normalize(st)

def expectation(state, H): return float(np.vdot(state, H @ state).real)

def spsa(func, x0, iters=120, a0=0.32, c0=0.22, seed=0, gamma_sched=True):
    rng = np.random.default_rng(seed); x = x0.copy(); hist=[]
    for k in range(1, iters+1):
        if gamma_sched:
            ak = a0/(k**0.5); ck = c0/(k**0.33)
        else:
            ak = a0/(k**0.602); ck = c0/(k**0.101)
        delta = rng.choice([-1,1], size=x.shape)
        yp = func(x + ck*delta); ym = func(x - ck*delta)
        ghat = (yp-ym)/(2*ck) * delta
        x = x - ak*ghat
        hist.append(float(func(x)))
    return x, hist

def random_instance(N, rng, h_scale=0.35, J_scale=0.7, p=0.7):
    h = rng.uniform(-h_scale, h_scale, size=N)
    J = np.zeros((N,N))
    for i in range(N):
        for j in range(i+1,N):
            if rng.random() < p: J[i,j] = rng.uniform(-J_scale, J_scale)
    J = J + J.T
    return h, J

# ---------- main ----------
def run(N=6, Ls=(2,3), which_list=("ring","helical","helical_ramp"),
        instances=4, iters=100, seed=2025, outprefix="pqs_N6"):
    rng = np.random.default_rng(seed)
    rows = []
    for inst in range(instances):
        h,J = random_instance(N, rng)
        H,HV,HK = build_H_parts(N, h, J)
        E0, psi0 = exact_ground_state(H)
        for L in Ls:
            for which in which_list:
                theta0 = np.zeros(L*N*2)
                def E_of_t(th):
                    return expectation(ansatz_apply(N,L,th,which), H)
                theta_opt, hist = spsa(E_of_t, theta0, iters=iters, seed=seed+inst)
                psi = ansatz_apply(N,L,theta_opt,which)
                gap = expectation(psi,H) - E0
                overlap = float(np.abs(np.vdot(psi, psi0))**2)
                rows.append({"N":N,"instance":inst,"L":L,"ansatz":which,
                             "gap":gap,"overlap":overlap})
    df = pd.DataFrame(rows)
    agg = df.groupby(["N","L","ansatz"]).agg(median_gap=("gap","median"),
                                            median_overlap=("overlap","median")).reset_index()
    # Save
    df.to_csv(f"{outprefix}_full.csv", index=False)
    agg.to_csv(f"{outprefix}_summary.csv", index=False)
    print(agg.sort_values(["median_gap","L"]))
    # Plot
    labels = [f"L={r.L},{r.ansatz}" for r in agg.itertuples()]
    import matplotlib.pyplot as plt
    plt.figure(figsize=(8,4))
    plt.bar(range(len(agg)), agg["median_gap"])
    plt.xticks(range(len(agg)), labels, rotation=45, ha='right')
    plt.ylabel("Median gap"); plt.title(f"PQS (N={N}) — Γ schedule"); plt.tight_layout()
    plt.savefig(f"{outprefix}_median_gap.png", dpi=160)
    return df, agg

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=6)
    ap.add_argument("--instances", type=int, default=4)
    ap.add_argument("--iters", type=int, default=100)
    ap.add_argument("--out", type=str, default="pqs_N6")
    args = ap.parse_args()
    run(N=args.n, instances=args.instances, iters=args.iters, outprefix=args.out)
