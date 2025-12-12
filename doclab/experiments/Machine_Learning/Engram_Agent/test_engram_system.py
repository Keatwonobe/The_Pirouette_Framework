#!/usr/bin/env python3
"""
Test Suite for Pirouette Engram System
======================================

Validates that all components work correctly before running expensive training.
"""

import numpy as np
import torch
import torch.nn as nn
from pathlib import Path
import sys

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from pirouette_engram import (
    GenerativeEngram,
    EngramLibrary,
    EngramDistiller,
    EngramFactory
)


def test_engram_creation():
    """Test basic engram creation and properties."""
    print("\n" + "="*60)
    print("TEST 1: Engram Creation")
    print("="*60)
    
    T, obs_dim, act_dim, brain_dim, hidden_dim = 100, 10, 5, 10, 256
    
    engram = GenerativeEngram(
        obs=np.random.randn(T, obs_dim),
        actions=np.random.randn(T, act_dim),
        brain_features=np.random.randn(T, brain_dim),
        hiddens=np.random.randn(T, hidden_dim),
        mean_gamma=1.5,
        mean_DR=0.85,
        mean_surprise=0.6,
        return_raw=250.0,
        origin_episode=42
    )
    
    print(f"✓ Engram created")
    print(f"  Length: {engram.length}")
    print(f"  Mean coherence: {engram.mean_coherence:.3f}")
    print(f"  Return: {engram.return_raw:.1f}")
    print(f"  Γ: {engram.mean_gamma:.2f}, DR: {engram.mean_DR:.2f}, S: {engram.mean_surprise:.2f}")
    
    # Test resonance
    score = engram.resonance_score(1.5, 0.85, 0.6)
    print(f"  Self-resonance: {score:.3f} (should be ~1.0)")
    
    score_diff = engram.resonance_score(2.0, 0.5, 0.3)
    print(f"  Different-resonance: {score_diff:.3f} (should be <0.5)")
    
    assert score > 0.95, "Self-resonance should be very high"
    assert score_diff < 0.5, "Different conditions should have low resonance"
    
    print("✓ Test 1 PASSED\n")
    return engram


def test_library_operations(sample_engram):
    """Test library add, query, and best operations."""
    print("="*60)
    print("TEST 2: Library Operations")
    print("="*60)
    
    lib = EngramLibrary(capacity=10)
    
    # Add multiple engrams
    for i in range(15):
        T = np.random.randint(50, 200)
        eng = GenerativeEngram(
            obs=np.random.randn(T, 10),
            actions=np.random.randn(T, 5),
            brain_features=np.random.randn(T, 10),
            hiddens=np.random.randn(T, 256),
            mean_gamma=1.0 + 0.3*i,
            mean_DR=0.8 + 0.02*i,
            mean_surprise=0.5 + 0.05*i,
            return_raw=100.0 + 25.0*i,
            origin_episode=i
        )
        added = lib.add(eng)
        if added:
            print(f"  Added engram {i}: R={eng.return_raw:.1f}")
    
    print(f"\n✓ Library size: {len(lib)} (max capacity: {lib.capacity})")
    
    # Test query
    query_results = lib.query(gamma=2.0, DR=0.85, surprise=0.7, top_k=3)
    print(f"\n✓ Query returned {len(query_results)} results")
    for i, (eng, score) in enumerate(query_results):
        print(f"  {i+1}. R={eng.return_raw:.1f}, resonance={score:.3f}")
    
    # Test best
    best = lib.get_best(n=5)
    print(f"\n✓ Best {len(best)} engrams:")
    for i, eng in enumerate(best):
        print(f"  {i+1}. R={eng.return_raw:.1f}, ep={eng.origin_episode}")
    
    # Test stats
    stats = lib.stats()
    print(f"\n✓ Library stats:")
    for k, v in stats.items():
        print(f"  {k}: {v:.2f}")
    
    assert len(lib) == lib.capacity, "Library should be at capacity"
    assert len(query_results) == 3, "Query should return top-k results"
    assert best[0].return_raw >= best[-1].return_raw, "Best should be sorted"
    
    print("✓ Test 2 PASSED\n")
    return lib


