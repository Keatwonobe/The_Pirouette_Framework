
import numpy as np
import math
import argparse
from dataclasses import dataclass, asdict

@dataclass
class CTIParams:
    eta: float = 0.96
    kappa: float = 0.35
    alpha: float = 0.12
    rho_star: float = 0.4
    omega: float = 0.17
    xi: float = 0.28
    c1: float = 0.15
    c2: float = 0.10
    r_eta: float = 0.94
    r_alpha: float = -0.10
    r_bias_close: float = 0.2
    lam_DR: float = 1.0
    lam_stab: float = 0.2
    lam_cost: float = 0.05
    beta: float = 8.0
    horizon: int = 8
    beam: int = 2
    eps_fd: float = 1e-3

@dataclass
class CTIEntity:
    K_t: float = 1.0
    Gamma: float = 1.0
    K_i: float = 1.0

@dataclass
class CTIState:
    rhoI: float = 0.0
    PI: float = 0.0
    phi: float = 0.0
    C: float = 0.0
    parity: int = 0
    run: int = 0
    last_bit: int = 0

def forward_step(s, b, prm, ent):
    s2 = CTIState(**asdict(s))
    s2.rhoI = ent.K_i * (prm.eta * s.rhoI + prm.kappa * b)
    dP = ent.K_t * (prm.alpha * (s2.rhoI - prm.rho_star))
    s2.PI = s.PI + dP
    s2.phi = (s.phi + prm.omega + prm.xi * b) % (2*np.pi)
    s2.parity = (s.parity ^ (b & 1))
    if s.run == 0:
        s2.run = 1
    else:
        s2.run = s.run + 1 if b == s.last_bit else 1
    s2.last_bit = b
    parity_closes = (s2.parity == 0) and (s2.run <= 3)
    s2.C = max(0.0, s.C + (prm.c1 if parity_closes else 0.0) - prm.c2 * abs(dP))
    return s2

def retro_step(s_next, b, prm, ent):
    sR = CTIState(**asdict(s_next))
    sR.rhoI = prm.r_eta * s_next.rhoI
    sR.PI = s_next.PI + prm.r_alpha * np.sign(s_next.PI) * ent.Gamma
    sR.phi = (s_next.phi - 0.5*prm.omega * np.tanh(s_next.PI)) % (2*np.pi)
    if (s_next.parity != 0) and (s_next.run >= 2):
        sR.C += prm.r_bias_close
    return sR

def seam_residual(sF, sR):
    vF = np.array([sF.rhoI, sF.PI, np.sin(sF.phi), np.cos(sF.phi), sF.C])
    vR = np.array([sR.rhoI, sR.PI, np.sin(sR.phi), np.cos(sR.phi), sR.C])
    return float(np.sum((vF - vR)**2))

def dark_residue(traj):
    if not traj:
        return 0.0
    PI_term = np.mean([abs(s.PI) for s in traj])
    ph = np.array([s.phi for s in traj])
    dphi = np.diff(np.unwrap(ph))
    phase_term = np.mean(np.abs(dphi)) if len(dphi)>0 else 0.0
    parity_term = np.mean([abs(s.PI) for s in traj if s.parity != 0]) if any(s.parity!=0 for s in traj) else 0.0
    run_term = np.mean([max(0, s.run-4) for s in traj])
    return 0.6*PI_term + 0.3*phase_term + 0.1*parity_term + 0.1*run_term

def jac_instability(s, b, prm, ent):
    eps = prm.eps_fd
    sF = forward_step(s, b, prm, ent)
    s_eps = CTIState(**asdict(s)); s_eps.rhoI += eps
    sF_eps = forward_step(s_eps, b, prm, ent)
    J = (sF_eps.rhoI - sF.rhoI) / eps
    return max(0.0, J - 1.0)

class Tail:
    def __init__(self, states, cost):
        self.states = states
        self.cost = cost

def greedy_completions(s_start, prm, ent, h, beam=2):
    beams = [(s_start, [], 0.0)]
    for _ in range(h):
        cand = []
        for s, lst, cost in beams:
            for b in (0,1):
                sF = forward_step(s, b, prm, ent)
                local = 0.2*abs(sF.PI) - 0.1*(1 if (sF.parity==0 and sF.run<=3) else 0)
                cand.append((sF, lst+[sF], cost+local))
        cand.sort(key=lambda x: x[2])
        beams = cand[:beam]
    return [Tail(states=lst, cost=cost) for (_, lst, cost) in beams]

