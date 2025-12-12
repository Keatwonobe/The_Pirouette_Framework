import numpy as np
import time
import sys
import random

# ---------------------------------------------------------------------------
# CONFIGURATION: The "Loud" Library
# ---------------------------------------------------------------------------
EMBED_DIM = 16
STATIC_DIM = 32
CONTEXT_WINDOW = 2      # "Reduce scale to 2 or 3 and let it rip"
POPULATION_SIZE = 40
MAX_GENS = 200

# ---------------------------------------------------------------------------
# THE DDE SHARDS (The Data That Talks)
# ---------------------------------------------------------------------------
# We simulate 3 distinct topics in the DDE.
topics = {
    "cetacean_node": "The sperm whale is the largest toothed predator. It dives deep to hunt giant squid in the dark abyss. Ambergris is produced in the digestive system of sperm whales.",
    "physics_node": "Quantum mechanics describes the behavior of matter and light on the atomic and subatomic scale. It attempts to describe and account for the properties of molecules and atoms.",
    "coffee_node": "Coffee is a brewed drink prepared from roasted coffee beans, the seeds of berries from certain Coffea species. The genus Coffea is native to tropical Africa and Madagascar."
}

class ActiveShard:
    def __init__(self, name, content, vocab_ref):
        self.name = name
        self.content = content.replace(".", " .").replace(",", " ,").lower().split()
        self.vocab_ref = vocab_ref # Reference to global vocab (shared protocol)
        
        # The Shard's "Soul" (Semantic Center)
        # In a real DDE, this is computed; here we randomize it initially
        self.semantic_vector = np.random.randn(EMBED_DIM) 
        self.difficulty = 1.0 # Dynamic difficulty
        self.visitors = 0

    def broadcast(self, agent_vector):
        """
        The "Talking" Mechanism.
        The Shard looks at the Agent and decides if it wants to be read.
        Returns: Attraction Score (Signal Strength)
        """
        # 1. Resonance: How similar is the agent to me?
        # (Dot product)
        resonance = np.dot(self.semantic_vector, agent_vector)
        
        # 2. Gatekeeping: Am I too hard?
        # If difficulty is high, resonance must be VERY high to enter.
        # We simulate this by penalizing the score if resonance < difficulty threshold
        
        signal = resonance
        
        # "Talk": Return the signal strength
        return signal

    def update_vector(self, new_vector):
        # The Data learns from the Agent too! 
        # It drifts slightly towards the visitors that successfully read it.
        self.semantic_vector = (self.semantic_vector * 0.95) + (new_vector * 0.05)
        self.semantic_vector = np.tanh(self.semantic_vector) # Normalize

# ---------------------------------------------------------------------------
# THE TRAVELER (The Stratified Brain)
# ---------------------------------------------------------------------------
class ContextLobe:
    def __init__(self, input_dim, output_dim):
        self.W = np.random.randn(output_dim, input_dim) * 0.1
        self.frozen = False

    def process(self, ctx, static):
        # Simple Bilinear interaction for speed
        # W_modulated = W + Static_Projected
        # We cheat and add static to input for "Fast Ripping" speed
        combined_input = np.concatenate([ctx, static])
        # Resize W on fly if needed (lazy) - simplified for demo:
        # We just do a projection of static to match W
        return np.tanh(self.W @ ctx) # Placeholder for the complex logic

