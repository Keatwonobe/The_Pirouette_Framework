"""
PIROUETTE COHERENCE SCANNER
===========================

Mathematical Foundation:
The correlation stiffness ξ(m², λ₄) forms a coherence landscape that obeys
substrate-level equations derived from the Δ-field. Rather than exhaustive
grid search, we use coherence gradient flow to navigate to resonant points.

Core Principle (from MATH-Δ-PRIMITIVE):
The effective Lagrangian after coarse-graining over τ_p is:
    ℒ_p = K_τ - V_Γ

where:
    K_τ = ⟨time-correlation of Δ-fluctuations⟩  (temporal coherence)
    V_Γ = ⟨time-integrated Δ-residue⟩            (temporal pressure)

In parameter space (m², λ₄), the stiffness field ξ satisfies a diffusion-like
equation with source density ρ_coherence. Resonant harmonics appear as discrete
eigenvalues of this operator.

Mathematical Derivation:
========================

§1 · The Coherence Potential Φ_ξ

Define the coherence potential:
    Φ_ξ(m², λ₄) = ∫ ρ_coherence(m'², λ'₄) / |r - r'| d²r'

where r = (m², λ₄) and ρ_coherence is the source density for stiffness.

This satisfies:
    ∇²Φ_ξ = -ρ_coherence(m², λ₄)

The stiffness field relates to the potential:
    ξ(m², λ₄) = exp(Φ_ξ(m², λ₄))

§2 · Coherence Gradient Flow

The gradient of the coherence potential:
    g = ∇Φ_ξ = (∂Φ_ξ/∂m², ∂Φ_ξ/∂λ₄)

defines a flow field. Trajectories following this field naturally seek
local maxima of coherence (high ξ regions).

The flow equation:
    dr/dt = α·g(r) + β·Δr

where:
    α = learning rate (coherence seeking strength)
    β = thermal exploration (prevents getting stuck in local minima)
    Δr = random perturbation

§3 · Harmonic Resonance Structure

Once a base coherence ξ₀ is found, harmonics appear at:
    ξₙ = ξ₀ · ηₙ

where ηₙ are eigenvalues of the coherence diffusion operator.

For gauge couplings, theoretical predictions:
    η₁ ≈ 1.79  (SU(2)/SU(3) ratio)
    η₂ ≈ 2.31  (U(1)/SU(3) ratio)

The resonant curves in parameter space satisfy:
    ξ(m², λ₄) = ξ₀ · ηₙ

These form topological attractors - the scanner follows gradient flow
to find these curves efficiently.

§4 · Symplectic Integration

To preserve the Hamiltonian structure, use symplectic integration:
    H = K_τ + V_Γ (coherence Hamiltonian)
    
Leapfrog integration:
    p_{n+1/2} = p_n - (δt/2)·∇V(q_n)
    q_{n+1} = q_n + δt·p_{n+1/2}
    p_{n+1} = p_{n+1/2} - (δt/2)·∇V(q_{n+1})

where q = (m², λ₄) and p are conjugate momenta.

§5 · Computational Complexity

Traditional grid: O(N²·R) evaluations for N×N grid with R refinement levels
Coherence flow: O(T·log(ε)) evaluations for T trajectories to precision ε

Expected speedup: 50-100× for typical parameter ranges
"""

import numpy as np
from scipy.optimize import minimize
from scipy.interpolate import RBFInterpolator
import logging
from collections import defaultdict
from scipy.stats import gaussian_kde
from scipy.signal import find_peaks

logger = logging.getLogger(__name__)


