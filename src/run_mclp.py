"""
Master pipeline script for running all MCLP algorithms.
Supports single runs and batch processing with reproducible seeding.
"""

import argparse
import yaml
import json
import time
import os
import sys
from pathlib import Path

from instance_loader import MCLPInstance
from greedy import greedy_heuristic
from closest_neighbor import closest_neighbor_heuristic
from multistart import multistart_local_search
from tabu_search import run_tabu_search

def load_config(config_path: str) -> dict:
    """Load YAML configuration file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def run_compact(instance: MCLPInstance, config: dict, seed: int) -> dict:
    """
    Run compact model (placeholder - requires Mosel/PuLP integration).
    Returns result dictionary.
    """
    print("[WARNING]  Compact model solver not implemented yet")
    print("    (Requires Mosel integration or PuLP/Gurobi setup)")
    return {
        'algorithm': 'compact',
        'objective': None,
        'runtime': 0.0,
        'facilities': [],
        'status': 'not_implemented'
    }


def run_algorithm(
    algorithm: str,
    instance: MCLPInstance,
    config: dict,
    seed: int
) -> dict:
    """
    Run specified algorithm and return standardized results.
    """
    start_time = time.time()
    
    if algorithm == 'compact':
        result = run_compact(instance, config, seed)
    
    elif algorithm == 'greedy':
        K, obj, covered = greedy_heuristic(instance, seed=seed)
        result = {
            'algorithm': 'greedy',
            'objective': obj,
            'coverage_pct': obj / instance.total_demand * 100,
            'runtime': time.time() - start_time,
            'facilities': sorted(K),
            'num_facilities': len(K),
            'budget_used': sum(instance.f[i] for i in K),
            'num_moves': 0,
            'num_iterations': 0
        }
    
    elif algorithm == 'cn':
        K, obj, covered = closest_neighbor_heuristic(instance, seed=seed)
        result = {
            'algorithm': 'closest_neighbor',
            'objective': obj,
            'coverage_pct': obj / instance.total_demand * 100,
            'runtime': time.time() - start_time,
            'facilities': sorted(K),
            'num_facilities': len(K),
            'budget_used': sum(instance.f[i] for i in K),
            'num_moves': 0,
            'num_iterations': 0
        }
    
    elif algorithm == 'ls':
        ls_params = config.get('ls_params', {})
        n_starts = ls_params.get('multistart_count', 10)
        max_moves = ls_params.get('max_moves', 200)
        
        K, obj, history = multistart_local_search(
            instance,
            n_starts=n_starts,
            max_moves=max_moves,
            base_seed=seed,
            verbose=False
        )
        
        total_moves = sum(h['num_moves'] for h in history)
        
        result = {
            'algorithm': 'local_search',
            'objective': obj,
            'coverage_pct': obj / instance.total_demand * 100,
            'runtime': time.time() - start_time,
            'facilities': sorted(K),
            'num_facilities': len(K),
            'budget_used': sum(instance.f[i] for i in K),
            'num_moves': total_moves,
            'num_iterations': n_starts
        }
    
    elif algorithm == 'ts':
        ts_params = config.get('ts_params', {})
        
        K, obj, history = run_tabu_search(
            instance,
            tenure=ts_params.get('tenure', 10),
            candidate_list_size=ts_params.get('candidate_list_size', 20),
            max_iterations=ts_params.get('max_iterations', 500),
            stagnation_limit=ts_params.get('stagnation_limit', 100),
            intensification_freq=ts_params.get('intensification_freq', 50),
            seed=seed,
            verbose=False
        )
        
        result = {
            'algorithm': 'tabu_search',
            'objective': obj,
            'coverage_pct': obj / instance.total_demand * 100,
            'runtime': time.time() - start_time,
            'facilities': sorted(K),
            'num_facilities': len(K),
            'budget_used': sum(instance.f[i] for i in K),
            'num_moves': len(history),
            'num_iterations': len(history)
        }
    
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")
    
    return result


def write_result(result: dict, instance_name: str, seed: int, output_path: str):
    """Append result to CSV file."""
    import csv
    
    output_dir = os.path.dirname(output_path)
    if output_dir:  
        os.makedirs(output_dir, exist_ok=True)
    
    file_exists = os.path.isfile(output_path)
    
    fieldnames = [
        'instance', 'seed', 'algorithm', 'objective', 'coverage_pct',
        'runtime_sec', 'num_facilities', 'budget_used', 'num_moves',
        'num_iterations', 'facilities'
    ]
    
    with open(output_path, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        row = {
            'instance': instance_name,
            'seed': seed,
            'algorithm': result['algorithm'],
            'objective': result.get('objective', ''),
            'coverage_pct': result.get('coverage_pct', ''),
            'runtime_sec': result.get('runtime', ''),
            'num_facilities': result.get('num_facilities', ''),
            'budget_used': result.get('budget_used', ''),
            'num_moves': result.get('num_moves', ''),
            'num_iterations': result.get('num_iterations', ''),
            'facilities': ','.join(map(str, result.get('facilities', [])))
        }
        
        writer.writerow(row)


def main():
    parser = argparse.ArgumentParser(
        description="MCLP Master Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run single algorithm
  python run_mclp.py --instance data/test_tiny.json --algorithm greedy --seed 42
  
  # Run all algorithms from config
  python run_mclp.py --config config.yaml
  
  # Batch mode with multiple seeds
  python run_mclp.py --instance data/test_tiny.json --algorithm ts --seeds 42 43 44
        """
    )
    
    parser.add_argument('--config', type=str, help='Path to config YAML file')
    parser.add_argument('--instance', type=str, help='Path to instance file')
    parser.add_argument('--algorithm', type=str, 
                       choices=['compact', 'greedy', 'cn', 'ls', 'ts'],
                       help='Algorithm to run')
    parser.add_argument('--seed', type=int, default=42, help='Random seed')
    parser.add_argument('--seeds', type=int, nargs='+', help='Multiple seeds for batch mode')
    parser.add_argument('--output', type=str, default='results/results.csv',
                       help='Output CSV path')
    parser.add_argument('--log-level', type=str, default='INFO',
                       choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'])
    
    args = parser.parse_args()
    
    # Load configuration
# Load configuration
    if args.config:
        config = load_config(args.config)
        
        # SAFETY CHECK: Handle malformed config files
        config_instance_path = config.get('instance', {}).get('path')
        
        # Command-line args override config (if provided)
        if args.instance:
            instance_path = args.instance
        elif config_instance_path:
            instance_path = config_instance_path
        else:
            raise ValueError("Instance path not found in args OR config file.")
                
        if args.algorithm:
            algorithms = [args.algorithm]  # Use command-line algorithm
        else:
            algorithms = config.get('algorithms', ['greedy'])  # Use config algorithms
        
        seed = args.seed if args.seed != 42 else config.get('seed', 42)
        
        # Prioritize command-line output over config
        if args.output != 'results/results.csv':
            output_path = args.output
        else:
            output_path = config['results']['output_csv']
    else:
        if not args.instance or not args.algorithm:
            parser.error("Must provide either --config or both --instance and --algorithm")
        
        # Try to load config for parameters, but use command-line for what to run
        if os.path.exists('config.yaml'):
            config = load_config('config.yaml')
        else:
            config = {}
        
        instance_path = args.instance
        algorithms = [args.algorithm]
        seed = args.seed
        output_path = args.output
    
    # Handle multiple seeds
    if args.seeds:
        seeds = args.seeds
    else:
        seeds = [seed]
    
    # Load instance
    print(f"Loading instance: {instance_path}")
    instance = MCLPInstance(instance_path)
    print()
    
    # Run experiments
    total_runs = len(algorithms) * len(seeds)
    run_count = 0
    
    print(f"Running {total_runs} experiments")
    print("="*70)
    
    for algorithm in algorithms:
        for seed_val in seeds:
            run_count += 1
            
            print(f"\n[Run {run_count}/{total_runs}] Algorithm={algorithm}, Seed={seed_val}")
            
            try:
                result = run_algorithm(algorithm, instance, config, seed_val)
                
                # Write to CSV
                write_result(result, instance.name, seed_val, output_path)
                
                # Print summary
                if result.get('objective') is not None:
                    print(f"  [OK] Objective: {result['objective']:.2f}")
                    print(f"    Coverage: {result['coverage_pct']:.1f}%")
                    print(f"    Runtime: {result['runtime']:.4f}s")
                    print(f"    Facilities: {result['facilities']}")
                
            except Exception as e:
                print(f"  ✗ Error: {e}")
                import traceback
                traceback.print_exc()
    
    print("\n" + "="*70)
    print(f"Results saved to: {output_path}")
    print("[DONE] Pipeline complete!")


if __name__ == "__main__":
    main()

    