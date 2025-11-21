"""
Instance loader for MCLP problems.
Loads JSON format and validates coverage sets.
"""

import json
import numpy as np
from typing import Dict, List, Tuple, Set

class MCLPInstance:
    def __init__(self, filepath: str):
        """Load MCLP instance from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        self.name = data.get('name', 'unnamed')
        self.I = data['I']  # Facility IDs
        self.J = data['J']  # Customer IDs
        self.f = {int(k): float(v) for k, v in data['f'].items()}  # Facility costs
        self.d = {int(k): float(v) for k, v in data['d'].items()}  # Customer demands
        self.I_j = {int(k): set(v) for k, v in data['I_j'].items()}  # Coverage sets
        self.B = float(data['B'])  # Budget
        self.radius = data.get('coverage_radius', None)
        
        # Compute reverse mapping J_i (customers covered by facility i)
        self.J_i = {i: set() for i in self.I}
        for j, facilities in self.I_j.items():
            for i in facilities:
                self.J_i[i].add(j)
        
        # Precompute total demand
        self.total_demand = sum(self.d.values())
        
        # Validate instance
        self._validate()
    
    def _validate(self):
        """Validate instance consistency."""
        # Check every customer is covered by at least one facility
        for j in self.J:
            if j not in self.I_j or len(self.I_j[j]) == 0:
                raise ValueError(f"Customer {j} has no covering facilities!")
        
        # Check budget feasibility
        min_cost = min(self.f.values())
        if self.B < min_cost:
            raise ValueError(f"Budget {self.B} too small (min facility cost = {min_cost})")
        
        # Check coverage matrix symmetry
        coverage_sum_1 = sum(len(facilities) for facilities in self.I_j.values())
        coverage_sum_2 = sum(len(customers) for customers in self.J_i.values())
        assert coverage_sum_1 == coverage_sum_2, "Coverage matrix asymmetry!"
        
        print(f"[OK] Instance '{self.name}' validated:")
        print(f"  - {len(self.I)} facilities, {len(self.J)} customers")
        print(f"  - Budget: {self.B}, Total facility cost: {sum(self.f.values()):.2f}")
        print(f"  - Total demand: {self.total_demand:.2f}")
        print(f"  - Coverage density: {coverage_sum_1 / (len(self.I) * len(self.J)):.2%}")
    
    def compute_coverage(self, open_facilities: Set[int]) -> Tuple[float, Set[int]]:
        """
        Compute total covered demand for a given facility set.
        Returns: (total_demand_covered, set_of_covered_customers)
        """
        covered = set()
        for i in open_facilities:
            covered.update(self.J_i[i])
        
        total_covered = sum(self.d[j] for j in covered)
        return total_covered, covered
    
    def is_feasible(self, open_facilities: Set[int]) -> bool:
        """Check if solution is budget-feasible."""
        total_cost = sum(self.f[i] for i in open_facilities)
        return total_cost <= self.B

# Test function
if __name__ == "__main__":
    instance = MCLPInstance("data/test_tiny.json")
    
    # Test feasibility
    K = {1, 3}  # Open facilities 1 and 3
    total_cost = sum(instance.f[i] for i in K)
    coverage, covered = instance.compute_coverage(K)
    
    print(f"\nTest solution K = {K}:")
    print(f"  Cost: {total_cost:.2f} / {instance.B:.2f} (feasible: {instance.is_feasible(K)})")
    print(f"  Covered customers: {covered}")
    print(f"  Total demand covered: {coverage:.2f}")