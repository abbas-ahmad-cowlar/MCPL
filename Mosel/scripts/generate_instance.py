"""
Instance generator for MCLP.
Creates random instances with configurable parameters.
"""

import argparse
import json
import numpy as np
from typing import Dict, List, Tuple, Set


def euclidean_distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """Compute Euclidean distance between two points."""
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def generate_instance(
    num_facilities: int,
    num_customers: int,
    budget: float,
    coverage_radius: float,
    coord_range: Tuple[float, float] = (0, 30),
    demand_range: Tuple[int, int] = (1, 100),
    cost_range: Tuple[float, float] = (1.0, 10.0),
    seed: int = 42
) -> Dict:
    """
    Generate random MCLP instance.
    
    Args:
        num_facilities: Number of potential facility locations
        num_customers: Number of customer demand points
        budget: Total budget for opening facilities
        coverage_radius: Maximum distance for a facility to cover a customer
        coord_range: (min, max) for x,y coordinates
        demand_range: (min, max) for customer demands
        cost_range: (min, max) for facility opening costs
        seed: Random seed for reproducibility
    
    Returns:
        Dictionary with instance data in JSON format
    """
    rng = np.random.RandomState(seed)
    
    # Generate facility locations and costs
    facilities = []
    for i in range(num_facilities):
        facilities.append({
            'id': i,
            'x': rng.uniform(*coord_range),
            'y': rng.uniform(*coord_range),
            'cost': rng.uniform(*cost_range)
        })
    
    # Generate customer locations and demands
    customers = []
    for j in range(num_customers):
        customers.append({
            'id': j,
            'x': rng.uniform(*coord_range),
            'y': rng.uniform(*coord_range),
            'demand': rng.randint(*demand_range)
        })
    
    # Compute coverage sets I(j) - facilities covering each customer
    I_j = {}
    for customer in customers:
        c_pos = (customer['x'], customer['y'])
        covering_facilities = []
        
        for facility in facilities:
            f_pos = (facility['x'], facility['y'])
            dist = euclidean_distance(c_pos, f_pos)
            
            if dist <= coverage_radius:
                covering_facilities.append(facility['id'])
        
        I_j[customer['id']] = covering_facilities
    
    # Validate: ensure every customer is covered by at least one facility
    uncovered = [j for j, facilities in I_j.items() if len(facilities) == 0]
    if uncovered:
        print(f"[WARN]  Warning: {len(uncovered)} customers have no covering facilities!")
        print(f"   Consider increasing coverage_radius (current: {coverage_radius})")
        print(f"   Uncovered customers: {uncovered[:10]}..." if len(uncovered) > 10 else f"   Uncovered: {uncovered}")
    
    # Format data for output
    instance_data = {
        "name": f"random_I{num_facilities}_J{num_customers}_B{budget}_R{coverage_radius}_s{seed}",
        "description": f"Random instance: {num_facilities} facilities, {num_customers} customers",
        "I": [f['id'] for f in facilities],
        "J": [c['id'] for c in customers],
        "f": {str(f['id']): round(f['cost'], 2) for f in facilities},
        "d": {str(c['id']): c['demand'] for c in customers},
        "I_j": {str(k): v for k, v in I_j.items()},
        "B": budget,
        "coverage_radius": coverage_radius,
        "generation_params": {
            "num_facilities": num_facilities,
            "num_customers": num_customers,
            "coord_range": coord_range,
            "demand_range": demand_range,
            "cost_range": cost_range,
            "seed": seed
        },
        "statistics": {
            "total_facility_cost": round(sum(f['cost'] for f in facilities), 2),
            "total_demand": sum(c['demand'] for c in customers),
            "avg_coverage_per_customer": round(np.mean([len(facs) for facs in I_j.values()]), 2),
            "min_coverage_per_customer": min([len(facs) for facs in I_j.values()]),
            "max_coverage_per_customer": max([len(facs) for facs in I_j.values()]),
            "coverage_density": round(sum(len(facs) for facs in I_j.values()) / (num_facilities * num_customers), 4),
            "num_uncovered_customers": len(uncovered)
        }
    }
    
    return instance_data