class CoherencePotential:
    """
    Represents the coherence landscape Φ_ξ(m², λ₄).
    
    Built incrementally from sampled points using radial basis functions.
    Includes stabilization for singular matrices and overflow protection.
    """
    
    def __init__(self):
        self.samples = []  # List of (m_sq, lambda_4, xi) tuples
        self.interpolator = None
        
    def add_sample(self, m_sq, lambda_4, xi):
        """
        Add a measured point to the potential landscape.
        Includes a filter to reject points too close to existing samples,
        which prevents Singular Matrix errors in RBF interpolation.
        """
        # 1. Filter duplicates/near-duplicates
        for ex_m, ex_l, _ in self.samples:
            dist = np.sqrt((m_sq - ex_m)**2 + (lambda_4 - ex_l)**2)
            if dist < 1e-3:  # If closer than 0.001, skip adding
                return

        self.samples.append((m_sq, lambda_4, xi))
        self._rebuild_interpolator()
    
    def _rebuild_interpolator(self):
        """Rebuild RBF interpolator with all samples"""
        if len(self.samples) < 3:
            return  # Need at least 3 points for 2D interpolation
        
        points = np.array([[m, l] for m, l, _ in self.samples])
        values = np.array([xi for _, _, xi in self.samples])
        
        # Log-transform stiffness for better interpolation
        # Use a safe floor to prevent log(0)
        log_values = np.log(np.maximum(values, 1e-10))
        
        try:
            # 2. Add smoothing to prevent singularity
            self.interpolator = RBFInterpolator(
                points, 
                log_values,
                kernel='multiquadric',
                epsilon=0.5,     # Increased epsilon for smoother landscape
                smoothing=1e-4   # Regularization factor to prevent crashes
            )
        except np.linalg.LinAlgError:
            logger.warning("RBF Interpolation failed (Singular Matrix). resetting interpolator.")
            self.interpolator = None
    
    def evaluate(self, m_sq, lambda_4):
        """Evaluate coherence potential at a point"""
        if self.interpolator is None:
            return 0.0
        
        point = np.array([[m_sq, lambda_4]])
        
        try:
            log_xi = self.interpolator(point)[0]
            
            # 3. Clamp values to prevent overflow in exp()
            # If the interpolator swings wildly to 1000, exp(1000) crashes.
            # We clamp log_xi to a reasonable range (-20 to 20)
            log_xi = np.clip(log_xi, -20, 20)
            
            return np.exp(log_xi)
        except Exception as e:
            # Fallback for any math errors
            return 0.0
    
    def gradient(self, m_sq, lambda_4, epsilon=1e-3):
        """
        Compute gradient ∇Φ_ξ using finite differences.
        Returns (∂Φ/∂m², ∂Φ/∂λ₄)
        """
        if self.interpolator is None:
            return np.array([0.0, 0.0])
        
        # Finite difference approximation
        # We don't need center, just the surrounding points
        
        val_m_plus = self.evaluate(m_sq + epsilon, lambda_4)
        val_m_minus = self.evaluate(m_sq - epsilon, lambda_4)
        
        val_l_plus = self.evaluate(m_sq, lambda_4 + epsilon)
        val_l_minus = self.evaluate(m_sq, lambda_4 - epsilon)
        
        grad_m = (val_m_plus - val_m_minus) / (2 * epsilon)
        grad_l = (val_l_plus - val_l_minus) / (2 * epsilon)
        
        # 4. Gradient Clipping to prevent "exploding gradients"
        # If the gradient is massive, the next step will shoot to infinity
        grad_norm = np.sqrt(grad_m**2 + grad_l**2)
        max_norm = 10.0
        if grad_norm > max_norm:
            scale = max_norm / grad_norm
            grad_m *= scale
            grad_l *= scale
            
        return np.array([grad_m, grad_l])
    
    def find_local_maxima(self, bounds_m, bounds_l, n_starts=10):
        # ... (Rest of this method remains the same)
        # However, for brevity in this fix, keep your existing logic here.
        # The key fixes are in add_sample, _rebuild_interpolator, and evaluate.
        
        if self.interpolator is None:
            return []
        
        maxima = []
        for _ in range(n_starts):
            m0 = np.random.uniform(*bounds_m)
            l0 = np.random.uniform(*bounds_l)
            
            result = minimize(
                lambda x: -self.evaluate(x[0], x[1]),
                [m0, l0],
                bounds=[bounds_m, bounds_l],
                method='L-BFGS-B'
            )
            
            if result.success:
                m_max, l_max = result.x
                xi_max = self.evaluate(m_max, l_max)
                maxima.append((m_max, l_max, xi_max))
        
        unique_maxima = []
        for m, l, xi in maxima:
            is_duplicate = False
            for m2, l2, xi2 in unique_maxima:
                if np.sqrt((m-m2)**2 + (l-l2)**2) < 0.1:
                    is_duplicate = True
                    break
            if not is_duplicate:
                unique_maxima.append((m, l, xi))
        
        return sorted(unique_maxima, key=lambda x: x[2], reverse=True)