def energy_for_bit(b, s_t, prm, ent):
    sF = forward_step(s_t, b, prm, ent)
    sR = retro_step(sF, b, prm, ent)
    seam = seam_residual(sF, sR)
    tails = greedy_completions(sF, prm, ent, h=prm.horizon-1, beam=prm.beam)
    bestE = float("inf")
    parts_best = {}
    for tl in tails:
        DR = dark_residue(tl.states)
        ST = np.mean([jac_instability(st, b, prm, ent) for st in tl.states])
        CF = tl.cost
        E = seam + prm.lam_DR*DR + prm.lam_stab*ST + prm.lam_cost*CF
        if E < bestE:
            bestE = E
            parts_best = {"seam": seam, "DR": DR, "ST": ST, "CF": CF}
    return bestE, parts_best

def predict_next_bit(s_t, prm, ent):
    E0, parts0 = energy_for_bit(0, s_t, prm, ent)
    E1, parts1 = energy_for_bit(1, s_t, prm, ent)
    # stable softmax over -beta*E
    m = min(E0, E1)
    x0 = -prm.beta*(E0 - m)
    x1 = -prm.beta*(E1 - m)
    # clip to avoid overflow/underflow
    x0 = max(-700.0, min(700.0, x0))
    x1 = max(-700.0, min(700.0, x1))
    e0 = math.exp(x0); e1 = math.exp(x1)
    Z = e0 + e1
    if Z == 0.0:
        p0 = 0.5; p1 = 0.5
    else:
        p0 = e0 / Z; p1 = e1 / Z
    next_bit = 1 if p1 > p0 else 0
    return next_bit, (p0, p1), {"0": parts0, "1": parts1}

def gen_parity_runs(T, seed=0):
    rng = np.random.default_rng(seed)
    bits = []
    parity = 0; last = 0; run = 0
    for t in range(T):
        if run >= 3:
            b = 1-last
        else:
            desire_close = (parity != 0) and (run >= 1)
            if desire_close and rng.random() < 0.7:
                b = 1
            else:
                b = last if rng.random() < 0.7 else 1-last
        if rng.random() < 0.05:
            b ^= 1
        bits.append(b)
        parity ^= b
        run = run+1 if b==last else 1
        last = b
    return np.array(bits, dtype=int)

def run_demo(T=256, seed=7, horizon=8, beam=2):
    prm = CTIParams(horizon=horizon, beam=beam)
    ent = CTIEntity(K_t=1.0, Gamma=1.0, K_i=1.0)
    truth = gen_parity_runs(T, seed=seed)
    s = CTIState()
    preds = []
    probs = []
    energies = []
    s = forward_step(s, int(truth[0]), prm, ent)
    preds.append(truth[0]); probs.append((0.5,0.5)); energies.append({"0":{}, "1":{}})
    for t in range(1, T):
        b_hat, (p0,p1), parts = predict_next_bit(s, prm, ent)
        preds.append(b_hat)
        probs.append((p0,p1))
        energies.append(parts)
        s = forward_step(s, int(truth[t]), prm, ent)
    preds = np.array(preds, dtype=int)
    acc = float(np.mean(preds == truth))
    return {
        "accuracy": acc,
        "truth": truth.tolist(),
        "preds": preds.tolist(),
        "probs": probs,
        "energies": energies
    }

def main():
    ap = argparse.ArgumentParser(description="CTI-1D demo")
    ap.add_argument("--demo", type=str, default="parity_runs")
    ap.add_argument("--T", type=int, default=256)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--horizon", type=int, default=8)
    ap.add_argument("--beam", type=int, default=2)
    args = ap.parse_args()
    if args.demo == "parity_runs":
        out = run_demo(T=args.T, seed=args.seed, horizon=args.horizon, beam=args.beam)
        print(f"[CTI-1D] accuracy={out['accuracy']:.3f} on {args.T} steps")
    else:
        raise SystemExit("Unknown demo")

if __name__ == "__main__":
    main()
