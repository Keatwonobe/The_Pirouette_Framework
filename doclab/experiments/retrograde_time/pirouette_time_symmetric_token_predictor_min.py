
# pirouette_time_symmetric_token_predictor_min.py
# ------------------------------------------------
# Lean, time-symmetric next-token predictor with an SMC "SeanceDecoder".
# Essentials only: forward/retro maps, seam residual, Dark Residue, short rollout,
# single energy, greedy & seance decoders.
#
# Run:
#   python pirouette_time_symmetric_token_predictor_min.py --demo

import math, random, argparse
from dataclasses import dataclass, asdict, replace
from typing import List, Tuple, Dict, Optional
import numpy as np

# ----------------------
# Tiny vocab and grammar
# ----------------------
TOKENS = [
    ("the","DET"), ("a","DET"),
    ("bright","ADJ"), ("quiet","ADJ"), ("strange","ADJ"),
    ("river","N"), ("forest","N"), ("machine","N"), ("signal","N"),
    ("flows","V"), ("listens","V"), ("awakens","V"), ("composes","V"),
    ("through","PREP"), ("beyond","PREP"), ("within","PREP"),
    ("and","CONJ"), ("then","ADV"), ("now","ADV")
]
CAT = {w:t for (w,t) in TOKENS}
_rng = np.random.default_rng(17)
EMB = {w: _rng.normal(0,1,2) for (w,_) in TOKENS}

TRANS = {
    "START": ["DET","ADJ","N"],
    "DET": ["ADJ","N"],
    "ADJ": ["ADJ","N"],
    "N": ["V","CONJ","PREP","END"],
    "V": ["DET","N","ADV","PREP","END"],
    "PREP": ["DET","N","ADJ"],
    "ADV": ["V","PREP","END"],
    "CONJ": ["DET","N","ADJ","V"],
}

def shortlist(prev_tag: str) -> List[str]:
    next_tags = TRANS.get(prev_tag, TRANS["N"])
    return [w for (w,t) in TOKENS if t in next_tags]

def topic_shortlist(topic: Optional[np.ndarray], cands: List[str], k: int=8) -> List[str]:
    if topic is None or not cands:
        return cands
    sims = []
    for w in cands:
        v = EMB[w]
        num = float(np.dot(v, topic))
        den = float(np.linalg.norm(v)*np.linalg.norm(topic) + 1e-8)
        sims.append((w, num/den))
    sims.sort(key=lambda x: x[1], reverse=True)
    return [w for (w,_) in sims[:max(1, min(k, len(cands)) )]]

# ----------------------
# State & parameters
# ----------------------
@dataclass
class Params:
    eta: float = 0.95
    kappa: float = 0.45
    alpha: float = 0.15
    rho_star: float = 0.6
    omega: float = 0.25
    xi: float = 0.20
    c1: float = 0.2
    c2: float = 0.1
    r_eta: float = 0.92
    r_alpha: float = -0.12
    r_bias_close: float = 0.25
    lam_DR: float = 1.0
    lam_stab: float = 0.15
    lam_cost: float = 0.05
    beta: float = 9.0
    horizon: int = 4
    beam: int = 3
    eps_fd: float = 1e-3

@dataclass
class Entity:
    K_t: float = 1.0
    Gamma: float = 1.0
    K_i: float = 1.0
    topic: Optional[np.ndarray] = None

@dataclass
class State:
    rhoI: float = 0.0
    PI: float = 0.0
    phi: float = 0.0
    C: float = 0.0
    open_det: int = 0
    open_verb: int = 0
    prev_tag: str = "START"
    last_token: str = ""

# ----------------------
# Core maps (time-symmetric)
# ----------------------
def _novelty(v: np.ndarray) -> float:
    return float(np.linalg.norm(v))

def _closure_bonus(prev: State, next_tag: str) -> float:
    bonus = 0.0
    if prev.open_det>0 and next_tag=="N" and prev.open_det<=2: bonus += 1.0
    if prev.open_verb>0 and next_tag=="V" and prev.open_verb<=3: bonus += 0.7
    return bonus