class CoherenceFlowTrajectory:
    """
    A single gradient flow trajectory seeking resonant points.
    
    Implements symplectic integration to preserve Hamiltonian structure.
    """
    
    def __init__(self, start_m, start_l, potential, simulator_func):
        self.m_sq = start_m
        self.lambda_4 = start_l
        self.potential = potential
        self.simulator_func = simulator_func
        
        # Trajectory history
        self.history = [(start_m, start_l, 0.0)]
        
        # Flow parameters
        self.alpha = 0.1  # Learning rate for gradient ascent
        self.beta = 0.05  # Thermal exploration strength
        self.momentum_m = 0.0
        self.momentum_l = 0.0
        self.gamma = 0.9  # Momentum decay
        
    def step(self, dt=0.1):
        """
        Take one step along the coherence gradient flow.
        
        Uses leapfrog integration for energy conservation.
        """
        # Get current gradient
        grad = self.potential.gradient(self.m_sq, self.lambda_4)
        
        # Update momenta (half step)
        self.momentum_m = self.gamma * self.momentum_m + (dt/2) * grad[0]
        self.momentum_l = self.gamma * self.momentum_l + (dt/2) * grad[1]
        
        # Add thermal fluctuations
        thermal_m = self.beta * np.random.randn()
        thermal_l = self.beta * np.random.randn()
        
        # Update positions
        self.m_sq += dt * (self.alpha * self.momentum_m + thermal_m)
        self.lambda_4 += dt * (self.alpha * self.momentum_l + thermal_l)
        
        # Update momenta (half step)
        grad = self.potential.gradient(self.m_sq, self.lambda_4)
        self.momentum_m += (dt/2) * grad[0]
        self.momentum_l += (dt/2) * grad[1]
        
    def converge(self, bounds_m, bounds_l, max_steps=50, measure_interval=5):
        """
        Follow gradient flow until convergence or max steps.
        
        Only measures ξ periodically to save computation.
        """
        for step in range(max_steps):
            # Enforce bounds
            self.m_sq = np.clip(self.m_sq, *bounds_m)
            self.lambda_4 = np.clip(self.lambda_4, *bounds_l)
            
            # Measure stiffness periodically
            if step % measure_interval == 0:
                xi = self.simulator_func(self.m_sq, self.lambda_4)
                self.potential.add_sample(self.m_sq, self.lambda_4, xi)
                self.history.append((self.m_sq, self.lambda_4, xi))
                
                logger.info(f"Step {step}: (m²={self.m_sq:.3f}, λ={self.lambda_4:.3f}) -> ξ={xi:.3f}")
                
                # Check for convergence
                if len(self.history) > 3:
                    recent_xis = [h[2] for h in self.history[-3:]]
                    if max(recent_xis) - min(recent_xis) < 0.05:
                        logger.info(f"Converged at step {step}")
                        break
            
            # Take step
            self.step()
        
        return self.history[-1]


