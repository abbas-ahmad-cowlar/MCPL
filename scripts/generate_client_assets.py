import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse
import os
import sys

def generate_assets(csv_path):
    # Setup
    print(f"Reading results from: {csv_path}")
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"Error: Could not find file {csv_path}")
        return

    output_dir = "report/assets"
    os.makedirs(output_dir, exist_ok=True)
    
    # Filter for main algorithms
    main_algos = ['greedy', 'cn', 'ls', 'ts']
    df_main = df[df['algorithm'].isin(main_algos)].copy()

    if df_main.empty:
        print("Error: No data found for main algorithms (greedy, cn, ls, ts)")
        return

    # ==========================================
    # 1. TABLE: Average Objective by Instance
    # ==========================================
    pivot_obj = df_main.pivot_table(
        index='instance', 
        columns='algorithm', 
        values='objective', 
        aggfunc='mean'
    )
    # Reorder columns if they exist
    cols = [c for c in ['greedy', 'cn', 'ls', 'ts'] if c in pivot_obj.columns]
    pivot_obj = pivot_obj[cols]
    
    # Calculate Improvement of TS over Greedy (%) if both exist
    if 'ts' in pivot_obj.columns and 'greedy' in pivot_obj.columns:
        pivot_obj['Improvement (%)'] = ((pivot_obj['ts'] - pivot_obj['greedy']) / pivot_obj['greedy']) * 100
    
    csv_table_path = f"{output_dir}/table_average_objective.csv"
    pivot_obj.to_csv(csv_table_path)
    print(f"[Created] Summary Table: {csv_table_path}")

    # ==========================================
    # 2. PLOT: Algorithm Comparison
    # ==========================================
    try:
        plt.figure(figsize=(12, 6))
        sns.set_style("whitegrid")
        
        # Normalize objective 
        best_per_instance = df_main.groupby('instance')['objective'].transform('max')
        df_main['Gap to Best (%)'] = ((best_per_instance - df_main['objective']) / best_per_instance) * 100
        
        sns.boxplot(x='instance', y='Gap to Best (%)', hue='algorithm', data=df_main, palette="viridis")
        plt.title('Algorithm Robustness: Gap to Best Found Solution')
        plt.ylabel('Gap (%) - Lower is Better')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        plot_path = f"{output_dir}/figure_boxplot_robustness.png"
        plt.savefig(plot_path, dpi=300)
        print(f"[Created] Boxplot: {plot_path}")
    except Exception as e:
        print(f"Could not create boxplot: {e}")

    # ==========================================
    # 3. PLOT: Runtime Scaling
    # ==========================================
    try:
        plt.figure(figsize=(10, 6))
        sns.lineplot(x='instance', y='runtime_sec', hue='algorithm', data=df_main, marker='o')
        plt.yscale('log')
        plt.title('Runtime Scalability (Log Scale)')
        plt.ylabel('Time (seconds)')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        runtime_path = f"{output_dir}/figure_runtime_scaling.png"
        plt.savefig(runtime_path, dpi=300)
        print(f"[Created] Runtime Plot: {runtime_path}")
    except Exception as e:
        print(f"Could not create runtime plot: {e}")

    print("\nDone! Assets are ready in 'report/assets/'.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/generate_client_assets.py <csv_file>")
    else:
        generate_assets(sys.argv[1])