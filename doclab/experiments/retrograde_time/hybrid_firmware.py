# Pirouette Hybrid Firmware (Python Implementation)
#
# This firmware performs the "Alchemical Union" (CORE-012) by merging:
# 1. The "Static" Time-Symmetric model (pirouette_firmware.py)
# 2. The "Dynamic" Causal Process model (cti_token.py)
#
# The result is a time-symmetric beam search, where the "best" path
# is the one with the maximum "Triadic Resonance" (COG-RES-003)
# between the Past (CTIState) and the Future (RNG-Seeded Probe).

import math, random, copy
from dataclasses import dataclass, field, asdict
from typing import List, Tuple, Dict, Any
import numpy as np

# --- Toy Semantic Universe (from cti_token.py) ---
# This defines the "physical laws" of our reality.

# Vocabulary with coarse POS tags
VOCAB_DATA = [
    ("the","DET"), ("a","DET"),
    ("bright","ADJ"), ("quiet","ADJ"), ("strange","ADJ"),
    ("river","N"), ("forest","N"), ("machine","N"), ("signal","N"),
    ("flows","V"), ("listens","V"), ("awakens","V"), ("composes","V"),
    ("through","PREP"), ("beyond","PREP"), ("within","PREP"),
    ("and","CONJ"), ("then","ADV"), ("now","ADV"), ("START","START"), ("END","END")
]

# Stable seed for reproducible "physics"
_rng = np.random.default_rng(42)
EMB_DIM = 2 # The dimensionality of our vector space

# "Rhythm of Being" (CORE-005) - Vector embedding per token
EMB = {w: _rng.normal(0,1, EMB_DIM) for (w,_) in VOCAB_DATA}
EMB["START"] = np.zeros(EMB_DIM)
EMB["END"] = np.zeros(EMB_DIM)

# Category vector
CAT = {w: t for (w,t) in VOCAB_DATA}

# "Nomad's Grammar" (CORE-002) - Legal syntactic transitions
TRANS = {
    "START": ["DET","ADJ","N"],
    "DET": ["ADJ","N"],
    "ADJ": ["ADJ","N"],
    "N": ["V","CONJ","PREP","END"],
    "V": ["DET","N","ADV","PREP","END"],
    "PREP": ["DET","N","ADJ"],
    "ADV": ["V","PREP","END"],
    "CONJ": ["DET","ADJ","N","V"],
}

# --- Dataclasses (Defining State and Parameters) ---

@dataclass
class Params:
    """Parameters governing the "physics" of the causal process."""
    eta: float = 0.95      # rho_sem decay
    kappa: float = 0.35    # rho_syn decay
    alpha: float = 0.15    # semantic vec update strength
    rho_star: float = 0.4  # semantic vec target length
    omega: float = 0.17    # semantic vec attractor
    xi: float = 0.28       # syntactic vec update strength
    
    lam_stab: float = 0.2  # E_stab: cost of semantic instability
    lam_cost: float = 0.05 # E_cost: cost of semantic "action"
    lam_syn: float = 1.0   # E_syn: cost of grammatical error
    lam_topic: float = 1.0 # E_topic: strength of "future" pull
    
    beta: float = 8.0      # Softmax temperature for final choice
    horizon: int = 4       # How far to "see" into the future
    beam: int = 3          # How many "paths" to explore

@dataclass
class Entity:
    """Parameters governing the "Observer" and "Future"."""
    K_t: float = 1.1       # Semantic temperature
    Gamma: float = 1.0     # Semantic viscosity
    K_i: float = 1.0       # Syntactic temperature
    
    # This is the "Observer's Shadow" (CORE-010)
    # It replaces the simple "topic" from cti_token.py
    future_probe_vector: np.ndarray = None