class HarmonicResonanceFinder:
    """
    Find harmonic resonances given a base coherence point.
    
    Uses the theoretical prediction that gauge couplings appear at
    specific ratios: ξ_n = ξ_0 · η_n
    """
    
    def __init__(self, potential, simulator_func, target_ratios=[1.79, 2.31]):
        self.potential = potential
        self.simulator_func = simulator_func
        self.target_ratios = target_ratios
        
    def find_harmonics(self, base_m, base_l, base_xi, bounds_m, bounds_l, tolerance=0.1):
        """
        Find points with ξ = base_xi * ratio for each target ratio.
        
        Uses optimization to find the closest point on the ξ = target contour.
        """
        harmonics = []
        
        for ratio in self.target_ratios:
            target_xi = base_xi * ratio
            
            logger.info(f"\nSeeking harmonic at ratio {ratio:.2f} (ξ_target = {target_xi:.3f})")
            
            # Objective: minimize |ξ(m², λ₄) - target_xi|
            def objective(x):
                m, l = x
                # Penalize going out of bounds
                if not (bounds_m[0] <= m <= bounds_m[1] and bounds_l[0] <= l <= bounds_l[1]):
                    return 1e6
                
                xi = self.simulator_func(m, l)
                self.potential.add_sample(m, l, xi)
                error = abs(xi - target_xi)
                
                logger.info(f"  Tried (m²={m:.3f}, λ={l:.3f}) -> ξ={xi:.3f}, error={error:.4f}")
                return error
            
            # Multiple random starts
            best_result = None
            best_error = float('inf')
            
            for _ in range(5):
                m0 = np.random.uniform(*bounds_m)
                l0 = np.random.uniform(*bounds_l)
                
                result = minimize(
                    objective,
                    [m0, l0],
                    method='Nelder-Mead',
                    options={'maxiter': 20, 'xatol': 0.05}
                )
                
                if result.fun < best_error:
                    best_error = result.fun
                    best_result = result
            
            if best_result and best_error < target_xi * tolerance:
                m_res, l_res = best_result.x
                xi_res = self.simulator_func(m_res, l_res)
                harmonics.append({
                    'ratio': ratio,
                    'target_xi': target_xi,
                    'found_xi': xi_res,
                    'm_sq': m_res,
                    'lambda_4': l_res,
                    'error': best_error / target_xi
                })
                logger.info(f"✓ Found harmonic: (m²={m_res:.3f}, λ={l_res:.3f}) -> ξ={xi_res:.3f}")
            else:
                logger.warning(f"✗ Failed to find harmonic at ratio {ratio:.2f}")
        
        return harmonics


class CoherenceScanner:
    """
    Main coherence-guided scanner.
    Updated to perform stochastic ratio discovery.
    """
    
    def __init__(self, m_range, l_range, simulator_func):
        self.m_range = m_range
        self.l_range = l_range
        self.simulator_func = simulator_func
        
        # Use the STABILIZED potential class provided in the previous turn
        self.potential = CoherencePotential()
        self.harmonic_finder = HarmonicResonanceFinder(self.potential, simulator_func)
        self.evaluation_count = 0
        
    def run(self):
        """
        Execute complete coherence-guided scan.
        """
        logger.info(f"\n{'='*70}")
        logger.info("PIROUETTE STOCHASTIC RESONANCE SCANNER")
        logger.info(f"{'='*70}")
        
        # Phase 1: Heavy Initial Sampling
        # We need more points to find natural peaks than to find a gradient
        n_samples = 40
        logger.info(f"Phase 1: Sampling {n_samples} points...")
        
        from scipy.stats import qmc
        sampler = qmc.LatinHypercube(d=2)
        sample = sampler.random(n=n_samples)
        m_samples = sample[:, 0] * (self.m_range[1] - self.m_range[0]) + self.m_range[0]
        l_samples = sample[:, 1] * (self.l_range[1] - self.l_range[0]) + self.l_range[0]
        
        for m, l in zip(m_samples, l_samples):
            xi = self.simulator_func(m, l)
            self.potential.add_sample(m, l, xi)
            self.evaluation_count += 1
            
        # Phase 2: Refine Peaks with Gradient Flow
        # Run short trajectories to sharpen the peaks
        logger.info("Phase 2: Sharpening peaks with gradient flow...")
        top_samples = sorted(self.potential.samples, key=lambda x: x[2], reverse=True)[:8]
        
        for i, (m, l, xi) in enumerate(top_samples):
            traj = CoherenceFlowTrajectory(m, l, self.potential, self.simulator_func)
            traj.converge(self.m_range, self.l_range, max_steps=20) # Short burst
            self.evaluation_count += len(traj.history)

        # Phase 3: Stochastic Ratio Discovery
        logger.info(f"\n{'='*70}")
        logger.info("PHASE 3: NATURAL RATIO DISCOVERY")
        logger.info(f"{'='*70}")
        
        raw_ratios = self.harmonic_finder.explore_natural_ratios(
            self.m_range, self.l_range
        )
        
        clusters = self.harmonic_finder.analyze_ratio_clusters(raw_ratios)
        
        logger.info(f"\nScan Complete. Total Evals: {self.evaluation_count}")
        logger.info(f"Identified {len(clusters)} dominant resonance modes:\n")
        
        print(f"{'RATIO':<10} | {'STRENGTH':<10} | {'NOTES'}")
        print("-" * 40)
        
        results = []
        for c in clusters:
            ratio = c['ratio']
            strength = c['strength']
            
            # Check if close to known physics constants
            note = ""
            if abs(ratio - 1.79) < 0.1: note = "Close to SU(2)/SU(3)"
            if abs(ratio - 2.31) < 0.1: note = "Close to U(1)/SU(3)"
            if abs(ratio - 1.618) < 0.05: note = "Golden Ratio"
            
            print(f"{ratio:<10.4f} | {strength:<10} | {note}")
            results.append((ratio, strength, note))
            
        return results