def validate_instance(instance_data: Dict) -> bool:
    """
    Validate instance for feasibility and consistency.
    Returns True if valid.
    """
    issues = []
    
    # Check coverage
    num_uncovered = instance_data['statistics']['num_uncovered_customers']
    if num_uncovered > 0:
        issues.append(f"{num_uncovered} customers have no covering facilities")
    
    # Check budget feasibility
    min_cost = min(instance_data['f'].values())
    if instance_data['B'] < min_cost:
        issues.append(f"Budget ({instance_data['B']}) < minimum facility cost ({min_cost})")
    
    # Check coverage matrix symmetry
    num_I = len(instance_data['I'])
    num_J = len(instance_data['J'])
    coverage_sum = sum(len(facilities) for facilities in instance_data['I_j'].values())
    expected_density = instance_data['statistics']['coverage_density']
    
    if abs(coverage_sum / (num_I * num_J) - expected_density) > 0.01:
        issues.append("Coverage density mismatch")
    
    if issues:
        print("[FAIL] Validation failed:")
        for issue in issues:
            print(f"   - {issue}")
        return False
    
    print("[OK] Instance validated successfully")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Generate random MCLP instances",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Small instance (50 facilities, 200 customers)
  python generate_instance.py --I 50 --J 200 --B 10 --radius 5.5 --seed 42 -o data/S1.json
  
  # Medium instance (100 facilities, 500 customers)
  python generate_instance.py --I 100 --J 500 --B 15 --radius 5.0 --seed 42 -o data/M1.json
  
  # Large instance (200 facilities, 1000 customers)
  python generate_instance.py --I 200 --J 1000 --B 20 --radius 4.5 --seed 42 -o data/L1.json
        """
    )
    
    parser.add_argument('--I', type=int, required=True, help='Number of facilities')
    parser.add_argument('--J', type=int, required=True, help='Number of customers')
    parser.add_argument('--B', type=float, required=True, help='Budget')
    parser.add_argument('--radius', type=float, required=True, help='Coverage radius')
    parser.add_argument('--seed', type=int, default=42, help='Random seed')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output JSON file')
    parser.add_argument('--coord-min', type=float, default=0.0, help='Min coordinate')
    parser.add_argument('--coord-max', type=float, default=30.0, help='Max coordinate')
    parser.add_argument('--demand-min', type=int, default=1, help='Min demand')
    parser.add_argument('--demand-max', type=int, default=100, help='Max demand')
    parser.add_argument('--cost-min', type=float, default=1.0, help='Min facility cost')
    parser.add_argument('--cost-max', type=float, default=10.0, help='Max facility cost')
    parser.add_argument('--validate', action='store_true', help='Validate instance after generation')
    
    args = parser.parse_args()
    
    print(f"Generating instance: {args.I} facilities, {args.J} customers")
    print(f"Budget: {args.B}, Radius: {args.radius}, Seed: {args.seed}")
    
    # Generate instance
    instance_data = generate_instance(
        num_facilities=args.I,
        num_customers=args.J,
        budget=args.B,
        coverage_radius=args.radius,
        coord_range=(args.coord_min, args.coord_max),
        demand_range=(args.demand_min, args.demand_max),
        cost_range=(args.cost_min, args.cost_max),
        seed=args.seed
    )
    
    # Print statistics
    print("\nInstance Statistics:")
    for key, value in instance_data['statistics'].items():
        print(f"  {key}: {value}")
    
    # Validate if requested
    if args.validate:
        print("\nValidating instance...")
        validate_instance(instance_data)
    
    # Save to file
    with open(args.output, 'w') as f:
        json.dump(instance_data, f, indent=2)
    
    print(f"\n[OK] Instance saved to: {args.output}")


if __name__ == "__main__":
    main()

    