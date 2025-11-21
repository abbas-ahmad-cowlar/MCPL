"""
Closest-Neighbor heuristic for MCLP.
Prioritizes high-demand customers and selects nearest facilities.
"""

import argparse
import time
import numpy as np
from instance_loader import MCLPInstance
from typing import Set, Tuple, Dict

def closest_neighbor_heuristic(
    instance: MCLPInstance, 
    distances: Dict = None, 
    seed: int = 42
) -> Tuple[Set[int], float, Set[int]]:
    """
    Closest-Neighbor heuristic:
    1. Sort customers by demand (descending)
    2. For each uncovered customer, open closest feasible facility
    
    Args:
        distances: Optional distance matrix {(i,j): distance}. 
                   If None, uses coverage set cardinality as proxy.
    
    Returns:
        open_facilities, objective, covered_customers
    """
    import random
    random.seed(seed)
    
    K = set()  # Open facilities
    covered = set()  # Covered customers
    budget_used = 0.0
    
    # Sort customers by demand (high to low)
    customers_sorted = sorted(instance.J, key=lambda j: instance.d[j], reverse=True)
    
    for j in customers_sorted:
        if j in covered or budget_used >= instance.B:
            continue
        
        # Find closest uncovered facility for customer j
        candidates = []
        for i in instance.I_j[j]:
            if i in K:
                continue  # Already open
            if budget_used + instance.f[i] > instance.B:
                continue  # Budget exceeded
            
            # Distance proxy: if no distance matrix, use cost as proxy
            if distances and (i, j) in distances:
                dist = distances[(i, j)]
            else:
                dist = instance.f[i]  # Use cost as tie-breaker
            
            candidates.append((i, dist, instance.f[i]))
        
        if not candidates:
            continue
        
        # Select closest (lowest distance, tie-break by lowest cost, then lowest ID)
        candidates.sort(key=lambda x: (x[1], x[2], x[0]))
        best_facility = candidates[0][0]
        
        # Open facility
        K.add(best_facility)
        covered.update(instance.J_i[best_facility])
        budget_used += instance.f[best_facility]
    
    objective = sum(instance.d[j] for j in covered)
    return K, objective, covered


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Closest-Neighbor MCLP Heuristic")
    parser.add_argument("--instance", type=str, default="data/test_tiny.json")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    
    # Load instance
    print(f"Loading instance: {args.instance}")
    instance = MCLPInstance(args.instance)
    
    # Run Closest-Neighbor
    print("\n" + "="*60)
    print("Running Closest-Neighbor Heuristic...")
    print("="*60)
    start_time = time.time()
    K, obj, covered = closest_neighbor_heuristic(instance, seed=args.seed)
    runtime = time.time() - start_time
    
    # Output results
    print(f"\n[OK] Closest-Neighbor Solution:")
    print(f"  Open facilities: {sorted(K)}")
    print(f"  Budget used: {sum(instance.f[i] for i in K):.2f} / {instance.B:.2f}")
    print(f"  Covered customers: {len(covered)} / {len(instance.J)}")
    print(f"  Total demand covered: {obj:.2f} / {instance.total_demand:.2f} ({obj/instance.total_demand:.1%})")
    print(f"  Runtime: {runtime:.4f} seconds")