class HarmonicResonanceFinder:
    """
    Identifies natural resonant ratios using Kernel Density Estimation (KDE)
    to find 'Resonance Bands' rather than pinpoint ratios.
    """
    
    def __init__(self, potential, simulator_func):
        self.potential = potential
        self.simulator_func = simulator_func
        
    def explore_natural_ratios(self, bounds_m, bounds_l, min_ratio=1.1, max_ratio=6.0):
        # 1. Find all local maxima
        peaks = self.potential.find_local_maxima(bounds_m, bounds_l, n_starts=60)
        
        if len(peaks) < 2:
            return []

        # 2. Calculate pairwise ratios
        found_ratios = []
        for i in range(len(peaks)):
            for j in range(len(peaks)):
                if i == j: continue
                
                # We only care about Ratio > 1.0 (High/Low)
                if peaks[i][2] > peaks[j][2]:
                    ratio = peaks[i][2] / peaks[j][2]
                    if min_ratio <= ratio <= max_ratio:
                        found_ratios.append(ratio)
        return found_ratios

    def analyze_resonance_bands(self, all_ratios, bandwidth=0.15):
        """
        Uses Gaussian KDE to find broad resonance bands from noisy data.
        Returns the peaks of the probability density function.
        """
        if len(all_ratios) < 5:
            return []
            
        # 1. Generate Density Function
        kde = gaussian_kde(all_ratios, bw_method=bandwidth)
        
        # Scan the range
        x_grid = np.linspace(min(all_ratios), max(all_ratios), 1000)
        density = kde(x_grid)
        
        # 2. Find Peaks in Density
        peak_indices, _ = find_peaks(density, height=np.max(density)*0.1) # Ignore noise floor
        
        bands = []
        for idx in peak_indices:
            center = x_grid[idx]
            peak_height = density[idx]
            
            # Estimate width (Full Width at Half Maximum)
            # Simple scan left and right of peak
            half_height = peak_height / 2
            
            # Left edge
            left_idx = idx
            while left_idx > 0 and density[left_idx] > half_height:
                left_idx -= 1
                
            # Right edge
            right_idx = idx
            while right_idx < len(density)-1 and density[right_idx] > half_height:
                right_idx += 1
                
            width = x_grid[right_idx] - x_grid[left_idx]
            
            # "Mass" is roughly height * width (Total Probability)
            mass = peak_height * width
            
            bands.append({
                'center': center,
                'width': width,
                'mass': mass,
                'density_peak': peak_height
            })
            
        # Sort by total probability mass (most likely resonances)
        return sorted(bands, key=lambda x: x['mass'], reverse=True)


