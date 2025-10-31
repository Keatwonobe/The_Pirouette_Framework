
# cti_token.py
import math, random
from dataclasses import dataclass, asdict
from typing import List, Tuple, Dict
import numpy as np

# ----------------------
# Toy semantic universe
# ----------------------
# Vocabulary with coarse POS tags and a tiny "topic" embedding
TOKENS = [
    ("the","DET"), ("a","DET"),
    ("bright","ADJ"), ("quiet","ADJ"), ("strange","ADJ"),
    ("river","N"), ("forest","N"), ("machine","N"), ("signal","N"),
    ("flows","V"), ("listens","V"), ("awakens","V"), ("composes","V"),
    ("through","PREP"), ("beyond","PREP"), ("within","PREP"),
    ("and","CONJ"), ("then","ADV"), ("now","ADV")
]

# Stable seed for reproducibility
_rng = np.random.default_rng(42)

# topic embedding per token (2-D for visualization)
EMB = {w: _rng.normal(0,1,2) for (w,_) in TOKENS}
# category vector
CAT = {w: t for (w,t) in TOKENS}

# legal transitions (simple grammar)
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

# helper to shortlist candidates by POS
def shortlist(prev_tag: str) -> List[str]:
    next_tags = TRANS.get(prev_tag, TRANS["N"])
    cand = [w for (w,t) in TOKENS if t in next_tags]
    return cand

# ----------------------
# State & parameters
# ----------------------
@dataclass
class Params:
    # forward
    eta: float = 0.95        # semantic density memory
    kappa: float = 0.45      # injection from embedding norm
    alpha: float = 0.15      # pressure response to density mismatch
    rho_star: float = 0.6    # target semantic density
    omega: float = 0.25      # phase drift
    xi: float = 0.20         # phase kick per novelty
    c1: float = 0.2          # coherence bump on syntactic closure
    c2: float = 0.1          # penalty per |ΔP_I|
    # retro
    r_eta: float = 0.92
    r_alpha: float = -0.12
    r_bias_close: float = 0.25
    # energy weights
    lam_DR: float = 1.0
    lam_stab: float = 0.15
    lam_cost: float = 0.05
    beta: float = 9.0
    # rollout
    horizon: int = 4
    beam: int = 3
    eps_fd: float = 1e-3

@dataclass
class Entity:
    K_t: float = 1.0
    Gamma: float = 1.0
    K_i: float = 1.0
    topic: np.ndarray = None  # desired topic direction

@dataclass
class State:
    rhoI: float = 0.0
    PI: float = 0.0
    phi: float = 0.0
    C: float = 0.0
    open_det: int = 0     # pending DET->N closure
    open_verb: int = 0    # pending N->V closure (subject needs verb)
    prev_tag: str = "START"
    last_token: str = ""

def novelty(v: np.ndarray) -> float:
    return float(np.linalg.norm(v))

def closure_bonus(st: State, tag: str) -> float:
    bonus = 0.0
    # Close determiner chain when N appears within 2 steps
    if st.open_det>0 and tag=="N" and st.open_det<=2:
        bonus += 1.0
    # Close subject-verb within 3 steps
    if st.open_verb>0 and tag=="V" and st.open_verb<=3:
        bonus += 0.7
    return bonus

def forward_step(s: State, token: str, prm: Params, ent: Entity) -> State:
    s2 = State(**asdict(s))
    v = EMB[token]
    nov = novelty(v)
    # semantic density & pressure
    s2.rhoI = ent.K_i * (prm.eta * s.rhoI + prm.kappa * nov)
    dP = ent.K_t * (prm.alpha * (s2.rhoI - prm.rho_star))
    s2.PI = s.PI + dP
    # phase: novelty kick plus drift
    s2.phi = (s.phi + prm.omega + prm.xi * (nov>1.5)) % (2*np.pi)
    # coherence from syntactic closure
    tag = CAT[token]
    # maintain obligations
    if tag=="DET": s2.open_det = min(3, s.open_det+1)
    if tag=="N":
        if s.open_det>0: s2.open_det = 0
        if s.prev_tag in ("START","DET","ADJ"): s2.open_verb = min(3, s.open_verb+1)
    if tag=="V" and s.open_verb>0: s2.open_verb = 0
    # coherence scalar
    bonus = closure_bonus(s, tag) > 0.0
    s2.C = max(0.0, s.C + (prm.c1 if bonus else 0.0) - prm.c2 * abs(dP))
    s2.prev_tag = tag
    s2.last_token = token
    return s2