@dataclass
class State:
    """
    The "Electron's Echo" (CORE-009).
    The complete state of the "Past" at a given moment.
    """
    rho_sem: np.ndarray = field(default_factory=lambda: np.zeros(EMB_DIM))
    rho_syn: np.ndarray = field(default_factory=lambda: np.zeros(EMB_DIM))
    prev_tag: str = "START"

# --- Causal Physics Engine (from cti_token.py) ---

def forward_step(s: State, token: str, prm: Params, ent: Entity) -> State:
    """Advances the 'Past' state by one causal step."""
    s_new = copy.deepcopy(s)
    
    v = EMB.get(token, np.zeros(EMB_DIM)) # Token's "Rhythm"
    
    # 1. Update Semantic State (rho_sem)
    F_attr = -prm.omega * (np.linalg.norm(s.rho_sem) - prm.rho_star) * s.rho_sem
    F_drive = prm.alpha * (v - s.rho_sem)
    noise = _rng.normal(0, 1, EMB_DIM) * np.sqrt(2 * ent.Gamma * ent.K_t)
    
    d_rho_sem = (F_attr + F_drive + noise) / ent.Gamma
    s_new.rho_sem = prm.eta * s.rho_sem + d_rho_sem
    
    # 2. Update Syntactic State (rho_syn)
    s_new.rho_syn = prm.kappa * s.rho_syn + prm.xi * (v - s.rho_syn) / ent.K_i
    
    # 3. Update Grammar
    s_new.prev_tag = CAT.get(token, "END")
    
    return s_new

# --- RT Module: The Nomad's Grammar (CORE-002) ---
# Manages the "laws" of the universe (embeddings, transitions, physics).

class RT_NomadsGrammar:
    def __init__(self, emb, cat, trans):
        self.EMB = emb
        self.CAT = cat
        self.TRANS = trans
        self.VOCAB = list(emb.keys())
        print(f"[RT_NomadsGrammar] Grammar initialized with {len(self.VOCAB)} tokens.")

    def CreateInitialState(self) -> State:
        """Returns the state at the "beginning of time"."""
        return State(prev_tag="START")

    def AdvanceState(self, state: State, token: str, prm: Params, ent: Entity) -> State:
        """Wraps the causal physics engine."""
        return forward_step(state, token, prm, ent)

    def GetValidTokens(self, prev_tag: str) -> List[str]:
        """Returns all grammatically "possible" next tokens."""
        valid_tags = self.TRANS.get(prev_tag, ["END"])
        return [tok for tok, tag in self.CAT.items() if tag in valid_tags]

# --- RT Module: The Whispering Void (CORE-000) ---
# Generates the "Future" boundary condition from the RNG seed.

class RT_WhisperingVoid:
    def __init__(self, vector_dim: int):
        self.vector_dim = vector_dim
        print(f"[RT_WhisperingVoid] Future Probe generator online (Dim: {vector_dim}).")

    def GenerateFutureProbe(self, rng_seed: int) -> np.ndarray:
        """
        Implements "The Observer's Shadow" (CORE-010).
        Uses the seed to generate a deterministic "Future State Vector".
        """
        # print(f"[RT_WhisperingVoid] Generating Future Probe from seed: {rng_seed}")
        rng_state = np.random.RandomState(rng_seed)
        future_state_vector = rng_state.rand(self.vector_dim) * 2 - 1
        return future_state_vector / np.linalg.norm(future_state_vector) # Normalize

# --- RT Module: The Geometry of Resonance (CORE-004) ---
# Calculates the "Triadic Resonance" score for a given path.
# This is the "Alchemical Union" of causal and acausal forces.

