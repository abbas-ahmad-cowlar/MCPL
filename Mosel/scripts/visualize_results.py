#!/usr/bin/env python3
"""
MCLP Results Visualization Script

Creates visualizations from experimental results:
1. Bar charts comparing objectives across algorithms
2. Runtime comparison charts
3. Quality vs. runtime scatter plots
4. Gap to best solution charts

Usage:
    python3 scripts/visualize_results.py

Requirements:
    - matplotlib
    - pandas (optional, will work without it)

Author: MCLP Migration Team
Date: November 2025
"""

import csv
import sys
from pathlib import Path

# Try to import matplotlib
try:
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
    import matplotlib.pyplot as plt
    import numpy as np
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("Warning: matplotlib not available. Will create text-based summaries instead.")

# Configuration
RESULTS_FILE = Path("results/experimental_results.csv")
PLOTS_DIR = Path("results/plots")


def load_results():
    """Load experimental results from CSV."""
    results = {}

    if not RESULTS_FILE.exists():
        print(f"Error: {RESULTS_FILE} not found")
        print("Please run experiments first: bash scripts/run_experiments.sh")
        return None

    with open(RESULTS_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            instance = row['Instance']
            algorithm = row['Algorithm']

            if instance not in results:
                results[instance] = {}

            results[instance][algorithm] = {
                'objective': float(row['Objective']) if row['Objective'] else 0,
                'runtime': float(row['Runtime_sec']) if row['Runtime_sec'] else 0,
                'gap': float(row['Gap_to_Best_Pct']) if row['Gap_to_Best_Pct'] else 0,
            }

    return results


def create_matplotlib_plots(results):
    """Create visualizations using matplotlib."""
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)

    instances = sorted(results.keys())
    algorithms = ['Greedy', 'Closest_Neighbor', 'Local_Search',
                  'MultiStart_LS', 'Tabu_Search_500']

    # Color scheme
    colors = {
        'Greedy': '#1f77b4',
        'Closest_Neighbor': '#ff7f0e',
        'Local_Search': '#2ca02c',
        'MultiStart_LS': '#d62728',
        'Tabu_Search_500': '#9467bd',
        'Tabu_Search_2000': '#8c564b',
        'Exact_MIP': '#e377c2'
    }

    print("\n" + "="*70)
    print("Creating Visualizations")
    print("="*70)

    # Plot 1: Objective Values Comparison
    print("\n1. Creating objective comparison chart...")
    fig, ax = plt.subplots(figsize=(14, 8))

    x = np.arange(len(instances))
    width = 0.15

    for i, alg in enumerate(algorithms):
        objectives = []
        for instance in instances:
            if alg in results[instance]:
                objectives.append(results[instance][alg]['objective'])
            else:
                objectives.append(0)

        offset = (i - len(algorithms)/2) * width
        ax.bar(x + offset, objectives, width, label=alg, color=colors.get(alg, 'gray'))

    ax.set_xlabel('Instance', fontsize=12, fontweight='bold')
    ax.set_ylabel('Objective Value (Covered Demand)', fontsize=12, fontweight='bold')
    ax.set_title('MCLP Algorithm Comparison: Objective Values', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(instances, rotation=45, ha='right')
    ax.legend(loc='upper left', fontsize=10)
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(PLOTS_DIR / 'objectives_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   ✓ Saved: {PLOTS_DIR}/objectives_comparison.png")

    # Plot 2: Runtime Comparison
    print("\n2. Creating runtime comparison chart...")
    fig, ax = plt.subplots(figsize=(14, 8))

    for i, alg in enumerate(algorithms):
        runtimes = []
        for instance in instances:
            if alg in results[instance]:
                runtimes.append(results[instance][alg]['runtime'])
            else:
                runtimes.append(0)

        offset = (i - len(algorithms)/2) * width
        ax.bar(x + offset, runtimes, width, label=alg, color=colors.get(alg, 'gray'))

    ax.set_xlabel('Instance', fontsize=12, fontweight='bold')
    ax.set_ylabel('Runtime (seconds)', fontsize=12, fontweight='bold')
    ax.set_title('MCLP Algorithm Comparison: Runtime', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(instances, rotation=45, ha='right')
    ax.legend(loc='upper left', fontsize=10)
    ax.grid(axis='y', alpha=0.3)
    ax.set_yscale('log')

    plt.tight_layout()
    plt.savefig(PLOTS_DIR / 'runtime_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   ✓ Saved: {PLOTS_DIR}/runtime_comparison.png")

    # Plot 3: Gap to Best Solution
    print("\n3. Creating gap comparison chart...")
    fig, ax = plt.subplots(figsize=(14, 8))

    for i, alg in enumerate(algorithms):
        gaps = []
        for instance in instances:
            if alg in results[instance]:
                gaps.append(results[instance][alg]['gap'])
            else:
                gaps.append(0)

        offset = (i - len(algorithms)/2) * width
        ax.bar(x + offset, gaps, width, label=alg, color=colors.get(alg, 'gray'))

    ax.set_xlabel('Instance', fontsize=12, fontweight='bold')
    ax.set_ylabel('Gap to Best (%)', fontsize=12, fontweight='bold')
    ax.set_title('MCLP Algorithm Comparison: Solution Quality Gap', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(instances, rotation=45, ha='right')
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(PLOTS_DIR / 'gap_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   ✓ Saved: {PLOTS_DIR}/gap_comparison.png")

    # Plot 4: Quality vs Runtime Scatter
    print("\n4. Creating quality-runtime scatter plot...")
    fig, ax = plt.subplots(figsize=(12, 8))

    for alg in algorithms:
        runtimes = []
        gaps = []

        for instance in instances:
            if alg in results[instance]:
                runtimes.append(results[instance][alg]['runtime'])
                gaps.append(results[instance][alg]['gap'])

        if runtimes:
            ax.scatter(runtimes, gaps, label=alg, s=100, alpha=0.7,
                      color=colors.get(alg, 'gray'), edgecolors='black', linewidth=1)

    ax.set_xlabel('Runtime (seconds, log scale)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Gap to Best (%)', fontsize=12, fontweight='bold')
    ax.set_title('MCLP: Solution Quality vs. Runtime Trade-off', fontsize=14, fontweight='bold')
    ax.set_xscale('log')
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(True, alpha=0.3)

    # Add annotation
    ax.text(0.02, 0.98, 'Better quality (lower gap)\n← Slower | Faster →',
            transform=ax.transAxes, fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()
    plt.savefig(PLOTS_DIR / 'quality_vs_runtime.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   ✓ Saved: {PLOTS_DIR}/quality_vs_runtime.png")

    # Plot 5: Average Performance Summary
    print("\n5. Creating average performance summary...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Average gap
    avg_gaps = []
    for alg in algorithms:
        gaps = [results[inst][alg]['gap'] for inst in instances
                if alg in results[inst]]
        avg_gaps.append(sum(gaps) / len(gaps) if gaps else 0)

    ax1.barh(algorithms, avg_gaps, color=[colors.get(alg, 'gray') for alg in algorithms])
    ax1.set_xlabel('Average Gap to Best (%)', fontsize=12, fontweight='bold')
    ax1.set_title('Average Solution Quality\n(Lower is Better)', fontsize=12, fontweight='bold')
    ax1.grid(axis='x', alpha=0.3)

    # Average runtime
    avg_runtimes = []
    for alg in algorithms:
        runtimes = [results[inst][alg]['runtime'] for inst in instances
                    if alg in results[inst]]
        avg_runtimes.append(sum(runtimes) / len(runtimes) if runtimes else 0)

    ax2.barh(algorithms, avg_runtimes, color=[colors.get(alg, 'gray') for alg in algorithms])
    ax2.set_xlabel('Average Runtime (seconds)', fontsize=12, fontweight='bold')
    ax2.set_title('Average Computational Time\n(Lower is Faster)', fontsize=12, fontweight='bold')
    ax2.set_xscale('log')
    ax2.grid(axis='x', alpha=0.3)

    plt.tight_layout()
    plt.savefig(PLOTS_DIR / 'average_performance.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   ✓ Saved: {PLOTS_DIR}/average_performance.png")

    print("\n" + "="*70)
    print(f"✓ All visualizations created in: {PLOTS_DIR}/")
    print("="*70)


def create_text_summary(results):
    """Create text-based summary when matplotlib is not available."""
    output_file = Path("results/VISUAL_SUMMARY.txt")

    with open(output_file, 'w') as f:
        f.write("="*80 + "\n")
        f.write("MCLP EXPERIMENTAL RESULTS - VISUAL SUMMARY\n")
        f.write("="*80 + "\n\n")

        f.write("Note: matplotlib not available. Showing text summary instead.\n")
        f.write("To create visualizations, install matplotlib:\n")
        f.write("  pip install matplotlib\n\n")

        f.write("="*80 + "\n")
        f.write("ALGORITHM PERFORMANCE SUMMARY\n")
        f.write("="*80 + "\n\n")

        algorithms = ['Greedy', 'Closest_Neighbor', 'Local_Search',
                      'MultiStart_LS', 'Tabu_Search_500']

        for alg in algorithms:
            f.write(f"\n{alg}:\n")
            f.write("-" * 40 + "\n")

            gaps = []
            runtimes = []

            for instance, alg_results in results.items():
                if alg in alg_results:
                    gaps.append(alg_results[alg]['gap'])
                    runtimes.append(alg_results[alg]['runtime'])

            if gaps:
                avg_gap = sum(gaps) / len(gaps)
                avg_runtime = sum(runtimes) / len(runtimes)
                min_gap = min(gaps)
                max_gap = max(gaps)

                f.write(f"  Average Gap to Best: {avg_gap:6.2f}%\n")
                f.write(f"  Gap Range: {min_gap:6.2f}% - {max_gap:6.2f}%\n")
                f.write(f"  Average Runtime: {avg_runtime:8.4f} seconds\n")

        f.write("\n" + "="*80 + "\n")
        f.write("RECOMMENDATIONS\n")
        f.write("="*80 + "\n\n")
        f.write("For Quick Solutions (< 1 second):\n")
        f.write("  → Use Greedy or Closest Neighbor\n\n")
        f.write("For Good Solutions (10-30 seconds):\n")
        f.write("  → Use Multi-Start Local Search\n\n")
        f.write("For Best Solutions (30-120 seconds):\n")
        f.write("  → Use Tabu Search\n\n")
        f.write("="*80 + "\n")

    print(f"\n✓ Text summary created: {output_file}")


def main():
    """Main visualization function."""
    print("="*70)
    print("MCLP RESULTS VISUALIZATION")
    print("="*70)

    # Load results
    print("\nLoading experimental results...")
    results = load_results()

    if results is None:
        return 1

    print(f"✓ Loaded results for {len(results)} instances")

    # Create visualizations
    if HAS_MATPLOTLIB:
        create_matplotlib_plots(results)
    else:
        print("\nmatplotlib not available. Creating text summary instead...")
        create_text_summary(results)
        print("\nTo create charts, install matplotlib:")
        print("  pip install matplotlib")
        print("Then run this script again.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
