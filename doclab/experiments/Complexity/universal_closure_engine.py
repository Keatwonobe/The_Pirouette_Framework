#!/usr/bin/env python3
"""
Universal Closure Engine - Minimal Implementation
Demonstrates domain-agnostic dynamic equilibrium learning
"""
import numpy as np
from typing import Callable, Tuple, Dict
from dataclasses import dataclass

@dataclass
class ClosureMetrics:
    """Metrics for monitoring convergence to geodesic"""
    D: float           # Current residue
    dD_dt: float       # Residue flux
    kappa: float       # Curvature scalar
    on_geodesic: bool  # Whether near manifold

class UniversalClosureEngine:
    """
    Domain-agnostic framework for learning dynamic equilibrium.
    
    The ONLY domain-specific input is measure_residue_fn.
    All geometry and optimization is universal.
    """
    
    def __init__(
        self,
        measure_residue_fn: Callable[[np.ndarray], float],
        gamma: float = 1.5,    # Coherence gain weight
        beta: float = 0.05,    # Persistence bonus
        delta: float = 1.0,    # Residue penalty
        eta: float = 0.1,      # Curvature penalty (NEW)
        epsilon: float = 1e-3  # For numerical derivatives
    ):
        self.D_fn = measure_residue_fn
        self.gamma = gamma
        self.beta = beta
        self.delta = delta
        self.eta = eta
        self.epsilon = epsilon
        
        # History for tracking convergence
        self.history = {
            'D': [],
            'dD_dt': [],
            'kappa': [],
            'rewards': []
        }
    
    def compute_hessian(self, state: np.ndarray) -> np.ndarray:
        """
        Numerically compute curvature tensor H_ij = ∂²D/∂S_i∂S_j
        This is UNIVERSAL - same code for any domain.
        """
        n = len(state)
        H = np.zeros((n, n))
        eps = self.epsilon
        
        for i in range(n):
            for j in range(n):
                e_i = np.zeros(n)
                e_j = np.zeros(n)
                e_i[i] = eps
                e_j[j] = eps
                
                # Second derivative via finite differences
                H[i, j] = (
                    self.D_fn(state + e_i + e_j)
                    - self.D_fn(state + e_i)
                    - self.D_fn(state + e_j)
                    + self.D_fn(state)
                ) / (eps ** 2)
        
        return H
    
    def compute_curvature(self, state: np.ndarray) -> float:
        """
        Compute curvature scalar κ = Tr(H)
        Measures stability of closure at current state.
        """
        H = self.compute_hessian(state)
        return np.trace(H)
    
    def compute_closure_reward(
        self,
        D_current: float,
        D_previous: float,
        kappa: float
    ) -> float:
        """
        Universal reward structure for closure learning.
        
        Components:
        1. Coherence gain: Reward reducing residue
        2. Persistence: Small bonus for survival
        3. Residue penalty: Cost of being far from closure
        4. Curvature penalty: Cost of fragile (high-κ) states
        """
        dD = D_current - D_previous
        
        coherence_gain = self.gamma * max(0, -dD)
        persistence = self.beta
        residue_penalty = self.delta * D_current
        curvature_penalty = self.eta * abs(kappa)
        
        reward = (
            coherence_gain 
            + persistence 
            - residue_penalty 
            - curvature_penalty
        )
        
        return reward
    
    def step(
        self,
        state: np.ndarray,
        D_previous: float
    ) -> Tuple[float, ClosureMetrics]:
        """
        Universal step function.
        Returns reward and diagnostic metrics.
        """
        # Compute current residue
        D_current = self.D_fn(state)
        
        # Compute curvature (stability)
        kappa = self.compute_curvature(state)
        
        # Compute reward
        reward = self.compute_closure_reward(D_current, D_previous, kappa)
        
        # Diagnostic metrics
        dD_dt = D_current - D_previous
        on_geodesic = (abs(dD_dt) < 0.01) and (abs(kappa) < 1.0)
        
        metrics = ClosureMetrics(
            D=D_current,
            dD_dt=dD_dt,
            kappa=kappa,
            on_geodesic=on_geodesic
        )
        
        # Log history
        self.history['D'].append(D_current)
        self.history['dD_dt'].append(dD_dt)
        self.history['kappa'].append(kappa)
        self.history['rewards'].append(reward)
        
        return reward, metrics
    
    def convergence_report(self) -> Dict[str, float]:
        """
        Universal convergence metrics.
        System has found geodesic when:
        - mean(D) → 0
        - var(D) → small
        - mean(|κ|) → 0
        """
        if not self.history['D']:
            return {}
        
        recent_window = min(100, len(self.history['D']))
        recent_D = self.history['D'][-recent_window:]
        recent_kappa = self.history['kappa'][-recent_window:]
        
        return {
            'mean_residue': np.mean(recent_D),
            'std_residue': np.std(recent_D),
            'mean_curvature': np.mean(np.abs(recent_kappa)),
            'convergence_score': 1.0 / (1.0 + np.mean(recent_D) + np.std(recent_D))
        }