def test_serialization(lib):
    """Test save/load functionality."""
    print("="*60)
    print("TEST 3: Serialization")
    print("="*60)
    
    test_path = Path("./test_library.json")
    
    # Save
    lib.save(test_path)
    print(f"✓ Saved library to {test_path}")
    
    # Load
    lib_loaded = EngramLibrary.load(test_path)
    print(f"✓ Loaded library from {test_path}")
    
    # Verify
    assert len(lib_loaded) == len(lib), "Loaded library should have same size"
    
    orig_returns = [e.return_raw for e in lib.engrams]
    loaded_returns = [e.return_raw for e in lib_loaded.engrams]
    
    assert np.allclose(orig_returns, loaded_returns), "Returns should match"
    
    print(f"  Original size: {len(lib)}")
    print(f"  Loaded size: {len(lib_loaded)}")
    print(f"  Returns match: {np.allclose(orig_returns, loaded_returns)}")
    
    # Cleanup
    test_path.unlink()
    print(f"✓ Cleaned up test file")
    
    print("✓ Test 3 PASSED\n")


def test_distiller():
    """Test engram distillation into policy."""
    print("="*60)
    print("TEST 4: Distillation")
    print("="*60)
    
    # Create dummy policy
    class DummyPolicy(nn.Module):
        def __init__(self, obs_dim, brain_dim, act_dim, hidden_dim):
            super().__init__()
            self.hidden_dim = hidden_dim
            inp_dim = obs_dim + brain_dim
            self.input_layer = nn.Linear(inp_dim, hidden_dim)
            self.gru = nn.GRUCell(hidden_dim, hidden_dim)
            self.output = nn.Linear(hidden_dim, 2*act_dim)
        
        def forward(self, obs, brain, h):
            x = torch.cat([obs, brain], dim=-1)
            x = torch.tanh(self.input_layer(x))
            h_next = self.gru(x, h)
            out = self.output(h_next)
            mean, log_std = torch.chunk(out, 2, dim=-1)
            return mean, log_std, h_next
    
    obs_dim, brain_dim, act_dim, hidden_dim = 10, 10, 5, 64
    policy = DummyPolicy(obs_dim, brain_dim, act_dim, hidden_dim)
    optimizer = torch.optim.Adam(policy.parameters(), lr=1e-3)
    
    # Create dummy engrams
    engrams = []
    for i in range(3):
        T = np.random.randint(50, 100)
        eng = GenerativeEngram(
            obs=np.random.randn(T, obs_dim),
            actions=np.random.randn(T, act_dim),
            brain_features=np.random.randn(T, brain_dim),
            hiddens=np.random.randn(T, hidden_dim),
            mean_gamma=1.5,
            mean_DR=0.8,
            mean_surprise=0.6,
            return_raw=200.0 + 50.0*i,
            origin_episode=i
        )
        engrams.append(eng)
    
    print(f"✓ Created {len(engrams)} test engrams")
    
    # Distill
    distiller = EngramDistiller(
        lr_scale=0.1,
        grad_clip=0.5,
        coherence_weight=True
    )
    
    print("\n  Running distillation...")
    loss = distiller.distill(
        policy=policy,
        optimizer=optimizer,
        engrams=engrams,
        n_steps=10,  # Small number for testing
        device="cpu"
    )
    
    print(f"\n✓ Distillation complete")
    print(f"  Final loss: {loss:.4f}")
    
    assert loss < 10.0, "Loss should converge to reasonable value"
    
    print("✓ Test 4 PASSED\n")