def forward_step(s: State, tok: str, prm: Params, ent: Entity) -> State:
    s2 = State(**asdict(s))
    v = EMB[tok]
    nov = _novelty(v)
    s2.rhoI = ent.K_i * (prm.eta * s.rhoI + prm.kappa * nov)
    dP = ent.K_t * (prm.alpha * (s2.rhoI - prm.rho_star))
    s2.PI = s.PI + dP
    s2.phi = (s.phi + prm.omega + prm.xi * (nov>1.5)) % (2*np.pi)
    tag = CAT[tok]
    # obligations
    if tag=="DET": s2.open_det = min(3, s.open_det+1)
    if tag=="N":
        if s.open_det>0: s2.open_det = 0
        if s.prev_tag in ("START","DET","ADJ"): s2.open_verb = min(3, s.open_verb+1)
    if tag=="V" and s.open_verb>0: s2.open_verb = 0
    # coherence
    clos = _closure_bonus(s, tag) > 0.0
    s2.C = max(0.0, s.C + (prm.c1 if clos else 0.0) - prm.c2 * abs(dP))
    s2.prev_tag = tag
    s2.last_token = tok
    return s2

def retro_step(s_next: State, tok: str, prm: Params, ent: Entity) -> State:
    sR = State(**asdict(s_next))
    sR.rhoI = prm.r_eta * s_next.rhoI
    sR.PI = s_next.PI + prm.r_alpha * np.sign(s_next.PI) * ent.Gamma
    sR.phi = (s_next.phi - 0.5*prm.omega * np.tanh(s_next.PI)) % (2*np.pi)
    if s_next.open_det>0: sR.C += 0.2
    if s_next.open_verb>0: sR.C += 0.2
    return sR

def seam_residual(sF: State, sR: State) -> float:
    vF = np.array([sF.rhoI, sF.PI, np.sin(sF.phi), np.cos(sF.phi), sF.C, sF.open_det, sF.open_verb])
    vR = np.array([sR.rhoI, sR.PI, np.sin(sR.phi), np.cos(sR.phi), sR.C, sR.open_det, sR.open_verb])
    return float(np.sum((vF - vR)**2))

def dark_residue(traj: List[State], ent: Entity) -> float:
    if not traj: return 0.0
    PI_term = np.mean([abs(s.PI) for s in traj])
    ph = np.array([s.phi for s in traj]); dphi = np.diff(np.unwrap(ph))
    phase_term = float(np.mean(np.abs(dphi))) if len(dphi)>0 else 0.0
    oblig = float(np.mean([0.5*s.open_det + 0.5*s.open_verb for s in traj]))
    topic_term = 0.0
    if ent.topic is not None:
        toks = [s.last_token for s in traj if s.last_token]
        if toks:
            mean_vec = np.mean([EMB[t] for t in toks], axis=0)
            cos = float(np.dot(mean_vec, ent.topic) / (np.linalg.norm(mean_vec)*np.linalg.norm(ent.topic)+1e-8))
            topic_term = max(0.0, 1.0 - cos)
    return 0.5*PI_term + 0.2*phase_term + 0.2*oblig + 0.1*topic_term

def jac_instability(s: State, tok: str, prm: Params, ent: Entity) -> float:
    eps = prm.eps_fd
    sF = forward_step(s, tok, prm, ent)
    s_eps = State(**asdict(s)); s_eps.rhoI += eps
    sF_eps = forward_step(s_eps, tok, prm, ent)
    J = (sF_eps.rhoI - sF.rhoI) / eps
    return max(0.0, J - 1.0)

# ----------------------
# Rollout & energy
# ----------------------
class Tail:
    __slots__ = ("states","toks","cost")
    def __init__(self, states, toks, cost): self.states=states; self.toks=toks; self.cost=cost

def greedy_completions(s_start: State, prm: Params, ent: Entity, top_k: Optional[int]=None) -> List[Tail]:
    # Short horizon beam search; optional top-k shortlist per expansion
    beams = [(s_start, [], [], 0.0)]
    H = max(0, prm.horizon-1)
    for _ in range(H):
        cand = []
        for s, lst, toks, cost in beams:
            cands = shortlist(s.prev_tag if s.prev_tag else "START")
            cands = topic_shortlist(ent.topic, cands, k=top_k or len(cands))
            for tok in cands:
                sF = forward_step(s, tok, prm, ent)
                rep = 0.2 if (s.last_token == tok) else 0.0
                must_close = 0.2 if ((s.open_det>0 or s.open_verb>0) and prm.horizon<=2) else 0.0
                local = 0.2*abs(sF.PI) - 0.2*(_closure_bonus(s, CAT[tok])) + rep + must_close
                cand.append((sF, lst+[sF], toks+[tok], cost+local))
        cand.sort(key=lambda x: x[3])
        beams = cand[:prm.beam] if cand else beams
    return [Tail(states=lst, toks=toks, cost=cost) for (_, lst, toks, cost) in beams]

