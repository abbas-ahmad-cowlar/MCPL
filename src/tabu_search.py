"""
Tabu Search metaheuristic for MCLP.
Implements tenure-based tabu list, aspiration criterion, and intensification.
"""

import random
import time
from typing import Set, Tuple, List, Dict, Optional
from collections import deque
from instance_loader import MCLPInstance
from greedy import greedy_heuristic
from local_search import run_local_search


class TabuSearch:
    def __init__(
        self,
        instance: MCLPInstance,
        tenure: int = 10,
        candidate_list_size: int = 20,
        max_iterations: int = 500,
        stagnation_limit: int = 100,
        intensification_freq: int = 50,
        seed: int = 42
    ):
        self.instance = instance
        self.tenure = tenure
        self.candidate_list_size = candidate_list_size
        self.max_iterations = max_iterations
        self.stagnation_limit = stagnation_limit
        self.intensification_freq = intensification_freq
        self.seed = seed
        random.seed(seed)
        
        # Current solution state
        self.K: Set[int] = set()  # Open facilities
        self.covered: Set[int] = set()
        self.budget_used: float = 0.0
        self.objective: float = 0.0
        
        # Coverage tracking (for delta-eval)
        self.covered_by_count: Dict[int, int] = {}
        
        # Global best solution
        self.best_K: Set[int] = set()
        self.best_obj: float = -float('inf')
        
        # Tabu list: {facility_id: iteration_when_tabu_expires}
        self.tabu_list: Dict[int, int] = {}
        
        # Statistics
        self.iteration = 0
        self.stagnation_counter = 0
        self.aspiration_hits = 0
        self.intensification_count = 0
        self.restart_count = 0
        self.max_restarts = 100
        
        # History tracking
        self.history = []
    
    def initialize_solution(self, initial_facilities: Set[int], reset_best: bool = True):
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
        
        # Only initialize global best on first call
        if reset_best:
            self.best_K = self.K.copy()
            self.best_obj = self.objective
    
    def _validate_state(self):
        """Sanity check to fix floating point drift."""
        recomputed_obj, _ = self.instance.compute_coverage(self.K)
        if abs(self.objective - recomputed_obj) > 1e-4:
            self.objective = recomputed_obj

    def compute_slack(self) -> float:
        """Compute remaining budget."""
        return self.instance.B - self.budget_used
    
    def is_tabu(self, facility: int) -> bool:
        """Check if facility is tabu."""
        return facility in self.tabu_list and self.tabu_list[facility] > self.iteration
    
    def aspiration_criterion(self, delta_obj: float) -> bool:
        """Override tabu if move improves global best."""
        return self.objective + delta_obj > self.best_obj
    
    def delta_eval_close(self, i: int) -> float:
        """Evaluate closing facility i."""
        if i not in self.K:
            return -float('inf')
        
        loss = 0.0
        for j in self.instance.J_i[i]:
            if self.covered_by_count[j] == 1:
                loss += self.instance.d[j]
        
        return -loss
    
    def delta_eval_open(self, j: int) -> Tuple[float, bool]:
        """Evaluate opening facility j."""
        if j in self.K:
            return -float('inf'), False
        
        cost = self.instance.f[j]
        if self.budget_used + cost > self.instance.B:
            return -float('inf'), False
        
        gain = 0.0
        for customer in self.instance.J_i[j]:
            if self.covered_by_count[customer] == 0:
                gain += self.instance.d[customer]
        
        return gain, True
    
    def delta_eval_swap(self, i_out: int, j_in: int) -> Tuple[float, bool]:
        """Evaluate swap: close i_out, open j_in."""
        if i_out not in self.K or j_in in self.K:
            return -float('inf'), False
        
        cost_diff = self.instance.f[j_in] - self.instance.f[i_out]
        if self.budget_used + cost_diff > self.instance.B:
            return -float('inf'), False
        
        loss = 0.0
        for j in self.instance.J_i[i_out]:
            if self.covered_by_count[j] == 1:
                loss += self.instance.d[j]
        
        gain = 0.0
        for j in self.instance.J_i[j_in]:
            if self.covered_by_count[j] == 0 or \
               (self.covered_by_count[j] == 1 and i_out in self.instance.I_j[j]):
                gain += self.instance.d[j]
        
        return gain - loss, True
    
    def apply_close(self, i: int):
        """Close facility i."""
        if i not in self.K:
            return
        
        self.K.remove(i)
        self.budget_used -= self.instance.f[i]
        
        for j in self.instance.J_i[i]:
            self.covered_by_count[j] -= 1
            if self.covered_by_count[j] == 0:
                self.covered.discard(j)
                self.objective -= self.instance.d[j]
        
        # Add to tabu list
        self.tabu_list[i] = self.iteration + self.tenure
    
    def apply_open(self, i: int):
        """Open facility i."""
        if i in self.K:
            return
        
        self.K.add(i)
        self.budget_used += self.instance.f[i]
        
        for j in self.instance.J_i[i]:
            if self.covered_by_count[j] == 0:
                self.covered.add(j)
                self.objective += self.instance.d[j]
            self.covered_by_count[j] += 1
        
        # Add to tabu list
        self.tabu_list[i] = self.iteration + self.tenure
    
    def apply_swap(self, i_out: int, j_in: int):
        """Execute swap."""
        self.apply_close(i_out)
        self.apply_open(j_in)
    
    def generate_candidate_moves(self) -> List[Tuple[str, any, float, bool]]:
        """
        Generate candidate moves (flip + swap).
        Returns list of: (move_type, move_data, delta_obj, is_tabu)
        """
        candidates = []
        
        # 1-flip: Close moves
        for i in self.K:
            delta = self.delta_eval_close(i)
            is_tabu = self.is_tabu(i)
            candidates.append(('close', i, delta, is_tabu))
        
        # 1-flip: Open moves
        for j in set(self.instance.I) - self.K:
            delta, feasible = self.delta_eval_open(j)
            if feasible:
                is_tabu = self.is_tabu(j)
                candidates.append(('open', j, delta, is_tabu))
        
        # Swap moves
        for i_out in self.K:
            for j_in in set(self.instance.I) - self.K:
                delta, feasible = self.delta_eval_swap(i_out, j_in)
                if feasible:
                    # Swap is tabu if either facility is tabu
                    is_tabu = self.is_tabu(i_out) or self.is_tabu(j_in)
                    candidates.append(('swap', (i_out, j_in), delta, is_tabu))
        
        return candidates
    
    def select_best_move(
        self, 
        candidates: List[Tuple[str, any, float, bool]]
    ) -> Optional[Tuple[str, any, float]]:
        """
        Select best non-tabu move, or best tabu move if aspiration criterion met.
        Uses candidate list restriction.
        """
        if not candidates:
            return None
        
        # Sort by delta (descending)
        candidates.sort(key=lambda x: x[2], reverse=True)
        
        # Restrict to top-k candidates
        candidates = candidates[:self.candidate_list_size]
        
        # Find best admissible move
        for move_type, move_data, delta, is_tabu in candidates:
            # Accept if non-tabu OR aspiration criterion met
            if not is_tabu or self.aspiration_criterion(delta):
                if is_tabu:
                    self.aspiration_hits += 1
                return (move_type, move_data, delta)
        
        # If all moves are tabu and no aspiration, take least-tabu (first in list)
        return (candidates[0][0], candidates[0][1], candidates[0][2])
    
    def shake(self):
        """
        Diversification: randomly flip 2-3 facilities to escape local optimum.
        """
        num_flips = random.randint(2, 3)
        
        # Randomly close some open facilities
        if len(self.K) >= num_flips:
            to_close = random.sample(list(self.K), min(num_flips, len(self.K)))
            for i in to_close:
                if i in self.K:  # Check again as we might close in loop
                    self.apply_close(i)
        
        # Try to open random facilities within budget
        candidates = list(set(self.instance.I) - self.K)
        random.shuffle(candidates)
        
        for i in candidates[:num_flips]:
            if self.budget_used + self.instance.f[i] <= self.instance.B:
                self.apply_open(i)
        
        self.restart_count += 1
    
    def intensify(self, verbose: bool = False):
        """
        Intensification: run local search from current solution.
        """
        if verbose:
            print(f"    [Intensification at iter {self.iteration}]")
        
        K_before = self.K.copy()
        obj_before = self.objective
        
        # Run short local search
        K_improved, obj_improved, _ = run_local_search(
            self.instance,
            self.K,
            max_moves=50,
            seed=self.seed + self.iteration,
            verbose=False
        )
        
        # Update state
        self.initialize_solution(K_improved, reset_best=False)
        
        if verbose:
            improvement = self.objective - obj_before
            print(f"    [LS improved by {improvement:+.2f}]")
        
        self.intensification_count += 1
    
    def update_best(self):
        """Update global best if current solution is better."""
        if self.objective > self.best_obj:
            self.best_obj = self.objective
            self.best_K = self.K.copy()
            self.stagnation_counter = 0
        else:
            self.stagnation_counter += 1
    
    def run(self, verbose: bool = True) -> Tuple[Set[int], float]:
        """
        Execute Tabu Search.
        Returns: (best_facilities, best_objective)
        """
        if verbose:
            print(f"Tabu Search Configuration:")
            print(f"  Tenure: {self.tenure}")
            print(f"  Candidate list size: {self.candidate_list_size}")
            print(f"  Max iterations: {self.max_iterations}")
            print(f"  Stagnation limit: {self.stagnation_limit}")
            print(f"  Intensification frequency: {self.intensification_freq}")
            print(f"\nInitial objective: {self.objective:.2f}")
            print("="*70)
        
        for iteration in range(self.max_iterations):
            self.iteration = iteration
            
            # Generate candidate moves
            candidates = self.generate_candidate_moves()
            
            if not candidates:
                if verbose:
                    print(f"Iteration {iteration}: No valid moves, terminating")
                break
            
            # Select best move
            best_move = self.select_best_move(candidates)
            
            if best_move is None:
                if verbose:
                    print(f"Iteration {iteration}: No admissible move, terminating")
                break
            
            move_type, move_data, delta = best_move
            
            # Apply move
            if move_type == 'close':
                self.apply_close(move_data)
            elif move_type == 'open':
                self.apply_open(move_data)
            elif move_type == 'swap':
                self.apply_swap(move_data[0], move_data[1])
            
            # Update global best
            self.update_best()
            
            # Log iteration
            self.history.append({
                'iteration': iteration,
                'current_obj': self.objective,
                'best_obj': self.best_obj,
                'delta': delta,
                'move_type': move_type,
                'tabu_list_size': len([v for v in self.tabu_list.values() if v > iteration]),
                'stagnation': self.stagnation_counter
            })
            
            # Verbose logging
            if verbose and (iteration + 1) % 50 == 0:
                print(f"Iter {iteration + 1:4d}: current={self.objective:.2f}, "
                      f"best={self.best_obj:.2f}, stagnation={self.stagnation_counter}, "
                      f"tabu_size={len([v for v in self.tabu_list.values() if v > iteration])}")
            
            # Intensification
            if (iteration + 1) % self.intensification_freq == 0:
                self.intensify(verbose=verbose)
                self.update_best()
            
            # Restart on stagnation
            if self.stagnation_counter >= self.stagnation_limit:
                if verbose:
                    print(f"  [Restart due to stagnation at iter {iteration}]")
                
                # Shake current solution
                self.shake()
                self._validate_state()  # <--- SNAP BACK TO REALITY
                self.stagnation_counter = 0
                
                if self.restart_count >= self.max_restarts:
                    if verbose:
                        print(f"  [Max restarts reached, terminating]")
                    break
                if self.restart_count >= self.max_restarts:
                        print(f"  [RESTART LIMIT] {self.restart_count}/{self.max_restarts} restarts")
                        print(f"  [RESTART LIMIT] Terminating at iteration {iteration}/{self.max_iterations}")
                        print(f"  [RESTART LIMIT] Best obj: {self.best_obj}, Current obj: {self.objective}")
                        break


                
        
        if verbose:
            print("="*70)
            print(f"Tabu Search Complete:")
            print(f"  Best objective: {self.best_obj:.2f}")
            print(f"  Best facilities: {sorted(self.best_K)}")
            print(f"  Total iterations: {self.iteration + 1}")
            print(f"  Aspiration hits: {self.aspiration_hits}")
            print(f"  Intensifications: {self.intensification_count}")
            print(f"  Restarts: {self.restart_count}")
        
        return self.best_K, self.best_obj

