import numpy as np
import random
import copy

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
    'SQ':   lambda x: x**2,
}

# Arity = Number of arguments the operator takes
ARITY = {
    'ADD': 2, 'SUB': 2, 'MUL': 2, 'DIV': 2,
    'SIN': 1, 'COS': 1, 'TANH': 1, 'SQ': 1
}

# ============================================================
# 2. THE EQUATION TREE
# ============================================================

class Node:
    def __init__(self, value, children=None):
        self.value = value  # Can be an OP string ('ADD'), a VAR string ('m', 'l'), or a float
        self.children = children if children else []

    def evaluate(self, m, l):
        """ Recursively solve the math question. """
        # 1. LEAF NODES (Variables or Constants)
        if not self.children:
            if self.value == 'm': return m
            if self.value == 'l': return l
            if isinstance(self.value, (int, float)): return self.value
            return 0.0

        # 2. OPERATOR NODES
        args = [child.evaluate(m, l) for child in self.children]
        return OPS[self.value](*args)

    def __repr__(self):
        if not self.children:
            return f"{self.value:.2f}" if isinstance(self.value, float) else str(self.value)
        if len(self.children) == 1:
            return f"{self.value}({self.children[0]})"
        return f"({self.children[0]} {self.value} {self.children[1]})"

# ============================================================
# 3. THE ALCHEMIST (Generator & Mutator)
# ============================================================

class SymbolicAlchemist:
    def __init__(self, max_depth=4):
        self.max_depth = max_depth
        self.terminals = ['m', 'l', 'const']

    def generate_random_tree(self, depth=0):
        # If we hit max depth, force a terminal (leaf)
        if depth >= self.max_depth or (depth > 1 and random.random() < 0.3):
            choice = random.choice(self.terminals)
            if choice == 'const':
                return Node(np.random.normal(0, 1.0))
            return Node(choice)
        
        # Otherwise, pick an operator
        op = random.choice(list(OPS.keys()))
        children = [self.generate_random_tree(depth + 1) for _ in range(ARITY[op])]
        return Node(op, children)

    def mutate(self, parent_node):
        """ 
        The Core Logic: 
        Returns a MODIFIED version of the math equation.
        """
        # Deep copy to ensure we don't break the parent history
        child = copy.deepcopy(parent_node)
        
        nodes_list = self._get_all_nodes(child)
        target = random.choice(nodes_list)
        
        mutation_type = random.choice(['logic_flip', 'number_shift', 'graft'])

        # TYPE 1: LOGIC FLIP (Change + to *, or sin to cos)
        if mutation_type == 'logic_flip' and hasattr(target, 'value') and isinstance(target.value, str):
            # Find ops with same arity (don't swap sin with add)
            current_arity = ARITY.get(target.value, 0)
            candidates = [k for k, v in ARITY.items() if v == current_arity]
            if candidates:
                target.value = random.choice(candidates)

        # TYPE 2: NUMBER SHIFT (Nudge constants)
        elif mutation_type == 'number_shift' and isinstance(target.value, (int, float)):
            target.value += np.random.normal(0, 0.1)

        # TYPE 3: GRAFT (Replace a limb with a new random limb)
        elif mutation_type == 'graft':
            # We can't easily replace "self" inside the object, 
            # so we modify the target's attributes to match a new random tree
            new_limb = self.generate_random_tree(depth=1)
            target.value = new_limb.value
            target.children = new_limb.children

        return child

    def _get_all_nodes(self, node):
        """ Helper to flatten tree for random selection """
        nodes = [node]
        for c in node.children:
            nodes.extend(self._get_all_nodes(c))
        return nodes

# ============================================================
# 4. TOPOLOGICAL INTEGRATION (The Physics)
# ============================================================

class SymbolicTopologicalHypernet:
    def __init__(self, output_dim, equation_tree):
        self.output_dim = output_dim
        self.equation = equation_tree
        
    def get_potential(self, x, y):
        # Evaluate the Symbolic Tree
        return self.equation.evaluate(x, y)

    def get_gradients(self, x, y):
        """
        Since the math is random, we can't hardcode derivatives.
        We use Central Difference approximation to find the slope.
        """
        h = 0.001
        V = self.get_potential
        
        # dV/dx
        dV_dx = (V(x + h, y) - V(x - h, y)) / (2 * h)
        # dV/dy
        dV_dy = (V(x, y + h) - V(x, y - h)) / (2 * h)
        
        return dV_dx, dV_dy

    def generate_weights(self, m, lam):
        weights = []
        curr_m, curr_l = m, lam
        dt = 0.1
        
        # Visualize the "Math Identity" based on value at origin
        center_val = self.get_potential(0.5, 0.5)
        if center_val > 1.0: color = "Red"   # High Energy Math
        elif center_val < 0: color = "Teal"  # Negative Potential
        else:                color = "Gold"  # Balanced

        # THE ITERATIVE LOOP
        # We flow DOWN the gradients of the generated math equation
        for _ in range(self.output_dim // 2 + 1):
            
            grad_m, grad_l = self.get_gradients(curr_m, curr_l)
            
            # Simple Momentum/Gradient Flow
            # Note: We reverse grad to "slide down" the potential (or up, depending on desire)
            # Adding a twist term (curr_l * 0.5) keeps it from getting stuck in local minima
            curr_m += dt * (grad_m + (curr_l * 0.5))
            curr_l += dt * (grad_l - (curr_m * 0.5))
            
            # Clamp to prevent explosion from unstable math (e.g. division by zero)
            curr_m = np.tanh(curr_m) * 2.0
            curr_l = np.tanh(curr_l) * 2.0
            
            weights.extend([np.tanh(curr_m), np.tanh(curr_l)])
            
        return np.array(weights[:self.output_dim], dtype=np.float32), color

# ============================================================
# EXAMPLE USAGE
# ============================================================
if __name__ == "__main__":
    trainer = SymbolicAlchemist("BipedalWalker-v3")
    final_strip = trainer.run()
    
    print("\nVisualizing the Holodeck...")
    trainer.evaluate(final_strip, "EXHALE", render=True)