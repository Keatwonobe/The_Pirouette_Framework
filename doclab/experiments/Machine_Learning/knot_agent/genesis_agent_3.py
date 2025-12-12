import gymnasium as gym
import numpy as np
from collections import deque
import networkx as nx # Graph theory library to count cycles

# --- CONFIGURATION ---
COHERENCE_RADIUS = 0.15  # Distance to form an "Edge" between states
MIN_CYCLE_LENGTH = 4     # The "Residue" threshold. 3 is trivial. 4+ is structure.
MEMORY_WINDOW = 100      # How far back we look for topology

class HomologicalMemory:
    def __init__(self):
        self.trace = deque(maxlen=MEMORY_WINDOW)
        self.graph = nx.Graph()
        self.betti_1_score = 0 # The count of current stable loops

    def update(self, state, step_id):
        # 1. Add Node
        self.trace.append((step_id, state))
        self.graph.add_node(step_id, pos=state)

        # 2. Remove Old Nodes (Pressure Gamma)
        if len(self.trace) == MEMORY_WINDOW:
            oldest_id, _ = self.trace[0]
            if self.graph.has_node(oldest_id):
                self.graph.remove_node(oldest_id)

        # 3. Form Edges (Vietoris-Rips Construction)
        # Connect the new state to any past state within Radius
        # BUT only if they are not *immediately* adjacent in time (prevents trivial line segments)
        current_pos = state
        
        # We only check recent history to save CPU, but skipping immediate predecessor
        trace_list = list(self.trace)
        for i in range(len(trace_list) - 2): # Skip immediate parent
            past_id, past_pos = trace_list[i]
            
            # Weighted Euclidean distance (Focus on Angle for Pendulum)
            # Using the v1.1 Weights: 5.0 on Angle, 0.5 on Velocity
            dist = np.sqrt(5.0*(current_pos[2]-past_pos[2])**2 + 0.5*(current_pos[1]-past_pos[1])**2)
            
            if dist < COHERENCE_RADIUS:
                self.graph.add_edge(step_id, past_id)

    def calculate_topology(self):
        """
        Calculates the Betti-1 Number (Number of Cycles).
        Filters out 'Triangles' (Length 3) as trivial noise.
        """
        try:
            # Find all simple cycles in the graph
            # (This can be expensive, we limit depth in a real scenario)
            cycles = nx.cycle_basis(self.graph)
        except:
            return 0, 0

        trivial_loops = 0
        persistent_loops = 0
        
        for cycle in cycles:
            if len(cycle) <= 3:
                trivial_loops += 1
            else:
                persistent_loops += 1
                
        return trivial_loops, persistent_loops

class BettiAgent:
    def __init__(self, action_space):
        self.action_space = action_space
        self.memory = HomologicalMemory()
        self.step_counter = 0
        self.current_betti_score = 0

    def step(self, state, reward_from_env):
        # 1. Update Manifold
        self.memory.update(state, self.step_counter)
        self.step_counter += 1

        # 2. Calculate Homology (The "Ghost" Structure)
        # We do this every N steps to save compute
        intrinsic_reward = 0
        if self.step_counter % 5 == 0:
            trivial, persistent = self.memory.calculate_topology()
            
            # THE BETTI LOSS FUNCTION INVERSE (Intrinsic Reward)
            # We punish triangles (noise), we reward squares+ (structure)
            intrinsic_reward = (persistent * 10.0) - (trivial * 0.5)
            
            if persistent > self.current_betti_score:
                print(f"  [+] STRUCTURE GROWTH: Found {persistent} stable loops (Residue confirmed).")
                self.current_betti_score = persistent

        # 3. Decision Logic (Hybrid)
        # If intrinsic reward is high, repeat previous action (Gradient Ascent on Topology)
        # This is a very simple heuristic for the demo
        action = self.action_space.sample() # Default: Explore
        
        # In a full version, we would use the intrinsic_reward to update a Policy Network.
        # Here, we just observe the 'Growth of Structure'.
        
        return action, intrinsic_reward

# --- RUNNER ---
def run_betti_simulation():
    env = gym.make("InvertedPendulum-v5")
    agent = BettiAgent(env.action_space)
    
    print("--- HOMOLOGICAL AGENT (BETTI-1) ---")
    print("Objective: Maximize Non-Trivial Cycles (N >= 4)")
    
    state, _ = env.reset()
    total_structure_score = 0
    
    for i in range(1000):
        action, topo_reward = agent.step(state, 0)
        next_state, _, terminated, truncated, _ = env.step(action)
        
        state = next_state
        total_structure_score += topo_reward
        
        if terminated or truncated:
            state, _ = env.reset()
            # We don't reset memory! The agent 'remembers' the topology across episodes.
            
    print(f"--- SIMULATION END ---")
    print(f"Final Structural Accumulation: {total_structure_score}")

if __name__ == "__main__":
    run_betti_simulation()