import gymnasium as gym
import numpy as np
from collections import deque
import networkx as nx
import random

# --- CONFIGURATION ---
MEMORY_WINDOW = 100       
COHERENCE_RADIUS = 0.25   # Slightly looser to allow "catching" the loop
MIN_CYCLE_LENGTH = 4      
CHECK_INTERVAL = 5        # Check faster

class StableLoop:
    def __init__(self, start_state, action_sequence, betti_score):
        self.start_state = start_state
        self.actions = action_sequence
        self.betti_score = betti_score
        self.usage = 0

class HolonomicAgent:
    def __init__(self, action_space):
        self.action_space = action_space
        
        # Short Term Memory (The Trace)
        self.trace_states = deque(maxlen=MEMORY_WINDOW)
        self.trace_actions = deque(maxlen=MEMORY_WINDOW)
        
        # Long Term Memory (The Library)
        self.engrams = [] 
        
        # State
        self.step_counter = 0
        self.active_engram = None
        self.playback_index = 0
        self.temperature = 1.0

    def detect_topology(self):
        """
        Builds a graph from recent history and counts holes.
        Returns: Betti Number, Start Index of the Loop
        """
        if len(self.trace_states) < MIN_CYCLE_LENGTH:
            return 0, 0

        # Build Graph
        graph = nx.Graph()
        states = list(self.trace_states)
        
        # Add nodes
        for i in range(len(states)):
            graph.add_node(i)

        # Add edges (Geometry Check)
        # Connect points that are close in phase space
        for i in range(len(states)):
            for j in range(i + 2, len(states)): # Skip immediate neighbors
                # Weighted distance (Focus on Angle)
                s1 = states[i]
                s2 = states[j]
                dist = np.sqrt(5.0*(s1[2]-s2[2])**2 + 0.5*(s1[1]-s2[1])**2)
                
                if dist < COHERENCE_RADIUS:
                    graph.add_edge(i, j)

        # Count Cycles
        try:
            cycles = nx.cycle_basis(graph)
        except:
            return 0, 0
            
        betti = 0
        best_loop_start = -1
        
        for cycle in cycles:
            if len(cycle) >= MIN_CYCLE_LENGTH:
                betti += 1
                # Find the earliest point in this cycle
                start_node = min(cycle)
                if best_loop_start == -1 or start_node < best_loop_start:
                    best_loop_start = start_node
                    
        return betti, best_loop_start

    def crystallize(self, betti, start_index):
        """
        Saves the successful sequence to Long Term Memory.
        """
        # Extract the sequence from the start of the loop to Now
        # Note: We grab the actions that CAUSED the loop
        raw_actions = list(self.trace_actions)
        saved_actions = raw_actions[start_index:]
        start_state = self.trace_states[start_index]
        
        # Optimization: Don't save duplicate weak loops
        for engram in self.engrams:
            dist = np.linalg.norm(engram.start_state - start_state)
            if dist < 0.1:
                return # We already know this spot

        new_knot = StableLoop(start_state, saved_actions, betti)
        self.engrams.append(new_knot)
        # Sort by complexity (Try the most complex knots first)
        self.engrams.sort(key=lambda x: x.betti_score, reverse=True)
        
        print(f"  [!] ENGRAM FORMED: Betti={betti} | Length={len(saved_actions)} | Total Engrams={len(self.engrams)}")

    def step(self, state):
        # 1. CHECK FOR REPLAY (Muscle Memory)
        if self.active_engram:
            if self.playback_index < len(self.active_engram.actions):
                action = self.active_engram.actions[self.playback_index]
                self.playback_index += 1
                # We still record this! Replaying strengthens the memory.
                self.trace_states.append(state)
                self.trace_actions.append(action)
                return action
            else:
                # Sequence finished
                self.active_engram = None
                self.playback_index = 0

        # 2. CHECK FOR TRIGGER (Resonance)
        # Can we switch to auto-pilot?
        for engram in self.engrams:
            # Check if current state matches engram start
            dist = np.sqrt(5.0*(state[2]-engram.start_state[2])**2 + 0.5*(state[1]-engram.start_state[1])**2)
            if dist < COHERENCE_RADIUS:
                self.active_engram = engram
                self.playback_index = 0
                engram.usage += 1
                # print(f"    >>> RESONANCE: Playing Engram (Betti {engram.betti_score})")
                return self.step(state)

        # 3. EXPLORE (Brownian Motion)
        self.trace_states.append(state)
        
        # Detect Structure while exploring
        if self.step_counter % CHECK_INTERVAL == 0:
            betti, start_idx = self.detect_topology()
            if betti > 0:
                self.crystallize(betti, start_idx)
                # OPTIONAL: Immediately switch to replaying what we just found?
                # For now, let's keep exploring to see if it gets better.

        action = self.action_space.sample()
        self.trace_actions.append(action)
        
        self.step_counter += 1
        return action

# --- RUNNER ---
def run_holonomic_simulation():
    try:
        env = gym.make("InvertedPendulum-v5")
    except:
        env = gym.make("InvertedPendulum-v4")

    agent = HolonomicAgent(env.action_space)
    
    print("--- CORE-027: RE-ENTRANT HOLONOMY AGENT ---")
    print("Goal: Capture Betti Loops and Replay them (Muscle Memory).")
    
    episodes = 50
    
    for ep in range(episodes):
        state, _ = env.reset()
        terminated = False
        truncated = False
        steps = 0
        
        # Clear Short Term Memory on reset, but KEEP Engrams
        agent.trace_states.clear()
        agent.trace_actions.clear()
        agent.active_engram = None
        
        while not terminated and not truncated:
            action = agent.step(state)
            next_state, _, terminated, truncated, _ = env.step(action)
            state = next_state
            steps += 1
            if steps > 500: truncated = True

        if (ep+1) % 5 == 0 or steps > 20:
            print(f"Ep {ep+1}: Survived {steps}. Engrams in Library: {len(agent.engrams)}")
            if len(agent.engrams) > 0:
                 top_knot = agent.engrams[0]
                 print(f"   Best Knot: Betti {top_knot.betti_score} (Used {top_knot.usage} times)")

    env.close()

if __name__ == "__main__":
    run_holonomic_simulation()