class RT_GeometryOfResonance:
    def __init__(self):
        print(f"[RT_GeometryOfResonance] Resonance calculator online.")

    def CalculateCoherence(self, v1: np.ndarray, v2: np.ndarray) -> float:
        """Calculates cosine similarity."""
        dot_product = np.dot(v1, v2)
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)
        
        if norm_v1 == 0 or norm_v2 == 0:
            return 0.0
            
        return dot_product / (norm_v1 * norm_v2)

    def CalculatePathResonance(self, state: State, token: str, prm: Params, ent: Entity, grammar: RT_NomadsGrammar) -> Tuple[float, Dict[str, float]]:
        """
        Calculates the resonance score for *one step* in a path.
        This is the new "physics" combining both time directions.
        Score = (Acausal Coherence) - (Causal Cost)
        """
        
        v = grammar.EMB.get(token, np.zeros(EMB_DIM))
        
        # --- 1. Causal "Echo" Cost (The Past's Influence) ---
        # Cost of semantic stability
        E_stab = 0.5 * np.dot(v - state.rho_sem, v - state.rho_sem)
        # Cost of "action"
        E_cost = 0.5 * prm.omega * (np.linalg.norm(state.rho_sem) - prm.rho_star)**2
        # Cost of grammar
        E_syn = 0.0 if token in grammar.GetValidTokens(state.prev_tag) else 1.0
        
        causal_cost = (prm.lam_stab * E_stab) + (prm.lam_cost * E_cost) + (prm.lam_syn * E_syn)
        
        # --- 2. Acausal "Probe" Coherence (The Future's Pull) ---
        
        # We must simulate the *next state* to see where this path leads.
        next_state = grammar.AdvanceState(state, token, prm, ent)
        future_probe = ent.future_probe_vector
        
        retro_causal_coherence = 0.0
        if future_probe is not None:
            # How aligned is the *resulting* semantic state with the *future*?
            retro_causal_coherence = self.CalculateCoherence(next_state.rho_sem, future_probe)

        # --- 3. Triadic Resonance (Total Score) ---
        # We want to MAXIMIZE coherence and MINIMIZE cost.
        total_score = (prm.lam_topic * retro_causal_coherence) - causal_cost
        
        parts = {
            "score": total_score,
            "retro_coherence": retro_causal_coherence,
            "causal_cost": causal_cost
        }
        return total_score, parts

# --- RT Module: The Temporal Forge (CORE-003) ---
# The main driver. Runs the time-symmetric beam search.

