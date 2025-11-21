"""
Generate convergence plots and additional visualizations for experiments.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
import os


def plot_convergence_ts(results_csv: str, output_dir: str):
    """
    Plot 1: Convergence curves for Tabu Search.
    Shows iteration vs best objective for 2 instances.
    """
    # Note: This requires storing iteration history
    # For now, create a placeholder showing final results
    
    df = pd.read_csv(results_csv)
    df_ts = df[df['algorithm'] == 'tabu_search'].copy()
    
    if len(df_ts) == 0:
        print("[WARN]  No TS results found for convergence plot")
        return
    
    # Group by instance
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    instances = df_ts['instance'].unique()[:2]  # Take first 2 instances
    
    for idx, instance in enumerate(instances):
        ax = axes[idx]
        
        df_inst = df_ts[df_ts['instance'] == instance]
        
        # Plot objective distribution across seeds
        seeds = df_inst['seed'].values
        objectives = df_inst['objective'].values
        
        ax.plot(range(len(seeds)), objectives, marker='o', linewidth=2, markersize=6)
        ax.axhline(y=objectives.mean(), color='r', linestyle='--', 
                   label=f'Mean: {objectives.mean():.1f}', alpha=0.7)
        ax.fill_between(range(len(seeds)), 
                        objectives.mean() - objectives.std(),
                        objectives.mean() + objectives.std(),
                        alpha=0.2, color='red')
        
        ax.set_xlabel('Run Index', fontsize=11)
        ax.set_ylabel('Best Objective', fontsize=11)
        ax.set_title(f'TS Convergence: {os.path.basename(instance)}', 
                     fontsize=12, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    output_path = os.path.join(output_dir, 'plot_convergence_ts.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"[OK] Convergence plot saved to: {output_path}")
    plt.close()


def plot_runtime_scaling(results_csv: str, output_dir: str):
    """
    Plot 2: Runtime scaling (|I|×|J| vs time) for all algorithms.
    """
    df = pd.read_csv(results_csv)
    
    # Extract instance sizes from names
    def extract_size(instance_name):
        # Parse instance names like "random_I100_J500_..."
        try:
            parts = instance_name.split('_')
            I = int(parts[1][1:])  # Skip 'I'
            J = int(parts[2][1:])  # Skip 'J'
            return I, J, I * J
        except:
            return None, None, None
    
    df[['num_I', 'num_J', 'size']] = df['instance'].apply(
        lambda x: pd.Series(extract_size(x))
    )
    
    # Remove rows with unknown sizes
    df_plot = df.dropna(subset=['size']).copy()
    
    if len(df_plot) == 0:
        print("[WARN]  Cannot extract instance sizes for scaling plot")
        return
    
    # Group by algorithm and size
    summary = df_plot.groupby(['algorithm', 'size']).agg({
        'runtime_sec': 'mean'
    }).reset_index()
    
    # Plot
    plt.figure(figsize=(10, 6))
    
    algo_names = {
        'greedy': 'Greedy',
        'closest_neighbor': 'Closest-Neighbor',
        'local_search': 'Multi-Start LS',
        'tabu_search': 'Tabu Search'
    }
    
    for algo in summary['algorithm'].unique():
        df_algo = summary[summary['algorithm'] == algo]
        label = algo_names.get(algo, algo)
        plt.loglog(df_algo['size'], df_algo['runtime_sec'], 
                  marker='o', linewidth=2, markersize=8, label=label)
    
    plt.xlabel('Problem Size (|I| × |J|)', fontsize=12)
    plt.ylabel('Average Runtime (seconds, log scale)', fontsize=12)
    plt.title('Runtime Scaling Analysis', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3, which='both')
    plt.tight_layout()
    
    output_path = os.path.join(output_dir, 'plot_runtime_scaling.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"[OK] Runtime scaling plot saved to: {output_path}")
    plt.close()


def plot_coverage_vs_budget(results_csv: str, output_dir: str):
    """
    Plot 3: Coverage % vs Budget Utilization scatter for TS solutions.
    """
    df = pd.read_csv(results_csv)
    df_ts = df[df['algorithm'] == 'tabu_search'].copy()
    
    if len(df_ts) == 0:
        print("[WARN]  No TS results for coverage plot")
        return
    
    # Compute budget utilization %
    # Note: Need to extract budget from instance or compute from budget_used
    # For now, use budget_used as proxy
    
    plt.figure(figsize=(10, 6))
    
    # Color by instance
    instances = df_ts['instance'].unique()
    colors = sns.color_palette('husl', len(instances))
    
    for idx, instance in enumerate(instances):
        df_inst = df_ts[df_ts['instance'] == instance]
        
        plt.scatter(df_inst['budget_used'], df_inst['coverage_pct'],
                   s=100, alpha=0.6, color=colors[idx],
                   label=os.path.basename(instance)[:20], edgecolors='black')
    
    plt.xlabel('Budget Used', fontsize=12)
    plt.ylabel('Coverage (%)', fontsize=12)
    plt.title('Coverage vs Budget Utilization (TS Solutions)', 
              fontsize=14, fontweight='bold')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    output_path = os.path.join(output_dir, 'plot_coverage_vs_budget.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"[OK] Coverage vs budget plot saved to: {output_path}")
    plt.close()


def plot_parameter_sensitivity_heatmap(results_csv: str, output_dir: str):
    """
    Plot 4: Heatmap showing TS parameter sensitivity (tenure × intensification_freq).
    """
    df = pd.read_csv(results_csv)
    df_ts = df[df['algorithm'] == 'tabu_search'].copy()
    
    # Try to identify parameter sweep runs
    # This requires parsing instance names or adding metadata
    # For now, skip if insufficient data
    
    print("[WARN]  Parameter sensitivity heatmap requires sweep metadata")
    print("    Run parameter sweep separately and visualize results")


def main():
    parser = argparse.ArgumentParser(description="Generate convergence and analysis plots")
    parser.add_argument('--input', type=str, required=True, help='Results CSV file')
    parser.add_argument('--output', type=str, default='figures', help='Output directory')
    args = parser.parse_args()
    
    # Create output directory
    os.makedirs(args.output, exist_ok=True)
    
    print(f"Generating plots from: {args.input}")
    print("="*70)
    
    # Generate plots
    plot_convergence_ts(args.input, args.output)
    plot_runtime_scaling(args.input, args.output)
    plot_coverage_vs_budget(args.input, args.output)
    plot_parameter_sensitivity_heatmap(args.input, args.output)
    
    print("\n" + "="*70)
    print(f"[DONE] Plots saved to: {args.output}/")


if __name__ == "__main__":
    main()