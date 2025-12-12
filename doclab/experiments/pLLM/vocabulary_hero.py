import numpy as np
import time
import sys
import random

# ---------------------------------------------------------------------------
# CONFIGURATION: The Physics of the Mini-Verse
# ---------------------------------------------------------------------------
EMBED_DIM = 16        # The dimensionality of a "Thought"
STATIC_DIM = 32       # The complexity of the "Intent" (Genome size)
LEARNING_RATE = 0.2   # How much the Short Term (Static) imprints on Long Term
MUTATION_RATE = 0.1   # How wildly the agent guesses new intents
POPULATION_SIZE = 50  # How many parallel "thoughts" it tries at once

target_text = "Call me Ishmael. Some years ago never mind how long precisely having little or no money in my purse and nothing particular to interest me on shore I thought I would sail about a little and see the watery part of the world."

# ---------------------------------------------------------------------------
# THE MIND: Mini Pirouette Cell
# ---------------------------------------------------------------------------
class PirouetteCell:
    def __init__(self, vocab_size, embed_dim):
        self.vocab_size = vocab_size
        self.embed_dim = embed_dim
        
        # LONG TERM MEMORY (The Tangle)
        # Maps Embedding -> Embedding transformation
        # Randomized initialization representing chaotic potential
        self.W_long_term = np.random.randn(embed_dim, embed_dim) * 0.1
        
        # WORD EMBEDDINGS (The Dictionary)
        # We learn these or keep them random? Let's keep them random but fixed per word
        # to simulate "Qualia" (the intrinsic feeling of a word).
        self.embeddings = {} 

    def get_embedding(self, word_idx):
        if word_idx not in self.embeddings:
            # Create a new random sensory pattern for this new word
            self.embeddings[word_idx] = np.random.randn(self.embed_dim)
        return self.embeddings[word_idx]

    def predict(self, current_word_idx, static_vec, candidates):
        """
        The Core Mechanism:
        Input (Word) + Intent (Static) -> Transformation -> Nearest Neighbor in Vocab
        """
        # 1. Sensation: Get the embedding of the current context word
        input_vec = self.get_embedding(current_word_idx)
        
        # 2. Intent: Unpack the Static Vector into a transient weight matrix
        # This is the "Bifurcation" - applying a temporary personality to the mind
        # We project STATIC_DIM down to (EMBED_DIM * EMBED_DIM)
        # To keep it fast, we just tile/slice.
        W_static_flat = np.tile(static_vec, (self.embed_dim * self.embed_dim) // len(static_vec) + 1)
        W_static = W_static_flat[:self.embed_dim * self.embed_dim].reshape(self.embed_dim, self.embed_dim)
        
        # 3. Processing: The "Thought"
        # The output is a mix of Habit (Long Term) and Will (Static)
        # Output = (W_long + W_static) @ Input
        combined_weights = self.W_long_term + W_static
        thought_vector = np.tanh(combined_weights @ input_vec) # Tanh for non-linearity
        
        # 4. Articulation: Find the closest word in the known dictionary (candidates)
        best_word = None
        best_score = -np.inf
        
        # We only look at words we "know" (the candidates)
        for word, idx in candidates.items():
            target_embed = self.get_embedding(idx)
            # Cosine similarity
            score = np.dot(thought_vector, target_embed) / (np.linalg.norm(thought_vector) * np.linalg.norm(target_embed) + 1e-9)
            
            if score > best_score:
                best_score = score
                best_word = word
                
        return best_word, thought_vector, W_static

    def learn(self, successful_W_static):
        """
        Hebbian Imprinting:
        When an Intent (Static) works, it leaves a residue in the Long Term Memory.
        The 'Will' becomes 'Habit'.
        """
        self.W_long_term = self.W_long_term + (successful_W_static * LEARNING_RATE)
        # Normalize to prevent explosion (The Coherence Clamp)
        self.W_long_term = np.clip(self.W_long_term, -1.0, 1.0)

# ---------------------------------------------------------------------------
# THE GAME ENGINE
# ---------------------------------------------------------------------------
def play_vocabulary_hero():
    print(f"\n--- INITIATING MINI PIROUETTE: VOCABULARY HERO ---")
    print(f"Target Text: \"{target_text[:40]}...\"")
    print(f"Physics: Embed={EMBED_DIM}, Static={STATIC_DIM}, Pop={POPULATION_SIZE}\n")
    MUTATION_RATE=1
    words = target_text.split()
    vocab = {"<START>": 0}
    next_id = 1
    
    # The Mind
    agent = PirouetteCell(vocab_size=1000, embed_dim=EMBED_DIM)
    
    total_generations = 0
    history_log = []
    
    previous_word = "<START>"
    
    for i, target_word in enumerate(words):
        # 1. Discovery: Add word to known vocabulary if new
        clean_target = target_word.strip(".,").lower() # Simple normalization
        
        if clean_target not in vocab:
            vocab[clean_target] = next_id
            next_id += 1
            is_new = True
        else:
            is_new = False
            
        target_idx = vocab[clean_target]
        prev_idx = vocab[previous_word.strip(".,").lower()] if previous_word != "<START>" else 0
        
        print(f"\n[Level {i+1}] Context: '{previous_word}' -> Target: '{target_word}'")
        print(f"   Vocab Size: {len(vocab)} | Known: {list(vocab.keys())[-5:]}...")
        
        # 2. The Struggle (Optimization Loop)
        # We need to find a Static Vector that makes the agent say 'target_word'
        
        solved = False
        generations = 0
        
        # Initialize Population (Random Intents)
        population = [np.random.randn(STATIC_DIM) for _ in range(POPULATION_SIZE)]
        
        start_time = time.time()
        
        while not solved:
            generations += 1
            scores = []
            
            best_gen_guess = ""
            
            # Evaluate Population
            for genome in population:
                guessed_word, thought_vec, _ = agent.predict(prev_idx, genome, vocab)
                
                # Fitness Function
                # If correct word: max reward
                if guessed_word == clean_target:
                    score = 100.0
                    solved = True
                    winning_genome = genome
                    best_gen_guess = guessed_word
                    break # Found it!
                
                # Partial Reward: Vector closeness (Proximity in semantic space)
                # This guides the evolution even if the word is wrong
                target_embed = agent.get_embedding(target_idx)
                similarity = np.dot(thought_vec, target_embed)
                score = similarity
                
                scores.append((score, genome))
                best_gen_guess = guessed_word
            
            if solved:
                break
                
            # Evolution (Selection + Mutation)
            # Sort by score descending
            scores.sort(key=lambda x: x[0], reverse=True)
            
            # Elitism: Keep top 20%
            cutoff = int(POPULATION_SIZE * 0.2)
            survivors = [s[1] for s in scores[:cutoff]]
            
            # Breeding: Create next gen
            new_population = survivors[:] # Keep elites
            while len(new_population) < POPULATION_SIZE:
                parent = random.choice(survivors)
                # Mutation: Add static noise
                child = parent + (np.random.randn(STATIC_DIM) * MUTATION_RATE)
                new_population.append(child)
            
            population = new_population
            
            # Visual Feedback
            if generations % 10 == 0:
                sys.stdout.write(f"\r   Gen {generations}: Best guess '{scores[0][1][:0]}' (Sim: {scores[0][0]:.2f}) -> '{best_gen_guess}'   ")
                sys.stdout.flush()
                
                # Failsafe for impossible words (if vocab collision is too high)
                if generations > 500:
                    print("\n   [!] Panic: Increasing Mutation Rate (High Entropy Mode)")
                    MUTATION_RATE *= 1.5
        
        # 3. Success & Consolidation
        elapsed = time.time() - start_time
        print(f"\r   [✓] Solved in {generations} gens ({elapsed:.2f}s).")
        
        # IMPRINTING: The Agent learns from this victory
        # We extract the matrix form of the winning static vector
        _, _, winning_W_static = agent.predict(prev_idx, winning_genome, vocab)
        agent.learn(winning_W_static)
        
        total_generations += generations
        previous_word = target_word
        history_log.append((target_word, generations))

    # ---------------------------------------------------------------------------
    # END GAME STATS
    # ---------------------------------------------------------------------------
    print("\n" + "="*40)
    print("       SEQUENCE COMPLETE")
    print("="*40)
    print(f"Total 'Mental Effort' (Generations): {total_generations}")
    print(f"Final Vocab Size: {len(vocab)}")
    print("\nEffort Profile (Hardest Words):")
    
    # Sort by difficulty
    sorted_log = sorted(history_log, key=lambda x: x[1], reverse=True)
    for word, gens in sorted_log[:5]:
        print(f"   '{word}': {gens} gens")

if __name__ == "__main__":
    play_vocabulary_hero()