def energy_for_token(tok: str, s_t: State, prm: Params, ent: Entity) -> Tuple[float, Dict[str,float]]:
    sF = forward_step(s_t, tok, prm, ent)
    sR = retro_step(sF, tok, prm, ent)
    seam = seam_residual(sF, sR)
    tails = greedy_completions(sF, prm, ent, top_k=8)
    bestE = float("inf"); parts_best={}
    rep = 0.4 if (s_t.last_token == tok) else 0.0
    for tl in tails if tails else [Tail(states=[sF], toks=[tok], cost=0.0)]:
        DR = dark_residue(tl.states, ent)
        ST = float(np.mean([jac_instability(st, tok, prm, ent) for st in tl.states]))
        CF = tl.cost
        E = seam + prm.lam_DR*DR + prm.lam_stab*ST + prm.lam_cost*CF + rep
        if E < bestE:
            bestE = E; parts_best = {"seam":seam,"DR":DR,"ST":ST,"CF":CF,"rep":rep}
    return bestE, parts_best

def stable_softmax(xs: List[float]) -> List[float]:
    m = max(xs); ys = [math.exp(min(700.0, max(-700.0, x-m))) for x in xs]
    Z = sum(ys); return [y/Z if Z>0 else 1.0/len(xs) for y in ys]

def predict_next_token(s_t: State, prm: Params, ent: Entity) -> Tuple[str, float, Dict[str,Dict[str,float]]]:
    prev = s_t.prev_tag if s_t.prev_tag else "START"
    cands = shortlist(prev); cands = topic_shortlist(ent.topic, cands, k=12)
    if not cands: cands = [w for (w,_) in TOKENS]
    Es=[]; parts_list=[]
    for tok in cands:
        E, parts = energy_for_token(tok, s_t, prm, ent)
        Es.append(-prm.beta*E); parts_list.append((tok, parts))
    ps = stable_softmax(Es)
    i = int(np.argmax(ps))
    return cands[i], float(ps[i]), dict(parts_list)

# ----------------------
# Seance Decoder (SMC over Params/Entity)
# ----------------------
NEUTRAL_PRM = Params()
NEUTRAL_ENT = Entity(K_t=1.0, Gamma=1.0, K_i=1.0, topic=None)

@dataclass
class Particle:
    prm: Params
    ent: Entity
    logw: float = 0.0

def param_prior(topic_pool=None, rng=None) -> Particle:
    rng = rng or random.Random()
    horizon = rng.choice([3,4,5])
    beam    = rng.choice([2,3])
    beta    = rng.choice([8.0,10.0,12.0])
    K_t   = 1.0 + rng.uniform(-0.15, 0.15)
    Gamma = 1.0 + rng.uniform(-0.15, 0.15)
    K_i   = 1.0 + rng.uniform(-0.15, 0.15)
    topic_vec = None
    if topic_pool:
        name, vec = rng.choice(topic_pool); topic_vec = vec
    prm = Params(horizon=horizon, beam=beam, beta=beta)
    ent = Entity(K_t=K_t, Gamma=Gamma, K_i=K_i, topic=topic_vec)
    return Particle(prm=prm, ent=ent, logw=0.0)

def _loglik_token(s_t: State, tok: str, p: Particle) -> float:
    E, _ = energy_for_token(tok, s_t, p.prm, p.ent)
    return - p.prm.beta * E

def _logsumexp(xs: List[float]) -> float:
    m = max(xs); s = sum(math.exp(x-m) for x in xs)
    return m + math.log(s) if s>0 else -1e9

def _norm_weights(parts: List[Particle]) -> List[float]:
    m = max(p.logw for p in parts)
    ws = [math.exp(p.logw - m) for p in parts]
    Z = sum(ws) or 1.0
    return [w/Z for w in ws]

def _ess(parts: List[Particle]) -> float:
    ws = _norm_weights(parts); return 1.0 / (sum(w*w for w in ws) + 1e-12)

