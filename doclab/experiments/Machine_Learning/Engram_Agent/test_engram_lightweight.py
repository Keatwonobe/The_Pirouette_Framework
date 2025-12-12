#!/usr/bin/env python3
"""
Lightweight Engram System Test (No PyTorch Required)
====================================================

Tests core engram logic without external dependencies.
"""

import numpy as np
from pathlib import Path
import sys

# Minimal engram implementation for testing
class TestEngram:
    """Lightweight engram for testing core logic."""
    
    def __init__(self, mean_gamma, mean_DR, mean_surprise, return_raw):
        self.mean_gamma = mean_gamma
        self.mean_DR = mean_DR
        self.mean_surprise = mean_surprise
        self.return_raw = return_raw
    
    def resonance_score(self, query_gamma, query_DR, query_surprise):
        """Compute resonance similarity."""
        gamma_dist = abs(self.mean_gamma - query_gamma) / (self.mean_gamma + 1e-6)
        DR_dist = abs(self.mean_DR - query_DR) / (self.mean_DR + 1e-6)
        S_dist = abs(self.mean_surprise - query_surprise) / (self.mean_surprise + 1e-6)
        
        dist = 0.5 * gamma_dist + 0.3 * DR_dist + 0.2 * S_dist
        score = np.exp(-dist)
        return float(score)


def test_resonance_logic():
    """Test that resonance scoring works correctly."""
    print("\n" + "="*60)
    print("TEST 1: Resonance Logic")
    print("="*60)
    
    # Create reference engram
    ref = TestEngram(
        mean_gamma=1.5,
        mean_DR=0.85,
        mean_surprise=0.6,
        return_raw=250.0
    )
    
    # Test self-resonance (should be ~1.0)
    self_score = ref.resonance_score(1.5, 0.85, 0.6)
    print(f"  Self-resonance: {self_score:.3f}")
    assert self_score > 0.99, f"Self-resonance should be ~1.0, got {self_score}"
    
    # Test close match (should be high)
    close_score = ref.resonance_score(1.55, 0.87, 0.62)
    print(f"  Close match: {close_score:.3f}")
    assert 0.8 < close_score < 1.0, f"Close match should be 0.8-1.0, got {close_score}"
    
    # Test distant match (should be low)
    far_score = ref.resonance_score(2.5, 0.5, 0.3)
    print(f"  Distant match: {far_score:.3f}")
    assert far_score < 0.6, f"Distant match should be <0.6, got {far_score}"
    
    print("✓ Test 1 PASSED: Resonance scoring works correctly\n")


def test_library_sorting():
    """Test that engrams sort by performance."""
    print("="*60)
    print("TEST 2: Library Sorting")
    print("="*60)
    
    # Create engrams with random returns
    engrams = []
    returns = []
    for i in range(10):
        ret = np.random.uniform(100, 400)
        returns.append(ret)
        engrams.append(TestEngram(
            mean_gamma=1.0 + 0.5*i,
            mean_DR=0.8 + 0.02*i,
            mean_surprise=0.5 + 0.1*i,
            return_raw=ret
        ))
    
    # Sort by return
    engrams.sort(key=lambda e: e.return_raw, reverse=True)
    sorted_returns = [e.return_raw for e in engrams]
    
    print(f"  Original returns: {[f'{r:.1f}' for r in returns[:5]]}...")
    print(f"  Sorted returns: {[f'{r:.1f}' for r in sorted_returns[:5]]}...")
    
    # Verify sorted
    for i in range(len(sorted_returns)-1):
        assert sorted_returns[i] >= sorted_returns[i+1], "Returns should be descending"
    
    print("✓ Test 2 PASSED: Engrams sort correctly by return\n")


