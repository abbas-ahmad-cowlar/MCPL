"""
Analyze experimental results and generate tables/plots.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
import os
from pathlib import Path


def load_results(csv_path: str) -> pd.DataFrame:
    """Load results CSV."""
    df = pd.read_csv(csv_path)
    return df


def generate_table1_greedy_vs_cn(df: pd.DataFrame, output_dir: str):
    """
    Table 1: Greedy vs Closest-Neighbor comparison.
    Columns: Instance, Greedy Obj, CN Obj, Greedy Time, CN Time, Greedy Wins
    """
    print("\n" + "="*70)
    print("Table 1: Greedy vs Closest-Neighbor")
    print("="*70)
    
    # Filter to only greedy and cn
    df_heur = df[df['algorithm'].isin(['greedy', 'closest_neighbor'])].copy()
    
    # Group by instance and algorithm
    summary = df_heur.groupby(['instance', 'algorithm']).agg({
        'objective': ['mean', 'std'],
        'runtime_sec': ['mean', 'std']
    }).round(2)
    
    print(summary)
    
    # Pivot for comparison
    pivot = df_heur.pivot_table(
        index='instance',
        columns='algorithm',
        values='objective',
        aggfunc='mean'
    )
    
    if 'greedy' in pivot.columns and 'closest_neighbor' in pivot.columns:
        pivot['greedy_wins'] = pivot['greedy'] > pivot['closest_neighbor']
        print("\n" + "="*70)
        print("Greedy wins: ", pivot['greedy_wins'].sum(), "/", len(pivot))
    
    # Save to file
    output_path = os.path.join(output_dir, 'table1_greedy_vs_cn.csv')
    summary.to_csv(output_path)
    print(f"\n[OK] Saved to: {output_path}")
    
    return summary


def generate_table2_multistart_improvement(df: pd.DataFrame, output_dir: str):
    """
    Table 2: Multi-Start LS improvement over constructive heuristics.
    """
    print("\n" + "="*70)
    print("Table 2: Multi-Start Local Search Improvement")
    print("="*70)
    
    # Get baseline (greedy) and LS results
    df_greedy = df[df['algorithm'] == 'greedy'].groupby('instance')['objective'].mean()
    df_ls = df[df['algorithm'] == 'local_search'].groupby('instance')['objective'].mean()
    
    comparison = pd.DataFrame({
        'greedy_baseline': df_greedy,
        'ls_objective': df_ls
    })
    
    comparison['improvement'] = comparison['ls_objective'] - comparison['greedy_baseline']
    comparison['improvement_pct'] = (comparison['improvement'] / comparison['greedy_baseline'] * 100).round(2)
    
    print(comparison)
    
    output_path = os.path.join(output_dir, 'table2_ls_improvement.csv')
    comparison.to_csv(output_path)
    print(f"\n[OK] Saved to: {output_path}")
    
    return comparison


def generate_table3_ts_vs_ls(df: pd.DataFrame, output_dir: str):
    """
    Table 3: Tabu Search vs Multi-Start LS.
    """
    print("\n" + "="*70)
    print("Table 3: Tabu Search vs Multi-Start LS")
    print("="*70)
    
    # Get LS and TS results
    summary = df[df['algorithm'].isin(['local_search', 'tabu_search'])].groupby(
        ['instance', 'algorithm']
    ).agg({
        'objective': ['mean', 'std'],
        'runtime_sec': ['mean', 'std']
    }).round(2)
    
    print(summary)
    
    # Comparison
    df_ls = df[df['algorithm'] == 'local_search'].groupby('instance')['objective'].mean()
    df_ts = df[df['algorithm'] == 'tabu_search'].groupby('instance')['objective'].mean()
    
    comparison = pd.DataFrame({
        'ls_objective': df_ls,
        'ts_objective': df_ts
    })
    
    comparison['ts_gain'] = comparison['ts_objective'] - comparison['ls_objective']
    comparison['ts_gain_pct'] = (comparison['ts_gain'] / comparison['ls_objective'] * 100).round(2)
    
    print("\n" + "="*70)
    print("TS vs LS Comparison:")
    print(comparison)
    
    output_path = os.path.join(output_dir, 'table3_ts_vs_ls.csv')
    summary.to_csv(output_path)
    print(f"\n[OK] Saved to: {output_path}")
    
    return summary


def plot_algorithm_comparison(df: pd.DataFrame, output_dir: str):
    """
    Plot 1: Box plot comparing all algorithms.
    """
    plt.figure(figsize=(10, 6))
    
    # Map algorithm names for better labels
    algo_names = {
        'greedy': 'Greedy',
        'closest_neighbor': 'Closest-Neighbor',
        'local_search': 'Multi-Start LS',
        'tabu_search': 'Tabu Search'
    }
    
    df_plot = df.copy()
    df_plot['algorithm'] = df_plot['algorithm'].map(algo_names)
    
    sns.boxplot(data=df_plot, x='algorithm', y='objective', palette='Set2')
    plt.xlabel('Algorithm', fontsize=12)
    plt.ylabel('Objective Value', fontsize=12)
    plt.title('Algorithm Performance Comparison', fontsize=14, fontweight='bold')
    plt.xticks(rotation=15, ha='right')
    plt.tight_layout()
    
    output_path = os.path.join(output_dir, 'plot1_algorithm_comparison.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n[OK] Plot saved to: {output_path}")
    plt.close()


def plot_runtime_comparison(df: pd.DataFrame, output_dir: str):
    """
    Plot 2: Runtime comparison across algorithms.
    """
    plt.figure(figsize=(10, 6))
    
    algo_names = {
        'greedy': 'Greedy',
        'closest_neighbor': 'Closest-Neighbor',
        'local_search': 'Multi-Start LS',
        'tabu_search': 'Tabu Search'
    }
    
    df_plot = df.copy()
    df_plot['algorithm'] = df_plot['algorithm'].map(algo_names)
    
    summary = df_plot.groupby('algorithm')['runtime_sec'].mean().sort_values()
    
    plt.bar(summary.index, summary.values, color='steelblue', alpha=0.7)
    plt.xlabel('Algorithm', fontsize=12)
    plt.ylabel('Average Runtime (seconds)', fontsize=12)
    plt.title('Runtime Comparison', fontsize=14, fontweight='bold')
    plt.xticks(rotation=15, ha='right')
    plt.tight_layout()
    
    output_path = os.path.join(output_dir, 'plot2_runtime_comparison.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"[OK] Plot saved to: {output_path}")
    plt.close()


def main():
    parser = argparse.ArgumentParser(description="Analyze MCLP experimental results")
    parser.add_argument('--input', type=str, required=True, help='Path to results CSV')
    parser.add_argument('--output', type=str, default='tables', help='Output directory')
    parser.add_argument('--figures', type=str, default='figures', help='Figures directory')
    args = parser.parse_args()
    
    # Create output directories
    os.makedirs(args.output, exist_ok=True)
    os.makedirs(args.figures, exist_ok=True)
    
    # Load results
    print(f"Loading results from: {args.input}")
    df = load_results(args.input)
    
    print(f"\nTotal experiments: {len(df)}")
    print(f"Algorithms: {df['algorithm'].unique()}")
    print(f"Instances: {df['instance'].unique()}")
    print(f"Seeds: {df['seed'].unique()}")
    
    # Generate tables
    generate_table1_greedy_vs_cn(df, args.output)
    generate_table2_multistart_improvement(df, args.output)
    generate_table3_ts_vs_ls(df, args.output)
    
    # Generate plots
    plot_algorithm_comparison(df, args.figures)
    plot_runtime_comparison(df, args.figures)
    
    print("\n" + "="*70)
    print("[DONE] Analysis complete!")
    print(f"   Tables: {args.output}/")
    print(f"   Figures: {args.figures}/")


if __name__ == "__main__":
    main()

    