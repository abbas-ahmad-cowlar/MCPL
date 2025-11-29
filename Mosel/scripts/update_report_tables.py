#!/usr/bin/env python3
"""
Update SCIENTIFIC_REPORT.tex with latest results from generated tables.
This script reads the generated performance_table.tex and runtime data,
then updates the corresponding tables in SCIENTIFIC_REPORT.tex.
"""

import re
import pandas as pd
from pathlib import Path
from typing import Dict, Tuple, List


class ReportTableUpdater:
    def __init__(self, report_file='SCIENTIFIC_REPORT.tex', 
                 performance_table='figures/performance_table.tex',
                 results_dir='results_complete'):
        self.report_file = Path(report_file)
        self.performance_table = Path(performance_table)
        self.results_dir = Path(results_dir)
        self.report_content = None
        self.performance_data = None
        self.runtime_data = None
        
    def load_performance_table(self):
        """Load the generated performance table"""
        if not self.performance_table.exists():
            raise FileNotFoundError(f"Performance table not found: {self.performance_table}")
        
        # Read the LaTeX table
        with open(self.performance_table, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract table rows (skip header and footer)
        rows = []
        for line in content.split('\n'):
            if '&' in line and not line.strip().startswith('%') and '\\toprule' not in line and '\\midrule' not in line and '\\bottomrule' not in line:
                # Parse LaTeX table row
                line = line.strip().rstrip('\\')
                if line and not line.startswith('Instance'):
                    rows.append(line)
        
        self.performance_data = rows
        print(f"  Loaded {len(rows)} performance table rows")
        
    def load_runtime_data(self):
        """Load runtime data from result files"""
        import re
        
        runtime_data = {}
        
        for file in self.results_dir.glob('*.txt'):
            if '_error' in file.name or '_ascii' in file.name:
                continue
                
            match = re.match(r'(.+)_(.+)\.txt', file.name)
            if not match:
                continue
                
            dataset, algorithm = match.groups()
            
            # Read file with multiple encodings
            content = None
            for encoding in ['utf-16-le', 'utf-16', 'utf-8', 'utf-8-sig', 'latin-1']:
                try:
                    content = file.read_text(encoding=encoding, errors='ignore')
                    if content and len(content.strip()) > 0:
                        break
                except:
                    continue
            
            if not content:
                continue
            
            # Extract runtime
            runtime = None
            for pattern in [
                r'Runtime:\s+([\d\.]+)',
                r'Solve time:\s+([\d\.]+)',
                r'Total runtime:\s+([\d\.]+)',
            ]:
                m = re.search(pattern, content)
                if m:
                    try:
                        runtime = float(m.group(1))
                        break
                    except:
                        continue
            
            if dataset not in runtime_data:
                runtime_data[dataset] = {}
            runtime_data[dataset][algorithm] = runtime
        
        self.runtime_data = runtime_data
        print(f"  Loaded runtime data for {len(runtime_data)} datasets")
        
    def load_report(self):
        """Load the LaTeX report"""
        if not self.report_file.exists():
            raise FileNotFoundError(f"Report file not found: {self.report_file}")
        
        with open(self.report_file, 'r', encoding='utf-8') as f:
            self.report_content = f.read()
        
        print(f"  Loaded report: {len(self.report_content)} characters")
        
    def update_performance_table(self):
        """Update the performance table in the report"""
        if not self.performance_data:
            print("  WARNING: No performance data loaded")
            return False
        
        # Find the performance table section
        pattern = r'(\\begin\{table\}.*?\\caption\{Performance Comparison.*?\\label\{tab:performance\}.*?\\begin\{tabular\}.*?\\toprule.*?\\midrule)(.*?)(\\bottomrule.*?\\end\{tabular\}.*?\\end\{table\})'
        
        match = re.search(pattern, self.report_content, re.DOTALL)
        if not match:
            print("  WARNING: Performance table not found in report")
            return False
        
        # Get the table header
        header = match.group(1)
        footer = match.group(3)
        
        # Build new table rows from performance_table.tex
        new_rows = []
        for row in self.performance_data:
            # Clean up the row
            row = row.strip()
            if row:
                new_rows.append('    ' + row + ' \\\\')
        
        # Reconstruct table
        new_table = header + '\n' + '\n'.join(new_rows) + '\n' + footer
        
        # Replace in report
        self.report_content = self.report_content[:match.start()] + new_table + self.report_content[match.end():]
        
        print("  Updated performance table")
        return True
        
    def update_runtime_table(self):
        """Update the runtime table in the report"""
        if not self.runtime_data:
            print("  WARNING: No runtime data loaded")
            return False
        
        # Algorithm order in the table
        alg_order = ['Exact', 'Greedy', 'ClosestNeighbor', 'LocalSearch', 'MultiStart', 'TabuSearch']
        alg_short = ['Exact', 'Greedy', 'Closest', 'Local', 'Multi', 'Tabu']
        
        # Dataset order
        dataset_order = ['S1', 'S2', 'M1', 'M2', 'L1', 'L2', 'XL1', 'XXL1']
        
        # Find the runtime table
        pattern = r'(\\begin\{table\}.*?\\caption\{Runtime Comparison.*?\\label\{tab:runtime\}.*?\\begin\{tabular\}.*?\\toprule.*?\\midrule)(.*?)(\\bottomrule.*?\\end\{tabular\}.*?\\end\{table\})'
        
        match = re.search(pattern, self.report_content, re.DOTALL)
        if not match:
            print("  WARNING: Runtime table not found in report")
            return False
        
        # Build new table rows
        new_rows = []
        for dataset in dataset_order:
            if dataset not in self.runtime_data:
                continue
                
            row_parts = [dataset]
            for alg in alg_order:
                runtime = self.runtime_data[dataset].get(alg)
                if runtime is None:
                    row_parts.append('---')
                elif runtime < 0.01:
                    row_parts.append('<0.01')
                else:
                    row_parts.append(f'{runtime:.2f}')
            
            new_rows.append('    ' + ' & '.join(row_parts) + ' \\\\')
        
        # Reconstruct table
        header = match.group(1)
        footer = match.group(3)
        new_table = header + '\n' + '\n'.join(new_rows) + '\n' + footer
        
        # Replace in report
        self.report_content = self.report_content[:match.start()] + new_table + self.report_content[match.end():]
        
        print("  Updated runtime table")
        return True
        
    def update_best_known_table(self):
        """Update the best known solutions table"""
        if not self.performance_data or not self.runtime_data:
            print("  WARNING: Missing data for best known table")
            return False
        
        # Parse best solutions from performance data
        # This is more complex - we need to find the best objective for each dataset
        # For now, we'll use a simpler approach: read from the performance table
        
        # Find the best known table
        pattern = r'(\\begin\{table\}.*?\\caption\{Best Known Solutions.*?\\label\{tab:best-known\}.*?\\begin\{tabular\}.*?\\toprule.*?\\midrule)(.*?)(\\bottomrule.*?\\end\{tabular\}.*?\\end\{table\})'
        
        match = re.search(pattern, self.report_content, re.DOTALL)
        if not match:
            print("  WARNING: Best known table not found (skipping)")
            return False
        
        # For now, we'll leave this table as-is since it requires more complex logic
        # to determine which algorithm found the best solution
        print("  Best known table left unchanged (requires manual review)")
        return True
        
    def save_report(self):
        """Save the updated report"""
        from datetime import datetime
        
        # Create archive directory for backups
        archive_dir = Path('archive/report_backups')
        archive_dir.mkdir(parents=True, exist_ok=True)
        
        # Read current report before updating
        current_content = Path(self.report_file).read_text(encoding='utf-8')
        
        # Create timestamped backup in archive
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        archive_backup = archive_dir / f"SCIENTIFIC_REPORT_{timestamp}.tex"
        with open(archive_backup, 'w', encoding='utf-8') as f:
            f.write(current_content)
        print(f"  Archived previous report: archive/report_backups/SCIENTIFIC_REPORT_{timestamp}.tex")
        
        # Also create immediate backup (for quick recovery)
        backup_file = self.report_file.with_suffix('.tex.backup')
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(current_content)
        print(f"  Created immediate backup: {backup_file.name}")
        
        # Save updated report
        with open(self.report_file, 'w', encoding='utf-8') as f:
            f.write(self.report_content)
        
        print(f"  Updated report saved: {self.report_file}")
        
    def update_all(self):
        """Run all update steps"""
        print("="*60)
        print("Updating SCIENTIFIC_REPORT.tex with latest results")
        print("="*60)
        
        try:
            print("\n1. Loading data...")
            self.load_performance_table()
            self.load_runtime_data()
            self.load_report()
            
            print("\n2. Updating tables...")
            self.update_performance_table()
            self.update_runtime_table()
            self.update_best_known_table()
            
            print("\n3. Saving updated report...")
            self.save_report()
            
            print("\n" + "="*60)
            print("Report update complete!")
            print("="*60)
            print("\nNote: Review the updated report and update the 'Best Known Solutions'")
            print("      table manually if needed, as it requires interpretation.")
            print("")
            
        except Exception as e:
            print(f"\nERROR: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        return True


if __name__ == '__main__':
    updater = ReportTableUpdater()
    updater.update_all()