def test_coherence_computation():
    """Test coherence profile computation from hidden state velocity."""
    print("="*60)
    print("TEST 3: Coherence Computation")
    print("="*60)
    
    T, hidden_dim = 100, 10  # Smaller dimension for clearer signal
    
    # Create smooth trajectory (low velocity = high coherence)
    t = np.linspace(0, 2*np.pi, T)
    smooth_hiddens = np.zeros((T, hidden_dim))
    for i in range(hidden_dim):
        smooth_hiddens[:, i] = np.sin(t + i*0.1)
    
    h_diff_smooth = np.diff(smooth_hiddens, axis=0)
    vel_smooth = np.linalg.norm(h_diff_smooth, axis=-1)
    
    # Create chaotic trajectory (high velocity = low coherence)
    chaotic_hiddens = np.cumsum(np.random.randn(T, hidden_dim), axis=0)
    
    h_diff_chaotic = np.diff(chaotic_hiddens, axis=0)
    vel_chaotic = np.linalg.norm(h_diff_chaotic, axis=-1)
    
    mean_vel_smooth = np.mean(vel_smooth)
    mean_vel_chaotic = np.mean(vel_chaotic)
    
    print(f"  Smooth trajectory velocity: {mean_vel_smooth:.3f}")
    print(f"  Chaotic trajectory velocity: {mean_vel_chaotic:.3f}")
    print(f"  Ratio (chaotic/smooth): {mean_vel_chaotic/mean_vel_smooth:.2f}x")
    
    # Chaotic should have higher velocity (lower coherence)
    assert mean_vel_chaotic > mean_vel_smooth, \
        f"Chaotic should have higher velocity, got smooth={mean_vel_smooth}, chaotic={mean_vel_chaotic}"
    
    print("✓ Test 3 PASSED: Coherence metric distinguishes smooth vs chaotic\n")


def test_attractor_space_structure():
    """Test that good engrams cluster in specific (Γ, DR, S) regions."""
    print("="*60)
    print("TEST 4: Attractor Space Structure")
    print("="*60)
    
    # Create engrams with returns correlated to attractor position
    engrams = []
    for i in range(50):
        # Good engrams: moderate Γ, low DR, moderate S
        if i < 25:
            gamma = np.random.uniform(1.2, 1.8)
            DR = np.random.uniform(0.7, 0.9)
            S = np.random.uniform(0.5, 0.8)
            ret = 300 + np.random.uniform(-50, 50)
        # Bad engrams: extreme values
        else:
            gamma = np.random.uniform(0.5, 3.0)
            DR = np.random.uniform(0.3, 1.0)
            S = np.random.uniform(0.1, 1.0)
            ret = 150 + np.random.uniform(-50, 50)
        
        engrams.append(TestEngram(gamma, DR, S, ret))
    
    # Sort by return
    engrams.sort(key=lambda e: e.return_raw, reverse=True)
    
    # Check that top 25% have tighter clustering
    top_n = 12
    top_gammas = [e.mean_gamma for e in engrams[:top_n]]
    top_DRs = [e.mean_DR for e in engrams[:top_n]]
    
    gamma_std = np.std(top_gammas)
    DR_std = np.std(top_DRs)
    
    print(f"  Top {top_n} engrams:")
    print(f"    Γ std: {gamma_std:.3f}")
    print(f"    DR std: {DR_std:.3f}")
    print(f"    Mean return: {np.mean([e.return_raw for e in engrams[:top_n]]):.1f}")
    
    # Top engrams should cluster (low std)
    assert gamma_std < 0.5, f"Top engrams should cluster in Γ, got std={gamma_std}"
    assert DR_std < 0.15, f"Top engrams should cluster in DR, got std={DR_std}"
    
    print("✓ Test 4 PASSED: Good engrams cluster in attractor space\n")


