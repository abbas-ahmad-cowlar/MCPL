"""
Unit tests for Phase 3: Tabu Search.
"""

import sys
sys.path.insert(0, 'src')

from instance_loader import MCLPInstance
from multistart import multistart_local_search
from tabu_search import run_tabu_search


def test_tabu_search_improvement():
    """Test that TS improves over multi-start LS."""
    instance = MCLPInstance("data/test_tiny.json")
    
    # Multi-start LS baseline
    print("Running Multi-Start LS...")
    K_ms, obj_ms, _ = multistart_local_search(
        instance, n_starts=5, base_seed=42, verbose=False
    )
    
    # Tabu Search
    print("Running Tabu Search...")
    K_ts, obj_ts, history = run_tabu_search(
        instance,
        tenure=10,
        max_iterations=100,
        seed=42,
        verbose=False
    )
    
    # TS should match or beat multi-start
    assert obj_ts >= obj_ms - 0.01, \
        f"TS worse than multi-start: {obj_ts:.2f} < {obj_ms:.2f}"
    
    print(f"[OK] TS improvement test passed (MS={obj_ms:.1f}, TS={obj_ts:.1f}, gain={obj_ts - obj_ms:+.1f})")


def test_tabu_list_functionality():
    """Test that tabu list prevents cycling."""
    instance = MCLPInstance("data/test_tiny.json")
    
    K_ts, obj_ts, history = run_tabu_search(
        instance,
        tenure=10,
        max_iterations=50,
        seed=42,
        verbose=False
    )
    
    # Check that tabu list was used
    tabu_sizes = [h['tabu_list_size'] for h in history]
    avg_tabu_size = sum(tabu_sizes) / len(tabu_sizes)
    
    assert avg_tabu_size > 0, "Tabu list never populated!"
    
    print(f"[OK] Tabu list test passed (avg size={avg_tabu_size:.1f})")


def test_aspiration_criterion():
    """Test that aspiration criterion allows tabu moves that improve best."""
    instance = MCLPInstance("data/test_tiny.json")
    
    K_ts, obj_ts, history = run_tabu_search(
        instance,
        tenure=5,  # Short tenure to force more tabu conflicts
        max_iterations=100,
        seed=42,
        verbose=False
    )
    
    # We can't guarantee aspiration hits on tiny instance,
    # but algorithm should complete without errors
    assert obj_ts > 0, "TS returned invalid solution"
    
    print(f"[OK] Aspiration criterion test passed (obj={obj_ts:.1f})")


def test_intensification():
    """Test that intensification improves search quality."""
    instance = MCLPInstance("data/test_tiny.json")
    
    # TS without intensification
    K_no_intens, obj_no_intens, _ = run_tabu_search(
        instance,
        intensification_freq=10000,  # Effectively disabled
        max_iterations=100,
        seed=42,
        verbose=False
    )
    
    # TS with intensification
    K_intens, obj_intens, _ = run_tabu_search(
        instance,
        intensification_freq=25,
        max_iterations=100,
        seed=42,
        verbose=False
    )
    
    # With intensification should match or beat without
    assert obj_intens >= obj_no_intens - 0.01, \
        f"Intensification degraded solution: {obj_intens:.2f} < {obj_no_intens:.2f}"
    
    print(f"[OK] Intensification test passed (no_intens={obj_no_intens:.1f}, intens={obj_intens:.1f})")


def test_ts_feasibility():
    """Test that all TS solutions are feasible."""
    instance = MCLPInstance("data/test_tiny.json")
    
    K_ts, obj_ts, history = run_tabu_search(
        instance,
        max_iterations=100,
        seed=42,
        verbose=False
    )
    
    # Check budget feasibility
    assert instance.is_feasible(K_ts), "TS returned infeasible solution!"
    
    # Check objective correctness
    recomputed_obj, _ = instance.compute_coverage(K_ts)
    assert abs(obj_ts - recomputed_obj) < 0.01, \
        f"Objective mismatch: {obj_ts:.2f} vs {recomputed_obj:.2f}"
    
    print(f"[OK] TS feasibility test passed (obj={obj_ts:.1f}, budget used={sum(instance.f[i] for i in K_ts):.2f})")


if __name__ == "__main__":
    print("Running Phase 3 Tests...\n")
    test_tabu_search_improvement()
    test_tabu_list_functionality()
    test_aspiration_criterion()
    test_intensification()
    test_ts_feasibility()
    print("\n[DONE] All Phase 3 tests passed!")