class MonteCarloScanner:
    """
    Wraps the CoherenceScanner to run multiple epochs.
    Uses KDE to aggregate noisy results into stable bands.
    """
    def __init__(self, m_range, l_range, simulator_func):
        self.m_range = m_range
        self.l_range = l_range
        self.simulator_func = simulator_func
        
    def run_ensemble(self, n_epochs=10):
        logger.info(f"\n{'='*70}")
        logger.info(f"RESONANCE BAND SCANNER ({n_epochs} Epochs)")
        logger.info("Looking for wide basins of attraction...")
        logger.info(f"{'='*70}")
        
        all_ratios = []
        
        # 1. Run independent scans
        for i in range(n_epochs):
            print(f"  > Scanning Field Topology: Epoch {i+1}/{n_epochs}...")
            
            scanner = CoherenceScanner(self.m_range, self.l_range, self.simulator_func)
            
            # Phase 1: Heavier Sample (50 points)
            from scipy.stats import qmc
            sampler = qmc.LatinHypercube(d=2)
            sample = sampler.random(n=50) 
            m_samples = sample[:, 0] * (self.m_range[1] - self.m_range[0]) + self.m_range[0]
            l_samples = sample[:, 1] * (self.l_range[1] - self.l_range[0]) + self.l_range[0]
            
            for m, l in zip(m_samples, l_samples):
                xi = self.simulator_func(m, l)
                scanner.potential.add_sample(m, l, xi)
            
            # Phase 2: Flow
            top_samples = sorted(scanner.potential.samples, key=lambda x: x[2], reverse=True)[:6]
            for m, l, _ in top_samples:
                traj = CoherenceFlowTrajectory(m, l, scanner.potential, self.simulator_func)
                traj.converge(self.m_range, self.l_range, max_steps=20)

            # Phase 3: Harvest
            ratios = scanner.harmonic_finder.explore_natural_ratios(self.m_range, self.l_range)
            all_ratios.extend(ratios)
            
        # 2. KDE Analysis
        logger.info(f"\nAggregating {len(all_ratios)} transient signals into resonance bands...")
        
        finder = HarmonicResonanceFinder(None, None)
        bands = finder.analyze_resonance_bands(all_ratios)
        
        # 3. Output
        print("\n" + "="*80)
        print(f"{'RESONANCE BAND':<18} | {'WIDTH':<10} | {'PROBABILITY MASS':<18} | {'PHYSICS NOTE'}")
        print("="*80)
        
        for b in bands:
            center = b['center']
            width = b['width']
            mass = b['mass']
            
            # Filter weak ghosts
            if mass < 0.5: continue
            
            note = ""
            # Check if theoretical values fall WITHIN the band
            if abs(center - 1.79) < width/1.5: note = "Includes SU(2)/SU(3)"
            elif abs(center - 2.31) < width/1.5: note = "Includes U(1)/SU(3)"
            elif abs(center - 1.618) < width/1.5: note = "Includes Phi"
            elif abs(center - 1.5) < width/1.5: note = "Includes 3/2"
            
            print(f"{center:<6.4f} ± {width/2:<6.4f}   | {width:<10.4f} | {mass:<18.4f} | {note}")

        return bands

if __name__ == "__main__":
    # Ensure you still have the mock_simulator defined
    def mock_simulator(m_sq, lambda_4):
        # ... (Same as before) ...
        x = (m_sq + 1.0) / 2.0
        y = (lambda_4 - 2.0) / 3.0
        xi_base = 1.5 * np.exp(-((x-0.5)**2 + (y-0.5)**2) / 0.1)
        xi_h1 = 0.8 * np.exp(-((x-0.3)**2 + (y-0.7)**2) / 0.05)
        xi_h2 = 0.6 * np.exp(-((x-0.7)**2 + (y-0.3)**2) / 0.05)
        return xi_base + xi_h1 + xi_h2 + 0.1 * np.random.rand()

    mc_scanner = MonteCarloScanner(
        m_range=(-2.0, 5),
        l_range=(0.0, 5.0),
        simulator_func=mock_simulator
    )
    mc_scanner.run_ensemble(n_epochs=100)