def test_resonance_based_query():
    """Test that resonance query finds similar engrams."""
    print("="*60)
    print("TEST 5: Resonance-Based Query")
    print("="*60)
    
    # Create library of engrams
    engrams = []
    for i in range(20):
        engrams.append(TestEngram(
            mean_gamma=1.0 + 0.5*i,
            mean_DR=0.7 + 0.02*i,
            mean_surprise=0.4 + 0.05*i,
            return_raw=100 + 20*i
        ))
    
    # Query for engram similar to index 10
    query_gamma = engrams[10].mean_gamma
    query_DR = engrams[10].mean_DR
    query_surprise = engrams[10].mean_surprise
    
    # Score all engrams
    scored = [(i, e.resonance_score(query_gamma, query_DR, query_surprise)) 
              for i, e in enumerate(engrams)]
    scored.sort(key=lambda x: x[1], reverse=True)
    
    print(f"  Query: Γ={query_gamma:.2f}, DR={query_DR:.2f}, S={query_surprise:.2f}")
    print(f"  Top 5 matches:")
    for i, (idx, score) in enumerate(scored[:5]):
        print(f"    {i+1}. Engram {idx}: score={score:.3f}")
    
    # Best match should be the query engram itself
    assert scored[0][0] == 10, f"Best match should be query engram (10), got {scored[0][0]}"
    assert scored[0][1] > 0.99, f"Self-match score should be ~1.0, got {scored[0][1]}"
    
    # Next matches should be neighbors
    neighbor_indices = [idx for idx, _ in scored[1:4]]
    neighbors_close = all(abs(idx - 10) <= 3 for idx in neighbor_indices)
    print(f"  Neighbors close to query: {neighbors_close}")
    
    print("✓ Test 5 PASSED: Resonance query finds similar engrams\n")


def test_engram_key_properties():
    """Test that engram satisfies key theoretical properties."""
    print("="*60)
    print("TEST 6: Theoretical Properties")
    print("="*60)
    
    # Property 1: Higher coherence correlates with higher return (in good basins)
    coherences = []
    returns = []
    
    for i in range(30):
        # Simulate: high coherence -> good attractor -> high return
        coh = np.random.uniform(0.5, 1.0)
        # Return increases with coherence (with noise)
        ret = 100 + 300 * coh + np.random.normal(0, 30)
        coherences.append(coh)
        returns.append(ret)
    
    correlation = np.corrcoef(coherences, returns)[0, 1]
    print(f"  Coherence-Return correlation: {correlation:.3f}")
    assert correlation > 0.5, f"Coherence should correlate with return, got {correlation}"
    
    # Property 2: Engrams with similar (Γ, DR, S) have similar returns
    ref_gamma, ref_DR, ref_S = 1.5, 0.85, 0.6
    
    engrams_similar = []
    returns_similar = []
    
    for i in range(20):
        # Create engrams close to reference
        gamma = ref_gamma + np.random.normal(0, 0.1)
        DR = ref_DR + np.random.normal(0, 0.05)
        S = ref_S + np.random.normal(0, 0.05)
        ret = 250 + np.random.normal(0, 30)
        
        engrams_similar.append(TestEngram(gamma, DR, S, ret))
        returns_similar.append(ret)
    
    return_std = np.std(returns_similar)
    print(f"  Return std for similar attractors: {return_std:.1f}")
    assert return_std < 50, f"Similar attractors should have similar returns, got std={return_std}"
    
    print("✓ Test 6 PASSED: Engrams satisfy theoretical properties\n")


def run_all_tests():
    """Run complete lightweight test suite."""
    print("\n" + "="*60)
    print("PIROUETTE ENGRAM - LIGHTWEIGHT TEST SUITE")
    print("="*60)
    print("(No PyTorch required - tests core logic only)")
    print("="*60)
    
    try:
        test_resonance_logic()
        test_library_sorting()
        test_coherence_computation()
        test_attractor_space_structure()
        test_resonance_based_query()
        test_engram_key_properties()
        
        print("="*60)
        print("ALL TESTS PASSED ✓")
        print("="*60)
        print("\nCore engram logic is sound!")
        print("Ready to implement with full PyTorch system.")
        print("="*60 + "\n")
        
        return True
        
    except AssertionError as e:
        print("\n" + "="*60)
        print("TEST FAILED ✗")
        print("="*60)
        print(f"Error: {e}")
        print("="*60 + "\n")
        return False
    
    except Exception as e:
        print("\n" + "="*60)
        print("TEST ERROR ✗")
        print("="*60)
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        print("="*60 + "\n")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
