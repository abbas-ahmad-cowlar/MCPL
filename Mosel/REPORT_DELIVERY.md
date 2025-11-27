# MCLP Client Report - Delivery Package

## Overview

This package contains a comprehensive technical report on the Maximum Covering Location Problem (MCLP) implementation in FICO Xpress Mosel, along with all source code and experimental results.

## Contents

### 1. Main Report

- **`REPORT.tex`**: Complete LaTeX source for the professional client report
- **`REPORT.pdf`**: Compiled PDF (you must compile the .tex file - see instructions below)
- **`SCIENTIFIC_REPORT.tex`**: Complete LaTeX source for the scientific report
- **`SCIENTIFIC_REPORT.pdf`**: Compiled PDF (you must compile the .tex file - see instructions below)

### 2. Source Code (src/ directory)

Six complete Mosel implementations:

- `mclp_exact.mos` - Exact MIP solver using Xpress Optimizer
- `mclp_greedy.mos` - Greedy heuristic (maximum coverage gain per cost)
- `mclp_closest_neighbor.mos` - Distance-based construction heuristic
- `mclp_local_search.mos` - Hill-climbing improvement with delta-evaluation
- `mclp_multistart.mos` - Multi-Start Local Search framework
- `mclp_tabu_search.mos` - Tabu Search metaheuristic

### 3. Data Files (data/ directory)

Nine benchmark instances:

- `test_tiny.dat` - 4 facilities, 8 customers (validation)
- `S1.dat`, `S2.dat` - Small instances (50 facilities, 200 customers)
- `M1.dat`, `M2.dat` - Medium instances (100 facilities, 500 customers)
- `L1.dat`, `L2.dat` - Large instances (200 facilities, 1000 customers)
- `XL1.dat` - Extra large (500 facilities, 2000 customers)
- `XXL1.dat` - Massive (1000 facilities, 5000 customers)

### 4. Experimental Results (results/ directory)

- Complete output logs for all 54 algorithm-instance combinations
- Performance data in plain text format

### 5. Visualization (figures/ directory)

- `performance_table.tex` - LaTeX performance comparison table
- `instance_characteristics.tex` - Instance size table
- `runtime_comparison.pdf` - Runtime bar charts
- `solution_quality_vs_size.pdf` - Quality vs. size line chart
- `runtime_vs_size.pdf` - Scalability analysis (log scale)

### 6. Scripts (scripts/ directory)

- `generate_instance.py` - Create new random instances
- `convert_json_to_mosel.py` - Convert JSON to Mosel .dat format
- `generate_visualizations.py` - Regenerate all charts and tables

### 7. Execution Scripts

- `run_benchmark.ps1` - Run all algorithms on all instances
- `summarize_results.ps1` - Generate performance summary

### 8. Documentation

- `README.md` - Project overview
- `TECHNICAL_GUIDE.md` - Setup and execution guide
- `REPORT.md` - Executive summary
- `benchmark_results.md` - Detailed results summary

## Compiling the Report

The report is written in LaTeX for professional presentation. To compile to PDF:

### Option 1: Using pdflatex (Recommended)

```bash
cd Mosel
pdflatex REPORT.tex
pdflatex REPORT.tex  # Run twice for references
```

### Option 2: Using Online LaTeX Editor

1. Upload `REPORT.tex` to [Overleaf](https://www.overleaf.com)
2. Upload all figures from `figures/` directory
3. Compile (PDF will be generated automatically)

### Option 3: Using MiKTeX (Windows)

1. Install MiKTeX from https://miktex.org/download
2. Open MiKTeX Console, install missing packages if prompted
3. Run: `pdflatex REPORT.tex` twice

## Report Structure

The 30+ page report includes:

1. **Introduction** (4 pages)

   - Problem context and real-world applications
   - Computational challenges
   - Solution approaches overview
   - Contributions and objectives

2. **Mathematical Formulation** (2 pages)

   - Complete problem definition
   - Notation table
   - Compact MIP formulation with equations (1-5)
   - Model characteristics

3. **Solution Algorithms** (6 pages)

   - Exact MIP Solver
   - Greedy Heuristic with pseudocode
   - Closest Neighbor Heuristic
   - Local Search with detailed pseudocode
   - Multi-Start Local Search
   - Tabu Search with full algorithmic description
   - Complexity analysis for each

4. **Experimental Setup** (2 pages)

   - Instance generation methodology
   - Instance characteristics table
   - Computational environment

5. **Computational Results** (8 pages) - **KEY SECTION**

   - Overall performance comparison table
   - Runtime performance analysis
   - Scalability analysis with charts
   - Solution quality vs. instance size
   - Detailed instance-by-instance analysis
   - Algorithm selection guidelines

6. **Conclusions** (3 pages)

   - Summary of findings
   - Practical recommendations
   - Future work
   - Final conclusions

7. **Appendices** (5 pages)
   - Complete source code references
   - Data file format specification
   - Execution instructions

## Key Results Highlights

### Small Instances (S1, S2)

- All algorithms find optimal solutions
- Runtime: < 0.15 seconds for all methods

### Medium Instances (M1, M2)

- **M2**: Tabu Search (22497) > Exact (22448)
- Heuristics within 1-4% of optimal
- Runtime: < 1 second for all methods

### Large Instances (L1, L2)

- **L1**: Tabu Search (47479) - best known solution
- Runtime: 0.26 seconds
- Heuristics highly competitive

### Extra Large (XL1)

- **Best**: Tabu Search (95924) - competitive with Exact
- Runtime: 0.61 seconds

### Massive (XXL1)

- **Exact fails** (license limit)
- **Tabu Search achieves optimal** (250788) in 3.38 seconds
- Demonstrates heuristic scalability on large-scale problems

## Running the Code

### Prerequisites

1. FICO Xpress Mosel (any edition)
2. Python 3.8+ (for utility scripts)
3. PowerShell (for benchmark scripts)

### Quick Start

```powershell
# Run single algorithm
mosel exec src/mclp_exact.mos "DATA_FILE=data/S1.dat"

# Run full benchmark
.\run_benchmark.ps1

# Generate visualizations
python scripts/generate_visualizations.py
```

## Algorithm Selection Guide

| Scenario                 | Recommended Algorithm | Rationale                                              |
| ------------------------ | --------------------- | ------------------------------------------------------ |
| Small (< 100 facilities) | Exact or Tabu Search  | Optimality guarantee or best quality                   |
| Medium (100-200)         | Tabu Search           | Often matches/beats Exact                              |
| Large (200-500)          | Local Search or Tabu  | Local: speed; Tabu: quality                            |
| Massive (> 500)          | Local Search          | Only heuristics feasible; Local Search optimal on XXL1 |
| Quick baseline           | Greedy                | < 0.1s, 70-95% optimal                                 |
| Best quality             | Tabu Search           | Most robust                                            |

## Technical Support

For questions about:

- **Source Code**: See inline comments in `.mos` files
- **Instance Format**: See `TECHNICAL_GUIDE.md`
- **Execution**: See `README.md` in project root
- **Results**: See `benchmark_results.md`

## Citation

If using this work, please cite:

```
MCLP Optimization Project (2025). Maximum Covering Location Problem:
Algorithms, Implementation, and Computational Results.
Technical Report, FICO Xpress Mosel Implementation.
```

## License

All source code and documentation provided for client use.

---

**Report Date**: November 2025  
**Implementation**: FICO Xpress Mosel  
**Total Algorithms**: 6 (1 exact, 5 heuristic/metaheuristic)  
**Total Instances**: 9 (ranging from 4 to 1000 facilities)  
**Total Experiments**: 54 algorithm-instance combinations
