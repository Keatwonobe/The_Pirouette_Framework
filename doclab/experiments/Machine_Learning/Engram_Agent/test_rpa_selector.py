#!/usr/bin/env python3
"""
Standalone RPA Test (No PyTorch)
================================

Tests the Reverse Pareto Analysis logic for engram selection.
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class MockEngram:
    """Minimal engram for testing RPA logic."""
    length: int
    coherence_profile: np.ndarray
    DR_trace: np.ndarray
    actions: np.ndarray
    
    @classmethod
    def create_mock(cls, length: int, critical_moments: List[Tuple[int, int]]):
        """
        Create mock engram with specified critical moments.
        
        Args:
            length: Total trajectory length
            critical_moments: List of (start, end) tuples for high-impact segments
        """
        coherence = np.ones(length) * 0.5  # Baseline coherence
        DR = np.ones(length) * 0.9  # Baseline DR
        
        # Add critical moments
        for start, end in critical_moments:
            coherence[start:end] = 0.9  # High coherence
            DR[start:end] = 0.6  # Low DR (good)
        
        actions = np.random.randn(length, 5)
        
        return cls(
            length=length,
            coherence_profile=coherence,
            DR_trace=DR,
            actions=actions
        )


def compute_impact_scores(engram: MockEngram) -> np.ndarray:
    """
    Compute per-timestep impact scores.
    
    High impact = coherence increase + DR decrease
    """
    delta_coh = np.diff(engram.coherence_profile, prepend=engram.coherence_profile[0])
    delta_DR = np.diff(engram.DR_trace, prepend=engram.DR_trace[0])
    
    # Impact = coherence gain - DR gain (negative DR is good)
    impact = np.zeros(engram.length)
    for t in range(engram.length):
        coh_gain = max(0, delta_coh[t])
        DR_drop = max(0, -delta_DR[t])
        impact[t] = 0.6 * coh_gain + 0.4 * DR_drop
    
    return impact


def find_critical_few(impact_scores: np.ndarray, 
                     threshold: float = 0.8) -> Tuple[np.ndarray, float]:
    """
    Find indices accounting for threshold fraction of total impact.
    
    Returns: (critical_indices, fraction_captured)
    """
    total_impact = np.sum(impact_scores)
    if total_impact == 0:
        return np.array([]), 0.0
    
    # Sort by impact descending
    sorted_indices = np.argsort(impact_scores)[::-1]
    
    cumulative = 0.0
    critical_count = 0
    
    for idx in sorted_indices:
        cumulative += impact_scores[idx]
        critical_count += 1
        
        if cumulative / total_impact >= threshold:
            break
    
    critical_indices = sorted_indices[:critical_count]
    return critical_indices, cumulative / total_impact


def test_rpa_identifies_critical_moments():
    """Test that RPA correctly identifies the critical few moments."""
    print("\n" + "="*60)
    print("TEST 1: RPA Identifies Critical Moments")
    print("="*60)
    
    # Create engram with 3 critical segments in 200-step trajectory
    engram = MockEngram.create_mock(
        length=200,
        critical_moments=[(50, 60), (120, 130), (180, 190)]
    )
    
    # Compute impact scores
    impact = compute_impact_scores(engram)
    
    # Find critical few (should identify our planted moments)
    critical_idx, fraction = find_critical_few(impact, threshold=0.8)
    
    print(f"Total timesteps: {engram.length}")
    print(f"Critical timesteps: {len(critical_idx)} ({len(critical_idx)/engram.length:.1%})")
    print(f"Impact captured: {fraction:.1%}")
    
    # Check that critical moments overlap with planted segments
    planted_moments = set()
    for start, end in [(50, 60), (120, 130), (180, 190)]:
        planted_moments.update(range(start, end))
    
    overlap = len(set(critical_idx) & planted_moments)
    overlap_rate = overlap / len(critical_idx) if len(critical_idx) > 0 else 0
    
    print(f"\nPlanted critical moments: 30 timesteps (15%)")
    print(f"RPA-identified moments: {len(critical_idx)}")
    print(f"Overlap: {overlap} ({overlap_rate:.1%})")
    
    # Should have high overlap
    assert overlap_rate > 0.7, f"RPA should find planted moments, got {overlap_rate:.1%}"
    assert len(critical_idx) < 0.3 * engram.length, "Should identify small fraction as critical"
    
    print("\n✓ Test 1 PASSED: RPA correctly identifies critical moments\n")


def test_rpa_compression():
    """Test that focusing on critical moments compresses learning."""
    print("="*60)
    print("TEST 2: RPA Compression")
    print("="*60)
    
    lengths = [100, 200, 500, 1000]
    
    for length in lengths:
        # Create engram with 10% truly critical moments
        n_critical = length // 10
        critical_start = length // 2 - n_critical // 2
        critical_end = critical_start + n_critical
        
        engram = MockEngram.create_mock(
            length=length,
            critical_moments=[(critical_start, critical_end)]
        )
        
        # Find critical few
        impact = compute_impact_scores(engram)
        critical_idx, fraction = find_critical_few(impact, threshold=0.8)
        
        compression = 1 - (len(critical_idx) / length)
        
        print(f"  Length={length:4d}: "
              f"{len(critical_idx):4d} critical ({len(critical_idx)/length:5.1%}) | "
              f"Compression: {compression:5.1%}")
        
        # Should achieve significant compression
        assert compression > 0.5, f"Should compress by >50%, got {compression:.1%}"
    
    print("\n✓ Test 2 PASSED: RPA achieves significant compression\n")


def test_rpa_handles_uniform():
    """Test RPA behavior when all moments are equally important."""
    print("="*60)
    print("TEST 3: RPA Handles Uniform Importance")
    print("="*60)
    
    # Create engram with uniform coherence (no critical moments)
    length = 200
    coherence = np.ones(length) * 0.7
    DR = np.ones(length) * 0.8
    actions = np.random.randn(length, 5)
    
    engram = MockEngram(
        length=length,
        coherence_profile=coherence,
        DR_trace=DR,
        actions=actions
    )
    
    # Compute impact
    impact = compute_impact_scores(engram)
    critical_idx, fraction = find_critical_few(impact, threshold=0.8)
    
    print(f"Uniform trajectory:")
    print(f"  Total timesteps: {length}")
    print(f"  Critical timesteps: {len(critical_idx)}")
    print(f"  Impact std: {np.std(impact):.4f} (low = uniform)")
    print(f"  Total impact: {np.sum(impact):.4f}")
    
    # When uniform with zero impact, RPA should return empty or minimal set
    # This is correct behavior - if nothing has impact, nothing is critical
    if np.sum(impact) == 0:
        print("\n  → Zero total impact detected (correct for uniform baseline)")
        assert len(critical_idx) == 0, "Zero impact should yield zero critical moments"
    else:
        # If there is some impact, should need most of trajectory
        assert len(critical_idx) > 0.6 * length, "Uniform trajectory needs most steps"
    
    print("\n✓ Test 3 PASSED: RPA handles uniform importance correctly\n")


def test_pareto_threshold_scaling():
    """Test that pareto threshold controls compression."""
    print("="*60)
    print("TEST 4: Pareto Threshold Scaling")
    print("="*60)
    
    # Create engram
    engram = MockEngram.create_mock(
        length=200,
        critical_moments=[(50, 60), (120, 130), (180, 190)]
    )
    
    impact = compute_impact_scores(engram)
    
    thresholds = [0.5, 0.7, 0.8, 0.9, 0.95]
    
    print(f"Trajectory length: {engram.length}")
    print(f"\nPareto threshold vs critical count:")
    
    for thresh in thresholds:
        critical_idx, fraction = find_critical_few(impact, threshold=thresh)
        print(f"  {thresh:.0%}: {len(critical_idx):3d} timesteps "
              f"({len(critical_idx)/engram.length:5.1%}) | "
              f"Impact: {fraction:.1%}")
        
        # Higher threshold should require more timesteps
        assert fraction >= thresh - 0.05, "Should capture requested threshold"
    
    print("\n✓ Test 4 PASSED: Threshold controls compression\n")


def test_weighted_learning_simulation():
    """Simulate effect of RPA weighting on learning."""
    print("="*60)
    print("TEST 5: Weighted Learning Simulation")
    print("="*60)
    
    # Create engram
    engram = MockEngram.create_mock(
        length=200,
        critical_moments=[(50, 60), (120, 130), (180, 190)]
    )
    
    impact = compute_impact_scores(engram)
    critical_idx, _ = find_critical_few(impact, threshold=0.8)
    
    # Create learning weights (5x for critical, 1x for others)
    weights = np.ones(engram.length)
    weights[critical_idx] = 5.0
    
    # Normalize
    weights = weights / weights.mean()
    
    # Simulate gradient magnitudes
    baseline_grads = np.ones(engram.length)
    weighted_grads = baseline_grads * weights
    
    # Compare learning allocation
    critical_set = set(critical_idx)
    
    baseline_on_critical = sum(baseline_grads[i] for i in critical_idx)
    weighted_on_critical = sum(weighted_grads[i] for i in critical_idx)
    
    total_baseline = sum(baseline_grads)
    total_weighted = sum(weighted_grads)
    
    baseline_fraction = baseline_on_critical / total_baseline
    weighted_fraction = weighted_on_critical / total_weighted
    
    print(f"Learning allocation to critical {len(critical_idx)} timesteps:")
    print(f"  Uniform: {baseline_fraction:.1%}")
    print(f"  RPA-weighted (5x): {weighted_fraction:.1%}")
    print(f"  Improvement: {weighted_fraction/baseline_fraction:.1f}x")
    
    # RPA should significantly increase focus on critical moments
    assert weighted_fraction > 2 * baseline_fraction, \
        "RPA weighting should double+ focus on critical moments"
    
    print("\n✓ Test 5 PASSED: RPA weighting increases focus on critical moments\n")


def run_all_tests():
    """Run complete RPA test suite."""
    print("\n" + "="*60)
    print("RPA ENGRAM SELECTOR - TEST SUITE")
    print("="*60)
    print("Testing INST-NALY-001 Reverse Pareto Analysis")
    print("="*60)
    
    try:
        test_rpa_identifies_critical_moments()
        test_rpa_compression()
        test_rpa_handles_uniform()
        test_pareto_threshold_scaling()
        test_weighted_learning_simulation()
        
        print("="*60)
        print("ALL TESTS PASSED ✓")
        print("="*60)
        print("\nRPA system validated!")
        print("The critical few moments CAN be identified.")
        print("Learning can be focused on high-leverage regions.")
        print("\nReady to integrate with engram distillation!")
        print("="*60 + "\n")
        
        return True
        
    except AssertionError as e:
        print("\n" + "="*60)
        print("TEST FAILED ✗")
        print("="*60)
        print(f"Error: {e}")
        print("="*60 + "\n")
        return False


if __name__ == "__main__":
    import sys
    success = run_all_tests()
    sys.exit(0 if success else 1)
