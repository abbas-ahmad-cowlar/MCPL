"""
Unit tests for Phase 0 and Phase 1.
Validates coverage computation, feasibility, and heuristic correctness.
"""

import sys
sys.path.insert(0, 'src')

from instance_loader import MCLPInstance
from greedy import greedy_heuristic
from closest_neighbor import closest_neighbor_heuristic

def test_instance_loading():
    """Test instance loader."""
    instance = MCLPInstance("data/test_tiny.json")
    assert len(instance.I) == 4
    assert len(instance.J) == 8
    assert instance.B == 5.0
    print("[OK] Instance loading test passed")

def test_coverage_computation():
    """Test coverage calculation."""
    instance = MCLPInstance("data/test_tiny.json")
    
    # Test solution: open facilities {1, 3}
    K = {1, 3}
    coverage, covered = instance.compute_coverage(K)
    
    expected_covered = {0, 1, 3, 4, 5, 7}  # From I_j definition (adjusted to match test_tiny.json)
    assert covered == expected_covered, f"Expected {expected_covered}, got {covered}"
    
    expected_demand = sum(instance.d[j] for j in expected_covered)
    assert abs(coverage - expected_demand) < 0.01, f"Coverage mismatch: {coverage} vs {expected_demand}"
    print(f"[OK] Coverage computation test passed (coverage={coverage:.1f})")

def test_feasibility():
    """Test budget feasibility check."""
    instance = MCLPInstance("data/test_tiny.json")
    
    K_feasible = {0, 3}  # Cost = 2.0 + 1.5 = 3.5 ≤ 5.0
    K_infeasible = {0, 1, 2}  # Cost = 2.0 + 3.0 + 2.5 = 7.5 > 5.0
    
    assert instance.is_feasible(K_feasible), "Should be feasible"
    assert not instance.is_feasible(K_infeasible), "Should be infeasible"
    print("[OK] Feasibility test passed")

def test_greedy_heuristic():
    """Test Greedy heuristic."""
    instance = MCLPInstance("data/test_tiny.json")
    K, obj, covered = greedy_heuristic(instance, seed=42)
    
    # Greedy should find a feasible solution
    assert instance.is_feasible(K), f"Greedy solution infeasible: cost={sum(instance.f[i] for i in K)}"
    
    # Check objective matches coverage
    recomputed_obj, _ = instance.compute_coverage(K)
    assert abs(obj - recomputed_obj) < 0.01, f"Objective mismatch: {obj} vs {recomputed_obj}"
    
    print(f"[OK] Greedy heuristic test passed (obj={obj:.1f}, facilities={sorted(K)})")

def test_closest_neighbor_heuristic():
    """Test Closest-Neighbor heuristic."""
    instance = MCLPInstance("data/test_tiny.json")
    K, obj, covered = closest_neighbor_heuristic(instance, seed=42)
    
    # CN should find a feasible solution
    assert instance.is_feasible(K), f"CN solution infeasible: cost={sum(instance.f[i] for i in K)}"
    
    # Check objective matches coverage
    recomputed_obj, _ = instance.compute_coverage(K)
    assert abs(obj - recomputed_obj) < 0.01, f"Objective mismatch: {obj} vs {recomputed_obj}"
    
    print(f"[OK] Closest-Neighbor heuristic test passed (obj={obj:.1f}, facilities={sorted(K)})")

def test_heuristic_comparison():
    """Compare Greedy vs Closest-Neighbor."""
    instance = MCLPInstance("data/test_tiny.json")
    
    K_greedy, obj_greedy, _ = greedy_heuristic(instance, seed=42)
    K_cn, obj_cn, _ = closest_neighbor_heuristic(instance, seed=42)
    
    print(f"\n Heuristic Comparison:")
    print(f"  Greedy:            obj={obj_greedy:.1f}, facilities={sorted(K_greedy)}")
    print(f"  Closest-Neighbor:  obj={obj_cn:.1f}, facilities={sorted(K_cn)}")
    print(f"  Greedy advantage:  {obj_greedy - obj_cn:+.1f} ({(obj_greedy - obj_cn)/obj_cn*100:+.1f}%)")

if __name__ == "__main__":
    print("Running Phase 0 & Phase 1 Tests...\n")
    test_instance_loading()
    test_coverage_computation()
    test_feasibility()
    test_greedy_heuristic()
    test_closest_neighbor_heuristic()
    test_heuristic_comparison()
    print("\n[DONE] All tests passed!")