def retro_step(s_next: State, token: str, prm: Params, ent: Entity) -> State:
    sR = State(**asdict(s_next))
    # aim to reduce |PI|, close obligations quickly
    sR.rhoI = prm.r_eta * s_next.rhoI
    sR.PI = s_next.PI + prm.r_alpha * np.sign(s_next.PI) * ent.Gamma
    sR.phi = (s_next.phi - 0.5*prm.omega * np.tanh(s_next.PI)) % (2*np.pi)
    tag = s_next.prev_tag
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
    ph = np.array([s.phi for s in traj])
    dphi = np.diff(np.unwrap(ph)); phase_term = np.mean(np.abs(dphi)) if len(dphi)>0 else 0.0
    oblig = np.mean([0.5*s.open_det + 0.5*s.open_verb for s in traj])
    # topic alignment (prefer following entity topic if provided)
    if ent.topic is None:
        topic_term = 0.0
    else:
        toks = [s.last_token for s in traj if s.last_token]
        if toks:
            mean_vec = np.mean([EMB[t] for t in toks], axis=0)
            topic_term = float(1.0 - (np.dot(mean_vec, ent.topic) / (np.linalg.norm(mean_vec)+1e-8) / (np.linalg.norm(ent.topic)+1e-8)))
            topic_term = max(0.0, topic_term)
        else:
            topic_term = 0.0
    return 0.5*PI_term + 0.2*phase_term + 0.2*oblig + 0.1*topic_term

def jac_instability(s: State, token: str, prm: Params, ent: Entity) -> float:
    eps = prm.eps_fd
    sF = forward_step(s, token, prm, ent)
    s_eps = State(**asdict(s)); s_eps.rhoI += eps
    sF_eps = forward_step(s_eps, token, prm, ent)
    J = (sF_eps.rhoI - sF.rhoI) / eps
    return max(0.0, J - 1.0)

@dataclass
class Tail:
    states: list
    toks: list
    cost: float

def greedy_completions(s_start: State, prm: Params, ent: Entity, h: int, beam: int=3):
    beams = [(s_start, [], [], 0.0)]  # (state, states, toks, cost)
    for _ in range(h):
        cand = []
        cands = shortlist(s_start.prev_tag) if s_start.prev_tag else shortlist("START")
        if not cands: cands = [w for (w,_) in TOKENS]
        # Try all cands (small vocab); could prune by top-k novelty closeness
        for s, lst, toks, cost in beams:
            prev = s.prev_tag if s.prev_tag else "START"
            cands = shortlist(prev)
            for tok in cands:
                sF = forward_step(s, tok, prm, ent)
                # local cost: prefer obligation closure and moderate |PI|; penalize repetition
                rep = 0.2 if (s.last_token == tok) else 0.0
                local = 0.2*abs(sF.PI) - 0.2*closure_bonus(s, CAT[tok]) + rep
                cand.append((sF, lst+[sF], toks+[tok], cost+local))
        cand.sort(key=lambda x: x[3])
        beams = cand[:beam]
    return [Tail(states=lst, toks=toks, cost=cost) for (_, lst, toks, cost) in beams]

def energy_for_token(tok: str, s_t: State, prm: Params, ent: Entity):
    sF = forward_step(s_t, tok, prm, ent)
    sR = retro_step(sF, tok, prm, ent)
    seam = seam_residual(sF, sR)
    tails = greedy_completions(sF, prm, ent, h=prm.horizon-1, beam=prm.beam)
    bestE = float("inf"); parts_best={}
    rep = 0.4 if (s_t.last_token == tok) else 0.0
    for tl in tails:
        DR = dark_residue(tl.states, ent)
        ST = np.mean([jac_instability(st, tok, prm, ent) for st in tl.states])
        CF = tl.cost
        E = seam + prm.lam_DR*DR + prm.lam_stab*ST + prm.lam_cost*CF + rep
        if E < bestE:
            bestE = E
            parts_best = {"seam": seam, "DR": DR, "ST": ST, "CF": CF, "rep": rep}
    return bestE, parts_best

def stable_softmax(xs):
    m = max(xs); ys = [math.exp(min(700.0, max(-700.0, x-m))) for x in xs]
    Z = sum(ys); return [y/Z if Z>0 else 1.0/len(xs) for y in ys]

def predict_next_token(s_t: State, prm: Params, ent: Entity):
    prev = s_t.prev_tag if s_t.prev_tag else "START"
    cands = shortlist(prev)
    if not cands: cands = [w for (w,_) in TOKENS]
    Es = []; parts_list=[]
    for tok in cands:
        E, parts = energy_for_token(tok, s_t, prm, ent)
        Es.append(-prm.beta*E); parts_list.append((tok, parts))
    ps = stable_softmax(Es)
    # choose argmax
    i = int(np.argmax(ps))
    return cands[i], float(ps[i]), dict(parts_list)

