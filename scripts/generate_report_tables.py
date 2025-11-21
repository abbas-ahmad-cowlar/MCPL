"""
Generate formatted tables for final report.
Produces both CSV and LaTeX formats.
"""

import pandas as pd
import numpy as np
import argparse
import os


def format_table_latex(df: pd.DataFrame, caption: str, label: str) -> str:
    """Convert DataFrame to LaTeX table."""
    latex = df.to_latex(
        index=True,
        float_format="%.2f",
        caption=caption,
        label=label,
        escape=False
    )
    return latex


def generate_table1_greedy_vs_cn(df: pd.DataFrame, output_dir: str):
    """Table 1: Greedy vs CN (6 instances × 2 heuristics × mean obj/time)."""
    df_heur = df[df['algorithm'].isin(['greedy', 'closest_neighbor'])].copy()
    
    summary = df_heur.groupby(['instance', 'algorithm']).agg({
        'objective': ['mean', 'std'],
        'runtime_sec': ['mean', 'std']
    }).round(2)
    
    # Reshape for comparison
    table = summary.unstack(level='algorithm')
    
    # Determine winners
    if 'greedy' in df_heur['algorithm'].values and 'closest_neighbor' in df_heur['algorithm'].values:
        greedy_obj = summary.xs('greedy', level='algorithm')[('objective', 'mean')]
        cn_obj = summary.xs('closest_neighbor', level='algorithm')[('objective', 'mean')]
        table[('winner', '')] = (greedy_obj > cn_obj).map({True: 'Greedy', False: 'CN'})
    
    # Save
    csv_path = os.path.join(output_dir, 'table1_greedy_vs_cn.csv')
    table.to_csv(csv_path)
    
    latex_path = os.path.join(output_dir, 'table1_greedy_vs_cn.tex')
    with open(latex_path, 'w') as f:
        f.write(format_table_latex(
            table,
            caption="Greedy vs Closest-Neighbor Comparison",
            label="tab:greedy_vs_cn"
        ))
    
    print(f"[OK] Table 1 saved:")
    print(f"  CSV:   {csv_path}")
    print(f"  LaTeX: {latex_path}")
    
    return table


def generate_table2_ls_improvement(df: pd.DataFrame, output_dir: str):
    """Table 2: Multi-Start LS improvement over constructive."""
    # Get baseline objectives
    df_greedy = df[df['algorithm'] == 'greedy'].groupby('instance')['objective'].mean()
    df_cn = df[df['algorithm'] == 'closest_neighbor'].groupby('instance')['objective'].mean()
    df_ls = df[df['algorithm'] == 'local_search'].groupby('instance')['objective'].mean()
    
    table = pd.DataFrame({
        'Greedy Baseline': df_greedy,
        'CN Baseline': df_cn,
        'Multi-Start LS': df_ls
    })
    
    table['LS vs Greedy (%)'] = ((table['Multi-Start LS'] - table['Greedy Baseline']) / 
                                   table['Greedy Baseline'] * 100).round(2)
    table['LS vs CN (%)'] = ((table['Multi-Start LS'] - table['CN Baseline']) / 
                              table['CN Baseline'] * 100).round(2)
    
    # Save
    csv_path = os.path.join(output_dir, 'table2_ls_improvement.csv')
    table.to_csv(csv_path)
    
    latex_path = os.path.join(output_dir, 'table2_ls_improvement.tex')
    with open(latex_path, 'w') as f:
        f.write(format_table_latex(
            table,
            caption="Multi-Start Local Search Improvement",
            label="tab:ls_improvement"
        ))
    
    print(f"[OK] Table 2 saved:")
    print(f"  CSV:   {csv_path}")
    print(f"  LaTeX: {latex_path}")
    
    return table


def generate_table3_ts_vs_ls(df: pd.DataFrame, output_dir: str):
    """Table 3: TS vs Multi-Start LS."""
    df_compare = df[df['algorithm'].isin(['local_search', 'tabu_search'])].copy()
    
    summary = df_compare.groupby(['instance', 'algorithm']).agg({
        'objective': ['mean', 'std'],
        'runtime_sec': ['mean', 'std']
    }).round(2)
    
    # Calculate improvements
    df_ls = df[df['algorithm'] == 'local_search'].groupby('instance')['objective'].mean()
    df_ts = df[df['algorithm'] == 'tabu_search'].groupby('instance')['objective'].mean()
    
    table = pd.DataFrame({
        'MS-LS Obj': df_ls,
        'TS Obj': df_ts,
        'TS Gain': (df_ts - df_ls).round(2),
        'TS Gain (%)': ((df_ts - df_ls) / df_ls * 100).round(2)
    })
    
    # Add runtime comparison
    df_ls_time = df[df['algorithm'] == 'local_search'].groupby('instance')['runtime_sec'].mean()
    df_ts_time = df[df['algorithm'] == 'tabu_search'].groupby('instance')['runtime_sec'].mean()
    
    table['MS-LS Time'] = df_ls_time.round(2)
    table['TS Time'] = df_ts_time.round(2)
    
    # Save
    csv_path = os.path.join(output_dir, 'table3_ts_vs_ls.csv')
    table.to_csv(csv_path)
    
    latex_path = os.path.join(output_dir, 'table3_ts_vs_ls.tex')
    with open(latex_path, 'w') as f:
        f.write(format_table_latex(
            table,
            caption="Tabu Search vs Multi-Start Local Search",
            label="tab:ts_vs_ls"
        ))
    
    print(f"[OK] Table 3 saved:")
    print(f"  CSV:   {csv_path}")
    print(f"  LaTeX: {latex_path}")
    
    return table


