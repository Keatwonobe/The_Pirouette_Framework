import gymnasium as gym
import numpy as np
import random
import copy
import math
import warnings

# Suppress runtime warnings from random math (div by zero, etc)
warnings.filterwarnings('ignore')

# ============================================================
# 1. THE VOCABULARY (Atoms of Math)
# ============================================================

OPS = {
    'ADD': lambda x, y: x + y,
    'SUB': lambda x, y: x - y,
    'MUL': lambda x, y: x * y,
    'DIV': lambda x, y: np.divide(x, y + 1e-9), # Safe division
    'SIN': lambda x: np.sin(x),
    'COS': lambda x: np.cos(x),
    'TANH': lambda x: np.tanh(x),
    'ABS':  lambda x: np.abs(x),
}

ARITY = {
    'ADD': 2, 'SUB': 2, 'MUL': 2, 'DIV': 2,
    'SIN': 1, 'COS': 1, 'TANH': 1, 'ABS': 1
}

# ============================================================
# 2. THE EQUATION TREE (The Genome)
# ============================================================

class Node:
    def __init__(self, value, children=None):
        self.value = value  # 'ADD', 'm', 'l', 0.5, etc.
        self.children = children if children else []

    def evaluate(self, m, l):
        # 1. LEAF NODES
        if not self.children:
            if self.value == 'm': return m
            if self.value == 'l': return l
            if isinstance(self.value, (int, float)): return self.value
            return 0.0

        # 2. OPERATOR NODES
        try:
            args = [child.evaluate(m, l) for child in self.children]
            return OPS[self.value](*args)
        except:
            return 0.0 # Fail safe

    def __repr__(self):
        if not self.children:
            if isinstance(self.value, float): return f"{self.value:.2f}"
            return str(self.value)
        if len(self.children) == 1:
            return f"{self.value}({self.children[0]})"
        return f"({self.children[0]} {self.value} {self.children[1]})"

    def deep_copy(self):
        return copy.deepcopy(self)

# ============================================================
# 3. THE ALCHEMIST (Generator & Mutator)
# ============================================================

class SymbolicAlchemist:
    def __init__(self, max_depth=5):
        self.max_depth = max_depth
        self.terminals = ['m', 'l', 'const']

    def generate_random_tree(self, depth=0):
        if depth >= self.max_depth or (depth > 1 and random.random() < 0.3):
            choice = random.choice(self.terminals)
            if choice == 'const': return Node(np.random.normal(0, 1.0))
            return Node(choice)
        
        op = random.choice(list(OPS.keys()))
        children = [self.generate_random_tree(depth + 1) for _ in range(ARITY[op])]
        return Node(op, children)

    def mutate(self, parent_node):
        child = parent_node.deep_copy()
        nodes_list = self._get_all_nodes(child)
        if not nodes_list: return child
        
        target = random.choice(nodes_list)
        mutation_type = random.choice(['logic_flip', 'number_shift', 'graft'])

        # TYPE 1: LOGIC FLIP
        if mutation_type == 'logic_flip' and isinstance(target.value, str) and target.value in OPS:
            current_arity = ARITY[target.value]
            candidates = [k for k, v in ARITY.items() if v == current_arity]
            if candidates: target.value = random.choice(candidates)

        # TYPE 2: NUMBER SHIFT
        elif mutation_type == 'number_shift' and isinstance(target.value, (int, float)):
            target.value += np.random.normal(0, 0.2)

        # TYPE 3: GRAFT
        elif mutation_type == 'graft':
            new_limb = self.generate_random_tree(depth=1)
            target.value = new_limb.value
            target.children = new_limb.children

        return child

    def _get_all_nodes(self, node):
        nodes = [node]
        for c in node.children:
            nodes.extend(self._get_all_nodes(c))
        return nodes

# ============================================================
# 4. SYMBOLIC PHYSICS (The Hypernet)
# ============================================================