# ----------------------
# Data generation & eval
# ----------------------

def gen_sentence(rng: random.Random, max_len=20):
    s = State(prev_tag="START")
    toks = []
    while len(toks) < max_len:
        cands = shortlist(s.prev_tag)
        tok = rng.choice(cands)
        s = forward_step(s, tok, Params(), Entity(K_t=1.0,Gamma=1.0,K_i=1.0))
        toks.append(tok)
        if CAT[tok] in ("ADV","V","N") and rng.random()<0.2:
            break
    return toks

def gen_corpus(n=64, seed=7):
    rng = random.Random(seed)
    return [gen_sentence(rng, max_len=16) for _ in range(n)]

def eval_next_token(corpus, prm: Params, ent: Entity):
    accs = []
    for sent in corpus:
        s = State(prev_tag="START")
        preds=[]; golds=[]
        for i in range(len(sent)-1):
            # update with current gold token, then predict the next
            s = forward_step(s, sent[i], prm, ent)
            gold_next = sent[i+1]
            pred, p, _ = predict_next_token(s, prm, ent)
            preds.append(pred); golds.append(gold_next)
        acc = np.mean([1.0 if p==g else 0.0 for p,g in zip(preds,golds)]) if golds else 0.0
        accs.append(acc)
    return float(np.mean(accs))

# === Seance Decoder (SMC over Params/Entity) ================================

from dataclasses import replace
import math, random

@dataclass
class Particle:
    prm: Params
    ent: Entity
    w: float = 1.0

def param_prior(topic_pool=None, rng=None):
    rng = rng or random.Random()
    # Discrete knobs from your good ridge; continuous small jitter
    horizon = rng.choice([3,4,5])
    beam    = rng.choice([2,3])
    beta    = rng.choice([8.0,10.0,12.0])
    # entity knobs near 1.0
    K_t   = 1.0 + rng.uniform(-0.15, 0.15)
    Gamma = 1.0 + rng.uniform(-0.15, 0.15)
    K_i   = 1.0 + rng.uniform(-0.15, 0.15)
    # topic as convex mix from pool
    if topic_pool:
        name, vec = rng.choice(topic_pool)
        topic_vec = vec
    else:
        topic_vec = None
    prm = Params(horizon=horizon, beam=beam, beta=beta)
    ent = Entity(K_t=K_t, Gamma=Gamma, K_i=K_i, topic=topic_vec)
    return Particle(prm=prm, ent=ent, w=1.0)

def stable_logsumexp(xs):
    m = max(xs); s = sum(math.exp(x-m) for x in xs)
    return m + math.log(s) if s>0 else -1e9

def particle_token_loglik(s_t: State, tok: str, part: Particle):
    # negative energy scaled by beta is a log-likelihood up to a constant
    E, _ = energy_for_token(tok, s_t, part.prm, part.ent)
    return - part.prm.beta * E

def shortlist_for_state(s_t: State):
    prev = s_t.prev_tag if s_t.prev_tag else "START"
    cands = shortlist(prev)
    return cands if cands else [w for (w,_) in TOKENS]

def effective_sample_size(parts):
    ws = [p.w for p in parts]
    s2 = sum(w*w for w in ws)
    return (sum(ws)**2) / s2 if s2>0 else 0.0

def systematic_resample(parts, rng=None):
    rng = rng or random.Random()
    N = len(parts)
    weights = [p.w for p in parts]
    S = sum(weights)
    if S <= 0:
        weights = [1.0/N]*N; S = 1.0
    cum = []
    c=0.0
    for w in weights:
        c += w/S; cum.append(c)
    u0 = rng.random()/N
    idx=[]; j=0
    for i in range(N):
        u = u0 + i*(1.0/N)
        while u > cum[j]:
            j += 1
        idx.append(j)
    new = []
    for j in idx:
        p = parts[j]
        new.append( Particle(prm=replace(p.prm), ent=replace(p.ent), w=1.0) )
    return new