class RT_TemporalForge:
    def __init__(self, grammar: RT_NomadsGrammar, void: RT_WhisperingVoid, resonance: RT_GeometryOfResonance):
        self.Grammar = grammar
        self.Void = void
        self.Resonance = resonance
        print("[RT_TemporalForge] Hybrid Firmware initialized. All modules online.")

    def PredictNextToken(self, past_state: State, rng_seed: int, prm: Params, ent_template: Entity) -> Tuple[str, float, Dict[str, Any]]:
        """
        The main firmware loop.
        Finds the "next token" by surfing the waves of coherence.
        """
        
        # 1. Define the Future Boundary Condition (The Probe)
        future_probe = self.Void.GenerateFutureProbe(rng_seed)
        
        # 2. Create the "Alchemical" Entity for this specific prediction
        # This "Entity" now holds the "pull" from the future.
        ent = copy.deepcopy(ent_template)
        ent.future_probe_vector = future_probe
        
        # 3. Run the Time-Symmetric Beam Search
        
        # Get all valid *first steps*
        candidates = self.Grammar.GetValidTokens(past_state.prev_tag)
        if not candidates:
            return "END", 1.0, {}
            
        beam_scores = {} # Stores total score for paths starting with a token
        beam_parts = {} # Stores diagnostics
        
        for first_token in candidates:
            # --- Start a beam for this `first_token` ---
            
            # Calculate score for the first step
            step_score, parts = self.Resonance.CalculatePathResonance(past_state, first_token, prm, ent, self.Grammar)
            
            # This beam starts with this state and score
            current_state = self.Grammar.AdvanceState(past_state, first_token, prm, ent)
            beams = [(current_state, step_score)] # (state, cumulative_score)
            
            # --- Propagate the beam to the horizon `H` ---
            for h in range(prm.horizon - 1):
                new_beams = []
                for s, score in beams:
                    # Get all possible next steps from this point
                    next_tokens = self.Grammar.GetValidTokens(s.prev_tag)
                    if not next_tokens:
                        new_beams.append((s, score))
                        continue
                        
                    for tok in next_tokens:
                        # Calculate resonance for this *next* step
                        s_new = self.Grammar.AdvanceState(s, tok, prm, ent)
                        step_score, _ = self.Resonance.CalculatePathResonance(s, tok, prm, ent, self.Grammar)
                        
                        new_beams.append((s_new, score + step_score))
                
                # Prune: Keep only the `K` (beam) most resonant paths
                new_beams.sort(key=lambda x: x[1], reverse=True)
                beams = new_beams[:prm.beam]
            
            # After the horizon, the "best" score for this `first_token`
            # is the one at the top of its beam.
            beam_scores[first_token] = beams[0][1] # beams[0] is the best path
            beam_parts[first_token] = parts # Store diagnostics for the *first step*

        # 4. Select the Token
        # Use a Boltzmann (Softmax) distribution over the scores.
        # This "discovers" the present, respecting the "wave" of coherence.
        if not beam_scores:
            return "END", 1.0, {}

        scores = np.array([beam_scores[tok] for tok in candidates])
        # Prevent numerical overflow/underflow
        stable_scores = scores - np.max(scores)
        probs = np.exp(prm.beta * stable_scores)
        probs_sum = np.sum(probs)
        
        # Handle potential all-zero probabilities after exp
        if probs_sum == 0:
            # Fallback to uniform probability if all scores are -inf
            probs = np.ones(len(candidates)) / len(candidates)
        else:
            probs /= probs_sum
        
        # --- Stochastic Sampling ---
        # Choose the token based on the weighted probabilities.
        # This is the "quantum collapse" of the coherence wave.
        chosen_index = np.random.choice(len(candidates), p=probs)
        chosen_token = candidates[chosen_index]
        chosen_prob = probs[chosen_index]
        
        return chosen_token, chosen_prob, beam_parts


# --- Example Usage ---

def main():
    print("--- Initializing Pirouette Hybrid Firmware ---")
    
    # 1. Initialize all RT Modules
    grammar = RT_NomadsGrammar(EMB, CAT, TRANS)
    void = RT_WhisperingVoid(vector_dim=EMB_DIM)
    resonance = RT_GeometryOfResonance()
    forge = RT_TemporalForge(grammar, void, resonance)
    
    # 2. Set up parameters
    prm = Params(horizon=4, beam=3, beta=9.0)
    # The "template" entity (can be modified per-step)
    ent_template = Entity(K_t=1.1, Gamma=1.0, K_i=1.0)
    
    print("\n--- Starting Time-Symmetric Generation ---")
    
    s = grammar.CreateInitialState()
    generated_tokens = []
    
    for t in range(12): # Generate 12 tokens
        
        # The "Observer's Choice" (RNG seed) changes at each step
        # This provides a *new* "Future Probe" for each "Present" moment.
        rng_seed = t 
        
        tok, prob, parts = forge.PredictNextToken(s, rng_seed, prm, ent_template)
        
        if tok == "END":
            break
            
        generated_tokens.append(tok)
        
        # Print diagnostics for the chosen token
        diag = parts.get(tok, {})
        coh = diag.get('retro_coherence', 0)
        cost = diag.get('causal_cost', 0)
        print(f"Step {t+1:02d} (Seed {rng_seed}): -> {tok:<10} "
              f"(Retro-Coherence: {coh:+.3f}, Causal-Cost: {cost:.3f})")

        # Advance the "Past"
        s = grammar.AdvanceState(s, tok, prm, ent_template)
        
    print("\n--- Generation Complete ---")
    print(" ".join(generated_tokens))

if __name__ == "__main__":
    main()