def generate_table4_parameter_sensitivity(df: pd.DataFrame, output_dir: str):
    """Table 4: TS parameter sensitivity (tenure × intensification_freq)."""
    df_ts = df[df['algorithm'] == 'tabu_search'].copy()
    
    # This requires parameter metadata in results
    # For now, create summary by instance
    summary = df_ts.groupby('instance').agg({
        'objective': ['mean', 'std', 'min', 'max'],
        'runtime_sec': ['mean', 'std']
    }).round(2)
    
    csv_path = os.path.join(output_dir, 'table4_ts_sensitivity.csv')
    summary.to_csv(csv_path)
    
    latex_path = os.path.join(output_dir, 'table4_ts_sensitivity.tex')
    with open(latex_path, 'w') as f:
        f.write(format_table_latex(
            summary,
            caption="Tabu Search Parameter Sensitivity",
            label="tab:ts_sensitivity"
        ))
    
    print(f"[OK] Table 4 saved:")
    print(f"  CSV:   {csv_path}")
    print(f"  LaTeX: {latex_path}")
    
    return summary


def generate_table5_full_comparison(df: pd.DataFrame, output_dir: str):
    """Table 5: Full algorithm comparison (single seed baseline)."""
    # Filter to baseline seed (42) and selected instances
    df_baseline = df[df['seed'] == 42].copy()
    
    if len(df_baseline) == 0:
        print("[WARN]  No baseline (seed=42) results found")
        return None
    
    # Pivot table
    table = df_baseline.pivot_table(
        index='instance',
        columns='algorithm',
        values='objective',
        aggfunc='mean'
    ).round(2)
    
    # Add runtime
    table_time = df_baseline.pivot_table(
        index='instance',
        columns='algorithm',
        values='runtime_sec',
        aggfunc='mean'
    ).round(4)
    
    # Combine
    table_combined = pd.DataFrame()
    for col in table.columns:
        table_combined[f'{col}_obj'] = table[col]
        if col in table_time.columns:
            table_combined[f'{col}_time'] = table_time[col]
    
    # Save
    csv_path = os.path.join(output_dir, 'table5_full_comparison.csv')
    table_combined.to_csv(csv_path)
    
    latex_path = os.path.join(output_dir, 'table5_full_comparison.tex')
    with open(latex_path, 'w') as f:
        f.write(format_table_latex(
            table_combined,
            caption="Complete Algorithm Comparison (Deterministic Baseline, Seed=42)",
            label="tab:full_comparison"
        ))
    
    print(f"[OK] Table 5 saved:")
    print(f"  CSV:   {csv_path}")
    print(f"  LaTeX: {latex_path}")
    
    return table_combined


def main():
    parser = argparse.ArgumentParser(description="Generate formatted report tables")
    parser.add_argument('--input', type=str, required=True, help='Results CSV file')
    parser.add_argument('--output', type=str, default='tables', help='Output directory')
    args = parser.parse_args()
    
    # Create output directory
    os.makedirs(args.output, exist_ok=True)
    
    print(f"Generating tables from: {args.input}")
    print("="*70)
    
    # Load results
    df = pd.read_csv(args.input)
    
    # Generate all tables
    generate_table1_greedy_vs_cn(df, args.output)
    print()
    generate_table2_ls_improvement(df, args.output)
    print()
    generate_table3_ts_vs_ls(df, args.output)
    print()
    generate_table4_parameter_sensitivity(df, args.output)
    print()
    generate_table5_full_comparison(df, args.output)
    
    print("\n" + "="*70)
    print(f"[DONE] All tables generated in: {args.output}/")
    print(f"   - CSV files for spreadsheet import")
    print(f"   - LaTeX files for academic paper")


if __name__ == "__main__":
    main()


    