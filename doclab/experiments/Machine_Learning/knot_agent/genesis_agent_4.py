import gymnasium as gym
import numpy as np
from collections import deque
import networkx as nx
import random

# --- CONFIGURATION ---
MEMORY_WINDOW = 60        # Keep short to find "local" knots quickly
COHERENCE_RADIUS = 0.2    # How close states must be to connect
MIN_CYCLE_LENGTH = 4      # The "Residue" threshold
CHECK_INTERVAL = 10       # How often we check topology (in steps)

# ANNEALING PARAMS
MAX_TEMP = 1.0            # High Noise (Exploration/Panic)
MIN_TEMP = 0.01           # Low Noise (Exploitation/Flow)
COOLING_RATE = 0.1        # How fast we freeze when structure is found
HEATING_RATE = 0.05       # How fast we panic when structure is lost

class HomologicalMemory:
    def __init__(self):
        self.trace = deque(maxlen=MEMORY_WINDOW)
        self.graph = nx.Graph()

    def update(self, state, step_id):
        # 1. Add Node
        self.trace.append((step_id, state))
        self.graph.add_node(step_id, pos=state)

        # 2. Prune Graph (Forget old nodes)
        if len(self.trace) == MEMORY_WINDOW:
            oldest_id, _ = self.trace[0]
            if self.graph.has_node(oldest_id):
                self.graph.remove_node(oldest_id)

        # 3. Form Edges (Vietoris-Rips)
        # Connect current node to past nodes if geometrically close
        current_pos = state
        trace_list = list(self.trace)
        
        # Look back in time
        for i in range(len(trace_list) - 2): 
            past_id, past_pos = trace_list[i]
            
            # Weighted Distance (Focus on Angle)
            # State: [x, x_dot, theta, theta_dot]
            # We heavily weight Theta (index 2)
            dist = np.sqrt(5.0*(current_pos[2]-past_pos[2])**2 + 0.5*(current_pos[1]-past_pos[1])**2)
            
            if dist < COHERENCE_RADIUS:
                self.graph.add_edge(step_id, past_id)

    def count_residue(self):
        """
        Returns the number of Non-Trivial Loops (Length >= 4).
        This is the 'Betti-1' Score.
        """
        try:
            cycles = nx.cycle_basis(self.graph)
        except:
            return 0
            
        residue_count = 0
        for cycle in cycles:
            if len(cycle) >= MIN_CYCLE_LENGTH:
                residue_count += 1
        return residue_count

class AnnealingAgent:
    def __init__(self, action_space):
        self.action_space = action_space
        self.memory = HomologicalMemory()
        
        # State Variables
        self.temperature = MAX_TEMP
        self.step_counter = 0
        self.last_action = np.array([0.0]) # Start neutral
        self.best_betti = 0

    def step(self, state):
        # 1. Update Memory Manifold
        self.memory.update(state, self.step_counter)
        self.step_counter += 1

        # 2. Topological Check (The Feedback Loop)
        if self.step_counter % CHECK_INTERVAL == 0:
            betti_score = self.memory.count_residue()
            
            # --- THE ANNEALING LOGIC ---
            if betti_score > 0:
                # STRUCTURE DETECTED! 
                # We are forming a knot. "Freeze" this behavior.
                self.temperature = max(MIN_TEMP, self.temperature - COOLING_RATE)
                if betti_score > self.best_betti:
                    self.best_betti = betti_score
                    print(f"  [!] CRYSTALLIZING: Betti={betti_score} | Temp dropped to {self.temperature:.2f}")
            else:
                # NO STRUCTURE (Entropy). 
                # "Heat up" to break out of this useless path.
                self.temperature = min(MAX_TEMP, self.temperature + HEATING_RATE)

        # 3. Action Generation (Brownian Motion scaled by Temperature)
        # Action = Last_Action + Noise(Temperature)
        noise = np.random.normal(0, self.temperature, size=self.action_space.shape)
        
        # We dampen the last action slightly (friction) so it doesn't run away
        base_action = self.last_action * 0.9 
        
        new_action = base_action + noise
        new_action = np.clip(new_action, -3.0, 3.0) # Clip to env limits

        self.last_action = new_action
        return new_action

# --- RUNNER ---
def run_annealing_simulation():
    # Inverted Pendulum v5 is the standard balance task
    try:
        env = gym.make("InvertedPendulum-v5") 
    except:
        env = gym.make("InvertedPendulum-v4") # Fallback

    agent = AnnealingAgent(env.action_space)
    
    print("--- SELF-ANNEALING TOPOLOGICAL AGENT ---")
    print("Goal: Find a 'Cold' Geometry (Low Temp, High Structure)")
    
    episodes = 20
    
    for ep in range(episodes):
        state, _ = env.reset()
        terminated = False
        truncated = False
        steps = 0
        
        # Reset temp slightly between episodes to allow re-adaptation
        # But keep some 'muscle memory' (don't reset fully to 1.0)
        agent.temperature = 0.5 
        
        while not terminated and not truncated:
            action = agent.step(state)
            next_state, _, terminated, truncated, _ = env.step(action)
            
            state = next_state
            steps += 1
            
            if steps > 1000: truncated = True # Success condition

        print(f"Ep {ep+1}: Survived {steps} steps. Final Temp: {agent.temperature:.2f}. Best Structure: {agent.best_betti}")

    env.close()

if __name__ == "__main__":
    run_annealing_simulation()