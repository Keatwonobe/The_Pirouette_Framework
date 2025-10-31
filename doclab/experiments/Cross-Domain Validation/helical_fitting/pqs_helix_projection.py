# pqs_helix_projection.py
import argparse, math, numpy as np, pandas as pd

I = np.array([[1,0],[0,1]], dtype=complex)
Z = np.array([[1,0],[0,-1]], dtype=complex)

def kron_n(ops):
    out=np.array([[1]],dtype=complex)
    for op in ops: out=np.kron(out,op)
    return out

def Zk(N,k): return kron_n([Z if i==k else I for i in range(N)])
def ZkZl(N,k,l): return kron_n([Z if (i==k or i==l) else I for i in range(N)])

def build_H_parts(N,h,J):
    HV=np.zeros((2**N,2**N),dtype=complex); HK=np.zeros_like(HV)
    for i in range(N): HV+=h[i]*Zk(N,i)
    for i in range(N):
        for j in range(i+1,N):
            if J[i,j]!=0: HK+=J[i,j]*ZkZl(N,i,j)
    return HV-HK, HV, HK

def exact_ground_state(H):
    vals,vecs=np.linalg.eigh((H+H.conj().T)/2)
    k=np.argmin(vals.real); return float(vals[k].real), vecs[:,k]

def normalize(v): n=np.linalg.norm(v); return v if n==0 else v/n
def ry(a):
    c,s=math.cos(a/2), math.sin(a/2)
    return np.array([[c,-s],[s,c]],dtype=complex)
def rz(p): return np.array([[np.exp(-1j*p/2),0],[0,np.exp(1j*p/2)]],dtype=complex)
def init_plus(N):
    plus=(1/np.sqrt(2))*np.array([1,1],dtype=complex); out=plus
    for _ in range(N-1): out=np.kron(out,plus)
    return out
def apply_single(state,N,q,U): return kron_n([U if i==q else I for i in range(N)]) @ state
def apply_cz_inplace(st,N,a,b):
    dim=2**N; ma=1<<(N-1-a); mb=1<<(N-1-b)
    for idx in range(dim):
        if (idx & ma) and (idx & mb): st[idx]*=-1
    return st
def phase_ramp_layer(state,N,layer_idx,strength):
    center=(N-1)/2
    for q in range(N):
        phi=strength*(layer_idx+1)*(q-center)
        state=apply_single(state,N,q,rz(phi))
    return state
def entangle_helical_ramp(state,N,layer_idx,strength):
    for q in range(N): state=apply_cz_inplace(state,N,q,(q+1)%N)
    off=layer_idx%2
    for q in range(off,N,2): state=apply_cz_inplace(state,N,q,(q+2)%N)
    return phase_ramp_layer(state,N,layer_idx,strength)
def ansatz_apply_and_trace(N,L,thetas,strength):
    st=init_plus(N); t=0; angles=[]
    for layer in range(L):
        for q in range(N):
            th=thetas[t]; t+=1
            ph=thetas[t]; t+=1
            angles.append((layer,q,th,ph))
            st=apply_single(st,N,q,rz(ph) @ ry(th))
        st=entangle_helical_ramp(st,N,layer,strength)
    return normalize(st), angles
def expectation(state,H): return float(np.vdot(state, H @ state).real)
def spsa(func,x0,iters=160,a0=0.32,c0=0.22,seed=0):
    rng=np.random.default_rng(seed); x=x0.copy()
    for k in range(1,iters+1):
        ak=a0/(k**0.5); ck=c0/(k**0.33)
        delta=rng.choice([-1,1], size=x.shape)
        yp=func(x+ck*delta); ym=func(x-ck*delta)
        ghat=(yp-ym)/(2*ck)*delta
        x = x - ak*ghat
    return x
def random_instance(N,rng,h_scale=0.35,J_scale=0.7,p=0.7):
    h=rng.uniform(-h_scale,h_scale,size=N)
    J=np.zeros((N,N))
    for i in range(N):
        for j in range(i+1,N):
            if rng.random()<p: J[i,j]=rng.uniform(-J_scale,J_scale)
    J=J+J.T
    return h,J
def maybe_import_matplotlib(do_plots):
    if not do_plots: return None, None
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D  # noqa
    return plt, Axes3D

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=6)
    ap.add_argument("--L", type=int, default=2)
    ap.add_argument("--phi", type=float, default=0.15)
    ap.add_argument("--iters", type=int, default=160)
    ap.add_argument("--seed", type=int, default=13)
    ap.add_argument("--plots", action="store_true")
    args=ap.parse_args()

    plt, Ax = maybe_import_matplotlib(args.plots)

    rng=np.random.default_rng(args.seed)
    h,J = random_instance(args.n, rng)
    H,HV,HK = build_H_parts(args.n,h,J)

    theta0 = np.zeros(args.L*args.n*2)
    def E_of_t(th):
        st,_ = ansatz_apply_and_trace(args.n,args.L,th,args.phi)
        return expectation(st,H)
    theta_opt = spsa(E_of_t, theta0, iters=args.iters, seed=args.seed+1)
    st, angles = ansatz_apply_and_trace(args.n,args.L,theta_opt,args.phi)

    # Save angles
    df=pd.DataFrame(angles, columns=["layer","qubit","theta","phi"])
    df.to_csv("pqs_angles_best.csv", index=False)
    print("Saved angles to pqs_angles_best.csv")

    if plt is not None:
        # 3D helix projection: map (qubit, layer) → (x,y,z) = (cosφ, sinφ, θ)
        xs=np.cos(df["phi"].values)
        ys=np.sin(df["phi"].values)
        zs=df["theta"].values
        fig=plt.figure(figsize=(6,5))
        ax=fig.add_subplot(111, projection="3d")
        ax.plot(xs,ys,zs, marker="o")
        ax.set_xlabel("cos φ"); ax.set_ylabel("sin φ"); ax.set_zlabel("θ")
        ax.set_title(f"PHA-χ helix projection (N={args.n}, L={args.L}, φ={args.phi})")
        fig.tight_layout(); fig.savefig("pqs_helix_projection_3d.png", dpi=160)
        print("Saved plot pqs_helix_projection_3d.png")

if __name__=="__main__":
    main()
