"""
Greedy heuristic for MCLP.
Iteratively selects facility with maximum coverage gain per cost.
"""

import argparse
import time
from instance_loader import MCLPInstance
from typing import Set, Tuple

def greedy_heuristic(instance: MCLPInstance, seed: int = 42) -> Tuple[Set[int], float, Set[int]]:
    """
    Greedy heuristic: select facilities by max (coverage_gain / cost).
    
    Returns:
        open_facilities: Set of facility IDs
        objective: Total covered demand
        covered_customers: Set of covered customer IDs
    """
    import random
    random.seed(seed)
    
    K = set()  # Open facilities
    covered = set()  # Covered customers
    budget_used = 0.0
    
    while budget_used < instance.B:
        best_facility = None
        best_gain_per_cost = 0.0
        
        # Evaluate all unopened facilities
        for i in instance.I:
            if i in K:
                continue
            
            # Check budget feasibility
            if budget_used + instance.f[i] > instance.B:
                continue
            
            # Compute incremental coverage gain
            new_customers = instance.J_i[i] - covered
            gain = sum(instance.d[j] for j in new_customers)
            gain_per_cost = gain / instance.f[i] if instance.f[i] > 0 else float('inf')
            
            # Tie-breaking: prefer lower facility ID (deterministic)
            if gain_per_cost > best_gain_per_cost or \
               (gain_per_cost == best_gain_per_cost and (best_facility is None or i < best_facility)):
                best_gain_per_cost = gain_per_cost
                best_facility = i
        
        if best_facility is None or best_gain_per_cost == 0:
            break  # No improving facility found
        
        # Open best facility
        K.add(best_facility)
        covered.update(instance.J_i[best_facility])
        budget_used += instance.f[best_facility]
    
    objective = sum(instance.d[j] for j in covered)
    return K, objective, covered


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Greedy MCLP Heuristic")
    parser.add_argument("--instance", type=str, default="data/test_tiny.json")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    
    # Load instance
    print(f"Loading instance: {args.instance}")
    instance = MCLPInstance(args.instance)
    
    # Run Greedy
    print("\n" + "="*60)
    print("Running Greedy Heuristic...")
    print("="*60)
    start_time = time.time()
    K, obj, covered = greedy_heuristic(instance, seed=args.seed)
    runtime = time.time() - start_time
    
    # Output results
    print(f"\n[OK] Greedy Solution:")
    print(f"  Open facilities: {sorted(K)}")
    print(f"  Budget used: {sum(instance.f[i] for i in K):.2f} / {instance.B:.2f}")
    print(f"  Covered customers: {len(covered)} / {len(instance.J)}")
    print(f"  Total demand covered: {obj:.2f} / {instance.total_demand:.2f} ({obj/instance.total_demand:.1%})")
    print(f"  Runtime: {runtime:.4f} seconds")