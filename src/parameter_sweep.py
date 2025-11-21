"""
Parameter sensitivity analysis for Tabu Search.
Sweeps over tenure and intensification frequency.
"""

import pandas as pd
import numpy as np
from instance_loader import MCLPInstance
from tabu_search import run_tabu_search
import time


def parameter_sweep(
    instance_path: str,
    tenure_values: list = [7, 10, 15],
    intensification_freq_values: list = [25, 50, 100],
    seeds: list = [42, 43, 44],
    max_iterations: int = 500,
    output_csv: str = "results/ts_parameter_sweep.csv"
):
    """
    Perform parameter sweep over TS configurations.
    """
    instance = MCLPInstance(instance_path)
    results = []
    
    total_configs = len(tenure_values) * len(intensification_freq_values) * len(seeds)
    config_count = 0
    
    print(f"Parameter Sweep: {total_configs} configurations")
    print(f"Instance: {instance.name}")
    print("="*70)
    
    for tenure in tenure_values:
        for i_freq in intensification_freq_values:
            for seed in seeds:
                config_count += 1
                
                print(f"\n[Config {config_count}/{total_configs}] "
                      f"Tenure={tenure}, I_freq={i_freq}, Seed={seed}")
                
                start_time = time.time()
                
                best_K, best_obj, history = run_tabu_search(
                    instance,
                    tenure=tenure,
                    intensification_freq=i_freq,
                    max_iterations=max_iterations,
                    seed=seed,
                    verbose=False
                )
                
                runtime = time.time() - start_time
                
                results.append({
                    'instance': instance.name,
                    'tenure': tenure,
                    'intensification_freq': i_freq,
                    'seed': seed,
                    'objective': best_obj,
                    'coverage_pct': best_obj / instance.total_demand * 100,
                    'runtime': runtime,
                    'num_iterations': len(history),
                    'facilities': ','.join(map(str, sorted(best_K)))
                })
                
                print(f"  → obj={best_obj:.2f}, time={runtime:.2f}s")
    
    # Save results
    df = pd.DataFrame(results)
    df.to_csv(output_csv, index=False)
    
    print("\n" + "="*70)
    print("Parameter Sweep Complete!")
    print(f"Results saved to: {output_csv}")
    
    # Summary statistics
    print("\nSummary Statistics:")
    summary = df.groupby(['tenure', 'intensification_freq']).agg({
        'objective': ['mean', 'std'],
        'runtime': ['mean', 'std']
    }).round(2)
    print(summary)
    
    # Best configuration
    best_row = df.loc[df['objective'].idxmax()]
    print(f"\nBest Configuration:")
    print(f"  Tenure: {best_row['tenure']}")
    print(f"  Intensification Freq: {best_row['intensification_freq']}")
    print(f"  Seed: {best_row['seed']}")
    print(f"  Objective: {best_row['objective']:.2f}")
    
    return df


if __name__ == "__main__":
    import argparse
    import os
    
    parser = argparse.ArgumentParser(description="TS Parameter Sweep")
    parser.add_argument("--instance", type=str, default="data/test_tiny.json")
    parser.add_argument("--output", type=str, default="results/ts_parameter_sweep.csv")
    args = parser.parse_args()
    
    # Ensure output directory exists
    os.makedirs("results", exist_ok=True)
    
    # Run sweep
    df = parameter_sweep(
        args.instance,
        tenure_values=[7, 10, 15],
        intensification_freq_values=[25, 50, 100],
        seeds=[42, 43, 44],
        output_csv=args.output
    )
    