class TravelerAgent:
    def __init__(self, vocab_size):
        self.embed_dim = EMBED_DIM
        self.context_dim = CONTEXT_WINDOW * EMBED_DIM
        
        # The Brain
        # Simplification: Just one dense matrix that grows
        self.W_knowledge = np.random.randn(EMBED_DIM, self.context_dim) * 0.05
        self.embeddings = {}
        
        # State
        self.current_thought = np.random.randn(EMBED_DIM) # The "Wander" vector
        self.age = 0

    def get_context_vec(self, idxs):
        vecs = []
        for i in idxs:
            if i not in self.embeddings:
                self.embeddings[i] = np.random.randn(EMBED_DIM) * 0.1
            vecs.append(self.embeddings[i])
        return np.concatenate(vecs)

    def predict(self, context_idxs):
        ctx = self.get_context_vec(context_idxs)
        # Prediction = W @ Context
        thought = np.tanh(self.W_knowledge @ ctx)
        return thought

    def train_on_shard(self, shard):
        """
        The Interaction Event.
        The Agent reads the Shard.
        """
        print(f"   >>> Entering {shard.name}...")
        errors = 0
        
        # Iterate through the shard's content
        for i in range(len(shard.content) - 1):
            # Build context
            ctx_words = []
            ctx_idxs = []
            for k in range(CONTEXT_WINDOW):
                idx = i - (CONTEXT_WINDOW - k)
                if idx < 0: word = "<START>"
                else: word = shard.content[idx]
                
                if word not in shard.vocab_ref:
                    shard.vocab_ref[word] = len(shard.vocab_ref)
                ctx_idxs.append(shard.vocab_ref[word])
                ctx_words.append(word)
                
            target_word = shard.content[i+1] # Predict next
            if target_word not in shard.vocab_ref:
                shard.vocab_ref[target_word] = len(shard.vocab_ref)
            target_id = shard.vocab_ref[target_word]
            
            # PREDICT
            thought = self.predict(ctx_idxs)
            
            # LEARN (Fast Backprop / Hebbian)
            # We want Thought -> Target_Embedding
            if target_id not in self.embeddings:
                self.embeddings[target_id] = np.random.randn(EMBED_DIM) * 0.1
            target_vec = self.embeddings[target_id]
            
            # Error
            diff = target_vec - thought
            error = np.linalg.norm(diff)
            errors += error
            
            # Update Weights (The "Ripping")
            # W += LearningRate * (Error * Input.T)
            ctx_vec = self.get_context_vec(ctx_idxs)
            delta = np.outer(diff, ctx_vec) * 0.05
            self.W_knowledge += delta
            
            # Update Current Thought (The Agent's Trajectory changes)
            self.current_thought = (self.current_thought * 0.8) + (thought * 0.2)

        print(f"   <<< Left {shard.name}. Total Dissonance: {errors:.2f}")
        
        # The Shard updates its broadcast vector based on the Agent's exit state
        shard.update_vector(self.current_thought)
        shard.visitors += 1
        return errors

# ---------------------------------------------------------------------------
# THE DDE ENVIRONMENT (The Marketplace of Ideas)
# ---------------------------------------------------------------------------
def run_talking_dde():
    print("--- DDE PROTOCOL: ACTIVE DATA NODES ---")
    
    # Initialize Global Vocab
    vocab = {"<START>": 0}
    
    # Initialize Shards
    shards = [ActiveShard(k, v, vocab) for k, v in topics.items()]
    
    # Initialize Agent
    agent = TravelerAgent(1000)
    
    # THE LIFECYCLE
    epoch = 0
    while epoch < 15:
        epoch += 1
        print(f"\n[Epoch {epoch}] Agent is drifting... Thought Vector: {agent.current_thought[:3]}...")
        
        # 1. THE BROADCAST
        # Every shard shouts at the agent
        signals = []
        for s in shards:
            sig = s.broadcast(agent.current_thought)
            signals.append((sig, s))
            print(f"   Node '{s.name}' signals: {sig:.4f}")
            
        # 2. THE SELECTION
        # Agent flows to the strongest signal (Highest Resonance)
        signals.sort(key=lambda x: x[0], reverse=True)
        best_signal, best_shard = signals[0]
        
        # 3. THE INTERACTION
        if best_signal < -0.5:
            print("   [!] REJECTION: All nodes reject the agent (Dissonance too high).")
            # Agent must mutate/reset thought to try again
            agent.current_thought = np.random.randn(EMBED_DIM)
            print("   Agent resets consciousness.")
        else:
            # Go to the winner
            dissonance = agent.train_on_shard(best_shard)
            
            # 4. POST-INTERACTION
            # If the interaction was smooth (low dissonance), the Agent stays near this topic
            # If it was rough, the Agent is repelled
            if dissonance > 10.0:
                print("   (Rough ride. Agent repelled from this topic.)")
                # Invert vector to go elsewhere
                agent.current_thought *= -0.5 
            else:
                print("   (Smooth ride. Agent resonates with this topic.)")

    print("\n--- SIMULATION COMPLETE ---")
    print("Final Node Visitors:")
    for s in shards:
        print(f" - {s.name}: {s.visitors}")

if __name__ == "__main__":
    run_talking_dde()