def test_factory():
    """Test engram factory creation from trajectories."""
    print("="*60)
    print("TEST 5: Engram Factory")
    print("="*60)
    
    T = 150
    obs_dim, act_dim, brain_dim, hidden_dim = 10, 5, 10, 256
    
    # Create trajectory data
    obs = np.random.randn(T, obs_dim)
    actions = np.random.randn(T, act_dim)
    
    # Brain features with structure: [DR, S, Gamma, ...]
    brain_features = np.zeros((T, brain_dim))
    brain_features[:, 0] = 0.8 + 0.1 * np.sin(np.linspace(0, 4*np.pi, T))  # DR
    brain_features[:, 1] = 0.6 + 0.2 * np.random.randn(T)  # S
    brain_features[:, 2] = 1.5 + 0.3 * np.random.randn(T)  # Gamma
    
    hiddens = np.random.randn(T, hidden_dim)
    return_raw = 300.0
    
    # Create engram
    engram = EngramFactory.from_trajectory(
        obs=obs,
        actions=actions,
        brain_features=brain_features,
        hiddens=hiddens,
        return_raw=return_raw,
        episode=99
    )
    
    print(f"✓ Factory created engram")
    print(f"  Length: {engram.length}")
    print(f"  Return: {engram.return_raw:.1f}")
    print(f"  Mean Γ: {engram.mean_gamma:.3f}")
    print(f"  Mean DR: {engram.mean_DR:.3f}")
    print(f"  Mean S: {engram.mean_surprise:.3f}")
    print(f"  Coherence: {engram.mean_coherence:.3f}")
    
    assert engram.length == T, "Length should match"
    assert engram.return_raw == return_raw, "Return should match"
    assert 1.0 < engram.mean_gamma < 2.0, "Gamma should be in expected range"
    
    print("✓ Test 5 PASSED\n")


def test_resonance_sensitivity():
    """Test that resonance scoring is sensitive to differences."""
    print("="*60)
    print("TEST 6: Resonance Sensitivity")
    print("="*60)
    
    # Create reference engram
    ref_engram = GenerativeEngram(
        obs=np.random.randn(100, 10),
        actions=np.random.randn(100, 5),
        brain_features=np.random.randn(100, 10),
        hiddens=np.random.randn(100, 256),
        mean_gamma=1.5,
        mean_DR=0.85,
        mean_surprise=0.6,
        return_raw=250.0
    )
    
    # Test cases
    test_cases = [
        ("Self", 1.5, 0.85, 0.6, 0.95, 1.0),
        ("Close", 1.55, 0.87, 0.62, 0.8, 1.0),
        ("Medium", 1.8, 0.9, 0.7, 0.4, 0.8),
        ("Far", 2.5, 0.5, 0.3, 0.0, 0.4)
    ]
    
    print("Testing resonance scoring:")
    for name, gamma, DR, S, min_score, max_score in test_cases:
        score = ref_engram.resonance_score(gamma, DR, S)
        passed = min_score <= score <= max_score
        status = "✓" if passed else "✗"
        print(f"  {status} {name:10s}: score={score:.3f} (expected {min_score:.2f}-{max_score:.2f})")
        assert passed, f"Resonance score out of expected range for {name}"
    
    print("✓ Test 6 PASSED\n")


def run_all_tests():
    """Run complete test suite."""
    print("\n" + "="*60)
    print("PIROUETTE ENGRAM SYSTEM - TEST SUITE")
    print("="*60)
    
    try:
        # Test 1: Basic creation
        engram = test_engram_creation()
        
        # Test 2: Library operations
        lib = test_library_operations(engram)
        
        # Test 3: Serialization
        test_serialization(lib)
        
        # Test 4: Distillation
        test_distiller()
        
        # Test 5: Factory
        test_factory()
        
        # Test 6: Resonance sensitivity
        test_resonance_sensitivity()
        
        # Success
        print("="*60)
        print("ALL TESTS PASSED ✓")
        print("="*60)
        print("\nThe engram system is operational!")
        print("You can now run: python sand_humanoid_engram.py --basin-json <path>")
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
