import numpy as np
import time
import sys
import random

# ---------------------------------------------------------------------------
# CONFIGURATION: The "Classroom" Physics
# ---------------------------------------------------------------------------
EMBED_DIM = 16          # The "Thought" Resolution
STATIC_DIM = 32         # The "Intent" Complexity
CONTEXT_WINDOW = 3      # How far back we look (The Triangulation)
CHUNK_SIZE = 2          # The "Lesson Plan" size (New words per epoch)
POPULATION_SIZE = 50
MAX_GENS = 400          # Patience before Bifurcation

# Moby Dick Opening (extended for curriculum)
full_corpus = "Call me Ishmael. Some years ago never mind how long precisely having little or no money in my purse and nothing particular to interest me on shore I thought I would sail about a little and see the watery part of the world. It is a way I have of driving off the spleen and regulating the circulation. Whenever I find myself growing grim about the mouth whenever it is a damp drizzly November in my soul."

# ---------------------------------------------------------------------------
# THE LOBE (The Contextual Processor)
# ---------------------------------------------------------------------------
class ContextLobe:
    def __init__(self, input_dim, output_dim):
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.frozen = False
        
        # The "Habit" Matrix: Maps Context -> Prediction
        self.W_long_term = np.random.randn(output_dim, input_dim) * 0.05
        
    def process(self, context_vec, static_vec):
        # 1. The Intent Modulation (Bifurcation)
        # We stretch the static vector to match the weight matrix shape
        # This is "applying the will to the habit"
        W_static_flat = np.tile(static_vec, (self.output_dim * self.input_dim) // len(static_vec) + 1)
        W_static = W_static_flat[:self.output_dim * self.input_dim].reshape(self.output_dim, self.input_dim)
        
        # 2. The Resonance
        combined_weights = self.W_long_term + W_static
        
        # 3. Activation
        return np.tanh(combined_weights @ context_vec)

    def learn(self, winning_static_vec, rate=0.1):
        if self.frozen: return
        W_static_flat = np.tile(winning_static_vec, (self.output_dim * self.input_dim) // len(winning_static_vec) + 1)
        W_static = W_static_flat[:self.output_dim * self.input_dim].reshape(self.output_dim, self.input_dim)
        self.W_long_term += (W_static * rate)
        self.W_long_term = np.clip(self.W_long_term, -2.0, 2.0)

# ---------------------------------------------------------------------------
# THE BRAIN (Manages Embeddings + Lobes)
# ---------------------------------------------------------------------------
class ContextBrain:
    def __init__(self, vocab_size):
        self.vocab_size = vocab_size
        self.embed_dim = EMBED_DIM
        # Input to lobes is (Context_Window * Embed_Dim)
        self.context_dim = CONTEXT_WINDOW * EMBED_DIM
        
        self.lobes = [ContextLobe(self.context_dim, self.embed_dim)]
        self.embeddings = {}
        
        # Initialize <PAD> and <START>
        # FIX 1: Non-zero PAD. Silence must have texture.
        self.embeddings[0] = np.random.randn(EMBED_DIM) * 0.01 
        self.embeddings[1] = np.random.randn(EMBED_DIM) # START

    def get_context_vector(self, history_indices):
        # Concatenate the embeddings of the last N words
        # history_indices should be length CONTEXT_WINDOW
        vecs = []
        for idx in history_indices:
            if idx not in self.embeddings:
                # Semantic Initialization:
                # If we don't know the word, init it near the previous word
                self.embeddings[idx] = np.random.randn(self.embed_dim)
            vecs.append(self.embeddings[idx])
        return np.concatenate(vecs)

    def predict(self, history_indices, static_vec, known_vocab):
        context_vec = self.get_context_vector(history_indices)
        
        # Sum outputs from all lobes (ResNet style)
        total_thought = np.zeros(self.embed_dim)
        for lobe in self.lobes:
            total_thought += lobe.process(context_vec, static_vec)
            
        total_thought = np.tanh(total_thought) # Normalize
        
        # Find nearest neighbor
        best_word = None
        best_score = -np.inf
        
        for word, idx in known_vocab.items():
            # FIX 2: Lazy Initialization for Targets
            if idx not in self.embeddings:
                self.embeddings[idx] = np.random.randn(self.embed_dim)
            
            target_embed = self.embeddings[idx]
            score = np.dot(total_thought, target_embed)
            if score > best_score:
                best_score = score
                best_word = word
        
        return best_word, total_thought

    def learn(self, winning_static_vec):
        for lobe in self.lobes:
            lobe.learn(winning_static_vec)

    def grow(self):
        for lobe in self.lobes:
            lobe.frozen = True
        print(f"\n   [+] CORTICAL EXPANSION: Lobe {len(self.lobes)+1} added.")
        self.lobes.append(ContextLobe(self.context_dim, self.embed_dim))

# ---------------------------------------------------------------------------
# THE CURRICULUM MANAGER
# ---------------------------------------------------------------------------
def run_curriculum():
    print(f"--- CONTEXTUAL PIROUETTE: CURRICULUM MODE ---")
    print(f"Context: {CONTEXT_WINDOW} words | Chunk Size: {CHUNK_SIZE}")
    
    # Pre-process text
    clean_text = full_corpus.replace(".", " .").replace(",", " ,").lower().split()
    vocab = {"<PAD>": 0, "<START>": 1}
    next_id = 2
    
    brain = ContextBrain(1000)
    
    # Master Loop: Iterate through chunks
    current_word_index = 0
    total_words = len(clean_text)
    
    while current_word_index < total_words:
        # Define the "Lesson"
        end_index = min(current_word_index + CHUNK_SIZE, total_words)
        lesson_words = clean_text[current_word_index:end_index]
        
        print(f"\n" + "="*50)
        print(f"LESSON PLAN: Words {current_word_index}-{end_index}")
        print(f"Target Vocabulary: {lesson_words}")
        print("="*50)
        
        # Register new words in vocab
        for w in lesson_words:
            if w not in vocab:
                vocab[w] = next_id
                next_id += 1
        
        # TRAINING LOOP FOR THIS CHUNK
        
        for i, target_word in enumerate(lesson_words):
            # Global position in text
            global_pos = current_word_index + i
            
            # Build Context History
            history_idxs = []
            for k in range(CONTEXT_WINDOW):
                lookback = global_pos - (CONTEXT_WINDOW - k)
                # FIX 3: Correctly handle the START token logic
                if lookback < -1:
                    history_idxs.append(0) # PAD
                elif lookback == -1:
                    history_idxs.append(1) # START
                else:
                    past_word = clean_text[lookback]
                    history_idxs.append(vocab[past_word])
            
            target_id = vocab[target_word]
            
            # Show context for debugging
            context_words = []
            for h_idx in history_idxs:
                word = [k for k, v in vocab.items() if v == h_idx][0]
                context_words.append(word)
            
            print(f"\nTarget: '{target_word}' | Context: {context_words}")
            
            # EVOLUTION LOOP (Find the Static Vector)
            solved = False
            generations = 0
            pop = [np.random.randn(STATIC_DIM) for _ in range(POPULATION_SIZE)]
            
            while not solved:
                generations += 1
                scores = []
                
                for genome in pop:
                    guess, thought = brain.predict(history_idxs, genome, vocab)
                    if guess == target_word:
                        score = 100
                        solved = True
                        winning_genome = genome
                        break
                    
                    # Similarity Score
                    target_vec = brain.embeddings[target_id]
                    sim = np.dot(thought, target_vec)
                    scores.append((sim, genome))
                
                if solved: break
                
                # Breed
                scores.sort(key=lambda x: x[0], reverse=True)
                survivors = [s[1] for s in scores[:10]]
                pop = survivors[:]
                while len(pop) < POPULATION_SIZE:
                    parent = random.choice(survivors)
                    child = parent + (np.random.randn(STATIC_DIM) * 0.2)
                    pop.append(child)
                
                # Check for Bifurcation
                if generations > MAX_GENS:
                    print("   [!] STIFFNESS LIMIT REACHED.")
                    brain.grow()
                    generations = 0
                    # Reset population to give new lobe a fresh start
                    pop = [np.random.randn(STATIC_DIM) for _ in range(POPULATION_SIZE)]
            
            print(f"   [✓] Mastered in {generations} gens.")
            brain.learn(winning_genome)
            
        # End of Chunk
        current_word_index = end_index
        print(f"\n>>> CHUNK COMPLETE. Integrating Memories...")
        time.sleep(0.5)

    print("\n--- TRAINING COMPLETE ---")
    print(f"Final Brain Topology: {len(brain.lobes)} Lobes")

if __name__ == "__main__":
    run_curriculum()