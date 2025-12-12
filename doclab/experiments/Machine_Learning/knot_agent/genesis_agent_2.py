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

        # New: simple fitness stats
        self.total_return = 0.0
        self.total_steps = 0
        self.trials = 0

    def resonates(self, current_state):
        diff = current_state - self.start_state
        weighted_dist = np.sqrt(np.dot(diff**2, STATE_WEIGHTS))
        return weighted_dist < COHERENCE_THRESHOLD

    @property
    def avg_steps(self):
        return self.total_steps / self.trials if self.trials > 0 else 0.0

    @property
    def avg_return(self):
        return self.total_return / self.trials if self.trials > 0 else 0.0

    def update_fitness(self, episode_return, episode_steps):
        self.total_return += episode_return
        self.total_steps += episode_steps
        self.trials += 1


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
        self.current_episode_engrams = set()

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
            resonant = []
            for engram in self.memory.engrams:
                if engram.resonates(state):
                    resonant.append(engram)

            if resonant:
                # Softmax over avg_steps to favor better loops
                beta = 0.1  # temperature: higher = more greedy
                scores = np.array([e.avg_steps for e in resonant], dtype=np.float32)
                if np.all(scores == 0):
                    # No information yet, pick uniformly
                    chosen = random.choice(resonant)
                else:
                    probs = np.exp(beta * (scores - scores.max()))
                    probs = probs / probs.sum()
                    chosen = np.random.choice(resonant, p=probs)

                self.active_engram = chosen
                self.engram_step = 0
                engram.usage_count += 1
                self.total_knots_used += 1
                self.current_episode_engrams.add(engram.id)
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

    def handle_death(self, episode_return, episode_steps):
        # Update fitness for all engrams used this episode
        for eid in self.current_episode_engrams:
            for e in self.memory.engrams:
                if e.id == eid:
                    e.update_fitness(episode_return, episode_steps)
                    break

        self.current_episode_engrams.clear()
        self.active_engram = None
        self.memory.cancel_candidate()
        self.memory.stm_trace.clear()

def pretrain_static_engrams(env, agent, num_candidates=200, seq_len=40, top_k=20):
    """
    Static generator: build open-loop action sequences, test them,
    and keep the best ones as initial engrams.
    """
    print(f"--- Static pretraining: {num_candidates} candidates, seq_len={seq_len}, top_k={top_k} ---")

    action_dim = env.action_space.shape[0]
    candidates = []

    for i in range(num_candidates):
        # Random smooth-ish sequence: Brownian walk in action space
        seq = np.zeros((seq_len, action_dim), dtype=np.float32)
        a = np.zeros(action_dim, dtype=np.float32)
        for t in range(seq_len):
            a = a + np.random.normal(0.0, 0.5, size=action_dim)
            a = np.clip(a, -3.0, 3.0)
            seq[t] = a

        # Evaluate this sequence
        state, _ = env.reset()
        start_state = state.copy()
        steps = 0
        terminated = False
        truncated = False

        while not terminated and not truncated and steps < seq_len:
            action = seq[steps]
            state, reward, terminated, truncated, _ = env.step(action)
            steps += 1

        candidates.append((steps, start_state, seq))

    # Sort by survival steps, descending
    candidates.sort(key=lambda x: x[0], reverse=True)
    elites = candidates[:top_k]

    # Turn elites into engrams
    for steps, start_state, seq in elites:
        new_engram = Engram(start_state=start_state, actions=list(seq), ID=agent.memory.engram_counter)
        # Give them initial fitness based on their test
        new_engram.update_fitness(episode_return=float(steps), episode_steps=steps)
        agent.memory.engrams.append(new_engram)
        agent.memory.engram_counter += 1

    print(f"  [Pretrain] Created {len(elites)} static engrams.")
    for e in agent.memory.engrams:
        print(f"    Engram {e.id}: avg_steps={e.avg_steps:.1f}, len={len(e.actions)}")


# --- RUNNER ---
def run_simulation():
    env = gym.make("InvertedPendulum-v5") # Try v5 if v4 warned
    agent = GenesisAgent(env.action_space)
    
    print("--- GENESIS v1.2 (WEIGHTED MANIFOLD + FITNESS + PRETRAIN) ---")
    
    pretrain_static_engrams(env, agent, num_candidates=300, seq_len=50, top_k=30)

    # Increase episodes to allow for 'Genesis' event
    episodes = 5000 
    
    for ep in range(episodes):
        state, _ = env.reset()
        terminated = False
        truncated = False
        steps = 0
        ep_return = 0.0
        
        while not terminated and not truncated:
            action = agent.step(state)
            next_state, reward, terminated, truncated, _ = env.step(action)
            
            ep_return += reward
            state = next_state
            steps += 1
            
            # Hard stop if it solves it (to prevent infinite loops in demo)
            if steps > 500: truncated = True 

        # Death Handler
        agent.handle_death(ep_return, steps)

        if (ep+1) % 500 == 0:
            print(f"Ep {ep+1}: Max Steps {steps}. Knots: {len(agent.memory.engrams)}")
            if len(agent.memory.engrams) > 0:
                last = agent.memory.engrams[-1]
                print(f"    Last engram {last.id}: trials={last.trials}, avg_steps={last.avg_steps:.1f}")

    env.close()

if __name__ == "__main__":
    run_simulation()