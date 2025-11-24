# MCLP Visualization Scripts - Quick Start Guide

## Installation

1. **Install required Python packages:**

   ```bash
   pip install pandas matplotlib seaborn numpy
   ```

   Or use the requirements file:

   ```bash
   pip install -r requirements_viz.txt
   ```

## Usage

1. **Generate all visualizations:**

   ```bash
   cd mosel
   python scripts/generate_visualizations.py
   ```

2. **Output:**
   All files will be created in the `figures/` directory:
   - `performance_table.tex` - LaTeX table with GAP% comparison
   - `performance_table.csv` - CSV version for reference
   - `instance_characteristics.tex` - LaTeX table of instance sizes
   - `runtime_comparison.pdf` - Bar charts comparing runtimes
   - `solution_quality_vs_size.pdf` - Line chart of objectives
   - `runtime_vs_size.pdf` - Scalability analysis (log scale)
   - PNG versions of all charts for preview

## What Gets Generated

### Tables (LaTeX format, ready for report):

1. **Performance Table** - Shows objective values and GAP% for each algorithm on each instance
2. **Instance Characteristics** - Lists facilities and customers for each dataset

### Charts (PDF + PNG):

1. **Runtime Comparison** - Two bar charts (heuristics vs metaheuristics)
2. **Solution Quality vs Size** - Line chart showing how algorithms scale
3. **Runtime vs Size** - Log-scale chart showing computational complexity

## Next Steps

After running the script:

1. Check the `figures/` directory for all outputs
2. The `.tex` files can be directly included in your LaTeX report
3. The PDF charts can be embedded using `\includegraphics{}`
4. Review the charts and tables before including in the report

## Troubleshooting

If you get import errors:

- Make sure Python 3.8+ is installed
- Install packages: `pip install pandas matplotlib seaborn numpy`

If charts look wrong:

- Check that `results/` directory contains all benchmark output files
- Verify file naming: `Dataset_Algorithm.txt` format
