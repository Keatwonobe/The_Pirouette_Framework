import numpy as np
import time
import sys
import random

# ---------------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------------
EMBED_DIM = 16
STATIC_DIM = 32
POPULATION_SIZE = 60
MAX_GENS_BEFORE_GROWTH = 300  # If we can't solve it in 300 gens, we grow.

target_text = "Call me Ishmael. Some years ago never mind how long precisely having little or no money in my purse and nothing particular to interest me on shore I thought I would sail about a little and see the watery part of the world."

# ---------------------------------------------------------------------------
# THE LOBE (Single Pirouette Loop)
# ---------------------------------------------------------------------------
class Lobe:
    def __init__(self, embed_dim, static_dim):
        self.embed_dim = embed_dim
        self.static_dim = static_dim
        # The "Habit" Matrix
        self.W_long_term = np.random.randn(embed_dim, embed_dim) * 0.1
        self.frozen = False # Once frozen, this lobe stops learning
        self.age = 0

    def process(self, input_vec, static_vec):
        """
        Returns the 'Thought Vector' for this specific lobe.
        """
        # Bifurcation: Map Static (Intent) to Weight Modulation
        W_static_flat = np.tile(static_vec, (self.embed_dim * self.embed_dim) // len(static_vec) + 1)
        W_static = W_static_flat[:self.embed_dim * self.embed_dim].reshape(self.embed_dim, self.embed_dim)
        
        # Combined Weight = Habit + Intent
        combined = self.W_long_term + W_static
        return np.tanh(combined @ input_vec)

    def learn(self, winning_static_vec, rate=0.2):
        if self.frozen:
            return
        # Hebbian Imprinting
        W_static_flat = np.tile(winning_static_vec, (self.embed_dim * self.embed_dim) // len(winning_static_vec) + 1)
        W_static = W_static_flat[:self.embed_dim * self.embed_dim].reshape(self.embed_dim, self.embed_dim)
        
        self.W_long_term += (W_static * rate)
        self.W_long_term = np.clip(self.W_long_term, -2.0, 2.0) # Clamp Coherence

# ---------------------------------------------------------------------------
# THE BRAIN (Multi-Lobe Manager)
# ---------------------------------------------------------------------------
class StratifiedBrain:
    def __init__(self, vocab_size):
        self.embed_dim = EMBED_DIM
        self.static_dim = STATIC_DIM
        self.lobes = [Lobe(EMBED_DIM, STATIC_DIM)] # Start with one lobe
        self.embeddings = {}
        self.vocab_size = vocab_size

    def get_embedding(self, word_idx):
        if word_idx not in self.embeddings:
            self.embeddings[word_idx] = np.random.randn(self.embed_dim)
        return self.embeddings[word_idx]

    def predict(self, current_word_idx, static_vec, candidates):
        input_vec = self.get_embedding(current_word_idx)
        
        # AGGREGATE THOUGHT: Sum of all Lobes
        # Each lobe processes the input with the SAME Static Intent
        total_thought = np.zeros(self.embed_dim)
        
        for lobe in self.lobes:
            total_thought += lobe.process(input_vec, static_vec)
        
        # Normalize the chaotic sum to keep it in the unit sphere
        total_thought = np.tanh(total_thought)

        # Find nearest word
        best_word = None
        best_score = -np.inf
        
        for word, idx in candidates.items():
            target_embed = self.get_embedding(idx)
            # Cosine Similarity
            score = np.dot(total_thought, target_embed) / (np.linalg.norm(total_thought) * np.linalg.norm(target_embed) + 1e-9)
            if score > best_score:
                best_score = score
                best_word = word
                
        return best_word, total_thought

    def learn(self, winning_static_vec):
        # Only the active (non-frozen) lobes learn
        # Usually only the newest one
        for lobe in self.lobes:
            lobe.learn(winning_static_vec)

    def grow(self):
        # Freeze current lobes to preserve their memory
        for lobe in self.lobes:
            lobe.frozen = True
        
        # Add a fresh lobe (New Capacity)
        print(f"\n   [+] GROWTH EVENT: Spawning Lobe {len(self.lobes) + 1}...")
        self.lobes.append(Lobe(self.embed_dim, self.static_dim))

# ---------------------------------------------------------------------------
# GAME LOOP
# ---------------------------------------------------------------------------
def play_stratified_hero():
    print(f"\n--- STRATIFIED PIROUETTE: MULTI-LOBE AGENT ---")
    
    words = target_text.split()
    vocab = {"<START>": 0}
    next_id = 1
    
    brain = StratifiedBrain(vocab_size=1000)
    
    previous_word = "<START>"
    history_log = []
    
    for i, target_word in enumerate(words):
        # Clean text
        clean_target = target_word.strip(".,").lower()
        if clean_target not in vocab:
            vocab[clean_target] = next_id
            next_id += 1
            
        target_idx = vocab[clean_target]
        prev_idx = vocab[previous_word.strip(".,").lower()] if previous_word != "<START>" else 0
        
        print(f"\n[Word {i+1}] '{previous_word}' -> '{target_word}' (Lobes: {len(brain.lobes)})")
        
        # Optimization Loop
        solved = False
        generations = 0
        population = [np.random.randn(STATIC_DIM) for _ in range(POPULATION_SIZE)]
        
        while not solved:
            generations += 1
            scores = []
            best_gen_guess = ""
            
            for genome in population:
                guess, thought_vec = brain.predict(prev_idx, genome, vocab)
                
                if guess == clean_target:
                    score = 100.0
                    solved = True
                    winning_genome = genome
                    break
                
                target_embed = brain.get_embedding(target_idx)
                sim = np.dot(thought_vec, target_embed)
                scores.append((sim, genome))
                best_gen_guess = guess
            
            if solved: 
                break
            
            # Evolution
            scores.sort(key=lambda x: x[0], reverse=True)
            survivors = [s[1] for s in scores[:int(POPULATION_SIZE * 0.2)]]
            
            new_pop = survivors[:]
            while len(new_pop) < POPULATION_SIZE:
                parent = random.choice(survivors)
                child = parent + (np.random.randn(STATIC_DIM) * 0.1)
                new_pop.append(child)
            population = new_pop
            
            # MONITOR STRESS
            if generations % 50 == 0:
                best_sim = scores[0][0]
                sys.stdout.write(f"\r   Gen {generations}: Best Sim {best_sim:.2f} (Guess: '{best_gen_guess}')")
                sys.stdout.flush()
            
            # THE GROWTH TRIGGER
            if generations >= MAX_GENS_BEFORE_GROWTH:
                sys.stdout.write("\n   [!] COHERENCE FAILURE DETECTED.")
                brain.grow() # Add new layer
                generations = 0 # Reset counter for new lobe
                population = [np.random.randn(STATIC_DIM) for _ in range(POPULATION_SIZE)] # Fresh thoughts

        print(f"\r   [✓] Solved in {generations} gens.")
        brain.learn(winning_genome)
        previous_word = target_word
        history_log.append(len(brain.lobes))

    print("\n" + "="*40)
    print(f"Final Structure: {len(brain.lobes)} Lobes")
    print("This agent grew a new brain region every time it got stuck.")

if __name__ == "__main__":
    play_stratified_hero()