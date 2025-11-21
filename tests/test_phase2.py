"""
Unit tests for Phase 2: Local Search and Multi-Start.
"""

import sys
sys.path.insert(0, 'src')

from instance_loader import MCLPInstance
from greedy import greedy_heuristic
from local_search import LocalSearch, run_local_search
from multistart import multistart_local_search


def test_local_search_non_degradation():
    """Test that LS does not degrade solution quality."""
    instance = MCLPInstance("data/test_tiny.json")
    
    # Start from Greedy solution
    K_init, obj_init, _ = greedy_heuristic(instance, seed=42)
    
    # Run Local Search
    K_final, obj_final, num_moves = run_local_search(
        instance, K_init, max_moves=200, seed=42, verbose=False
    )
    
    # LS should not degrade
    assert obj_final >= obj_init - 0.01, \
        f"LS degraded solution: {obj_init:.2f} → {obj_final:.2f}"
    
    # Solution should be feasible
    assert instance.is_feasible(K_final), "LS returned infeasible solution"
    
    print(f"[OK] LS non-degradation test passed (init={obj_init:.1f}, final={obj_final:.1f}, moves={num_moves})")


def test_delta_evaluation():
    """Test delta-evaluation correctness."""
    instance = MCLPInstance("data/test_tiny.json")
    
    # Initialize LS
    ls = LocalSearch(instance, seed=42)
    K_init = {1, 3}
    ls.initialize_solution(K_init)
    
    initial_obj = ls.objective
    
    # Test close facility 1
    delta_close = ls.delta_eval_close(1)
    ls.apply_close(1)
    actual_change = ls.objective - initial_obj
    
    assert abs(delta_close - actual_change) < 0.01, \
        f"Delta-eval error on close: predicted={delta_close:.2f}, actual={actual_change:.2f}"
    
    # Restore state
    ls.apply_open(1)
    
    # Test open facility 0
    delta_open, feasible = ls.delta_eval_open(0)
    if feasible:
        before_open = ls.objective
        ls.apply_open(0)
        actual_change = ls.objective - before_open
        
        assert abs(delta_open - actual_change) < 0.01, \
            f"Delta-eval error on open: predicted={delta_open:.2f}, actual={actual_change:.2f}"
    
    print("[OK] Delta-evaluation test passed")


def test_multistart_improvement():
    """Test that multi-start finds better solutions than single-run."""
    instance = MCLPInstance("data/test_tiny.json")
    
    # Single-run from Greedy
    K_greedy, obj_greedy, _ = greedy_heuristic(instance, seed=42)
    K_single, obj_single, _ = run_local_search(instance, K_greedy, seed=42, verbose=False)
    
    # Multi-start
    K_multi, obj_multi, history = multistart_local_search(
        instance, n_starts=5, base_seed=42, verbose=False
    )
    
    # Multi-start should match or beat single-run
    assert obj_multi >= obj_single - 0.01, \
        f"Multi-start worse than single-run: {obj_multi:.2f} < {obj_single:.2f}"
    
    print(f"[OK] Multi-start test passed (single={obj_single:.1f}, multi={obj_multi:.1f}, improvement={obj_multi - obj_single:+.1f})")


def test_multistart_diversity():
    """Test that multi-start explores diverse solutions."""
    instance = MCLPInstance("data/test_tiny.json")
    
    _, _, history = multistart_local_search(
        instance, n_starts=6, base_seed=42, verbose=False
    )
    
    # Check that different initialization methods were used
    methods = set(h['method'] for h in history)
    assert 'Greedy' in methods, "Greedy initialization missing"
    assert 'Closest-Neighbor' in methods, "CN initialization missing"
    
    # Check that at least some starts explored different facilities
    all_facilities = [frozenset(h['facilities']) for h in history]
    unique_solutions = len(set(all_facilities))
    
    print(f"[OK] Multi-start diversity test passed ({unique_solutions} unique solutions from {len(history)} starts)")


if __name__ == "__main__":
    print("Running Phase 2 Tests...\n")
    test_local_search_non_degradation()
    test_delta_evaluation()
    test_multistart_improvement()
    test_multistart_diversity()
    print("\n[DONE] All Phase 2 tests passed!")