def _resample(parts: List[Particle], rng=None) -> List[Particle]:
    rng = rng or random.Random()
    N = len(parts); ws = _norm_weights(parts)
    cdf = []; c=0.0
    for w in ws: c+=w; cdf.append(c)
    u0 = rng.random()/N; idx=[]; j=0
    for i in range(N):
        u = u0 + i*(1.0/N)
        while u > cdf[j]: j+=1
        idx.append(j)
    out = [Particle(prm=replace(parts[j].prm), ent=replace(parts[j].ent), logw=0.0) for j in idx]
    return out

def _adapt_particle(s_t: State, tok: str, p: Particle, rng=None) -> None:
    rng = rng or random.Random()
    E, parts = energy_for_token(tok, s_t, p.prm, p.ent)
    seam = parts.get("seam", 0.0); DR = parts.get("DR", 0.0)
    if seam > 0.8 and p.prm.horizon < 6 and rng.random()<0.5: p.prm.horizon += 1
    if seam > 0.8 and p.prm.beam < 4 and rng.random()<0.5: p.prm.beam += 1
    if DR > 0.6:
        p.ent.Gamma = max(0.7, min(1.3, p.ent.Gamma*1.02))
        p.ent.K_i   = max(0.7, min(1.3, p.ent.K_i*1.02))
    if DR < 0.3: p.prm.beta = min(16.0, p.prm.beta + 0.3)

class SeanceDecoder:
    def __init__(self, N_parts=24, seed=13, topic_pool=None):
        self.rng = random.Random(seed)
        if topic_pool is None:
            # singletons + a few noun/adj pairs (limited)
            nouns_adjs = [w for (w,t) in TOKENS if t in ("N","ADJ")]
            pool = [(w, EMB[w]) for w in nouns_adjs]
            pairs = []
            for i,a in enumerate(nouns_adjs):
                for b in nouns_adjs[i+1:i+6]:
                    pairs.append( (f"{a}+{b}", (EMB[a]+EMB[b])/2) )
            pool += pairs[:12]
            topic_pool = pool
        self.parts = [param_prior(topic_pool, self.rng) for _ in range(N_parts)]

    def next_token(self, s_t: State) -> Tuple[str, Dict[str,float]]:
        cands = shortlist(s_t.prev_tag if s_t.prev_tag else "START")
        cands = topic_shortlist(None, cands, k=12)  # neutral shortlist across particles
        if not cands: cands = [w for (w,_) in TOKENS]
        # aggregate token posterior
        logP = {tok: -1e9 for tok in cands}
        for p in self.parts:
            for tok in cands:
                ll = _loglik_token(s_t, tok, p) + p.logw
                logP[tok] = np.logaddexp(logP[tok], ll)
        m = max(logP.values()); Z = sum(math.exp(v-m) for v in logP.values()) or 1.0
        post = {tok: math.exp((v-m))/Z for tok,v in logP.items()}
        tok_star = max(post.items(), key=lambda kv: kv[1])[0]
        # weight update
        for p in self.parts:
            p.logw += _loglik_token(s_t, tok_star, p)
        # resample if needed
        if _ess(self.parts) < len(self.parts)/2.0:
            self.parts = _resample(self.parts, self.rng)
        # tiny adaptation
        for i in range(len(self.parts)):
            if self.rng.random() < 0.5:
                _adapt_particle(s_t, tok_star, self.parts[i], self.rng)
        return tok_star, post

# ----------------------
# Demos
# ----------------------
def generate_autopoietic(decoder, steps=22, seed=0):
    rng = random.Random(seed)
    s = State(prev_tag="START"); toks=[]
    for _ in range(steps):
        if isinstance(decoder, SeanceDecoder):
            tok, post = decoder.next_token(s)
        else:
            tok, p, _ = predict_next_token(s, Params(), Entity())
        toks.append(tok)
        s = forward_step(s, tok, NEUTRAL_PRM, NEUTRAL_ENT)  # neutral advance
        if CAT[tok] in ("ADV","V","N") and rng.random()<0.12:
            break
    return toks

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--parts", type=int, default=24)
    ap.add_argument("--steps", type=int, default=22)
    ap.add_argument("--seed", type=int, default=7)
    args = ap.parse_args()

    if args.demo:
        dec = SeanceDecoder(N_parts=args.parts, seed=args.seed)
        toks = generate_autopoietic(decoder=dec, steps=args.steps, seed=args.seed)
        print("[Seance Demo]", " ".join(toks))
    else:
        print("Use --demo to run a short autopoietic sample.")

if __name__ == "__main__":
    main()
