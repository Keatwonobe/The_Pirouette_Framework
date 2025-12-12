import gymnasium as gym
import numpy as np
import random

# --- CONFIGURATION v1.1 ---
# State: [x, x_dot, theta, theta_dot]
# We want to ignore 'x' (pos 0) and focus heavily on 'theta' (pos 2)
STATE_WEIGHTS = np.array([0.0, 0.5, 5.0, 1.0]) 

COHERENCE_THRESHOLD = 0.15  # Slightly looser to allow for "fuzzy" loops
MIN_KNOT_LENGTH = 8         # Increased: Don't memorize tiny twitches
STABILITY_TEST_PERIOD = 10  # Must survive this long AFTER the knot to save it
STM_SIZE = 500

class Engram:
    def __init__(self, start_state, actions, ID):
        self.id = ID
        self.start_state = start_state
        self.actions = actions
        self.usage_count = 0

    def resonates(self, current_state):
        # Weighted distance check
        diff = current_state - self.start_state
        weighted_dist = np.sqrt(np.dot(diff**2, STATE_WEIGHTS))
        return weighted_dist < COHERENCE_THRESHOLD

class TopologicalMemory:
    def __init__(self):
        self.engrams = []
        self.stm_trace = [] 
        self.engram_counter = 0
        # A buffer to hold potential knots while we test if they lead to death
        self.candidate_knot = None 
        self.stability_timer = 0

    def add_trace(self, state, action):
        self.stm_trace.append((state, action))
        if len(self.stm_trace) > STM_SIZE:
            self.stm_trace.pop(0)

    def check_candidate_stability(self):
        """
        If we found a knot recently, we wait to see if the agent survives.
        If it survives STABILITY_TEST_PERIOD steps, we crystallize the knot.
        """
        if self.candidate_knot:
            self.stability_timer -= 1
            if self.stability_timer <= 0:
                # IT SURVIVED! Crystallize it.
                start, acts = self.candidate_knot
                self.crystallize(start, acts)
                self.candidate_knot = None

    def cancel_candidate(self):
        """Agent died. The knot was a lie."""
        self.candidate_knot = None

    def detect_closed_loop(self, current_state):
        # If we are already testing a candidate, don't look for new ones
        if self.candidate_knot: 
            return

        # Scan backwards
        # We look for a previous state that matches current state
        for i in range(len(self.stm_trace) - MIN_KNOT_LENGTH, -1, -1):
            past_state, _ = self.stm_trace[i]
            
            # Weighted Distance
            diff = current_state - past_state
            weighted_dist = np.sqrt(np.dot(diff**2, STATE_WEIGHTS))
            
            if weighted_dist < COHERENCE_THRESHOLD:
                # FOUND A LOOP. 
                # Don't save yet. Put it in "Probation".
                raw_loop = self.stm_trace[i:]
                actions = [step[1] for step in raw_loop]
                
                self.candidate_knot = (past_state, actions)
                self.stability_timer = STABILITY_TEST_PERIOD
                return # Stop scanning

    def crystallize(self, start_state, actions):
        # Deduplicate
        for engram in self.engrams:
            if engram.resonates(start_state):
                return 
        
        new_engram = Engram(start_state, actions, self.engram_counter)
        self.engrams.append(new_engram)
        self.engram_counter += 1
        print(f"  [!] STABLE KNOT FORMED: ID {new_engram.id} | Len: {len(actions)}")

class GenesisAgent:
    def __init__(self, action_space):
        self.action_space = action_space
        self.memory = TopologicalMemory()
        self.active_engram = None
        self.engram_step = 0
        self.total_knots_used = 0

    def step(self, state):
        # 0. Verify Stability of pending knots
        self.memory.check_candidate_stability()

        # 1. PLAYING A KNOT
        if self.active_engram:
            if self.engram_step < len(self.active_engram.actions):
                action = self.active_engram.actions[self.engram_step]
                self.engram_step += 1
                self.memory.add_trace(state, action)
                return action
            else:
                self.active_engram = None
                self.engram_step = 0

        # 2. RESONANCE CHECK
        # Only check for resonance if we aren't currently testing a candidate
        # (Or maybe we should? Let's stick to exploring for now)
        if not self.memory.candidate_knot: 
            for engram in self.memory.engrams:
                if engram.resonates(state):
                    self.active_engram = engram
                    self.engram_step = 0
                    engram.usage_count += 1
                    self.total_knots_used += 1
                    return self.step(state) 

        # 3. BROWNIAN MOTION (with Momentum)
        # Pure random noise is too jerky. Let's bias towards the previous action slightly
        # to create "smooth" curves, increasing chance of finding loops.
        if len(self.memory.stm_trace) > 0:
            last_action = self.memory.stm_trace[-1][1]
            noise = np.random.normal(0, 0.2, size=last_action.shape)
            action = np.clip(last_action + noise, -3, 3) # Small deviations
        else:
            action = self.action_space.sample()

        # 4. RECORD & DETECT
        self.memory.add_trace(state, action)
        self.memory.detect_closed_loop(state)

        return action

    def handle_death(self):
        self.active_engram = None
        self.memory.cancel_candidate() # Validated: Death kills the hypothesis
        self.memory.stm_trace.clear()

# --- RUNNER ---
def run_simulation():
    env = gym.make("InvertedPendulum-v5") # Try v5 if v4 warned
    agent = GenesisAgent(env.action_space)
    
    print("--- GENESIS v1.1 (WEIGHTED MANIFOLD) ---")
    
    # Increase episodes to allow for 'Genesis' event
    episodes = 5000 
    
    for ep in range(episodes):
        state, _ = env.reset()
        terminated = False
        truncated = False
        steps = 0
        
        while not terminated and not truncated:
            action = agent.step(state)
            next_state, reward, terminated, truncated, _ = env.step(action)
            
            state = next_state
            steps += 1
            
            # Hard stop if it solves it (to prevent infinite loops in demo)
            if steps > 500: truncated = True 

        # Death Handler
        agent.handle_death()

        if (ep+1) % 500 == 0:
            print(f"Ep {ep+1}: Max Steps {steps}. Knots: {len(agent.memory.engrams)}")
            if len(agent.memory.engrams) > 0:
                print(f"    Last knot used {agent.memory.engrams[-1].usage_count} times")

    env.close()

if __name__ == "__main__":
    run_simulation()