class SymbolicTopologicalHypernet:
    def __init__(self, input_dim, output_dim, equation_tree):
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.total_weights = input_dim * output_dim
        self.equation = equation_tree
        
    def get_gradients(self, x, y):
        h = 0.01
        try:
            v_curr = self.equation.evaluate(x, y)
            v_x = self.equation.evaluate(x + h, y)
            v_y = self.equation.evaluate(x, y + h)
            
            dV_dx = (v_x - v_curr) / h
            dV_dy = (v_y - v_curr) / h
            
            # Clip gradients to prevent explosion
            return np.clip(dV_dx, -5, 5), np.clip(dV_dy, -5, 5)
        except:
            return 0.0, 0.0

    def generate_weights(self):
        weights = []
        # Start the flow at a fixed point to be deterministic per tree
        curr_m, curr_l = 0.5, -0.5 
        dt = 0.1
        
        # We need enough weights to fill the matrix
        steps_needed = (self.total_weights // 2) + 2
        
        for _ in range(steps_needed):
            grad_m, grad_l = self.get_gradients(curr_m, curr_l)
            
            # Topological Flow: Gradient Descent + Twist
            # This turns the static equation into a dynamic orbit
            curr_m += dt * (grad_m + (curr_l * 0.5))
            curr_l += dt * (grad_l - (curr_m * 0.5))
            
            # Activation function for weights
            w1 = np.tanh(curr_m)
            w2 = np.tanh(curr_l)
            weights.extend([w1, w2])
            
        return np.array(weights[:self.total_weights], dtype=np.float32)

# ============================================================
# 5. THE AGENT
# ============================================================

class SymbolicAgent:
    def __init__(self, obs_dim, act_dim, tree):
        self.obs_dim = obs_dim
        self.act_dim = act_dim
        self.tree = tree
        self.hypernet = SymbolicTopologicalHypernet(obs_dim, act_dim, tree)
        
        # Bake the weights once at initialization
        # (The math doesn't change during the lifetime of the agent)
        raw_weights = self.hypernet.generate_weights()
        self.weight_matrix = raw_weights.reshape(act_dim, obs_dim)

    def get_action(self, obs):
        # Simple Linear Policy: Action = Weights @ Obs
        return np.tanh(self.weight_matrix @ obs)

# ============================================================
# 6. GENETIC PROGRAMMING TRAINER
# ============================================================

class SymbolicTrainer:
    def __init__(self, env_name, pop_size=20):
        self.env_name = env_name
        self.pop_size = pop_size
        self.alchemist = SymbolicAlchemist()
        
        dummy = gym.make(env_name)
        self.obs_dim = dummy.observation_space.shape[0]
        self.act_dim = dummy.action_space.shape[0]
        dummy.close()
        
        # Initialize Population with Random Math
        self.population = [self.alchemist.generate_random_tree() for _ in range(pop_size)]
        self.generation = 0
        self.best_tree = None
        self.best_score = -9999

    def evaluate(self, tree, render=False):
        try:
            agent = SymbolicAgent(self.obs_dim, self.act_dim, tree)
        except Exception as e:
            # If the math is so bad it crashes generation (e.g. overflow), it dies.
            return -500.0

        env = gym.make(self.env_name, render_mode="human" if render else None)
        obs, _ = env.reset()
        total_reward = 0
        steps = 0
        
        # BipedalWalker Limit
        max_steps = 1600 if render else 500
        
        while steps < max_steps:
            action = agent.get_action(obs)
            obs, reward, term, trunc, _ = env.step(action)
            total_reward += reward
            steps += 1
            if term or trunc: break
            
            # Early stopping for falling
            if total_reward < -100: break
            
        env.close()
        return total_reward

    def evolve(self, generations=10):
        print(f"⚗️ SYMBOLIC ALCHEMIST: {self.env_name}")
        print(f"   Evolving Mathematical Physics to solve walking.")

        for g in range(generations):
            scores = []
            print(f"\n--- Gen {g} ---")
            
            for i, tree in enumerate(self.population):
                score = self.evaluate(tree)
                scores.append(score)
                
                # Print the "Equation" of the best performers
                if score > 0:
                    print(f"   Org {i}: {score:.1f} | V = {tree}")
            
            # Statistics
            avg_score = np.mean(scores)
            max_score = np.max(scores)
            best_idx = np.argmax(scores)
            
            print(f"   Avg: {avg_score:.1f} | Max: {max_score:.1f}")
            
            if max_score > self.best_score:
                self.best_score = max_score
                self.best_tree = self.population[best_idx].deep_copy()
                print(f"   ★ NEW LAW OF PHYSICS DISCOVERED!")
                print(f"   V(m,l) = {self.best_tree}")

            # SELECTION (Tournament)
            new_pop = []
            # Elitism: Keep the best
            new_pop.append(self.best_tree.deep_copy())
            
            while len(new_pop) < self.pop_size:
                # Tournament size 3
                candidates = random.sample(list(enumerate(self.population)), 3)
                # Winner is one with highest score
                winner_idx, _ = max(candidates, key=lambda x: scores[x[0]])
                parent = self.population[winner_idx]
                
                # MUTATION
                child = self.alchemist.mutate(parent)
                new_pop.append(child)
            
            self.population = new_pop

        return self.best_tree

if __name__ == "__main__":
    # Create the trainer
    trainer = SymbolicTrainer("BipedalWalker-v3", pop_size=16)
    
    # Run evolution
    # Note: BipedalWalker is hard. Expect negative scores initially.
    # Positive scores mean it is actually walking forward.
    best_math = trainer.evolve(generations=20)
    
    print("\nSimulating Best Found Physics...")
    trainer.evaluate(best_math, render=True)