def run_tabu_search(
    instance: MCLPInstance,
    tenure: int = 10,
    candidate_list_size: int = 20,
    max_iterations: int = 500,
    stagnation_limit: int = 100,
    intensification_freq: int = 50,
    seed: int = 42,
    verbose: bool = True
) -> Tuple[Set[int], float, List[dict]]:
    """
    Convenience wrapper for Tabu Search.
    Initializes with Greedy heuristic + randomization.
    
    Returns: (best_facilities, best_objective, history)
    """
    import random
    random.seed(seed)
    
    # Get initial solution from Greedy
    if verbose:
        print("Initializing with Greedy heuristic...")
    K_init, _, _ = greedy_heuristic(instance, seed=seed)
    
    # ADD RANDOMIZATION: Remove 1-3 random facilities and add different ones
    if len(K_init) > 3:
        num_perturb = random.randint(1, min(3, len(K_init) // 2))
        to_remove = random.sample(list(K_init), num_perturb)
        for i in to_remove:
            K_init.remove(i)
        
        # Try to add random facilities
        candidates = list(set(instance.I) - K_init)
        random.shuffle(candidates)
        budget_used = sum(instance.f[i] for i in K_init)
        
        for i in candidates:
            if budget_used + instance.f[i] <= instance.B:
                K_init.add(i)
                budget_used += instance.f[i]
                if len(K_init) >= len(to_remove) + len(K_init):
                    break
    
    # Run Tabu Search
    ts = TabuSearch(
        instance,
        tenure=tenure,
        candidate_list_size=candidate_list_size,
        max_iterations=max_iterations,
        stagnation_limit=stagnation_limit,
        intensification_freq=intensification_freq,
        seed=seed
    )
    
    ts.initialize_solution(K_init)
    best_K, best_obj = ts.run(verbose=verbose)
    
    return best_K, best_obj, ts.history


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Tabu Search for MCLP")
    parser.add_argument("--instance", type=str, default="data/test_tiny.json")
    parser.add_argument("--tenure", type=int, default=10)
    parser.add_argument("--candidate-list-size", type=int, default=20)
    parser.add_argument("--max-iterations", type=int, default=500)
    parser.add_argument("--stagnation-limit", type=int, default=100)
    parser.add_argument("--intensification-freq", type=int, default=50)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    
    # Load instance
    print(f"Loading instance: {args.instance}\n")
    instance = MCLPInstance(args.instance)
    
    # Run Tabu Search
    start_time = time.time()
    
    best_K, best_obj, history = run_tabu_search(
        instance,
        tenure=args.tenure,
        candidate_list_size=args.candidate_list_size,
        max_iterations=args.max_iterations,
        stagnation_limit=args.stagnation_limit,
        intensification_freq=args.intensification_freq,
        seed=args.seed,
        verbose=True
    )
    
    runtime = time.time() - start_time
    
    # Final summary
    print(f"\nTotal runtime: {runtime:.2f} seconds")
    print(f"Budget used: {sum(instance.f[i] for i in best_K):.2f} / {instance.B:.2f}")
    print(f"Coverage: {best_obj / instance.total_demand:.1%} of total demand")