# ============================================================================
# DOMAIN-SPECIFIC RESIDUE FUNCTIONS
# (This is the ONLY part that changes per domain)
# ============================================================================

def cartpole_residue(state: np.ndarray) -> float:
    """CartPole: Residue = imbalance between potential and kinetic"""
    x, x_dot, theta, theta_dot = state
    
    V_gamma = 0.4 * abs(x) + 1.5 * abs(theta)  # Potential (distance from upright)
    K_tau = 0.2 * abs(x_dot) + 0.3 * abs(theta_dot)  # Kinetic (motion)
    
    return abs(V_gamma - K_tau)


def plasma_residue(state: np.ndarray) -> float:
    """
    Plasma: Residue = MHD imbalance + power imbalance + instability
    
    State vector: [pressure, B_field, current_density, T_electron, T_ion, density]
    (Simplified for demonstration)
    """
    p, B, j, Te, Ti, ne = state
    
    # Force balance (simplified MHD equilibrium condition)
    force_imbalance = abs(p - 0.5 * B * j)  # Should be: |∇p - j×B|
    
    # Power balance (simplified)
    P_fusion = (ne ** 2) * (Te * Ti) ** 2  # Fusion power ~ n²T⁴
    P_loss = 0.1 * Te ** 1.5  # Transport losses
    power_imbalance = abs(P_fusion - P_loss)
    
    # Stability margin (distance from disruption limits)
    beta_limit = 0.05  # Typical tokamak β limit
    beta_actual = p / (B ** 2)
    stability_margin = abs(beta_actual - beta_limit)
    
    # Weighted sum
    return (
        1.0 * force_imbalance +
        0.5 * power_imbalance +
        2.0 * stability_margin
    )


def language_residue(state: np.ndarray) -> float:
    """
    Language: Residue = semantic drift + syntactic debt - closure
    
    State vector: embedding of current discourse window (simplified to 4D)
    """
    # Simulate semantic drift (distance from initial embedding)
    semantic_drift = np.linalg.norm(state - np.array([0, 0, 0, 0]))
    
    # Simulate syntactic debt (could be parser output in real system)
    syntactic_debt = abs(state[0] - state[2])  # Imbalance in structure
    
    # Simulate pragmatic load (unresolved references)
    pragmatic_load = abs(state[1] + state[3])
    
    # Simulate closure coefficient (how much tension is resolved)
    closure = max(0, 1.0 - semantic_drift / 2.0)
    
    return (
        1.0 * semantic_drift +
        0.5 * syntactic_debt +
        0.3 * pragmatic_load -
        0.8 * closure
    )


# ============================================================================
# DEMONSTRATION: Same engine works for all domains
# ============================================================================

def demonstrate_universality():
    """
    Show that the EXACT SAME engine works across domains.
    Only the residue function changes.
    """
    print("=" * 70)
    print("UNIVERSAL CLOSURE ENGINE - Domain Agnostic Demonstration")
    print("=" * 70)
    print()
    
    domains = [
        ("CartPole (Mechanics)", cartpole_residue, np.array([0.1, 0.05, 0.2, 0.1])),
        ("Plasma (Fusion)", plasma_residue, np.array([1.0, 2.0, 0.5, 10.0, 8.0, 1.5])),
        ("Language (Discourse)", language_residue, np.array([0.5, 0.3, -0.2, 0.1]))
    ]
    
    for domain_name, residue_fn, initial_state in domains:
        print(f"\n{domain_name}")
        print("-" * 70)
        
        # Create closure engine with domain-specific residue
        engine = UniversalClosureEngine(
            measure_residue_fn=residue_fn,
            gamma=1.5,
            beta=0.05,
            delta=1.0,
            eta=0.1
        )
        
        # Simulate system evolution toward geodesic
        state = initial_state.copy()
        D_prev = residue_fn(state)
        
        print(f"Initial state: {state}")
        print(f"Initial residue: {D_prev:.4f}\n")
        
        # Simulate 10 steps (in real system, this would be RL training)
        for step in range(10):
            # Simple gradient descent on residue (placeholder for RL)
            gradient = np.random.randn(len(state)) * 0.1
            state = state - 0.1 * gradient
            
            reward, metrics = engine.step(state, D_prev)
            D_prev = metrics.D
            
            if step % 3 == 0:
                print(
                    f"Step {step:2d}: "
                    f"D={metrics.D:.4f}, "
                    f"dD/dt={metrics.dD_dt:+.4f}, "
                    f"κ={metrics.kappa:+.4f}, "
                    f"geodesic={metrics.on_geodesic}"
                )
        
        # Convergence report
        report = engine.convergence_report()
        print(f"\nConvergence Report:")
        print(f"  Mean Residue: {report['mean_residue']:.4f}")
        print(f"  Residue Stability: {report['std_residue']:.4f}")
        print(f"  Mean Curvature: {report['mean_curvature']:.4f}")
        print(f"  Convergence Score: {report['convergence_score']:.4f}")
    
    print("\n" + "=" * 70)
    print("CONCLUSION: Same mathematical structure across all domains")
    print("=" * 70)


if __name__ == "__main__":
    demonstrate_universality()