"""
Multi-start wrapper for Local Search.
Generates diverse initial solutions and tracks global best.
"""

import random
from typing import Set, Tuple, List, Callable
from instance_loader import MCLPInstance
from greedy import greedy_heuristic
from closest_neighbor import closest_neighbor_heuristic
from local_search import run_local_search


def generate_perturbed_greedy(
    instance: MCLPInstance, 
    seed: int,
    perturbation_rate: float = 0.3
) -> Set[int]:
    """
    Generate perturbed greedy solution:
    1. Run greedy to get K
    2. Remove random facilities (perturbation_rate fraction)
    3. Add different facilities within budget
    """
    random.seed(seed)
    K, _, _ = greedy_heuristic(instance, seed=seed)
    
    # Perturb: remove some facilities
    num_remove = max(1, int(len(K) * perturbation_rate))
    K_list = list(K)
    random.shuffle(K_list)
    to_remove = set(K_list[:num_remove])
    K = K - to_remove
    
    # Try to add different facilities
    budget_used = sum(instance.f[i] for i in K)
    candidates = list(set(instance.I) - K)
    random.shuffle(candidates)
    
    for i in candidates:
        if budget_used + instance.f[i] <= instance.B:
            K.add(i)
            budget_used += instance.f[i]
    
    return K


def generate_random_solution(instance: MCLPInstance, seed: int) -> Set[int]:
    """
    Generate random feasible solution:
    Randomly add facilities until budget exhausted.
    """
    random.seed(seed)
    K = set()
    budget_used = 0.0
    
    candidates = list(instance.I)
    random.shuffle(candidates)
    
    for i in candidates:
        if budget_used + instance.f[i] <= instance.B:
            K.add(i)
            budget_used += instance.f[i]
    
    return K


def multistart_local_search(
    instance: MCLPInstance,
    n_starts: int = 10,
    max_moves: int = 200,
    base_seed: int = 42,
    verbose: bool = True
) -> Tuple[Set[int], float, List[dict]]:
    """
    Multi-start local search with diverse initialization.
    
    Initialization strategy:
    - 1x deterministic Greedy
    - 1x deterministic Closest-Neighbor
    - (n_starts - 2) / 2 perturbed Greedy
    - (n_starts - 2) / 2 random solutions
    
    Returns:
        best_facilities: Best solution found
        best_objective: Best objective value
        history: List of dicts with per-start results
    """
    if verbose:
        print(f"Multi-Start Local Search: {n_starts} starts")
        print("="*70)
    
    global_best_K = None
    global_best_obj = -float('inf')
    history = []
    
    for start_idx in range(n_starts):
        seed = base_seed + start_idx
        
        # Determine initialization method
        if start_idx == 0:
            method = "Greedy"
            K_init, obj_init, _ = greedy_heuristic(instance, seed=seed)
        elif start_idx == 1:
            method = "Closest-Neighbor"
            K_init, obj_init, _ = closest_neighbor_heuristic(instance, seed=seed)
        elif start_idx < n_starts // 2 + 1:
            method = f"Perturbed-Greedy-{start_idx-2}"
            K_init = generate_perturbed_greedy(instance, seed=seed)
            obj_init, _ = instance.compute_coverage(K_init)
        else:
            method = f"Random-{start_idx - n_starts//2 - 1}"
            K_init = generate_random_solution(instance, seed=seed)
            obj_init, _ = instance.compute_coverage(K_init)
        
        if verbose:
            print(f"\nStart {start_idx + 1}/{n_starts} ({method})")
            print(f"  Initial: obj={obj_init:.2f}, facilities={sorted(K_init)}")
        
        # Run Local Search
        K_final, obj_final, num_moves = run_local_search(
            instance, K_init, max_moves=max_moves, seed=seed, verbose=False
        )
        
        if verbose:
            improvement = obj_final - obj_init
            print(f"  Final:   obj={obj_final:.2f}, improvement={improvement:+.2f}, moves={num_moves}")
        
        # Track history
        history.append({
            'start_idx': start_idx,
            'method': method,
            'seed': seed,
            'initial_obj': obj_init,
            'final_obj': obj_final,
            'improvement': obj_final - obj_init,
            'num_moves': num_moves,
            'facilities': K_final
        })
        
        # Update global best
        if obj_final > global_best_obj:
            global_best_obj = obj_final
            global_best_K = K_final
            if verbose:
                print(f"  [*] New global best!")
    
    if verbose:
        print("\n" + "="*70)
        print(f"Best solution found: obj={global_best_obj:.2f}")
        print(f"Open facilities: {sorted(global_best_K)}")
    
    return global_best_K, global_best_obj, history


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Multi-Start Local Search for MCLP")
    parser.add_argument("--instance", type=str, default="data/test_tiny.json")
    parser.add_argument("--n-starts", type=int, default=10)
    parser.add_argument("--max-moves", type=int, default=200)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    
    # Load instance
    print(f"Loading instance: {args.instance}\n")
    instance = MCLPInstance(args.instance)
    
    # Run Multi-Start
    import time
    start_time = time.time()
    
    best_K, best_obj, history = multistart_local_search(
        instance,
        n_starts=args.n_starts,
        max_moves=args.max_moves,
        base_seed=args.seed,
        verbose=True
    )
    
    runtime = time.time() - start_time
    
    # Summary statistics
    print("\n" + "="*70)
    print("Multi-Start Summary")
    print("="*70)
    initial_objs = [h['initial_obj'] for h in history]
    final_objs = [h['final_obj'] for h in history]
    improvements = [h['improvement'] for h in history]
    
    print(f"Total starts:         {args.n_starts}")
    print(f"Total runtime:        {runtime:.2f} seconds")
    print(f"Avg initial obj:      {sum(initial_objs)/len(initial_objs):.2f}")
    print(f"Avg final obj:        {sum(final_objs)/len(final_objs):.2f}")
    print(f"Avg improvement:      {sum(improvements)/len(improvements):.2f}")
    print(f"Best obj found:       {best_obj:.2f}")
    print(f"Best facilities:      {sorted(best_K)}")
    print(f"Budget used:          {sum(instance.f[i] for i in best_K):.2f} / {instance.B:.2f}")