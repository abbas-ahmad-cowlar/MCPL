"""
Local Search for MCLP with 1-flip and swap neighborhoods.
Implements delta-evaluation for efficient move assessment.
"""

import random
import time
from typing import Set, Tuple, Dict, Optional
from instance_loader import MCLPInstance


class LocalSearch:
    def __init__(self, instance: MCLPInstance, seed: int = 42):
        self.instance = instance
        self.seed = seed
        random.seed(seed)
        
        # Current solution state
        self.K: Set[int] = set()  # Open facilities
        self.covered: Set[int] = set()  # Covered customers
        self.budget_used: float = 0.0
        self.objective: float = 0.0
        
        # Delta-evaluation cache
        self.covered_by_count: Dict[int, int] = {}  # How many facilities cover each customer
        self.move_count = 0
        self.revalidation_interval = 50
    
    def initialize_solution(self, initial_facilities: Set[int]):
        """Initialize from a given facility set."""
        self.K = initial_facilities.copy()
        self.budget_used = sum(self.instance.f[i] for i in self.K)
        self.covered = set()
        
        # Initialize coverage counts
        self.covered_by_count = {j: 0 for j in self.instance.J}
        
        for i in self.K:
            for j in self.instance.J_i[i]:
                self.covered_by_count[j] += 1
                if self.covered_by_count[j] == 1:
                    self.covered.add(j)
        
        self.objective = sum(self.instance.d[j] for j in self.covered)
        self._validate_state()
    
    def _validate_state(self):
        """Sanity check: recompute objective from scratch."""
        recomputed_obj, recomputed_covered = self.instance.compute_coverage(self.K)
        assert abs(self.objective - recomputed_obj) < 0.01, \
            f"Objective drift detected: cached={self.objective:.2f}, actual={recomputed_obj:.2f}"
        assert self.covered == recomputed_covered, "Coverage set mismatch!"
    
    def compute_slack(self) -> float:
        """Compute remaining budget."""
        return self.instance.B - self.budget_used
    
    def delta_eval_close(self, i: int) -> float:
        """
        Evaluate change in objective if we CLOSE facility i.
        Loss = demand of customers uniquely covered by i.
        """
        if i not in self.K:
            return 0.0
        
        loss = 0.0
        for j in self.instance.J_i[i]:
            if self.covered_by_count[j] == 1:  # j is uniquely covered by i
                loss += self.instance.d[j]
        
        return -loss
    
    def delta_eval_open(self, j: int) -> Tuple[float, bool]:
        """
        Evaluate change in objective if we OPEN facility j.
        Gain = demand of currently uncovered customers in J(j).
        Returns: (delta_obj, is_feasible)
        """
        if j in self.K:
            return 0.0, False
        
        cost = self.instance.f[j]
        if self.budget_used + cost > self.instance.B:
            return 0.0, False
        
        gain = 0.0
        for customer in self.instance.J_i[j]:
            if self.covered_by_count[customer] == 0:
                gain += self.instance.d[customer]
        
        return gain, True
    
    def delta_eval_swap(self, i_out: int, j_in: int) -> Tuple[float, bool]:
        """
        Evaluate swap: close i_out, open j_in.
        Returns: (delta_obj, is_feasible)
        """
        if i_out not in self.K or j_in in self.K:
            return 0.0, False
        
        cost_diff = self.instance.f[j_in] - self.instance.f[i_out]
        if self.budget_used + cost_diff > self.instance.B:
            return 0.0, False
        
        # Loss from closing i_out
        loss = 0.0
        for j in self.instance.J_i[i_out]:
            if self.covered_by_count[j] == 1:
                loss += self.instance.d[j]
        
        # Gain from opening j_in
        gain = 0.0
        for j in self.instance.J_i[j_in]:
            # Gain if customer is uncovered OR only covered by i_out (which we're closing)
            if self.covered_by_count[j] == 0 or (self.covered_by_count[j] == 1 and i_out in self.instance.I_j[j]):
                gain += self.instance.d[j]
        
        return gain - loss, True
    
    def apply_close(self, i: int):
        """Close facility i and update state."""
        if i not in self.K:
            return
        
        self.K.remove(i)
        self.budget_used -= self.instance.f[i]
        
        for j in self.instance.J_i[i]:
            self.covered_by_count[j] -= 1
            if self.covered_by_count[j] == 0:
                self.covered.discard(j)
                self.objective -= self.instance.d[j]
        
        self.move_count += 1
    
    def apply_open(self, i: int):
        """Open facility i and update state."""
        if i in self.K:
            return
        
        self.K.add(i)
        self.budget_used += self.instance.f[i]
        
        for j in self.instance.J_i[i]:
            if self.covered_by_count[j] == 0:
                self.covered.add(j)
                self.objective += self.instance.d[j]
            self.covered_by_count[j] += 1
        
        self.move_count += 1
    
    def apply_swap(self, i_out: int, j_in: int):
        """Execute swap: close i_out, open j_in."""
        self.apply_close(i_out)
        self.apply_open(j_in)
    
    def first_improvement_step(self) -> bool:
        """
        Perform one first-improvement iteration.
        Returns True if an improving move was found.
        """
        # Randomize exploration order for diversification
        facilities_open = list(self.K)
        facilities_closed = list(set(self.instance.I) - self.K)
        random.shuffle(facilities_open)
        random.shuffle(facilities_closed)
        
        best_move = None
        best_delta = 0.0
        
        # 1-flip: Try closing open facilities
        for i in facilities_open:
            delta = self.delta_eval_close(i)
            if delta > best_delta:
                best_delta = delta
                best_move = ('close', i)
        
        # 1-flip: Try opening closed facilities
        for j in facilities_closed:
            delta, feasible = self.delta_eval_open(j)
            if feasible and delta > best_delta:
                best_delta = delta
                best_move = ('open', j)
        
        # Swap: Try all combinations
        for i_out in facilities_open:
            for j_in in facilities_closed:
                delta, feasible = self.delta_eval_swap(i_out, j_in)
                if feasible and delta > best_delta:
                    best_delta = delta
                    best_move = ('swap', i_out, j_in)
        
        # Apply best move if improving
        if best_move and best_delta > 1e-6:  # Epsilon for numerical stability
            if best_move[0] == 'close':
                self.apply_close(best_move[1])
            elif best_move[0] == 'open':
                self.apply_open(best_move[1])
            elif best_move[0] == 'swap':
                self.apply_swap(best_move[1], best_move[2])
            
            # Revalidate periodically
            if self.move_count % self.revalidation_interval == 0:
                self._validate_state()
            
            return True
        
        return False
    
    def run(self, max_moves: int = 200, verbose: bool = False) -> Tuple[Set[int], float]:
        """
        Run local search until no improving move or max_moves reached.
        Returns: (best_facilities, best_objective)
        """
        if verbose:
            print(f"Initial objective: {self.objective:.2f}")
        
        for iteration in range(max_moves):
            improved = self.first_improvement_step()
            
            if not improved:
                if verbose:
                    print(f"Local optimum reached at iteration {iteration}")
                break
            
            if verbose and (iteration + 1) % 10 == 0:
                print(f"  Iteration {iteration + 1}: obj={self.objective:.2f}, moves={self.move_count}")
        
        if verbose:
            print(f"Final objective: {self.objective:.2f} (total moves: {self.move_count})")
        
        return self.K.copy(), self.objective