def adapt_particle(s_t: State, chosen_tok: str, part: Particle, rng=None):
    """Heuristic micro-updates to ride the ridge; keeps it cheap & stable."""
    rng = rng or random.Random()
    # Peek at energy parts to steer knobs
    E, parts = energy_for_token(chosen_tok, s_t, part.prm, part.ent)
    seam = parts.get("seam", 0.0); DR = parts.get("DR", 0.0)
    # If seam high → try slightly longer horizon/beam (bounded)
    if seam > 0.8 and part.prm.horizon < 6 and rng.random()<0.5:
        part.prm.horizon += 1
    if seam > 0.8 and part.prm.beam < 4 and rng.random()<0.5:
        part.prm.beam += 1
    # If DR high → nudge dissipation/stiffness toward more stability
    if DR > 0.6:
        part.ent.Gamma = max(0.7, min(1.3, part.ent.Gamma * 1.02))
        part.ent.K_i   = max(0.7, min(1.3, part.ent.K_i   * 1.02))
    # Confidence sharpening: if posterior was very peaky, bump beta a touch
    part.prm.beta = max(4.0, min(16.0, part.prm.beta + (0.5 if DR < 0.3 else 0.0)))
    return part

def seance_predict_next(s_t: State, parts, rng=None):
    """Return next token + posterior, updating particle weights in-place."""
    rng = rng or random.Random()
    cands = shortlist_for_state(s_t)
    # 1) particle-wise log-liks
    ll_by_tok = {tok: [] for tok in cands}
    for p in parts:
        for tok in cands:
            ll = particle_token_loglik(s_t, tok, p)
            ll_by_tok[tok].append( ll + math.log(max(p.w, 1e-12)) )
    # 2) aggregate posterior over tokens
    logP = {tok: stable_logsumexp(v) for tok,v in ll_by_tok.items()}
    # normalize
    m = max(logP.values()); Z = sum(math.exp(v-m) for v in logP.values())
    post = {tok: (math.exp((v-m))/Z if Z>0 else 1.0/len(cands)) for tok,v in logP.items()}
    # pick argmax (or sample)
    tok_star = max(post.items(), key=lambda kv: kv[1])[0]
    # 3) weight update given chosen token
    for p in parts:
        p.w *= math.exp(particle_token_loglik(s_t, tok_star, p))
    # 4) resample if degenerate
    if effective_sample_size(parts) < len(parts)/2:
        parts[:] = systematic_resample(parts, rng)
    # 5) tiny adaptation
    for i in range(len(parts)):
        if rng.random() < 0.5:
            adapt_particle(s_t, tok_star, parts[i], rng)
    return tok_star, post

def run_seance_demo(N_parts=24, steps=20, seed=13):
    rng = random.Random(seed)
    # Topic pool: singletons + simple pairs
    pool = [(w, EMB[w]) for w,_ in TOKENS]
    pool += [ (f"{a}+{b}", (EMB[a]+EMB[b])/2) for a,_ in TOKENS for b,_ in TOKENS if a<b and CAT[a] in ("N","ADJ") and CAT[b] in ("N","ADJ") ][:12]
    # initialize particles
    parts = [param_prior(topic_pool=pool, rng=rng) for _ in range(N_parts)]
    s = State(prev_tag="START")
    toks = []
    for _ in range(steps):
        tok, post = seance_predict_next(s, parts, rng)
        toks.append(tok)
        s = forward_step(s, tok, parts[0].prm, parts[0].ent)  # advance state with any prm; state def is token-driven
        if CAT[tok] in ("ADV","V","N") and rng.random()<0.12:
            break
    return toks


# ----------------------
# Autopoietic generation
# ----------------------
def generate_autopoietic(prm: Params, ent: Entity, steps=20, seed=0):
    rng = random.Random(seed)
    s = State(prev_tag="START")
    toks = []
    for _ in range(steps):
        tok, p, _ = predict_next_token(s, prm, ent)
        toks.append(tok)
        s = forward_step(s, tok, prm, ent)
        if CAT[tok] in ("ADV","V","N") and rng.random()<0.15:
            break
    return toks

# ----------------------
# Demo
# ----------------------
def run_demo():
    prm = Params(horizon=4, beam=3, beta=9.0)
    # choose a topic (e.g., average of river/forest)
    topic = (EMB["river"] + EMB["forest"])/2
    ent = Entity(K_t=1.1, Gamma=1.0, K_i=1.0, topic=topic)
    corpus = gen_corpus(n=80, seed=11)
    acc = eval_next_token(corpus, prm, ent)
    auto = generate_autopoietic(prm, ent, steps=18, seed=3)
    return {"accuracy": acc, "autopoietic": auto}

if __name__ == "__main__":
    out = run_demo()
    run_seance_demo(N_parts=24, steps=20, seed=13)
    print(f"[CTI-Token] next-token accuracy={out['accuracy']:.3f}")
    print("Autopoietic sample:", " ".join(out["autopoietic"]))
