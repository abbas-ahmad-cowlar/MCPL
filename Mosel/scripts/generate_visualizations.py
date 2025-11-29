"""
MCLP Benchmark Visualization Script
Generates all charts and tables for the LaTeX report
Based on sample report format (pages 19-27)
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import re

# Set style for professional plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'serif'

class MCLPVisualizer:
    def __init__(self, results_dir='results_complete', output_dir='figures'):
        self.results_dir = Path(results_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.data = None
        
    def parse_results(self):
        """Parse all result files and extract metrics"""
        results = []
        
        for file in self.results_dir.glob('*.txt'):
            # Skip temp files
            if '_error' in file.name or '_ascii' in file.name:
                continue
                
            # Parse filename: Dataset_Algorithm.txt
            match = re.match(r'(.+)_(.+)\.txt', file.name)
            if not match:
                continue
                
            dataset, algorithm = match.groups()
            
            # Read file content - try multiple encodings (including UTF-16)
            content = None
            for encoding in ['utf-16-le', 'utf-16', 'utf-8', 'utf-8-sig', 'latin-1', 'cp1252']:
                try:
                    content = file.read_text(encoding=encoding, errors='ignore')
                    # Check if we got valid text (not just null bytes)
                    if content and len(content.strip()) > 0:
                        break
                except:
                    continue
            if content is None or len(content.strip()) == 0:
                continue
            
            # Extract objective value (try multiple patterns)
            # Patterns must handle variable whitespace
            objective = None
            for pattern in [
                r'Covered demand:\s+([\d\.]+)',  # Exact: "Covered demand:      7646.00"
                r'Final objective:\s+([\d\.]+)\s+/\s+[\d\.]+',  # Local/Tabu: "Final objective:    7646.00 /    9749.00"
                r'Total demand covered:\s+([\d\.]+)\s+/\s+[\d\.]+',  # Greedy/Closest: "Total demand covered:    7646.00 /    9749.00"
                r'Total demand covered:\s+([\d\.]+)',  # Fallback without ratio
                r'Best solution found:\s*\n\s*Objective:\s+([\d\.]+)',  # MultiStart: "Best solution found:\n  Objective:    7646.00"
                r'Objective:\s+([\d\.]+)\s+/\s+[\d\.]+',  # MultiStart/Tabu summary format
                r'Objective:\s+([\d\.]+)',  # Initial objective or fallback
            ]:
                match = re.search(pattern, content, re.MULTILINE)
                if match:
                    try:
                        objective = float(match.group(1))
                        break
                    except:
                        continue
            
            # Extract runtime (try multiple patterns)
            # Patterns must handle "seconds" suffix and variable whitespace
            runtime = None
            for pattern in [
                r'Runtime:\s+([\d\.]+)',  # "Runtime:   0.0004 seconds" or "Runtime:   0.3571 seconds"
                r'Solve time:\s+([\d\.]+)',  # "Solve time:     0.03 seconds"
                r'Total runtime:\s+([\d\.]+)',  # MultiStart: "Total runtime:     0.01 seconds"
                r'Runtime:\s+([\d\.]+)\s+seconds',  # Explicit with seconds
                r'Solve time:\s+([\d\.]+)\s+seconds',  # Explicit with seconds
                r'Total runtime:\s+([\d\.]+)\s+seconds',  # MultiStart explicit
            ]:
                match = re.search(pattern, content)
                if match:
                    try:
                        runtime = float(match.group(1))
                        break
                    except:
                        continue
            
            # Extract instance size info
            facilities = customers = None
            match = re.search(r'Facilities:\s+(\d+),\s+Customers:\s+(\d+)', content)
            if match:
                facilities = int(match.group(1))
                customers = int(match.group(2))
            
            results.append({
                'Dataset': dataset,
                'Algorithm': algorithm,
                'Objective': objective,
                'Runtime': runtime,
                'Facilities': facilities,
                'Customers': customers
            })
        
        self.data = pd.DataFrame(results)
        return self.data
    
    def calculate_gaps(self):
        """Calculate GAP% for each algorithm vs best solution"""
        if self.data is None:
            self.parse_results()
        
        # Find best objective for each dataset
        best_obj = self.data.groupby('Dataset')['Objective'].max()
        
        # Calculate GAP%
        self.data['BestObjective'] = self.data['Dataset'].map(best_obj)
        self.data['GAP%'] = ((self.data['BestObjective'] - self.data['Objective']) / 
                             self.data['BestObjective'] * 100)
        self.data['GAP%'] = self.data['GAP%'].fillna(0)
        
        return self.data
    
    def create_performance_table(self):
        """Create performance comparison table (like sample page 20-21)"""
        if 'GAP%' not in self.data.columns:
            self.calculate_gaps()
        
        # Get all unique algorithms and datasets
        all_algorithms = sorted(self.data['Algorithm'].unique())
        all_datasets = sorted(self.data['Dataset'].unique())
        
        # Create a complete index with all dataset-algorithm combinations
        complete_index = pd.MultiIndex.from_product([all_datasets, all_algorithms], 
                                                     names=['Dataset', 'Algorithm'])
        
        # Pivot table: Datasets x Algorithms
        table = self.data.pivot_table(
            index='Dataset',
            columns='Algorithm',
            values=['Objective', 'GAP%'],
            aggfunc='first'
        )
        
        # Reindex to ensure all algorithms are present (fill missing with NaN)
        if isinstance(table.columns, pd.MultiIndex):
            # Create full MultiIndex with all algorithms
            full_columns = pd.MultiIndex.from_product([
                ['Objective', 'GAP%'],
                all_algorithms
            ])
            table = table.reindex(columns=full_columns)
        
        # Save as CSV for LaTeX
        table.to_csv(self.output_dir / 'performance_table.csv')
        
        # Create formatted LaTeX table
        with open(self.output_dir / 'performance_table.tex', 'w') as f:
            f.write('\\begin{table}[htbp]\n')
            f.write('\\centering\n')
            f.write('\\caption{Performance Comparison Across All Instances}\n')
            f.write('\\label{tab:performance}\n')
            f.write('\\begin{tabular}{l' + 'rr' * len(table.columns.levels[1]) + '}\n')
            f.write('\\toprule\n')
            
            # Header
            f.write('Instance & ')
            for alg in table.columns.levels[1]:
                f.write(f'\\multicolumn{{2}}{{c}}{{{alg}}} ')
                if alg != table.columns.levels[1][-1]:
                    f.write('& ')
            f.write('\\\\\n')
            f.write('& ' + ' & '.join(['Obj', 'GAP\\%'] * len(table.columns.levels[1])) + ' \\\\\n')
            f.write('\\midrule\n')
            
            # Data rows
            for idx in table.index:
                f.write(f'{idx} & ')
                row_data = []
                for alg in table.columns.levels[1]:
                    try:
                        obj = table.loc[idx, ('Objective', alg)]
                        gap = table.loc[idx, ('GAP%', alg)]
                        if pd.notna(obj):
                            row_data.append(f'{obj:.0f} & {gap:.1f}\\%')
                        else:
                            row_data.append('N/A & N/A')
                    except (KeyError, IndexError):
                        row_data.append('N/A & N/A')
                f.write(' & '.join(row_data) + ' \\\\\n')
            
            f.write('\\bottomrule\n')
            f.write('\\end{tabular}\n')
            f.write('\\end{table}\n')
        
        print(f"Created performance table: {self.output_dir / 'performance_table.tex'}")
        return table
    
    def plot_runtime_comparison(self):
        """Create runtime comparison bar chart (like sample page 22)"""
        if self.data is None:
            self.parse_results()
        
        # Filter out failed runs
        plot_data = self.data[self.data['Runtime'].notna()].copy()
        
        # Create figure with subplots for different algorithm groups
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Group 1: Heuristics (Greedy, ClosestNeighbor, LocalSearch)
        heuristics = ['Greedy', 'ClosestNeighbor', 'LocalSearch']
        heur_data = plot_data[plot_data['Algorithm'].isin(heuristics)]
        
        if not heur_data.empty:
            pivot1 = heur_data.pivot(index='Dataset', columns='Algorithm', values='Runtime')
            pivot1.plot(kind='bar', ax=ax1, width=0.8)
            ax1.set_title('Runtime Comparison: Heuristics', fontsize=12, fontweight='bold')
            ax1.set_xlabel('Instance')
            ax1.set_ylabel('Time (seconds)')
            ax1.legend(title='Algorithm', loc='upper left')
            ax1.grid(axis='y', alpha=0.3)
        
        # Group 2: Metaheuristics (MultiStart, TabuSearch, Exact)
        metaheuristics = ['MultiStart', 'TabuSearch', 'Exact']
        meta_data = plot_data[plot_data['Algorithm'].isin(metaheuristics)]
        
        if not meta_data.empty:
            pivot2 = meta_data.pivot(index='Dataset', columns='Algorithm', values='Runtime')
            pivot2.plot(kind='bar', ax=ax2, width=0.8)
            ax2.set_title('Runtime Comparison: Metaheuristics & Exact', fontsize=12, fontweight='bold')
            ax2.set_xlabel('Instance')
            ax2.set_ylabel('Time (seconds)')
            ax2.legend(title='Algorithm', loc='upper left')
            ax2.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'runtime_comparison.pdf', bbox_inches='tight')
        plt.savefig(self.output_dir / 'runtime_comparison.png', bbox_inches='tight')
        plt.close()
        
        print(f"Created runtime comparison: {self.output_dir / 'runtime_comparison.pdf'}")
    
    def plot_solution_quality_vs_size(self):
        """Plot objective value vs instance size"""
        if self.data is None:
            self.parse_results()
        
        # Create size ordering
        size_order = ['test_tiny', 'S1', 'S2', 'M1', 'M2', 'L1', 'L2', 'XL1', 'XXL1']
        plot_data = self.data[self.data['Dataset'].isin(size_order)].copy()
        plot_data['Dataset'] = pd.Categorical(plot_data['Dataset'], categories=size_order, ordered=True)
        plot_data = plot_data.sort_values('Dataset')
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        for alg in plot_data['Algorithm'].unique():
            alg_data = plot_data[plot_data['Algorithm'] == alg]
            if not alg_data.empty and alg_data['Objective'].notna().any():
                ax.plot(alg_data['Dataset'], alg_data['Objective'], 
                       marker='o', label=alg, linewidth=2, markersize=6)
        
        ax.set_title('Solution Quality Across Instance Sizes', fontsize=14, fontweight='bold')
        ax.set_xlabel('Instance', fontsize=12)
        ax.set_ylabel('Objective Value (Demand Covered)', fontsize=12)
        ax.legend(title='Algorithm', loc='upper left', framealpha=0.9)
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        plt.savefig(self.output_dir / 'solution_quality_vs_size.pdf', bbox_inches='tight')
        plt.savefig(self.output_dir / 'solution_quality_vs_size.png', bbox_inches='tight')
        plt.close()
        
        print(f"Created solution quality chart: {self.output_dir / 'solution_quality_vs_size.pdf'}")
    
    def plot_runtime_vs_size(self):
        """Plot runtime vs instance size (log scale)"""
        if self.data is None:
            self.parse_results()
        
        size_order = ['test_tiny', 'S1', 'S2', 'M1', 'M2', 'L1', 'L2', 'XL1', 'XXL1']
        plot_data = self.data[self.data['Dataset'].isin(size_order)].copy()
        plot_data['Dataset'] = pd.Categorical(plot_data['Dataset'], categories=size_order, ordered=True)
        plot_data = plot_data.sort_values('Dataset')
        plot_data = plot_data[plot_data['Runtime'].notna()]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        for alg in plot_data['Algorithm'].unique():
            alg_data = plot_data[plot_data['Algorithm'] == alg]
            if not alg_data.empty:
                ax.plot(alg_data['Dataset'], alg_data['Runtime'], 
                       marker='s', label=alg, linewidth=2, markersize=6)
        
        ax.set_yscale('log')
        ax.set_title('Runtime Scalability Analysis', fontsize=14, fontweight='bold')
        ax.set_xlabel('Instance', fontsize=12)
        ax.set_ylabel('Runtime (seconds, log scale)', fontsize=12)
        ax.legend(title='Algorithm', loc='upper left', framealpha=0.9)
        ax.grid(True, alpha=0.3, which='both')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        plt.savefig(self.output_dir / 'runtime_vs_size.pdf', bbox_inches='tight')
        plt.savefig(self.output_dir / 'runtime_vs_size.png', bbox_inches='tight')
        plt.close()
        
        print(f"Created runtime scalability chart: {self.output_dir / 'runtime_vs_size.pdf'}")
    
    def create_instance_characteristics_table(self):
        """Create instance characteristics table"""
        # Get unique instances
        instances = self.data.groupby('Dataset').first()[['Facilities', 'Customers']].reset_index()
        instances = instances.sort_values('Facilities')
        
        # Save as CSV
        instances.to_csv(self.output_dir / 'instance_characteristics.csv', index=False)
        
        # Create LaTeX table
        with open(self.output_dir / 'instance_characteristics.tex', 'w') as f:
            f.write('\\begin{table}[htbp]\n')
            f.write('\\centering\n')
            f.write('\\caption{Instance Characteristics}\n')
            f.write('\\label{tab:instances}\n')
            f.write('\\begin{tabular}{lrr}\n')
            f.write('\\toprule\n')
            f.write('Instance & Facilities & Customers \\\\\n')
            f.write('\\midrule\n')
            
            for _, row in instances.iterrows():
                if pd.notna(row['Facilities']):
                    f.write(f"{row['Dataset']} & {int(row['Facilities'])} & {int(row['Customers'])} \\\\\n")
            
            f.write('\\bottomrule\n')
            f.write('\\end{tabular}\n')
            f.write('\\end{table}\n')
        
        print(f"Created instance characteristics table: {self.output_dir / 'instance_characteristics.tex'}")
    
    def generate_all(self):
        """Generate all visualizations and tables"""
        print("="*60)
        print("MCLP Benchmark Visualization Generator")
        print("="*60)
        
        print("\n1. Parsing results...")
        self.parse_results()
        print(f"   Found {len(self.data)} result entries")
        
        print("\n2. Calculating performance gaps...")
        self.calculate_gaps()
        
        print("\n3. Creating performance comparison table...")
        self.create_performance_table()
        
        print("\n4. Creating instance characteristics table...")
        self.create_instance_characteristics_table()
        
        print("\n5. Generating runtime comparison charts...")
        self.plot_runtime_comparison()
        
        print("\n6. Generating solution quality chart...")
        self.plot_solution_quality_vs_size()
        
        print("\n7. Generating runtime scalability chart...")
        self.plot_runtime_vs_size()
        
        print("\n" + "="*60)
        print("All visualizations generated successfully!")
        print(f"Output directory: {self.output_dir.absolute()}")
        print("="*60)
        print("\nGenerated files:")
        for file in sorted(self.output_dir.glob('*')):
            print(f"  - {file.name}")

if __name__ == '__main__':
    visualizer = MCLPVisualizer()
    visualizer.generate_all()