def run_local_search(
    instance: MCLPInstance,
    initial_facilities: Set[int],
    max_moves: int = 200,
    seed: int = 42,
    verbose: bool = True
) -> Tuple[Set[int], float, int]:
    """
    Convenience wrapper for running local search.
    Returns: (facilities, objective, num_moves)
    """
    ls = LocalSearch(instance, seed=seed)
    ls.initialize_solution(initial_facilities)
    
    K, obj = ls.run(max_moves=max_moves, verbose=verbose)
    return K, obj, ls.move_count


if __name__ == "__main__":
    import argparse
    from greedy import greedy_heuristic
    
    parser = argparse.ArgumentParser(description="Local Search for MCLP")
    parser.add_argument("--instance", type=str, default="data/test_tiny.json")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--max-moves", type=int, default=200)
    args = parser.parse_args()
    
    # Load instance
    print(f"Loading instance: {args.instance}")
    instance = MCLPInstance(args.instance)
    
    # Get initial solution from Greedy
    print("\n" + "="*60)
    print("Step 1: Running Greedy Heuristic...")
    print("="*60)
    K_init, obj_init, _ = greedy_heuristic(instance, seed=args.seed)
    print(f"Greedy solution: obj={obj_init:.2f}, facilities={sorted(K_init)}")
    
    # Run Local Search
    print("\n" + "="*60)
    print("Step 2: Running Local Search...")
    print("="*60)
    K_final, obj_final, num_moves = run_local_search(
        instance, K_init, max_moves=args.max_moves, seed=args.seed, verbose=True
    )
    
    # Summary
    print("\n" + "="*60)
    print("Summary")
    print("="*60)
    print(f"Initial (Greedy): obj={obj_init:.2f}")
    print(f"Final (LS):       obj={obj_final:.2f}")
    print(f"Improvement:      {obj_final - obj_init:+.2f} ({(obj_final - obj_init)/obj_init*100:+.1f}%)")
    print(f"Total moves:      {num_moves}")